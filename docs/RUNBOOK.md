# Daily Economic Briefing — runbook

## What runs, and when

`.github/workflows/briefing.yml` fires twice every weekday, at **00:00 and
01:00 UTC**. `scripts/gate.py` lets exactly one through, so that the run always
sits at **20:00 America/New_York** — about four hours after the US close:

| | UTC fire | Bangkok | New York | outcome |
|---|---|---|---|---|
| Mar–Oct (EDT) | 00:00 | 07:00 | 20:00 | **runs** |
| | 01:00 | 08:00 | 21:00 | skips — already published |
| Nov–Mar (EST) | 00:00 | 07:00 | 19:00 | skips — too early |
| | 01:00 | 08:00 | 20:00 | **runs** |

GitHub's scheduler is not punctual: runs routinely start 5–30 minutes late and
are occasionally dropped entirely. Expect delivery around **07:30–08:15 GMT+7**.
A dropped run is self-healing — the next day's gate widens the window and covers
both sessions.

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
the push. `deliver.yml` is otherwise untouched.

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
- **Missed a day** → do nothing. The next run widens its window automatically.
  To backfill a specific date, dispatch with `force` and `edition_date`.
