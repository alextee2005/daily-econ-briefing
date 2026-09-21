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

## Schedule
Run every weekday. Pick the trigger's local time so the effective research
cutoff lands roughly 4 hours after the US market close (20:15 ET) — during
US daylight time that's 00:00 UTC; adjust for standard time. On Mondays
(or after any gap), cover the full window back to the previous edition's
cutoff, including the weekend.

## Standing facts — verify fresh every edition, never from memory
- **Fed Chair is Kevin Warsh**, not Jerome Powell. Warsh was Senate-confirmed
  13 May 2026, sworn in 22 May 2026. Re-confirmed fresh 20 Sept 2026 directly
  against federalreserve.gov's own Board of Governors bio page. **Re-verify
  this fresh against federalreserve.gov every single edition** — do not carry
  it forward from a prior run's text or from training data.
- **The September 2026 FOMC meeting (15–16 Sept) is fully resolved and does
  not need re-verifying again:** the Committee raised the federal funds target
  range 25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, unanimous 12-0, the
  first hike since 2023.
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed fresh 20 Sept 2026
  directly against federalreserve.gov's own FOMC calendar page (still marked
  "tentative until confirmed at the meeting immediately preceding it" — normal
  boilerplate). Re-confirm the date is still listed unchanged each edition as
  that meeting approaches.
- **October-hike odds have rebounded and the two venues have largely
  converged** as of 18 Sept: Polymarket approx. 55% hike / 45% hold; Kalshi
  approx. 55% hike (implied) / 45% hold — up sharply from both venues'
  sub-50%-hike reads at edition 23 (17 Sept). Kalshi's fetch was rate-limited
  twice this run and the figure used is search-cached with an imprecise
  timestamp — get a clean, directly-fetched Kalshi read next time if possible.
  Secondary citations put CME FedWatch-implied odds around 58-60%, consistent
  in direction but **still not independently verifiable — the official page
  remains unreachable via direct fetch**. **Verify fresh every edition into
  the 27-28 Oct meeting, disclose all venues, and do not average or force a
  single number.**
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks'
  policy rates) from memory or from the prompt's own framing — verify it
  fresh from a primary source (federalreserve.gov, bankofengland.co.uk,
  boj.or.jp, kansascityfed.org, etc.) every edition, exactly like any other
  data point.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — this is
  now two editions old and does not need re-confirming again unless a new
  decision date has passed. **Next BoE decision: Thursday 5 November 2026**,
  confirmed directly against bankofengland.co.uk's own MPC-dates page (this
  was the prior edition's open item — now resolved). Re-check that date is
  still listed correctly as 5 Nov approaches.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high — confirmed directly against boj.or.jp's
  own statement (k260918a.pdf). **This was NOT a unanimous decision despite a
  unanimous 52/52-analyst consensus**: the vote split 7-2. Dissenters Asada
  Toichiro and Sato Ayano both preferred holding (underlying inflation/wage-
  price pass-through not yet judged strong enough); separately, two other
  board members (Takata Hajime, Tamura Naoki) dissented on the outlook
  *language* from the hawkish side (they believe underlying inflation has
  already reached target). Governor Ueda: further hikes remain likely but
  "case-by-case," data-dependent, no pre-commitment on pace. The yen weakened
  despite the hike, on doubts the split vote raises about further tightening.
  **This decision is resolved and does not need re-verifying** — but the
  **next BoJ meeting date was not established this run and is the top
  standing-facts open item for edition 25**: check boj.or.jp's own policy
  calendar fresh (do not assume the usual ~6-7 week cadence without
  confirming).

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
  can't catch a mismatch there.
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart #2 by what the day's dominant
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
  has occasionally failed to post in time. It posted normally and cleanly for
  18 Sept (edition 24, cross-confirmed via three syndication mirrors plus an
  independent corroborating wrap), continuing the pattern that the 15-Sept
  gap (edition 21) looks like a one-off, not a recurring failure. Fall back
  to a corroborated secondary source plus multi-ETF-proxy triangulation
  (SPY/DIA/QQQ/IWM vs. their tracked indices) and disclose the gap if it
  recurs.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **A same-day close and a next-day after-hours-triggered move can
  legitimately combine into one large single-day % change** — edition 24's
  Xenon Pharmaceuticals -30.7% Friday move looked at first like it might
  conflict with a same-day "+1% then -25% after-hours Thursday" report, but
  both were correct: the AE disclosure broke Thursday after-hours, and
  Friday's regular-session close captured the full move from Thursday's
  regular close. Check whether a headline % move is measured close-to-close
  (which will include an intervening after-hours event) before assuming two
  reports conflict.
