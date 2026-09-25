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
};

const START = new Set(["/start", "/subscribe"]);
const STOP = new Set(["/stop", "/unsubscribe"]);

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
async function enqueue(env, item, seq, n = 0) {
  const uid = Number.isFinite(seq) ? seq : Date.now();
  const id = `${String(uid).padStart(16, "0")}-${String(n).padStart(4, "0")}`;
  await env.QUEUE.put(`q:${id}`, JSON.stringify({ id, ...item }));
  return id;
}

/**
 * The current list, read from the public repository. No credential needed — the
 * repo is public, which is what makes this cheap. Failure is not fatal: the
 * Worker falls back to answering without list context rather than going silent.
 */
async function currentList(env) {
  try {
    const r = await fetch(env.LIST_URL, { cf: { cacheTtl: 30 } });
    if (!r.ok) return null;
    const d = await r.json();
    return {
      approved: new Set((d.approved || []).map((e) => e.chat_id)),
      pending: (d.pending || []).map((e) => e.chat_id),
    };
  } catch {
    return null;
  }
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
  if (START.has(verb)) {
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
                          "DRAIN_SECRET", "LIST_URL", "QUEUE"]) {
        config[name] = Boolean(env[name]);
      }
      const missing = Object.entries(config).filter(([, v]) => !v).map(([k]) => k);

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

      return Response.json({
        ok: missing.length === 0 && untrimmed.length === 0 && queueError === null,
        queued,
        config,
        ...(missing.length ? { missing } : {}),
        ...(untrimmed.length
          ? { whitespace: untrimmed, hint: "these have leading or trailing whitespace" }
          : {}),
        ...(queueError ? { queueError } : {}),
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
