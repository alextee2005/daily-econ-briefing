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
  is where the sessions covered belong, not the date line. This has now been
  applied correctly for thirty-two straight editions (33 through 54) — treat as
  settled; edition 54 read "Monday 2 November 2026" as the date line, covering
  the Friday 30 October session in the window line.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 54 all reused the
  same pattern — now confirmed clean across twenty-six consecutive editions;
  edition 54 phrased it "Window: Thu 29 Oct 2026 20:00 ET – Sun 1 Nov 2026
  20:21 ET (Fri 30 Oct close/AH, the window's one NYSE session; Sat–Sun no
  equity trading)." No further confirmation needed; treat this as settled.

## Schedule
Run every weekday. Pick the trigger's local time so the effective research
cutoff lands roughly 4 hours after the US market close (20:15 ET) — during
US daylight time that's 00:00 UTC; adjust for standard time. **US daylight
time ended Sunday 1 November 2026, as scheduled — now a resolved, settled
transition, not a forward-looking watch item.** Edition 54's own window closed
at 2026-11-01 20:21 ET, which converts to 2026-11-02 01:21 UTC — consistent
with EST (UTC-5) already being in effect, confirming the conversion worked
correctly across the boundary. **From edition 54 onward, use EST (UTC-5) for
all ET/UTC conversions** until DST resumes — conventionally the second Sunday
in March (expected March 2027; this specific future date is a general
calendar convention, not yet independently verified, so don't cite it as a
confirmed fact until closer to the event). On Mondays (or after any gap),
cover the full window back to the previous edition's cutoff, including the
weekend.

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
reported still surfaces within weeks rather than never. **The November 2026
monthly audit was completed at edition 54** (the first edition of November) —
all ten central-bank rows in Section 3 were reconfirmed directly against
their own primary sources, with no contradictions, except Riksbank's rate
value (page 404'd, only its next-decision date is primary-sourced) and
Banxico (site unreachable, secondary-sourced only) — both already flagged as
such below. **The next monthly audit falls on the first edition of December
2026** — whichever edition covers the first NYSE session on or after 1
December 2026; no specific edition number is estimated this far out given
holidays and potential gaps.

A date does not promote itself. A future meeting date is live until it
passes; only afterwards is it settled history. When you do promote something,
write the date and source of its last direct confirmation and the event that
would invalidate it — a tier with no audit trail is just an assumption.

- **SETTLED — the September 2026 FOMC meeting (15–16 Sept) is fully resolved
  and does not need re-verifying again:** the Committee raised the federal funds
  target range 25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, unanimous 12-0, the
  first hike since 2023.
- **SETTLED — FOMC minutes from the Sept 15-16 meeting, closed as of edition
  37, do not re-derive:** released Wednesday 7 October 2026, 2:00pm ET, read
  directly against federalreserve.gov. Vote was unanimous 12-0 with no dissent
  recorded ("all participants viewed a higher target range... as
  appropriate"). The one internal-division signal: "most participants" (not
  all) assessed that another increase would likely be appropriate by year-end,
  with the Committee stressing data-dependency meeting to meeting.
- **SETTLED — the October 27-28, 2026 FOMC meeting is fully resolved, closed
  thread, do not re-verify again:** the Committee **held** the federal funds
  target range at 3.75%-4.00% on Wednesday 28 October 2026 (not an SEP
  meeting, no fresh dot plot), confirmed directly against
  federalreserve.gov's own press release text at edition 52, **re-confirmed
  again directly at edition 54's monthly audit, no change.** Vote 10-2 — a
  hawkish dissent, the first dissent of either kind logged in this report's
  history: Governor Lisa Cook and Cleveland Fed President Beth Hammack both
  preferred raising the target range 25bp. Statement language: activity
  "expanding at a strong pace," inflation "remains elevated," further moves
  data-dependent. A companion implementation note set IORB at 3.90% (eff. 29
  Oct), ON RRP at 3.75%, primary credit rate 4.0%, standing repo rate 4.0%.
  Kevin Warsh's actual press-conference remarks remained unverified through
  edition 53 and were not re-attempted at edition 54 — stale news now, not
  worth a dedicated search. Blackout (Oct 17-29, 2026) held clean through the
  decision, as expected. **Next meeting: 8-9 December 2026, an SEP meeting.**
- **Rate-path odds at edition 54 (DeFi Rate's Kalshi/Polymarket-blended
  aggregator, snapshot timestamped Sun 1 Nov 2026 approx. 7:49pm ET):**
  December 8-9 odds were little changed from edition 53 — hike approx. 70%
  (hold approx. 28%, cut near zero), down marginally from edition 53's approx.
  71% hike. Cross-validated against a **direct Polymarket Gamma-API pull**
  (not a plain site visit) showing an almost identical 69.5% hike / 27.5%
  hold — the first time in several editions a direct, non-aggregator
  Polymarket fetch has actually succeeded, via
  `gamma-api.polymarket.com/public-search` rather than the site itself, which
  has shown only an expired December 2025 contract for two straight prior
  editions (52-53). **Worth repeating this API-based approach at edition 55**
  rather than reverting to a plain site visit. The source's own internal
  inconsistency persisted an **EIGHTH straight edition (47-54)**: DeFi Rate's
  own Kalshi decision-table hike contract priced 70.5% against a separate
  Kalshi rate-level contract at 72.5% — same recurring pattern, not
  self-correcting; keep disclosing both rather than picking one. **Kalshi's
  own direct fetch failed again at edition 54, now EIGHTEEN consecutive
  failures (37-54).** CME FedWatch also failed again directly (timeout), a
  **FOURTEENTH** consecutive failure (41-54). The composite "at least one more
  hike in 2026" read has still not been freshly re-pulled since edition 38
  (last known approx. 80%) — don't cite without a fresh pull.
- **US-China "30-for-30" tariff framework — remains a closed thread, do not
  re-open absent a genuine dated Federal Register filing.** Resolved at
  edition 37 (framework) and edition 47 (implementation-notice sub-question:
  no effective date, no set timeline, none imminent). No new development was
  found at edition 54 either (a light-touch check only); the
  federalregister.gov search-interface block (302-redirect to
  `unblock.federalregister.gov`, logged at edition 48) was not re-tested
  again — log as a standing access obstacle. Separately: secondary reporting
  (a Thomson Reuters regulatory-insight piece) describes a Busan truce
  extension to **10 January 2027**, but this remains **NOT confirmed via any
  published Federal Register notice** as of edition 54 — treat the January
  2027 date as reported-not-verified, not settled law, if cited.
- **Fed Chair: Kevin Warsh — SETTLED, stop re-verifying it every run.** No
  contradiction surfaced through edition 54; **directly re-confirmed again via
  federalreserve.gov's own bios page at edition 54's November monthly
  audit**, closing that housekeeping item cleanly. His Chairman term ends 21
  May 2030 (took office 22 May 2026, a four-year term); his separate term as a
  Board of Governors member runs to 31 January 2040. The Chairmanship
  re-opens as a live fact only on a successor nominated/confirmed, a
  resignation or removal, or that 21 May 2030 term-end date actually
  arriving, or the **next monthly audit (first edition of December 2026)**.
- General principle for everything still live: do not assume a routine
  macro-calendar fact (meeting dates, symposium schedules, other central
  banks' policy rates, government funding status) from memory or from the
  prompt's own framing — verify it fresh from a primary source
  (federalreserve.gov, bankofengland.co.uk, boj.or.jp, kansascityfed.org,
  norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, rba.gov.au,
  ecb.europa.eu, bankofcanada.ca, whitehouse.gov, etc.) every edition, exactly
  like any other data point. These are the rates and dates that feed Section
  3's policy-rate table, so the table is the natural place to land them.
  **The BoE's current rate (3.75%) and its 5 November 2026 next-decision date
  were both reconfirmed directly against bankofengland.co.uk at edition 54.**
  The 17 Sept decision's 6-3 vote detail remains sourced only via consistent
  secondary corroboration (BoE's own page doesn't restate historical vote
  splits) — a sourcing-tier note, not a concern. **Thursday 5 November's
  decision itself falls just outside edition 54's own window** (which closed
  Sunday 1 Nov 20:21 ET) — it will land in whichever edition covers the
  Thursday 5 November session, roughly estimated as edition 58 if a daily
  cadence holds from edition 54 (55=Mon 2 Nov, 56=Tue 3 Nov, 57=Wed 4 Nov,
  58=Thu 5 Nov) — watch for the actual outcome there rather than assuming a
  hold. **The shutdown/CR status URL
  (`whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500/`)
  reconfirmed CLEANLY at edition 54**, resolving edition 53's failed
  reconfirmation attempt: H.R. 6500, the Continuing Appropriations and
  Extensions Act 2027, funds federal agencies through **11 December 2026**,
  no shutdown in effect. Treat edition 53's failure as resolved/transient;
  resume the standard re-check-every-edition discipline with no special
  urgency. **SETTLED — the Bank of Canada's Wednesday 28 October 2026
  decision is fully resolved, closed thread:** a genuine surprise 25bp hike
  to 2.50% (Bank Rate 2.75%, deposit rate 2.45%), confirmed directly against
  bankofcanada.ca at edition 52, **re-confirmed again directly at edition
  54's monthly audit, no change. Next decision: 9 December 2026** (same date
  as the Fed's). **The ECB's current policy rate is CONFIRMED UNCHANGED for a
  SECOND consecutive direct post-meeting confirmation (editions 53 and 54),
  but still not yet promotable to SETTLED — one more consecutive clean
  confirmation needed.** The Governing Council's rates (deposit facility
  2.50%, main refi 2.65%, marginal lending 2.90%) were reconfirmed again
  directly against ecb.europa.eu at edition 54. The press-conference-content/
  vote-split sub-question and the exact next-meeting date both remain
  unconfirmed/unreachable at edition 54 too (not specifically re-attempted
  this edition, out of scope) — still estimated mid-December by typical
  six-weekly cadence, not verified. **The BoJ's Oct 29-30, 2026 meeting
  decision is now RESOLVED, closing the live numeric-rate question edition 53
  carried forward.** The Bank **HELD** its policy rate at approx. 1.25% at
  its 29-30 October meeting, confirmed directly against boj.or.jp's own
  statement PDF (released 12:02 JST Friday 30 Oct, approx. 11:02pm ET
  Thursday 29 Oct — just inside edition 54's window open). **Vote 8-1:**
  Takata Hajime dissented, proposing a hike to approx. 1.5% on grounds that
  underlying inflation had reached target; September's two dissenters (Asada
  Toichiro, Sato Ayano) both voted for hold this time — a notable shift in
  the dissent composition worth watching if it recurs. A companion unanimous
  vote raised the pace of ETF sales to approx. ¥860bn/year (from approx.
  ¥330bn/year) effective January 2027 — a balance-sheet item, not a rate
  move. **BoJ's next decision date was not confirmed at edition 54** (the
  research pass didn't reach BoJ's own meeting calendar) — try boj.or.jp's
  schedule page directly at edition 55; do not state a specific date without
  checking, even though typical cadence suggests mid-to-late December 2026.
  **Riksbank's next-decision date remains RESOLVED** (3 Nov meeting, decision
  published 4 Nov 2026), re-confirmed again at edition 54 via riksbank.se's
  own calendar page directly. **The CURRENT RATE VALUE (1.75%) could NOT be
  reconfirmed directly at edition 54** — riksbank.se's own dedicated
  policy-rate page 404'd; the value is corroborated only by consistent
  secondary sourcing. Try a different riksbank.se URL path at edition 55. The
  exact origin date of the 1.75% level itself remains a separate,
  lower-priority imprecision. **The Reserve Bank of Australia's current rate
  (4.60%) was reconfirmed DIRECTLY at edition 54** for the first time in
  several editions — rba.gov.au's media-releases page loaded and confirmed
  the latest posted item is still the 29 Sept 2026 rate-hike release, with no
  November item yet (a dedicated schedules-events page 404'd, but the
  media-releases page itself worked). **Next decision: Tuesday 3 November
  2026, 2:30pm AEDT** (approx. 10:30-11:30pm ET Monday 2 November) — falls
  just after edition 54's own window closed and most likely after whichever
  edition covers the Monday 2 November session too, given typical cutoff
  timing; watch directly for the actual outcome, probably landing in the
  edition after that. **Norges Bank's next-decision date (17 December 2026)
  was reconfirmed directly against norges-bank.no at edition 54's monthly
  audit**, alongside its current rate (4.50%, unchanged since 24 Sept 2026).
  **SNB's current rate (0.00%) was reconfirmed directly against snb.ch at
  edition 54** (effective, most recent assessment 24 Sept 2026) but its
  **next assessment date remains unconfirmed** — SNB's dedicated
  decisions/schedule page was not reached again; try a different URL pattern
  at edition 55. **Banxico's current rate (6.50%) could not be reconfirmed
  directly at edition 54 either** — both banxico.org.mx and an alternate
  mirror (anterior.banxico.org.mx) returned 404; the rate is corroborated
  only by consistent secondary sourcing (Bloomberg Línea, Monex, Mexico Cómo
  Vamos). Banxico's next-decision date also remains unavailable. Try a
  different banxico.org.mx URL path (perhaps the English-language IR site,
  or a press-release index) at edition 55.
