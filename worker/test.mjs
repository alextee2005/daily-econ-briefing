/**
 * Exercise the webhook Worker without deploying it. Run: node worker/test.mjs
 *
 * The Worker is the only part of this system that talks to a person in real
 * time, so the cases here are about what actually reaches Telegram and what
 * lands in the queue — not about internal shape. KV and fetch are stubbed; the
 * handler is the real one.
 */
import worker from "./src/index.js";

import { readFileSync } from "node:fs";

const OWNER = 111;
const FRIEND = 222;
const STRANGER = 333;

let failures = 0;
const expect = (label, got, want) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (!ok) failures++;
  console.log(`${ok ? "PASS" : "FAIL"}  ${label}`);
  if (!ok) {
    console.log(`      want ${JSON.stringify(want)}`);
    console.log(`      got  ${JSON.stringify(got)}`);
  }
};


/** The Worker's own wording for a key, so tests never re-type it. */
function MSGOF(_env, key) {
  const src = readFileSync(new URL("./src/index.js", import.meta.url), "utf8");
  const block = src.split("const MSG = {")[1].split("\n};")[0];
  const flat = block.replace(/"\s*\+\s*\n?\s*"/g, "");
  const m = new RegExp(`"?${key}"?:\\s*\\n?\\s*"((?:[^"\\\\]|\\\\.)*)"`).exec(flat);
  return m ? m[1] : null;
}

/** A KV namespace that behaves enough like Cloudflare's. */
function kv() {
  const m = new Map();
  return {
    m,
    put: async (k, v) => void m.set(k, v),
    get: async (k) => m.get(k) ?? null,
    delete: async (k) => void m.delete(k),
    list: async ({ prefix = "", limit = 1000 } = {}) => ({
      keys: [...m.keys()].filter((k) => k.startsWith(prefix)).slice(0, limit)
        .map((name) => ({ name })),
    }),
  };
}

let sent = [];
function harness({ approved = [], pending = [] } = {}) {
  sent = [];
  globalThis.fetch = async (url, init) => {
    const u = String(url);
    if (u.includes("/list.json")) {
      return new Response(JSON.stringify({
        approved: approved.map((c) => ({ chat_id: c })),
        pending: pending.map((c) => ({ chat_id: c })),
      }), { headers: { "content-type": "application/json" } });
    }
    const method = u.split("/").pop();
    sent.push({ method, body: JSON.parse(init.body) });
    return new Response(JSON.stringify({ ok: true, result: { message_id: 1 } }), {
      headers: { "content-type": "application/json" },
    });
  };
  return {
    QUEUE: kv(),
    BOT_TOKEN: "t",
    OWNER_CHAT_ID: String(OWNER),
    WEBHOOK_SECRET: "hook",
    DRAIN_SECRET: "drain",
    LIST_URL: "https://example.test/list.json",
  };
}

let uid = 5000;
const nextUid = () => ++uid;

const hook = (env, update, secret = "hook") =>
  worker.fetch(new Request("https://w.test/telegram", {
    method: "POST",
    headers: { "content-type": "application/json", "x-telegram-bot-api-secret-token": secret },
    body: JSON.stringify({ update_id: update.update_id ?? nextUid(), ...update }),
  }), env);

const msg = (chat_id, text, extra = {}) => ({
  message: { chat: { id: chat_id, type: "private", first_name: "Sam", ...extra }, text },
});

const queued = async (env) => {
  const { keys } = await env.QUEUE.list({ prefix: "q:" });
  const out = [];
  for (const k of keys.sort((a, b) => (a.name < b.name ? -1 : 1))) {
    out.push(JSON.parse(await env.QUEUE.get(k.name)));
  }
  return out;
};

// --- /start: instant reply, owner notified with buttons, one queue item --------
{
  const env = harness();
  await hook(env, msg(FRIEND, "/start", { username: "sam" }));
  const toFriend = sent.find((s) => s.body.chat_id === FRIEND);
  const toOwner = sent.find((s) => String(s.body.chat_id) === String(OWNER));

  expect("/start is answered immediately",
    [toFriend.method, toFriend.body.text],
    ["sendMessage", "Your request for subscription is pending."]);
  expect("the owner is notified in the same request", toOwner !== undefined, true);
  expect("the owner's notice carries Approve and Deny buttons",
    toOwner.body.reply_markup.inline_keyboard[0].map((b) => b.callback_data),
    [`a:${FRIEND}`, `d:${FRIEND}`]);
  expect("the owner's notice names who is asking",
    toOwner.body.text.includes("Sam") && toOwner.body.text.includes("@sam"), true);
  expect("exactly one decision is queued",
    (await queued(env)).map((i) => [i.verb, i.chat_id]), [["start", FRIEND]]);
}

// --- the owner taps Approve ----------------------------------------------------
{
  const env = harness({ pending: [FRIEND] });
  await hook(env, {
    callback_query: {
      id: "cb1", from: { id: OWNER }, data: `a:${FRIEND}`,
      message: { chat: { id: OWNER }, message_id: 9, text: "New subscription request" },
    },
  });
  expect("the button is answered first so it stops spinning",
    sent[0].method, "answerCallbackQuery");
  expect("the subscriber is told at once",
    sent.some((s) => s.body.chat_id === FRIEND &&
      s.body.text === "Your request for subscription has been approved."), true);
  expect("the buttons are replaced by the outcome",
    sent.some((s) => s.method === "editMessageText" && s.body.text.includes("approved")), true);
  expect("the approval is queued",
    (await queued(env)).map((i) => [i.verb, i.chat_id]), [["approve", FRIEND]]);
}

