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
  is where the sessions covered belong, not the date line. **Editions 33
  through 38 have all applied this correctly** ("Friday 2 October 2026,"
  "Monday 5 October 2026," "Tuesday 6 October 2026," "Wednesday 7 October
  2026," "Thursday 8 October 2026" and "Friday 9 October 2026" respectively as
  the date line, with the window line carrying the session(s) covered) — now
  confirmed stable across six consecutive editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 38 all reused the
  same pattern for single-session windows — now confirmed clean across ten
  consecutive single-session or single-session-plus-weekend editions (29
  through 38). No further confirmation needed; treat this as settled.

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
- **FOMC minutes from the Sept 15-16 meeting — closed thread as of edition 37,
  do not re-derive:** released Wednesday 7 October 2026, 2:00pm ET, read
  directly against federalreserve.gov. Vote was unanimous 12-0 with no dissent
  recorded ("all participants viewed a higher target range... as
  appropriate"). The one internal-division signal: "most participants" (not
  all) assessed that another increase would likely be appropriate by year-end,
  with the Committee stressing data-dependency meeting to meeting. No overt
  October-specific debate was named in the text.
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 38
  directly against federalreserve.gov's own FOMC calendar page. The meeting is
  now under three weeks out — continue re-confirming every edition between now
  and then. Decision and press conference both land 28 Oct, 2:30pm ET. The
  following meeting is December 8-9, 2026 (an SEP meeting).
- **October-hike odds — the first POST-minutes reading was finally obtained at
  edition 38, closing the single most important open item flagged at edition
  37:** DeFi Rate's Kalshi/Polymarket-blended aggregator, snapshot Thursday 8
  Oct 2026 8:19pm ET (more than 30 hours after the Wednesday 2:00pm ET minutes
  release), shows **October 27-28 hike odds approx. 16-17%** (Kalshi ~15.5-17%,
  Polymarket ~15.5%) and **December 8-9 hike odds approx. 74-76%** (page's
  meeting-path table said 75%, movers table implied ~74%) — essentially
  **unchanged from the pre-minutes range** (edition 37's carried-forward
  approx. 16-18% Oct / approx. 72% Dec), meaning the hawkish-but-cautious
  minutes (unanimous Sept hike, but only "most" not "all" backing a further
  2026 move) did not meaningfully reprice the path. A composite "at least one
  more hike in 2026" market read approx. 80%. Treat this thread as closed for
  now; refresh with a new snapshot every edition as usual, but there is no
  longer an urgent pre/post-minutes gap to chase.
- **US-China "30-for-30" tariff framework — closed thread as of edition 37, do
  not re-open:** the list-size reversal flagged at edition 36 (a secondary
  source describing China's list at ~1,619 items and the US list at 77, the
  opposite of the long-standing primary-confirmed framing) is resolved. A
  direct whitehouse.gov fetch of the framework's own Terms of Reference
  document, confirmed at edition 37, shows the original assignment is
  correct: **77 US product categories (household goods, textiles, appliances,
  toys, sporting goods, vacuum flasks) and 1,619 Chinese categories (dominated
  by food/farm goods — beef, pork, poultry, seafood, grains, dairy,
  wine/whiskey — plus some medical devices; soybeans, chips, EVs and batteries
  excluded from both sides)**, each side's treatment benchmarked at approx.
  $30bn against 2024 bilateral trade. One minor unresolved wrinkle: two
  whitehouse.gov PDF copies of the terms of reference carry different dates
  (Sept 23 vs Sept 27, 2026), text otherwise identical — not worth chasing
  further unless it becomes load-bearing. Still pending each side's domestic
  legal processes for actual implementation — watch for a formal
  implementation/effective date in a future edition.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch,
  rba.gov.au, etc.) every edition, exactly like any other data point. Edition
  34 reconfirmed Kevin Warsh as Fed Chair directly against federalreserve.gov's
  Board of Governors bios page; editions 35 through **38 have all
  re-confirmed the same page again — still Kevin Warsh, unchanged, now six
  straight direct re-confirmations.** The BoE and shutdown/CR open gaps
  flagged at edition 35 were closed at edition 36 via direct primary-source
  fetches (bankofengland.co.uk, whitehouse.gov); **edition 38's shutdown/CR
  reconfirmation used two independent secondary sources (AACOM, ASAHP) rather
  than a direct whitehouse.gov fetch** — the underlying fact is unchanged
  (funded through 11 Dec 2026 via H.R. 6500) but note the primary-source touch
  lapsed this one round; try a direct whitehouse.gov fetch again at edition 39
  if time allows, though this is not urgent given two independent
  corroborating secondaries agreed exactly. **The BoJ primary-source gap on
  its *next meeting date* — three straight editions of secondary-only sourcing
  — was finally closed at edition 38**: a direct fetch of
  boj.or.jp/en/mopo/mpmsche_minu/index.htm (the BoJ's own MPM schedule page)
  succeeded on the first attempt this time (no local-PDF-extraction workaround
  needed), confirming the next Monetary Policy Meeting is **October 29-30,
  2026**, followed by a Summary of Opinions November 10 and the October
  meeting's minutes December 23. This closes the last standing BoJ
  primary-sourcing gap; no further action needed on this specific item unless
  a new one surfaces.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — last directly re-confirmed
  at edition 37 via bankofengland.co.uk; **not freshly re-touched at edition
  38** (explicitly deprioritized given the heavier post-minutes Fed-odds and
  BoJ research load that edition). No further confirmation needed until closer
  to the 5 Nov decision, but resume the direct-fetch discipline once the
  meeting is inside a roughly one-week window.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano), both primary-sourced as of edition 37 — closed thread, do
  not re-derive. **The next policy meeting date (Oct 29-30, 2026) is now also
  primary-sourced as of edition 38** (see above) — this closes the BoJ's last
  open sourcing gap. No further action needed on BoJ facts unless a new
  meeting/decision supersedes the above.
- **The four-central-bank Thursday 24 September 2026 cluster remains fully
  resolved — closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% (matching an 18-economist
  Bloomberg survey) but signalled a greater chance of a Q4 hike; Banxico held
  at 6.50% unanimously; SNB held at 0% and raised its inflation forecasts
  (0.7%/0.8%/0.8% for 2026-28), confirmed directly against snb.ch. No fifth
  central-bank decision was identified in this window either.
- **The Reserve Bank of Australia's Tuesday 29 September 2026 decision remains
  fully resolved — closed thread, do not re-open:** hiked 25bp to **4.60%,
  unanimous**, a 15-year high and its fourth hike of 2026, confirmed directly
  against rba.gov.au's own Statement by the Monetary Policy Board.