- **SETTLED — Bank of England held at 3.75% on Thursday 17 Sept 2026, a 6-3
  vote** (same three dissenters as 30 July, all favoring a hike to 4.00%) —
  resolved, does not need re-confirming again unless a new decision date has
  passed. **Next BoE decision: Thursday 5 November 2026** — this falls just
  outside edition 54's own window; it will land in whichever edition covers
  the Thursday 5 November session (estimated edition 58 if daily cadence
  holds) — watch for the actual outcome there.
- **SETTLED (the September decision only) — Bank of Japan hiked 25bp to
  approx. 1.25% on 18 September 2026** (effective 24 Sept), a 31-year high, a
  7-2 vote (dissenters Asada Toichiro and Sato Ayano) — closed thread, do not
  re-derive. **The Bank's SUBSEQUENT 29-30 October 2026 meeting HELD the rate
  at approx. 1.25% (8-1 vote, dissenter Takata Hajime)** — see the dedicated
  general-principle entry above for full detail; this October decision is now
  itself resolved meeting history (one direct confirmation so far, edition
  54) and the numeric rate is live again only pending BoJ's next meeting,
  whose date is not yet confirmed.
- **SETTLED — the four-central-bank Thursday 24 September 2026 cluster,
  closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% but signalled a greater chance of
  a Q4 hike; Banxico held at 6.50% unanimously; SNB held at 0% and raised its
  inflation forecasts, confirmed directly against snb.ch.
- **SETTLED — the Reserve Bank of Australia's Tuesday 29 September 2026
  decision, closed thread, do not re-open:** hiked 25bp to **4.60%,
  unanimous**, a 15-year high and its fourth hike of 2026, confirmed directly
  against rba.gov.au's own Statement by the Monetary Policy Board at edition
  47; re-confirmed directly again via rba.gov.au at edition 50 and a third
  time at edition 54's monthly audit.
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
  2022; the trade-services-excluded measure was +0.5% m/m / +5.0% y/y.
  Energy (+10.8% m/m, gasoline +20.3%) drove over 80% of the goods-side
  increase. Confirmed directly against bls.gov.
- **September 2026 Import/Export Price Indexes — closed thread as of edition
  44, do not re-derive:** import prices **+1.1% m/m / +8.1% y/y** (the
  largest 12-month increase since July 2022), export prices **+2.2% m/m /
  +11.6% y/y**; export prices to China specifically +2.7% m/m / +7.5% y/y,
  import prices from China +3.1% y/y. Released Friday 16 October 2026,
  confirmed directly against bls.gov.
- **September 2026 Industrial Production & Capacity Utilization (G.17) —
  closed thread as of edition 44, do not re-derive:** total industrial
  production **+0.7% m/m / +2.2% y/y**, manufacturing output +0.3% m/m/+1.1%
  y/y, capacity utilization **76.9%**. Released Friday 16 October 2026,
  confirmed directly against federalreserve.gov's G.17 release. The Fed
  flagged an annual benchmark revision to this series due 24 November 2026 —
  watch for a level reset around that date, not a genuine month-over-month
  signal.
- **US Q3 2026 GDP (advance estimate) — closed thread as of edition 53,
  do not re-derive:** real GDP **+3.4% annualized** (vs. +2.2% in Q2 2026),
  led by services- and goods-led consumption, private inventory investment
  and equipment spending; real final sales to private domestic purchasers
  +4.9%. Released Thursday 29 October 2026, 8:30am ET, confirmed directly
  against bea.gov. No independently-confirmed consensus figure was found at
  edition 53 — don't cite a "vs. consensus" framing without a fresh source.
  Next release (2nd estimate + corporate profits): 25 November 2026.
- **September 2026 PCE / core PCE — closed thread as of edition 53, do
  not re-derive:** headline **+0.5% m/m / +3.6% y/y**, core **+0.3% m/m /
  +3.1% y/y** — both well above the Fed's 2% target and a further
  acceleration from August's +0.3%/+3.4% headline, +0.2%/+3.0% core. Released
  in the same 8:30am ET slot as Q3 GDP on Thursday 29 October 2026, confirmed
  directly against bea.gov.
- **No US federal government shutdown is in effect — directly reconfirmed at
  edition 54 via whitehouse.gov**, resolving edition 53's failed
  reconfirmation attempt. H.R. 6500 funds federal agencies through **11
  December 2026** per the clean edition-54 confirmation. Watch for shutdown
  risk resurfacing as that date approaches.
- **University of Michigan October 2026 consumer sentiment — CLOSED thread as
  of edition 49, both preliminary and final readings in hand:** preliminary
  46.3 (a five-month low); **final 48.0** (vs. September's final 48.1 and the
  approx. 47.6 consensus). Final sub-indices: current conditions 46.7,
  expectations 48.8; year-ahead inflation expectations 4.7%, long-run 3.5%.
  The final reading remains secondary-sourced only (umich.edu itself not
  directly fetched).
