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
- **The September 2026 FOMC meeting (15–16 Sept) is fully resolved and does
  not need re-verifying again:** the Committee raised the federal funds target
  range 25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, unanimous 12-0, the
  first hike since 2023.
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed fresh 24 Sept 2026
  (edition 28) directly against federalreserve.gov's own FOMC calendar page
  (Dec 8-9 is the next SEP meeting after that). Re-confirm the date is still
  listed unchanged each edition as that meeting approaches.
- **October-hike odds moved sharply at edition 28 and sources now disagree more,
  not less — re-verify fresh and expect continued volatility into the 27-28 Oct
  meeting:** Polymarket direct fetch showed approx. 65-67% hike probability
  (up from approx. 54-56% at edition 27), following a week of hawkish Fed-speak
  (Governor Barr) and hot data (flash PMI, jobless claims, new home sales).
  CME FedWatch **secondary** citations split badly this run between approx. 54%
  (almost certainly a stale republish of an earlier read) and approx. 73-73.5%
  (consistent with the post-Barr/PMI repricing) — **not reconciled, report both
  rather than picking one until a cleaner read is available.** The official CME
  FedWatch tool itself timed out on direct fetch at edition 28 — keep trying a
  direct fetch each edition. **Kalshi direct fetch failed a sixth straight
  edition (23-28)** — now a confirmed structural gap; keep attempting but don't
  spend much prose on it. Treat the true consensus as "hike-favored, roughly
  60s-to-low-70s%, contested" rather than a single clean number until the
  CME/Polymarket gap narrows.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, etc.)
  every edition, exactly like any other data point.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — this is
  now several editions old and does not need re-confirming again unless a new
  decision date has passed. **Next BoE decision: Thursday 5 November 2026**,
  confirmed directly against bankofengland.co.uk's own MPC-dates page at
  edition 24. Re-check that date is still listed correctly as 5 Nov
  approaches. **Not re-checked at editions 26, 27 or 28** since the date
  remains well out — re-confirm once it's within roughly two weeks.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus — this decision is resolved and does not
  need re-verifying. **The Bank of Japan's next policy meeting is confirmed
  for October 29-30, 2026**, direct from boj.or.jp's own Monetary Policy
  Meeting schedule page (fetched fresh 22 Sept 2026; December 17-18, 2026 is
  also listed further out). Re-confirm this date is still listed unchanged as
  it approaches. **Not re-checked at editions 26, 27 or 28** since the date
  remains well out.
