# Daily Economic Briefing — runbook

## What runs, and when

`.github/workflows/briefing.yml` fires **five times every weekday**, at `:17`
past 00:00 to 04:00 UTC. They are retries, not a schedule. `scripts/gate.py`
lets exactly one through — the first fire past **20:00 America/New_York**,
about four hours after the US close — and every later fire that day stops on
`already published`:

| | UTC fire | Bangkok | New York | outcome |
|---|---|---|---|---|
| Mar–Oct (EDT) | 00:17 | 07:17 | 20:17 | **runs** |
| | 01:17 | 08:17 | 21:17 | skips — already published |
| | 02:17 | 09:17 | 22:17 | skips — already published |
| | 03:17 | 10:17 | 23:17 | skips — already published |
| | 04:17 | 11:17 | 00:17 | skips — too early |
| Nov–Mar (EST) | 00:17 | 07:17 | 19:17 | skips — too early |
| | 01:17 | 08:17 | 20:17 | **runs** |
| | 02:17 | 09:17 | 21:17 | skips — already published |
| | 03:17 | 10:17 | 22:17 | skips — already published |
| | 04:17 | 11:17 | 23:17 | skips — already published |

Four usable chances in each half of the year. The set spans five hours because
the ET cutoff slides with US daylight saving: summer uses the first four,
winter the last four.

**GitHub's scheduler is genuinely unreliable, not just slightly late.** The
first scheduled run of this workflow fired **2h 43m** after its cron time, from
`0 0 * * 1-5`. Midnight UTC on the hour is the most contended minute there is —
it is the default everyone picks, and queued scheduled jobs are low-priority.
Hence `:17`. The **second** scheduled run was dropped entirely: no runner, no
logs, no record that anything was due. That is why there are now five entries
rather than two — `:17` helps with lateness and does nothing at all for a fire
that never happens.

Two entries looked like redundancy and were not. In EST the 00:17 fire is
19:17 ET and always too early, so winter had exactly **one** usable fire and no
second chance. If you ever trim this list, `scripts/test_gate.py` fails: it
reads the cron entries out of the workflow and asserts at least four usable
chances in both DST regimes.

Each fire is independent on purpose. Chaining them — retry only if the previous
one ran — would put back the single point of failure, because the thing being
defended against is a fire that never happens at all. What cancels the rest of
the day is committed state: today's edition exists, so the gate stops. No
dropped fire can disturb that, and a wasted fire costs about **20 seconds** of
runner time (measured: 21s, `pip install` included) and nothing in money on a
public repo.

Even so, treat the delivery time as a hope rather than a guarantee: plan for
**07:20 GMT+7 at best, and 09:17 or 10:17 on a morning where the early fires
are dropped**. The gate accepts any fire from 20:00 ET onward, so a late run
still produces a correct edition with an honest cutoff — it is the arrival time
that slips, not the content. A wholly missed day is self-healing: the next
day's gate widens the window and covers both sessions.

If a hard delivery time ever matters more than simplicity, the cron has to go
and be replaced by an external scheduler calling `workflow_dispatch`. Nothing
inside GitHub Actions can make `schedule` punctual.

Because a run happens at 20:00 ET *the evening before* its own date, a Monday
run sits at 20:00 ET **Sunday** and produces the Friday-plus-weekend edition.
That is why the gate does not simply ask "was yesterday a trading day".

## Skip rules

Three, all in `scripts/gate.py`:

- **too early** — the ET clock is short of 20:00. Kills the winter 00:00 fire.
- **already published** — an edition for this date is committed. Kills the
  duplicate second fire, and makes a manual re-run idempotent.
- **no session** — no NYSE session has closed since the previous edition's
  cutoff. This is the market-holiday skip.

`workflow_dispatch` with **force** overrides all three.

## The pipeline

```
gate.py ─► install toolchain ─► claude-code-action ─► verify_edition.py ─► push ─► dispatch deliver.yml ─► Telegram
```

Claude writes files only. **Every git operation is a deterministic workflow
step**, so a bad run cannot produce a strange commit.

Note that a push made with `GITHUB_TOKEN` does **not** fire another workflow's
`push` trigger. That is why the last step invokes `deliver.yml` explicitly
through the `workflow_dispatch` input it already exposes, rather than relying on
the push.

