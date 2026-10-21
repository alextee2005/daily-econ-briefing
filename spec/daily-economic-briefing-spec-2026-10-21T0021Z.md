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
  through 46 have all applied this correctly** ("Friday 2 October 2026"
  through "Wednesday 21 October 2026" as the date line in each respective
  edition, with the window line carrying the session(s) covered) — now
  confirmed stable across fourteen consecutive editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 46 all reused the
  same pattern — now confirmed clean across eighteen consecutive editions (29
  through 46; edition 46 phrased it "Window: Mon 19 Oct 2026 20:00 ET – Tue 20
  Oct 2026 20:21 ET (Tue 20 Oct close/AH, the window's one NYSE session)"). No
  further confirmation needed; treat this as settled.

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
  with the Committee stressing data-dependency meeting to meeting.
- **Next FOMC meeting: October 27–28, 2026 — now less than a week out from
  edition 46's cutoff.** Decision expected approx. 2:00pm ET; press
  conference confirmed at **2:30pm ET on Oct 28** via federalreserve.gov's
  monthly events calendar (`federalreserve.gov/newsevents/2026-october.htm`
  — this `newsevents/YYYY-month.htm` URL pattern is the one that works for
  meeting TIMES; `fomccalendars.htm` only shows dates, not times).
  Re-confirmed again at edition 46 via federalreserve.gov directly. Following
  meeting: December 8-9, 2026 (an SEP meeting). **The next edition whose
  covered session falls on or after Oct 27-28 should lead with the
  decision.**
- **Rate-path odds at edition 46 (DeFi Rate's Kalshi/Polymarket-blended
  aggregator, fetched at Tuesday 20 Oct's approx. 8:21pm ET cutoff):** October
  27-28 hold approx. **87%** (hike approx. 13%), essentially flat to slightly
  firmer than edition 45's 84-86% hold range. **December 8-9 odds were a
  genuine data gap at edition 46, not carried forward** — DeFi Rate's site did
  not surface a usable blended December figure this run; this was disclosed in
  Annex A rather than reusing edition 45's stale 73-81% hike figure as if
  current. Re-attempt a full fetch, specifically checking the December
  sub-view, at edition 47. **Kalshi's own direct fetch failed again (HTTP 429)
  at edition 46, now ten consecutive failures (37-46).** Official CME FedWatch
  also failed again directly (timeout) at edition 46, a **sixth** consecutive
  failure (41-46). The composite "at least one more hike in 2026" read has
  still not been freshly re-pulled since edition 38 (last known approx. 80%)
  — don't cite without a fresh pull.
- **US-China "30-for-30" tariff framework — closed thread as of edition 37, do
  not re-open:** 77 US product categories (household goods, textiles,
  appliances, toys, sporting goods, vacuum flasks) and 1,619 Chinese
  categories (dominated by food/farm goods, plus some medical devices;
  soybeans, chips, EVs and batteries excluded from both sides), each side's
  treatment benchmarked at approx. $30bn against 2024 bilateral trade,
  confirmed directly against whitehouse.gov's own Terms of Reference
  document. **Implementation-notice sub-question remains open:** edition 46
  made a fresh direct attempt and still did not find an implementation
  notice, but found a new lead worth chasing. The Federal Register's public
  API (queried directly, bypassing the search UI's bot-check/unblock wall)
  returned only unrelated Section 301 China filings dated 7 October 2026; a
  targeted query for reciprocal-trade/tariff-reduction terms since
  mid-September returned zero results. USTR.gov's press-release index (no
  longer 404ing, unlike edition 45) showed no October release on the
  framework itself, but surfaced a **27 September 2026 statement from
  Ambassador Greer on recommendations from a "U.S.-China Board of Trade"**
  — plausibly tied to the 30-for-30 mechanism's governing body, though edition
  46's fetch only returned the title, not the body text. **Edition 47 should
  pull the full text of this 27 Sept USTR statement directly** as the next
  concrete step, rather than repeating the same blind USTR/Federal-Register
  sweep. The framework itself remains fully resolved; only whether/when it has
  actually been implemented is open.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates, government funding status) from memory or from the prompt's own
  framing — verify it fresh from a primary source (federalreserve.gov,
  bankofengland.co.uk, boj.or.jp, kansascityfed.org, norges-bank.no,
  riksbank.se, banxico.org.mx, snb.ch, rba.gov.au, whitehouse.gov, etc.) every
  edition, exactly like any other data point. **Edition 46 re-confirmed Kevin
  Warsh as Fed Chair directly against federalreserve.gov's Board of Governors
  bios page — a seventeenth straight direct re-confirmation.** The BoE's next
  decision (Thursday 5 November, now under two weeks out) was freshly
  re-touched at edition 46 via a direct bankofengland.co.uk fetch — unchanged,
  now confirmed directly for eight straight editions (39-46). The shutdown/CR
  status check remained on a clean direct primary-source footing at edition
  46: a direct whitehouse.gov fetch of
  `https://www.whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500/`
  again confirms H.R. 6500 funds federal agencies through **11 December
  2026**, no shutdown in effect — this URL pattern is now confirmed working
  for four straight editions (43-46); reuse it directly. **The BoJ's
  next-meeting-date primary source stayed confirmed via direct read at
  edition 46** (boj.or.jp's Monetary Policy Meeting schedule page, Oct 29-30
  2026, now six straight editions 41-46) — **edition 46 again could not get a
  direct numeric read of the current policy rate itself (approx. 1.25%) off
  boj.or.jp; a direct fetch of the Sept 18 policy-statement PDF
  (`boj.or.jp/en/mopo/mpmdeci/mpr_2026/k260918a.pdf`) returned undecodable raw
  PDF-stream data rather than extractable text, and the "What's New" page
  served a stale June snapshot.** This gap is now two straight editions
  (45-46) — try a PDF-text-extraction-capable fetch or a different
  rate/guideline-specific HTML page next time, since the raw-PDF approach has
  now failed twice.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed directly
  again at edition 46 (following decision 17 December 2026). Continue the
  direct-fetch discipline given the meeting is now under two weeks out.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano), both primary-sourced as of edition 37 — closed thread, do
  not re-derive. **The next policy meeting date (Oct 29-30, 2026) was
  re-confirmed via a direct boj.or.jp plain-text fetch again at edition 46**,
  now six straight editions (41-46) on the direct-fetch method; see the
  general-principle entry above for the numeric-rate caveat, now two straight
  editions open.
- **The four-central-bank Thursday 24 September 2026 cluster remains fully
  resolved — closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% but signalled a greater chance of
  a Q4 hike; Banxico held at 6.50% unanimously; SNB held at 0% and raised its
  inflation forecasts, confirmed directly against snb.ch.
- **The Reserve Bank of Australia's Tuesday 29 September 2026 decision remains
  fully resolved — closed thread, do not re-open:** hiked 25bp to **4.60%,
  unanimous**, a 15-year high and its fourth hike of 2026, confirmed directly
  against rba.gov.au's own Statement by the Monetary Policy Board.
- **August 2026 PCE inflation — closed thread, resolved at edition 32, do not
  re-open:** headline +0.3% m/m/+3.4% y/y, core +0.2% m/m/+3.0% y/y — a clean
  disinflation signal that proximately triggered edition 32's October-hike-odds
  collapse.
- **September 2026 jobs report — closed thread since edition 34, do not
  re-derive, but watch for revisions in later BLS releases:** nonfarm payrolls
  +29,000 (the weakest print of the cycle) vs. approx. 84,000-90,000
  consensus; unemployment rate 4.2%; average hourly earnings +0.1% m/m /
  +3.0% y/y; July revised to -10,000, August revised to +133,000 (a combined
  -60,000 revision), confirmed directly against bls.gov's Employment
  Situation Summary.
- **September 2026 ISM Services/Non-Manufacturing PMI — closed thread as of
  edition 35, do not re-derive:** headline 54.9% (down from August's 55.4%),
  Prices Paid 74.0% (+1.4pt, highest since July 2022). Confirmed directly
  against ISM's own press release.
- **September 2026 US CPI — closed thread as of edition 42, do not re-derive:**
  headline **+0.6% m/m / +3.7% y/y**, core **+0.3% m/m / +2.6% y/y**, both
  above the Dow Jones consensus of approx. 3.6%/2.5%, confirmed directly
  against bls.gov's CPI Summary release. This was the proximate trigger for
  edition 42's broad equity selloff, VIX spike and sharp October-hike-odds
  repricing.
- **September 2026 US PPI — closed thread as of edition 43, do not
  re-derive:** final demand **+1.3% m/m / +6.3% y/y** (NSA), the largest
  monthly gain since March 2022 and largest 12-month rise since December
  2022; the trade-services-excluded measure (BLS's closest analog to "core,"
  since BLS's September release does not publish a conventional ex-food/
  -energy PPI) was +0.5% m/m / +5.0% y/y. Energy (+10.8% m/m, gasoline
  +20.3%) drove over 80% of the goods-side increase. Confirmed directly
  against bls.gov. Notably, this hot print barely moved Fed rate-path odds at
  the time — and odds have since eased further (see rate-path-odds entry
  above), underscoring that CPI, not PPI, has been the proximate driver of
  this cycle's Fed-odds repricings.
- **September 2026 Import/Export Price Indexes — closed thread as of edition
  44, do not re-derive:** import prices **+1.1% m/m / +8.1% y/y** (the
  largest 12-month increase since July 2022), export prices **+2.2% m/m /
  +11.6% y/y**; export prices to China specifically +2.7% m/m (largest
  monthly rise since March 2022) / +7.5% y/y, import prices from China +3.1%
  y/y. Released Friday 16 October 2026, 8:30am ET, confirmed directly
  against bls.gov.
- **September 2026 Industrial Production & Capacity Utilization (G.17) —
  closed thread as of edition 44, do not re-derive:** total industrial
  production **+0.7% m/m / +2.2% y/y**, manufacturing output +0.3% m/m/+1.1%
  y/y, capacity utilization **76.9%**. Released Friday 16 October 2026,
  9:15am ET, confirmed directly against federalreserve.gov's G.17 release.
  The Fed flagged an annual benchmark revision to this series due 24 November
  2026 — watch for a level reset around that date, not a genuine month-over-
  month signal.
- **No US federal government shutdown is in effect — status re-confirmed on a
  clean direct primary-source footing at edition 46** (fourth straight
  edition on the exact URL pattern, 43-46; see general principle entry
  above). H.R. 6500 funds the government through **11 December 2026**. Watch
  for shutdown risk resurfacing as that date approaches.
- **University of Michigan preliminary October 2026 consumer sentiment —
  still not a "closed thread," watch for the final reading:** 46.3, a
  five-month low (current conditions 44.7, expectations 47.3, year-ahead
  inflation expectations 4.7%, long-run 3.5%), confirmed via
  investinglive.com and advisorperspectives.com, both dated 9 Oct 2026.
  **Final October reading due Friday 23 October 2026, 10:00am ET** (time
  confirmed directly against sca.isr.umich.edu at edition 46) — now just two
  days out from edition 46's cutoff; **edition 47 should watch for it
  directly if its window reaches Friday 23 Oct.**
- **China September 2026 CPI/PPI — RESOLVED at edition 42, closed thread, do
  not re-derive:** CPI **+0.9% y/y** (+0.2% m/m), PPI **+5.0% y/y** (the
  fastest PPI rise since June 2022), driven by fuel costs. Sourced to gov.cn's
  English-language NBS-attributed news release (stats.gov.cn itself remained
  stale/unreachable) — continue treating the gov.cn English release as an
  acceptable near-primary substitute if stats.gov.cn remains unreachable.
- **China Q3 2026 GDP — RESOLVED at edition 45, closed thread, do not
  re-derive:** printed **Monday 19 October 2026**, settling edition 44's
  disputed release-date (19 vs. 20 Oct) in favor of the 19th, confirmed
  directly against the National Bureau of Statistics' English-language press
  release at stats.gov.cn. Q3 alone: **+4.5% y/y, +1.2% q/q**; first-three-
  quarters 2026 cumulative: **+4.6% y/y** (GDP RMB 107,107.1bn).
- **New Mexico v. Meta — still an open thread, no specific ruling date
  confirmed:** the penalty-phase hearing (following the jury's late-September
  verdict that Meta violated the state's Unfair Practices Act roughly 43.9
  million times, re: hate-speech policy and its Cambridge Analytica response)
  was held Thursday 1 October 2026 before Judge Francis Mathew in Santa Fe.
  New Mexico is seeking **$35-40bn** in penalties (reduced from the statutory
  theoretical maximum of approx. $219bn at $5,000/violation); Meta is asking
  the judge to cap penalties at **$3.45bn**. Judge Mathew has indicated he
  expects to rule "later in October" 2026 — no outlet has given a specific
  date through edition 46 (re-confirmed no ruling had posted as of Tuesday 20
  Oct). **New detail surfaced at edition 46: on 9 October 2026 the judge
  granted Meta's unopposed motion to stay enforcement of any judgment once
  issued** — meaning New Mexico could not immediately collect even after a
  ruling lands; worth keeping in the briefing once a ruling is reported so
  readers don't assume immediate collection. The edition-45 judge-name
  discrepancy was not seen again at edition 46 — continue treating "Francis
  Mathew" as the established name absent a further corroborated correction.
  This is a distinct proceeding from the March 2026 child-safety jury verdict
  ($375m, before a different judge, Bryan Biedscheid) and the August 2026
  abatement ruling ($567m, same Biedscheid case, under appeal) — don't
  conflate the three. **Still open — watch for the actual ruling, do not cite
  a specific expected date until one is corroborated.**
- **New calendar-awareness item from edition 40, reconfirmed relevant at
  edition 41: "equities-open, bonds-closed" US holidays need an explicit
  check every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. **Next candidate to verify when it lands: Veterans Day, Wed 11 Nov
  2026 — confirm whether that is also bonds-only before assuming.**
- **The vendor-retroactive-revision trap hit its broadest case yet at edition
  46: THREE instruments revised simultaneously, not the usual single rotating
  offender.** Gold, silver and Henry Hub natural gas all showed their own
  Monday 19 Oct close revised upward by the vendor (Investing.com) versus what
  this report logged for Monday in edition 45 — gold $4,151.65→$4,160.10
  (softening -0.70% to -0.50%), silver $57.030→$57.273 (softening -0.48% to
  -0.06%), nat gas $3.042→$3.058 (softening -2.37% to -1.86%) — while each
  instrument's own Friday 16 Oct base (checked as a secondary cross-reference)
  stayed consistent, isolating the revision specifically to the Monday close
  in all three cases. WTI, Brent, copper, GBP/USD and the Treasury curve all
  reconciled cleanly against their edition-45-logged bases at edition 46;
  EUR/USD and USD/JPY showed only negligible (approx. 0.02pp) rounding-level
  differences, not true revisions. **Recommendation reinforced again:
  fresh-refetch every commodity/FX/Treasury prior-session base from the same
  vendor table every single edition — not just the instruments that drifted
  last time — and disclose every divergence found, however small. The locus
  keeps rotating (WTI at 45, gold/silver/nat-gas together at 46); there is no
  instrument that has proven permanently immune except copper and the
  Treasury curve (see their own entries below).**
- **Henry Hub natural gas returned to base ambiguity at edition 46** after
  breaking its streak cleanly at edition 45 — see the vendor-revision entry
  above (Monday base revised $3.042→$3.058). The November contract (NGX6) was
  still front-month at edition 46, not yet rolled to December. **This
  confirms edition 45's own caution not to treat one clean read as
  resolved** — the instrument has now shown ambiguity in six of the last
  seven editions; continue double-checking it fresh every edition.
- **The Kitco live-spot-vs-headline cross-check was NOT attempted at edition
  46** (Investing.com's history tables sufficed for a clean gold/silver read
  once the vendor-revision issue above was identified and disclosed) — no new
  data point on this recurring trap this edition; resume testing it when
  research-pass timing allows a same-day check.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company (owns AOL, Evernote,
  WeTransfer, Issuu and other consumer/SaaS apps), IPO'd 1 July 2026 at
  $29/share (above its $26-28 range), rising approx. 41% on debut to a
  approx. $25bn market value. Logged here so a future edition doesn't waste
  effort re-verifying the ticker's legitimacy if it moves sharply again.
- **The "named secondary outlet's own percentage-move headline can be flatly
  wrong" trap (first logged edition 44, J.B. Hunt/FreightWaves) is a standing
  caution, not a one-off:** treat any single-sourced, named-outlet
  percentage-move headline as a claim to verify against the underlying
  price-history table before using it, not as a citable fact on its own.
- **A reinforcing, non-novel reminder from edition 44: premarket indications
  are not the close, and earnings-day reactions can diverge from the simple
  EPS-beat/miss framing.** Three bank earnings reactions in one edition
  illustrated this: Truist's stock fell approx. 2.5% premarket on a large
  revenue miss but closed **up** 1.07%; M&T Bank beat on EPS and revenue yet
  **fell** 1.54% on NIM/provision deterioration; Regions Financial beat on
  EPS despite a slight revenue miss and rose modestly. Always fetch the
  actual verified close separately from any premarket quote, and look past
  the simple beat/miss framing to NIM, credit-provision and guidance detail
  when a reaction looks surprising.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent in BOTH
  directions — edition 46 saw the two AGREE for a second straight session.**
  DXY fell -0.18% and USD/JPY fell -0.13% Tuesday 20 Oct, both negative (both
  point to broad dollar softness), following edition 45's agreement (+0.13%/
  +0.33%, both positive) and edition 44's divergence (-0.22%/+0.01%). Keep
  disclosing the comparison every edition regardless of which way it goes —
  it is not a standing feature in either direction, though two consecutive
  agreements is worth watching for whether it's becoming more the norm.
- **A new single-aggregator-dependence pattern logged at edition 45, broader
  than the standing movers-list/analyst-action caution:** with no AP/Reuters
  wire posting for Monday 19 Oct by cutoff, nearly the entire equities
  section (most individual mover catalysts, both earnings' exact figures, and
  the full analyst-action roundup) traced to one outlet (Investrade's market
  review). Index closes and the clearest single-stock catalysts (Intel's
  JPMorgan upgrade, Amazon's Morgan Stanley "Top Pick") were independently
  corroborated via a second outlet; most individual mover catalysts and all
  earnings figures were not. **Continue flagging single-sourced items
  individually rather than treating a whole section as multi-sourced just
  because the closes/direction happen to be independently verified.**
- **A ticker-confusion / internally-inconsistent-aggregator trap, logged for
  the first time at edition 45:** a single aggregator's own writeup can be
  internally inconsistent, not just wrong relative to other sources. Edition
  45 found and excluded a reported "IAM" Monday mover whose own description
  was self-contradictory (described both a same-day IPO open and a prior
  Friday close) and, on independent checking, likely conflated Iambic
  Therapeutics' actual IPO day (Thursday 15 Oct) with Monday; and an
  unconfirmed PayPal "Cleveland" downgrade claim that could not be found in
  any other outlet and was contradicted by PYPL's own flat (-0.34%) close.
  Both excluded rather than repeated. **A single aggregator's own internal
  inconsistencies are a reason to exclude a claim, not just a cross-source
  conflict.**
- **GE Vernova's Wednesday 14 Oct -6.20% decline — CLOSED at edition 45 with a
  caveat, do not carry forward further.** A fourth genuine search attempt
  found a plausible but not fully confirming explanation: a modest
  Susquehanna price-target trim ($1,300 to $1,270 on 14 Oct, rating kept
  positive — too small alone to explain approx. 6%), profit-taking ahead of
  the stock's now-confirmed Oct 28 earnings date, lingering Wind-segment
  margin concerns, and that day's broad market selloff. No single hard
  catalyst (8-K, guidance cut, specific news event) was found. Closed per the
  Fastly precedent (edition 43) rather than pursued to a fifth attempt. Do
  not re-open unless genuinely new information surfaces unprompted.
- **Movers-chart outlier-capping label-overlap fix, logged at edition 45:** a
  spread this extreme (SLN +125.58% vs. next-largest CLF +16.34%, approx.
  7.7x; EYPT -85.28% vs. CLF, approx. 5.2x) found the existing capping
  mechanism's label text (a "(capped)" text suffix) long enough to visually
  overlap the y-axis tick labels even at pad_frac as high as 0.26-0.42 —
  because the label's anchor point sits just outside the capped bar while the
  text itself (unclipped by default in matplotlib) can still bleed into the
  tick-label margin. **Fix that worked: shorten the capped-value annotation
  from a "(capped)" text suffix to a single trailing asterisk
  ("+125.58%*"), and add one plain-language footnote to the chart's own
  x-axis label ("*bar capped at ±30pts; label = actual value") instead of
  repeating the word on every outlier's annotation.** This freed enough
  horizontal room that pad_frac=0.42 (the movers chart) rendered clean on the
  next attempt. **It is the label TEXT LENGTH, not just the padding
  fraction, that drives this overlap — use the asterisk+footnote pattern as
  the default for any future capped-outlier chart** rather than re-deriving
  pad_frac by trial and error. Separately, edition 45's 11-category sector
  panel (small magnitudes, all under approx. 2%) also needed a higher-than-
  default pad_frac (0.30 vs. the usual 0.12) to avoid an analogous overlap on
  its own largest-magnitude bar — **the needed pad_frac scales with how close
  the largest bar's label sits to the axis edge relative to the data's own
  span, not with category count**; check every chart's rendered PNG visually
  regardless of category count or past success.
- **A new trap, logged for the first time at edition 46: a secondary outlet's
  own qualitative SECTOR-level narrative can be flatly contradicted by actual
  ETF data, the same way a single-stock percentage headline can be.** One
  outlet's Tuesday 20 Oct recap framed Energy as the session's worst-performing
  sector and Communication Services as a Meta-driven laggard; a direct fetch of
  all 11 SPDR sector ETFs showed both claims false — Energy (XLE) closed
  +0.25% and Communication Services (XLC) +0.09%, both positive, with
  Technology (XLK, -0.28%) the actual sole laggard. **This generalizes the
  existing single-stock-headline-verification discipline to sector-level
  narrative claims: when a research pass reports a qualitative sector
  narrative without citing the underlying ETF figures, fetch all 11 SPDR
  sector ETFs directly rather than trusting the narrative framing** — this
  was feasible in well under the research window and should be the default,
  not a fallback only used when a conflict is suspected.
- **SpotGamma logged its own distinct dealer-gamma failure mode for the first
  time at edition 46 (tried as a zerogex.io alternative): a pure marketing
  homepage with no gamma levels, prices or dashboard content at all** (the
  real dashboard sits behind a dashboard.spotgamma.com login) — distinct from
  zerogex's own populated-landing-page/placeholder-dash mode (now a seventh
  straight failure for zerogex specifically, 40-46 with one mode-repeat).
  Both sources remain fully unusable; this is a data point for the running
  failure-mode log, not a reason to stop trying either source.
- **A primary-source-over-third-party-calendar lesson, logged at edition 46:**
  several third-party earnings calendars listed Meta Platforms' Q3 2026
  report date as 28 October 2026, but Meta's own investor-relations press
  release (dated 12 Oct, found via a direct search rather than a calendar
  aggregator) confirmed the actual date as **Wednesday 21 October 2026, after
  market close** — a full week earlier than the aggregators' consensus guess.
  **When a third-party earnings calendar's date looks load-bearing for the
  day-ahead section, check the company's own investor-relations announcement
  directly rather than trusting the aggregator consensus**, exactly as this
  report already does for macro-calendar facts.
- **Equifax's +11.33% Tuesday 20 Oct rally joins the standing
  "unexplained-magnitude" pattern (distinct from "beat yet fall"): a reaction
  size that looks too large for the underlying print.** Q3 adjusted EPS of
  $2.26 was roughly in line with an approx. $2.27 consensus, and FY guidance
  was actually cut slightly (EPS midpoint to $8.50) — yet the stock rose over
  11%. No analyst commentary explaining the magnitude was found. Logged as an
  open thread, not chased further this edition; revisit if bandwidth allows
  or if the pattern recurs on another name.

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
  uniqueness of use (editions 33-45 have all done this for stockanalysis.com
  single-stock closes and other repeatedly-used outlets, confirmed stable
  across thirteen editions). **Citing the prior edition itself as a source**
  (e.g. "[32] Daily Economic Briefing, edition 44, logged prior-session
  baseline figures") is a legitimate, already-used pattern when disclosing a
  divergence against a previously-logged figure — editions 43, 44 and 45 have
  all done this cleanly with `check_refs.py`.
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart 2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes). **Chart
  placement is editorial, not fixed to Section 2** — editions 24, 34, 39 and
  44 all placed a CFTC-positioning chart #2 in Section 5 (Derivatives) rather
  than Section 2, since that's where the content actually belongs; editions 45
  and 46 both reverted to the sector-ETF-proxy default in its usual Section 2
  placement since no fresher CFTC data was due inside either window (next
  report Fri 23 Oct, covering Tue 20 Oct data — should be fresh for whichever
  edition's window extends past 3:30pm ET that day).
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
  has occasionally failed to post in time. **Neither had posted for Tuesday 20
  Oct by edition 46's cutoff either — a second straight edition of this gap**
  — used two independent secondary outlets (Investing.com, Vistapglobal) plus
  an ETF-proxy cross-check (SPY/DIA/QQQ/IWM) plus a Reuters intraday snapshot
  via GV Wire syndication, all agreeing closely. Fall back to this tier
  (secondary outlet(s) + ETF-proxy triangulation, plus an intraday Reuters
  snapshot if a full closing wire isn't found) when AP/Reuters genuinely
  haven't posted, and disclose the fallback explicitly every time, not just
  the first time it happens.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Edition 44 found a new, stronger version of this trap: a
  FreightWaves headline's percentage-move claim for J.B. Hunt was not just
  mistimed but flatly contradicted by the stock's own verified close (claimed
  "+12%," actual close -2.78%).** Always check a dated article's own claimed
  magnitude against the underlying price-history table, not just its date,
  before repeating it. **Edition 45 found a related but distinct trap: a
  single aggregator's own writeup can be internally self-contradictory** (see
  the dedicated Standing Facts entry above on the "IAM" ticker-confusion
  case) — treat internal inconsistency within one source as its own reason to
  exclude a claim.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  **Edition 46 continued this discipline on two fronts:** individually
  verifying single-stock closes directly against stockanalysis.com (BRZE,
  EFX, NFLX among others) where the two secondary index-close outlets
  disagreed slightly on points-level index figures, and independently
  fetching all 11 SPDR sector ETFs directly rather than trusting a secondary
  outlet's sector narrative — which caught the Energy/Communication-Services
  narrative contradiction logged above. The exclusions this edition (the
  Moderna +6.7% claim, the "Salesforce shares slipped" claim) came from
  checking a headline percentage against the underlying closing-price table,
  not from a disagreement between two research passes.
- **Premarket is not the close.** Reinforced explicitly at edition 44 (see
  the dedicated Standing Facts entry above) after three bank-earnings
  reactions in one table diverged from their premarket indications or from
  simple EPS-beat/miss framing. Always fetch the verified close separately.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent in both
  directions** — see Standing Facts entry above for edition 46's second
  straight clean (non-divergent) reading. Continue disclosing the
  DXY-vs-USD/JPY directional comparison explicitly every edition regardless
  of which way it goes.
- **The Kitco live-spot-vs-headline cross-check was not attempted at edition
  46** — see the dedicated Standing Facts entry above. Resume attempting it
  each edition when research-pass timing allows a same-day check.
- **GBP/USD reconciled cleanly for a second straight edition (45-46); EUR/USD
  and USD/JPY showed only negligible rounding-level differences (approx.
  0.02pp), not true revisions, at edition 46** — the vendor-revision trap's
  locus moved to gold/silver/Henry Hub simultaneously instead this time (see
  the dedicated Standing Facts entry above). Resume the fuller multi-source
  method on any FX pair if a fresh same-day conflict reappears.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for ten further editions (37-46)** — edition 46 again found the full
  Treasury curve the one instrument class (alongside copper) that reconciled
  perfectly against the prior edition's logged base (2-yr 4.77%→4.79%, +2bp;
  10-yr 5.15%→5.12%, -3bp; 30-yr 5.48%→5.42%, -6bp; 2s10s 38bp→33bp, -5bp, a
  mild bull-flattening led by the long end). Treat as resolved/noise unless a
  fresh conflict appears.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 46 have all run clean (or
  clean after one quick fix) — **edition 46 ran clean 42/42 on the first
  pass, no fix needed**, continuing the established pattern of needing at
  most one quick fix pass.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 46 have all rendered with zero stray tildes on the
  first draft.** Edition 46 had none to fix.
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39 and 44 have all
  resolved this cleanly for CFTC CoT, with full OI and Asset-Manager/
  Leveraged-Funds breakdowns for ES, NQ and RTY. **Edition 46 confirmed
  directly (cftc.gov's `financial_lf.htm`) that no new report has posted
  since Friday 16 October** (still Tuesday 13 Oct's figures: ES OI 1,931,607,
  AM net approx. +47%/LF approx. -21%; NQ OI 279,515; RTY OI 444,784,
  unchanged from edition 45's logged figures, as expected). **The next CFTC
  report is due Friday 23 October 2026, 3:30pm ET, covering Tuesday 20
  October data** — check cftc.gov directly at edition 47 if its window
  extends past that release time, and re-evaluate chart #2 (fresh CFTC vs.
  sector-ETF-proxy default) based on what's actually available.
- **The diffuse-overflow lesson from editions 44-45 did NOT recur at edition
  46 — the first render landed cleanly at 4 pages with no trim rounds
  needed.** Worth noting as a data point that the diffuse-overflow failure
  mode is not inevitable; it correlates with how much prose/table content a
  session's volume demands, not a fixed feature of the CSS baseline. Continue
  re-rendering immediately after any content change regardless, and don't
  assume a clean first render means the CSS has more room than it does —
  budget for possible diffuse-overflow trims on a higher-volume session.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping. **Edition 46's
  spread (BRZE +51.70% vs. next-largest EFX +11.33%, approx. 4.6x) fell just
  under the 5x threshold, so no capping was needed** — a useful contrast with
  edition 45's 7.7x spread, which did need the asterisk+footnote fix. Confirms
  the threshold is being applied correctly in both directions, not just
  reached for by default.
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists.** Edition 46 again found a substantive list
  (a wire-reprint page citing 354 same-day rating changes) but, with no
  AP/Reuters wire available, it traced to a single aggregator — disclosed as
  such rather than treated as multi-sourced, continuing the pattern from
  edition 45. This sub-item continues to look genuinely intermittent in both
  yield and sourcing depth across editions 40-46 — report whatever a genuine
  search attempt turns up each edition, with its sourcing tier disclosed.
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38** — when a secondary-sourced EPS figure conflicts sharply with
  a primary filing's GAAP number without a stated basis, prefer the primary
  filing and flag the secondary figure in Annex A. **Edition 45 logged
  another clean non-trap confirmation of the contrasting, legitimate
  pattern**: Fifth Third Bancorp disclosed both a GAAP ($0.90) and an
  adjusted ($1.13) EPS figure clearly labelled in its own 8-K — reported in
  full per the established precedent, not treated as a conflict.
- **The "preview-consensus-only miss/beat framing" caution (first logged at
  edition 41, followed up without resolution at editions 42-44, not re-chased
  at edition 45) was again NOT actively re-chased at edition 46** — remains an
  open, unconfirmed disclosed inference carried forward. Pick this thread back
  up at a future edition if bandwidth allows.
- **GE Vernova's Wednesday 14 Oct -6.20% decline — CLOSED at edition 45, do
  not carry forward.** See the dedicated Standing Facts entry above.
- **Equifax's +11.33% Tuesday 20 Oct unexplained-magnitude rally — logged as
  an open thread at edition 46, not yet chased further.** See the dedicated
  Standing Facts entry above.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 46 all got a fresh,
  same-day-timestamped sweep** — nineteen consecutive fresh sweeps now.
  **The feed's two known bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) are genuinely intermittent, not a one-way ratchet: edition 44 saw
  both bugs hit every series simultaneously, while editions 45 and 46 both
  saw NEITHER bug on any of the six series (all percent fields matched an
  independent manual calculation exactly, two straight clean editions).**
  Freshness and bug-presence remain two independent axes. **Always compute
  day-over-day % change manually regardless of how many consecutive
  bug-free reads preceded the current one** — the bugs can return (or stay
  absent) without warning either way. VIX9D-vs-spot-VIX: edition 46 saw the
  term structure stay in contango (VIX9D 16.27 < VIX 17.31 < VIX3M 18.99 <
  VIX6M 20.74), compressing further as the whole complex kept unwinding (VIX
  -6.13%, VIX9D -9.26%, VVIX -9.15%) off Monday's already-reduced levels.
  Keep watching rather than assuming continuation of any prior trend.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 46 fetched all 11 directly rather than
  trusting a secondary outlet's narrative** (10 of 11 sectors green: Health
  Care +2.37%, Real Estate +1.70%, Utilities +1.26%, Financials +1.20%, Cons.
  Discretionary +0.91%, Cons. Staples +0.62%, Materials +0.55%, Energy
  +0.25%, Comm. Svcs +0.09%, Industrials +0.07% the gainers; Technology
  -0.28% the sole laggard) — this caught a secondary outlet's narrative
  claim that Energy/Communication Services were laggards, which the ETF data
  contradicted (see the dedicated new-trap entry in Standing Facts above).
  **Fetching all 11 ETFs directly is now the recommended default**, not a
  fallback only used when a conflict is suspected. Reverted to the
  sector-ETF-proxy chart as chart #2 again at edition 46 (no fresher CFTC
  data was due; next report Fri 23 Oct).
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (10 of 11 at edition 46) —
  continue treating an uncorroborated single-aggregator breadth figure as
  not usable.