// --- Deny is silent to the subscriber -----------------------------------------
{
  const env = harness({ pending: [STRANGER] });
  await hook(env, {
    callback_query: {
      id: "cb2", from: { id: OWNER }, data: `d:${STRANGER}`,
      message: { chat: { id: OWNER }, message_id: 9, text: "req" },
    },
  });
  expect("a denied subscriber is told nothing",
    sent.some((s) => s.body.chat_id === STRANGER), false);
  expect("but the denial is queued",
    (await queued(env)).map((i) => [i.verb, i.chat_id]), [["deny", STRANGER]]);
}

// --- THE security case: only the owner may decide -----------------------------
{
  const env = harness({ pending: [STRANGER] });
  await hook(env, {
    callback_query: {
      id: "cb3", from: { id: STRANGER }, data: `a:${STRANGER}`,
      message: { chat: { id: STRANGER }, message_id: 9, text: "req" },
    },
  });
  expect("a stranger tapping Approve is refused",
    [sent.length, sent[0].method, sent[0].body.show_alert], [1, "answerCallbackQuery", true]);
  expect("and nothing is queued", await queued(env), []);
}
{
  const env = harness();
  await hook(env, msg(STRANGER, `/approve ${STRANGER}`));
  expect("a stranger typing /approve is ignored entirely",
    [sent.length, (await queued(env)).length], [0, 0]);
}

// --- /stop --------------------------------------------------------------------
{
  const env = harness({ approved: [FRIEND] });
  await hook(env, msg(FRIEND, "/stop"));
  expect("/stop is acknowledged immediately",
    sent[0].body.text,
    "We have received your unsubscribe request. Please give us time to process it.");
  expect("and queued", (await queued(env)).map((i) => i.verb), ["stop"]);
}

// --- an existing subscriber sending /start ------------------------------------
{
  const env = harness({ approved: [FRIEND] });
  await hook(env, msg(FRIEND, "/start"));
  expect("an existing subscriber is told so, and not re-queued",
    [sent[0].body.text, (await queued(env)).length],
    ["You are already subscribed. Send /stop to unsubscribe.", 0]);
}

// --- the owner's own /stop and text commands ----------------------------------
{
  const env = harness({ pending: [FRIEND] });
  await hook(env, msg(OWNER, "/stop"));
  expect("the owner's /stop is refused honestly",
    sent[0].body.text.startsWith("You are the owner"), true);
  expect("and nothing is queued", await queued(env), []);
}
{
  const env = harness({ pending: [FRIEND] });
  await hook(env, msg(OWNER, `/approve ${FRIEND}`));
  expect("the owner can also approve by typing",
    (await queued(env)).map((i) => [i.verb, i.chat_id]), [["approve", FRIEND]]);
}
{
  const env = harness({ approved: [FRIEND], pending: [STRANGER] });
  await hook(env, msg(OWNER, "/pending"));
  expect("/pending answers with the waiting ids",
    sent[0].body.text.includes(String(STRANGER)), true);
  expect("and queues nothing", await queued(env), []);
}
{
  const env = harness();
  await hook(env, msg(OWNER, "/approve"));
  expect("/approve with no argument explains itself rather than failing",
    sent[0].body.text.startsWith("Usage:"), true);
}

// --- the endpoint must not be an open relay -----------------------------------
{
  const env = harness();
  const r = await hook(env, msg(FRIEND, "/start"), "wrong-secret");
  expect("a forged webhook request is rejected",
    [r.status, sent.length, (await queued(env)).length], [403, 0, 0]);
}

// Telegram retries anything that is not 2xx, which would duplicate replies, so a
// handler that throws must still acknowledge.
{
  const env = harness();
  globalThis.fetch = async () => { throw new Error("Telegram down"); };
  const r = await hook(env, msg(FRIEND, "/start"));
  expect("a handler failure still returns 200 so Telegram does not retry",
    r.status, 200);
}

// --- drain and ack ------------------------------------------------------------
{
  const env = harness();
  await hook(env, msg(FRIEND, "/start"));
  await hook(env, msg(STRANGER, "/stop"));

  const bad = await worker.fetch(new Request("https://w.test/queue?secret=nope"), env);
  expect("the queue is not readable without the secret", bad.status, 403);

  const good = await worker.fetch(new Request("https://w.test/queue?secret=drain"), env);
  const { items } = await good.json();
  expect("the queue hands out items in the order they happened",
    items.map((i) => [i.verb, i.chat_id]), [["start", FRIEND], ["stop", STRANGER]]);

  // Reading must NOT delete: the workflow acknowledges only after committing.
  const again = await worker.fetch(new Request("https://w.test/queue?secret=drain"), env);
  expect("reading the queue does not consume it",
    (await again.json()).items.length, 2);

  const ack = await worker.fetch(new Request("https://w.test/ack?secret=drain", {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ ids: items.map((i) => i.id) }),
  }), env);
  expect("acknowledging removes them", (await ack.json()).removed, 2);
  expect("and the queue is then empty", (await queued(env)).length, 0);
}

