/**
 * Telegram webhook receiver for the Daily Economic Briefing.
 *
 * WHY THIS EXISTS
 * Telegram gives a bot two ways to hear anything: getUpdates polling, or a
 * webhook. Polling has a floor — GitHub's shortest cron is five minutes, and it
 * runs late — so "instant" is not reachable that way. A webhook is pushed within
 * milliseconds, and this is the smallest thing that can receive one.
 *
 * WHAT IT DOES NOT DO
 * It is deliberately not the source of truth. subscribers.json in the repository
 * decides who receives the briefing, and only a GitHub workflow writes it. This
 * Worker replies to people at once and appends the decision to a durable queue;
 * subscriptions.yml drains that queue and commits. So the Worker holds no
 * GitHub credential, and losing it loses nothing but latency.
 *
 * AT-LEAST-ONCE, NOT AT-MOST-ONCE
 * Queue items are handed out on GET /queue and only deleted on POST /ack, after
 * the workflow has committed. A drain that dies mid-way replays, so applying an
 * item must be idempotent — see apply_queue() in scripts/subscribers.py. The
 * alternative, deleting on read, would silently drop an opt-out, which is the
 * one outcome worth engineering against.
 *
 * Endpoints:
 *   POST /telegram   Telegram's webhook. Verified by the secret header.
 *   GET  /queue      The workflow reads pending items.      ?secret=DRAIN_SECRET
 *   POST /ack        The workflow confirms it committed them. ?secret=DRAIN_SECRET
 *   GET  /health     Liveness, with queue depth.
 *
 * Bindings (see wrangler.toml): QUEUE (KV), and the secrets BOT_TOKEN,
 * OWNER_CHAT_ID, WEBHOOK_SECRET, DRAIN_SECRET, LIST_URL.
 */

// Kept identical to MSG in scripts/subscribers.py. Two copies is a real cost,
// but the alternative is the Worker fetching its own wording over the network
// before it can answer, which defeats the point of being instant.
const MSG = {
  pending: "Your request for subscription is pending.",
  approved: "Your request for subscription has been approved.",
  stopped:
    "We have received your unsubscribe request. Please give us time to process it.",
  "already-subscribed":
    "You are already subscribed. Send /stop to unsubscribe.",
  "owner-stop":
    "You are the owner of this briefing. Your own copy is configured in the " +
    "repository, not by this bot, so it will keep arriving.",
  denied: "Your subscription request was not approved.",
  paid:
    "Payment received — thank you. Your subscription runs for a year from " +
    "today, and the next briefing is on its way.",
  cancelled:
    "Your subscription will not renew. You keep receiving the briefing until " +
    "the year you have paid for runs out.",


  // The paywall. Templates; {n} and {link} are filled at send time, and
  // the same raw strings live in scripts/subscribers.py — test_subscribers.py
  // compares them so the two copies cannot drift.
  trial:
    "You are on a free trial — the next {n} editions are yours, " +
    "starting with the next one. After that it is $4.99 for a year: " +
    "{link}",
  "signed-up":
    "You are already on the list. A year of the briefing is $4.99 " +
    "whenever you want it: {link}",
  pay:
    "Your free editions are used up. A year of the briefing is " +
    "$4.99: {link}",
  lapsed:
    "Your subscription has ended, so the briefing has stopped. A " +
    "year is $4.99 whenever you want it back: {link}",
  reminder:
    "Your subscription renews in {n} day(s) at $4.99. It renews " +
    "automatically — nothing to do. Send /stop if you would rather " +
    "it did not.",
  "comp-applied": "Code accepted — you are subscribed for a year. Thank you.",
  "comp-bad":
    "That code is not valid. If you think it should be, reply and " +
    "the owner will take a look.",
};

const START = new Set(["/start", "/subscribe"]);
const STOP = new Set(["/stop", "/unsubscribe"]);

// Bumped by hand whenever this file changes in a way worth confirming is live.
// The Worker runs from code pasted into the dashboard, not from this repository,
// so "did my paste actually deploy?" is otherwise unanswerable — and a stale
// deploy looks exactly like a configuration fault.
const VERSION = "2026-11-05a";

// The subscriber list lives here, in KV, not in the repository. Chat IDs are
// personal data and the repository is public; KV is private and already present
// for the queue, so it costs nothing extra and needs no new credential.
//
// Deliberately not under the `q:` prefix, so listing the queue never picks it up.
const LIST_KEY = "list";

