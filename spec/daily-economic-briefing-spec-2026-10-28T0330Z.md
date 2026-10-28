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
figure cannot be verified, it goes in Annex B.

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
  through 49 have all applied this correctly** ("Friday 2 October 2026"
  through "Monday 26 October 2026" as the date line in each respective
  edition, with the window line carrying the session(s) covered) — now
  confirmed stable across seventeen consecutive editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 49 all reused the
  same pattern — now confirmed clean across twenty-one consecutive editions
  (29 through 49; edition 49 phrased it "Window: Thu 22 Oct 2026 20:00 ET –
  Sun 25 Oct 2026 20:21 ET (Fri 23 Oct close/AH, the window's one NYSE
  session)"). No further confirmation needed; treat this as settled.

## Schedule
Run every weekday. Pick the trigger's local time so the effective research
cutoff lands roughly 4 hours after the US market close (20:15 ET) — during
US daylight time that's 00:00 UTC; adjust for standard time. On Mondays
(or after any gap), cover the full window back to the previous edition's
cutoff, including the weekend.

## Standing facts — settled ones carry forward, live ones verify fresh

**Read this before working the list below.** Standing facts are in two tiers
and they get different treatment. The old rule — re-verify everything, every
edition — was right about the live ones and wasteful about the rest: by
edition 47 the Fed Chair had been directly re-confirmed eighteen editions
running, unchanged every time, and that fetch displaced research that had
somewhere to go.

- **Live — verify fresh from a primary source every edition.** A moving value
  or a scheduled next change: current policy rates, upcoming meeting dates,
  rate-path odds, whether a scheduled event has happened yet, government
  funding status and its expiry, and every open thread below.
- **Settled — carry forward, do not re-verify.** Qualifies only when both
  hold: directly confirmed unchanged on three or more consecutive editions,
  *and* changeable only through a discrete announced event that the day's own
  research would surface anyway. Entries below marked **SETTLED** are done;
  do not spend a fetch on them.

A settled entry re-opens on exactly three triggers, and otherwise not at all:
a **contradiction** surfaced by any research pass (verify before drafting);
its **named expiry** landing; or the **monthly audit** — on the first edition
of each calendar month, re-confirm every settled entry directly, then record
the date. That is one sweep a month instead of one a day, so a change nobody
reported still surfaces within weeks rather than never. **The next monthly
audit falls on the first edition of November 2026** — whichever edition
covers the first NYSE session on or after 1 Nov 2026 (Monday 2 November
2026, since Nov 1 is a Sunday) should re-confirm the full settled list
directly. Given this report's one-edition-per-session cadence, that is very
likely edition 55 (dated approx. 2026-11-03) — NOT edition 50 through 54,
all of which cover sessions in late October. **This remains an important
upcoming housekeeping item but is no longer the single most urgent one; the
FOMC decision (very likely edition 52) takes priority.**

A date does not promote itself. A future meeting date is live until it
passes; only afterwards is it settled history. When you do promote something,
write the date and source of its last direct confirmation and the event that
would invalidate it — a tier with no audit trail is just an assumption.

- **SETTLED — the September 2026 FOMC meeting (15–16 Sept) is fully resolved
  and does not need re-verifying again:** the Committee raised the federal funds target
  range 25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, unanimous 12-0, the
  first hike since 2023.
- **SETTLED — FOMC minutes from the Sept 15-16 meeting, closed as of edition
  37, do not re-derive:** released Wednesday 7 October 2026, 2:00pm ET, read
  directly against federalreserve.gov. Vote was unanimous 12-0 with no dissent
  recorded ("all participants viewed a higher target range... as
  appropriate"). The one internal-division signal: "most participants" (not
  all) assessed that another increase would likely be appropriate by year-end,
  with the Committee stressing data-dependency meeting to meeting.
- **The October 27-28, 2026 FOMC meeting is now imminent — it was still 1-2
  days away as of edition 50's Monday 26 Oct cutoff, and did NOT land inside
  edition 50's window.** Directly reconfirmed scheduled via
  federalreserve.gov/monetarypolicy/fomccalendars.htm at edition 50 (not an
  SEP meeting; next meeting after this one is December 8-9, 2026, an SEP
  meeting). Decision expected approx. 2:00pm ET, press conference approx.
  2:30pm ET — these exact clock times remain a high-confidence inference from
  pattern/secondary calendars, not a direct federalreserve.gov quote.
  **Blackout (Oct 17-29, 2026) was reconfirmed holding clean at edition 50**
  — no Fed-speaker commentary or leaks found. **Correction to edition 49's own
  forward-looking guess: edition 49 predicted "very likely edition 50" would
  lead with the decision — that was wrong. Given this report's one-edition-
  per-session cadence, edition 50 covers Monday 26 Oct (meeting hasn't started
  yet), edition 51 will cover Tuesday 27 Oct (meeting day 1, no decision), and
  the decision itself (Wednesday 28 Oct) will fall inside whichever edition
  covers that session — very likely edition 52. That is the edition that must
  lead with the decision, the press conference, and the immediate market
  reaction (no fresh dot plot expected, non-SEP meeting).**
- **Rate-path odds at edition 50 (DeFi Rate's Kalshi/Polymarket-blended
  aggregator, fetched Mon 26 Oct's approx. 8:29pm ET cutoff window):** October
  27-28 hold approx. **93%** (hike approx. 7%) — essentially unchanged from
  edition 49's 94%. **December 8-9 odds**: the source's own headline/
  standalone figure showed hike approx. **74%** while a separate meeting-path
  table on the same page showed approx. **77%** — the same category of
  internal inconsistency logged at editions 47 (80/22), 48 (72/77) and 49
  (76/79), now a **fourth** straight edition, still not self-corrected;
  re-check again at edition 51 or 52. **Kalshi's own direct fetch failed again
  (HTTP 429) at edition 50, now fourteen consecutive failures (37-50).**
  Official CME FedWatch also failed again directly (timeout) at edition 50, a
  **tenth** consecutive failure (41-50). The composite "at least one more
  hike in 2026" read has still not been freshly re-pulled since edition 38
  (last known approx. 80%) — don't cite without a fresh pull.
- **US-China "30-for-30" tariff framework — remains a closed thread, do not
  re-open absent a genuine dated Federal Register filing.** Resolved at
  edition 37 (framework) and edition 47 (implementation-notice sub-question:
  no effective date, no set timeline, none imminent). Edition 48 found
  federalregister.gov's search interface blocked (302-redirect to
  `unblock.federalregister.gov`, an apparent bot/rate-limit gate) — not
  re-attempted at edition 49 (out of this edition's research-pass scope); log
  as a standing access obstacle for any future tariff-filing search attempt,
  not as new information about the thread itself. Separately noted at edition
  47: the Busan US-China trade truce has reportedly been extended to **10
  January 2027** (background context, not independently primary-sourced).
- **Fed Chair: Kevin Warsh — SETTLED, stop re-verifying it every run.** No
  contradiction surfaced at edition 50 (twentieth-plus straight unchanged
  confirmation chain; last direct federalreserve.gov bios-page confirmation
  at edition 47 — due for re-confirmation at the November monthly audit). **The exact term-end date — open since edition 48 — was
  resolved at edition 49 via a direct federalreserve.gov/aboutthefed/bios/
  board/warsh.htm fetch: his Chairman term ends 21 May 2030 (took office 22
  May 2026, a four-year term); his separate term as a Board of Governors
  member runs to 31 January 2040.** Record this as the named-expiry anchor
  going forward: the Chairmanship re-opens as a live fact only on a successor
  nominated/confirmed, a resignation or removal, or that 21 May 2030 term-end
  date actually arriving. If any pass reports a different Chair, that is a
  contradiction — verify it before drafting, do not assume the pass is wrong.
- General principle for everything still live: do not assume a routine
  macro-calendar fact (meeting dates, symposium schedules, other central
  banks' policy rates, government funding status) from memory or from the
  prompt's own framing — verify it fresh from a primary source
  (federalreserve.gov, bankofengland.co.uk, boj.or.jp, kansascityfed.org,
  norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, rba.gov.au,
  ecb.europa.eu, bankofcanada.ca, whitehouse.gov, etc.) every edition, exactly
  like any other data point. These are the rates and dates that feed Section
  3's policy-rate table, so the table is the natural place to land them.
  **The BoE's next decision (Thursday 5 November 2026) was re-confirmed
  directly at edition 50 via bankofengland.co.uk's own "upcoming MPC dates"
  page** — now eleven straight editions clean (39-50), under two weeks out;
  confirm once more at edition 51 if bandwidth allows given how close it now
  is. The shutdown/CR status URL
  (`whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500/`)
  was re-fetched cleanly again at edition 50 — unchanged, funding through 11
  December 2026, no shutdown; continue standardizing on this URL. The
  Bank of Canada's Wednesday 28 October 2026 decision (current overnight rate
  target **2.25%** going in) was reconfirmed again at edition 50 via
  bankofcanada.ca's own press page — no change/leak found; the exact 9:45am ET
  announcement time itself is secondary-sourced (BoC's own page does not
  print it). **The ECB's current policy rate remains settled** (deposit
  facility 2.50%, main refi 2.65%, marginal lending 2.90%, all effective 16
  September 2026, resolved at edition 49). **Its exact Governing Council
  meeting start date (28 Oct) remains secondary-sourced only — a third
  attempt at edition 50 confirmed the 29 Oct press-conference date directly
  via ecb.europa.eu's own calendar, but not the Council's own meeting-day
  text; try once more at edition 51/52 if the window still needs it.**
  **The BoJ's exact numeric policy rate is FINALLY resolved at edition 50,
  closing a five-straight-edition primary-source gap (45-49): a direct fetch
  of boj.or.jp's own English-language homepage confirms the uncollateralized
  overnight call rate target at approx. 1.25%, with the complementary deposit
  facility rate at 1.25% and the basic loan rate at 1.5%, both effective 24
  September 2026.** This closes the sourcing-gap open thread, but the rate
  itself remains a LIVE fact (not yet eligible for settled status, having
  only been directly confirmed once) because the BoJ's Oct 29-30, 2026
  meeting is imminent and could change it — **whichever edition covers that
  meeting (very likely edition 53 or 54) must watch directly for the decision
  and verify the rate fresh, not carry forward the 1.25% figure
  automatically.** **Riksbank's rate figure, previously stuck behind
  navigation-markup noise despite a working URL, was successfully extracted
  at edition 50: held at 1.75%, effective 30 September 2026** — closing that
  open thread; the URL is
  `riksbank.se/en-gb/monetary-policy/monetary-policy-report/2026/
  monetary-policy-decision-september-2026/`. **The Reserve Bank of
  Australia's current rate was re-confirmed directly via rba.gov.au at
  edition 50** — closing a two-edition (48-49) secondary-sourcing gap: 4.60%,
  with the 25bp hike taking effect **30 September 2026** (the decision itself
  was announced 29 Sept — a one-day decision-vs-effective-date distinction,
  not a contradiction of prior editions' "29 Sept" framing). **Norges Bank's
  and the SNB's next-decision dates were confirmed directly at edition 50**
  — Norges Bank's next decision is **17 December 2026** (norges-bank.no) and
  the SNB's is **10 December 2026** (snb.ch) — closing that open thread.
  **Banxico's next decision date remains unavailable** — not found at
  edition 50 either; try again at edition 51 if bandwidth allows.
- **SETTLED — Bank of England held at 3.75% on Thursday 17 Sept 2026, a 6-3
  vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — directly reconfirmed at
  edition 50 (following decision 17 December 2026).
- **SETTLED (the September decision only) — Bank of Japan hiked 25bp to
  approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano) — closed thread, do not re-derive. **The exact numeric rate
  itself is now also primary-sourced as of edition 50 (see the
  general-principle entry above), closing the five-edition sourcing gap, but
  stays a LIVE fact pending the Oct 29-30, 2026 meeting's outcome — do not
  promote to settled until that meeting has passed with the rate confirmed
  unchanged (or updated) directly.**
- **SETTLED — the four-central-bank Thursday 24 September 2026 cluster,
  closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% but signalled a greater chance of
  a Q4 hike; Banxico held at 6.50% unanimously; SNB held at 0% and raised its
  inflation forecasts, confirmed directly against snb.ch.
- **SETTLED — the Reserve Bank of Australia's Tuesday 29 September 2026
  decision, closed thread, do not re-open:** hiked 25bp to **4.60%,
  unanimous**, a 15-year high and its fourth hike of 2026, confirmed directly
  against rba.gov.au's own Statement by the Monetary Policy Board at edition
  47; re-confirmed directly again via rba.gov.au at edition 50 (effective
  date 30 Sept 2026 per the bank's own page), closing a two-edition
  secondary-sourcing gap (48-49).
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
  against bls.gov.
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
- **No US federal government shutdown is in effect — re-confirmed again at
  edition 49 via the standing whitehouse.gov URL (see the general-principle
  entry above).** H.R. 6500 funds federal agencies through **11 December
  2026**. Watch for shutdown risk resurfacing as that date approaches.
- **University of Michigan October 2026 consumer sentiment — CLOSED thread as
  of edition 49, both preliminary and final readings now in hand:**
  preliminary 46.3 (a five-month low); **final 48.0** (vs. September's final
  48.1 and the approx. 47.6 consensus) — an upward revision from the
  preliminary print despite still reading as a multi-month low in context.
  Final sub-indices: current conditions 46.7 (vs. prelim 44.7), expectations
  48.8 (vs. prelim 47.3); year-ahead inflation expectations 4.7% (unchanged
  from prelim), long-run 3.5% (up from prelim's same 3.5%, i.e. unchanged).
  **The final reading is secondary-sourced only** (three independent outlets
  agreed on the headline; umich.edu itself could not be fetched directly at
  edition 49) — if a primary umich.edu fetch becomes available at a future
  edition, use it to upgrade this thread's sourcing tier, though the figures
  themselves are not expected to change.
- **China September 2026 CPI/PPI — RESOLVED at edition 42, closed thread, do
  not re-derive:** CPI **+0.9% y/y** (+0.2% m/m), PPI **+5.0% y/y** (the
  fastest PPI rise since June 2022), driven by fuel costs. Sourced to gov.cn's
  English-language NBS-attributed news release (stats.gov.cn itself remained
  stale/unreachable) — continue treating the gov.cn English release as an
  acceptable near-primary substitute if stats.gov.cn remains unreachable.
  China's October PMI is due approx. 31 October 2026, now about a week out —
  watch for it at edition 50 or 51 depending on cutoff timing.
- **China Q3 2026 GDP — RESOLVED at edition 45, closed thread, do not
  re-derive:** printed **Monday 19 October 2026**, settling edition 44's
  disputed release-date (19 vs. 20 Oct) in favor of the 19th, confirmed
  directly against the National Bureau of Statistics' English-language press
  release at stats.gov.cn. Q3 alone: **+4.5% y/y, +1.2% q/q**; first-three-
  quarters 2026 cumulative: **+4.6% y/y** (GDP RMB 107,107.1bn).
- **New Mexico v. Meta — a $25bn civil-penalty ruling was reported, multi-
  sourced, at edition 47 (Judge Francis Mathew, Wednesday 21 Oct 2026); the
  stay/appeal sub-question is now substantially clarified at edition 50,
  though not fully confirmed.** Meta owes **$25bn** in civil penalties for the
  jury's late-September verdict (Meta violated the state's Unfair Practices
  Act roughly 43.9 million times, re: hate-speech policy and its Cambridge
  Analytica response) — above the 48-other-state, $18bn settlement Meta
  already reached elsewhere, but well below New Mexico's $35-40bn ask and the
  $219.5bn theoretical statutory maximum. Meta has said it will appeal.
  **Edition 50 found that this $25bn judgment is distinct from a SEPARATE,
  earlier New Mexico Unfair Practices Act matter** (an original judgment plus
  a $567m August add-on, totaling approx. $942m, for which Meta posted an
  $1.8bn bond and received an unopposed stay of enforcement around 9 October
  2026). Since the $25bn judgment (21 Oct 2026) postdates that 9 Oct stay, it
  is unlikely the stay covers it — but this is an inference from timing, not
  a direct confirmation, and should not be presented as settled. **Whether
  Meta has filed a formal notice of appeal of the $25bn judgment specifically
  remains unconfirmed, now a fourth straight edition (47-50)** — Meta's chief
  legal officer continues to express only future-tense confidence in
  prevailing "on appeal." This is a distinct proceeding from the March 2026
  child-safety jury verdict ($375m, before a different judge, Bryan
  Biedscheid) and the August 2026 abatement ruling ($567m, same Biedscheid
  case, under appeal) — don't conflate the three. Also distinct from Meta's
  own Q3 2026 earnings charge: a separate $9.89bn one-time charge tied to an
  **August 2026, 52-state-AG** teen-safety settlement that explicitly
  excludes New Mexico (which pursued its own litigation) — don't conflate the
  nationwide settlement with the New Mexico judgment. Sources used at edition
  50: santafenewmexican.com (the approx. $942m matter/stay), sourcenm.com
  (the $25bn judgment), thedeepdive.ca (Meta's appeal statement).
- **New calendar-awareness item from edition 40, reconfirmed relevant at
  edition 41: "equities-open, bonds-closed" US holidays need an explicit
  check every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. **Next candidate to verify when it lands: Veterans Day, Wed 11 Nov
  2026 — confirm whether that is also bonds-only before assuming.**
- **CLOSED at edition 49 — Bank of Canada's Wednesday 28 October 2026
  decision is now primary-confirmed** (first flagged secondary-only at
  edition 48): 9:45am ET, same day as the FOMC decision; current overnight
  rate target 2.25% going in. See the general-principle entry above.
- **The vendor-retroactive-revision trap recurred again at edition 49, in a
  broader form than edition 48's gold/silver-only narrowing.** Re-fetching
  Thursday 22 Oct's closes from the same vendor (Investing.com) at edition 49
  found: gold $4,038.35→$4,060.40 (+0.54pp, a second straight edition of
  upward revision), silver $54.61→$55.007 (+0.72pp, also a second straight
  revision), WTI $99.28→$99.47 (+0.19pp, minor), and — new this edition —
  USD/JPY $156.54→$156.77 (+23 pips / +0.14pp), the first time this specific
  trap has clearly hit USD/JPY rather than EUR/USD. **By contrast, Brent,
  Treasury yields (14th straight clean edition) and GBP/USD (5th straight
  clean edition) all reconciled exactly**, and EUR/USD and Henry Hub showed
  only immaterial (single-digit-pip / sub-1%) drift not large enough to call a
  genuine revision. Copper could not be checked against this specific trap
  via LME this edition since westmetall.com had been down at edition 48 —
  see the dedicated copper entry below for its recovery.
  **Recommendation reinforced yet again: fresh-refetch every commodity/FX/
  Treasury prior-session base from the same vendor table every single
  edition — not just the instruments that drifted last time.** The locus
  keeps rotating or narrowing (WTI at 45, gold/silver/nat-gas at 46,
  gold/silver/DXY/EUR-USD/USD-JPY at 47, gold/silver only at 48,
  gold/silver/WTI/USD-JPY at 49); the Treasury curve remains the one
  instrument class that has never shown this trap across every edition
  checked (now 15 straight clean editions through edition 50).
  **Edition 50 reversed the pattern (WTI, gold, silver, copper, EUR/USD,
  GBP/USD and USD/JPY all reconciled exactly against edition 49's logged
  Friday 23 Oct figures) but found by far the largest single instance of this
  trap yet, isolated to Brent: the previously-published Friday 23 Oct close
  of $116.72 (+3.14%) re-fetched at edition 50 as $111.70 (+2.80%) from the
  same vendor — an approx. 4.3% discrepancy, versus a typical sub-1pp drift
  in every prior instance of this trap. No independent settlement report for
  that date could be found to arbitrate which figure was correct; this is
  disclosed in the briefing rather than resolved. Treat as the single
  highest-priority item in this trap's history — attempt an independent
  cross-check (ICE, EIA, or a dated news settlement report, not just
  Investing.com) for Brent specifically at edition 51 or 52.**
- **New sourcing-mechanics trap logged at edition 50, relevant to any
  Monday-dated (or any day-after-a-non-trading-day) edition: Investing.com
  inserts an electronic Sunday-evening re-open print as its own row for every
  24-hour-traded instrument (oil, gas, metals, DXY, FX pairs).** This means
  the site's own displayed "Change %" on the Monday row is Monday-vs-Sunday-
  evening, not Monday-vs-Friday-close — silently understating or overstating
  the real weekly move if taken at face value. **Fix used at edition 50 and
  recommended going forward: always pull the raw Friday, Sunday and Monday
  closing prints and compute the Friday→Monday change manually, rather than
  trusting the vendor's own displayed change column on a post-weekend
  edition.** This does not apply to Treasury yields or to any instrument
  without 24-hour/Sunday-evening trading.
- **CLOSED at edition 49 — LME copper's primary source (westmetall.com) is
  back online; the edition-48 outage was transient, not permanent.** Both the
  homepage and the direct market-data table returned normal, dated content
  with no certificate error. LME cash-settlement copper closed Thu 22 Oct at
  $14,215.00/tonne, Fri 23 Oct at $14,415.00/tonne (+1.41%), directionally
  consistent with a COMEX cross-check (+1.71%). westmetall.com is reinstated
  as the standing primary source; COMEX remains available as a disclosed
  secondary cross-reference going forward rather than a forced substitute.
- **Henry Hub natural gas: the OHLC internal-consistency issue that recurred
  across several earlier editions was NOT present at edition 48, 49 or 50** —
  all six rows checked (Thu/Fri/Mon across the last two editions) had open
  and close within the stated low/high range. **CLOSED at edition 50 — the
  front-month has already rolled from NGX6 (November) to NGZ6 (December) in
  vendor quoting, confirmed via both the Investing.com contract header and a
  TradingView expiry-calendar cross-check (NGX6 expiry 28 Oct 2026, NGZ6
  expiry 25 Nov 2026)** — ahead of NGX6's actual expiry, a normal vendor
  convention rather than an error. Continue treating this instrument's
  price-data quality as requiring a fresh check every edition despite three
  consecutive clean reads — it has been unstable too many times to assume it
  is now permanently fixed.
- **The Kitco live-spot-vs-headline cross-check was repeated again at edition
  50 for gold only** — spot $4,011.00 sat approx. $7.65 (approx. 0.2%) below
  the futures close of $4,018.65, consistent with a normal futures/spot
  basis. Silver spot was not separately quoted on the page at edition 50 (only
  a derived gold/silver-ratio estimate, approx. $53.84, close to but not an
  independent print of the $53.928 futures close) — treat the silver side as
  an inconclusive/weak cross-check this edition rather than a clean one.
  Continue attempting both metals each edition when research-pass timing
  allows a same-day check.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company (owns AOL, Evernote,
  WeTransfer, Issuu and other consumer/SaaS apps), IPO'd 1 July 2026 at
  $29/share (above its $26-28 range), rising approx. 41% on debut to a
  approx. $25bn market value. Logged here so a future edition doesn't waste
  effort re-verifying the ticker's legitimacy if it moves sharply again.
- **The "named secondary outlet's own percentage-move headline can be flatly
  wrong" trap (first logged edition 44, J.B. Hunt/FreightWaves) recurred at
  edition 49 (twice in one session: Tesla and NU Holdings) and again at
  edition 50:** a secondary aggregator claimed JetBlue fell approx. -13%
  Monday 26 Oct when the verified stockanalysis.com close was actually
  **-9.71%** — always check a headline's claimed magnitude against the
  underlying price-history table before repeating it. AT&T's exact Wednesday
  21 Oct close (-6.45% per stockanalysis.com vs. a third-party archive's
  -6.1%) remains unresolved for a 4th straight edition, a standing low-
  priority item given the larger, separate, equally uncatalyzed -7.96% AT&T
  decline on Friday 23 Oct.
- **A reinforcing, non-novel reminder, reinforced again at edition 48-49:
  premarket/regular-session-close is not the after-hours earnings reaction,
  and the two can diverge sharply — and an after-hours reaction does not
  necessarily hold, extend, or reverse uniformly across a multi-name
  reporting cluster into the next regular session, nor does a strong beat
  guarantee a positive reaction even in the SAME session it is reported.**
  Edition 49 added a same-session (not just cross-session) version of this
  lesson: Friday 23 Oct, Bloom Energy beat-and-raised (after Thursday's
  close) yet fell -11.24% in Friday's regular session, and American Express
  beat-and-raised (before Friday's open) yet fell -3.68% the same day — both
  read as profit-taking/"sell the news" into a broadly negative tape rather
  than a guidance problem. **Lesson: a clean beat-and-raise is not
  sufficient to assume a positive reaction, especially inside a down-market
  session — always report the reaction as a separate, disclosed fact from
  the earnings quality itself, and don't infer a negative catalyst where
  none was found; "no specific sell-the-news driver identified beyond broad
  session weakness" is a legitimate, honest conclusion.** Always fetch and
  separately label the regular-session close vs. the after-hours reaction,
  and check the next session's close before assuming an after-hours move has
  "held."
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent, but has
  now agreed for a sixth straight session (45-50).** DXY rose and USD/JPY
  rose Monday 26 Oct, both positive — directionally agreeing for a sixth
  straight session. Keep disclosing the comparison every edition regardless
  of which way it goes, and keep watching whether this becomes the norm
  rather than staying truly intermittent.
- **The single-aggregator-dependence pattern continued at edition 50: neither
  AP's wire nor Reuters' updated wrap was indexed/fetchable for Monday 26 Oct
  by cutoff**, a third straight edition (48-50). The established fallback
  combination (stockanalysis.com's ETF-proxy data cross-checked against a
  direct-index-snapshot source) was used again — fool.com and FRED's daily
  DJIA series both reconciled cleanly, with Investrade's market review as a
  further secondary cross-check (particularly useful for the Dow and Russell
  2000). The Nasdaq-100 again had no direct-index-snapshot cross-check this
  edition — it remains ETF-proxy-derived only via QQQ. The Russell 2000
  similarly remains IWM-proxy-derived, with Investrade's own direct figure
  close but not identical.
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38** — when a secondary-sourced EPS figure conflicts sharply with
  a primary filing's GAAP number without a stated basis, prefer the primary
  filing and flag the secondary figure in Annex B. Edition 50 again reported
  both GAAP and adjusted figures cleanly for Verizon and Cadence Design
  Systems, both via their own 8-Ks — no conflict found, per the established
  precedent.
- **The "preview-consensus-only miss/beat framing" caution (first logged at
  edition 41) remains an open, unconfirmed disclosed inference, not
  re-chased at edition 50 either.** Pick this thread back up at a future
  edition if bandwidth allows.
- **Equifax's unexplained-magnitude rally thread, partially reversed at
  edition 49, saw a further -2.08% decline Monday 26 Oct** (reportedly tied to
  an RBC downgrade to Sector Perform, single-sourced and not independently
  confirmed) — the underlying catalyst gap for Thursday 22 Oct's +6.59% leg
  specifically remains open after a further edition-50 search pass found
  nothing new (only a differently-dated +10.7% move on 20 Oct and a +6.17%
  move on 14 Oct, neither matching). Declining urgency given the magnitude is
  shrinking rather than compounding; keep on the open-threads list.
- **New at edition 47, reinforced at editions 48-50: when standard "biggest
  movers" aggregator pages aren't retrievable, SEC EDGAR's full-text search
  for same-date 8-K filings is an effective, primary-source-grounded
  discovery/verification method** — used again at edition 50 to pull Surgery
  Partners', EQT's, Verizon's and Cadence's own filings directly, and to
  confirm Exxon/Chevron/AbbVie/Newell Brands had no new Item 2.02 filings.
- **The edition-49 "forward-looking calendar aggregator" trap (Chevron,
  Exxon Mobil, AbbVie, Newell Brands falsely listed as Friday 23 Oct
  reporters) remains open and was re-confirmed still accurate at edition 50:
  a direct SEC EDGAR check found no new Item 2.02 filings for any of the four
  names** — all four remain expected around 30 October 2026. Watch for actual
  reports at whichever edition's window reaches that date.
- **A megacap multi-name earnings cluster reporting on the same evening can
  produce genuinely uncorrelated reactions, both at the after-hours stage
  (edition 47) and again at the next-regular-session stage (edition 48); a
  same-session variant was logged at edition 49 (Bloom Energy, American
  Express) and recurred again at edition 50 (Verizon beat-and-raised yet fell
  -3.49% the same session, no sourced explanation beyond the revenue miss;
  Cadence beat-and-raised and rose +2.62% after hours the same evening —
  genuinely uncorrelated reactions to comparable headline quality).**

## Role framing
Write as a top-tier economist / equity, commodity and derivatives investor,
sector-agnostic. Plain English. Single-stock focus (see coverage below).

## Coverage and weighting
Single stocks are the centre of gravity. Weight roughly: **~45% single
stocks & earnings, ~20% macro, ~20% commodities/FX, ~15% derivatives.**

**These percentages describe the shape of the briefing, not a cap on its
length.** Market recap's sector coverage, added at edition 49, is **on top of
them** rather than carved out of equities: the sector material moved out of
section 2, but section 2's share did not move with it. Give the freed space
back to single stocks as more names and more read-across depth. If the result
runs long, that is what the page-4 spillover rule is for — do not cut
single-stock coverage to make room for the sector section.

0. **Market recap** — index closes in the snap-grid tiles, the recap
   paragraph, and **all sector and ETF coverage**: the sector-ETF chart and
   the narration of how each sector performed in the session. Sized by what
   the sector story actually warrants, not by a percentage.
1. **US equities & earnings (LEAD, largest section) — single stocks only** —
   single-stock movers, earnings since last cutoff, guidance changes,
   analyst actions. **No sector rotation or ETF commentary here; that is
   section 1's from edition 49.** **Bias name selection toward:**
   Technology, SaaS/software, consumer staples, consumer discretionary,
   telcos, and large industrials. This is the section the user reads first —
   give it the most column space and the most "why it moved / read-across"
   depth.
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
- **Length: 4 pages total, hard. Do not exceed.** The split inside those
  four changed at edition 49: sections 1-6 are no longer confined to the
  first three. If they run past page 3 they may spill onto page 4 and the
  annex follows immediately below the spillover, sharing that page rather
  than being pushed to a fifth. See the page-break bullet under Production
  notes for exactly when the forced break stays and when it goes. Trimming
  is still the answer once four pages genuinely will not hold it, just no
  longer the first answer. **Edition 49 ran clean at 4 pages with the forced
  break kept (sections 1-6 ended on page 3) — no spillover needed, despite
  running a third chart. Edition 50 is the first edition to actually use the
  spillover mechanism as designed: sections 1-6 ran onto page 4, the forced
  break was deleted, and the annex followed the spillover down page 4 —
  exactly the workflow this rule was built for, and it worked cleanly on the
  first attempt at applying it. A first draft still needed two rounds of
  content trimming afterward (see the edition-50 log entry) before the
  spillover converged to 4 pages rather than 5 — deleting the break alone is
  not guaranteed to be enough by itself.**
- **No "So what" lines.** Interpretation lives in the 60-second read at the
  top, and inline only where a number is meaningless without it — never as a
  standalone labelled line.
- **Sources:** numbered inline references `[n]` in a small blue superscript
  span, full list in Annex C. Never inline URLs in the body. **Each citation
  number gets its own `<sup class="ref">[n]</sup>` tag** — do not write
  `[26][27]` inside one sup tag; write `<sup class="ref">[26]</sup><sup
  class="ref">[27]</sup>`. `check_refs.py`'s regex only matches one bracket
  per sup tag, so combined-bracket citations silently fail the cross-check.
  Note that bracket text baked into a chart PNG's axis label (e.g. `[6]`) is
  NOT scanned by `check_refs.py` (it only reads the HTML, not image pixels) —
  keep those numbers consistent with Annex C by hand; the tool can't catch a
  mismatch there. **Also watch for a stray bracket typed outside a `<sup>`
  tag entirely** — `check_refs.py` will not flag it since its regex only
  matches inside `sup class="ref"` tags, so a bare `[n]` slips through
  silently. Proofread citation-heavy sentences visually, not just via the
  script, when a sentence carries two or more consecutive citations. A
  related trap, worth naming explicitly: placeholder ref text (e.g.
  `[note1]`) typed during drafting and never swapped for a real number.
  `check_refs.py`'s regex requires `\d+` inside the brackets, so a
  non-numeric placeholder simply won't match either the inline or Annex-B
  regex — it won't show up as "missing" or "unused," it just silently
  doesn't count. **Never use a letter suffix to disambiguate a citation —
  always mint a new integer.** Annex C numbers do not need to be contiguous,
  only matched 1:1 against inline citations — deleting an unused reserved
  number and leaving a gap is completely fine and simpler than renumbering
  everything after it. **Reusing the same Annex C number for multiple
  movers/figures citing the same outlet/method is fine and recommended** —
  `check_refs.py` only checks presence/absence, not uniqueness of use
  (editions 33-49 have all done this for stockanalysis.com single-stock
  closes and other repeatedly-used outlets, confirmed stable across sixteen
  editions). **Citing the prior edition itself as a source** (e.g. "[7]
  Daily Economic Briefing, edition 47, logged prior-session baseline
  figures") is a legitimate, already-used pattern when disclosing a
  divergence against a previously-logged figure — editions 43 through 48
  have all done this cleanly with `check_refs.py`; edition 49 instead
  disclosed its Thursday-base revisions inline within the sourced Annex C
  entry for Investing.com rather than citing the prior edition directly —
  both patterns are acceptable, use whichever reads more cleanly for the
  specific disclosure.
- **Structure:** correction box (only when there is one) → 60-second read
  (5 ranked items) → 1 Market recap, **including sector performance** → 2
  Equities and earnings (LEAD, **single stocks only**) → 3 Macro, policy and
  rates (condensed; policy-rate table + prose, see below) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A
  (assumptions, status, and the full record of any correction) → Annex B
  (what could not be verified) → Annex C (sources) → Method note. **Do not duplicate the
  day-ahead calendar as both a prose paragraph (e.g. at the end of Section 3)
  and the Section 6 table — edition 47's first draft did exactly this and it
  was the single largest contributor to a 5-page overflow; Section 6's table
  is the one and only place the day-ahead calendar belongs.**
- **The disclosure box is now a correction box — new at edition 49, by
  request.** It used to carry assumptions, corrections and status notes
  together at the top of page 1. Assumptions and status move to **Annex A**,
  where a reader can go and look if they want them. What stays on page 1 is
  **corrections only**: a figure published in an earlier edition that turned
  out to be wrong, or a premise-level correction (a date, a person, an event
  that did or didn't happen). Terse — what was published, what it should
  have been — with the full record in Annex A if it needs more than a line.
  **Omit the box entirely on an edition that corrects nothing**, which will
  be most of them. The reasoning for the split: a reader who acted on
  yesterday's wrong number will not go hunting through an annex to find out,
  whereas nobody is harmed by missing a status note. **Edition 49 omitted the
  box — nothing published in a prior edition was found to be wrong.** (A
  draft concern about edition 48 mislabeling a GBP/USD date turned out, on
  checking the actual edition-48 PDF text directly, to be a misreading in
  this edition's own research brief rather than a real error in the
  published document — worth remembering: verify an apparent prior-edition
  error against the actual published PDF/HTML before writing a correction
  box entry, not against a secondhand paraphrase of it.)
- **All sector and ETF material belongs to Section 1 — new at edition 49, by
  request.** Section 1 keeps its snap-grid tiles and recap paragraph and
  gains the sector-ETF chart plus the narration of how each sector did in
  the session. **Section 2 is purely single-stock**: movers chart, movers
  table, earnings, guidance, analyst actions. The test is simple — if a
  sentence is about a sector rather than about a named company, it goes in
  Section 1. Section 6's "sector setup we take into [session]" bullets stay
  where they are; they are forward-looking, not a recap of what happened.
- **Section 3 carries a central-bank policy-rate table.** Other central
  banks' rates in a paragraph are the least readable thing in the document;
  put the levels in a table and keep the prose for what a table cannot hold.
  Columns: **Central bank | Policy rate | Last change | Next decision**. The
  Fed goes first as the anchor to compare against, then whichever of the
  BoE, BoJ, ECB, SNB, Norges Bank, Riksbank, RBA, BoC and Banxico the window
  actually touches — eight to ten rows is the working range. A bank whose
  current rate could not be verified still gets its row, with that cell
  marked unavailable and a matching Annex B entry; dropping the row hides the
  gap instead of disclosing it. **Edition 49 ran a full 10-row table
  (Fed, BoE, BoJ, ECB, Norges Bank, Riksbank, SNB, RBA, BoC, Banxico) — the
  ECB rejoined after edition 48's exclusion now that its rate is resolved;
  several next-decision cells were marked "not re-confirmed this edition"
  rather than guessed at, which is the intended disclosure pattern when a
  bank's rate is settled/carried-forward but its next-decision date wasn't
  freshly fetched that edition.** If page 3 overflows anyway, cut rows that
  had no news in the window before cutting any prose. Follow the usual table
  convention — plain `<tr>` header rows, no `<thead>`.
- **Charts: two fixed, a third only when earned — changed at edition 49.**
  Placement is no longer editorial for the first two. The **sector-ETF
  performance chart always goes in Section 1**, beside the sector narration
  it illustrates, and the **single-stock movers bar always goes in Section
  2**, with the names. Neither may duplicate a table.
  A **third chart is allowed only when positioning or volatility is
  genuinely the day's dominant story** — not merely present, and never to
  fill a short page — and it goes in the section it belongs to: CFTC
  asset-manager vs. leveraged-funds positioning or a VIX term structure in
  Section 5, an implied-vs-realized earnings bar in Section 2. **Edition 49
  used the CFTC third chart in Section 5** — the first fresh CFTC print since
  13 Oct showed a genuine, non-trivial shift (leveraged funds covering a
  chunk of their ES net short while staying net-short RTY) that tied
  directly to the week's positioning narrative; this is the same placement
  editions 24, 34, 39 and 44 used under the old rules. **Three charts is real
  pressure on four pages: the third chart is the first thing to drop when
  the budget is tight**, after sector table rows with no news and before any
  prose — edition 49 did not need to drop it; the document rendered clean at
  4 pages with all three charts in on the first attempt. Next CFTC report
  expected Fri 30 Oct, covering Tue 27 Oct data — check cftc.gov directly at
  edition 50 if its window extends past 3:30pm ET that day.
- **Tilt:** market-wide. No portfolio tilt, no holdings commentary.
- **Window:** everything since the previous edition's cutoff. On Mondays
  (or after any gap) this includes the weekend/missed sessions.
- **Data gaps:** keep Annex B. State plainly what could not be verified.
  Never estimate, infer, or fill from memory.
- **Page margins:** 1 inch (25.4mm) top and bottom, 13mm left and right.
- **Text alignment:** body prose (paragraphs, bullet lists) justified.
  Tables, headers (h1/h2/h3), the snap-grid tiles, the meta line, and Annex
  B's narrow 3-column source list stay left-aligned — justifying short table
  cells or a dense multi-column list produces ugly ragged spacing.

## Hard rules
- Every data point needs a named source. If unverifiable, say so in Annex B
  rather than producing a plausible-sounding number.
- Where sources disagree, use the more authoritative one **and** disclose
  the disagreement. AP's "How major US stock indexes fared" and the Reuters
  market wrap are normally the most reliable for index closes — but check
  they're actually indexed for the target date before relying on them; this
  has occasionally failed to post in time, or blocked direct automated fetch
  even when it did post. **Editions 48, 49 and now 50 all found neither wire
  indexed/fetchable at all** — fall back to secondary outlet(s) + ETF-proxy
  triangulation plus a direct-index-snapshot source (fool.com and FRED's
  DJIA series at edition 50; StatMuse and FRED's NASDAQ100 series at edition
  49) when AP/Reuters genuinely haven't posted or can't be fetched directly,
  and disclose the fallback explicitly every time. **This is now a
  three-edition streak of wire unavailability (48-50) — increasingly looking
  like it may be becoming the norm rather than staying intermittent;
  re-attempt AP/Reuters directly at edition 51 regardless, but don't be
  surprised if it fails a fourth time.**
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Edition 44 found a new, stronger version of this trap: a
  FreightWaves headline's percentage-move claim for J.B. Hunt was not just
  mistimed but flatly contradicted by the stock's own verified close.**
  Always check a dated article's own claimed magnitude against the
  underlying price-history table, not just its date, before repeating it.
  **Edition 49 found the same trap recur twice in one session** (Tesla and
  NU Holdings both had flatly wrong aggregator-claimed percentages — see the
  dedicated Standing Facts entry above) **and a new forward-looking variant:
  an earnings-calendar aggregator listing companies as reporting before they
  actually had** (Chevron/Exxon/AbbVie/Newell Brands, also detailed above) —
  verify a calendar aggregator's claimed report-date against the company's
  own IR calendar before treating a name as having reported.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  **Edition 49 continued this discipline**, individually verifying
  single-stock closes directly against stockanalysis.com, cross-checking SEC
  EDGAR 8-Ks for the session's primary earnings movers (SLB, American
  Express, Bloom Energy) and running a negative-result EDGAR search to
  confirm Equifax had no new filing.
- **Premarket is not the close, and the close is not the after-hours
  earnings reaction — and an after-hours reaction does not necessarily hold
  into the next regular session, uniformly or at all. A strong beat-and-raise
  does not guarantee a positive reaction even within the SAME session.**
  Reinforced explicitly at editions 44, 47, 48 and again at 49 (see the
  dedicated Standing Facts entry above) — edition 49's Bloom Energy
  (beat-and-raise, -11.24% same-session) and American Express
  (beat-and-raise, -3.68% same-session) are the clearest same-session
  examples logged to date. Always fetch the verified close, the after-hours
  reaction, AND (when the window allows) the next regular session's close as
  three separate, clearly labelled figures, and do not assume a reaction
  direction from earnings quality alone.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent but has
  now agreed for five straight editions (45-49)** — see Standing Facts entry
  above. Continue disclosing the DXY-vs-USD/JPY directional comparison
  explicitly every edition regardless of which way it goes, and watch
  whether the agreement streak is becoming the new norm.
- **The Kitco live-spot-vs-headline cross-check was resumed cleanly again at
  edition 49, no conflict found for a second straight edition** — see the
  dedicated Standing Facts entry above. Continue attempting it each edition
  when research-pass timing allows a same-day check.
- **GBP/USD reconciled cleanly for a fifth straight edition (45-49); the
  vendor-revision trap widened again at edition 49 to gold/silver/WTI/
  USD-JPY** (after edition 48's narrower gold/silver-only instance) — see
  the dedicated Standing Facts entry above. Resume the fuller multi-source
  method on any FX/commodity pair if a fresh same-day conflict reappears.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for fourteen further editions (37-50)** — edition 50 again found the full
  Treasury curve reconciled perfectly against the prior edition's logged
  base via home.treasury.gov, though the usual Trading Economics cross-check
  was incomplete this edition (the page surfaced only a current snapshot,
  not extractable dated history — not a contradiction, just a gap). Treat as
  resolved/noise unless a fresh conflict appears.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 50 have all run clean (or
  clean after one quick fix) — **edition 50 needed two small fixes (three
  Annex-C sources initially unused, each missing an inline citation that was
  added rather than deleting the source) before reaching 35/35 clean.**
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 50 have all rendered with zero stray tildes on the
  first draft.**
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39, 44 and now **49**
  have all resolved this cleanly for CFTC CoT, with full OI and Asset-
  Manager/Leveraged-Funds breakdowns for ES, NQ and RTY, normalized as % of
  open interest. **Edition 49 confirmed directly (cftc.gov's
  `financial_lf.htm`) the first fresh report since 13 October, covering
  Tuesday 20 October data**: ES OI 1,935,470 (AM +46.6%/LF -19.2%), NQ OI
  272,462 (AM +28.6%/LF +0.4%), RTY (full-size) OI 466,789 (AM +6.6%/LF
  -11.4%). **The next CFTC report is due Friday 30 October 2026, 3:30pm ET,
  covering Tuesday 27 October data** — check cftc.gov directly at edition 50
  if its window extends past that release time, and decide on that basis
  (plus whatever the FOMC-week positioning story turns out to be) whether it
  earns the optional **third** chart in Section 5 again. The sector-ETF panel
  remains fixed in Section 1 and does not compete with it for a slot.
- **The diffuse-overflow lesson from editions 44-45 and the duplicated-
  content lesson from edition 47 are both still worth checking first on any
  overflow** — editions 48 and 49 both rendered clean at 4 pages on the first
  attempt with no trims needed (edition 49 despite running all three
  possible charts), but if a future edition overflows, check for duplicated
  content across sections before diffuse trimming; it has twice been the
  larger, single-fix win.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — **specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation.** Edition 49
  again confirmed this is routinely NOT triggered: the largest mover (Bloom
  Energy -11.24%) was only approx. 1.41x the second-largest (AT&T -7.96%) —
  no capping needed, consistent with most editions' spreads. Edition 49's
  movers chart did need a wider-than-default `pad_frac` (0.26, up from the
  single-series default of 0.12) to stop the largest bar's value label from
  visually crowding the y-axis tick-label margin — **when a chart's largest
  bar extends close to the plot's edge, increase `pad_frac` rather than
  shortening the label text**, a cheap fix worth trying before the
  asterisk/footnote technique (which remains the right fix specifically for
  capped-outlier labels, a different problem).

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 50 all got a fresh,
  same-day-timestamped sweep** — twenty-three consecutive fresh sweeps now,
  including a full six-series sweep (VIX, VIX9D, VIX3M, VIX6M, VVIX, SKEW)
  every time since edition 47. **The feed's two known bugs (a duplicated
  `prev_day_close`, and a `price_change_percent` that divides by current
  price instead of prior close) are genuinely intermittent, not a one-way
  ratchet** — edition 48 saw neither bug, edition 49 saw both on every
  series, and **edition 50 again saw neither bug present**, reconfirming the
  intermittency runs both ways. **Always compute day-over-day % change
  manually regardless of how many consecutive bug-free reads preceded the
  current one.** Edition 50 saw the VIX complex unwind sharply as Friday's
  event-driven pop reversed (VIX -5.45% to 18.39, VVIX -7.54% to 101.43),
  term structure staying in contango throughout but compressed (VIX9D 17.92 <
  VIX 18.39 < VIX3M 19.94 < VIX6M 21.63) — a mean-reversion unwind of
  Friday's hedges tracking the equity rally, not a new shock.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 50 fetched all 11 directly again**
  (Technology +1.69% the clear leader on a chip/AI rally, Communication
  Services -1.57% the clear laggard on Verizon's post-earnings decline; 8 of
  11 green) — continue this direct-fetch-by-default method.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (8 of 11 at edition 50) —
  continue treating an uncorroborated single-aggregator breadth figure as
  not usable.
- **Dealer gamma:** zerogex.io hit an **eleventh consecutive edition of
  failure at edition 50** (loaded this time, but every metric showed
  placeholder dashes with no timestamped data — the same functional failure
  mode as prior editions). SpotGamma logged a **fifth straight failure at
  edition 50**, confirmed again as a client-side React single-page app with
  zero server-rendered data behind its dashboard.spotgamma.com login. Both
  sources remain fully unusable.
- **Official CME FedWatch probabilities:** the page blocks fetching
  (edition 50's direct attempt timed out again, a **tenth** consecutive
  failure, 41-50) — use secondary citations (Polymarket, Kalshi, Reuters/
  other economist polls, desk notes) and give a range rather than a single
  invented number. DeFi Rate's Kalshi/Polymarket-blended aggregator remains a
  stable, consistently working source for both the near-dated (Oct) and
  December meetings — though its December sub-table has now shown an
  internal inconsistency for four straight editions (47: 80/22; 48: 72/77;
  49: 76/79; 50: 74/77), worth re-checking again at edition 51 or 52.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, now **fourteen consecutive failures (37-50)** — a confirmed
  structural gap, not transient. Resume the attempt-every-edition discipline
  at edition 51 regardless, but expect a block of some kind. Use Kalshi's
  own secondary reporting or DeFi Rate's blended aggregator as the
  workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). westmetall.com remains the standing LME
  copper primary source, reconciling cleanly again at edition 50 ($14,500.00
  Mon 26 Oct, +0.59% vs. an unrevised Friday base). COMEX's own secondary
  cross-check could not be sourced at edition 50 (only stale/undated
  snapshots found) — try again at edition 51. LME's own site (lme.com) has
  not been re-attempted as primary since edition 35.
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **remained clean at edition 50** (2-yr
  4.68%, 10-yr 5.00%, 30-yr 5.31%, all 26 Oct, matching the previously-logged
  Friday base exactly), extending the clean streak to **fifteen editions
  (37-50)** with no repeat of the edition-36 33bp gap. **Trading Economics'
  cross-check degraded at edition 50 — the page surfaced only a current
  snapshot, not extractable dated history for 23/26 Oct** — the usual
  TE-vs-Treasury.gov comparison is incomplete rather than contradicted this
  edition; try again at edition 51. Continue scoping the TextView URL to the
  specific month (`field_tdr_date_value_month=202610`-style parameter)
  rather than the full year.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). Edition 49's fresh report (covering Tuesday 20 Oct 2026) was
  the last one posted; **edition 50 confirmed directly against cftc.gov's own
  release schedule that nothing new has posted since, as expected** (releases
  fall on the 2nd, 9th, 16th, 23rd and 30th of the month). **The next report
  is due Friday 30 October 2026, 3:30pm ET, covering Tuesday 27 October
  data** — check cftc.gov directly at whichever edition's window extends past
  that release time (likely edition 54), and judge the third-chart decision
  on both freshness and that edition's dominant story (very likely the FOMC
  aftermath by then).
- **GBP/USD clean close:** remains fully resolved since edition 37, now
  reconciling cleanly for a **sixth straight edition (45-50)**. Edition 50
  reversed the broader vendor-revision pattern (WTI, gold, silver, copper,
  EUR/USD, GBP/USD and USD/JPY all reconciled exactly against edition 49's
  logged Friday base) but found by far the largest single revision yet,
  isolated to Brent — see the dedicated Standing Facts entry above. EUR/USD
  closed Monday 26 Oct at 1.1174 (-0.26% vs. Friday); GBP/USD closed at
  1.3345 (-0.21%); USD/JPY closed at 157.54 (+0.43%) — all single-sourced to
  Investing.com's close-to-close history table, recomputed manually against
  the raw Friday base rather than the vendor's own Sunday-anchored change
  column (see the new sourcing-mechanics trap logged above).
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot-vs-headline cross-check was repeated at edition 50 for gold only
  (silver inconclusive this time)** — see the dedicated Standing Facts entry
  above. Gold and silver futures continue to source via Investing.com;
  **edition 50 found both instruments' Friday 23 Oct closes unrevised from
  this report's previously-logged figures** ($4,007.90 gold, $53.949 silver)
  — a reversal of the two-straight-edition upward-revision pattern seen at
  editions 48-49. Monday 26 Oct: gold +0.27% to $4,018.65, silver -0.04% to
  $53.928.
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is also a closed thread as of
  edition 45 — see the dedicated Standing Facts entry above. **US
  import/export prices and industrial production:** both closed threads for
  September — see Standing Facts above. **University of Michigan October
  consumer sentiment** (both preliminary and final) is a **closed thread as
  of edition 49** — see the dedicated Standing Facts entry above. China's
  October PMI is due approx. 31 October 2026 (a Saturday) — not independently
  confirmed via stats.gov.cn at edition 50 (only a secondary calendar
  aggregator date); watch for it at edition 54 or 55 depending on cutoff
  timing, and try stats.gov.cn directly rather than relying on the
  aggregator's date.
- **Henry Hub natural gas:** the front-month-contract-identity question
  remains resolved via the TradingView-expiry-calendar technique (edition
  47). **CLOSED at edition 50 — the front-month roll from NGX6 (Nov) to
  NGZ6 (Dec) has already occurred in vendor quoting** (see the dedicated
  Standing Facts entry above), and the instrument's own OHLC price-data
  quality was clean for a third straight edition (48-50) — continue
  double-checking fresh every edition regardless, since it has reverted to
  instability before.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 50 again found no notable
  single-stock options-flow/skew commentary** tied to Monday's movers or to
  FOMC positioning despite a targeted search — a **fourteenth** consecutive
  largely-empty edition on this general sub-item (37-50). Treat this
  sub-item as reliably low-yield and keep it a brief, secondary effort each
  edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. Not
  applicable through edition 50; next due approx. 14 November 2026, now
  under three weeks out — start watching for it in editions covering early
  November.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22). Not attempted
  again through edition 50.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully at
  editions 39, 44, 45, 46, 47, 48, 49 (the first since 13 Oct to show
  genuinely fresh, moved figures) and **confirmed-no-new-report-yet at
  edition 50** (next release not due until 30 Oct, verified directly against
  cftc.gov's own release schedule). Repeat the three-instrument fetch at
  whichever edition's window extends past Friday 30 Oct, 3:30pm ET (likely
  edition 54), watching for the Micro-vs-full-size Russell naming trap each
  time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 50 did find
  a general analyst-action roundup (via Investrade, a secondary source) with
  nine named firm/ticker pairings but no dollar price targets attached to any
  of them — the pattern across 37-50 continues to look genuinely intermittent
  in yield and increasingly variable in sourcing depth; watch each edition
  independently rather than assuming a trend.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** Edition 49 caught two flatly-wrong aggregator percentage
  claims (Tesla, NU Holdings); **edition 50 caught a third instance** (JetBlue
  claimed approx. -13% by a secondary aggregator vs. a verified -9.71% close)
  — see the dedicated Standing Facts entry above. AT&T's exact Wednesday 21
  Oct close (-6.45% vs. a third-party archive's -6.1%) remains the one
  standing, unresolved single-sourced conflict from that specific session,
  now carried four editions, still lower priority given the larger, separate,
  also-uncatalyzed AT&T declines since. Continue this direct-verification
  discipline on high-confidence-seeming figures, not just surprising ones.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted at editions 48, 49 or 50 (out of scope each time); try an
  alternate DOL page or a secondary economic-calendar aggregator for the
  consensus figure at edition 51.
- **federalregister.gov's direct search interface is blocked, logged at
  edition 48, not re-attempted directly at edition 49 or 50** (a edition-50
  web search for a new tariff-related Federal Register filing found nothing
  dated to the window, but did not re-test the search interface itself): a
  prior search attempt 302-redirected to `unblock.federalregister.gov`, an
  apparent bot/rate-limit gate. Note this for any future tariff- or
  trade-filing search attempt rather than re-discovering the same block.
- **CLOSED at edition 50 — Riksbank's primary policy-rate page.** The
  edition-49 URL (`riksbank.se/en-gb/monetary-policy/monetary-policy-report/
  2026/monetary-policy-decision-september-2026/`) was fetched again and the
  rate figure successfully extracted this time: held at 1.75%, effective 30
  September 2026. No further action needed on this specific gap.
- **ECB's current policy rate:** CLOSED at edition 49 via a direct
  ecb.europa.eu fetch — deposit facility 2.50%, main refi 2.65%, marginal
  lending 2.90%, all effective 16 Sept 2026. The ECB rejoined the policy-rate
  table from edition 49 onward. **Its exact Governing Council meeting start
  date (approx. 28 Oct 2026) remains secondary-sourced only** — a second
  direct ecb.europa.eu attempt at edition 50 confirmed the 29 Oct
  press-conference date directly, but not the Council's own meeting-day
  text; try once more at edition 51 if the window still needs it (the
  meeting itself will likely have passed by then).

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel
  (confirmed clean at editions 37 through 43, 45 through 49, and now **50**,
  thirteen editions total) — this remains correct for 10-11 categories
  specifically. For charts with fewer categories, scale the height down:
  roughly `(9.8, 1.65-1.95)` for 3-9 categories (editions 47 and 48 used
  `(9.8, 1.95)` for a 9-category chart; edition 49 used `(9.8, 1.85)` for a
  7-category movers chart; **edition 50 used `(9.8, 1.95)` for an 8-category
  movers chart**). **Always render and visually inspect (via the Read tool)
  the actual PNG at or near full resolution before embedding it**, regardless
  of what a past edition's success might suggest. **Default to pad_frac=0.30
  from the start for an 11-category sector-ETF panel** — now a confirmed,
  repeated pattern across six straight small-magnitude 11-category panels
  (45-50). **The edition-49 finding (a movers chart whose largest bar exceeds
  10% needs a wider-than-default pad_frac to avoid value-label crowding) was
  reconfirmed at edition 50**: an 8-category movers chart with a 47.62%
  outlier used pad_frac=0.26 and rendered clean with no crowding, no capping
  needed (ratio to the second-largest bar was approx. 2.7x, well under the
  5x capping threshold) — continue trying pad_frac in the 0.22-0.30 range
  from the start for any movers chart with a double-digit-percent outlier.
- **Capped-outlier label-overlap fix (from edition 45):** when a capped
  bar's value label uses a "(capped)" text suffix, the label text can be
  long enough to visually bleed into the y-axis tick-label margin even at a
  wide pad_frac, because matplotlib's `ax.text()` is unclipped by default.
  **Fix: shorten the per-bar suffix to a single trailing asterisk (`"*"`
  instead of `" (capped)"`) and add one footnote to the chart's x-axis label
  instead.** This remains the recommended default for any future
  capped-outlier chart. **Editions 47, 48, 49 and now 50 all fell well under
  the approx. 5x capping threshold despite some editions' largest mover
  having an unusually big raw magnitude, so no capping was needed any of the
  four times** — reinforcing that the trigger is the ratio to the
  next-largest bar, not the largest bar's absolute size. Edition 50's largest
  mover (Surgery Partners +47.62%, on a confirmed take-private deal) was only
  approx. 2.7x the second-largest (Range Resources +17.66%, also a confirmed
  merger) — well under threshold despite the largest bar's raw magnitude
  being the biggest seen in several editions. (Edition 49's
  largest-magnitude crowding issue was a different problem — uncapped bars
  simply needing more pad_frac — solved with that fix, not the asterisk
  technique, which is specifically for capped-outlier labels.)
- **A grouped (two-series) horizontal bar chart — needed for the CFTC
  Asset-Manager-vs-Leveraged-Funds positioning chart — requires custom chart
  code, not the standard single-series `barh()` helper used for the
  movers/sector charts** (first built at edition 44, reused successfully at
  edition 49 after a five-edition gap). The standard helper only plots one
  value per category; the CFTC chart needs two bars (Asset Manager,
  Leveraged Funds) per category (ES/NQ/RTY), offset vertically by a fixed
  height fraction (`h=0.32` worked cleanly for 3 categories) around each
  category's tick position. **Fix that worked for the legend:** use a
  FIGURE-level legend (`fig.legend(handles, labels, loc="lower center",
  bbox_to_anchor=(0.5, 0.0), ...)`) combined with
  `fig.tight_layout(rect=(0, 0.1, 1, 1))` to reserve the bottom 10% of the
  figure for the legend, clear of the x-axis label — an axis-level legend
  placed too far below the axes will overlap the x-axis label text.
  Figsize `(9.8, 2.15)` (taller than the movers chart's 1.8-1.95 range)
  rendered cleanly at both edition 44 and edition 49. **Reuse this exact
  pattern** for any future grouped/multi-series chart rather than re-deriving
  the legend-placement fix from scratch.
- PDF: HTML → Chromium print-to-PDF via Playwright. Launch Chromium with an
  explicit `executablePath` (check the environment for the installed
  Chromium build path) and `--no-sandbox`. Do not run `playwright install`.
- Set margins in **exactly one place** — either the CSS `@page` block or the
  Playwright `page.pdf()` margin option, never both (they stack and double
  the margin). Passing `{top:'1in', bottom:'1in', left:'13mm', right:'13mm'}`
  via `page.pdf()` with the HTML body at `margin:0; padding:0` and no CSS
  `@page` block is the pattern that has worked reliably.
- **At most ONE forced `page-break-before` in the whole document:
  immediately before Annex A — and on a spillover edition, none at all.**
  Let sections 1-6 flow naturally; never add a break between them. The rule
  from edition 49:
    - Sections 1-6 end on page 3 (the common case) → keep the break. The
      annex opens a clean page 4, exactly as before. **This was edition 49's
      case.**
    - Sections 1-6 spill onto page 4 → **delete the `pagebreak` div and
      re-render**, so the annex follows the spillover down page 4 instead of
      starting a fifth page.
    - Still five pages with the break gone → now trim, in this order: sector
      table rows with no news in the window, the third chart if there is
      one, then prose.
  Note on the `grep -c 'pagebreak'` self-check: the CSS baseline defines a
  `.pagebreak` class rule AND the body uses one `<div class="pagebreak">` —
  a literal `grep -c 'pagebreak'` therefore normally returns **2** on a
  correctly-built edition (one CSS rule line, one div usage line), not 1.
  The actual check that matters is `grep -c 'class="pagebreak"'` (counts
  only div usages), which should be 1, or 0 on a spillover edition, never 2
  — use that more specific pattern to avoid a false alarm from the CSS rule
  definition itself. A stray extra *div* still produces a 5-page PDF with a
  mostly-blank orphan page, and that looks identical to a spillover edition
  that kept its break, so check the div count before anything else when the
  page count is wrong. Always check for content duplication across sections
  first when a draft overflows — it has twice been the cheapest,
  highest-leverage fix.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix.
- **A markup-correctness trap, logged at edition 47: a `<sup class="ref">`
  citation tag placed immediately after a table row's last `</td>` but still
  inside the `<tr>` (i.e. not nested inside any `<td>`) is invalid table
  structure.** `check_refs.py` will NOT catch this. **Always nest every
  `<sup class="ref">` tag inside a `<td>...</td>` pair, never as a sibling of
  one inside a `<tr>`** — grep for `</td><sup` as a quick self-check if a
  table was built with a lot of copy-paste. Edition 49's draft was checked
  this way and came back clean (0 matches).
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  **Edition 49 rendered clean at 4 pages on the first attempt, no trims
  needed, despite running all three optional/fixed charts.**

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across editions 40 through
49's very different content volumes. Treat as the durable default; the
lever to pull on a high-volume or overflowing day is first checking for
duplicated content across sections, then merging/trimming redundant content
across whichever sections are longest — not loosening the CSS further.)
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
- Annex A: two columns at 7.1pt, same treatment as Annex B below.
- Annex B: two columns at 7.1pt, `break-inside:avoid` per `li` (left-aligned
  — reads cleanly at this width; justify only if it still looks clean after
  testing).
- Annex C: three columns at 5.5pt, left-aligned.
- Content budget: 60-second read (5 items); equities as the largest block
  plus the movers table; macro/commodities/derivatives tighter; **a "This
  week's known catalysts" table plus a "Sector setup we take into [session]"
  bullet list at the end of Section 6 by default** for any single-session or
  weekend-window edition (skip only if a multi-session catch-up already
  fills 3 pages). **An optional "Commodities & FX levels" table (~9-13
  rows)** at the end of Section 4 is available as padding if page 3 runs
  short after the two default blocks — reach for it only when content alone
  doesn't fill the page; editions 44 through 49 all folded commodities, FX
  and Treasuries into ONE combined table (10-14 rows, edition 49 used 13) as
  the PRIMARY commodities table rather than padding, now the standing
  default rather than an edition-specific choice. **On a high-single-stock-
  volume earnings day, watch the movers table specifically for verbosity**
  (multi-clause driver text, rows that could share a combined cell) before
  assuming the page budget is safe. **Edition 49, despite a genuinely dense
  Friday earnings morning and three charts, converged to a clean 4-page
  render on the first attempt with no trims needed. Edition 50, by contrast,
  genuinely overflowed on the first attempt (5 pages, sections 1-6 spilling
  onto page 4 with room to spare) despite using only two charts** — a single
  merger-and-earnings-dense Monday session (two confirmed M&A deals, Verizon
  and Cadence earnings, a resolved multi-edition BoJ sourcing gap, a major
  Brent vendor-revision disclosure, and a New Mexico v. Meta clarification)
  produced enough prose and annex content to overflow even without a third
  chart. **Fix applied: dropped the forced page break (per the spillover
  rule) and trimmed several Annex A/B bullets and two Section-2 prose
  paragraphs** — converged to a clean 4 pages on the second attempt. Always
  re-render immediately after adding (or removing) any content to confirm
  the page count. **When overflow appears, check for duplicated content
  across sections FIRST before diffuse trimming; if no duplication is found,
  trim a little from several sections rather than gutting one** — edition 50
  found no duplication, so went straight to distributed trimming (annex
  bullets and prose), which worked in two short rounds.

**Chart selection guidance — rewritten at edition 49.** Placement is no
longer editorial for the first two charts, so the old "pick chart #2 by the
day's story" decision no longer exists:

- **Sector-ETF performance chart → Section 1 (Market recap), every
  edition.** Same-day closes by default; a grouped day-over-day bar instead
  on a multi-session or weekend window, or on a genuine multi-sector
  broadening selloff across consecutive sessions. This was already the
  standing default across twenty-five eligible editions (25-50); what has
  changed is that it is now mandatory and sits beside the sector narration
  in Section 1 rather than in Section 2.
- **Single-stock movers bar → Section 2 (Equities), every edition.**
- **A third chart only when positioning or volatility is genuinely the
  day's dominant story**, never to fill a page, placed in the section it
  belongs to:
  - Fresh CFTC CoT data → the ES/NQ/RTY asset-manager-vs-leveraged-funds
    positioning chart, normalized as % of open interest, built with the
    grouped-bar technique documented under Production notes, in **Section
    5**. Editions 24, 34, 39, 44 and 49 have all placed it there.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully.
  - A holiday-window preview edition with no fresher data → VIX futures
    term structure with event annotations, in **Section 5**.

**Three charts is real pressure on a four-page document; two is not
automatically safe either.** Edition 49 ran all three without needing to
drop anything; **edition 50 ran only two (no fresh CFTC data, and the
VIX/vol move was judged a mean-reversion unwind rather than a genuinely
dominant story) and still needed a page-4 spillover fix and two rounds of
trimming** — a reminder that the chart count is one input to the page
budget, not the only one; a content-dense single session can overflow on
two charts just as easily as a lighter session survives three.

**Edition 54 should check cftc.gov's freshness** (the Friday 30 Oct report,
covering Tuesday 27 Oct) — that release falls inside edition 54's window
(Monday 2 November, covering Friday 30 October). Edition 51 confirmed no
fresh report was available to it, as expected. **Edition 52 (covering
the Wednesday 28 Oct FOMC-decision session) should default to NOT adding a
third chart purely because of the Fed decision** — a rate decision alone is
not automatically "positioning or volatility is the dominant story"; judge
it the same way edition 50 judged Monday's VIX unwind (mean-reversion vs. a
genuine dislocation) rather than assuming a third chart is owed to a big
macro day.