// --- the subscriber list lives in KV, not in the repository --------------------
// Chat IDs are personal data and the repository is public. These cases cover the
// endpoints a workflow uses to read the list, apply the queue to it, and put it
// back — and that it is never readable without the secret, which is the entire
// point of moving it.
{
  const env = harness();
  const listJson = {
    approved: [{ chat_id: FRIEND, type: "private", added: "2026-09-30" }],
    pending: [], unsubscribed: [], last_update_id: 0,
  };

  const noSecret = await worker.fetch(new Request("https://w.test/list?secret=nope"), env);
  expect("the list is not readable without the secret", noSecret.status, 403);

  const noSecretPut = await worker.fetch(new Request("https://w.test/list?secret=nope", {
    method: "PUT", body: JSON.stringify(listJson),
  }), env);
  expect("and not writable without it", noSecretPut.status, 403);

  const put = await worker.fetch(new Request("https://w.test/list?secret=drain", {
    method: "PUT", headers: { "content-type": "application/json" },
    body: JSON.stringify(listJson),
  }), env);
  expect("storing the list reports what it stored",
    await put.json(), { ok: true, stored: { approved: 1, pending: 0, unsubscribed: 0 } });

  const got = await worker.fetch(new Request("https://w.test/list?secret=drain"), env);
  const body = await got.json();
  expect("reading it back is lossless", [body.source, body.list], ["kv", listJson]);
  expect("the list is never cached",
    got.headers.get("cache-control"), "no-store, max-age=0");

  // Once KV holds the list, the Worker must stop consulting the repository — that
  // is what makes the repo's visibility irrelevant.
  let fetchedGit = false;
  const realFetch = globalThis.fetch;
  globalThis.fetch = async (u, i) => { if (String(u).includes("/list.json")) fetchedGit = true;
                                       return realFetch(u, i); };
  await hook(env, msg(FRIEND, "/start"));
  expect("an approved subscriber is recognised from KV, without touching the repo",
    [sent[0].body.text, fetchedGit],
    ["You are already subscribed. Send /stop to unsubscribe.", false]);
}
{
  // Garbage must be refused. The caller is a shell script whose upstream steps
  // can fail while still producing output, and writing that would lose every
  // subscriber at once.
  const env = harness();
  for (const [label, payload] of [
    ["a bare string", '"nope"'],
    ["an object with no arrays", '{"approved":1,"pending":2}'],
    ["approved missing", '{"pending":[]}'],
    ["empty body", ""],
  ]) {
    const r = await worker.fetch(new Request("https://w.test/list?secret=drain", {
      method: "PUT", headers: { "content-type": "application/json" }, body: payload,
    }), env);
    expect(`PUT /list refuses ${label}`, r.status >= 400, true);
  }
  // Nothing reached KV. GET still answers, because it falls back to the
  // repository copy during migration — so the property to assert is the source,
  // not that the list is empty.
  const still = await (await worker.fetch(new Request("https://w.test/list?secret=drain"), env)).json();
  expect("and none of them reached KV", still.source === "kv", false);
}
{
  // A workflow may PUT either the bare list or {list: …}; accept both so the
  // shell does not have to reshape what GET handed it.
  const env = harness();
  const wrapped = { list: { approved: [], pending: [{ chat_id: 9, type: "private" }],
                            unsubscribed: [] } };
  const r = await worker.fetch(new Request("https://w.test/list?secret=drain", {
    method: "PUT", headers: { "content-type": "application/json" },
    body: JSON.stringify(wrapped),
  }), env);
  expect("PUT accepts the wrapped shape GET returns",
    (await r.json()).stored.pending, 1);
}
{
  // Migration window: KV empty, repository copy still readable.
  const env = harness({ approved: [FRIEND] });
  const body = await (await worker.fetch(new Request("https://w.test/list?secret=drain"), env)).json();
  expect("with KV empty it falls back to the repository copy", body.source, "git");

  const h = await (await worker.fetch(new Request("https://w.test/health"), env)).json();
  expect("health says which source is in use, so migration is checkable",
    [h.list.source, h.list.approved], ["git", 1]);
}
{
  // And with neither, it says so rather than pretending the list is empty.
  const env = harness();
  delete env.LIST_URL;
  const body = await (await worker.fetch(new Request("https://w.test/list?secret=drain"), env)).json();
  expect("with nothing configured the source is empty", [body.source, body.list],
    ["empty", null]);
}

// --- ordering, which a random key suffix used to scramble ----------------------
// Two decisions in the same millisecond must still apply in the order they
// happened: the last one wins, so getting this wrong could leave somebody
// subscribed after they had asked to leave.
{
  const env = harness();
  await hook(env, { update_id: 9001, ...msg(FRIEND, "/start") });
  await hook(env, { update_id: 9002, ...msg(FRIEND, "/stop") });
  await hook(env, { update_id: 9003, ...msg(FRIEND, "/start") });
  expect("the queue preserves the order the messages arrived in",
    (await queued(env)).map((i) => i.verb), ["start", "stop", "start"]);
}
{
  // Telegram retries a delivery it did not see acknowledged. The same update
  // must not become two queue items.
  const env = harness();
  await hook(env, { update_id: 7001, ...msg(FRIEND, "/start") });
  await hook(env, { update_id: 7001, ...msg(FRIEND, "/start") });
  expect("a retried delivery does not duplicate the queue item",
    (await queued(env)).length, 1);
}
{
  // One command, several targets: each needs its own slot, still ordered.
  const env = harness({ pending: [FRIEND, STRANGER] });
  await hook(env, { update_id: 7100, ...msg(OWNER, `/approve ${FRIEND} ${STRANGER}`) });
  expect("one /approve with two ids queues both, in order",
    (await queued(env)).map((i) => [i.verb, i.chat_id]),
    [["approve", FRIEND], ["approve", STRANGER]]);
}