- **The four-central-bank Thursday 24 September 2026 cluster is now fully
  resolved — closed thread, do not re-open:** all four decisions were
  confirmed directly against primary sources at edition 28. **Norges Bank**
  hiked 25bp to 4.50% (from 4.25%), a hawkish surprise, confirmed via
  norges-bank.no's own September 2026 decision page. **Riksbank** held at
  1.75% (matching all 18 economists in a Bloomberg survey) but signalled a
  greater chance of a Q4 hike, confirmed via riksbank.se's own press release.
  **Banxico** held at 6.50% unanimously, confirmed via multiple concordant
  Mexican-press sources (a direct banxico.org.mx fetch redirected to a legacy
  mirror and wasn't completed — try the primary site again next time this
  matters, though the secondary sourcing here was strong and concordant).
  **SNB** held at 0% and raised its inflation forecasts (0.7%/0.8%/0.8% for
  2026-28) — **confirmed directly against snb.ch itself** ("Monetary policy
  assessment of 24 September 2026"), closing the two-edition date-uncertainty
  thread (the SNB's site had 404'd on every attempted URL at editions 26-27).
  No fifth central-bank decision was identified in this window.

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
  show up as "missing" or "unused," it just silently doesn't count, and the
  citation looks fine visually (blue, superscript) without actually pointing
  anywhere. Caught and fixed before render at edition 28 only because the
  citation counts (42 inline vs. 43 Annex B entries before the fix) didn't
  match the expected 1:1 source list — **grep the draft for non-numeric
  bracket content (e.g. `grep -oE '\[[a-zA-Z][^]]*\]' briefing.html`) before
  running `check_refs.py`**, since the script cannot catch this class of
  error on its own.
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
  **Edition 27 and edition 28 are both clean counter-examples worth keeping in
  mind**: both posted an AP wire (edition 28 via WTOP/ABC News) in time, and
  edition 28's AP figure cross-checked exactly against an independent Yahoo
  Finance pull on the S&P 500 closing level — so treat AP/Reuters as "try
  first, expect to sometimes need the fallback chain," not as unreliable by
  default. Always have Yahoo Finance + FRED ready as the working fallback
  regardless of which way this edition goes.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example (Trefis "Market Movers" re-serving
  Friday 18 Sept's figures under a Monday 21 Sept URL); edition 26 caught
  another (several "AP" reposts of Monday 21 Sept's numbers under a Tuesday
  22 Sept dateline); edition 27 caught a third (a techflowpost article
  reproducing Tuesday's numbers under a Wednesday URL, confirmed stale via a
  second source explicitly stating the move happened "on Tuesday"). **Edition
  28 caught a fourth and fifth instance in the same run**: a WebSearch-returned
  AI summary confidently stated Thursday's VIX close was "15.18, up 6.83%" —
  that is Wednesday's already-logged figure, verbatim, mislabeled as Thursday's
  (caught by cross-checking against a direct Cboe feed pull with a verified
  same-day `last_trade_time`); separately, a 24/7 Wall St. article dated
  "Sept 24, 9:08am ET" restated Wednesday's Airbnb close (-7.56% to $149.58)
  as if it were current, caught by cross-checking against stockanalysis.com's
  own history table showing that figure under the *prior* day's row. **This is
  now five documented instances across five consecutive editions (24-28)** —
  treat same-numbers-as-yesterday as the standing tell, and always locate a
  second, independently-dated source (or a source with a verifiable
  same-day timestamp field) before accepting a "today"-dated figure at face
  value — this now applies just as much to AI-summarized search results as to
  aggregator news articles. **A same-day close and a next-day after-hours-
  triggered move can legitimately combine into one large single-day % change**
  — edition 24's Xenon Pharmaceuticals -30.7% Friday move looked at first like
  it might conflict with a same-day "+1% then -25% after-hours Thursday"
  report, but both were correct. Check whether a headline % move is measured
  close-to-close (which will include an intervening after-hours event) before
  assuming two reports conflict. **A related but distinct trap surfaced at
  edition 26 and recurred in milder forms at editions 27 and 28:**
  intraday-move coverage vs. the actual close can diverge sharply even with no
  after-hours event involved — Worthington Enterprises (WOR, ed. 26), Paychex
  and Cracker Barrel (ed. 27), and at edition 28 a reported Oracle intraday
  drop of "6-7%" vs. its actual -3.47% close, all showed this pattern. Treat a
  stockanalysis.com (or equivalent timestamped) closing print as authoritative
  over an intraday-coverage percentage, and cross-check against a second,
  independent source (a wire story or piece explicitly describing the close)
  when available rather than just picking the stockanalysis.com number in
  isolation.
- Do not repeat items already carried in the previous edition.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET, before
  a 2pm Fed decision) vs. continuously-traded spot (which captured the
  post-decision reversal) — a genuine, explainable divergence, not a data
  error. Check whether two conflicting prices are actually two different
  instruments/timestamps before treating it as a sourcing failure. Edition 26
  found a similar but less cleanly-explained case: Kitco/Fortune's 4:32pm ET
  gold spot read ($4,358.80, -0.45%) and USAGOLD's own daily report
  ($4,307.63, which recomputes to approx. -1.62% against the same Monday
  baseline) disagreed by more than a normal cross-vendor spread, with no
  identifiable settle-vs-spot timing mechanism to explain it (both are spot
  reads) — disclosed as a genuine, unreconciled divergence rather than forced
  to one number. **This gap narrowed across the next two editions and, as of
  edition 28, has essentially closed**: edition 27 found it down to about $7
  (Kitco $4,297.53 vs. USAGOLD $4,304.11); edition 28 found the two vendors
  just $0.16 apart ($4,273.20 vs. $4,273.36). **Treat the Kitco-vs-USAGOLD
  vendor split as resolved going forward** unless it re-widens — no need to
  keep tracking it as an open thread. One residual wrinkle from edition 28:
  each vendor's own *stated* day-over-day % change still implied a
  slightly different Wednesday baseline than the other vendor's own prior-day
  figure (Kitco's own baseline recomputes close to the previously-logged
  figure; USAGOLD's own -0.32%/-$13.74 implied a baseline about $17 off from
  its own previously-logged Wednesday figure) — worth a glance next time but
  not worth chasing hard given the headline gap is now negligible.
  Similarly, **a price level can be correct while a vendor's stated %-change
  is wrong** if the vendor used a different prior-day base — edition 24 found
  WTI's Friday level ($100.30) and stated -1.58% change both correct only
  once Thursday's true settle was corrected from a previously-published
  $101.09 to $101.91 (see edition log) — always sanity-check that a stated
  price level and stated % change actually reconcile arithmetically against
  the prior session's logged close before reporting both. **The oil
  contract-month-roll trap, seen at editions 24, 25/26 and 27, did NOT recur
  at edition 28** — Wednesday's roll to the November contract held cleanly
  into Thursday, with both days' prints on the same contract month and a
  clean, reconcilable +2.7%/+3.4% change for WTI/Brent. **The general lesson,
  reinforced four times now:** whenever a commodity price splits or looks
  discontinuous across sessions, check for a contract-month roll or a
  contract-month mismatch across sources before concluding it's a sourcing
  failure — and don't assume the trap recurs just because it has before;
  edition 28 confirms it isn't present every session, just worth checking.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done** — and if it reports 0 inline citations found
  while your Annex B clearly has entries, check for the combined-bracket
  `[n][m]` mistake above before assuming something else is wrong. Also
  remember it only scans HTML text — a citation number baked into a chart
  PNG's label is invisible to it (see Confirmed format above), and so is a
  bare `[n]` typed outside any `<sup>` tag, and so is a **non-numeric
  placeholder like `[note1]`** (see Confirmed format above, new at edition
  28) — none of these will show up as a mismatch in the script's counts, so a
  citation-count sanity check (does the inline count roughly match the Annex B
  count you expect?) is a useful independent cross-check on top of running the
  script. Also remember it flags Annex B entries that were drafted but never
  actually cited inline (e.g. in a movers table) — edition 26 hit this with
  four single-stock sources drafted into Annex B before the citations were
  added to the movers table's driver column, and edition 28 hit a milder
  version (one prose-only source, the Washington Post wrap, was named in text
  but not cited) — caught and fixed both times by running the check before
  declaring done, per this rule.
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
  Commodities & FX table didn't display; edition 28 did the same thing again
  — a Wednesday-baseline-vs-Thursday-close table covering oil, gold, copper,
  DXY, the major FX crosses and VIX — after page 3 first rendered about 40%
  short) — don't reject the idea purely because the instrument list overlaps;
  check whether the *added* column carries real information first. **Edition
  28 also confirms the overshoot risk on the other side**: the first version
  of its levels table (12 rows, including 10-year/2-year Treasury rows whose
  "not yet posted" status was already stated in prose) pushed the document to
  5 pages; trimming to 10 rows (dropping the two Treasury rows and shortening
  one cell's text) brought it back to a well-balanced 4. **When adding this
  table, budget it at roughly 9-10 rows of genuinely new instruments, not
  every instrument mentioned anywhere in Section 4** — re-render and check the
  page count immediately after adding it rather than assuming the row count
  is safe. Not needed at editions 26 or 27, which filled page 3 from content
  alone.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` delayed-quotes JSON endpoint first — it often
  returns VIX, VIX9D, VIX3M, VIX6M, VVIX and SKEW directly, but has (at least)
  three observed failure modes: (a) a full clean sweep with genuinely fresh
  timestamps on every series, (b) the more common "thin-series-stale"
  pattern, where VIX/VIX3M refresh but the thinner series silently serve a
  stale prior-session snapshot, (c) total failure, where every series is
  stale (including a "full stale sweep" variant seen at edition 27, where
  even VIX itself carried the prior session's `last_trade_time`). **Edition
  28 got a full clean sweep** — every one of VIX/VIX9D/VIX3M/VIX6M/VVIX/SKEW
  carried a same-day `last_trade_time`, verified individually per series via
  a raw `curl` pull (not a tool-summarized fetch, which had previously
  produced an AI-hallucinated "Thursday" figure that was actually Wednesday's
  — see Hard rules above) — so the "full stale sweep" mode does not appear to
  be a permanent state; keep checking `last_trade_time` on each series every
  time regardless of which mode you got last edition. Also note a
  `prev_day_close` field bug, observed **seven editions running (22-28)**:
  it duplicates the day's own `close`/`current_price` rather than giving a
  real prior-day reference, and this corrupts the feed's own
  `price_change`/`price_change_percent` fields too — **never quote the
  feed's `price_change`/`price_change_percent` fields directly; always
  compute day-over-day % change manually against the previous edition's
  logged close.** Fall back to news coverage (Yahoo Finance, CNBC,
  MarketWatch) for at least the headline VIX close if the feed is stale, and
  disclose it as single-sourced. Separately: the mechanical VIX9D-vs-spot-VIX
  distortion from the 16 Sept FOMC aging out of the 9-day lookback window
  (tracked editions 23-25, stabilized since) has not re-emerged in its
  original form, but **edition 28 found spot VIX (15.67) sitting above
  VIX9D (14.11) — an unusual front-end inversion** worth a second look next
  edition to see if it's a fresh, distinct pattern or noise.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table
  and (absent fresher CoT data or another dominant story) chart #2. Worked
  cleanly again at editions 26, 27 and 28. **Stockanalysis.com single-stock
  pages are also the standing default for pinning an exact closing
  price/% change on any individual mover** — editions 26, 27 and 28 all used
  direct fetches to it to resolve several sources' conflicting intraday-move
  percentages (edition 28: Oracle's reported "6-7% intraday" drop vs. its
  actual -3.47% close, MGM Resorts, Darden, Costco, Meta, and the Expedia/
  Airbnb rebound). Worth doing proactively for any mover whose research-pass
  figures disagree by more than a rounding error, rather than only for the
  single biggest story of the day. Note that a headline wire's own GICS
  sector-index percentages can differ slightly from the SPDR ETF price-change
  figures (a normal index-vs-ETF-price methodology gap, not a data conflict);
  keep using the SPDR ETF figures as the table's primary numbers (for
  consistency with the chart) and mention a wire variant only if it's
  notably different.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**, but note wire commentary sometimes gives a usable
  qualitative/approximate breadth read in prose even when the table isn't
  available. Not needed at edition 28 — no breadth commentary was chased this
  run since the AP wire's own "roughly back where they started" framing
  already captured the session's character.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page on direct fetch — this has now
  recurred at editions 22, 24, 25, 26, 27 and 28 (six straight). **zerogex.io
  is now a confirmed, repeatable alternative across two straight clean
  editions (27 and 28)**: edition 27 gave a dated read reconciling well
  against the 7,706 close, and edition 28 gave a second dated, timestamped
  read (net SPX GEX +$3.63bn, down from +$9.47bn, flip level 7,698) that
  again reconciled well against the actual 7,704.13 close. **Promote this
  from "worth trying" to the standing default source for dealer gamma** —
  still worth a SpotGamma attempt first each edition in case it recovers, but
  treat zerogex.io as reliable rather than experimental at this point, and
  keep watching whether the reconciliation-against-actual-close pattern holds
  for a third edition.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Edition
  27's secondary citations had converged to approx. 54-55.1%; **edition 28's
  secondary citations split badly instead, between approx. 54% (likely a
  stale republish) and approx. 73-73.5%** — a reminder that convergence in
  one edition doesn't mean the sourcing problem is solved; keep treating CME
  FedWatch as needing a disclosed range, not a single figure, and expect the
  degree of disagreement to vary edition to edition with how much the
  odds are moving.
- **Kalshi direct fetch:** now rate-limited (HTTP 429) for **six straight
  editions (23-28)** — this is a confirmed structural gap, not a transient
  issue. Keep attempting a direct fetch each edition (it may recover), but
  there is no need to spend much prose on the failure each time — a one-line
  "failed again, Nth straight edition" plus whatever Polymarket/CME-FedWatch
  range is available is sufficient.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  seven editions running (22-28)** — treat this as a durable, confirmed
  pattern rather than re-attempting lme.com first each time; **default
  straight to the fallback chain.** Shanghai Metals Market (metal.com) has
  now failed **seven editions running (22-28)** — skip metal.com entirely and
  go straight to Westmetall.com (a German metals-data provider that
  republishes official LME cash/3-month settlement prices), which has now
  worked cleanly **seven editions running** as the fallback. Disclose
  whichever was used. Because the fallback chain can change edition to
  edition, treat any day-over-day copper % change built across two different
  sourcing chains as approximate, not a precise like-for-like comparison.
- **Official Treasury par yields:** official home.treasury.gov H.15 data for
  the prior day worked cleanly for editions 25 and 26 for both the 10-year
  and 2-year. Edition 27 found a same-day TextView pull for the 2-year gave
  an implausible reading (4.10%) while the 10-year same-day read was broadly
  consistent — **FRED (fred.stlouisfed.org, DGS10/DGS2) proved the more
  reliable route for pinning the most recently *completed* trading day's
  yields (it lags one business day, same as official H.15)**, and edition 28
  used exactly this pattern to resolve Wednesday's previously-unresolved
  2-year close at 4.85% and reconfirm the 10-year at 5.11% (in line with the
  prior estimated range). **This pattern is now confirmed working across two
  consecutive editions (27 and 28) — keep using FRED as the primary route for
  the prior completed day's yields, and expect the *current* day's close to
  simply not be available yet (same T+1 lag) rather than trying to force a
  same-day TextView read**, which has been unreliable, especially for the
  2-year. CNBC's own quote pages (US10Y/US2Y) returned HTTP 403 on direct
  fetch at edition 26 — not re-tried since.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly rather than presenting old data as current. Note
  the report comes in (at least) two different methodologies/pages depending
  on the instrument: `financial_lf.htm` (Traders in Financial Futures, Asset
  Manager/Leveraged Funds categories) works well for equity index futures
  (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report is what actually carries VIX futures
  positioning — don't expect one page to have both. As of edition 28 the most
  recent data is still dated 15 Sept (published Friday 18 Sept, confirmed via
  direct fetch and an unchanged `Last-Modified` header); the next report was
  due approx. Friday 25 Sept, which postdates edition 28's own Thursday
  20:20 ET cutoff — check for it fresh next edition.
- **GBP/USD and EUR/USD clean close:** fully resolved as of edition 26 —
  Yahoo Finance as primary is the standing working pattern for both pairs,
  confirmed again cleanly at editions 27 and 28. **The DXY-vs-majors
  magnitude-mismatch flagged at edition 27 (DXY +0.53% vs. much smaller
  EUR/USD/GBP/USD moves) did not repeat in the same form at edition 28** —
  Thursday's DXY move (Yahoo: +0.19%) was directionally consistent with
  EUR/USD (-0.58%), GBP/USD (-0.76%) and USD/JPY (+0.51%), all pointing to
  dollar strength. A separate, smaller-magnitude version of the same puzzle
  did appear: a naive weighted contribution from just those three pairs
  (approx. +0.49%) ran somewhat larger than DXY's own +0.19% move — plausibly
  explained by other basket currencies (CAD, SEK, CHF) moving against the
  dollar, not confirmed. **New at edition 28: DXY itself now has a genuine
  cross-source split** — Yahoo Finance showed 101.29 (+0.19%) while
  TradingEconomics showed 101.08 (-0.02%), disagreeing on both level and
  direction. Yahoo was used as primary (consistent with the FX-pair moves and
  the established working pattern); the TradingEconomics read was disclosed
  as a disagreement rather than discarded. Worth watching whether this
  Yahoo-vs-TradingEconomics DXY split recurs.
- **Gold/silver clean close on a non-event day:** **this thread is now
  resolved and can be dropped from active tracking.** The Kitco-vs-USAGOLD
  split that first appeared at edition 26 (approx. $50 apart) narrowed to
  approx. $7 at edition 27 and to $0.16 at edition 28 — for three editions
  running the gap has only closed, never widened, and edition 28's gap is
  small enough to treat as normal cross-vendor noise rather than a genuine
  divergence needing disclosure. Continue citing both if convenient, but
  it no longer needs the "unreconciled split" framing in the main text. One
  minor residual: each vendor's *stated* own day-over-day % change can still
  imply a slightly different prior-day baseline than the other vendor's own
  previously-logged figure — not worth chasing given the headline gap is
  now negligible.
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue, not with Friday retail sales — confirm on
  the BLS/Fed release schedule rather than assuming a date. **PCE inflation
  (Personal Income and Outlays):** confirmed via bea.gov (most recently
  re-checked at edition 28) that the report covering a given month's data
  publishes at the *end* of the following month — August 2026 data is
  confirmed for **Tuesday 30 September 2026**, 8:30am ET. Re-confirm once
  more as that date arrives, then this thread can close.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27 via direct philadelphiafed.org fetch (Tuesday 22 Sept release,
  Regional Activity Index -22.0). Closed thread — no action needed unless a
  future release date approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  a new, more serious data-quality problem surfaced at edition 28 and needs
  chasing next time this page is used. Edition 27 logged 902,421 contracts
  for Wednesday (confirmed as "not a stale repeat" of Tuesday's figure at the
  time). At edition 28, the *same URL*, when checked for a Thursday figure,
  instead showed the page's most recent populated date as Wednesday 23 Sept
  again — but this time with a **Wednesday total of 13,781,355 contracts**
  (call 7,416,936 / put 6,364,419), roughly **15x larger** than the
  902,421 previously logged for the same date. This looks like two different
  tables/categories living on the same URL (e.g., a single-exchange vs.
  all-exchange total) rather than either figure being simply wrong, but it
  was not resolved at edition 28. **Next edition: before citing any figure
  from this page, identify which specific table/category is being read (look
  for a selector, tab, or column header distinguishing exchange scope) and
  note it explicitly** — do not assume the two prior editions' figures
  (713,342 and 902,421) are comparable to each other or to this new
  13,781,355 reading until that's sorted out. Also note Thursday's own figure
  had still not posted to this page as of edition 28's cutoff — the page
  appears to lag by at least a session.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22) — either find a citable
  benchmark before reaching for that chart type, or stick to describing
  implied-vs-realized in prose without the third bar. Not attempted again at
  editions 23-28 since no single dominant earnings print called for it.
- **CFTC total open interest by instrument/date** (needed to normalize
  positioning "as % of open interest" per the chart-#2 guidance) was not
  obtainable via quick search at edition 24 for the 15 Sept report — a
  category's own gross long+short was used as a substitute denominator
  instead (see Hard rules above). Worth trying cftc.gov's own report pages
  directly (rather than search) next time this chart type is needed, since
  the total OI figure is normally printed in the report header. Not
  revisited at editions 25-28 since no fresh CoT data posted in any of those
  windows (still dated 15 Sept as of edition 28).
- **Named-desk confirmation of individual index-fund passive-flow figures**
  (e.g. estimated closing-auction imbalance dollar amounts around a
  quarterly rebalance) tends to come from independent research
  Substacks/blogs (e.g. QSG Research) rather than a sell-side desk by name —
  treat as citable but note it's not a bulge-bracket named source when it
  matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear** — editions 27 and 28
  both confirmed several rating changes (direction + firm name) without being
  able to pin an exact dollar price target for all of them via available
  sourcing. Report the rating direction and firm with confidence; treat a
  missing dollar target as a normal gap to flag rather than something to
  chase hard, unless the name is the edition's dominant story.

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
  wrong — but note the CSS rule definition itself also contains the string
  "pagebreak," so a raw `grep -c` will show 2 for a correctly-built document
  (one CSS rule + one actual `<div>` usage); check specifically for
  `<div class="pagebreak">` occurrences, not the raw grep count, when
  verifying there's exactly one usage. **A 5-page render is not always a
  stray break** — edition 24 hit 5 pages with only the one correct pagebreak
  present; the cause was genuine copy overflow. Edition 28 hit the same
  overflow-not-a-stray-break situation after intentionally adding an optional
  filler table that turned out to be a few rows too long — the fix in both
  cases was trimming content (rows from the added table, in edition 28's
  case), not hunting for a phantom extra break. Check `grep -n pagebreak`
  first as the cheap check, but if that comes back clean (one real `<div>`
  usage), read the actual page images: the fix is trimming a handful of
  lines/rows from whichever page is overflowing, not hunting for a break that
  isn't there.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`.
- Always verify the render: `pdftoppm -png -r 72` (or higher resolution, e.g.
  `-r 100`, for easier visual review) and actually read the page images
  before delivering — don't trust the page count alone. Edition 25's page 3
  ran visibly short (roughly 40% blank) on the first render despite passing
  the 4-page check; adding the optional Commodities & FX levels table fixed
  it. **Edition 28 hit the same short-page-3 symptom and used the same fix**
  (a Wednesday-baseline-vs-Thursday-close levels table), but the first
  attempt overshot into a 5-page render — trimmed from 12 rows to 10 and
  re-rendered clean at 4 pages. **The lesson compounds: after adding filler
  content of any kind, always re-render and re-check the page count
  immediately — don't assume a "genuinely additive, moderate-sized" table is
  automatically safe.** Editions 26 and 27 both rendered a well-balanced 4
  pages on the first try with no padding block needed — content volume alone
  was enough both times, so don't reach for the filler table reflexively;
  check whether page 3 actually runs short first.

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
  fills 3 pages). **An optional "Commodities & FX levels" table (~9-10 rows,
  not more)** at the end of Section 4 is available as padding if page 3 runs
  short after the two default blocks — genuinely general-purpose, reach for
  it only when content alone doesn't fill the page. It doesn't have to be a
  from-scratch instrument list: a Wednesday-baseline-vs-Thursday-close (or
  equivalent) comparison for instruments already in the main Commodities
  table is legitimate padding because the *baseline* column is new
  information, not a straight duplicate — used at edition 25 and again at
  edition 28. **Budget this table conservatively (9-10 rows)**: edition 28's
  first attempt at 12 rows (including two Treasury-yield rows whose content
  was already stated in prose) pushed the document to 5 pages; trimming to
  10 rows fixed it. Always re-render immediately after adding this table to
  confirm the page count, rather than assuming a "moderate" row count is
  safe. Conversely, **if page 3 overflows by a handful of lines**, the
  cheapest trims are: shortening day-ahead table cell text, cutting one
  "sector setup" bullet or merging two into one, tightening the last prose
  paragraph in Section 5, or trimming rows from the optional levels table if
  one was added — usually 3-6 lines/rows is enough, re-render and re-check
  rather than guessing how much was needed.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 3x between
  the largest and next-largest mover does not need capping (edition 22's
  JBHT at -13.3% vs. next-largest GS at -3.96%, about 3.4x, was left
  uncapped; edition 24's XENE at -30.7% vs. next-largest SNDK at +11.0%,
  about 2.8x, was also left uncapped on the same basis; edition 25's GRAL at
  approx. +30% vs. next-largest ARM at +16.6%, about 1.8x, needed no
  capping either). Edition 26 extended the precedent further: VKTX at
  +35.67% vs. next-largest ONON at +7.58%, about 4.7x — still left uncapped,
  since "order of magnitude" (approx. 10x) is the actual threshold and 4.7x
  reads fine on the standard axis. Edition 27's spread was much narrower
  still (PAYX -8.77% vs. next-largest EXPE -7.72%, about 1.14x) — obviously
  no capping needed. **Edition 28's spread (MGM -10.99% vs. next-largest
  META +4.50%, about 2.4x) also needed no capping.** The rule has not yet had
  a genuine 10x+ case to test.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used again at edition 28 for a
