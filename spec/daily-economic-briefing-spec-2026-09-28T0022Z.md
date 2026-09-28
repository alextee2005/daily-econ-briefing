# Daily Economic Briefing — Standing Spec (v3)

Source of truth for the recurring Daily Economic Briefing. This version is
driven by a **GitHub Actions workflow** in `alextee2005/daily-econ-briefing`
(`.github/workflows/briefing.yml`), which runs Claude Code headlessly, commits
the PDF, and lets the existing delivery workflow forward it to Telegram.

Everything about *content*, *format*, *sourcing*, and *production* below is
carried forward unchanged from v2 — it took 21 editions to work out and remains
correct. Only the "how this runs" section has been rewritten to match the
pipeline that now executes it.

## How this runs (do not re-derive — this is already wired up)

Each weekday the workflow fires, decides whether there is anything to cover,
installs the toolchain, and invokes the `/daily-economic-briefing` skill
(vendored at `.claude/skills/daily-economic-briefing/`) with this spec as its
instructions. The run is **non-interactive** — there is nobody to ask. If a
figure cannot be verified, it goes in Annex A.

What the workflow hands each run, and what each run must produce:

1. **Inputs, supplied in the prompt:** the path to this spec (always the newest
   `spec/daily-economic-briefing-spec-<ISO>.md`), the edition date, the research
   window, and the list of NYSE sessions covered. Trust these over your own
   date arithmetic — but still run `date -u` and sanity-check.
2. **Output 1 — the PDF:** written to
   `editions/Daily_Economic_Briefing_YYYY-MM-DD.pdf`. A verification step then
   checks it is exactly 4 pages, that `check_refs.py` passes, and that there are
   zero stray `~` characters. Fix these before finishing, not after.
3. **Output 2 — the next spec:** written to a new
   `spec/daily-economic-briefing-spec-<ISO>.md` (the exact path is given in the
   prompt). This is the full spec carried forward, with standing facts
   re-verified, a new edition-log row appended, older editions condensed per the
   log's own convention, and open threads updated. You have free rein over its
   content — but it is the *only* instructions the next run will get, so never
   truncate a section or drop a rule you did not deliberately decide to change.
4. **Do not run any `git` command.** A later workflow step commits and pushes.
   Delivery to Telegram is handled downstream; there is no in-chat delivery step
   and no file to send.
5. **The environment is already prepared.** Chromium is installed and
   `CHROMIUM_PATH`/`PLAYWRIGHT_BROWSERS_PATH` is set — do **not** run
   `playwright install`. matplotlib and `pdftoppm` (poppler-utils) are present.

Operational setup (secrets, how to trigger a manual run, how to recover from a
failed run) lives in `docs/RUNBOOK.md`, not here.

## Two header details worth re-stating (both got wrong in earlier editions)

- **The document's date line is the EDITION date, not the session it covers.**
  Editions 20 and 21 both read "Tuesday 15 September 2026" and "Wednesday 16
  September 2026" matching their filenames; edition 22 used the session date
  instead and so carried the same headline date as edition 21. The window line
  is where the sessions covered belong, not the date line.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Worth reusing this phrasing pattern for
  any future single-session-plus-weekend edition.

## Schedule
Run every weekday. Pick the trigger's local time so the effective research
cutoff lands roughly 4 hours after the US market close (20:15 ET) — during
US daylight time that's 00:00 UTC; adjust for standard time. On Mondays
(or after any gap), cover the full window back to the previous edition's
cutoff, including the weekend.

## Standing facts — verify fresh every edition, never from memory
- **The September 2026 FOMC meeting (15–16 Sept) is fully resolved and does
  not need re-verifying again:** the Committee raised the federal funds target
  range 25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, unanimous 12-0, the
  first hike since 2023.
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed fresh again at
  edition 29 (Fri 25 Sept report) directly against federalreserve.gov's own
  FOMC calendar page (Dec 8-9 is the next SEP meeting after that). Re-confirm
  the date is still listed unchanged each edition as that meeting approaches —
  it is now roughly four weeks out, so keep checking every edition.
- **October-hike odds remain contested, not settled — re-verify fresh every
  edition and expect continued volatility into the 27-28 Oct meeting:**
  Polymarket held essentially flat over the Fri 25–Sun 27 Sept weekend at
  approx. 65% hike probability (25bp), approx. 34% no-change — little changed
  from edition 28's approx. 65-67% Thursday read. CME FedWatch's official tool
  would not load directly at edition 29 either; **secondary citations split
  three ways this run**: approx. 54% (almost certainly the same stale
  republished figure edition 28 already flagged), an undated approx. 69%, and
  a Friday-dated approx. 75.8% — treat the effective range as approx. 69-76%,
  broadly consistent with (if anything slightly above) edition 28's approx.
  73-73.5% read, not a clean reconciliation. **Kalshi direct fetch failed a
  seventh straight edition (23-29)** — now a firmly confirmed structural gap
  (HTTP 429 every time); keep attempting but don't spend much prose on it.
  Treat the true consensus as "hike-favored, roughly high-60s-to-mid-70s%,
  contested" rather than a single clean number until the CME/Polymarket gap
  narrows.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, etc.)
  every edition, exactly like any other data point.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026**, re-confirmed again at
  edition 29 directly against bankofengland.co.uk's own MPC-dates page (first
  re-check since edition 24 — the date is now under six weeks out, so
  re-confirm again next edition or two as it approaches).
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus — resolved, does not need re-verifying.
  **The Bank of Japan's next policy meeting is confirmed for October 29-30,
  2026**, re-confirmed again at edition 29 direct from boj.or.jp's own
  Monetary Policy Meeting schedule page (first re-check since edition 22 —
  now about a month out; re-confirm again next edition or two as it
  approaches).
- **The four-central-bank Thursday 24 September 2026 cluster remains fully
  resolved — closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% (matching an 18-economist
  Bloomberg survey) but signalled a greater chance of a Q4 hike; Banxico held
  at 6.50% unanimously; SNB held at 0% and raised its inflation forecasts
  (0.7%/0.8%/0.8% for 2026-28), confirmed directly against snb.ch. No fifth
  central-bank decision was identified in this window either.
- **New at edition 29 — August 2026 PCE inflation (Personal Income and
  Outlays) is confirmed for Tuesday 30 September 2026, 8:30am ET**, re-checked
  fresh against bea.gov's own release schedule. Consensus per multiple
  week-ahead previews: headline approx. +0.4% m/m / 3.7% y/y, core approx.
  +0.3% m/m / 3.3% y/y — note one desk (BofA) flagged that BEA's concurrent
  annual benchmark revisions could mechanically shave roughly 0.2pp off the
  y/y prints, which is worth a footnote if the actual print looks like a
  "beat" purely on a revised base. This is the week's key data risk; once it
  prints, re-confirm the actual figures and this thread can close.

