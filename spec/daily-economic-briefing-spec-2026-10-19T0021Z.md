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
  through 44 have all applied this correctly** ("Friday 2 October 2026"
  through "Monday 19 October 2026" as the date line in each respective
  edition, with the window line carrying the session(s) covered) — now
  confirmed stable across twelve consecutive editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 44 all reused the
  same pattern for single-session (or single-session-plus-weekend) windows —
  now confirmed clean across sixteen consecutive editions (29 through 44;
  edition 44 phrased it "Window: Thu 15 Oct 2026 20:00 ET – Sun 18 Oct 2026
  20:21 ET (Fri 16 Oct close/AH + weekend)"). No further confirmation needed;
  treat this as settled.

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
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 44
  directly against federalreserve.gov. **The decision/press-conference time
  question is now CLOSED, resolved at edition 44 after three straight prior
  editions (42, 43, and earlier) failed to find it:** the FOMC-specific
  calendar page (`federalreserve.gov/monetarypolicy/fomccalendars.htm`) still
  shows only the date, no time, but a DIFFERENT Fed-owned page — the monthly
  events calendar at `federalreserve.gov/newsevents/2026-october.htm` —
  directly displays "FOMC Press Conference" at **2:30pm ET on October 28,
  2026** (statement expected approx. 2:00pm ET per secondary corroboration).
  **For future editions needing a meeting TIME specifically (not just a date),
  try the `newsevents/YYYY-month.htm` events-calendar URL pattern first** —
  it is the one that actually works for this purpose; reserve
  `fomccalendars.htm` for date-only confirmation. The following meeting is
  December 8-9, 2026 (an SEP meeting).
- **Rate-path odds eased further toward "hold" at edition 44, continuing this
  cycle's pattern of hot inflation-adjacent prints not moving the Fed:**
  DeFi Rate's Kalshi/Polymarket-blended aggregator, fresh snapshot Sunday 18
  Oct 2026 approx. 8pm ET, shows **October 27-28 hike odds approx. 13-14%**
  (hold approx. 86-87%) and **December 8-9 hike odds approx. 73-77%** — a
  sharp further easing from Thursday 15 Oct's post-PPI read of approx.
  28%/77% (edition 43), even though September import/export prices (released
  Fri 16 Oct) ran hot (import +1.1% m/m/+8.1% y/y, the fastest 12-month rise
  since July 2022). **DeFi Rate's own page again carried an internally
  inconsistent view at edition 44** — its summary, meeting-table, and
  "7-day movers" sub-views disagreed with each other by 3-4 percentage points
  on both the October and December reads — the same reconciliation gap
  logged at edition 43, now confirmed recurring rather than one-off; disclose
  it every edition rather than silently picking one of DeFi Rate's own
  sub-views. Kalshi's own direct fetch failed again (HTTP 429) at edition 44,
  now **eight** consecutive failures (37-44). Official CME FedWatch also
  failed again directly (timeout) at edition 44, a fourth consecutive
  failure (41-44). The composite "at least one more hike in 2026" read has
  still not been freshly re-pulled since edition 38 (last known approx. 80%)
  — don't cite without a fresh pull.
- **US-China "30-for-30" tariff framework — closed thread as of edition 37, do
  not re-open:** 77 US product categories (household goods, textiles,
  appliances, toys, sporting goods, vacuum flasks) and 1,619 Chinese
  categories (dominated by food/farm goods, plus some medical devices;
  soybeans, chips, EVs and batteries excluded from both sides), each side's
  treatment benchmarked at approx. $30bn against 2024 bilateral trade,
  confirmed directly against whitehouse.gov's own Terms of Reference
  document. Still pending each side's domestic legal processes for actual
  implementation — no Federal Register/USTR implementation notice has been
  found through edition 44, though edition 44's check was only secondary
  (a Covington & Burling client alert stating no effective date has been
  published), NOT a direct USTR.gov/federalregister.gov fetch — a regression
  from the direct-fetch discipline used at prior editions. **Make a direct
  USTR.gov/federalregister.gov fetch attempt at edition 45** rather than
  relying on the secondary source again.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates, government funding status) from memory or from the prompt's own
  framing — verify it fresh from a primary source (federalreserve.gov,
  bankofengland.co.uk, boj.or.jp, kansascityfed.org, norges-bank.no,
  riksbank.se, banxico.org.mx, snb.ch, rba.gov.au, whitehouse.gov, etc.) every
  edition, exactly like any other data point. **Edition 44 re-confirmed Kevin
  Warsh as Fed Chair directly against federalreserve.gov's Board of Governors
  bios page — a fifteenth straight direct re-confirmation.** The BoE's next
  decision (Thursday 5 November) was freshly re-touched at edition 44 via a
  direct bankofengland.co.uk fetch — unchanged, now confirmed directly for
  six straight editions (39-44). The shutdown/CR status check remained on a
  clean direct primary-source footing at edition 44: a direct whitehouse.gov
  fetch of `https://www.whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500/`
  confirms H.R. 6500 (the Continuing Appropriations and Extensions Act, 2027,
  signed 2 September 2026) funds federal agencies through **11 December
  2026**, no shutdown in effect — this exact URL pattern is now confirmed
  working for two straight editions (43-44); reuse it directly. The BoJ's
  next-meeting-date primary source stayed confirmed via direct read at
  edition 44: a direct boj.or.jp fetch of its Monetary Policy Meeting
  schedule page confirmed Oct 29 (Thu) – Oct 30 (Fri), 2026 in plain text,
  unchanged, now four straight editions (41-44) on the restored direct-fetch
  method.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed directly
  again at edition 44 (following decision 17 December 2026). Continue the
  direct-fetch discipline every edition given the meeting is now under three
  weeks out.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano), both primary-sourced as of edition 37 — closed thread, do
  not re-derive. **The next policy meeting date (Oct 29-30, 2026) was
  re-confirmed via a direct boj.or.jp plain-text fetch again at edition 44**,
  now four straight editions (41-44) on the direct-fetch method.
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
- **September 2026 Import/Export Price Indexes — NEW at edition 44, closed
  thread, do not re-derive:** import prices **+1.1% m/m / +8.1% y/y** (the
  largest 12-month increase since July 2022), export prices **+2.2% m/m /
  +11.6% y/y**; export prices to China specifically +2.7% m/m (largest
  monthly rise since March 2022) / +7.5% y/y, import prices from China +3.1%
  y/y. Released Friday 16 October 2026, 8:30am ET, confirmed directly
  against bls.gov. Despite running hot, this did not move Fed rate-path odds
  hawkish (odds eased further the same session — see above), extending this
  cycle's pattern of inflation-adjacent data no longer moving the Fed-odds
  needle much.