- **Dealer gamma:** zerogex.io hit a **seventh consecutive edition of failure
  at edition 46** — the same populated-landing-page/placeholder-dash mode as
  editions 42 and 45. SpotGamma was tried as an alternative at edition 46 for
  the first time in a while and also failed, but in a distinct mode: a pure
  marketing homepage with no gamma levels or dashboard content at all (real
  dashboard behind a login at dashboard.spotgamma.com). Both sources remain
  fully unusable.
- **Official CME FedWatch probabilities:** the page blocks fetching (edition
  46's direct attempt timed out again, a **sixth** consecutive failure,
  41-46) — use secondary citations (Polymarket, Kalshi, Reuters/other
  economist polls, desk notes) and give a range rather than a single
  invented number. DeFi Rate's Kalshi/Polymarket-blended aggregator remains a
  stable, consistently working source for the near-dated (Oct) meeting
  across editions 37-46, but **edition 46 found its December sub-view
  specifically could not be pulled this run** — a genuine gap, not a
  structural failure of the whole source; re-attempt December specifically
  next edition.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, now **ten consecutive failures (37-46)** — a confirmed
  structural gap, not transient. Resume the attempt-every-edition discipline
  at edition 47 regardless, but expect a block of some kind. Use Kalshi's
  own secondary reporting or DeFi Rate's blended aggregator as the
  workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has not been
  re-attempted as primary since edition 35 beyond a routine confirming try.
  **Westmetall.com has now worked cleanly TWENTY-FIVE editions running**
  as the fallback (copper +0.30% to $14,540.00/tonne at edition 46, Monday
  base unrevised at $14,496.00/tonne, confirmed exactly). Copper remains,
  along with Treasuries, one of the two instrument classes that have never
  shown the vendor-revision trap.
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve CSV and the rendered HTML TextView page **agreed cleanly
  again at edition 46** (2-yr 4.79%, 10-yr 5.12%, 30-yr 5.42%, all 20 Oct),
  extending the clean streak to **eleven editions (37-46)** with no repeat of
  the edition-36 33bp gap. Keep fetching both endpoints and comparing rather
  than trusting either by default.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY). **Edition 46 confirmed directly that no new report
  has posted since Friday 16 Oct's release** (covering Tue 13 Oct 2026: ES
  OI 1,931,607, Asset Mgr net approx. +47%/Leveraged Funds approx. -21%; NQ
  OI 279,515; RTY full-size OI 444,784 — unchanged from edition 45's logged
  figures, as expected since no new data was due). **The next report is due
  Friday 23 October 2026, 3:30pm ET, covering Tuesday 20 October data** —
  check cftc.gov directly at edition 47 if its window extends past that
  release time, which is likely for most plausible edition-47 cutoffs;
  re-evaluate chart #2 (fresh CFTC vs. sector-ETF-proxy default) based on
  what's actually available.