- Do not repeat items already carried in the previous edition.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET, before
  a 2pm Fed decision) vs. continuously-traded spot (which captured the
  post-decision reversal) — a genuine, explainable divergence, not a data
  error. Check whether two conflicting prices are actually two different
  instruments/timestamps before treating it as a sourcing failure.
  Similarly, **a price level can be correct while a vendor's stated %-change
  is wrong** if the vendor used a different prior-day base — edition 24 found
  WTI's Friday level ($100.30) and stated -1.58% change both correct only
  once Thursday's true settle was corrected from a previously-published
  $101.09 to $101.91 (see edition log) — always sanity-check that a stated
  price level and stated % change actually reconcile arithmetically against
  the prior session's logged close before reporting both.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done** — and if it reports 0 inline citations found
  while your Annex B clearly has entries, check for the combined-bracket
  `[n][m]` mistake above before assuming something else is wrong. Also
  remember it only scans HTML text — a citation number baked into a chart
  PNG's label is invisible to it (see Confirmed format above).
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 24 needed CFTC leveraged-funds
  positioning normalized "as % of open interest" per the chart-selection
  guidance, but total open interest for the exact CoT date wasn't obtainable
  from a quick search; it substituted "net position as % of the leveraged-
  funds category's own gross long+short" instead — a real, sourced,
  self-normalizing figure — and labelled the chart and xlabel accordingly
  rather than claiming an OI-normalized figure it didn't have.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` delayed-quotes JSON endpoint first — it often
  returns VIX, VIX9D, VIX3M, VIX6M, VVIX and SKEW directly, but has three
  observed failure modes: (a) a full clean sweep with genuinely fresh
  timestamps on every series, (b) the more common "thin-series-stale"
  pattern, where VIX/VIX3M refresh but the thinner series silently serve a
  stale prior-session snapshot, (c) total failure, where every series is
  stale. **Always check the `last_trade_time` field on each individual
  series** — never trust that the endpoint responded as proof the data is
  fresh. Edition 24 got a full clean sweep (all series fresh 16:15-17:00 ET
  Friday prints), continuing to show the endpoint is usable when checked
  carefully. Also note a `prev_day_close` field bug, now observed **three
  editions running (22, 23 and 24)**: it duplicates the day's own
  `close`/`current_price` rather than giving a real prior-day reference, and
  this corrupts the feed's own `price_change_percent` field too — **never
  quote the feed's `price_change`/`price_change_percent` fields directly;
  always compute day-over-day % change manually against the previous
  edition's logged close.** Fall back to news coverage (Yahoo Finance, CNBC,
  MarketWatch) for at least the headline VIX close if the feed is stale, and
  disclose it as single-sourced. Separately: a clean day-over-day term
  structure comparison can look counterintuitive right after an event —
  editions 23 and 24 both saw the front-end tenor (VIX9D) fall
  disproportionately faster than spot VIX in the sessions after the 16 Sept
  FOMC, simply because the event was progressively rolling out of the 9-day
  lookback window (a mechanical effect that shrank from edition 23 to 24 as
  expected, consistent with it nearing completion) — check whether a
  scheduled event just aged out of a tenor before reading a term-structure
  move as new information.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table
  and (absent fresher CoT data or another dominant story) chart #2.
- **NYSE/Nasdaq closing breadth:** not obtainable; Reuters' final wrap drops
  the breadth block. Mark unavailable.