## Role framing
Write as a top-tier economist / equity, commodity and derivatives investor,
sector-agnostic. Plain English. Single-stock focus (see coverage below).

## Coverage and weighting
Single stocks are the centre of gravity. Weight roughly: **~45% single
stocks & earnings, ~20% macro, ~20% commodities/FX, ~15% derivatives.**
1. **US equities & earnings (LEAD, largest section)** — index closes, sector
   rotation, single-stock movers, earnings since last cutoff, guidance
   changes, analyst actions. **Bias name selection toward:** Technology,
   SaaS/software, consumer staples, consumer discretionary, telcos, and
   large industrials. This is the section the user reads first — give it the
   most column space and the most "why it moved / read-across" depth.
2. **Macro & policy (condensed)** — keep only macro that plausibly moves
   single stocks or sectors: inflation prints, jobs, the Fed rate path,
   major central-bank and trade/tariff decisions, and the day-ahead calendar
   with consensus. Drop general-interest macro colour with no equity
   read-through.
3. **Commodities & FX (trimmed)** — oil, gas, gold, copper; DXY and major
   crosses. **No soft commodities/agriculture** (no corn/wheat/soybeans/
   WASDE — user not interested). Hard assets and FX only.
4. **Derivatives & positioning (condensed further)** — VIX and vol term
   structure, options flow/single-stock gamma or skew, CFTC CoT, funding in
   one line. **No credit spreads** (IG/HY OAS, issuance — user not
   interested).

## Confirmed format (locked)
- **Length:** 3 pages of briefing + 1-page annex. Do not exceed.
- **No "So what" lines.** Interpretation lives in the 60-second read at the
  top, and inline only where a number is meaningless without it — never as a
  standalone labelled line.
- **Sources:** numbered inline references `[n]` in a small blue superscript
  span, full list in Annex B. Never inline URLs in the body. **Each citation
  number gets its own `<sup class="ref">[n]</sup>` tag** — do not write
  `[26][27]` inside one sup tag; write `<sup class="ref">[26]</sup><sup
  class="ref">[27]</sup>`. `check_refs.py`'s regex only matches one bracket
  per sup tag, so combined-bracket citations silently fail the cross-check
  (this bit edition 22 — caught and fixed before render, avoid it from the
  start). Note that bracket text baked into a chart PNG's axis label (e.g.
  `[6]`) is NOT scanned by `check_refs.py` (it only reads the HTML, not image
  pixels) — keep those numbers consistent with Annex B by hand; the tool
  can't catch a mismatch there. **Also watch for a stray bracket typed outside
  a `<sup>` tag entirely** (e.g. `<sup class="ref">[27]</sup>[28]`) — edition
  27 caught one of these in its own draft before rendering; `check_refs.py`
  will not flag it since its regex only matches inside `sup class="ref"`
  tags, so a bare `[n]` slips through silently. Proofread citation-heavy
  sentences visually, not just via the script, when a sentence carries two or
  more consecutive citations. **A related trap surfaced at edition 28's own
  draft, worth naming explicitly: placeholder ref text (e.g. `[note1]`) typed
  during drafting and never swapped for a real number.** `check_refs.py`'s
  regex requires `\d+` inside the brackets, so a non-numeric placeholder like
  `[note1]` simply won't match either the inline or Annex-B regex — it won't
  show up as "missing" or "unused," it just silently doesn't count. **Edition
  29 hit a related but distinct trap worth naming too: reserving Annex B
  numbers (e.g. `[32] (reserved)`) for sources planned but not used** — these
  show up as "listed but never cited" in `check_refs.py`'s output (correctly
  flagged that time), but the fix is to delete the unused placeholder entries
  outright rather than leave reserved gaps in the numbering; Annex B numbers
  do not need to be contiguous, only matched 1:1 against inline citations, so
  deleting an unused reserved number and leaving a gap (e.g. jumping from [31]
  to [33]) is completely fine and simpler than renumbering everything after
  it.
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart 2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes). **Chart
  placement is editorial, not fixed to Section 2** — edition 24 placed a
  CFTC-positioning chart #2 in Section 5 (Derivatives) rather than Section 2,
  since that's where the content actually belongs; the asset/skill template's
  `chart2_panel` position under the Equities heading is just a default for the
  common case (sector rotation), not a hard rule.
- **Tilt:** market-wide. No portfolio tilt, no holdings commentary.
- **Window:** everything since the previous edition's cutoff. On Mondays
  (or after any gap) this includes the weekend/missed sessions.
- **Data gaps:** keep Annex A. State plainly what could not be verified.
  Never estimate, infer, or fill from memory.
- **Page margins:** 1 inch (25.4mm) top and bottom, 13mm left and right.
- **Text alignment:** body prose (paragraphs, bullet lists) justified.
  Tables, headers (h1/h2/h3), the snap-grid tiles, the meta line, and Annex
  B's narrow 3-column source list stay left-aligned — justifying short table
  cells or a dense multi-column list produces ugly ragged spacing.

## Hard rules
- Every data point needs a named source. If unverifiable, say so in Annex A
  rather than producing a plausible-sounding number.