- **GBP/USD and EUR/USD clean close:** both remain fully resolved since
  edition 37/26 respectively. **Edition 46 found GBP/USD unrevised for a
  second straight edition, and EUR/USD + USD/JPY both showed only
  negligible (approx. 0.02pp) rounding-level differences, not true
  revisions** — the vendor-revision trap's locus moved to gold/silver/Henry
  Hub simultaneously instead this time (see Standing Facts above). EUR/USD
  closed Tuesday at 1.1226 (+0.12% off a Monday base of 1.1212); GBP/USD
  closed at 1.3381 (+0.56% off a Monday base of 1.3306, exact match to
  edition 45's logged figure); USD/JPY closed at 158.29 (-0.13% off a Monday
  base of 158.50) — all single-sourced to Investing.com's close-to-close
  history table.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot-vs-headline cross-check was not attempted at edition 46**
  (Investing.com sufficed once the vendor-revision issue was identified) —
  see the dedicated Standing Facts entry above. Gold and silver futures
  continue to source via Investing.com, but **edition 46 found both
  instruments' own Monday 19 Oct closes had been revised upward since
  edition 45 logged them** (gold to $4,160.10 from $4,151.65; silver to
  $57.273 from $57.030) — see the dedicated vendor-revision Standing Facts
  entry above for the full write-up. Tuesday 20 Oct: gold -0.66% to
  $4,132.45, silver +1.14% to $57.928, both off the freshly-fetched Monday
  bases.
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is now also a closed thread as of
  edition 45 — see the dedicated Standing Facts entry above. **US
  import/export prices and industrial production:** both closed threads for
  September — see Standing Facts above. **University of Michigan final
  October consumer sentiment** (see Standing Facts above): due Friday 23
  October 2026, 10:00am ET — watch for it, now just two days out.