- **August 2026 PCE inflation — closed thread, resolved at edition 32, do not
  re-open:** headline +0.3% m/m/+3.4% y/y (down from 3.7% in July), core +0.2%
  m/m/+3.0% y/y (down from 3.3% in July) — a clean disinflation signal that was
  the proximate trigger (with NY Fed Williams' remarks) for edition 32's
  October-hike-odds collapse. One minor sub-item never resolved and remains a
  standing Annex-A-level gap if it ever matters again: the precise quantified
  effect of BEA's concurrent annual benchmark revision on the y/y base was not
  isolated from the release text.
- **September 2026 jobs report — closed thread since edition 34, do not
  re-derive, but watch for revisions in later BLS releases:** nonfarm payrolls
  +29,000 (the weakest print of the cycle) vs. approx. 84,000-90,000
  consensus; unemployment rate 4.2% (up from 4.1%); average hourly earnings
  +0.1% m/m / +3.0% y/y; July revised from +21,000 to an outright -10,000,
  August revised from +162,000 to +133,000 (a combined -60,000 revision),
  confirmed directly against bls.gov's Employment Situation Summary. This was
  the single biggest catalyst of edition 34's window — see the October-hike
  odds entry above for how the market reaction has since evolved.
- **September 2026 ISM Services/Non-Manufacturing PMI — closed thread as of
  edition 35, do not re-derive:** headline 54.9% (down from August's 55.4%),
  Prices Paid 74.0% (+1.4pt, highest since July 2022), the sixth month in
  seven above 70%. Confirmed directly against ISM's own press release.
- **No US federal government shutdown is in effect — last directly
  re-confirmed at edition 37 via a whitehouse.gov fetch, and again at edition
  38 via two independent secondary sources (AACOM, ASAHP)** (briefing
  statement on H.R. 6500, the Continuing Appropriations and Extensions Act,
  2027): signed into law 2 September 2026, funds the government through
  **11 December 2026**. Watch for shutdown risk resurfacing as 11 December
  2026 approaches. The generic "Government Shutdown Clock" page with
  stale/inconsistent content (flagged at edition 35) was not encountered again
  at editions 36, 37 or 38.
- **China September 2026 CPI/PPI — open, not yet released as of edition 38's
  cutoff:** a direct fetch of stats.gov.cn's latest-releases page (checked
  8-9 Oct Beijing time, within edition 38's window) still showed August data
  only (+0.8% y/y CPI, +3.8% y/y PPI, both dated 9 Sept 2026) and did not
  forward-list a September release date. One secondary source (financecalendar.com)
  claims 14 October 2026, which conflicts with the usual 9th-10th-of-the-month
  pattern — **the release date itself is unresolved, not just the data.**
  Check stats.gov.cn directly again at edition 39 rather than assuming either
  date.

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
  more consecutive citations. A related trap surfaced at edition 28's own
  draft, worth naming explicitly: placeholder ref text (e.g. `[note1]`) typed
  during drafting and never swapped for a real number. `check_refs.py`'s
  regex requires `\d+` inside the brackets, so a non-numeric placeholder like
  `[note1]` simply won't match either the inline or Annex-B regex — it won't
  show up as "missing" or "unused," it just silently doesn't count. **Never
  use a letter suffix to disambiguate a citation — always mint a new
  integer** (edition 30's `[9b]` near-miss). Annex B numbers do not need to
  be contiguous, only matched 1:1 against inline citations — deleting an
  unused reserved number and leaving a gap is completely fine and simpler
  than renumbering everything after it (edition 29). **Reusing the same
  Annex B number for multiple movers/figures citing the same outlet/method is
  fine and recommended** — `check_refs.py` only checks presence/absence, not
  uniqueness of use (editions 33-38 have all done this for stockanalysis.com
  single-stock closes and other repeatedly-used outlets, confirmed stable
  across six editions).
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart 2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes). **Chart
  placement is editorial, not fixed to Section 2** — edition 24 and edition
  34 both placed a CFTC-positioning chart #2 in Section 5 (Derivatives)
  rather than Section 2, since that's where the content actually belongs.
  Editions 35 through 38 all reverted to the sector-ETF-proxy default (no
  fresh CoT data due in any of those editions) and kept it in its default
  Section 2 placement — use Section 5 placement again whenever a future
  CFTC-positioning chart #2 recurs (likely edition 39, given the fresh CFTC
  report due Friday 9 October lands inside its window — see Known-hard-to-
  source below).
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
  **Editions 27 through 38 are all clean counter-examples worth keeping in
  mind**: all twelve posted a usable AP wire eventually — edition 38's AP
  wire was only reachable via a La Nación syndication mirror, still a clean,
  dated, directly-attributable AP figure. **Edition 37 is a useful
  cautionary tale about method, not about the source itself**: a
  general-purpose WebSearch AI-summary returned the correct AP figures
  attached to a *guessed* URL, and the research subagent — correctly
  following the standing caution about AI-summarized fetches inventing
  numbers — could not independently corroborate it and flagged it as
  possibly fabricated. **The lead/writer step then directly re-fetched the
  real article plus a second independent syndication mirror and got the
  exact same figures, confirming they were correct all along, not
  fabricated.** The lesson stands: the standing caution against AI-summary
  fabrication is about **unverified precision that conflicts with
  everything else** — a precise figure that *cannot yet be corroborated* is
  not automatically a fabrication, and the correct response is to attempt a
  direct, independent second fetch before discarding it, not to assume bad
  faith by default. Always have Yahoo Finance + FRED/stockanalysis.com ready
  as the working fallback regardless. **Edition 36's AMD-price-target and
  Novavax/Moderna-driver fabrications remain the clearer, more severe
  examples of the opposite failure mode** (a number that conflicted with
  independently-sourced reality) — both lessons stand side by side: verify
  before excluding AND verify before including.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. This has been caught at least thirteen times across editions 25
  through 34 (Trefis, Rio Times, FXStreet, Kitco and others re-serving prior-
  day data under a new dateline). **Edition 35 caught a distinct variant on
  analyst commentary rather than price data** (stale Nike price-target cuts
  recirculated as if dated Monday when they were Friday/Saturday originals).
  Always check a dated article's own body text against the logged
  prior-session figures before trusting its date stamp, regardless of which
  outlet it is. A same-day close and a next-day after-hours-triggered move
  can legitimately combine into one large single-day % change — edition 24's
  Xenon Pharmaceuticals -30.7% Friday move is the reference example. Check
  whether a headline % move is measured close-to-close before assuming two
  reports conflict. **The intraday-vs-close divergence trap is still very
  much alive**, caught across many editions (Worthington, Paychex/Cracker
  Barrel, Oracle, Akamai, STX/WDC/SNDK, MongoDB, Liquidia, Concentrix,
  Citigroup options-wire, Nike, SPCX). Resolved the same way as always: treat
  the stockanalysis.com (or equivalent timestamped) close as authoritative,
  and disclose explicitly when an earlier-session figure doesn't match the
  close. **A distinct corporate-action (stock-split) data artifact trap was
  first logged at edition 35** (Paramount Skydance's spurious "+96%"
  premarket figure, actually a 2-for-1 split artifact) — before reporting any
  single-stock move that looks like an outright magnitude error (roughly
  doubling, halving, or near-100%), check for a split/reverse-split/listing
  change and exclude the figure if a stale unadjusted-quote explanation fits.
  **A related but distinct ticker-change trap recurred at edition 36-37**:
  when Paramount Skydance/Warner Bros. Discovery's $110bn merger closed
  Tuesday 6 Oct and the surviving entity moved to ticker SKYD, no reliable
  same-day % figure was obtainable on the transition day itself (edition 36,
  correctly left unreported) — but **by the very next session (edition 37),
  stockanalysis.com had a clean, exchange-timestamped close under the new
  ticker (SKYD $8.89, -6.72%)**, fully resolvable. **General technique worth
  keeping: when a ticker-change/listing-transition makes the transition day
  itself unsourceable, don't force it — but re-check the new ticker on the
  very next session, since the gap is often transition-day-only, not
  durable.** **A distinct "driver not found same-session" pattern recurred at
  edition 37→38: Caterpillar's Wednesday -5.75% move had no corroborated
  driver at edition 37's cutoff, but a dated FTC/USDA farm-equipment-inquiry
  article (published Wednesday, simply not yet indexed/discoverable within
  edition 37's research window) fully explained it by edition 38.** General
  technique worth keeping alongside the ticker-transition one above: when a
  same-day mover's driver can't be found despite a real search attempt, don't
  force a guess — report the move without a driver and explicitly flag it as
  an open thread, then re-search for a delayed explanation at the very next
  edition before assuming none exists.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. **Similarly, a price level can be correct while a vendor's stated
  %-change is wrong** if the vendor used a different prior-day base — always
  sanity-check that a stated price and stated % change reconcile
  arithmetically against the prior session's logged close. This exact pattern
  has now recurred repeatedly on oil specifically, and **edition 38 hit the
  most severe version yet — the gap persisted for a third-plus consecutive
  session on both WTI and Brent simultaneously**: multiple independent
  vendors (Investing.com, oilprice.com, TradingEconomics) agreed closely on
  Thursday's own closing *levels* (approx. $91.15-91.23 WTI, approx.
  $103.80-104.28 Brent) but none of their own stated %-changes reconciled
  against the prior session's logged close — each vendor's own internally-
  logged "Wednesday close" conflicted with the baseline this report carries
  forward (e.g. Investing.com's own historical table showed Wednesday WTI at
  $88.28 vs. this report's logged $89.07, and Wednesday Brent at $100.20 vs.
  logged $101.13). **This is now a well-established, durable pattern specific
  to oil (not a one-off) spanning at least editions 35, 37 and 38 — always
  compute the day's %-change directly off this report's own logged prior
  close rather than trusting any vendor's self-stated change, every edition,
  not just when something looks surprising, and disclose the method
  explicitly in the text.** The oil contract-month-roll trap (Brent
  Nov-to-Dec) remains resolved; not re-checked at edition 38 (no roll due).
  The CBOE vol-complex feed's two documented bugs (duplicate-
  `prev_day_close`, and `price_change_percent` dividing by current price
  instead of prior close) remain intermittent — **edition 38's direct fetch
  showed neither bug, a fifth consecutive clean read (35 through 38 plus the
  underlying pattern holds back further)** — always compute day-over-day %
  change manually as `price_change ÷ (current_price − price_change)` and
  treat the feed's own `price_change_percent` field as unreliable until
  checked each time regardless.
