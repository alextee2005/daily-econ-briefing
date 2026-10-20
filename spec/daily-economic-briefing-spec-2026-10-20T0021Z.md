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
  through 45 have all applied this correctly** ("Friday 2 October 2026"
  through "Tuesday 20 October 2026" as the date line in each respective
  edition, with the window line carrying the session(s) covered) — now
  confirmed stable across thirteen consecutive editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 45 all reused the
  same pattern — now confirmed clean across seventeen consecutive editions (29
  through 45; edition 45 phrased it "Window: Sun 18 Oct 2026 20:00 ET – Mon 19
  Oct 2026 20:21 ET (Mon 19 Oct close/AH, the window's one NYSE session)"). No
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
- **Next FOMC meeting: October 27–28, 2026 — now about a week out from edition
  45's cutoff.** Decision expected approx. 2:00pm ET; press conference
  confirmed at **2:30pm ET on Oct 28** via federalreserve.gov's monthly events
  calendar (`federalreserve.gov/newsevents/2026-october.htm` — this
  `newsevents/YYYY-month.htm` URL pattern is the one that works for meeting
  TIMES; `fomccalendars.htm` only shows dates, not times). Re-confirmed again
  at edition 45 via federalreserve.gov directly. Following meeting: December
  8-9, 2026 (an SEP meeting). **The next edition whose covered session falls
  on or after Oct 27-28 should lead with the decision.**
- **Rate-path odds at edition 45 (DeFi Rate's Kalshi/Polymarket-blended
  aggregator, fetched at Monday 19 Oct's approx. 8:21pm ET cutoff):** October
  27-28 hold approx. **84-86%** (hike approx. 13-19% depending on sub-view;
  cut negligible/unshown on some views), December 8-9 hike approx. **73-81%**
  — a more hawkish-leaning December than October, roughly flat week-over-week
  versus edition 44's own range (Oct hold approx. 86-87%, Dec hike approx.
  73-77%). DeFi Rate's own summary/meeting-table/7-day-mover sub-views again
  disagreed with each other by 1-5 points — the same recurring internal
  reconciliation gap logged every edition since 43, now confirmed persistent
  across three editions (43-45); disclose it every edition rather than
  silently picking one sub-view. **Kalshi's own direct fetch failed again
  (HTTP 429) at edition 45, now nine consecutive failures (37-45).** Official
  CME FedWatch also failed again directly (timeout) at edition 45, a **fifth**
  consecutive failure (41-45) — note edition 45's own research pass
  miscounted this as a sixth straight failure; the correct consecutive count
  from this log is five (41, 42, 43, 44, 45). The composite "at least one more
  hike in 2026" read has still not been freshly re-pulled since edition 38
  (last known approx. 80%) — don't cite without a fresh pull.
- **US-China "30-for-30" tariff framework — closed thread as of edition 37, do
  not re-open:** 77 US product categories (household goods, textiles,
  appliances, toys, sporting goods, vacuum flasks) and 1,619 Chinese
  categories (dominated by food/farm goods, plus some medical devices;
  soybeans, chips, EVs and batteries excluded from both sides), each side's
  treatment benchmarked at approx. $30bn against 2024 bilateral trade,
  confirmed directly against whitehouse.gov's own Terms of Reference
  document. **Implementation-notice sub-question remains open:** edition 45
  made the direct USTR.gov/federalregister.gov fetch attempt instructed at
  edition 44 and still did not find an implementation notice —
  federalregister.gov's search sat behind a bot-check/unblock wall, and
  ustr.gov's press-release index returned HTTP 404. This was a genuine
  direct-primary-source attempt (not a secondary law-firm alert), restoring
  the direct-fetch discipline even though it came up empty-handed again.
  **Continue attempting a direct fetch each edition** — the framework itself
  is fully resolved; only whether/when it has actually been implemented is
  open.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates, government funding status) from memory or from the prompt's own
  framing — verify it fresh from a primary source (federalreserve.gov,
  bankofengland.co.uk, boj.or.jp, kansascityfed.org, norges-bank.no,
  riksbank.se, banxico.org.mx, snb.ch, rba.gov.au, whitehouse.gov, etc.) every
  edition, exactly like any other data point. **Edition 45 re-confirmed Kevin
  Warsh as Fed Chair directly against federalreserve.gov's Board of Governors
  bios page — a sixteenth straight direct re-confirmation.** The BoE's next
  decision (Thursday 5 November, now under three weeks out) was freshly
  re-touched at edition 45 via a direct bankofengland.co.uk fetch — unchanged,
  now confirmed directly for seven straight editions (39-45). The shutdown/CR
  status check remained on a clean direct primary-source footing at edition
  45: a direct whitehouse.gov fetch of
  `https://www.whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500/`
  again confirms H.R. 6500 funds federal agencies through **11 December
  2026**, no shutdown in effect — this URL pattern is now confirmed working
  for three straight editions (43-45); reuse it directly. **The BoJ's
  next-meeting-date primary source stayed confirmed via direct read at
  edition 45** (boj.or.jp's Monetary Policy Meeting schedule page, Oct 29-30
  2026, now five straight editions 41-45) — **but edition 45 could not get a
  direct numeric read of the current policy rate itself (approx. 1.25%) off
  boj.or.jp; only secondary sources confirmed the number this time.** This is
  a narrower gap than before (the meeting-schedule page keeps working
  cleanly) — try boj.or.jp's rate/guideline-specific page next time the rate
  number itself needs re-confirming, not just the next-meeting date.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed directly
  again at edition 45 (following decision 17 December 2026). Continue the
  direct-fetch discipline given the meeting is now under three weeks out.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano), both primary-sourced as of edition 37 — closed thread, do
  not re-derive. **The next policy meeting date (Oct 29-30, 2026) was
  re-confirmed via a direct boj.or.jp plain-text fetch again at edition 45**,
  now five straight editions (41-45) on the direct-fetch method; see the
  general-principle entry above for the narrower numeric-rate caveat logged
  this edition.
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
  clean direct primary-source footing at edition 45** (third straight edition
  on the exact URL pattern, 43-45; see general principle entry above). H.R.
  6500 funds the government through **11 December 2026**. Watch for shutdown
  risk resurfacing as that date approaches.