- **September 2026 Industrial Production & Capacity Utilization (G.17) — NEW
  at edition 44, closed thread, do not re-derive:** total industrial
  production **+0.7% m/m / +2.2% y/y**, manufacturing output +0.3% m/m/+1.1%
  y/y, capacity utilization **76.9%**. Released Friday 16 October 2026,
  9:15am ET, confirmed directly against federalreserve.gov's G.17 release.
  The Fed flagged an annual benchmark revision to this series due 24 November
  2026 — watch for a level reset around that date, not a genuine month-over-
  month signal.
- **No US federal government shutdown is in effect — status re-confirmed on a
  clean direct primary-source footing at edition 44** (second straight
  edition on the direct-fetch method; see general principle entry above for
  the URL pattern). H.R. 6500 funds the government through **11 December
  2026**. Watch for shutdown risk resurfacing as that date approaches.
- **University of Michigan preliminary October 2026 consumer sentiment —
  still not a "closed thread," watch for the final reading:** 46.3, a
  five-month low (current conditions 44.7, expectations 47.3, year-ahead
  inflation expectations 4.7%, long-run 3.5%), confirmed via
  investinglive.com and advisorperspectives.com, both dated 9 Oct 2026.
  **Final October reading due Friday 23 October 2026** — watch for it; not
  re-touched since edition 40, now under 5 days out at edition 44's cutoff.
- **China September 2026 CPI/PPI — RESOLVED at edition 42, closed thread, do
  not re-derive:** CPI **+0.9% y/y** (+0.2% m/m), PPI **+5.0% y/y** (the
  fastest PPI rise since June 2022), driven by fuel costs. Sourced to gov.cn's
  English-language NBS-attributed news release (stats.gov.cn itself remained
  stale/unreachable) — continue treating the gov.cn English release as an
  acceptable near-primary substitute if stats.gov.cn remains unreachable.
- **China Q3 2026 GDP — NEW open thread at edition 44, watch for the actual
  release:** secondary calendars disagree on the release date (one source
  says Monday 19 Oct, a competing source says Tuesday 20 Oct); could not be
  confirmed directly against the National Bureau of Statistics (stats.gov.cn)
  at edition 44. **Check stats.gov.cn (or the gov.cn English NBS mirror, per
  the standing CPI/PPI workaround) directly at edition 45 once the print has
  actually landed, and reconcile which date was correct.**
- **New Mexico v. Meta — still an open thread, no specific ruling date
  confirmed:** the penalty-phase hearing (following the jury's late-September
  verdict that Meta violated the state's Unfair Practices Act roughly 43.9
  million times, re: hate-speech policy and its Cambridge Analytica response)
  was held Thursday 1 October 2026 before Judge Francis Mathew in Santa Fe.
  New Mexico is seeking **$35-40bn** in penalties (reduced from the statutory
  theoretical maximum of approx. $219bn at $5,000/violation); Meta is asking
  the judge to cap penalties at **$3.45bn**. Judge Mathew has indicated he
  expects to rule "later in October" 2026 — no outlet has given a specific
  date through edition 44 (re-confirmed no ruling had posted as of Sunday 18
  Oct). **Still open — watch for the actual ruling, do not cite a specific
  expected date until one is corroborated.** This is a distinct proceeding
  from the March 2026 child-safety jury verdict ($375m) and the August 2026
  abatement ruling ($567m, under appeal) — don't conflate the three.
- **New calendar-awareness item from edition 40, reconfirmed relevant at
  edition 41: "equities-open, bonds-closed" US holidays need an explicit
  check every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. **Next candidate to verify when it lands: Veterans Day, Wed 11 Nov
  2026 — confirm whether that is also bonds-only before assuming.**