Meta-Muse-driven Communications-Services-led rotation, at edition 27 for a
genuine rate-spike-driven rotation into defensives, at edition 26 for a
financials-vs-materials rotation reversal, and at edition 25 for a broad
chip-led rally with sector rotation as the clearest secondary story — this is
now the fourth consecutive edition using this default, and it continues to
work well). Fresh CFTC CoT data on a Monday/weekend-window edition → the
ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart — **normalize as
% of open interest if that figure can be sourced; if not, a category's own
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
(movers) already covers the earnings/single-name story, the sector proxy is a
good complementary choice even on a stock-heavy day — editions 25, 26, 27 and
now 28 have all used exactly this combination (single-name movers as chart
#1, sector rotation as chart #2) with the two stories reinforcing rather than
duplicating each other every time. **Chart #2's placement in the document
should follow its content, not a fixed section** — a CFTC/positioning chart
reads better in Section 5 than Section 2 even though the asset template
defaults to embedding it right after the Section 2 heading (edition 24).

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–26 (condensed):** established the format (edition 1 baseline;
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
edition 21's Tuesday 15 Sept report (day one of the two-day FOMC meeting): a
second straight losing session pricing in the hike, 10-year spiked intraday
to approx. 5.045% (a 2007 high), S&P 7,585.73 (-0.45%); edition 22 (Thu 17
Sept, covering the Wed 16 Sept FOMC day): the Fed hiked 25bp to 3.75%-4.00%,
unanimous 12-0, equities reversed hard during Chair Warsh's press conference
to close lower (S&P 7,551.81 -0.4%), 10-year first closed above 5% since
2007, a genuine COMEX-vs-spot gold settle-timing split, copper's LME
direct-fetch failure streak began here; edition 23 (Fri 18 Sept, covering
Thu 17 Sept): equities reversed most of the post-FOMC selloff (S&P 7,637.76
+1.1%), Bank of England held at 3.75% (6-3), Generac +18.3%, Lucid +10.0%;
edition 24 (Mon 21 Sept, covering Fri 18 Sept triple witching + weekend
catch-up): approx. $7tn September triple-witching notional expired alongside
the quarterly S&P/Nasdaq-100 rebalance, Xenon Pharmaceuticals -30.7%, Warren
Buffett stepped down as Berkshire chairman, Bank of Japan hiked 25bp to
approx. 1.25% (31-year high, 7-2 split), copper fallback chain moved to
Westmetall after lme.com/metal.com both failed; edition 25 (Tue 22 Sept,
covering Mon 21 Sept): a broad chip-stock rally (Intel +12.0%, AMD above a
$1tn market cap, Arm +16.6%) pushed the Nasdaq to a record 27,122.09
(+2.26%), the quarterly S&P 500/400/600 and Nasdaq-100 rebalance took effect,
EUR/USD and GBP/USD both got clean single Yahoo Finance closes for the first
time; and **edition 26** (Wed 23 Sept, covering Tue 22 Sept, the window's
one NYSE session): a financials-led sector rotation rather than a broad
index move — S&P effectively flat at 7,764.64 (-0.00%), Dow -0.36% to
51,863.69 on a bank selloff (JPMorgan -3.42%, Wells Fargo -3.92%), Nasdaq a
second consecutive record close at 27,244.28 (+0.45%) — confirmed via
Yahoo Finance/FRED after several syndicated "AP" reposts were caught
stale-republishing Monday's numbers under a Tuesday date. A paywalled
Bloomberg piece first floated the "Meta Muse AI shopping agent
disintermediation" thesis tying the bank selloff to Expedia/Booking/Carnival/
American Airlines moves (later corroborated at edition 27). Viking
Therapeutics +35.67% was the standout single-name mover. The Block Inc./Hess
Corp S&P 500 swap open thread (carried from edition 25) was resolved as a
stale premise — the actual swap happened in July 2025, over a year earlier,
not "effective Wed 23 Sept" as reported. Treasury H.15 gave a clean 10-year
4.96% flat and what was then logged as a 2-year of 4.43% — corrected to
4.71% at edition 27, then further corrected to 4.85% at edition 28 (all
three figures reference the same Tuesday 22 Sept session; treat 4.85% as
final). The five-central-bank Thursday/Friday cluster was first dated here
(SNB initially misdated Friday 25 Sept, corrected to Thursday 24th at
edition 27, confirmed directly at edition 28). Gold showed a genuine
Kitco-vs-USAGOLD split (approx. $50 apart) that closed over the following
two editions (see Known-hard-to-source above). VIX closed 14.21 (lowest
close of the year at the time, -4.44%) on a full clean CBOE sweep. 50
sources, zero mismatches.

**Edition 27 (condensed)** — Thu 24 Sept 2026 report covering Wednesday 23
Sept 2026, the window's one NYSE session. A broad risk-off session: S&P 500
-0.75% to 7,706.03, Dow -0.68% to 51,511.59, Nasdaq -1.13% to 26,936.04,
Russell -1.77% to 2,838.66 — confirmed via two independently-agreeing wires
(AP via ABC News, Reuters via Honolulu Star-Advertiser) after both had failed
to post Tuesday's close in time for the prior two editions. A live
stale-date-republishing trap was caught and discarded (a techflowpost article
reproducing Tuesday's exact index levels under a Wednesday URL). Driver: the
10-year Treasury spiked to a 19-year high (approx. 5.09-5.14%, not fully
reconciled) after a hot flash September composite PMI (58.4, strongest since
July 2021) and Fed Governor Barr's Chicago remarks that inflation is "not
clearly trending toward target." Sector rotation flipped to rate-driven:
Utilities and Real Estate worst, Energy the only sector up. The "Meta Muse"
AI-agent disintermediation theme (flagged paywalled/unconfirmed at edition
26) rotated from banks into online travel names and was independently
corroborated: Expedia -7.72%, Airbnb -7.56%, Booking -5.07%, while Meta rose
+1.02% and got a Cantor Fitzgerald price-target raise to $860 (from $680); a
Goldman Sachs note explicitly extended the thesis to financials, insurance
and telecom. Paychex -8.77% (earnings-quality concerns despite a topline
beat); Cracker Barrel +4.49% (large adjusted-EPS beat). Alphabet -3.80% and
Amazon -2.24% fell on pure yield-driven de-rating with no company-specific
news. Correction: edition 26's logged Tuesday 2-year Treasury (4.43%) was
corrected to 4.71% via a fresh FRED pull (itself later refined to 4.85% at
edition 28 — all reference the same Tuesday session). Resolved the
Philadelphia Fed Nonmanufacturing Business Outlook thread (Tuesday 22 Sept
release, Index -22.0, confirmed via direct philadelphiafed.org fetch).
October-hike odds converged into the mid-50s across venues for the first
time in several editions (Polymarket approx. 54-56%, CME FedWatch secondary
citations approx. 54-55.1%) — this convergence did not hold at edition 28,
where odds jumped and sources diverged again. The five-central-bank
Thursday/Friday cluster saw SNB's date corrected from Friday 25 Sept to
Thursday 24th (confirmed directly at edition 28). Oil hit a fresh instance of
the contract-roll trap on the WTI Oct-to-Nov roll itself (did not recur at
edition 28). Gold's Kitco-vs-USAGOLD split narrowed to about $7 (from approx.
$50) — closed entirely by edition 28. VIX closed 15.18 (+6.83%, computed
manually) on a CBOE feed "full stale sweep" failure (recovered to a full
clean sweep at edition 28). zerogex.io gave a first working dealer-gamma
read, later confirmed repeatable at edition 28. 35 sources, zero mismatches,
zero stray tildes.

**Edition 28 (most recent — full detail)** — Fri 25 Sept 2026 report
covering Thursday 24 September 2026, the window's one NYSE session, research
window Wed 23 Sept 20:00 ET through Thu 24 Sept 20:20 ET. Verified the two
structural header rules again: date line reads the edition date (Friday 25
September 2026), not the session date; window line starts at the given
research-window start (Wed 23 Sept 20:00 ET), not earlier.

A genuine whipsaw session that closed almost exactly flat: S&P 500 -0.1% to
7,704.13, Dow -0.3% to 51,349.98, Nasdaq Composite +0.1% to 26,939.37,
Russell 2000 -0.1% to 2,835.57 — confirmed via the AP wire (through WTOP/ABC
News), with the S&P closing level cross-checking exactly against an
independent Yahoo Finance pull. The AP wire's own framing ("ended the day
roughly back where they started after whipping through a couple reversals")
was the most accurate one-line summary, corroborated by a separately-sourced
Washington Post wrap. A live stale-date/hallucination trap was caught twice
in one run: a WebSearch AI summary confidently restated Wednesday's VIX close
(15.18) as Thursday's, and a 24/7 Wall St. article dated Thursday morning
restated Wednesday's Airbnb close — both caught via cross-checks against
sources with verifiable same-day timestamps (a direct Cboe `curl` pull with
`last_trade_time` verification, and stockanalysis.com's own dated history
table).

Sector leadership flipped entirely from Wednesday's rate-driven,
Energy-only-positive pattern: Communication Services (XLC +1.27%) led on
Meta's rally, Health Care (XLV +0.63%) and Energy (XLE +0.37%, still
positive on the oil spike) followed; Materials (XLB -1.19%) and Utilities
(XLU -0.98%) lagged; Financials (XLF -0.02%) stabilized further after two
rough sessions. Single-name stories dominated: MGM Resorts -10.99% after
Barry Diller's People Inc. withdrew its $48.30/share take-private bid;
Oracle -3.47% on a force-majeure notice to developer Blue Owl Capital tied to
a delayed gas-pipeline commissioning threatening the Stargate New Mexico
data center's 2028 target; Darden Restaurants -3.02% on a razor-thin Q1
EPS/revenue miss; Paychex -2.78% (second-day continuation of Wednesday's
earnings-quality selloff, no new news); Costco -0.91% in the regular session
before reporting a Q4/FY2026 beat (EPS $6.75 vs. approx. $6.55 consensus,
comps +9.4%) after the close to a muted after-hours reaction, with the
fuller market verdict falling in Friday's session outside this window; and
Meta Platforms +4.50% (best month since 2013) after detailing Muse AI-agent
monetization at Connect — a partner-fee model (including a travel
integration through Expedia) rather than pure bypass, which let Wednesday's
Muse-driven travel-stock selloff partially reverse (Expedia +1.05%, Airbnb
+1.21%, Booking +0.97%). Analyst actions: Oppenheimer raised its Dynatrace
target to $71 from $60 (Top Picks addition); Jefferies cut Edison
International to $53 from $68; Citi initiated Rivian at Neutral, $18; Bank of
America maintained Buy on Ecolab, $342 target.

Macro: Fed Chair Kevin Warsh and the Oct 27-28 FOMC date both re-confirmed
fresh. All four previewed Thursday central-bank decisions landed and were
confirmed against primary sources: Norges Bank hiked 25bp to 4.50% (hawkish
surprise); Riksbank held at 1.75% (unanimous per a Bloomberg economist
survey) but flagged a greater Q4-hike chance; SNB held at 0% and raised its
inflation forecasts, with its Thursday decision date now directly confirmed
against snb.ch, closing a two-edition open thread; Banxico held at 6.50%
unanimously. October-hike odds jumped and sources diverged sharply: Polymarket
approx. 65-67% (up from approx. 54-56%), CME FedWatch secondary citations
split between approx. 54% (likely stale) and approx. 73-73.5% (following
Barr's remarks and a hot PMI), unreconciled; Kalshi failed direct fetch a
sixth straight edition. The Trump-Xi Washington summit culminated Thursday
with the main bilateral meeting, a military ceremony and a state dinner
attended by tech CEOs; per Treasury Secretary Bessent, the US-China trade
truce was extended to January 10, 2027, with no comprehensive new deal or
Taiwan breakthrough. A fresh FRED pull resolved Wednesday's previously-
unverified 2-year Treasury close at 4.85% (10-year 5.11%, in line with the
prior estimated range); Thursday's own closes had not yet posted (T+1 lag) —
secondary coverage disagreed on Thursday's exact 10-year intraday high
(approx. 5.10% vs. approx. 5.22%), though the 30-year's 5.43% print (highest
since 2004) was corroborated by two sources. Jobless claims beat (197,000,
lowest since mid-July) and new home sales beat (684,000 SAAR, +6.4% m/m).

Commodities/FX: oil rallied on a Houthi missile strike on Saudi cities
(Brent briefly topped $108) before paring on reports of US-Iran talks toward
a phased Strait of Hormuz reopening — Brent closed +3.4% at $106.60, WTI
+2.7% at $94.61, both on the same November contract as Wednesday's close (no
contract-roll mismatch this session, unlike editions 24/25/26/27). Gold's
Kitco ($4,273.20)-vs-USAGOLD ($4,273.36) split closed to just $0.16, down
from approx. $7 last edition and approx. $50 two editions ago — this thread
is now resolved. Copper via Westmetall $14,765.00/t (+0.20%). DXY showed a
genuine Yahoo-vs-TradingEconomics split (101.29/+0.19% vs. 101.08/-0.02%),
disclosed rather than resolved; Yahoo's read was directionally consistent
with EUR/USD (-0.58%), GBP/USD (-0.76%) and USD/JPY (+0.51%), unlike
Wednesday's magnitude mismatch.

