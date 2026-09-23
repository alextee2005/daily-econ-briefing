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
  13 May 2026, sworn in 22 May 2026. **Re-confirmed fresh 23 Sept 2026**
  directly against federalreserve.gov's own Board of Governors bio page (still
  lists Warsh as Chairman, first entry). **Re-verify this fresh against
  federalreserve.gov every single edition** — do not carry it forward from a
  prior run's text or from training data.
- **The September 2026 FOMC meeting (15–16 Sept) is fully resolved and does
  not need re-verifying again:** the Committee raised the federal funds target
  range 25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, unanimous 12-0, the
  first hike since 2023.
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed fresh 23 Sept 2026
  directly against federalreserve.gov's own FOMC calendar page (still marked
  "tentative until confirmed at the meeting immediately preceding it" — normal
  boilerplate). Re-confirm the date is still listed unchanged each edition as
  that meeting approaches.
- **October-hike odds, re-confirmed fresh 23 Sept 2026, still no single clean
  number, and the range has not narrowed:** Polymarket approx. 53% hike/46%
  hold (clean direct fetch this run, approx. $10.27m volume, up from $9.17m
  last edition). Kalshi failed direct fetch (HTTP 429) for a **fourth straight
  edition (23, 24, 25, 26)** — and this run, unlike prior ones, the
  search-cached figure found was internally inconsistent (a snippet mixing up
  Yes/No framing) and was **not used at all**, rather than disclosed with an
  "imprecise timestamp" caveat as before. CME FedWatch's own page still blocks
  direct fetch; secondary citations continue to disagree with each other
  (approx. 56% vs. approx. 59.7%), not just with the other venues. **Range
  across all venues: still roughly 53-60% probability of an October hike** —
  the modal outcome, but a genuinely wide, multi-venue range. Treat Kalshi as a
  structural gap on the level of the old EUR/GBP problem: keep attempting a
  direct fetch each edition, but stop expecting the "imprecise timestamp"
  compromise to be available every time — some editions may simply have no
  usable Kalshi read at all, as this one did.
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
  approaches. Not re-checked at edition 26 since the date remains well out.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus — this decision is resolved and does not
  need re-verifying. **The Bank of Japan's next policy meeting is confirmed
  for October 29-30, 2026**, direct from boj.or.jp's own Monetary Policy
  Meeting schedule page (fetched fresh 22 Sept 2026; December 17-18, 2026 is
  also listed further out). Re-confirm this date is still listed unchanged as
  it approaches. Not re-checked at edition 26 since the date remains well out.