- **The vendor-retroactive-revision trap (first logged edition 41, broadened
  at editions 42-43) RECURRED AGAIN at edition 44 on EUR/USD and GBP/USD —
  now logged on the same pair of instruments for a THIRD consecutive
  edition.** At edition 44, a fresh fetch of Thursday 15 Oct's EUR/USD base
  showed +0.56% (vs. edition 43's own logged +0.50%), and GBP/USD showed
  +0.62% (vs. edition 43's logged +0.58%) — both small (6-8bp) but real,
  continuing drift rather than a one-off. WTI, Brent and Henry Hub could not
  be cleanly compared against edition 43's logged Wednesday/Thursday figures
  this edition since edition 44's commodities pass used Thursday-to-Friday
  changes throughout (a different comparison window), so no fresh read on
  whether those three still show the same revision pattern — **check WTI,
  Brent and Henry Hub specifically against this edition's own logged Friday
  16 Oct figures next time, not just EUR/USD and GBP/USD.** Treasuries and
  copper again reconciled cleanly against the prior edition's logged base —
  the one instrument class (Treasuries) and one instrument (copper, via
  Westmetall) that have never shown this trap. **Recommendation unchanged:
  compute every commodity/FX/Treasury %-change off a freshly-refetched
  prior-session base from the same vendor table, never off the
  previously-logged figure, and disclose every divergence found.**
- **Henry Hub natural gas remains the worst-sourced instrument in the
  report, now a FIFTH consecutive edition (40-44) with some form of base
  ambiguity.** At edition 44, a fresh Investing.com fetch of the same table
  used for Thursday 15 Oct and Friday 16 Oct gave a self-consistent pair
  ($3.198 Wed-equivalent-row / actually this edition's own Thu-to-Fri read
  was $3.236 Thu → $3.116 Fri, -3.71%), with the $3.198 figure matching only
  ONE of edition 43's three mutually conflicting Wednesday reference points
  (the "re-fetched table" value) — still not reconciled against the other
  two (edition 42's logged $3.289, or the "live-quote previous close"
  $3.240). An EIA Henry Hub spot series (cash, not futures — a genuinely
  different series) gave a rough same-ballpark sanity check ($3.10-3.22) but
  could not be date-mapped cleanly enough to serve as independent
  confirmation. **Continue disclosing this instrument's base ambiguity every
  edition rather than attempting to force a resolution** — it has not
  resolved across five editions and there is no indication a sixth attempt
  would succeed where five didn't.
- **A new, narrower trap logged for the first time at edition 44: the
  documented Kitco live-spot-vs-headline cross-check cannot be meaningfully
  re-tested after the fact.** Kitco does not appear to retain or expose a
  historical intraday "live spot" snapshot for a past session — when edition
  44's research (conducted Sun 18 Oct, two days after the Friday 16 Oct
  session it was checking) tried to re-run the standing Kitco live-quote-vs-
  headline comparison for Friday, only a live quote dated to the actual
  fetch time (18 Oct) was retrievable, not a historical Friday snapshot.
  **This is likely a structural limitation of the check, not an edition-44-
  specific failure: the Kitco cross-check can only be meaningfully performed
  if the research pass runs on gold/silver DURING or very shortly after the
  session being covered, not from a later research window.** Future editions
  should still attempt it, but expect this same limitation to recur whenever
  the research pass runs with any lag past the session's close, and disclose
  it as a structural gap rather than treating a successful check as the
  default.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company (owns AOL, Evernote,
  WeTransfer, Issuu and other consumer/SaaS apps), IPO'd 1 July 2026 at
  $29/share (above its $26-28 range), rising approx. 41% on debut to a
  approx. $25bn market value. Logged here so a future edition doesn't waste
  effort re-verifying the ticker's legitimacy if it moves sharply again.
- **A new sourcing trap logged for the first time at edition 44: a named
  secondary outlet's own percentage-move headline can be flatly wrong, not
  just stale or mistimed.** A FreightWaves headline claimed J.B. Hunt shares
  "jumped approx. 12%" after its Thursday 15 Oct after-close earnings beat;
  the stock's own verified Friday 16 Oct close was actually **down 2.78%**
  (confirmed directly via stockanalysis.com's price-history table) — the
  opposite direction entirely, not just a different magnitude. The claim was
  disclosed and excluded rather than repeated. **Treat any single-sourced,
  named-outlet percentage-move headline as a claim to verify against the
  underlying price-history table before using it, not as a citable fact on
  its own** — this is a stronger version of the existing "snapshot mistaken
  for close" caution, since here the entire direction was wrong, not just
  the timing.
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
- **The DXY-vs-its-own-FX-crosses conflict RECURRED at edition 44** — DXY
  fell -0.22% Friday while USD/JPY rose a marginal +0.01%, an opposite-sign
  divergence (though USD/JPY's move was economically negligible in
  magnitude, 1-2 pips). This continues to confirm the divergence pattern is
  genuinely intermittent, not a standing feature in either direction — keep
  disclosing the comparison every edition regardless of which way it goes.

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
  uniqueness of use (editions 33-44 have all done this for stockanalysis.com
  single-stock closes and other repeatedly-used outlets, confirmed stable
  across twelve editions). **Citing the prior edition itself as a source**
  (e.g. "[4] Daily Economic Briefing, edition 43, logged prior-session
  baseline figures") is a legitimate, already-used pattern when disclosing a
  divergence against a previously-logged figure — editions 43 and 44 have
  both done this cleanly with `check_refs.py`.
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart 2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes). **Chart
  placement is editorial, not fixed to Section 2** — editions 24, 34, 39 and
  now **44** all placed a CFTC-positioning chart #2 in Section 5
  (Derivatives) rather than Section 2, since that's where the content
  actually belongs. Editions 35 through 43 (nine straight) had reverted to
  the sector-ETF-proxy default (no fresher CoT data due in any of those
  editions) and kept it in its default Section 2 placement — edition 44
  broke that streak once fresh CFTC data finally posted inside its window.
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
  has occasionally failed to post in time. **Edition 44 used AP's wire
  successfully via La Nación syndication** (the same syndication-mirror
  fallback tier documented at prior editions), cross-checked against an
  independent "Tapeboard Market Pulse" source with only trivial rounding
  differences — a clean, high-confidence reconciliation with no fallback
  tier needed beyond the standard syndication mirror.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Edition 44 found a new, stronger version of this trap, logged
  above as its own entry: a FreightWaves headline's percentage-move claim
  for J.B. Hunt was not just mistimed but flatly contradicted by the stock's
  own verified close (claimed "+12%," actual close -2.78%).** Always check a
  dated article's own claimed magnitude against the underlying price-history
  table, not just its date, before repeating it.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  **Edition 44 continued this discipline**, independently re-verifying via
  direct stockanalysis.com fetches every single-stock close the equities
  research pass reported (TFC, MTB, TRV, RF, CFG, AA, JBHT, BSP, TLK, GRAL,
  VICR, NBIS, CRGY, MU, INTC) before drafting — all matched the research
  pass's figures exactly, giving high confidence, and the extra verification
  pass caught the FreightWaves JBHT magnitude error (the pass itself had
  flagged it as unverified; the direct re-fetch confirmed the actual
  direction was negative, not just unconfirmed-positive).
- **Premarket is not the close.** Reinforced explicitly at edition 44 (see
  the dedicated Standing Facts entry above) after three bank-earnings
  reactions in one table diverged from their premarket indications or from
  simple EPS-beat/miss framing. Always fetch the verified close separately.
- **The DXY-vs-its-own-FX-crosses conflict RECURRED at edition 44** — see
  Standing Facts entry above. Continue disclosing the DXY-vs-USD/JPY
  directional comparison explicitly every edition regardless of which way it
  goes.
- **The Kitco live-spot-vs-headline conflict could not be tested at edition
  44** — a likely structural limitation when the research pass runs with any
  lag past the covered session's close (see the dedicated Standing Facts
  entry above). Keep attempting it each edition, but do not expect it to be
  testable every time, and disclose the limitation rather than silently
  skipping it when it isn't.
- **GBP/USD's data-quality problem has now stayed resolved for eight further
  editions (37-44)**, though edition 44 again logged the vendor-revision
  pattern on its Thursday base (a base-revision disclosure, not a same-day
  conflict — see Standing Facts above). Resume the fuller multi-source
  method if a fresh same-day conflict reappears.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for eight further editions (37-44)** — edition 44 again found Treasuries
  the one commodity/FX-adjacent instrument class that reconciled perfectly
  against the prior edition's logged base (2-yr 4.74%, down 3bp; 10-yr
  5.09%, down 1bp; 30-yr 5.43%, unchanged; 2s10s widened 2bp to 35bp, a bull
  steepening). Treat as resolved/noise unless a fresh conflict appears.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 44 have all run clean (or
  clean after one quick fix) — **edition 44 needed one quick fix pass**
  (six sources initially drafted into Annex B without their matching inline
  `<sup>` tags — CFG, Alcoa, JBHT, the FreightWaves claim, the Employment
  Cost Index homepage, and Westmetall's copper note — all caught and given
  inline citations before render), consistent with the established pattern
  of needing one quick fix pass.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 44 have all rendered clean after at most one quick
  fix.** Edition 44's first draft had exactly one stray `~` (in a disclosure-
  box sentence about a FreightWaves "~12%" claim) — fixed immediately.
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39 and now **44** have
  all resolved this cleanly for CFTC CoT, with full OI and Asset-Manager/
  Leveraged-Funds breakdowns for ES, NQ and RTY. **The next CFTC report is
  due Friday 23 October 2026, 3:30pm ET, covering Tuesday 20 October data**
  — check cftc.gov directly at edition 45 if its window extends past that
  release time.
