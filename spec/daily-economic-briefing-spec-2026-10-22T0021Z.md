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
  through 47 have all applied this correctly** ("Friday 2 October 2026"
  through "Thursday 22 October 2026" as the date line in each respective
  edition, with the window line carrying the session(s) covered) — now
  confirmed stable across fifteen consecutive editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 47 all reused the
  same pattern — now confirmed clean across nineteen consecutive editions (29
  through 47; edition 47 phrased it "Window: Tue 20 Oct 2026 20:00 ET – Wed 21
  Oct 2026 20:21 ET (Wed 21 Oct close/AH, the window's one NYSE session)"). No
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
  with the Committee stressing data-dependency meeting to meeting. (Note: the
  openmarket.htm policy-statement page itself does not list vote tallies — if
  a future pass checks that page instead of the minutes and doesn't see a vote
  count, that is not a contradiction; the minutes remain the authoritative
  source for the 12-0 figure, re-confirmed via that route as recently as
  edition 37.)
- **Next FOMC meeting: October 27–28, 2026 — now six days out from edition
  47's cutoff.** Decision expected approx. 2:00pm ET; press conference
  confirmed at **2:30pm ET on Oct 28** via federalreserve.gov's monthly events
  calendar (`federalreserve.gov/newsevents/2026-october.htm` — this
  `newsevents/YYYY-month.htm` URL pattern is the one that works for meeting
  TIMES; `fomccalendars.htm` only shows dates, not times). Re-confirmed again
  at edition 47 via federalreserve.gov directly. **New at edition 47: the
  Fed's blackout period was directly confirmed as Oct 17–29, 2026** (via
  Chicago Fed / St. Louis Fed blackout-period schedule pages) — the meeting's
  session window is now fully inside blackout, so no Fed speakers should
  appear on the calendar before the decision; don't expect or hunt for Fed
  commentary through edition 48 unless the decision itself has landed.
  Following meeting: December 8-9, 2026 (an SEP meeting). **The next edition
  whose covered session falls on or after Oct 27-28 should lead with the
  decision.**
- **Rate-path odds at edition 47 (DeFi Rate's Kalshi/Polymarket-blended
  aggregator, fetched at Wednesday 21 Oct's approx. 8:26pm ET cutoff):**
  October 27-28 hold approx. **88%** (hike approx. 12%), essentially flat vs.
  edition 46's approx. 87%. **December 8-9 odds were successfully pulled
  fresh this run** after edition 46's genuine data gap: blended hike approx.
  **77%** — but note Kalshi's own December sub-table on the same DeFiRate
  page shows 80% hike / 22% hold, which does not sum to 100%; this is a
  disclosed internal inconsistency in the source, not an error in the blended
  77% figure. Re-check the December sub-view's internal consistency again at
  edition 48 rather than assuming it has self-corrected. **Kalshi's own
  direct fetch failed again (HTTP 429) at edition 47, now eleven consecutive
  failures (37-47).** Official CME FedWatch also failed again directly
  (timeout) at edition 47, a **seventh** consecutive failure (41-47). The
  composite "at least one more hike in 2026" read has still not been freshly
  re-pulled since edition 38 (last known approx. 80%) — don't cite without a
  fresh pull.
- **US-China "30-for-30" tariff framework — the framework itself remains
  fully resolved (closed since edition 37); the implementation-notice
  sub-question, open since edition 43, was substantively answered at edition
  47 — treat as a closed thread going forward unless a genuine Federal
  Register filing surfaces.** The full text of Ambassador Greer's 27
  September 2026 USTR statement was read directly against ustr.gov: it
  announces the "U.S.-China Board of Trade"'s recommendations for approx.
  $30bn of tariff treatment on each side's non-sensitive goods, but commits to
  no effective date or implementation deadline. Separately, Greer stated
  publicly on 1 October 2026 (reported via SCMP/thestar.com.my) that there is
  **no specific implementation timeline** — recommendations must clear public
  comment and a formal legal determination before any tariff action is
  adopted. **Bottom line: no implementation notice exists, and none is
  imminent — this is the answer, not a continuing gap.** No further blind
  USTR/Federal-Register sweep is needed; only re-open if a dated filing
  actually surfaces. Separately noted at edition 47: the Busan US-China trade
  truce has reportedly been extended to **10 January 2027** (background
  context, not independently primary-sourced this run).
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates, government funding status) from memory or from the prompt's own
  framing — verify it fresh from a primary source (federalreserve.gov,
  bankofengland.co.uk, boj.or.jp, kansascityfed.org, norges-bank.no,
  riksbank.se, banxico.org.mx, snb.ch, rba.gov.au, whitehouse.gov, etc.) every
  edition, exactly like any other data point. **Edition 47 re-confirmed Kevin
  Warsh as Fed Chair directly against federalreserve.gov's Board of Governors
  bios page — an eighteenth straight direct re-confirmation.** The BoE's next
  decision (Thursday 5 November, now under two weeks out) was freshly
  re-touched at edition 47 via a direct bankofengland.co.uk fetch —
  unchanged, now confirmed directly for nine straight editions (39-47).
  **The shutdown/CR status check broke its clean four-edition URL streak at
  edition 47:** the usual whitehouse.gov congressional-bill URL pattern
  (confirmed working at editions 43-46) returned only an unrelated
  bill-signing list this run, not the funding-status language. The underlying
  fact (H.R. 6500 funds the government through 11 December 2026, no shutdown
  in effect) was re-confirmed instead via a Statement of Administration
  Policy PDF plus multiple corroborating outlets — the fact itself remains
  solid, but **edition 48 should re-establish a clean, working direct URL/
  document rather than assuming either the old pattern or this edition's
  substitute is now stable.** **The BoJ's next-meeting-date (Oct 29-30, 2026)
  remained consistent with boj.or.jp's own decision-index page at edition
  47**, though the research pass did not perform an unambiguous dedicated
  fresh direct fetch for the date specifically the way editions 41-46 did —
  treat the date as still reliable but **re-establish an explicit, dedicated
  direct boj.or.jp fetch for the meeting date at edition 48** to keep the
  confirmation chain unambiguous. **Edition 47 again could not get a direct
  numeric read of the current policy rate itself (approx. 1.25%) off
  boj.or.jp** — the Sept 18 policy-statement PDF again returned undecodable
  raw PDF-stream data, and the English decision-index page lists no rate
  figures. This numeric-rate gap is now **three straight editions (45-47)** —
  try a dedicated rate-specific HTML page (not the decision PDF) at edition
  48, since the raw-PDF approach has now failed three times running.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed directly
  again at edition 47 (following decision 17 December 2026). Continue the
  direct-fetch discipline given the meeting is now under two weeks out.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano), both primary-sourced as of edition 37 — closed thread, do
  not re-derive. **The next policy meeting date (Oct 29-30, 2026) remained
  consistent with boj.or.jp's decision-index page through edition 47**,
  though not via an explicit dedicated fresh direct fetch this run — see the
  general-principle entry above for both this caveat and the numeric-rate gap
  (now three straight editions open, 45-47).
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
- **No US federal government shutdown is in effect — re-confirmed at edition
  47, though via a different method after the previously-reliable URL
  broke (see general principle entry above).** H.R. 6500 funds federal
  agencies through **11 December 2026**. Watch for shutdown risk resurfacing
  as that date approaches, and re-establish a clean direct URL at edition 48.
- **University of Michigan preliminary October 2026 consumer sentiment —
  still not a "closed thread," watch for the final reading:** 46.3, a
  five-month low (current conditions 44.7, expectations 47.3, year-ahead
  inflation expectations 4.7%, long-run 3.5%), confirmed via
  investinglive.com and advisorperspectives.com, both dated 9 Oct 2026.
  **Final October reading due Friday 23 October 2026, 10:00am ET** (time
  confirmed directly against sca.isr.umich.edu at edition 46, re-confirmed via
  multiple calendar sources at edition 47) — now just two days out from
  edition 47's cutoff; **edition 48 should watch for it directly if its
  window reaches Friday 23 Oct.**
