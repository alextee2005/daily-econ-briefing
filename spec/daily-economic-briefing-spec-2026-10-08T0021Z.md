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
  through 37 have all applied this correctly** ("Friday 2 October 2026,"
  "Monday 5 October 2026," "Tuesday 6 October 2026," "Wednesday 7 October
  2026" and "Thursday 8 October 2026" respectively as the date line, with the
  window line carrying the session(s) covered) — now confirmed stable across
  five consecutive editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 37 all reused the
  same pattern for single-session windows — now confirmed clean across nine
  consecutive single-session or single-session-plus-weekend editions (29
  through 37). No further confirmation needed; treat this as settled.

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
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 37
  directly against federalreserve.gov's own FOMC calendar page
  (federalreserve.gov/newsevents/2026-october.htm). The meeting is now about
  three weeks out — continue re-confirming every edition between now and then.
  Decision and press conference both land 28 Oct, 2:30pm ET.
- **October-hike odds: a fresher (though still pre-minutes) reading was found
  at edition 37** via DeFi Rate's Kalshi/Polymarket-blended aggregator:
  October 27-28 hike odds approx. 16-18% (Polymarket approx. 17%, Kalshi
  approx. 18.5%), dated Oct 2-4 snapshots — essentially unchanged from edition
  35/36's carried-forward approx. 16.5-23% range, just narrower. **December
  8-9 hike odds: approx. 72%** (DeFi Rate's Kalshi-sourced figure, same Oct
  1-4 window), within edition 35/36's logged approx. 65-75% range. **Critical
  caveat, the single most important open item for edition 38: no reading
  POST the 2:00pm ET Wednesday 7 Oct minutes release was found at edition
  37** — every cited figure above predates the minutes. The minutes read as
  hawkish-but-cautious (unanimous Sept hike, but only "most" not "all" backing
  a further 2026 move) — a fresh post-minutes market snapshot is needed to see
  whether this shifted pricing. Make this the first search of edition 38.
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
  Board of Governors bios page; editions 35, 36 and **37 all re-confirmed the
  same page again — still Kevin Warsh, unchanged, now five straight direct
  re-confirmations.** The BoE and shutdown/CR open gaps flagged at edition 35
  were closed at edition 36 via direct primary-source fetches
  (bankofengland.co.uk, whitehouse.gov) and **both facts were re-confirmed
  again at edition 37 with no change.** **The BoJ primary-source gap (two
  straight editions of secondary-only sourcing on the Sept 18 decision) was
  finally closed at edition 37**: the decision PDF
  (boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260918a.pdf — note this is the `a`
  suffix, not the `b` suffix tried at edition 36) was downloaded directly and
  run through `pdftotext` locally, since WebFetch's own HTML-conversion path
  still fails to parse this specific PDF. **This is a reusable technique for
  any future BoJ-PDF (or similar stubborn-PDF) parsing failure: download the
  raw file and extract text locally rather than relying on the fetch tool's
  built-in conversion.** The primary document revealed the September hike
  passed **7-2, not unanimously as had been assumed by default** — see the
  BoJ entry below for the vote detail. The BoJ's *next meeting date* (Oct
  29-30, 2026) remains secondary-only for a third straight edition; try the
  same local-PDF-extraction technique on BoJ's calendar page (or its
  publication list) at edition 38 rather than repeating the same failing
  WebFetch call.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed again at
  edition 37 via bankofengland.co.uk. No further confirmation needed until
  closer to the 5 Nov decision.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high. **New at edition 37, now primary-
  sourced for the first time: the vote was 7-2, not unanimous.** Dissenters
  Asada Toichiro and Sato Ayano both preferred holding — Asada cited core CPI
  still below the 2% target ("it could not necessarily be said that the
  economic situation was strong"), Sato cited price/economic developments
  that "did not appear to have substantially accelerated." Voting for:
  Governor Ueda Kazuo, Himino Ryozo, Uchida Shinichi, Takata Hajime, Tamura
  Naoki, Koeda Junko, Masu Kazuyuki. The BoJ's outlook language retains a
  tightening bias: underlying CPI inflation is described as "approaching 2
  percent" and expected to "accelerate to a level clearly above 2 percent
  from the second half of fiscal 2026," with further hikes conditional on
  data. **The Bank of Japan's next policy meeting is believed to be October
  29-30, 2026** but this specific date remains secondary-sourced only (Nation
  Thailand, Free Press Journal, investinglive.com, financecalendar.com) for a
  third edition running — the September *decision* itself is now primary- 
  sourced (see above), but the primary calendar page with the *next* meeting
  date has not yet been successfully fetched. Try the local-PDF/text-
  extraction technique on BoJ's own calendar or publications-schedule page at
  edition 38.
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
- **No US federal government shutdown is in effect — re-confirmed again at
  edition 37 via a direct whitehouse.gov fetch** (briefing statement on H.R.
  6500, the Continuing Appropriations and Extensions Act, 2027): signed into
  law 2 September 2026, funds the government through **11 December 2026**.
  Watch for shutdown risk resurfacing as 11 December 2026 approaches. The
  generic "Government Shutdown Clock" page with stale/inconsistent content
  (flagged at edition 35) was not encountered again at edition 36 or 37.

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
  uniqueness of use (editions 33-37 have all done this for stockanalysis.com
  single-stock closes, confirmed stable across five editions).
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
  Editions 35, 36 and 37 all reverted to the sector-ETF-proxy default (no
  fresh CoT data due in any of those three editions) and kept it in its
  default Section 2 placement — use Section 5 placement again whenever a
  future CFTC-positioning chart #2 recurs.
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
  **Editions 27 through 37 are all clean counter-examples worth keeping in
  mind**: all eleven posted a usable AP wire eventually. **Edition 37 is a
  useful cautionary tale about method, not about the source itself**: a
  general-purpose WebSearch AI-summary returned the correct AP figures
  (S&P 7,801.77 -0.2%, Dow 51,179.87 -0.7%, Nasdaq Composite 27,538.69 -0.2%,
  Russell 2,793.20 -1.3%) attached to a *guessed* wtop.com URL, and the
  research subagent — correctly following the standing caution about
  AI-summarized fetches inventing numbers — could not independently
  corroborate it and flagged it as possibly fabricated, excluding the point
  levels from its report. **The lead/writer step then directly re-fetched
  the real wtop.com article plus a second independent AP syndication mirror
  (krmg.com) and got the exact same figures, confirming they were correct all
  along, not fabricated.** The lesson for edition 38 and beyond: the standing
  caution against AI-summary fabrication (edition 33, sharpened at edition 36
  with the fabricated AMD price targets) is about **unverified precision that
  conflicts with everything else** — a precise figure that *cannot yet be
  corroborated* is not automatically a fabrication, and the correct response
  is to attempt a direct, independent second fetch (ideally of the real URL,
  not a guess) before discarding it, not to assume bad faith by default. If
  time-constrained and a second fetch isn't feasible, excluding pending
  corroboration (as the subagent did) remains the right conservative call —
  just don't treat that exclusion as final if a follow-up verification pass
  has time to run. Always have Yahoo Finance + FRED/stockanalysis.com ready
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
  durable.**
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. **Similarly, a price level can be correct while a vendor's stated
  %-change is wrong** if the vendor used a different prior-day base — always
  sanity-check that a stated price and stated % change reconcile
  arithmetically against the prior session's logged close. This exact pattern
  has now recurred repeatedly on oil specifically: edition 35 hit it on WTI
  (used Investrade's internally-consistent figure over a non-reconciling
  second aggregator); **edition 37 hit a more severe version on BOTH WTI and
  Brent simultaneously** — three independent vendors (Investing.com,
  oilprice.com, TradingEconomics) all agreed closely on Wednesday's *price
  level* (~$89.0-89.1 WTI, ~$101.1-101.2 Brent) but none of their own stated
  %-changes (+0.8-0.9% WTI, +0.9-1.01% Brent) reconciled against Tuesday's
  logged closes ($89.97 WTI, $100.58 Brent) — all three vendors' own
  "previous close" baseline appears to differ from the one this report
  anchors to (likely a CFD/continuous-contract vs. official-settlement
  mismatch that recurs across vendors, not a single bad source). **Resolved
  by computing the change directly off the trusted logged prior-close instead
  of trusting any vendor's self-stated %** (approx. -1.0% WTI, approx. +0.55%
  Brent were used) — this is now a well-established, recurring pattern on oil
  specifically; always perform this reconciliation check on WTI/Brent by
  default, not just when something looks surprising. The oil
  contract-month-roll trap (Brent Nov-to-Dec) remains resolved; Brent's
  December contract was reconfirmed still front-month at edition 37 with no
  new roll (the hypothesized Dec-to-Jan roll around 31 Oct/1 Nov is not yet
  due). The CBOE vol-complex feed's two documented bugs (duplicate-
  `prev_day_close`, and `price_change_percent` dividing by current price
  instead of prior close) remain intermittent — **edition 37's direct fetch
  showed neither bug, a fourth consecutive clean read (35, 36, 37 plus the
  underlying pattern holds back further)** — always compute day-over-day %
  change manually as `price_change ÷ (current_price − price_change)` and
  treat the feed's own `price_change_percent` field as unreliable until
  checked each time regardless.