- **A genuinely new editorial lesson surfaced at edition 44, distinct from
  edition 43's: overflow can be DIFFUSE across many small blocks rather than
  concentrated in one verbose table.** Edition 44's first render came out at
  5 pages (one correct pagebreak present, confirmed via `grep -n
  pagebreak`), but unlike edition 43's single-table-driven overflow, the
  excess here was spread thinly across the earnings-table note cells, the
  day-ahead table's row count, the sector-setup bullets, and the CFTC/VIX/
  zerogex prose in Section 5 — no single block was egregiously long. **The
  fix required iterating across five or six separate small trims/merges
  (shortening earnings-table notes to one clause each, merging day-ahead
  table rows by overlapping date range, condensing the Section 5 prose
  paragraphs, and merging sector-setup bullets) rather than one decisive
  structural fix.** When a 5-page render's overflow is small (spilling by
  under half a page onto the notional 4th content page), check whether it is
  concentrated (ed. 43 pattern — one fix resolves it) or diffuse (ed. 44
  pattern — needs several small cuts across sections) before assuming one
  trim will be sufficient; re-render after each round to track convergence.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at edition 44 (BSP -15.60% vs. TLK -13.69%, about 1.14x), left uncapped.
  Edition 30 remains the one genuine 10x+ case to date. No need to revisit
  the threshold or mechanism absent a genuinely new edge case.
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists.** Edition 44 found essentially nothing
  dated specifically to Friday 16 Oct — the one KeyBanc Rocket Lab
  price-target cut found was dated to Thursday 15 Oct's Neutron-delay news,
  not Friday. Editions 40-43 pattern (empty, thin, normal, empty) plus
  edition 44 (empty again for the target date specifically) continues to
  look genuinely intermittent — report whatever a genuine search attempt
  turns up each edition, including "nothing dated to this exact session."
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38** — when a secondary-sourced EPS figure conflicts sharply with
  a primary filing's GAAP number without a stated basis, prefer the primary
  filing and flag the secondary figure in Annex A. **Edition 44 logged
  several more clean non-trap confirmations of the contrasting, legitimate
  pattern**: Truist, M&T Bank, Citizens Financial and Alcoa all disclosed
  both a GAAP and an adjusted EPS figure clearly labelled by the company
  itself — reported in full per the Delta/JNJ/UnitedHealth/Bank of America/
  Schwab precedent, not treated as a conflict.
- **The "preview-consensus-only miss/beat framing" caution (first logged at
  edition 41, followed up without resolution at edition 42-43) was NOT
  actively re-chased at edition 44** — remains an open, unconfirmed disclosed
  inference carried forward. Pick this thread back up at a future edition if
  bandwidth allows.
- **Rocket Lab's Thursday 15 Oct -6.64% decline — RESOLVED/CLOSED at edition
  44, do not carry forward.** The company disclosed the inaugural Neutron
  launch has slipped from 2026 into 2027 on a booster "forward dome"
  manufacturing issue; KeyBanc cut its price target to $100 from $135. Found
  via Trendspider, Sherwood News and an iTiger/Financial Modeling Prep
  aggregation, all converging on the same dated event even though the exact
  logged percentage varied slightly by source (-6.64% to -7.85% across
  sources) — treated as resolved given the consistent dated catalyst, not
  held open over the percentage variance.
- **GE Vernova's Wednesday 14 Oct -6.20% decline remains unexplained after a
  THIRD genuine search attempt (edition 44)** — no dated driver for 14 Oct
  has been found across three consecutive editions (42, 43, 44). **Consider
  the Fastly precedent at edition 45: if a fourth genuine search attempt
  also comes up empty, it may be acceptable to let this lapse as an
  unresolved historical move without forcing a retroactive explanation**
  (per the precedent set when Fastly's own four-session unexplained-mover
  streak was allowed to close quietly at edition 43 once the name reverted
  to unremarkable moves) — but make the fourth attempt first before invoking
  that precedent.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 44 all got a fresh,
  same-day-timestamped sweep** — seventeen consecutive fresh sweeps now.
  **However, edition 44 marks an important escalation worth tracking
  separately from "freshness": the feed's two known bugs (a duplicated
  `prev_day_close`, and a `price_change_percent` that divides by current
  price instead of prior close) appeared on EVERY ONE of the six series
  simultaneously for the first time** — previously these bugs were
  intermittent and partial (hitting some series, some editions). Freshness
  (same-day timestamps) and bug-presence are two independent axes; a "clean
  sweep" going forward should specify which axis it refers to. **Always
  compute day-over-day % change manually regardless of how many consecutive
  bug-free reads preceded the current one** — edition 44 shows the bugs can
  return in full force without warning. VIX9D-vs-spot-VIX: edition 44 saw a
  full sign reversal, from -2.49 (Thu) to **+0.13** (Fri) — a flip into
  slight backwardation, not just a narrowing or widening. Keep watching
  rather than assuming continuation of any prior trend.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table. **Edition 44 used this for the sector table as usual**
  (6 of 11 sectors green: Energy +2.52%, Utilities +1.34%, Cons. Staples
  +1.08%, Materials +0.71%, Financials +0.45%, Real Estate +0.40% the
  gainers; Industrials -0.08%, Health Care -0.27%, Cons. Discretionary
  -0.84%, Comm. Services -1.89%, Technology -3.02% the five laggards) **but
  used the fresh CFTC positioning data as chart #2 instead of the sector
  panel**, ending the sector-ETF-proxy chart's nine-edition run (35-43) as
  the default. The sector table itself remains a reliable, separate
  deliverable regardless of which chart type is used.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (6 of 11 at edition 44) —
  continue treating an uncorroborated single-aggregator breadth figure as
  not usable.
- **Dealer gamma:** zerogex.io hit a **fifth consecutive edition of
  failure at edition 44**, this time best described as a repeat/combination
  of two previously-seen modes rather than a clean new one: the front-end
  still shows the populated-shell placeholder-dash pattern (first seen
  edition 42), while `/api/gex/spx` reverted to the edition-40/41-style 401
  auth-gated response and `/api/gex` gave the edition-42-style 404. **This
  breaks the prior four-editions-running pattern of "a new failure mode
  every time"** — edition 44's failure recombines elements of modes already
  seen rather than introducing a fifth distinct one. Still fully unusable
  regardless. SpotGamma remains untried as an alternative per standing
  practice (it has failed for many editions).