## Who receives it

Two places, on purpose:

| recipient | stored in | visibility |
|---|---|---|
| the owner | `TELEGRAM_CHAT_ID` secret | private |
| everyone else | the Worker's Cloudflare KV | private |

**The list is not in this repository.** Chat IDs are personal data and this
repository is public, so committing them published them. They live in the KV
namespace the Worker already uses for its queue: private, no new credential, read
and written with the same `DRAIN_SECRET`. `subscribers.json` is gitignored;
workflows fetch it to that path at run time and must never commit it.

That makes **the Worker required**. A polling-only setup has nowhere to keep the
list, and a copy in git would undo the point, so `subscriptions.yml` fails loudly
rather than treating an unreachable Worker as "nobody is subscribed".
`deliver.yml` is the one exception: it degrades to owner-only with a warning,
because a briefing that reaches you beats no briefing.

Two ids — `702837256` and `870201856` — were committed before this change and
remain in the public history. See *Purging the old ids* below.

`deliver.yml` sends to the owner first, then to every approved subscriber. It
uploads the PDF once and reuses the `file_id` Telegram returns for the rest, so
twenty recipients cost one upload rather than twenty.

**Adding someone.** They send the bot `/start`. The Worker answers them in
milliseconds and queues the decision; `subscriptions.yml` later applies it to the
list, recording them under `pending` — which entitles them to nothing — and
messages **you** with their name and id so you can decide without opening GitHub.

The reply is instant. The bookkeeping is not. GitHub does not honour
`*/5 * * * *`: measured over the 20 runs to 2026-11-05, the mean gap between
fires was 5h47m and the longest 10h06m — roughly 1.5% of the declared cadence.
Treat the list as catching up within **hours**, not minutes. Delivery does not wait for it —
`deliver.yml` drains the queue itself before reading the list, so every edition
goes out against current state regardless of when the poller last ran.

Two ways to enrol them, and they do the same thing:

| | how | applied |
|---|---|---|
| From Telegram | reply `/approve <id>` to the bot | by the next poller run (hours), and always before the next edition |
| From GitHub | **Actions → Find my Telegram chat ID**, `approve` input | immediately |

The owner's commands, honoured **only** from the owner's own chat:

| command | effect |
|---|---|
| `/approve <id> [<id>…]` | enrol; the subscriber is told they are approved |
| `/deny <id> [<id>…]` | drop the request; the subscriber is told nothing |
| `/pending` | the waiting ids, and how to act on them |
| `/status` | how many are approved, waiting and opted out |

Authorisation is the sender's chat id, and that is sound rather than lazy:
Telegram asserts the id in the payload, a sender cannot set it, and the owner's
id comes from a repository secret no message can influence. A command from
anyone else changes nothing and is logged as a warning — someone probing for an
admin interface is worth seeing.

`/deny` is silent on purpose. "You were refused" helps nobody, and denial is
also how obvious spam gets cleared.

A `/start` and your `/approve` that both land before the next poll are resolved
in one pass, and the subscriber is told only the outcome rather than "pending"
followed seconds later by "approved".

Approval is a separate step deliberately. Anyone who finds the bot can message
it, so enrolling automatically would mean strangers receiving the briefing and
spending the Telegram send quota. **Discovery is automatic; consent is not.**
If you would rather `/start` enrol people directly, it is one line in
`process()` — but that is the decision it reverses.

**Leaving needs nobody's permission.** A `/stop` (or `/unsubscribe`) is
acknowledged instantly by the Worker and applied to the list by the next poller
run — and in any case before the next edition, which drains the queue first.
They are also remembered in an `unsubscribed` list, so a message still sitting
in Telegram's backlog cannot re-propose them as a
candidate. `/start` later puts them back in `pending` — returning still needs
approval. An `approve` overrides a remembered opt-out, since that is the owner
saying so explicitly.

### Why the poller is its own workflow

This started as a step inside `briefing.yml`, which was wrong in two ways that
only showed up in use:

- It ran **at most once a weekday**, so "auto-response" meant a reply the next
  morning — and a message sent on a Friday afternoon was **lost**, because
  Telegram keeps updates for 24 hours and the next sweep was 66 hours away.