- **China September 2026 CPI/PPI — RESOLVED at edition 42, closed thread, do
  not re-derive:** CPI **+0.9% y/y** (+0.2% m/m), PPI **+5.0% y/y** (the
  fastest PPI rise since June 2022), driven by fuel costs. Sourced to gov.cn's
  English-language NBS-attributed news release (stats.gov.cn itself remained
  stale/unreachable) — continue treating the gov.cn English release as an
  acceptable near-primary substitute if stats.gov.cn remains unreachable.
  **Edition 47 could not confirm whether any NBS data release printed
  specifically on 20-21 October 2026** — stats.gov.cn's own calendar page did
  not resolve to usable date-level content via direct fetch; China's October
  PMI is separately due approx. 31 October 2026, outside this window.
- **China Q3 2026 GDP — RESOLVED at edition 45, closed thread, do not
  re-derive:** printed **Monday 19 October 2026**, settling edition 44's
  disputed release-date (19 vs. 20 Oct) in favor of the 19th, confirmed
  directly against the National Bureau of Statistics' English-language press
  release at stats.gov.cn. Q3 alone: **+4.5% y/y, +1.2% q/q**; first-three-
  quarters 2026 cumulative: **+4.6% y/y** (GDP RMB 107,107.1bn).
- **New Mexico v. Meta — RULING ISSUED at edition 47, closing the "still
  pending" status carried since edition 37; a new, narrower open thread
  follows.** Judge Francis Mathew ruled Wednesday 21 October 2026 that Meta
  owes **$25bn** in civil penalties for the jury's late-September verdict
  (Meta violated the state's Unfair Practices Act roughly 43.9 million times,
  re: hate-speech policy and its Cambridge Analytica response) — above the
  48-other-state, $18bn settlement Meta already reached elsewhere, but well
  below New Mexico's $35-40bn ask and the $219.5bn theoretical statutory
  maximum ($5,000/violation). The judge reportedly cited due-process/
  excessiveness concerns in reducing the figure, and described Meta's
  conduct as "a coherent strategy designed to mislead the public." Meta has
  said it will appeal, and its chief legal officer characterized the ruling
  and the state AG's approach as making it "all but impossible to do business
  in the state of New Mexico." Reported directly and consistently by CNBC,
  Axios, CNN, The Hill and others, all dated 21 Oct 2026 — multi-sourced.
  **Open sub-question for edition 48: whether the 9 October stay of
  enforcement (granted on Meta's unopposed motion, logged at edition 46)
  carries over to this specific $25bn judgment, and whether Meta has filed
  its formal notice of appeal** — neither was found or confirmable at edition
  47. This is a distinct proceeding from the March 2026 child-safety jury
  verdict ($375m, before a different judge, Bryan Biedscheid) and the August
  2026 abatement ruling ($567m, same Biedscheid case, under appeal) — don't
  conflate the three.
- **New calendar-awareness item from edition 40, reconfirmed relevant at
  edition 41: "equities-open, bonds-closed" US holidays need an explicit
  check every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. **Next candidate to verify when it lands: Veterans Day, Wed 11 Nov
  2026 — confirm whether that is also bonds-only before assuming.**
- **The vendor-retroactive-revision trap recurred again at edition 47,
  rotating back to the gold/silver/DXY/EUR-USD/USD-JPY cluster** (a
  five-instrument hit, slightly different composition from edition 46's
  three-instrument gold/silver/nat-gas case). Re-fetching Tuesday 20 Oct's
  closes from the same vendor (Investing.com) at edition 47 found: gold
  $4,132.45→$4,142.60 (softening -0.66% to -0.42%), silver $57.928→$58.000
  (firming +1.14% to +1.27%), DXY -0.18%→-0.27%, EUR/USD 1.1226→1.1237
  (firming +0.12% to +0.22%), USD/JPY 158.29→158.17 (softening -0.13% to
  -0.21%) — all shifted versus this report's last-logged figures by
  0.08-0.24pp, each in the direction of a slightly different Tuesday session
  than previously reported. GBP/USD, copper and the full Treasury curve
  again reconciled exactly. **Recommendation reinforced yet again:
  fresh-refetch every commodity/FX/Treasury prior-session base from the same
  vendor table every single edition — not just the instruments that drifted
  last time — and disclose every divergence found, however small. The locus
  keeps rotating (WTI at 45, gold/silver/nat-gas at 46, gold/silver/DXY/EUR-
  USD/USD-JPY at 47); copper and the Treasury curve remain the only two
  instrument classes that have never shown this trap.**
- **Henry Hub natural gas: the front-month-contract-identity question was
  cleanly resolved at edition 47 via a new technique, but a distinct
  data-quality flag replaced it.** A direct cross-check against TradingView's
  futures contract-expiry calendar confirmed NGX6 (November 2026) remains
  front-month through its own 28 October 2026 expiry (NGZ6/December doesn't
  expire until 25 November) — **log this TradingView-expiry-calendar
  cross-check as a durable addition to the Henry Hub sourcing playbook for
  resolving front-month ambiguity going forward.** However, Investing.com's
  own Wednesday 21 Oct row showed an internally inconsistent OHLC (reported
  "open" above reported "high"), and the day's -6.11% move could not be
  independently cross-verified against a second source. Continue treating
  this instrument's price data (not just its contract identity) as requiring
  a fresh double-check every edition.
- **The Kitco live-spot-vs-headline cross-check was NOT attempted at edition
  47 either** (Investing.com's history tables again sufficed for the
  gold/silver read) — no new data point on this recurring trap this edition;
  resume testing it when research-pass timing allows a same-day check.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company (owns AOL, Evernote,
  WeTransfer, Issuu and other consumer/SaaS apps), IPO'd 1 July 2026 at
  $29/share (above its $26-28 range), rising approx. 41% on debut to a
  approx. $25bn market value. Logged here so a future edition doesn't waste
  effort re-verifying the ticker's legitimacy if it moves sharply again.
- **The "named secondary outlet's own percentage-move headline can be flatly
  wrong" trap (first logged edition 44, J.B. Hunt/FreightWaves) is a standing
  caution, not a one-off, and gained two new variants at edition 47.** First,
  a smaller-magnitude instance of the original pattern: AT&T's Wednesday 21
  Oct close was logged at -6.45% from stockanalysis.com, while a third-party
  intraday-movers archive (tapeboard.com) showed -6.1% for the same session —
  both plausible, neither independently reconciled, disclosed as a
  single-sourced figure rather than treated as exact. Second, a genuinely
  new variant: **a single aggregator can show two different numbers for the
  very same quote.** Meta's Wednesday-evening after-hours move was shown as
  +2.16% (to $712.61) on stockanalysis.com's own live-quote box, while a
  TheFly headline embedded in that same page's news feed cited +4% (to
  $723.00) for what appears to be the same after-hours print — no wire
  service was found to break the tie, so the figure was reported as a range
  rather than a single number. **Treat any single-aggregator percentage claim
  as a candidate for this kind of internal conflict, not just a candidate for
  cross-aggregator conflict — check a page's own quote box against its own
  embedded headlines/news feed before citing either.**