- **Official CME FedWatch probabilities:** the page blocks fetching (edition
  44's direct attempt timed out again, a fourth consecutive failure,
  41-44) — use secondary citations (Polymarket, Kalshi, Reuters/other
  economist polls, desk notes) and give a range rather than a single
  invented number. DeFi Rate's Kalshi/Polymarket-blended aggregator remains
  a stable, consistently working source across editions 37-44, albeit with
  its own internal sub-view reconciliation gap disclosed every edition since
  43.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, now **eight consecutive failures (37-44)** — a confirmed
  structural gap, not transient. Resume the attempt-every-edition discipline
  at edition 45 regardless, but expect a block of some kind. Use Kalshi's
  own secondary reporting or DeFi Rate's blended aggregator as the
  workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has not been
  re-attempted as primary since edition 35 beyond a routine confirming try.
  **Westmetall.com has now worked cleanly TWENTY-THREE editions running**
  as the fallback (copper +0.39% to 14,595.00/tonne at edition 44 — the unit
  label was not explicitly re-confirmed on this specific fetch, though
  USD/tonne remains the series' standard convention; double-check the label
  explicitly next time it's fetched). Copper's Thursday base again matched
  the prior edition's logged figure exactly — the one commodity instrument
  besides Treasuries that has never shown the vendor-revision trap.
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve CSV and the rendered HTML TextView page **agreed cleanly
  again at edition 44** (2-yr 4.74%, 10-yr 5.09%, 30-yr 5.43%, all 16 Oct),
  extending the clean streak to **nine editions (37-44, plus 39's
  confirmation)** with no repeat of the edition-36 33bp gap. Keep fetching
  both endpoints and comparing rather than trusting either by default.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY). **Fresh data finally posted inside edition 44's
  window** (released Fri 16 Oct 2026, 3:30pm ET, covering Tue 13 Oct 2026):
  ES OI 1,931,607 (Asset Mgr net +47.42% of OI, Leveraged Funds net
  -21.17%); NQ OI 279,515 (Asset Mgr net +26.95%, Leveraged Funds -4.15%);
  RTY full-size OI 444,784 (Asset Mgr net +6.64%, Leveraged Funds -20.61%).
  Versus the prior (9 Oct, covering 6 Oct) read, leveraged funds covered
  net-short NQ/RTY exposure meaningfully while asset managers cut RTY
  net-long exposure by over 4 points even as RTY open interest grew approx.
  4.6% — a still-crowded split that predates Friday 16 Oct's own equity
  selloff entirely (the CoT data is dated Tuesday 13 Oct). VIX futures (CFE)
  OI was 448,469, Asset Managers/Institutional net short 17.23% (the usual
  structural short-vol posture), Leveraged Funds flat at +0.25% — this
  secondary CFE detail was cut from the edition-44 draft for page-budget
  reasons, not because it's unavailable; restore it if space allows. **The
  next report is due Friday 23 October 2026, 3:30pm ET, covering Tuesday 20
  October data** — check cftc.gov directly at edition 45 if its window
  extends past that release time, which is likely for most plausible
  edition-45 cutoffs.
- **GBP/USD and EUR/USD clean close:** both remain fully resolved since
  edition 37/26 respectively, subject to the standing vendor-revision
  caveat on their PRIOR-session base (not a same-day conflict). **Edition 44
  single-sourced both to Investing.com's close-to-close history table again**
  (EUR/USD +0.18% Fri off a freshly-fetched +0.56% Thu base; GBP/USD +0.40%
  Fri off a freshly-fetched +0.62% Thu base) — both Thursday bases had
  shifted again from edition 43's own logged figures (+0.50%→+0.56% and
  +0.58%→+0.62% respectively), continuing the vendor-revision pattern for a
  third consecutive edition on this specific pair of instruments.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot-vs-headline cross-check could not be re-tested at edition 44** —
  see the dedicated Standing Facts entry above on this likely being a
  structural, not intermittent, limitation when the research pass runs with
  any lag past the session's close. Gold and silver futures continue to
  source cleanly via Investing.com (Fri 16 Oct: gold +0.26% to $4,181.10,
  silver +0.26% to $57.305), with direction independently corroborated via
  Upstox at edition 44.
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is a new open thread at edition 44
  — see the dedicated Standing Facts entry above (release date disputed
  between secondary sources, 19 vs. 20 Oct). **US import/export prices and
  industrial production:** both released as scheduled on Friday 16 October
  2026 and are now closed threads for September — see Standing Facts above.
  **University of Michigan final October consumer sentiment** (see Standing
  Facts above): due Friday 23 October 2026 — watch for it, now under 5 days
  out.
- **Henry Hub natural gas:** the November contract (NGX6) had NOT rolled to
  December as of edition 44 (still front-month). **The vendor-revision/base-
  ambiguity wrinkle is now a FIFTH consecutive edition (40-44) data-quality
  issue specific to this instrument** — see the dedicated Standing Facts
  entry above for the full write-up; more severe and longer-running than any
  other commodity/FX vendor-revision case logged to date. Still not labeled
  an official CME settlement print by any vendor checked.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 44 found no notable
  Friday-dated single-stock options-flow/skew commentary** for the session's
  largest chip movers (Micron, Intel) despite targeted searches — an eighth
  consecutive empty edition on this general sub-item (37-44). Treat this
  sub-item as reliably low-yield and keep it a brief, secondary effort each
  edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. Not
  applicable through edition 44; next due approx. 14 November 2026, now
  under four weeks out — start watching for it in editions covering early
  November.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22). Not attempted
  again through edition 44.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully
  again at editions 39 and now **44** (the latter covering Tue 13 Oct data).
  Repeat this same three-instrument fetch at edition 45 when the Friday 23
  Oct report should be available, watching for the Micro-vs-full-size
  Russell naming trap each time (confirmed again at edition 44: used the
  full-size RTY contract, OI 444,784, not the Micro).
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 44 found
  essentially nothing dated specifically to Friday 16 Oct (the one KeyBanc
  Rocket Lab cut found was dated to Thursday 15 Oct's news, already covered
  under the Rocket Lab driver resolution, not as a standalone Friday
  action). The pattern across 37-44 (empty, thin, normal, empty, empty,
  empty, thin-but-real, empty-for-the-target-date) continues to look
  genuinely intermittent rather than a structural change.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** Edition 44 individually re-verified every single-stock
  close directly against stockanalysis.com (15 tickers: TFC, MTB, TRV, RF,
  CFG, AA, JBHT, BSP, TLK, GRAL, VICR, NBIS, CRGY, MU, INTC) rather than
  trusting the research pass's own figures wholesale — all matched exactly
  except the JBHT direction (see the new FreightWaves-trap entry above),
  which the verification step caught. Continue this direct-verification
  discipline on high-confidence-seeming figures, not just surprising ones.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel
  (confirmed clean at editions 37 through 43, seven straight) — this remains
  correct for 10-11 categories specifically. For charts with fewer
  categories, scale the height down: roughly `(9.8, 1.65-1.85)` for
  3-8 categories. **Edition 44 used `(9.8, 1.8)` with `pad_frac=0.24` for an
  8-category single-stock movers chart** (BSP, TLK, GRAL, VICR, NBIS, CRGY,
  INTC, MU), continuing the identical pairing used at editions 41-43 (now
  four consecutive editions), rendered cleanly on the first attempt with no
  label overlap. **Always render and visually inspect (via the Read tool)
  the actual PNG at or near full resolution before embedding it**,
  regardless of what a past edition's success might suggest.