- **The DXY-vs-its-own-FX-crosses conflict** has now recurred, at least
  partially, in roughly half of all occurrences since edition 29 (resolved
  cleanly at 31, 33, 35; recurred at 32, 34, 36, 37; **and recurred again at
  edition 38, now a third consecutive session** — Thursday's DXY was
  flat-to-softer (approx. -0.02%) consistent with EUR/USD (+0.1%) and GBP/USD
  (flat/+0.03%) both ticking up against the dollar, but **USD/JPY again rose
  (+0.11%), the opposite direction** — the same specific cross (USD/JPY) that
  broke the pattern at editions 36 and 37 too, now three editions running.
  **Given USD/JPY has now been the specific break on three consecutive
  occasions, treat this going forward as a standing regime feature (a
  USD/JPY-specific, likely BoJ-policy-related dynamic) rather than an
  independent recurrence each time** — continue disclosing it explicitly
  every edition, but the "worth watching whether this continues" framing can
  graduate to "expect this by default and flag if it ever stops" at edition
  39 if the pattern holds a fourth time.
- **The same-day silver sign conflict first flagged at edition 31 has now
  stayed resolved for seven straight editions (32-38)** — silver rose/fell
  consistently across spot and futures at every session in that span. Treat
  as closed unless a fresh mismatch appears.
- **GBP/USD's two-edition data-quality problem (a minor two-source gap at
  edition 35, a genuine three-way level/direction conflict at edition 36)
  has now stayed resolved for two further editions (37, 38)**: edition 38
  again used the four-source method (Pound Sterling Live close-to-close
  history, live quotes, TradingEconomics) and found no conflict (approx.
  flat, +0.03%). **Note this timing artifact for future editions: a live FX
  quote fetched near/after the NY 5pm close may reflect the *next* session's
  opening tick, with its own "previous close" already equal to the session
  just completed — don't mistake this near-zero "live" change for the day's
  actual close-to-close move. Use a dedicated close-to-close history source
  (Pound Sterling Live worked well) rather than a live snapshot when fetching
  this late in the window.**
- **The 2-year Treasury yield conflict from edition 36 (TextView 4.46% vs.
  CSV 4.79%, a 33bp gap) has stayed resolved for two further editions (37,
  38)** — edition 38 fetched both the TextView and CSV endpoints directly
  again and found them in full agreement (2-yr 4.75%, 10-yr 5.22%, 30-yr
  5.60%, all Oct 8; Oct 7's figures, 4.77%/5.28%/5.67%, also matched the
  previously-logged baseline exactly). Treat as resolved/noise unless a fresh
  conflict appears; if one does, the standing advice stands — dig into which
  endpoint is wrong via a market-wrap secondary cross-check for the specific
  disputed maturity.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 38 have all run clean (or
  clean after one quick fix) — edition 38 drafted 25/28 on the first pass
  (three Annex B entries in the day-ahead table — BLS CPI schedule, TSMC
  earnings-call consensus, and the Meta/New Mexico penalty item — were
  defined but not yet cited inline), caught immediately by running the
  script, fixed by adding `<sup class="ref">` tags to the relevant day-ahead
  table cells, then re-ran clean at 28/28. Worth re-stating: table cells
  (and disclosure-box/tile-adjacent sentences) are a legitimate, already-used
  place to put a citation — use them rather than forcing an awkward prose
  mention just to attach a `<sup>` tag.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 38 have all rendered clean at zero tildes** on the
  first check. **Reminder: `grep -c` exits with status 1 (not 0) when the
  count is zero, since no lines matched — don't chain it with `&&` into a
  longer command and assume a silent failure means the check itself failed;
  read the printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 34 resolved this cleanly for
  CFTC CoT, with full OI and Asset-Manager/Leveraged-Funds breakdowns for
  ES, NQ and RTY. One naming note worth preserving: the CFTC's
  financial-futures table lists the full-size Russell 2000 E-mini ("RTY") as
  a separate line from the Micro E-mini Russell 2000, which has very
  different (much smaller) open interest and a different net-position sign
  at times — always confirm which of the two lines is being read before
  charting "RTY." No new CFTC report was due within editions 35 through 38's
  windows; the chart #2 slot reverted to the sector-ETF-proxy default each
  time accordingly. **The next CFTC report (due Friday 9 October, covering
  Tuesday 6 October data) will land inside edition 39's window — check
  cftc.gov first thing at edition 39 and use the positioning chart if a
  fresh report is available and edition 39 is a Monday/weekend-window
  edition per standing guidance.**