- **A reinforcing, non-novel reminder from edition 44, reinforced again hard
  at edition 47: premarket/regular-session-close is not the after-hours
  earnings reaction, and the two can diverge sharply.** Edition 47's megacap
  earnings quadfecta illustrated this cleanly: IBM rose 3.94% into Wednesday's
  close (before its own report) then fell 4.63% after hours on narrow gross
  margin; Tesla similarly rose 3.41% into the close then fell 3.32% after
  hours on a margin miss, despite both companies beating consensus on revenue
  and EPS. Always fetch and separately label the regular-session close vs.
  the after-hours reaction; never imply the close already reflects a report
  that lands after it.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent, but has
  now agreed for a third straight session (45-47), worth watching for
  whether it is becoming the norm rather than staying truly intermittent.**
  DXY fell -0.01% and USD/JPY fell -0.01% Wednesday 21 Oct, both effectively
  flat but both negative — directionally agreeing for a second straight
  session (following edition 46's -0.18%/-0.13% agreement) and continuing a
  run that started with edition 45's positive-direction agreement (+0.13%/
  +0.33%). Keep disclosing the comparison every edition regardless of which
  way it goes.
- **The single-aggregator-dependence pattern from edition 45 continued in a
  modified form at edition 47: AP's wire did actually post this time (unlike
  editions 45-46's full gaps), but apnews.com itself blocked direct fetch
  (403) — a syndication mirror was used instead, cross-checked against an
  independent secondary outlet (Investrade) and an ETF-proxy triangulation,
  all agreeing closely.** Much of the earnings-heavy equities section
  (individual closes, earnings figures, after-hours quotes) still traced
  predominantly to stockanalysis.com and SEC EDGAR filings rather than a
  wire service — appropriate given SEC filings are primary sources, but
  continue disclosing the sourcing tier explicitly rather than treating
  single-aggregator price/AH data as independently confirmed.
- **A ticker-confusion / internally-inconsistent-aggregator trap, first
  logged at edition 45, gained a related instance at edition 47 distinct
  from the Meta same-aggregator-conflict case above:** Opendoor's -5.34% and
  MillerKnoll's -4.91% Wednesday declines each had an identified same-day 8-K
  filing (an officer/director change for Opendoor, a permanent-CEO
  announcement for MillerKnoll), but neither filing's own text fully
  explained a decline of that magnitude — similar in character to edition
  46's Equifax unexplained-magnitude case (see below), but for a
  confirmed-filing-with-insufficient-explanation rather than a fully
  unexplained rally. Logged as open threads, not chased further this
  edition.
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
  pad_frac by trial and error. **Edition 47 reinforced that the relevant
  threshold is the RATIO between the largest and second-largest mover, not
  the absolute size of the largest move:** Arcus Biosciences' -19.58% move
  was by far the largest raw number logged to date outside edition 45's
  biotech extremes, yet needed no capping at all, because the next-largest
  mover (Integra LifeSciences, -11.18%) was only approx. 1.75x smaller — well
  under the approx. 5x threshold. A single very large bar is not itself a
  reason to cap; only a large RATIO to the next-largest bar is.
- **A new trap, logged for the first time at edition 46: a secondary outlet's
  own qualitative SECTOR-level narrative can be flatly contradicted by actual
  ETF data, the same way a single-stock percentage headline can be.** One
  outlet's Tuesday 20 Oct recap framed Energy as the session's worst-performing
  sector and Communication Services as a Meta-driven laggard; a direct fetch of
  all 11 SPDR sector ETFs showed both claims false. **This generalizes the
  existing single-stock-headline-verification discipline to sector-level
  narrative claims: fetch all 11 SPDR sector ETFs directly by default**, not
  as a fallback only used when a conflict is suspected. **Edition 47 again
  fetched all 11 directly from the start** (no secondary-outlet sector
  narrative was separately checked against it this run, since the research
  pass went straight to stockanalysis.com's ETF tables) — no conflict arose,
  consistent with this being the right default method rather than only a
  conflict-resolution tool.
- **SpotGamma logged its own distinct dealer-gamma failure mode starting at
  edition 46 (tried as a zerogex.io alternative): a pure marketing homepage
  with no gamma levels, prices or dashboard content at all** (the real
  dashboard sits behind a dashboard.spotgamma.com login) — **a second
  straight failure in the same mode at edition 47.** zerogex.io logged its
  **eighth consecutive edition of failure at edition 47** (blank dashboard
  fields, the same populated-landing-page/placeholder-dash mode as prior
  editions). Both sources remain fully unusable; this is a data point for the
  running failure-mode log, not a reason to stop trying either source.
- **A primary-source-over-third-party-calendar lesson, logged at edition 46
  and implicitly re-validated at edition 47:** Meta's own investor-relations
  date (Wednesday 21 October 2026, after market close) held up exactly as
  the primary source said, confirming the lesson that a company's own IR
  announcement beats third-party earnings-calendar aggregators when the two
  conflict.
- **Equifax's +11.33% Tuesday 20 Oct rally remains an open, not-yet-chased
  "unexplained-magnitude" thread** (roughly in-line print, slightly cut
  guidance, outsized rally) — not revisited at edition 47; carry forward.
- **New at edition 47: when standard "biggest movers" aggregator pages
  (CNBC, MarketWatch, Barchart, Yahoo Finance) aren't retrievable for the
  target date, SEC EDGAR's full-text search for same-date 8-K filings is an
  effective, primary-source-grounded alternative discovery method** — used
  successfully at edition 47 to identify Arcus Biosciences, Integra
  LifeSciences, Lithia Motors, M/I Homes and others as the session's largest
  movers, each then cross-referenced against stockanalysis.com for the
  actual price move and catalyst detail. **tapeboard.com (a third-party
  intraday-movers archive) was also used successfully for the first time at
  edition 47** as a supplementary same-day gainer/loser list, and is what
  surfaced the AT&T percentage discrepancy logged above — usable but
  single-sourced, cross-check its figures against stockanalysis.com before
  citing.
- **New at edition 47: a megacap multi-name earnings cluster reporting on the
  same evening can produce genuinely uncorrelated reactions — don't assume a
  shared narrative just because results land together.** Meta, Tesla, IBM
  and Texas Instruments all reported after Wednesday 21 Oct's close; all four
  beat on revenue, yet their after-hours reactions ranged from a disputed
  +2-4% (Meta, on a legal-charge-driven GAAP miss but a clean revenue beat)
  to -4.63% (IBM, margin-driven) to -3.32% (Tesla, margin-driven) to +1.21%
  (Texas Instruments, a clean beat-and-raise). Treat each name's reaction on
  its own terms even within a single reporting-night cluster.

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
  uniqueness of use (editions 33-47 have all done this for stockanalysis.com
  single-stock closes and other repeatedly-used outlets, confirmed stable
  across fourteen editions; **edition 47 went further and reused one shared
  Annex B number across thirteen different companies' SEC EDGAR 8-K filings**,
  which worked cleanly with `check_refs.py` and kept the source count
  manageable on an extremely earnings-heavy day — use this same-method,
  different-document reuse pattern again whenever a single day has many
  primary-source filings of the same type). **Citing the prior edition
  itself as a source** (e.g. "[32] Daily Economic Briefing, edition 44,
  logged prior-session baseline figures") is a legitimate, already-used
  pattern when disclosing a divergence against a previously-logged figure —
  editions 43 through 47 have all done this cleanly with `check_refs.py`.
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note. **Do not duplicate the
  day-ahead calendar as both a prose paragraph (e.g. at the end of Section 3)
  and the Section 6 table — edition 47's first draft did exactly this and it
  was the single largest contributor to a 5-page overflow; Section 6's table
  is the one and only place the day-ahead calendar belongs.**
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart 2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes). **Chart
  placement is editorial, not fixed to Section 2** — editions 24, 34, 39 and
  44 all placed a CFTC-positioning chart #2 in Section 5 (Derivatives) rather
  than Section 2, since that's where the content actually belongs; editions
  45, 46 and 47 all reverted to the sector-ETF-proxy default in its usual
  Section 2 placement since no fresher CFTC data was due inside any of those
  windows (next report Fri 23 Oct, covering Tue 20 Oct data — should be
  fresh for whichever edition's window extends past 3:30pm ET that day).
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
  has occasionally failed to post in time, or (new at edition 47) posted but
  blocked direct automated fetch (apnews.com returned HTTP 403), requiring a
  syndication-mirror workaround even though the wire itself did exist this
  time. Fall back to secondary outlet(s) + ETF-proxy triangulation (plus an
  intraday Reuters snapshot if a full closing wire isn't found) when AP/
  Reuters genuinely haven't posted or can't be fetched directly, and disclose
  the fallback explicitly every time, not just the first time it happens.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Edition 44 found a new, stronger version of this trap: a
  FreightWaves headline's percentage-move claim for J.B. Hunt was not just
  mistimed but flatly contradicted by the stock's own verified close (claimed
  "+12%," actual close -2.78%).** Always check a dated article's own claimed
  magnitude against the underlying price-history table, not just its date,
  before repeating it. **Edition 45 found a related but distinct trap: a
  single aggregator's own writeup can be internally self-contradictory**
  (see the "IAM" ticker-confusion case, Standing Facts above). **Edition 47
  found a further variant: the SAME aggregator can show two DIFFERENT
  numbers for the SAME quote** (Meta's after-hours move: +2.16% on
  stockanalysis.com's own live quote vs. +4% on a TheFly headline embedded
  in that same page) — check a page's own quote box against its own embedded
  headlines/news feed, not just against other aggregators, before citing a
  single figure.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  **Edition 47 continued this discipline**, individually verifying
  single-stock closes directly against stockanalysis.com for both the
  overnight/AH megacap quadfecta (Meta, Tesla, IBM, Texas Instruments) and
  the broader Q3 earnings slate (Netflix, United Airlines, Capital One,
  AT&T, CME Group, Abbott, Danaher, Thermo Fisher, Elevance Health), and
  separately re-fetching all 11 SPDR sector ETFs directly rather than
  trusting a secondary outlet's narrative (no conflict arose this time,
  consistent with edition 46's finding that this should be the default
  method, not just a conflict-resolution fallback).
- **Premarket is not the close, and the close is not the after-hours
  earnings reaction.** Reinforced explicitly at edition 44 and again hard at
  edition 47 (see the dedicated Standing Facts entry above) — Wednesday 21
  Oct's megacap quadfecta (IBM, Tesla both rising into the close on
  pre-earnings drift, then falling sharply after hours on the actual print)
  is the clearest example logged to date. Always fetch the verified close
  and the after-hours reaction as two separate, clearly labelled figures.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent but has
  now agreed for three straight editions (45-47)** — see Standing Facts
  entry above. Continue disclosing the DXY-vs-USD/JPY directional comparison
  explicitly every edition regardless of which way it goes, and watch
  whether the agreement streak is becoming the new norm.