- **NEW at edition 44: a grouped (two-series) horizontal bar chart — needed
  for the CFTC Asset-Manager-vs-Leveraged-Funds positioning chart — requires
  custom chart code, not the standard single-series `barh()` helper used for
  the movers/sector charts.** The standard helper only plots one value per
  category; the CFTC chart needs two bars (Asset Manager, Leveraged Funds)
  per category (ES/NQ/RTY), offset vertically by a fixed height fraction
  (`h=0.32` worked cleanly for 3 categories) around each category's tick
  position. **A genuine first-attempt bug worth flagging:** an axis-level
  `ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.46), ...)` placed
  the legend so far below the axes that it overlapped the x-axis label text
  — both rendered in the same visual band. **Fix that worked: use a
  FIGURE-level legend (`fig.legend(handles, labels, loc="lower center",
  bbox_to_anchor=(0.5, 0.0), ...)`) combined with
  `fig.tight_layout(rect=(0, 0.1, 1, 1))`** to explicitly reserve the bottom
  10% of the figure for the legend, clear of the x-axis label. Figsize
  `(9.8, 2.15)` (taller than the movers chart's 1.8-1.95 range, to
  accommodate the reserved legend band) rendered cleanly on the second
  attempt. **Reuse this exact pattern (`fig.legend` + `tight_layout(rect=...)`
  + the taller `2.15` figsize) for any future grouped/multi-series chart**
  rather than re-deriving the legend-placement fix from scratch.
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
  single concentrated overflow either — edition 44 is the clearest example
  yet of DIFFUSE overflow** (see the dedicated Hard Rules entry above for the
  full write-up): small excess spread across the earnings-table notes, the
  day-ahead table, the sector-setup bullets and the Section 5 prose, needing
  five or six separate small trims rather than one structural fix. **A large,
  suspicious blank area at the bottom of a page (as opposed to a page that's
  merely a bit short) is usually caused by an atomic block** — most often a
  chart `<img>` — not fitting in the remaining space and being pushed whole
  to the next page; edition 44's overflow did not show this pattern (no
  atomic block was pushed whole — content simply ran a fraction of a page
  too long across several blocks).
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix. **Edition 44's
  "Commodities and FX" and "The day ahead" tables both split across a page
  boundary naturally** (table header stayed with the first rows on the
  earlier page, remaining rows continued on the next page with no repeated
  header) — confirmed safe, not an issue.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  A visibly short page 3 has recurred at several earlier editions, each
  needing a genuinely additive fix (never a padding table that just repeats
  an existing table's rows). Edition 43 hit the opposite problem (overflow,
  concentrated in one table). **Edition 44 hit overflow again but diffuse
  this time** — iterative re-rendering after each small trim (rather than
  guessing the total cut needed up front) was the practical approach that
  converged after approximately five rounds of edit-and-re-render. Budget
  for this iterative pattern rather than expecting one edit to resolve a
  diffuse overflow.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across editions 40 through
44's very different content volumes (40 needed a padding table to fill page
3, 41 and 42 both filled naturally with no padding needed, 43 needed a
content TRIM to avoid overflow on a very high single-stock-volume session,
44 needed several small content trims across multiple sections to avoid a
diffuse overflow). Treat as the durable default; the lever to pull on a
high-volume or diffusely-long day is merging/trimming redundant content
across whichever sections are longest, not loosening the CSS further.)
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
  page; edition 44 used a 10-row version of this table as its PRIMARY
  commodities table (merging WTI/Brent and Gold/Silver into combined rows to
  save space), not as padding, since the session needed trimming rather than
  filling. **On a high-single-stock-volume earnings day (many
  reporters/movers in one session), the opposite problem is more likely —
  watch the movers table specifically for verbosity (multi-clause driver
  text, rows that could share a combined cell) before assuming the page
  budget is safe.** Always re-render immediately after adding (or removing)
  any content to confirm the page count, rather than assuming a change is
  safe. **When overflow is small and diffuse (edition 44 pattern), trim a
  little from several sections rather than gutting one** — day-ahead table
  rows, earnings-table note cells, and Section 5 prose paragraphs are all
  good, low-cost candidates to shave a clause or merge a row from first.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across nineteen eligible
editions, 25 through 43, with editions 34, 39 and now **44** the
exceptions when fresher CFTC data was available). Fresh CFTC CoT data on a
Monday/weekend-window edition → the ES/NQ/RTY asset-manager-vs-leveraged-
funds positioning chart, normalized as % of open interest — **edition 44
used this chart type, built with the new grouped-bar technique documented
under Production notes above, and placed it in Section 5 (Derivatives)
rather than Section 2, following the editions 24/34/39 precedent for
CFTC-content placement.** A single dominant earnings print with a clean,
well-sourced implied-vs-realized-move story → a three-bar implied/
historical-average/realized move chart (the historical-average leg has
never actually been sourced successfully). A genuine multi-sector
broadening/deepening selloff across consecutive sessions → the sector-ETF
proxy rendered as a grouped (day-over-day) bar instead of single-day. A
holiday-window preview edition with no fresher data → VIX futures term
structure with event annotations. When chart 1 (movers) already covers the
earnings/single-name story, the sector proxy (or, as at edition 44, a
fresh CFTC positioning chart) is a good complementary choice even on a
stock-heavy day, since the two stories reinforce rather than duplicate each
other. **Edition 45 should check cftc.gov's freshness first** (the Friday
23 Oct report, covering Tuesday 20 Oct) before defaulting back to the
sector-ETF proxy — if CFTC data has NOT posted fresh by edition 45's
cutoff, revert to the sector-ETF-proxy default as usual. **Remember the
figsize-scales-to-category-count guidance above (ceiling `(9.8, 1.95)` for
an 11-category panel, `(9.8, 2.15)` for the 3-category grouped CFTC chart,
scale down for fewer single-series categories) regardless of which chart
type is chosen.**

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–41 (condensed):** established the format (edition 1 baseline;
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
`check_refs.py` pass, zero stray tildes, clean 4-page render.

**Edition 42 (condensed)** — Thursday 15 October 2026 report covering
Wednesday 14 October 2026. September CPI printed hot (headline +0.6% m/m/
+3.7% y/y, core +0.3%/+2.6%), triggering the broadest risk-off session in
weeks (S&P -1.11% to 7,718.94, Nasdaq -1.88%, Russell -1.90%) with a sharp
defensive rotation (Health Care/Staples led, Tech lagged, only 3 of 11
sectors green); the Dow held almost flat (-0.09%). AP's wire 403'd again;
closes recovered via CNBC/Yahoo/TheStreet and reconciled arithmetically.
Bank of America's GAAP EPS fell to $1.08 on a $1.2bn regulatory-settlement
charge (adjusted approx. $1.25, both company-disclosed); Morgan Stanley beat
cleanly on EPS and revenue but still fell with the market. CoreWeave
(-15.46%) and Oracle (-8.83%) led single-stock decliners on renewed
AI-infrastructure-funding-stress; Fastly (-7.72%) and GE Vernova (-6.20%)
both went unexplained. Bumble's buyout mystery resolved (Ithaca Holdings,
$6.05/share, confirmed via 8-K, not a split). No analyst action dated to 14
October was found for any name. Rate-path odds repriced sharply hawkish on
the CPI print (DeFi Rate: Oct hike approx. 19%→29%, Dec approx. 78%); a
conflicting Seeking Alpha 49.3% CME-FedWatch-attributed claim could not be
verified. China's September CPI/PPI finally posted (CPI +0.9% y/y, PPI
+5.0% y/y) via gov.cn's English NBS release after stats.gov.cn failed again.
The US shutdown/funding re-confirmation regressed to secondary-only this
edition. Commodities swung hard: silver futures -6.14% (the sharpest
single-session commodity move logged all cycle), gold futures -1.06%, both
contradicted by a mistimed Kitco live spot quote conflicting with Kitco's
own headline — a new sourcing trap. The Treasury curve flattened (2-yr +3bp
to 4.82%, 10-yr -2bp to 5.19%, 30-yr -4bp to 5.52%). The vendor-
retroactive-revision trap broadened further (WTI, Henry Hub revised again;
for the first time hit FX — EUR/USD, GBP/USD, USD/JPY all drifted). The DXY-
vs-USD/JPY divergence pattern resumed after a 3-session pause. The VIX
complex spiked hard (VIX +10.48% to 16.87, VIX9D +21.68%, VVIX +10.62%) with
neither CBOE feed bug recurring despite the large move. zerogex hit a third,
distinct failure mode (populated page shell, all-placeholder values). CFTC
CoT confirmed no fresh data as expected. 49 sources, clean 47/49 on the
first `check_refs.py` pass (two Annex-B-only orphans fixed), zero stray
tildes, clean 4-page render on the first attempt.