- **A genuinely new chart-layout bug surfaced at edition 37, worth fixing
  permanently in `make_charts.py`'s documented defaults: the sector-ETF-proxy
  panel2 chart at `figsize=(9.8, 1.55)` with `tick_fs=7.6` and 11 categories
  produced visibly overlapping y-axis category labels** (confirmed by
  rendering and visually inspecting the PNG directly, not just trusting the
  matplotlib call succeeded) — the 1.55-inch height does not give 11 rows
  enough vertical room at that font size in this environment. **Fixed by
  bumping panel2's figsize to `(9.8, 1.95)`**, which rendered cleanly with no
  overlap. **Edition 38 reused `(9.8, 1.95)` for panel2 (an 11-category
  sector chart) and confirmed it again renders cleanly with no overlap** — a
  second consecutive clean confirmation of the fix. **Going forward: use
  `(9.8, 1.95)` as the default panel2 figsize for any 10-11-category
  sector-ETF-proxy chart, and always visually inspect chart2 (not just
  chart1) at full resolution before embedding it** — a layout failure here
  was previously only being caught (if at all) by accident, not by a
  standing discipline. If a future chart2 has fewer categories (e.g. a 7-8
  row CFTC chart), 1.55-1.75in may still be fine — re-verify visually rather
  than assuming either figsize by default.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at editions 33 through 38 (edition 38: AAOI -13.58% vs. STZ +4.43%, about
  3.1x), all left uncapped. Edition 30 remains the one genuine 10x+ case to
  date (about 15x, capped at a fixed axis max of 30). No need to revisit the
  threshold or mechanism absent a genuinely new edge case (e.g. something in
  the 5-10x range).
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists** — confirmed again at edition 35 (four
  analyst actions all traced to one Benzinga/Yahoo roundup, disclosed as
  such). **Edition 37 hit the inverse problem: no analyst-action roundup for
  any name could be located at all for the session — and edition 38 hit the
  same gap again, a second consecutive edition with no dated roundup found
  beyond the earnings-tied price-target changes on the session's own biggest
  mover** (edition 37: none at all; edition 38: only Applied Digital's two
  earnings-linked PT changes, Needham and Wells Fargo). Don't force an
  analyst-actions subsection with weak/uncorroborated content just because
  most editions have one; disclosing the absence is the correct move when a
  genuine search comes up empty, and this is now looking like a more common
  outcome than a rare one — don't treat a missing roundup as a research
  failure requiring extra effort beyond one real attempt.
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38**: a secondary aggregator (TheFly, via stockanalysis.com's news
  feed) cited Applied Digital's Q1 EPS as "+1¢ vs. a -30¢ consensus," which
  flatly conflicted with the GAAP figures in the company's own 8-K ($(0.76)
  continuing-ops / $(0.82) total EPS). The likely explanation is that the
  aggregator's figure is a non-GAAP/adjusted metric reported without stating
  its basis — **when a secondary-sourced EPS figure conflicts sharply with a
  primary filing's GAAP number, prefer the primary filing, exclude the
  conflicting secondary figure from the main text, and flag it in Annex A
  rather than trying to reconcile or silently picking one.** This is a new,
  distinct trap from the already-documented price/percent-change
  reconciliation issue — watch for recurrences on other earnings prints.
- **Know when to treat a third-party data feed's own internal
  inconsistencies as a data-quality flag rather than a reportable trend.**
  Edition 38's zerogex (dealer-gamma) reads carried three separate
  within-session anomalies: the SPX page's own UI disclosed a "temporarily
  delayed... last available snapshot" caveat alongside its headline figure;
  the SPY net-GEX reading was roughly 24x smaller than the prior session's
  logged figure with no explanation (a scale discontinuity, not a smooth
  decline); and the QQQ page displayed two different values for the same
  metric in two different UI locations. None of these looked like a single
  clean trend (e.g. "gamma collapsed") — they looked like a feed/vendor
  data-quality problem. **The right call was to report the directional
  headline (still net positive-gamma across SPX/SPY/QQQ) while explicitly
  flagging each inconsistency, rather than asserting a clean quantified
  move.** Watch at edition 39 whether this was a one-session anomaly (likely,
  if next edition reads clean again) or a recurring zerogex data-quality
  issue worth adding permanently to the known-intermittent-bugs list
  alongside the CBOE feed's two documented bugs.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. **Editions 28 through 38 all got a full clean sweep** —
  eleven consecutive clean sweeps now, every series carrying a same-day
  `last_trade_time`, verified individually per series via a raw `curl`/direct
  fetch (not a tool-summarized fetch) each time. Still not a guarantee — keep
  checking `last_trade_time` on each series every time. The feed has two
  known intermittent bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) — **both have now been absent for four straight editions (35
  through 38)** — manual recomputation matched the feed's own stated
  percentages exactly each time. **Always compute day-over-day % change
  manually against the previous edition's logged close regardless.** The
  VIX9D-vs-spot-VIX front-end inversion (first flagged edition 28) had been on
  a broadening trend through edition 37 (-3.30) but **narrowed for the first
  time at edition 38, to -3.20** — watch at edition 39 whether this is the
  start of a reversal or a one-session blip; the pattern remains irregular,
  not monotonic in either direction, so don't assume either continuation or
  reversal by default.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table,
  and (absent fresher CoT data or another dominant story) chart #2. Editions
  35 through 38 all had no fresh CoT data due and used the sector-ETF-proxy
  default (eleven of twelve eligible editions now, the sole exception being
  edition 34's CFTC chart). **Stockanalysis.com single-stock pages remain the
  standing default for pinning an exact closing price/% change on any
  individual mover** — editions 26 through 38 (thirteen straight) have all
  used direct fetches to it. Note that a headline wire's own GICS sector-index
  percentages can differ slightly from the SPDR ETF price-change figures (a
  normal index-vs-ETF-price methodology gap); keep using the SPDR ETF figures
  as the table's primary numbers.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. Edition 38 used
  the "8 of 11 sectors closed higher" sector-ETF read as the best available
  breadth proxy, consistent with recent editions. Continue treating an
  uncorroborated single-aggregator (or unsourced search-summary) breadth
  figure as not usable — this has recurred enough times to treat as a
  durable, not occasional, gap.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — a recurring failure for many
  editions, not separately re-attempted at edition 38 (zerogex tried first
  per standing practice; a WebSearch for SpotGamma's Oct 8 content
  specifically returned only stale pre-October headlines). **zerogex.io
  remains the only working source across twelve straight editions (27-38)**,
  but **edition 38's reads carried unusual internal data-quality issues for
  the first time** (see the new Hard Rules entry above: SPX's own stale-
  snapshot disclaimer, a 24x SPY net-GEX scale discontinuity vs. edition 37's
  logged figure, and two conflicting QQQ figures on the same page). Reported
  directionally (SPX approx. +$22.56bn down from +$57.61bn, SPY approx.
  +$246.9mn, QQQ approx. +$203-223mn, all still net positive) but with
  explicit caveats rather than as a clean trend. **Watch at edition 39
  whether this was a one-off site/feed glitch (if clean again, treat edition
  38 as an anomaly and move on) or a recurring issue (if so, add it formally
  to the known-intermittent-bugs list).** The magnitude remains
  single-sourced (zerogex only; SpotGamma still yields no real numbers to
  cross-check against). Minor open item carried forward, still low priority:
  zerogex's own stated wall levels (call/put wall) have still not been
  cross-checked against a secondary options note's implied walls.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Edition
  38 used DeFi Rate's Kalshi/Polymarket-blended aggregator (the first
  genuinely post-FOMC-minutes snapshot obtained — see Standing Facts above)
  rather than a CME-attributed figure specifically — no fresh CME-attributed
  citation was sought this edition either. Keep treating CME FedWatch as
  needing a disclosed range from secondary sources, not a single figure.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, 23-35, 37 and **38** (not attempted at edition 36) — a confirmed
  structural gap, not transient. **The failure mode changed at edition 38**:
  prior editions consistently got a "Vercel Security Checkpoint" page;
  edition 38's attempt instead returned a plain HTTP 429 (Too Many Requests)
  — same practical outcome (no usable data), but worth tracking whether this
  is now the new standing failure mode or just session-to-session variance.
  Resume the attempt-every-edition discipline at edition 39. Use Kalshi's own
  secondary reporting (its blog, prediction-market news aggregators —
  news.kalshi.com, or DeFi Rate's own Kalshi/Polymarket-blended aggregator,
  which has now worked cleanly at editions 37 and 38) as the workaround in
  the meantime.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has failed many
  editions running; not re-attempted at editions 35 through 38 (went straight
  to the Westmetall fallback per standing practice). Westmetall.com has now
  worked cleanly **seventeen editions running** as the fallback (copper
  +0.11% to $14,526.00/tonne cash settlement at edition 38, reconciling
  exactly against edition 37's logged $14,510.00). A standalone Investing.com/
  oilprice.com/TradingEconomics-derived Brent/WTI page continues to work as a
  level-confirmation route, **but the oil level-vs-%-change-reconciliation
  pattern recurred again at edition 38, now a well-established, durable
  feature of oil sourcing specifically (see Hard Rules above) — always
  reconcile the %-change against the logged prior close rather than trusting
  any single vendor's self-stated change, on every edition going forward.**
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) has
  historically been preferred since TextView carries a known
  maturity-column mis-mapping bug, but edition 36 found a sharp 33bp
  disagreement between the two specifically on the 2-year. **Both endpoints
  have now agreed cleanly for three straight editions (36's fix confirmed at
  37, reconfirmed again at 38: 2-yr 4.75%, 10-yr 5.22%, 30-yr 5.60%, all Oct
  8, with Oct 7's logged 4.77%/5.28%/5.67% also matching exactly)** — treat
  the 33bp gap as resolved/noise, but keep fetching both endpoints and
  comparing rather than trusting either by default, since the gap has
  appeared once already without warning. Yield moves at edition 38 were a
  modest curve-wide decline (2-yr -2bp, 10-yr -6bp, 30-yr -7bp) after an
  intraday spike reversed by the close per AP's own narrative.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. The most recent full report (posted Friday 2
  October 2026, covering Tuesday 29 September 2026 data) remained the current
  one through edition 38 — re-confirmed directly against cftc.gov's own
  release-schedule page that no fresher report had posted as of Thursday
  evening 8 October. **The next report is due Friday 9 October 2026,
  covering Tuesday 6 October data — this now falls squarely inside edition
  39's window.** Check cftc.gov first thing and pull OI/gross-long-short for
  ES, NQ and RTY (plus the CFE legacy report for VIX futures) — this is a
  near-certain fresh-data opportunity for edition 39's chart #2 if it's a
  Monday/weekend-window edition per standing guidance.