- **Henry Hub natural gas:** the November contract (NGX6) had NOT rolled to
  December as of edition 46 (still front-month). **The vendor-revision/base-
  ambiguity wrinkle, which broke its five-edition streak (40-44) cleanly at
  edition 45, returned at edition 46** — see the dedicated Standing Facts
  entry above for the full write-up; continue double-checking it fresh every
  edition, it has not stabilized either way.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 46 found no notable
  Tuesday-dated single-stock options-flow/skew commentary** for the
  session's largest chip/tech movers despite targeted searches — a **tenth**
  consecutive empty edition on this general sub-item (37-46). Treat this
  sub-item as reliably low-yield and keep it a brief, secondary effort each
  edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. Not
  applicable through edition 46; next due approx. 14 November 2026, now
  under four weeks out — start watching for it in editions covering early
  November.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22). Not attempted
  again through edition 46.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully
  again at editions 39, 44 and 45's confirming check (the latter covering
  Tue 13 Oct data, still the most recent as of edition 46's confirming
  check). Repeat this same three-instrument fetch at edition 47 when the
  Friday 23 Oct report should be available, watching for the Micro-vs-
  full-size Russell naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 46 again
  found a substantive list for Tuesday 20 Oct (one wire-reprint page citing
  354 same-day rating changes) but, with no AP/Reuters wire available,
  nearly all of it traced to one aggregator — disclosed as single-sourced
  rather than treated as independently confirmed. The pattern across 37-46
  (empty, thin, normal, empty, empty, empty, thin-but-real,
  empty-for-the-target-date, substantive-but-single-sourced,
  substantive-but-single-sourced again) continues to look genuinely
  intermittent in yield but increasingly consistent in sourcing depth
  (single-aggregator two editions running) — watch whether this becomes the
  norm rather than an intermittent pattern.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** Edition 46 individually re-verified single-stock closes
  directly against stockanalysis.com (BRZE, EFX, NFLX among others) where two
  secondary index-close outlets showed minor points-level disagreement —
  all matched. The exclusions this edition (the Moderna +6.7% claim, the
  "Salesforce shares slipped" claim) came from checking a headline percentage
  against the underlying closing-price table — continue this
  direct-verification discipline on high-confidence-seeming figures, not
  just surprising ones.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel
  (confirmed clean at editions 37 through 43 and again at 45 and 46, nine
  editions total) — this remains correct for 10-11 categories specifically.
  For charts with fewer categories, scale the height down: roughly
  `(9.8, 1.65-1.95)` for 3-9 categories (edition 46 used `(9.8, 1.9)` for an
  8-category single-stock movers chart). **Always render and visually
  inspect (via the Read tool) the actual PNG at or near full resolution
  before embedding it**, regardless of what a past edition's success might
  suggest.