/** The chat a Stripe customer belongs to, learned at checkout. */
async function chatForCustomer(env, customerId) {
  if (!customerId) return null;
  const { list } = await storedList(env);
  for (const key of ["approved", "pending", "unsubscribed"]) {
    for (const e of (list && list[key]) || []) {
      if (e.stripe_customer_id === customerId) return e.chat_id;
    }
  }
  return null;
}

/**
 * Turn a verified Stripe event into a queued decision.
 *
 * Queued, not applied. Every other decision this Worker makes goes through the
 * same queue, drained and committed by subscriptions.yml, and payments have no
 * business being the one exception: the queue is what makes the whole thing
 * at-least-once and replay-safe, and apply_queue() is where the list is
 * actually written.
 *
 * The queue key is the Stripe event id, so Stripe's own retries collapse onto
 * one entry rather than granting a year each time.
 *
 * WHICH EVENTS GRANT, AND WHY ONLY THOSE
 *
 * A first payment raises BOTH checkout.session.completed and invoice.paid. If
 * both granted, a new subscriber would get two years for one payment. So the
 * first payment is granted from the checkout session, which is also the only
 * event carrying client_reference_id and therefore the only place the chat id
 * can be learned; and invoice.paid grants only when its billing_reason says
 * subscription_cycle, which is a renewal.
 */
async function onStripe(env, event) {
  const obj = (event && event.data && event.data.object) || {};
  const type = event && event.type;
  const evt = event && event.id;
  const key = `z-stripe-${evt}`;   // sorts after the numeric Telegram ids

  if (type === "checkout.session.completed") {
    const chat = Number(obj.client_reference_id);
    if (!Number.isFinite(chat) || !chat) {
      // Nothing ties this payment to a chat. Refunding or linking it by hand
      // is the owner's call, so say so loudly rather than dropping it.
      console.warn("checkout.session.completed with no usable client_reference_id;",
                   "payment cannot be linked to a chat:", evt);
      await notifyOwner(env,
        "A Stripe payment arrived that is not linked to any Telegram chat. " +
        "It needs linking or refunding by hand. Stripe event: " + evt);
      return { handled: false, why: "no client_reference_id" };
    }
    await enqueueKeyed(env, {
      verb: "paid", chat_id: chat, event_id: evt, years: 1,
      stripe_customer_id: obj.customer || null,
      stripe_subscription_id: obj.subscription || null,
    }, key);
    // Answer now rather than at the next drain. They have just paid; a
    // five-minute silence is exactly when someone wonders if it worked.
    await tg(env, "sendMessage", { chat_id: chat, text: MSG.paid });
    return { handled: true };
  }

  if (type === "invoice.paid") {
    if (obj.billing_reason && obj.billing_reason !== "subscription_cycle") {
      // The first invoice of a new subscription. checkout.session.completed
      // has it; granting here as well would double it.
      return { handled: false, why: `ignored billing_reason ${obj.billing_reason}` };
    }
    const chat = await chatForCustomer(env, obj.customer);
    if (!chat) {
      console.warn("invoice.paid for a customer not on the list:", evt);
      return { handled: false, why: "customer not on the list" };
    }
    await enqueueKeyed(env, {
      verb: "paid", chat_id: chat, event_id: evt, years: 1,
      stripe_customer_id: obj.customer || null,
    }, key);
    return { handled: true };
  }

  if (type === "customer.subscription.deleted") {
    const chat = await chatForCustomer(env, obj.customer);
    if (!chat) return { handled: false, why: "customer not on the list" };
    // Deliberately does NOT revoke. They paid for a year; cancelling stops the
    // renewal, it does not buy back the months already paid for.
    await enqueueKeyed(env, { verb: "cancelled", chat_id: chat, event_id: evt }, key);
    await tg(env, "sendMessage", { chat_id: chat, text: MSG.cancelled });
    return { handled: true };
  }

  if (type === "invoice.payment_failed") {
    // Stripe retries on its own schedule; the grace window exists so this is
    // not felt as being cut off. Nothing to do but leave a trace.
    console.warn("invoice.payment_failed:", evt);
    return { handled: false, why: "payment failed, left to Stripe's retries" };
  }

  return { handled: false, why: `no handler for ${type}` };
}

// --- Stripe webhook verification -------------------------------------------
//
// Stripe signs every delivery. The header looks like
//
//     t=1614556800,v1=<hex hmac>,v1=<another>,v0=<legacy>
//
// and the signed payload is `${t}.${raw body}` — the RAW body, byte for byte.
// Parsing the JSON first and re-serialising it changes the bytes and every
// signature then fails, which is the classic way to get this wrong.
//
// Without this check the endpoint is an open door: anyone who learns the URL
// could POST a fabricated "payment succeeded" and subscribe themselves free.
const STRIPE_TOLERANCE_S = 300;

