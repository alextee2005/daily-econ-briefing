# Instant Telegram replies

This Worker holds Telegram's webhook so that `/start`, `/stop` and your Approve
tap are answered in **milliseconds** instead of waiting for a cron.

It is deliberately not the source of truth. `subscribers.json` in the repository
decides who receives the briefing, and only a GitHub workflow writes it. The
Worker replies at once and appends the decision to a durable queue;
`subscriptions.yml` drains that queue and commits. **So the Worker holds no
GitHub credential**, and if it goes down you lose latency, not data.

```
Telegram ──► Worker ──► KV queue ──► subscriptions.yml ──► subscribers.json
             (ms)       (durable)    (drains, then acks)    (git, authoritative)
```

## What is instant, and what is not

| | when |
|---|---|
| `/start` → "Your request for subscription is pending." | instant |
| Your notification of the request, with Approve / Deny buttons | instant |
| Approve tap → "…has been approved." to the subscriber | instant |
| `/stop` → "We have received your unsubscribe request…" | instant |
| `subscribers.json` catching up | ≤ 5 minutes |

The last row is the only lag, and it matters in one narrow case: a subscriber
approved seconds before an edition is generated may miss that one edition,
because delivery reads the committed list. They will receive the next.

---

# Setting it up in the browser

No terminal needed. Everything below is the Cloudflare dashboard plus one
GitHub Actions run. Free plan throughout — Workers and KV both have free tiers
far above this volume. Allow about fifteen minutes.

**You will need two random strings.** Generate them in your password manager, or
anywhere that makes long random text. Keep them somewhere you can paste from.

| name | rules | used by |
|---|---|---|
| `WEBHOOK_SECRET` | **16–256 characters, letters/digits/underscore/hyphen only** | Telegram ↔ Worker |
| `DRAIN_SECRET` | any long random string | GitHub ↔ Worker |

Telegram genuinely rejects other characters in the first one, so no `!`, `$`, `/`
or spaces. The workflow in step 6 checks this before calling Telegram, so a bad
one fails there with an explanation rather than mysteriously later.

## 1. Create the KV namespace (the queue)

Cloudflare dashboard → **Storage & Databases** → **KV** → **Create instance**
(older accounts: **Workers & Pages** → **KV** → **Create a namespace**).

Name it `econ-briefing-queue`. Nothing else to configure.

## 2. Create the Worker

**Workers & Pages** → **Create** → **Workers** → **Create Worker**.

Name it `econ-briefing-bot`, then **Deploy** the placeholder it offers. You have
to deploy once before you can edit it — the dashboard has no "create without
deploying".

## 3. Paste in the code

On the Worker's page → **Edit code** (or **</> Edit code**).

Open [`src/index.js`](src/index.js) in GitHub, copy the **whole file**, and
replace everything in the dashboard editor with it. Then **Deploy**.

It is one self-contained file with no imports and no build step, specifically so
that this step is a copy and paste.

## 4. Wire up the bindings and secrets

Worker's page → **Settings**.

**Under Bindings** (older UI: *Variables* → *KV Namespace Bindings*) →
**Add binding** → **KV namespace**:

| field | value |
|---|---|
| Variable name | `QUEUE` |
| KV namespace | `econ-briefing-queue` |

The variable name must be exactly `QUEUE` — that is what the code looks for.

**Under Variables and Secrets** → **Add**, four times:

| Variable name | Type | Value |
|---|---|---|
| `BOT_TOKEN` | **Secret** | your Telegram bot token, same as `TELEGRAM_BOT_TOKEN` |
| `OWNER_CHAT_ID` | **Secret** | your chat id, same as `TELEGRAM_CHAT_ID` |
| `WEBHOOK_SECRET` | **Secret** | the first random string |
| `DRAIN_SECRET` | **Secret** | the second random string |
| `LIST_URL` | Text | `https://raw.githubusercontent.com/alextee2005/daily-econ-briefing/main/subscribers.json` |

Choose **Secret** (encrypted) for the first four so they cannot be read back.
`LIST_URL` is plain text — it is a public URL.

Then **Deploy** again. Bindings only take effect on a deploy.

## 5. Check it is alive

Note the Worker's URL from its page — something like
`https://econ-briefing-bot.<your-subdomain>.workers.dev`.

Visit **`<that URL>/health`** in your browser. You should see:

```json
{"ok":true,"queued":0}
```

If you get an error instead, the usual cause is a missing `QUEUE` binding, or a
deploy not done after adding it.

## 6. Point Telegram at it — from GitHub, not your browser