- It was gated on the edition being due, so any fire that found the edition
  already published skipped it entirely. There was no cheap way to process a
  message at all: a manual run either skipped the sweep or regenerated a whole
  briefing.

So it polls on **GitHub's** cron, not a Claude Routine. GitHub's scheduler is
unreliable, which is fatal for producing an edition and harmless here — a dropped
poll delays a reply by a few minutes rather than losing a briefing. It also costs
no model tokens, where a Routine at this cadence would cost roughly $0.43 a time.

`briefing.yml` no longer touches `subscribers.json` at all. One writer means the
`telegram-subscribers` concurrency group is enough to prevent races, and
`deliver.yml` simply reads whatever the list says when it checks out — at most a
few minutes stale.

### Exactly once

Two different mechanisms, depending on the path.

**Under the webhook**, queue keys are derived from Telegram's `update_id`, which
is monotonic per bot. That makes enqueueing idempotent — a delivery Telegram
retries rewrites the same key rather than adding a second item — and makes a
lexical sort of the queue true chronological order. Ordering matters because the
last decision in a batch wins: an earlier version keyed on `Date.now()` plus a
random suffix, so two decisions in the same millisecond sorted randomly and a
`/stop` could be applied before the `/start` it followed, leaving somebody
subscribed after asking to leave.

The queue is **at-least-once**: items are handed out on read and deleted only
after the workflow has committed, so `apply_queue()` is written to be idempotent
and every case is tested applied twice. Acknowledging on read would instead lose
an opt-out silently.

`apply_queue()` sends nothing. The Worker already answered the sender at the
time; messaging them again days later because a drain replayed would be worse
than saying nothing.

**Under polling**, every message must be acted on once, or a five-minute poller
reading a 24-hour backlog would answer the same `/start` about 288 times a day.
Two independent guards:

1. The poll asks Telegram for `offset = last_update_id + 1`, so confirmed
   updates are not served again.
2. `process()` ignores any update whose id is at or below `last_update_id`, even
   if Telegram serves it anyway.

Both are needed: an offset that fails to stick, a retry, or a second reader
would otherwise replay the backlog. An update arriving with **no** usable id is
processed rather than dropped — a duplicate confirmation is a nuisance, an
opt-out that vanished means messaging someone who asked you to stop.

If the poll sends its replies but then cannot push, `last_update_id` is not
saved and the next poll will answer those messages again. That is the deliberate
choice: confirming to Telegram before the commit would instead lose the opt-out
silently.

The remaining limit: `getUpdates` still only retains 24 hours, so if the poller
is down for a whole day, messages in that window are gone. The instant,
guaranteed opt-out remains blocking the bot — Telegram then refuses delivery
outright, whatever the list says.

A failed poll never fails anything else: an unreachable Telegram, a rejected
token or a garbage response each log a warning and exit 0.

### Purging the old ids

`702837256` and `870201856` are in this repository's history from before the list
moved to KV. Deleting the file did not unpublish them, and a Telegram chat ID
cannot be rotated — only abandoned with the account.

Removing them means rewriting history and force-pushing `main`. Read the whole of
this before starting.

**What it costs.** Every existing clone and fork diverges. `main` is also pushed
to by the briefing pipeline, so a run in flight will conflict. Anyone who already
cloned still has the ids. This reduces casual discoverability; it does not undo
exposure.

**What it does not need.** Nothing else in the pipeline depends on those commits,
so no workflow or secret changes.

The steps, from a machine with a clone and `git-filter-repo` installed:

1. **Stop the pipeline.** Disable **Answer the Telegram bot** and **Daily
   Economic Briefing** in the Actions tab, and pause both Routines, so nothing
   pushes while you work.
2. **Back up.** `git clone --mirror` the repository somewhere else, and
   `curl "<worker>/list?secret=<DRAIN_SECRET>" > backup.json`.
3. **Confirm the list is in KV**, not just in git: `<worker>/health` must show
   `"list":{"source":"kv"`. If it says `git`, migrate first — otherwise this
   deletes the only copy.
4. **Rewrite:** `git filter-repo --path subscribers.json --invert-paths`
5. **Check:** `git log --all -p -- subscribers.json` prints nothing, and
   `git log --all -S 870201856 --oneline` finds nothing.
