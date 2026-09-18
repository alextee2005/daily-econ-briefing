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
   `CHROMIUM_PATH` is set — do **not** run `playwright install`. matplotlib and
   `pdftoppm` (poppler-utils) are present.

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
  13 May 2026, sworn in 22 May 2026. Current full Board (last verified 17
  Sept 2026 via federalreserve.gov's own Board of Governors bio page, plus
  its own record of the oath-of-office press release): Kevin Warsh
  (Chairman), Philip N. Jefferson (Vice Chair), Michelle W. Bowman
  (Vice Chair for Supervision), Michael S. Barr, Lisa D. Cook, Jerome H.
  Powell (Governor — remains on the Board, no longer Chair), Christopher J.
  Waller (Governor). **Re-verify this fresh against federalreserve.gov every
  single edition** — do not carry it forward from a prior run's text or from
  training data.
- **The September 2026 FOMC meeting (15–16 Sept) has now happened and is
  fully resolved.** The Committee raised the federal funds target range
  25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, a unanimous 12-0 vote — the
  first hike since 2023, confirmed directly against federalreserve.gov's own
  press release (monetary20260916a.htm, re-confirmed fresh 17 Sept). Do not
  re-verify the decision itself again.
- **Next FOMC meeting: October 27–28, 2026**, confirmed fresh 17 Sept 2026
  directly against federalreserve.gov's own FOMC calendar page. The Fed's
  calendar itself notes 2026 dates remain "tentative until confirmed at the
  meeting immediately preceding it" — re-confirm the date is still listed
  unchanged each edition as that meeting approaches.
- **October-hike odds have reversed sharply from the approx. 92% figure
  flagged at edition 22** (which was single-sourced to Polymarket and never
  cross-checked). As of 17 Sept, two venues now show hold-leaning-to-coin-flip
  pricing: Polymarket approx. 50-52% hold / 50-51% hike; Kalshi approx. 63%
  hold / 38% hike / 3% cut. Both venues agree directionally (hike conviction
  has fallen well below the prior read) but disagree on magnitude — **verify
  fresh every edition into the 27-28 Oct meeting, disclose both venues, and
  do not average or force a single number.** CME FedWatch remains unobtained
  (page blocks fetching) — worth another attempt if a workaround is found.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks'
  policy rates) from memory or from the prompt's own framing — verify it
  fresh from a primary source (federalreserve.gov, bankofengland.co.uk,
  boj.or.jp, kansascityfed.org, etc.) every edition, exactly like any other
  data point.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote** —
  confirmed fresh directly against bankofengland.co.uk. Same three dissenters
  (Greene, Mann, Pill, all favoring a hike to 4.00%) as the 30 July hold, no
  change in voting alignment. UK CPI was 3.1% in August and the BoE's own
  language flagged inflation risks "tilted to the upside, and more so than at
  the time of the July Monetary Policy Report"; the Bank also announced plans
  for gilt sales of up to £20bn annually. Next BoE decision date not yet
  checked — confirm fresh next edition, do not assume the standard 6-week
  cadence without checking bankofengland.co.uk's own calendar.
- **Bank of Japan: policy rate is currently 1.00%** (hiked 25bp on 16 June
  2026 to what was then the highest level since 1995; held at 1.00% on 31
  July 2026) — confirmed via CNBC/Trading Economics reporting cross-checked
  against the BoJ's own statements page, which lists no 2026 release beyond
  31 July as of 17 Sept. **The BoJ's 17-18 Sept 2026 meeting decision had NOT
  been announced as of this edition's 22:43 ET Thursday cutoff** — boj.or.jp
  showed no September statement posted. Typical announcement timing is
  approx. 11:30am-12:30pm JST on the meeting's second day (approx.
  22:30-23:30 ET the prior evening), which straddled this edition's cutoff.
  Consensus (Bloomberg survey, 52/52 BOJ watchers) is unanimous for +25bp to
  approx. 1.25%. **This is the top open item for the next edition — confirm
  the actual outcome fresh from boj.or.jp, do not assume it happened as
  consensus expected.**

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
  (this bit edition 22 — caught and fixed before render, but avoid it from
  the start next time).
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart #2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes).
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
  has occasionally failed to post in time (it did not post for 15 Sept —
  edition 21 — but posted normally again for 16 Sept — edition 22, three
  independent syndication mirrors checked — so that gap looks like a
  one-off, not a pattern). Fall back to a corroborated secondary source plus
  multi-ETF-proxy triangulation (SPY/DIA/QQQ/IWM vs. their tracked indices)
  and disclose the gap if it recurs.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure.