- **The Kitco live-spot-vs-headline cross-check was not attempted at edition
  47** — see the dedicated Standing Facts entry above. Resume attempting it
  each edition when research-pass timing allows a same-day check.
- **GBP/USD reconciled cleanly for a third straight edition (45-47); gold,
  silver, DXY, EUR/USD and USD/JPY all showed a genuine vendor-revision
  shift at edition 47** (0.08-0.24pp each) — the vendor-revision trap's
  locus moved to this five-instrument cluster instead this time (see the
  dedicated Standing Facts entry above). Resume the fuller multi-source
  method on any FX/commodity pair if a fresh same-day conflict reappears.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for eleven further editions (37-47)** — edition 47 again found the full
  Treasury curve the one instrument class (alongside copper) that reconciled
  perfectly against the prior edition's logged base (2-yr 4.79%→4.81%, +2bp;
  10-yr 5.12%→5.13%, +1bp; 30-yr 5.42%→5.42%, flat; 2s10s 33bp→32bp, -1bp, a
  marginal narrowing). Treat as resolved/noise unless a fresh conflict
  appears.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 47 have all run clean (or
  clean after one quick fix) — **edition 47 needed one markup fix first**
  (stray `<sup>` citation tags had been placed outside their `<td>` cells in
  the commodities table during drafting; this doesn't break `check_refs.py`
  itself, which only parses the HTML text, but it would break the rendered
  table layout, so catch and fix it by eye before rendering, not just by
  running the ref-checker) — 34/34 clean after that one fix.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 47 have all rendered with zero stray tildes on the
  first draft.**
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39 and 44 have all
  resolved this cleanly for CFTC CoT, with full OI and Asset-Manager/
  Leveraged-Funds breakdowns for ES, NQ and RTY. **Edition 47 confirmed
  directly (cftc.gov's `financial_lf.htm`) that no new report has posted
  since Friday 16 October** (still Tuesday 13 Oct's figures: ES OI 1,931,607,
  AM net approx. +47%/LF approx. -21%; NQ OI 279,515; RTY OI 444,784,
  unchanged, as expected). **The next CFTC report is due Friday 23 October
  2026, 3:30pm ET, covering Tuesday 20 October data** — check cftc.gov
  directly at edition 48 if its window extends past that release time (very
  likely for most plausible edition-48 cutoffs), and re-evaluate chart #2
  (fresh CFTC vs. sector-ETF-proxy default) based on what's actually
  available.
- **The diffuse-overflow lesson from editions 44-45 recurred at edition 47
  in a cleanly-diagnosed form: the first HTML draft rendered at 5 pages, and
  the single largest contributor was a genuinely redundant prose paragraph**
  (a "Day ahead" paragraph duplicated in Section 3 when Section 6 already
  carried the same calendar as a dedicated table — see the new Structure
  rule above). After removing that duplication and trimming several smaller
  spots (two prose clauses, one table-row merge, one bullet merge), the
  render landed cleanly at 4 pages. **Lesson for edition 48: before hunting
  for small trims across many sections, first check whether any single block
  of content is accidentally duplicated across two sections — that is a much
  larger, single-fix win than diffuse trimming.** Continue re-rendering
  immediately after any content change regardless.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — **specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation.** Edition 47
  reinforced this distinction cleanly: Arcus Biosciences' -19.58% move (the
  largest raw number logged outside edition 45's biotech extremes) needed no
  capping because the next-largest mover (-11.18%) was only approx. 1.75x
  smaller, well under the threshold.
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists.** Edition 47 again found two outlets
  (UBS, Guggenheim) independently cross-confirmed for Netflix's post-earnings
  target cuts, but a longer list of additional cuts traced to one aggregator
  each and is disclosed as such; a general, non-earnings-related
  analyst-action roundup for the session could not be found at all (unlike
  editions 45-46, which both found at least a thin or substantive
  single-aggregator list). This sub-item continues to look genuinely
  intermittent in both yield and sourcing depth across editions 40-47 —
  report whatever a genuine search attempt turns up each edition, with its
  sourcing tier disclosed.
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38** — when a secondary-sourced EPS figure conflicts sharply with
  a primary filing's GAAP number without a stated basis, prefer the primary
  filing and flag the secondary figure in Annex A. **Edition 47 logged
  another clean confirmation of the contrasting, legitimate pattern across
  several names at once**: Meta ($3.83 GAAP vs. $7.40 ex-charge), AT&T
  ($0.13 GAAP vs. $0.65 adjusted) and Elevance Health ($6.27 GAAP vs. $6.99
  adjusted, itself flagged as including a one-time non-operating gain) all
  disclosed both figures clearly labelled in their own filings — reported in
  full per the established precedent, not treated as a conflict.
- **The "preview-consensus-only miss/beat framing" caution (first logged at
  edition 41, not actively re-chased since edition 41) remains an open,
  unconfirmed disclosed inference carried forward** — not re-chased at
  edition 47 either. Pick this thread back up at a future edition if
  bandwidth allows.
- **GE Vernova's Wednesday 14 Oct -6.20% decline — CLOSED at edition 45, do
  not carry forward.** See the dedicated Standing Facts entry above.
- **Equifax's +11.33% Tuesday 20 Oct unexplained-magnitude rally — still an
  open thread, not yet chased at edition 47.** See the dedicated Standing
  Facts entry above.
- **New at edition 47: on a day with an extremely heavy earnings/filing
  volume and standard movers-aggregator pages unavailable, SEC EDGAR
  full-text search for same-date 8-K filings is an effective, primary-
  source-grounded discovery method** — see the dedicated Standing Facts
  entry above for the full write-up and the names it surfaced.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 47 all got a fresh,
  same-day-timestamped sweep** — twenty consecutive fresh sweeps now.
  **Edition 47 also pulled a clean, fresh SKEW read alongside the usual five
  series (-6.26% to 150.36) — log that a full six-series sweep (VIX, VIX9D,
  VIX3M, VIX6M, VVIX, SKEW) is reliably obtainable in one pass, not just the
  headline five.** **The feed's two known bugs (a duplicated `prev_day_close`,
  and a `price_change_percent` that divides by current price instead of
  prior close) are genuinely intermittent, not a one-way ratchet: edition 44
  saw both bugs hit every series simultaneously, while editions 45, 46 and
  47 all saw NEITHER bug on any series (all percent fields matched an
  independent manual calculation exactly, three straight clean editions).**
  Freshness and bug-presence remain two independent axes. **Always compute
  day-over-day % change manually regardless of how many consecutive
  bug-free reads preceded the current one** — the bugs can return (or stay
  absent) without warning either way. VIX9D-vs-spot-VIX: edition 47 saw the
  term structure stay in contango (VIX9D 15.49 < VIX 16.68 < VIX3M 18.72 <
  VIX6M 20.62), extending the complex's unwind for a third straight session
  (VIX -3.64%, VIX9D -4.79%, VVIX -2.68%). Keep watching rather than
  assuming continuation of any prior trend. A secondary aggregator
  (vistapglobal.com) again showed a conflicting VIX figure (-3.12% to 16.77
  vs. CBOE's own -3.64% to 16.68) — treat CBOE's direct feed as
  authoritative when the two disagree, consistent with past editions.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 47 fetched all 11 directly as the
  default method from the start** (Technology +1.67% the clear leader,
  Communication Services -1.11% the sole laggard ahead of Meta's own
  report; 7 of 11 green) — no secondary-outlet sector narrative was
  separately checked against it this run, and no conflict arose, consistent
  with edition 46's finding that direct-fetch-by-default (not just as a
  conflict-resolution fallback) is the right standing method.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (7 of 11 at edition 47) —
  continue treating an uncorroborated single-aggregator breadth figure as
  not usable.
