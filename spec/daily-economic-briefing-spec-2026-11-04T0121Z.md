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
  applied correctly for thirty-four straight editions (33 through 56) — treat
  as settled; edition 56 read "Wednesday 4 November 2026" as the date line,
  covering the Tuesday 3 November session in the window line.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 56 all reused the
  same pattern — now confirmed clean across twenty-eight consecutive editions;
  edition 56 phrased it "Window: Mon 2 Nov 2026 20:00 ET – Tue 3 Nov 2026
  20:21 ET (Tue 3 Nov close/AH, the window's one NYSE session)." No further
  confirmation needed; treat this as settled.

## Schedule
Run every weekday. Pick the trigger's local time so the effective research
cutoff lands roughly 4 hours after the US market close (20:15 ET) — during
US daylight time that's 00:00 UTC; adjust for standard time. **US daylight
time ended Sunday 1 November 2026, as scheduled — now a resolved, settled
transition, not a forward-looking watch item.** Edition 54's own window closed
at 2026-11-01 20:21 ET, which converts to 2026-11-02 01:21 UTC — consistent
with EST (UTC-5) already being in effect; edition 55's and edition 56's window
closes (2026-11-02 20:21 ET → 2026-11-03 01:21 UTC, and 2026-11-03 20:21 ET →
2026-11-04 01:21 UTC) both confirm the same conversion again. **From edition
54 onward, use EST (UTC-5) for all ET/UTC conversions** until DST resumes —
conventionally the second Sunday in March (expected March 2027; this specific
future date is a general calendar convention, not yet independently verified,
so don't cite it as a confirmed fact until closer to the event). On Mondays
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
reported still surfaces within weeks rather than never. **The November 2026
monthly audit was completed at edition 54** (the first edition of November) —
all ten central-bank rows in Section 3 were reconfirmed directly against
their own primary sources, with no contradictions, except Riksbank's rate
value (page 404'd, only its next-decision date is primary-sourced) and
Banxico (site unreachable, secondary-sourced only) — both remained flagged as
such through edition 56 (neither resolved across editions 54-56). **The next
monthly audit falls on the first edition of December 2026** — whichever
edition covers the first NYSE session on or after 1 December 2026; no
specific edition number is estimated this far out given holidays and
potential gaps.

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
  edition 53 and were not re-attempted at editions 54, 55 or 56 — stale news
  now, not worth a dedicated search. Blackout (Oct 17-29, 2026) held clean
  through the decision, as expected. **Next meeting: 8-9 December 2026, an SEP
  meeting.**
- **Rate-path odds at edition 56 (direct Polymarket Gamma-API pull plus
  DeFi Rate's Kalshi/Polymarket-blended aggregator, snapshot Tue 3 Nov 2026
  approx. 7:30-8:24pm ET):** December 8-9 odds firmed further to **approx.
  74-75% hike** (approx. 23-24% hold, cut near zero) — up from approx. 72-73%
  hike at edition 55 and approx. 70% at edition 54, a third straight edition of
  hardening hike odds. The Gamma-API approach
  (`gamma-api.polymarket.com/public-search`) worked cleanly for a **third
  consecutive edition** — remains the preferred route over the plain
  Polymarket site. DeFi Rate's own internal inconsistency between its Kalshi
  decision-table hike contract and its separate Kalshi rate-level contract
  persisted a **TENTH straight edition (47-56)** but stayed narrow (approx.
  2-3 points, consistent with edition 55's narrowing) — keep disclosing both
  rather than picking one. **Kalshi's own direct fetch failed again at edition
  56 — HTTP 429 (rate-limited) again — now TWENTY consecutive failures
  (37-56).** CME FedWatch also failed again directly (timeout), a
  **SIXTEENTH** consecutive failure (41-56). The composite "at least one more
  hike in 2026" read has still not been freshly re-pulled since edition 38
  (last known approx. 80%) — don't cite without a fresh pull.
- **US-China "30-for-30" tariff framework — remains a closed thread, do not
  re-open absent a genuine dated Federal Register filing.** Resolved at
  edition 37 (framework) and edition 47 (implementation-notice sub-question:
  no effective date, no set timeline, none imminent). No new development was
  found at editions 54, 55 or 56 either (light-touch checks only); the
  federalregister.gov search-interface block (302-redirect to
  `unblock.federalregister.gov`, logged at edition 48) was not re-tested at
  edition 56 either — log as a standing access obstacle. Separately: secondary
  reporting (a Thomson Reuters regulatory-insight piece) describes a Busan
  truce extension to **10 January 2027**, but this remains **NOT confirmed via
  any published Federal Register notice** as of edition 56 — treat the January
  2027 date as reported-not-verified, not settled law, if cited. A reciprocal-
  tariff suspension and Section 301 exclusions for 178 Chinese products are
  reported (secondary sourcing only) to run to **approx. 9-10 November 2026**
  (a one-day split persists across secondary sources — one law-firm bulletin
  says 9 Nov, another says "through November 10"), with no Federal Register
  extension filed as of edition 56's check either — this falls inside the
  very next edition's plausible window; check directly once a window reaches
  that date.
- **Fed Chair: Kevin Warsh — SETTLED, stop re-verifying it every run.** No
  contradiction surfaced through edition 56; **directly re-confirmed via
  federalreserve.gov's own bios page at edition 54's November monthly
  audit**, closing that housekeeping item cleanly; not re-attempted at
  editions 55 or 56 (settled, no fetch needed). His Chairman term ends 21 May
  2030 (took office 22 May 2026, a four-year term); his separate term as a
  Board of Governors member runs to 31 January 2040. The Chairmanship
  re-opens as a live fact only on a successor nominated/confirmed, a
  resignation or removal, or that 21 May 2030 term-end date actually arriving,
  or the **next monthly audit (first edition of December 2026)**.
- General principle for everything still live: do not assume a routine
  macro-calendar fact (meeting dates, symposium schedules, other central
  banks' policy rates, government funding status) from memory or from the
  prompt's own framing — verify it fresh from a primary source
  (federalreserve.gov, bankofengland.co.uk, boj.or.jp, kansascityfed.org,
  norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, rba.gov.au,
  ecb.europa.eu, bankofcanada.ca, whitehouse.gov, etc.) every edition, exactly
  like any other data point, until an entry below is marked SETTLED. These
  are the rates and dates that feed Section 3's policy-rate table, so the
  table is the natural place to land them. Per-bank status as of edition 56:
  - **Reserve Bank of Australia:** **current rate changed this edition —
    hiked 25bp to 4.85% on Tuesday 3 November 2026**, confirmed directly
    against rba.gov.au's own Statement by the Monetary Policy Board (Media
    Release 2026-30). This is the RBA's FIFTH hike of 2026 (not fourth as the
    prior 4.60% level implied) and, notably, the **first split vote this
    cycle: 6-3**, with three members preferring a hold at 4.60% — the prior
    four 2026 hikes were all unanimous. **Next decision date not confirmed
    this edition** — Annex B item, try rba.gov.au's own published 2026/2027
    meeting calendar directly at edition 57.
  - **Bank of England:** current rate 3.75%, SETTLED (see dedicated bullet
    below). **Next decision Thursday 5 November 2026 — now directly
    reconfirmed against bankofengland.co.uk's own "Upcoming MPC dates" page
    at edition 56**, upgraded from edition 55's secondary-only corroboration
    (financecalendar.com, ebc.com, cambridgecurrencies.com). The 17 Sept
    decision's 6-3 vote detail remains sourced only via consistent secondary
    corroboration (BoE's own page doesn't restate historical vote splits) — a
    sourcing-tier note, not a concern. The decision itself lands inside
    edition 58 (Thu 5 Nov session, on a daily cadence from edition 56:
    57=Wed 4 Nov, 58=Thu 5 Nov) — watch for the actual outcome there rather
    than assuming a hold.
  - **European Central Bank:** rate complex (deposit facility 2.50%, main
    refi 2.65%, marginal lending 2.90%) remains **SETTLED** (promoted at
    edition 55 after a third consecutive direct reconfirmation) — not
    re-attempted at edition 56 (no fetch needed). It reopens on contradiction,
    the next Governing Council decision, or the monthly audit. The
    press-conference-content/vote-split sub-question and the exact
    next-meeting date both remain unconfirmed/unreachable (not re-attempted
    at edition 56, out of scope) — still estimated mid-December by typical
    six-weekly cadence, not verified; this remains the ECB's one outstanding
    live sub-question, worth a dedicated check once a window approaches that
    date.
  - **Bank of Japan:** current rate approx. 1.25%, SETTLED pending its own
    next meeting (see dedicated bullet below). Next decision 17-18 December
    2026, confirmed directly against boj.or.jp at edition 55 — not
    re-attempted at edition 56 (no fetch needed, date stands).
  - **Bank of Canada:** SETTLED — see dedicated bullet below. Next decision 9
    December 2026 (same date as the Fed's).
  - **Swiss National Bank:** current rate 0.00%, SETTLED (effective, most
    recent assessment 24 Sept 2026). Next assessment 10 December 2026,
    confirmed directly against snb.ch at edition 55 — not re-attempted at
    edition 56 (no fetch needed, date stands).
  - **Norges Bank:** current rate 4.50% (unchanged since 24 Sept 2026), next
    decision 17 December 2026 — both SETTLED, reconfirmed directly at edition
    54's monthly audit; next re-verification due at the December monthly
    audit.
  - **Riksbank:** next-decision date RESOLVED and SETTLED (Wednesday 4
    November 2026 meeting/decision, approx. 9:30 CET — lands inside edition
    57's window, near its start). **The CURRENT RATE VALUE (approx. 1.75%)
    could not be reconfirmed directly for a THIRD straight edition (54-56)**
    — riksbank.se's dedicated rate page 404'd again at edition 56 on multiple
    URL patterns (`/en-gb/monetary-policy/the-policy-rate/`,
    `/en-gb/monetary-policy/the-repo-rate-table/`); a calendar-page fetch
    returned only nav chrome, no rate data. The value remains corroborated
    only by consistent secondary sourcing (Continuum Economics, MNI Markets,
    financecalendar.com), which also converges on the rate being unchanged
    since a prior-cycle cut, last confirmed held 26 Aug 2026 per one secondary
    source — a detail that sits awkwardly against this report's own earlier
    note that the 1.75% level took effect 30 September 2026; both readings
    describe "held, unchanged" rather than a fresh move, so this is most
    likely just imprecision about which of several 2026 hold decisions is
    "the" effective date, not a contradiction requiring urgent resolution —
    flagged as a standing low-priority imprecision, not re-chased this
    edition. Try yet another riksbank.se URL path at edition 57, which will
    also be the edition that covers this Wednesday's actual decision outcome.
  - **Banxico:** current rate approx. 6.50% and next-decision date both
    remain unconfirmed directly for a further edition — banxico.org.mx and
    its anterior.banxico.org.mx mirror both failed again at edition 56 on
    three different URL paths (tasas-de-interes redirect 404'd; indicadores
    redirect timed out; decisiones-de-politica-monetaria redirect 404'd); the
    rate remains corroborated only by consistent secondary sourcing (Zeta
    Tijuana, Ámbito). **New secondary detail found at edition 56:** a
    secondary minutes-list snippet shows 2026 decision dates of 5 Feb, 26 Mar,
    7 May, 25 Jun and 6 Aug, with no Sept/Oct/Nov entries visible — consistent
    with the rate having last moved (a 25bp cut, "closing the easing cycle")
    around **7 May 2026**, then held at subsequent meetings through at least
    6 Aug. This refines, but does not primary-source-confirm, the "last
    change" cell. A speculative, UNCONFIRMED analyst note (Finamex/Bankaool)
    continues to float a possible decision around 5 November 2026 with a
    25bp-cut call — still not corroborated anywhere else and not reported as
    fact; watch directly rather than assuming either the date or the outcome.
    Try the English-language IR site or a press-release index at edition 57.
  - **Government funding/shutdown status:** H.R. 6500 funds federal agencies
    through 11 December 2026, no shutdown in effect — reconfirmed directly
    against whitehouse.gov at edition 56 for a third straight clean edition.
    Continue the standard re-check-every-edition discipline.
- **SETTLED — Bank of England held at 3.75% on Thursday 17 Sept 2026, a 6-3
  vote** (same three dissenters as 30 July, all favoring a hike to 4.00%) —
  resolved, does not need re-confirming again unless a new decision date has
  passed. **Next BoE decision: Thursday 5 November 2026** — now directly
  primary-confirmed; see the dedicated per-bank bullet above.
- **SETTLED (the September decision only) — Bank of Japan hiked 25bp to
  approx. 1.25% on 18 September 2026** (effective 24 Sept), a 31-year high, a
  7-2 vote (dissenters Asada Toichiro and Sato Ayano) — closed thread, do not
  re-derive. **The Bank's SUBSEQUENT 29-30 October 2026 meeting HELD the rate
  at approx. 1.25% (8-1 vote, dissenter Takata Hajime)** — see the dedicated
  per-bank bullet above for full detail; this October decision is now itself
  resolved meeting history and the numeric rate is live again only pending
  BoJ's next meeting, confirmed for **17-18 December 2026**.
- **SETTLED — the four-central-bank Thursday 24 September 2026 cluster,
  closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% but signalled a greater chance of
  a Q4 hike; Banxico held at 6.50% unanimously; SNB held at 0% and raised its
  inflation forecasts, confirmed directly against snb.ch.
- **SETTLED — the Reserve Bank of Australia's Tuesday 29 September 2026
  decision, closed thread, do not re-open:** hiked 25bp to 4.60%, unanimous,
  a 15-year high and its fourth hike of 2026, confirmed directly against
  rba.gov.au. **SETTLED — the RBA's Tuesday 3 November 2026 decision, also
  now closed thread, do not re-open:** hiked a further 25bp to 4.85%, its
  fifth hike of 2026, this time on a split 6-3 vote (first split vote this
  cycle), confirmed directly against rba.gov.au's Media Release 2026-30 at
  edition 56. The current numeric rate is live again only pending the RBA's
  next decision, date not yet confirmed (Annex B item).
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
  Situation Summary. **October's employment report is expected Friday 6
  November 2026** (if on the normal schedule) — not yet confirmed, consensus
  not yet available (Annex B item, carried since edition 55, not independently
  re-attempted at edition 56 — out of scope this close to the date, will be
  directly checked whichever edition's window includes Friday 6 Nov, likely
  edition 59).
- **September 2026 ISM Services/Non-Manufacturing PMI — closed thread as of
  edition 35, do not re-derive:** headline 54.9% (down from August's 55.4%),
  Prices Paid 74.0% (+1.4pt, highest since July 2022). Confirmed directly
  against ISM's own press release. **October's ISM Services PMI is expected
  Wednesday 4 November 2026** — this falls inside edition 57's window; a
  consensus figure for the October read could not be found at edition 56
  (Annex B item) — try again at edition 57 once closer to the release.
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
- **No US federal government shutdown is in effect — directly reconfirmed
  again at edition 56 via whitehouse.gov**, a third straight clean
  confirmation. H.R. 6500 funds federal agencies through **11 December 2026**.
  Watch for shutdown risk resurfacing as that date approaches.
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
  English-language NBS-attributed news release. **China's October 2026 PMI**
  (resolved at edition 54): manufacturing PMI **49.3** (down from September's
  50.1, a third contraction in four months) and non-manufacturing PMI **49.7**
  (down from 50.2) — both back below the 50 expansion/contraction threshold,
  reversing September's above-50 readings. The non-manufacturing figure is
  sourced directly to Xinhua's English wire; the manufacturing figure rests on
  Reuters-sourced wire coverage (stats.gov.cn's own English-language PMI
  release had not posted at the time of the edition-54 fetch) — upgrade the
  manufacturing figure's sourcing tier if a direct stats.gov.cn fetch
  succeeds at a future edition, though low priority now that the headline
  figures are corroborated and the thread is otherwise closed.
- **China Q3 2026 GDP — RESOLVED at edition 45, closed thread, do not
  re-derive:** printed Monday 19 October 2026, confirmed directly against the
  National Bureau of Statistics' English-language press release. Q3 alone:
  **+4.5% y/y, +1.2% q/q**; first-three-quarters 2026 cumulative: **+4.6%
  y/y** (GDP RMB 107,107.1bn).
- **New Mexico v. Meta — the $25bn civil-penalty ruling (Judge Francis
  Mathew, Wed 21 Oct 2026) remains substantially clarified but Meta's formal
  notice of appeal is still unconfirmed for an ELEVENTH straight edition
  (47-56).** Meta owes **$25bn** in civil penalties for the jury's
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
  re-attempted at editions 55 or 56 either (out of scope); no new development
  in the 48-state settlement or the Unfair Practices Act stay.
- **New calendar-awareness item, reconfirmed relevant across several
  editions: "equities-open, bonds-closed" US holidays need an explicit check
  every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. **Next candidate to verify when it lands: Veterans Day, Wed 11 Nov
  2026** — not yet inside any edition's window; confirm whether that is also
  bonds-only before assuming, when it lands (now about a week out). **The DST
  transition (ended Sunday 1 November 2026) is now itself resolved/settled**
  — see the Schedule section above for confirmation detail.
- **The vendor-retroactive-revision trap showed another mixed outcome at
  edition 56, continuing the pattern first split at edition 55.** (1)
  Gold/silver: a genuine instance recurred, but **mild** — this edition's
  fresh Investing.com re-fetch of the prior session's (Monday 2 Nov) base
  came back gold $3,969.60 / silver $50.888, approx. 0.3-0.4% above the
  figures edition 55 itself had logged as its own fresh Monday close ($3,957.55
  / $50.685). This is materially smaller than the large multi-dollar gaps
  seen at editions 50-54 and was disclosed as a minor vendor-data variance in
  Annex A rather than treated as a full repeat of the larger pattern — keep
  the every-edition re-fetch-and-compare discipline regardless. Copper, FX
  (EUR/USD, GBP/USD) and Treasuries all again matched their logged prior-day
  bases exactly at edition 56, no discrepancy. (2) **Henry Hub: the
  base-price problem, persistent for FIVE straight prior editions (51-55),
  BROKE at edition 56** — Investing.com and Yahoo Finance's NG=F history both
  independently returned $2.895-2.896/MMBtu for Tuesday's close (+1.4% vs. a
  matching $2.856 Monday base on both platforms), the first genuine
  two-source cross-reconciliation for this series in six editions. CME
  settlement (timeout), Barchart NGZ26 (empty response) and Trading Economics
  (stale/internally inconsistent date-stamp) all still failed. **Treat this
  as encouraging but not yet a closed thread — confirm the Investing.com/
  Yahoo Finance reconciliation holds for at least one more edition before
  downgrading Henry Hub's priority from "elevated."** One flagged oddity:
  Yahoo's own Tuesday row showed suspiciously thin volume (1,364 contracts vs.
  163,066 the prior day) even though the price matched Investing.com closely
  — worth a quick freshness sanity-check next time rather than assuming it is
  resolved for good.
- **New sourcing technique validated at edition 54 (citing the prior
  edition's own already-directly-confirmed figure as a substitute for a
  same-day-only primary source), not needed at edition 55 or 56:**
  westmetall.com's live page accepted a direct date-query again at edition 56
  and returned clean Tuesday 3 Nov figures (LME cash $14,110.50/t, 3-month
  $14,001.00/t) consistent with a COMEX cross-check on direction and rough
  magnitude. Keep the carried-forward-prior-edition-figure workaround
  documented for whenever the live page reverts to exposing only the current
  day's row — it remains a legitimate substitute for a fresh fetch in that
  circumstance.
- **New sourcing-mechanics trap logged at edition 50, relevant to any
  Monday-dated (or any day-after-a-non-trading-day) edition: Investing.com
  inserts an electronic Sunday-evening re-open print as its own row for every
  24-hour-traded instrument.** Not applicable at edition 56 (a normal weekday
  session following a normal weekday session) — continue applying this
  discipline on every post-weekend or post-gap edition; it remains confirmed
  as a structural vendor behavior.
- **LME copper's primary source (westmetall.com) remains reliable — at
  edition 56 a direct date-query again successfully retrieved current-day
  figures cleanly.** A COMEX cross-check (Investing.com, $6.4105/lb, -2.39%
  Mon→Tue) agreed directionally and in rough magnitude with the LME figure
  (LME cash -1.88%) — no cross-source conflict this edition, unlike the
  occasional small basis gaps seen in prior editions.
- **Henry Hub natural gas: see the dedicated, elevated entry under the
  vendor-retroactive-revision trap above — this report's historically
  worst-performing data series had its first clean two-source edition (56)
  after five straight failed editions (51-55).** The front-month-contract
  identity (NGZ6/December, rolling toward NGF7/January as November
  progresses — watch for the roll) remains correct; OHLC internal consistency
  was not specifically re-checked at edition 56.
- **The Kitco live-spot-vs-headline cross-check succeeded for both metals
  again at edition 56, but this time surfaced a genuine change-%
  direction conflict against the futures close (see the dedicated Hard Rules
  entry below) even though absolute price levels agreed closely (within
  approx. 0.1-0.3%) for both gold and silver.** This is a different failure
  mode than prior editions' spot-vs-headline agreement — continue attempting
  both metals directly each edition and disclosing any conflict rather than
  silently resolving it.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company, IPO'd 1 July 2026 at
  $29/share. Logged here so a future edition doesn't waste effort
  re-verifying the ticker's legitimacy if it moves sharply again.
- **The "named secondary outlet's own claim can be flatly wrong" trap gained
  a new instance at edition 56: a claimed Oracle analyst-upgrade note citing
  "JPMorgan/Oppenheimer/Bernstein SocGen Group" was investigated and
  rejected** — the source page's own timestamps were internally inconsistent
  (claiming both a March and a May 2026 publish/update date for content about
  a November 3 event) and "Bernstein SocGen Group" is not a coherently named
  real firm (Bernstein and SocGen are separate, unrelated entities). Not used
  in the edition 56 briefing. Prior flatly-wrong instances remain: JetBlue
  (edition 50, magnitude), Carvana/Barron's (edition 52, direction/framing),
  Tesla and NU Holdings (edition 49, magnitude, twice in one session),
  Marvell/Lumentum and Barclays/PayPal (edition 53, claimed driver and a
  likely-fabricated analyst action), a misdated Reuters-style squib plus a
  wrong-year Trefis list (edition 54), and Brent crude's disclosed
  settle-to-settle-vs-"more than 7%" methodology discrepancy (edition 55).
- **A reinforcing, non-novel reminder, with a notable counter-example added
  at edition 56: a clean beat-and-raise continues to carry essentially no
  predictive power for the market's AH/next-day reaction — but edition 56
  shows it can occasionally still work as expected.** AMD's fiscal Q3 beat
  (revenue +45% y/y to $13.4bn, non-GAAP EPS $2.09, Data Center +97% y/y) and
  raised Q4 guide (approx. $17bn) WAS followed by a positive, sizeable AH
  reaction (approx. +5.02%) — a genuine instance of the "expected" pattern,
  standing in contrast to Apple, Oracle and Palantir's own muted-to-negative
  reactions to clean beats earlier in the same week (edition 55) and to
  AMD's own prior-quarter pattern of selling off after beats. Treat this as a
  reminder that the "no predictive power" finding describes a *distribution*,
  not a universal rule — always fetch the actual reaction rather than
  assuming either outcome. Edition 53 remains the largest-magnitude
  same-session negative instance logged to date (ServiceNow -26.95%); edition
  55 added Apple (-1.83%/-2.75% AH) and Palantir (-3.13%/-2.98% AH) as two
  more negative instances the same week AMD then bucked the pattern.
- **The DXY-vs-its-own-FX-crosses conflict, genuinely intermittent, persisted
  a SECOND straight edition at edition 56** (after first reappearing at
  edition 55 following five straight clean editions). Yahoo Finance's
  DX-Y.NYB ticker read Tuesday's dollar softer (101.49, -0.26%), while an
  Investing.com futures-style DXY proxy read it firmer (101.726, +0.10%) —
  absolute levels stayed close (~0.2 points apart) but direction disagreed,
  as at edition 55. The three major crosses (EUR/USD, GBP/USD, USD/JPY) all
  ticked modestly higher against the dollar on Tuesday, a mild dollar-soft
  signal that sits closer to the Yahoo read than the Investing.com futures
  proxy. MarketWatch's own DXY page was blocked by tooling at edition 56 and
  could not be used as a tie-breaking third source. Try Yahoo Finance again
  at edition 57, and keep trying a genuinely different third source (ICE
  direct, a cleanly-dated Trading Economics pull) to resolve the conflict
  rather than letting it become a standing unresolved feature.
- **The single-aggregator-dependence pattern for the AP/Reuters index-close
  wire: the La Nación (Argentina) international-syndication-mirror
  workaround, first found at edition 54, worked again cleanly at edition 56
  — now THREE consecutive successes (54-56).** Neither apnews.com nor
  Reuters' own wire page was directly located for Tuesday 3 November; the La
  Nación mirror carried the full "How major US stock indexes fared" content
  and matched independent ETF-proxy triangulation (SPY/DIA/QQQ/IWM) closely
  with no disagreement of concern. **This remains the established
  first-choice workaround** — keep using it before the Yahoo-Finance-plus-
  secondary-recap fallback, while still re-attempting apnews.com/Reuters
  directly every edition regardless.
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38, most recently exercised at edition 52.** Not exercised at
  editions 54, 55 or 56 either — no megacap GAAP/non-GAAP EPS conflict
  surfaced in any of those sessions' earnings.
- **The "preview-consensus-only miss/beat framing" caution (first logged at
  edition 41) remains an open, unconfirmed disclosed inference, not
  re-chased at editions 54, 55 or 56 either.** Pick this thread back up at a
  future edition if bandwidth allows.
- **Equifax's unexplained-magnitude rally thread remains open but of
  declining urgency; not re-checked at edition 55 or 56 either** (Equifax was
  not among either session's movers). The "Credit Abuse Risk" product-launch
  false-lead dead end from edition 54 remains excluded from future searches
  on this thread.
- **New at edition 47, reinforced every edition since including 56: when
  standard "biggest movers" aggregator pages aren't retrievable, SEC EDGAR's
  full-text search / `cgi-bin/browse-edgar` (filtered by CIK and form type
  8-K) is an effective, primary-source-grounded discovery/verification
  method** — used again at edition 56 to confirm AMD's own fiscal Q3 2026
  Exhibit 99.1 filing directly, and separately to confirm Caterpillar's
  already-reported (29 Oct, not 4 Nov as a planning assumption had it) Q3
  2026 results via its own 8-K. This remains the firmly established default
  verification route for any megacap or notable earnings report, and also a
  useful way to catch an incorrect assumed earnings date before it reaches
  the day-ahead calendar.
- **The edition-49 "forward-looking calendar aggregator" trap (names falsely
  listed as past reporters before they actually reported) remains closed**
  and gained a fresh, related instance at edition 56: a carried internal
  planning note had assumed Caterpillar would report Wednesday 4 November
  2026, when in fact it had already reported Thursday 29 October 2026 — found
  and corrected before publication via a direct SEC 8-K check, not via a
  correction box (the wrong assumption lived only in planning notes, never in
  a published edition). **Lesson reinforced: always verify an assumed future
  earnings date against the company's own IR page or a primary filing before
  listing it in the day-ahead calendar, even when the date comes from a
  seemingly reliable aggregator or a prior edition's own forward-looking
  note.**
- **A megacap multi-name earnings cluster producing genuinely uncorrelated
  reactions is a standing, repeated pattern — now at least TEN distinct
  instances through edition 55 (editions 44, 47, 48, 49 x2, 50, 52, 53 x3,
  55).** Edition 56 did not add a fresh instance of this specific pattern (it
  had a single dominant earnings report — AMD — rather than a cluster), but
  did add a related, useful counter-example to the adjacent "beat-and-raise
  guarantees nothing" reminder (see the dedicated entry above: AMD's beat DID
  hold up positively after hours). Treat "beat and raise" (or "similar
  financing news") as having no reliably predictable effect on the reaction
  without also checking the specific sub-metric or guidance nuance investors
  are reacting to, and always fetch the actual reaction as a separate,
  disclosed fact.
- **New production lesson from edition 53: CSS multi-column (`.cols3`/
  `.cols2`) pagination under Chromium print-to-PDF can plateau stubbornly on
  marginal content trims** — see the condensed mega-block below for the
  mechanics and the fix (merging several Annex C entries at once rather than
  iterating with small per-entry trims). **Not triggered at edition 54, 55 or
  56** — all three editions converged cleanly on the first render (edition 54
  via the spillover-break-deletion mechanism; editions 55 and 56 both with the
  forced break retained throughout, sections 1-6 ending within page 3 on the
  first attempt) — reinforcing that edition 53's plateau was
  content-volume-specific rather than a general property of the CSS approach.
- **New at edition 54: the VIX feed's two known bugs (duplicated
  `prev_day_close`, and a `price_change_percent` that divides by the wrong
  price) appeared on ALL SIX series at edition 54, not intermittently as
  several prior editions found. At editions 55 and 56, by contrast, BOTH bugs
  were ABSENT on all six series for two consecutive editions** — the feed's
  own reported `price_change_percent` matched an independently computed
  manual calculation to four decimal places on every series both times.
  **Continue the manual-calculation discipline unconditionally regardless of
  how many bug-free editions might follow** — two clean editions is not
  evidence the bug is fixed for good.
- **New at edition 54: a markup-correctness self-check caught three
  instances of the `</td><sup` table trap (documented under Production
  notes below) before rendering, in the Commodities table's FX/Treasury rows
  where an empty trailing "Note" cell was followed by a citation tag typed
  outside it. Editions 55 and 56 both ran the same proactive `grep -n
  '</td><sup'` check and found ZERO instances** — worth continuing to run
  this grep proactively on every edition with a table that has an empty
  trailing cell or a cell containing only a citation, not just after a
  page-count problem.
- **New at edition 54: the CFTC Asset-Manager-vs-Leveraged-Funds grouped-bar
  chart was reused for a fifth time (editions 34, 39, 44, 49, 54 — a clean
  Monday/weekend-window pattern) with the same figsize (9.8, 2.15), `h=0.32`
  bar offset and figure-level legend technique documented under Production
  Notes.** **Neither edition 55 nor edition 56 used the chart** — no fresh
  CFTC data fell inside either single-session window (the Friday 30 Oct
  report, covering Tuesday 27 Oct data, had already been used at edition 54),
  and in both cases a genuinely present VIX-complex story (a kinked term
  structure at edition 55, its partial narrowing at edition 56) was judged
  not the day's dominant one next to the session's equity and commodity
  moves. The next opportunity is the Friday 6 November 2026 report (covering
  Tuesday 3 Nov data) — check cftc.gov directly whichever edition's window
  includes it, likely edition 59 on a daily cadence.

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
  tale**: a genuinely dense single-session day rendered at 6 pages on the
  first draft and needed roughly a dozen trim/merge rounds to converge.
  **Editions 54, 55 and 56 have all now converged cleanly within one or two
  renders** (54 after deleting the one forced break; 55 and 56 both on the
  very first render with the break retained, sections 1-6 ending within page
  3 both times) — reinforcing that content density alone does not predict
  whether a trim marathon will be needed; check the actual render before
  assuming one is.
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
  mismatch there. If a chart aggregates figures from several different Annex
  C entries (as a movers chart often does), it is legitimate to omit a
  bracket number from the axis label entirely rather than force a single
  potentially-misleading citation — edition 55 did this for the movers chart
  (sector chart kept its single citation since all 11 values share one
  source); **edition 56's movers chart used a single citation since all ten
  values shared one source (stockanalysis.com)**, a simpler case. **Also
  watch for a stray bracket typed outside a `<sup>` tag entirely** —
  `check_refs.py` will not flag it since its regex only matches inside `sup
  class="ref"` tags, so a bare `[n]` slips through silently. Proofread
  citation-heavy sentences visually, not just via the script, when a sentence
  carries two or more consecutive citations. A related trap, worth naming
  explicitly: placeholder ref text (e.g. `[note1]`) typed during drafting and
  never swapped for a real number. `check_refs.py`'s regex requires `\d+`
  inside the brackets, so a non-numeric placeholder simply won't match either
  the inline or Annex-B regex — it won't show up as "missing" or "unused," it
  just silently doesn't count. **Never use a letter suffix to disambiguate a
  citation — always mint a new integer.** Annex C numbers do not need to be
  contiguous, only matched 1:1 against inline citations — deleting an unused
  reserved number and leaving a gap is completely fine and simpler than
  renumbering everything after it (**edition 56 did exactly this**: a
  tentatively reserved source number for a carried-forward-prior-edition
  citation was dropped before rendering once it turned out not to be needed
  inline, leaving the Annex C list at 29 clean, contiguous entries rather
  than renumbering). **Reusing the same Annex C number for multiple
  movers/figures citing the same outlet/method is fine and recommended** —
  `check_refs.py` only checks presence/absence, not uniqueness of use.
  **Citing the prior edition itself as a source** (e.g. "logged prior-session
  baseline figures") is a legitimate, already-used pattern when disclosing a
  divergence against, or carrying forward, a previously-logged figure —
  edition 55 used this for the Fed/BoC/Norges-Bank policy-table "last change"
  cell; edition 56 did not need it (no cell required a prior-edition
  self-citation this time).
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
  corrects nothing**, which will be most of them. **Editions 54, 55 and 56
  have all omitted the box** — in each case nothing published in a prior
  edition was found to be wrong. (Edition 56's Caterpillar day-ahead
  correction concerned only an internal planning assumption carried in prior
  spec notes, never a figure published in a prior PDF edition, so it did not
  warrant a correction box — it was simply fixed in this edition's own
  day-ahead table and logged in Annex A.)
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
  a matching Annex B entry. **Editions 54, 55 and 56 have all run the same
  full 10-row table** (Fed, BoJ, BoE, ECB, BoC, RBA, SNB, Norges Bank,
  Riksbank, Banxico). Riksbank's rate value and Banxico's rate/next-decision
  remain the only unavailable-marked cells as of edition 56; the RBA's
  "next decision" cell became newly unavailable at edition 56 (its current
  rate changed and is primary-confirmed, but the next meeting date is not
  yet known) — the inverse of the BoJ/SNB pattern from edition 54, where the
  rate was known but the date wasn't. If page 3 overflows anyway, cut rows
  that had no news in the window before cutting any prose. Follow the usual
  table convention — plain `<tr>` header rows, no `<thead>`.
- **Charts: two fixed, a third only when earned — changed at edition 49.**
  The **sector-ETF performance chart always goes in Section 1**, beside the
  sector narration it illustrates, and the **single-stock movers bar always
  goes in Section 2**, with the names. Neither may duplicate a table.
  A **third chart is allowed only when positioning or volatility is
  genuinely the day's dominant story** — not merely present, and never to
  fill a short page — and it goes in the section it belongs to: CFTC
  asset-manager vs. leveraged-funds positioning or a VIX term structure in
  Section 5, an implied-vs-realized earnings bar in Section 2. **Edition 54
  used the CFTC positioning chart** (fresh data posted on schedule, the fifth
  time this specific Monday/weekend-window trigger has justified the chart —
  editions 34, 39, 44, 49, 54). **Neither edition 55 nor edition 56 used a
  third chart** — in both cases no fresh CFTC data fell inside the window,
  and a genuinely present VIX-complex story (a kinked term structure at
  edition 55, its narrowing but not resolving at edition 56) was each time
  judged not dominant enough next to the session's equity and commodity
  moves to earn a chart over prose. Next CFTC report due **Friday 6 November
  2026**, covering Tuesday 3 November data — check cftc.gov directly
  whichever edition's window includes it.
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
  rather than producing a plausible-sounding number. **Never report a
  derived/aggregate figure (e.g. a combined dollar value) that was not
  itself directly sourced — edition 55's first draft briefly stated an
  invented "approx. $40bn combined market value erased" for the
  Marvell-Lumentum deal before being caught and replaced with the two
  companies' actually-sourced percentage moves; this is exactly the kind of
  plausible-sounding-but-unsourced number this rule exists to prevent. Treat
  any sentence that computes or combines two sourced figures into a new
  number as needing its own source or a cut, not an estimate.** No violation
  of this rule was found needing a fix at edition 56.
- Where sources disagree, use the more authoritative one **and** disclose
  the disagreement. AP's "How major US stock indexes fared" and the Reuters
  market wrap are normally the most reliable for index closes — but check
  they're actually indexed for the target date before relying on them.
  **Editions 48 through 53 all found neither wire indexed/fetchable** (with a
  single one-edition exception at edition 51 via a syndicated mirror).
  **Edition 54 found a NEW, cleaner variant of the same workaround: an
  AP-wire mirror syndicated through an international outlet (lanacion.com.ar)
  carried the full wire content and matched two independent US secondary
  sources exactly. Editions 55 and 56 both reused the same La Nación mirror
  successfully — now THREE consecutive successes** — this is the established
  first-choice workaround; try it before the Yahoo-Finance-plus-secondary-
  recap fallback, while still re-attempting apnews.com/Reuters directly every
  edition regardless.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Always check a dated article's own claimed magnitude AND
  direction against the underlying price-history table or primary filing,
  not just its date, before repeating it** — this trap has now hit
  magnitude (J.B. Hunt ed.44, Tesla/NU Holdings ed.49, JetBlue ed.50),
  direction/framing (Carvana/Barron's ed.52), claimed drivers that don't
  hold up (Marvell/Lumentum ed.53), a claimed analyst action that appears
  outright fabricated (Barclays/PayPal ed.53; **Oracle ed.56, see the
  dedicated Standing Facts entry above**), the claimed DATE/YEAR itself
  (edition 54's Reuters-squib/Trefis exclusions; **edition 56's carried
  Caterpillar-reports-Nov-4 planning assumption, caught against Caterpillar's
  own 8-K before publication**), and a disclosed cross-source
  percentage-methodology discrepancy (edition 55's Brent crude move) — treat
  ANY surprising secondary claim (price move, driver, analyst action, date,
  or computed percentage) as needing this same verification discipline.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  **Edition 55 exercised this discipline directly on Apple's earnings date;
  edition 56 had no cross-pass disagreement requiring a dedicated
  verification pass**, though the equities pass independently flagged and
  rejected the unreliable Oracle analyst-action claim on its own initiative,
  which the same discipline would also have caught had it slipped through.
- **Premarket is not the close, and the close is not the after-hours
  earnings reaction — and an after-hours reaction does not necessarily hold
  into the next regular session, uniformly or at all. A strong beat-and-raise
  does not guarantee a positive reaction even within the SAME session —
  though, per the updated Standing Facts entry above, it does not guarantee a
  negative one either.** Reinforced at essentially every edition since 44;
  edition 53 remains the largest-magnitude same-session negative instance
  (ServiceNow, -26.95% despite a clean beat-and-raise); **edition 56 added
  AMD as a positive counter-example (+5.02% AH on a clean beat-and-raise)**.
  Always fetch the verified close, the after-hours reaction, AND (when the
  window allows) the next regular session's close as three separate, clearly
  labelled figures. A premarket-only figure that cannot be confirmed to have
  held into the regular close should be excluded rather than reported as a
  close-of-day mover — edition 55 excluded EchoStar's premarket approx. +5%
  read on exactly this basis; **no comparable exclusion was needed at edition
  56**.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent** — see
  the dedicated, updated Standing Facts entry above, which now records a
  SECOND consecutive edition (55-56) of the same specific conflict (Yahoo
  Finance DX-Y.NYB reading softer, an Investing.com futures-style proxy
  reading firmer). Continue disclosing the DXY-vs-FX-crosses directional
  comparison explicitly every edition regardless of which way it goes, and
  keep trying a genuinely different third source to break the tie.
- **The Kitco live-spot-vs-headline cross-check succeeded in getting a level
  for both metals again at edition 56, but this time the comparison itself
  surfaced a genuine change-% sign conflict against the futures close**
  (spot showed both metals up on the day; futures settle-to-settle showed
  both down; absolute levels agreed within approx. 0.1-0.3%). Disclose this
  explicitly rather than picking one reading — it is most likely a reference-
  point artifact (Kitco's displayed "change" appears computed against a
  different intraday baseline than a clean settle-to-settle comparison), not
  a data error on either side.
- **GBP/USD, EUR/USD and USD/JPY all reconciled cleanly again at edition 56**
  against their logged Monday base — the vendor-revision trap this edition
  hit gold/silver mildly (see Standing Facts) but not the FX crosses,
  Treasuries, or copper.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for twenty-one further editions (37-56)** — edition 56 again found the full
  Treasury curve reconciled cleanly against the official home.treasury.gov
  TextView page (2-year 4.61%, 10-year 4.95%, 30-year 5.32%, a modest
  parallel upward shift with slight front-end steepening on the day). Treat
  as resolved/noise unless a fresh conflict appears.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 56 have all run clean (or
  clean after quick fixes) — **edition 54 needed one fix** (a source cited
  only in a chart axis label needed an inline body citation added too);
  **edition 55 needed two fixes** (two Annex C entries needed a matching
  inline citation added); **edition 56 needed one fix** (a reserved Annex C
  entry for a carried-forward-prior-edition citation was never cited inline
  once the draft didn't end up needing it, and was deleted rather than
  force-cited, per the standing "unused reserved numbers are fine to drop"
  rule) — clean on the second check.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 55 rendered with zero stray tildes on the first
  draft; edition 56 needed one fix** (a snap-grid tile's Bitcoin value used a
  literal `~` before being caught by the pre-render grep and swapped for
  "approx." — a reminder that the tile shorthand is exactly the kind of
  late-added, outside-the-main-drafting-pass spot where a stray tilde tends
  to slip in, consistent with the standing caution in references/format.md).
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
  content requiring real trimming, while editions 54, 55 and 56 all showed
  the opposite: heavy content does NOT automatically mean a multi-round
  trim.** Edition 54 converged after deleting the one forced break; editions
  55 and 56 both converged on the first render with the break retained
  throughout. Always check which situation you're in (stray break vs.
  genuine overflow vs. spillover that just needs the break deleted vs. a
  dense day that simply fits) before assuming a trim marathon is required.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — **specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation.** Edition 54's
  movers chart had a ratio of only approx. 2.7x; edition 55's had a ratio of
  only approx. 1.5x; **edition 56's movers chart (10 categories, ORCL +5.85%
  largest, COIN +5.53% second largest) had a ratio of only approx. 1.06x** —
  no capping needed in any of the three. Used `pad_frac=0.22` for edition
  56's movers chart (max abs value approx. 5.85%, figsize (9.8, 1.95)) and
  `pad_frac=0.30` for the 11-category sector panel (same figsize), both
  rendering cleanly with no label crowding.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 56 have all got a fresh,
  same-day-timestamped sweep** — twenty-nine consecutive fresh sweeps now.
  **The feed's two known bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) appeared on ALL SIX series at edition 54 but were ABSENT on all six
  series at editions 55 AND 56** (the feed's own reported percent-change
  matched an independent manual calculation to four decimal places both
  times). **Always compute day-over-day % change manually regardless of how
  many consecutive bug-free reads preceded the current one.** Edition 56 saw
  the VIX complex ease across the board as Monday's reversal/vol-pop
  partially unwound: VIX -1.51% to 20.83, VIX9D -2.23% to 21.96, VIX3M -1.53%
  to 21.27, VIX6M -1.59% to 22.31, VVIX -2.78% to 107.40, SKEW -1.81% to
  150.01 — Monday's term-structure kink (VIX9D above both VIX and VIX3M)
  narrowed (VIX9D's premium over VIX fell from 1.31 to 1.13 points, over
  VIX3M from 0.86 to 0.69) but did not fully resolve; VIX3M-VIX6M stayed in
  ordinary contango throughout.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 56 fetched all 11 directly again**
  (Technology +1.31% the clear leader on the session's megacap/AI bounce,
  Communication Services +1.18% and Industrials +0.95% also higher, Real
  Estate roughly flat at +0.07%; Consumer Staples -2.07% and Materials
  -2.01% the clear laggards with no identified single-name driver despite a
  targeted search; 4 of 11 green) — continue this direct-fetch-by-default
  method.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (4 of 11 at edition 56, consistent
  with AP's own characterization that most constituents actually fell even
  as the cap-weighted indices rose) — no competing secondary-aggregator
  breadth figure was checked this edition.
- **Dealer gamma:** zerogex.io hit a **seventeenth consecutive edition of
  failure at edition 56** (all widgets still show placeholder dashes with no
  timestamped data). SpotGamma logged an **eleventh straight failure at
  edition 56**, confirmed again as a client-side React single-page app with
  zero server-rendered data behind its dashboard.spotgamma.com login. Both
  sources remain fully unusable.
- **Official CME FedWatch probabilities:** the page blocks fetching
  (edition 56's direct attempt timed out again, a **sixteenth** consecutive
  failure, 41-56) — use secondary citations (Polymarket, Kalshi, Reuters/
  other economist polls, desk notes) and give a range rather than a single
  invented number. DeFi Rate's Kalshi/Polymarket-blended aggregator remains
  a stable, consistently working source for both the near-dated and
  December meetings — though its December sub-table has now shown an
  internal inconsistency for **ten straight editions** (47 through 56),
  staying narrow (approx. 2-3 points) as at edition 55 — should simply be
  expected and disclosed, not treated as a transient bug. **Polymarket
  direct, tried via its Gamma API (`gamma-api.polymarket.com/public-search`)
  rather than a plain site visit, succeeded again at edition 56 — a third
  consecutive success** — this remains the preferred first approach; try it
  before reverting to a plain site visit.
- **Kalshi direct fetch:** rate-limited or blocked across every edition it
  has been attempted, now **TWENTY consecutive failures (37-56)** — a
  confirmed structural gap, not transient (edition 56's specific failure
  mode was again HTTP 429 rather than an outright block/404). Resume the
  attempt-every-edition discipline at edition 57 regardless, but expect a
  block of some kind. Use Kalshi's own secondary reporting or DeFi Rate's
  blended aggregator as the workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages); the CME natural-gas settlement page also
  timed out again at edition 56. **westmetall.com remains the standing LME
  copper primary source and at edition 56 a direct date-query again
  successfully retrieved current-day figures cleanly.**
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **remained clean at edition 56** (2-yr
  4.61%, 10-yr 4.95%, 30-yr 5.32%, all 3 Nov, with the prior Monday base
  matching the previous edition exactly), extending the clean streak to
  **twenty-one editions (37-56)** with no repeat of the edition-36 33bp gap.
  Continue scoping the TextView URL to the specific month
  (`field_tdr_date_value_month=202611`-style parameter) rather than the
  full year.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). **No new report fell inside edition 56's single-session
  window** (the Friday 30 Oct report, covering Tuesday 27 Oct data, remains
  the most recent) — confirmed nothing posted early. **The next report is
  due Friday 6 November 2026, 3:30pm ET, covering Tuesday 3 November data**
  — check cftc.gov directly whichever edition's window includes it (likely
  edition 59 on a daily cadence). The CFTC release-schedule change (moving to
  twice-weekly releases by end of 2026, per a 27 Oct 2026 CFTC announcement,
  Press Release 9316-26) was reconfirmed at edition 56 via the press release
  itself — proposed structure: Monday data published Wednesday, Wednesday
  data published Friday, both at 3:30pm ET — but still has **no confirmed
  start date**; worth a one-line check when the 6 November report actually
  lands, in case the covered-data convention has shifted by then.
- **GBP/USD, EUR/USD, USD/JPY clean close:** all remain fully resolved,
  reconciling cleanly again at edition 56 (EUR/USD 1.1194 +0.06%, GBP/USD
  1.3415 +0.06%, USD/JPY 158.68 +0.46%, all single-sourced to Investing.com's
  close-to-close history table, Monday base matching this edition's own
  fresh re-fetch exactly). **DXY itself remains in an unresolved cross-source
  direction conflict for a second straight edition (55-56)** — see the
  dedicated Standing Facts entry above for the full disclosure. Try Yahoo
  Finance again at edition 57, ideally with a second, different corroborating
  source (MarketWatch was blocked by tooling at edition 56, not yet tried
  successfully).
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot cross-check succeeded in getting a level for both metals again
  at edition 56, but surfaced a genuine change-% direction conflict against
  the futures close** — see the dedicated Standing Facts and Hard Rules
  entries above. **The base-price vendor-revision discrepancy recurred mildly
  at edition 56** (approx. 0.3-0.4%, well below the multi-dollar gaps seen at
  editions 50-54) — disclosed in Annex A as a minor variance rather than a
  full repeat of the larger pattern. Monday 2 Nov base figures this edition's
  fresh Investing.com fetch returned: gold $3,969.60, silver $50.888 (vs.
  edition 55's own logged $3,957.55 / $50.685). Tuesday 3 Nov futures close:
  gold $3,946.92 (-0.57%), silver $49.923 (-1.90%); Kitco spot same session:
  gold $3,950.40 (shown +0.53%), silver $49.91 (shown +0.47%).
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is also a closed thread as of
  edition 45. **US GDP, PCE, import/export prices and industrial
  production:** all closed threads — see Standing Facts above. **University
  of Michigan October consumer sentiment** is a closed thread as of edition
  49. **China's October PMI** is a closed thread as of edition 54.
- **Henry Hub natural gas:** the front-month-contract-identity question
  remains resolved (NGZ6/December, watch for the roll to NGF7/January as
  November progresses). **The base-price reliability problem, this report's
  historically worst-performing data-quality issue across five straight
  failed editions (51-55), had its first clean two-source reconciliation at
  edition 56** — see the dedicated, elevated Standing Facts entry above for
  full detail, including the specific sources (Investing.com, Yahoo Finance
  NG=F) that finally agreed, and the ones that still failed (CME, Barchart,
  Trading Economics). **Confirm this holds for at least one more edition
  before downgrading the priority of this item from "elevated."**
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 56 again found no notable
  single-stock options-flow/skew commentary** tied to Tuesday's movers
  (specifically searched around AMD's pre-earnings positioning, Coinbase and
  Strategy) — a **nineteenth-plus** largely-empty edition on this general
  sub-item (AMD's own implied-move figures that were found were conflicting
  and undated/stale, and were excluded rather than reported). Treat this
  sub-item as reliably low-yield and keep it a brief, secondary effort each
  edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. **Q3's
  approx. 14 November 2026 deadline falls on a Saturday** — the natural lead
  item for whichever edition covers the following Monday, 16 November 2026
  (a weekend-gap edition), now under two weeks out.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22, not attempted
  again since). Revisit only if a future edition has spare research
  bandwidth on an FOMC day specifically — not relevant to most editions.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully at
  editions 39, 44-49 and 54 (the Friday 30 Oct report, covering Tuesday 27
  Oct data). No new report fell inside edition 55's or edition 56's window.
  Repeat the three-instrument fetch whichever edition's window extends past
  Friday 6 November, 3:30pm ET, watching for the micro-vs-full-size naming
  trap each time, and for a possible release-schedule change (see the CFTC
  CoT entry above).
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Not specifically
  re-attempted at editions 54, 55 or 56 (out of scope each time, though
  edition 56 did investigate and reject one specific claimed Oracle action —
  see Standing Facts); watch each edition independently rather than assuming
  a trend. Edition 53 separately found and explicitly rejected a claimed
  Barclays "Underweight" downgrade on PayPal that could not be substantiated
  at all. Edition 55, by contrast, DID obtain two clean, directly-sourced
  analyst actions (BofA cutting Marvell, Stifel downgrading Lumentum) tied
  directly to the Marvell-Lumentum deal — the gap is about non-headline,
  isolated analyst actions specifically, not all analyst actions generally.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** This discipline has now caught: Tesla/NU Holdings
  (ed.49, magnitude), JetBlue (ed.50, magnitude), Carvana/Barron's (ed.52,
  direction/framing), Marvell/Lumentum and Barclays/PayPal (ed.53, claimed
  driver and a likely-fabricated analyst action), two more exclusions at
  edition 54 (a misdated Reuters-style squib and a wrong-year Trefis list),
  and **a claimed Oracle analyst-upgrade note at edition 56** (internally
  inconsistent timestamps, a non-existent firm name). At edition 56, index
  closes, sector closes and single-stock closes were all independently
  cross-checked (AP mirror vs. ETF proxies; this edition's fresh Monday
  baseline re-fetch vs. the prior edition's own logged figures) with no
  disagreement of concern found on any of those series; two smaller items
  (Clorox's +4.34% move within Staples, and Kenvue's apparent 2 Nov
  delisting consistent with the pending Kimberly-Clark deal) remained
  confirmed-price-but-no-driver or inferred-but-not-primary-confirmed
  respectively, and were disclosed as such in Annex A/B rather than
  individually chased further given time constraints. Continue this
  direct-verification discipline on high-confidence-seeming figures and
  claims, not just surprising ones, prioritizing the largest/most prominent
  movers first when time is limited.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted at editions 48 through 56 (out of scope each time); try
  an alternate DOL page or a secondary economic-calendar aggregator for the
  consensus figure at edition 57.
- **federalregister.gov's direct search interface is blocked, logged at
  edition 48, not re-attempted directly since** (editions 54, 55 and 56's own
  light-touch checks for a new tariff filing found nothing dated to their
  respective windows, but none re-tested the search interface itself): a
  prior search attempt 302-redirected to `unblock.federalregister.gov`, an
  apparent bot/rate-limit gate. Note this for any future tariff- or
  trade-filing search attempt rather than re-discovering the same block.
- **SEC EDGAR's `cgi-bin/browse-edgar` company-search page (filtered by CIK
  and form type 8-K) is a highly reliable, fast way to confirm both WHETHER
  a company has reported on a given date and to find the accession number
  for the underlying exhibit** — used again at edition 56 for AMD (confirming
  its fiscal Q3 2026 Exhibit 99.1) and for Caterpillar (confirming it had
  already reported 29 Oct, correcting a carried planning assumption of 4
  Nov). This remains the firmly established default verification route for
  any megacap or notable earnings report, and a useful way to catch a wrong
  assumed earnings date before it reaches the day-ahead calendar.
- **Riksbank's primary policy-rate/next-meeting page.** CLOSED at edition 50
  for the current-rate sub-question's prior iteration and CLOSED at edition
  53 for the next-decision-date sub-question (4 Nov decision, re-confirmed
  again directly at edition 54). **The current rate VALUE could not be
  reconfirmed directly for a THIRD straight edition (54-56)** —
  riksbank.se's own dedicated rate page 404'd again on multiple URL patterns
  at edition 56; try yet another path at edition 57, which will also be the
  edition covering Wednesday's actual decision outcome. The exact origin
  date of the current approx. 1.75% level (secondary sources describe both a
  30 September 2026 effective date and a 26 August 2026 last-hold date,
  probably just two different ways of describing the same "unchanged since a
  prior-cycle cut" state rather than a contradiction) remains a minor,
  low-priority imprecision.
- **ECB's current policy rate: SETTLED since edition 55** (reconfirmed
  directly for a third consecutive edition — 53, 54, 55 — unchanged through
  the 28-29 October 2026 meeting: deposit facility 2.50%, main refi 2.65%,
  marginal lending 2.90%); not re-attempted at edition 56 (no fetch needed).
  Do not spend a fetch on the rate level itself going forward; it reopens on
  contradiction, the next Governing Council decision, or the monthly audit.
  **Its exact Governing Council press-conference content/vote-split remains
  unobtainable** and was not specifically re-attempted at edition 56 (out of
  scope) — low priority. **The Council's own next-meeting date is not yet
  known** — this remains the ECB's one outstanding live sub-question; verify
  directly whenever a window approaches the plausible next date (likely
  mid-December given typical six-weekly cadence), do not assume.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel —
  confirmed clean again at edition 56 (seventeen editions total: 37-43,
  45-50, 52-56). For charts with fewer categories, scale the height down:
  roughly `(9.8, 1.65-1.95)` for 3-9 categories. **Edition 56 used `(9.8,
  1.95)` for a 10-category movers chart with `pad_frac=0.22`**, rendering
  cleanly with no label crowding (largest-to-second-largest ratio only
  approx. 1.06x, well under the 5x capping threshold — the tightest ratio
  logged to date). **Always render and visually inspect (via the Read tool)
  the actual PNG at or near full resolution before embedding it**, regardless
  of what a past edition's success might suggest. **Default to pad_frac=0.30
  from the start for an 11-category sector-ETF panel** — now confirmed
  across eleven straight small-magnitude 11-category panels (45-50, 52-56).
  For any movers chart with a double-digit-percent outlier, continue trying
  pad_frac in the 0.22-0.30 range from the start; for a tighter-spread
  single-digit chart like edition 56's, pad_frac=0.22 alone was sufficient.
- **Capped-outlier label-overlap fix (from edition 45):** when a capped
  bar's value label uses a "(capped)" text suffix, the label text can be
  long enough to visually bleed into the y-axis tick-label margin even at a
  wide pad_frac, because matplotlib's `ax.text()` is unclipped by default.
  **Fix: shorten the per-bar suffix to a single trailing asterisk (`"*"`
  instead of `" (capped)"`) and add one footnote to the chart's x-axis label
  instead.** This remains the recommended default for any future
  capped-outlier chart. No edition since 45 has actually needed outlier
  capping (every spread has stayed well under the approx. 5x ratio
  threshold, including edition 56's approx. 1.06x, the tightest yet) —
  reinforcing that the trigger is the ratio to the next-largest bar, not the
  largest bar's absolute size.
- **A grouped (two-series) horizontal bar chart — needed for the CFTC
  Asset-Manager-vs-Leveraged-Funds positioning chart — requires custom chart
  code, not the standard single-series `barh()` helper used for the
  movers/sector charts** (first built at edition 44, reused successfully at
  editions 49 and 54; not needed at edition 55 or 56 since no fresh CFTC data
  fell inside either window). The standard helper only plots one value per
  category; the CFTC chart needs two bars (Asset Manager, Leveraged Funds)
  per category (ES/NQ/RTY), offset vertically by a fixed height fraction
  (`h=0.32` worked cleanly at edition 54) around each category's tick
  position. **Fix that worked for the legend:** use a FIGURE-level legend
  (`fig.legend(..., loc="lower center", bbox_to_anchor=(0.5, 0.0), ...)`)
  combined with `fig.tight_layout(rect=(0, 0.1, 1, 1))` to reserve the
  bottom 10% of the figure for the legend. Figsize `(9.8, 2.15)` rendered
  cleanly at edition 54. **Reuse this exact pattern** for any future
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
      annex opens a clean page 4, exactly as before. **Editions 55 and 56
      both landed here**, with sections 1-6 ending partway through page 3 and
      the annex opening cleanly on page 4 both times (page 4 itself had some
      unused space at the bottom in both cases — acceptable; the "Filling a
      short page 3/4" guidance is optional padding, not a requirement, when
      the content is already precise and complete).
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
  overflows — it has repeatedly been the cheapest, highest-leverage fix.
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
  table) and caught all three via a proactive grep before rendering.
  **Editions 55 and 56 both ran the same proactive grep and found zero
  instances** — confirming the trap is specifically easy to introduce when a
  table row has an empty trailing cell that still needs a citation (both
  editions' Commodities tables always placed the citation sup tag as genuine
  cell content, never after an empty `<td></td>`). Run the grep on every
  edition with such a table, not just when troubleshooting a layout problem.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Edition 53 needed this discipline more than almost any prior edition (see
  the condensed mega-block for the writeup); edition 54's own page-4
  orphaned-bullet symptom was also only visible by reading the actual page
  image, not from the page count alone. **Editions 55 and 56 both rendered
  cleanly on the first attempt** (no symptom to catch either time), but the
  page images were still read in full as standard practice both times,
  confirming no broken tables, no overlapping chart labels, and no cut-off
  content on any of the 4 pages.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across many editions'
genuinely different content volumes, including editions 53's, 54's, 55's and
56's. Treat as the durable default; the lever to pull on a high-volume or
overflowing day is first checking for duplicated content across sections,
then merging/trimming redundant content across whichever sections (or Annex
C citations) are longest — not loosening the CSS further.)
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
  runs short — editions 44 through 56 have all folded commodities, FX and
  Treasuries into ONE combined table (10-14 rows; edition 56 used 13) as the
  PRIMARY commodities table rather than padding, now the standing default.
  **Always re-render immediately after adding (or removing) any content to
  confirm the page count.**

**Chart selection guidance.** Placement is not editorial for the first two
charts:

- **Sector-ETF performance chart → Section 1 (Market recap), every
  edition.** Same-day closes by default; a grouped day-over-day bar instead
  on a multi-session or weekend window, or on a genuine multi-sector
  broadening selloff across consecutive sessions. **Editions 54, 55 and 56
  all used a single-day bar** (only one NYSE session fell inside any of those
  windows).
- **Single-stock movers bar → Section 2 (Equities), every edition.**
- **A third chart only when positioning or volatility is genuinely the
  day's dominant story**, never to fill a page, placed in the section it
  belongs to:
  - Fresh CFTC CoT data → the ES/NQ/RTY asset-manager-vs-leveraged-funds
    positioning chart, normalized as % of open interest, built with the
    grouped-bar technique documented under Production notes, in **Section
    5**. Editions 24, 34, 39, 44, 49 and 54 have all placed it there; neither
    edition 55 nor edition 56 had fresh data to place it with.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully. Not used at edition 55
    (Apple) or edition 56 (AMD) despite each being a genuine earnings story —
    no reliably-sourced implied-move figure was found for either session
    (AMD's own pre-earnings implied-move figures were found but conflicting
    and undated, and were excluded rather than used).
  - A holiday-window preview edition with no fresher data → VIX futures
    term structure with event annotations, in **Section 5**. Not used at
    edition 55 or edition 56 — in both cases the VIX term structure was
    genuinely newsworthy (a kink, then its narrowing) but was judged
    secondary to the session's equity and commodity stories and was covered
    fully in prose instead.

**Edition 57 (expected to cover Wednesday 4 November 2026, assuming no gap)
has a real, contained macro-calendar load.** Watch directly rather than
assuming: **the Riksbank's decision** (due approx. 9:30 CET Wed 4 Nov, which
lands inside edition 57's own window — confirm the actual outcome against
riksbank.se, and try yet another URL path for the current rate value given
three straight prior failures); **Qualcomm's FQ4/FY2026 earnings** (after
Wednesday's close, confirmed via Qualcomm's own press release at edition 56);
**October's ISM Services PMI** (also due Wednesday 4 Nov — no consensus
figure was found at edition 56, try again closer to release). It should also
retry: a direct bankofengland.co.uk recheck is no longer needed (primary-
confirmed at edition 56) but the actual Thursday 5 Nov BoE outcome itself
will land in edition 58, not 57; a second, different source to corroborate or
resolve the Yahoo-Finance-vs-Investing.com DXY direction conflict (now two
straight editions unresolved); confirmation that Henry Hub's edition-56
two-source reconciliation (Investing.com + Yahoo Finance) holds for a second
consecutive clean edition before downgrading its priority; Banxico's rate/
next-decision date via yet another URL path; the RBA's own next-decision date
(unconfirmed as of edition 56, now that its current rate itself is
primary-confirmed at 4.85%). The La Nación AP-wire-mirror approach and the
Polymarket Gamma-API approach are both now the established first-choice
methods, each on a three-edition clean streak — use them first rather than
their respective fallbacks.