- **China September 2026 CPI/PPI — RESOLVED, closed thread, do not
  re-derive:** CPI **+0.9% y/y** (+0.2% m/m), PPI **+5.0% y/y** (the fastest
  PPI rise since June 2022), driven by fuel costs. Sourced to gov.cn's
  English-language NBS-attributed news release. **China's October 2026 PMI is
  now also RESOLVED as of edition 54:** manufacturing PMI **49.3** (down from
  September's 50.1, a third contraction in four months) and non-manufacturing
  PMI **49.7** (down from 50.2) — both back below the 50 expansion/
  contraction threshold, reversing September's above-50 readings. The
  non-manufacturing figure is sourced directly to Xinhua's English wire; the
  manufacturing figure rests on Reuters-sourced wire coverage (stats.gov.cn's
  own English-language PMI release had not posted at the time of the
  edition-54 fetch, and the Chinese-language original article 403'd) —
  upgrade the manufacturing figure's sourcing tier if a direct stats.gov.cn
  fetch succeeds at a future edition, though low priority now that the
  headline figures are corroborated and the thread is otherwise closed.
- **China Q3 2026 GDP — RESOLVED at edition 45, closed thread, do not
  re-derive:** printed Monday 19 October 2026, confirmed directly against the
  National Bureau of Statistics' English-language press release. Q3 alone:
  **+4.5% y/y, +1.2% q/q**; first-three-quarters 2026 cumulative: **+4.6%
  y/y** (GDP RMB 107,107.1bn).
- **New Mexico v. Meta — the $25bn civil-penalty ruling (Judge Francis
  Mathew, Wed 21 Oct 2026) remains substantially clarified but Meta's formal
  notice of appeal is still unconfirmed for a NINTH straight edition
  (47-54).** Meta owes **$25bn** in civil penalties for the jury's
  late-September verdict — above the 48-other-state $18bn settlement Meta
  already reached elsewhere, well below New Mexico's $35-40bn ask and the
  $219.5bn theoretical statutory maximum. Meta has said it will appeal but
  continues to express only future-tense confidence in prevailing "on
  appeal," per the last dated company statement (edition 50). This $25bn
  judgment is **distinct** from: (1) a separate, earlier New Mexico Unfair
  Practices Act matter (approx. $942m total, Meta posted an $1.8bn bond,
  received an unopposed stay of enforcement around 9 Oct 2026); (2) the March
  2026 child-safety jury verdict ($375m, Judge Bryan Biedscheid); (3) the
  August 2026 abatement ruling ($567m, same Biedscheid case, under appeal);
  (4) Meta's own Q3 2026 earnings charge — a separate $9.89bn one-time charge
  tied to an August 2026, 52-state-AG teen-safety settlement that explicitly
  excludes New Mexico. Don't conflate any of these four. Not independently
  re-attempted at edition 54 beyond a standard check; no new development in
  the 48-state settlement or the Unfair Practices Act stay either.
- **New calendar-awareness item, reconfirmed relevant across several
  editions: "equities-open, bonds-closed" US holidays need an explicit check
  every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. **Next candidate to verify when it lands: Veterans Day, Wed 11 Nov
  2026** — not yet inside any edition's window; confirm whether that is also
  bonds-only before assuming, when it lands. **The DST transition (ended
  Sunday 1 November 2026) is now itself resolved/settled** — see the Schedule
  section above for confirmation detail.
- **The vendor-retroactive-revision trap continued at edition 54, now a
  FOURTH consecutive edition for gold and silver, and a FOURTH consecutive
  edition of unresolved base-price unreliability for Henry Hub.** (1) Gold
  and silver: edition 54's freshly re-fetched Thursday 29 October base (gold
  $4,031.40, silver $52.380) again did not match edition 53's own
  directly-confirmed Thursday figures (gold $4,019.65, silver $51.980) — an
  $11.75 and $0.40 discrepancy respectively on the identical calendar date
  from the same vendor (Investing.com). Continue the fresh-refetch-every-
  edition discipline; the discrepancy is disclosed in the published report
  each time rather than silently resolved by picking one figure. (2) Henry
  Hub: edition 54 attempted a genuinely independent primary source again
  (CME/NYMEX settlement page timed out twice, Barchart's NGZ26 futures-prices
  page returned empty content twice, and EIA's daily Henry Hub spot series
  had not yet posted Thursday/Friday data at fetch time due to its normal
  lag) — all three attempts failed, and edition 54's figures remain
  single-sourced to Investing.com. Recommendation reinforced again: keep
  trying a genuinely different primary source at edition 55; until then,
  continue treating Henry Hub as this report's single worst-performing data
  series and disclose it as provisional every edition. **By contrast, WTI,
  Brent, copper (LME cash, carried forward from edition 53's own log for the
  Thursday base — see the dedicated sourcing-mechanics note below), DXY,
  EUR/USD, GBP/USD, USD/JPY and the Treasury curve all reconciled without
  incident at edition 54** — the trap's locus continues to rotate rather than
  spreading to every instrument at once. The Treasury curve remains the one
  instrument class that has never shown this trap across every edition
  checked (now 19 straight clean editions, 37-54).
- **New sourcing technique validated at edition 54, worth reusing: when a
  same-day primary source (e.g. westmetall.com for LME copper) exposes only
  the CURRENT day's row and a prior-session base can't be re-fetched, citing
  the prior edition's own already-directly-confirmed figure for that prior
  date is a legitimate substitute for a fresh fetch** — consistent with the
  citation-reuse/prior-edition-as-source pattern already established for the
  Annex C numbering rules. Edition 54 used edition 53's own logged Thursday
  29 October LME copper close ($14,560.00, confirmed directly against
  westmetall.com at edition 53) as the base for computing Friday's -0.76%
  move, rather than leaving the comparison blank or estimating. Apply this
  pattern generally whenever a same-day-only primary source blocks a fresh
  prior-session re-fetch, provided the prior edition's own figure was itself
  a direct confirmation, not a carried-forward or disputed one.
- **New sourcing-mechanics trap logged at edition 50, relevant to any
  Monday-dated (or any day-after-a-non-trading-day) edition: Investing.com
  inserts an electronic Sunday-evening re-open print as its own row for every
  24-hour-traded instrument.** Applicable in principle at edition 54 (a
  weekend-gap, Monday-dated edition) — the commodities research pass
  explicitly pulled the raw Thursday 29 Oct and Friday 30 Oct closes and
  computed the Thu-to-Fri change manually, and separately identified (but did
  not conflate into that change) a Sunday-evening Kitco spot gold reading
  timestamped Sun 1 Nov approx. 8:26pm ET — correctly keeping the weekend
  re-open-adjacent reading distinct from the Friday close used for the
  reported % change. No incident this edition; continue applying this
  discipline on every post-weekend or post-gap edition.
- **LME copper's primary source (westmetall.com) remains reliable in
  principle** — edition 54's Friday fetch succeeded cleanly ($14,449.00 cash,
  $14,250.00 3-month) — but the live page exposed only the CURRENT day's row,
  meaning a same-day Thursday base could not be independently re-fetched at
  edition 54; the carried-forward-prior-edition-figure workaround was used
  instead (see the dedicated new sourcing-mechanics entry above). A COMEX
  cross-check (Investing.com, $6.4820/lb, -1.83%) again agreed directionally
  but not in magnitude with the (carried-forward) LME figure — the
  recurring, disclosed-but-not-alarming pattern continues.
- **Henry Hub natural gas: see the dedicated, elevated entry under the
  vendor-retroactive-revision trap above — this remains the report's
  single worst-performing data series.** The front-month-contract identity
  (NGZ6/December) was confirmed again via Investing.com's own page header at
  edition 54; OHLC internal consistency was not specifically re-checked this
  edition.
- **The Kitco live-spot-vs-headline cross-check was attempted again at
  edition 54, but only for gold this time** — no silver quote was directly
  obtainable from the fetched page (a derived gold/silver ratio of 78.4
  implied an indicative, not quoted, silver price of approx. $49.8, within
  approx. 1% of Investing.com's Friday close). Gold spot $3,906.10 (ask
  $3,908.10), explicitly timestamped Sunday 1 Nov 2026, 8:26pm ET (a weekend
  re-open-adjacent reading, kept distinct per the dedicated Monday-trap entry
  above), versus Friday's futures close of $3,898.90 — an approx. 0.19% gap,
  within the normal sub-1% premium range, no red flag. Continue attempting
  both metals directly each edition when timing allows.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company, IPO'd 1 July 2026 at
  $29/share. Logged here so a future edition doesn't waste effort
  re-verifying the ticker's legitimacy if it moves sharply again.
- **The "named secondary outlet's own claim can be flatly wrong" trap**
  — edition 54 added further reinforcement without a new flatly-wrong
  instance of its own, but DID catch and discard two low-quality/misdated
  sources before they could enter the report: a Reuters-style "stocks on the
  move" squib (Verisk alongside Fiserv/Boeing) carrying no confirmable year
  and possibly misdated to 2025, and a Trefis "movers" list whose own URL was
  dated to 2025-10-31, not this edition's session — both excluded entirely
  rather than cited with a caveat, extending the discipline of checking
  source dates (not just claimed drivers) before use. Prior instances:
  JetBlue (edition 50, magnitude), Carvana/Barron's (edition 52,
  direction/framing), Tesla and NU Holdings (edition 49, magnitude, twice in
  one session), Marvell/Lumentum and Barclays/PayPal (edition 53, claimed
  driver and a likely-fabricated analyst action).
- **A reinforcing, non-novel reminder: a clean beat-and-raise continues to
  carry essentially no predictive power for the market's reaction.** Edition
  54 did not add a new same-session instance of this specific pattern (no
  equivalent of ServiceNow's or Intel's beat-then-fall case surfaced in the
  Friday 30 Oct earnings cluster), but the four previously-pending reporters
  that DID surface Friday (Chevron, Exxon Mobil, AbbVie, Newell Brands) all
  both beat AND rose — a reminder that the pattern is about reaction
  unpredictability in general, not a rule that beats always disappoint;
  continue fetching the actual reaction as a separate, disclosed fact every
  edition regardless of earnings quality. Edition 53 remains the
  largest-magnitude instance logged to date (ServiceNow -26.95%).
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent, but has
  agreed again at edition 54** (DXY futures-proxy -0.14%, UUP -0.14%,
  USD/JPY -0.10%, all pointing to a modestly softer dollar) — a fifth
  straight session logged. **The DXY true-spot sourcing gap WIDENED rather
  than resolved: both ICE's own index page (404) and MarketWatch
  (unreachable) failed again at edition 54, now a THIRD straight edition with
  no working true-spot route.** Try a different approach entirely at edition
  55 — e.g. Yahoo Finance's own DXY ticker page, Trading Economics, or a
  wire-service FX report — rather than repeating ICE/MarketWatch a third
  time.
- **The single-aggregator-dependence pattern for the AP/Reuters index-close
  wire: a NEW variant of the standing workaround succeeded at edition 54.**
  Neither apnews.com nor Reuters' own wire page was directly located for
  Friday 30 October, but an AP-wire mirror syndicated through an
  INTERNATIONAL outlet (lanacion.com.ar, Argentina) carried the full "How
  major US stock indexes fared" content and matched two independent US
  secondary sources (stockmarketwatch.com's Nightly Market Digest,
  thebusinessjournal.com) exactly, plus SPY/DIA/QQQ/IWM ETF-proxy
  corroboration. **Try this international-syndication-mirror approach FIRST
  at edition 55**, ahead of the Yahoo-Finance-plus-Investrade fallback that
  has been the recommended default since edition 53 — it is closer to the
  actual AP wire content, not just a corroborating secondary source.
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38, most recently exercised at edition 52.** Not exercised at
  edition 54 — no megacap GAAP/non-GAAP EPS conflict surfaced in the Friday
  30 Oct earnings cluster. Coinbase's Q3 did show a related-but-distinct
  pattern (a GAAP profit of approx. $719m driven almost entirely by crypto
  mark-to-market gains, with adjusted net income of only approx. $78m) —
  reported plainly with both figures disclosed, not flagged as a new
  instance of the specific trap.
- **The "preview-consensus-only miss/beat framing" caution (first logged at
  edition 41) remains an open, unconfirmed disclosed inference, not
  re-chased at edition 54 either.** Pick this thread back up at a future
  edition if bandwidth allows.
- **Equifax's unexplained-magnitude rally thread remains open but of
  declining urgency, with one dead end now explicitly ruled out:** Equifax
  rose a further 2.90% Friday 30 Oct with no dated catalyst found despite a
  targeted search; a "Credit Abuse Risk" product-launch lead was checked and
  found to be dated 30 January 2026, not 30 October — a false lead, not a
  driver, now explicitly excluded from future searches on this thread.
- **New at edition 47, reinforced every edition since including 54: when
  standard "biggest movers" aggregator pages aren't retrievable, SEC EDGAR's
  full-text search / `cgi-bin/browse-edgar` (filtered by CIK and form type
  8-K) is an effective, primary-source-grounded discovery/verification
  method** — used again at edition 54 to confirm and source Chevron's, Exxon
  Mobil's, AbbVie's, Newell Brands' and Colgate-Palmolive's own Exhibit 99.1
  filings directly. This is now the firmly established default verification
  route for any megacap or notable earnings report.