- **Dealer gamma:** zerogex.io hit an **eighth consecutive edition of
  failure at edition 47** — the same populated-landing-page/placeholder-dash
  mode as prior editions. SpotGamma logged a **second straight failure in
  its own distinct mode at edition 47** — a pure marketing homepage with no
  gamma levels or dashboard content at all (real dashboard behind a login at
  dashboard.spotgamma.com). Both sources remain fully unusable.
- **Official CME FedWatch probabilities:** the page blocks fetching (edition
  47's direct attempt timed out again, a **seventh** consecutive failure,
  41-47) — use secondary citations (Polymarket, Kalshi, Reuters/other
  economist polls, desk notes) and give a range rather than a single
  invented number. DeFi Rate's Kalshi/Polymarket-blended aggregator remains a
  stable, consistently working source for both the near-dated (Oct) and now
  the December meeting across editions 37-47 — **edition 47 successfully
  pulled the December sub-view after edition 46's one-edition gap**, though
  note Kalshi's own December sub-table on that page shows an internal
  inconsistency (80% hike/22% hold, not summing to 100%) worth re-checking
  at edition 48.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, now **eleven consecutive failures (37-47)** — a confirmed
  structural gap, not transient. Resume the attempt-every-edition discipline
  at edition 48 regardless, but expect a block of some kind. Use Kalshi's
  own secondary reporting or DeFi Rate's blended aggregator as the
  workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has not been
  re-attempted as primary since edition 35 beyond a routine confirming try.
  **Westmetall.com has now worked cleanly TWENTY-SIX editions running**
  as the fallback (copper -0.68% to $14,441.00/tonne at edition 47, Tuesday
  base unrevised at $14,540.00/tonne, confirmed exactly). Copper remains,
  along with Treasuries, one of the two instrument classes that have never
  shown the vendor-revision trap.
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve CSV and the rendered HTML TextView page **agreed cleanly
  again at edition 47** (2-yr 4.81%, 10-yr 5.13%, 30-yr 5.42%, all 21 Oct),
  extending the clean streak to **twelve editions (37-47)** with no repeat of
  the edition-36 33bp gap. Keep fetching both endpoints and comparing rather
  than trusting either by default. **Note: a full-year-scoped TextView URL
  attempt at edition 47 got truncated by page length and failed to return
  the October rows — scope the URL to the specific month
  (`field_tdr_date_value_month=202610`-style parameter) rather than the
  full year, which worked cleanly on the second attempt.**
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). **Edition 47 confirmed directly that no new report has
  posted since Friday 16 Oct's release** (covering Tue 13 Oct 2026: ES OI
  1,931,607, Asset Mgr net approx. +47%/Leveraged Funds approx. -21%; NQ OI
  279,515; RTY full-size OI 444,784 — unchanged from edition 46's logged
  figures, as expected since no new data was due). **The next report is due
  Friday 23 October 2026, 3:30pm ET, covering Tuesday 20 October data** —
  check cftc.gov directly at edition 48 if its window extends past that
  release time, which is likely for most plausible edition-48 cutoffs;
  re-evaluate chart #2 (fresh CFTC vs. sector-ETF-proxy default) based on
  what's actually available.