**Remember the figsize-scales-to-category-count guidance above
(ceiling `(9.8, 1.95)` for an 11-category panel, `(9.8, 2.15)` for the
3-category grouped CFTC chart, scale down for fewer single-series
categories), that an 11-category sector-ETF panel should default to
pad_frac=0.30 from the start (now confirmed across eleven editions, including
56), a movers chart with a double-digit-percent outlier should try pad_frac
in the 0.22-0.30 range from the start (edition 56 used 0.22 for a
10-category panel with a tight +5.85%/-1.90% range, ratio approx. 1.06x, the
tightest logged to date), and the capped-outlier asterisk/footnote fix when a
spread crosses the approx. 5x RATIO threshold** (it has not since edition
45).

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

**Edition 56's carried-forward spec was 117,964 bytes, over the 100,000-byte
threshold — this run folded edition 54 into the mega-block and condensed
edition 55 to a medium paragraph, per the log's own standard rotation, as
part of producing this file.** There is no maximum size; condensing is
housekeeping done by the run itself, not a check to pass — there is no
penalty for the file staying somewhat large if the alternative is losing
information.

**Editions 1–54 (condensed):** established the format (edition 1 baseline;
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
adding five missing inline citations. **Edition 53 (Fri 30 Oct, covering
Thu 29 Oct):** Q3 GDP (+3.4%) and September core PCE (+3.1% y/y) both
printed hot the same session the market largely shrugged off; December hike
odds eased slightly despite it, and the DeFi Rate aggregator's internal
decision-vs-rate-level inconsistency persisted a seventh straight edition.
Alphabet lost approx. $500bn of market value in a single session (-12.64%),
extending Wednesday's AH mark-to-market-loss reaction even as Search and
Cloud both beat, dragging Communication Services to the day's sector laggard
even as 9 of 11 sectors closed higher. Amazon's Q3 was a "double miss on the
surface" (EPS missed on a prior-year comp effect) masking real AWS/margin
strength (shares -4.25% regular, -7.30% AH). "Beat-and-raise guarantees
nothing" produced its largest cases yet: ServiceNow -26.95%, Intel -23.04%
AH, Caterpillar -9.25%, all on clean beats; Mastercard/Eli Lilly/Merck/Crocs
beat and rose the same session. Smaller movers: Xerox -40.32%, Glaukos
+33.65%, ADT +33.20%, Marvell -13.24% (a claimed Lumentum-acquisition-talks
driver found unsubstantiated — a claim that, strikingly, became real M&A
four sessions later at edition 55), Carvana +15.68%. The vendor-retroactive-
revision trap hit gold/silver a second straight edition and Henry Hub a
third, the latter now this report's worst-performing series. A claimed
Barclays PayPal downgrade was investigated and found fabricated, dropped
entirely. The ECB held as expected (not yet promotable to settled); the
BoJ's Oct 29-30 decision had not posted by cutoff, carried to edition 54 as
live; Riksbank's next-decision date resolved directly. First draft ran a
genuine 6 pages; converged to 4 after deleting the forced break and a dozen
rounds of trimming/citation-merging (54 sources to 41), surfacing a new CSS
multi-column pagination lesson documented under Production notes. **Edition
54 (Mon 2 Nov, covering Fri 30 Oct, a weekend-gap edition):** a tech-led
selloff dropped the major indices broadly (S&P -1.82% to 7,580.07, Nasdaq
-2.86% to 25,437.00, worst session since June) on Intel's historic -28.58%
collapse to $65.76 (worst day since 1974) following a weak Q4 guide despite
beating Q3; Nvidia -4.22% the single largest index-point drag. A record
approx. $6.3bn Binance hack (the largest exchange hack on record, reportedly
tied to North Korea's "TraderTraitor" group) roiled crypto-adjacent names:
Coinbase -10.62%, Strategy -7.84%, Bitcoin below $77,000. Two long-running
Asia threads resolved the same session: the BoJ held its rate at approx.
1.25% (8-1 vote, dissenter Takata Hajime), and China's October PMI slipped
back below 50 on both gauges (manufacturing 49.3, non-manufacturing 49.7).
Four previously-pending earnings reports (Chevron, Exxon Mobil, AbbVie,
Newell Brands) all beat and rose; a fresh CFTC CoT report (covering Tuesday
27 October) powered the third positioning chart. The VIX complex jumped
sharply (+12.91% to 19.42) but stayed in clean contango, both known CBOE
feed bugs present on all six series. The gold/silver vendor-revision trap
continued a fourth consecutive edition; Henry Hub remained unresolved for a
fourth consecutive edition. The November monthly settled-facts audit
completed cleanly across all ten central-bank rows. First draft ran 5 pages
on a single orphaned Section 6 bullet spilling alone onto page 4 with the
forced break still present; deleting the break converged to a clean 4 pages
on the next render. A proactive `grep -n '</td><sup'` caught and fixed three
table-markup-trap instances before rendering. 44/44 sources clean after one
fix; zero stray tildes.

**Edition 55 (condensed)** — Tuesday 3 November 2026 report covering Monday
2 November 2026 (the window's one NYSE session). Equities diverged sharply
on composition: the Dow rose 0.41% to 51,983.98 (a third straight advance)
while the S&P 500 fell 0.51% to 7,541.40 (lowest close since 31 July) and
the Nasdaq fell 1.07% to 25,164.32; 8 of 11 sectors closed higher but
Technology (-2.95%) and Energy (-3.96%), both cap-weighted-index-heavy,
dragged the headline indices down. Crude collapsed 7-11% on an Iran/US
diplomatic-thaw signal (WTI -7.40% to $96.42, Brent -10.94% to $104.77,
wire coverage separately describing "more than 7%" for Brent, a disclosed
methodology discrepancy). Apple's fiscal Q4 2026 earnings (revenue $114.5bn
+12% y/y, EPS $2.10 +14% y/y) were confirmed directly against its own SEC
8-K; shares fell 1.83% regular / 2.75% further AH on a soft, secondary-
sourced margin outlook. Intel extended its collapse a further -8.80% to
$59.97; Oracle fell -8.76% on a disclosed $20bn AI-capex raise; Marvell
agreed to acquire Lumentum in an all-stock deal (Marvell -12.72%, Lumentum
-18.59%, with same-day downgrades from BofA and Stifel) — notably, an
unsubstantiated Marvell-Lumentum deal-talk rumor had been explicitly
rejected as unverified at edition 53, becoming real four sessions later.
Palantir beat-and-raised yet fell -3.13% regular/-2.98% AH, the latest
"beat-and-raise guarantees nothing" instance. Crypto-adjacent names
continued absorbing the prior Friday's Binance hack: Coinbase -3.98%,
Strategy +0.19%, Bitcoin around $77,000. BoJ's and SNB's next-meeting dates
both resolved directly (17-18 Dec and 10 Dec respectively); the ECB's rate
complex was promoted to SETTLED after a third consecutive direct
reconfirmation. DXY's true spot succeeded via Yahoo Finance for the first
time in four editions (101.81) but disagreed on direction with a
futures-proxy/UUP — disclosed, not resolved, a conflict that recurred at
edition 56. The gold/silver/copper/FX vendor-revision pattern that had hit
for four straight prior editions did not recur; Henry Hub remained
unresolved for a fifth consecutive edition (later broken at edition 56). The
CBOE VIX feed's two known bugs were absent on all six series for the first
time in recent memory (also true again at edition 56). VIX jumped +8.91% to
21.15 with a genuinely kinked term structure (backwardation inside 30 days)
that persisted into, and partially narrowed at, edition 56. December FOMC
hike odds firmed to approx. 72-73% (from approx. 70%) per Polymarket's
Gamma-API and DeFi Rate. No shutdown in effect, H.R. 6500 reconfirmed
through 11 December 2026. The RBA's own decision (due just after this
edition's cutoff) had not posted as of the window close, landing instead
inside edition 56's window, where it delivered a 6-3 split hike to 4.85%.
First draft converged cleanly to 4 pages with the forced break retained;
41/41 sources clean after two fixes; zero stray tildes; zero `</td><sup`
instances.

**Edition 56 (most recent — full detail)** — Wednesday 4 November 2026 report
covering Tuesday 3 November 2026, research window Mon 2 Nov 2026 20:00 ET
through Tue 3 Nov 2026 20:21 ET (the window's one NYSE session).

**Equities diverged on composition, not breadth, a continuation of Monday's
pattern.** The S&P 500 rose 0.36% to 7,568.92 and the Nasdaq Composite rose
0.83% to 25,372.01, powered by a megacap/AI bounce (Nvidia +2.29%, Oracle
+5.85%, Arista Networks +3.52%, Super Micro +3.12%) — even as the Dow fell
0.38% to 51,786.72 and AP's own wire (via the La Nación mirror, a third
consecutive success) noted most S&P 500 constituents actually declined on
the session. The Russell 2000 added 0.23% to 2,812.45. Only 4 of 11 SPDR
sector ETFs closed higher: Technology (+1.31%), Communication Services
(+1.18%) and Industrials (+0.95%) led, Real Estate was roughly flat
(+0.07%); Consumer Staples (-2.07%) and Materials (-2.01%) led decliners
with no single dominant driver identified for either despite a targeted
search.

**The Reserve Bank of Australia delivered its fifth hike of 2026** — 25bp to
4.85% — but for the first time this cycle on a split vote, 6-3, confirmed
directly against rba.gov.au's own Media Release 2026-30. The prior four 2026
hikes were all unanimous; the RBA's next decision date is not yet confirmed
(Annex B).

**AMD's fiscal Q3 2026 results were the session's headline earnings story
and a genuine counter-example to this report's "beat-and-raise guarantees
nothing" pattern.** Revenue $13.4bn (+45% y/y), non-GAAP diluted EPS $2.09,
Data Center revenue +97% y/y, Q4 guide raised to approx. $17bn — all
confirmed directly against AMD's own SEC Form 8-K. AMD's regular-session
close of $483.90 (+3.65%) predated the release (reflecting the broader AI
rally); shares then added a further approx. 5.02% after hours to $508.20 —
a genuinely positive beat-and-raise reaction, unlike Apple, Oracle and
Palantir's muted-to-negative reactions to their own recent reports the same
week. Coinbase (+5.53%) and Strategy (+3.72%) partly retraced Monday's
Binance-hack-driven selloff as Bitcoin held little changed around $77,000.
Apple fell a further 1.90% to $331.90, extending Monday's post-earnings
decline; Palantir continued fading (-1.65%); Intel (+0.97%) and Marvell
(+0.33%) broadly stabilized with no fresh Tuesday-specific catalyst
identified. A claimed Oracle analyst-upgrade note was investigated and
rejected as unreliable (internally inconsistent timestamps, a non-existent
firm name) — excluded from the briefing.

**Several standing sourcing gaps resolved or improved this edition.** The
Bank of England's 5 November decision date was upgraded to primary-sourced
(bankofengland.co.uk) from secondary-only. Henry Hub natural gas finally
reconciled cleanly across two independent sources (Investing.com, Yahoo
Finance) after five straight failed editions — not yet closed as a thread,
watch for a second consecutive clean edition. The VIX feed's two known bugs
were absent for a second consecutive edition. Oil stabilized after Monday's
crash (WTI +0.13%, Brent -1.12%). Gold/silver showed a mild (approx.
0.3-0.4%) vendor-data variance on the re-fetched Monday baseline, disclosed
as minor rather than a full recurrence of the larger pattern seen at
editions 50-54; separately, Kitco spot and Investing.com futures agreed
closely on Tuesday's price level for both metals but disagreed on the sign
of the day's change, a disclosed, unresolved conflict. The DXY
Yahoo-Finance-vs-Investing.com-futures-proxy direction conflict persisted a
second straight edition. A carried planning assumption that Caterpillar
would report earnings 4 November was found and corrected before publication
via Caterpillar's own 8-K — it had already reported 29 October.

**Rate-path odds firmed further**: Dec FOMC hike odds approx. 74-75% (from
approx. 72-73% at edition 55) per a direct Polymarket Gamma-API pull (a
third consecutive success) and DeFi Rate's blended aggregator; DeFi Rate's
own internal Kalshi inconsistency persisted a tenth straight edition but
stayed narrow. Kalshi direct failed again (HTTP 429, twentieth consecutive
failure); CME FedWatch direct timed out again (sixteenth consecutive
failure). No shutdown in effect, H.R. 6500 reconfirmed through 11 December
2026. Riksbank's current rate value remained unconfirmable directly for a
third straight edition; its 4 November decision lands inside edition 57.
Banxico's rate and next-decision date remained unconfirmed; a new secondary
detail suggested the rate's last change was a 25bp cut around 7 May 2026.

**Format:** no correction box (nothing from a prior edition found wrong).
First draft converged cleanly to 4 pages with the forced break retained
(sections 1-6 ended within page 3; page 4 had some unused space at the
bottom, not filled, since the content was already precise and complete).
29/29 sources clean on check_refs.py after one fix (a reserved-but-unused
Annex C entry was deleted rather than force-cited); zero stray tildes after
one fix (a snap-grid tile's literal `~` was caught by the pre-render grep
and swapped for "approx."); zero `</td><sup` instances found on a proactive
grep.

**Open threads for edition 57.** Edition 57 covers **Wednesday 4 November
2026**. Watch directly rather than assuming: **the Riksbank's decision**
(due approx. 9:30 CET Wed 4 Nov, lands inside this edition's own window;
confirm the actual outcome against riksbank.se, and try yet another URL path
for the current rate value given three straight prior failures);
**Qualcomm's FQ4/FY2026 earnings** (after Wednesday's close); **October's
ISM Services PMI** (also due Wednesday 4 Nov, no consensus figure found yet
— try again closer to release). Retry at edition 57: confirmation that Henry
Hub's edition-56 reconciliation holds a second consecutive clean edition
before downgrading its priority; a second, different source (not
MarketWatch, blocked by tooling at edition 56) to help resolve the
DXY-vs-futures-proxy direction conflict, now two straight editions
unresolved; Banxico's rate/next-decision date via yet another URL path; the
RBA's own next-decision date (unconfirmed as of edition 56). The La Nación
AP-wire-mirror approach and the Polymarket Gamma-API approach are both now
on three-edition clean streaks — use them first rather than their respective
fallbacks.

**Still open and unchanged:** Brent crude's Friday 23 October close remains
a three-way split ($116.72/$111.70/$113.17), not re-attempted since edition
53; the ECB's exact next-meeting date (unconfirmed, estimated mid-December
by cadence) and its press-conference-content/vote-split sub-question (404,
not re-attempted); Equifax's unexplained multi-session pullback (declining
urgency, not re-checked at editions 55 or 56); New Mexico v. Meta's formal
notice of appeal (unconfirmed for an eleventh straight edition, 47-56); the
"preview-consensus-only miss/beat framing" caution (dormant since edition
41); the DOL weekly jobless-claims parsing problem (not re-attempted); the
federalregister.gov search-interface block (not re-tested this edition
either). Options implied-vs-realized and single-stock flow/skew remain
low-yield, now a nineteenth-plus largely-empty edition on that sub-item.
Kenvue's apparent 2 Nov delisting (consistent with the pending
Kimberly-Clark acquisition) could not be confirmed via a primary filing.
The precise expiry date of the Section 301 exclusions/reciprocal-tariff
suspension remains split between 9 and 10 November 2026 across secondary
sources, and falls inside the very next edition's plausible window to check
directly.

**Dates to hold on to.** Riksbank decision Wed 4 Nov 2026 (lands in edition
57). ISM Services PMI and Qualcomm earnings also due Wed 4 Nov (edition 57).
BoE decision Thu 5 Nov 2026 (expected to land in edition 58). CFTC's next
report and the October US employment report are both due Fri 6 Nov 2026
(expected edition 59). 13F filings are due approx. 14 November 2026 (a
Saturday) — the natural lead item for whichever edition covers the following
Monday, 16 November 2026, now under two weeks out. Veterans Day (Wednesday
11 November) needs the same "equities-open, bonds-closed" check Columbus Day
received, once it is inside a window. The next monthly settled-facts audit
falls on the first edition of December 2026.
