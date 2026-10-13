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
  through 39 have all applied this correctly** ("Friday 2 October 2026,"
  "Monday 5 October 2026," "Tuesday 6 October 2026," "Wednesday 7 October
  2026," "Thursday 8 October 2026," "Friday 9 October 2026" and "Monday 12
  October 2026" respectively as the date line, with the window line carrying
  the session(s) covered) — now confirmed stable across eight consecutive
  editions (edition 40: "Tuesday 13 October 2026" as the date line, window
  line carrying the session), treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 39 all reused the
  same pattern for single-session (or single-session-plus-weekend) windows —
  now confirmed clean across twelve consecutive editions (29 through 40;
  edition 40 phrased it "Window: Sun 11 Oct 2026 20:00 ET – Mon 12 Oct 2026
  20:21 ET (Mon 12 Oct close/AH)"). No further confirmation needed; treat
  this as settled.

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
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 39
  directly against federalreserve.gov's own FOMC calendar page — now under
  three weeks out, continue re-confirming every edition until then. Decision
  and press conference both land 28 Oct, 2:30pm ET. The following meeting is
  December 8-9, 2026 (an SEP meeting).
- **October-hike odds — edition 40 found the first directional move in
  several editions, still modest:** DeFi Rate's Kalshi/Polymarket-blended
  aggregator, snapshot Monday 12 Oct 2026 8:24pm ET, shows **October 27-28
  hike odds approx. 18%** (hold approx. 81-82%, cut approx. 2%) and
  **December 8-9 hike odds approx. 75%** — up from Sunday 11 Oct's approx.
  16% Oct / approx. 73-74% Dec (edition 39's read). This is the first move in
  either direction across editions 37-40, though still within normal noise;
  don't over-read a single 1-2pt tick, but note whether it extends at edition
  41, especially with Sept CPI landing Wed 14 Oct. The composite "at least one
  more hike in 2026" read was not freshly re-pulled at edition 40 either (last
  known approx. 80%, edition 38) — don't cite without a fresh pull. Kalshi's
  own direct fetch returned HTTP 429 again at edition 40, now a confirmed
  standing failure mode across four consecutive attempts (37-40).
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
  $30bn against 2024 bilateral trade. Still pending each side's domestic legal
  processes for actual implementation — edition 39 searched again for a
  Federal Register/USTR implementation notice specifically and found none
  (only unrelated routine Section 301 product-exclusion conforming
  amendments) — watch for a formal implementation/effective date in a future
  edition. The two whitehouse.gov PDF copies carrying different dates (Sept 23
  vs Sept 27, 2026) remains an unresolved minor wrinkle, not worth chasing
  unless load-bearing.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch,
  rba.gov.au, etc.) every edition, exactly like any other data point. Edition
  40 re-confirmed Kevin Warsh as Fed Chair directly against
  federalreserve.gov's Board of Governors bios page — **a tenth straight
  direct re-confirmation.** The BoE's next decision (Thursday 5 November) was
  freshly re-touched at edition 40 via a direct bankofengland.co.uk fetch —
  unchanged, now confirmed directly for two straight editions (39, 40) inside
  the roughly 3.5-week (now under 3.5-week) window. The shutdown/CR
  primary-source lapse closed at edition 39 stayed closed at edition 40 via
  another genuine direct whitehouse.gov fetch of the same dated permalink
  (`whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500/`)
  — still funded through 11 December 2026, no new shutdown/CR news. **The
  BoJ's next-meeting-date primary source regressed slightly at edition 40**:
  rather than a direct plain-text re-read of boj.or.jp (as achieved at
  editions 38-39), edition 40 could only corroborate the Oct 29-30, 2026 date
  and the approx. 1.25% rate level via secondary sources (securities.io, MNI
  Markets) describing the primary PDF's filename/date, not a directly
  machine-read primary-source sentence — the fact itself is not in doubt
  (multiple consistent secondaries, plus two prior direct confirmations), but
  **re-attempt the direct boj.or.jp plain-text read at edition 41** to restore
  the stronger verification standard rather than letting the secondary-only
  method become the default.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed directly
  again at edition 40 (following decision 17 December 2026). Continue the
  direct-fetch discipline every edition given the meeting is now under four
  weeks out.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano), both primary-sourced as of edition 37 — closed thread, do
  not re-derive. **The next policy meeting date (Oct 29-30, 2026) remains
  correct but edition 40's re-confirmation stepped down to secondary-only
  corroboration** (see general-principle entry above) rather than the direct
  primary read achieved at editions 38-39 — re-attempt the direct boj.or.jp
  plain-text fetch at edition 41 to restore the stronger method. No doubt
  about the underlying fact, only about this edition's verification rigor.
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
- **No US federal government shutdown is in effect — re-confirmed at edition
  39 via a genuine direct whitehouse.gov fetch** (briefing statement on H.R.
  6500, the Continuing Appropriations and Extensions Act, 2027): signed into
  law 2 September 2026, funds the government through **11 December 2026**.
  This closes the primary-source lapse flagged at edition 38 (which had used
  two independent secondaries, AACOM/ASAHP, instead) — see the general
  principle entry above for the working URL pattern. Watch for shutdown risk
  resurfacing as 11 December 2026 approaches.
- **University of Michigan preliminary October 2026 consumer sentiment — new
  this edition, not yet a "closed thread," watch for the final reading:**
  46.3, a five-month low (current conditions 44.7, expectations 47.3,
  year-ahead inflation expectations 4.7% from 4.6%, long-run 3.5% from 3.4%),
  confirmed via investinglive.com and advisorperspectives.com (dshort), both
  dated 9 Oct 2026. Consensus estimates disagreed sharply across outlets
  (approx. 47.6-50.5) — no single consensus figure should be cited without
  disclosing the range. **Final October reading due 23 October 2026** — watch
  for it.
- **China September 2026 CPI/PPI — still open as of edition 40's cutoff,
  unchanged for a second straight edition:** a direct fetch of stats.gov.cn's
  latest-releases page (checked again at edition 40) still showed August data
  only and did not forward-list a September release date — the page's most
  recent entry was a semi-monthly "Market Prices of Important Means of
  Production" bulletin dated 9 Oct, not CPI/PPI. One secondary source
  (financecalendar.com) continues to claim **14 October 2026**, consistent
  with NBS's typical 9th-15th cadence and last year's equivalent release
  landing on the 15th (Beijing time). Edition 39's unverified Golden-Week-delay
  hypothesis was **not re-tested at edition 40** (time constraints) — still
  not citable as fact. **Check stats.gov.cn directly again at edition 41**;
  if 14 Oct Beijing time (= evening of 13 Oct ET) has passed by then, check
  whether the release actually landed on schedule.