6. **Force-push:** `git push --force --all && git push --force --tags`
7. **Re-enable** the workflows and Routines, and run **Answer the Telegram bot**
   once by hand to confirm it still reads the list from KV.
8. **Ask GitHub Support to purge cached views** if it matters — rewritten commits
   can stay reachable by SHA through the API and forks until they do.

If any of that reads as more risk than the exposure of two ids you control,
leaving them is a defensible choice. Nothing else in the design depends on it.

### What the bot says

All five messages are in `MSG` at the top of `scripts/subscribers.py`, and
`scripts/send_replies.sh` delivers them for both workflows so the two cannot
drift apart.

| trigger | reply | sent by |
|---|---|---|
| `/start` | "Your request for subscription is pending." | `subscriptions.yml` poll |
| owner approves | "Your request for subscription has been approved." | `find-chat-id.yml` |
| `/stop` | "We have received your unsubscribe request. Please give us time to process it." | `subscriptions.yml` poll |
| `/start` when already subscribed | "You are already subscribed…" | `subscriptions.yml` poll |
| owner sends `/stop` | explains their copy comes from the secret | `subscriptions.yml` poll |

Only a real state change is announced. Re-running `approve` on somebody already
approved messages nobody, so the owner can re-run the workflow freely.

**How fast a reply arrives depends on whether the Worker is deployed.**

| | webhook (`worker/`) | polling only |
|---|---|---|
| `/start`, `/stop` answered | milliseconds | next poll, 5–15 min |
| owner notified of a request | milliseconds, with Approve/Deny buttons | next poll |
| Approve → subscriber told | milliseconds | immediately, if approved from the GitHub workflow |
| the stored list caught up | hours, not minutes | GitHub throttles the poller; see *Adding someone* above |

`worker/README.md` has the one-time deploy. The switch is the
`TELEGRAM_DRAIN_URL` secret: present means drain the Worker's queue, absent means
poll. **Setting a Telegram webhook disables `getUpdates`** — they are mutually
exclusive — which is why this is a switch and not an addition, and why undoing it
means deleting both the webhook and the secret.

That lag used to cost an edition: a subscriber approved seconds before one was
generated missed it. It no longer does. `deliver.yml` drains the queue itself
before it reads the list, so an approval — or a payment — lands in the edition
it preceded rather than the one after.

**Chat IDs no longer appear in any log.** The list itself lives in Cloudflare
KV rather than in this repository, and `subscribers.py` masks every id on the
way out of the process — `…890`, enough to tell two chats apart and not enough
to message one. That covers stdout, stderr and the run summaries, in every
workflow. Two paths deliberately keep the real id: the `recipients` output that
`deliver.yml` reads to address the sends, which is consumed through a pipe and
never logged, and the Telegram payloads, which is how **you** still get full
ids — send the bot `/pending` and it answers in your own chat.

**Display names are the exception, and still reach the log.** The discovery
workflow prints them so you can tell who is asking to be added, and on a public
repository **run logs are public too**. Masking a name is not useful the way
masking a number is — a half-shown name identifies the person as well as the
whole one — so this is a trade rather than an oversight. The same is true of an
id you type into the `approve` input: GitHub shows a workflow's inputs on the
run page, so that one number is public whatever this code does. If either
matters, make the repo private; nothing else here depends on it being public
except free Actions minutes.

**A subscriber who blocks the bot** fails every morning with
`403 Forbidden: bot was blocked by the user`. That is a warning, not a failure —
one dead subscriber must not stop the briefing reaching everyone else. The job
summary names them; drop them with the `remove` input. A failure delivering to
the *owner* does fail the job, because that means the setup itself is broken.

### Diagnosing the subscription path

Every run writes what it did to the job summary, because a subscription that
silently did not happen looks exactly like a run that succeeded.

**On a poll** (`subscriptions.yml`), under *Subscriptions*: how many updates arrived and from
how many chats, each chat classified (`new`, `pending`, `approved`,
`unsubscribed`, `owner`), every owner command with its effect, arguments that
were not chat ids, owner-only commands attempted by other chats, and the three
list sizes **before and after** with a marker on the ones that moved. Then
*Bot confirmations*: each message, and for a failure Telegram's own reason.