**Remember the figsize-scales-to-category-count guidance above
(ceiling `(9.8, 1.95)` for an 11-category panel, `(9.8, 2.15)` for the
3-category grouped CFTC chart, scale down for fewer single-series
categories), that an 11-category sector-ETF panel should default to
pad_frac=0.30 from the start (six straight confirming editions, 45-50), a
movers chart with a double-digit-percent outlier should try pad_frac in the
0.22-0.30 range from the start (confirmed again at edition 50), and the
capped-outlier asterisk/footnote fix when a spread crosses the approx. 5x
RATIO threshold** (it did not at editions 47, 48, 49 or 50).

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Condense on a schedule, not on a whim. Once this spec exceeds 100,000
bytes, condense the log as part of that run** — the run is told the current
size in its prompt, and verification reports it afterwards either way.
Condensing means folding the OLDEST full-detail and medium entries further
back into the mega-block; it never means dropping a rule, a standing fact or
an open thread, which live outside the log and are not space to reclaim.

There is no longer any maximum size, and the history behind that is worth
keeping. A 120,000-byte ceiling used to reject an oversized spec outright.
On 28 October 2026 the spec reached 127,499 bytes, was rejected, and the
edition it had just published was lost from its own log — and because every
later run would have restarted from the same oversized base, it would have
failed again every morning. The ceiling was removed and this threshold put
in its place: advisory, acted on by the run itself, and incapable of
throwing away correct work. Condensing is now housekeeping you do, not a
check you pass.