function timingSafeEqual(a, b) {
  // Compares in constant time. A plain === leaks, through its own early exit,
  // how much of a guessed signature was correct.
  if (typeof a !== "string" || typeof b !== "string") return false;
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

async function hmacHex(secret, payload) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(payload));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

/** {ok} or {ok:false, why} — `why` is for the Worker log, never the response. */
async function stripeSigned(env, raw, header, nowMs) {
  if (!env.STRIPE_WEBHOOK_SECRET) {
    return { ok: false, why: "STRIPE_WEBHOOK_SECRET is not set on this Worker" };
  }
  if (!header) {
    return { ok: false, why: "no Stripe-Signature header — this did not come from Stripe" };
  }
  const parts = {};
  for (const kv of String(header).split(",")) {
    const i = kv.indexOf("=");
    if (i < 0) continue;
    const k = kv.slice(0, i).trim();
    (parts[k] = parts[k] || []).push(kv.slice(i + 1).trim());
  }
  const t = Number((parts.t || [])[0]);
  if (!Number.isFinite(t)) {
    return { ok: false, why: "the signature header carried no timestamp" };
  }
  // Replay protection. Without it, one captured delivery could be replayed
  // forever; Stripe's own libraries default to the same five minutes.
  const age = Math.abs(nowMs / 1000 - t);
  if (age > STRIPE_TOLERANCE_S) {
    return {
      ok: false,
      why: `signature is ${Math.round(age)}s old, over the ${STRIPE_TOLERANCE_S}s ` +
           "tolerance — a replay, or this Worker's clock is wrong",
    };
  }
  const expected = await hmacHex(env.STRIPE_WEBHOOK_SECRET, `${t}.${raw}`);
  const offered = parts.v1 || [];
  if (!offered.some((v) => timingSafeEqual(v, expected))) {
    return {
      ok: false,
      why: "no v1 signature matched — STRIPE_WEBHOOK_SECRET here and the " +
           "signing secret of the endpoint in Stripe differ, or the body was altered",
    };
  }
  return { ok: true };
}