- **GBP/USD and EUR/USD clean close:** both have now been fully resolved
  since edition 37 (EUR/USD since edition 26) — **edition 38 found no
  conflict on either pair using the standard four/three-source method**
  (Pound Sterling Live close-to-close history, live quotes, TradingEconomics).
  Treat both as closed for now; if a fresh conflict appears, repeat the same
  multi-source close-to-close-history method rather than relying on a single
  live quote.
- **Gold/silver clean close on a non-event day:** USAGOLD's own history pages
  have now 403'd or returned empty JS-only content for **four editions
  running (35 through 38)** — edition 38 tried three genuinely different URL
  paths (homepage, /daily-gold-price-history/, /futures-charts/) and all
  failed. **Try a fundamentally different access pattern at edition 39** — a
  cached/archived version (e.g. a web archive snapshot) rather than another
  live URL path on the same site, since four different live-URL attempts
  across two editions have now all failed identically. Kitco continues to
  work cleanly (spot gold and spot silver both fetched without issue at
  edition 38); gold futures continue to source cleanly via Investing.com.
  Silver's sign conflict (live since edition 31) has now stayed resolved for
  seven straight editions (32-38).
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month, but **edition 38 found September's release had not posted as of
  cutoff, and the release date itself is now in dispute** (one secondary
  source cites 14 October against the usual pattern) — see Standing Facts
  above, this is now an open thread for edition 39, not a routine calendar
  check. **US import/export prices and industrial production:**
  frequently release mid-month on a Mon/Tue — confirm on the BLS/Fed release
  schedule rather than assuming a date; **BLS's own schedule gives: Sept CPI
  Wed 14 Oct 8:30am ET** (re-confirmed via a direct bls.gov fetch at edition
  38), **Sept PPI Thu 15 Oct 8:30am ET, Import/Export Price Indexes Fri 16
  Oct 8:30am ET** (both carried forward from edition 37's direct fetch, not
  freshly re-touched at edition 38 — a direct fetch of the specific schedule
  subpage 404'd this round), **Q3 Employment Cost Index Fri 30 Oct 8:30am
  ET** (re-confirmed via a direct bls.gov fetch at edition 38). **FOMC
  minutes from the 15-16 September meeting are a closed thread** (see
  Standing Facts above). **US August 2026 trade deficit (BEA) widened to
  $132.6bn, released Tuesday 6 October** — the headline direction is
  reasonably solid but the precise July baseline used by secondary sources
  was internally inconsistent across outlets ($118.9bn vs. $88.6bn) and was
  not resolved — treat the exact consensus comparison with caution if
  revisited; not revisited at edition 37 or 38.
- **Henry Hub natural gas:** the October contract thread resolved at edition
  32 (final settlement $3.00/MMBtu). The November contract failed to yield a
  confirmed CME end-of-day settlement for five straight editions (33-37), but
  **edition 38 produced the cleanest read in many editions**: Investing.com
  and TradingEconomics both specified the contract month explicitly (November
  2026, ticker NGX6) and agreed closely (approx. $3.136/MMBtu, approx.
  -1.07%), with no "unofficial pricing" disclaimer on either source. **Still
  not labeled as an official CME settlement print by either vendor, so it was
  reported in the main text with that caveat rather than as a fully resolved
  settlement** — but this is a meaningfully better read than prior editions.
  Watch at edition 39 whether this data-quality improvement persists (if so,
  consider promoting the Investing.com+TradingEconomics convergence to the
  standing default method for Henry Hub rather than only a periodic check) or
  reverts to the prior pattern of implausible/unconfirmed aggregator reads.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. Not attempted at editions 33 through
  38 (secondary priority; options-flow colour has instead been sourced from
  dedicated options-flow wires or zerogex's broader snapshot). Edition 38
  found no notable single-stock options-flow/skew commentary dated to its
  session despite targeted searches on Applied Digital and AMD specifically
  — don't force this sub-item if nothing turns up, consistent with the
  derivatives section's own secondary-priority weighting.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable through edition 38;
  next due approx. 14 November 2026.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22). Not attempted again
  through edition 38.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov. Repeat this full
  three-instrument fetch whenever a fresh CoT-based chart is next used —
  **likely edition 39 itself, given the Friday 9 Oct report due date now
  falls inside its window** — watching for the Micro-vs-full-size Russell
  naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 37 hit the
  most extreme version yet: no analyst-action roundup for any name could be
  located at all. **Edition 38 hit a milder version of the same gap**: only
  the session's own biggest earnings mover (Applied Digital) had any dated
  analyst price-target activity (Needham, Wells Fargo, both tied directly to
  the earnings release); no roundup for any other name was found. This is
  now looking like the more common outcome across recent editions, not a
  rare one — report the rating direction and firm with confidence when
  something is found; treat a missing dollar target, unclear dating, or a
  total/near-total absence of any roundup as a normal gap to flag, not
  something to chase indefinitely.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29, recurred with milder
  versions through edition 36). Editions 37 and 38 did not hit a new instance
  of this specific trap — all of edition 38's named movers (AAOI, COHR, LITE,
  APLD, CAT, STZ) were corroborated across at least two independent sources
  each (stockanalysis.com plus a dated news article or company filing). The
  right call when time-constrained remains: corroborate with a second source,
  report the move without the unverified driver, or flag it as unverified in
  Annex A — never invent or infer a plausible-sounding explanation to fill
  the gap.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. `figsize=(9.8, 1.95)` for
  BOTH chart 1 (movers) and chart 2 (an 11-category sector-ETF-proxy panel) —
  **this supersedes the previous `(9.8, 1.55)`–`(9.8, 1.75)` guidance for
  panel2, which produced overlapping y-axis labels when actually rendered and
  inspected at edition 37 (see Hard Rules above for the full writeup);
  edition 38 reused `(9.8, 1.95)` for an 11-category panel2 and confirmed it
  again rendered cleanly with no overlap.** Use `font.size 9.6`, dpi 210,
  `width:100%` in the page. A shorter-category-count chart2 (e.g. 7-8 rows,
  such as a CFTC positioning chart) may still be fine at 1.55-1.75in — but
  **always render and visually inspect (via the Read tool) the actual PNG at
  or near full resolution before embedding it**, regardless of what a past
  edition's page-count success might suggest; a layout failure in chart2
  specifically does not show up in the page-count check, only in the
  rendered image itself. For a grouped (multi-series) bar chart, such as
  edition 34's CFTC Asset-Manager-vs-Leveraged-Funds chart, the simple
  single-series `barh()` helper in `make_charts.py` doesn't apply — write a
  dedicated `grouped_bar()` function instead (vertical bars, two series per
  category, legend below the plot), watching for the legend-overlap and
  y-axis-label-clipping traps documented in earlier editions. **This is
  likely needed at edition 39 given the fresh CFTC CoT data expected.**
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
  `grep -c` will show 2 for a correctly-built document). A 5-page render is
  not always a stray break — editions 24, 28 and 33 all hit 5 pages with
  only the one correct pagebreak present; the cause was genuine copy
  overflow each time. **Editions 34 through 38 have all rendered clean at 4
  pages on the first (or near-first) attempt.** Always re-render and
  re-check the page count after each trim/pad round rather than guessing how
  much is enough.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. The Commodities & FX table has split cleanly
  across the page 2/3 boundary with no repeated header row in multiple
  recent editions (35 through 38) — plain-`<tr>` tables reflow across a page
  break safely; this is expected behavior, not a bug to fix.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  A visibly short page 3 has recurred at editions 25, 28, 32 and 36, each
  needing a genuinely additive fix (never a padding table that just repeats
  an existing table's rows). **Editions 37 and 38 both rendered clean at 4
  pages on the first attempt with page 3 filling comfortably from content
  alone — no padding or trimming needed, now two editions running.**
  Continue checking for both failure modes (short page 3, overflow) after
  every render regardless of recent-edition track record.

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
  doesn't fill the page. Needed at editions 25, 28 and 36 (the latter via a
  Treasury yield-curve table variant); not needed at most other editions,
  including 34, 35, 37 and **38**. Always re-render immediately after adding
  (or removing) any content to confirm the page count, rather than assuming a
  change is safe.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across thirteen eligible