**Editions 1–49 (condensed):** established the format (edition 1 baseline;
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
equities extended records on falling yields; two severe sourcing traps hit
(fabricated AMD price targets, an unverifiable WHO claim, both rejected);
the Paramount Skydance/Warner Bros. Discovery merger closed (ticker SKYD); a
secondary source reversed the US-China tariff list-size assignment (resolved
edition 37); the 2-year Treasury hit a 33bp cross-endpoint gap (resolved
edition 37); GBP/USD hit a three-way conflict (resolved edition 37). Edition
37 (Thu 8 Oct): the FOMC minutes showed a unanimous 12-0 September hike but
only "most" backing a further 2026 move; equities retreated on a bond-market
selloff; three standing conflicts all resolved this edition; WTI and Brent
both hit a sharp level-vs-%-change reconciliation failure; a chart-layout
bug was found and fixed. Edition 38 (Fri 9 Oct): equities fell a second
straight session but breadth stayed strong; a second straight AI-optics
profit-taking session; Applied Digital's blowout print drew a muted reaction
and logged the first non-GAAP-vs-GAAP EPS conflict trap; a primary-source
breakthrough closed BoJ's last standing gap; oil's vendor-%-reconciliation
failure became well-established; zerogex logged three within-session
anomalies as a new data-quality trap. Edition 39 (Mon 12 Oct, covering Fri 9
Oct + weekend): SpaceX's approx. $8bn spectrum purchase rattled telecom but
equities shrugged it off, closing a record-setting week; a parallel biotech
rally ran alongside it; Delta's 8-K cleanly disclosed both GAAP and adjusted
EPS; Goldman upgraded Palantir; a chart-sizing refinement and deliberate CSS
retightening were needed to fix a genuine 5-page overflow. Edition 40 (Tue
13 Oct, covering Mon 12 Oct, Columbus Day): a value/growth split on renewed
memory-chip/AI-hardware weakness; AP's wire needed search-snippet recovery;
oil delivered its cleanest-ever dual-grade reconciliation (later found to
rest on a retroactively revised Monday base); zerogex's SPX gamma hit a
harder auth-gated/blank failure mode; a chart-label pad_frac bug was found
and fixed; a short-page-3 recurrence was fixed with a new Treasury-yield-
curve table. Edition 41 (Wed 14 Oct, covering Tue 13 Oct, the opening day of
Q3 bank/healthcare earnings season): JPMorgan, Goldman, Wells Fargo,
Citigroup, UnitedHealth and Johnson & Johnson all reported; JNJ's GAAP EPS
collapsed to $0.09 on a one-time talc-settlement charge while adjusted EPS
and raised guidance were both disclosed cleanly; equities finished
essentially flat via a clean AP wire recovered through two syndication
mirrors; Bumble's unexplained +56.58% surfaced (resolved edition 42: a
$1.3bn Ithaca Holdings buyout); the AI-optics/AI-hardware selloff cluster
finally found its delayed driver (Broadcom CEO Hock Tan's remarks); a new
vendor-retroactive-revision trap hit WTI, Brent and Henry Hub for the first
time. Edition 42 (Thu 15 Oct, covering Wed 14 Oct): September CPI printed
hot, triggering the broadest risk-off session in weeks (S&P -1.11%, Nasdaq
-1.88%); CoreWeave and Oracle led decliners on renewed AI-infrastructure-
funding-stress; Bumble's buyout mystery resolved; rate-path odds repriced
sharply hawkish; the Treasury curve flattened; the vendor-retroactive-
revision trap broadened to FX for the first time; the VIX complex spiked
hard. Edition 43 (Fri 16 Oct, covering Thu 15 Oct): a second straight
blowout inflation print (September PPI) barely moved Fed odds; an overnight
memory-chip rout reversed sharply on Nvidia CEO Jensen Huang's defense of
CoreWeave's balance sheet; TSMC's record Q3 still fell on cautious guidance;
Ericsson's beat drove the session's largest single-stock move (+11.80%); six
of eleven commodities/FX instruments showed a silently-shifted Wednesday
base. Edition 44 (Mon 19 Oct, covering Fri 16 Oct + weekend): equities fell
broadly Friday on renewed AI-infra. spending doubts (Nasdaq -2.14%, its
worst week since June); the VIX complex spiked hard with both CBOE feed bugs
appearing simultaneously for the first time; five large movers had no
confirmed catalyst; a FreightWaves "+12%" J.B. Hunt headline was flatly
wrong (actual close -2.78%); CFTC CoT posted fresh data, powering the first
grouped-bar positioning chart; the first HTML draft overflowed to 5 pages,
fixed over roughly five trim rounds. Edition 45 (Tue 20 Oct, covering Mon 19
Oct + weekend): equities rebounded broadly though breadth stayed narrow;
neither AP nor Reuters had posted a wire by cutoff, a new CNBC-live-blog/
Investrade/SPY-proxy fallback tier was used; biotech produced the day's
extremes (Silence Therapeutics +125.58% on a Merck KGaA buyout, EyePoint
Pharmaceuticals -85.28% on a failed trial), the chart's first
outlier-capping use, surfacing a label-overlap bug (fixed via an
asterisk+footnote pattern); two claims were excluded after failing
corroboration; GE Vernova's decline closed with a caveat; China's Q3 GDP
release-date dispute resolved; the vendor-revision trap's locus rotated to
WTI while EUR/USD and GBP/USD reconciled cleanly; Henry Hub also broke its
own five-edition base-ambiguity streak; the VIX complex unwound sharply off
Friday's spike. 33 sources, clean 33/33 on `check_refs.py` after one quick
fix, clean 4-page render. **Edition 46** (Wed 21 Oct, covering Tue 20 Oct):
equities rallied broadly in a sharp rotation reversal (S&P +0.29%, Dow
+1.02%, Nasdaq roughly flat, Russell +1.65%), 10 of 11 sectors green;
neither AP nor Reuters had posted a wire by cutoff for a second straight
edition; a new trap was logged when a secondary outlet's sector narrative
was flatly contradicted by a direct 11-ETF fetch. A packed earnings Tuesday:
Salesforce's $47.50/share Braze buyout (BRZE +51.70%), Equifax (+11.33%, a
new unexplained-magnitude thread) and Hasbro (+11.20%) led gainers; GM fell
6.84% despite a beat and a $20bn buyback; Netflix fell in the regular
session then further after hours on soft Q4 guidance. Standing Fed facts
all re-verified unchanged; rate-path odds little changed; Kalshi and CME
FedWatch both failed again; New Mexico v. Meta logged a new 9 Oct
stay-of-enforcement detail (later superseded by the actual ruling at edition
47). The vendor-revision trap hit its broadest case yet (gold, silver and
Henry Hub); WTI, Brent, copper, GBP/USD and the Treasury curve reconciled
cleanly. The VIX complex extended its unwind; dealer gamma fully unusable;
CFTC CoT confirmed no new data as expected. The first HTML draft rendered
clean at 4 pages with no trims needed. 42 sources, clean 42/42 on the first
`check_refs.py` pass, zero stray tildes. **Edition 47** (Thu 22 Oct, covering
Wed 21 Oct): equities extended Tuesday's rally a second straight session
(S&P +0.58%, Dow +0.68%, Nasdaq +1.05%), led by Technology even as
Communication Services lagged ahead of Meta's evening report; AP's wire
posted but needed a syndication-mirror workaround. A genuinely enormous Q3
earnings day: Netflix, AT&T (-6.45%, a disputed close), United Airlines,
Capital One, CME Group, Abbott, Danaher, Thermo Fisher and Elevance Health
around Tuesday close/Wednesday open; Meta, Tesla, IBM and Texas Instruments
after Wednesday's close with four distinct after-hours reactions. The
movers chart was dominated by SEC-EDGAR-sourced non-megacap names (Arcus
Biosciences, Integra LifeSciences, Lithia Motors, M/I Homes). New Mexico's
Judge Mathew ruled Meta owes $25bn; USTR's Greer statement closed the
tariff-implementation sub-question. Standing Fed facts reconfirmed;
rate-path odds Oct 28 hold approx. 88%, Dec hike approx. 77% (an internal
80/22 inconsistency, first logged); Kalshi and CME FedWatch both failed
again. The vendor-revision trap rotated to gold/silver/DXY/EUR-USD/USD-JPY;
GBP/USD, copper and the Treasury curve reconciled cleanly. VIX extended its
unwind a third session. The first draft overflowed to 5 pages from one
duplicated day-ahead paragraph, fixed; 34/34 sources clean.