async function tg(env, method, body) {
  const r = await fetch(`https://api.telegram.org/bot${env.BOT_TOKEN}/${method}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
  return r.json().catch(() => ({ ok: false, description: "unparseable" }));
}

const say = (env, chat_id, text, extra = {}) =>
  tg(env, "sendMessage", { chat_id, text, ...extra });

/**
 * Append to the queue, keyed so that a lexical sort is true chronological order.
 *
 * The key is Telegram's update_id, which increases monotonically per bot, plus a
 * counter for the case where one update produces several items (`/approve 1 2`).
 * An earlier version used Date.now() and a random suffix: two decisions landing
 * in the same millisecond then sorted RANDOMLY, and since the last decision in a
 * batch wins, a /stop could be applied before the /start it followed — leaving
 * somebody subscribed after they had asked to leave.
 *
 * Deriving the key from update_id also makes enqueueing idempotent: Telegram
 * retrying a delivery rewrites the same key instead of queueing a duplicate.
 */
/** Queue under a caller-chosen key, so a retried delivery collapses onto one. */
async function enqueueKeyed(env, item, key) {
  const id = `q:${key}`;
  await env.QUEUE.put(id, JSON.stringify({ id: key, ...item }));
  return key;
}

async function notifyOwner(env, text) {
  if (!env.OWNER_CHAT_ID) return;
  try {
    await tg(env, "sendMessage", { chat_id: env.OWNER_CHAT_ID, text });
  } catch (e) {
    console.error("could not notify the owner", e && e.stack);
  }
}

async function enqueue(env, item, seq, n = 0) {
  const uid = Number.isFinite(seq) ? seq : Date.now();
  const id = `${String(uid).padStart(16, "0")}-${String(n).padStart(4, "0")}`;
  await env.QUEUE.put(`q:${id}`, JSON.stringify({ id, ...item }));
  return id;
}

/**
 * The current list, from KV. Reports where it came from, because "did my
 * migration land?" and "why is it answering as though nobody is subscribed?"
 * are the same question asked from two directions, and only the source answers
 * both. Failure is not fatal: the Worker answers without list context rather
 * than going silent.
 */
async function storedList(env) {
  // KV first — the authoritative home. LIST_URL is only a migration fallback,
  // for the window between deploying this code and seeding KV; it also only
  // works while the repository is public, which is the whole thing being fixed.
  try {
    const raw = await env.QUEUE.get(LIST_KEY);
    if (raw) return { source: "kv", list: JSON.parse(raw) };
  } catch {
    /* fall through to the repository copy */
  }
  if (env.LIST_URL) {
    try {
      const r = await fetch(env.LIST_URL, { cf: { cacheTtl: 30 } });
      if (r.ok) return { source: "git", list: await r.json() };
    } catch {
      /* nothing readable */
    }
  }
  return { source: "empty", list: null };
}

async function currentList(env) {
  const { list } = await storedList(env);
  if (!list) return null;
  return {
    approved: new Set((list.approved || []).map((e) => e.chat_id)),
    pending: (list.pending || []).map((e) => e.chat_id),
  };
}

const isOwner = (env, id) =>
  env.OWNER_CHAT_ID && String(id) === String(env.OWNER_CHAT_ID);

/** Approve/Deny buttons, so the owner never has to type a chat id. */
const decisionKeyboard = (chat_id) => ({
  reply_markup: {
    inline_keyboard: [[
      { text: "✅ Approve", callback_data: `a:${chat_id}` },
      { text: "🚫 Deny", callback_data: `d:${chat_id}` },
    ]],
  },
});

// --- Stripe Checkout Session ------------------------------------------------
//
// Configured in Checkout Studio. Gated on STRIPE_SECRET_KEY: without it the
// route 404s and nothing changes, which is how every other part of this
// paywall is staged.
//
// WHY THIS SITS BESIDE THE PAYMENT LINK RATHER THAN REPLACING IT
//
// The paywall already works through a dashboard Payment Link with
// ?client_reference_id=<chat id>, chosen so that no key capable of moving
// money lives in this Worker. Creating a Checkout Session needs the secret
// key here, so this is a deliberate change of posture, not a refactor — and
// both paths raise the same checkout.session.completed event, which /stripe
// already handles. Nothing downstream needed changing.
//
// There is no Stripe SDK in this project: the Worker is a single file pasted
// into the dashboard with no build step and no imports, so this calls the
// REST API with fetch and form encoding, as it already does for Telegram.
// That is also why ui_mode defaults to hosted_page — there is no SDK version
// to read. See STRIPE_INTEGRATION_TODO.md.
function checkoutForm(env, chatId) {
  const f = new URLSearchParams();

  // fixed_by_ui — set in Checkout Studio, used exactly as given.
  f.set("ui_mode", "hosted_page");
  f.set("billing_address_collection", "auto");
  f.set("phone_number_collection[enabled]", "false");
  f.set("automatic_tax[enabled]", "false");
  f.set("allow_promotion_codes", "true");
  f.set("submit_type", "auto");
  f.set("saved_payment_method_options[payment_method_save]", "enabled");
  f.set("integration_identifier", "hosted_web_0001");
  f.set("origin_context", "web");

  // The briefing is sold as an annual subscription, so mode is subscription
  // and payment_method_collection applies (it is only valid for that mode).
  f.set("mode", "subscription");
  f.set("payment_method_collection", "always");

  // sample_only — placeholders, listed in STRIPE_INTEGRATION_TODO.md.
  f.set("success_url", (env.CHECKOUT_SUCCESS_URL || "https://example.com/success") +
    "?session_id={CHECKOUT_SESSION_ID}");
  f.set("cancel_url", env.CHECKOUT_CANCEL_URL || "https://example.com/cancel");
  f.set("line_items[0][price]", env.STRIPE_PRICE_ID || "price_...");
  f.set("line_items[0][quantity]", "1");

  // Not from Checkout Studio, and not optional here: /stripe matches a
  // payment to a Telegram chat by this field alone. Without it a completed
  // checkout cannot be attributed to anybody.
  if (chatId) f.set("client_reference_id", String(chatId));
  return f;
}

async function createCheckoutSession(env, chatId) {
  const r = await fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: {
      authorization: `Bearer ${env.STRIPE_SECRET_KEY}`,
      "content-type": "application/x-www-form-urlencoded",
    },
    body: checkoutForm(env, chatId).toString(),
  });
  const body = await r.json().catch(() => ({}));
  if (!r.ok) {
    // Stripe's own message is the useful part; surface it to the log rather
    // than to the caller, since it can name configuration.
    const why = (body.error && body.error.message) || `HTTP ${r.status}`;
    console.error("checkout session refused:", why);
    return { ok: false, why };
  }
  return { ok: true, url: body.url, id: body.id };
}

// --- the paywall ------------------------------------------------------------
//
// PAY_URL is the switch. Until it is set, /start behaves exactly as it did
// before the paywall existed: the chat lands in pending and waits on the
// owner. That is deliberate — this code can ship and sit inert until Stripe
// is actually ready, rather than being held back in a branch.
const TRIAL_EDITIONS = 3;

function paywallOn(env) {
  return Boolean(env.PAY_URL);
}

/** The Payment Link with this chat attached, so the webhook can match it up. */
function payLink(env, chatId) {
  const base = String(env.PAY_URL || "");
  if (!base) return "";
  return base + (base.includes("?") ? "&" : "?") +
    "client_reference_id=" + encodeURIComponent(String(chatId));
}

function fill(key, vars) {
  let text = MSG[key];
  for (const [k, v] of Object.entries(vars || {})) {
    text = text.split("{" + k + "}").join(String(v));
  }
  return text;
}

/**
 * Free comp codes, from the COMP_CODES variable: "FRIENDS:1, PRESS:2".
 *
 * Deliberately has no redemption limits and no expiry. Those need race-safe
 * counting, which KV cannot give without transactions, and a limit that
 * quietly miscounts is worse than no limit at all. Discounts and anything
 * needing a cap go through Stripe's own promotion codes, which already solve
 * this properly; only 100%-free comps come through the bot.
 */
function compYears(env, code) {
  const want = String(code || "").trim().toUpperCase();
  if (!want) return 0;
  for (const pair of String(env.COMP_CODES || "").split(",")) {
    const [name, years] = pair.split(":").map((x) => (x || "").trim());
    if (name && name.toUpperCase() === want) {
      const n = parseInt(years || "1", 10);
      return Number.isFinite(n) && n > 0 ? n : 1;
    }
  }
  return 0;
}

/** What to say to a /start, and what to queue, once the paywall is on. */
async function paywallStart(env, id, chatType, seq) {
  const { list } = await storedList(env);
  const all = [
    ...((list && list.approved) || []),
    ...((list && list.pending) || []),
    ...((list && list.unsubscribed) || []),
  ];
  const entry = all.find((e) => e.chat_id === id) || null;

  if (entry && entry.paid_until) {
    // Already paying. Nothing to sell them and nothing to queue.
    return void (await say(env, id, MSG["already-subscribed"]));
  }

  if (entry && entry.trial_started) {
    // They have had a trial already. Whether it still has editions left is
    // not knowable here — that is counted out of git on the delivery side —
    // so this says the one thing true either way. The notices sweep is what
    // tells them the moment it actually runs out.
    //
    // Reaching this branch at all is what closes the /stop-then-/start
    // loophole: trial_started follows the chat through an opt-out, so coming
    // back does not look like a new arrival.
    await say(env, id, fill("signed-up", { link: payLink(env, id) }));
    return;
  }

  await say(env, id, fill("trial", { n: TRIAL_EDITIONS, link: payLink(env, id) }));
  await enqueue(env, { verb: "trial", chat_id: id, type: chatType }, seq);
}

async function onMessage(env, msg, seq) {
  const chat = msg.chat || {};
  const id = chat.id;
  const text = (msg.text || "").trim();
  if (id == null || !text.startsWith("/")) return;

  const verb = text.split(/\s+/)[0].split("@")[0].toLowerCase();
  const args = text
    .split(/\s+/)
    .slice(1)
    .map((t) => parseInt(t.replace(/,/g, ""), 10))
    .filter(Number.isFinite);

  // --- the owner's own commands ---------------------------------------------
  if (isOwner(env, id)) {
    if (STOP.has(verb)) return void say(env, id, MSG["owner-stop"]);

    if (verb === "/approve" || verb === "/deny") {
      if (!args.length) {
        return void say(env, id, `Usage: ${verb} <chat id> [<chat id>…]`);
      }
      let n = 0;
      for (const target of args) {
        await decide(env, target, verb === "/approve", id, seq, n++);
      }
      return;
    }

    if (verb === "/pending" || verb === "/status") {
      const list = await currentList(env);
      if (!list) {
        return void say(env, id, "Could not read the subscriber list just now.");
      }
      const body =
        `Approved: ${list.approved.size}. Awaiting approval: ${list.pending.length}.` +
        (verb === "/pending" && list.pending.length
          ? `\nPending: ${list.pending.join(", ")}` +
            `\nReply /approve <id>, or use the buttons on the request.`
          : "");
      return void say(env, id, body);
    }
    // The owner sending /start is treated like anyone else's below.
  }

  // --- everyone else --------------------------------------------------------
  if (verb === "/promo") {
    if (!paywallOn(env)) return;
    const code = text.split(/\s+/)[1] || "";
    const years = compYears(env, code);
    if (!years) return void say(env, id, MSG["comp-bad"]);
    await say(env, id, MSG["comp-applied"]);
    await enqueue(env, {
      verb: "comp", chat_id: id, type: chat.type || "?",
      code: code.trim().toUpperCase(), years,
    }, seq);
    await notifyOwner(env, `Comp code ${code.trim().toUpperCase()} redeemed by chat ${id}.`);
    return;
  }

  if (START.has(verb)) {
    if (paywallOn(env)) {
      await paywallStart(env, id, chat.type || "?", seq);
      if (env.OWNER_CHAT_ID && !isOwner(env, id)) {
        const who = [chat.title, chat.first_name, chat.last_name]
          .filter(Boolean).join(" ");
        const tag = chat.username ? ` (@${chat.username})` : "";
        await say(env, env.OWNER_CHAT_ID,
          `Trial started\n${who || "?"}${tag}\nchat ${id} (${chat.type || "?"})`);
      }
      return;
    }
    const list = await currentList(env);
    if (list && list.approved.has(id)) {
      return void say(env, id, MSG["already-subscribed"]);
    }
    await say(env, id, MSG.pending);
    await enqueue(env, { verb: "start", chat_id: id, type: chat.type || "?" }, seq);
    if (env.OWNER_CHAT_ID && !isOwner(env, id)) {
      const who = [chat.title, chat.first_name, chat.last_name]
        .filter(Boolean)
        .join(" ");
      const tag = chat.username ? ` (@${chat.username})` : "";
      // The name goes to the owner's private chat only. It is never queued and
      // never committed — the repository is public.
      await say(
        env,
        env.OWNER_CHAT_ID,
        `New subscription request\n${who || "?"}${tag}\nchat ${id} (${chat.type || "?"})`,
        decisionKeyboard(id),
      );
    }
    return;
  }

  if (STOP.has(verb)) {
    await say(env, id, MSG.stopped);
    await enqueue(env, { verb: "stop", chat_id: id, type: chat.type || "?" }, seq);
    return;
  }
}

/** Apply a decision: tell the subscriber at once, and queue the list change. */
async function decide(env, target, approved, ownerChat, seq, n = 0) {
  if (isOwner(env, target)) {
    return void say(env, ownerChat, "That is your own chat; nothing to approve.");
  }
  await enqueue(env, { verb: approved ? "approve" : "deny", chat_id: target }, seq, n);
  // Denial is silent to the subscriber by design: "you were refused" helps
  // nobody, and denial is also how obvious spam gets cleared.
  if (approved) await say(env, target, MSG.approved);
  if (ownerChat) {
    await say(env, ownerChat, `${approved ? "Approved" : "Denied"} chat ${target}.`);
  }
}

async function onCallback(env, cq, seq) {
  const from = cq.from || {};
  const data = cq.data || "";
  const m = /^([ad]):(-?\d+)$/.exec(data);

  // Answer first, always, so the button stops spinning within its few seconds.
  if (!isOwner(env, from.id)) {
    await tg(env, "answerCallbackQuery", {
      callback_query_id: cq.id,
      text: "Only the owner can approve subscriptions.",
      show_alert: true,
    });
    return;
  }
  if (!m) {
    await tg(env, "answerCallbackQuery", { callback_query_id: cq.id, text: "Unknown action." });
    return;
  }

  const approve = m[1] === "a";
  const target = parseInt(m[2], 10);
  await tg(env, "answerCallbackQuery", {
    callback_query_id: cq.id,
    text: approve ? "Approved." : "Denied.",
  });

  // Replace the buttons with the outcome, so the message cannot be tapped twice
  // and reads as a record afterwards.
  if (cq.message) {
    await tg(env, "editMessageText", {
      chat_id: cq.message.chat.id,
      message_id: cq.message.message_id,
      text: `${cq.message.text}\n\n— ${approve ? "✅ approved" : "🚫 denied"}`,
    });
  }
  await decide(env, target, approve, null, seq);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const auth = (name) => url.searchParams.get("secret") === env[name];

    if (url.pathname === "/health") {
      // Reports which bindings EXIST, never their values, because the failure
      // this has to explain is invisible from outside: a missing or misnamed
      // secret makes env.X undefined, the header comparison below fails for
      // every request, and Telegram reports a bare "403 Forbidden" that looks
      // identical to a wrong value. Booleans are enough to tell those apart and
      // leak nothing.
      const config = {};
      for (const name of ["BOT_TOKEN", "OWNER_CHAT_ID", "WEBHOOK_SECRET",
                          "DRAIN_SECRET", "LIST_URL", "QUEUE",
                          "STRIPE_WEBHOOK_SECRET", "PAY_URL", "COMP_CODES",
                          "STRIPE_SECRET_KEY", "STRIPE_PRICE_ID"]) {
        config[name] = Boolean(env[name]);
      }
      // STRIPE_WEBHOOK_SECRET is reported but does not count as missing. The
      // paywall is a later arrival than the rest of this Worker, and a health
      // check that reads "not ok" for months before anyone sets up Stripe is a
      // health check people learn to ignore. /stripe refuses clearly on its own
      // when the secret is absent, which is where that failure belongs.
      // PAY_URL is the paywall's switch and COMP_CODES is empty until there
      // are codes, so neither absence is a fault. /health still reports both,
      // because "is the paywall actually on?" is otherwise unanswerable from
      // outside.
      const OPTIONAL = new Set(["STRIPE_WEBHOOK_SECRET", "PAY_URL", "COMP_CODES",
                                "STRIPE_SECRET_KEY", "STRIPE_PRICE_ID"]);
      const missing = Object.entries(config)
        .filter(([k, v]) => !v && !OPTIONAL.has(k)).map(([k]) => k);
      const unconfigured = Object.entries(config)
        .filter(([k, v]) => !v && OPTIONAL.has(k)).map(([k]) => k);

      // A value pasted into a dashboard field very easily carries a trailing
      // newline or space, which is equally invisible and equally fatal.
      const untrimmed = ["BOT_TOKEN", "OWNER_CHAT_ID", "WEBHOOK_SECRET", "DRAIN_SECRET"]
        .filter((n) => typeof env[n] === "string" && env[n] !== env[n].trim());

      let queued = null;
      let queueError = null;
      try {
        queued = (await env.QUEUE.list({ prefix: "q:", limit: 1000 })).keys.length;
      } catch (e) {
        queueError = String((e && e.message) || e);
      }

      // Where the list is read from is the one fact that says whether migration
      // has happened. "git" means KV is still empty and the repository copy is
      // being used — which stops working the moment the repo goes private.
      const { source, list } = await storedList(env);

      return Response.json({
        ok: missing.length === 0 && untrimmed.length === 0 && queueError === null,
        version: VERSION,
        at: new Date().toISOString(),
        queued,
        list: {
          source,
          approved: list ? (list.approved || []).length : null,
          pending: list ? (list.pending || []).length : null,
          unsubscribed: list ? (list.unsubscribed || []).length : null,
        },
        config,
        // Present but not yet set up. Informational, never a failure.
        unconfigured,
        ...(missing.length ? { missing } : {}),
        ...(untrimmed.length
          ? { whitespace: untrimmed, hint: "these have leading or trailing whitespace" }
          : {}),
        ...(queueError ? { queueError } : {}),
      }, {
        // A diagnostic that can be served from a cache is worse than none: it
        // reports a state that may be minutes old and looks indistinguishable
        // from the live one. `at` above is the second check — if it does not
        // move between reloads, something is caching regardless.
        headers: { "cache-control": "no-store, max-age=0" },
      });
    }

    if (url.pathname === "/telegram" && request.method === "POST") {
      // Telegram echoes the secret set with setWebhook. Without this check the
      // endpoint is an open relay for forged subscription changes.
      const presented = request.headers.get("x-telegram-bot-api-secret-token");
      if (presented !== env.WEBHOOK_SECRET) {
        // Telegram surfaces this only as "Wrong response from the webhook: 403
        // Forbidden", which says nothing about why. Name the cause in the
        // Worker's own log (Logs tab, or `wrangler tail`) without printing
        // either secret.
        console.warn(
          "rejected a delivery:",
          !env.WEBHOOK_SECRET
            ? "WEBHOOK_SECRET is not set on this Worker — check the variable is " +
              "named exactly WEBHOOK_SECRET, and that you deployed after adding it"
            : !presented
              ? "the request carried no secret header, so it did not come from " +
                "Telegram's webhook — or setWebhook was called without secret_token"
              : "the secret header did not match WEBHOOK_SECRET — the value here " +
                "and TELEGRAM_WEBHOOK_SECRET in GitHub differ, possibly by " +
                "trailing whitespace",
        );
        return new Response("forbidden", { status: 403 });
      }
      let update;
      try {
        update = await request.json();
      } catch {
        return new Response("bad json", { status: 400 });
      }
      // Telegram retries anything that is not a 2xx, which would duplicate
      // replies. Always acknowledge, and handle failures by logging.
      try {
        const seq = update.update_id;
        if (update.callback_query) await onCallback(env, update.callback_query, seq);
        else await onMessage(env, update.message || update.channel_post || {}, seq);
      } catch (e) {
        console.error("handler failed", e && e.stack);
      }
      return new Response("ok");
    }

    if (url.pathname === "/stripe" && request.method === "POST") {
      // The RAW body, before any parsing. Stripe signs the exact bytes, so
      // re-serialising parsed JSON here would fail every signature.
      const raw = await request.text();
      const check = await stripeSigned(
        env, raw, request.headers.get("stripe-signature"), Date.now(),
      );
      if (!check.ok) {
        // 400, unlike /telegram's always-200. A retry cannot fix a bad
        // signature, and Stripe showing the endpoint as failing in its
        // dashboard is exactly the signal a misconfigured secret needs.
        console.warn("rejected a Stripe delivery:", check.why);
        return new Response("bad signature", { status: 400 });
      }
      let event;
      try {
        event = JSON.parse(raw);
      } catch {
        return new Response("bad json", { status: 400 });
      }
      try {
        const out = await onStripe(env, event);
        if (!out.handled) console.warn("stripe event not acted on:", event.type, out.why);
      } catch (e) {
        // 500 so Stripe retries. The queue key is the event id, so a retry
        // that arrives after a partial success collapses onto the same entry
        // instead of granting a second year.
        console.error("stripe handler failed", e && e.stack);
        return new Response("handler failed", { status: 500 });
      }
      return new Response("ok");
    }

    if (url.pathname === "/create-checkout-session" && request.method === "POST") {
      if (!env.STRIPE_SECRET_KEY) {
        // Not configured, so not a route. Deliberately indistinguishable from
        // an unknown path: an endpoint that announces it exists but cannot
        // work is only useful to somebody probing.
        return new Response("not found", { status: 404 });
      }
      let chatId = url.searchParams.get("chat_id");
      if (!chatId) {
        const body = await request.json().catch(() => ({}));
        chatId = body && body.chat_id;
      }
      const out = await createCheckoutSession(env, chatId);
      if (!out.ok) return new Response("could not create a session", { status: 502 });
      return Response.json({ url: out.url, id: out.id });
    }

    if (url.pathname === "/queue" && request.method === "GET") {
      if (!auth("DRAIN_SECRET")) return new Response("forbidden", { status: 403 });
      const { keys } = await env.QUEUE.list({ prefix: "q:", limit: 200 });
      const items = [];
      for (const k of keys.sort((a, b) => (a.name < b.name ? -1 : 1))) {
        const v = await env.QUEUE.get(k.name);
        if (v) items.push(JSON.parse(v));
      }
      return Response.json({ items });
    }

    // The subscriber list. GET hands it to a workflow, PUT takes it back after
    // that workflow has applied the queue to it. Both are DRAIN_SECRET-protected:
    // this is the personal data the whole change exists to keep out of a public
    // repository, so it must never be readable without the secret.
    if (url.pathname === "/list" && request.method === "GET") {
      if (!auth("DRAIN_SECRET")) return new Response("forbidden", { status: 403 });
      const { source, list } = await storedList(env);
      return Response.json({ source, list }, {
        headers: { "cache-control": "no-store, max-age=0" },
      });
    }

    if (url.pathname === "/list" && request.method === "PUT") {
      if (!auth("DRAIN_SECRET")) return new Response("forbidden", { status: 403 });
      let body;
      try {
        body = await request.json();
      } catch {
        return new Response("bad json", { status: 400 });
      }
      // Refuse anything that is not recognisably a list. Writing garbage here
      // would lose every subscriber at once, and the caller is a shell script
      // whose upstream steps can fail in ways that still produce output.
      const list = body && body.list !== undefined ? body.list : body;
      const shaped = list && Array.isArray(list.approved) && Array.isArray(list.pending);
      if (!shaped) {
        return Response.json(
          { ok: false, error: "expected an object with approved[] and pending[]" },
          { status: 400 },
        );
      }
      await env.QUEUE.put(LIST_KEY, JSON.stringify(list));
      return Response.json({
        ok: true,
        stored: {
          approved: list.approved.length,
          pending: list.pending.length,
          unsubscribed: (list.unsubscribed || []).length,
        },
      });
    }

    if (url.pathname === "/ack" && request.method === "POST") {
      if (!auth("DRAIN_SECRET")) return new Response("forbidden", { status: 403 });
      const { ids } = await request.json().catch(() => ({ ids: [] }));
      let removed = 0;
      for (const id of ids || []) {
        await env.QUEUE.delete(`q:${id}`);
        removed++;
      }
      return Response.json({ removed });
    }

    return new Response("not found", { status: 404 });
  },
};
