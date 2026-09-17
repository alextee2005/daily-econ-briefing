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
  13 May 2026, sworn in 22 May 2026. Current full Board (last verified 16
  Sept 2026 via federalreserve.gov's own Board of Governors bio page): Kevin
  Warsh (Chairman), Philip N. Jefferson (Vice Chair), Michelle W. Bowman
  (Vice Chair for Supervision), Michael S. Barr, Lisa D. Cook, Jerome H.
  Powell (Governor — remains on the Board, no longer Chair), Christopher J.
  Waller (Governor). **Re-verify this fresh against federalreserve.gov every
  single edition** — do not carry it forward from a prior run's text or from
  training data.
- **The September 2026 FOMC meeting (15–16 Sept) has now happened.** The
  Committee raised the federal funds target range 25bp to 3.75%–4.00% on
  Wednesday 16 Sept 2026, a unanimous 12-0 vote — the first hike since 2023,
  confirmed directly against federalreserve.gov's own press release
  (monetary20260916a.htm). The SEP/dot plot was hawkish: median fed funds
  4.1% by end-2026 (up from 3.8% in June), 4.1% in 2027 (up from 3.6%); 16 of
  18 participants see at least one more 2026 hike. **This item is now
  resolved — do not re-verify the decision itself, but do verify fresh
  whether an October or later meeting has since produced a follow-up move,**
  since Polymarket was pricing approx. 92% odds of an October hike as of 16
  Sept (single-sourced, not cross-checked against a second venue — worth a
  fresh look).
- **Next FOMC meeting: confirm the date fresh from federalreserve.gov's FOMC
  calendar page** — do not assume from memory. As of the last edition this
  had not yet been re-checked for the meeting after September.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks'
  policy rates) from memory or from the prompt's own framing — verify it
  fresh from a primary source (federalreserve.gov, bankofengland.co.uk,
  boj.or.jp, kansascityfed.org, etc.) every edition, exactly like any other
  data point.