**Edition 48** — Friday 23 Oct report covering Thursday 22 Oct: a tech-led
rotation, not a broad selloff (S&P -1.21%, Nasdaq approx. -2.58%, Dow
+0.02%), Technology -3.29% on Meta's -6.98% post-earnings reversal against
a Staples/Utilities bid; the AP/Reuters wire gap began here and the
ETF-proxy fallback was used; Riksbank's URL 404'd and the ECB showed a
2.00%-vs-2.40% conflict, so the ECB was excluded from the rate table;
westmetall.com went down on an expired certificate (COMEX substituted);
clean 4-page first draft, 24/24 refs.

**Edition 49** — Monday 26 Oct report covering Friday 23 Oct: a modest,
narrow risk-off session (S&P -0.52%, Dow -1.24%, only 3 of 11 sectors
green), a second straight edition with no indexed AP/Reuters wire, with
StatMuse and FRED's NASDAQ100 series newly added as direct-snapshot
fallbacks.

**Edition 50 (condensed)** — Tuesday 27 October 2026 report covering Monday
26 October 2026. A broad risk-on reversal of Friday's narrower selloff: S&P
500 +0.70% to approx. 7,676.77, Dow +0.28%, Nasdaq Composite +0.82% to
26,169.38, 8 of 11 sectors higher, Technology +1.69% on the chip/AI complex,
Communication Services -1.57% the laggard on Verizon. Third straight edition
with no indexed AP/Reuters wire. Two confirmed M&A deals led single stocks:
Surgery Partners +47.62% (HealthSpan's $5.7bn take-private) and Range
Resources +17.66% (EQT all-stock), both 8-K-confirmed. Verizon beat and
raised yet fell -3.49% on a revenue miss — another "a beat does not
guarantee a positive reaction" case. **Three standing sourcing gaps closed
at once: the Bank of Japan's numeric policy rate (approx. 1.25%, direct from
boj.or.jp, after five straight editions unresolved), the Riksbank's rate
figure (1.75%) and the RBA's current rate (4.60%).** BoE 5 Nov and BoC 28
Oct/2.25% both re-confirmed directly; the ECB's exact Governing Council
start date stayed secondary-sourced and Banxico's next date unavailable.
**The largest instance yet of the vendor-retroactive-revision trap hit Brent
crude** — Friday's published $116.72 re-fetched as $111.70, approx. 4.3%
apart, with no independent settlement report to arbitrate. A related
sourcing-mechanics trap was logged: Investing.com inserts an electronic
Sunday-evening print for 24-hour instruments, so its displayed Monday "%
change" is measured against Sunday evening rather than Friday's close —
every figure that edition was recomputed by hand. **The first HTML draft
genuinely overflowed to five pages — the spillover mechanism's first real
use — and was fixed by deleting the forced page break** plus two rounds of
distributed trimming. 35 sources, 35/35 clean after adding two missing
inline citations.