// --- health, which has to explain a 403 nobody can see from outside -----------
// Telegram reports a rejected delivery only as "Wrong response from the webhook:
// 403 Forbidden". A missing secret and a wrong secret look identical from there,
// so /health has to distinguish them — reporting presence, never values.
{
  const env = harness();
  await hook(env, msg(FRIEND, "/start"));
  const h = await worker.fetch(new Request("https://w.test/health"), env);
  const body = await h.json();
  expect("health reports queue depth and a clean config",
    [body.ok, body.queued, body.missing], [true, 1, undefined]);
  expect("health confirms each binding is present",
    body.config,
    { BOT_TOKEN: true, OWNER_CHAT_ID: true, WEBHOOK_SECRET: true,
      DRAIN_SECRET: true, LIST_URL: true, QUEUE: true,
      STRIPE_WEBHOOK_SECRET: false, PAY_URL: false, COMP_CODES: false,
      STRIPE_SECRET_KEY: false, STRIPE_PRICE_ID: false,
      PORTAL_URL: false, PORTAL_RETURN_URL: false });
  // The paywall arrived after the rest of this Worker. A health check that
  // reads "not ok" for months before anyone sets up Stripe is one people stop
  // reading, so an absent Stripe secret is reported and not counted against it.
  expect("the paywall's own variables are reported without failing health",
    [body.ok, body.unconfigured],
    [true, ["STRIPE_WEBHOOK_SECRET", "PAY_URL", "COMP_CODES",
            "STRIPE_SECRET_KEY", "STRIPE_PRICE_ID",
            "PORTAL_URL", "PORTAL_RETURN_URL"]]);
  expect("health never echoes a secret value",
    JSON.stringify(body).includes(env.WEBHOOK_SECRET), false);
  // A cached diagnostic reports a state that may be minutes old and is
  // indistinguishable from the live one — worse than having no diagnostic.
  expect("health forbids caching",
    h.headers.get("cache-control"), "no-store, max-age=0");
  // The Worker runs from code pasted into a dashboard, so "is my paste live?"
  // has to be answerable from the response itself.
  expect("health reports which code is running",
    typeof body.version === "string" && body.version.length > 0, true);
  expect("health timestamps itself so a frozen reply is visible",
    typeof body.at === "string" && body.at.endsWith("Z"), true);
}
{
  // The exact failure we hit: the secret named something else, so env.X is
  // undefined and every delivery is refused.
  const env = harness();
  delete env.WEBHOOK_SECRET;
  const h = await worker.fetch(new Request("https://w.test/health"), env);
  const body = await h.json();
  expect("health names a missing secret instead of just failing",
    [body.ok, body.missing], [false, ["WEBHOOK_SECRET"]]);

  const r = await hook(env, msg(FRIEND, "/start"), "anything");
  expect("and the webhook refuses every delivery while it is missing",
    [r.status, sent.length], [403, 0]);
}
{
  // A value pasted into a dashboard field with a trailing newline: equally
  // invisible, equally fatal, and not caught by a presence check alone.
  const env = harness();
  env.WEBHOOK_SECRET = "hook\n";
  const h = await worker.fetch(new Request("https://w.test/health"), env);
  const body = await h.json();
  expect("health flags trailing whitespace in a secret",
    [body.ok, body.whitespace], [false, ["WEBHOOK_SECRET"]]);
}
{
  // A broken or unbound KV namespace must be reported, not thrown.
  const env = harness();
  env.QUEUE = { list: async () => { throw new Error("no such namespace"); } };
  const body = await (await worker.fetch(new Request("https://w.test/health"), env)).json();
  expect("health reports a broken queue binding",
    [body.ok, body.queued, body.queueError], [false, null, "no such namespace"]);
}

// --- ordinary chatter is not a command ----------------------------------------
{
  const env = harness();
  await hook(env, msg(FRIEND, "thanks for the briefing"));
  expect("a plain message is ignored",
    [sent.length, (await queued(env)).length], [0, 0]);
}


// ---------------------------------------------------------------------------
// Stripe
//
// Signature verification is the whole security of this endpoint: without it
// anyone who learns the URL can POST a fabricated payment and subscribe
// themselves free. So most of these cases are forgeries.
// ---------------------------------------------------------------------------

const WHSEC = "whsec_test_secret";

async function stripeSig(secret, raw, t) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(`${t}.${raw}`));
  const hex = [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
  return `t=${t},v1=${hex}`;
}

/** POST an event to /stripe, signed unless `header` overrides it. */
async function stripeHook(env, event, { secret = WHSEC, t = null, header = null } = {}) {
  const raw = JSON.stringify(event);
  const when = t ?? Math.floor(Date.now() / 1000);
  const sig = header ?? (await stripeSig(secret, raw, when));
  return worker.fetch(new Request("https://w.test/stripe", {
    method: "POST",
    headers: { "content-type": "application/json", "stripe-signature": sig },
    body: raw,
  }), env);
}

const checkout = (chat, id = "evt_1") => ({
  id, type: "checkout.session.completed",
  data: { object: { client_reference_id: String(chat), customer: "cus_1",
                    subscription: "sub_1" } },
});

// --- a genuine first payment ----------------------------------------------
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  const r = await stripeHook(env, checkout(FRIEND));
  expect("a correctly signed checkout is accepted", r.status, 200);
  const q = await queued(env);
  expect("it queues one paid decision for the right chat",
    q.map((i) => [i.verb, i.chat_id, i.years]), [["paid", FRIEND, 1]]);
  expect("carrying the Stripe ids for later reconciliation",
    [q[0].stripe_customer_id, q[0].stripe_subscription_id], ["cus_1", "sub_1"]);
  expect("and the payer is told immediately, not at the next drain",
    sent.map((s) => [s.method, s.body.chat_id]), [["sendMessage", FRIEND]]);
}