- **University of Michigan preliminary October 2026 consumer sentiment —
  still not a "closed thread," watch for the final reading:** 46.3, a
  five-month low (current conditions 44.7, expectations 47.3, year-ahead
  inflation expectations 4.7%, long-run 3.5%), confirmed via
  investinglive.com and advisorperspectives.com, both dated 9 Oct 2026.
  **Final October reading due Friday 23 October 2026** — now under a week
  out from edition 45's cutoff; not re-touched since edition 40 — watch for
  it directly if edition 46's window reaches that date.
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
  date through edition 45 (re-confirmed no ruling had posted as of Monday 19
  Oct). **One edition-45 secondary source rendered the presiding judge's name
  differently than this report's established "Francis Mathew"** — treat
  "Francis Mathew" as the established name absent a corroborated correction,
  and note the discrepancy again if it recurs. This is a distinct proceeding
  from the March 2026 child-safety jury verdict ($375m) and the August 2026
  abatement ruling ($567m, under appeal) — don't conflate the three. **Still
  open — watch for the actual ruling, do not cite a specific expected date
  until one is corroborated.**
- **New calendar-awareness item from edition 40, reconfirmed relevant at
  edition 41: "equities-open, bonds-closed" US holidays need an explicit
  check every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. **Next candidate to verify when it lands: Veterans Day, Wed 11 Nov
  2026 — confirm whether that is also bonds-only before assuming.**
- **The vendor-retroactive-revision trap's locus ROTATED at edition 45 — it
  is not fixed to any one instrument.** For three straight prior editions
  (42-44), EUR/USD and GBP/USD were the recurring offenders. At edition 45,
  BOTH of those pairs' Thursday/Friday bases matched their previously-logged
  figures exactly (clean, no revision) — but **WTI's Friday 16 Oct base was
  revised from this report's own previously-logged $101.41 to a
  freshly-fetched $99.02 (approx. -2.4%), a materially larger revision than
  this report's typical small vendor-drift pattern, with no clear cause
  identified.** Every other instrument checked at edition 45 (Brent, Henry
  Hub, gold, silver, copper, and the full Treasury curve) matched its
  previously-logged Friday base exactly, zero revision. **Recommendation
  reinforced: compute every commodity/FX/Treasury %-change off a
  freshly-refetched prior-session base from the same vendor table every
  single edition, for EVERY instrument — not just the ones that drifted last
  time — and disclose every divergence found, however small.**
- **Henry Hub natural gas BROKE its five-edition streak (40-44) of base
  ambiguity at edition 45:** a fresh Investing.com fetch of the Friday 16 Oct
  base matched the previously-logged $3.116 exactly, and Monday 19 Oct's
  close/change ($3.042, -2.37%) was computed cleanly off that base. The
  November contract (NGX6) was still front-month, not yet rolled to December,
  as of edition 45. **Do not assume this instrument is now permanently
  resolved** — it has shown base ambiguity in five of the last six editions;
  continue double-checking it fresh every edition rather than treating this
  one clean read as the new default.
- **The Kitco live-spot-vs-headline cross-check WAS testable at edition 45**
  (the research pass ran the same day as the covered session, Monday evening,
  shortly before the cutoff), supporting edition 44's theory that the check
  only works without research-pass lag. What it found this time was a
  different kind of inconsistency than previously logged: Kitco's live quotes
  for gold and silver both sat below the COMEX futures settle (expected, a
  normal spot-vs-futures basis), but Kitco's own "PM Report" headline text
  ("silver holds modest gains") directly conflicted with its own live ticker,
  which showed silver down on the session — an internal inconsistency on
  Kitco's own page, not a live-vs-headline timing mismatch. Disclose this
  kind of internal conflict the same way: flagged, not resolved. **When the
  check CAN be run (same-day), expect some kind of inconsistency rather than
  a clean confirmation** — it has never yet produced a fully clean result.
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
  directions — edition 45 saw the two AGREE for the first time in several
  editions.** DXY rose +0.13% and USD/JPY rose +0.33% Monday 19 Oct, both
  positive, no sign divergence. This follows edition 44's divergent reading
  (DXY -0.22% vs. USD/JPY +0.01%). Keep disclosing the comparison every
  edition regardless of which way it goes — it is not a standing feature in
  either direction.
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
  than Section 2, since that's where the content actually belongs; edition 45
  reverted to the sector-ETF-proxy default in its usual Section 2 placement
  since no fresher CFTC data was due inside its window (next report Fri 23
  Oct).
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
  has occasionally failed to post in time. **Edition 45 found neither had
  posted for Monday 19 Oct by cutoff** — used CNBC's live-blog snippet plus
  Investrade's market review plus an SPY ETF-proxy cross-check instead, all
  three agreeing closely. Fall back to this tier (secondary outlet(s) +
  ETF-proxy triangulation) when AP/Reuters genuinely haven't posted, and
  disclose the fallback explicitly.
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
  **Edition 45 continued this discipline**, individually verifying every
  single-stock close directly against stockanalysis.com (EYPT, SLN, CLF,
  DDOG, AMZN, MTCH, NBIS, INTC, JPM, CRWV) — all matched the research pass's
  figures exactly; the exclusions this edition (IAM, the PayPal downgrade
  claim, the Silgan/Trivium and Accenture/China-sale deal-driver claims) came
  from catching claims that could not be independently corroborated at all,
  not from a close-price mismatch.
