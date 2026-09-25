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
| everyone else | `subscribers.json`, `approved` list | **public — this repo is public** |

`deliver.yml` sends to the owner first, then to every approved subscriber. It
uploads the PDF once and reuses the `file_id` Telegram returns for the rest, so
twenty recipients cost one upload rather than twenty.

**Adding someone.** They send the bot `/start`. `subscriptions.yml` polls the
bot **every five minutes**, records them under `pending` — which entitles them to
nothing — replies telling them so, and messages **you** with their name and id so
you can decide without opening GitHub.

Two ways to enrol them, and they do the same thing:

| | how | applied |
|---|---|---|
| From Telegram | reply `/approve <id>` to the bot | within ~5 minutes |
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

**Leaving needs nobody's permission.** A `/stop` (or `/unsubscribe`) is acted on
within about five minutes. They are also remembered in an `unsubscribed` list, so
a message still sitting in Telegram's backlog cannot re-propose them as a
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

Every message must be acted on once, or a five-minute poller reading a
24-hour backlog would answer the same `/start` about 288 times a day. Two
independent guards:

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

**Replies arrive within about five minutes, not instantly.** There is no webhook;
the bot only "hears" anything when `subscriptions.yml` polls. GitHub's cron is
late and skips, so treat five minutes as the floor and a quarter of an hour as a
bad case. An approval done from the GitHub workflow is the exception — it
messages the subscriber straight away.

Truly instant would need a webhook, which needs a public HTTPS endpoint this
design deliberately does not have. Note also that **setting a webhook disables
`getUpdates`** — Telegram allows one or the other, so adopting one would replace
this poller rather than supplement it.

Only numeric chat IDs and a chat type are ever committed — never names or
usernames. The workflow prints display names in its log so you can tell who is
asking to be added, and on a public repository **run logs are public too**, so
that is the one place a subscriber's name is briefly exposed. If that matters,
make the repo private; nothing else in the pipeline depends on it being public
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