- **Capped-outlier label-overlap fix (from edition 45, see the dedicated
  Standing Facts entry above for the full write-up):** when a capped bar's
  value label uses a "(capped)" text suffix, the label text can be long
  enough to visually bleed into the y-axis tick-label margin even at a wide
  pad_frac, because matplotlib's `ax.text()` is unclipped by default and the
  label's anchor point sits just outside the capped bar already. **Fix:
  shorten the per-bar suffix to a single trailing asterisk (`"*"` instead of
  `" (capped)"`) and add one footnote to the chart's x-axis label instead**
  (e.g. `"% change, Monday 19 Oct close [6] (*bar capped at ±30pts; label =
  actual value)"`). This remains the recommended default for any future
  capped-outlier chart — tune pad_frac for visual breathing room as before,
  but fix genuine text-overlap with shorter label text first, since a wider
  pad_frac alone did not fully resolve it at edition 45 (0.26 still
  overlapped; the asterisk fix combined with 0.42 finally rendered clean).
  **Edition 46's own movers spread (approx. 4.6x) fell under the approx. 5x
  capping threshold, so no capping was needed** — confirming the threshold
  works correctly in both directions, not just a trigger reached for by
  default. Separately, note that even a chart with small-magnitude data (e.g.
  an 11-category sector panel where every bar is under approx. 2.5%) can
  need a pad_frac well above the function's 0.12 default (edition 45 used
  0.30, edition 46 reused 0.30 successfully) — the needed value scales with
  the data's own span, not category count or chart type.