// --- forgeries -------------------------------------------------------------
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  const r = await stripeHook(env, checkout(STRANGER), { secret: "whsec_wrong" });
  expect("a signature from the wrong secret is refused", r.status, 400);
  expect("and nothing is queued", (await queued(env)).length, 0);
  expect("and nobody is told anything", sent.length, 0);
}
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  const r = await stripeHook(env, checkout(STRANGER), { header: "t=1,v1=deadbeef" });
  expect("a hand-written signature header is refused", r.status, 400);
}
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  const r = await stripeHook(env, checkout(STRANGER), { header: "" });
  expect("no signature header at all is refused", r.status, 400);
}
{
  // Replay: a real, correctly signed delivery captured and sent again later.
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  const old = Math.floor(Date.now() / 1000) - 3600;
  const r = await stripeHook(env, checkout(STRANGER), { t: old });
  expect("a correctly signed but hour-old delivery is refused as a replay",
    r.status, 400);
  expect("and grants nothing", (await queued(env)).length, 0);
}
{
  // The Worker deployed before Stripe is set up at all.
  const env = harness();
  const r = await stripeHook(env, checkout(FRIEND));
  expect("with no STRIPE_WEBHOOK_SECRET set, everything is refused", r.status, 400);
  expect("and no payment is invented", (await queued(env)).length, 0);
}
{
  // The body must be signed byte-for-byte. A tampered body with a valid
  // signature for the original must not pass.
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  const original = JSON.stringify(checkout(FRIEND));
  const t = Math.floor(Date.now() / 1000);
  const sig = await stripeSig(WHSEC, original, t);
  const tampered = JSON.stringify(checkout(STRANGER));
  const r = await worker.fetch(new Request("https://w.test/stripe", {
    method: "POST",
    headers: { "content-type": "application/json", "stripe-signature": sig },
    body: tampered,
  }), env);
  expect("a body swapped after signing is refused", r.status, 400);
}

// --- a payment nothing can be linked to ------------------------------------
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  const ev = checkout(FRIEND, "evt_nolink");
  delete ev.data.object.client_reference_id;
  const r = await stripeHook(env, ev);
  expect("a payment with no chat reference still returns 200", r.status, 200);
  expect("but grants nothing", (await queued(env)).length, 0);
  expect("and the owner is told it needs handling by hand",
    sent.map((s) => s.body.chat_id), [String(OWNER)]);
}

// --- the double-grant trap -------------------------------------------------
// A first payment raises BOTH checkout.session.completed and invoice.paid. If
// both granted, one payment would buy two years.
{
  const env = harness({ approved: [] });
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  await stripeHook(env, {
    id: "evt_first_invoice", type: "invoice.paid",
    data: { object: { customer: "cus_1", billing_reason: "subscription_create" } },
  });
  expect("the first invoice of a new subscription grants nothing on its own",
    (await queued(env)).length, 0);
}
{
  // A renewal a year later. The chat is found through the customer id stored
  // on the list at checkout.
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  await env.QUEUE.put("list", JSON.stringify({
    approved: [{ chat_id: FRIEND, stripe_customer_id: "cus_1" }],
    pending: [], unsubscribed: [],
  }));
  await stripeHook(env, {
    id: "evt_renewal", type: "invoice.paid",
    data: { object: { customer: "cus_1", billing_reason: "subscription_cycle" } },
  });
  const q = await queued(env);
  expect("a renewal invoice grants another year to the right chat",
    q.map((i) => [i.verb, i.chat_id, i.years]), [["paid", FRIEND, 1]]);
}
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  await stripeHook(env, {
    id: "evt_unknown", type: "invoice.paid",
    data: { object: { customer: "cus_nobody", billing_reason: "subscription_cycle" } },
  });
  expect("a renewal for a customer not on the list grants nothing",
    (await queued(env)).length, 0);
}

// --- retries must not stack ------------------------------------------------
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  await stripeHook(env, checkout(FRIEND, "evt_same"));
  await stripeHook(env, checkout(FRIEND, "evt_same"));
  await stripeHook(env, checkout(FRIEND, "evt_same"));
  expect("three deliveries of one event collapse onto a single queue entry",
    (await queued(env)).length, 1);
}

// --- cancellation ----------------------------------------------------------
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  await env.QUEUE.put("list", JSON.stringify({
    approved: [{ chat_id: FRIEND, stripe_customer_id: "cus_1",
                 paid_until: "2027-11-02" }],
    pending: [], unsubscribed: [],
  }));
  await stripeHook(env, {
    id: "evt_cancel", type: "customer.subscription.deleted",
    data: { object: { customer: "cus_1" } },
  });
  const q = await queued(env);
  expect("cancelling queues a cancellation, not a revocation",
    q.map((i) => [i.verb, i.chat_id]), [["cancelled", FRIEND]]);
  expect("and the subscriber is told they keep what they paid for",
    sent.length === 1 && /until/.test(sent[0].body.text), true);
}

// --- events we do not act on -----------------------------------------------
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  const r = await stripeHook(env, {
    id: "evt_fail", type: "invoice.payment_failed",
    data: { object: { customer: "cus_1" } },
  });
  expect("a failed payment is acknowledged and left to Stripe's retries",
    [r.status, (await queued(env)).length], [200, 0]);
  const r2 = await stripeHook(env, {
    id: "evt_other", type: "customer.created", data: { object: {} },
  });
  expect("an event with no handler is acknowledged, not errored",
    [r2.status, (await queued(env)).length], [200, 0]);
}

// --- the endpoint must not answer anything else ----------------------------
{
  const env = harness();
  env.STRIPE_WEBHOOK_SECRET = WHSEC;
  const r = await worker.fetch(new Request("https://w.test/stripe"), env);
  expect("GET /stripe is not a route", r.status, 404);
}


// ---------------------------------------------------------------------------
// The paywall in the bot
//
// PAY_URL is the switch. The first group is the one that matters most: with
// it unset, nothing below changes, so this can be merged and sit inert until
// Stripe is actually ready.
// ---------------------------------------------------------------------------

const PAY = "https://buy.stripe.com/test_abc";

{
  const env = harness();                       // no PAY_URL
  await hook(env, msg(FRIEND, "/start"));
  expect("with the paywall off, /start still answers with the pending wording",
    sent.map((s) => s.body.text).includes(MSGOF(env, "pending")) ||
      /pending/i.test(sent[0].body.text), true);
  expect("and still queues a plain start, not a trial",
    (await queued(env)).map((i) => i.verb), ["start"]);
}
{
  const env = harness();                       // no PAY_URL
  await hook(env, msg(FRIEND, "/promo FRIENDS"));
  expect("with the paywall off, /promo is ignored entirely",
    [sent.length, (await queued(env)).length], [0, 0]);
}