- **The edition-49 "forward-looking calendar aggregator" trap (names falsely
  listed as past reporters before they actually reported) remains closed and
  was reconfirmed accurate again at edition 54:** all four names (Chevron,
  Exxon Mobil, AbbVie, Newell Brands) that third-party calendars had placed
  on Friday 30 October did in fact report that day, each confirmed via its
  own 8-K Exhibit 99.1 — closing this specific multi-edition watch thread
  with no incident.
- **A megacap multi-name earnings cluster producing genuinely uncorrelated
  reactions is a standing, repeated pattern across at least NINE distinct
  instances through edition 53 (editions 44, 47, 48, 49 x2, 50, 52, 53 x3).**
  Edition 54 did not add a dramatic new instance (see the updated
  beat-and-raise entry above — Friday's four pending reporters all beat and
  rose uniformly), keeping the standing count at nine through edition 53.
  Treat "beat and raise" as having essentially no predictive power for this
  report's purposes without also checking the specific sub-metric or
  guidance nuance investors are reacting to, and always fetch the actual
  reaction as a separate, disclosed fact.
- **New production lesson from edition 53: CSS multi-column (`.cols3`/
  `.cols2`) pagination under Chromium print-to-PDF can plateau stubbornly on
  marginal content trims** — see edition 53's full writeup (now condensed in
  the edition log) for the mechanics and the fix (merging several Annex C
  entries at once rather than iterating with small per-entry trims). **Not
  triggered at edition 54** — the spillover mechanism (deleting the single
  forced page break when sections 1-6 ran onto page 4) converged cleanly on
  the first re-render with no Annex C column-balancing issue, consistent
  with most editions' experience; edition 53's plateau appears to have been
  content-volume-specific rather than a general property of the CSS
  approach.
- **New at edition 54: the VIX feed's two known bugs (duplicated
  `prev_day_close`, and a `price_change_percent` that divides by the wrong
  price) appeared on ALL SIX series at edition 54** (VIX, VIX9D, VIX3M,
  VIX6M, VVIX and SKEW), not intermittently as several recent editions
  found — continue the manual-calculation discipline unconditionally
  regardless of how many bug-free editions might follow.
- **New at edition 54: a markup-correctness self-check caught three
  instances of the `</td><sup` table trap (documented under Production
  notes below) before rendering, in the Commodities table's FX/Treasury rows
  where an empty trailing "Note" cell was followed by a citation tag typed
  outside it.** Worth running `grep -n '</td><sup'` proactively on every
  edition with a table that has an empty trailing cell, not just after a
  page-count problem — the trap is easiest to introduce exactly there.
- **New at edition 54: the CFTC Asset-Manager-vs-Leveraged-Funds grouped-bar
  chart was reused for a fifth time (editions 34, 39, 44, 49, 54 — a clean
  Monday/weekend-window pattern) with the same figsize (9.8, 2.15), `h=0.32`
  bar offset and figure-level legend technique documented under Production
  Notes — rendered cleanly on the first attempt with no overlap or
  legend-placement issue, reinforcing this as a stable, reusable pattern.**

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
  longer the first answer. **Edition 53 remains the clearest cautionary
  tale**: a genuinely dense single-session day (a dominant macro print plus
  a double-digit-name earnings cluster) rendered at 6 pages on the first
  draft and needed roughly a dozen trim/merge rounds to converge. **Edition
  54, despite its own dense load (BoJ decision, China PMI, a monthly audit,
  a historic Intel drop, a major crypto hack, four resolved pending-earnings
  reporters and fresh CFTC data feeding a third chart), converged to a clean
  4 pages on the FIRST re-render after simply deleting the one forced page
  break** — a reminder that not every dense day requires a trimming
  marathon; check the spillover-vs-still-overflowing distinction before
  assuming heavy content automatically means a multi-round trim.
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
  `check_refs.py` only checks presence/absence, not uniqueness of use.
  **Citing the prior edition itself as a source** (e.g. "[35] ... Daily
  Economic Briefing edition 53, logged prior-session baseline figures") is a
  legitimate, already-used pattern when disclosing a divergence against, or
  carrying forward, a previously-logged figure — edition 54 used this again
  for LME copper's Thursday base.
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
  request.** Assumptions and status live in **Annex A**. What stays on page
  1 is **corrections only**: a figure published in an earlier edition that
  turned out to be wrong, or a premise-level correction. Terse — what was
  published, what it should have been — with the full record in Annex A if
  it needs more than a line. **Omit the box entirely on an edition that
  corrects nothing**, which will be most of them. **Edition 54 omitted the
  box** — nothing published in a prior edition was found to be wrong; the
  gold/silver vendor-revision discrepancy was treated as a sourcing-trap
  disclosure in Annex A, not a correction, consistent with how prior
  editions have handled the same recurring vendor-revision pattern.
- **All sector and ETF material belongs to Section 1 — by request since
  edition 49.** Section 1 keeps its snap-grid tiles and recap paragraph and
  gains the sector-ETF chart plus the narration of how each sector did in
  the session. **Section 2 is purely single-stock**: movers chart, movers
  table, earnings, guidance, analyst actions. The test is simple — if a
  sentence is about a sector rather than about a named company, it goes in
  Section 1. Section 6's "sector setup we take into [session]" bullets stay
  where they are; they are forward-looking, not a recap of what happened.
- **Section 3 carries a central-bank policy-rate table.** Columns: **Central
  bank | Policy rate | Last change | Next decision**. The Fed goes first as
  the anchor to compare against, then whichever of the BoE, BoJ, ECB, SNB,
  Norges Bank, Riksbank, RBA, BoC and Banxico the window actually touches —
  eight to ten rows is the working range. A bank whose current rate could
  not be verified still gets its row, with that cell marked unavailable and
  a matching Annex B entry. **Edition 54 ran a full 10-row table** (Fed, BoJ,
  BoE, ECB, BoC, RBA, SNB, Norges Bank, Riksbank, Banxico), with BoJ's, ECB's,
  SNB's and Banxico's "next decision" cells marked as not confirmed rather
  than guessed — the intended disclosure pattern. If page 3 overflows anyway,
  cut rows that had no news in the window before cutting any prose. Follow
  the usual table convention — plain `<tr>` header rows, no `<thead>`.
- **Charts: two fixed, a third only when earned — changed at edition 49.**
  The **sector-ETF performance chart always goes in Section 1**, beside the
  sector narration it illustrates, and the **single-stock movers bar always
  goes in Section 2**, with the names. Neither may duplicate a table.
  A **third chart is allowed only when positioning or volatility is
  genuinely the day's dominant story** — not merely present, and never to
  fill a short page — and it goes in the section it belongs to: CFTC
  asset-manager vs. leveraged-funds positioning or a VIX term structure in
  Section 5, an implied-vs-realized earnings bar in Section 2. **Edition 54
  used the CFTC positioning chart** (fresh data posted on schedule, covering
  Tuesday 27 October, the fifth time this specific Monday/weekend-window
  trigger has justified the chart — editions 34, 39, 44, 49, 54), in Section
  5, alongside a VIX complex that spiked sharply (+12.91%) but stayed in
  clean contango and so did not independently justify its own chart. Next
  CFTC report due **Friday 6 November 2026**, covering Tuesday 3 November
  data — check cftc.gov directly whichever edition's window includes it.
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
  they're actually indexed for the target date before relying on them.
  **Editions 48 through 53 all found neither wire indexed/fetchable** (with a
  single one-edition exception at edition 51 via a syndicated mirror).
  **Edition 54 found a NEW, cleaner variant of the same workaround: an
  AP-wire mirror syndicated through an international outlet (lanacion.com.ar)
  carried the full wire content and matched two independent US secondary
  sources exactly.** Try this international-syndication-mirror approach
  FIRST at edition 55, ahead of the Yahoo-Finance-plus-Investrade fallback —
  but re-attempt apnews.com/Reuters directly every edition regardless.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Always check a dated article's own claimed magnitude AND
  direction against the underlying price-history table or primary filing,
  not just its date, before repeating it** — this trap has now hit
  magnitude (J.B. Hunt ed.44, Tesla/NU Holdings ed.49, JetBlue ed.50),
  direction/framing (Carvana/Barron's ed.52), claimed drivers that don't
  hold up (Marvell/Lumentum ed.53), a claimed analyst action that appears
  outright fabricated (Barclays/PayPal ed.53), and **at edition 54, the
  claimed DATE/YEAR itself** (a Reuters-style squib and a Trefis movers list
  both excluded after their own dates couldn't be confirmed against this
  edition's actual session) — treat ANY surprising secondary claim (price
  move, driver, analyst action, or date) as needing this same verification
  discipline.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  **Edition 54 continued this discipline**, individually verifying
  single-stock closes directly against stockanalysis.com, cross-checking SEC
  EDGAR 8-Ks for Chevron, Exxon Mobil, AbbVie, Newell Brands and
  Colgate-Palmolive, and excluding two misdated/unconfirmed secondary
  sources before they entered the report.
- **Premarket is not the close, and the close is not the after-hours
  earnings reaction — and an after-hours reaction does not necessarily hold
  into the next regular session, uniformly or at all. A strong beat-and-raise
  does not guarantee a positive reaction even within the SAME session.**
  Reinforced at essentially every edition since 44; edition 53 remains the
  largest-magnitude same-session instance (ServiceNow, -26.95% despite a
  clean beat-and-raise). Edition 54 did not add a new instance of this
  specific pattern — its four previously-pending reporters all beat AND rose
  uniformly — but the actual reaction was still fetched and disclosed as a
  separate fact from earnings quality, per the standing discipline. Always
  fetch the verified close, the after-hours reaction, AND (when the window
  allows) the next regular session's close as three separate, clearly
  labelled figures.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent but has
  agreed again at edition 54** — see the dedicated, updated Standing Facts
  entry above (which also now flags a THIRD straight failed attempt at
  finding a true ICE-spot DXY source). Continue disclosing the DXY-vs-USD/JPY
  directional comparison explicitly every edition regardless of which way it
  goes.
- **The Kitco live-spot-vs-headline cross-check was attempted again at
  edition 54, gold only this time** — no conflict found, a normal sub-1%
  premium. Continue attempting both metals each edition when research-pass
  timing allows a same-day check.
- **GBP/USD, EUR/USD and USD/JPY all reconciled cleanly again at edition 54**
  against their logged Thursday base — the vendor-revision trap this
  edition hit gold, silver and (again) Henry Hub, but not the FX crosses,
  WTI/Brent, or Treasuries. Resume the fuller multi-source method on any
  FX/commodity pair if a fresh same-day conflict reappears.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for nineteen further editions (37-54)** — edition 54 again found the full
  Treasury curve reconciled perfectly against the prior edition's logged
  base via home.treasury.gov (2-year 4.56%, 10-year 4.94%, 30-year 5.31%,
  down 1-5bp on the day). Treat as resolved/noise unless a fresh conflict
  appears.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 54 have all run clean (or
  clean after quick fixes) — **edition 54 needed one fix** (a source cited
  only in a chart axis label, [1], needed an inline body citation added
  too), **and separately caught, via a proactive `grep -n '</td><sup'`, three
  instances of the table markup-correctness trap BEFORE rendering** (empty
  trailing "Note" cells in the Commodities table followed by a stray `<sup>`
  tag outside the `<td>`) — worth running that grep on every edition with a
  table that has an empty trailing cell, not just after a page-count
  problem.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 54 have all rendered with zero stray tildes on the
  first draft.**
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39, 44, 49 and 54 have
  all resolved this cleanly for CFTC CoT, with full OI and Asset-Manager/
  Leveraged-Funds breakdowns for ES, NQ and RTY, normalized as % of open
  interest. The next CFTC report (due Fri 6 Nov, covering Tue 3 Nov data)
  falls inside a future edition's window — check cftc.gov directly then.
- **The diffuse-overflow lesson from editions 44-45 and the duplicated-
  content lesson from edition 47 are both still worth checking first on any
  overflow** — but **edition 53 showed overflow can also be genuinely dense
  content requiring real trimming, while edition 54 showed the opposite:
  heavy content does NOT automatically mean a multi-round trim** — edition
  54's own dense load converged to 4 pages on the first re-render after
  simply deleting the one forced page break. Always check which situation
  you're in (stray break vs. genuine overflow vs. spillover that just needs
  the break deleted) before assuming a trim marathon is required.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — **specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation.** Edition 54's
  movers chart (10 categories, Intel -28.58% largest, Coinbase -10.62%
  second largest) had a ratio of only approx. 2.7x — no capping needed. Used
  `pad_frac=0.26` for the movers chart (9.8, 1.95 figsize) and
  `pad_frac=0.30` for the 11-category sector panel, both rendering cleanly
  with no label crowding.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 54 have all got a fresh,
  same-day-timestamped sweep** — twenty-seven consecutive fresh sweeps now.
  **The feed's two known bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) appeared on ALL SIX series at edition 54** — not intermittently, as
  several recent editions found. **Always compute day-over-day % change
  manually regardless of how many consecutive bug-free reads preceded the
  current one.** Edition 54 saw the VIX complex jump sharply on Friday's
  tech-led selloff: VIX +12.91% to 19.42, VIX9D +21.30% to 19.25, VIX3M
  +7.28% to 20.78, VIX6M +4.52% to 22.20, VVIX +8.59% to 106.43, SKEW -0.84%
  to 149.76 — the complex's largest one-day jump logged in months, yet
  term structure held clean contango throughout (VIX9D < VIX < VIX3M <
  VIX6M), arguing against a structural stress signal.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 54 fetched all 11 directly again**
  (Energy +1.91% the clear leader on Friday's energy-earnings beats and a
  firmer oil tape, Technology -4.89% the clear laggard on Intel's historic
  plunge and Nvidia's drag; 6 of 11 green) — continue this
  direct-fetch-by-default method.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (6 of 11 at edition 54) — no
  competing secondary-aggregator breadth figure was checked this edition.
- **Dealer gamma:** zerogex.io hit a **fifteenth consecutive edition of
  failure at edition 54** (all widgets still show placeholder dashes with no
  timestamped data). SpotGamma logged a **ninth straight failure at edition
  54**, confirmed again as a client-side React single-page app with zero
  server-rendered data behind its dashboard.spotgamma.com login. Both
  sources remain fully unusable.
- **Official CME FedWatch probabilities:** the page blocks fetching
  (edition 54's direct attempt timed out again, a **fourteenth** consecutive
  failure, 41-54) — use secondary citations (Polymarket, Kalshi, Reuters/
  other economist polls, desk notes) and give a range rather than a single
  invented number. DeFi Rate's Kalshi/Polymarket-blended aggregator remains
  a stable, consistently working source for both the near-dated and
  December meetings — though its December sub-table has now shown an
  internal inconsistency for **eight straight editions** (47 through 54) and
  should simply be expected and disclosed, not treated as a transient bug.
  **Polymarket direct, tried via its Gamma API (`gamma-api.polymarket.com/
  public-search`) rather than a plain site visit at edition 54, succeeded
  for the first time in several editions** — returned live, correctly-dated
  December 2026 contract pricing matching DeFi Rate's own figures almost
  exactly. Use this API-based approach first at edition 55, rather than
  reverting to a plain site visit (which showed only an expired December
  2025 contract at editions 52-53).
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, now **eighteen consecutive failures (37-54)** — a confirmed
  structural gap, not transient. Resume the attempt-every-edition discipline
  at edition 55 regardless, but expect a block of some kind. Use Kalshi's
  own secondary reporting or DeFi Rate's blended aggregator as the
  workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages); the CME natural-gas settlement page also
  timed out again at edition 54 (see Henry Hub entry below). westmetall.com
  remains the standing LME copper primary source for the CURRENT day, but
  edition 54 found its live page exposes only that day's own row, not a
  prior-session history table — see the dedicated new sourcing-technique
  entry in Standing Facts for the carried-forward-prior-edition-figure
  workaround this produced.
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **remained clean at edition 54** (2-yr
  4.56%, 10-yr 4.94%, 30-yr 5.31%, all 30 Oct, with the prior Thursday base
  matching the previous edition exactly), extending the clean streak to
  **nineteen editions (37-54)** with no repeat of the edition-36 33bp gap.
  Continue scoping the TextView URL to the specific month
  (`field_tdr_date_value_month=202610`/`202611`-style parameter) rather than
  the full year.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). **The Friday 30 October 2026 report, covering Tuesday 27
  October data, posted on schedule and was pulled in full at edition 54**
  (ES: OI 1,955,711, AM +47.2%/LF -20.5% of OI; NQ: OI 268,508, AM +24.4%/LF
  +0.9%; RTY: OI 458,959, AM +4.3%/LF -10.5%), powering the third chart (see
  Chart Selection Guidance). **Watch the micro-vs-full-size Russell/Nasdaq
  naming trap each time** — edition 54 confirmed the correct full-size
  contracts (E-MINI S&P 500, NASDAQ MINI, RUSSELL E-MINI), distinct from
  their micro counterparts. **The next report is due Friday 6 November
  2026, 3:30pm ET, covering Tuesday 3 November data** — check cftc.gov
  directly whichever edition's window includes it.