editions, 25 through 38, with edition 34 the sole exception when fresher CFTC
data was available). Fresh CFTC CoT data on a Monday/weekend-window edition →
the ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart, normalized
as % of open interest — this materialized for the first (and so far only)
time at edition 34; editions 35 through 38 all had no fresh CoT data due and
correctly reverted to the sector-ETF-proxy default. **The next CFTC report
(due Friday 9 October, covering Tuesday 6 October data) will land inside
edition 39's window — check cftc.gov first thing and use the positioning
chart if it's available and edition 39 is a Monday/weekend-window edition.**
A single dominant earnings print with a clean, well-sourced
implied-vs-realized-move story → a three-bar implied/historical-average/
realized move chart (the historical-average leg has never actually been
sourced successfully). A genuine multi-sector broadening/deepening selloff
across consecutive sessions → the sector-ETF proxy rendered as a grouped
(day-over-day) bar instead of single-day. A holiday-window preview edition
with no fresher data → VIX futures term structure with event annotations.
When chart 1 (movers) already covers the earnings/single-name story, the
sector proxy (or, when fresh, the CFTC positioning chart) is a good
complementary choice even on a stock-heavy day, since the two stories
reinforce rather than duplicate each other. Chart #2's placement in the
document should follow its content, not a fixed section — edition 24 and
edition 34 both placed a CFTC/positioning chart #2 in Section 5
(Derivatives) rather than Section 2; editions 35 through 38, all back on the
sector-proxy default, placed it back in its usual Section 2 spot. Continue
checking CoT freshness first each Monday/weekend-window edition rather than
assuming either chart type is now the permanent default for that edition
type. **Remember the figsize fix above (`(9.8, 1.95)` for an 11-category
panel) regardless of which chart type is chosen.**

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–35 (condensed):** established the format (edition 1 baseline;
edition 2 revised weighting/sourcing; edition 3 fixed the ET-cutoff math);
corrected the Fed Chair premise to Kevin Warsh at edition 6 (re-verified
every edition since); tracked the Jackson Hole keynote (28 Aug, hawkish) and
the resulting rate-odds repricing through editions 10–18; resolved the
SPDR-sector-ETF-proxy and CBOE-feed sourcing techniques at editions 10–11;
corrected the FOMC decision date to Wednesday 16 Sept at edition 18. Major
single-name events across editions 1-21: Moderna's melanoma-data
spike/unwind, Nvidia's Q2 FY27 beat/Hugging Face acquisition,
Walmart/Advance Auto Parts/Deere earnings, the PayPal-Stripe deal collapse,
California SB 492 hitting utilities, an Iran/Hormuz escalation cycle
repeatedly driving oil, Lululemon's guidance-slash collapse, Canada's approx.
$27.6bn retaliatory tariffs, Apple's first Ternus-era product event,
Oracle's Q1 FY27 vol-crush beat, the Fed debate flipping from "hold vs. cut"
to "hold vs. hike" on hot core CPI, and Anthropic CEO Dario Amodei's
AI-safety essay driving a chip-selloff/cybersecurity rotation. **The Sept
15-16 FOMC meeting and its aftermath (editions 21-23):** S&P 7,585.73
pre-decision; the Fed hiked 25bp to 3.75%-4.00% unanimous 12-0, equities
reversed hard (S&P 7,551.81, 10-year first closed above 5% since 2007); then
a sharp relief rally (S&P 7,637.76 +1.1%), BoE held at 3.75% (6-3). Edition
24 (triple witching + weekend): approx. $7tn September triple-witching
notional expired, Xenon Pharmaceuticals -30.7%, Buffett stepped down as
Berkshire chairman, BoJ hiked to approx. 1.25% (31-year high). Edition 25: a
broad chip rally pushed Nasdaq to a then-record 27,122.09; quarterly index
rebalances took effect. Edition 26: financials-led rotation, Viking
Therapeutics +35.67%, a genuine Kitco-vs-USAGOLD gold split (later
resolved). Edition 27: risk-off on a 19-year 10-year yield high, the "Meta
Muse" AI-agent theme rotated from banks into online travel names, VIX 15.18.
Edition 28: a whipsaw near-flat session, MGM Resorts -10.99% on a withdrawn
take-private bid, the Trump-Xi summit extended the US-China trade truce.
Edition 29: a relief rally, Meta -3.33% on the Cambridge Analytica verdict,
the US-China $30bn tariff-cut agreement first reported, zerogex's first
anomalous gamma jump. Edition 30: broad risk-off on a rejected Iran Hormuz
offer, Kodiak Sciences +177.96% (the movers-chart capping rule's first
genuine case), MongoDB -18.46%. Edition 31: DXY-vs-FX-crosses conflict
resolved cleanly; zerogex -$17.19bn. Edition 32: a volatile round-trip
close, Liquidia -57.19%, Micron beat with a muted AH reaction, gold
spot/futures split (later converged). Edition 33: yields (not equities)
drove the session on a hot ISM Prices Paid print, Accenture +15.78% and
Synopsys +12.78% led an AI-infra earnings cluster, Nike missed FQ1 guidance
(resolved edition 34); the document overflowed to 5 pages, needing five trim
rounds. Edition 34 (Mon 5 Oct, covering Fri 2 Oct + weekend): a badly-missed
September jobs report (nonfarm payrolls +29,000) drove a broad risk-on
rally and a sharp October-hike-odds collapse (to approx. 17-21.6%); S&P 500
+0.73% to 7,722.72; a fresh CFTC CoT report gave the first fully-consistent
ES/NQ/RTY OI normalization, powering a CFTC-positioning chart #2; zerogex
flipped decisively positive (+$22.96bn from -$11.58bn). Edition 35 (Tue 6
Oct, covering Mon 5 Oct): two same-day cash buyouts drove the tape
(Schneider Electric/PTC Inc, C.H. Robinson/RXO Inc) — PTC +33.49%, RXO
+22.54%; equities extended Friday's rally to a Nasdaq Composite record
(27,477.31); September's ISM Services PMI printed 54.9% with a hot 74.0%
Prices Paid sub-index driving the 10-year to a fresh 24-year high near
5.35%; two new sourcing traps logged (stale Nike price-target recirculation,
the Paramount Skydance stock-split "+96%" artifact); zerogex roughly doubled
to +$46.35bn. Edition 36 (Wed 7 Oct, covering Tue 6 Oct): equities extended
Monday's rally to fresh records with no single dominant catalyst (S&P 500
+0.58% to 7,818.93, Nasdaq +0.45% to 27,599.79, Dow +0.49% to 51,521.28) on
falling yields driving a clean rate-sensitive rotation (Utilities +2.98%
led, ten of eleven sectors green), though Russell 2000 bucked the trend
(-0.59%); Constellation Energy +12.25% on a reported Google nuclear PPA
(terms unconfirmed), AMD +2.80% to a fresh all-time high; two severe
sourcing traps hit (fabricated AMD price targets from a tool-summarized
fetch, an unverifiable "WHO" claim cited as the Novavax/Moderna driver,
both rejected); the Paramount Skydance/Warner Bros. Discovery $110bn merger
closed, renaming to Skydance Corporation under ticker SKYD with no reliable
same-day % figure obtainable given the ticker change (resolved the next
session); a secondary source reversed the US-China tariff list-size
assignment (resolved edition 37); the 2-year Treasury hit a 33bp
cross-endpoint gap (resolved edition 37); GBP/USD hit a genuine three-way
conflict (resolved edition 37); zerogex's SPX gamma hit a third consecutive
sharp step-up to +$74.26bn (reversed edition 37); BoJ's primary PDF was
located but unparseable by fetch tooling for a second straight edition
(resolved edition 37 via local text-extraction).