- **The DXY-vs-its-own-FX-crosses conflict** has now recurred, at least
  partially, in roughly half of all occurrences since edition 29 (resolved
  cleanly at 31, 33, 35; recurred at 32, 34, 36; **and recurred again,
  partially, at edition 37** — Wednesday's DXY rise (approx. +0.42%) was
  consistent with EUR/USD (-0.56%) and GBP/USD (-0.47%) both falling, but
  **USD/JPY was essentially flat (-0.016%) rather than falling** — the same
  specific cross (USD/JPY) that broke the pattern at edition 36 too, now two
  editions running. Treat a partial mismatch (one cross tracking, one or more
  not) as a normal, recurring outcome rather than an anomaly, and keep
  disclosing it explicitly every time. **Given USD/JPY has now been the
  specific break on two consecutive occasions, it may be worth treating
  USD/JPY as the structurally "noisiest" of the three crosses against DXY
  going forward** rather than treating each recurrence as independent —
  watch whether this continues at edition 38.
- **The same-day silver sign conflict first flagged at edition 31 has now
  stayed resolved for six straight editions (32-37)** — silver rose/fell
  consistently across spot and futures at every session in that span. Treat
  as closed unless a fresh mismatch appears.
- **GBP/USD's two-edition data-quality problem (a minor two-source gap at
  edition 35, a genuine three-way level/direction conflict at edition 36)
  appears resolved at edition 37**: a dedicated four-source check (Pound
  Sterling Live close-to-close history, XE.com mid-rate, Yahoo Finance,
  TradingEconomics) converged cleanly on 1.3213, -0.47% day-over-day, once
  the live-quote sources' "Thursday pre-market, previous-close-equals-
  Wednesday's-close" timing artifact was correctly identified and excluded.
  **Note this timing artifact for future editions: a live FX quote fetched
  near/after the NY 5pm close may reflect the *next* session's opening tick,
  with its own "previous close" already equal to the session just completed
  — don't mistake this near-zero "live" change for the day's actual
  close-to-close move. Use a dedicated close-to-close history source (Pound
  Sterling Live worked well) rather than a live snapshot when fetching this
  late in the window.**