- **Premarket is not the close.** Reinforced explicitly at edition 44 (see
  the dedicated Standing Facts entry above) after three bank-earnings
  reactions in one table diverged from their premarket indications or from
  simple EPS-beat/miss framing. Always fetch the verified close separately.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent in both
  directions** — see Standing Facts entry above for edition 45's clean
  (non-divergent) reading. Continue disclosing the DXY-vs-USD/JPY directional
  comparison explicitly every edition regardless of which way it goes.
- **The Kitco live-spot-vs-headline cross-check WAS testable at edition 45**
  when the research pass ran same-day — see the dedicated Standing Facts
  entry above for what it found (an internal Kitco inconsistency, not a
  clean confirmation). Keep attempting it each edition; when research runs
  with lag past the session, expect it to be untestable per edition 44's
  structural-limitation finding.
- **GBP/USD and EUR/USD both reconciled cleanly against their previously-
  logged Thursday/Friday bases at edition 45**, breaking three straight prior
  editions (42-44) where they were the recurring vendor-revision offenders —
  see the "locus rotated" Standing Facts entry above (WTI was the offender
  instead this time). Resume the fuller multi-source method on either pair
  if a fresh same-day conflict reappears.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for nine further editions (37-45)** — edition 45 again found the full
  Treasury curve the one instrument class that reconciled perfectly against
  the prior edition's logged base (2-yr 4.74%→4.77%, +3bp; 10-yr
  5.09%→5.15%, +6bp; 30-yr 5.43%→5.48%, +5bp; 2s10s 35bp→38bp, +3bp, a mild
  bear-steepening). Treat as resolved/noise unless a fresh conflict appears.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 45 have all run clean (or
  clean after one quick fix) — **edition 45 needed one quick fix pass** (one
  source, the prior-edition AP-wire citation, drafted into Annex B without
  its matching inline `<sup>` tag — caught and given an inline citation
  before render), consistent with the established pattern of needing at most
  one quick fix pass.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 45 have all rendered with zero stray tildes on the
  first draft.** Edition 45 had none to fix.
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39 and 44 have all
  resolved this cleanly for CFTC CoT, with full OI and Asset-Manager/
  Leveraged-Funds breakdowns for ES, NQ and RTY. **The next CFTC report is
  due Friday 23 October 2026, 3:30pm ET, covering Tuesday 20 October data**
  — check cftc.gov directly at edition 46 if its window extends past that
  release time, which is likely for most plausible edition-46 cutoffs.
- **A genuinely new editorial lesson surfaced at edition 44, confirmed again
  at edition 45: overflow can be DIFFUSE across many small blocks rather than
  concentrated in one verbose table.** Edition 45's first render came out at
  5 pages (one correct pagebreak present, confirmed via `grep -n
  pagebreak`); the excess was spread thinly across the disclosure box, the
  60-second read, the market-recap paragraph, the movers-table driver cells,
  the analyst-actions paragraph, the macro-section prose, the commodities
  dagger-note, the derivatives prose, and the day-ahead table/sector-setup
  bullets. **The fix required four successive small-trim-and-re-render
  rounds** (first a broad pass shortening the movers table, earnings notes
  and analyst-actions/GE-Vernova prose; then tightening the commodities
  dagger-note and derivatives prose; then the disclosure box, market-recap
  paragraph and macro-section prose together with merging two day-ahead
  table rows and three sector-setup bullets into two; then a final one-line
  trim to the last remaining sector-setup bullet and merging the two
  smallest remaining day-ahead rows) before the render finally landed at 4
  pages. **When a 5-page render's overflow is small, check after EACH
  individual trim whether it was concentrated (one fix resolves it, per
  edition 43) or still diffuse (several more small cuts needed, per editions
  44-45) — don't assume one round of trims is sufficient; keep re-rendering
  until the page count actually drops.**
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping. **Edition 45 hit
  the most extreme spread logged yet** (SLN +125.58% vs. CLF +16.34%,
  approx. 7.7x; EYPT -85.28% vs. CLF, approx. 5.2x) and found the existing
  "(capped)" text-suffix label overlapped the y-axis tick labels even at a
  wide pad_frac — see the dedicated Standing Facts entry above for the fix
  (asterisk + x-axis-label footnote instead of a per-bar text suffix), now
  the recommended default for any future capped-outlier chart.
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists.** Edition 45 found a substantive list
  (upgrades and downgrades across several names) but, with no AP/Reuters
  wire available, it traced almost entirely to one aggregator
  (Investrade) — disclosed as such rather than treated as multi-sourced. The
  editions-40-45 pattern (empty, thin, normal, empty, empty-for-the-target-
  date, substantive-but-single-sourced) continues to look genuinely
  intermittent in both yield and sourcing depth — report whatever a genuine
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
  edition 41, followed up without resolution at editions 42-44) was NOT
  actively re-chased at edition 45** — remains an open, unconfirmed disclosed
  inference carried forward. Pick this thread back up at a future edition if
  bandwidth allows.