// --- the trial -------------------------------------------------------------
{
  const env = harness();
  env.PAY_URL = PAY;
  await hook(env, msg(FRIEND, "/start"));
  const q = await queued(env);
  expect("with the paywall on, /start queues a trial", q.map((i) => i.verb), ["trial"]);
  const toUser = sent.find((s) => s.body.chat_id === FRIEND);
  expect("the subscriber is told the trial length and the price",
    /free trial/.test(toUser.body.text) && /3 editions/.test(toUser.body.text) &&
      /\$4\.99/.test(toUser.body.text), true);
  expect("and the link carries their chat id, so the webhook can match it up",
    toUser.body.text.includes(`client_reference_id=${FRIEND}`), true);
  expect("the owner is told a trial started, with no approve buttons to press",
    sent.some((s) => String(s.body.chat_id) === String(OWNER) &&
      /Trial started/.test(s.body.text) && !s.body.reply_markup), true);
}
{
  // Coming back after a trial must not mint a second one, and must not claim
  // a number of editions the Worker cannot know.
  const env = harness();
  env.PAY_URL = PAY;
  await env.QUEUE.put("list", JSON.stringify({
    approved: [{ chat_id: FRIEND, trial_started: "2026-01-01" }],
    pending: [], unsubscribed: [],
  }));
  await hook(env, msg(FRIEND, "/start"));
  expect("a chat that already trialled gets no second trial queued",
    (await queued(env)).length, 0);
  const t = sent.find((s) => s.body.chat_id === FRIEND).body.text;
  expect("and is told they are already on the list, with the price",
    /already on the list/.test(t) && /\$4\.99/.test(t), true);
  expect("without claiming a number of editions left",
    /\{n\}/.test(t) || /editions? to go/.test(t), false);
}
{
  // The trial follows a chat through an opt-out. This is the /stop-then-
  // /start loophole, checked from the talking end.
  const env = harness();
  env.PAY_URL = PAY;
  await env.QUEUE.put("list", JSON.stringify({
    approved: [], pending: [],
    unsubscribed: [{ chat_id: FRIEND, trial_started: "2026-01-01" }],
  }));
  await hook(env, msg(FRIEND, "/start"));
  expect("a chat that trialled, left, and came back gets no fresh trial",
    (await queued(env)).length, 0);
}
{
  const env = harness();
  env.PAY_URL = PAY;
  await env.QUEUE.put("list", JSON.stringify({
    approved: [{ chat_id: FRIEND, paid_until: "2027-11-02" }],
    pending: [], unsubscribed: [],
  }));
  await hook(env, msg(FRIEND, "/start"));
  expect("a paying subscriber is not sold anything",
    [(await queued(env)).length,
     /already subscribed/i.test(sent.find((s) => s.body.chat_id === FRIEND).body.text)],
    [0, true]);
}

// --- comp codes ------------------------------------------------------------
{
  const env = harness();
  env.PAY_URL = PAY;
  env.COMP_CODES = "FRIENDS:1, PRESS:2";
  await hook(env, msg(FRIEND, "/promo friends"));
  const q = await queued(env);
  expect("a valid comp code is accepted, case-insensitively",
    q.map((i) => [i.verb, i.code, i.years]), [["comp", "FRIENDS", 1]]);
  expect("and the redeemer is told, and the owner is told who redeemed it",
    [sent.some((s) => s.body.chat_id === FRIEND && /accepted/i.test(s.body.text)),
     sent.some((s) => String(s.body.chat_id) === String(OWNER) &&
       /FRIENDS/.test(s.body.text))],
    [true, true]);
}
{
  const env = harness();
  env.PAY_URL = PAY;
  env.COMP_CODES = "FRIENDS:1, PRESS:2";
  await hook(env, msg(FRIEND, "/promo PRESS"));
  expect("a multi-year code grants what it says",
    (await queued(env)).map((i) => i.years), [2]);
}
for (const bad of ["/promo NOPE", "/promo", "/promo FRIEND", "/promo  "]) {
  const env = harness();
  env.PAY_URL = PAY;
  env.COMP_CODES = "FRIENDS:1";
  await hook(env, msg(FRIEND, bad));
  expect(`"${bad.trim()}" grants nothing`, (await queued(env)).length, 0);
}
{
  // No codes configured at all: every code must be refused, not accepted by
  // an empty-string match.
  const env = harness();
  env.PAY_URL = PAY;
  await hook(env, msg(FRIEND, "/promo ANYTHING"));
  expect("with no COMP_CODES set, no code works", (await queued(env)).length, 0);
  expect("and the refusal is explained rather than silent",
    /not valid/i.test(sent[0].body.text), true);
}

// --- the pay link ----------------------------------------------------------
{
  const env = harness();
  env.PAY_URL = "https://buy.stripe.com/test_abc?utm=tg";
  await hook(env, msg(STRANGER, "/start"));
  const t = sent.find((s) => s.body.chat_id === STRANGER).body.text;
  expect("a link that already has a query gets & rather than a second ?",
    t.includes(`?utm=tg&client_reference_id=${STRANGER}`), true);
}


// ---------------------------------------------------------------------------
// Checkout Session (Checkout Studio)
//
// The fixed_by_ui parameters are asserted one by one, because a silently
// dropped one is the failure mode: Stripe accepts the call, the session
// works, and the setting the user chose in the UI is simply not in effect.
// ---------------------------------------------------------------------------

