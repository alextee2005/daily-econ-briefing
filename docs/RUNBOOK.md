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

**Adding someone.** They send the bot `/start`. Every weekday, *before* it
delivers, `briefing.yml` reads `getUpdates` and records them under `pending`,
which entitles them to nothing, and replies telling them so. To enrol them, run
**Actions → Find my Telegram chat ID** with their id in the `approve` input;
they receive the next edition. The `remove` input takes them back off.

Approval is a separate step deliberately. Anyone who finds the bot can message
it, so enrolling automatically would mean strangers receiving the briefing and
spending the Telegram send quota. **Discovery is automatic; consent is not.**
If you would rather `/start` enrol people directly, it is one line in
`process()` — but that is the decision it reverses.

**Leaving needs nobody's permission.** A `/stop` (or `/unsubscribe`) is acted on
in that same pre-delivery sweep, so a chat that opts out in the morning is gone
from that morning's edition. They are also remembered in an `unsubscribed` list,
because their messages sit in Telegram's backlog for 24 hours and would
otherwise re-propose them as a candidate the next day. `/start` later puts them
back in `pending` — returning still needs approval. An `approve` overrides a
remembered opt-out, since that is the owner saying so explicitly.

The sweep lives inside `briefing.yml` rather than in a workflow of its own
because **the Routines that dispatch it every weekday are the schedule**. There
is no separate poller and no webhook to run.

Two limits worth knowing:

- **`getUpdates` only retains 24 hours.** A `/stop` sent on Friday evening is
  gone before Monday's sweep, so weekend opt-outs can be missed. The instant,
  guaranteed opt-out remains blocking the bot — Telegram then refuses delivery
  outright, whatever the list says.
- The sweep runs **after** verification, so a run whose PDF failed processes no
  commands and sends no confirmations. Nothing is delivered on such a run
  either, so a missed `/stop` costs the sender nothing that day.

A failed sweep never fails the briefing: an unreachable Telegram, a rejected
token or a garbage response each log a warning and the edition goes out.

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