**On a delivery run,** under *Telegram delivery*: a row per recipient with its
role (owner or subscriber), whether the PDF was uploaded or a `file_id` reused,
and the result — including HTTP status and Telegram's description on a failure.
Every recipient is listed, not only the failures, because a plausible-looking
"delivered" with the wrong recipient count is the fault that would otherwise go
unnoticed.

**On Find my Telegram chat ID:** the whole list, by category, with the chats in
each. It runs on `always()`, so a run that failed earlier still answers the
question it is usually opened to answer — did my approval land?

Things worth knowing when reading these:

- **`ok: false` with HTTP 200 is a real Telegram response**, and both send paths
  check it. Trusting the status code alone would report a message as sent when
  the recipient never got it.
- **Messages are base64-encoded between the script and the send loop.** The
  owner's `/pending` answer and the new-request notice are multi-line; an
  earlier tab-separated version treated each line as its own record and tried to
  send a message to a chat id of `Pending ids: 555, 777, 888`.
- A confirmation failing never fails the run. `scripts/send_replies.sh` exits 0
  unconditionally — a confirmation that does not arrive is a nuisance, a briefing
  that does not arrive because of one is a fault.

## The paywall

**$4.99 a year, and it is off until `STRIPE_PAY_URL` is set.** That one secret
is the switch for delivery; `PAY_URL` on the Worker is the switch for what the
bot says. Both have to be set for the thing to work end to end, and the gate
is deliberately keyed on the pay link rather than on anything else: the
harmful misconfiguration is enforcing with no link for people to pay at, and
keying it this way round makes that state unreachable. The opposite slip —
selling while still delivering to everyone — costs revenue and announces
itself in the delivery summary's entitlement table.

### Who receives an edition

Everything is decided by `scripts/entitlement.py` and applied in one place,
`recipients()`:

| state | receives it | meaning |
|---|---|---|
| `paid` | yes | inside `paid_until` |
| `grace` | yes | up to 7 days past it, covering a card Stripe is retrying |
| `trial` | yes | fewer than 3 editions since `trial_started` |
| `lapsed` | no | was paid or trialling, and that ran out |
| `none` | no | nothing has ever granted this chat anything |

The owner is never filtered. A chat with no entitlement fields receives
nothing, which is the safe default for one that has only just appeared.

The trial is counted in **editions, not days**, and counted out of git: the
editions committed since `trial_started`. Nothing is decremented at send time,
so the delivery path still only reads.

### Reading the delivery summary

Every edition's summary carries an entitlement table — each approved chat, its
plan, and why it did or did not receive that edition. Read it when a
subscriber says they stopped getting the briefing; it answers that directly.

If the paywall excludes **every** subscriber the run says so as a warning,
because "1 recipient" otherwise looks like an ordinary quiet day. That is
either a genuinely empty paid list or the paywall misfiring, and the two need
opposite responses.

### Turning it on

1. Create the Stripe product, a $4.99/year recurring price, and a Payment Link
   with *Allow promotion codes* ticked.
2. Run **Find my Telegram chat ID** with **grandfather** ticked, so existing
   subscribers are not cut off. Done 3 November 2026 for the original four,
   who are covered to 3 November 2027.
3. Set `PAY_URL` and `STRIPE_WEBHOOK_SECRET` on the Worker, re-paste it, and
   check `/health` reports the new `version` and both under `config`.
4. Point a Stripe webhook at `<worker>/stripe` and paste its signing secret
   into `STRIPE_WEBHOOK_SECRET`.
5. Set `STRIPE_PAY_URL` in GitHub secrets. **This is the step that starts
   enforcing** — do it last.

### The autocomplete menu

Telegram shows a command menu only if the bot has been told what it is.
Actions → **Point the Telegram webhook at the Worker** → `commands`.

It publishes two scopes: a public one, and a chat-scoped one for the owner, so
subscribers are never shown the four owner commands that would refuse them.

Whether `/promo` and `/manage` are listed is **asked, not assumed** — the run
reads the Worker's `/health` and looks at `config.PAY_URL`. Both commands
return without replying until that variable is set, and a menu entry for a
command that answers nothing is worse than no entry.