/** Capture the form Stripe would have been sent. */
function stripeApiHarness(env) {
  const seen = [];
  const realFetch = globalThis.fetch;
  globalThis.fetch = async (u, init) => {
    if (String(u).includes("api.stripe.com")) {
      seen.push({ url: String(u), init,
                  form: new URLSearchParams(init.body) });
      return new Response(JSON.stringify({
        id: "cs_test_1", url: "https://checkout.stripe.com/c/pay/cs_test_1",
      }), { headers: { "content-type": "application/json" } });
    }
    return realFetch(u, init);
  };
  return seen;
}

{
  const env = harness();
  const r = await worker.fetch(new Request("https://w.test/create-checkout-session",
    { method: "POST" }), env);
  expect("without STRIPE_SECRET_KEY the route does not exist", r.status, 404);
}

{
  const env = harness();
  env.STRIPE_SECRET_KEY = "sk_test_x";
  const seen = stripeApiHarness(env);
  const r = await worker.fetch(new Request(
    "https://w.test/create-checkout-session",
    { method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ chat_id: FRIEND }) }), env);
  const body = await r.json();
  expect("a session is created and its URL returned",
    [r.status, body.url], [200, "https://checkout.stripe.com/c/pay/cs_test_1"]);
  expect("called with the secret key, form-encoded",
    [seen.length,
     seen[0].init.headers.authorization,
     seen[0].init.headers["content-type"]],
    [1, "Bearer sk_test_x", "application/x-www-form-urlencoded"]);

  const f = seen[0].form;
  // Every fixed_by_ui value from Checkout Studio, checked individually.
  for (const [k, v] of [
    ["ui_mode", "hosted_page"],
    ["billing_address_collection", "auto"],
    ["phone_number_collection[enabled]", "false"],
    ["automatic_tax[enabled]", "false"],
    ["allow_promotion_codes", "true"],
    ["payment_method_collection", "always"],
    ["submit_type", "auto"],
    ["saved_payment_method_options[payment_method_save]", "enabled"],
    ["integration_identifier", "hosted_web_0001"],
    ["origin_context", "web"],
  ]) {
    expect(`fixed_by_ui ${k} = ${v}`, f.get(k), v);
  }

  // The briefing is an annual subscription, and payment_method_collection is
  // only valid in that mode.
  expect("mode matches the product: a recurring subscription",
    f.get("mode"), "subscription");

  // Not from Checkout Studio, and the one field without which a completed
  // payment cannot be attributed to a Telegram chat at all.
  expect("the chat id travels as client_reference_id",
    f.get("client_reference_id"), String(FRIEND));

  expect("the success URL keeps Stripe's session-id template",
    /\{CHECKOUT_SESSION_ID\}/.test(f.get("success_url")), true);
  expect("a single line item, quantity one",
    [f.get("line_items[0][quantity]"), f.has("line_items[0][price]")], ["1", true]);
}

{
  // chat_id may also arrive as a query parameter.
  const env = harness();
  env.STRIPE_SECRET_KEY = "sk_test_x";
  const seen = stripeApiHarness(env);
  await worker.fetch(new Request(
    `https://w.test/create-checkout-session?chat_id=${STRANGER}`,
    { method: "POST" }), env);
  expect("chat_id is accepted from the query string too",
    seen[0].form.get("client_reference_id"), String(STRANGER));
}

{
  // Real values must override the placeholders rather than sitting beside them.
  const env = harness();
  env.STRIPE_SECRET_KEY = "sk_test_x";
  env.STRIPE_PRICE_ID = "price_1RealOne";
  env.CHECKOUT_SUCCESS_URL = "https://t.me/mybot";
  env.CHECKOUT_CANCEL_URL = "https://t.me/mybot";
  const seen = stripeApiHarness(env);
  await worker.fetch(new Request("https://w.test/create-checkout-session",
    { method: "POST" }), env);
  const f = seen[0].form;
  expect("a configured price replaces the placeholder",
    f.get("line_items[0][price]"), "price_1RealOne");
  expect("and the configured success URL is used, template intact",
    f.get("success_url"), "https://t.me/mybot?session_id={CHECKOUT_SESSION_ID}");
  expect("and the configured cancel URL is used",
    f.get("cancel_url"), "https://t.me/mybot");
}

{
  // Stripe refusing the call must not look like success.
  const env = harness();
  env.STRIPE_SECRET_KEY = "sk_test_x";
  const realFetch = globalThis.fetch;
  globalThis.fetch = async (u, init) => {
    if (String(u).includes("api.stripe.com")) {
      return new Response(JSON.stringify({
        error: { message: "No such price: 'price_...'" },
      }), { status: 400, headers: { "content-type": "application/json" } });
    }
    return realFetch(u, init);
  };
  const r = await worker.fetch(new Request("https://w.test/create-checkout-session",
    { method: "POST" }), env);
  expect("a refusal from Stripe is surfaced, not swallowed", r.status, 502);
}

{
  const env = harness();
  env.STRIPE_SECRET_KEY = "sk_test_x";
  const r = await worker.fetch(new Request("https://w.test/create-checkout-session"), env);
  expect("GET is not a route", r.status, 404);
}


// ---------------------------------------------------------------------------
// Customer portal
//
// The point of this is that /stop must not leave somebody paying for a
// briefing they no longer receive. Most of these cases are that one sentence.
// ---------------------------------------------------------------------------

/** Capture Stripe billing-portal calls and answer them. */
function portalApiHarness(env, { ok = true } = {}) {
  const seen = [];
  const realFetch = globalThis.fetch;
  globalThis.fetch = async (u, init) => {
    if (String(u).includes("billing_portal/sessions")) {
      seen.push(new URLSearchParams(init.body));
      return ok
        ? new Response(JSON.stringify({ url: "https://billing.stripe.com/session/xyz" }),
            { headers: { "content-type": "application/json" } })
        : new Response(JSON.stringify({ error: { message: "No configuration provided" } }),
            { status: 400, headers: { "content-type": "application/json" } });
    }
    return realFetch(u, init);
  };
  return seen;
}

