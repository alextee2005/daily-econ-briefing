/**
 * Exercise the webhook Worker without deploying it. Run: node worker/test.mjs
 *
 * The Worker is the only part of this system that talks to a person in real
 * time, so the cases here are about what actually reaches Telegram and what
 * lands in the queue — not about internal shape. KV and fetch are stubbed; the
 * handler is the real one.
 */
import worker from "./src/index.js";

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
      DRAIN_SECRET: true, LIST_URL: true, QUEUE: true });
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

console.log(`\n${failures} failure(s)`);
process.exit(failures ? 1 : 0);