**Edition 51 (most recent — full detail)** — Wednesday 28 October 2026
report covering Tuesday 27 October 2026, research window Mon 26 Oct 20:00 ET
through Tue 27 Oct 20:21 ET (the window's one NYSE session). **This entry
was reconstructed by hand from the published PDF on 28 October 2026.** The
run's own spec update was rejected by the then-current 120,000-byte ceiling
(it came in at 127,499) and discarded, so the original write-up — including
whatever that run concluded about its own open threads — is lost. Everything
below is read off the edition as published; the forward-looking items in
"open threads for edition 52" were re-derived rather than reproduced. The
ceiling has since been removed.

**A third straight up session on narrow breadth:** S&P 500 +0.60% to
7,722.60, Dow +0.03% to 52,377.57, Nasdaq Composite +1.17% to 26,477.81 (a
fresh high), Russell 2000 +1.17% to 2,818.87, VIX -4.73% to 17.52. Only 5 of
11 SPDR sectors closed higher and AP's own wire said "most S&P 500 stocks
fell" — the index gain was Technology (+1.70%, a second straight session on
the same Micron/AMD/Broadcom/Nvidia complex) and a handful of AI/chip
mega-caps carrying a weak tape. Energy was the clear laggard (-2.05%),
tracking the day's oil pullback rather than any sector-specific catalyst;
none was found despite a dedicated search. **AP's "How major US stock
indexes fared" was fetchable again via a syndicated mirror, the first time
in four editions** — the editions 48-50 fallback tier was not needed. The
Nasdaq-100 again had no directly-sourced index print; QQQ's +1.27% was used
and disclosed as a proxy.