- **The 2-year Treasury yield conflict from edition 36 (TextView 4.46% vs.
  CSV 4.79%, a 33bp gap) is resolved as of edition 37** — both the CSV
  endpoint and the TextView endpoint were fetched directly and returned
  identical figures (2-yr 4.77%, 10-yr 5.28%, both Oct 7) with no gap this
  time; re-checking Oct 6 through both endpoints also showed agreement
  (4.79%). Treat as resolved/noise unless a fresh conflict appears; if one
  does, the standing advice stands — dig into which endpoint is wrong via a
  market-wrap secondary cross-check for the specific disputed maturity.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 37 have all run clean (or
  clean after one quick fix) — edition 37 drafted 30/31 on the first pass
  (one Annex B entry, the Treasury-yields source, was defined but not yet
  cited inline), caught immediately by running the script, fixed by adding
  the missing `<sup class="ref">[28]</sup>` tag to the already-written
  Treasury-yields sentence in the Market recap section, then re-ran clean at
  31/31. Worth re-stating: table cells (and disclosure-box/tile-adjacent
  sentences) are a legitimate, already-used place to put a citation — use
  them rather than forcing an awkward prose mention just to attach a `<sup>`
  tag.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 37 have all rendered clean at zero tildes** on the
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
  charting "RTY." No new CFTC report was due within editions 35, 36 or 37's
  windows; the chart #2 slot reverted to the sector-ETF-proxy default each
  time accordingly.
- **A genuinely new chart-layout bug surfaced at edition 37, worth fixing
  permanently in `make_charts.py`'s documented defaults: the sector-ETF-proxy
  panel2 chart at `figsize=(9.8, 1.55)` with `tick_fs=7.6` and 11 categories
  produced visibly overlapping y-axis category labels** (confirmed by
  rendering and visually inspecting the PNG directly, not just trusting the
  matplotlib call succeeded) — the 1.55-inch height does not give 11 rows
  enough vertical room at that font size in this environment. **Fixed by
  bumping panel2's figsize to `(9.8, 1.95)`** (same height as the movers
  chart), which rendered cleanly with no overlap. This directly contradicts
  the previously-stated claim that "(9.8, 1.55)...continues to work cleanly
  with no layout issues" for the simple single-series `barh()` helper on an
  11-category sector panel — that claim was evidently never visually
  re-verified at full column width/11 rows in this exact environment, only
  assumed stable from page-count success. **Going forward: use `(9.8, 1.95)`
  as the default panel2 figsize for any 10-11-category sector-ETF-proxy
  chart, and always visually inspect chart2 (not just chart1) at full
  resolution before embedding it — a layout failure here was previously only
  being caught (if at all) by accident, not by a standing discipline.** If a
  future chart2 has fewer categories (e.g. a 7-8-row CFTC chart), 1.55-1.75in
  may still be fine — re-verify visually rather than assuming either figsize
  by default.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at editions 33 through 37 (edition 37: SKYD -6.72% vs. APLD -6.04%, about
  1.11x), all left uncapped. Edition 30 remains the one genuine 10x+ case to
  date (about 15x, capped at a fixed axis max of 30). No need to revisit the
  threshold or mechanism absent a genuinely new edge case (e.g. something in
  the 5-10x range).
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists** — confirmed again at edition 35 (four
  analyst actions all traced to one Benzinga/Yahoo roundup, disclosed as
  such). **Edition 37 hit the inverse problem: no analyst-action roundup for
  any name could be located at all for the session**, despite searching —
  disclosed explicitly in the body as a departure from most prior editions
  rather than silently omitted. Don't force an analyst-actions subsection
  with weak/uncorroborated content just because most editions have one;
  disclosing the absence is the correct move when a genuine search comes up
  empty.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. **Editions 28 through 37 all got a full clean sweep** — ten
  consecutive clean sweeps now, every series carrying a same-day
  `last_trade_time`, verified individually per series via a raw `curl`/direct
  fetch (not a tool-summarized fetch) each time. Still not a guarantee — keep
  checking `last_trade_time` on each series every time. The feed has two
  known intermittent bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) — **both have now been absent for three straight editions (35, 36,
  37)** — manual recomputation matched the feed's own stated percentages
  exactly each time. **Always compute day-over-day % change manually against
  the previous edition's logged close regardless.** The VIX9D-vs-spot-VIX
  front-end inversion (first flagged edition 28) has been on a broader
  widening trend with one pause (edition 35 narrowed to -2.67, edition 36
  resumed widening to -2.98, **edition 37 widened further to -3.30**) —
  continue reporting as a standing regime feature and watch each edition for
  whether it narrows, holds, or widens further; the pattern remains
  irregular, not monotonic in either direction, but has now widened in two
  of the last three editions.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table,
  and (absent fresher CoT data or another dominant story) chart #2. Editions
  35, 36 and 37 all had no fresh CoT data due and used the sector-ETF-proxy
  default (ten of eleven eligible editions now, the sole exception being
  edition 34's CFTC chart). **Stockanalysis.com single-stock pages remain the
  standing default for pinning an exact closing price/% change on any
  individual mover** — editions 26 through 37 (twelve straight) have all used
  direct fetches to it. Note that a headline wire's own GICS sector-index
  percentages can differ slightly from the SPDR ETF price-change figures (a
  normal index-vs-ETF-price methodology gap); keep using the SPDR ETF figures
  as the table's primary numbers.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available — not found at
  edition 37 either (ten of eleven sectors down made the pullback's breadth
  less ambiguous in prose anyway). Continue treating an uncorroborated
  single-aggregator (or unsourced search-summary) breadth figure as not
  usable — this has recurred enough times to treat as a durable, not
  occasional, gap.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — a recurring failure for many
  editions, not separately re-attempted at edition 37 (zerogex succeeded, per
  standing practice). **zerogex.io remains confirmed across eleven straight
  clean editions (27-37)**: after three consecutive sharp step-ups through
  edition 36 (+$22.96bn → +$46.35bn → +$74.26bn), **edition 37 broke that
  streak with a sharp pullback to +$57.61bn (-22% day-over-day)** — still
  solidly positive, plausibly tied to the FOMC minutes landing in the window,
  but the first reversal after three straight increases. SPY (+$5.91bn) and
  QQQ (+$116mn) net-GEX stayed positive too, consistent in direction with
  SPX. The magnitude remains single-sourced (zerogex only; SpotGamma still
  yields no real numbers to cross-check against). **Watch at edition 38
  whether the pullback continues, stabilizes, or whether Tuesday-Wednesday's
  step-up/step-down pattern was itself the anomaly** — the series has now
  shown both a 3x run-up and an immediate sharp reversal within the same
  five-session span, so neither direction should be assumed to persist by
  default. Minor open item carried forward, still low priority: zerogex's own
  stated wall levels (call/put wall) have still not been cross-checked
  against a secondary options note's implied walls.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Edition
  37 used DeFi Rate's Kalshi/Polymarket-blended aggregator snapshots (Oct 2-4
  dated, pre-minutes) rather than a CME-attributed figure specifically — no
  fresh CME-attributed citation was sought this edition. Keep treating CME
  FedWatch as needing a disclosed range from secondary sources, not a single
  figure.