- **GBP/USD clean close:** remains fully resolved since edition 37, now
  reconciling cleanly for a **third straight edition (45-47)**. **EUR/USD
  and USD/JPY, by contrast, both showed a genuine vendor-revision shift at
  edition 47** (alongside gold, silver and DXY) — see the dedicated Standing
  Facts entry above for the full write-up. EUR/USD closed Wednesday 21 Oct at
  1.1234 (-0.03% off a freshly-re-fetched Tuesday base of 1.1237, itself
  revised from this report's prior-logged 1.1226); GBP/USD closed at 1.3394
  (+0.10% off a Tuesday base of 1.3381, an exact match to edition 46's logged
  figure); USD/JPY closed at 158.15 (-0.01% off a freshly-re-fetched Tuesday
  base of 158.17, itself revised from this report's prior-logged 158.29) —
  all single-sourced to Investing.com's close-to-close history table.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot-vs-headline cross-check was not attempted at edition 47** —
  see the dedicated Standing Facts entry above. Gold and silver futures
  continue to source via Investing.com, but **edition 47 found both
  instruments' own Tuesday 20 Oct closes had been revised since this
  report's last-logged figures** (gold to $4,142.60 from $4,132.45; silver to
  $58.000 from $57.928) — see the dedicated vendor-revision Standing Facts
  entry above for the full write-up. Wednesday 21 Oct: gold approx. flat
  (-$0.20 to $4,142.40), silver -0.71% to $57.590, both off the
  freshly-fetched Tuesday bases.
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is also a closed thread as of
  edition 45 — see the dedicated Standing Facts entry above. **US
  import/export prices and industrial production:** both closed threads for
  September — see Standing Facts above. **University of Michigan final
  October consumer sentiment** (see Standing Facts above): due Friday 23
  October 2026, 10:00am ET — watch for it, now just two days out.
- **Henry Hub natural gas:** the front-month-contract-identity question was
  cleanly resolved at edition 47 via a new technique (TradingView's futures
  contract-expiry calendar — see the dedicated Standing Facts entry above);
  **use this technique as the default going forward whenever front-month
  identity is in doubt.** The instrument's own price-data quality remains
  unstable: edition 47's Wednesday row showed an internally inconsistent
  OHLC (open above high), and the day's -6.11% move could not be
  independently cross-verified — continue double-checking this instrument
  fresh every edition.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 47 found no notable
  Wednesday-dated single-stock options-flow/skew commentary** for the
  session's chip/tech names despite a targeted search (though a non-desk
  options-data aggregator did yield a usable Meta pre-earnings implied-move
  figure, approx. ±7.0%) — an **eleventh** consecutive largely-empty edition
  on the general chip/tech sub-item (37-47). Treat this sub-item as reliably
  low-yield and keep it a brief, secondary effort each edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. Not
  applicable through edition 47; next due approx. 14 November 2026, now
  under four weeks out — start watching for it in editions covering early
  November.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22). Not attempted
  again through edition 47.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully
  again at editions 39, 44, 45 and 46's confirming checks (all covering Tue
  13 Oct data, still the most recent as of edition 47's confirming check).
  Repeat this same three-instrument fetch at edition 48 when the Friday 23
  Oct report should be available, watching for the Micro-vs-full-size
  Russell naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 47 found
  two independently cross-confirmed Netflix price-target cuts (UBS,
  Guggenheim) but, beyond that, a general non-earnings-related
  analyst-action roundup for the session could not be found at all —
  slightly thinner than editions 45-46, which both found at least a
  single-aggregator list. The pattern across 37-47 continues to look
  genuinely intermittent in yield and increasingly variable in sourcing
  depth — watch each edition independently rather than assuming a trend.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** Edition 47 individually re-verified single-stock closes
  directly against stockanalysis.com across the full earnings slate and the
  SEC-EDGAR-discovered mid-cap movers — all reconciled; the AT&T figure
  (-6.45% vs. a third-party archive's -6.1%) and the Meta after-hours figure
  (+2.16% vs. +4% from the same aggregator) are the two unresolved
  single-sourced conflicts logged this edition (see Standing Facts above).
  Continue this direct-verification discipline on high-confidence-seeming
  figures, not just surprising ones.
- **New at edition 47: the DOL's weekly initial-jobless-claims release
  document could not be parsed** (returned unreadable/binary data via direct
  fetch) — a first-logged, minor gap; try an alternate DOL page or a
  secondary economic-calendar aggregator for the consensus figure at edition
  48 rather than repeating the same PDF fetch.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel
  (confirmed clean at editions 37 through 43 and again at 45, 46 and 47, ten
  editions total) — this remains correct for 10-11 categories specifically.
  For charts with fewer categories, scale the height down: roughly
  `(9.8, 1.65-1.95)` for 3-9 categories (edition 47 used `(9.8, 1.95)` for a
  9-category single-stock movers chart). **Always render and visually
  inspect (via the Read tool) the actual PNG at or near full resolution
  before embedding it**, regardless of what a past edition's success might
  suggest. **Edition 47 found the 11-category sector panel's default
  pad_frac (0.12) was NOT enough even though every bar's magnitude was small
  (under approx. 1.7%) — the leftmost bar's label ("Comm. Svcs (XLC)
  -1.11%") visually ran into the y-axis tick labels at pad_frac=0.12. Raising
  pad_frac to 0.30 (matching editions 45-46's small-magnitude-panel value)
  fixed it cleanly on the first retry** — this is now a confirmed, repeated
  pattern (0.30 has now worked for three straight small-magnitude 11-category
  panels, 45-47): **default to pad_frac=0.30 from the start for an
  11-category sector-ETF panel, rather than trying 0.12 first and
  discovering the overlap.**
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
  capped-outlier chart. **Edition 47's own movers spread (approx. 1.75x, the
  largest mover at -19.58%) fell well under the approx. 5x capping
  threshold despite the largest mover's unusually big raw magnitude, so no
  capping was needed** — reinforcing that the trigger is the ratio to the
  next-largest bar, not the largest bar's absolute size (see the dedicated
  Hard Rules entry above).
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
  single concentrated overflow.** Editions 44 and 45 were diffuse-overflow
  examples; edition 46 rendered clean on the first attempt; **edition 47 was
  a third distinct pattern — a single clean root cause (a redundant,
  duplicated content block across two sections) rather than either a stray
  break or truly diffuse overflow.** Always check for content duplication
  across sections first when a draft overflows — it's the cheapest, highest-
  leverage fix to check before diffuse trimming. **A large, suspicious blank
  area at the bottom of a page (as opposed to a page that's merely a bit
  short) is usually caused by an atomic block** — most often a chart `<img>`
  — not fitting in the remaining space and being pushed whole to the next
  page; editions 44 through 47 have shown no instance of this pattern (when
  overflow occurs, content simply runs too long across several blocks or one
  duplicated block, not one pushed-whole block).
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix.
- **A markup-correctness trap, logged for the first time at edition 47: a
  `<sup class="ref">` citation tag placed immediately after a table row's
  last `</td>` but still inside the `<tr>` (i.e. not nested inside any
  `<td>`) is invalid table structure.** `check_refs.py` will NOT catch this
  — its regex only cares whether the `[n]` text exists somewhere in the
  HTML, not where structurally — so it can silently ship a malformed table
  row. Caught and fixed by eye at edition 47 before rendering. **Always
  nest every `<sup class="ref">` tag inside a `<td>...</td>` pair, never as
  a sibling of one inside a `<tr>`** — grep for `</td><sup` as a quick
  self-check if a table was built with a lot of copy-paste.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Edition 47 needed one trim round (removing a duplicated day-ahead
  paragraph plus several smaller cuts) to go from 5 pages to 4; budget for
  at least one re-render-and-check cycle on any edition with a borderline or
  very high content volume, and check for cross-section duplication before
  diffuse trimming (see the dedicated note above).

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across editions 40 through
47's very different content volumes (40 needed a padding table to fill page
3, 41 and 42 both filled naturally with no padding needed, 43 needed a
content TRIM to avoid overflow on a very high single-stock-volume session,
44 and 45 both needed several small content trims across multiple sections
to avoid a diffuse overflow, 46 rendered clean on the first attempt with no
trims or padding needed at all, 47 needed one trim round driven mainly by a
single duplicated content block rather than truly diffuse overflow. Treat as
the durable default; the lever to pull on a high-volume or overflowing day
is first checking for duplicated content across sections, then
merging/trimming redundant content across whichever sections are longest —
not loosening the CSS further.)
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
  page; editions 44 through 47 all folded commodities, FX and Treasuries into
  ONE combined table (10-14 rows) as the PRIMARY commodities table rather
  than padding, now the standing default rather than an edition-specific
  choice. **On a high-single-stock-volume earnings day (many reporters/movers
  in one session), the opposite problem is more likely — watch the movers
  table specifically for verbosity (multi-clause driver text, rows that could
  share a combined cell) before assuming the page budget is safe.** Edition
  47 had an extremely high-earnings-volume Wednesday (Meta, Tesla, IBM, Texas
  Instruments after close, plus Netflix, AT&T, United Airlines, Capital One,
  CME, Abbott, Danaher, Thermo Fisher and Elevance Health all reporting
  around the session) and still converged to a clean 4-page render after one
  trim round — the earnings volume itself was handled by splitting coverage
  across a tight movers table (one sentence per row) plus grouped prose
  paragraphs (the "after-hours quadfecta" and "rest of a very heavy earnings
  slate") rather than one giant table, which kept the section readable
  despite covering roughly thirteen reporting companies in one edition.
  Always re-render immediately after adding (or removing) any content to
  confirm the page count. **When overflow appears, check for duplicated
  content across sections FIRST (edition 47's lesson) before diffuse
  trimming; if no duplication is found, trim a little from several sections
  rather than gutting one** — day-ahead table rows, earnings-table note
  cells, movers-table driver cells, sector-setup bullets and macro/
  derivatives/commodities prose paragraphs are all good, low-cost candidates
  to shave a clause or merge a row from first.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across twenty-two eligible
editions, 25 through 47, with editions 34, 39 and 44 the exceptions when
fresher CFTC data was available; editions 45, 46 and 47 all reverted to this
default since the CFTC's next report was not yet due inside any of those
windows). Fresh CFTC CoT data on a Monday/weekend-window edition → the
ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart, normalized as
% of open interest, built with the grouped-bar technique documented under
Production notes, placed in Section 5 (Derivatives) per the editions
24/34/39/44 precedent. A single dominant earnings print with a clean,
well-sourced implied-vs-realized-move story → a three-bar implied/
historical-average/realized move chart (the historical-average leg has
never actually been sourced successfully). A genuine multi-sector
broadening/deepening selloff across consecutive sessions → the sector-ETF
proxy rendered as a grouped (day-over-day) bar instead of single-day. A
holiday-window preview edition with no fresher data → VIX futures term
structure with event annotations. When chart 1 (movers) already covers the
earnings/single-name story, the sector proxy (or a fresh CFTC positioning
chart, when available) is a good complementary choice even on a stock-heavy
day, since the two stories reinforce rather than duplicate each other —
editions 46 and 47 both used exactly this combination on high-earnings-
volume sessions. **Edition 48 should check cftc.gov's freshness first** (the
Friday 23 Oct report, covering Tuesday 20 Oct) before defaulting back to the
sector-ETF proxy — if CFTC data has posted fresh by edition 48's cutoff
(likely for most plausible cutoffs given the 3:30pm ET release time), use
the fresh CFTC chart per the established technique; otherwise revert to the
sector-ETF-proxy default as usual. **Remember the figsize-scales-to-
category-count guidance above (ceiling `(9.8, 1.95)` for an 11-category
panel, `(9.8, 2.15)` for the 3-category grouped CFTC chart, scale down for
fewer single-series categories), that an 11-category sector-ETF panel should
default to pad_frac=0.30 from the start (three straight confirming editions,
45-47), and the capped-outlier asterisk/footnote fix when a spread crosses
the approx. 5x RATIO threshold** (it did not at edition 47, despite the
largest mover's unusually large raw magnitude — see the dedicated note
above).

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–45 (condensed):** established the format (edition 1 baseline;
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
Henry Hub for the first time. Edition 42 (Thu 15 Oct, covering Wed 14 Oct):
September CPI printed hot, triggering the broadest risk-off session in
weeks (S&P -1.11%, Nasdaq -1.88%); CoreWeave and Oracle led decliners on
renewed AI-infrastructure-funding-stress; Bumble's buyout mystery resolved;
rate-path odds repriced sharply hawkish; the Treasury curve flattened; the
vendor-retroactive-revision trap broadened to FX for the first time; the VIX
complex spiked hard. Edition 43 (Fri 16 Oct, covering Thu 15 Oct): a second
straight blowout inflation print (September PPI) barely moved Fed odds; an
overnight memory-chip rout reversed sharply on Nvidia CEO Jensen Huang's
defense of CoreWeave's balance sheet; TSMC's record Q3 still fell on
cautious guidance; Ericsson's beat drove the session's largest single-stock
move (+11.80%); six of eleven commodities/FX instruments showed a
silently-shifted Wednesday base. Edition 44 (Mon 19 Oct, covering Fri 16 Oct
+ weekend): equities fell broadly Friday on renewed AI-infra. spending
doubts (Nasdaq -2.14%, its worst week since June); the VIX complex spiked
hard with both CBOE feed bugs appearing simultaneously for the first time;
five large movers had no confirmed catalyst; a FreightWaves "+12%" J.B. Hunt
headline was flatly wrong (actual close -2.78%); CFTC CoT posted fresh data,
powering the first grouped-bar positioning chart; the first HTML draft
overflowed to 5 pages, fixed over roughly five trim rounds. Edition 45 (Tue
20 Oct, covering Mon 19 Oct + weekend): equities rebounded broadly (S&P
+0.41%, Dow -0.07%, Nasdaq +1.11%, Russell +0.25%) though breadth stayed
narrow; neither AP nor Reuters had posted a wire by cutoff, a new
CNBC-live-blog/Investrade/SPY-proxy fallback tier was used; biotech produced
the day's extremes (Silence Therapeutics +125.58% on a Merck KGaA buyout,
EyePoint Pharmaceuticals -85.28% on a failed trial), the chart's first
outlier-capping use, surfacing a label-overlap bug (fixed via an
asterisk+footnote pattern); two claims were excluded after failing
corroboration, logging a new ticker-confusion/internal-inconsistency
sourcing trap; GE Vernova's decline closed with a caveat; China's Q3 GDP
release-date dispute resolved; the vendor-revision trap's locus rotated to
WTI while EUR/USD and GBP/USD reconciled cleanly, ending a three-edition
streak; Henry Hub also broke its own five-edition base-ambiguity streak; the
VIX complex unwound sharply off Friday's spike. 33 sources, clean 33/33 on
`check_refs.py` after one quick fix, clean 4-page render.

