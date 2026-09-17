---
name: daily-economic-briefing
description: Produce a sourced, 3-page-plus-annex daily economic briefing PDF covering US equities and earnings, macro and policy, commodities and FX, and derivatives and positioning — from parallel research through verification, charting, and Chromium PDF render. Use this skill whenever the user asks for a daily/market briefing, morning note, market wrap, pre-open or post-close summary, "what happened in markets", a recurring market report, or wants to set up or run a scheduled markets briefing — even if they don't say the word "briefing". Also use it when editing, re-running, or troubleshooting an existing edition of such a report.
---

# Daily Economic Briefing

Produces a dense, fully-sourced market briefing PDF: exactly 3 pages of briefing
plus a 1-page annex. The hard part is not the writing — it is sourcing figures
that are real, correctly dated, and reconciled where vendors disagree. Budget
your effort accordingly.

## Workflow

### 1. Establish the window

Run `date -u` — never assume today's date. The cutoff is normally ~20:15 ET
(≈00:15 UTC next day), roughly four hours after the US close, which captures the
close plus after-hours earnings reactions.

Find the previous edition's cutoff (the edition log in the user's spec doc, or
ask). Cover everything material since then, up to now. A Monday or post-gap run
covers the weekend/missed sessions too — give full depth to the most recent
session and condensed catch-up treatment to older ones. Never repeat items the
previous edition already carried.

### 2. Research — four parallel passes

Spawn one subagent per domain, in a single message so they run concurrently.
Parallel passes also cross-check each other: when two independently report the
same standing fact differently, that disagreement is a signal worth chasing.

| Pass | Weight | Covers |
|---|---|---|
| Equities & earnings | ~45% | Index closes, sector rotation, single-stock movers, earnings/guidance, analyst actions |
| Macro & policy | ~20% | Central banks, rate-path odds, inflation/jobs prints, trade/tariffs, day-ahead calendar with consensus |
| Commodities & FX | ~20% | Oil, gas, gold, copper; DXY and major crosses. No agriculture |
| Derivatives & positioning | ~15% | VIX and vol term structure, options flow/skew/gamma, CFTC CoT, funding. No credit spreads |

Give each subagent: the exact window and cutoff, what the previous edition
already covered (so it doesn't duplicate), the sourcing rules below, and an
instruction to report anything unverifiable rather than filling the gap.

Bias single-stock selection toward technology, SaaS/software, consumer staples,
consumer discretionary, telcos and large industrials — but include any name with
a genuinely large move regardless of sector.

Read `references/sourcing.md` before briefing the subagents. It holds the source
playbook: which vendors are reliable for what, the endpoints that work, the data
that is reliably unobtainable, and the traps (stale-date republishing, snapshot
quotes mistaken for closes) that have produced real errors.

### 3. Verify before you build

Reconcile conflicts first — this is cheap and catches errors that would
otherwise ship. Where two sources disagree, prefer the more authoritative, use
the better-corroborated figure, and disclose the disagreement rather than
silently picking one. Where a figure is single-sourced, say so inline.

Re-verify standing facts fresh from primary sources every single run — who
chairs the Fed, when the next policy meeting lands, whether a scheduled event
already happened. These drift, and a prompt's own framing is not a verified
source. Assuming one from memory has been the single largest error class in
this report's history.

Anything still unresolved goes in Annex A as unavailable. Never estimate,
infer, or reconstruct a number from memory.

### 4. Build

Read `references/format.md` for the locked structure, the CSS baseline, chart
selection guidance, and the layout traps. Then:

- Generate two charts with `scripts/make_charts.py` (edit the data arrays at the
  top). Chart 1 is always single-stock movers; pick chart 2 by what the day's
  dominant story actually is. Neither chart may duplicate a table.
- Write `briefing.html` following the structure in `references/format.md`.
- Assign source numbers sequentially as you draft, rather than renumbering
  afterward — post-hoc renumbering reliably produces orphaned references.

### 5. Check, render, verify

```bash
grep -c '~' briefing.html                    # expect 0 — write "approx." instead
python3 scripts/check_refs.py briefing.html  # inline [n] vs Annex B, both ways
node scripts/render_pdf.js briefing.html Daily_Economic_Briefing_YYYY-MM-DD.pdf
pdftoppm -png -r 72 Daily_Economic_Briefing_*.pdf page
```

Then actually read the page images. Page count alone does not tell you whether
a page broke badly or ran half-empty. Expect exactly 4 pages; if you get 5, the
cause is almost always a stray forced page break rather than genuine overflow —
check that before trimming copy.

### 6. Deliver

Deliver however the user has set up: sending the file in-session, committing it
into a repo's `editions/` folder and pushing, or both. If the user has a spec
doc with an edition log, append a row recording today's date, the cutoff, key
items covered, and open threads for next time — that log is what lets the next
run know where to start.

## Quality bar

The report earns trust by being right, not by being comprehensive. A disclosed
gap reads as rigor; a confident wrong number destroys the whole document's
credibility. When you catch an error from a previous edition, correct it
explicitly rather than quietly revising it — the user needs to know which
figures moved.

Interpretation belongs in the 60-second read at the top, and inline only where
a number is meaningless without context. Never as standalone labelled "so what"
lines.