- **Dealer gamma:** third-party sources only; mark unavailable unless a
  specific desk note is found and cited. SpotGamma's own substack/site
  articles return 403 on direct fetch — this has now recurred at editions 22
  and 24 (not attempted at 23) — search snippets can still surface headline
  numbers but treat as lower-confidence secondary sourcing, and if a figure
  looks implausible relative to the underlying index level (edition 24 found
  a "gamma flip level" that didn't reconcile with any plausible SPX price),
  discard it rather than reporting it.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Expect
  a genuinely wide range across venues/dates — report the range and don't
  force it to a single number.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  three editions running (22, 23 and 24)** — treat this as a durable,
  confirmed pattern rather than re-attempting lme.com first each time;
  **default straight to the fallback chain.** Try Shanghai Metals Market
  (metal.com) first, but it has also failed at recent editions (sign-in wall
  or JS-gated content with no pricing surfaced) — if it fails, use
  Westmetall.com (a German metals-data provider that republishes official LME
  cash/3-month settlement prices) as a same-quality single-sourced fallback,
  and disclose whichever was used. Because the fallback chain can change
  edition to edition, treat any day-over-day copper % change built across two
  different sourcing chains as approximate, not a precise like-for-like
  comparison.
- **Official Treasury par yields:** not posted by the ~20:15 ET cutoff (H.15
  publishes the *prior* day's data the next afternoon). Quote secondary
  market levels and disclose the gap, or report direction vs. the prior
  official close. The 10-year is usually obtainable cleanly via AP/CNBC
  coverage even same-day. **The 2-year is more failure-prone and, as of
  edition 24, has now gone unobtained entirely for a session (Friday 18
  Sept) rather than merely conflicting across sources** — worth trying a
  source that states the figure in prose (news wire) over a raw data-table
  fetch, which carries higher hallucination/misread risk.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly rather than presenting old data as current. Note
  the report comes in (at least) two different methodologies/pages depending
  on the instrument: `financial_lf.htm` (Traders in Financial Futures, Asset
  Manager/Leveraged Funds categories) works well for equity index futures
  (ES/NQ/RTY); the legacy `deacboelf.htm` (CFE non-commercial/commercial)
  report is what actually carries VIX futures positioning — don't expect one
  page to have both.
- **GBP/USD and EUR/USD clean close:** three editions running (22, 23 and 24)
  have found no single authoritative 4pm-London print for either pair —
  sources cluster in a range. Default to reporting the range across sources
  rather than continuing to hunt for one number that may not be publicly
  reconcilable this way; consider this a structural gap in freely-accessible
  sources rather than a one-off worth extensive re-hunting each edition.
- **Gold/silver clean close on a non-event day:** even without an FOMC-style
  settle-vs-spot timing split, Kitco's own quote can differ meaningfully by
  timestamp within the same session. Cite the print closest to a standard NY
  4-5pm ET close as primary and disclose the wider range rather than
  presenting one snapshot as *the* close.
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue, not with Friday retail sales — confirm on
  the BLS/Fed release schedule rather than assuming a date. **PCE inflation
  (Personal Income and Outlays):** confirmed via bea.gov that the report
  covering a given month's data publishes at the *end* of the following
  month (e.g. August 2026 data on 30 Sept 2026) — a "week ahead" secondary
  source at edition 24 mis-dated this to 27 Sept (a Sunday, impossible);
  verify PCE's date against bea.gov directly rather than trusting a
  secondary "week ahead" roundup.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22) — either find a citable
  benchmark before reaching for that chart type, or stick to describing
  implied-vs-realized in prose without the third bar.
- **CFTC total open interest by instrument/date** (needed to normalize
  positioning "as % of open interest" per the chart-#2 guidance) was not
  obtainable via quick search at edition 24 for the 15 Sept report — a
  category's own gross long+short was used as a substitute denominator
  instead (see Hard rules above). Worth trying cftc.gov's own report pages
  directly (rather than search) next time this chart type is needed, since
  the total OI figure is normally printed in the report header.

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
  wrong. **But a 5-page render is not always a stray break** — edition 24 hit
  5 pages with only the one correct pagebreak present; the cause was genuine
  copy overflow (page 3 ran about 3-4 lines too long, spilling a handful of
  bullets onto a near-blank page 4). Check `grep -n pagebreak` first as the
  cheap check, but if that comes back clean, read the actual page images:
  the fix is trimming 3-6 lines of prose/bullets from the page that's
  overflowing (day-ahead table cell text and the last one or two "sector
  setup" bullets are easy, low-value places to tighten first), not hunting
  for a phantom extra break that isn't there.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`.
- Always verify the render: `pdftoppm -png -r 72` and actually read the page
  images before delivering — don't trust the page count alone.

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
  week's known catalysts" table plus a "Sector setup we take into" bullet
  list at the end of Section 6 by default** for any single-session or
  weekend-window edition (skip only if a multi-session catch-up already
  fills 3 pages). **An optional "Commodities & FX levels" table (~13 rows)
  at the end of Section 4** is available as padding if page 3 runs short
  after the two default blocks — genuinely general-purpose, reach for it
  only when content alone doesn't fill the page. Conversely, **if page 3
  overflows by a handful of lines** (edition 24), the cheapest trims are:
  shortening day-ahead table cell text, cutting one "sector setup" bullet
  or merging two into one, and tightening the last prose paragraph in
  Section 5 — usually 3-6 lines is enough, re-render and re-check rather
  than guessing how much was needed.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 3x between
  the largest and next-largest mover does not need capping (edition 22's
  JBHT at -13.3% vs. next-largest GS at -3.96%, about 3.4x, was left
  uncapped; edition 24's XENE at -30.7% vs. next-largest SNDK at +11.0%,
  about 2.8x, was also left uncapped on the same basis).

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default). Fresh CFTC CoT data on a
Monday/weekend-window edition → the ES/NQ/RTY asset-manager-vs-leveraged-
funds positioning chart — **normalize as % of open interest if that figure
can be sourced; if not, a category's own net-position-as-%-of-its-own-
gross-long+short is an acceptable, honestly-labelled substitute** (used at
edition 24 when total OI wasn't obtainable). A single dominant earnings
print with a clean, well-sourced implied-vs-realized-move story → a
three-bar implied/historical-average/realized move chart (see the
known-hard-to-source note above — the historical-average leg has never
actually been sourced successfully yet). A genuine multi-sector
broadening/deepening selloff across consecutive sessions → the sector-ETF
proxy rendered as a grouped (day-over-day) bar instead of single-day. A
holiday-window preview edition with no fresher data → VIX futures term
structure with event annotations (CPI/FOMC/OpEx, etc.). When chart #1
(movers) already covers the earnings story, the sector proxy is a good
complementary choice even on an earnings-heavy day. **Chart #2's placement
in the document should follow its content, not a fixed section** — a CFTC/
positioning chart reads better in Section 5 than Section 2 even though the
asset template defaults to embedding it right after the Section 2 heading
(edition 24).

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–21 (condensed):** established the format (edition 1 baseline;
edition 2 revised weighting/sourcing; edition 3 fixed the ET-cutoff math and
introduced the multi-session-gap and duplicate-fire handling conventions);
corrected the Fed Chair premise to Kevin Warsh at edition 6 (re-verified
every edition since); tracked the Jackson Hole keynote (28 Aug, hawkish) and
the resulting rate-odds repricing through editions 10–18; resolved the
SPDR-sector-ETF-proxy and CBOE-feed (`last_trade_time` check) sourcing
techniques at editions 10–11; corrected the FOMC decision date to Wednesday
16 Sept at edition 18 (superseding editions 15–17's Tuesday assumption).
Major single-name events across this span: Moderna's melanoma-data spike and
unwind (ed. 4–5), Nvidia's Q2 FY27 beat and Hugging Face acquisition (ed.
8–9), Walmart/Advance Auto Parts/Deere earnings reactions (ed. 5), the
PayPal-Stripe deal collapse (ed. 10), California SB 492 hitting utilities
(ed. 11), an Iran/Hormuz escalation cycle running through the whole period
and repeatedly driving oil, Lululemon's guidance-slash collapse (ed. 15),
Canada's approx. $27.6bn retaliatory tariffs taking effect (ed. 16), Apple's
first Ternus-era product event (ed. 17), Oracle's Q1 FY27 beat with a
vol-crush AH reaction (ed. 18), the Fed debate flipping from "hold vs. cut"
to "hold vs. hike" on hot core CPI (ed. 19), Anthropic CEO Dario Amodei's
AI-safety essay driving a chip-selloff/cybersecurity-rally rotation (ed. 20),
and edition 21's Tuesday 15 Sept report (day one of the two-day FOMC
meeting): a second straight losing session pricing in the hike, 10-year
spiked intraday to approx. 5.045% (a 2007 high), S&P 7,585.73 (-0.45%), Dow
52,093.11 (-0.63%), Nasdaq 25,981.57 (-0.78%); Enova International -23/-24%
(withdrew a bank-acquisition bid), Dave & Buster's -19% (Q2 miss); copper via
a then-still-working direct lme.com fetch, $14,001/t (-1.68%); VIX approx.
17.20. First edition under the current 1in/1in/13mm/13mm margins: ed. 19.

**Edition 22 (condensed)** — Thu 17 Sept 2026 report covering Wednesday 16
Sept — FOMC decision day. **The Fed hiked 25bp to 3.75%-4.00%, unanimous
12-0**, confirmed against federalreserve.gov; hawkish SEP (median fed funds
4.1% end-2026). Equities rose on the decision, then reversed hard during
Chair Warsh's press conference to close lower — a clean intraday-vs-close
distinction. S&P 7,551.81 (-0.4%), Dow 51,461.90 (-1.2%), Nasdaq 25,978.42
(flat); Energy/Financials worst, banks the clearest single-name losers (GS
-3.96%, WFC -2.98%). J.B. Hunt -13.3% (Q3 guidance warning); Lennar missed
Q3; Intel +4.03% on SK Hynix Ohio-fab talk. 10-year closed 5.016%, first
close above 5% since 2007; 2-year approx. 4.73-4.74%, a 2024 high. A genuine
gold settle-vs-spot split around the 2pm decision (COMEX +1.3% to $4,387.50
pre-decision vs. spot -1.2% to $4,240.10 post-decision) — a real timing
divergence, not a data error. Oil reversed (Brent -2.7% to $105.83) on Saudi
pipeline-restoration progress. Copper: LME direct fetch failed (first of what
became a 3-edition streak); SMM fallback used, approx. $14,250/t. DXY 100.28,
5th straight up day. VIX closed 17.71 (+3.0%). Fixed a `check_refs.py`
false-negative caused by combined-bracket `[26][27]` citations. 35 sources,
zero mismatches.

**Edition 23 (condensed)** — Fri 18 Sept 2026 report covering Thursday 17
Sept, window Tue 15 Sept close/AH through Thu 17 Sept close/AH. Fixed the two
header/structure errors edition 22 introduced (date line = edition date, not
session date; Method note restored after Annex B). Equities reversed most of
Wednesday's post-FOMC selloff as oil and yields eased: S&P 7,637.76 (+1.1%),
Dow 51,778.04 (+0.6%), Nasdaq 26,418.30 (+1.7%), Russell 2,874.63 (+0.6%),
confirmed via the AP wire (three syndication mirrors plus an independent
Yahoo/Bloomberg figure). Sector rotation inverted from Wednesday: Technology
(XLK +2.25%) led, Financials (XLF -0.09%) the only sector ETF lower. Movers:
Generac +18.3% (Amazon data-center power deal), Lucid +10.0% (Bolt robotaxi
deal), Intel +7.7%, Micron +5.5% (memory-shortage theme), AutoNation -9.4%
to a 52-week low. Fed Chair Warsh and the 16 Sept hike re-confirmed; next
FOMC meeting confirmed Oct 27-28. October-hike odds reversed sharply from
edition 22's single-sourced approx. 92% figure — Polymarket approx. 50-52%
hold, Kalshi approx. 63% hold, disclosed as disagreeing venues. Bank of
England held at 3.75%, 6-3 (confirmed fresh). Bank of Japan's 17-18 Sept
decision had **not** been announced as of the 22:43 ET cutoff — flagged as
the top open item (resolved at edition 24, see standing facts). Initial
jobless claims beat (196K vs. 207K); housing starts/permits softened; Philly
Fed cooled but beat. 10-year fell to 4.93%; 2-year had three conflicting
secondary reads (CNBC approx. 4.67% used). Gold prints varied by Kitco
timestamp ($4,300-4,355 range), approx. 4:49pm ET print ($4,341, +1.83%) used.
Brent $104.82 (-0.95%), WTI $101.09 (-1.31%) — **the WTI Thursday figure was
later found to be wrong; edition 24 corrected it to $101.91 via CNBC**. Copper:
lme.com failed a second straight edition, metal.com also failed, Westmetall.com
used, $14,409/t. DXY approx. flat (100.22). GBP/USD and EUR/USD both
unresolved (GBP/USD range 1.3358-1.3381; EUR/USD omitted to Annex A). VIX
closed 15.44, down 12.82% (required correcting a broken CBOE
`prev_day_close` field, cross-confirmed via Yahoo Finance — the same feed bug
recurred at editions 22-24). CFTC CoT still dated 8 Sept (fresh data due
Friday 18 Sept). Chart #2: SPDR sector-ETF single-day rotation bar. 39
sources, zero mismatches, zero stray tildes.

**Edition 24 (most recent — full detail)** — Mon 21 Sept 2026 report covering
Friday 18 Sept (the window's one NYSE session, a September quarterly triple
witching), research window Thu 17 Sept 20:00 ET through Sun 20 Sept 20:00 ET
(weekend catch-up included). Verified the two structural rules the prompt
flagged before finishing: date line reads the edition date (Monday 21
September 2026), not the session date; Method note is present after Annex B.

Dominant story: Friday's indexes closed little-changed — S&P 500 7,650.50
(+0.2%), Dow 51,682.64 (-0.2%), Nasdaq 26,522.55 (+0.4%), Russell 2000
2,860.40 (-0.5%) — confirmed via AP's wire (via WTOP, cross-mirrored on four
syndication sites) and corroborated independently by TheStreet, even as AP's
own copy noted the majority of individual stocks fell as the 10-year
Treasury yield climbed back to 5.00%. The real story was technical: approx.
$7tn in US options notional expired at the year's second-largest September
triple witching (60% at the open, per Citadel Securities/Scott Rubner),
layering onto Monday 21 Sept's quarterly S&P 500/100/MidCap/SmallCap and
Nasdaq-100 rebalances, in which SpaceX's confirmed Nasdaq-100 weight jumps to
2.82% from 1.28%. Sector rotation: Technology (XLK +0.82%) led a second
straight session, Industrials (XLI +0.44%) the only other sector ETF higher;
Materials and Utilities tied as laggards (both -1.42%).

Single-stock movers were idiosyncratic: Xenon Pharmaceuticals -30.7% to
$39.75 (a Phase 3 depression-trial enrollment pause on a neuropsychiatric
adverse-event signal, disclosed Thursday after-hours and continuing into
Friday's regular session — the close-to-close % correctly captures both
legs, see Hard rules above for how this was reconciled); Nucor -6.1% to
$249.03 (Q3 EPS guidance $5.55-5.65 vs. $5.99 consensus, a 6.5% miss, despite
a record-shipment Q2); Netflix -4.7% to $71.79 (Wells Fargo downgrade to
Underweight, PT $80→$57, on weak engagement and a lighter H2 originals
slate); SanDisk +11.0% and Micron +3.9% (continued AI/NAND memory-shortage
rally); Robinhood +9.1% to $119.82 (SEC's new five-year "Innovation
Exemption" opening a pathway for tokenized-stock trading venues). Separately,
Warren Buffett stepped down as Berkshire Hathaway chairman effective Friday
(Howard Buffett succeeds him as chairman; Greg Abel remains CEO) — BRK.B
traded roughly flat (+0.11%), a muted reaction to a major governance
headline; some low-quality aggregator snippets claimed a decline, discarded
in favor of the better-corroborated closing-price figure.

Macro: the Bank of Japan hiked 25bp to approx. 1.25% on 18 Sept, a 31-year
high — but on a 7-2 split vote against a unanimous 52/52-analyst consensus,
confirmed directly against boj.or.jp's own statement; the yen weakened
despite the hike. Fed Chair Warsh and the 16 Sept hike re-confirmed; next
FOMC meeting confirmed unchanged at 27-28 Oct. October-hike odds rebounded
and converged: Polymarket approx. 55% hike, Kalshi approx. 55% hike
(implied, search-cached), versus both venues' sub-50%-hike reads at edition
23. Bank of England's next decision date confirmed as 5 Nov 2026 (prior
edition's open item, now resolved). Conference Board LEI fell 0.1% in August
to 99.5; University of Michigan final September sentiment came in at 47.8,
the second-weakest reading on record, with 1-year inflation expectations
jumping to 4.6%. The US is reportedly delaying new China tariffs pending a
tentative 24 Sept Trump-Xi Washington summit (not yet confirmed by China); a
revised US import-ban list on Canadian goods takes effect 29 Sept.

Commodities/FX: gold $4,382.38 (+0.85%) and silver $66.13 (+1.58%) held
weekly gains despite a late-session yield pop; Brent $103.87 (-0.9%) and WTI
$100.30 (-1.58%) eased as Saudi Arabia continued restoring the Yanbu export
hub — **WTI's Friday figures required correcting Thursday's previously-
published settle from $101.09 to $101.91 (CNBC) for the price level and %
change to reconcile arithmetically; treated as a prior-edition correction,
not a new data error.** Copper: lme.com failed a third straight edition
(confirmed durable pattern), Westmetall.com fallback used, $14,529/t
(+0.83%). DXY held roughly flat (100.2-100.5 range, no clean single close).
GBP/USD (1.3376-1.3392) and EUR/USD (qualitative, "below 1.15") both
unresolved for a third straight edition. USD/JPY was the FX story: a wide
155.7-158.1 intraday range on the BoJ's split-vote-driven yen weakness, no
single confirmed NY close available. Over the weekend, Iran-backed Houthi
forces fired missiles and drones at Riyadh early Saturday with a second
claimed strike attempting to hit Saudi Aramco infrastructure at Yanbu — all
intercepted per the Saudi-led coalition, no casualties or damage, but a
fresh oil-supply headline risk into Monday.

Derivatives: VIX closed 14.81, down 4.08% from Thursday's 15.44 (computed
manually — the CBOE feed's `prev_day_close`/`price_change_percent` bug
recurred for a third straight edition; every series' `last_trade_time` was
checked individually and all were genuinely fresh Friday prints, a full
clean sweep). Term structure stayed in contango with the front end again
unwinding faster than spot (VIX9D -8.37% vs. VIX -4.08%) — the same
mechanical FOMC-lookback-window effect as edition 23, smaller in magnitude
as expected. VIX options volume stayed elevated (652,794 contracts, 540,186
calls) despite falling spot VIX. Fresh CFTC CoT data (as of 15 Sept,
published Friday — first update since 8 Sept) showed leveraged funds
trimming net-short index-futures exposure across ES/NQ/RTY while remaining
net short in all three; charted as net position vs. each category's own
gross long+short (total open interest for the date wasn't obtainable, so
this was used as an honest substitute for the usual %-of-OI normalization —
see Hard rules above). SOFR jumped to 3.85% on 17 Sept from 3.62%, confirmed
via two sources, cause unexplained. Chart #2 (CFTC positioning) was placed
in Section 5 rather than Section 2, since that's where the content actually
belongs — a template-default deviation, not an error. 45 sources, zero
mismatches, zero stray tildes. Page 3 initially overflowed to a 5-page PDF
by about 3-4 lines with only the one correct pagebreak present (genuine
copy overflow, not a stray break) — trimmed day-ahead table cell text and
consolidated two "sector setup" bullets into one to bring it back to 4 pages.

**Open threads for edition 25:** Bank of Japan's *next* policy meeting date
— not established this run, now the top standing-facts item, check
boj.or.jp's own calendar fresh rather than assuming the usual cadence; a
clean 2-year Treasury yield for Friday 18 Sept (went entirely unobtained
this run, worse than the usual conflicting-sources problem) — try the
official H.15 page, which should have posted Friday's data by the following
Monday afternoon; EUR/USD and GBP/USD clean single closes (three editions
unresolved — likely a structural sourcing gap, consider whether continued
hunting is worth the effort each edition); a clean, non-rate-limited Kalshi
October-hike-odds fetch with a firm timestamp; whether October-hike odds
keep converging or diverge again as the 27-28 Oct meeting approaches; the
cause of Thursday 17 Sept's SOFR jump (3.62%→3.85%), still unexplained;
Sonic Automotive's and Asbury Automotive's exact Thursday 17 Sept closes,
unreconciled across sources for two straight research passes now — consider
dropping this thread if a third pass also fails; USD/JPY follow-through
Monday 21 Sept given Friday's wide 155.7-158.1 range and the BoJ's split
vote; whether the tentative 24 Sept Trump-Xi summit actually happens and its
outcome, alongside Thursday 24 Sept's four other central-bank decisions
(Riksbank, SNB, Norges Bank, Banxico); confirmation of Monday's completed
S&P/Nasdaq-100 rebalance flows and whether elevated volume/volatility shows
up in the sessions right after triple witching; named analyst rating changes
on Tyson Foods, Southwest, Waste Connections, Ball Corp., Crown Holdings,
Accenture and Equinor from a Friday roundup headline, individual details
unconfirmed; Seagate/Western Digital/SK Hynix's exact Friday % moves,
single-sourced to an aggregator; whether lme.com's direct fetch ever
recovers (3 straight failures — keep defaulting to Westmetall.com but it
costs little to retry lme.com first in case it's back).