- **Bank of England:** held at 3.75% on 30 July 2026 (divided 6-3 vote); a
  decision was due Thursday 17 Sept 2026 (after this edition's cutoff) —
  confirm the outcome fresh next edition, do not assume "hold" carried
  forward.
- **Bank of Japan:** consensus heading into the 17-18 Sept 2026 meeting was
  +25bp to approx. 1.25% (Bloomberg survey of 52 BOJ watchers, all 52
  expecting the hike); decision expected approx. 18 Sept, 3:30pm JST —
  confirm the outcome fresh next edition, do not assume it happened as
  expected.

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
  `prev_day_close` field bug observed at edition 22: it was identical to
  `close` on the VIX series (not a real prior-day reference) — compute
  day-over-day % change manually against the previous edition's logged close
  rather than trusting that field. Fall back to news coverage (Yahoo
  Finance, CNBC, MarketWatch) for at least the headline VIX close if the
  feed is stale, and disclose it as single-sourced.
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
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has worked via
  direct fetch on some editions** (a specific 3-month copper settlement
  worked at edition 21) **but failed again at edition 22** — it is
  inconsistent, not reliably one way or the other. Try it first for copper,
  but have Shanghai Metals Market (metal.com / SMM's LME 3-month
  morning-meeting minutes) ready as a same-quality single-sourced fallback,
  and disclose whichever was used.
- **Official Treasury par yields:** not posted by the ~20:15 ET cutoff. Quote
  secondary market levels (Trading Economics is the most consistent) and
  disclose the gap, or report direction vs. the prior official close. Note:
  a specific closing-tick 10-year yield *was* obtainable via CNBC coverage
  at edition 22 (5.016%) even though the official H.15 print wasn't — check
  news coverage for an explicit close before defaulting to "direction only."
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly rather than presenting old data as current.
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

**Editions 1–18 (condensed):** established the format (edition 1 baseline;
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
first Ternus-era product event (ed. 17), and Oracle's Q1 FY27 beat with a
vol-crush AH reaction (ed. 18).

**Edition 19** — Mon 14 Sept 2026, cutoff Fri 11 Sept close/AH + weekend
(Sun 13 Sept approx. 20:10 ET). First edition under the revised
1in/1in/13mm/13mm margins (confirmed working, no CSS changes needed).
Dominant story: the Fed's debate flipped from "hold vs. cut" to "hold vs.
hike" after hot core CPI and a collapsed UMich print; hike odds 79–98%
across a wide, disclosed cross-venue spread. Oracle's Friday session
reversed intraday (opened +8.5%, closed -1.74%) on heavy capex/negative FCF.
Copper's Comex-vs-LME "2026 ATH" reopened as an unreconciled cross-exchange
conflict. CFTC CoT (leveraged funds adding to S&P/Nasdaq-100 shorts) used
for chart #2. 58 sources, zero mismatches.

**Edition 20** — Tue 15 Sept 2026, cutoff Mon 14 Sept close/AH. Dominant
story: Anthropic CEO Dario Amodei's weekend AI-safety essay drove a sharp
chip/AI-infrastructure selloff (Corning, Coherent, HP Enterprise, Intel,
AMD, Marvell, Lumentum, Fabrinet) while cybersecurity rallied double-digits
(Zscaler, CrowdStrike, Palo Alto, Okta, Fortinet) — sector rotation (Comm.
Services/Health Care up, Tech/Industrials down) confirmed it cleanly. Hike
odds for Wed 16 Sept firmed to an 84–92% cluster. Dave & Buster's missed
badly after Monday's close (AH reaction later superseded by edition 21's
confirmed Tuesday regular-session close). CBOE's vol feed failed outright
(zero of six series fresh) — VIX's logged 17.42 close was later revised at
edition 21 to a two-source-corroborated 17.10. Copper's Comex-vs-LME
conflict partially resolved (LME pinned to $14,875/t, 10 Sept). 42 sources,
zero mismatches.

**Edition 21** — Wed 16 Sept 2026 report *covering Tuesday 15 Sept*, window
Tuesday 15 Sept 2026 full session/AH, research cutoff approx. 20:08 ET Tue
15 Sept. Day one of the two-day FOMC meeting. Dominant story: a second
straight losing session as the market priced a genuine hike into
Wednesday's decision (hike odds 78–92% clustered; Reuters poll of 101
economists at 85%). 10-year yield spiked intraday to approx. 5.045%, a 2007
high. Index closes (TheStreet + ETF-proxy triangulation, AP wire could not
be located for this session — a gap later resolved at edition 22): S&P
7,585.73 (-0.45%), Dow 52,093.11 (-0.63%), Nasdaq 25,981.57 (-0.78%),
Russell 2,867.27 (-0.86%); Energy (XLE +2.17%) led on the oil spike,
Consumer Discretionary (XLY -1.75%) lagged. Biggest single-stock moves:
Enova International -23% to -24% (withdrew Grasshopper Bancorp bid), Axon
Enterprise approx. -9.8% to -10.8% ($1.0bn convertible-note dilution), Dave
& Buster's -19.0% to $6.86 (Q2 miss reaction). JPMorgan cut Aptiv/Lear/
Magna; Oppenheimer upgraded Etsy. Iran/Hormuz: Salalah talks postponed (not
collapsed) at Saudi request — a correction to edition 20. Commodities:
Brent approx. $107.1 (+1.3%), WTI approx. $103.1 (+1.6%); gold approx. flat
(-0.1%) to approx. $4,290-4,297; silver -0.68% to $62.82; copper — a direct
lme.com fetch succeeded, $14,001/tonne (-1.68%), cooling from 10 Sept's
$14,875/t ATH, closing out the Comex-vs-LME conflict thread; DXY approx.
99.5-99.65 (+0.15-0.22%), 4th straight up day. Derivatives: VIX closed
approx. 17.20 (+0.58%, single-sourced), after a retroactive correction of
Monday's close to 17.10; CFTC CoT dated 8 Sept. Chart #2: SPDR sector-ETF
single-day rotation bar. 47 sources, zero mismatches.

**Edition 22 (most recent — full detail)** — Thu 17 Sept 2026 report
*covering Wednesday 16 Sept*, window Tuesday 15 Sept close/AH through
Wednesday 16 Sept close/AH, research cutoff approx. 20:00 ET Wed 16 Sept.
**The FOMC decision — the lead story flagged as open at edition 21 — landed
this edition.**

Dominant story: the Fed hiked 25bp to 3.75%-4.00%, unanimous 12-0, the first
hike since 2023 — confirmed directly against federalreserve.gov's press
release. The SEP/dot plot was hawkish (median fed funds 4.1% end-2026, up
from 3.8% in June; 16 of 18 participants see at least one more 2026 hike).
Equities initially rose on the decision, then reversed hard during Chair
Warsh's press conference ("inflation remains elevated") to close lower — a
clean intraday-vs-close distinction that needed explicit handling (Fortune's
widely-quoted -1%/-1.7%/-0.8% figures were the press-conference trough, not
the close; disclosed as such rather than silently discarded).