- Do not repeat items already carried in the previous edition.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET, before
  a 2pm Fed decision) vs. continuously-traded spot (which captured the
  post-decision reversal) — a genuine, explainable divergence, not a data
  error. Check whether two conflicting prices are actually two different
  instruments/timestamps before treating it as a sourcing failure.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done** — and if it reports 0 inline citations found
  while your Annex B clearly has entries, check for the combined-bracket
  `[n][m]` mistake above before assuming something else is wrong.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` delayed-quotes JSON endpoint first — it often
  returns VIX, VIX9D, VIX3M, VIX6M, VVIX and SKEW directly, but has three
  observed failure modes: (a) a full clean sweep with genuinely fresh
  timestamps on every series (the good case — happened at edition 22, all
  series carrying a fresh 16:15 ET timestamp, SKEW at 17:00 ET), (b) the
  more common "thin-series-stale" pattern, where VIX/VIX3M refresh but the
  thinner series (VIX9D/VIX6M/VVIX/SKEW) silently serve a stale prior-session
  snapshot, (c) total failure, where every series is stale. **Always check
  the `last_trade_time` field on each individual series** — never trust that
  the endpoint responded as proof the data is fresh. Note also a
  `prev_day_close` field bug, now observed **two editions running (22 and
  23)**: it duplicates the day's own `close`/`current_price` rather than
  giving a real prior-day reference. At edition 23 this bug propagated into
  the feed's own `price_change_percent` field too (it read -14.70% when the
  true move, cross-confirmed against Yahoo Finance, was -12.82%) — **never
  quote the feed's `price_change`/`price_change_percent` fields directly;
  always compute day-over-day % change manually against the previous
  edition's logged close.** Fall back to news coverage (Yahoo Finance, CNBC,
  MarketWatch) for at least the headline VIX close if the feed is stale, and
  disclose it as single-sourced. Separately: a clean day-over-day term
  structure comparison can look counterintuitive right after an event —
  edition 23 saw VIX9D fall proportionally *more* than spot VIX the day after
  the FOMC decision, simply because the event rolled out of the 9-day
  lookback window. That is a mechanical artifact of the window, not fresh
  risk; check whether a scheduled event just aged out of a tenor before
  reading a term-structure move as new information.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for both the sector
  table and (absent fresher CoT data) chart #2.
- **NYSE/Nasdaq closing breadth:** not obtainable; Reuters' final wrap drops
  the breadth block. Mark unavailable.
- **Dealer gamma:** third-party sources only; mark unavailable unless a
  specific desk note is found and cited. SpotGamma's own substack/site
  articles have started returning 403 on direct fetch (edition 22) — search
  snippets can still surface their headline numbers, but treat as
  lower-confidence secondary sourcing, not a verified primary citation.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Expect
  a genuinely wide range across venues/dates (edition 22 saw pre-meeting odds
  cited anywhere from ~58% to ~93% depending on venue and how close to the
  meeting the citation was dated) — report the range and don't force it to a
  single number.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) worked at
  edition 21 but has now failed two editions running (22 and 23)** — a
  403 both times at edition 23 (both the copper metals page and the closing-
  prices report page). This is starting to look like a real pattern, not a
  one-off — **default to the fallback chain rather than spending much time on
  lme.com**: try Shanghai Metals Market (metal.com) first, but note it failed
  at edition 23 too (historical data required sign-in) — if both fail, use
  Westmetall.com (a German metals-data provider that republishes official LME
  cash/3-month settlement prices) as a same-quality single-sourced fallback,
  and disclose whichever was used. Because the fallback chain can change
  edition to edition, treat any day-over-day copper % change built across two
  different sourcing chains as approximate, not a precise like-for-like
  comparison.
- **Official Treasury par yields:** not posted by the ~20:15 ET cutoff (H.15
  publishes the *prior* day's data the next afternoon — e.g. Wednesday 16
  Sept's official close only became available via the H.15 page on Thursday
  17 Sept). Quote secondary market levels and disclose the gap, or report
  direction vs. the prior official close. The 10-year is usually obtainable
  cleanly via CNBC coverage even same-day (edition 22: 5.016%; edition 23:
  approx. 4.93%, cross-confirmed via the AP wire itself). **The 2-year is
  more failure-prone**: edition 23 saw three conflicting figures (CNBC
  approx. 4.67%, Trading Economics 4.39%, and a WebFetch AI-summary of the
  Treasury.gov par-yield table that produced an implausible 4.07-4.09% —
  treat AI-summarized fetches of data tables as higher hallucination risk
  than a direct news citation, and prefer a source that states the figure in
  prose over one where a model summarized a table). When sources conflict
  this much, cite the best-corroborated one by name with a caveat rather than
  silently picking one or averaging.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly rather than presenting old data as current.
- **GBP/USD clean close:** two editions running (22 and 23) found no single
  authoritative 4pm-London print — poundsterlinglive.com gives a usable
  reference point, but other sources cluster in a range around it. Default to
  reporting the range across sources rather than continuing to hunt for one
  number that may not be publicly reconcilable this way.
- **Gold/silver clean close on a non-event day:** even without an FOMC-style
  settle-vs-spot timing split, Kitco's own quote can differ meaningfully by
  timestamp within the same session (edition 23 saw +0.23% to +1.83% for gold
  depending on which few-hour-apart Kitco snapshot was used). Cite the print
  closest to a standard NY 4-5pm ET close as primary and disclose the wider
  range rather than presenting one snapshot as *the* close.
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue, not with Friday retail sales — confirm on
  the BLS/Fed release schedule rather than assuming a date.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22) — either find a citable
  benchmark before reaching for that chart type, or stick to describing
  implied-vs-realized in prose without the third bar.

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
  wrong.
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
  after the two default blocks — genuinely general-purpose (used across
  holiday, catch-up, and normal single-session windows alike), reach for it
  only when content alone doesn't fill the page.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A roughly 2–3x spread between the
  largest and next-largest mover does not need capping (edition 22's JBHT at
  -13.3% vs. next-largest GS at -3.96%, about a 3.4x spread, was left
  uncapped on this basis — worked fine).

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default). Fresh CFTC CoT data on a
Monday/weekend-window edition → the ES/NQ/RTY asset-manager-vs-leveraged-
funds positioning chart, normalized as net position (% of open interest) to
avoid a scale problem between indices. A single dominant earnings print with
a clean, well-sourced implied-vs-realized-move story → a three-bar
implied/historical-average/realized move chart (see the known-hard-to-source
note above — the historical-average leg has never actually been sourced
successfully yet). A genuine multi-sector broadening/deepening selloff
across consecutive sessions → the sector-ETF proxy rendered as a grouped
(day-over-day) bar instead of single-day. A holiday-window preview edition
with no fresher data → VIX futures term structure with event annotations
(CPI/FOMC/OpEx, etc.). When chart #1 (movers) already covers the earnings
story in depth, the sector proxy is a good complementary choice even on an
earnings-heavy day — used at edition 22 (FOMC day: banks/energy rotation was
the dominant story, movers chart covered JBHT/earnings separately).

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the two most recent in fuller detail and
condense further back each time a new edition is added.

**Editions 1–20 (condensed):** established the format (edition 1 baseline;
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
to "hold vs. hike" on hot core CPI (ed. 19), and Anthropic CEO Dario
Amodei's AI-safety essay driving a chip-selloff/cybersecurity-rally rotation
(ed. 20). First edition under the current 1in/1in/13mm/13mm margins: ed. 19.

**Edition 21 (condensed)** — Wed 16 Sept 2026 report covering Tuesday 15
Sept, day one of the two-day FOMC meeting. A second straight losing session
pricing in the hike (odds 78–92% clustered); 10-year spiked intraday to
approx. 5.045%, a 2007 high. S&P 7,585.73 (-0.45%), Dow 52,093.11 (-0.63%),
Nasdaq 25,981.57 (-0.78%); Energy led (oil spike), Consumer Discretionary
lagged. Enova International -23/-24% (withdrew a bank-acquisition bid), Dave
& Buster's -19% (Q2 miss). Iran/Hormuz: Salalah talks confirmed postponed
(not collapsed). Copper: a direct lme.com fetch succeeded, $14,001/t
(-1.68%). VIX approx. 17.20, after Monday's close was retroactively
corrected to 17.10. 47 sources, zero mismatches.

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
pipeline-restoration progress. Copper: LME direct fetch failed (reversal
from ed. 21); SMM fallback used, approx. $14,250/t. DXY 100.28, 5th straight
up day. VIX closed 17.71 (+3.0%); CBOE feed gave a rare full clean sweep.
Fixed a `check_refs.py` false-negative caused by combined-bracket `[26][27]`
citations (see Confirmed format above). 35 sources, zero mismatches.

**Edition 23 (most recent — full detail)** — Fri 18 Sept 2026 report
covering Thursday 17 Sept, window Tuesday 15 Sept close/AH through Thursday
17 Sept close/AH, research cutoff approx. 22:43 ET Thu 17 Sept. **Fixed the
two header/structure errors edition 22 introduced: the date line now reads
the edition/publication date rather than the session date, and the Method
note is restored after Annex B.**

Dominant story: equities reversed most of Wednesday's post-FOMC selloff as
oil and yields eased. Index closes confirmed directly via the AP wire
("How major US stock indexes fared," cross-checked against three syndication
mirrors plus an independent Yahoo/Bloomberg live-blog figure — both matched
exactly): S&P 7,637.76 (+1.1%), Dow 51,778.04 (+0.6%), Nasdaq 26,418.30
(+1.7%), Russell 2,874.63 (+0.6%). Sector rotation inverted from Wednesday:
Technology (XLK +2.25%) led, Financials (XLF -0.09%) was the only sector
ETF to close lower — banks did not reverse Wednesday's hike-driven losses
(GS +1.44% but WFC -0.18%, C -0.19%) even as the index rallied broadly.
Single-stock movers were broad and idiosyncratic rather than one dominant
story: Generac +18.3% (Amazon data-center backup-power supply deal), Lucid
+10.0% (Bolt robotaxi deal), Intel +7.7% (extending Wednesday's SK Hynix-talk
rally), Micron +5.5% (memory-shortage commentary), AutoNation -9.4% to a
52-week low (auto-dealer sector pressure). J.B. Hunt, Wednesday's -13.3%
mover, was flat despite a same-day Citizens JMP upgrade — the guidance cut
looks priced.

Macro: Fed Chair Warsh and the Sept 16 hike both re-confirmed fresh against
federalreserve.gov; next FOMC meeting confirmed as **Oct 27-28, 2026** via
the Fed's own calendar. **October-hike odds reversed sharply** from edition
22's single-sourced approx. 92% figure — Polymarket now approx. 50-52%
hold, Kalshi approx. 63% hold; disclosed as two disagreeing venues, not
forced to one number. Bank of England held at 3.75%, 6-3 (same three
dissenters as July) — confirmed fresh against bankofengland.co.uk. Bank of
Japan's 17-18 Sept decision had **not** been announced as of the 22:43 ET
cutoff (typical announcement timing straddles that cutoff almost exactly);
consensus is unanimous (52/52 surveyed) for +25bp to approx. 1.25% from a
confirmed-current 1.00%. Initial jobless claims beat (196K vs. 207K cons.);
housing starts and permits both softened; Philly Fed cooled but beat
consensus. 10-year fell to 4.93% (AP-confirmed); 2-year had three
conflicting secondary reads (CNBC approx. 4.67% used, Trading Economics'
4.39% and a WebFetch AI-table-summary's 4.07-4.09% both discarded as
unreliable) — official H.15 for the 17th won't post until Friday.

Commodities: no repeat of Wednesday's genuine gold timing split — Thursday's
prints simply varied by Kitco timestamp ($4,300-4,355 range), the approx.
4:49pm ET print ($4,341, +1.83%) used as primary. Brent $104.82 (-0.95%),
WTI $101.09 (-1.31%), both easing as Saudi Arabia ran ship-to-ship
workarounds around Hormuz. Copper: lme.com failed for a **second straight
edition** (a real pattern now, not a one-off) and the metal.com fallback
also failed (sign-in wall) — Westmetall.com used as a new single-sourced
fallback, $14,409/t. DXY approx. flat (100.22), breaking Wednesday's 5-day
up streak. GBP/USD and EUR/USD both remained hard to pin to one clean close
(GBP/USD reported as a 1.3358-1.3381 range; EUR/USD omitted entirely,
Annex A).

Derivatives: VIX closed 15.44, down 12.82% — but this required a correction,
since the CBOE feed's own `price_change_percent` field read -14.70% off a
broken `prev_day_close` (identical to the day's own close, same bug flagged
at ed. 22, now confirmed recurring); the true move was cross-confirmed via
Yahoo Finance. Term structure stayed in contango but the front-end kink
*widened* in relative terms (VIX9D -23.1% vs. VIX -12.8%) simply because
Wednesday's FOMC event rolled out of the 9-day lookback window — a
mechanical effect, not fresh risk. CFTC CoT still dated 8 Sept (fresh data
due Friday). Chart #2: SPDR sector-ETF single-day rotation bar (the
Tech-led/Financials-lagged inversion was the clearest readable story).
39 sources, zero mismatches, zero stray tildes.

**Open threads for edition 24:** Bank of Japan's 17-18 Sept decision result
(consensus +25bp to approx. 1.25% from 1.00%, unanimous 52/52 survey) — this
is the single most important unresolved item, confirm fresh from boj.or.jp,
do not assume it happened as expected; USD/JPY's stall just under
156.30-156.50 resistance (support eyed 155.00/154.00) makes the BoJ outcome
a real swing event; September triple witching's actual dollar-notional
outcome if a same-day/next-day figure surfaces (approx. $6.2tn Citadel
estimate was several weeks old as cited); fresh CFTC CoT (due Fri 18 Sept
3:30pm ET, covering 15 Sept data) — first update since 8 Sept; whether
October-hike odds continue converging between Polymarket and Kalshi or
diverge further as the 27-28 Oct meeting approaches; whether LME's
direct-fetch failure (now 2 of the last 2 editions) is a durable pattern —
consider defaulting straight to the metal.com/Westmetall.com fallback chain
rather than spending research time on lme.com first; whether a cleaner
GBP/USD and EUR/USD close can be found (both unresolved again this edition);
Conference Board LEI (Fri 18 Sept, 10am ET) — no consensus figure was found
this run, worth another look; Sonic Automotive and Asbury Automotive's
actual Thursday moves, if a reconciled source turns up (both single-sourced/
conflicting this edition, sector-wide auto-dealer pressure was the broader
confirmed theme via AutoNation).