- **GE Vernova's Wednesday 14 Oct -6.20% decline — CLOSED at edition 45, do
  not carry forward.** See the dedicated Standing Facts entry above.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 45 all got a fresh,
  same-day-timestamped sweep** — eighteen consecutive fresh sweeps now.
  **The feed's two known bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) are genuinely intermittent, not a one-way ratchet: edition 44 saw
  both bugs hit every series simultaneously, while edition 45 saw NEITHER
  bug on any of the six series (all percent fields matched an independent
  manual calculation exactly).** Freshness and bug-presence remain two
  independent axes. **Always compute day-over-day % change manually
  regardless of how many consecutive bug-free reads preceded the current
  one** — the bugs can return (or stay absent) without warning either way.
  VIX9D-vs-spot-VIX: edition 45 saw the term structure flip from Friday's
  brief backwardation (VIX9D 20.12 > VIX 19.99) back into contango (VIX9D
  17.93 < VIX 18.44 < VIX3M 19.60 < VIX6M 21.12) as the whole complex
  unwound sharply off Friday's spike (VIX -7.75%, VIX9D -10.89%). Keep
  watching rather than assuming continuation of any prior trend.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table. **Edition 45 used this for the sector table as usual**
  (3 of 11 sectors green: Cons. Discretionary +1.78%, Technology +1.36%,
  Materials +0.06% the gainers; Utilities -2.01%, Real Estate -1.16%,
  Financials -0.83% among the eight laggards) **and reverted to the
  sector-ETF-proxy chart as chart #2** in its default Section 2 placement,
  since no fresher CFTC data was due inside edition 45's window (next report
  Fri 23 Oct). The sector table itself remains a reliable, separate
  deliverable regardless of which chart type is used.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (3 of 11 at edition 45) —
  continue treating an uncorroborated single-aggregator breadth figure as
  not usable.
- **Dealer gamma:** zerogex.io hit a **sixth consecutive edition of failure
  at edition 45** — this time the populated-landing-page/placeholder-dash
  mode (every Net GEX, Flip, Call Wall, Put Wall and Max Pain tile showed
  "--"), a repeat of the mode first seen at edition 42, not a new failure
  mode. Still fully unusable regardless. SpotGamma remains untried as an
  alternative per standing practice (it has failed for many editions).
- **Official CME FedWatch probabilities:** the page blocks fetching (edition
  45's direct attempt timed out again, a fifth consecutive failure,
  41-45) — use secondary citations (Polymarket, Kalshi, Reuters/other
  economist polls, desk notes) and give a range rather than a single
  invented number. DeFi Rate's Kalshi/Polymarket-blended aggregator remains
  a stable, consistently working source across editions 37-45, albeit with
  its own internal sub-view reconciliation gap disclosed every edition since
  43.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, now **nine consecutive failures (37-45)** — a confirmed
  structural gap, not transient. Resume the attempt-every-edition discipline
  at edition 46 regardless, but expect a block of some kind. Use Kalshi's
  own secondary reporting or DeFi Rate's blended aggregator as the
  workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has not been
  re-attempted as primary since edition 35 beyond a routine confirming try.
  **Westmetall.com has now worked cleanly TWENTY-FOUR editions running**
  as the fallback (copper -0.68% to $14,496.00/tonne at edition 45, Friday
  base unrevised at $14,595.00/tonne, confirmed exactly). Copper remains,
  along with Treasuries, one of the two instrument classes that have never
  shown the vendor-revision trap.
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve CSV and the rendered HTML TextView page **agreed cleanly
  again at edition 45** (2-yr 4.77%, 10-yr 5.15%, 30-yr 5.48%, all 19 Oct),
  extending the clean streak to **ten editions (37-45)** with no repeat of
  the edition-36 33bp gap. Keep fetching both endpoints and comparing rather
  than trusting either by default.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY). **Edition 45 confirmed directly that no new report
  has posted since Friday 16 Oct's release** (covering Tue 13 Oct 2026: ES
  OI 1,931,607, Asset Mgr net +47.42%/Leveraged Funds -21.17%; NQ OI
  279,515, AM +26.95%/LF -4.15%; RTY full-size OI 444,784, AM +6.64%/LF
  -20.61% — unchanged from edition 44's logged figures, as expected since no
  new data was due). **The next report is due Friday 23 October 2026,
  3:30pm ET, covering Tuesday 20 October data** — check cftc.gov directly at
  edition 46 if its window extends past that release time, which is likely
  for most plausible edition-46 cutoffs; re-evaluate chart #2 (fresh CFTC vs.
  sector-ETF-proxy default) based on what's actually available.
- **GBP/USD and EUR/USD clean close:** both remain fully resolved since
  edition 37/26 respectively. **Edition 45 found BOTH pairs' Thursday/Friday
  bases unrevised against their previously-logged figures** — the first
  clean read after three straight editions (42-44) of vendor-revision
  drift on this specific pair of instruments; see the "locus rotated"
  Standing Facts entry above (WTI drifted instead this edition). EUR/USD
  closed Monday at 1.1214 (-0.23% off a Friday base of 1.1240, unrevised);
  GBP/USD closed at 1.3306 (-0.17% off a Friday base of 1.3329, unrevised),
  both single-sourced to Investing.com's close-to-close history table.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot-vs-headline cross-check WAS re-tested at edition 45** (same-day
  research pass) — see the dedicated Standing Facts entry above; it found an
  internal Kitco inconsistency rather than a clean confirmation. Gold and
  silver futures continue to source cleanly via Investing.com (Mon 19 Oct:
  gold -0.70% to $4,151.65, silver -0.48% to $57.030, both off unrevised
  Friday bases).
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is now also a closed thread as of
  edition 45 — see the dedicated Standing Facts entry above. **US
  import/export prices and industrial production:** both closed threads for
  September — see Standing Facts above. **University of Michigan final
  October consumer sentiment** (see Standing Facts above): due Friday 23
  October 2026 — watch for it, now under a week out.