- **A five-central-bank cluster lands this week (confirmed fresh at edition
  26):** Norges Bank decides **Thursday 24 September 2026**, confirmed
  directly against norges-bank.no's own decision-calendar page (URL itself
  encodes the date, `26-09-24`); prior level held at 4.25% since 12 Aug.
  Sweden's **Riksbank** is reported for the same Thursday 24 September via
  secondary coverage only — riksbank.se's own calendar/press pages did not
  render body text on direct fetch, so this is not yet a clean primary-source
  confirmation; try riksbank.se directly again next time it matters. Mexico's
  **Banxico** is likewise reported for Thursday 24 September via secondary
  coverage only (current rate 6.50%, held in August; a Citi survey of 37
  analysts expects another hold). Switzerland's **SNB** — an open date thread
  carried from edition 24 (24th vs. 25th, possibly a mis-surfaced 2025
  article) — now looks **best-supported as Friday 25 September 2026**: a
  Reuters economist poll (40 of 41 expecting a hold at 0.00%), ING THINK and
  Morningstar Europe all independently converge on the 25th, and a genuine SNB
  page titled "Monetary policy assessment of **25 September 2025**" was found,
  strongly supporting the hypothesis that an earlier "24th" citation was that
  2025 article mis-surfaced as current. **Still not confirmed directly against
  snb.ch**, which had not yet posted a 2026 assessment page as of this
  edition's fetch — confirm directly once it does, and report the actual
  outcomes of all four Thursday/Friday decisions once they land (they postdate
  this window).

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
  has occasionally failed to post in time. **It failed again at edition 26**
  for Tuesday 22 Sept: neither apnews.com's own piece nor a Reuters wrap could
  be located/fetched, and — a live example of the stale-date-republishing
  trap — several syndicated "AP" reposts (arkansasonline.com,
  magnoliabannernews.com) carried a Tuesday-dated URL but were exact
  republishes of Monday 21 Sept's already-reported index levels. Discarded
  once cross-checked; the index-close table was instead built from Yahoo
  Finance's historical OHLC tables cross-validated against FRED's official
  SP500 series (exact match) and ETF-proxy triangulation. This is now enough
  occurrences (15 Sept gap at ed. 21, 22 Sept gap at ed. 26) that AP/Reuters
  should be treated as "try first, expect to need the fallback chain," not as
  a reliably-clean primary source — always have Yahoo Finance + FRED ready as
  the default working chain rather than a last resort.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example: a Trefis "Market Movers" page
  carrying a Monday-21-Sept-dated URL was actually re-serving Friday 18
  Sept's already-reported figures (Xenon Pharmaceuticals -30.7%, etc.) —
  discarded once cross-checked against the actual Monday session's numbers.
  Edition 26 caught another (see AP/Reuters note above, same trap, different
  vendor). **A same-day close and a next-day after-hours-triggered move can
  legitimately combine into one large single-day % change** — edition 24's
  Xenon Pharmaceuticals -30.7% Friday move looked at first like it might
  conflict with a same-day "+1% then -25% after-hours Thursday" report, but
  both were correct. Check whether a headline % move is measured close-to-close
  (which will include an intervening after-hours event) before assuming two
  reports conflict. **A related but distinct trap surfaced at edition 26:
  intraday-move coverage vs. the actual close can diverge sharply even with no
  after-hours event involved** — Worthington Enterprises (WOR) had aggregator
  coverage citing an approx. +15% earnings-day spike to $67.94, but its
  stockanalysis.com closing print showed only +1.36% to $58.94; PayPal (PYPL)
  had aggregators citing 2-4.8% intraday moves on its Meta-Muse integration
  news, but closed at just +0.51%. Neither was reconciled to a single
  consistent story — treat a stockanalysis.com (or equivalent timestamped)
  closing print as authoritative over an intraday-coverage percentage, and
  flag the gap rather than silently using whichever number sounds more
  interesting.
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
  to one number.
  Similarly, **a price level can be correct while a vendor's stated %-change
  is wrong** if the vendor used a different prior-day base — edition 24 found
  WTI's Friday level ($100.30) and stated -1.58% change both correct only
  once Thursday's true settle was corrected from a previously-published
  $101.09 to $101.91 (see edition log) — always sanity-check that a stated
  price level and stated % change actually reconcile arithmetically against
  the prior session's logged close before reporting both. Edition 25 hit the
  same class of problem with Monday's WTI settlement: sources split roughly
  $92.28-$95.80/bbl. **Edition 26 fully resolved this one**: a UAE state-wire
  (WAM) recap clarified that Monday's front-month October WTI contract
  settled at $95.78 while a separate November contract settled at $92.47 —
  the earlier split was a contract-month mismatch across sources, not a
  genuine data conflict. Use $95.78 as the clean Monday WTI baseline in any
  future day-over-day comparison. **General lesson reinforced twice now:**
  when a commodity price splits into an unreconciled range across sources,
  check whether different contract months/tenors are being quoted before
  concluding it's a sourcing failure.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done** — and if it reports 0 inline citations found
  while your Annex B clearly has entries, check for the combined-bracket
  `[n][m]` mistake above before assuming something else is wrong. Also
  remember it only scans HTML text — a citation number baked into a chart
  PNG's label is invisible to it (see Confirmed format above). Also remember
  it flags Annex B entries that were drafted but never actually cited inline
  (e.g. in a movers table) — edition 26 hit this with four single-stock
  sources drafted into Annex B before the citations were added to the movers
  table's driver column; caught and fixed by running the check before
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
  Commodities & FX table didn't display) — don't reject the idea purely
  because the instrument list overlaps; check whether the *added* column
  carries real information first. **Not needed at edition 26** — page 3 filled
  naturally from content alone with no padding block required.

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
  fresh. Edition 26 got a full clean sweep again (all six series fresh at
  Tuesday's 16:15-17:00 ET prints, a second straight edition of failure mode
  (a)). Also note a `prev_day_close` field bug, now observed **five editions
  running (22-26)**: it duplicates the day's own `close`/`current_price`
  rather than giving a real prior-day reference, and this corrupts the feed's
  own `price_change_percent` field too — **never quote the feed's
  `price_change`/`price_change_percent` fields directly; always compute
  day-over-day % change manually against the previous edition's logged
  close.** Fall back to news coverage (Yahoo Finance, CNBC, MarketWatch) for
  at least the headline VIX close if the feed is stale, and disclose it as
  single-sourced. Separately: the mechanical VIX9D-vs-spot-VIX distortion from
  the 16 Sept FOMC aging out of the 9-day lookback window, tracked across
  editions 23-24 and looking stabilized by edition 25, **remains stabilized at
  edition 26** — no re-emergence. Treat this thread as resolved absent a new
  event resetting it.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table
  and (absent fresher CoT data or another dominant story) chart #2. Worked
  cleanly again at edition 26. **Stockanalysis.com single-stock pages are
  also the standing default for pinning an exact closing price/% change on
  any individual mover** — edition 26 used direct fetches to it to resolve
  several sources' conflicting intraday-move percentages (Viking
  Therapeutics, On Holding, SanDisk, GameStop, AutoZone, JPMorgan, Wells
  Fargo, PayPal, Worthington Enterprises all pinned this way). Worth doing
  proactively for any mover whose research-pass figures disagree by more than
  a rounding error, rather than only for the single biggest story of the day.