- **Kalshi direct fetch:** rate-limited (HTTP 429, served a "Vercel Security
  Checkpoint" page) across every edition it has been attempted, 23-35 and
  **37** (not attempted at edition 36) — a confirmed structural gap, not
  transient. The attempt-every-edition discipline resumed at edition 37 and
  failed again identically; resume again at edition 38 so the streak count
  stays meaningful. Use Kalshi's own secondary reporting (its blog,
  prediction-market news aggregators — news.kalshi.com, or DeFi Rate's own
  Kalshi/Polymarket-blended aggregator, which worked cleanly at edition 37)
  as the workaround in the meantime.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has failed many
  editions running; not re-attempted at editions 35, 36 or 37 (went straight
  to the Westmetall fallback per standing practice). Westmetall.com has now
  worked cleanly **sixteen editions running** as the fallback (copper +0.03%
  to $14,510.00/tonne cash settlement at edition 37, reconciling almost
  exactly against edition 36's logged $14,505.00). A standalone Investing.com/
  oilprice.com/TradingEconomics-derived Brent/WTI page continues to work as a
  level-confirmation route, **but edition 37 hit the oil
  level-vs-%-change-reconciliation pattern in its most severe form yet
  (see Hard Rules above) — always reconcile the %-change against the logged
  prior close rather than trusting any single vendor's self-stated change,
  on every edition going forward, not just when something looks surprising.**
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) has
  historically been preferred since TextView carries a known
  maturity-column mis-mapping bug, but edition 36 found a sharp 33bp
  disagreement between the two specifically on the 2-year. **Edition 37
  fetched both endpoints directly again and found them in full agreement
  (2-yr 4.77%, 10-yr 5.28%, both Oct 7; re-checking Oct 6 also showed
  agreement at 4.79%)** — treat the 33bp gap as resolved/noise for now, but
  keep fetching both endpoints and comparing rather than trusting either by
  default, since the gap has appeared once already without warning. Yield
  moves at edition 37 were small and directionally mixed (2-yr -2bp, 10-yr
  +1bp, 30-yr +3bp) — a reminder that a muted yield move is a normal outcome
  too, not every session needs a "yields spike/dive" framing.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. The most recent full report (posted Friday 2
  October 2026, covering Tuesday 29 September 2026 data) remains the current
  one — editions 35, 36 and **37 all re-confirmed directly against cftc.gov's
  own release-schedule page** that no fresher report has posted. **The next
  report is due Friday 9 October 2026, covering Tuesday 6 October data** —
  this now falls inside whatever window edition 38 covers if its cutoff is
  Thursday 8 Oct evening or later; check cftc.gov first thing and pull
  OI/gross-long-short for ES, NQ and RTY (plus the CFE legacy report for VIX
  futures) if it has posted.
- **GBP/USD and EUR/USD clean close:** EUR/USD has been fully resolved since
  edition 26. **GBP/USD's two-edition data-quality problem (minor gap at
  edition 35, genuine three-way conflict at edition 36) is resolved as of
  edition 37** — see the dedicated Hard Rules entry above for the method
  (four independent sources, correctly excluding a "Thursday pre-market"
  timing artifact from live quotes) that resolved it. Treat GBP/USD as closed
  for now; if a fresh conflict appears, repeat the same four-source
  close-to-close-history method rather than relying on a single live quote.