Derivatives: the CBOE delayed-quotes feed returned a full, individually
timestamp-verified clean sweep (VIX 15.67 +3.23%, VIX9D 14.11, VIX3M 18.43,
VIX6M 20.35, VVIX 90.57, SKEW 146.04), recovering from Wednesday's "full
stale sweep" failure; a notable front-end inversion (spot VIX above VIX9D)
was flagged for a second look next edition. Cboe's options-volume page had
not posted a Thursday figure by cutoff, and surfaced a new, unresolved
methodology mismatch: a same-page Wednesday re-read (13,781,355 contracts)
was roughly 15x larger than the 902,421 figure logged for the same date last
edition — likely a different aggregation category on the same URL, not
sorted out this run. SpotGamma failed a sixth straight edition; zerogex.io
produced a second consecutive clean, reconciling dealer-gamma read (net GEX
+$3.63bn, flip 7,698), now promoted to the standing default source. CFTC CoT
remains dated 15 September, next report due approx. Friday 25 Sept (postdates
this window). 43 sources, zero mismatches, zero stray tildes. Page 3 first
rendered short, then briefly overshot to 5 pages after adding a levels table
that was too long (12 rows, including two already-stated-in-prose Treasury
rows); trimmed to 10 rows and re-rendered clean at 4 pages.