- Where sources disagree, use the more authoritative one **and** disclose
  the disagreement. AP's "How major US stock indexes fared" and the Reuters
  market wrap are normally the most reliable for index closes — but check
  they're actually indexed for the target date before relying on them; this
  has occasionally failed to post in time (15 Sept gap at ed. 21, 22 Sept gap
  at ed. 26 requiring the Yahoo Finance/FRED fallback chain both times).
  **Editions 27, 28 and 29 are all clean counter-examples worth keeping in
  mind**: all three posted an AP wire in time (ed. 28 via WTOP/ABC News, ed.
  29 via WTOP again with an explicit on-page timestamp), and ed. 28's and ed.
  29's AP figures both cross-checked exactly against an independent second
  pull (Yahoo Finance) — so treat AP/Reuters as "try first, expect to
  sometimes need the fallback chain," not as unreliable by default. Always
  have Yahoo Finance + FRED ready as the working fallback regardless of which
  way this edition goes.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example (Trefis "Market Movers" re-serving
  Friday 18 Sept's figures under a Monday 21 Sept URL); edition 26 caught
  another (several "AP" reposts of Monday 21 Sept's numbers under a Tuesday
  22 Sept dateline); edition 27 caught a third (a techflowpost article
  reproducing Tuesday's numbers under a Wednesday URL); edition 28 caught a
  fourth and fifth in the same run (a WebSearch AI summary mislabeling
  Wednesday's VIX close as Thursday's; a 24/7 Wall St. article restating
  Wednesday's Airbnb close as current). **Edition 29 is the first clean
  edition in six straight: the equities research pass explicitly checked for
  stale-date republishing on every figure and found none** — one
  unsourceable aggregator's Russell 2000 figure (2,844.32) was rejected in
  favor of two independently-agreeing, explicitly-timestamped sources, but
  that was a bad number, not a stale-date repost. **Do not read this as the
  problem being solved — it is a six-edition tell, not a permanent fix —
  keep checking every figure's session date every edition regardless of how
  clean the last one was.** A same-day close and a next-day
  after-hours-triggered move can legitimately combine into one large
  single-day % change — edition 24's Xenon Pharmaceuticals -30.7% Friday move
  is the reference example. Check whether a headline % move is measured
  close-to-close before assuming two reports conflict. **The intraday-vs-close
  divergence trap (distinct from stale-dating) is still very much alive**:
  Worthington Enterprises (ed. 26), Paychex/Cracker Barrel (ed. 27), Oracle
  (ed. 28), and at **edition 29 two clean examples in one run** — Akamai's
  reported intraday move as large as +16.4% vs. its actual +3.20% close, and
  a cluster of storage names (Seagate, Western Digital, SanDisk) reported by
  several aggregators as down sharply "ahead of the open" Friday that
  actually closed **up** (+1.20%/+1.44%/+1.38%) after an intraday reversal —
  a stronger version of the pattern than a mere magnitude gap, since the
  pre-market snapshot had the *direction* wrong, not just the size. Treat a
  stockanalysis.com (or equivalent timestamped) closing print as authoritative
  over any pre-market, intraday, or "ahead of the open" figure, and
  cross-check against a second independent source when available.
- Do not repeat items already carried in the previous edition.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. Check whether two conflicting prices are actually two different
  instruments/timestamps before treating it as a sourcing failure.
  **The Kitco-vs-USAGOLD gold split, treated as resolved since edition 28
  (gap had narrowed to $0.16), ticked back up to approx. $4.78 at edition
  29** — still far short of the approx. $50 gap seen three editions ago, so
  this is normal vendor noise, not a reopened divergence; no need to revert
  to "unreconciled split" framing unless the gap widens materially again.
  Similarly, **a price level can be correct while a vendor's stated %-change
  is wrong** if the vendor used a different prior-day base — always
  sanity-check that a stated price and stated % change reconcile
  arithmetically against the prior session's logged close. **New at edition
  29, a related but distinct pattern worth naming: a vendor's own
  self-reported day-over-day % change can differ from what you'd compute
  against the previously-logged cross-edition baseline, because the vendor is
  computing against its own internal reference, not your logged figure** —
  USAGOLD's Friday close of $4,280.19 was reported by USAGOLD itself as
  "+$4.96 (+0.12%)," but that implies a Thursday baseline of about $4,275.23,
  not the $4,273.36 logged from edition 28's own USAGOLD pull. The gap is
  trivial (about $2) and not worth chasing, but when reporting a vendor's own
  stated %-change, note whether it was computed against its own internal
  baseline or the report's logged cross-edition baseline if the two might
  diverge, rather than assuming they're the same calculation.
  **The oil contract-month-roll trap, absent at edition 28, also did not
  recur at edition 29** — Friday's WTI/Brent both stayed cleanly on the same
  November contract as Thursday's close, with the reported dollar and
  percentage changes reconciling exactly against the prior logged closes.
  The general lesson stands: check for a contract-month roll whenever a
  commodity price looks discontinuous, but don't assume the trap recurs just
  because it has before — it is now absent in two of the last six editions.
- **New genuine cross-source conflict surfaced at edition 29, worth watching
  as its own thread: DXY vs. its own component FX crosses.** Two independent
  sources (Yahoo Finance and Investing.com) agreed with each other that
  Friday's DXY fell to 100.97 (approx. -0.31/-0.32%) — but that move is
  directionally opposite to Friday's own EUR/USD (-0.06%), GBP/USD (-0.24%)
  and USD/JPY (+0.35%) readings, which all point to modest dollar *strength*,
  not weakness. This is a step beyond edition 27/28's simple magnitude
  mismatches — the two DXY sources agree with each other but disagree with
  the basket's own visible components. Disclosed as an unreconciled
  discrepancy rather than forced to one story (plausible but unconfirmed
  explanation: other basket currencies — CAD, SEK, CHF — moved against the
  dollar enough to flip the index). Watch whether this recurs or was a
  one-off data artifact.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done** — and if it reports 0 inline citations found
  while your Annex B clearly has entries, check for the combined-bracket
  `[n][m]` mistake above before assuming something else is wrong. Also
  remember it only scans HTML text — a citation number baked into a chart
  PNG's label is invisible to it, and so is a bare `[n]` typed outside any
  `<sup>` tag, and so is a non-numeric placeholder like `[note1]`. **And, per
  the new edition-29 trap above, so is a genuinely unused but present Annex B
  placeholder (e.g. `(reserved)`) — that one the script DOES catch (as
  "listed but never cited"), so this is really a reminder to run the script
  and act on that specific line of its output, not skip past it.** Also
  remember it flags Annex B entries that were drafted but never actually
  cited inline — edition 26 hit this with four single-stock sources, edition
  28 with one prose-only source (Washington Post), and edition 29's reserved
  placeholders (see above) are the same failure mode by a different route —
  caught and fixed each time by running the check before declaring done.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Edition 29 still caught one stray `~` in its own draft** (in a
  disclosure-box bullet written during a late editing pass, not the main
  drafting pass) — a reminder that the late-added lines (corrections,
  disclosure-box notes) are where a stray one usually slips in even when the
  main body was written cleanly from the start.
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 24 needed CFTC leveraged-funds
  positioning normalized "as % of open interest" but couldn't source total OI
  for the exact CoT date; it substituted "net position as % of the
  leveraged-funds category's own gross long+short" instead. **Edition 29 had
  a different, milder version of this problem: fresh CFTC CoT data posted
  (covering Tue 22 Sept) on this Monday-window edition, which per the chart-2
  guidance below would normally point to the ES/NQ/RTY positioning chart —
  but only ES's gross long/short breakdown (and, from a second research pass,
  its total open interest) was actually obtained; NQ and RTY were only
  reported as net positions, with no gross or OI breakdown, making a
  consistent normalization impossible across all three indices.** Rather than
  build a chart mixing normalization methods across bars (OI-normalized ES
  next to un-normalizable NQ/RTY net contracts), edition 29 reported the CoT
  positioning as prose in Section 5 instead and used the SPDR sector-ETF
  proxy as chart 2, since Friday's actual dominant story was the sector
  rotation, not three-session-stale positioning data. **Lesson: "fresh CoT
  data on a Monday/weekend edition" is a strong default for chart 2, but not
  an automatic one — check that you can get a consistent normalization
  (or at least a consistent unit) across all the instruments you'd chart
  before committing to it, and fall back to prose plus the standing
  sector-proxy default if you can't.** If this recurs, it may be worth having
  the macro or derivatives research pass explicitly ask CFTC.gov's own report
  pages for the OI/gross-long-short breakdown on all three of ES, NQ and RTY
  (not just ES) up front, rather than discovering the gap after the fact.
- **When an "optional" filler element (e.g. a levels table) would just
  restate the same instrument list already in a main table with one extra
  column, that's still legitimate as long as the extra column is genuinely
  additive** (editions 25 and 28 both added a prior-session-baseline-vs-close
  levels table to a short page 3) — don't reject the idea purely because the
  instrument list overlaps; check whether the *added* column carries real
  information first. **Edition 29 did not need this padding at all** — page 3
  filled cleanly from content alone (Section 3, 4, 5 and 6 prose plus the
  day-ahead table and sector-setup bullets), the same pattern seen at
  editions 26 and 27. This is now the third time out of the last four editions
  that no filler was needed — keep reaching for the optional levels table
  only when page 3 actually runs short after the two default end-of-Section-6
  blocks, not as a routine addition.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` delayed-quotes JSON endpoint first — it often
  returns VIX, VIX9D, VIX3M, VIX6M, VVIX and SKEW directly, but has (at least)
  three observed failure modes: (a) a full clean sweep with genuinely fresh
  timestamps on every series, (b) the more common "thin-series-stale"
  pattern, (c) total failure, where every series is stale. **Editions 28 and
  29 both got a full clean sweep** — every one of VIX/VIX9D/VIX3M/VIX6M/VVIX/
  SKEW carried a same-day `last_trade_time`, verified individually per series
  via a raw `curl` pull (not a tool-summarized fetch — see Hard rules above
  for why) both times. Two consecutive clean sweeps is encouraging but not a
  guarantee — keep checking `last_trade_time` on each series every time.
  Also note a `prev_day_close` field bug, now observed **eight editions
  running (22-29)**: it duplicates the day's own `close`/`current_price`
  rather than giving a real prior-day reference, corrupting the feed's own
  `price_change`/`price_change_percent` fields too — **never quote the
  feed's `price_change`/`price_change_percent` fields directly; always
  compute day-over-day % change manually against the previous edition's
  logged close.** Fall back to news coverage if the feed is stale, and
  disclose it as single-sourced. **The VIX9D-vs-spot-VIX front-end inversion
  flagged at edition 28 (spot VIX 15.67 above VIX9D 14.11) did NOT recur at
  edition 29** — Friday's term structure reverted to a normal upward slope
  (VIX9D 12.76 < VIX 14.87 < VIX3M 17.93 < VIX6M 20.01). Treat Thursday's
  inversion as resolved/noise; this thread can close unless it reappears.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table
  and (absent fresher CoT data or another dominant story) chart #2. Worked
  cleanly again at editions 26, 27, 28 and 29. **Stockanalysis.com
  single-stock pages are also the standing default for pinning an exact
  closing price/% change on any individual mover** — editions 26 through 29
  all used direct fetches to it to resolve conflicting intraday-move
  percentages (edition 29: Akamai's "+16.4% intraday" vs. its actual +3.20%
  close, and the STX/WDC/SNDK pre-market-vs-close reversal — see Hard rules
  above). Worth doing proactively for any mover whose research-pass figures
  disagree by more than a rounding error. Note that a headline wire's own
  GICS sector-index percentages can differ slightly from the SPDR ETF
  price-change figures (a normal index-vs-ETF-price methodology gap); keep
  using the SPDR ETF figures as the table's primary numbers.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. Not chased at
  edition 29 — no research pass flagged a need for it this run.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — now recurred at editions 22, 24-29
  (seven straight, still worth a quick attempt each time in case it
  recovers). **zerogex.io is now confirmed across three straight clean
  editions (27, 28, 29)**: edition 27 reconciled well against the close,
  edition 28 likewise, and **edition 29 gave a third dated read but with a
  striking magnitude jump — net SPX GEX +$32.56bn, roughly 9x edition 28's
  +$3.63bn.** Directionally explicable (Friday's sharp VIX decline pushes
  dealers deeper into positive gamma), but the size of the jump was flagged
  rather than passed through silently, and it's worth a skeptical check next
  edition: if the pattern of large, hard-to-sanity-check swings continues,
  zerogex.io's precision (not just its directional usefulness) should be
  revisited. Continue treating it as the standing default source for dealer
  gamma, but don't stop cross-checking its output against the day's actual
  index close for plausibility.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Edition
  28's secondary citations split between approx. 54% (likely stale) and
  approx. 73-73.5%; **edition 29's split three ways instead (approx. 54%,
  69%, 75.8%)** — the 54% figure looks like the same stale republish
  persisting across two editions now, worth naming explicitly as "the
  recurring stale ~54% figure" if it shows up a third time. Keep treating CME
  FedWatch as needing a disclosed range, not a single figure.
- **Kalshi direct fetch:** now rate-limited (HTTP 429) for **seven straight
  editions (23-29)** — a confirmed structural gap, not transient. Keep
  attempting each edition (it may recover), but a one-line "failed again,
  Nth straight edition" is sufficient prose.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  eight editions running (22-29)** — treat as durable; default straight to
  the fallback chain. Shanghai Metals Market (metal.com) has also now failed
  **eight editions running (22-29)** — skip it entirely and go straight to
  Westmetall.com, which has now worked cleanly **eight editions running** as
  the fallback. Disclose whichever was used. Because the fallback chain can
  change edition to edition, treat any day-over-day copper % change built
  across two different sourcing chains as approximate.
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) worked
  cleanly for the prior completed day at edition 29, resolving Thursday 24
  Sept's previously-unposted 2-year/10-year closes (4.87%/5.18%), cross-checked
  against FRED. **New wrinkle at edition 29: an initial fetch of the
  rendered HTML table returned garbled/mis-mapped figures (values shifted
  into the wrong maturity columns); re-pulling the raw CSV directly resolved
  it cleanly and matched FRED and a CNBC news figure exactly.** Prefer the
  CSV endpoint over the HTML TextView page going forward if both are
  available — the CSV is less prone to this column-mapping problem. FRED
  (fred.stlouisfed.org, DGS10/DGS2) remains the reliable secondary route for
  the most recently *completed* trading day's yields (T+1 lag, same as
  official H.15) — confirmed working again at edition 29 as a cross-check
  against the Treasury CSV. Expect the *current* session's own close to
  simply not be posted yet via either route (same T+1 lag) rather than
  forcing a same-day read.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. **A new report posted on schedule at edition
  29** (published Fri 25 Sept, dated Tue 22 Sept, a 3-day lag) — confirmed via
  direct fetch: equity-index Asset Managers net long approx. 934,000-936,000
  ES contracts (two research passes' independent pulls agreed closely) vs.
  Leveraged Funds net short approx. 375,600-376,000; VIX futures
  non-commercial net short approx. 79,300, a modest reduction in short-vol
  positioning from the approx. 86,600 logged for 15 Sept. **Only ES's gross
  long/short breakdown and total open interest (approx. 1.9mn contracts) were
  obtained this run — NQ and RTY were only reported as net positions, without
  OI or gross breakdowns** (see Hard rules above for how this affected chart
  selection). Next report due **approx. Friday 2 October 2026**, which would
  cover Tuesday 29 Sept — check for it fresh next edition, and if a CoT-based
  chart is wanted again, try to get OI/gross-long-short for all three of
  ES/NQ/RTY up front this time, not just ES.
- **GBP/USD and EUR/USD clean close:** fully resolved since edition 26 —
  Yahoo Finance as primary works cleanly, confirmed again at editions 27, 28
  and 29. **New at edition 29: a DXY-vs-FX-crosses directional conflict** —
  see Hard rules above for the full writeup. This supersedes edition 27/28's
  magnitude-mismatch observations as the more precise description of what's
  going on: it isn't that DXY's move is a different *size* than the crosses
  imply, it's that two independent DXY sources both show it moving the
  *opposite direction*. Treat as an open, unresolved thread; watch whether it
  recurs.
- **Gold/silver clean close on a non-event day:** **this thread remains
  substantially resolved, with a minor caveat.** The Kitco-vs-USAGOLD gap
  that first appeared at edition 26 (approx. $50) narrowed to approx. $7 at
  edition 27 and to $0.16 at edition 28; **at edition 29 it ticked back up to
  approx. $4.78** — still a small, normal-range vendor spread, not a reopened
  divergence, so continue treating the split as resolved/non-newsworthy
  unless it widens back toward the $20-50 range seen historically. Separately,
  note that a vendor's own self-reported day-over-day %-change can imply a
  slightly different prior-day baseline than what's logged from that same
  vendor the previous edition (see Hard rules above, new at edition 29) — not
  worth chasing given the headline gap is small, but worth remembering when
  quoting a vendor's own "+X%" figure verbatim.
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue — confirm on the BLS/Fed release schedule
  rather than assuming a date. **PCE inflation:** confirmed for Tuesday 30
  September 2026, 8:30am ET (see Standing facts above) — re-confirm once more
  as that date arrives, then this thread can close.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  **substantially resolved at edition 29.** Edition 28 found the same URL
  giving two wildly different totals for what should have been the same
  Wednesday figure (902,421 vs. 13,781,355, roughly 15x apart). Edition 29
  identified the mechanism directly from the page's embedded data payload:
  **the URL hosts several distinct, stacked category tables** — Sum of All
  Products, Index Options, Equity Options, Exchange-Traded Products, plus
  instrument-specific tables (e.g. Cboe Volatility Index/VIX, SPX+SPXW) —
  each with its own volume and put/call totals. Friday's Sum-of-All-Products
  total (13,939,864) sits in the same range as the previously-logged "13.78m"
  figure, suggesting that earlier reading was the all-products category; the
  much smaller 902,421 figure still cannot be matched to any category visible
  at edition 29 and **remains genuinely unattributed** — treat it as a
  standing unresolved data point, not comparable to either all-products
  total, until a future edition manages to identify exactly which table
  produced it (if it recurs). **Going forward: always state which specific
  category/table a Cboe options-volume figure comes from** (e.g. "VIX-specific
  volume" vs. "Sum of All Products") rather than citing a bare total — this
  page's ambiguity is now well-documented and citing an unlabeled number from
  it is a known trap.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable at edition 29.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22) — either find a citable
  benchmark before reaching for that chart type, or stick to describing
  implied-vs-realized in prose without the third bar. Not attempted again at
  editions 23-29.
- **CFTC total open interest by instrument/date** (needed to normalize
  positioning "as % of open interest"): **partially resolved at edition 29**
  — ES's total OI (approx. 1.9mn contracts) was obtained directly from
  cftc.gov, but NQ's and RTY's were not pulled this run (see Hard rules and
  the CFTC CoT entry above). Next time an OI-normalized CoT chart is wanted,
  fetch OI/gross-long-short for all three of ES, NQ and RTY explicitly up
  front rather than assuming one contract's availability implies the others'.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear** — editions 27, 28
  and **29** all confirmed several rating changes (direction + firm name)
  without being able to pin an exact dollar price target for all of them.
  **Edition 29's clearest example: Costco's post-earnings analyst reaction** —
  a bullish Goldman Sachs note was well corroborated directionally, but its
  exact revised price target could not be pinned down amid conflicting
  figures across sources (some evidently misdated/unrelated), and Wells Fargo
  and Bernstein price-target figures were blocked behind 403 errors entirely.
  Report the rating direction and firm with confidence; treat a missing
  dollar target as a normal gap to flag, not something to chase hard, unless
  the name is the edition's dominant story.
- **New at edition 29 — single-aggregator-only movers lists need individual
  verification, not bulk acceptance.** A long secondary list of purported
  Friday movers (including names like MRNA, SWKS, FLEX, HPQ, NTAP, FIX) came
  from one unverified aggregator; two other names from that same list (Clorox,
  and the STX/WDC/SNDK cluster) were independently confirmed **wrong on
  direction** at the close. Rather than spend the remaining research budget
  verifying each name individually, edition 29 flagged the entire remaining
  list as unverified in Annex A instead of reporting any of it as fact. **This
  is the right call when time-constrained**: one aggregator getting two
  checked names wrong is a strong signal the rest of its list isn't reliable
  either, and Annex A exists exactly for this situation.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. `figsize=(9.8, 1.95)` and
  `(9.8, 1.55)`, `font.size 9.6`, dpi 210, `width:100%` in the page.
- PDF: HTML → Chromium print-to-PDF via Playwright. Launch Chromium with an
  explicit `executablePath` (check the environment for the installed
  Chromium build path) and `--no-sandbox`. Do not run `playwright install`.
- Set margins in **exactly one place** — either the CSS `@page` block or the
  Playwright `page.pdf()` margin option, never both (they stack and double
  the margin). Passing `{top:'1in', bottom:'1in', left:'13mm', right:'13mm'}`
  via `page.pdf()` with the HTML body at `margin:0; padding:0` and no CSS
  `@page` block is the pattern that has worked reliably.
- **Only ONE forced `page-break-before` in the whole document: immediately
  before Annex A.** Let sections 1–6 flow naturally — a stray extra break
  produces a 5-page PDF with a mostly-blank orphan page. `grep -n
  'pagebreak'` before troubleshooting anything else if page count looks
  wrong — check specifically for `<div class="pagebreak">` occurrences (the
  CSS rule definition itself also contains the string "pagebreak," so a raw
  `grep -c` will show 2 for a correctly-built document). **A 5-page render is
  not always a stray break** — editions 24 and 28 both hit 5 pages with only
  the one correct pagebreak present; the cause was genuine copy overflow in
  both cases. Edition 29 rendered clean at 4 pages on the first try with the
  standard single pagebreak and no filler content needed.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Editions 25 and 28 both hit a visibly short page 3 on the first render
  despite passing the 4-page check, fixed with an optional levels table.
  **Edition 29 did not have this problem** — page 3 filled naturally from
  Section 3-6 content, matching editions 26 and 27's experience. This is now
  3 of the last 4 editions where no padding was needed — don't add the
  optional levels table reflexively; check whether page 3 actually runs short
  first.

### Working settings (current baseline — confirmed stable across many editions under the 1in/1in/13mm/13mm margins)
- Letter size. Body **8.0pt** / line-height **1.20**, serif; `p`
  margin-bottom **2.4px**.
- h1 14.5pt; h2 **9.1pt, margin 4px 0 1.6px 0**; h3 **7.9pt, margin 2.4px 0
  1px 0**.
- Tables **7.4pt**, **1.8px cell padding**, table margin-bottom **3px**.
- Snap-grid tiles: 7.4pt label / 9.4pt value / 7.3pt change; tile padding
  **2px 4px**, snapgrid margin-bottom **3.5px**.
- Bullet lists (`ul.bullets`): **1.4px** margin-bottom per `li`.
- Annex A: two columns at 7.1pt, `break-inside:avoid` per `li` (left-aligned
  — reads cleanly at this width; justify only if it still looks clean after
  testing).
- Annex B: three columns at 5.5pt, left-aligned.
- Content budget: 60-second read (5 items); equities as the largest block
  plus the movers table; macro/commodities/derivatives tighter; **a "This
  week's known catalysts" table plus a "Sector setup we take into [session]"
  bullet list at the end of Section 6 by default** for any single-session or
  weekend-window edition (skip only if a multi-session catch-up already fills
  3 pages). **An optional "Commodities & FX levels" table (~9-10 rows, not
  more)** at the end of Section 4 is available as padding if page 3 runs
  short after the two default blocks — reach for it only when content alone
  doesn't fill the page (needed at editions 25 and 28; not needed at 26, 27
  or 29 — 3 of the last 4 editions have filled page 3 from content alone).
  Always re-render immediately after adding this table to confirm the page
  count if it is used, rather than assuming a "moderate" row count is safe
  (edition 28's first attempt at 12 rows overshot to 5 pages; 10 rows fixed
  it). Conversely, **if page 3 overflows by a handful of lines**, the
  cheapest trims are: shortening day-ahead table cell text, cutting one
  "sector setup" bullet or merging two into one, tightening the last prose
  paragraph in Section 5, or trimming rows from the optional levels table if
  one was added.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 3x between
  the largest and next-largest mover does not need capping — confirmed again
  at edition 26 (VKTX +35.67% vs. next-largest ONON +7.58%, about 4.7x, left
  uncapped since "order of magnitude" (approx. 10x) is the real threshold),
  edition 27 (PAYX -8.77% vs. EXPE -7.72%, about 1.14x), edition 28 (MGM
  -10.99% vs. META +4.50%, about 2.4x), and **edition 29 (TWLO -7.96% vs.
  next-largest DELL +5.01%, about 1.6x — also left uncapped)**. The rule has
  still not yet had a genuine 10x+ case to test.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — **used for a fifth consecutive
edition at edition 29**, for a Friday relief-rally rotation into Industrials/
Technology and out of Energy/Communication Services; also used at edition 28
for a Meta-Muse-driven rotation, edition 27 for a rate-spike-driven rotation
into defensives, edition 26 for a financials-vs-materials reversal, and
edition 25 for a chip-led rally — this remains a reliable, low-risk default).
Fresh CFTC CoT data on a Monday/weekend-window edition → the ES/NQ/RTY
asset-manager-vs-leveraged-funds positioning chart, **normalized as % of open
interest if that figure can be sourced for all instruments being charted; if
not, a category's own net-position-as-%-of-its-own-gross-long+short is an
acceptable, honestly-labelled substitute — but check that a *consistent*
normalization (or at least a consistent unit) is available across every
instrument in the chart before committing to it.** Edition 29 had fresh CoT
data on a Monday-window edition (matching this scenario on paper) but only
had a full OI/gross breakdown for ES, not NQ or RTY, and the dominant story
of the session was genuinely the sector rotation, not stale (3-session-old)
positioning data — so it reported CoT positioning as prose in Section 5
instead and used the sector-ETF proxy for chart 2. **Treat "fresh CoT data"
as a strong candidate for chart 2, not an automatic trigger** — verify data
completeness and genuine narrative relevance first. A single dominant
earnings print with a clean, well-sourced implied-vs-realized-move story → a
three-bar implied/historical-average/realized move chart (the
historical-average leg has never actually been sourced successfully — see
Known-hard-to-source above). A genuine multi-sector broadening/deepening
selloff across consecutive sessions → the sector-ETF proxy rendered as a
grouped (day-over-day) bar instead of single-day. A holiday-window preview
edition with no fresher data → VIX futures term structure with event
annotations. When chart #1 (movers) already covers the earnings/single-name
story, the sector proxy is a good complementary choice even on a stock-heavy
day — editions 25 through 29 have all used exactly this combination (movers
as chart #1, sector rotation as chart #2) with the two stories reinforcing
rather than duplicating each other every time. **Chart #2's placement in the
document should follow its content, not a fixed section** — a
CFTC/positioning chart reads better in Section 5 than Section 2 (edition 24).

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–27 (condensed):** established the format (edition 1 baseline;
edition 2 revised weighting/sourcing; edition 3 fixed the ET-cutoff math and
introduced the multi-session-gap and duplicate-fire handling conventions);
corrected the Fed Chair premise to Kevin Warsh at edition 6 (re-verified
every edition since); tracked the Jackson Hole keynote (28 Aug, hawkish) and
the resulting rate-odds repricing through editions 10–18; resolved the
SPDR-sector-ETF-proxy and CBOE-feed (`last_trade_time` check) sourcing
techniques at editions 10–11; corrected the FOMC decision date to Wednesday
16 Sept at edition 18 (superseding editions 15–17's Tuesday assumption).
Major single-name events across editions 1-21: Moderna's melanoma-data spike
and unwind (ed. 4–5), Nvidia's Q2 FY27 beat and Hugging Face acquisition (ed.
8–9), Walmart/Advance Auto Parts/Deere earnings reactions (ed. 5), the
PayPal-Stripe deal collapse (ed. 10), California SB 492 hitting utilities
(ed. 11), an Iran/Hormuz escalation cycle running through the whole period
and repeatedly driving oil, Lululemon's guidance-slash collapse (ed. 15),
Canada's approx. $27.6bn retaliatory tariffs taking effect (ed. 16), Apple's
first Ternus-era product event (ed. 17), Oracle's Q1 FY27 beat with a
vol-crush AH reaction (ed. 18), the Fed debate flipping from "hold vs. cut"
to "hold vs. hike" on hot core CPI (ed. 19), Anthropic CEO Dario Amodei's
AI-safety essay driving a chip-selloff/cybersecurity-rally rotation (ed. 20),
edition 21's Tuesday 15 Sept report (day one of the two-day FOMC meeting):
S&P 7,585.73 (-0.45%), 10-year spiked intraday to approx. 5.045% (a 2007
high); edition 22 (Thu 17 Sept, covering Wed 16 Sept FOMC day): the Fed
hiked 25bp to 3.75%-4.00%, unanimous 12-0, equities reversed hard to close
lower (S&P 7,551.81 -0.4%), 10-year first closed above 5% since 2007;
edition 23 (Fri 18 Sept, covering Thu 17 Sept): equities reversed most of the
post-FOMC selloff (S&P 7,637.76 +1.1%), Bank of England held at 3.75% (6-3),
Generac +18.3%, Lucid +10.0%; edition 24 (Mon 21 Sept, covering Fri 18 Sept
triple witching + weekend catch-up): approx. $7tn September triple-witching
notional expired alongside the quarterly rebalance, Xenon Pharmaceuticals
-30.7%, Warren Buffett stepped down as Berkshire chairman, Bank of Japan
hiked 25bp to approx. 1.25% (31-year high, 7-2 split); edition 25 (Tue 22
Sept, covering Mon 21 Sept): a broad chip-stock rally (Intel +12.0%, AMD
above a $1tn market cap, Arm +16.6%) pushed the Nasdaq to a record 27,122.09
(+2.26%), the quarterly S&P 500/400/600 and Nasdaq-100 rebalance took effect;
edition 26 (Wed 23 Sept, covering Tue 22 Sept): a financials-led sector
rotation — S&P effectively flat at 7,764.64 (-0.00%), Dow -0.36% to
51,863.69 on a bank selloff, Nasdaq a second consecutive record close at
27,244.28 (+0.45%); Viking Therapeutics +35.67% was the standout mover; the
five-central-bank Thursday/Friday cluster was first dated here; gold showed
a genuine Kitco-vs-USAGOLD split (approx. $50 apart, later resolved). Edition
27 (Thu 24 Sept, covering Wed 23 Sept): a broad risk-off session — S&P -0.75%
to 7,706.03, Dow -0.68% to 51,511.59, Nasdaq -1.13% to 26,936.04, driven by
the 10-year spiking to a 19-year high (approx. 5.09-5.14%) after a hot flash
PMI and Fed Governor Barr's hawkish remarks; the "Meta Muse" AI-agent
disintermediation theme rotated from banks into online travel names (Expedia
-7.72%, Airbnb -7.56%, Booking -5.07%) and was independently corroborated;
Paychex -8.77% (earnings-quality concerns), Cracker Barrel +4.49% (EPS beat);
gold's Kitco-vs-USAGOLD split narrowed to about $7; VIX closed 15.18
(+6.83%) on a CBOE feed "full stale sweep" failure; zerogex.io gave its
first working dealer-gamma read.

**Edition 28 (condensed)** — Fri 25 Sept 2026 report covering Thursday 24
September 2026, the window's one NYSE session. A whipsaw session that closed
almost exactly flat: S&P 500 -0.1% to 7,704.13, Dow -0.3% to 51,349.98,
Nasdaq +0.1% to 26,939.37, Russell -0.1% to 2,835.57, confirmed via AP/WTOP
cross-checked against Yahoo Finance. Sector leadership flipped to
Communication Services (XLC +1.27%) leading on a Meta rally, with Materials
and Utilities lagging. Single-name stories: MGM Resorts -10.99% (Barry
Diller's People Inc. withdrew its take-private bid), Oracle -3.47% (Blue
Owl/Stargate New Mexico force-majeure notice), Darden -3.02% (EPS/revenue
miss), Paychex -2.78% (second-day continuation), Costco -0.91% in the
regular session ahead of an after-close Q4/FY2026 beat (EPS $6.75 vs. approx.
$6.55 consensus) that drew only a muted AH reaction (fuller verdict left as
an open thread, resolved at edition 29), and Meta +4.50% (best month since
2013) on Muse AI-agent monetization details at Connect, which let Wednesday's
travel-stock selloff partially reverse. All four previewed Thursday
central-bank decisions (Norges Bank hike, Riksbank hold, SNB hold, Banxico
hold) were confirmed against primary sources — this thread is now closed.
The Trump-Xi Washington summit culminated Thursday; per Bessent, the US-China
trade truce was extended to January 10, 2027. October-hike odds jumped
(Polymarket to approx. 65-67%) and CME FedWatch secondary citations
diverged sharply (approx. 54% vs. approx. 73-73.5%), unreconciled. Oil
rallied on a Houthi strike on Saudi Arabia before paring on US-Iran talk
(Brent +3.4% to $106.60, WTI +2.7% to $94.61). Gold's Kitco-vs-USAGOLD split
closed to just $0.16. The CBOE feed gave a full clean sweep (VIX 15.67
+3.23%) but flagged an unusual front-end VIX9D inversion (resolved as noise
at edition 29). Cboe's options-volume page surfaced an unresolved 15x
same-page discrepancy (902,421 vs. 13,781,355 for Wednesday), substantially
explained at edition 29 as multiple stacked category tables on one URL.
zerogex.io gave a second consecutive clean dealer-gamma read. 43 sources,
zero mismatches, zero stray tildes. Page 3 briefly overshot to 5 pages after
an over-long levels table; trimmed to 10 rows and re-rendered clean.

**Edition 29 (most recent — full detail)** — Mon 28 Sept 2026 report covering
Friday 25 September 2026, the window's one NYSE session (markets closed the
weekend), research window Thu 24 Sept 20:00 ET through Sun 27 Sept 20:22 ET.
Verified the two structural header rules again: date line reads the edition
date (Monday 28 September 2026), not the session date; window line states
the given research-window start (Thu 24 Sept 20:00 ET) with the actual
session covered noted parenthetically.

A broad relief rally closed out the week: S&P 500 +0.5% to 7,743.41, Dow
+0.9% to 51,828.62, Nasdaq Composite +0.5% to 27,068.72, Russell 2000 +0.1%
to 2,837.55 — the index's first winning week in three, within 0.7% of its
all-time high — confirmed via AP (through WTOP, with an on-page timestamp)
cross-checked against Yahoo Finance/CNBC, with zero stale-date issues found
this run (the first clean edition on that specific trap in six). Oil fell
roughly 2% (Brent -2.1% to $104.32, WTI -2.3% to $92.41, cleanly on the same
November contract as Thursday) on rising US-Iran truce hope, and Treasury
yields steadied after Thursday's spike (10-year 5.17% vs. a now-confirmed
5.18% Thursday close).

Sector leadership rotated out of Thursday's Communication-Services-led
pattern into Industrials (XLI +0.95%) and Technology (XLK +0.80%), with
Financials, Health Care, Staples and Utilities also positive; Real Estate,
Energy (still pressured by the oil pullback) and Communication Services
(dragged by Meta) lagged. Single-name stories: Meta Platforms -3.33% after a
Santa Fe, New Mexico jury found the company liable on a reported 43.9 million
counts of consumer-protection-law violations tied to the Cambridge Analytica
scandal (theoretical exposure cited up to approx. $219.5bn, final penalty to
be set by the judge), reversing Thursday's Muse-driven rally; Costco +2.93%
to $922.77, resolving the prior edition's open thread on its Q4/FY2026 beat
into a clean "buy the beat" session; Twilio -7.96% (HSBC downgrade to Reduce,
arguing the AI-agent-driven run-up since Meta's Muse debut overstated
Twilio's monetization slice); Palo Alto Networks -3.89% (confirmed at close,
no negative catalyst identified — a valuation reset alongside Twilio); Nike
-0.67% (BofA downgrade to Underperform, PT cut to $30 from $47); Comcast
-0.99% (KeyBanc downgrade to Underweight, $18 PT); Akamai +3.20% (approx.
$11.6bn, 7-year Anthropic cloud deal — a clean intraday-vs-close divergence
example, reported intraday as high as +16.4%); Dell +5.01% (RBC initiated
Outperform $640 PT). A notable snapshot-vs-close trap: Seagate, Western
Digital and SanDisk were reported by aggregators as down sharply "ahead of
the open" on yields/oversupply fears but all three actually closed higher
(+1.20%/+1.44%/+1.38%) after an intraday reversal.

Macro: Fed Chair Kevin Warsh, the Oct 27-28 FOMC date, the BoE's Nov 5
decision and the BoJ's Oct 29-30 meeting were all re-confirmed fresh against
primary sources. October-hike odds held roughly flat over the weekend
(Polymarket approx. 65%) but stayed contested (CME FedWatch secondary
citations split three ways: approx. 54%/69%/75.8%); Kalshi failed a seventh
straight edition. Thursday 24 Sept's previously-unresolved Treasury closes
were confirmed via Treasury's own par-yield CSV (2-year 4.87%, 10-year
5.18%); Friday closed little changed (4.81%/5.17%). A new CFTC CoT report
posted on schedule (dated Tue 22 Sept): equity-index Asset Managers net long
approx. 934,000-936,000 ES contracts vs. Leveraged Funds net short approx.
375,600-376,000; only ES had a full OI/gross breakdown, so this was reported
as prose rather than a chart (see Hard rules above). Over the weekend, the US
and China reportedly agreed to a $30bn tariff cut and a new AI dialogue
following the Trump-Xi summit's Friday conclusion; separately, a fresh
Houthi missile/drone attack targeted Riyadh directly for the first time since
the conflict resumed, and Trump publicly rejected an Iranian Hormuz-reopening
proposal (Iran says no formal rejection was conveyed; Trump expects talks to
resume this week) — both keep a geopolitical oil-risk premium alive into
Monday, with unconfirmed early coverage suggesting oil re-approached
Thursday's levels.

Commodities/FX: gold's Kitco-vs-USAGOLD gap, closed to $0.16 last edition,
ticked back up to approx. $4.78 (still normal-range noise, not a reopened
split). Copper via Westmetall $14,740.00/t (-0.17%). A new, more precise DXY
problem surfaced: Yahoo Finance and Investing.com agree with each other
(100.97, approx. -0.31/-0.32%) but disagree directionally with Friday's own
FX-cross moves (EUR/USD -0.06%, GBP/USD -0.24%, USD/JPY +0.35%, all pointing
to dollar strength) — disclosed as unreconciled.

Derivatives: the CBOE feed gave a second consecutive full clean sweep (VIX
14.87 -5.11%, computed manually per the standing `prev_day_close` bug, now
8 editions running); the VIX9D front-end inversion flagged last edition
resolved as noise. Cboe's options-volume methodology mismatch (flagged
edition 28) was substantially explained: the page hosts several stacked
category tables per URL; the prior "13.78m" figure is likely the
"Sum of All Products" category (Friday's equivalent: 13,939,864), while the
smaller "902,421" figure remains unattributed. zerogex.io gave a third
consecutive dealer-gamma read but with a striking approx. 9x jump in net GEX
(+$32.56bn vs. Thursday's +$3.63bn) — flagged as a magnitude anomaly to
recheck, not passed through uncritically. 41 sources, zero mismatches after
one round of fixes (a stray tilde in a late-added disclosure-box bullet, and
two unused reserved Annex B placeholders, both caught by `check_refs.py` and
corrected before render). Page 3 filled cleanly from content alone, no
filler table needed — rendered a clean 4 pages on the first attempt.

**Open threads for edition 30:** the Cboe options-volume "902,421" figure
remains unattributed to a specific category even after the stacked-tables
mechanism was identified — keep an eye out if this exact ambiguity recurs.
The DXY-vs-FX-crosses directional conflict (100.97/-0.31% vs.
dollar-strength-implying crosses) needs watching for whether it recurs,
reverses, or was a one-off data artifact — try TradingEconomics again for a
third data point if its historical table becomes fetchable. zerogex.io's
approx. 9x dealer-gamma jump should be sanity-checked again next edition;
if another large, hard-to-explain swing shows up, treat zerogex.io's
precision (not just its directional signal) with more skepticism. Costco's
exact Goldman Sachs/Wells Fargo/Bernstein price targets remain unresolved —
low priority unless the stock moves further. Palo Alto Networks' and the
STX/WDC/SNDK cluster's precise Friday catalysts remain unidentified — low
priority. The reported $30bn US-China tariff cut and new AI dialogue is
sourced only to news aggregators/CNBC, not a primary USTR or Treasury
release — worth a firmer primary-source check if it becomes more
market-relevant. JOLTS (August)'s exact release date this week was not
independently confirmed — check the BLS calendar directly next time it
matters. Meta's Cambridge Analytica verdict is very likely to keep
generating follow-on coverage (potential appeal, the judge's eventual
penalty ruling) — treat as an ongoing story, not a closed one. Tuesday's
PCE print (30 Sept) is the week's key data risk and should be the first
macro item verified next edition, followed by ISM Manufacturing (Wed 1 Oct)
and the September jobs report (Fri 2 Oct) if the research window reaches
that far. Threads closed after resolution rather than carried further: the
Thursday 24 Sept Treasury-close gap (resolved via Treasury CSV/FRED); the
VIX9D front-end inversion (resolved as noise); the Cboe options-volume
mechanism (stacked category tables identified, though the specific
902,421-figure attribution remains open per above); Costco's fuller Friday
market reaction (resolved, +2.93%).