**Edition 46 (condensed)** — Wednesday 21 October 2026 report covering
Tuesday 20 October 2026. Equities rallied broadly in a sharp rotation
reversal from Monday (S&P +0.29% to 7,712.76, Dow +1.02%, Nasdaq roughly
flat, Russell +1.65%), 10 of 11 sectors green; neither AP nor Reuters had
posted a wire by cutoff for a second straight edition, so a secondary-outlet-
plus-ETF-proxy-plus-Reuters-intraday-snapshot fallback was used; a new trap
was logged when a secondary outlet's sector narrative (Energy/Communication
Services as laggards) was flatly contradicted by a direct 11-ETF fetch. A
packed earnings Tuesday: Salesforce's $47.50/share Braze buyout (BRZE
+51.70%, no capping needed), Equifax (+11.33%, a new unexplained-magnitude
thread) and Hasbro (+11.20%) led gainers; GM fell 6.84% despite a beat and a
$20bn buyback; Netflix fell in the regular session then further after hours
on soft Q4 guidance; two secondary-source claims (Moderna, "Salesforce
slipped") were checked against closing-price data and excluded. Standing Fed
facts all re-verified unchanged (Kevin Warsh, 17th straight confirmation);
rate-path odds little changed (Oct hold approx. 87%) with December a
genuine data gap; Kalshi (10th straight failure) and CME FedWatch (6th
straight failure) both failed again; the US-China tariff implementation
notice remained unresolved but surfaced a new lead (the 27 Sept USTR Greer
statement, later pulled in full at edition 47); New Mexico v. Meta remained
pending, with a new 9 Oct stay-of-enforcement detail surfacing (later
superseded by the actual ruling at edition 47). The vendor-revision trap
hit its broadest case yet (gold, silver and Henry Hub's Monday closes all
revised simultaneously) while WTI, Brent, copper, GBP/USD and the Treasury
curve reconciled cleanly. The VIX complex extended its unwind, feed clean
for a second straight edition; dealer gamma fully unusable (zerogex and
SpotGamma both failed, in distinct modes); CFTC CoT confirmed no new data as
expected. The first HTML draft rendered clean at 4 pages with no trims
needed. 42 sources, clean 42/42 on the first `check_refs.py` pass, zero
stray tildes.

**Edition 47 (most recent — full detail)** — Thursday 22 October 2026
report covering Wednesday 21 October 2026, research window Tue 20 Oct 2026
20:00 ET through Wed 21 Oct 2026 20:21 ET (the window's one NYSE session).
Verified the two structural header rules again — now clean across fifteen
(date-line) and nineteen (window-line) consecutive applicable editions
respectively.

**Equities extended Tuesday's rally for a second straight session** (S&P 500
+0.58% to 7,757.17, Dow +0.68% to 52,856.09, Nasdaq Composite +1.05% to
26,702.86, Russell 2000 +0.27% to 2,781.02), led by Technology (+1.67%) even
as Communication Services (-1.11%) lagged ahead of Meta's own evening
report — 7 of 11 SPDR sectors closed green. **AP's wire did post this time,
but apnews.com itself blocked direct automated fetch (403)**; a syndication
mirror plus an independent secondary outlet (Investrade) plus ETF-proxy
triangulation (SPY/DIA/QQQ/IWM) all agreed closely. **A genuinely enormous
Q3 earnings day:** around Tuesday's close/Wednesday's open, Netflix
(-5.31% on soft Q4 guidance), AT&T (-6.45% despite a beat-and-raise,
single-sourced with a conflicting third-party -6.1% figure), United
Airlines (+3.99% despite a guidance cut), Capital One, CME Group, Abbott,
Danaher (+4.29%), Thermo Fisher and Elevance Health all reported, continuing
this cycle's "beat yet fall" pattern across several names at once (Elevance,
Abbott, AT&T). **After Wednesday's close, a genuine megacap quadfecta
reported with four distinct reaction patterns:** Meta (a clean revenue beat
to $64.60bn overshadowed by a $9.89bn legal-settlement charge, and a
genuinely disputed after-hours move — the same aggregator showed both
+2.16% and +4% for the same quote, a new "same-aggregator-internal-conflict"
trap), Tesla (-3.32% AH on a margin miss despite an EPS/revenue beat), IBM
(-4.63% AH on narrow gross margin despite a beat) and Texas Instruments
(+1.21% AH on a clean beat-and-raise). The single-stock-movers chart was
instead dominated by non-megacap names found via a new discovery technique
(SEC EDGAR full-text search for same-date 8-Ks, used after CNBC/MarketWatch/
Barchart/Yahoo "biggest movers" pages weren't retrievable): Arcus
Biosciences -19.58% on a dilutive stock offering, Integra LifeSciences
-11.18%, Lithia Motors -10.15% and M/I Homes -8.08%, none needing
outlier-capping despite the largest move's size (approx. 1.75x the
next-largest, well under the 5x ratio threshold). **New Mexico's Judge
Francis Mathew ruled Meta owes $25bn in civil penalties**, closing the
"still pending" status carried since edition 37 (Meta plans to appeal;
whether the 9 Oct stay carries to this judgment is unconfirmed). **The
US-China tariff-implementation sub-question was substantively answered** via
USTR Ambassador Greer's full 27 Sept statement and a 1 Oct follow-up:
recommendations only, no effective date, no set timeline — treat as closed
unless a genuine filing surfaces. Standing Fed facts re-verified unchanged
(Kevin Warsh, 18th straight confirmation; funds rate 3.75%-4.00%; FOMC Oct
27-28, now inside its confirmed Oct 17-29 blackout period). Rate-path odds
(DeFi Rate): Oct 28 hold approx. 88%, little changed; December 9 odds were
successfully pulled fresh after edition 46's gap (hike approx. 77% blended,
though Kalshi's own December sub-table showed an internal 80/22
inconsistency). Kalshi (11th straight failure) and CME FedWatch (7th
straight failure) both failed direct fetch again. The whitehouse.gov
shutdown-status URL broke its four-edition streak; the underlying fact was
re-confirmed via an alternate document. The vendor-revision trap recurred,
rotating to gold/silver/DXY/EUR-USD/USD-JPY (five instruments); GBP/USD,
copper and the Treasury curve again reconciled cleanly. Henry Hub's
front-month ambiguity was cleanly resolved via a new technique (TradingView's
contract-expiry calendar) though the session's own OHLC data looked
internally inconsistent. The VIX complex extended its unwind for a third
straight session (VIX -3.64% to 16.68), feed clean for a third straight
edition, with a bonus clean SKEW read (-6.26% to 150.36). CFTC CoT confirmed
no new data as expected (next due Fri 23 Oct). Dealer gamma remained fully
unusable (zerogex an eighth straight failure, SpotGamma a second straight
failure in the same marketing-homepage mode). **The first HTML draft
overflowed to 5 pages from a single, cleanly-diagnosed root cause** (a prose
"day ahead" paragraph in Section 3 duplicating Section 6's own table) **—
clean at 4 pages after removing the duplication plus a few smaller trims.**
34 sources, clean 34/34 on `check_refs.py` after fixing one markup bug
(stray `<sup>` citation tags placed outside their `<td>` cells in the
commodities table — a new trap, logged in Hard Rules above), zero stray
tildes, clean 4-page render.

**Open threads for edition 48:** Meta's exact after-hours/Thursday-session
move remains a genuine, unresolved range (approx. +2% to +4%) — the same
aggregator showed two different numbers for the same quote; try to resolve
with a wire-service or exchange-confirmed figure once Thursday 22 Oct's
session data is available. Whether the 9 October stay of enforcement in New
Mexico v. Meta applies to the new $25bn judgment, and whether Meta has filed
its formal notice of appeal, were both unconfirmed at edition 47 — check
directly. BoJ's exact numeric policy rate (approx. 1.25%) remains
unconfirmed via a readable primary-source numeric page for a third straight
edition (45-47) — try a dedicated rate-specific HTML page (not the decision
PDF) at edition 48; also re-establish an explicit, dedicated direct
boj.or.jp fetch for the Oct 29-30 meeting date specifically, since edition
47's confirmation of the date was not via an unambiguous fresh direct fetch.
Re-establish a working whitehouse.gov shutdown-status URL at edition 48 —
the previously-reliable four-edition pattern broke for the first time at
edition 47 (the underlying fact remains confirmed via an alternate
document). University of Michigan's final October consumer-sentiment
reading is due Friday 23 October, 10:00am ET — now just two days out, watch
for it directly if edition 48's window reaches that date. The CFTC CoT
report due Friday 23 October 2026 (covering Tue 20 Oct data) should land
inside edition 48's window if its cutoff extends past 3:30pm ET that day —
check cftc.gov directly and expect fresh data; re-evaluate chart #2 (fresh
CFTC vs. sector-ETF-proxy default) based on what's actually available. Q3
Employment Cost Index is confirmed for Friday 30 October, 8:30am ET, now
about a week out. AT&T's exact Wednesday 21 Oct close % (-6.45% vs. a
third-party archive's -6.1%) is an unresolved single-source conflict, as is
whether Guggenheim cut or raised its Netflix price target (two sources gave
opposite directions). Netflix's, United Airlines' and Capital One's exact
Tuesday-evening after-hours % moves and precise sell-side consensus figures
were not found at edition 47. Opendoor's -5.34% and MillerKnoll's -4.91%
Wednesday declines each have an identified same-day 8-K filing but neither
fully explains the magnitude — open, not yet chased further. Equifax's
+11.33% Tuesday 20 Oct unexplained-magnitude rally remains open from
edition 46, not yet chased. The JPMorgan EPS-miss-framing and Wells Fargo/
Citigroup credit-provision-selloff-rationale threads from editions 41-42
remain open, unconfirmed disclosed inferences — revisit if bandwidth
allows. The "preview-consensus-only miss/beat framing" caution was not
re-chased at edition 47 and remains open. 13F filings are due approx. 14
November 2026, now under four weeks out — start watching for it in editions
covering early November. Threads closed after resolution rather than
carried further: New Mexico v. Meta's ruling (issued, $25bn, edition 47 —
see the narrower open sub-question above); the US-China tariff
implementation-notice sub-question (substantively answered, edition 47);
Henry Hub's front-month-contract-identity question (resolved via a new
TradingView-expiry-calendar technique, edition 47, though the instrument's
own price-data quality remains a separate, still-open concern).