- **New calendar-awareness item from edition 40: "equities-open,
  bonds-closed" US holidays need an explicit check every time they land in
  the window, not an assumption from memory.** Monday 12 Oct 2026 was
  Columbus Day — NYSE/Nasdaq traded a normal full session but the Treasury
  cash market and SOFR/EFFR/OBFR fixings were closed (SIFMA-recommended bond
  holiday), so the session's rates/funding figures simply repeated Friday's
  last marks. This was inferred circumstantially (the absence of an Oct 9 or
  Oct 12 SOFR print, consistent secondary-source confirmation) rather than
  confirmed against a 2026-dated primary CME/SIFMA holiday calendar — worth a
  tighter primary-source check if it recurs (next candidate: Veterans Day,
  Wed 11 Nov 2026 — verify whether that is also bonds-only before assuming).

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
  uniqueness of use (editions 33-39 have all done this for stockanalysis.com
  single-stock closes and other repeatedly-used outlets, confirmed stable
  across seven editions).
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart 2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes). **Chart
  placement is editorial, not fixed to Section 2** — edition 24, edition 34
  and **edition 39** all placed a CFTC-positioning chart #2 in Section 5
  (Derivatives) rather than Section 2, since that's where the content
  actually belongs. Editions 35 through 38 reverted to the sector-ETF-proxy
  default (no fresh CoT data due in any of those editions) and kept it in
  its default Section 2 placement. **Edition 40 should revert to the
  sector-ETF-proxy default** (no fresh CoT data due until Friday 16 October,
  covering Tuesday 13 October) unless that report has already landed inside
  edition 40's window.
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
  **Editions 27 through 40 are all clean counter-examples worth keeping in
  mind**: all fourteen posted a usable AP wire eventually — editions 38 and
  39 both needed a syndication mirror (La Nación) rather than a direct
  AP fetch; **edition 40 hit a harder version of the same problem** (both a
  direct fetch and two syndication-mirror URLs returned HTTP 403) and
  recovered the figures via a search-engine snippet instead, cross-checked
  against a dated Yahoo Finance/Motley Fool close article, stockanalysis.com,
  and arithmetic reconciliation against the prior session's logged close —
  all four independently agreed, so the figures were used with confidence
  despite not reaching AP's own site directly. Treat "search-snippet recovery
  with multi-source reconciliation" as an acceptable fallback tier below a
  syndication mirror, not a reason to discard the figures, provided the
  reconciliation genuinely checks out.
  **Edition 37 is a useful cautionary tale about method, not about the source
  itself**: a general-purpose WebSearch AI-summary returned the correct AP
  figures attached to a *guessed* URL, and the research subagent — correctly
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
  Citigroup options-wire, Nike, SPCX). **Edition 39 added two more names to
  this list**: Moderna (a secondary source's intraday magnitude of approx.
  8-11% didn't reconcile with the +14.21% close — disclosed, not resolved)
  and AST SpaceMobile (a secondary source's -13.6%/$49.20 figure didn't
  reconcile with stockanalysis.com's -10.48% close — the latter used as
  authoritative). Resolved the same way as always: treat the
  stockanalysis.com (or equivalent timestamped) close as authoritative, and
  disclose explicitly when an earlier-session figure doesn't match the
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
  edition 37's research window) fully explained it by edition 38.** **Edition
  39 hit two fresh instances of this same pattern that remain OPEN, not yet
  resolved: a second consecutive session of unexplained AI-optics moves
  (AAOI +3.53%, COHR +3.40%, LITE +5.22%, rebounding Friday with no fresh
  catalyst found) and Fastly's +15.86% move with literally no driver found
  at all despite a real search attempt.** General technique worth keeping
  alongside the ticker-transition one above: when a same-day mover's driver
  can't be found despite a real search attempt, don't force a guess — report
  the move without a driver and explicitly flag it as an open thread, then
  re-search for a delayed explanation at the very next edition before
  assuming none exists. **AAOI/COHR/LITE and FSLY were checked again at
  edition 40 and the pattern continued rather than resolved**: all four
  reversed sharply (AAOI -8.17%, COHR -7.87%, LITE -9.78%, FSLY -9.80%,
  nearly erasing Friday's unexplained spike), with only a generic,
  non-company-specific "AI-stock pullback" framing found in a dated Yahoo
  article — still no confirmed company-specific driver for any of the four
  across two straight sessions now. Three more names joined the same
  unexplained-AI-hardware-selloff bucket at edition 40: Cerebras (CBRS,
  -10.69%), Semtech (SMTC, -10.15%) and Ciena (CIEN, -9.95%), none with a
  dated driver despite a genuine search. **Check all seven names again at
  edition 41** for a delayed explanation, and consider whether this cluster
  needs a dedicated "AI-hardware complex" framing rather than treating each
  name as an independent open thread.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. **Similarly, a price level can be correct while a vendor's stated
  %-change is wrong** if the vendor used a different prior-day base — always
  sanity-check that a stated price and stated % change reconcile
  arithmetically against the prior session's logged close. This exact pattern
  has now recurred repeatedly on oil across editions 35, 37 and 38, narrowed
  to WTI-only at edition 39 (Brent reconciled cleanly that session), and
  **cleared for BOTH grades at once at edition 40** — WTI -0.92% and Brent
  -0.86% both matched their own vendor-stated % exactly, the first clean
  dual-grade reconciliation logged in this report's history. **Don't treat
  this as the problem being fixed** — it is a vendor-side data-quality issue
  that has now shown every combination (WTI-only, Brent-only implicitly via
  WTI-only sessions, both clean) — keep computing and disclosing every
  edition regardless of how the last one went. Edition 39 additionally found
  the same vendor-%-vs-computed-%change gap, in milder form, on gold spot,
  silver spot and DXY; **edition 40 found the same pattern again on gold
  spot, silver spot, Henry Hub and DXY** (each vendor's own daily-change
  field was computed against Sunday's thin pre-open print rather than
  Friday's actual close — a different, specific mechanism from the earlier
  editions' unexplained base mismatches, worth naming explicitly when
  disclosing). Broaden the standing guidance accordingly: **compute every
  commodity and FX %-change directly off this report's own logged prior
  close, every edition, for every instrument, not just oil and not just when
  something looks surprising** — disclose the method explicitly in the text
  with a `*` and a footnote (now standard practice since edition 39). The oil
  contract-month-roll trap (Brent Nov-to-Dec) remains resolved; both grades
  rolled to new contract months again at edition 40 (WTI Nov '26/CLX6, Brent
  Dec '26/LCOZ6) with no issues. The CBOE vol-complex feed's two documented
  bugs (duplicate-`prev_day_close`, and `price_change_percent` dividing by
  current price instead of prior close) **were ABSENT at edition 40 — the
  feed's own percent field matched our manual recompute across all six
  series for the first time in several editions.** This does NOT mean the
  bugs are fixed: they recurred at edition 39 after four clean editions
  (35-38), so they remain genuinely intermittent. Always compute day-over-day
  % change manually as `price_change ÷ (current_price − price_change)` and
  treat the feed's own `price_change_percent` field as unreliable until
  checked each time regardless, even after a clean read.
- **The DXY-vs-its-own-FX-crosses conflict** has now recurred, at least
  partially, in roughly half of all occurrences since edition 29 (resolved
  cleanly at 31, 33, 35; recurred at 32, 34, 36, 37, 38 — all three times via
  USD/JPY specifically breaking from DXY's direction). **This pattern PAUSED
  at edition 39 and stayed paused at edition 40**: USD/JPY moved in the
  *same* direction as DXY for a second consecutive session (edition 40:
  USD/JPY +0.12% vs. DXY +0.35%, both dollar-strength readings, internally
  consistent with EUR/USD -0.37% and GBP/USD -0.20% too). **Still do not
  graduate this to "expected by default"** — two consecutive non-divergent
  sessions is a short streak against a longer history of intermittent
  divergence; keep watching whether the USD/JPY-specific divergence resumes
  at edition 41 rather than assuming either continuation or reversal.
  Continue disclosing the DXY-vs-crosses comparison explicitly every edition
  regardless of which way it goes.
- **The same-day silver sign conflict first flagged at edition 31 has now
  stayed resolved for nine straight editions (32-40)** — silver rose/fell
  consistently across spot and futures at every session in that span. Treat
  as closed unless a fresh mismatch appears.
- **GBP/USD's two-edition data-quality problem (a minor two-source gap at
  edition 35, a genuine three-way level/direction conflict at edition 36)
  has now stayed resolved for four further editions (37-40)**, with edition
  40 single-sourced to Investing.com's close-to-close history table (no
  conflict found, -0.20% computed) rather than the fuller multi-source check
  — consistent with edition 39's lighter-touch approach. Resume the fuller
  multi-source method if a fresh conflict reappears, or periodically to
  re-confirm the lighter method is still safe. **Note this timing artifact
  for future editions: a live FX quote fetched near/after the NY 5pm close
  may reflect the *next* session's opening tick, with its own "previous
  close" already equal to the session just completed — don't mistake this
  near-zero "live" change for the day's actual close-to-close move. Use a
  dedicated close-to-close history source rather than a live snapshot when
  fetching this late in the window** (edition 40 again saw this exact
  artifact on DXY: a live quote near the window's edge showed a trivial
  -0.04% tick against its own just-set "previous close," while the real
  close-to-close move was +0.35%).
- **The 2-year Treasury yield conflict from edition 36 (TextView 4.46% vs.
  CSV 4.79%, a 33bp gap) has stayed resolved for four further editions (37-40,
  though not re-checked at 40 since the Treasury market was closed for
  Columbus Day)** — edition 39 fetched both the TextView and CSV endpoints
  directly and found them in full agreement (2-yr 4.80%, 10-yr 5.24%, 30-yr
  5.60%, all Oct 9) — these remain the last-available marks carried into
  edition 40's report. Treat as resolved/noise unless a fresh conflict
  appears; if one does, the standing advice stands — dig into which endpoint
  is wrong via a market-wrap secondary cross-check for the specific disputed
  maturity. **Re-fetch fresh Tuesday 13 Oct yields at edition 41** now that
  the Treasury market has reopened.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 40 have all run clean (or
  clean after one quick fix) — **edition 40 drafted clean on the first pass
  at 34/34**, no Annex-B-only orphans this time. Worth re-stating: table
  cells (and disclosure-box/tile-adjacent sentences) are a legitimate,
  already-used place to put a citation — use them rather than forcing an
  awkward prose mention just to attach a `<sup>` tag.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 40 have all rendered clean at zero tildes** on the
  first check. **Reminder: `grep -c` exits with status 1 (not 0) when the
  count is zero, since no lines matched — don't chain it with `&&` into a
  longer command and assume a silent failure means the check itself failed;
  read the printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 34 resolved this cleanly for
  CFTC CoT, with full OI and Asset-Manager/Leveraged-Funds breakdowns for
  ES, NQ and RTY. **Edition 39 repeated this successfully** — full OI and
  Asset-Manager/Leveraged-Funds breakdowns for all three instruments again,
  plus a bonus CFE legacy-report pull for VIX futures positioning (not
  charted, reported in prose only). One naming note worth preserving: the
  CFTC's financial-futures table lists the full-size Russell 2000 E-mini
  ("RTY") as a separate line from the Micro E-mini Russell 2000, which has
  very different (much smaller) open interest and a different net-position
  sign at times — **edition 39 again explicitly confirmed it was reading the
  full-size RTY line (OI 425,152) and not the Micro line (OI 64,741) or the
  blended "NASDAQ-100 Consolidated" line for NQ** — always do this check
  before charting. **The next CFTC report is due Friday 16 October 2026,
  covering Tuesday 13 October data** — this will NOT fall inside edition 40's
  window (edition 39 covered through Fri 9 Oct; edition 40 will cover roughly
  Mon 12 Oct), so edition 40 should revert to the sector-ETF-proxy chart #2
  default per standing guidance, and the next CFTC-chart opportunity is more
  likely around edition 43-44 depending on scheduling.
- **A genuinely new chart-layout bug surfaced at edition 37, worth fixing
  permanently in `make_charts.py`'s documented defaults: the sector-ETF-proxy
  panel2 chart at `figsize=(9.8, 1.55)` with `tick_fs=7.6` and 11 categories
  produced visibly overlapping y-axis category labels** (confirmed by
  rendering and visually inspecting the PNG directly, not just trusting the
  matplotlib call succeeded) — the 1.55-inch height does not give 11 rows
  enough vertical room at that font size in this environment. **Fixed by
  bumping panel2's figsize to `(9.8, 1.95)`**, which rendered cleanly with no
  overlap; editions 38 reused this and confirmed it again. **Edition 39
  refined this further: a fuller `figsize=(9.8, 1.95)` is NOT needed for
  lower-category-count charts.** Edition 39 used `(9.8, 1.65)` for a
  7-category single-stock movers chart and `(9.8, 1.85)` for a 3-category
  grouped (Asset-Manager-vs-Leveraged-Funds) CFTC chart, both visually
  inspected at full resolution and confirmed clean with no label overlap or
  legend collision, and both saved meaningful vertical space versus the
  11-category-sized default — this was needed at edition 39 specifically
  because the day's content volume was unusually high (a dominant
  single-stock story plus fresh CFTC data plus a guidance-cut earnings print
  all in one session) and the document was overflowing to 5 pages at the
  11-category-sized chart heights. **Going forward: treat `(9.8, 1.95)` as
  the ceiling for an 11-category panel specifically, not a fixed default for
  every chart — scale figsize down for charts with fewer categories (roughly
  `(9.8, 1.95)` for 10-11 categories, `(9.8, 1.65-1.85)` for 3-8 categories),
  and always visually inspect the actual PNG at or near full resolution
  before embedding it regardless of category count.**
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at editions 33 through 40 (edition 40: FIGS +12.42% vs. CBRS -10.69%, about
  1.16x), all left uncapped. Edition 30 remains the one genuine 10x+ case to
  date (about 15x, capped at a fixed axis max of 30). No need to revisit the
  threshold or mechanism absent a genuinely new edge case (e.g. something in
  the 5-10x range).
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists** — confirmed again at edition 35 (four
  analyst actions all traced to one Benzinga/Yahoo roundup, disclosed as
  such). Edition 37 hit the inverse problem (no roundup for any name could be
  located at all), edition 38 hit a milder version (only the session's own
  biggest earnings mover had dated activity), and edition 39 broke that
  streak with a normal, well-corroborated result (Goldman/Palantir upgrade,
  two Humana PT raises). **Edition 40 reverted to the empty-result pattern**:
  no analyst action dated specifically to 12 October could be independently
  confirmed for any name despite a genuine search — two cited drivers (a
  Meta AI-product launch, a Salesforce analyst upgrade) were found only via a
  single aggregator without a confirmable firm/date and were excluded from
  the stated cause as a result. **The pattern is clearly intermittent, not
  trending in either direction (37 empty, 38 thin, 39 normal, 40 empty)** —
  keep treating each edition's result on its own merits; an empty result
  remains a legitimate, disclosable gap, not a sign of a broken search.
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38**: a secondary aggregator (TheFly, via stockanalysis.com's news
  feed) cited Applied Digital's Q1 EPS as "+1¢ vs. a -30¢ consensus," which
  flatly conflicted with the GAAP figures in the company's own 8-K. The
  likely explanation is that the aggregator's figure is a non-GAAP/adjusted
  metric reported without stating its basis — **when a secondary-sourced EPS
  figure conflicts sharply with a primary filing's GAAP number, prefer the
  primary filing, exclude the conflicting secondary figure from the main
  text, and flag it in Annex A rather than trying to reconcile or silently
  picking one.** **Edition 39 encountered a related-but-distinct, non-trap
  scenario worth contrasting explicitly: Delta Air Lines' own 8-K disclosed
  BOTH a GAAP diluted EPS ($1.15) and an adjusted non-GAAP diluted EPS
  ($1.72), each clearly labelled with its own basis by the company itself.**
  This is NOT the edition-38 trap — when the *company's own primary filing*
  discloses both figures with clear labelling, report both; the trap is
  specifically about a *secondary-only* non-GAAP figure presented without a
  stated basis that conflicts with the primary filing. **Edition 39 also
  logged a new, distinct trap worth tracking separately: an EPS-consensus
  figure can be genuinely conflicted across sources due to a currency/
  share-basis mismatch, not a GAAP-basis mismatch** — TSMC's Oct 15 earnings
  call consensus showed approx. $4.39 (USD ADR-equivalent) in one source, a
  dispersed NT$4.32-4.65 range (local-currency, per-ordinary-share) in
  another, and an apparent outlier of $0.88 likely reflecting a raw
  share-count mismatch in a third. When comparing EPS consensus figures
  across sources, check whether they're quoted in the same currency and on
  the same per-share basis (ADR vs. ordinary share, which for TSMC is a 1:5
  ratio) before treating a gap as a genuine conflict.
- **Know when to treat a third-party data feed's own internal
  inconsistencies as a data-quality flag rather than a reportable trend.**
  Edition 38's zerogex (dealer-gamma) reads carried a stale-snapshot caveat
  on the SPX page plus two now-resolved one-off anomalies (SPY scale
  discontinuity, conflicting QQQ figures); edition 39 confirmed the SPX
  staleness caveat as a structural, standing limitation (two straight
  editions). **Edition 40 found a harder failure mode on the same source:
  the direct API call returned `{"error":"Authentication required"}`, and
  the public front-end rendered only blank placeholder values with no
  timestamp at all** — a step beyond staleness into total unavailability.
  Treat zerogex as now carrying TWO documented failure modes (stale/
  timestamp-inconsistent SPX snapshot, and outright auth-gated blank reads)
  rather than one — check for both every edition, and when neither a usable
  number nor even a stale one is available, report SPX gamma as unavailable
  for that edition rather than omitting the caveat silently. SpotGamma
  remains untried as an alternative per standing practice (it has failed for
  many editions). If zerogex's blank-page failure recurs at edition 41,
  consider this the new baseline rather than a one-off.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. **Editions 28 through 40 all got a full clean sweep** —
  thirteen consecutive clean sweeps now, every series carrying a same-day
  `last_trade_time`, verified individually per series via a raw `curl`/direct
  fetch (not a tool-summarized fetch) each time. Still not a guarantee — keep
  checking `last_trade_time` on each series every time. **The feed's two
  known intermittent bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) were ABSENT at edition 40** (the manual recompute matched the feed's
  own percent field across all six series) **after recurring at edition 39
  following four clean editions (35-38) — this confirms the bugs are
  genuinely intermittent, not fixed/eradicated or a monotonic trend.** Always
  compute day-over-day % change manually against the previous edition's
  logged close regardless of how many consecutive clean reads preceded the
  current one. The VIX9D-vs-spot-VIX front-end inversion (first flagged
  edition 28) widened to -3.58 at edition 39, then **narrowed slightly to
  -3.53 at edition 40** — still irregular/non-monotonic, don't assume either
  continuation or reversal by default in either direction.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table,
  and (absent fresher CoT data or another dominant story) chart #2. **Edition
  40 reverted to the sector-ETF-proxy chart #2 default as planned** (8 of 11
  sectors green: Energy +1.43%, Cons. Staples +1.17%, Comm. Svcs +0.97%, Real
  Estate +0.75%, Health Care +0.69%, Financials +0.58%, Utilities +0.53%,
  Materials +0.02%; Industrials -0.06%, Cons. Discretionary -0.51%,
  Technology -1.22% the three laggards) — no fresh CFTC data was due this
  window as expected. **Stockanalysis.com single-stock pages remain the
  standing default for pinning an exact closing price/% change on any
  individual mover** — editions 26 through 40 (fifteen straight) have all
  used direct fetches to it. Note that a headline wire's own GICS
  sector-index percentages can differ slightly from the SPDR ETF price-change
  figures (a normal index-vs-ETF-price methodology gap); keep using the SPDR
  ETF figures as the table's primary numbers. **Editions 41 through
  (approx.) 43 should also default to the sector-ETF-proxy chart #2** — the
  next CFTC report is due Fri 16 Oct, covering Tue 13 Oct data, and will most
  likely land inside the edition covering that Friday session (approx.
  edition 44 if the daily cadence holds); check cftc.gov's schedule directly
  each edition rather than assuming the date.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. Editions 38
  through 40 all used the "X of 11 sectors closed higher" sector-ETF read as
  the best available breadth proxy (9 of 11 at edition 39, 8 of 11 at edition
  40), consistent with recent editions. Continue treating an uncorroborated
  single-aggregator (or unsourced search-summary) breadth figure as not
  usable — this has recurred enough times to treat as a durable, not
  occasional, gap.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — a recurring failure for many
  editions, not re-attempted at edition 40 (zerogex tried first per standing
  practice). **zerogex.io remains the only attempted source across fourteen
  straight editions (27-40), but edition 40 hit its hardest failure yet**: a
  direct API probe returned `{"error":"Authentication required"}` and the
  public front-end showed only blank placeholder values with no timestamp at
  all — no usable SPX gamma figure, not even a stale one, was obtained this
  edition. This is distinct from (and more severe than) the stale-snapshot/
  timestamp-inconsistency caveat that recurred at editions 38-39 — **zerogex
  now carries two separate documented failure modes on its SPX read: stale/
  inconsistent timestamps, and outright auth-gated blank pages.** Check for
  both every edition. The SPY scale-discontinuity and QQQ internal-conflict
  anomalies from edition 38 have not recurred since (resolved/one-off,
  confirmed across nine SPY-page instances through edition 39; not re-checked
  at 40 given the SPX page itself was unusable). The magnitude remains
  single-sourced (zerogex only; SpotGamma still yields no real numbers to
  cross-check against). Minor open item carried forward, still low priority:
  zerogex's own stated wall levels (call/put wall) have still not been
  cross-checked against a secondary options note's implied walls.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Edition
  40 again used DeFi Rate's Kalshi/Polymarket-blended aggregator (now a
  stable, consistently-working source across editions 37-40) rather than a
  CME-attributed figure specifically — no fresh CME-attributed citation was
  sought this edition either. Keep treating CME FedWatch as needing a
  disclosed range from secondary sources, not a single figure.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, 23-35, 37-40 (not attempted at edition 36) — a confirmed
  structural gap, not transient. The failure mode changed at edition 38 from
  a "Vercel Security Checkpoint" page to a plain HTTP 429 (Too Many
  Requests); **edition 40 got the same HTTP 429 response again — now the
  confirmed standing failure mode across four consecutive attempts (37-40),
  not session-to-session variance.** Resume the attempt-every-edition
  discipline at edition 41 regardless, but expect the 429. Use Kalshi's own
  secondary reporting (its blog, prediction-market news aggregators —
  news.kalshi.com, or DeFi Rate's own Kalshi/Polymarket-blended aggregator,
  which has now worked cleanly at editions 37-40) as the workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has failed many
  editions running; not re-attempted at editions 35 through 40 (went straight
  to the Westmetall fallback per standing practice). **Westmetall.com has now
  worked cleanly nineteen editions running** as the fallback (copper +0.91%
  to $14,822.00/tonne cash settlement at edition 40, computed off edition
  39's logged $14,689.00 base — no vendor % field to compare against, still
  no reconciliation issue on copper specifically, unlike oil/gold/silver).
  **The oil level-vs-%-change-reconciliation problem that has dogged WTI
  (and occasionally Brent) across editions 35, 37, 38 and 39 cleared for BOTH
  grades at once at edition 40** (WTI -0.92%, Brent -0.86%, both matching
  vendor-stated exactly) — see Hard Rules above for why this should not be
  read as the underlying issue being fixed.
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) has
  historically been preferred since TextView carries a known
  maturity-column mis-mapping bug, but edition 36 found a sharp 33bp
  disagreement between the two specifically on the 2-year. **Both endpoints
  agreed cleanly through edition 39 (2-yr 4.80%, 10-yr 5.24%, 30-yr 5.60%,
  all dated Oct 9) — not re-fetched at edition 40 since the Treasury cash
  market was closed for Columbus Day**, so these remain the last-available
  marks carried into edition 40's report. Treat the 33bp gap as
  resolved/noise, but keep fetching both endpoints and comparing rather than
  trusting either by default once Tuesday 13 Oct's fresh print is available.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. Edition 39 pulled fresh data (Friday 9 Oct
  2026, covering Tuesday 6 October): ES OI 1,932,227 (Asset Mgr net +46.93%
  of OI, Leveraged Funds net -21.48%); NQ OI 283,586 (Asset Mgr net +26.03%,
  Leveraged Funds net -6.78%); RTY (full-size) OI 425,152 (Asset Mgr net
  +10.70%, Leveraged Funds net -24.77%). **Edition 40 confirmed via
  cftc.gov's own release schedule that no new report posted this window** (no
  holiday-delay flag on the 16th) — these edition-39 figures remain the
  latest available. **The next report is due Friday 16 October 2026,
  covering Tuesday 13 October data** — check cftc.gov's release-schedule page
  every edition between now and then rather than assuming the gap continues.