- **GBP/USD, EUR/USD, USD/JPY clean close:** all remain fully resolved,
  reconciling cleanly again at edition 54 (EUR/USD 1.1160 -0.18%, GBP/USD
  1.3392 +0.10%, USD/JPY 157.55 -0.10%, all single-sourced to Investing.com's
  close-to-close history table, Thursday base matching this edition's own
  fresh re-fetch). **DXY itself is NOT cleanly sourceable as a true ICE
  spot index — a third attempt at a genuine spot source (ICE's own page,
  404; MarketWatch, unreachable) failed again at edition 54**, extending the
  gap first logged at edition 52. UUP (the dollar ETF) continues as the
  directional cross-check (-0.14% Fri 30 Oct, same direction as the
  futures-proxy DXY's -0.14%) — both corroborate a modestly softer dollar.
  **DXY and USD/JPY direction agreed for a fifth straight session at
  edition 54** — continue disclosing this comparison every edition. Try
  Yahoo Finance's DXY ticker page or Trading Economics at edition 55 rather
  than ICE/MarketWatch a third time.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot cross-check was repeated at edition 54 for gold only** (no
  silver quote directly obtainable) — see the dedicated Standing Facts entry
  above. **The base price itself showed a vendor-revision discrepancy for a
  FOURTH consecutive edition at edition 54 — see the elevated, dedicated
  Standing Facts entry on the vendor-retroactive-revision trap above.**
  Thursday 29 Oct (re-fetched base): gold -0.50% to $4,031.40, silver -2.40%
  to $52.380. Friday 30 Oct: gold -3.29% to $3,898.90 (breaking below
  $4,000), silver -5.93% to $49.276.
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is also a closed thread as of
  edition 45. **US GDP, PCE, import/export prices and industrial
  production:** all closed threads — see Standing Facts above. **University
  of Michigan October consumer sentiment** is a closed thread as of edition
  49. **China's October PMI is now also RESOLVED as of edition 54** — see
  Standing Facts above for the manufacturing (49.3) and non-manufacturing
  (49.7) figures and their sourcing tiers.
- **Henry Hub natural gas:** the front-month-contract-identity question
  remains resolved (NGZ6/December, confirmed again at edition 54 via
  Investing.com's own page header). **The base-price reliability problem
  remains this report's single worst-performing data-quality issue — see the
  dedicated, elevated Standing Facts entry above** for the full
  four-edition escalation. A genuinely independent primary source (CME,
  Barchart, EIA daily) was attempted again at edition 54 and all three
  failed or lagged — try yet another route at edition 55.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 54 again found no notable
  single-stock options-flow/skew commentary** tied to Friday's movers
  (specifically searched around the Alphabet/Amazon/ServiceNow/Intel
  reactions) — a **seventeenth-plus** largely-empty edition on this general
  sub-item. Treat this sub-item as reliably low-yield and keep it a brief,
  secondary effort each edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. **Q3's
  approx. 14 November 2026 deadline falls on a Saturday** — the natural lead
  item for whichever edition covers the following Monday, 16 November 2026
  (a weekend-gap edition), now less than two weeks out.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22, not attempted
  again since). Revisit only if a future edition has spare research
  bandwidth on an FOMC day specifically — not relevant to most editions.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully at
  editions 39, 44-49 and **again at edition 54** (the Friday 30 Oct report,
  covering Tuesday 27 Oct data). Repeat the three-instrument fetch whichever
  edition's window extends past Friday 6 November, 3:30pm ET, watching for
  the micro-vs-full-size naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Not specifically
  re-attempted at edition 54 (out of scope); watch each edition
  independently rather than assuming a trend. Edition 53 separately found
  and explicitly rejected a claimed analyst action (a Barclays "Underweight"
  downgrade on PayPal) that could not be substantiated at all — see the
  dedicated Standing Facts entry above.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** This discipline has now caught: Tesla/NU Holdings
  (ed.49, magnitude), JetBlue (ed.50, magnitude), Carvana/Barron's (ed.52,
  direction/framing), Marvell/Lumentum and Barclays/PayPal (ed.53, claimed
  driver and a likely-fabricated analyst action), and **at edition 54, two
  more exclusions caught BEFORE publication rather than needing a
  post-hoc correction**: a misdated Reuters-style squib and a Trefis list
  dated to the wrong year, both excluded entirely rather than cited.
  Continue this direct-verification discipline on high-confidence-seeming
  figures and claims, not just surprising ones.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted at editions 48 through 54 (out of scope each time); try
  an alternate DOL page or a secondary economic-calendar aggregator for the
  consensus figure at edition 55.