**So re-run it after setting `PAY_URL`**, or the menu keeps hiding two
commands that now work. Nothing reminds you; the run says so in its own log,
which you will not be reading at that point.

Aliases are deliberately left out of the menu: `/subscribe`, `/unsubscribe`
and `/billing` keep working, but three ways to do one thing in a six-item
menu reads as three features.

### Cancellation

`/stop` removes someone from the delivery list, and that on its own does not
cancel what Stripe is charging them — so a subscriber with live billing is
also sent a customer-portal link in the same reply. `/manage` (or `/billing`)
gives them the same link without unsubscribing, for a card change.

The link is a one-time portal session created for their stored
`stripe_customer_id` when `STRIPE_SECRET_KEY` is set; otherwise the
`PORTAL_URL` login page; otherwise nothing is sent and **you are messaged to
cancel it in the dashboard by hand**. That last case is the floor, so a
missing variable degrades rather than misleading somebody into thinking the
money has stopped.

The portal must be enabled in Stripe itself before any of it works —
https://dashboard.stripe.com/settings/billing/portal, allow cancellation,
Save. Until that configuration is saved the API refuses the session with "No
configuration provided" and the fallback takes over.

A trial or comped subscriber is never offered a portal: there is no money
behind either.

### Comp codes

`COMP_CODES` on the Worker, as `FRIENDS:1, PRESS:2` — code and years.
Redeemed with `/promo CODE`, granting a year on the spot with no Stripe
involved. No expiry and no redemption limits, on purpose: those need race-safe
counting, KV has no transactions, and a cap that miscounts is worse than none.
Anything needing a limit should be a Stripe 100%-off promotion code instead.

## Recalling a briefing sent in error

**The clock is 48 hours.** Telegram lets a bot delete its own messages for
that long and no longer. After it runs out the copy in a subscriber's chat
cannot be removed by anything in this repository, by Support, or by deleting
the bot. Start the recall before anything else, then work out what went
wrong.

Actions → **Recall a misdelivered briefing** → Run workflow.

1. `file_name` — the exact document name, e.g.
   `Daily_Economic_Briefing_20260907.pdf`. It is matched against the file name
   Telegram itself reports for the message, so a typo deletes nothing rather
   than the wrong thing.
2. Leave the defaults (`targets: owner`, `apply` off) for the first run. That
   rehearses the entire walk against the owner's chat alone and deletes
   nothing. Read the summary table: it should show the bad file found.
3. Then `targets: all` with `apply` on, which does the same across the owner
   and every approved subscriber and leaves a one-line correction in each
   chat.

`targets` and `apply` are separate on purpose. A chat the real run could not
clean is retried on its own with `targets: owner` — or by narrowing the list —
rather than by re-running everything and sending a second correction to
people who were already dealt with.

### How it finds the message, and why that is safe

Nothing records the message ids — Telegram offers a bot no way to list what it
has sent. The run therefore sends the correction first and walks backwards
from its id, because private-chat message ids are one ascending counter.

Each candidate is probed with `editMessageCaption`, which succeeds **only** on
the bot's own captioned messages. A subscriber's own messages cannot be
edited, read or copied by it, so the walk steps over them blind. That rules
out the two obvious alternatives, `forwardMessage` and `copyMessage`: either
would relay a subscriber's private messages to the owner to discover what they
were.

The probe writes the target's own caption plus one or more zero-width spaces.
The padding is invisible and is load-bearing: `editMessageCaption` rejects an
edit that changes nothing with "message is not modified", and that rejection
is indistinguishable from "this message is not ours". The first real run hit
exactly this — the preceding rehearsal had written the plain caption onto the
owner's copy, so the run meant to delete it read the rejection as a miss,
walked past and stopped on the previous edition. Four subscribers were
cleaned; the owner's copy survived. Probes now always differ, a "not
modified" reply is retried with more padding, and a rehearsal puts the
caption back before it finishes.

A message is deleted only when the file name Telegram returns matches exactly.
If the newest document in a chat is some *other* edition, the run restores
that message's caption and stops for that chat rather than digging back
through older briefings — the operator's assumption is wrong at that point and
the summary says so.

### Tidying the notices afterwards

