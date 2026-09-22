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
  13 May 2026, sworn in 22 May 2026. **Re-confirmed fresh 22 Sept 2026**
  directly against federalreserve.gov's own Board of Governors bio page (still
  lists Warsh as Chairman, first entry). **Re-verify this fresh against
  federalreserve.gov every single edition** — do not carry it forward from a
  prior run's text or from training data.
- **The September 2026 FOMC meeting (15–16 Sept) is fully resolved and does
  not need re-verifying again:** the Committee raised the federal funds target
  range 25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, unanimous 12-0, the
  first hike since 2023.
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed fresh 22 Sept 2026
  directly against federalreserve.gov's own FOMC calendar page (still marked
  "tentative until confirmed at the meeting immediately preceding it" — normal
  boilerplate). Re-confirm the date is still listed unchanged each edition as
  that meeting approaches.
- **October-hike odds, re-confirmed fresh 22 Sept 2026, still no single clean
  number:** Polymarket approx. 53% hike/47% hold (direct fetch this run,
  $9.17m volume — resolves prior editions' single-sourced/rate-limited
  reads with a clean direct number). Kalshi remains rate-limited on direct
  fetch **for a third straight edition (23, 24, 25)** — the figure used is
  again search-cached, approx. 55-56% hike, imprecise timestamp. Secondary
  citations for CME FedWatch-implied odds now disagree with each other
  (approx. 56% vs. approx. 59.7%), not just with the other venues — the
  official CME page remains unreachable via direct fetch. **Range across all
  venues: roughly 53-60% probability of an October hike — still the modal
  outcome, but treat as a genuinely wide, multi-venue range, not a single
  number, and get a clean directly-fetched Kalshi read next time if at all
  possible (this is now a structural gap, not a one-off).**
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks'
  policy rates) from memory or from the prompt's own framing — verify it
  fresh from a primary source (federalreserve.gov, bankofengland.co.uk,
  boj.or.jp, kansascityfed.org, etc.) every edition, exactly like any other
  data point.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — this is
  now three editions old and does not need re-confirming again unless a new
  decision date has passed. **Next BoE decision: Thursday 5 November 2026**,
  confirmed directly against bankofengland.co.uk's own MPC-dates page at
  edition 24. Re-check that date is still listed correctly as 5 Nov
  approaches.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus — this decision is resolved and does not
  need re-verifying. **The Bank of Japan's next policy meeting is now
  confirmed for October 29-30, 2026**, direct from boj.or.jp's own Monetary
  Policy Meeting schedule page (fetched fresh 22 Sept 2026; December 17-18,
  2026 is also listed further out). This resolves the top open item carried
  from edition 24. Note: the page presents Oct 29-30 as a routine forward-
  calendar entry with no "newly added" marker — whether this date was already
  on BoJ's standing calendar before the 18 Sept hike or was set as a result of
  it was not established and is not material; the date itself is what matters
  and is confirmed. Re-confirm this date is still listed unchanged as it
  approaches, same as any other central-bank meeting date.

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
  has occasionally failed to post in time. It has now posted normally and
  cleanly for three straight editions (18, 21 Sept via AP/WTOP), continuing
  to look like the 15-Sept gap (edition 21) was a one-off, not a recurring
  failure. Fall back to a corroborated secondary source plus multi-ETF-proxy
  triangulation (SPY/DIA/QQQ/IWM vs. their tracked indices) and disclose the
  gap if it recurs.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example: a Trefis "Market Movers" page
  carrying a Monday-21-Sept-dated URL was actually re-serving Friday 18
  Sept's already-reported figures (Xenon Pharmaceuticals -30.7%, etc.) —
  discarded once cross-checked against the actual Monday session's numbers.
  **A same-day close and a next-day after-hours-triggered move can
  legitimately combine into one large single-day % change** — edition 24's
  Xenon Pharmaceuticals -30.7% Friday move looked at first like it might
  conflict with a same-day "+1% then -25% after-hours Thursday" report, but
  both were correct. Check whether a headline % move is measured close-to-close
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
  the prior session's logged close before reporting both. Edition 25 hit the
  same class of problem with Monday's WTI settlement: sources split roughly
  $92.28-$95.80/bbl, and rather than force a single number, the wider range
  was disclosed with the better-reconciling estimate ($95.50-95.80, -4.5%)
  flagged as primary.
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
- **When an "optional" filler element (e.g. a levels table) would just
  restate the same instrument list already in a main table with one extra
  column, that's still legitimate as long as the extra column is genuinely
  additive** (edition 25 added a Friday-baseline-vs-Monday-close levels
  table to a short page 3, showing the prior-session base that the main
  Commodities & FX table didn't display) — don't reject the idea purely
  because the instrument list overlaps; check whether the *added* column
  carries real information first.

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
  fresh. Edition 25 got a full clean sweep again (all series fresh at
  Monday's 16:15-17:00 ET prints). Also note a `prev_day_close` field bug,
  now observed **four editions running (22, 23, 24 and 25)**: it duplicates
  the day's own `close`/`current_price` rather than giving a real prior-day
  reference, and this corrupts the feed's own `price_change_percent` field
  too — **never quote the feed's `price_change`/`price_change_percent`
  fields directly; always compute day-over-day % change manually against the
  previous edition's logged close.** Fall back to news coverage (Yahoo
  Finance, CNBC, MarketWatch) for at least the headline VIX close if the feed
  is stale, and disclose it as single-sourced. Separately: the mechanical
  VIX9D-vs-spot-VIX distortion from the 16 Sept FOMC aging out of the 9-day
  lookback window, tracked across editions 23-24, **looks to have largely
  stabilized by edition 25** — VIX9D no longer swings by double-digit
  percentages day-to-day and simply sits at its normal contango discount to
  spot VIX. Treat this thread as resolved absent a new event resetting it.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table
  and (absent fresher CoT data or another dominant story) chart #2. Worked
  cleanly again at edition 25.
- **NYSE/Nasdaq closing breadth:** not obtainable; Reuters' final wrap drops
  the breadth block. Mark unavailable.
- **Dealer gamma:** third-party sources only; mark unavailable unless a
  specific desk note is found and cited. SpotGamma's own substack/site
  articles return either 403 or an empty static page on direct fetch — this
  has now recurred at editions 22, 24 and 25 — search snippets can still
  surface headline numbers but treat as lower-confidence secondary sourcing,
  and if a figure looks implausible relative to the underlying index level
  (edition 24 found a "gamma flip level" that didn't reconcile with any
  plausible SPX price; edition 25 found a third-party GEX tool showing
  dollar figures many orders of magnitude too small to be real SPX dealer
  gamma), discard it rather than reporting it.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Expect
  a genuinely wide range across venues/dates — report the range and don't
  force it to a single number. As of edition 25, even the *secondary*
  citations for CME FedWatch disagree with each other (approx. 56% vs.
  approx. 59.7%) — treat CME FedWatch as the least precise of the three
  venues reported, not just the hardest to fetch directly.
- **Kalshi direct fetch:** now rate-limited (HTTP 429) for **three straight
  editions (23, 24, 25)** — treat this as a structural gap similar to
  EUR/USD and GBP/USD rather than a transient issue; keep trying a direct
  fetch each edition (it may recover) but default to disclosing a
  search-cached figure with an explicit "imprecise timestamp" caveat when it
  fails again.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  four editions running (22, 23, 24 and was not re-attempted at 25 given the
  confirmed durable pattern)** — treat this as a durable, confirmed pattern
  rather than re-attempting lme.com first each time; **default straight to
  the fallback chain.** Shanghai Metals Market (metal.com) has now failed
  **four editions running (22-25)** — it may be worth skipping metal.com
  entirely next time and going straight to Westmetall.com (a German
  metals-data provider that republishes official LME cash/3-month settlement
  prices), which has worked cleanly every time it's been used as the
  fallback. Disclose whichever was used. Because the fallback chain can
  change edition to edition, treat any day-over-day copper % change built
  across two different sourcing chains as approximate, not a precise
  like-for-like comparison.
- **Official Treasury par yields:** not posted by the ~20:15 ET cutoff (H.15
  publishes the *prior* day's data the next afternoon). Quote secondary
  market levels and disclose the gap, or report direction vs. the prior
  official close. The 10-year is usually obtainable cleanly via AP/CNBC
  coverage even same-day, and — as of edition 25 — the official H.15 page
  itself was successfully fetched direct from home.treasury.gov for **both**
  the 10-year and 2-year, backfilling Friday 18 Sept's previously-unobtained
  2-year print (4.44%) as well as giving a clean Monday 21 Sept read (2-year
  approx. 4.45%, 10-year approx. 4.96%). Keep trying the official page
  directly each edition before falling back to secondary coverage — it may
  simply have been a matter of the right day's table being available by the
  time of the fetch.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly rather than presenting old data as current. Note
  the report comes in (at least) two different methodologies/pages depending
  on the instrument: `financial_lf.htm` (Traders in Financial Futures, Asset
  Manager/Leveraged Funds categories) works well for equity index futures
  (ES/NQ/RTY); the legacy `deacboelf.htm` (CFE non-commercial/commercial)
  report is what actually carries VIX futures positioning — don't expect one
  page to have both. As of edition 25 the most recent data is still dated 15
  Sept (published Friday 18 Sept); no new report had posted by the Monday 21
  Sept cutoff — next update due approx. Friday 25 Sept.
- **GBP/USD and EUR/USD clean close:** a structural sourcing gap across
  editions 22-24 (no single authoritative 4pm-London print for either pair
  from a news-wire/official source) — **edition 25 obtained clean single
  closes for both from Yahoo Finance's historical-price pages** (EUR/USD
  1.1480, GBP/USD 1.3389), which is a genuine improvement, but this rests on
  a **single vendor with no independent second-source corroboration** —
  don't yet treat this as fully resolved. Try to cross-check the Yahoo
  Finance figure against a second independent close (a news wire, or a
  different data vendor) next time before calling this thread closed for
  good.
- **Gold/silver clean close on a non-event day:** even without an FOMC-style
  settle-vs-spot timing split, Kitco's own quote can differ meaningfully by
  timestamp within the same session, and futures (GC=F/SI=F) vs. spot XAU/
  XAG quotes from different vendors can also diverge by several tenths of a
  percent on an ordinary day (edition 25: Yahoo GC=F $4,383.90 vs. Bloomberg
  spot $4,378.63, both "near-flat" but not identical). Cite the print closest
  to a standard NY 4-5pm ET close as primary and disclose the wider range
  rather than presenting one snapshot as *the* close.
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
  the total OI figure is normally printed in the report header. Not
  revisited at edition 25 since no fresh CoT data posted this window.
- **Cboe's US Options Daily Market Statistics page** (used for VIX options
  volume) does not carry an explicit date stamp — edition 25 got a plausible
  figure (713,342 contracts) that could not be independently confirmed as
  genuinely Monday's session vs. a cached snapshot. Treat any figure pulled
  from this page as moderate-confidence unless a date parameter/stamp can be
  confirmed to actually change the returned data.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  (e.g. estimated closing-auction imbalance dollar amounts around a
  quarterly rebalance) tends to come from independent research
  Substacks/blogs (e.g. QSG Research) rather than a sell-side desk by name —
  treat as citable but note it's not a bulge-bracket named source when it
  matters for confidence level.

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
- Always verify the render: `pdftoppm -png -r 72` (or higher resolution, e.g.
  `-r 100`, for easier visual review) and actually read the page images
  before delivering — don't trust the page count alone. Edition 25's page 3
  ran visibly short (roughly 40% blank) on the first render despite passing
  the 4-page check; adding the optional Commodities & FX levels table (see
  below) and two extra sector-setup/day-ahead lines fixed it on re-render —
  a reminder that a correct page count doesn't mean a well-balanced page.

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
  fills 3 pages). **An optional "Commodities & FX levels" table (~9-13 rows)
  at the end of Section 4** is available as padding if page 3 runs short
  after the two default blocks — genuinely general-purpose, reach for it
  only when content alone doesn't fill the page. It doesn't have to be a
  from-scratch instrument list: edition 25 built it as a Friday-baseline-vs-
  Monday-close comparison for the same instruments already in the main
  Commodities table, which is legitimate padding because the *baseline*
  column is new information, not a straight duplicate. Conversely, **if page
  3 overflows by a handful of lines** (edition 24), the cheapest trims are:
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
  about 2.8x, was also left uncapped on the same basis; edition 25's GRAL at
  approx. +30% vs. next-largest ARM at +16.6%, about 1.8x, needed no
  capping either).

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used again at edition 25 for a
broad chip-led rally with sector rotation as the clearest secondary story).
Fresh CFTC CoT data on a Monday/weekend-window edition → the ES/NQ/RTY
asset-manager-vs-leveraged-funds positioning chart — **normalize as % of
open interest if that figure can be sourced; if not, a category's own
net-position-as-%-of-its-own-gross-long+short is an acceptable, honestly-
labelled substitute** (used at edition 24 when total OI wasn't obtainable).
A single dominant earnings print with a clean, well-sourced implied-vs-
realized-move story → a three-bar implied/historical-average/realized move
chart (see the known-hard-to-source note above — the historical-average leg
has never actually been sourced successfully yet). A genuine multi-sector
broadening/deepening selloff across consecutive sessions → the sector-ETF
proxy rendered as a grouped (day-over-day) bar instead of single-day. A
holiday-window preview edition with no fresher data → VIX futures term
structure with event annotations (CPI/FOMC/OpEx, etc.). When chart #1
(movers) already covers the earnings story, the sector proxy is a good
complementary choice even on an earnings-heavy day — edition 25 used exactly
this combination (chip-stock movers as chart #1, sector rotation as chart
#2) since the two stories reinforced rather than duplicated each other.
**Chart #2's placement in the document should follow its content, not a
fixed section** — a CFTC/positioning chart reads better in Section 5 than
Section 2 even though the asset template defaults to embedding it right
after the Section 2 heading (edition 24).

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
Chair Warsh's press conference to close lower. S&P 7,551.81 (-0.4%), Dow
51,461.90 (-1.2%), Nasdaq 25,978.42 (flat); banks the clearest single-name
losers (GS -3.96%, WFC -2.98%). J.B. Hunt -13.3% (Q3 guidance warning);
Lennar missed Q3; Intel +4.03% on SK Hynix Ohio-fab talk. 10-year closed
5.016%, first close above 5% since 2007. A genuine gold settle-vs-spot split
around the 2pm decision (COMEX +1.3% vs. spot -1.2%) — a real timing
divergence, not a data error. Oil reversed (Brent -2.7% to $105.83). Copper:
LME direct fetch failed (first of what became a multi-edition streak); SMM
fallback used, approx. $14,250/t. DXY 100.28. VIX closed 17.71 (+3.0%). Fixed
a `check_refs.py` false-negative caused by combined-bracket `[26][27]`
citations. 35 sources, zero mismatches.

**Edition 23 (condensed)** — Fri 18 Sept 2026 report covering Thursday 17
Sept. Fixed the two header/structure errors edition 22 introduced (date line
= edition date, not session date; Method note restored after Annex B).
Equities reversed most of Wednesday's post-FOMC selloff: S&P 7,637.76
(+1.1%), Dow 51,778.04 (+0.6%), Nasdaq 26,418.30 (+1.7%), Russell 2,874.63
(+0.6%). Movers: Generac +18.3%, Lucid +10.0%, Intel +7.7%, Micron +5.5%,
AutoNation -9.4% (52-week low). October-hike odds reversed sharply from
edition 22's single-sourced approx. 92% figure — Polymarket approx. 50-52%
hold, Kalshi approx. 63% hold. Bank of England held at 3.75%, 6-3. Bank of
Japan's 17-18 Sept decision had not yet been announced as of cutoff (flagged
open item, resolved at edition 24). Initial jobless claims beat (196K vs.
207K). 10-year fell to 4.93%. Copper: lme.com and metal.com both failed,
Westmetall.com used, $14,409/t. GBP/USD and EUR/USD both unresolved. VIX
closed 15.44, down 12.82% (CBOE `prev_day_close` field bug first recurred
here). CFTC CoT still dated 8 Sept. 39 sources, zero mismatches.

**Edition 24 (condensed)** — Mon 21 Sept 2026 report covering Friday 18 Sept
(a September quarterly triple witching), weekend catch-up window. Indexes
little-changed: S&P 7,650.50 (+0.2%), Dow 51,682.64 (-0.2%), Nasdaq 26,522.55
(+0.4%), Russell 2,860.40 (-0.5%). Dominant story was technical: approx. $7tn
in options notional expired at the year's second-largest September triple
witching, layering onto Monday 21 Sept's quarterly S&P/Nasdaq-100 rebalances
(SpaceX's Nasdaq-100 weight confirmed rising to 2.82% from 1.28%). Movers:
Xenon Pharmaceuticals -30.7% (Phase 3 enrollment pause, a close-to-close
figure correctly combining a Thursday AH disclosure with Friday's regular
session), Nucor -6.1% (Q3 guidance miss), Netflix -4.7% (Wells Fargo
downgrade), SanDisk +11.0% and Micron +3.9% (AI/NAND rally), Robinhood +9.1%
(SEC tokenized-stock exemption). Warren Buffett stepped down as Berkshire
chairman (Howard Buffett succeeds; Abel remains CEO), BRK.B roughly flat.
Bank of Japan hiked 25bp to approx. 1.25% on 18 Sept, a 31-year high, 7-2
split vote. October-hike odds rebounded: Polymarket and Kalshi both approx.
55% hike (up from sub-50% at edition 23). Gold $4,382.38 (+0.85%), silver
$66.13 (+1.58%); Brent $103.87 (-0.9%), WTI $100.30 (-1.58%, requiring a
correction to Thursday's previously-published $101.09 settle to $101.91 for
the price/percent to reconcile). Copper: lme.com failed a third straight
edition, Westmetall.com used, $14,529/t (+0.83%). DXY 100.2-100.5 range.
USD/JPY the FX story: wide 155.7-158.1 range on the BoJ's split-vote-driven
yen weakness. Weekend: Iran-backed Houthi forces fired on Riyadh/attempted a
strike on Saudi Aramco's Yanbu hub, intercepted, no damage. VIX closed 14.81
(-4.08%), a full clean CBOE feed sweep; VIX9D unwinding faster than spot on
the FOMC-lookback mechanical effect. Fresh CFTC CoT (as of 15 Sept) showed
leveraged funds trimming net-short ES/NQ/RTY exposure. 45 sources, zero
mismatches. Page 3 initially overflowed to 5 pages by 3-4 lines (genuine
copy overflow, not a stray break) — trimmed to 4.

**Edition 25 (most recent — full detail)** — Tue 22 Sept 2026 report covering
Monday 21 Sept (the window's one NYSE session), research window Sun 20 Sept
20:00 ET through Mon 21 Sept 23:29 ET. Verified the two structural header
rules the prompt flagged before finishing: date line reads the edition date
(Tuesday 22 September 2026), not the session date; window line starts at the
given research-window start (Sun 20 Sept 20:00 ET), not earlier.

Dominant story: a broad chip-stock rally (Intel +12.0%, AMD approx. +10%
and above a $1tn market cap for the first time, Qualcomm approx. +9%, Arm
Holdings +16.6% to $322.90 on a Piper Sandler Overweight initiation) pushed
the Nasdaq Composite to a record close of 27,122.09 (+2.26%), with the S&P
500 7,764.70 (+1.49%) and Dow 52,048.83 (+0.71%) also higher and the Russell
2000 2,875.36 (+0.52%) — confirmed via AP's wire (via WTOP, cross-mirrored
on further syndication and independently corroborated by CNBC/TheStreet).
Sector rotation: Communication Services (XLC +3.56%) and Technology (XLK
+2.89%) led, Energy (XLE -2.30%) the clear laggard on the day's oil selloff,
Materials (XLB -0.56%) and Utilities (XLU -0.34%) also softer. The quarterly
S&P 500/400/600 and Nasdaq-100 rebalance took effect at Monday's open: Bloom
Energy, Illumina and Everpure joined the S&P 500 (replacing Molson Coors,
The Trade Desk and Builders FirstSource); SpaceX's Nasdaq-100 weight rose to
2.82% from 1.28% as previously flagged. Whether the rebalance itself drove
above-normal Monday trading volume could not be confirmed either way (Annex
A). Other movers: Grail (GRAL) approx. +30% (FDA advisory-committee review
of its Galleri test scheduled) and HP Inc. (HPQ) -4.22% (withheld FY2027
guidance, warned of mid-single-digit PC-volume declines through 2027 — the
best-sourced figure of a range spanning -2% to -10.5% across aggregators,
unreconciled). Earnings docket was thin (only minor names reported, no
market-moving reaction). Analyst actions: HubSpot, Palo Alto Networks and
CrowdStrike all had PTs raised; Equifax downgraded to Neutral; and the prior
edition's Friday-18-Sept analyst-roundup names (Tyson Foods, Southwest,
Waste Connections, Ball Corp., Crown Holdings, Accenture, Equinor) were all
confirmed in full detail this run, including a genuine split call on
Accenture (Deutsche Bank raised its PT while maintaining Hold; Guggenheim
downgraded to Neutral on soft demand channel checks; shares fell approx. 4%
that day).

Macro: Fed Chair Kevin Warsh and the Oct 27-28 next FOMC meeting both
re-confirmed fresh against federalreserve.gov. October-hike odds: Polymarket
approx. 53% hike (clean direct fetch this run), Kalshi approx. 55-56% (still
rate-limited on direct fetch, a third straight edition), secondary CME
FedWatch citations disagreeing with each other (approx. 56% vs. approx.
59.7%) as well as with the other venues — range across venues roughly
53-60%. The Bank of Japan's next policy meeting is now confirmed as October
29-30, 2026 (direct from boj.or.jp), resolving edition 24's top open item.
The Trump-Xi Washington summit, "tentative" as of edition 24, is now
reported as proceeding Thursday 24 Sept. The US import ban on Canadian
dairy/alcohol/motor vehicles remains on track for 29 Sept. Thursday 24 Sept
also brings four other central-bank decisions: Norges Bank and Banxico both
confirmed for that date; Riksbank likely 24 Sept but not fully
primary-confirmed; SNB's exact date unresolved between 24-25 Sept (one
source read as a possibly mis-surfaced 2025 article). Treasury yields: the
official H.15 page was successfully fetched direct, backfilling Friday
18 Sept's previously-unobtained 2-year print (4.44%) and giving a clean
Monday reading (2-year approx. 4.45%, 10-year approx. 4.96%, down from
Friday's 5.01%). SOFR held at Thursday's elevated 3.85% through Friday;
Monday's reading not yet published at cutoff (normal one-day lag), and the
cause of the mid-week 3.62%→3.85% jump remains unexplained.

Commodities/FX: oil sold off on reported Iran-Oman diplomacy toward
reopening Strait of Hormuz shipping around the UN General Assembly — Brent
$100.34 (-2.97%, well-corroborated), WTI unresolved to a single print
(sources split $92.28-95.80/bbl; $95.50-95.80, approx. -4.5%, used as the
better-reconciling estimate). The Houthis publicly pledged not to target
US-flagged vessels while continuing to threaten Saudi-linked targets
specifically; no Monday update was found on Saudi Aramco's Yanbu
pipeline-restoration progress (offline since a 10 Sept drone strike). Gold
$4,378.63 (approx. -0.1%, essentially flat) and silver $65.82 (-0.47%) held
broadly steady. Copper: lme.com not re-attempted (confirmed durable
failure), Shanghai Metals Market (metal.com) failed a fourth straight
edition, Westmetall.com fallback used again, $14,788/t (+1.78% vs. Friday's
$14,529/t). DXY 100.43 (+0.21%) — a clean single close. EUR/USD (1.1480,
approx. +0.03%) and GBP/USD (1.3389, approx. +0.23%) both produced clean
single closes via Yahoo Finance for the first time in three editions,
though single-sourced and not yet cross-corroborated by a second vendor.
USD/JPY 157.05 (+0.59%) — yen weakness continued but the day's 156.72-157.11
range was much tighter than Friday's 155.7-158.1 swing.

Derivatives: VIX closed 14.87, +0.41% vs. Friday's 14.81 (computed manually
— the CBOE feed's `prev_day_close` bug recurred a fourth straight edition).
Term structure stayed in normal contango (VIX9D 13.14, VIX3M 18.08, VIX6M
20.16); the FOMC-lookback mechanical distortion tracked since edition 23
looks to have largely stabilized. VVIX 85.77, SKEW 142.19. VIX options
volume approx. 713,342 contracts (moderate confidence — Cboe's stats page
carried no explicit date stamp). CFTC CoT still dated 15 Sept, no new report
this window (next due approx. 25 Sept). Dealer gamma unavailable —
SpotGamma inaccessible, third-party GEX dollar figures implausible and
discarded. Chart #2 (SPDR sector rotation) placed in Section 2 per the
default, since it complemented rather than duplicated chart #1's chip-rally
story. Page 3 ran visibly short on first render (about 40% blank) despite
passing the 4-page check — added an optional Commodities & FX
levels table (Friday-baseline-vs-Monday, legitimately additive since the
main table doesn't show the baseline) plus two extra day-ahead/sector-setup
lines, re-rendered clean at 4 pages. 42 sources, zero mismatches, zero
stray tildes.

**Open threads for edition 26:** SNB's exact September 2026 decision date
(24th vs. 25th — one source may have been a mis-surfaced 2025 article);
Riksbank's 24 Sept decision date (plausible via a press-release title, not
yet confirmed via a direct riksbank.se fetch); a clean, non-rate-limited
Kalshi October-hike fetch (now a structural gap across three editions, like
EUR/GBP used to be); cross-corroborating EUR/USD and GBP/USD against a
second independent vendor beyond Yahoo Finance before calling that thread
fully closed; Monday 21 Sept's SOFR reading (not yet posted at cutoff) and
the still-unexplained cause of the 17 Sept 3.62%→3.85% jump; whether
Monday's quarterly index rebalance produced above-normal trading volume or
volatility (unconfirmed either way); primary-source (S&P Global or similar)
confirmation of reported plans for Block Inc. to replace Hess Corp. in the
S&P 500 effective Wed 23 Sept (found only in secondary market-wrap coverage
this run); whether October-hike odds keep converging or diverge again as
the 27-28 Oct meeting approaches, especially after Thursday 24 Sept's
five-central-bank cluster; confirmation of a firm WTI Monday settlement
(sources still split $92.28-95.80); whether metal.com's persistent failure
(now four editions) means the fallback chain should simply skip straight to
Westmetall.com going forward. Two threads are being dropped after repeated
unreconciled attempts rather than chased further: Asbury Automotive's exact
Thursday 17 Sept close/move (-3.73% vs. approx. -4.8-5.0%, conflicting
across three research passes), and Seagate's/SK Hynix's exact Friday 18
Sept moves (multiple non-reconciled figures across sources).