const payingList = (extra = {}) => JSON.stringify({
  approved: [{ chat_id: FRIEND, paid_until: "2027-11-03", plan: "paid",
               stripe_customer_id: "cus_1", stripe_subscription_id: "sub_1",
               ...extra }],
  pending: [], unsubscribed: [],
});

// --- /stop with a live subscription ---------------------------------------
{
  const env = harness();
  env.PAY_URL = PAY;
  env.STRIPE_SECRET_KEY = "sk_test_x";
  await env.QUEUE.put("list", payingList());
  const seen = portalApiHarness(env);
  await hook(env, msg(FRIEND, "/stop"));

  expect("a portal session is created for the stored customer",
    seen.map((f) => f.get("customer")), ["cus_1"]);
  const t = sent.find((s) => s.body.chat_id === FRIEND).body.text;
  expect("and the unsubscribe reply carries the cancel link",
    [/still active with Stripe/.test(t),
     t.includes("https://billing.stripe.com/session/xyz")], [true, true]);
  expect("while the request itself is still honoured",
    (await queued(env)).map((i) => i.verb), ["stop"]);
}

// --- /stop with no billing behind it --------------------------------------
{
  const env = harness();
  env.PAY_URL = PAY;
  env.STRIPE_SECRET_KEY = "sk_test_x";
  await env.QUEUE.put("list", JSON.stringify({
    approved: [{ chat_id: FRIEND, trial_started: "2026-11-01" }],
    pending: [], unsubscribed: [],
  }));
  const seen = portalApiHarness(env);
  await hook(env, msg(FRIEND, "/stop"));
  expect("a trial chat is not sent a billing link it has no use for",
    [seen.length, /billing.stripe.com/.test(
      sent.find((s) => s.body.chat_id === FRIEND).body.text)], [0, false]);
}
{
  // A comp has no money behind it either, so there is nothing to cancel.
  const env = harness();
  env.PAY_URL = PAY;
  env.STRIPE_SECRET_KEY = "sk_test_x";
  await env.QUEUE.put("list", JSON.stringify({
    approved: [{ chat_id: FRIEND, paid_until: "2027-11-03", plan: "comp",
                 stripe_customer_id: "cus_1" }],
    pending: [], unsubscribed: [],
  }));
  const seen = portalApiHarness(env);
  await hook(env, msg(FRIEND, "/stop"));
  expect("a comped subscriber is not offered a portal", seen.length, 0);
}

// --- the case the subscriber cannot fix alone ------------------------------
{
  const env = harness();
  env.PAY_URL = PAY;              // paywall on, but no key and no PORTAL_URL
  await env.QUEUE.put("list", payingList());
  await hook(env, msg(FRIEND, "/stop"));
  expect("with no portal configured the owner is told to cancel it by hand",
    sent.some((s) => String(s.body.chat_id) === String(OWNER) &&
      /keep being charged/.test(s.body.text)), true);
  expect("and the subscriber still gets the ordinary unsubscribe reply",
    /give us time to process/.test(
      sent.find((s) => s.body.chat_id === FRIEND).body.text), true);
}

// --- the login-page fallback ----------------------------------------------
{
  const env = harness();
  env.PAY_URL = PAY;
  env.PORTAL_URL = "https://billing.stripe.com/p/login/abc";
  await env.QUEUE.put("list", payingList());
  await hook(env, msg(FRIEND, "/stop"));
  const t = sent.find((s) => s.body.chat_id === FRIEND).body.text;
  expect("with no secret key, the shareable login page is used instead",
    t.includes("https://billing.stripe.com/p/login/abc"), true);
  expect("and the owner is not pestered, since the subscriber can act",
    sent.some((s) => String(s.body.chat_id) === String(OWNER)), false);
}
{
  // A refused session must fall back rather than leaving them with nothing.
  const env = harness();
  env.PAY_URL = PAY;
  env.STRIPE_SECRET_KEY = "sk_test_x";
  env.PORTAL_URL = "https://billing.stripe.com/p/login/abc";
  await env.QUEUE.put("list", payingList());
  portalApiHarness(env, { ok: false });
  await hook(env, msg(FRIEND, "/stop"));
  expect("a refused portal session falls back to the login page",
    sent.find((s) => s.body.chat_id === FRIEND).body.text
      .includes("/p/login/abc"), true);
}

// --- /manage, for a card change without unsubscribing ---------------------
{
  const env = harness();
  env.PAY_URL = PAY;
  env.STRIPE_SECRET_KEY = "sk_test_x";
  env.PORTAL_RETURN_URL = "https://t.me/mybot";
  await env.QUEUE.put("list", payingList());
  const seen = portalApiHarness(env);
  await hook(env, msg(FRIEND, "/manage"));
  expect("/manage hands over the portal link", /Manage your subscription/.test(
    sent.find((s) => s.body.chat_id === FRIEND).body.text), true);
  expect("and does not unsubscribe anybody", (await queued(env)).length, 0);
  expect("the return URL is passed through when configured",
    seen[0].get("return_url"), "https://t.me/mybot");
}
{
  const env = harness();
  env.PAY_URL = PAY;
  await env.QUEUE.put("list", payingList());
  await hook(env, msg(FRIEND, "/billing"));
  expect("/billing is the same command, and says so when unavailable",
    /could not open the billing page/.test(
      sent.find((s) => s.body.chat_id === FRIEND).body.text), true);
}
{
  const env = harness();                       // paywall off
  await hook(env, msg(FRIEND, "/manage"));
  expect("with the paywall off, /manage does nothing", sent.length, 0);
}

console.log(`\n${failures} failure(s)`);
process.exit(failures ? 1 : 0);