Each run leaves its correction notice behind — it has to, because that message
is the anchor the walk counts back from. `clean_notices` removes them once the
deletions are done.

It works only on the **owner's** chat, and the code refuses any other rather
than relying on the operator to get it right. Reading a message back to decide
whether it is a notice needs `forwardMessage`, which is fine in the owner's
own chat (each copy is deleted the moment it is read) but pointed at a
subscriber would relay their private messages. `editMessageText` is the probe
it deliberately does not use: on a message that is not a notice it does not
report what was there, it overwrites it — and the owner's chat also carries
approval notifications.

Subscribers keep their correction notice. That is intended: it is the only
record they have of why a briefing vanished.

### What it cannot do

- Nothing older than 48 hours.
- Nothing a subscriber has already forwarded, saved or screenshotted.
- Nothing in a chat that has since blocked the bot; that row reports the
  failure and the run carries on to the others.

## Verification gate

`scripts/verify_edition.py` runs before anything is committed, and the workflow
branches on its exit code:

| code | meaning | what commits |
|---|---|---|
| 0 | PDF and spec both good | both |
| 2 | PDF good, spec rejected | PDF only; previous spec stays current |
| 1 | PDF bad | nothing; the run fails and alerts |

Checks: the PDF exists, is ≥40 KB and exactly 4 pages; `check_refs.py` passes
(no dangling `[n]` citations, no stray `~`); the new spec is 8–120 KB, is at
least 60% the size of its predecessor, has an `## Edition log`, and records the
new edition date.

The spec checks are structural, not editorial — Claude has free rein over the
spec's content. What they prevent is a truncated or half-written spec becoming
the instructions for every future run.

## Diagnosing a run

Every run writes a **stage table to the job summary** (the Actions run page,
above the logs) showing how far it got:

| stage | status | detail |
|---|---|---|
| 1. Read the standing spec | ok | 1 Read calls |
| 2. Research passes | PARTIAL | 4 subagents, 31 web lookups |
| 3. Charts rendered | MISSING | 0 PNG(s) in build/ |
| … | | |

**First stage that did not complete** names where it broke. `PARTIAL` means
Claude invoked the thing but no output appeared — it failed while running.
`MISSING` means the stage was never reached. Below the table sit Claude's own
result fields, its closing messages, and the tool-call sequence.

Below the stage table the summary also carries:

- **Cost** — dollars, minutes and turns. Token counts are *not* available: the
  SDK's `modelUsage` reports context limits, not consumption, and the action
  hides the per-message output that would carry them. The line says so rather
  than looking like an omission. For real token metrics you would need
  `CLAUDE_CODE_ENABLE_TELEMETRY` and an OTEL endpoint to send them to.
- **Permission denials**, named. `permission_denials_count: 1` on its own says
  something was blocked without saying what. The table names the tool, how many
  times, and whether it was in `--allowedTools` — which separates the two cases:
  a tool absent from the list is a workflow fix, a tool present and still denied
  is a settings problem. When the count is non-zero but no denial message
  survives in the log, the report says the tool could not be identified rather
  than staying silent.
- **Tool errors** that are not permission-related — a repeatedly failing
  `WebFetch` against a known-awkward source, for instance.

`ALLOWED_TOOLS` is defined once at job level and passed both to the action and
to the reporter, so the comparison is against the list actually in force.

The verification checks append to the same summary, so one page covers the
whole run and a failure rarely needs a second one. Every run also uploads its
`build/` directory, the PDF and the new spec as an artifact, successes
included.

This exists because a run costs ~18 minutes and real quota. Read the stage
table first; go to the raw logs only when it is not enough.

`scripts/run_report.py` builds the table and is pinned by
`scripts/test_run_report.py` against the run shapes this pipeline actually hit
— backgrounded research that built nothing, a spec that was never written, and
an auth failure where no stage ran.

## Spec versioning

Specs live in `spec/daily-economic-briefing-spec-<ISO>.md`. "Latest" is the
newest timestamp, matched on a strict pattern so a stray or hand-renamed file
cannot become the next run's instructions. Every run writes a new one; all
versions are kept (~23 KB each).

To roll back a bad spec, delete the offending file (or copy an older one to a
fresh, later timestamp) and commit. To edit the spec by hand, write a new
timestamped file rather than editing an existing one.