- **federalregister.gov's direct search interface is blocked, logged at
  edition 48, not re-attempted directly since** (edition 54's own light-touch
  check for a new tariff filing found nothing dated to the window, but did
  not re-test the search interface itself): a prior search attempt
  302-redirected to `unblock.federalregister.gov`, an apparent bot/
  rate-limit gate. Note this for any future tariff- or trade-filing search
  attempt rather than re-discovering the same block.
- **SEC EDGAR's `cgi-bin/browse-edgar` company-search page (filtered by CIK
  and form type 8-K) is a highly reliable, fast way to confirm both WHETHER
  a company has reported on a given date and to find the accession number
  for the underlying exhibit** — used successfully again at edition 54 for
  Chevron, Exxon Mobil, AbbVie, Newell Brands and Colgate-Palmolive, each
  cross-checked directly against the company's own Exhibit 99.1 rather than
  a secondary aggregator's figures. This is now the firmly established
  default verification route for any megacap or notable earnings report.
- **Riksbank's primary policy-rate/next-meeting page.** CLOSED at edition 50
  for the current-rate sub-question (held at 1.75%, effective 30 September
  2026), and CLOSED at edition 53 for the next-decision-date sub-question
  (3 Nov meeting, decision published 4 Nov) — **re-confirmed again directly
  at edition 54.** **The current rate VALUE could not be reconfirmed
  directly at edition 54** — riksbank.se's own dedicated rate page 404'd;
  try a different URL path at edition 55. The exact origin date of the
  current 1.75% level (vs. a possible earlier-cycle cut) remains a minor,
  low-priority imprecision.
- **ECB's current policy rate:** reconfirmed directly at edition 54 for a
  SECOND consecutive edition (unchanged through the 28-29 October 2026
  meeting: deposit facility 2.50%, main refi 2.65%, marginal lending 2.90%)
  — one more consecutive clean confirmation would promote this to SETTLED.
  **Its exact Governing Council press-conference content/vote-split remains
  unobtainable** and was not specifically re-attempted at edition 54 (out of
  scope) — low priority. **The Council's own next-meeting date is not yet
  known** — verify directly whenever a window approaches the plausible next
  date (likely mid-December given typical six-weekly cadence), do not
  assume.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel —
  confirmed clean again at edition 54 (fifteen editions total: 37-43,
  45-50, 52-54). For charts with fewer categories, scale the height down:
  roughly `(9.8, 1.65-1.95)` for 3-9 categories. **Edition 54 used
  `(9.8, 1.95)` for a 10-category movers chart with `pad_frac=0.26`**,
  rendering cleanly with no label crowding (largest-to-second-largest ratio
  only approx. 2.7x, well under the 5x capping threshold). **Always render
  and visually inspect (via the Read tool) the actual PNG at or near full
  resolution before embedding it**, regardless of what a past edition's
  success might suggest. **Default to pad_frac=0.30 from the start for an
  11-category sector-ETF panel** — now confirmed across nine straight
  small-magnitude 11-category panels (45-50, 52-54). For any movers chart
  with a double-digit-percent outlier, continue trying pad_frac in the
  0.22-0.30 range from the start.
- **Capped-outlier label-overlap fix (from edition 45):** when a capped
  bar's value label uses a "(capped)" text suffix, the label text can be
  long enough to visually bleed into the y-axis tick-label margin even at a
  wide pad_frac, because matplotlib's `ax.text()` is unclipped by default.
  **Fix: shorten the per-bar suffix to a single trailing asterisk (`"*"`
  instead of `" (capped)"`) and add one footnote to the chart's x-axis label
  instead.** This remains the recommended default for any future
  capped-outlier chart. No edition since 45 has actually needed outlier
  capping (every spread has stayed well under the approx. 5x ratio
  threshold, including edition 54's approx. 2.7x) — reinforcing that the
  trigger is the ratio to the next-largest bar, not the largest bar's
  absolute size.
- **A grouped (two-series) horizontal bar chart — needed for the CFTC
  Asset-Manager-vs-Leveraged-Funds positioning chart — requires custom chart
  code, not the standard single-series `barh()` helper used for the
  movers/sector charts** (first built at edition 44, reused successfully at
  editions 49 and 54). The standard helper only plots one value per
  category; the CFTC chart needs two bars (Asset Manager, Leveraged Funds)
  per category (ES/NQ/RTY), offset vertically by a fixed height fraction
  (`h=0.32` worked cleanly again at edition 54) around each category's tick
  position. **Fix that worked for the legend:** use a FIGURE-level legend
  (`fig.legend(..., loc="lower center", bbox_to_anchor=(0.5, 0.0), ...)`)
  combined with `fig.tight_layout(rect=(0, 0.1, 1, 1))` to reserve the
  bottom 10% of the figure for the legend. Figsize `(9.8, 2.15)` rendered
  cleanly again at edition 54. **Reuse this exact pattern** for any future
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
- **At most ONE forced `page-break-before` in the whole document:
  immediately before Annex A — and on a spillover edition, none at all.**
  Let sections 1-6 flow naturally; never add a break between them. The rule:
    - Sections 1-6 end on page 3 (the common case) → keep the break. The
      annex opens a clean page 4, exactly as before.
    - Sections 1-6 spill onto page 4 → **delete the `pagebreak` div and
      re-render**, so the annex follows the spillover down page 4 instead of
      starting a fifth page. **Edition 54's case** — a stray fourth bullet in
      Section 6's sector-setup list spilled alone onto an otherwise-blank
      page 4 when the break was still present (producing a 5-page draft);
      deleting the break let the annex flow up right after it, converging to
      a clean 4 pages on the very next render with no further trimming
      needed.
    - Still five (or more) pages with the break gone → now trim, in this
      order: sector table rows with no news in the window, the third chart
      if there is one, then prose — and, per edition 53's experience, if the
      specific symptom is "one lonely Annex C entry on an otherwise blank
      extra page," jump to merging several Annex C citation numbers together
      rather than iterating with small per-entry trims.
  Note on the `grep -c 'pagebreak'` self-check: the CSS baseline defines a
  `.pagebreak` class rule AND the body uses one `<div class="pagebreak">` —
  a literal `grep -c 'pagebreak'` therefore normally returns **2** on a
  correctly-built edition (one CSS rule line, one div usage line), not 1.
  The actual check that matters is `grep -c 'class="pagebreak"'` (counts
  only div usages), which should be 1, or 0 on a spillover edition, never 2.
  Always check for content duplication across sections first when a draft
  overflows — it has repeatedly been the cheapest, highest-leverage fix,
  though edition 53 needed genuine trimming instead and edition 54 needed
  only the break deletion.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix.
- **A markup-correctness trap, logged at edition 47: a `<sup class="ref">`
  citation tag placed immediately after a table row's last `</td>` but still
  inside the `<tr>` (i.e. not nested inside any `<td>`) is invalid table
  structure.** `check_refs.py` will NOT catch this. **Always nest every
  `<sup class="ref">` tag inside a `<td>...</td>` pair, never as a sibling of
  one inside a `<tr>`** — grep for `</td><sup` as a quick self-check if a
  table was built with a lot of copy-paste. **Edition 54 actually TRIGGERED
  this trap three times** (empty trailing "Note" cells in the Commodities
  table for EUR/USD, GBP/USD and the three Treasury rows, each originally
  written as `<td></td><sup class="ref">[n]</sup>`) and caught all three via
  a proactive grep before rendering — confirming the trap is real and easy
  to introduce specifically when a table row has an empty trailing cell that
  still needs a citation. Run the grep on every edition with such a table,
  not just when troubleshooting a layout problem.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Edition 53 needed this discipline more than almost any prior edition (see
  the condensed log entry); edition 54's own page-4 orphaned-bullet symptom
  was also only visible by reading the actual page image, not from the page
  count alone (6→5→4 would have looked identical whether the fix was the
  break deletion or something else).

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across many editions'
genuinely different content volumes, including editions 53's and 54's. Treat
as the durable default; the lever to pull on a high-volume or overflowing
day is first checking for duplicated content across sections, then
merging/trimming redundant content across whichever sections (or Annex C
citations) are longest — not loosening the CSS further.)
- Letter size. Body **8.0pt** / line-height **1.20**, serif; `p`
  margin-bottom **1.6px**.
- h1 14.5pt; h2 **9.1pt, margin 3px 0 1.2px 0, padding-bottom 0.6px**; h3
  **7.9pt, margin 1.8px 0 0.8px 0**.
- Tables **7.4pt**, **1.0px cell padding**, table margin-bottom **2px**.
- Snap-grid tiles: 7.4pt label / 9.4pt value / 7.3pt change; tile padding
  **2px 4px**, snapgrid margin-bottom **3.5px**.
- Bullet lists (`ul.bullets`): **1.0px** margin-bottom per `li`.
- Annex A: two columns at 7.1pt, same treatment as Annex B below.
- Annex B: two columns at 7.1pt, `break-inside:avoid` per `li` (left-aligned).
- Annex C: three columns at 5.5pt, left-aligned.
- Content budget: 60-second read (5 items); equities as the largest block
  plus the movers table; macro/commodities/derivatives tighter; **a "This
  week's known catalysts" table plus a "Sector setup we take into [session]"
  bullet list at the end of Section 6 by default** for any single-session or
  weekend-window edition. **An optional "Commodities & FX levels" table
  (~9-13 rows)** at the end of Section 4 is available as padding if page 3
  runs short — editions 44 through 54 have all folded commodities, FX and
  Treasuries into ONE combined table (10-14 rows; edition 54 used 13) as the
  PRIMARY commodities table rather than padding, now the standing default.
  **Always re-render immediately after adding (or removing) any content to
  confirm the page count.**