**A dense pre-FOMC earnings morning, and the beat/reaction logic broke
again:** Boeing -10.69% on a core-EPS miss (-$0.34 vs. -$0.21) with a
$697mn Commercial Airplanes operating loss and an approx. $0.7bn DOJ
settlement payment; JetBlue +18.99% *despite* missing (-$0.60 vs. -$0.55) on
a +18-22% Q4 unit-revenue guide; UPS +5.75% and Royal Caribbean +5.46% on
clean beats; Hilton -2.06% after beating on EPS and RevPAR but cutting FY26
EBITDA guidance; Sherwin-Williams -2.73% on a miss. PayPal (+2.00%),
American Tower (-2.36%), Corning (-1.13%) and S&P Global (-0.38%) all beat
and moved in directions their earnings quality did not predict. After hours:
NXP Semiconductors beat and fell -6.90%, Robinhood beat and fell -7.63%,
Visa missed narrowly and fell -1.15% while raising its dividend 16%, Caesars
missed badly (-$0.61 vs. -$0.11) with no verifiable reaction. **No sell-side
upgrade, downgrade or price-target change could be reliably dated to
Tuesday's session** despite a dedicated multi-query search — reported as a
gap rather than filled with an undated claim.

**The FOMC's meeting day one passed quietly.** The blackout held clean
through cutoff (confirmed against the Fed's own blackout-period calendar PDF)
and the odds moved to a near-lock **96% hold** for Wednesday's approx.
2:00pm ET decision. **December's odds remain internally inconsistent on the
same aggregator — 75% headline against 78% on its own meeting-path table —
now a fifth straight edition of the same discrepancy.** Kalshi's direct
fetch failed for a **15th** straight edition and CME FedWatch for an
**11th**; Polymarket's own site showed only an expired 2025 market. DeFi
Rate's blended aggregator remains the only working source.

**The Brent sourcing problem got worse rather than better.** An independent
cross-check against ICE, EIA and wire sources turned up a *third* candidate
for Friday 23 October's close — $113.17, alongside the existing $116.72 and
$111.70 — and no authoritative primary source could arbitrate. Friday's
Brent level should now be read as a disclosed $111.70–$116.72 range, not a
figure. Separately, **the same vendor's Monday 26 October gold and silver
levels were found revised out from under edition 50's own published
numbers** — treat those as superseded. WTI -1.57% and Brent -1.20% on the
session, with no dated catalyst found for the pullback.

**Vol priced unusually little into the decision:** VIX9D fell 7.1% to 16.65,
*below* the headline VIX, with VVIX and SKEW also lower — a term structure
closer to complacency than hedging on the eve of a Fed decision. The
derivatives pass read Tuesday as "a quiet positioning day", so **no third
chart was used**: neither a fresh CFTC report nor a genuinely dominant
options/volatility story was present. Dealer gamma failed again from both
sources (zerogex 12th straight, SpotGamma 6th).

**A carried open thread closed, and not the way it was framed:** Confluent
(CFLT), flagged at edition 50 as a possible Tuesday reporter, has been
delisted from Nasdaq since 17 March 2026 following its acquisition by IBM —
it no longer exists as a public company. Removed from future watch lists.

**Format:** the second edition under the edition-49 structure. Sector
performance and its chart sat in Section 1 and Section 2 stayed purely
single-stock; Annexes A, B and C all rendered; no correction box, there
being no prior-edition figure found wrong on a premise level. Clean 4-page
render, 30 sources, 30/30 on `check_refs.py`, zero stray tildes.

**Open threads for edition 52:** Edition 52 covers **Wednesday 28 October
2026 — the FOMC decision day — and must lead with it.** The decision lands
approx. 2:00pm ET with the press conference at 2:30pm ET; it is a non-SEP
meeting, so expect no fresh dot plot. Going in, the market priced an approx.
96% hold. **The Bank of Canada also decided 28 Oct** (9:45am ET, 2.25%
going in) and **the ECB decides 28-29 Oct** (2.50% deposit facility going
in) — both fall in the same window, and the ECB's exact Governing Council
start date is still only secondary-sourced, so try ecb.europa.eu directly
once more. **The Bank of Japan's Oct 29-30 meeting** lands in edition 53's
or 54's window depending on announcement timing against the 20:21 ET cutoff
— watch for the decision and the rate directly at boj.or.jp, whose English
homepage is the established working route. **Q3 GDP and September PCE both
release Thursday 29 October, 8:30am ET** (BEA-confirmed), so they belong to
edition 53; this edition's day-ahead consensus figures were single-sourced
to a secondary calendar, which is worth upgrading to a bank or wire survey
if one can be found.

**Brent crude's Friday 23 October close remains the single highest-priority
open item, and is now a three-way split** ($116.72 / $111.70 / $113.17)
after a dedicated ICE/EIA/wire cross-check failed to arbitrate it. Keep
publishing it as a disclosed range until an authoritative primary settlement
source surfaces; do not quietly pick one. Edition 50's published Monday
gold and silver levels are superseded by the vendor's own revision — the
retroactive-revision trap is now recurring often enough that re-fetching the
prior edition's commodity levels should be treated as routine, not
exceptional.

Still open and unchanged: Banxico's next policy decision date (another
direct attempt at banxico.org.mx failed); the Riksbank's and the RBA's
next-decision dates, carried forward from edition 50's direct confirmation
rather than re-fetched; Equifax's unexplained multi-session pullback, now
uncatalyzed across several editions and of declining urgency; AT&T's exact
Wednesday 21 Oct close (-6.45% vs. -6.1%), low priority; New Mexico v.
Meta's formal notice of appeal, unconfirmed for a fifth straight edition;
the "preview-consensus-only miss/beat framing" caution, not re-chased since
edition 41. Options implied-vs-realized and single-stock flow/skew remain
low-yield — brief, secondary effort only.