- **NYSE/Nasdaq closing breadth:** not obtainable; Reuters' final wrap drops
  the breadth block. Mark unavailable.
- **Dealer gamma:** third-party sources only; mark unavailable unless a
  specific desk note is found and cited. SpotGamma's own substack/site
  articles return either 403 or an empty static page on direct fetch — this
  has now recurred at editions 22, 24, 25 and 26 — search snippets can still
  surface headline numbers but treat as lower-confidence secondary sourcing,
  and if a figure looks implausible relative to the underlying index level
  (edition 24 found a "gamma flip level" that didn't reconcile with any
  plausible SPX price; edition 25 found a third-party GEX tool showing
  dollar figures many orders of magnitude too small to be real SPX dealer
  gamma), discard it rather than reporting it. Edition 26 found nothing at
  all (page returned only boilerplate/educational text, no figure to even
  evaluate) — mark unavailable in that case too rather than searching further.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Expect
  a genuinely wide range across venues/dates — report the range and don't
  force it to a single number. As of edition 25, even the *secondary*
  citations for CME FedWatch disagree with each other (approx. 56% vs.
  approx. 59.7%) — treat CME FedWatch as the least precise of the three
  venues reported, not just the hardest to fetch directly. **Unchanged and
  unresolved at edition 26** — same two figures still cited by different
  secondary sources, no narrowing.
- **Kalshi direct fetch:** now rate-limited (HTTP 429) for **four straight
  editions (23, 24, 25, 26)** — this is now a confirmed structural gap, not a
  transient issue. **Escalation at edition 26: even the search-cached
  fallback failed** — the only snippet found was internally inconsistent (a
  "56¢ No / 45¢ Yes" figure with confusing Yes/No labeling that contradicted
  the direction implied by Polymarket) and was discarded rather than
  disclosed with a caveat. Keep attempting a direct fetch each edition (it
  may recover), but stop assuming a search-cached fallback will always be
  available as a compromise — some editions may have literally nothing
  usable from Kalshi.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  five editions running (22-26)** — treat this as a durable, confirmed pattern
  rather than re-attempting lme.com first each time; **default straight to
  the fallback chain.** Shanghai Metals Market (metal.com) has now failed
  **five editions running (22-26)** — skip metal.com entirely and go straight
  to Westmetall.com (a German metals-data provider that republishes official
  LME cash/3-month settlement prices), which has now worked cleanly **five
  editions running** as the fallback. Disclose whichever was used. Because the
  fallback chain can change edition to edition, treat any day-over-day copper
  % change built across two different sourcing chains as approximate, not a
  precise like-for-like comparison.