- **GBP/USD and EUR/USD clean close:** both have now been fully resolved
  since edition 37 (EUR/USD since edition 26). **Edition 40 single-sourced
  both to Investing.com's close-to-close history table** (GBP/USD -0.20%,
  EUR/USD -0.37%, both computed off the logged Friday close) rather than the
  fuller multi-source check, consistent with edition 39's lighter-touch
  approach — no conflict found. Resume the fuller multi-source method if a
  fresh conflict appears, or periodically to re-confirm the lighter method
  remains safe.
- **Gold/silver clean close on a non-event day:** USAGOLD is now a confirmed
  **permanent standing gap** (zero archived Wayback snapshots found at
  edition 39) — not re-attempted at edition 40, per the edition 39
  recommendation; continue not attempting it absent a new URL/method. **Kitco
  worked again at edition 40**, breaking its two-edition failure streak (38,
  39) — live gold/silver bids were obtained, though without a disclosed
  prior-close reference on the page, so they were used only as secondary
  color (roughly $8/oz and $0.21/oz off Investing.com's settled figures) with
  Investing.com as the primary source. **Treat Kitco's two-edition failure as
  a resolved blip, not a durable degradation** — continue trying it each
  edition but keep Investing.com as the primary fallback regardless. Gold
  futures continue to source cleanly via Investing.com. Silver's sign
  conflict (live since edition 31) has now stayed resolved for nine straight
  editions (32-40).
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month, but September's release had still not posted as of edition 40's
  direct stats.gov.cn fetch, and the release date itself remains disputed —
  one secondary source (financecalendar.com) cites 14 October, consistent
  with NBS's typical 9th-15th cadence. The National Day Golden Week delay
  hypothesis from edition 39 remains unverified (not re-tested at edition
  40) — see Standing Facts above. Check stats.gov.cn directly at edition 41;
  if 14 Oct Beijing time has now passed, check whether it actually posted on
  schedule. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue — confirm on the BLS/Fed release schedule
  rather than assuming a date; BLS's own schedule gives: **Sept CPI Wed 14
  Oct 8:30am ET, Sept PPI Thu 15 Oct 8:30am ET, Import/Export Price Indexes
  Fri 16 Oct 8:30am ET** (re-confirmed again via a direct bls.gov fetch of
  the dated monthly-schedule subpage —
  `bls.gov/schedule/2026/10_sched_list.htm` — at edition 40, unchanged for a
  second straight direct re-confirmation; note the generic `2026_sched.htm`
  URL 404's, use the dated monthly-list path), **Q3 Employment Cost Index Fri
  30 Oct 8:30am ET**. **FOMC minutes from the 15-16 September meeting are a
  closed thread** (see Standing Facts above). **US August 2026 trade deficit
  (BEA) widened to $132.6bn, released Tuesday 6 October** — the headline
  direction is reasonably solid but the precise July baseline used by
  secondary sources was internally inconsistent across outlets and was not
  resolved; not revisited at editions 37 through 40. **University of
  Michigan preliminary October consumer sentiment** (see Standing Facts
  above): 46.3, final reading due 23 October 2026 — watch for it.
- **Henry Hub natural gas:** the October contract thread resolved at edition
  32 (final settlement $3.00/MMBtu). The November contract (NGX6) gave its
  cleanest-ever dual-vendor read at edition 38 but that did NOT persist at
  edition 39 or 40 — **edition 40 again single-sourced to Investing.com**
  (NGX6 still front-month, not yet rolled to December; $3.180/MMBtu Monday,
  computed -1.24% off Friday's logged $3.220 close — the vendor's own daily
  figure of +0.25% used Sunday's close as its base, the same artifact seen on
  gold/silver/DXY this edition). **Treat the dual-vendor method as
  genuinely one-off** (only edition 38 in three attempts since) — keep
  testing each edition. Still not labeled an official CME settlement print by
  either vendor.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. Not attempted at editions 33 through
  40 (secondary priority; options-flow colour has instead been sourced from
  dedicated options-flow wires or zerogex's broader snapshot). **Edition 40
  found no notable Monday-dated single-stock options-flow/skew commentary for
  any name at all** (fourth consecutive empty edition on this general
  sub-item, 37-40, now also no longer anchored to a specific name since
  APLD/AMD had nothing either) — the "rotate to the session's biggest mover"
  idea floated at edition 39 was tried at edition 40 and still came up empty;
  treat this sub-item as reliably low-yield and keep it a brief, secondary
  effort rather than a sustained search each edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable through edition 40;
  next due approx. 14 November 2026.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22). Not attempted again
  through edition 40.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully
  again at edition 39 (see CFTC CoT entry above); not re-attempted at edition
  40 since no new report was due. Repeat this full three-instrument fetch
  whenever a fresh CoT-based chart is next used — next due Friday 16 October
  2026 (covering Tuesday 13 October data) — watching for the
  Micro-vs-full-size Russell naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 37 hit the
  most extreme version (no roundup for any name located at all); edition 38
  a milder version (only the biggest earnings mover had activity); edition 39
  broke that streak with a normal, multi-name result (Goldman/Palantir,
  Cantor Fitzgerald and Barclays/Humana, all with clear dollar price targets
  and dates). **Edition 40 reverted to the empty-result end of the range**:
  no dollar-price-target action dated specifically to 12 October could be
  confirmed for any name. The pattern across 37-40 (empty, thin, normal,
  empty) looks genuinely intermittent rather than trending — report whatever
  a genuine search attempt turns up each edition, whether that's zero, one,
  or several actions, without treating any single result as the new
  baseline.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29, recurred with milder
  versions through edition 36). Editions 37 through 40 did not hit a new
  instance of this specific trap on any NAMED mover's price in the body —
  edition 40's charted/tabled movers (FIGS, CBRS, SMTC, CIEN, FSLY, LITE,
  AAOI, COHR) were all pinned via stockanalysis.com and cross-checked against
  a dated Yahoo Finance close article. **Edition 40 applied the same
  discipline to several names that did NOT make the cut**: FICO's price
  (+10.85%) and CCC Intelligent Solutions' price (+8.12%) were each only
  single-aggregator-sourced (a Yahoo movers list) and were excluded from the
  main body/chart as a result, reported only in Annex A — the same pattern as
  edition 39's Palantir-price exclusion. The right call when time-constrained
  remains: corroborate with a second source, report the move without the
  unverified driver, or flag it as unverified in Annex A — never invent or
  infer a plausible-sounding explanation to fill the gap.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything** — this
  was refined at edition 39 after the previous fixed-size guidance caused a
  5-page overflow on a high-content-volume edition. Use `(9.8, 1.95)` as the
  ceiling for an 11-category sector-ETF-proxy panel (confirmed clean at
  edition 37, reused at edition 38) — this remains correct for 10-11
  categories specifically. For charts with fewer categories, scale the
  height down: edition 39 used `(9.8, 1.65)` for a 7-category single-stock
  movers chart and `(9.8, 1.85)` for a 3-category grouped
  (Asset-Manager-vs-Leveraged-Funds) CFTC chart, both visually inspected at
  full resolution and confirmed clean with no label overlap or legend
  collision. Use `font.size 9.6`, dpi 210, `width:100%` in the page. A
  shorter-category-count chart2 (e.g. 7-8 rows, such as a CFTC positioning
  chart) may still need 1.65-1.85in depending on whether it's a simple or
  grouped bar — **always render and visually inspect (via the Read tool) the
  actual PNG at or near full resolution before embedding it**, regardless of
  what a past edition's page-count success might suggest. For a grouped
  (multi-series) bar chart, such as edition 34's and edition 39's CFTC
  Asset-Manager-vs-Leveraged-Funds chart, the simple single-series `barh()`
  helper in `make_charts.py` doesn't apply — use a dedicated `grouped_bar()`
  function instead (vertical offset bars per category, two series, legend
  below the plot via `bbox_to_anchor` with enough negative y-offset and a
  matching `fig.subplots_adjust(bottom=...)` to avoid the legend colliding
  with the x-axis label — this collision was caught and fixed at edition 39
  specifically; don't rely on `tight_layout()` alone for a grouped chart with
  a below-axis legend, it doesn't reserve enough room by default). **A
  distinct label-overlap bug surfaced and was fixed at edition 40, in the
  simple `barh()` helper's default `pad_frac=0.12`:** when the longest bar in
  a chart (the one with the greatest |value|) approaches the computed xlim
  edge, its value-label text (placed just beyond the bar end) can overflow
  past the axis into the margin where the y-axis category tick labels sit,
  visually overlapping them (confirmed by rendering and reading the PNG
  directly — both edition 40's charts showed this on their single longest
  bar, e.g. "CBRS" overlapping with "-10.7%"). **Fixed by raising `pad_frac`
  to `0.26`** for both of edition 40's charts, which gave enough margin for
  every label (including the longest one) to clear the tick-label area
  cleanly on re-render. Treat `pad_frac=0.12` (the script's literal default)
  as too tight whenever the data's max magnitude is large relative to the
  chart's category-label text width (longer tickers/names need more
  clearance) — `0.2-0.26` is a safer starting point, confirmed at edition 40
  for both a single-series 8-category chart and an 11-category chart; always
  visually inspect the rendered PNG regardless, since the right value still
  depends on label text length and chart width.
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
  overflow each time, and **edition 39 is a further example: the body
  content for a high-volume session (telecom-sector shock + fresh CFTC data
  + a guidance-cut earnings print + a biotech rally all in one window)
  genuinely overflowed 3 pages at the standing CSS baseline and needed both
  real content trims AND a deliberate, evidence-based tightening of the CSS
  baseline (see Working settings below) to fit — this was not a bug, it was
  a genuinely content-heavy edition.** Always re-render and re-check the
  page count after each trim/pad round rather than guessing how much is
  enough. **A large, suspicious blank area at the bottom of a page (as
  opposed to a page that's merely a bit short) is usually caused by an
  atomic block — most often a chart `<img>` — not fitting in the remaining
  space and being pushed whole to the next page, leaving the page that
  precedes it under-filled.** Edition 39 hit this on page 1 (the Section 2
  movers chart got pushed entirely to page 2, leaving roughly 40% of page 1
  blank) — the fix was trimming earlier content (the disclosure box, mainly)
  so the chart had room to start and finish on the same page as its
  preceding heading, not a layout bug in the chart itself. Check for this
  specific failure mode (a heading near the bottom of a page immediately
  followed by a large blank area, with the heading's content starting fresh
  on the next page) before assuming a page is simply "short."
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. The Commodities & FX table has split cleanly
  across page boundaries with no repeated header row in multiple recent
  editions (35 through 39) — plain-`<tr>` tables reflow across a page break
  safely; this is expected behavior, not a bug to fix.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  A visibly short page 3 has recurred at editions 25, 28, 32 and 36, each
  needing a genuinely additive fix (never a padding table that just repeats
  an existing table's rows). Editions 37 and 38 both rendered clean at 4
  pages on the first attempt. Edition 39 needed six render-and-inspect rounds
  to go from 5 pages to 4 on an unusually content-heavy session, combining
  real content trims with a deliberate CSS tightening (see Working settings
  below). **Edition 40 hit the short-page-3 failure mode again** (roughly 40%
  of page 3 blank below the sector-setup bullets, on a lighter-content
  single-session edition) — the fix was the standing-recommended one: added
  a genuinely new, small Treasury-yield-curve table (2-yr/10-yr/30-yr, framed
  explicitly around the session's Columbus Day bond-market closure) at the
  end of Section 4, rather than a padding table that repeats existing rows.
  One render-and-inspect round was enough to confirm the fix. **This
  continues to validate the standing guidance: when page 3 is short, add
  genuine content first, don't loosen the CSS** — the tightened edition-39
  CSS baseline was left untouched and still rendered comfortably at 4 pages
  once the added table filled the gap.
  Continue checking for both failure modes (short page 3, overflow) after
  every render regardless of recent-edition track record.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable for that edition's unusually
high content volume, treat as the new default and only loosen it back toward
the old values if a future edition renders with noticeably excessive
whitespace at these settings)
- Letter size. Body **8.0pt** / line-height **1.20**, serif; `p`
  margin-bottom **1.6px** (tightened from 2.4px at edition 39).
- h1 14.5pt; h2 **9.1pt, margin 3px 0 1.2px 0, padding-bottom 0.6px**
  (tightened from `4px 0 1.6px 0` / `1px`); h3 **7.9pt, margin 1.8px 0 0.8px
  0** (tightened from `2.4px 0 1px 0`).
- Tables **7.4pt**, **1.0px cell padding** (tightened from 1.8px), table
  margin-bottom **2px** (tightened from 3px).
- Snap-grid tiles: 7.4pt label / 9.4pt value / 7.3pt change; tile padding
  **2px 4px**, snapgrid margin-bottom **3.5px** (unchanged — tiles were not a
  contributor to edition 39's overflow).
- Bullet lists (`ul.bullets`): **1.0px** margin-bottom per `li` (tightened
  from 1.4px).
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
  doesn't fill the page. Needed at editions 25, 28, 36 and **40** (36 and 40
  both via a Treasury yield-curve table variant — edition 40's used the
  Columbus Day bond-market closure as the natural framing); not needed at
  most other editions, including 34, 35, 37 and 38; **39 was the opposite
  problem (overflow, not a short page)**, so this padding table was never
  relevant there. Always
  re-render immediately after adding (or removing) any content to confirm
  the page count, rather than assuming a change is safe. **If a future
  edition is short on page 3 at the new tightened CSS baseline, the first
  lever to pull is adding genuine content (the padding table above), not
  loosening the CSS back toward the old baseline — only loosen the CSS if
  several consecutive editions all run short, suggesting the tightening
  overshot.**

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across fifteen eligible
editions, 25 through 40, with editions 34 and 39 the exceptions when fresher
CFTC data was available). Fresh CFTC CoT data on a Monday/weekend-window
edition → the ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart,
normalized as % of open interest — this has now happened twice (edition 34,
edition 39); editions 35 through 38 and **40** all had no fresh CoT data due
and correctly reverted to the sector-ETF-proxy default (edition 40: Energy
+1.43% led, Technology -1.22% lagged, 8 of 11 sectors green). **Editions 41
through roughly 43 should also default to the sector-ETF-proxy chart**
(next CFTC report due Fri 16 Oct, covering Tue 13 Oct data — won't post
until the edition covering that Friday session, likely around edition 44).
A single dominant earnings print with a
clean, well-sourced implied-vs-realized-move story → a three-bar implied/
historical-average/realized move chart (the historical-average leg has never
actually been sourced successfully). A genuine multi-sector broadening/
deepening selloff across consecutive sessions → the sector-ETF proxy
rendered as a grouped (day-over-day) bar instead of single-day. A holiday-
window preview edition with no fresher data → VIX futures term structure
with event annotations. When chart 1 (movers) already covers the earnings/
single-name story, the sector proxy (or, when fresh, the CFTC positioning
chart) is a good complementary choice even on a stock-heavy day, since the
two stories reinforce rather than duplicate each other — **edition 39 used
a dominant single-stock/sector story (SpaceX spectrum deal, telecom/tower
REITs) for chart 1 and the CFTC positioning data for chart 2, which worked
well as genuinely independent, complementary stories.** Chart #2's placement
in the document should follow its content, not a fixed section — editions
24, 34 and **39** all placed a CFTC/positioning chart #2 in Section 5
(Derivatives) rather than Section 2; editions 35 through 38, all back on the
sector-proxy default, placed it back in its usual Section 2 spot. Continue
checking CoT freshness first each Monday/weekend-window edition rather than
assuming either chart type is now the permanent default for that edition
type. **Remember the figsize-scales-to-category-count guidance above
(ceiling `(9.8, 1.95)` for an 11-category panel, scale down for fewer
categories) regardless of which chart type is chosen.**

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–38 (condensed):** established the format (edition 1 baseline;
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
(resolved edition 37 via local text-extraction). Edition 37 (Thu 8 Oct,
covering Wed 7 Oct): the FOMC minutes (released 2:00pm ET inside the window)
showed a unanimous 12-0 September hike but only "most" not "all" backing a
further 2026 move; equities retreated broadly on a bond-market selloff (S&P
500 -0.2% to 7,801.77, Dow -0.7%, Nasdaq -0.2%, Russell -1.3%), Industrials
led losses on an unexplained Caterpillar -5.75% (driver resolved edition 38);
Skydance Corporation's first clean post-transition close under ticker SKYD
was -6.72%; Applied Digital -6.04% intraday ahead of an after-the-close
fiscal Q1 beat (revenue +322% y/y); the AI-optics trade (AAOI, COHR, LITE)
reversed Tuesday's rally with no fresh catalyst found; a primary-source
breakthrough on the Bank of Japan (local `pdftotext` extraction) revealed
the Sept 18 hike passed 7-2, not unanimous, with two named dissenters; three
standing conflicts were all resolved this edition (US-China tariff
list-size, the 2-year Treasury's 33bp gap, GBP/USD's three-way conflict);
WTI and Brent both hit a sharp level-vs-%-change reconciliation failure
across three independent vendors; a genuine chart-layout bug was found and
fixed (panel2's figsize bumped from `(9.8, 1.55)` to `(9.8, 1.95)` after
overlapping y-axis labels were caught on visual inspection). Edition 38 (Fri
9 Oct, covering Thu 8 Oct): equities fell a second straight session but
breadth stayed strong (S&P 500 -0.5% to 7,765.36, Dow +0.1% to 51,231.64 the
only major average higher, Nasdaq -1.3% to 27,193.34, Russell flat +0.03%);
a second straight session of AI-optics profit-taking (AAOI -13.58%, COHR
-9.63%, LITE -5.62%) was the main drag; Caterpillar's Wednesday -5.75%
mystery resolved (FTC/USDA farm-equipment antitrust inquiry); Applied
Digital's blowout fiscal Q1 print drew a muted reaction and logged the
first non-GAAP-vs-GAAP EPS conflict trap (a secondary "+1¢" figure excluded
in favor of the 8-K's GAAP loss); the first post-FOMC-minutes hike-odds read
showed approx. 16-17% Oct, essentially unchanged; Kalshi's failure mode
changed from a Vercel checkpoint page to a plain HTTP 429; a primary-source
breakthrough closed BoJ's last standing gap (next meeting Oct 29-30, direct
fetch); oil's vendor-%-reconciliation failure became a well-established
durable pattern; zerogex logged three within-session anomalies (stale SPX
snapshot, SPY scale discontinuity, QQQ conflict) as a new data-quality trap,
two of which (SPY, QQQ) later proved to be one-offs. 28 sources, clean
28/28 on the second `check_refs.py` pass, zero stray tildes, clean 4-page
render on the first attempt.

**Edition 39 (condensed)** — Monday 12 October 2026 report covering Friday
9 October 2026 (a weekend-window edition, research window Thu 8 Oct 20:00
ET through Sun 11 Oct 20:21 ET). SpaceX's approx. $8bn purchase of Grain
Management's 800MHz spectrum for Starlink Mobile rattled telecom (T-Mobile
-13.27%, AT&T -9.81%, Verizon -8.75%, Crown Castle +15.60% on the
infrastructure read-through), but equities shrugged it off, closing a
record-setting week: S&P 500 +0.6% to 7,811.54, Dow +0.8% to 51,654.95,
Nasdaq Composite +0.6% to 27,366.17, Russell 2000 +0.5% to 2,806.98, 9 of 11
sectors green. A parallel broad biotech rally ran alongside it (Moderna
+14.21% on joining the Nasdaq-100, Novavax +15.80%, Humana +11.56% on a
Star Ratings beat); Fastly (+15.86%) and a second unexplained AI-optics
session (AAOI/COHR/LITE) both remained open threads with no driver found.
Delta's 8-K cleanly disclosed both GAAP ($1.15) and adjusted ($1.72) EPS
alongside a guidance cut to $5.10-5.60, stock closed flat; Goldman upgraded
Palantir to Buy, the first normal analyst-action result after two
near-empty editions. Standing facts all re-verified unchanged (Warsh a
ninth straight confirmation, FOMC Oct 27-28, BoE/BoJ next meetings,
shutdown funding through 11 Dec via a genuine direct whitehouse.gov fetch);
October-hike odds flat at approx. 16%/Dec 73-74%; China Sept CPI/PPI still
pending, with an unverified Golden-Week-delay hypothesis surfacing. Oil,
gold spot, silver spot, DXY and Henry Hub all needed the logged-prior-close
computation method (WTI's vendor base still didn't reconcile, but Brent
reconciled cleanly for the first time); USAGOLD confirmed a permanent dead
end via the Wayback Machine's Availability API; Kitco failed for the first
time in many editions. CBOE's two known bugs resurfaced after four clean
editions; VIX9D-VIX inversion widened back to -3.58; zerogex's SPX
stale-snapshot caveat recurred for a second edition (now treated as
structural); CFTC CoT posted fresh data for the first time since edition 34
(ES/NQ/RTY Asset-Manager-long/Leveraged-Funds-short), powering a
Section-5-placed positioning chart; SOFR 3.87% (Oct 8). A chart-sizing
refinement (figsize scaling to category count, e.g. `(9.8, 1.65)` for a
7-category chart vs. the `(9.8, 1.95)` 11-category ceiling) and a deliberate
CSS retightening were needed to fix a genuine 5-page overflow across six
render-and-inspect rounds on an unusually content-heavy session. 42 sources,
clean 42/42 on `check_refs.py` after two Annex-B-only additions were caught
and given inline citations, zero stray tildes.

**Edition 40 (most recent — full detail)** — Tuesday 13 October 2026 report
covering Monday 12 October 2026, the window's one NYSE session (Columbus
Day — equities and commodities traded a full session, but the Treasury
market and SOFR/EFFR/OBFR fixings were closed), research window Sun 11 Oct
2026 20:00 ET through Mon 12 Oct 2026 20:21 ET. Verified the two structural
header rules again — now clean across eight (date-line) and twelve
(window-line) consecutive applicable editions respectively (see the header
rules section above for the running counts).

The session's dominant story was a genuine value/growth split driven by a
renewed memory-chip and AI-hardware selloff: the Dow added +0.38% to a
record 51,850.55 while the Nasdaq Composite fell -0.44% to 27,245.90 and the
S&P 500 slipped -0.06% to 7,807.24 (Russell 2000 -0.45% to 2,794.48) — all
four figures reconciled exactly against Friday's logged closes despite AP's
wire needing recovery via a search-engine snippet after both a direct fetch
and two syndication mirrors returned HTTP 403 (cross-checked against Yahoo
Finance/Motley Fool and stockanalysis.com, all agreeing). CNBC named
memory-chip weakness (Micron -3.88%, Sandisk -5.97%, also Marvell -3.42%,
Intel -3.20%, Nvidia -1.29%, Nokia -4.44%) as the specific drag, pulling
Technology to -1.22% even as 8 of 11 SPDR sectors closed green (Energy
+1.43%, Cons. Staples +1.17% led; Industrials -0.06% and Cons. Discretionary
-0.51% also lagged). A second, sharper AI-hardware/photonics pullback hit
smaller names hard: Cerebras -10.69%, Semtech -10.15%, Ciena -9.95%,
Lumentum -9.78%, Applied Optoelectronics -8.17% and Coherent -7.87%, none
with a confirmed company-specific driver; Fastly fell -9.80%, reversing
nearly all of Friday's unexplained +15.86% spike, extending that open
thread to a second session and adding three new names (CBRS, SMTC, CIEN) to
the same unexplained-AI-hardware-selloff bucket. FIGS was the session's lone
large gainer (+12.42%) on an unconfirmed "positive industry review" driver;
FICO (+10.85%) and CCC Intelligent Solutions (+8.12%) were both excluded
from the body as single-aggregator-sourced, the same discipline edition 39
applied to Palantir's price. Telecom (T, TMUS, VZ, CCI) bounced without a
confirmed catalyst and Moderna fell -5.00% with no Monday-dated news — both
reported without a driver rather than a guessed one. No major US company
reported earnings Monday; no analyst action dated specifically to 12
October could be confirmed for any name, a full reversion to the
edition-37/38-style empty-result pattern after edition 39 broke it.

Standing facts were re-verified fresh with two notable items: Kevin Warsh
remains Fed Chair (a tenth straight direct re-confirmation), next FOMC
27-28 October and BoE's 5 November decision both re-confirmed directly, and
the shutdown/CR status (funded through 11 Dec) re-confirmed via the same
dated whitehouse.gov permalink technique — all unchanged. **BoJ's
next-meeting verification stepped down to secondary-only corroboration**
(securities.io, MNI) rather than the direct boj.or.jp plain-text read
achieved at editions 38-39 — the fact itself (Oct 29-30, approx. 1.25%) is
not in doubt given multiple consistent secondaries plus two prior direct
confirmations, but re-attempt the direct read at edition 41 to restore the
stronger method. Rate-path odds firmed modestly hawkish for the first
directional move in several editions: DeFi Rate's Monday 8:24pm ET snapshot
showed October hike odds approx. 18% (up from Sunday's approx. 16%) and
December approx. 75% (up from approx. 73-74%) — still within normal noise,
but worth watching at edition 41 given Sept CPI lands Wed 14 Oct. Kalshi's
direct fetch returned HTTP 429 for a fourth consecutive edition. China's
September CPI/PPI still had not posted per a direct stats.gov.cn fetch; the
Golden-Week-delay hypothesis was not re-tested this edition (time
constraints).

Commodities and FX delivered the best reconciliation read in this report's
history: **WTI (-0.92%) and Brent (-0.86%) both matched their own
vendor-stated % exactly — the first clean dual-grade reconciliation ever
logged** (after editions 35, 37, 38 showing both-grade or WTI-only failures,
and edition 39 narrowing it to WTI-only). Gold spot, silver spot, Henry Hub
and DXY all needed the logged-prior-close computation method again, this
time with a specifically identified mechanism: each vendor's own
daily-change field was based on Sunday's thin pre-open print rather than
Friday's actual close. Copper computed +0.91% to $14,822.00/tonne via
Westmetall (no vendor % field to compare). USD/JPY moved in the same
direction as DXY for a second consecutive session, extending Friday's pause
in the divergence pattern — still not graduating to "expected by default."
Kitco's gold/silver quotes worked again, breaking its two-edition failure
streak (38-39), though used only as secondary color pending a disclosed
prior-close reference. GBP/USD and EUR/USD were both single-sourced cleanly
to Investing.com with no conflict found.

CBOE's delayed-quotes feed gave a clean, fresh sweep (VIX 15.21, +2.49%
manually computed; VIX9D 11.68, +3.73%) with **both of the feed's known
calculation bugs ABSENT** this edition — the manual recompute matched the
feed's own percent field across all six series for the first time in
several editions, though this does not mean the bugs are fixed (they
recurred at 39 after four clean editions, so remain genuinely intermittent).
The VIX9D-VIX inversion narrowed slightly to -3.53 from -3.58. **zerogex's
SPX dealer-gamma read hit a harder failure than the prior stale-snapshot
caveat**: the direct API call returned an authentication-required error and
the public page showed only blank placeholder values with no timestamp at
all — no usable SPX gamma figure was obtained this edition, a new standing
failure mode added alongside the existing staleness caveat. The CFTC's
Commitments of Traders report carried no fresh data this window as
expected (confirmed via cftc.gov's own release schedule, next due Fri 16
Oct); SOFR remained frozen at 3.87% (Oct 8) — a genuine two-session gap, not
the normal one-day lag, since Columbus Day delayed the Oct 9 fixing.

Production notes: a genuinely new chart bug was found and fixed — the
`barh()` helper's default `pad_frac=0.12` let the longest bar's value label
overflow into the y-axis tick-label margin on both of this edition's charts;
raising `pad_frac` to `0.26` cleared it on re-render, confirmed by visual
inspection. A short-page-3 recurrence (roughly 40% blank below the
sector-setup bullets) was fixed in one round by adding a genuinely new
Treasury-yield-curve table at the end of Section 4, framed around the
session's Columbus Day bond-market closure — consistent with the standing
guidance to add real content rather than loosen the CSS. 34 sources, clean
34/34 on `check_refs.py`'s first pass, zero stray tildes, clean 4-page
render.

**Open threads for edition 41:** Fastly, AAOI, COHR, LITE, Cerebras, Semtech
and Ciena all need a delayed-driver check — seven names now in the
unexplained-AI-hardware-selloff bucket across two sessions, following the
Caterpillar precedent (resolved one edition late at 37→38). BoJ's
next-meeting verification should return to a direct boj.or.jp plain-text
fetch rather than resting on secondary corroboration. The USD/JPY-vs-DXY
divergence has now paused for two straight sessions — watch whether it
resumes at edition 41 rather than assuming either outcome. China's
September CPI/PPI remains unresolved on both data and release date — check
stats.gov.cn directly at edition 41, and if time allows, properly source
the Golden-Week-delay hypothesis rather than continuing to carry it
unsourced. zerogex's new auth-gated/blank SPX failure needs a second data
point at edition 41 to determine if it's the new baseline or a one-off.
Rate-path odds ticked up for the first time in several editions (approx.
18% Oct/75% Dec) — watch whether this extends once Wednesday's CPI lands.
FICO, CCC Intelligent Solutions, Meta's cited AI-product driver and
Salesforce's cited analyst-upgrade driver all remain unconfirmed — check
for delayed corroboration. The next CFTC CoT report (Friday 16 October,
covering Tuesday 13 October) will not fall inside edition 41's window —
continue the sector-ETF-proxy chart #2 default through roughly edition 43.
TSMC's Q3 earnings call (Thursday 15 October, approx. 2:00am ET) and
Tuesday's bank-and-healthcare earnings kickoff (JPMorgan, Goldman Sachs,
Citigroup, Wells Fargo, Bank of America, Morgan Stanley, Johnson & Johnson,
UnitedHealth) are the week's next big equity catalysts — check follow-
through and actual results. Wednesday 14 October's September CPI is the
week's key macro catalyst, directly ahead of the 27-28 October FOMC
meeting. The New Mexico v. Meta penalty ruling (expected approx. 22 Oct)
remains a flagged catalyst, not yet revisited. University of Michigan's
final October consumer-sentiment reading is due 23 October. Threads closed
after resolution rather than carried further: AP's sourcing problem (closed
via search-snippet recovery, new technique logged); the oil
vendor-%-reconciliation problem (closed for this edition, both grades
clean — but don't assume fixed, see Hard Rules); Kitco's two-edition
failure (closed, resolved as a blip); the chart label-overlap bug (closed,
`pad_frac` fix logged); the short-page-3 recurrence (closed, Treasury-yield
table added); USAGOLD (remains closed permanently, see Known-
hard-to-source above).