**Dates to hold on to.** Chevron, Exxon Mobil, AbbVie and Newell Brands are
expected approx. 30 October 2026 — edition 54's window (Monday 2 November,
covering Friday 30 October). China's October PMI is due approx. 31 October
(a Saturday); try stats.gov.cn directly rather than a secondary calendar,
whose 31 Oct date is all that could be found. **The next CFTC CoT report is
due Friday 30 October, 3:30pm ET, covering Tuesday 27 October data** — that
release falls inside **edition 54's** window, so check cftc.gov directly
there and judge the optional third chart on both freshness and that
edition's dominant story. 13F filings are due approx. 14 November 2026.
Veterans Day (Wednesday 11 November) needs the same "equities-open,
bonds-closed" check Columbus Day received, once it is inside a window.

**The monthly settled-facts audit is due at edition 54 (Monday 2 November),
the first edition dated in November.** This corrects edition 50's open
threads, which put it at edition 55 by reading the rule as "the edition
covering the first November session" — SKILL.md says the first edition of
each calendar month, and the two readings differ by one edition. Edition 54
it is.

**Threads closed since edition 50:** Confluent's expected Q3 report
(resolved at edition 51 — the company has been delisted since March 2026
and will not report; removed from watch lists). The AP/Reuters wire outage
eased at edition 51 via a syndicated mirror, but it has failed often enough
across editions 48-50 that the ETF-proxy fallback tier should stay
documented rather than retired.