- **Official Treasury par yields:** not posted by the ~20:15 ET cutoff (H.15
  publishes the *prior* day's data the next afternoon) — but the official
  home.treasury.gov H.15 page itself has now been **successfully fetched
  direct for two straight editions (25, 26)**, giving clean same-window reads
  for both the 10-year and 2-year each time. Keep trying the official page
  directly each edition before falling back to secondary coverage (Trading
  Economics, AP, CNBC) — it now looks like the more reliable default, not
  just an occasional win. CNBC's own quote pages (US10Y/US2Y) returned HTTP
  403 on direct fetch at edition 26 — not a usable fallback right now.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly rather than presenting old data as current. Note
  the report comes in (at least) two different methodologies/pages depending
  on the instrument: `financial_lf.htm` (Traders in Financial Futures, Asset
  Manager/Leveraged Funds categories) works well for equity index futures
  (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report is what actually carries VIX futures
  positioning — don't expect one page to have both. As of edition 26 the most
  recent data is still dated 15 Sept (published Friday 18 Sept); no new
  report had posted by the Tuesday 22 Sept cutoff — next update due approx.
  Friday 25 Sept, confirmed by direct fetch of the CFTC page itself.
- **GBP/USD and EUR/USD clean close:** a structural sourcing gap across
  editions 22-24 (no single authoritative 4pm-London print for either pair
  from a news-wire/official source), first resolved to a single Yahoo Finance
  vendor at edition 25 (single-sourced, not yet cross-corroborated). **Now
  fully resolved at edition 26:** both pairs got a second independent
  corroborating source (NordFX Market Pulse for EUR/USD; a separate
  market-news aggregate for GBP/USD), each within a few pips of the Yahoo
  Finance read and matching direction/theme. **Treat this thread as closed**
  — Yahoo Finance as primary with a second wire/vendor piece as corroboration
  is now the standing working pattern for both pairs; no further special
  flagging needed unless a future edition finds a fresh disagreement.
- **Gold/silver clean close on a non-event day:** even without an FOMC-style
  settle-vs-spot timing split, Kitco's own quote can differ meaningfully by
  timestamp within the same session, and futures (GC=F/SI=F) vs. spot XAU/
  XAG quotes from different vendors can also diverge by several tenths of a
  percent on an ordinary day (edition 25: Yahoo GC=F $4,383.90 vs. Bloomberg
  spot $4,378.63, both "near-flat" but not identical). **Edition 26 found a
  larger, less explicable split** on another ordinary day: Kitco/Fortune spot
  at $4,358.80 (-0.45%) vs. USAGOLD's own report at $4,307.63 (recomputed
  approx. -1.62% against the same baseline) — over a full point of
  disagreement with no settle-vs-spot timing mechanism identified. Cite the
  print closest to a standard NY 4-5pm ET close as primary (Kitco/Fortune's
  4:32pm ET read at edition 26) and disclose the wider range rather than
  presenting one snapshot as *the* close — this looks like a recurring
  category of gap on gold specifically, not a one-off.
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
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey (new at
  edition 26):** released Tuesday 22 Sept 2026, but secondary aggregators
  gave materially conflicting headline figures (one framed the general
  activity index as -22.0 vs. -10.6 prior; another described a firm-level
  index moving from -8.2 to +0.3 alongside a separate services-specific
  reading of 22.0) with no clean philadelphiafed.org confirmation obtained
  by cutoff. Marked unavailable rather than picking one figure. Try
  philadelphiafed.org's own release page directly next time this survey is
  needed, rather than search aggregators.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  previously flagged only as lacking an explicit date stamp (edition 25: a
  plausible 713,342-contract figure, moderate confidence). **Escalated at
  edition 26 to a confirmed data-quality problem**: the figure returned for
  Tuesday's session was identical, to the exact contract count, to edition
  25's already-logged Monday figure — strong evidence the page serves a
  stale/cached read rather than refreshing per-session. **Do not report a
  figure from this page without first checking it differs from the
  previous edition's logged number.** If it doesn't, mark unavailable rather
  than reporting a number that is almost certainly not the current day's
  data. Worth trying an alternative source (e.g. OCC volume data) next time
  this metric is needed.
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
  revisited at editions 25 or 26 since no fresh CoT data posted either
  window.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  (e.g. estimated closing-auction imbalance dollar amounts around a
  quarterly rebalance) tends to come from independent research
  Substacks/blogs (e.g. QSG Research) rather than a sell-side desk by name —
  treat as citable but note it's not a bulge-bracket named source when it
  matters for confidence level.
- **A stale "already happened" premise can survive multiple editions as an
  open thread if nobody actually chases the primary source (new lesson at
  edition 26):** edition 25 carried forward an open thread asking for
  confirmation of a reported Block Inc.-for-Hess Corp S&P 500 swap "effective
  Wed 23 Sept" — this had actually happened in **July 2025**, over a year
  earlier; the "effective Wed 23 Sept" framing appears to have been a
  secondary-source error that went unchallenged. Resolved at edition 26 by
  directly checking S&P Global's own press release archive rather than
  re-searching news coverage of the "upcoming" event. **General lesson:** for
  any open thread describing a still-pending corporate/index action, try the
  primary source (the company's own IR site, the index provider's own press
  releases) before re-running the same news search that produced the
  ambiguous premise in the first place — a wrong premise doesn't correct
  itself by repeating the same search.

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
  Edition 26 rendered a well-balanced 4 pages on the first try with no
  padding block needed — content volume alone was enough this time.

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
  capping either). **Edition 26 extended the precedent further**: VKTX at
  +35.67% vs. next-largest ONON at +7.58%, about 4.7x — still left uncapped,
  since "order of magnitude" (approx. 10x) is the actual threshold and 4.7x
  reads fine on the standard axis. The rule has not yet had a genuine
  10x+ case to test.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used again at edition 26 for a
