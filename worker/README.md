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

## Deploying it, once

You need a free Cloudflare account and `npx`. Nothing here costs money at this
volume.

**1. Create the queue.**

```sh
cd worker
npx wrangler kv namespace create QUEUE
```

Paste the printed id into `wrangler.toml`, replacing
`REPLACE_WITH_YOUR_KV_NAMESPACE_ID`.

**2. Invent two random secrets** and keep them to hand:

```sh
openssl rand -hex 32   # this is WEBHOOK_SECRET
openssl rand -hex 32   # this is DRAIN_SECRET
```

**3. Give the Worker its secrets.** Each command prompts for the value:

```sh
npx wrangler secret put BOT_TOKEN       # the same token as TELEGRAM_BOT_TOKEN
npx wrangler secret put OWNER_CHAT_ID   # the same value as TELEGRAM_CHAT_ID
npx wrangler secret put WEBHOOK_SECRET
npx wrangler secret put DRAIN_SECRET
```

**4. Deploy.** Note the URL it prints — call it `$WORKER`.

```sh
npx wrangler deploy
curl "$WORKER/health"      # expect {"ok":true,"queued":0}
```

**5. Point Telegram at it.**

```sh
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
  -H 'content-type: application/json' \
  -d '{"url":"'"$WORKER"'/telegram",
       "secret_token":"<WEBHOOK_SECRET>",
       "allowed_updates":["message","callback_query"]}'
```

**6. Tell the repository where to drain from.** Add two repository secrets under
Settings → Secrets and variables → Actions:

| secret | value |
|---|---|
| `TELEGRAM_DRAIN_URL` | `$WORKER` |
| `TELEGRAM_DRAIN_SECRET` | the `DRAIN_SECRET` from step 2 |

`subscriptions.yml` switches to draining the moment `TELEGRAM_DRAIN_URL` exists.
**Until then it keeps polling, so merging this before deploying breaks nothing.**

**7. Check it.** Send the bot `/start` from another account. The reply should be
immediate, and you should get the request with buttons. Tap Approve: the
subscriber is told at once, and within five minutes a "Update briefing
subscribers" commit appears.

## Undoing it

```sh
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/deleteWebhook"
```

Then delete the `TELEGRAM_DRAIN_URL` secret. Polling resumes on the next run.
**Do both:** a webhook and `getUpdates` are mutually exclusive, so leaving the
webhook set while the drain URL is gone means the bot hears nothing at all.

## Things that will bite

**A webhook disables `getUpdates`.** Telegram allows one or the other. That is
why this is a switch rather than an addition, and why undoing it is two steps.

**The secret header is the only thing standing between this endpoint and the
open internet.** Without it, anyone could POST a forged "the owner approved
chat X". The Worker rejects any request whose
`X-Telegram-Bot-Api-Secret-Token` does not match, and returns 403.

**Only your chat id may approve.** Telegram asserts the sender's id and a sender
cannot set it, so comparing against `OWNER_CHAT_ID` is sound. A stranger tapping
a forwarded button gets an alert and nothing happens.

**The queue is at-least-once.** Items are handed out on read and deleted only
after the workflow has committed. A drain that dies replays, which is why
`apply_queue()` in `scripts/subscribers.py` is idempotent. Acknowledging on read
instead would lose an opt-out silently — the one outcome worth engineering
against.

**The Worker always returns 200 to Telegram**, even when a handler throws.
Telegram retries anything else, which would duplicate replies; failures are
logged (`npx wrangler tail`) rather than surfaced as a retry.

## Testing without deploying

```sh
node worker/test.mjs
```

34 cases against a stubbed Telegram and KV: the instant replies, the button
flow, that a stranger cannot approve, that a forged request is rejected, that
reading the queue does not consume it, and that queue order survives two
decisions in the same millisecond.

That last one was a real bug. The queue key was originally `Date.now()` plus a
random suffix, so two decisions in the same millisecond sorted **randomly** —
and since the last decision in a batch wins, a `/stop` could be applied before
the `/start` it followed, leaving somebody subscribed after asking to leave. The
key is now Telegram's `update_id`, which is monotonic, and which also makes
enqueueing idempotent under Telegram's own retries.
