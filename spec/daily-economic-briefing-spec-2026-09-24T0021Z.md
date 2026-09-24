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
  13 May 2026, sworn in 22 May 2026. **Re-confirmed fresh 24 Sept 2026**
  directly against federalreserve.gov's own Board of Governors bio page (still
  lists Warsh as Chairman, first entry). **Re-verify this fresh against
  federalreserve.gov every single edition** — do not carry it forward from a
  prior run's text or from training data.
- **The September 2026 FOMC meeting (15–16 Sept) is fully resolved and does
  not need re-verifying again:** the Committee raised the federal funds target
  range 25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, unanimous 12-0, the
  first hike since 2023.
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed fresh 24 Sept 2026
  directly against federalreserve.gov's own FOMC calendar page (Dec 8-9 is the
  next SEP meeting after that). Re-confirm the date is still listed unchanged
  each edition as that meeting approaches.
- **October-hike odds, re-confirmed fresh 24 Sept 2026 — the range has
  converged into the mid-50s for the first time in several editions:**
  Polymarket approx. 54-56% hike (up modestly from approx. 53% last edition,
  direct fetch), CME FedWatch secondary citations approx. 54-55.1% (still
  blocked on direct fetch; secondary sourcing only, but the two figures
  cited by different secondary sources are now much closer together than the
  approx. 56% vs. approx. 59.7% split seen at editions 25-26). Kalshi failed
  direct fetch (HTTP 429) for a **fifth straight edition (23, 24, 25, 26,
  27)** and this run's search-cached fallback was not usable either. **Treat
  the range as approx. 54-56% across the two working venues** — narrower than
  the "53-60%" range carried in recent editions, but still watch for whether
  this convergence holds or was a one-edition coincidence. Keep attempting a
  direct Kalshi fetch each edition (it may recover) but there is no need for
  extensive caveat language each time this fails — a plain "failed again,
  Nth straight edition" is sufficient.
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
  approaches. Not re-checked at editions 26 or 27 since the date remains well
  out.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus — this decision is resolved and does not
  need re-verifying. **The Bank of Japan's next policy meeting is confirmed
  for October 29-30, 2026**, direct from boj.or.jp's own Monetary Policy
  Meeting schedule page (fetched fresh 22 Sept 2026; December 17-18, 2026 is
  also listed further out). Re-confirm this date is still listed unchanged as
  it approaches. Not re-checked at editions 26 or 27 since the date remains
  well out.
