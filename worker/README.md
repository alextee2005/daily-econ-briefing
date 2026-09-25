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

**Under Variables and Secrets** → **Add**, five times.

⚠️ **Use *Variables and Secrets*, not *Build variables*.** The dashboard has two
places that look equivalent and are not:

| where | visible to the Worker at runtime? |
|---|---|
| Settings → **Variables and Secrets** | ✅ yes — the one you want |
| Settings → **Build** → *Build variables and secrets* | ❌ no — build-time only |

Adding them in the wrong place saves without any complaint and leaves every one
of them `undefined` at runtime. The symptom is a bare `403 Forbidden` on every
Telegram delivery, because the secret comparison can never succeed. Step 5 shows
this as `"missing"` listing all of them while `QUEUE` stays `true` — the binding
is configured elsewhere and is unaffected.

⚠️ **Press Deploy afterwards.** The dashboard stages these changes and discards
them if you navigate away.

| Variable name | Type | Value |
|---|---|---|
| `BOT_TOKEN` | **Secret** | your Telegram bot token, same as `TELEGRAM_BOT_TOKEN` |
| `OWNER_CHAT_ID` | **Secret** | your chat id, same as `TELEGRAM_CHAT_ID` |
| `WEBHOOK_SECRET` | **Secret** | the first random string |
| `DRAIN_SECRET` | **Secret** | the second random string |
| `LIST_URL` | Text | `https://raw.githubusercontent.com/alextee2005/daily-econ-briefing/main/subscribers.json` |

Choose **Secret** (encrypted) for the first four so they cannot be read back.
`LIST_URL` is plain text — it is a public URL.

⚠️ **The names in Cloudflare are NOT the names in GitHub.** The same two random
strings are stored twice under different names, and copying the GitHub name here
is the easiest way to break this:

| the string | in Cloudflare | in GitHub |
|---|---|---|
| first | `WEBHOOK_SECRET` | `TELEGRAM_WEBHOOK_SECRET` |
| second | `DRAIN_SECRET` | `TELEGRAM_DRAIN_SECRET` |

A misnamed secret is not an error anywhere. `env.WEBHOOK_SECRET` is simply
`undefined`, so every delivery is refused and Telegram reports only
`Wrong response from the webhook: 403 Forbidden`. Step 5 catches it.

⚠️ **Watch for a trailing newline** when pasting into the dashboard field. It is
invisible and equally fatal. Step 5 catches that too.

Then **Deploy** again. Bindings only take effect on a deploy.

## 5. Check it is alive

Note the Worker's URL from its page — something like
`https://econ-briefing-bot.<your-subdomain>.workers.dev`.

Visit **`<that URL>/health`** in your browser. You want:

```json
{"ok":true,"queued":0,"config":{"BOT_TOKEN":true,"OWNER_CHAT_ID":true,
 "WEBHOOK_SECRET":true,"DRAIN_SECRET":true,"LIST_URL":true,"QUEUE":true}}
```

**Every value in `config` must be `true`, and `ok` must be `true`.** This endpoint
reports only whether each binding exists — never its value — because that is the
one fault you cannot see from anywhere else:

| what you see | what it means |
|---|---|
| `"missing":["WEBHOOK_SECRET"]` | misnamed or not added — see the warning in step 4 |
| `"whitespace":["DRAIN_SECRET"]` | a stray newline or space got pasted in |
| `"queueError":…` | the `QUEUE` binding is absent, misnamed, or you did not deploy after adding it |
| `"queued":null` | same as above |
| an error page, not JSON | the code did not deploy, or the URL is wrong |
| no `version` field at all | you are running older code — the paste in step 3 did not deploy |
| `at` identical across two reloads | something is caching the reply; add `?x=1` to the URL |

The `version` field is the answer to "is my paste actually live?". The Worker runs
from code pasted into the dashboard, not from this repository, so a stale deploy
looks exactly like a configuration fault. If `version` is missing or older than
the `VERSION` constant at the top of `src/index.js`, fix that before reading
anything else on the page.

Do not go further until this is clean. Every later failure looks like a bare
`403` and tells you nothing.

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

## 7. Add the drain URL — LAST, and only now

| secret | value |
|---|---|
| `TELEGRAM_DRAIN_URL` | your Worker URL, e.g. `https://econ-briefing-bot.….workers.dev` (no trailing slash, no `/telegram`) |

**This secret is the switch, not a setting.** `subscriptions.yml` stops polling
and starts draining the moment it exists, so adding it before the Worker works
deadlocks the whole thing: the poller skips `getUpdates`, the drain finds no
Worker, and nothing is processed at all. Nothing is broken loudly — it just goes
quiet.

So the order matters in both directions:

| state | result |
|---|---|
| Worker working, webhook pointed, secret added | correct |
| secret added, Worker not working | **nothing processed at all** |
| webhook pointed, secret missing | instant replies still work, `subscribers.json` frozen |
| secret added, webhook not pointed | **nothing processed at all** |

If you are unsure, delete `TELEGRAM_DRAIN_URL` and unpoint the webhook: that is
the known-good polling configuration, and it works on its own.

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
