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
| `CLAUDE_CODE_OAUTH_TOKEN` | the Claude step | `claude setup-token` locally. Expires — regenerate when runs start failing on auth |
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

Locally: `python3 scripts/test_gate.py` pins the schedule logic across DST, the
two-cron arrangement, market holidays, multi-day gaps and cron delay. Run it
after touching `gate.py`. The workflow runs it too, before spending anything.

## Cost

The briefing spawns four parallel research subagents doing heavy web research.
The model defaults to **Sonnet**; switch a single run to Opus with the `model`
dispatch input, or change the default in `briefing.yml`. Runs bill against the
subscription behind `CLAUDE_CODE_OAUTH_TOKEN`, not the API.

## When something breaks

A failed run sends a Telegram message with a link to it. A run that shipped the
PDF but had its spec update rejected sends a different message — worth acting on,
since the spec then stops advancing.

- **Auth failure** → regenerate `CLAUDE_CODE_OAUTH_TOKEN`.
- **PDF is 5 pages** → almost always a stray forced page break, not overflow.
  The spec's production notes cover this; `grep -n 'pagebreak'` first.
- **No Chromium** → the toolchain step checks for it explicitly and fails early;
  look there rather than at the render.
- **PDF committed but no Telegram** → check the "Deliver to Telegram" step
  dispatched, then look at the `deliver.yml` run it triggered.
- **Missed a day** → do nothing. The next run widens its window automatically.
  To backfill a specific date, dispatch with `force` and `edition_date`.