- **A four-to-five-central-bank cluster lands Thursday 24 September 2026 —
  now likely all on the same day, corrected at edition 27:** Norges Bank
  decides Thursday 24 September 2026, confirmed directly against
  norges-bank.no's own decision-calendar page (URL itself encodes the date,
  `26-09-24`); prior level held at 4.25% since 12 Aug; desk previews are split
  hold vs. a 25bp hike. Sweden's **Riksbank** is confirmed for the same
  Thursday 24 September via Newsquawk's dated preview (still not a clean
  riksbank.se-own-page confirmation — riksbank.se's calendar/press pages have
  not rendered body text on direct fetch across two editions now; try again
  next time it matters). Mexico's **Banxico** decides Thursday 24 September,
  13:00 Mexico City time, with a Citi survey of 36 analysts showing 25 expect
  a hold at 6.50%. **Switzerland's SNB — corrected at edition 27:** the
  previous best-supported date (Friday 25 September, per edition 26) has been
  superseded by fresh sourcing pointing to **Thursday 24 September** instead
  — matching the SNB's own established Thursday cadence for its last three
  quarterly assessments (11 Dec 2025, 19 March 2026, 18 June 2026, all
  independently verified as Thursdays) and a dated FXStreet preview
  (published 23 Sept) quoting a DBS economist referring to "the September 24
  meeting." The earlier "25th" framing traced back to a genuine SNB page
  titled "Monetary policy assessment of **25 September 2025**" being
  mis-surfaced as a 2026 citation — a confirmed instance of the
  date-conflation trap, not a new ambiguity. **Still not confirmed directly
  against snb.ch**, which continued to 404 on every attempted URL at edition
  27 — confirm directly once it does, and report the actual outcomes of all
  four (now likely same-day) decisions once they land; they postdate this
  window's research cutoff (Tue 22 Sept 20:00 ET – Wed 23 Sept 20:21 ET).

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
  more consecutive citations.
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
  **Edition 27 is a clean counter-example worth keeping in mind**: both AP
  (via ABC News) and Reuters (via Honolulu Star-Advertiser) posted the
  Wednesday 23 Sept close in time and agreed to the dollar (S&P within a
  penny) — so treat AP/Reuters as "try first, expect to sometimes need the
  fallback chain," not as unreliable by default. Always have Yahoo Finance +
  FRED ready as the working fallback regardless of which way this edition
  goes.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example (Trefis "Market Movers" re-serving
  Friday 18 Sept's figures under a Monday 21 Sept URL); edition 26 caught
  another (several "AP" reposts of Monday 21 Sept's numbers under a Tuesday
  22 Sept dateline). **Edition 27 caught a third, textbook example**: a
  Wednesday-dated aggregator article (techflowpost) reproduced Tuesday 22
  Sept's exact index levels (S&P 7,764.64, Dow 51,863.69, Nasdaq +0.45% to
  27,244.28) and the Schwab/Ameriprise bank-selloff story under a Wednesday
  URL — confirmed as stale via a second source (thestar.com.my) that
  explicitly stated the move happened "on Tuesday." This is now the fourth
  documented instance across four consecutive editions (24-27, counting
  Trefis/AP-reposts/techflowpost) — treat same-numbers-as-yesterday as the
  standing tell, and always locate a second, independently-dated source
  before accepting a "today"-dated figure at face value. **A same-day close
  and a next-day after-hours-triggered move can legitimately combine into one
  large single-day % change** — edition 24's Xenon Pharmaceuticals -30.7%
  Friday move looked at first like it might conflict with a same-day "+1%
  then -25% after-hours Thursday" report, but both were correct. Check
  whether a headline % move is measured close-to-close (which will include an
  intervening after-hours event) before assuming two reports conflict. **A
  related but distinct trap surfaced at edition 26 and recurred in a milder
  form at edition 27:** intraday-move coverage vs. the actual close can
  diverge sharply even with no after-hours event involved — Worthington
  Enterprises (WOR, ed. 26) and, at edition 27, Paychex (two intraday
  snippets of -6.84%/-7.13% vs. the actual -8.77% close) and Cracker Barrel
  (a discarded "+8.3%" snippet vs. the actual, wire-corroborated +4.49%
  close) all showed this pattern. Treat a stockanalysis.com (or equivalent
  timestamped) closing print as authoritative over an intraday-coverage
  percentage, and cross-check against a second, independent source (a wire
  story or Motley Fool piece explicitly describing the close) when available
  rather than just picking the stockanalysis.com number in isolation.
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
  to one number. **Edition 27 found the same two vendors' gap narrow sharply**
  (Kitco approx. $4,297.53 vs. USAGOLD $4,304.11, about $7 apart vs.
  approx. $50 on Tuesday) — still disclosed as two separate reads against two
  separate prior-day baselines (implying very different %-changes, approx.
  -1.4% vs. approx. -0.08%) rather than picked to one number, but worth
  tracking whether the gap keeps narrowing or was a one-day coincidence.
  Similarly, **a price level can be correct while a vendor's stated %-change
  is wrong** if the vendor used a different prior-day base — edition 24 found
  WTI's Friday level ($100.30) and stated -1.58% change both correct only
  once Thursday's true settle was corrected from a previously-published
  $101.09 to $101.91 (see edition log) — always sanity-check that a stated
  price level and stated % change actually reconcile arithmetically against
  the prior session's logged close before reporting both. Edition 25 hit the
  same class of problem with Monday's WTI settlement: sources split roughly
  $92.28-$95.80/bbl. Edition 26 fully resolved this one: a UAE state-wire
  (WAM) recap clarified that Monday's front-month October WTI contract
  settled at $95.78 while a separate November contract settled at $92.47 —
  the earlier split was a contract-month mismatch across sources, not a
  genuine data conflict. **Edition 27 hit a fresh instance of exactly this
  trap on the contract *roll* itself** (not just a cross-source split): the
  front-month rolled October-to-November between Tuesday and Wednesday, so
  Wednesday's $92.16 November print had to be compared against Tuesday's
  November close ($90.52, +1.81%) rather than the expired October settle
  ($94.59), which would have implied a misleading -2.5%-ish "decline." **The
  general lesson, now reinforced three times:** whenever a commodity price
  splits or looks discontinuous across sessions, check for a contract-month
  roll or a contract-month mismatch across sources before concluding it's a
  sourcing failure — this is now a near-routine check for oil specifically
  around monthly expiries.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done** — and if it reports 0 inline citations found
  while your Annex B clearly has entries, check for the combined-bracket
  `[n][m]` mistake above before assuming something else is wrong. Also
  remember it only scans HTML text — a citation number baked into a chart
  PNG's label is invisible to it (see Confirmed format above), and so is a
  bare `[n]` typed outside any `<sup>` tag (see edition 27's near-miss under
  Confirmed format above — caught by visual proofreading, not by the script).
  Also remember it flags Annex B entries that were drafted but never actually
  cited inline (e.g. in a movers table) — edition 26 hit this with four
  single-stock sources drafted into Annex B before the citations were added
  to the movers table's driver column; caught and fixed by running the check
  before declaring done, per this rule.
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
  carries real information first. Not needed at editions 26 or 27 — page 3
  filled naturally from content alone both times, with no padding block
  required.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` delayed-quotes JSON endpoint first — it often
  returns VIX, VIX9D, VIX3M, VIX6M, VVIX and SKEW directly, but has (at least)
  three observed failure modes: (a) a full clean sweep with genuinely fresh
  timestamps on every series, (b) the more common "thin-series-stale"
  pattern, where VIX/VIX3M refresh but the thinner series silently serve a
  stale prior-session snapshot, (c) total failure, where every series is
  stale. Editions 25-26 got full clean sweeps. **Edition 27 hit a variant of
  (c) worth naming explicitly: a "full stale sweep"** — every one of the six
  series, including VIX itself, carried the *prior* session's `last_trade_time`
  and value, not just the thin series. This is functionally the same as
  mode (c) but is worth distinguishing from a partial/thin-series failure
  when logging which failure mode occurred, since the required fallback
  (headline VIX only, from news) is the same either way but a full sweep
  failure means zero series are usable, not just the thinner ones. **Always
  check the `last_trade_time` field on each individual series** — never trust
  that the endpoint responded as proof the data is fresh. Also note a
  `prev_day_close` field bug, now observed **six editions running (22-27)**:
  it duplicates the day's own `close`/`current_price` rather than giving a
  real prior-day reference, and this corrupts the feed's own
  `price_change`/`price_change_percent` fields too — **never quote the
  feed's `price_change`/`price_change_percent` fields directly; always
  compute day-over-day % change manually against the previous edition's
  logged close.** Fall back to news coverage (Yahoo Finance, CNBC,
  MarketWatch) for at least the headline VIX close if the feed is stale, and
  disclose it as single-sourced — this is what edition 27 did for the full
  stale sweep. Separately: the mechanical VIX9D-vs-spot-VIX distortion from
  the 16 Sept FOMC aging out of the 9-day lookback window (tracked editions
  23-25, stabilized since) remains resolved — no re-emergence, and it's not
  currently checkable anyway while the feed itself is down.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table
  and (absent fresher CoT data or another dominant story) chart #2. Worked
  cleanly again at editions 26 and 27. **Stockanalysis.com single-stock pages
  are also the standing default for pinning an exact closing price/% change
  on any individual mover** — editions 26 and 27 both used direct fetches to
  it to resolve several sources' conflicting intraday-move percentages
  (edition 26: Viking Therapeutics, On Holding, SanDisk, GameStop, AutoZone,
  JPMorgan, Wells Fargo, PayPal, Worthington Enterprises; edition 27:
  Paychex, Cracker Barrel, Expedia, Airbnb, Booking Holdings, Alphabet,
  Amazon, Meta). Worth doing proactively for any mover whose research-pass
  figures disagree by more than a rounding error, rather than only for the
  single biggest story of the day. Note that AP's own GICS sector-index
  percentages can differ slightly from the SPDR ETF price-change figures
  (edition 27: AP's utilities -1.72%/communication services -1.49% vs. SPDR
  XLU -1.92%/XLC -0.85%) — this is a normal index-vs-ETF-price methodology
  gap, not a data conflict; keep using the SPDR ETF figures as the table's
  primary numbers (for consistency with the chart) and mention the AP
  variant only if it's notably different.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**, but note wire commentary sometimes gives a usable
  qualitative/approximate breadth read in prose even when the table isn't
  available — edition 27 cited Reuters' "decliners led advancers roughly
  1.9-to-1" and AP's "more than 72% of issues fell" directly from the wire
  stories used for the index closes, with no extra sourcing effort required.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page on direct fetch — this has now
  recurred at editions 22, 24, 25, 26 and 27 (five straight) — search
  snippets can still surface headline numbers but treat as lower-confidence
  secondary sourcing, and if a figure looks implausible relative to the
  underlying index level, discard it rather than reporting it (edition 24: a
  "gamma flip level" that didn't reconcile with any plausible SPX price;
  edition 25: a third-party GEX tool showing dollar figures many orders of
  magnitude too small to be real SPX dealer gamma). **Edition 27 found a
  working alternative worth trying again: zerogex.io** — its SPX
  gamma-levels page gave a dated, timestamped read (net SPX GEX approx.
  +$9.47bn, positive-gamma regime, flip level 7,685) that reconciled well
  against the actual 7,706 close and is now the first usable dealer-gamma
  figure in three editions. Treat it as single-sourced/moderate-confidence
  until it's been corroborated or has worked reliably across a few more
  editions, but try it before giving up on this metric entirely.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. As of
  edition 25, even the *secondary* citations for CME FedWatch disagreed with
  each other (approx. 56% vs. approx. 59.7%) — unchanged through edition 26.
  **Edition 27's secondary citations converged to approx. 54-55.1%**, much
  closer together than the prior split — worth watching whether this holds.
- **Kalshi direct fetch:** now rate-limited (HTTP 429) for **five straight
  editions (23-27)** — this is a confirmed structural gap, not a transient
  issue. Edition 26's search-cached fallback failed outright (an internally
  inconsistent snippet, discarded); edition 27's attempt found nothing
  reportable either. Keep attempting a direct fetch each edition (it may
  recover), but there is no need to spend much prose on the failure each
  time — a one-line "failed again, Nth straight edition" plus whatever
  Polymarket/CME-FedWatch range is available is sufficient; do not treat the
  absence of a Kalshi read as requiring special narrative treatment anymore.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  six editions running (22-27)** — treat this as a durable, confirmed pattern
  rather than re-attempting lme.com first each time; **default straight to
  the fallback chain.** Shanghai Metals Market (metal.com) has now failed
  **six editions running (22-27)** — skip metal.com entirely and go straight
  to Westmetall.com (a German metals-data provider that republishes official
  LME cash/3-month settlement prices), which has now worked cleanly **six
  editions running** as the fallback. Disclose whichever was used. Because the
  fallback chain can change edition to edition, treat any day-over-day copper
  % change built across two different sourcing chains as approximate, not a
  precise like-for-like comparison.
- **Official Treasury par yields:** official home.treasury.gov H.15 data for
  the prior day worked cleanly for editions 25 and 26 for both the 10-year
  and 2-year. **Edition 27 found a new wrinkle: a same-day
  (rather than prior-day) Treasury.gov TextView pull for the 2-year gave an
  implausible reading (4.10%, a 60bp one-day move with no corroboration)
  while the 10-year figure from the same pull was broadly consistent with
  other sources.** The FRED series (fred.stlouisfed.org, DGS10/DGS2) proved
  more reliable for pinning the *prior* day's confirmed close and is what
  actually caught and corrected an error in edition 26's own logged Tuesday
  2-year figure (4.43% → corrected to 4.71%, see edition log). **Going
  forward: use FRED as the primary cross-check for the most recently
  *completed* trading day's yields (it lags one business day, same as
  official H.15), and treat a same-day TextView pull — especially for the
  2-year, which moves more in daily bp terms — with more skepticism than a
  10-year same-day read.** CNBC's own quote pages (US10Y/US2Y) returned HTTP
  403 on direct fetch at edition 26 — not a usable fallback right now; not
  re-tried at edition 27.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly rather than presenting old data as current. Note
  the report comes in (at least) two different methodologies/pages depending
  on the instrument: `financial_lf.htm` (Traders in Financial Futures, Asset
  Manager/Leveraged Funds categories) works well for equity index futures
  (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report is what actually carries VIX futures
  positioning — don't expect one page to have both. As of edition 27 the most
  recent data is still dated 15 Sept (published Friday 18 Sept); no new
  report had posted by the Wednesday 23 Sept cutoff — next update due approx.
  Friday 25 Sept, confirmed by direct fetch of the CFTC page itself both at
  editions 26 and 27.
- **GBP/USD and EUR/USD clean close:** fully resolved as of edition 26 —
  Yahoo Finance as primary with a second wire/vendor piece as corroboration
  is the standing working pattern for both pairs. **Edition 27 used Yahoo
  Finance alone (the corroboration step is no longer treated as mandatory
  now that the pattern is established) and flagged a separate, new
  observation instead: Wednesday's DXY gain (+0.53%) looked large relative
  to the -0.15%/-0.21% moves in EUR/USD/GBP/USD** (EUR/USD is DXY's dominant
  weight) — this magnitude mismatch was disclosed rather than resolved; worth
  a second look if it recurs, since a properly weighted DXY move should
  track its two largest components fairly closely absent a divergence in a
  smaller-weight component (e.g. USD/JPY, which also only moved +0.06%).
- **Gold/silver clean close on a non-event day:** even without an FOMC-style
  settle-vs-spot timing split, Kitco's own quote can differ meaningfully by
  timestamp within the same session, and futures (GC=F/SI=F) vs. spot XAU/
  XAG quotes from different vendors can also diverge by several tenths of a
  percent on an ordinary day. Edition 26 found a larger, less explicable
  split on an ordinary day: Kitco/Fortune spot at $4,358.80 (-0.45%) vs.
  USAGOLD's own report at $4,307.63 (recomputed approx. -1.62% against the
  same baseline) — over a full point of disagreement with no settle-vs-spot
  timing mechanism identified. **Edition 27 found the same two vendors much
  closer together** ($4,297.53 Kitco vs. $4,304.11 USAGOLD, about $7 apart)
  — still disclosed as two separate reads (each vendor's own day-over-day %
  change differs meaningfully: approx. -1.4% vs. approx. -0.08%) rather than
  picked to one number, since the underlying cause of the gap (whatever it
  is) hasn't been identified either way. Cite the print closest to a
  standard NY 4-5pm ET close as primary and disclose the wider range rather
  than presenting one snapshot as *the* close — this looks like a recurring
  category of gap on gold specifically (now two editions running), worth
  continued tracking of whether the gap narrows further, stays roughly
  constant, or widens again.
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue, not with Friday retail sales — confirm on
  the BLS/Fed release schedule rather than assuming a date. **PCE inflation
  (Personal Income and Outlays):** confirmed via bea.gov that the report
  covering a given month's data publishes at the *end* of the following
  month (e.g. August 2026 data on 30 Sept 2026) — a "week ahead" secondary
  source at edition 24 mis-dated this to 27 Sept (a Sunday, impossible);
  verify PCE's date against bea.gov directly rather than trusting a
  secondary "week ahead" roundup. Not re-checked at edition 27; worth
  re-confirming as 30 Sept approaches.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey — resolved at
  edition 27:** edition 26 flagged this as unavailable due to materially
  conflicting secondary-aggregator figures for what was believed to be a
  Tuesday 22 Sept release. A direct philadelphiafed.org fetch at edition 27
  confirmed the release date (Tuesday 22 Sept 2026, not Wednesday) and the
  headline Regional Activity Index (-22.0, weakest since June), along with
  several sub-indices (General Activity/firm-level 0.3, New Orders -2.2,
  Sales/Revenues 6.8, Full-Time Employment 19.0, Prices Paid 37.8, Prices
  Received 20.0). **This thread is closed** — going forward, go straight to
  philadelphiafed.org's own release page for this survey rather than search
  aggregators, per the general lesson below.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  edition 25 flagged this only for lacking an explicit date stamp (a
  plausible 713,342-contract figure, moderate confidence). Edition 26
  escalated this to a confirmed data-quality problem: the figure for
  Tuesday's session was identical, to the exact contract count, to edition
  25's already-logged Monday figure — strong evidence the page was serving a
  stale/cached read. **Edition 27's read (902,421 contracts) was genuinely
  different from Tuesday's stale-duplicate 713,342 figure**, so it passed the
  "not a repeat" check and was reported — but the page still displays no
  visible date/"as-of" label, so date attribution still rests on inference
  (the value being pulled at/near cutoff) rather than an on-page timestamp.
  **Keep applying the same-as-last-time check every edition before reporting
  a figure from this page**; if it ever repeats a previously-logged number
  again, mark unavailable rather than reporting a stale read.
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
  revisited at editions 25, 26 or 27 since no fresh CoT data posted in any of
  those windows.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  (e.g. estimated closing-auction imbalance dollar amounts around a
  quarterly rebalance) tends to come from independent research
  Substacks/blogs (e.g. QSG Research) rather than a sell-side desk by name —
  treat as citable but note it's not a bulge-bracket named source when it
  matters for confidence level.
- **A stale "already happened" premise can survive multiple editions as an
  open thread if nobody actually chases the primary source (lesson from
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
  Editions 26 and 27 both rendered a well-balanced 4 pages on the first try
  with no padding block needed — content volume alone was enough both times.

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
  capping either). Edition 26 extended the precedent further: VKTX at
  +35.67% vs. next-largest ONON at +7.58%, about 4.7x — still left uncapped,
  since "order of magnitude" (approx. 10x) is the actual threshold and 4.7x
  reads fine on the standard axis. **Edition 27's spread was much narrower
  still** (PAYX -8.77% vs. next-largest EXPE -7.72%, about 1.14x) — obviously
  no capping needed. The rule has not yet had a genuine 10x+ case to test.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used again at edition 27 for a
genuine rate-spike-driven rotation into defensives/away from Energy's
strength, at edition 26 for a financials-vs-materials rotation reversal, and
at edition 25 for a broad chip-led rally with sector rotation as the clearest
secondary story). Fresh CFTC CoT data on a Monday/weekend-window edition →
the ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart —
**normalize as % of open interest if that figure can be sourced; if not, a
category's own net-position-as-%-of-its-own-gross-long+short is an
acceptable, honestly-labelled substitute** (used at edition 24 when total OI
wasn't obtainable). A single dominant earnings print with a clean,
well-sourced implied-vs-realized-move story → a three-bar
implied/historical-average/realized move chart (see the known-hard-to-source
note above — the historical-average leg has never actually been sourced
successfully yet). A genuine multi-sector broadening/deepening selloff across
consecutive sessions → the sector-ETF proxy rendered as a grouped
(day-over-day) bar instead of single-day. A holiday-window preview edition
with no fresher data → VIX futures term structure with event annotations
(CPI/FOMC/OpEx, etc.). When chart #1 (movers) already covers the
earnings/single-name story, the sector proxy is a good complementary choice
even on a stock-heavy day — edition 25 used exactly this combination (chip-
stock movers as chart #1, sector rotation as chart #2), edition 26 again
(biotech/consumer movers as chart #1, financials-led rotation as chart #2),
and edition 27 again (earnings/Muse-driven single-name movers as chart #1,
a rate-spike-driven sector rotation as chart #2) — in all three cases the two
stories reinforced rather than duplicated each other. **Chart #2's placement
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

**Editions 1–25 (condensed):** established the format (edition 1 baseline;
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
lines of genuine copy overflow, trimmed to 4. **Edition 25** (Tue 22 Sept,
covering Mon 21 Sept, the window's one session): a broad chip-stock rally
(Intel +12.0%, AMD approx. +10% and above a $1tn market cap for the first
time, Qualcomm approx. +9%, Arm Holdings +16.6% to $322.90 on a Piper Sandler
initiation) pushed the Nasdaq to a record 27,122.09 (+2.26%), S&P 500
7,764.70 (+1.49%); the quarterly S&P 500/400/600 and Nasdaq-100 rebalance
took effect at the open (Bloom Energy/Illumina/Everpure joined the S&P 500;
SpaceX's Nasdaq-100 weight rose to 2.82%); Grail approx. +30% (FDA review
pending), HP Inc. -4.22% (withheld FY2027 guidance); Brent -2.97% to $100.34
on Iran-Oman Hormuz diplomacy while WTI's Monday settlement split
($92.28-95.80) went unresolved at the time (later resolved at edition 26 as
an October/November contract-month mismatch, clean baseline $95.78); EUR/USD
and GBP/USD both got clean single Yahoo Finance closes for the first time,
single-sourced at the time (cross-corroborated and closed as a thread at
edition 26); VIX 14.87 (+0.41%); an open thread asking for confirmation of a
reported Block Inc.-for-Hess Corp S&P 500 swap "effective Wed 23 Sept" was
later found at edition 26 to describe an event from July 2025, a stale
premise now closed.

**Edition 26 (condensed)** — Wed 23 Sept 2026 report covering Tuesday 22
Sept 2026, the window's one NYSE session. Dominant story was a
financials-led sector rotation, not a broad index move: S&P 500 closed
effectively flat at 7,764.64 (-0.00%), Dow fell 0.36% to 51,863.69 on a bank
selloff (JPMorgan -3.42%, Wells Fargo -3.92%, Morgan Stanley -2.88%), Nasdaq
set a second consecutive record close at 27,244.28 (+0.45%) — confirmed via
Yahoo Finance/FRED after neither AP nor Reuters could be located for the
date and several syndicated "AP" reposts were caught stale-republishing
Monday's numbers under a Tuesday date/URL. A paywalled Bloomberg piece tied
the bank selloff (and separately, Expedia/Booking Holdings/Carnival/American
Airlines moves) to fears that Meta's new "Muse" AI shopping agent
disintermediates commission-based business models — reported as plausible
but unconfirmed context at the time; Richmond Fed President Barkin's same-day
hawkish remarks were the more concretely-sourced driver. Viking Therapeutics
(VKTX) +35.67% (positive obesity-drug data) was the session's standout
mover; On Holding +7.58%, SanDisk +6.82%, GameStop +5.58%, AutoZone +3.26%
also moved on company-specific news. Worthington Enterprises' reported
intraday spike to approx. +15% vs. its actual +1.36% close, and PayPal's
reported 2-4.8% intraday Muse-related move vs. its actual +0.51% close, were
both flagged as unreconciled intraday-vs-close gaps. The Block Inc./Hess
Corp S&P 500 swap thread (carried from edition 25) was resolved as a stale
premise — the actual swap happened in July 2025. Fed Chair Kevin Warsh and
the Oct 27-28 FOMC date were re-confirmed; October-hike odds were Polymarket
approx. 53% hike (clean fetch) against Kalshi's fourth straight direct-fetch
failure (this time with no usable cached fallback either) and a still-split
CME FedWatch (approx. 56% vs. approx. 59.7%). Treasury H.15 gave a clean
10-year 4.96% flat and what was then logged as a 2-year of 4.43% — **this
2-year figure is corrected to 4.71% at edition 27, see below.** The
five-central-bank Thursday/Friday cluster (Norges Bank, Riksbank, Banxico,
SNB) was first dated here, with SNB then best-supported as Friday 25 Sept
(later corrected to Thursday 24 Sept at edition 27). Oil fell a second
session (Brent -1.09% to $99.25, WTI -1.24% to $94.59) on a Saudi pipeline
restart and US-Iran UNGA diplomacy, with the UAE state-wire recap resolving
edition 25's WTI settlement ambiguity as an October/November contract-month
split ($95.78 vs. $92.47). Gold showed a genuine, unreconciled Kitco-vs-
USAGOLD split ($4,358.80 vs. $4,307.63) that narrowed sharply at edition 27.
VIX closed 14.21 (lowest close of the year at the time, -4.44%) on a full
clean CBOE sweep; VIX options volume of 713,342 contracts was later found to
be a stale duplicate of Monday's already-logged figure. 50 sources, zero
mismatches, zero stray tildes.

**Edition 27 (most recent — full detail)** — Thu 24 Sept 2026 report
covering Wednesday 23 Sept 2026, the window's one NYSE session, research
window Tue 22 Sept 20:00 ET through Wed 23 Sept 20:21 ET. Verified the two
structural header rules again: date line reads the edition date (Thursday
24 September 2026), not the session date; window line starts at the given
research-window start (Tue 22 Sept 20:00 ET), not earlier.

A broad risk-off session, not sector-specific: S&P 500 -0.75% to 7,706.03,
Dow -0.68% to 51,511.59, Nasdaq Composite -1.13% to 26,936.04, Russell 2000
-1.77% to 2,838.66 — confirmed via two independently-agreeing wires (AP via
ABC News, Reuters via Honolulu Star-Advertiser) after both wires had failed
to post Tuesday's close in time for the prior two editions running; this
time both posted cleanly and agreed to the dollar/penny, a useful reminder
not to write off AP/Reuters as unreliable by default. A live stale-date-
republishing trap was caught and discarded: a Wednesday-dated aggregator
article (techflowpost) reproduced Tuesday 22 Sept's exact index levels and
the Schwab/Ameriprise bank-selloff story under a Wednesday URL — confirmed
stale via a second source (thestar.com.my) that explicitly stated the move
happened "on Tuesday."

Driver: the 10-year Treasury yield spiked to a 19-year high (sources range
approx. 5.09%-5.14%, not fully reconciled to one print) after S&P Global's
flash September composite PMI hit 58.4 (up from 56.0, strongest since July
2021; manufacturing 57.0, services 58.7) and Fed Governor Michael Barr said
in a Chicago speech that inflation is "not clearly trending toward target"
and further tightening "is likely to be needed." Sector rotation flipped
from Tuesday's financials-led selloff to a rate-driven decline: Utilities
(XLU -1.92%) and Real Estate (XLRE -1.55%) worst, Consumer Discretionary
(XLY -1.50%) dragged by travel names, Energy (XLE +0.96%) the only sector up
on an oil rally. Financials (XLF -0.47%) stabilized rather than extending
Tuesday's -1.97% rout; Materials (XLB -0.49%), Tuesday's leader, fell back
in line with the market.

The "Meta Muse" AI-agent disintermediation theme (flagged paywalled/
unconfirmed at edition 26) rotated from banks into online travel agencies
and was independently corroborated: Expedia -7.72%, Airbnb -7.56%, Booking
Holdings -5.07%, while Meta itself rose +1.02% as the AI distributor and got
a Cantor Fitzgerald price-target raise to $860 (from $680); a Goldman Sachs
trading-desk note explicitly extended the disintermediation thesis to
financials, insurance and telecom, closing this open thread. Paychex fell
-8.77% despite a topline/adjusted-EPS beat, on GAAP-vs-adjusted
earnings-quality concerns (GAAP EPS $1.21 vs. $1.34 adjusted) and weak free
cash flow; Cracker Barrel rose +4.49% on a large adjusted-EPS beat ($0.99
vs. approx. $0.26 consensus) and a reassuring FY2027 revenue/EBITDA
outlook. Alphabet -3.80% and Amazon -2.24% fell on no company-specific
news — a pure yield-driven de-rating of high-multiple megacaps. Analyst
actions beyond Meta/Cantor were confirmed by rating direction only (Stifel/
MSFT upgrade, JPMorgan/BP upgrade and TotalEnergies downgrade, Guggenheim/
Editas upgrade, UBS/CoreWeave initiation and PG&E downgrade, Citi/Smiths
Group downgrade, Raymond James/Baldwin Group downgrade) — dollar price
targets were not obtained for these.

Correction: edition 26's logged Tuesday 2-year Treasury yield of 4.43% is
corrected to 4.71% after a fresh direct FRED/H.15 pull this run; treat 4.71%
as the standing Tuesday baseline going forward. Wednesday's own 2-year close
could not be verified (a Treasury.gov TextView read of 4.10% was
arithmetically implausible against the corrected base and was discarded).
Open thread resolved: the Philadelphia Fed Nonmanufacturing Business Outlook
(flagged unavailable at edition 26) is confirmed via direct philadelphiafed.
org fetch as a Tuesday 22 Sept release, Regional Activity Index -22.0.

Macro: Fed Chair Kevin Warsh and the Oct 27-28 FOMC date both re-confirmed
fresh. October-hike odds converged into the mid-50s for the first time in
several editions: Polymarket approx. 54-56% hike (up from approx. 53%), CME
FedWatch secondary citations approx. 54-55.1% (versus the approx. 56%/59.7%
split carried since edition 25); Kalshi failed direct fetch a fifth straight
edition (23-27) with no usable cached fallback this time either. The
five-central-bank Thursday/Friday cluster (first dated at edition 26) saw a
correction: SNB's date moved from the previously best-supported Friday 25
Sept to Thursday 24 Sept — the same day as Norges Bank, Riksbank and
Banxico — based on the SNB's own established Thursday cadence and a dated
FXStreet preview; still not confirmed directly against snb.ch, which
continued to 404 on every attempted URL. The Trump-Xi Washington summit's
opening-day protocol events (Trump personally greeting Xi and Peng Liyuan at
Joint Base Andrews; Bessent-He Lifeng meeting) took place Wednesday; the
main bilateral meeting, military ceremony and state dinner are Thursday.
SOFR's most recent published reading (Tuesday, T+1 lag) was 3.87%, up from
3.85%.

Commodities/FX: oil reversed sharply intraday — an early slide below $99
(Saudi pipeline restart, a larger-than-consensus EIA build, magnitude
unreconciled across sources at approx. 1.7-3.0m barrels) gave way to a rally
after Iranian President Pezeshkian told the UN Iran "cannot be made to
surrender" (Brent +3.86% to $103.08, snapping a five-session losing streak).
WTI hit a fresh instance of the contract-roll trap: the front-month rolled
October-to-November this session, so Wednesday's $92.16 November print was
compared against Tuesday's November close ($90.52, +1.81%) rather than the
expired October settle ($94.59), which would have implied a misleading
decline — this is now the third documented instance of a contract-month
mismatch/roll issue on oil (editions 24, 25/26, 27). Gold's Kitco-vs-USAGOLD
split (first flagged at edition 26) persisted but narrowed sharply to about
$7 apart (from approx. $50 on Tuesday); each read against its own prior-day
baseline still implies a different % change (approx. -1.4% Kitco vs. approx.
-0.08% USAGOLD). Copper via Westmetall (lme.com/metal.com now a confirmed
6-for-6 failure streak) $14,735.00/t (-0.42%). DXY approx. 101.10 (+0.53%),
a magnitude that looks large next to EUR/USD's -0.15% and GBP/USD's -0.21%
moves — flagged as an unreconciled gap rather than smoothed over.

Derivatives: the CBOE delayed-quotes feed hit a new failure-mode variant — a
full stale sweep across all six series (not just the thinner ones), every
`last_trade_time` reading Tuesday's close. VIX's Wednesday close of 15.18
(+6.83%, computed manually vs. Tuesday's 14.21) was sourced from news
coverage only; VIX9D/VIX3M/VIX6M/VVIX/SKEW are unavailable for Wednesday.
Cboe's options-volume page gave 902,421 contracts, genuinely different from
Tuesday's stale-duplicate 713,342 (so the recurring staleness check cleared
this time), though the page still carries no on-page date stamp. SpotGamma
failed a fifth straight edition (boilerplate only); a new alternative
source, zerogex.io, gave a fresh, dated, sanity-checked net SPX gamma read
(+$9.47bn, flip level 7,685 vs. a 7,706 close) — worth trying again as a
SpotGamma fallback in future editions. CFTC CoT confirmed still dated 15
Sept via direct cftc.gov fetch, next due approx. Fri 25 Sept. 35 sources,
zero mismatches, zero stray tildes. Page 3 filled naturally; no padding
block needed.

**Open threads for edition 28:** the four (now likely same-day) Thursday
central-bank decisions (Norges Bank, Riksbank, Banxico, likely SNB) and the
Trump-Xi summit's Thursday culmination (bilateral meeting, state dinner) all
postdate this window — track their actual outcomes once they land, and
confirm SNB's exact date and outcome directly against snb.ch once it posts.
Wednesday's 2-year Treasury close was never resolved (the only figure found
was implausible and discarded) — try again via FRED once Wednesday's data
posts. Dollar-figure price targets for Wednesday's non-Meta analyst actions
were not obtained — worth another look if any of those names move further.
zerogex.io is a promising new SpotGamma alternative for dealer gamma — test
it again next edition to see if it's repeatable or was a one-off. The CBOE
feed's new "full stale sweep" failure mode (distinct from the usual
thin-series-stale pattern) — watch whether this recurs or was a one-off.
The DXY-vs-EUR/USD-GBP/USD magnitude mismatch on Wednesday is unresolved —
worth a second look if it recurs. The Kitco-vs-USAGOLD gold split has now
narrowed for a second straight edition (from approx. $50 to approx. $7) —
keep tracking whether it continues to close, stays roughly constant, or
widens again. Two threads are recommended for dropping rather than further
carrying: whether Monday 21 Sept's quarterly index rebalance produced
above-normal trading volume/volatility (carried since edition 24/25 with no
resolution across four editions now and not chased again at edition 27); and
Worthington Enterprises' intraday-spike-vs-close gap (approx. $67.94 vs.
$58.94, not revisited at edition 27 either) — both can be dropped unless a
future edition happens to surface a decisive figure on either. One thread is
closed after resolution rather than chased further: the Block Inc./Hess
Corp S&P 500 premise (resolved as stale at edition 26) — do not re-open
unless a genuinely new index-change report surfaces.