**Edition 37 (condensed)** — Thursday 8 October 2026 report covering
Wednesday 7 October 2026, the window's one NYSE session. The FOMC minutes
(released 2:00pm ET squarely inside the window) showed a unanimous 12-0
September hike but only "most" not "all" backing a further 2026 move,
closing the standing top-open-item from edition 36. Equities retreated
broadly on a bond-market selloff: S&P 500 -0.2% to 7,801.77, Dow -0.7% to
51,179.87, Nasdaq Composite -0.2% to 27,538.69, Russell 2000 -1.3% to
2,793.20; ten of eleven SPDR sectors closed lower, Industrials (-2.18%) led
on an unexplained Caterpillar -5.75% (driver resolved edition 38 — a joint
FTC/USDA farm-equipment antitrust inquiry), Health Care (+1.03%) the lone
gainer. Skydance Corporation's first clean post-transition close under
ticker SKYD was -6.72%; Applied Digital -6.04% intraday ahead of an
after-the-close fiscal Q1 beat (revenue +322% y/y); the AI-optics trade
(AAOI, COHR, LITE) reversed Tuesday's rally with no fresh catalyst found (a
pattern that extended into edition 38); Constellation Brands +2.35% on an
FY2027 guidance raise. No Wednesday-dated analyst roundup could be located
at all. A primary-source breakthrough on the Bank of Japan: its own Sept 18
decision PDF, downloaded directly and run through `pdftotext` locally,
revealed the hike passed 7-2 (not unanimous), with two named dissenters.
Three standing conflicts were all resolved this edition: the US-China
tariff list-size assignment (confirmed 77 US/1,619 China via a direct
whitehouse.gov fetch), the 2-year Treasury's 33bp cross-endpoint gap (both
endpoints agreed at 4.77%), and GBP/USD's three-way conflict (four sources
converged on 1.3213, -0.47%). WTI and Brent both hit a sharp
level-vs-%-change reconciliation failure across three independent vendors
(resolved by computing off the logged prior close — a pattern that recurred
again at edition 38). DXY +0.42% was consistent with EUR/USD and GBP/USD but
not USD/JPY (essentially flat), the same cross breaking the pattern as
edition 36. CBOE gave a tenth consecutive clean sweep (VIX 15.08, +0.47%);
VIX9D inversion widened further to -3.30 (later narrowed at edition 38).
zerogex's SPX dealer gamma broke its three-session sharp-step-up streak,
pulling back 22% to +$57.61bn. No new CFTC CoT report was due. SOFR 3.90%. A
genuine chart-layout bug was found and fixed: panel2's figsize bumped from
`(9.8, 1.55)` to `(9.8, 1.95)` after overlapping y-axis labels were caught on
visual inspection. 31 sources, clean 31/31 on the second `check_refs.py`
pass, zero stray tildes, clean 4-page render on the first attempt.

**Edition 38 (most recent — full detail)** — Friday 9 October 2026 report
covering Thursday 8 October 2026, the window's one NYSE session, research
window Wed 7 Oct 2026 20:00 ET through Thu 8 Oct 2026 20:21 ET. Verified the
two structural header rules again — now clean across ten consecutive
single-session or single-session-plus-weekend editions (29-38).

Equities fell for a second straight session but breadth stayed strong: S&P
500 -0.5% to 7,765.36, Dow +0.1% to 51,231.64 (the only major average
higher), Nasdaq Composite -1.3% to 27,193.34, Russell 2000 effectively flat
(+0.03% to 2,794.13) — confirmed via AP's wire (through a La Nación
syndication mirror) and cross-checked against ETF proxies, with the
Wednesday-to-Thursday arithmetic reconciling exactly against the prior
edition's logged closes. Eight of eleven SPDR sectors closed green;
Technology (-1.79%) was the sole sector drag of real size as a second
straight session of AI-optics profit-taking (Applied Optoelectronics
-13.58%, Coherent -9.63%, Lumentum -5.62%, all attributed by a 24/7 Wall St.
report to broad profit-taking against outsized 2026 gains rather than any
new catalyst) extended Wednesday's reversal; Energy (+2.97%) and Consumer
Staples (+2.11%) led gainers. Caterpillar's Wednesday -5.75% mystery
(unresolved at edition 37) was resolved: a joint FTC/USDA inquiry into
farm-equipment dealer practices launched Wednesday, hitting CAT, DE, AGCO
and CNH broadly — CAT extended the move Thursday, -2.17% to $796.18.
Applied Digital's blowout fiscal Q1 print (revenue +322% y/y, released
Wednesday after close) drew a muted +0.17% stock reaction despite a wide
GAAP loss; analysts split on price targets (Needham cut to $70 from $83,
Wells Fargo raised to $55 from $50); a separately-cited non-GAAP EPS figure
conflicted with the 8-K's GAAP numbers and was excluded (a new trap, see
Hard Rules). Constellation Brands extended its post-guidance-raise strength
for a second session, +4.43% to $123.63. No Thursday-dated analyst-action
roundup beyond the APLD price-target changes could be located — a second
consecutive edition with this gap.