- **Henry Hub natural gas:** the November contract (NGX6) had NOT rolled to
  December as of edition 45 (still front-month). **The vendor-revision/base-
  ambiguity wrinkle broke its five-edition streak (40-44) at edition 45** —
  see the dedicated Standing Facts entry above for the full write-up; do not
  assume this means the instrument is now permanently resolved, continue
  double-checking it fresh every edition.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 45 found no notable
  Monday-dated single-stock options-flow/skew commentary** for the session's
  largest chip/tech movers despite targeted searches — a ninth consecutive
  empty edition on this general sub-item (37-45). Treat this sub-item as
  reliably low-yield and keep it a brief, secondary effort each edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. Not
  applicable through edition 45; next due approx. 14 November 2026, now
  under four weeks out — start watching for it in editions covering early
  November.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22). Not attempted
  again through edition 45.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully
  again at editions 39 and 44 (the latter covering Tue 13 Oct data, still
  the most recent as of edition 45's confirming check). Repeat this same
  three-instrument fetch at edition 46 when the Friday 23 Oct report should
  be available, watching for the Micro-vs-full-size Russell naming trap each
  time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 45 found a
  substantive list for Monday 19 Oct (nine upgrades, five downgrades) but,
  with no AP/Reuters wire available, nearly all of it traced to one
  aggregator — disclosed as single-sourced rather than treated as
  independently confirmed. The pattern across 37-45 (empty, thin, normal,
  empty, empty, empty, thin-but-real, empty-for-the-target-date,
  substantive-but-single-sourced) continues to look genuinely intermittent
  in both yield and sourcing depth rather than a structural change.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** Edition 45 individually re-verified every single-stock
  close directly against stockanalysis.com (10 tickers: EYPT, SLN, CLF,
  DDOG, AMZN, MTCH, NBIS, INTC, JPM, CRWV) rather than trusting the research
  pass's own figures wholesale — all matched exactly. The exclusions this
  edition (a reported "IAM" mover, a PayPal downgrade claim, the
  Silgan/Trivium and Accenture/China-sale deal-driver claims) came from
  failing independent corroboration entirely, not from a close-price
  mismatch — continue this direct-verification discipline on
  high-confidence-seeming figures, not just surprising ones.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel
  (confirmed clean at editions 37 through 43 and again at 45, eight
  editions total) — this remains correct for 10-11 categories specifically.
  For charts with fewer categories, scale the height down: roughly
  `(9.8, 1.65-1.95)` for 3-9 categories (edition 45 used `(9.8, 1.9)` for a
  9-category single-stock movers chart). **Always render and visually
  inspect (via the Read tool) the actual PNG at or near full resolution
  before embedding it**, regardless of what a past edition's success might
  suggest.
- **Capped-outlier label-overlap fix (NEW at edition 45, see the dedicated
  Standing Facts entry above for the full write-up):** when a capped bar's
  value label uses a "(capped)" text suffix, the label text can be long
  enough to visually bleed into the y-axis tick-label margin even at a wide
  pad_frac, because matplotlib's `ax.text()` is unclipped by default and the
  label's anchor point sits just outside the capped bar already. **Fix:
  shorten the per-bar suffix to a single trailing asterisk (`"*"` instead of
  `" (capped)"`) and add one footnote to the chart's x-axis label instead**
  (e.g. `"% change, Monday 19 Oct close [6] (*bar capped at ±30pts; label =
  actual value)"`). This is now the recommended default for any future
  capped-outlier chart — tune pad_frac for visual breathing room as before,
  but fix genuine text-overlap with shorter label text first, since a wider
  pad_frac alone did not fully resolve it at edition 45 (0.26 still
  overlapped; the asterisk fix combined with 0.42 finally rendered clean).
  Separately, note that even a chart with small-magnitude data (e.g. an
  11-category sector panel where every bar is under approx. 2%) can need a
  pad_frac well above the function's 0.12 default (edition 45 used 0.30) to
  avoid an analogous overlap on its own largest bar — the needed value
  scales with the data's own span, not category count or chart type.
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
  single concentrated overflow — editions 44 and now 45 are both clear
  examples of DIFFUSE overflow** (see the dedicated Hard Rules entry above
  for edition 45's full write-up): small excess spread across many blocks,
  needing four successive small-trim-and-re-render rounds to fully resolve
  at edition 45 (vs. roughly five at edition 44) — re-render after every
  round rather than guessing the total cut needed up front. **A large,
  suspicious blank area at the bottom of a page (as opposed to a page that's
  merely a bit short) is usually caused by an atomic block** — most often a
  chart `<img>` — not fitting in the remaining space and being pushed whole
  to the next page; neither edition 44's nor edition 45's overflow showed
  this pattern (no atomic block was pushed whole — content simply ran a
  fraction of a page too long across several blocks each time).
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix. Edition 45's
  "Commodities and FX" table fit entirely on page 3 without needing to split
  across a page boundary.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  A visibly short page 3 (or in editions 44-45's case, page 4) has recurred
  at several earlier editions, each needing a genuinely additive fix (never
  a padding table that just repeats an existing table's rows) OR, as at
  editions 44-45, a genuinely diffuse set of small trims. **Edition 45
  converged after four rounds of edit-and-re-render**, each round checked by
  re-rendering immediately rather than batching multiple guessed trims
  together — budget for this iterative pattern on any edition with a
  borderline page count.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across editions 40 through
45's very different content volumes (40 needed a padding table to fill page
3, 41 and 42 both filled naturally with no padding needed, 43 needed a
content TRIM to avoid overflow on a very high single-stock-volume session,
44 and 45 both needed several small content trims across multiple sections
to avoid a diffuse overflow, 45 converging in four rounds vs. 44's five.
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
  page; editions 44 and 45 both folded commodities, FX and Treasuries into
  ONE combined table (10-14 rows) as the PRIMARY commodities table rather
  than padding, since both sessions needed trimming rather than filling.
  **On a high-single-stock-volume earnings day (many reporters/movers in one
  session), the opposite problem is more likely — watch the movers table
  specifically for verbosity (multi-clause driver text, rows that could
  share a combined cell) before assuming the page budget is safe.** Always
  re-render immediately after adding (or removing) any content to confirm
  the page count, rather than assuming a change is safe. **When overflow is
  small and diffuse (editions 44-45 pattern), trim a little from several
  sections rather than gutting one** — day-ahead table rows, earnings-table
  note cells, movers-table driver cells, sector-setup bullets and
  macro/derivatives/commodities prose paragraphs are all good, low-cost
  candidates to shave a clause or merge a row from first; edition 45 needed
  trims across eight distinct spots before the page count actually dropped
  from 5 to 4.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across twenty eligible
editions, 25 through 45, with editions 34, 39 and 44 the exceptions when
fresher CFTC data was available; edition 45 reverted to this default since
the CFTC's next report was not yet due inside its window). Fresh CFTC CoT
data on a Monday/weekend-window edition → the ES/NQ/RTY asset-manager-vs-
leveraged-funds positioning chart, normalized as % of open interest, built
with the grouped-bar technique documented under Production notes, placed in
Section 5 (Derivatives) per the editions 24/34/39/44 precedent. A single
dominant earnings print with a clean, well-sourced implied-vs-realized-move
story → a three-bar implied/historical-average/realized move chart (the
historical-average leg has never actually been sourced successfully). A
genuine multi-sector broadening/deepening selloff across consecutive
sessions → the sector-ETF proxy rendered as a grouped (day-over-day) bar
instead of single-day. A holiday-window preview edition with no fresher
data → VIX futures term structure with event annotations. When chart 1
(movers) already covers the earnings/single-name story, the sector proxy
(or a fresh CFTC positioning chart, when available) is a good complementary
choice even on a stock-heavy day, since the two stories reinforce rather
than duplicate each other. **Edition 46 should check cftc.gov's freshness
first** (the Friday 23 Oct report, covering Tuesday 20 Oct) before
defaulting back to the sector-ETF proxy — if CFTC data has posted fresh by
edition 46's cutoff (likely for most plausible cutoffs given the 3:30pm ET
release time), use the fresh CFTC chart per the established technique;
otherwise revert to the sector-ETF-proxy default as usual. **Remember the
figsize-scales-to-category-count guidance above (ceiling `(9.8, 1.95)` for
an 11-category panel, `(9.8, 2.15)` for the 3-category grouped CFTC chart,
scale down for fewer single-series categories) and the capped-outlier
asterisk/footnote fix regardless of which chart type is chosen.**

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–42 (condensed):** established the format (edition 1 baseline;
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
render.

**Edition 43 (condensed)** — Friday 16 October 2026 report covering
Thursday 15 October 2026. A second straight blowout inflation print
(September PPI, +1.3% m/m/+6.3% y/y) landed hours after Wednesday's hot CPI,
yet Fed rate-path odds barely moved. An overnight memory-chip rout (Kospi
-8%) dragged the Nasdaq down approx. 1.9% intraday before a sharp reversal
on Nvidia CEO Jensen Huang's on-record defense of CoreWeave's balance sheet;
all four major indices closed green (S&P +0.33% to 7,744.10, Dow +1.08% to
52,177.81, Nasdaq +0.08% to 26,713.03, Russell +1.38% to 2,767.28), recovered
via a new fallback sourcing tier (Investrade market-review + ETF-proxy +
multi-blog corroboration) after AP's wire was unavailable with no
syndication mirror. TSMC delivered a record Q3 yet fell on cautious 2027
commentary. Bank earnings extended the "beat yet fall" pattern (Schwab
-2.73%; U.S. Bancorp +2.01%). Ericsson's Q3 beat drove the session's largest
single-stock move (+11.80%). GE Vernova (-1.63%) and Rocket Lab (-6.64%,
Thu) both went unexplained (Rocket Lab resolved edition 44; GE Vernova's Wed
14 Oct move resolved edition 45). Fastly's unexplained-mover streak closed
quietly. Commodities/FX reconciliation work broadened: six of eleven
instruments showed a Wednesday base that had silently shifted since edition
42 logged it. Treasuries rallied broadly and reconciled perfectly clean. The
VIX complex retreated on a full clean raw-fetch sweep (VIX -2.43% to 16.46).
CFTC CoT confirmed not yet posted. Dealer gamma (zerogex) hit a fourth,
hybrid failure mode. 50 sources, clean 46/50 on the first `check_refs.py`
pass, zero stray tildes, clean 4-page render.

**Edition 44 (condensed)** — Monday 19 October 2026 report covering Friday
16 October 2026 plus the weekend. Equities fell broadly Friday (S&P -1.09%
to 7,659.44, Dow -0.34% to 52,002.41, Nasdaq -2.14% to 26,140.03 — its worst
week since June, -4.5% — Russell -1.66% to 2,721.37) as renewed AI-infra.
spending doubts hit chipmakers hardest (Micron -5.63%, Intel -5.79%); the
Dow's defensive weighting left it the week's only green major index (+0.7%).
AP's wire posted via La Nación syndication, cross-checked cleanly against an
independent source. Sector rotation was a clean value/defensive split (6 of
11 SPDR sectors green, Energy led tracking WTI's +3.51% gain). The VIX
complex spiked hard (VIX +21.45% to 19.99) with both documented CBOE feed
bugs appearing on every series simultaneously for the first time. Five of
the day's largest movers had no confirmed catalyst (Bending Spoons -15.60%,
Telkom Indonesia -13.69%, GRAIL -13.03%, Vicor -12.92%, Nebius -12.18%).
Rocket Lab's Thu 15 Oct -6.64% decline resolved (Neutron launch delay to
2027). Bank earnings continued the "beat yet mixed reaction" pattern across
five large banks. J.B. Hunt's FreightWaves "+12%" headline claim was flatly
wrong (actual close -2.78%) — a new sourcing-trap instance. The FOMC's Oct
28 decision/press-conference time was confirmed (2:30pm ET) via the Fed's
monthly events calendar. September import/export prices and industrial
production both printed hot without moving Fed odds, which instead eased
further (DeFi Rate: Oct hike approx. 28%→13-14%). China's Q3 GDP release
date was disputed (resolved edition 45: Monday 19 Oct). Commodities: oil led
higher (WTI +3.51%, Brent +3.72%); Henry Hub fell -3.71% (base ambiguity
resolved edition 45); gold/silver rose modestly with the Kitco cross-check
untestable. EUR/USD and GBP/USD both showed Thursday-base revisions (a third
straight edition, resolved edition 45); DXY and USD/JPY diverged in
direction (resolved/agreed edition 45). CFTC CoT finally posted fresh data
(Tue 13 Oct), used as chart #2 in Section 5 — building it required new
grouped-bar chart code and a figure-level-legend fix. Dealer gamma hit a
fifth consecutive failure. The first HTML draft rendered at 5 pages from
diffuse overflow, fixed through roughly five rounds of small trims. 41
sources, clean 41/41 on the first `check_refs.py` pass after one quick fix,
one stray tilde caught and fixed before render, clean 4-page render.

**Edition 45 (most recent — full detail)** — Tuesday 20 October 2026 report
covering Monday 19 October 2026, research window Sun 18 Oct 2026 20:00 ET
through Mon 19 Oct 2026 20:21 ET (the window's one NYSE session). Verified
the two structural header rules again — now clean across thirteen
(date-line) and seventeen (window-line) consecutive applicable editions
respectively.

**Equities rebounded broadly Monday** (S&P 500 +0.41% to 7,690.73, Dow
-0.07% to 51,966.03, Nasdaq Composite +1.11% to 26,430.89, Russell 2000
+0.25% to 2,728.30) after last week's worst week since June, led by a
tech/consumer-discretionary rotation back into names sold off in Friday's
chip-led selloff; breadth stayed narrow (3 of 11 SPDR sectors green —
Consumer Discretionary +1.78%, Technology +1.36%, Materials +0.06% the
gainers; Utilities -2.01% and Real Estate -1.16% among the eight laggards as
the 10-year yield rose 6bp). **Neither AP nor Reuters had posted a wire for
the session by cutoff** — a new fallback tier was used (CNBC's live-blog
search snippet + Investrade's market review + an SPY ETF-proxy check, all
agreeing closely) and disclosed explicitly as a weaker sourcing tier than
usual; most individual single-stock-mover catalysts and the full
analyst-action roundup traced to Investrade alone, flagged accordingly.
**Biotech produced the day's extremes**: Silence Therapeutics +125.58% to
$19.58 on a $20.00/ADS Merck KGaA all-cash buyout (closing almost exactly at
the deal price), and EyePoint Pharmaceuticals -85.28% to $0.44 after a
late-stage trial failed to maintain vision gains and the company cut over
half its staff — both the most extreme single-session movers logged to
date, requiring the chart's outlier-capping mechanism and surfacing a new
label-overlap bug (fixed via an asterisk+footnote pattern, documented in
Production notes). Other movers: Cleveland-Cliffs +16.34% on a Q3 adjusted
EPS beat; Datadog +5.36% (Bernstein upgrade); Amazon +4.98% (Morgan
Stanley "Top Pick," independently corroborated); Match Group +4.14%
(Evercore upgrade); Nebius +2.88% (neocloud-group bounce); Intel +2.43%
(JPMorgan upgrade, independently corroborated); JPMorgan -1.82% (largest Dow
drag, no identified catalyst). CoreWeave was flat (-0.44%) despite a
Goldman upgrade/price-target-cut combination. Fifth Third Bancorp disclosed
both GAAP ($0.90) and adjusted ($1.13) EPS cleanly in its 8-K, closing only
+0.28% (muted). **Two claims were found and excluded** after failing
independent corroboration: a reported "IAM" Monday mover (internally
inconsistent in its own source, likely conflating Iambic Therapeutics'
actual Thursday 15 Oct IPO) and an unconfirmed PayPal "Cleveland" downgrade
(PYPL itself closed flat) — both logged as a new ticker-confusion/
internal-inconsistency sourcing trap. **GE Vernova's Wed 14 Oct -6.20%
decline (open since edition 42) was CLOSED with a caveat** after a fourth
search attempt found a plausible but not fully confirming explanation
(a modest Susquehanna PT trim, profit-taking ahead of its now-confirmed Oct
28 earnings date, Wind-margin concerns, broad market weakness) — closed per
the Fastly precedent. **China's Q3 GDP release-date dispute (open since
edition 44) was RESOLVED**: it printed Monday 19 Oct (+4.5% y/y, +1.2% q/q,
cumulative +4.6% y/y), confirmed directly against the NBS English release.
Standing Fed facts all re-verified unchanged (Kevin Warsh Fed Chair, fed
funds 3.75%-4.00%, FOMC Oct 27-28 with the press conference at 2:30pm ET on
the 28th, BoE holds 3.75% next decision 5 Nov, no shutdown through 11 Dec);
BoJ's next-meeting date was re-confirmed directly but its numeric policy
rate (approx. 1.25%) could only be re-confirmed via secondary sources this
edition. Rate-path odds (DeFi Rate): Oct 28 hold approx. 84-86%, Dec 8-9
hike approx. 73-81%, roughly flat week-over-week; Kalshi (ninth straight
failure) and CME FedWatch (fifth straight failure) both failed direct fetch
again. The US-China tariff implementation notice remains unresolved despite
a genuine direct federalregister.gov/ustr.gov attempt (bot-check wall;
404). New Mexico v. Meta remains pending with no ruling date.
**Commodities/FX: the vendor-retroactive-revision trap's locus rotated** —
WTI's Friday base was revised a notable approx. -2.4% (from $101.41 to
$99.02, no clear cause), while EUR/USD and GBP/USD (the prior three
editions' offenders) both reconciled cleanly this time, as did Brent,
gold, silver, copper and the full Treasury curve. **Henry Hub broke its
five-edition streak of base ambiguity**, reading cleanly off an unrevised
Friday base (-2.37% to $3.042). DXY (+0.13%) and USD/JPY (+0.33%) agreed in
direction for the first time in several editions. The Kitco live-spot
cross-check, run same-day for the first time in several editions, found an
internal Kitco inconsistency (its own "PM Report" text contradicting its
ticker on silver's direction) rather than a clean confirmation. Treasuries
rose across the curve (10-yr +6bp to 5.15%, 2s10s +3bp to 38bp, a mild bear-
steepening) on both CSV and TextView agreeing for a tenth straight edition.
**Derivatives: the VIX complex unwound sharply off Friday's spike** (VIX
-7.75% to 18.44, VIX9D -10.89% to 17.93), flipping the term structure from
backwardation back into contango; neither of the feed's two known bugs
appeared on this pull, a clean read breaking edition 44's all-series-
affected occurrence. No options-flow/skew commentary was found for Monday
(ninth consecutive empty edition). Dealer gamma (zerogex) hit a sixth
consecutive failure, a repeat of the populated-landing-page/placeholder-dash
mode first seen at edition 42. CFTC CoT confirmed no new data as expected
(next due Fri 23 Oct). Chart #2 reverted to the sector-ETF-proxy default
(no fresher CFTC data due inside the window), ending edition 44's one-
edition CFTC-chart interruption. **A new editorial lesson, a direct
continuation of edition 44's**: the first HTML draft again rendered at 5
pages from diffuse overflow (spread across the disclosure box, 60-second
read, market-recap paragraph, movers-table driver cells, analyst-actions
paragraph, macro-section prose, commodities dagger-note, derivatives prose,
and the day-ahead table/sector-setup bullets) — fixed through four
successive small-trim-and-re-render rounds, converging slightly faster than
edition 44's five. 33 sources, clean 33/33 on the first `check_refs.py` pass
after one quick fix (one Annex-B-only orphan given its inline citation),
zero stray tildes on the first draft, clean 4-page render after the
diffuse-overflow trim rounds.

**Open threads for edition 46:** the US-China "30-for-30" tariff
implementation notice remains unresolved despite three editions (43, 44,
45) checking directly against USTR.gov/federalregister.gov — make another
direct attempt. The CFTC CoT report due Friday 23 October 2026 (covering
Tue 20 Oct data) should land inside edition 46's window if its cutoff
extends past 3:30pm ET that day — check cftc.gov directly and expect fresh
data; re-evaluate chart #2 (fresh CFTC vs. sector-ETF-proxy default) based
on what's actually available. University of Michigan's final October
consumer-sentiment reading is due Friday 23 October — now under a week out,
watch for it directly at edition 46 if the window reaches that date. New
Mexico v. Meta's ruling is still pending, expected "later in October" per
the 1 Oct hearing — watch for the actual date/ruling, don't re-cite a
specific expected date until confirmed; also note one edition-45 source
rendered the judge's name differently than the established "Francis
Mathew" — flag again if it recurs. Q3 Employment Cost Index is due 30
October. The FOMC meets 27-28 October with its press-conference time
confirmed (2:30pm ET) — the next edition whose covered session falls on/
after the meeting date should lead with the decision. BoJ's exact numeric
policy rate (approx. 1.25%) was only secondary-sourced at edition 45 — try
a direct numeric read off boj.or.jp's rate/guideline-specific page next
time it needs re-confirming. The JPMorgan EPS-miss-framing and Wells
Fargo/Citigroup credit-provision-selloff-rationale threads from editions
41-42 remain open, unconfirmed disclosed inferences — revisit if bandwidth
allows. The "preview-consensus-only miss/beat framing" caution was not
re-chased at edition 45 and remains open. JPMorgan's Monday 19 Oct -1.82%
decline (the Dow's largest drag) has no identified catalyst — a new,
not-yet-chased thread; attempt a search if it recurs or if bandwidth
allows. 13F filings are due approx. 14 November 2026, now under four weeks
out — start watching for it in editions covering early November. Threads
closed after resolution rather than carried further: GE Vernova's Wed 14
Oct -6.20% decline (closed with caveat per the Fastly precedent); China's
Q3 GDP release-date dispute (resolved — printed Monday 19 Oct); Henry
Hub's five-edition base-ambiguity streak (broken this edition, though not
assumed permanently resolved); EUR/USD and GBP/USD's three-edition vendor-
revision streak (broken this edition, locus rotated to WTI instead); the
DXY-vs-USD/JPY divergence (agreed this edition, genuinely intermittent in
both directions).