Add two repository secrets first: GitHub → **Settings** → **Secrets and
variables** → **Actions** → **New repository secret**:

| secret | value |
|---|---|
| `TELEGRAM_WEBHOOK_SECRET` | the first random string, exactly as in Cloudflare |
| `TELEGRAM_DRAIN_SECRET` | the second random string |

Then GitHub → **Actions** → **Telegram webhook (point / check / unpoint)** →
**Run workflow**:

- **What to do**: `point`
- **Worker URL**: your `https://econ-briefing-bot.….workers.dev` (no `/telegram`
  on the end — the workflow adds it)

**Do not** put the `setWebhook` URL in your browser address bar instead. It works,
but it writes your bot token into browser history, autocomplete and sync. That is
the same reason `find-chat-id.yml` exists. The workflow already has the token as
a secret and never prints it.

Run it with `check` first if you want to see the current state — that changes
nothing.

## 7. Add the drain URL

One more repository secret:

| secret | value |
|---|---|
| `TELEGRAM_DRAIN_URL` | your Worker URL, e.g. `https://econ-briefing-bot.….workers.dev` |

`subscriptions.yml` switches from polling to draining the moment this exists.
**Until you add it, people still get instant replies from the Worker, but
`subscribers.json` stops moving** — the webhook has disabled `getUpdates`, so the
polling path now finds nothing. So do not stop between steps 6 and 7.

## 8. Try it

From another Telegram account, send the bot `/start`.

| expect | if not |
|---|---|
| instant "Your request for subscription is pending." | run the webhook workflow with `check`; a `last delivery attempt failed: 403` means `WEBHOOK_SECRET` and `TELEGRAM_WEBHOOK_SECRET` differ |
| you get the request with Approve / Deny buttons | `OWNER_CHAT_ID` is wrong or not set |
| tapping Approve → subscriber told at once | check the Worker's live logs (**Logs** on its page) |
| a "Update briefing subscribers" commit within 5 minutes | check the **Answer the Telegram bot** workflow run |

## Undoing it

Actions → **Telegram webhook** → `unpoint`, **then delete the
`TELEGRAM_DRAIN_URL` secret**. Polling resumes on the next run.

Do both. A webhook and `getUpdates` are mutually exclusive, so leaving the
webhook set while the drain URL is gone — or the reverse — means the bot hears
nothing at all. The workflow prints the matching reminder each way.

## If you would rather use a terminal

```sh
cd worker
npx wrangler kv namespace create QUEUE      # paste the id into wrangler.toml
npx wrangler secret put BOT_TOKEN           # and OWNER_CHAT_ID, WEBHOOK_SECRET, DRAIN_SECRET
npx wrangler deploy
npx wrangler tail                           # live logs
```

`wrangler.toml` is already in this directory for that path. Step 6 is still worth
doing from Actions, for the same browser-history reason.

---

## Things that will bite

**A webhook disables `getUpdates`.** Telegram allows one or the other. That is
why `subscriptions.yml` is a switch rather than an addition, and why undoing it
is two steps.

**The secret header is the only thing between this endpoint and the open
internet.** Without it, anyone could POST a forged "the owner approved chat X".
The Worker rejects any request whose `X-Telegram-Bot-Api-Secret-Token` does not
match, and returns 403. If you rotate it, change it in both places.

**Only your chat id may approve.** Telegram asserts the sender's id and a sender
cannot set it, so comparing against `OWNER_CHAT_ID` is sound. A stranger tapping
a forwarded button gets an alert and nothing happens.

**The queue is at-least-once.** Items are handed out on read and deleted only
after the workflow has committed. A drain that dies replays, which is why
`apply_queue()` in `scripts/subscribers.py` is idempotent. Acknowledging on read
instead would lose an opt-out silently — the one outcome worth engineering
against.

**The Worker always returns 200 to Telegram**, even when a handler throws.
Telegram retries anything else, which would duplicate replies; failures show up
in the Worker's **Logs** tab rather than as a retry.

## Testing without deploying

```sh
node worker/test.mjs
```

34 cases against a stubbed Telegram and KV: the instant replies, the button
flow, that a stranger cannot approve, that a forged request is rejected, that
reading the queue does not consume it, and that queue order survives two
decisions in the same millisecond. It also runs in CI.

That last one was a real bug. The queue key was originally `Date.now()` plus a
random suffix, so two decisions in the same millisecond sorted **randomly** —
and since the last decision in a batch wins, a `/stop` could be applied before
the `/start` it followed, leaving somebody subscribed after asking to leave. The
key is now Telegram's `update_id`, which is monotonic, and which also makes
enqueueing idempotent under Telegram's own retries.