The first Fed-odds reading obtained after Wednesday's 2:00pm ET FOMC-minutes
release (DeFi Rate's Kalshi/Polymarket-blended aggregator, snapshot Thursday
8:19pm ET) showed October hike odds approx. 16-17% and December approx.
74-76% — essentially unchanged from the pre-minutes range, closing the "top
open item" flagged at edition 37. Kalshi's direct fetch remains blocked, now
returning HTTP 429 rather than the earlier Vercel checkpoint page. Thursday's
initial jobless claims came in at 197,000 (week ended Oct 3); no consensus
could be sourced. Standing facts reconfirmed: Kevin Warsh as Fed Chair
(direct federalreserve.gov fetch); next FOMC Oct 27-28; no US shutdown,
funded through Dec 11 2026 (via two secondary sources this round, not a
direct whitehouse.gov fetch). A primary-source breakthrough closed the Bank
of Japan's last standing secondary-only gap: its own MPM schedule page
confirms the next meeting is Oct 29-30, 2026. China's September CPI/PPI had
not posted as of cutoff; the release date itself is unresolved (secondary
sources split between the usual 9th-10th pattern and Oct 14).

Oil posted its sharpest move in several editions — WTI approx. +2.3% to
$91.16, Brent approx. +3.1% to $104.28, with AP's own wire separately noting
Brent "topped $104" intraday — but vendors' own stated %-changes again
failed to reconcile against the logged prior close, a pattern now recurring
for three-plus sessions on oil specifically; the changes above were computed
off the trusted baseline instead, and the session's specific catalyst could
not be pinned down. Gold and silver both sourced cleanly with no sign
conflict (gold spot +0.30% to $4,145.10, silver spot +0.69% to $59.47);
copper +0.11% to $14,526.00/tonne. DXY was successfully 3-source
corroborated for the first time in several editions (approx. -0.02% to
102.10); USD/JPY diverged from DXY's direction for a third consecutive
session, reinforcing the case this is a USD/JPY-specific dynamic. Henry
Hub's November contract gave its cleanest read in many editions (contract
month specified, two sources agreeing closely at approx. -1.07%), though
still not labeled an official settlement. Treasury yields eased across the
curve (2-year -2bp to 4.75%, 10-year -6bp to 5.22%), both CSV and TextView
endpoints agreeing. USAGOLD remained inaccessible for a fourth straight
edition across three different URL paths tried.

CBOE gave an eleventh consecutive clean sweep (VIX 15.41, +2.19%; VIX9D
12.21; VIX3M 18.08; VIX6M 20.04; VVIX 87.66; SKEW 149.19, though SKEW's flat
OHLC suggested a thin/single print). The VIX9D-vs-VIX inversion narrowed to
-3.20 from -3.30, breaking a multi-session widening trend for the first
time. zerogex's dealer-gamma reads carried unusual internal inconsistencies
this session: SPX's own page disclosed a stale/delayed-snapshot caveat for
its approx. +$22.56bn read (down from +$57.61bn); SPY's +$246.9mn was
roughly 24x smaller than Wednesday's +$5.91bn with no clear explanation;
QQQ showed two conflicting figures for the same metric on the same page —
all three stayed directionally net positive-gamma despite the data-quality
concerns, reported with explicit caution (a new data-quality trap, watch for
recurrence). No new CFTC CoT report was due (next due Friday 9 Oct, covering
Tuesday 6 Oct data — will land inside edition 39's window). SOFR eased 2bp
to 3.88% (Oct 7, one-day lag). 28 sources, clean 28/28 on the second
`check_refs.py` pass (three Annex B entries were initially uncited in the
day-ahead table, fixed immediately), zero stray tildes, clean 4-page render
on the first attempt.

**Open threads for edition 39:** The next CFTC CoT report is due Friday 9
October (covering Tuesday 6 Oct data) and falls squarely inside edition 39's
window — **check cftc.gov first thing**; pull a fresh ES/NQ/RTY
Asset-Manager-vs-Leveraged-Funds normalization and use it as chart #2
(Section 5 placement per prior CFTC-chart editions) if edition 39 is a
Monday/weekend-window edition per standing guidance. The WTI/Brent
vendor-baseline reconciliation gap is now a well-established, durable
pattern (editions 35, 37, 38) — continue computing changes off the logged
prior close every edition by default, not just when something looks
surprising. DXY-vs-USD/JPY divergence has now recurred three consecutive
editions (36, 37, 38) — treat as an increasingly likely structural/BoJ-
policy-related feature rather than independent noise each time; if it
recurs a fourth time, the framing can graduate from "worth watching" to
"expected by default." zerogex's edition-38 data-quality issues (SPX
stale-snapshot caveat, SPY 24x scale discontinuity, QQQ internal figure
conflict) need a clean-or-not check at edition 39 to determine whether this
was a one-off site glitch or a recurring issue worth formally documenting
alongside the CBOE feed's known bugs. The VIX9D-VIX inversion narrowed for
the first time (edition 38, to -3.20 from -3.30) after a multi-session
widening trend — watch whether this is a reversal's start or a one-session
blip. Henry Hub's unusually clean edition-38 read (contract month specified,
two sources agreeing) should be checked for persistence — if clean again,
consider promoting it from a periodic check to the standing default method.
China's September CPI/PPI had not released as of edition 38's cutoff and its
expected release date is itself disputed (9th-10th vs. 14th) — check
stats.gov.cn directly at edition 39 rather than assuming either date.
Thursday's oil-price catalyst was never pinned down — if a delayed
explanation surfaces (as happened with Caterpillar's driver between editions
37 and 38), revisit. Applied Digital's non-GAAP EPS figure (+1¢ vs. a -30¢
consensus, from TheFly) remains unreconciled against the GAAP 8-K figures —
leave excluded unless a credible methodology explanation surfaces.
Constellation Brands' precise Q2 actual EPS/revenue vs. consensus remains
unresolved across conflicting secondary sources — revisit only if
load-bearing. USAGOLD's history pages have now failed across four straight
editions and multiple distinct URL paths — try a genuinely different access
pattern (e.g. a web-archive snapshot) at edition 39 rather than another live
URL on the same site. Kalshi's direct-fetch failure mode changed from a
Vercel checkpoint page to a plain HTTP 429 at edition 38 — note whether this
persists. The Bank of England's Thursday 5 Nov decision was not freshly
re-touched at edition 38 (deprioritized that round) — resume direct
bankofengland.co.uk reconfirmation once the meeting is inside roughly a
one-week window. TSMC's Oct 15 earnings call (approx. 2:00am ET, consensus
revenue approx. $45.8bn / EPS approx. $4.39) and the New Mexico v. Meta
penalty ruling (expected approx. 20 Oct, state seeking $35-40bn vs. Meta's
proposed $3.45bn cap) remain the next flagged catalysts — watch for
developments. Threads closed after resolution rather than carried further:
the BoJ next-meeting-date primary-sourcing gap (closed via a direct
boj.or.jp schedule-page fetch); Caterpillar's Wednesday driver (closed via a
dated FTC/USDA farm-equipment-inquiry article); the post-FOMC-minutes
Fed-odds reading (closed, first obtained edition 38); the US shutdown/CR
status (reconfirmed via secondaries, unchanged).