**Edition 43 (condensed)** — Friday 16 October 2026 report covering
Thursday 15 October 2026, research window Wed 14 Oct 20:00 ET – Thu 15 Oct
20:21 ET. A second straight blowout inflation print (September PPI, +1.3%
m/m/+6.3% y/y) landed hours after Wednesday's hot CPI, yet Fed rate-path
odds barely moved (a genuine non-reaction). An overnight memory-chip rout
(Kospi -8%) dragged the Nasdaq down approx. 1.9% intraday before a sharp
reversal on Nvidia CEO Jensen Huang's on-record defense of CoreWeave's
balance sheet; all four major indices closed green (S&P +0.33% to 7,744.10,
Dow +1.08% to 52,177.81, Nasdaq +0.08% to 26,713.03, Russell +1.38% to
2,767.28), recovered via a new fallback sourcing tier (Investrade
market-review + ETF-proxy + multi-blog corroboration) after AP's wire was
unavailable with no syndication mirror. TSMC delivered a record Q3 (EPS
$4.60/ADR, FY26 guide lifted) yet fell on cautious 2027 commentary. Bank
earnings extended the "beat yet fall" pattern (Schwab -2.73% despite a
clean GAAP/adjusted EPS disclosure; U.S. Bancorp +2.01%). Ericsson's Q3 beat
drove the session's largest single-stock move (+11.80%). GE Vernova
(-1.63%) and Rocket Lab (-6.64%, Thu) both went unexplained (Rocket Lab
resolved at edition 44; GE Vernova's underlying Wed 14 Oct move remains
open). Fastly's unexplained-mover streak closed quietly. Commodities/FX
reconciliation work broadened significantly: six of eleven instruments
(WTI, Henry Hub, gold, EUR/USD, GBP/USD, USD/JPY) showed a Wednesday base
that had silently shifted since edition 42 logged it; Henry Hub specifically
carried a third conflicting Wednesday reference point. Treasuries rallied
broadly and were the one instrument class that reconciled perfectly clean.
The VIX complex retreated on a full clean raw-fetch sweep (VIX -2.43% to
16.46). CFTC CoT confirmed not yet posted. Dealer gamma (zerogex) hit a
fourth, hybrid failure mode. A new editorial lesson: the first HTML draft
rendered at 5 pages from genuine content overflow in a verbose 15-row
movers table, fixed by merging same-driver rows. 50 sources, clean 46/50 on
the first `check_refs.py` pass, zero stray tildes, clean 4-page render.

**Edition 44 (most recent — full detail)** — Monday 19 October 2026 report
covering Friday 16 October 2026 plus the weekend, research window Thu 15
Oct 2026 20:00 ET through Sun 18 Oct 2026 20:21 ET (the window's one NYSE
session was Friday 16 Oct; no material weekend corporate news was found
after a genuine search). Verified the two structural header rules again —
now clean across twelve (date-line) and sixteen (window-line) consecutive
applicable editions respectively.