- **Gold/silver clean close on a non-event day:** USAGOLD's own history pages
  have now 403'd for **three editions running (35, 36, 37)** — worth trying a
  genuinely different access pattern (a different URL path, or a cached/
  archived version) rather than repeating the same failing fetch a fourth
  time. **Kitco recovered at edition 37** after 404'ing at edition 36 — both
  spot gold and spot silver fetched cleanly this time, suggesting edition
  36's gap was transient rather than durable. Gold futures continue to source
  cleanly via Yahoo Finance/Investing.com agreement. Silver's sign conflict
  (live since edition 31) has now stayed resolved for six straight editions
  (32-37).
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month — due again around 9-10 October 2026, check if edition 38's window
  reaches that far. **US import/export prices and industrial production:**
  frequently release mid-month on a Mon/Tue — confirm on the BLS/Fed release
  schedule rather than assuming a date; **BLS's own October 2026 schedule
  page (bls.gov/schedule/2026/10_sched_list.htm) was fetched directly at
  edition 37 and gives: Sept CPI Wed 14 Oct 8:30am ET, Sept PPI Thu 15 Oct
  8:30am ET, Import/Export Price Indexes Fri 16 Oct 8:30am ET, Q3 Employment
  Cost Index Fri 30 Oct 8:30am ET** — use this page directly for US release
  dates going forward rather than secondary calendar aggregators where
  possible. **FOMC minutes from the 15-16 September meeting are now a closed
  thread** (see Standing Facts above). **US August 2026 trade deficit (BEA)
  widened to $132.6bn, released Tuesday 6 October** — the headline direction
  is reasonably solid but the precise July baseline used by secondary
  sources was internally inconsistent across outlets ($118.9bn vs. $88.6bn)
  and was not resolved — treat the exact consensus comparison with caution
  if revisited; not revisited at edition 37.