**Open threads for edition 29:** the Cboe options-volume methodology mismatch
(902,421 vs. 13,781,355 for what may or may not be comparable Wednesday
figures) needs sorting out before citing this page's total-volume figure
again — identify which table/category is being read. The front-end VIX
inversion (spot VIX above VIX9D) seen Thursday is worth a second look to see
if it recurs or was noise. The CME FedWatch approx. 54%-vs-73% split from
this run should be checked for whether it narrows, and October-hike odds
generally are now more volatile and contested than the prior edition's
mid-50s consensus suggested — track closely into the Oct 27-28 FOMC. The
residual Kitco/USAGOLD baseline-implied-%-change wrinkle (each vendor's own
stated day-over-day % implies a slightly different prior-day base than the
other vendor's own previously-logged figure) is a low-priority watch item
only, given the headline gap is now negligible. Costco's fuller market
reaction to its Thursday-after-close Q4/FY2026 beat falls in Friday's
session — worth checking if it becomes a Monday-edition story. Two threads
are recommended for dropping rather than further carrying: Henry Hub natural
gas's precise Wed-to-Thu % change (two sources approx. 5% apart, likely a
delivery-month/averaging convention difference, not chased hard this run and
low-value to keep chasing); and Rivian's exact Thursday closing %/Palantir's
cited Rosenblatt price-target reiteration (both sourced only secondarily this
run, low-priority unless either name moves further). Threads closed after
resolution rather than carried further: the Kitco-vs-USAGOLD gold split
(closed to $0.16, treat as resolved per Known-hard-to-source above); the
SNB Thursday-vs-Friday decision-date uncertainty (confirmed directly against
snb.ch); the Wednesday 2-year Treasury close (resolved to 4.85% via FRED);
the CBOE "full stale sweep" feed failure (recovered to a full clean sweep,
though keep checking `last_trade_time` regardless); and the oil
contract-month-roll trap (did not recur this session, though keep checking
for it going forward as a matter of routine, not because it's expected every
time).