## Setup

Repository secrets:

| secret | for | notes |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | the Claude step | `claude setup-token` locally; valid one year. Bills against the subscription, not per run. Capture it with `\| tr -d '\n'` — a truncated paste gives `401 Invalid bearer token` |
| `TELEGRAM_BOT_TOKEN` | delivery + alerts | already set |
| `TELEGRAM_CHAT_ID` | delivery + alerts | already set |

Also required: the [Claude GitHub App](https://github.com/apps/claude) installed
on this repository.

**Merge the enabling PR yourself.** Scheduled workflows only run from the
default branch, and GitHub attributes a scheduled run to whoever last edited the
cron — your merge makes that a person rather than a bot.

## Testing

`workflow_dispatch` on the Actions tab takes four inputs:

- **force** — bypass all three skip rules
- **dry_run** — build and verify, commit nothing, upload the PDF as a run
  artifact instead. Use this for the first run.
- **edition_date** — override the date
- **model** — defaults to `claude-sonnet-5`

A first run should be `force: true, dry_run: true`. Download the artifact, read
the PDF, then re-run without `dry_run`.

`workflow_dispatch` also only works from the default branch, so the workflow has
to be merged before it can be tested at all.

**Changes to `briefing.yml` cannot be dry-run from a branch.**
`claude-code-action` compares this workflow file against the copy on the default
branch and refuses to run when they differ — a security control, since otherwise
a branch could rewrite the workflow and read the secrets. It logs `Workflow
validation failed` and then **exits reporting success**, so the step goes green
having done nothing. The "Confirm Claude actually ran" step exists to turn that
into a clear failure.

The practical consequence: any edit to this workflow has to be merged to the
default branch before it can be exercised at all. Edits to `gate.py`,
`verify_edition.py` or the vendored skill are not affected — only the workflow
file itself is compared.

Locally, three suites — the workflow runs all three before spending anything:

```bash
python3 scripts/test_gate.py        # schedule: DST, holidays, gaps, cron delay
python3 scripts/test_verify.py      # spec validation, incl. the edition log
python3 scripts/test_run_report.py  # stage detection on real failure shapes
python3 scripts/test_subscribers.py # who receives it, and who must not
node    worker/test.mjs             # the instant replies and the queue
```

## Cost

The briefing spawns four parallel research subagents doing heavy web research,
so a run is not a small job. Billing goes against the **subscription behind
`CLAUDE_CODE_OAUTH_TOKEN`**, not per-run API charges — a daily edition consumes
subscription quota rather than money.

The model defaults to **Sonnet** — switch a single run to Opus with the `model`
dispatch input, or change the default in `briefing.yml`. Opus costs several
times the quota for this workload; Sonnet is the sensible standing default and
Opus a deliberate choice for an edition that warrants it.

If runs start hitting subscription limits, the levers are the model, how many
research subagents the spec asks for, and how much each one fetches.

## When something breaks

A failed run sends a Telegram message with a link to it. A run that shipped the
PDF but had its spec update rejected sends a different message — worth acting on,
since the spec then stops advancing.

- **Auth failure** (`401 Invalid bearer token`) → the token is wrong, expired or
  truncated; re-run `claude setup-token`. (`Credit balance is too low` instead
  means the workflow is on an API key with no Console credit.)
  The "Diagnose a failed briefing step" step prints Claude's own error;
  a 401 is the credential, not the code.
- **PDF is 5 pages** → almost always a stray forced page break, not overflow.
  The spec's production notes cover this; `grep -n 'pagebreak'` first.
- **No Chromium** → the toolchain step checks for it explicitly and fails early;
  look there rather than at the render.
- **PDF committed but no Telegram** → check the "Deliver to Telegram" step
  dispatched, then look at the `deliver.yml` run it triggered.
- **`Invalid username or token` on push** → `claude-code-action` rewrites
  `origin` to carry its own GitHub App token and revokes that token when it
  finishes, leaving a dead credential behind. The commit step resets the remote
  URL before pushing; if that line is removed, every push fails this way while
  the commit itself still succeeds.
- **Missed a day** → do nothing. The next run widens its window automatically.
  To backfill a specific date, dispatch with `force` and `edition_date`.