- **Henry Hub natural gas:** the October contract thread resolved at edition
  32 (final settlement $3.00/MMBtu). The November contract has now failed to
  yield a confirmed CME end-of-day settlement for **five straight editions
  (33-37)**, a durable, not occasional, gap. **Edition 37's periodic
  aggregator check returned an implausible reading again** (TradingEconomics,
  no contract-month specified, explicit non-official-pricing disclaimer,
  implied approx. +7.7% one-day jump from the $3.03 last logged at edition
  35) — excluded per standing policy. Continue the periodic-check cadence
  (not every edition) rather than reverting to attempting the CME settlements
  page each time, and continue excluding any aggregator figure that implies
  an implausible one-day jump or lacks contract-month/official-pricing
  specificity.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. Not attempted at editions 33 through
  37 (secondary priority; options-flow colour has instead been sourced from
  dedicated options-flow wires or zerogex's broader snapshot). Edition 37
  found no notable single-stock options-flow/skew commentary dated to its
  session at all — don't force this sub-item if nothing turns up, consistent
  with the derivatives section's own secondary-priority weighting.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable through edition 37;
  next due approx. 14 November 2026.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22). Not attempted again
  through edition 37.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov. Repeat this full
  three-instrument fetch whenever a fresh CoT-based chart is next used
  (likely edition 38 or soon after, given the Friday 9 Oct report due date),
  watching for the Micro-vs-full-size Russell naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** **Edition 37 hit
  the most extreme version yet: no analyst-action roundup for any name could
  be located at all**, not even a single-aggregator one — disclosed
  explicitly in the body rather than omitted silently. Report the rating
  direction and firm with confidence when something is found; treat a
  missing dollar target, unclear dating, or (as at edition 37) a total
  absence of any roundup as a normal gap to flag, not something to chase
  indefinitely.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29, recurred with milder
  versions through edition 36). Edition 37 did not hit a new instance of this
  specific trap, but continued the discipline of excluding any mover whose
  only source was a single uncorroborated aggregator (Paramount Skydance/
  SKYD's prior "proposed merger" narrative from a dateless Weiss Ratings
  alert was checked against primary sources and found to describe a stage of
  the deal that had already closed — excluded from the driver narrative,
  only the confirmed closing/settlement terms were used). The right call
  when time-constrained remains: corroborate with a second source, report
  the move without the unverified driver, or flag it as unverified in Annex
  A — never invent or infer a plausible-sounding explanation to fill the gap.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. `figsize=(9.8, 1.95)` for
  BOTH chart 1 (movers) and chart 2 (an 11-category sector-ETF-proxy panel) —
  **this supersedes the previous `(9.8, 1.55)`–`(9.8, 1.75)` guidance for
  panel2, which produced overlapping y-axis labels when actually rendered and
  inspected at edition 37 (see Hard Rules above for the full writeup).** Use
  `font.size 9.6`, dpi 210, `width:100%` in the page. A shorter-category-count
  chart2 (e.g. 7-8 rows, such as a CFTC positioning chart) may still be fine
  at 1.55-1.75in — but **always render and visually inspect (via the Read
  tool) the actual PNG at or near full resolution before embedding it**,
  regardless of what a past edition's page-count success might suggest; a
  layout failure in chart2 specifically does not show up in the page-count
  check, only in the rendered image itself. For a grouped (multi-series) bar
  chart, such as edition 34's CFTC Asset-Manager-vs-Leveraged-Funds chart,
  the simple single-series `barh()` helper in `make_charts.py` doesn't apply
  — write a dedicated `grouped_bar()` function instead (vertical bars, two
  series per category, legend below the plot), watching for the legend-
  overlap and y-axis-label-clipping traps documented in earlier editions.
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
  overflow each time. **Editions 34 through 37 have all rendered clean at 4
  pages on the first (or near-first) attempt.** Always re-render and
  re-check the page count after each trim/pad round rather than guessing how
  much is enough.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. The Commodities & FX table has split cleanly
  across the page 2/3 boundary with no repeated header row in multiple
  recent editions (35, 36, 37) — plain-`<tr>` tables reflow across a page
  break safely; this is expected behavior, not a bug to fix.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  A visibly short page 3 has recurred at editions 25, 28, 32 and 36, each
  needing a genuinely additive fix (never a padding table that just repeats
  an existing table's rows). **Edition 37 rendered clean at 4 pages on the
  first attempt with page 3 filling comfortably from content alone — no
  padding or trimming needed.** Continue checking for both failure modes
  (short page 3, overflow) after every render regardless of recent-edition
  track record.

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
  including 34, 35 and **37**. Always re-render immediately after adding (or
  removing) any content to confirm the page count, rather than assuming a
  change is safe.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across twelve eligible
editions, 25 through 37, with edition 34 the sole exception when fresher CFTC
data was available). Fresh CFTC CoT data on a Monday/weekend-window edition →
the ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart, normalized
as % of open interest — this materialized for the first (and so far only)
time at edition 34; editions 35, 36 and 37 all had no fresh CoT data due in
their windows and correctly reverted to the sector-ETF-proxy default. **The
next CFTC report (due Friday 9 October, covering Tuesday 6 October data) may
land inside edition 38's window — check cftc.gov first thing and use the
positioning chart if it's available and the edition is a Monday/weekend-
window edition.** A single dominant earnings print with a clean, well-sourced
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
(Derivatives) rather than Section 2; editions 35, 36 and 37, all back on the
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
every edition since, now six straight direct re-confirmations); tracked the
Jackson Hole keynote (28 Aug, hawkish) and the resulting rate-odds repricing
through editions 10–18; resolved the SPDR-sector-ETF-proxy and CBOE-feed
sourcing techniques at editions 10–11; corrected the FOMC decision date to
Wednesday 16 Sept at edition 18. Major single-name events across editions
1-21: Moderna's melanoma-data spike/unwind, Nvidia's Q2 FY27 beat/Hugging
Face acquisition, Walmart/Advance Auto Parts/Deere earnings, the
PayPal-Stripe deal collapse, California SB 492 hitting utilities, an
Iran/Hormuz escalation cycle repeatedly driving oil, Lululemon's
guidance-slash collapse, Canada's approx. $27.6bn retaliatory tariffs,
Apple's first Ternus-era product event, Oracle's Q1 FY27 vol-crush beat, the
Fed debate flipping from "hold vs. cut" to "hold vs. hike" on hot core CPI,
and Anthropic CEO Dario Amodei's AI-safety essay driving a
chip-selloff/cybersecurity rotation. **The Sept 15-16 FOMC meeting and its
aftermath (editions 21-23):** S&P 7,585.73 pre-decision; the Fed hiked 25bp
to 3.75%-4.00% unanimous 12-0, equities reversed hard (S&P 7,551.81, 10-year
first closed above 5% since 2007); then a sharp relief rally (S&P 7,637.76
+1.1%), BoE held at 3.75% (6-3). Edition 24 (triple witching + weekend):
approx. $7tn September triple-witching notional expired, Xenon
Pharmaceuticals -30.7%, Buffett stepped down as Berkshire chairman, BoJ
hiked to approx. 1.25% (31-year high). Edition 25: a broad chip rally pushed
Nasdaq to a then-record 27,122.09; quarterly index rebalances took effect.
Edition 26: financials-led rotation, Viking Therapeutics +35.67%, a genuine
Kitco-vs-USAGOLD gold split (later resolved). Edition 27: risk-off on a
19-year 10-year yield high, the "Meta Muse" AI-agent theme rotated from banks
into online travel names, VIX 15.18. Edition 28: a whipsaw near-flat session,
MGM Resorts -10.99% on a withdrawn take-private bid, the Trump-Xi summit
extended the US-China trade truce. Edition 29: a relief rally, Meta -3.33% on
the Cambridge Analytica verdict, the US-China $30bn tariff-cut agreement
first reported, zerogex's first anomalous gamma jump. Edition 30: broad
risk-off on a rejected Iran Hormuz offer, Kodiak Sciences +177.96% (the
movers-chart capping rule's first genuine case), MongoDB -18.46%. Edition 31:
DXY-vs-FX-crosses conflict resolved cleanly; zerogex -$17.19bn. Edition 32: a
volatile round-trip close, Liquidia -57.19%, Micron beat with a muted AH
reaction, gold spot/futures split (later converged). Edition 33: yields (not
equities) drove the session on a hot ISM Prices Paid print, Accenture
+15.78% and Synopsys +12.78% led an AI-infra earnings cluster, Nike missed
FQ1 guidance (resolved edition 34); the document overflowed to 5 pages,
needing five trim rounds. Edition 34 (Mon 5 Oct, covering Fri 2 Oct +
weekend): a badly-missed September jobs report (nonfarm payrolls +29,000)
drove a broad risk-on rally and a sharp October-hike-odds collapse (to
approx. 17-21.6%); S&P 500 +0.73% to 7,722.72; a fresh CFTC CoT report gave
the first fully-consistent ES/NQ/RTY OI normalization, powering a
CFTC-positioning chart #2; zerogex flipped decisively positive (+$22.96bn
from -$11.58bn). Edition 35 (Tue 6 Oct, covering Mon 5 Oct): two same-day
cash buyouts drove the tape (Schneider Electric/PTC Inc, C.H. Robinson/RXO
Inc) — PTC +33.49%, RXO +22.54%; equities extended Friday's rally to a
Nasdaq Composite record (27,477.31); September's ISM Services PMI printed
54.9% with a hot 74.0% Prices Paid sub-index driving the 10-year to a fresh
24-year high near 5.35%; two new sourcing traps logged (stale Nike
price-target recirculation, the Paramount Skydance stock-split "+96%"
artifact); zerogex roughly doubled to +$46.35bn.