**Chart selection guidance.** Placement is not editorial for the first two
charts:

- **Sector-ETF performance chart → Section 1 (Market recap), every
  edition.** Same-day closes by default; a grouped day-over-day bar instead
  on a multi-session or weekend window, or on a genuine multi-sector
  broadening selloff across consecutive sessions. **Edition 54 used a
  single-day bar** (only one NYSE session fell inside its window despite
  being a weekend-gap, Monday-dated edition).
- **Single-stock movers bar → Section 2 (Equities), every edition.**
- **A third chart only when positioning or volatility is genuinely the
  day's dominant story**, never to fill a page, placed in the section it
  belongs to:
  - Fresh CFTC CoT data → the ES/NQ/RTY asset-manager-vs-leveraged-funds
    positioning chart, normalized as % of open interest, built with the
    grouped-bar technique documented under Production notes, in **Section
    5**. Editions 24, 34, 39, 44, 49 and 54 have all placed it there.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully.
  - A holiday-window preview edition with no fresher data → VIX futures
    term structure with event annotations, in **Section 5**.

**Edition 55 (expected to cover Monday 2 November 2026, assuming no gap) has
a lighter but still real macro-calendar load.** Watch directly rather than
assuming: **Apple's fiscal Q4 2026 earnings** (shifted to Monday 2 Nov per
secondary sourcing only — confirm against Apple's own IR calendar when
checking the reaction); **the RBA's 2-3 November decision** (very likely
lands just after edition 55's own cutoff, inside the edition after it
instead — don't assume it's simply missed, watch the precise timing); and
continuing follow-up on the **Binance-hack fallout** (regulatory response,
fund-recovery updates, continued reaction in Coinbase/Strategy and other
crypto-adjacent names). It should also retry: a genuinely different Henry
Hub primary source; a different DXY true-spot route (Yahoo Finance / Trading
Economics / a wire FX report, not ICE/MarketWatch a third time); BoJ's own
meeting-calendar page for its next decision date; riksbank.se's dedicated
rate page via an alternate URL; SNB's decisions/schedule page via an
alternate URL; and banxico.org.mx via an alternate path. The
international-AP-mirror wire-gap workaround (lanacion.com.ar-style
syndication) is worth trying first before the Yahoo/Investrade fallback, and
the Polymarket Gamma-API approach is worth trying first before a plain site
visit.

**Remember the figsize-scales-to-category-count guidance above
(ceiling `(9.8, 1.95)` for an 11-category panel, `(9.8, 2.15)` for the
3-category grouped CFTC chart, scale down for fewer single-series
categories), that an 11-category sector-ETF panel should default to
pad_frac=0.30 from the start (now confirmed across nine editions, including
54), a movers chart with a double-digit-percent outlier should try pad_frac
in the 0.22-0.30 range from the start (edition 54 used 0.26 for a
10-category panel with a -28.6% outlier), and the capped-outlier asterisk/
footnote fix when a spread crosses the approx. 5x RATIO threshold** (it has
not since edition 45; edition 54's largest-to-second-largest ratio was
approx. 2.7x).

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

**Edition 54's carried-forward spec was 112,802 bytes, over the 100,000-byte
threshold — this run folded edition 52 into the mega-block and condensed
edition 53 to a medium paragraph, per the log's own standard rotation, as
part of producing this file.** There is no maximum size; condensing is
housekeeping done by the run itself, not a check to pass — there is no
penalty for the file staying somewhat large if the alternative is losing
information.