**Equities fell broadly Friday** (S&P 500 -1.09% to 7,659.44, Dow -0.34% to
52,002.41, Nasdaq Composite -2.14% to 26,140.03 — its worst week since June,
-4.5% — Russell 2000 -1.66% to 2,721.37) as renewed doubts about the
durability of AI-infrastructure spending hit chipmakers hardest (Micron
-5.63% to $878.84, Intel -5.79% to $89.85, both independently re-verified
directly against stockanalysis.com); the Dow's heavier value/defensive
weighting limited its decline and left it the week's only green major index
(+0.7%). AP's wire posted successfully via La Nación syndication this time,
cross-checked against an independent "Tapeboard Market Pulse" source with
only trivial rounding differences — no fallback tier beyond the standard
syndication mirror was needed. Sector rotation was a clean value/defensive
split: 6 of 11 SPDR sector ETFs closed higher (Energy +2.52% led, tracking
WTI's +3.51% gain; Technology -3.02% and Communication Services -1.89%
lagged on the chip selloff). The VIX complex spiked hard (VIX +21.45% to
19.99, VIX9D +44.02% to 20.12, VVIX +18.74% to 109.91) with BOTH documented
CBOE feed bugs (duplicated prior-close, wrong-denominator %-change)
appearing on every single series simultaneously for the first time — all
%-changes computed manually. The VIX9D-vs-VIX gap flipped from -2.49
Thursday to +0.13 Friday, a full sign reversal into slight backwardation.
**Five of the day's largest single-stock movers had no confirmed dated
catalyst despite genuine search attempts**: Bending Spoons (BSP, -15.60% to
$47.07, a Nasdaq-listed Italian software/app holding company that IPO'd 1
July 2026 — newly covered, logged as a legitimate ticker for future
reference), Telkom Indonesia (TLK, -13.69%), GRAIL (GRAL, -13.03%), Vicor
(VICR, -12.92%, a second straight double-digit decline) and Nebius Group
(NBIS, -12.18%); Crescent Energy (CRGY, +10.07%) led a broader small-cap
E&P rally tracking the day's oil gain rather than any individual catalyst.
**Rocket Lab's Thursday 15 Oct -6.64% decline (open since edition 43) was
RESOLVED**: the inaugural Neutron launch slipped to 2027 on a booster
"forward dome" manufacturing issue, KeyBanc cutting its price target to
$100 from $135. **GE Vernova's Wednesday 14 Oct -6.20% decline remains
unexplained after a third genuine search attempt** — a fourth attempt is
warranted at edition 45 before considering the Fastly-precedent "let it
lapse" option. Bank earnings continued the "beat yet mixed reaction"
pattern across five large banks: Truist's premarket -2.53% plunge (on a
$1.4bn AFS-securities-loss-driven revenue miss) reversed to a +1.07% close;
M&T Bank beat on EPS/revenue yet fell -1.54% on NIM/provision
deterioration; Travelers beat big and rose +1.47% despite a 34% y/y rise in
catastrophe losses; Regions Financial beat on EPS and rose +0.51% despite a
slight revenue miss; Citizens Financial beat on EPS, missed slightly on
revenue, and closed essentially flat (-0.11%). Four Thursday after-close
reporters were followed up: Alcoa beat and rose +2.55%; J.B. Hunt beat
in-line on EPS but fell -2.78% — **a FreightWaves headline claiming shares
"jumped approx. 12%" could not be corroborated at all and was the opposite
direction of the verified close, a new sourcing-trap instance logged
in full in the Standing Facts section**; Interactive Brokers, WaFd and
Independent Bank Corp all beat or met expectations but sit outside this
report's bias sectors and their Friday reactions could not be confirmed.
No analyst actions dated specifically to Friday 16 Oct were found and
verified. **The FOMC's Oct 28 decision/press-conference time was CONFIRMED
(2:30pm ET)** via a different Fed-owned page (the monthly events calendar)
after the FOMC-specific calendar page had failed to show a time for three
straight prior editions — closed thread, URL pattern logged for reuse.
September import/export prices (released Fri 16 Oct) ran hot (import +1.1%
m/m/+8.1% y/y, the fastest 12-month rise since July 2022) and September
industrial production also printed (+0.7% m/m, capacity utilization 76.9%)
— neither moved Fed rate-path odds hawkish; odds instead eased further
toward "hold" (DeFi Rate: Oct hike approx. 28%→13-14%, Dec approx. 77%→
73-77%), continuing this cycle's pattern. DeFi Rate's own internal
sub-views (summary/meeting-table/7-day-movers) disagreed by 3-4 points on
both meetings for a second straight edition — disclosed, not resolved.
Kalshi (8th straight failure) and CME FedWatch (4th straight failure) both
failed direct fetch again. New Mexico v. Meta remains pending with no
ruling and no specific date. China's Q3 GDP release date is disputed
between secondary sources (19 vs. 20 Oct) — a new open thread. Commodities:
oil led higher (WTI +3.51% to $101.41, Brent +3.72% to $109.86, both
single-sourced to Investing.com with no independent settlement
confirmation found this edition); Henry Hub fell -3.71% to $3.116, still
the worst-sourced instrument in the report (a fifth consecutive edition of
base ambiguity); gold and silver both rose modestly (+0.26% each) with the
standing Kitco live-spot-vs-headline cross-check UNTESTABLE this edition — a
newly-identified likely structural limitation (Kitco does not appear to
expose historical intraday snapshots, so the check may only be performable
when the research pass runs same-day). EUR/USD and GBP/USD both showed
their Thursday base revised again vs. edition 43's own logged figures, a
third consecutive edition of this specific vendor-revision pattern on this
pair of instruments; DXY and USD/JPY diverged in direction (a recurrence of
the standing intermittent conflict). Treasuries and copper both reconciled
perfectly clean against the prior edition's logged base, as usual. **CFTC
CoT finally posted fresh data (Tue 13 Oct) for the first time in six
editions**, used as chart #2 (placed in Section 5, per the editions
24/34/39 precedent for CFTC content), ending the sector-ETF-proxy chart's
nine-edition run as the default — building the chart required new grouped-
bar chart code and a figure-level-legend fix, both documented in Production
notes. Dealer gamma (zerogex) hit a fifth consecutive failure, this time a
repeat/combination of two previously-seen modes rather than a clean new
one. **A new editorial lesson**: the first HTML draft rendered at 5 pages
from DIFFUSE overflow (small excess spread across the earnings table,
day-ahead table, sector-setup bullets and Section 5 prose, not one
concentrated block) — fixed through roughly five rounds of small trims and
merges with re-rendering after each round, a different pattern from edition
43's single-table-driven overflow. 41 sources, clean 41/41 on the first
`check_refs.py` pass after one quick fix (six sources needed their inline
citation added), one stray tilde caught and fixed before render, clean
4-page render after the diffuse-overflow trim rounds.

**Open threads for edition 45:** GE Vernova's Wednesday 14 Oct -6.20%
decline remains unexplained after three search attempts — make a fourth
attempt, and consider the Fastly-precedent "let it lapse" option if that
also fails. China's Q3 2026 GDP release date is disputed (19 vs. 20 Oct) —
check stats.gov.cn (or the gov.cn English NBS mirror) directly once the
print has landed and reconcile. The US-China "30-for-30" tariff
implementation check regressed to secondary-only at edition 44 — make a
direct USTR.gov/federalregister.gov fetch attempt at edition 45. The CFTC
CoT report due Friday 23 October 2026 (covering Tue 20 Oct data) should
land inside edition 45's window if its cutoff extends past 3:30pm ET that
day — check cftc.gov directly and expect fresh data; re-evaluate chart #2
(fresh CFTC vs. sector-ETF-proxy default) based on what's actually
available. University of Michigan's final October consumer-sentiment
reading is due Friday 23 October — now very close, watch for it directly at
edition 45 if the window reaches that date. New Mexico v. Meta's ruling is
still pending, expected "later in October" per the 1 Oct hearing — watch
for the actual date/ruling, don't re-cite a specific expected date until
confirmed. Q3 Employment Cost Index is due 30 October. The FOMC meets
27-28 October with its press-conference time now confirmed (2:30pm ET) —
the next edition to fall on/after the meeting date should lead with the
decision. The JPMorgan EPS-miss-framing and Wells Fargo/Citigroup
credit-provision-selloff-rationale threads from editions 41-42 remain open,
unconfirmed disclosed inferences — revisit if bandwidth allows. The
"preview-consensus-only miss/beat framing" caution was not re-chased at
edition 44 and remains open. Threads closed after resolution rather than
carried further: Rocket Lab's Thursday 15 Oct -6.64% decline (closed —
Neutron launch delay to 2027, KeyBanc PT cut); the FOMC decision/press-
conference time (closed — 2:30pm ET confirmed via the Fed's monthly events
calendar, a working URL pattern now logged for reuse); the "which chart #2"
nine-edition sector-ETF-proxy streak (closed by the fresh CFTC data finally
posting — re-evaluate fresh each edition going forward, no standing default
assumption either way until cftc.gov is checked).