**Edition 36 (condensed)** — Wednesday 7 October 2026 report covering
Tuesday 6 October 2026, the window's one NYSE session. Equities extended
Monday's rally to fresh records with no single dominant catalyst: S&P 500
+0.58% to 7,818.93 (record), Nasdaq Composite +0.45% to 27,599.79 (second
consecutive record), Dow +0.49% to 51,521.28 — but Russell 2000 bucked the
trend, -0.59% to 2,830.30. Falling yields drove a clean rate-sensitive
rotation: Utilities led all 11 sectors (+2.98%), ten of eleven closed green.
Constellation Energy +12.25% (reported Google nuclear PPA, terms
unconfirmed), Lamb Weston +7.49%, Marvell +5.81%, AMD +2.80% to a fresh
all-time high; Novavax -9.87% and Moderna -7.75% both fell on drivers that
could not be corroborated by any source. The Paramount Skydance/Warner Bros.
Discovery $110bn merger closed, renaming to Skydance Corporation and moving
to NYSE under ticker SKYD — no reliable same-day % figure was obtainable
given the ticker change (resolved the very next session, see edition 37).
Two severe sourcing traps: a tool-summarized fetch cited fabricated AMD price
targets ($800 Citi, $705 Mizuho) that conflicted with real, much-lower
targets found independently; an unverifiable "WHO" claim was cited as the
driver behind both Novavax's and Moderna's declines and rejected. Macro facts
reconfirmed; the BoE and US-shutdown/CR gaps were both closed via direct
primary fetches; BoJ's primary PDF was located but unparseable by fetch
tooling for a second straight edition (resolved edition 37 via local
text-extraction); no fresher Fed-hike-odds reading was found dated Tuesday.
A secondary source reversed the US-China tariff list-size assignment
(resolved edition 37). WTI +0.60% to $89.97, Brent +0.26% to $100.58; gold
spot became newly unverifiable (Kitco 404, USAGOLD 403, resolved edition 37
for Kitco); DXY -0.24%, consistent with EUR/USD but not USD/JPY; GBP/USD hit
a genuine three-way conflict (resolved edition 37). The 2-year Treasury
yield could not be resolved (33bp gap between endpoints, resolved edition
37). CBOE gave a ninth consecutive clean sweep (VIX 15.01, -3.29%); VIX9D
inversion widened to -2.98. zerogex's SPX gamma extended a third consecutive
sharp step-up to +$74.26bn (reversed edition 37). No new CFTC CoT report was
due. SOFR 3.89%. 32 sources, clean 32/32 on the first check_refs.py pass,
zero stray tildes, clean 4-page render (page 3 ran short, fixed with a
Treasury yield-curve table and additive gamma color).

**Edition 37 (most recent — full detail)** — Thursday 8 October 2026 report
covering Wednesday 7 October 2026, the window's one NYSE session, research
window Tue 6 Oct 2026 20:00 ET through Wed 7 Oct 2026 20:21 ET. Verified the
two structural header rules again — now clean across nine consecutive
single-session or single-session-plus-weekend editions (29-37).

The dominant story was the Fed, not a single stock: the September FOMC
minutes, released Wednesday 2:00pm ET squarely inside the window, showed a
unanimous 12-0 hike with no dissent but only "most" (not all) participants
currently backing a further 2026 hike — read directly off federalreserve.gov,
closing the standing "top open item" flagged at edition 36. Equities
retreated broadly from Tuesday's records on a bond-market selloff: S&P 500
-0.2% to 7,801.77, Dow -0.7% to 51,179.87, Nasdaq Composite -0.2% to
27,538.69, Russell 2000 -1.3% to 2,793.20 (underperforming for a second
straight session) — confirmed via AP's wire, independently mirrored across
two syndication sites (wtop.com, krmg.com) and arithmetically reconciling
exactly against Monday's logged closes. Ten of eleven SPDR sectors closed
lower: Industrials (-2.18%) led losses on an unexplained -5.75% drop in
Caterpillar (driver never corroborated despite repeated searches); Health
Care (+1.03%) was the lone gainer. Single-name action: Skydance Corporation
(formerly Paramount Skydance/PSKY, renamed Tuesday on the WBD merger close)
-6.72% under its new ticker SKYD, the first clean post-transition close;
Applied Digital -6.04% intraday ahead of an after-the-close fiscal Q1 beat
(revenue +322% y/y vs. consensus); the AI-optics trade (AAOI -5.85%, COHR
-1.12%, LITE -1.97%) reversed Tuesday's rally with no fresh catalyst found;
Constellation Brands +2.35% on an FY2027 guidance raise (precise EPS/revenue
vs. consensus unresolved); GE -1.86% and Boeing -0.79% tracked broad
Industrials weakness with no distinct driver. No Wednesday-dated analyst
upgrade/downgrade roundup could be located for any name — a new, more severe
gap than prior editions' single-aggregator-only roundups.