**Editions 1–52 (condensed):** established the format (edition 1 baseline;
edition 2 revised weighting/sourcing; edition 3 fixed the ET-cutoff math);
corrected the Fed Chair premise to Kevin Warsh at edition 6 (re-verified
every edition since, now settled); tracked the Jackson Hole keynote (28 Aug,
hawkish) and the resulting rate-odds repricing through editions 10–18;
resolved the SPDR-sector-ETF-proxy and CBOE-feed sourcing techniques at
editions 10–11; corrected the FOMC decision date to Wednesday 16 Sept at
edition 18. Major single-name events across editions 1-21: Moderna's
melanoma-data spike/unwind, Nvidia's Q2 FY27 beat/Hugging Face acquisition,
Walmart/Advance Auto Parts/Deere earnings, the PayPal-Stripe deal collapse,
California SB 492 hitting utilities, an Iran/Hormuz escalation cycle
repeatedly driving oil, Lululemon's guidance-slash collapse, Canada's approx.
$27.6bn retaliatory tariffs, Apple's first Ternus-era product event, Oracle's
Q1 FY27 vol-crush beat, the Fed debate flipping from "hold vs. cut" to "hold
vs. hike" on hot core CPI, and Anthropic CEO Dario Amodei's AI-safety essay
driving a chip-selloff/cybersecurity rotation. **The Sept 15-16 FOMC meeting
and its aftermath (editions 21-23):** the Fed hiked 25bp to 3.75%-4.00%
unanimous 12-0; BoE held at 3.75% (6-3). Edition 24: approx. $7tn September
triple-witching, Xenon Pharmaceuticals -30.7%, Buffett stepped down as
Berkshire chairman, BoJ hiked to approx. 1.25%. Edition 25: chip rally to a
then-record Nasdaq. Edition 26: financials-led rotation, a Kitco-vs-USAGOLD
gold split (later resolved). Edition 27: risk-off on a 19-year 10-year yield
high. Edition 28: MGM -10.99% on a withdrawn take-private bid, Trump-Xi
summit extended the US-China trade truce. Edition 29: the US-China $30bn
tariff-cut agreement first reported. Edition 30: Iran Hormuz offer rejection
drove risk-off, Kodiak Sciences +177.96% (the movers-chart capping rule's
first case). Edition 31: DXY-vs-FX-crosses conflict resolved cleanly.
Edition 32: a volatile round-trip close, gold spot/futures split (later
converged). Edition 33: a hot ISM Prices Paid print, Nike missed FQ1
guidance (resolved edition 34); overflowed to 5 pages, five trim rounds.
Edition 34 (Mon 5 Oct): a badly-missed September jobs report drove a broad
risk-on rally; a fresh CFTC CoT report powered the first positioning chart.
Edition 35 (Tue 6 Oct): two same-day cash buyouts (PTC, RXO) drove the tape;
Nasdaq Composite record; September ISM Services PMI printed hot. Edition 36
(Wed 7 Oct): records extended on falling yields; fabricated AMD price
targets and an unverifiable WHO claim both rejected; Paramount Skydance/
Warner Bros. Discovery merger closed (SKYD); the 2-year Treasury hit a 33bp
gap (resolved ed.37); GBP/USD hit a three-way conflict (resolved ed.37).
Edition 37 (Thu 8 Oct): FOMC minutes showed unanimous 12-0 hike but only
"most" backing a further 2026 move; equities retreated on a bond selloff.
Edition 38 (Fri 9 Oct): a second straight decline but strong breadth;
Applied Digital's blowout drew a muted reaction, first non-GAAP/GAAP EPS
conflict logged; a primary-source breakthrough closed BoJ's last gap.
Edition 39 (Mon 12 Oct): SpaceX's approx. $8bn spectrum purchase rattled
telecom but equities shrugged it off, a record week; Goldman upgraded
Palantir; deliberate CSS retightening fixed a genuine 5-page overflow.
Edition 40 (Tue 13 Oct, Columbus Day): a value/growth split on memory-chip
weakness; oil's cleanest-ever dual-grade reconciliation later found to rest
on a revised base. Edition 41 (Wed 14 Oct): JPMorgan/Goldman/Wells Fargo/
Citigroup/UnitedHealth/J&J all reported; JNJ's GAAP EPS collapsed to $0.09
on a one-time talc charge; Bumble's +56.58% surfaced (resolved ed.42: a
$1.3bn Ithaca Holdings buyout); first vendor-retroactive-revision trap hit
WTI/Brent/Henry Hub. Edition 42 (Thu 15 Oct): September CPI printed hot,
triggering the broadest risk-off session in weeks; CoreWeave/Oracle led
decliners on AI-infra-funding-stress; rate-path odds repriced sharply
hawkish. Edition 43 (Fri 16 Oct): a second straight blowout inflation print
(PPI) barely moved Fed odds; an overnight memory-chip rout reversed sharply
on Nvidia CEO Jensen Huang's CoreWeave defense; Ericsson's beat drove
+11.80%, the session's largest move. Edition 44 (Mon 19 Oct): equities fell
broadly Friday on renewed AI-infra doubts (Nasdaq -2.14%, worst week since
June); VIX complex spiked with both CBOE feed bugs appearing simultaneously;
a FreightWaves "+12%" J.B. Hunt headline was flatly wrong; CFTC CoT powered
the first grouped-bar positioning chart; first draft overflowed to 5 pages,
five trim rounds. Edition 45 (Tue 20 Oct): equities rebounded on narrow
breadth; biotech produced extremes (Silence Therapeutics +125.58%, EyePoint
-85.28%); the chart's first outlier-capping use surfaced a label-overlap
bug (fixed via asterisk+footnote); China's Q3 GDP release-date dispute
resolved. Edition 46 (Wed 21 Oct): a sharp rotation reversal (10 of 11
sectors green); Salesforce's $47.50/share Braze buyout (BRZE +51.70%),
Equifax (+11.33%, an unexplained-magnitude thread) and Hasbro (+11.20%) led
gainers; GM fell 6.84% despite a beat and buyback. Edition 47 (Thu 22 Oct):
equities extended a rally a second session; Netflix/AT&T(-6.45%, disputed)/
United/Capital One/CME/Abbott/Danaher/Thermo Fisher/Elevance around
Tuesday-close/Wednesday-open, then Meta/Tesla/IBM/Texas Instruments after
Wednesday's close; New Mexico's Judge Mathew ruled Meta owes $25bn; USTR's
Greer statement closed the tariff-implementation sub-question; 5-page
overflow fixed from one duplicated paragraph. Edition 48 (Fri 23 Oct): a
tech-led rotation not a broad selloff, Meta -6.98% post-earnings; AP/Reuters
wire gap began; westmetall.com went down on an expired certificate (later
resolved transient). Edition 49 (Mon 26 Oct): a modest narrow risk-off
session, second straight no-wire edition. Edition 50 (Tue 27 Oct): a broad
risk-on reversal (8 of 11 sectors higher); Surgery Partners +47.62% and
Range Resources +17.66% on confirmed M&A; BoJ's numeric rate, Riksbank's
rate and RBA's current rate all closed at once; the largest-yet Brent
vendor-revision trap hit ($116.72 vs. $111.70); the first genuine 5-page
overflow fixed via the new spillover mechanism. Edition 51 (Wed 28 Oct,
covering Tue 27 Oct, reconstructed by hand after the then-current
120,000-byte spec ceiling rejected and discarded the run's own update — the
ceiling has since been removed): a third straight up session on narrow
breadth (S&P +0.60% to 7,722.60, Nasdaq to a fresh high of 26,477.81, only 5
of 11 sectors green), AP's recovered wire saying "most S&P 500 stocks fell"
even as the index rose on a handful of megacaps; a dense pre-FOMC earnings
morning broke the beat/reaction logic repeatedly (Boeing -10.69% on a miss,
JetBlue +18.99% despite missing); Brent's Friday 23 Oct close became a
three-way split ($116.72/$111.70/$113.17), still unresolved. Edition 52
(Thu 29 Oct, covering Wed 28 Oct FOMC day): the Fed held at 3.75%-4.00% on a
10-2 hawkish dissent (Cook, Hammack) — the report's first-ever dissent; the
Bank of Canada delivered the bigger surprise with a genuine 25bp hike to
2.50%. Equities notched a fourth straight up session on narrow leadership
(S&P +0.28%, 6 of 11 sectors higher); Microsoft beat and rose, Alphabet's
GAAP EPS fell on a one-time mark-to-market loss (shares approx. -10% AH),
Fortinet beat-and-raised yet fell 5.90%, Carvana's clean beat was wrongly
headlined a "miss" by Barron's (corrected against the 8-K). Smaller movers:
F5 -20.4%, Enphase -16.0%, Vertiv +16.5%, SK Hynix +13.3%, Oracle +10.6%,
Wendy's +15.1% (Trian take-private proposal). Vol priced the decision as a
non-event (VIX -3.48% to 16.91, clean contango) — no third chart. First
draft spilled onto page 4 (expected given the day's density), fixed via the
spillover rule, converging on the first re-render. 26 sources, clean after
adding five missing inline citations.

**Edition 53 (condensed)** — Friday 30 October 2026 report covering
Thursday 29 October 2026. Q3 GDP (+3.4%) and September core PCE (+3.1% y/y)
both printed hot the same session the market largely shrugged off;
December hike odds eased slightly despite it, and the DeFi Rate aggregator's
internal decision-vs-rate-level inconsistency persisted a seventh straight
edition. Alphabet lost approx. $500bn of market value in a single session
(-12.64%), extending Wednesday's AH mark-to-market-loss reaction even as
Search and Cloud both beat, dragging Communication Services to the day's
sector laggard even as 9 of 11 sectors closed higher. Amazon's Q3 was a
"double miss on the surface" (EPS missed on a prior-year comp effect)
masking real AWS/margin strength (shares -4.25% regular, -7.30% AH).
"Beat-and-raise guarantees nothing" produced its largest cases yet:
ServiceNow -26.95%, Intel -23.04% AH, Caterpillar -9.25%, all on clean
beats; Mastercard/Eli Lilly/Merck/Crocs beat and rose the same session.
Smaller movers: Xerox -40.32%, Glaukos +33.65%, ADT +33.20%, Marvell -13.24%
(a claimed Lumentum-acquisition-talks driver found unsubstantiated), Carvana
+15.68%. The vendor-retroactive-revision trap hit gold/silver a second
straight edition and Henry Hub a third, the latter now this report's
worst-performing series. A claimed Barclays PayPal downgrade was
investigated and found fabricated, dropped entirely. The ECB held as
expected (not yet promotable to settled); the BoJ's Oct 29-30 decision had
not posted by cutoff, carried to edition 54 as live; Riksbank's
next-decision date resolved directly. First draft ran a genuine 6 pages;
converged to 4 after deleting the forced break and a dozen rounds of
trimming/citation-merging (54 sources to 41), surfacing a new CSS
multi-column pagination lesson (documented in Standing Facts above).

**Edition 54 (most recent — full detail)** — Monday 2 November 2026 report
covering Friday 30 October 2026, research window Thu 29 Oct 2026 20:00 ET
through Sun 1 Nov 2026 20:21 ET (the window's one NYSE session; a
weekend-gap, Monday-dated edition — no genuinely new weekend-specific
corporate news was found despite a dedicated search).

**A tech-led selloff dropped the major indices broadly** — S&P 500 -1.82% to
7,580.07 (worst session since June 2026), Nasdaq Composite -2.86% to
25,437.00 (Nasdaq-100 reportedly dipped into correction territory
intraday), Dow -1.09% to 51,770.31, Russell 2000 -1.66% to 2,811.84 — on
only 5 of 11 sectors falling, Technology (XLK -4.89%) by far the worst,
dragged by **Intel's -28.58% collapse to $65.76, its worst day since
1974**, on a Q4 profit guide below Street despite beating Q3 revenue/EPS,
and Nvidia (-4.22%), named the single largest index-point drag. Neither
AP's nor Reuters' own wire page was directly located for Friday; a new
workaround (an AP-wire mirror syndicated through lanacion.com.ar) cross-
checked cleanly against two independent secondary sources and ETF proxies.

**A record crypto heist roiled crypto-adjacent equities**: approx. $6.3bn
was stolen from Binance overnight Thursday into Friday (the largest
exchange hack on record, reportedly tied to North Korea's "TraderTraitor"
group per blockchain-analytics firms, not an official government
attribution); Bitcoin fell below $77,000, Coinbase fell 10.62% (its own Q3
GAAP profit was almost entirely crypto mark-to-market gains, adjusted
income far smaller) and Strategy (MicroStrategy) fell 7.84% (also citing a
CFO resignation).

**Two long-running Asia macro threads resolved the same session.** The Bank
of Japan held its policy rate at approx. 1.25% at its 29-30 October meeting
on an 8-1 vote — dissenter Takata Hajime wanted a hike to 1.5%, while
September's two dissenters both voted for hold this time — confirmed
directly against boj.or.jp's own statement PDF, closing the live question
edition 53 carried forward. China's October PMI slipped back below 50 on
both gauges (manufacturing 49.3, non-manufacturing 49.7), reversing
September's above-50 readings. Separately, the whitehouse.gov funding-status
URL reconfirmed cleanly after failing to at edition 53 (funding through 11
December 2026, no shutdown), and the November monthly settled-facts audit
was completed with no contradictions bar two sourcing-tier notes (Riksbank's
rate value, Banxico, both secondary-sourced only this edition).

**Four previously-pending earnings reports (Chevron, Exxon Mobil, AbbVie,
Newell Brands) all beat and rose Friday**, each confirmed directly against
its own SEC 8-K Exhibit 99.1, helping Energy (XLE +1.91%) lead sector
gainers as oil rose alongside (WTI +2.08%, Brent +2.40%). Smaller movers:
Mondelez +3.85%, Colgate-Palmolive +2.29%. A fresh CFTC CoT report (covering
Tuesday 27 October, posted on schedule Friday) powered the edition's third
chart — asset managers remain net long all three index-futures contracts,
most heavily ES (+47.2% of OI); leveraged funds net short ES and RTY but
roughly flat on NQ. The VIX complex jumped sharply (VIX +12.91% to 19.42,
VIX9D +21.30%) but stayed in clean contango throughout, both known CBOE
feed bugs present on all six series this edition. The gold/silver
vendor-revision trap continued a fourth consecutive edition; Henry Hub
remained single-sourced and unresolved for a fourth consecutive edition
despite fresh attempts at CME, Barchart and EIA. LME copper's Thursday base
was carried forward from edition 53's own log (a new, reusable sourcing
technique) after westmetall.com's live page exposed only Friday's own row.

**Format:** no correction box (nothing from a prior edition found wrong).
First draft ran 5 pages — a single orphaned fourth bullet in Section 6's
sector-setup list spilled alone onto an otherwise-blank page 4 with the
forced break still in place; deleting the break converged to a clean 4
pages on the very next render, with no further trimming needed. A
proactive `grep -n '</td><sup'` caught and fixed three instances of the
table markup-correctness trap before rendering (empty trailing "Note" cells
in the Commodities table). 44/44 sources clean on `check_refs.py` after one
fix (an image-only citation needed an inline body citation added too); zero
stray tildes.

**Open threads for edition 55.** Edition 55 covers **Monday 2 November
2026** (assuming no gap). Watch directly rather than assuming: **Apple's
fiscal Q4 2026 earnings** (shifted to Monday 2 Nov per secondary sourcing
only); **the RBA's 2-3 November decision** (very likely lands just after
edition 55's own cutoff, inside the edition after it instead); and
continuing **Binance-hack fallout** (regulatory response, fund-recovery
updates, continued reaction in crypto-adjacent names). Retry at edition 55:
a genuinely different Henry Hub primary source; a different DXY true-spot
route (not ICE/MarketWatch a third time); BoJ's own meeting-calendar page
for its next decision date; riksbank.se's dedicated rate page via an
alternate URL; SNB's decisions/schedule page via an alternate URL;
banxico.org.mx via an alternate path. Use the international-AP-mirror
wire-gap workaround and the Polymarket Gamma-API approach first, before
their respective fallbacks.

**Still open and unchanged:** Brent crude's Friday 23 October close remains
a three-way split ($116.72/$111.70/$113.17), not re-attempted since edition
53; the ECB's next-meeting date (unconfirmed, estimated mid-December by
cadence); the ECB's press-conference-content/vote-split sub-question (404,
not re-attempted at 54); Equifax's unexplained multi-session pullback
(declining urgency, one dead-end lead now ruled out); New Mexico v. Meta's
formal notice of appeal (unconfirmed for a ninth straight edition); the
"preview-consensus-only miss/beat framing" caution (dormant since edition
41); the DOL weekly jobless-claims parsing problem (not re-attempted); the
federalregister.gov search-interface block (not re-tested). Options
implied-vs-realized and single-stock flow/skew remain low-yield, now a
seventeenth-plus largely-empty edition on that sub-item.

**Dates to hold on to.** 13F filings are due approx. 14 November 2026 (a
Saturday) — the natural lead item for whichever edition covers the
following Monday, 16 November 2026, now less than two weeks out. Veterans
Day (Wednesday 11 November) needs the same "equities-open, bonds-closed"
check Columbus Day received, once it is inside a window. The next monthly
settled-facts audit falls on the first edition of December 2026.