- **A grouped (two-series) horizontal bar chart — needed for the CFTC
  Asset-Manager-vs-Leveraged-Funds positioning chart — requires custom chart
  code, not the standard single-series `barh()` helper used for the
  movers/sector charts** (first built at edition 44). The standard helper
  only plots one value per category; the CFTC chart needs two bars (Asset
  Manager, Leveraged Funds) per category (ES/NQ/RTY), offset vertically by a
  fixed height fraction (`h=0.32` worked cleanly for 3 categories) around
  each category's tick position. **Fix that worked for the legend:** use a
  FIGURE-level legend (`fig.legend(handles, labels, loc="lower center",
  bbox_to_anchor=(0.5, 0.0), ...)`) combined with
  `fig.tight_layout(rect=(0, 0.1, 1, 1))` to reserve the bottom 10% of the
  figure for the legend, clear of the x-axis label — an axis-level legend
  placed too far below the axes will overlap the x-axis label text.
  Figsize `(9.8, 2.15)` (taller than the movers chart's 1.8-1.95 range)
  rendered cleanly. **Reuse this exact pattern** for any future
  grouped/multi-series chart rather than re-deriving the legend-placement
  fix from scratch.
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
  wrong. **A 5-page render is not always a stray break, and not always a
  single concentrated overflow — editions 44 and 45 were clear examples of
  DIFFUSE overflow, but edition 46 rendered clean on the first attempt at 4
  pages with no trims needed** (see the dedicated Hard Rules entry above) —
  diffuse overflow correlates with session content volume, it is not an
  inevitable feature of the current CSS baseline. Re-render after every
  content change regardless of which outcome you expect. **A large,
  suspicious blank area at the bottom of a page (as opposed to a page that's
  merely a bit short) is usually caused by an atomic block** — most often a
  chart `<img>` — not fitting in the remaining space and being pushed whole
  to the next page; editions 44, 45 and 46 have shown no instance of this
  pattern (when overflow occurs, content simply runs a fraction of a page too
  long across several blocks, not one pushed-whole block).
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix. Edition 46's
  combined "Commodities and FX" table (14 rows, folding in Treasuries) fit
  entirely on page 3 without needing to split across a page boundary.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  A visibly short page 3 (or in editions 44-45's case, page 4) has recurred
  at several earlier editions, each needing a genuinely additive fix (never
  a padding table that just repeats an existing table's rows) OR, as at
  editions 44-45, a genuinely diffuse set of small trims; **edition 46 needed
  neither — the first render was already well-filled across all 4 pages with
  no visibly short page.** Edition 45 converged after four rounds of
  edit-and-re-render, each round checked by
  re-rendering immediately rather than batching multiple guessed trims
  together — budget for this iterative pattern on any edition with a
  borderline page count.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across editions 40 through
46's very different content volumes (40 needed a padding table to fill page
3, 41 and 42 both filled naturally with no padding needed, 43 needed a
content TRIM to avoid overflow on a very high single-stock-volume session,
44 and 45 both needed several small content trims across multiple sections
to avoid a diffuse overflow (45 converging in four rounds vs. 44's five), 46
rendered clean on the first attempt with no trims or padding needed at all.
Treat as the durable default; the lever to pull on a high-volume or
diffusely-long day is merging/trimming redundant content across whichever
sections are longest, not loosening the CSS further.)
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
  3 pages). **An optional "Commodities & FX levels" table (~9-13 rows)** at
  the end of Section 4 is available as padding if page 3 runs short after the
  two default blocks — reach for it only when content alone doesn't fill the
  page; editions 44, 45 and 46 all folded commodities, FX and Treasuries into
  ONE combined table (10-14 rows) as the PRIMARY commodities table rather
  than padding, now the standing default rather than an edition-specific
  choice. **On a high-single-stock-volume earnings day (many reporters/movers
  in one session), the opposite problem is more likely — watch the movers
  table specifically for verbosity (multi-clause driver text, rows that could
  share a combined cell) before assuming the page budget is safe.** Edition
  46 had a high-earnings-volume Tuesday (3M, GM, GPC, Equifax, Hasbro,
  Netflix and more all reporting) and still rendered clean at 4 pages on the
  first attempt by keeping movers-table driver cells to one tight sentence
  each. Always re-render immediately after adding (or removing) any content
  to confirm the page count, rather than assuming a change is safe. **When
  overflow is small and diffuse (editions 44-45 pattern), trim a little from
  several sections rather than gutting one** — day-ahead table rows,
  earnings-table note cells, movers-table driver cells, sector-setup bullets
  and macro/derivatives/commodities prose paragraphs are all good, low-cost
  candidates to shave a clause or merge a row from first; edition 45 needed
  trims across eight distinct spots before the page count actually dropped
  from 5 to 4 (edition 46 needed none).

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across twenty-one eligible
editions, 25 through 46, with editions 34, 39 and 44 the exceptions when
fresher CFTC data was available; editions 45 and 46 both reverted to this
default since the CFTC's next report was not yet due inside either window).
Fresh CFTC CoT data on a Monday/weekend-window edition → the ES/NQ/RTY
asset-manager-vs-leveraged-funds positioning chart, normalized as % of open
interest, built with the grouped-bar technique documented under Production
notes, placed in Section 5 (Derivatives) per the editions 24/34/39/44
precedent. A single dominant earnings print with a clean, well-sourced
implied-vs-realized-move story → a three-bar implied/historical-average/
realized move chart (the historical-average leg has never actually been
sourced successfully). A genuine multi-sector broadening/deepening selloff
across consecutive sessions → the sector-ETF proxy rendered as a grouped
(day-over-day) bar instead of single-day. A holiday-window preview edition
with no fresher data → VIX futures term structure with event annotations.
When chart 1 (movers) already covers the earnings/single-name story, the
sector proxy (or a fresh CFTC positioning chart, when available) is a good
complementary choice even on a stock-heavy day, since the two stories
reinforce rather than duplicate each other — edition 46 used exactly this
combination on a high-earnings-volume Tuesday. **Edition 47 should check
cftc.gov's freshness first** (the Friday 23 Oct report, covering Tuesday 20
Oct) before defaulting back to the sector-ETF proxy — if CFTC data has
posted fresh by edition 47's cutoff (likely for most plausible cutoffs given
the 3:30pm ET release time), use the fresh CFTC chart per the established
technique; otherwise revert to the sector-ETF-proxy default as usual.
**Remember the figsize-scales-to-category-count guidance above (ceiling
`(9.8, 1.95)` for an 11-category panel, `(9.8, 2.15)` for the 3-category
grouped CFTC chart, scale down for fewer single-series categories) and the
capped-outlier asterisk/footnote fix when a spread does cross the approx. 5x
threshold (it did not at edition 46).**

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–44 (condensed):** established the format (edition 1 baseline;
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
15-16 FOMC meeting and its aftermath (editions 21-23):** the Fed hiked 25bp
to 3.75%-4.00% unanimous 12-0, equities reversed hard then rallied sharply;
BoE held at 3.75% (6-3). Edition 24: approx. $7tn September triple-witching
notional expired, Xenon Pharmaceuticals -30.7%, Buffett stepped down as
Berkshire chairman, BoJ hiked to approx. 1.25% (31-year high). Edition 25:
chip rally to a then-record Nasdaq. Edition 26: financials-led rotation, a
genuine Kitco-vs-USAGOLD gold split (later resolved). Edition 27: risk-off on
a 19-year 10-year yield high. Edition 28: a whipsaw near-flat session, MGM
-10.99% on a withdrawn take-private bid, Trump-Xi summit extended the
US-China trade truce. Edition 29: relief rally, the US-China $30bn
tariff-cut agreement first reported. Edition 30: broad risk-off on a
rejected Iran Hormuz offer, Kodiak Sciences +177.96% (the movers-chart
capping rule's first genuine case). Edition 31: DXY-vs-FX-crosses conflict
resolved cleanly. Edition 32: a volatile round-trip close, gold spot/futures
split (later converged). Edition 33: yields drove the session on a hot ISM
Prices Paid print, an AI-infra earnings cluster, Nike missed FQ1 guidance
(resolved edition 34); the document overflowed to 5 pages, needing five trim
rounds. Edition 34 (Mon 5 Oct, covering Fri 2 Oct + weekend): a badly-missed
September jobs report drove a broad risk-on rally and sharp October-hike-odds
collapse; a fresh CFTC CoT report powered the first ES/NQ/RTY positioning
chart. Edition 35 (Tue 6 Oct): two same-day cash buyouts (PTC Inc, RXO Inc)
drove the tape; equities hit a Nasdaq Composite record; September ISM
Services PMI printed hot; two new sourcing traps logged (stale price-target
recirculation, a stock-split "+96%" artifact). Edition 36 (Wed 7 Oct):
equities extended records on falling yields (clean rate-sensitive rotation);
two severe sourcing traps hit (fabricated AMD price targets, an unverifiable
WHO claim, both rejected); the Paramount Skydance/Warner Bros. Discovery
merger closed (ticker SKYD); a secondary source reversed the US-China tariff
list-size assignment (resolved edition 37); the 2-year Treasury hit a 33bp
cross-endpoint gap (resolved edition 37); GBP/USD hit a three-way conflict
(resolved edition 37). Edition 37 (Thu 8 Oct): the FOMC minutes showed a
unanimous 12-0 September hike but only "most" backing a further 2026 move;
equities retreated on a bond-market selloff; three standing conflicts all
resolved this edition; WTI and Brent both hit a sharp level-vs-%-change
reconciliation failure; a chart-layout bug was found and fixed (panel2
figsize bumped to `(9.8, 1.95)`). Edition 38 (Fri 9 Oct): equities fell a
second straight session but breadth stayed strong; a second straight
AI-optics profit-taking session; Applied Digital's blowout print drew a
muted reaction and logged the first non-GAAP-vs-GAAP EPS conflict trap; a
primary-source breakthrough closed BoJ's last standing gap; oil's
vendor-%-reconciliation failure became well-established; zerogex logged
three within-session anomalies as a new data-quality trap. Edition 39 (Mon
12 Oct, covering Fri 9 Oct + weekend): SpaceX's approx. $8bn spectrum
purchase rattled telecom but equities shrugged it off, closing a
record-setting week; a parallel biotech rally ran alongside it; Delta's 8-K
cleanly disclosed both GAAP and adjusted EPS; Goldman upgraded Palantir, the
first normal analyst-action result after two near-empty editions; a
chart-sizing refinement and deliberate CSS retightening were needed to fix a
genuine 5-page overflow. Edition 40 (Tue 13 Oct, covering Mon 12 Oct,
Columbus Day): a value/growth split on renewed memory-chip/AI-hardware
weakness; AP's wire needed search-snippet recovery; oil delivered its
cleanest-ever dual-grade reconciliation (later found to rest on a Monday
base itself retroactively revised); zerogex's SPX gamma hit a harder
auth-gated/blank failure mode; a chart-label pad_frac bug was found and
fixed (raised to 0.26); a short-page-3 recurrence was fixed with a new
Treasury-yield-curve table. Edition 41 (Wed 14 Oct, covering Tue 13 Oct,
the opening day of Q3 bank/healthcare earnings season): JPMorgan, Goldman,
Wells Fargo, Citigroup, UnitedHealth and Johnson & Johnson all reported;
JNJ's GAAP EPS collapsed to $0.09 on a one-time talc-settlement charge while
adjusted EPS and raised guidance were both disclosed cleanly; equities
finished essentially flat (S&P -0.02% to 7,805.45) via a clean AP wire
recovered through two syndication mirrors; Bumble's unexplained +56.58%
surfaced (resolved edition 42: a $1.3bn Ithaca Holdings buyout, not a
split); the AI-optics/AI-hardware selloff cluster finally found its delayed
driver (Broadcom CEO Hock Tan's remarks on AI-infrastructure capital-access
constraints); a new vendor-retroactive-revision trap hit WTI, Brent and
Henry Hub for the first time. 49 sources, clean 49/49 on the first
`check_refs.py` pass, zero stray tildes, clean 4-page render. **Edition 42**
(Thu 15 Oct, covering Wed 14 Oct): September CPI printed hot (headline
+0.6% m/m/+3.7% y/y, core +0.3%/+2.6%), triggering the broadest risk-off
session in weeks (S&P -1.11% to 7,718.94, Nasdaq -1.88%, Russell -1.90%,
only 3 of 11 sectors green); the Dow held almost flat (-0.09%). AP's wire
403'd again; closes recovered via CNBC/Yahoo/TheStreet. Bank of America's
GAAP EPS fell to $1.08 on a regulatory-settlement charge (adjusted approx.
$1.25); Morgan Stanley beat cleanly but still fell with the market.
CoreWeave (-15.46%) and Oracle (-8.83%) led decliners on renewed
AI-infrastructure-funding-stress; Fastly (-7.72%) and GE Vernova (-6.20%)
both went unexplained (GE Vernova resolved edition 45). Bumble's buyout
mystery resolved (Ithaca Holdings, $6.05/share). Rate-path odds repriced
sharply hawkish (DeFi Rate: Oct hike approx. 19%→29%, Dec approx. 78%).
China's September CPI/PPI finally posted via gov.cn's English NBS release.
Commodities swung hard: silver futures -6.14%, gold futures -1.06%, both
contradicted by a mistimed Kitco live spot quote — a new sourcing trap. The
Treasury curve flattened. The vendor-retroactive-revision trap broadened
further, for the first time hitting FX (EUR/USD, GBP/USD, USD/JPY). The VIX
complex spiked hard (VIX +10.48% to 16.87) with neither CBOE feed bug
recurring. zerogex hit a third, distinct failure mode. 49 sources, clean
47/49 on the first `check_refs.py` pass, zero stray tildes, clean 4-page
render. Edition 43 (Fri 16 Oct, covering Thu 15 Oct): a second straight
blowout inflation print (September PPI) barely moved Fed odds; an overnight
memory-chip rout reversed sharply on Nvidia CEO Jensen Huang's defense of
CoreWeave's balance sheet, all four indices closing green; TSMC's record Q3
still fell on cautious guidance; Ericsson's beat drove the session's largest
single-stock move (+11.80%); six of eleven commodities/FX instruments showed
a silently-shifted Wednesday base. Edition 44 (Mon 19 Oct, covering Fri 16
Oct + weekend): equities fell broadly Friday on renewed AI-infra. spending
doubts (Nasdaq -2.14%, its worst week since June); the VIX complex spiked
hard with both CBOE feed bugs appearing simultaneously for the first time;
five large movers had no confirmed catalyst; a FreightWaves "+12%" J.B. Hunt
headline was flatly wrong (actual close -2.78%); CFTC CoT posted fresh data,
powering the first grouped-bar positioning chart; the first HTML draft
overflowed to 5 pages, fixed over roughly five trim rounds.

**Edition 45 (condensed)** — Tuesday 20 October 2026 report covering Monday
19 October 2026. Equities rebounded broadly (S&P +0.41% to 7,690.73, Dow
-0.07% to 51,966.03, Nasdaq +1.11% to 26,430.89, Russell +0.25% to 2,728.30)
after the prior week's worst week since June, though breadth stayed narrow
(3 of 11 sectors green). Neither AP nor Reuters had posted a wire by
cutoff — a new fallback tier (CNBC live-blog + Investrade + SPY ETF-proxy)
was used and disclosed. Biotech produced the day's extremes: Silence
Therapeutics +125.58% on a Merck KGaA buyout, EyePoint Pharmaceuticals
-85.28% on a failed trial — both the most extreme single-session movers
logged to date, requiring the chart's first outlier-capping use and
surfacing a label-overlap bug (fixed via an asterisk+footnote pattern). Two
claims were excluded after failing corroboration (a self-contradictory "IAM"
mover claim, an unconfirmed PayPal downgrade), logging a new
ticker-confusion/internal-inconsistency sourcing trap. GE Vernova's Wed 14
Oct -6.20% decline closed with a caveat (Susquehanna PT trim, profit-taking,
Wind-margin concerns — no single hard catalyst). China's Q3 GDP release-date
dispute resolved (printed Mon 19 Oct, +4.5% y/y). Standing Fed facts all
re-verified unchanged; rate-path odds (DeFi Rate) eased only slightly (Oct
hold approx. 84-86%, Dec hike approx. 73-81%); Kalshi and CME FedWatch both
failed direct fetch again (ninth and fifth consecutive failures
respectively). The vendor-retroactive-revision trap's locus rotated to WTI
(Friday base revised approx. -2.4%) while EUR/USD and GBP/USD both
reconciled cleanly, ending a three-edition streak; Henry Hub also broke its
own five-edition base-ambiguity streak. DXY and USD/JPY agreed in direction
for the first time in several editions. The VIX complex unwound sharply off
Friday's spike (VIX -7.75% to 18.44) back into contango, feed clean. CFTC
CoT confirmed no new data as expected. The first HTML draft again rendered
at 5 pages from diffuse overflow, fixed through four small-trim rounds. 33
sources, clean 33/33 on `check_refs.py` after one quick fix, clean 4-page
render.

**Edition 46 (most recent — full detail)** — Wednesday 21 October 2026
report covering Tuesday 20 October 2026, research window Mon 19 Oct 2026
20:00 ET through Tue 20 Oct 2026 20:21 ET (the window's one NYSE session).
Verified the two structural header rules again — now clean across fourteen
(date-line) and eighteen (window-line) consecutive applicable editions
respectively.

**Equities rallied broadly** (S&P 500 +0.29% to 7,712.76, Dow +1.02% to
52,497.42, Nasdaq Composite -0.02% to 26,424.82, Russell 2000 +1.65% to
2,773.41) in a sharp rotation reversal from Monday: 10 of 11 SPDR sectors
closed green (Health Care +2.37%, Real Estate +1.70%, Utilities +1.26% and
Financials +1.20% led; Technology -0.28% the sole laggard), a near-mirror of
Monday's pattern. **Neither AP nor Reuters had posted a closing wire by
cutoff for a second straight edition** — two independent secondary outlets
plus an ETF-proxy cross-check plus a Reuters intraday snapshot (via GV Wire
syndication) were used instead, all agreeing closely. **A new trap was
logged: a secondary outlet's own qualitative sector narrative (Energy
worst-performing, Communication Services a Meta-driven laggard) was flatly
contradicted by a direct fetch of all 11 SPDR sector ETFs** (Energy +0.25%,
Communication Services +0.09%, both positive) — generalizing the existing
single-stock-headline-verification discipline to sector-level claims.
**A packed earnings Tuesday:** Salesforce agreed to buy Braze for $47.50/
share cash (BRZE +51.70%, no capping needed at a approx. 4.6x spread,
confirming the approx. 5x threshold works in both directions); Equifax
(+11.33%) and Hasbro (+11.20%) both jumped on raised/beat results, Equifax's
reaction size logged as a new open "unexplained-magnitude" thread (roughly
in-line print, slightly cut guidance, outsized rally); 3M (+5.78%) also
raised guidance. GM fell 6.84% despite beating on EPS/revenue and announcing
a $20bn buyback (cited commodity costs, soft truck demand) — another
beat-yet-fall instance. Netflix fell 1.66% regular session then a further
5.78% after-hours on soft Q4 margin guidance; SpaceX's after-hours figures
from one aggregator could not be confirmed against a primary filing. Two
secondary-source claims were checked against closing-price data and excluded
(Moderna's claimed +6.7%, actually flat; a "Salesforce shares slipped" claim,
actually flat). Standing Fed facts all re-verified unchanged (Kevin Warsh
Fed Chair, 17th straight direct confirmation; fed funds 3.75%-4.00%; FOMC
Oct 27-28 with the press conference at 2:30pm ET on the 28th; BoE holds
3.75%, next decision 5 Nov; no shutdown through 11 Dec). Rate-path odds
(DeFi Rate): Oct 28 hold approx. 87% (hike approx. 13%), little changed;
**December odds were a genuine data gap this run**, not carried forward as
if current. Kalshi (tenth straight failure) and CME FedWatch (sixth straight
failure) both failed direct fetch again. BoJ's numeric policy rate remains
only secondary-sourced for a second straight edition (a direct PDF fetch
returned undecodable binary data). The US-China tariff implementation notice
remains unresolved, but surfaced a new lead (a 27 Sept USTR statement on a
"US-China Board of Trade," not yet pulled in full). New Mexico v. Meta
remains pending; a new detail surfaced (a 9 Oct stay of judgment once any
ruling issues). **Commodities/FX: the vendor-revision trap hit its broadest
case yet** — gold, silver and Henry Hub's own Monday closes were all found
revised upward simultaneously versus what edition 45 logged (softening each
one's Monday decline), while WTI, Brent, copper, GBP/USD and the Treasury
curve all reconciled cleanly. DXY (-0.18%) and USD/JPY (-0.13%) agreed in
direction for a second straight session. The Treasury curve flattened
modestly (2s10s 38bp→33bp, a mild bull-flattening). **Derivatives: the VIX
complex extended its unwind** (VIX -6.13% to 17.31, VVIX -9.15%), staying in
contango, feed clean for a second straight edition. Dealer gamma: zerogex
hit a seventh consecutive failure; SpotGamma, tried as an alternative, logged
its own distinct failure mode (marketing-page-only). CFTC CoT confirmed no
new data as expected (next due Fri 23 Oct). Chart #2 was the sector-ETF-proxy
default again. **The first HTML draft rendered clean at 4 pages on the first
attempt — no trim rounds needed**, a contrast with editions 44-45's diffuse
overflow. 42 sources, clean 42/42 on the first `check_refs.py` pass, zero
stray tildes, clean 4-page render.

**Open threads for edition 47:** the US-China "30-for-30" tariff
implementation notice remains unresolved despite four editions (43-46)
checking directly against USTR.gov/federalregister.gov — edition 46 found a
new lead (a 27 Sept 2026 USTR statement from Ambassador Greer on "U.S.-China
Board of Trade" recommendations); **pull its full text directly next
edition** rather than repeating the same blind sweep. The CFTC CoT report
due Friday 23 October 2026 (covering Tue 20 Oct data) should land inside
edition 47's window if its cutoff extends past 3:30pm ET that day — check
cftc.gov directly and expect fresh data; re-evaluate chart #2 (fresh CFTC vs.
sector-ETF-proxy default) based on what's actually available. University of
Michigan's final October consumer-sentiment reading is due Friday 23
October, 10:00am ET — now just two days out, watch for it directly if
edition 47's window reaches that date. New Mexico v. Meta's ruling is still
pending, expected "later in October" per the 1 Oct hearing — watch for the
actual date/ruling, don't re-cite a specific expected date until confirmed;
note also the newly-surfaced 9 Oct stay-of-judgment order, worth mentioning
once a ruling is reported. Q3 Employment Cost Index is now confirmed for
Friday 30 October, 8:30am ET. The FOMC meets 27-28 October with its
press-conference time confirmed (2:30pm ET) — the next edition whose covered
session falls on/after the meeting date should lead with the decision; Meta
Platforms reports Q3 2026 results after Wed 21 Oct's close (today, just past
this window's cutoff) — watch for the reaction to feed into edition 47 if
its window reaches Thursday 22 Oct. BoJ's exact numeric policy rate (approx.
1.25%) was only secondary-sourced for a second straight edition at edition
46 — try a PDF-text-extraction-capable fetch or a different rate-specific
HTML page next time, since the raw-PDF approach has now failed twice.
December 2026 FOMC rate-path odds could not be freshly sourced at edition
46 — re-attempt a full DeFi Rate fetch, specifically checking the December
sub-view, at edition 47. Equifax's +11.33% Tuesday 20 Oct rally (roughly
in-line print, slightly cut guidance) is a new, not-yet-chased
unexplained-magnitude thread — attempt a search if bandwidth allows. GM's
-6.84% Tuesday 20 Oct beat-yet-fall decline and DaVita's -6.23% single-
sourced decline (a reported federal dialysis-competition plan) both remain
open, not yet independently corroborated beyond what edition 46 found. The
JPMorgan EPS-miss-framing and Wells Fargo/Citigroup credit-provision-selloff-
rationale threads from editions 41-42, and JPMorgan's Monday 19 Oct -1.82%
decline, all remain open, unconfirmed disclosed inferences — revisit if
bandwidth allows. The "preview-consensus-only miss/beat framing" caution
was not re-chased at edition 46 and remains open. 13F filings are due
approx. 14 November 2026, now under four weeks out — start watching for it
in editions covering early November. Threads closed after resolution rather
than carried further: GE Vernova's Wed 14 Oct -6.20% decline (closed with
caveat, edition 45); China's Q3 GDP release-date dispute (resolved, edition
45); Henry Hub's base-ambiguity (returned at edition 46 after one clean
edition — treat as still-open/intermittent, not resolved either way); the
Meta earnings-date conflict between third-party calendars (28 Oct) and
Meta's own IR announcement (resolved in favor of 21 Oct, edition 46).