A primary-source breakthrough on the Bank of Japan: its own Sept 18 decision
PDF, previously unparseable via the fetch tool's HTML-conversion path, was
downloaded directly and run through `pdftotext` locally — revealing the
September hike passed 7-2, not unanimously as previously assumed, with two
named dissenters (Asada Toichiro, Sato Ayano) preferring to hold. The BoJ's
next meeting date (Oct 29-30) remains secondary-only for a third edition.
Three standing open-conflict threads were all resolved this edition: the
US-China tariff list-size assignment (confirmed 77 US/1,619 China via a
direct whitehouse.gov fetch), the 2-year Treasury yield's 33bp cross-endpoint
gap (both CSV and TextView now agree at 4.77%), and GBP/USD's three-way
level/direction conflict (four sources converged on 1.3213, -0.47%, once a
live-quote timing artifact was correctly excluded). No post-minutes
prediction-market odds snapshot was found — all cited October (approx.
16-18%) and December (approx. 72%) figures predate the 2:00pm ET release,
flagged as the top open item for edition 38. WTI and Brent both hit a sharp
level-vs-%-change reconciliation failure across three independent vendors
(resolved by computing off the logged prior close: approx. -1.0% WTI,
approx. +0.55% Brent, rather than trusting any vendor's self-stated change).
Gold and silver both sourced cleanly (Kitco recovered after a 404 last
edition); copper +0.03% to $14,510.00/tonne via Westmetall. DXY +0.42% was
consistent with EUR/USD (-0.56%) and GBP/USD (-0.47%) but not USD/JPY
(-0.016%, essentially flat) — the same specific cross breaking the pattern as
edition 36, now flagged as possibly structural. CBOE gave a tenth consecutive
clean sweep with neither documented bug present (VIX 15.08, +0.47%); VIX9D
inversion widened further to -3.30 from -2.98. zerogex's SPX dealer gamma
broke its three-session sharp-step-up streak, pulling back 22% to +$57.61bn
from Tuesday's record +$74.26bn — still solidly positive; SPY/QQQ net-GEX
stayed positive too. No new CFTC CoT report was due (next due Fri 9 Oct,
covering Tue 6 Oct data — may land inside edition 38's window). SOFR 3.90%
(Tue 6 Oct, one-day lag). A genuine chart-layout bug was found and fixed:
the sector-ETF-proxy panel2 chart's documented `(9.8, 1.55)` figsize produced
overlapping y-axis labels at 11 categories when actually rendered and
inspected — fixed by bumping to `(9.8, 1.95)`, now the corrected default (see
Hard Rules and Production notes above). 31 sources, clean 31/31 on the second
`check_refs.py` pass (one Annex B entry was initially uncited, fixed
immediately), zero stray tildes, clean 4-page render on the first attempt
with page 3 filling comfortably from content alone.

**Open threads for edition 38:** No post-FOMC-minutes (2:00pm ET Wed 7 Oct)
prediction-market odds snapshot has been found yet for October/December hike
probabilities — **this is the top open item**; make it the first search of
edition 38, since every currently-logged figure predates the minutes. The
next CFTC CoT report is due Friday 9 October (covering Tuesday 6 Oct data) —
check cftc.gov first thing; if edition 38's window reaches Friday, use it for
a fresh ES/NQ/RTY positioning chart #2 (Monday/weekend-window editions
only, per standing guidance) and watch for the CFE legacy report's VIX
futures positioning too. The Bank of Japan's next meeting date (Oct 29-30)
remains secondary-sourced only for a third straight edition — try the same
local-PDF-text-extraction technique that resolved the September decision
document on BoJ's own calendar/publications page. DXY-vs-USD/JPY has now
broken the DXY-vs-crosses consistency pattern on two consecutive editions
(36, 37) — worth watching whether this is becoming a structural (not random)
feature of USD/JPY specifically. zerogex's SPX dealer gamma broke a
three-session run-up with a sharp -22% pullback at edition 37 — watch
whether it continues falling, stabilizes, or resumes climbing, especially
around any fresh Fed-odds repricing. Caterpillar's -5.75% Wednesday driver
remains unresolved — watch for a delayed explanation (an analyst note, a
delayed news item) surfacing in the next day or two. Constellation Brands'
precise Q2 FY2027 EPS/revenue vs. consensus remains unconfirmed — revisit
only if load-bearing. Applied Digital's Thursday opening reaction to its
large fiscal Q1 revenue beat (reported after Wednesday's close) is the first
readable data point on the print — check Thursday's action. The DXY's single
-sourced Wednesday close (Investing.com only) should get a second
corroborating source attempt next edition if feasible. Thursday 8 Oct's
jobless-claims print and the Sept CPI (Wed 14 Oct)/PPI (Thu 15 Oct)
consensus estimates were not sourced this edition — pull the actual prints
and consensus figures as they land. TSMC's Oct 15 earnings call remains the
next flagged catalyst for the Intel/TSMC "Terafab" storyline, which had no
Wednesday-specific development. The Meta/Cambridge Analytica penalty
decision remains signaled for roughly 20 October — watch for it. USAGOLD's
history pages have now 403'd three editions running (35-37) — try a
genuinely different access pattern next time rather than repeating the same
fetch a fourth time. Kalshi's direct fetch was attempted and blocked again
at edition 37 (resumed after edition 36 skipped it) — resume the
attempt-every-edition discipline at edition 38. Threads closed after
resolution rather than carried further: the BoJ September-decision
primary-sourcing gap (closed via local PDF text-extraction); the US-China
tariff list-size conflict (closed via direct whitehouse.gov fetch); the
2-year Treasury 33bp cross-endpoint gap (closed, both endpoints now agree);
GBP/USD's three-way conflict (closed via a four-source close-to-close-history
check); the Paramount Skydance/SKYD ticker-transition sourcing gap (closed
the session after the transition); the sector-ETF-proxy chart2 figsize bug
(closed, `(9.8, 1.95)` is now the corrected documented default).