genuine financials-vs-materials rotation reversal, and at edition 25 for a
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
(movers) already covers the earnings/single-name story, the sector proxy is
a good complementary choice even on a stock-heavy day — edition 25 used
exactly this combination (chip-stock movers as chart #1, sector rotation as
chart #2), and edition 26 again (biotech/consumer movers as chart #1,
financials-led rotation as chart #2), since in both cases the two stories
reinforced rather than duplicated each other. **Chart #2's placement in the
document should follow its content, not a fixed section** — a CFTC/
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

**Editions 1–24 (condensed):** established the format (edition 1 baseline;
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
**Edition 22** (Thu 17 Sept, covering Wed 16 Sept FOMC day): the Fed hiked
25bp to 3.75%-4.00%, unanimous 12-0; equities rose on the decision, then
reversed hard during Chair Warsh's press conference to close lower (S&P
7,551.81 -0.4%, Dow 51,461.90 -1.2%, Nasdaq flat); banks (GS -3.96%, WFC
-2.98%) the clearest single-name losers; J.B. Hunt -13.3% on Q3 guidance;
10-year first closed above 5% since 2007; a genuine COMEX-vs-spot gold
settle-timing split around the 2pm decision; copper's LME direct-fetch
failure streak began here. **Edition 23** (Fri 18 Sept, covering Thu 17
Sept): equities reversed most of the post-FOMC selloff (S&P 7,637.76 +1.1%,
Nasdaq +1.7%); October-hike odds swung from edition 22's single-sourced
approx. 92% to Polymarket approx. 50-52% hold, Kalshi approx. 63% hold; Bank
of England held at 3.75% (6-3); Generac +18.3%, Lucid +10.0%, AutoNation
-9.4%; initial jobless claims beat. **Edition 24** (Mon 21 Sept, covering Fri
18 Sept triple witching + weekend catch-up): approx. $7tn September
triple-witching notional expired alongside Monday's quarterly S&P/Nasdaq-100
rebalance (SpaceX's Nasdaq-100 weight to 2.82%); Xenon Pharmaceuticals -30.7%
(Phase 3 enrollment pause); Nucor -6.1%, Netflix -4.7%, SanDisk +11.0%,
Robinhood +9.1%; Warren Buffett stepped down as Berkshire chairman; Bank of
Japan hiked 25bp to approx. 1.25%, a 31-year high, 7-2 split vote;
October-hike odds rebounded to approx. 55% both venues; WTI required a
settle correction (Thu $101.09→$101.91) to reconcile Friday's -1.58% change;
copper fallback chain moved to Westmetall after lme.com/metal.com both
failed; weekend Houthi strike attempt on Saudi Aramco's Yanbu hub
intercepted; fresh CFTC CoT (as of 15 Sept) showed leveraged funds trimming
net-short ES/NQ/RTY exposure; page 3 initially overflowed to 5 pages by 3-4
lines of genuine copy overflow, trimmed to 4.

**Edition 25 (condensed)** — Tue 22 Sept 2026 report covering Monday 21 Sept,
the window's one NYSE session, research window Sun 20 Sept 20:00 ET through
Mon 21 Sept 23:29 ET. Dominant story: a broad chip-stock rally (Intel +12.0%,
AMD approx. +10% and above a $1tn market cap for the first time, Qualcomm
approx. +9%, Arm Holdings +16.6% to $322.90 on a Piper Sandler Overweight
initiation) pushed the Nasdaq Composite to a record close of 27,122.09
(+2.26%), S&P 500 7,764.70 (+1.49%), Dow 52,048.83 (+0.71%), Russell 2000
2,875.36 (+0.52%). Sector rotation: Communication Services (XLC +3.56%) and
Technology (XLK +2.89%) led, Energy (XLE -2.30%) lagged on an oil selloff.
The quarterly S&P 500/400/600 and Nasdaq-100 rebalance took effect at
Monday's open (Bloom Energy, Illumina, Everpure joined the S&P 500 replacing
Molson Coors, The Trade Desk, Builders FirstSource; SpaceX's Nasdaq-100
weight rose to 2.82% from 1.28%). Other movers: Grail (GRAL) approx. +30%
(FDA advisory-committee review pending) and HP Inc. (HPQ) -4.22% (withheld
FY2027 guidance). Analyst actions: HubSpot/Palo Alto Networks/CrowdStrike PTs
raised, Equifax downgraded; a split call on Accenture (Deutsche Bank PT raise
vs. Guggenheim downgrade) confirmed in full. Macro: Fed Chair Kevin Warsh and
the Oct 27-28 next FOMC meeting both re-confirmed; October-hike odds
Polymarket approx. 53% hike (clean direct fetch), Kalshi approx. 55-56%
(rate-limited, third straight edition), CME FedWatch citations disagreeing
(approx. 56% vs. approx. 59.7%); Bank of Japan's next meeting confirmed Oct
29-30; the Trump-Xi Washington summit reported proceeding Thursday 24 Sept;
Treasury H.15 fetched directly and cleanly (2-year approx. 4.45%, 10-year
approx. 4.96%, down from Friday's 5.01%); SOFR held at 3.85% through Friday,
Monday's reading and the cause of the mid-week 3.62%→3.85% jump both left
open. Commodities/FX: oil sold off on reported Iran-Oman Hormuz diplomacy
(Brent $100.34, -2.97%, well-corroborated; WTI unresolved to a single print
at the time, sources split $92.28-95.80/bbl — **fully resolved at edition
26**, see Hard rules); gold $4,378.63 (approx. -0.1%) and silver $65.82
(-0.47%) both near-flat; copper via Westmetall $14,788/t (+1.78%); DXY 100.43
(+0.21%); EUR/USD (1.1480) and GBP/USD (1.3389) both got clean single closes
via Yahoo Finance for the first time, but single-sourced at the time —
**cross-corroborated and closed as a thread at edition 26**; USD/JPY 157.05
(+0.59%). Derivatives: VIX closed 14.87 (+0.41%, computed manually), full
clean CBOE sweep; term structure normal contango; VIX options volume approx.
713,342 contracts (moderate confidence at the time — **this exact figure
turned out to be stale/duplicated at edition 26, see Known-hard-to-source**);
CFTC CoT still dated 15 Sept. An open thread asking for primary confirmation
of a reported Block Inc.-for-Hess Corp S&P 500 swap "effective Wed 23 Sept"
turned out, once chased at edition 26, to describe an event from **July
2025** — a stale premise, now closed. 42 sources, zero mismatches, zero
stray tildes.

**Edition 26 (most recent — full detail)** — Wed 23 Sept 2026 report covering
Tuesday 22 Sept 2026, the window's one NYSE session, research window Mon 21
Sept 20:00 ET through Tue 22 Sept 20:21 ET. Verified the two structural
header rules again: date line reads the edition date (Wednesday 23 September
2026), not the session date; window line starts at the given research-window
start (Mon 21 Sept 20:00 ET), not earlier.

Dominant story was a financials-led sector rotation, not a broad index move.
S&P 500 closed effectively flat at 7,764.64 (-0.00%), Dow fell 0.36% to
51,863.69 on a bank-stock selloff, Nasdaq Composite set a second consecutive
record close at 27,244.28 (+0.45%), Russell 2000 +0.51% to 2,889.92 —
confirmed via Yahoo Finance historical OHLC cross-validated against FRED's
official SP500 series (exact match: 7,764.64), since neither AP's own wire
piece nor a Reuters wrap could be located for the date and several
syndicated "AP" reposts were caught stale-republishing Monday's numbers under
a Tuesday date/URL (see Hard rules — another live stale-date example).
Sector rotation reversed hard from Monday: Financials (XLF -1.97%) worst,
Materials (XLB +1.65%) best — JPMorgan -3.42% to $340.00, Wells Fargo -3.92%
to $83.15, Morgan Stanley -2.88% to $200.18 the clearest single-name losers.
A Bloomberg piece ("Meta's Muse Drags Down Stocks That Depend on Consumer
Inertia") tied bank/travel-stock weakness to fears that Meta's "Muse" AI
shopping agent disintermediates commission-based business models; only the
headline/snippet were accessible (paywalled), so reported as plausible
context rather than a confirmed driver — Richmond Fed President Barkin's
same-day hawkish remarks (further hikes still possible) are the more
concretely-sourced contributing factor. Expedia and Booking Holdings both
traded weak on the same Muse-disintermediation theme (Expedia's overhang
compounded by Morgan Stanley's 16 Sept downgrade to Underweight; Booking's by
the EU General Court's 9 Sept ETraveli-block ruling); Carnival and American
Airlines rose on falling fuel costs.

Movers: Viking Therapeutics (VKTX) +35.67% to $40.85 (positive VK2735
obesity-drug maintenance-dosing data; Lilly/Novo dipped in sympathy) was the
session's standout — cleanly pinned via a direct stockanalysis.com fetch
after research passes reported an unreconciled 28-35% range. On Holding
+7.58% (Investor Day: first-ever buyback, new long-term targets), SanDisk
+6.82% (Rosenblatt initiated Buy, $2,400 PT, on AI/NAND demand), GameStop
+5.58% (continued reaction to Ryan Cohen's Monday share purchase), AutoZone
+3.26% (FQ4 beat on EPS, missed on revenue). Earnings: MillerKnoll beat FQ1
EPS/missed revenue, guided FQ2 lower; KB Home beat FQ3 EPS but softened FY
sales guidance (AH +2.9%); Worthington Enterprises beat FQ1 estimates and
was covered by some aggregators as spiking intraday to approx. $67.94
(approx. +15%), but its stockanalysis.com close showed only +1.36% to
$58.94 — unreconciled, flagged rather than picking one figure. PayPal,
despite a Meta-Muse checkout-integration announcement covered by some
aggregators as a 2-4.8% intraday mover, closed up just +0.51% — the
stockanalysis.com close is treated as authoritative over intraday-coverage
percentages per the (updated) Hard rules.

Correction: edition 25's open thread asking for primary confirmation of a
reported Block Inc.-for-Hess Corp S&P 500 swap "effective Wed 23 Sept" was
chased down and found to be a stale premise — Block already replaced Hess in
the index before the open on 23 July 2025 (confirmed via S&P Global's own
press release archive), over a year before this window. No S&P 500
constituent change was found effective this window beyond the already-
reported 21 Sept quarterly rebalance. Closed — do not carry forward.

Macro: Fed Chair Kevin Warsh and the Oct 27-28 next FOMC meeting both
re-confirmed fresh against federalreserve.gov. Treasury H.15 fetched
directly and cleanly for a second straight edition (10-year 4.96% flat,
2-year eased to 4.43% from 4.45%). Monday's SOFR (published Tuesday,
standard T+1 lag) held at 3.85%; Tuesday's own reading not yet published at
cutoff; the mechanism behind the 17 Sept jump from 3.62% remains unconfirmed
beyond the plausible FOMC-hike read-through. October-hike odds: Polymarket
approx. 53% hike/46% hold (clean direct fetch, approx. $10.27m volume, up
from $9.17m); Kalshi failed direct fetch (HTTP 429) a fourth straight
edition and this run's search-cached figure was internally inconsistent, so
nothing was used at all (an escalation from prior editions' "imprecise
timestamp" compromise); CME FedWatch secondary citations remain split
(approx. 56% vs. approx. 59.7%). Richmond Fed Manufacturing fell to -2 in
September (from +4, missing +5 consensus); Philadelphia Fed's Nonmanufacturing
Business Outlook also released Tuesday but secondary aggregators gave
materially conflicting headline figures, marked unavailable. A
five-central-bank cluster is now dated: Norges Bank confirmed Thu 24 Sept
directly via its own site; Riksbank and Banxico both reported (secondary-
sourced only) for Thu 24 Sept; SNB's long-open 24-vs-25 date thread resolved
to a best-supported Fri 25 Sept (Reuters poll, ING THINK, Morningstar Europe
all converge; a genuine SNB page titled "Monetary policy assessment of 25
September 2025" supports the mis-surfaced-2025-article hypothesis), but not
yet confirmed directly against snb.ch. The Trump-Xi Washington summit runs
23-25 Sept with the actual meeting/Rose Garden/state dinner Thursday 24
Sept. Canada import-ban timeline (29 Sept) unchanged.

Commodities/FX: oil fell a second straight session on two converging
catalysts — Saudi Arabia restarted its East-West Pipeline and moved toward
resuming Yanbu crude exports, and US/Iran officials held a roughly
three-hour UNGA-sideline meeting Trump called "a very good meeting" (Brent
-1.09% to $99.25, WTI -1.24% to $94.59, both cleanly triangulated). A UAE
state-wire recap resolved edition 25's flagged WTI ambiguity: Monday's
front-month October contract settled $95.78 while a separate November
contract settled $92.47 — the earlier $92.28-95.80 split was a
contract-month mismatch, not an error; $95.78 is the clean Monday baseline
going forward. Gold showed a new, genuine same-day split: Kitco/Fortune's
4:32pm ET spot read $4,358.80 (-0.45%) vs. USAGOLD's own report $4,307.63
(recomputed approx. -1.62% vs. the same baseline) — not reconciled to a
common timestamp, disclosed rather than picked; COMEX Dec futures rose
+0.40% the same session, a genuine spot/futures divergence. Silver $65.27
(-0.84%). Copper via Westmetall (lme.com and metal.com both now five-for-
five failures, skipped without retrying) $14,797/t, essentially flat
(+0.06%) after Monday's sharp move. DXY 100.57 (+0.14%). EUR/USD (1.1465,
-0.13%) and GBP/USD (1.3371, -0.13%) both got a second independent
corroborating source (NordFX; a separate market-news aggregate) beyond
Yahoo Finance for the first time — resolves edition 25's single-sourced
flag, thread now closed. USD/JPY 157.369 (+0.21%), continued post-BoJ yen
weakness.

Derivatives: VIX closed 14.21, its lowest close of the year, -4.44%
(computed manually vs. Monday's logged 14.87) — the Cboe feed gave a full
clean sweep (all six series fresh at the 16:15-17:00 ET prints, a second
straight clean-sweep edition). Term structure stayed in normal contango
(VIX9D 12.13, VIX3M 17.61, VIX6M 19.79); no re-emergence of the FOMC-lookback
distortion. VVIX 83.17, SKEW 144.80 (a small uptick in tail-risk pricing even
as realized/implied vol fell broadly). VIX options volume escalated from a
"no date stamp" caveat to a confirmed data-quality problem: Tuesday's read
from Cboe's stats page was identical, to the exact contract count, to
edition 25's already-logged Monday figure (713,342) — treated as a
stale/cached page and not reported. CFTC CoT confirmed still dated 15 Sept
via direct cftc.gov fetch, no new report, next due approx. Fri 25 Sept.
Dealer gamma unavailable again (SpotGamma boilerplate-only, no figure to
evaluate). 50 sources, zero mismatches, zero stray tildes. Page 3 filled
naturally on the first render — no padding block needed.

**Open threads for edition 27:** the four Thursday/Friday central-bank
decisions (Norges Bank, Riksbank, Banxico Thu 24 Sept; SNB likely Fri 25
Sept) and the Trump-Xi summit's Thursday culmination all postdate this
window — track their actual outcomes once they land rather than re-reporting
them as upcoming; confirm SNB's exact date directly against snb.ch once it
posts a 2026 assessment page; get a clean primary (philadelphiafed.org)
read on the Philadelphia Fed Nonmanufacturing Business Outlook headline for
September if it's still relevant; a fifth straight Kalshi direct-fetch
attempt (now a confirmed structural gap — consider whether continuing to
retry every edition is worth it, or whether to default straight to
disclosing "unavailable" going forward); Worthington Enterprises' intraday-
spike-vs-close gap (approx. $67.94 vs. $58.94) if further coverage clarifies
which is real; the full text of Bloomberg's "Muse disintermediation" piece,
if accessible via a different route, to confirm or discount it as the actual
bank-selloff driver; whether Monday 21 Sept's quarterly index rebalance
produced above-normal trading volume or volatility — carried open since
edition 24/25 with no resolution across three editions now, consider
dropping this thread if edition 27 doesn't resolve it either; whether
October-hike odds keep converging or diverge further once the Thursday
central-bank cluster and Friday SNB decision land. One thread is closed after
resolution rather than chased further: the Block Inc./Hess Corp S&P 500
premise (resolved as stale, see edition 26 above) — do not re-open unless a
genuinely new index-change report surfaces.