Index closes (AP wire, confirmed via three independent syndication mirrors
plus SPY/DIA/IWM proxy triangulation — resolving edition 21's AP-gap
concern): S&P 7,551.81 (-0.4%), Dow 51,461.90 (-1.2%), Nasdaq 25,978.42
(-0.01%, effectively flat), Russell 2,858.81 (-0.4%). Sector rotation
inverted from Tuesday: Energy (XLE -2.88%) was worst as oil reversed lower,
Financials (XLF -1.62%) second-worst on the hike; only Technology (+0.10%)
and Health Care (+0.07%) closed green. Banks were the clearest single-name
rate-hike losers: Goldman Sachs -3.96%, Wells Fargo -2.98%, Bank of America
-2.72%, Citigroup -2.36% (CEO Solomon flagged softer FICC trading).
J.B. Hunt was the day's biggest mover, -13.3%, on a Q3 guidance warning
(record diesel costs, higher driver expenses) — Barclays/BofA cut price
targets same day. Lennar missed Q3 (EPS $1.23 vs. $1.28 cons., revenue -8.7%
YoY). Intel +4.03% on reported SK Hynix Ohio-fab talks.

Macro: no Iran/Hormuz, US-Canada tariff, or copper-tariff developments
(Salalah talks remain postponed, no new date). August retail sales beat
(+1.2% m/m vs. +0.8% cons., control group +1.4%, strongest since Sept
2024) — a same-day hawkish data point. 10-year yield closed 5.016% (+2bp),
first close above 5% since 2007; 2-year rose to approx. 4.73-4.74%, a 2024
high. Pre-meeting odds ranged 58-93% across venues/dates — never a single
consensus number; disclosed as a range rather than forced to one figure.

Commodities: **a genuine, explainable gold split, not a data error** — COMEX
December futures settled +1.3% to $4,387.50 at the 1:30pm ET pit close
(before the 2pm decision), while continuously-traded spot gold fell 1.2% to
$4,240.10 by 3:10pm ET after the hawkish reversal; both disclosed, spot
treated as the fuller read. Oil reversed sharply (Brent -2.7% to $105.83,
WTI -3.2% to $102.43) on Saudi East-West pipeline restoration progress
(Energy Sec. Wright: "days" to partial, approx. six weeks to full) outweighing
Iran risk premium. Copper: LME's direct site failed this run (a reversal
from edition 21's success) — Shanghai Metals Market's LME 3-month print used
instead and flagged single-sourced (approx. $14,250/tonne, +0.96%). DXY
100.28 (+0.61%), 5th straight up day, biggest 1-day gain since mid-June.

Derivatives: VIX closed 17.71 (+3.0%), intraday spike to 18.94 around the
2pm decision. CBOE feed returned a rare full clean sweep (all series fresh,
16:15 ET timestamp) — term structure kinked: VIX9D (17.40) just below spot,
VIX3M/VIX6M (19.73/21.03) stepped up. SPX realized move -0.45% close-to-close
vs. approx. 1.1% implied from Tuesday's weekly options — a three-bar
implied/historical/realized chart was attempted but dropped for lack of a
sourced historical-average-FOMC-move benchmark (still unsourced as of this
edition). CFTC CoT still dated 8 Sept. Chart #2: SPDR sector-ETF single-day
rotation bar (banks/energy rotation was the dominant readable story; movers
chart separately covered the earnings/guidance angle).

**Production note:** caught and fixed a `check_refs.py` false-negative this
edition — writing two citations as one combined `[26][27]` inside a single
`<sup class="ref">` tag makes the checker's regex silently match zero of
them (see Hard rules and Confirmed format above for the fix: one `<sup>` per
number). 35 sources (renumbered cleanly after the fix), zero mismatches,
zero stray tildes.

**Open threads for edition 23:** Bank of England's Thursday 17 Sept decision
(consensus was hold at 3.75%, but UK CPI at 2.9% keeps a hike live) —
confirm the actual outcome, don't assume hold; Bank of Japan's Friday 18
Sept decision (consensus +25bp to approx. 1.25%, all 52 surveyed watchers
expected it) — confirm the actual outcome; September triple witching Friday
18 Sept (approx. $6.2tn Citadel estimate); fresh CFTC CoT due Friday 18 Sept
covering 15 Sept data; Polymarket's approx. 92% October-hike odds
(single-sourced at edition 22) — check whether a second venue now
corroborates it, and whether Fed communications have shifted the picture
into the October meeting; USD/JPY's outsized move into the Fed decision
(156.11, notable one-day yen weakness) sets up the BoJ meeting as a real
swing event, not a formality; confirm GBP/USD's exact Wednesday close if a
cleaner source turns up (omitted this edition, no verified print found);
watch whether LME's direct-fetch failure this edition was a one-off or the
start of a pattern (it worked at edition 21, failed at 22 — inconsistent
so far, not yet a trend either way).
