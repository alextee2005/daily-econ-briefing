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
  applied correctly for thirty-seven straight editions (33 through 59) —
  treat as settled; edition 59 read "Monday 9 November 2026" as the date
  line, covering the Friday 6 November session (plus the weekend) in the
  window line.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 59 all reused the
  same pattern — now confirmed clean across thirty-one consecutive editions;
  edition 59 phrased it "Window: Thu 5 Nov 2026 20:00 ET – Sun 8 Nov 2026
  20:21 ET (Fri 6 Nov close/AH, the window's one NYSE session, plus the
  weekend)." No further confirmation needed; treat this as settled.

## Schedule
Run every weekday. Pick the trigger's local time so the effective research
cutoff lands roughly 4 hours after the US market close (20:15 ET) — during
US daylight time that's 00:00 UTC; adjust for standard time. **US daylight
time ended Sunday 1 November 2026, as scheduled — now a resolved, settled
transition, not a forward-looking watch item.** Edition 54's own window closed
at 2026-11-01 20:21 ET, which converts to 2026-11-02 01:21 UTC — consistent
with EST (UTC-5) already being in effect; editions 55 through 58's window
closes (2026-11-02 20:21 ET → 2026-11-03 01:21 UTC; 2026-11-03 20:21 ET →
2026-11-04 01:21 UTC; 2026-11-04 20:21 ET → 2026-11-05 01:21 UTC; 2026-11-05
20:21 ET → 2026-11-06 01:21 UTC) all confirm the same conversion again, now
five straight. **From edition 54 onward, use EST (UTC-5) for all ET/UTC
conversions** until DST resumes — conventionally the second Sunday in March
(expected March 2027; this specific future date is a general calendar
convention, not yet independently verified, so don't cite it as a confirmed
fact until closer to the event). On Mondays (or after any gap), cover the
full window back to the previous edition's cutoff, including the weekend.

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
  research would surface anyway. Entries below marked SETTLED are done;
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
value (page 404'd at the time, only its next-decision date was primary-sourced)
and Banxico (site unreachable, secondary-sourced only) — both remained flagged
as such through edition 56. **Riksbank's rate-value gap was resolved at
edition 57 by a genuine rate change**, not merely a successful re-fetch of the
old level — see the dedicated bullet below. **Banxico's rate itself was
likewise resolved by a genuine rate change at edition 58** (a surprise cut),
though it remains secondary-sourced in terms of confirmation tier — see the
dedicated bullet below. **The next monthly audit falls on the first edition
of December 2026** — whichever edition covers the first NYSE session on or
after 1 December 2026; no specific edition number is estimated this far out
given holidays and potential gaps.

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
  edition 53 and were not re-attempted at editions 54-58 — stale news now,
  not worth a dedicated search. Blackout (Oct 17-29, 2026) held clean through
  the decision, as expected. **Next meeting: 8-9 December 2026, an SEP
  meeting.**
- **Rate-path odds — reversed sharply back at edition 59, undoing almost all
  of edition 58's swing.** A fresh Polymarket Gamma-API pull
  (`gamma-api.polymarket.com/public-search`, snapshot 9 Nov 2026 01:25 UTC)
  put December 8-9 odds at **approx. 76.5% hike / 22.5% no change / approx.
  1.5% cut** — snapping back from edition 58's approx. 66.5% hike read, which
  itself had been a sharp one-edition easing from approx. 77-80% at edition
  57. **DeFi Rate's blended Kalshi/Polymarket aggregator refreshed past its
  stale late-September snapshot for the first time** (snapshot 8 Nov 2026
  20:24 ET): 77% hike / 23% hold, with its own Kalshi-only daily history
  showing the reversal happening Friday itself (approx. 64.5% hike Wed/Thu
  &rarr; approx. 77.5% Fri &rarr; approx. 76.5% Sat) — the proximate driver
  was Friday's much-stronger-than-expected October payrolls print (see the
  dedicated jobs-report bullet below), not a reversal of Thursday's own
  selloff dynamics. **Kalshi's own direct fetch failed again at edition 59 —
  HTTP 429 (rate-limited) again — now TWENTY-THREE consecutive failures
  (37-59).** CME FedWatch also failed again directly (timeout), a
  **NINETEENTH** consecutive failure (41-59). The composite "at least one
  more hike in 2026" read has still not been freshly re-pulled since edition
  38 (last known approx. 80%) — don't cite without a fresh pull. **Given that
  this is now a full round-trip within two editions, a fresh read at edition
  60 is again a priority, not routine upkeep** — confirm whether approx.
  76-77% holds, extends further, or eases again.
- **US-China "30-for-30" tariff framework — remains a closed thread, do not
  re-open absent a genuine dated Federal Register filing.** Resolved at
  edition 37 (framework) and edition 47 (implementation-notice sub-question:
  no effective date, no set timeline, none imminent). No new development was
  found at editions 54-59 either (light-touch checks only); the
  federalregister.gov search-interface block (302-redirect to
  `unblock.federalregister.gov`, logged at edition 48) was re-tested directly
  again at edition 59 and remains blocked — govinfo.gov continues to be the
  working mirror. Separately: secondary reporting (a Thomson Reuters
  regulatory-insight piece) describes a Busan truce extension to **10 January
  2027**, but this remains **NOT confirmed via any published Federal Register
  notice** as of edition 59 — treat the January 2027 date as
  reported-not-verified, not settled law, if cited. **The separate
  reciprocal-tariff suspension / Section 301 exclusion question for 178
  Chinese products, substantially resolved at edition 57, gained a new
  wrinkle at edition 59: the Federal Register notice itself (Doc 2025-21671,
  govinfo.gov mirror) is internally inconsistent about its own lapse date.**
  Its DATES section states the 178 exclusions lapse at **11:59pm ET on
  Monday 9 November 2026**, while its own background narrative, and a
  separate USTR press release, both instead say the exclusions are "extended
  until **November 10, 2026**" — the same notice gives two different dates.
  No new USTR extension had been filed as of edition 59's window close (Sun
  8 Nov 20:21 ET, before either stated lapse moment). **Both candidate
  lapse moments (11:59pm ET Monday 9 Nov, or effectively Tuesday 10 Nov)
  fall after edition 60's own cutoff (around 8:15pm ET Monday), so this
  places the lapse itself, and the rate-resumption's visible effect, both
  inside edition 61's window (covering Tuesday 10 Nov), not edition 60's**
  — check federalregister.gov/govinfo.gov and
  ustr.gov directly for any last-minute extension filing, and note which of
  the two dates the notice ultimately treats as operative.
- **Fed Chair: Kevin Warsh — SETTLED, stop re-verifying it every run.** No
  contradiction surfaced through edition 58; **directly re-confirmed via
  federalreserve.gov's own bios page at edition 54's November monthly
  audit**, closing that housekeeping item cleanly; not re-attempted at
  editions 55 through 58 (settled, no fetch needed). His Chairman term ends 21
  May 2030 (took office 22 May 2026, a four-year term); his separate term as a
  Board of Governors member runs to 31 January 2040. The Chairmanship
  re-opens as a live fact only on a successor nominated/confirmed, a
  resignation or removal, or that 21 May 2030 term-end date actually arriving,
  or the **next monthly audit (first edition of December 2026)**.
- **The 3 November 2026 US midterm elections — still LIVE, certification
  status not confirmed at edition 59 either, watch again.** Democrats
  won control of both the House and Senate — called by AP/CNBC/NBC/PBS by
  Wednesday 4 November morning — ending unified Republican control of
  Washington. Democrats flipped at least seven Senate seats (Iowa, Kansas,
  Ohio, North Carolina, New Hampshire, South Carolina, Texas); a handful of
  races were still uncalled as of edition 57's cutoff and this was not
  independently re-checked at editions 58 or 59 — do not cite a final seat
  count without re-checking. **The election's second-order market effect
  dominated edition 58's own session**: Tuesday's local ballot measures
  rejected data-center buildouts in 40 of 41 votes, and UBS flagged approx.
  30% of 2028 data-center capacity additions as at risk under the incoming
  Democratic Congress — this drove Thursday 5 November's broad AI-capex
  selloff (S&P -4.4%, Nasdaq -5.5% into correction territory, VIX +69.66% to
  28.18), a near-complete reversal of Wednesday's election-rally session.
  **The semiconductor complex partly recovered at edition 59's own session**
  (Friday 6 Nov) on no fresh company-specific news, consistent with a
  reaction to the same underlying story rather than a resolution of it.
  **Re-verify certification status and watch for any further policy response
  (fiscal, trade, AI/data-center regulation, Iran) in the next several
  editions' macro passes** — a dedicated search at edition 59 again found
  only pre-certification, still-provisional vote-count reporting, with no
  official certification news either way.
- General principle for everything still live: do not assume a routine
  macro-calendar fact (meeting dates, symposium schedules, other central
  banks' policy rates, government funding status) from memory or from the
  prompt's own framing — verify it fresh from a primary source
  (federalreserve.gov, bankofengland.co.uk, boj.or.jp, kansascityfed.org,
  norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, rba.gov.au,
  ecb.europa.eu, bankofcanada.ca, whitehouse.gov, etc.) every edition, exactly
  like any other data point, until an entry below is marked SETTLED. These
  are the rates and dates that feed Section 3's policy-rate table, so the
  table is the natural place to land them. Per-bank status as of edition 58:
  - **Reserve Bank of Australia:** current rate **4.85%**, hiked 25bp on
    Tuesday 3 November 2026 (6-3 split vote, its fifth hike of 2026) —
    SETTLED pending the RBA's own next decision, **7-8 December 2026**
    (confirmed directly at edition 57 against rba.gov.au's own meeting-dates
    release). Not re-attempted at edition 58 (no fetch needed, date stands).
    No further action needed until 8 Dec.
  - **Bank of England — MAJOR UPDATE at edition 58, the decision long flagged
    as pending now resolved.** Confirmed directly against
    bankofengland.co.uk's own Monetary Policy Summary and minutes
    (November 2026): the MPC raised Bank Rate **25bp to 4.00%** on Thursday 5
    November 2026 — its first hike since August 2023 — on an **8-1 vote**
    (Bailey, Breeden, Dhingra, Greene, Lombardelli, Pill, Ramsden, Taylor for
    +25bp; Catherine Mann dissenting in favor of +50bp; zero votes to hold).
    Cited driver: Middle East-conflict energy-supply disruption pushing
    headline inflation (currently 3.5%) toward a forecast approx. 5% by
    mid-2027. Governor Bailey: the hike "shouldn't be seen as the first in an
    inevitable long sequence," further moves possible "unless the conflict in
    the Middle East is resolved"; MPC member Alan Taylor called it a
    "one-for-now" insurance hike. **Next decision: 17 December 2026**,
    confirmed on the same page. The rate and next-decision date are both now
    SETTLED pending that meeting.
  - **European Central Bank — the one open sub-question closed at edition
    59.** Rate complex (deposit facility 2.50%, main refi 2.65%, marginal
    lending 2.90%) remains **SETTLED** (promoted at edition 55 after a third
    consecutive direct reconfirmation) — not re-attempted at editions 56
    through 59 (no fetch needed). It reopens on contradiction, the next
    Governing Council decision, or the monthly audit. **The Council's own
    next-meeting date, previously only an estimated "mid-December" guess,
    was confirmed directly against ecb.europa.eu at edition 59: 16-17
    December 2026** — now SETTLED alongside the rate, pending that meeting.
    The press-conference-content/vote-split sub-question from the 28-29
    October meeting remains unobtainable and was not specifically
    re-attempted at edition 59 (out of scope, low priority).
  - **Bank of Japan:** current rate approx. 1.25%, SETTLED pending its own
    next meeting. Next decision 17-18 December 2026, confirmed directly
    against boj.or.jp at edition 55 — not re-attempted at edition 56, 57 or
    58 (no fetch needed, date stands).
  - **Bank of Canada:** SETTLED. Current rate 2.50%, hiked 25bp 28 October
    2026. Next decision 9 December 2026 (same date as the Fed's) — not
    re-attempted at edition 56, 57 or 58 (no fetch needed, date stands).
  - **Swiss National Bank:** current rate 0.00%, SETTLED (effective, most
    recent assessment 24 Sept 2026). Next assessment 10 December 2026,
    confirmed directly against snb.ch at edition 55 — not re-attempted at
    edition 56, 57 or 58 (no fetch needed, date stands).
  - **Norges Bank:** current rate 4.50% (unchanged since 24 Sept 2026), next
    decision 17 December 2026 — both SETTLED, reconfirmed directly at edition
    54's monthly audit; next re-verification due at the December monthly
    audit.
  - **Riksbank:** current rate **2.00%**, hiked 25bp on Wednesday 4 November
    2026 (its first hike since 2023), confirmed directly against
    riksbank.se — SETTLED pending the next decision, **16 December 2026**
    (inferred from the Riksbank's own confirmation that its next Monetary
    Policy Report is due that date, not an explicit "next decision" label —
    high-confidence but not pixel-perfect primary sourcing). **The vote
    split/dissent from the 4 Nov decision remained unresolved at edition
    59** — minutes, due **10 November 2026**, had not posted as of edition
    59's window close (Sun 8 Nov 20:21 ET), consistent with the due date
    falling after that window — likely landing inside **edition 61's**
    window (covering Tuesday 10 Nov) rather than edition 60's (Monday 9
    Nov) — treat the vote detail as a live open sub-question until then.
  - **Banxico — rate itself settled by the edition-58 surprise cut;
    sourcing tier unchanged at edition 59.** Per consistent multi-outlet
    Mexican financial press (Milenio, El CEO, Exc&eacute;lsior-affiliate,
    PorEsto, Grupo Animal, Almomento, Uno TV, Zeta Tijuana, Bloomberg
    L&iacute;nea), Banxico **cut its overnight interbank rate 25bp, from
    6.50% to 6.25%**, decision dated 5 November, effective 6 November 2026,
    against a consensus expectation of a hold — a **3-2 vote**, Deputy
    Governors Galia Borja G&oacute;mez and Jonathan Heath dissenting in
    favor of holding. Headline inflation rose to 3.62% y/y in October (from
    3.42% in September). Minutes due 19 November 2026; **next decision 17
    December 2026** (secondary-sourced, same convergence date as several
    other banks this cycle). **banxico.org.mx failed again at edition 59,
    via a new failure signature**: every path tried (the standard
    policy-rate page, the English boletines page, a guessed PDF path) now
    302-redirects to an "anterior.banxico.org.mx" subdomain, which itself
    returns HTTP 404 — a different failure mode from editions 56-58's
    straight 404/redirect-loop. This remains secondary-sourced only, not
    directly primary-confirmed, for a further edition. Try yet another
    fresh URL path at edition 60.
  - **Government funding/shutdown status:** H.R. 6500 funds federal agencies
    through 11 December 2026, no shutdown in effect — **a direct
    whitehouse.gov fetch did NOT surface funding-related content at edition
    59** (every page checked either 404'd or returned content with no
    mention of funding/CR/shutdown status), a one-edition downgrade from
    edition 58's clean direct confirmation, echoing the same one-edition dip
    edition 57 had before edition 58's success. Carried forward this
    edition on secondary sourcing only (Fox News, NASFAA, and other
    outlets, all consistent). Continue the standard re-check-every-edition
    discipline regardless.
- **SETTLED (historical) — Bank of England held at 3.75% on Thursday 17 Sept
  2026, a 6-3 vote** (same three dissenters as 30 July, all favoring a hike
  to 4.00%). **Superseded by a subsequent decision**: the MPC hiked 25bp to
  **4.00% on Thursday 5 November 2026** (8-1, Mann for 50bp) — see the
  dedicated per-bank bullet above for full detail. The September hold remains
  accurate as a historical record of that specific meeting; it no longer
  describes the current rate.
- **SETTLED (the September decision only) — Bank of Japan hiked 25bp to
  approx. 1.25% on 18 September 2026** (effective 24 Sept), a 31-year high, a
  7-2 vote (dissenters Asada Toichiro and Sato Ayano) — closed thread, do not
  re-derive. **The Bank's SUBSEQUENT 29-30 October 2026 meeting HELD the rate
  at approx. 1.25% (8-1 vote, dissenter Takata Hajime)** — this October
  decision is now itself resolved meeting history and the numeric rate is
  live again only pending BoJ's next meeting, confirmed for **17-18 December
  2026**.
- **SETTLED — the four-central-bank Thursday 24 September 2026 cluster,
  closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% but signalled a greater chance of
  a Q4 hike — a signal that materialized at edition 57 (see dedicated bullet
  above); Banxico held at 6.50% unanimously (since cut at edition 58 — see
  dedicated bullet above); SNB held at 0% and raised its inflation forecasts,
  confirmed directly against snb.ch.
- **SETTLED — the Reserve Bank of Australia's Tuesday 29 September 2026
  decision, closed thread, do not re-open:** hiked 25bp to 4.60%, unanimous,
  a 15-year high and its fourth hike of 2026, confirmed directly against
  rba.gov.au. **SETTLED — the RBA's Tuesday 3 November 2026 decision, also
  now closed thread, do not re-open:** hiked a further 25bp to 4.85%, its
  fifth hike of 2026, this time on a split 6-3 vote (first split vote this
  cycle), confirmed directly against rba.gov.au's Media Release 2026-30. The
  current numeric rate and the RBA's next decision date (7-8 Dec 2026) are
  both now SETTLED pending that meeting — see the dedicated per-bank bullet
  above.
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
  Situation Summary. **October 2026's jobs report — RESOLVED at
  edition 59, closed thread, do not re-derive:** nonfarm payrolls
  **+165,000**, a 100,000 upside surprise against a FactSet-polled median
  consensus of **+65,000** (found this edition after three prior failed
  attempts at editions 55, 57 and 58) and a median unemployment-rate
  forecast of 4.2%; unemployment held at **4.1%**; average hourly earnings
  **+0.4% m/m / +3.1% y/y**; August revised up 53,000 (to +186,000) and
  September revised up 31,000 (to +60,000), a combined +84,000 —
  confirmed directly against bls.gov's Employment Situation Summary,
  released 6 November 2026, 8:30am ET. This print was the proximate driver
  of edition 59's sharp rate-odds reversal (see the dedicated Standing
  Facts bullet above).
- **September 2026 ISM Services/Non-Manufacturing PMI — closed thread as of
  edition 35, do not re-derive:** headline 54.9% (down from August's 55.4%),
  Prices Paid 74.0% (+1.4pt, highest since July 2022). **October's ISM
  Services PMI — RESOLVED at edition 57:** headline **54.5%**, below the
  **54.8%** consensus/forecast and a third straight month without
  acceleration, confirmed via Investing.com's Economic Calendar. Sub-index
  detail (Prices Paid, New Orders, Employment) remains an Annex B item, not
  re-attempted at edition 58.
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
  +11.6% y/y**. Released Friday 16 October 2026, confirmed directly against
  bls.gov.
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
  and equipment spending. Released Thursday 29 October 2026, confirmed
  directly against bea.gov. No independently-confirmed consensus figure was
  found. Next release (2nd estimate + corporate profits): 25 November 2026.
- **September 2026 PCE / core PCE — closed thread as of edition 53, do
  not re-derive:** headline **+0.5% m/m / +3.6% y/y**, core **+0.3% m/m /
  +3.1% y/y** — both well above the Fed's 2% target. Released in the same
  8:30am ET slot as Q3 GDP on Thursday 29 October 2026, confirmed directly
  against bea.gov.
- **No US federal government shutdown is in effect — re-confirmed cleanly and
  directly against whitehouse.gov at edition 58.** H.R. 6500 funds federal
  agencies through **11 December 2026**. Watch for shutdown risk resurfacing
  as that date approaches.
- **University of Michigan October 2026 consumer sentiment — CLOSED thread as
  of edition 49, both preliminary and final readings in hand:** preliminary
  46.3 (a five-month low); **final 48.0** (vs. September's final 48.1 and the
  approx. 47.6 consensus). Final sub-indices: current conditions 46.7,
  expectations 48.8; year-ahead inflation expectations 4.7%, long-run 3.5%.
  The final reading remains secondary-sourced only.
- **China September 2026 CPI/PPI — RESOLVED, closed thread, do not
  re-derive:** CPI **+0.9% y/y** (+0.2% m/m), PPI **+5.0% y/y**. **China's
  October 2026 PMI** (resolved at edition 54): manufacturing PMI **49.3**
  (down from September's 50.1) and non-manufacturing PMI **49.7** (down from
  50.2) — both back below the 50 threshold.
- **China Q3 2026 GDP — RESOLVED at edition 45, closed thread, do not
  re-derive:** printed Monday 19 October 2026. Q3 alone: **+4.5% y/y, +1.2%
  q/q**; first-three-quarters 2026 cumulative: **+4.6% y/y** (GDP RMB
  107,107.1bn).
- **New Mexico v. Meta — the $25bn civil-penalty ruling (Judge Francis
  Mathew, Wed 21 Oct 2026) remains substantially clarified but Meta's formal
  notice of appeal is still unconfirmed for a FOURTEENTH straight edition
  (47-59).** Meta owes **$25bn** in civil penalties for the jury's
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
  re-attempted at editions 55 through 59 (out of scope); no new development
  in the 48-state settlement or the Unfair Practices Act stay.
- **New calendar-awareness item, reconfirmed relevant across several
  editions: "equities-open, bonds-closed" US holidays need an explicit check
  every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. **Veterans Day, Wednesday 11 November 2026, was independently
  verified at edition 57 and follows the same pattern:** SIFMA's own 2026
  holiday schedule confirms a full bond-market close that day, while
  NYSE/Nasdaq trade their regular session — this item is now resolved/closed
  for Veterans Day 2026 specifically; no further action needed unless a
  future edition's window reaches a different holiday. **The DST transition
  (ended Sunday 1 November 2026) is now itself resolved/settled** — see the
  Schedule section above.
- **The vendor-retroactive-revision trap hit harder at edition 59 than at
  edition 58 &mdash; four of seven tracked commodity/FX series showed a
  revised Thursday base on fresh re-pull.** WTI's own Thursday figure moved
  from the logged $91.26 (+3.56%) to a freshly re-pulled $90.52 (+2.72%)
  &mdash; direction unchanged but both price and magnitude shifted, leaving
  Friday's own day-over-day direction ambiguous depending which base is used
  (Friday's $90.83 is +0.34% against the fresh base, -0.47% against the
  original). Gold futures' Thursday figure moved from $4,095.85 (+0.56%) to
  $4,113.50 (+0.99%, magnitude only). **Silver futures' Thursday figure
  flipped sign outright**, from the logged $51.730 (-1.06%) to a freshly
  re-pulled $52.376 (+0.18%) &mdash; the most severe single-series revision
  logged to date. COMEX copper's Thursday figure moved from $6.2295 (-3.10%)
  to $6.2700 (-2.47%, magnitude only). By contrast, **Brent, EUR/USD,
  GBP/USD, USD/JPY and Treasury yields all reconciled cleanly against their
  logged Thursday bases with no revision.** Keep the every-edition
  re-fetch-and-compare discipline regardless; report each instrument's
  current Friday figure against the vendor's own current numbers, with any
  revision disclosed rather than hidden.
- **Henry Hub: now a FOURTH consecutive clean two-source reconciliation at
  edition 59 &mdash; this thread stays substantially closed.** Edition 59
  found Investing.com's Friday close ($2.998/MMBtu, +1.73%) and Yahoo
  Finance's NG=F close (also $2.998) matching almost exactly. Still NGZ6
  (December); no roll to NGF7 (January) yet as of Friday 6 Nov. Continue
  occasional spot-checks rather than a dedicated every-edition
  reconciliation effort unless a fresh conflict appears.
- **westmetall.com (LME copper) &mdash; the edition-58 missing-row question
  is now RESOLVED at edition 59: a one-off publication lag, not a new
  recurring problem.** Both Thursday 5 Nov (cash $14,110.00/t, 3-month
  $14,030.00/t) and Friday 6 Nov (cash $13,955.00/t, 3-month $13,780.00/t)
  rows are now posted, with the previously-confirmed Wednesday 4 Nov figure
  ($14,201.00/$14,095.00) unchanged on re-check. Resume treating this as the
  standing primary source without a dedicated watch item; the COMEX
  cross-check (Investing.com) remains available as a fallback whenever LME
  itself lags.
- **New sourcing-mechanics trap logged at edition 50, relevant to any
  Monday-dated (or any day-after-a-non-trading-day) edition: Investing.com
  inserts an electronic Sunday-evening re-open print as its own row for every
  24-hour-traded instrument.** Not applicable at edition 59 either (Friday
  followed a normal weekday, Thursday) — continue applying this discipline
  on every post-weekend or post-gap edition; edition 60's window reaches
  back across this past weekend's close-to-reopen gap for 24-hour
  instruments, so check it there.
- **The Kitco live-spot-vs-headline cross-check hit a NEW failure mode at
  edition 59: total inaccessibility, not just a conflict.** Both canonical
  historical-close URLs (`kitco.com/charts/livegold.html`,
  `/livesilver.html`) now 302-redirect to live-quote-only pages with no
  retained close row for any past date; `kitco.com/price/precious-metals`
  likewise shows only a real-time bid/ask. A web.archive.org lookup for a
  cached close was attempted and failed (the fetch tool could not reach
  archive.org). No Kitco spot figure is reported for Friday 6 Nov as a
  result &mdash; see Annex B. This is the fourth distinct problem mode
  logged for this sub-item in four editions (sign conflict at 56, magnitude
  gap at 57, sign-plus-magnitude-plus-internal-baseline conflict at 58, now
  total inaccessibility at 59); keep attempting it fresh every edition, but
  do not assume the historical pages will be reachable.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company, IPO'd 1 July 2026 at
  $29/share. Logged here so a future edition doesn't waste effort
  re-verifying the ticker's legitimacy if it moves sharply again.
- **The "named secondary outlet's own claim can be flatly wrong" trap gained
  THREE new instances at edition 58**, all caught and excluded before
  publication: (1) a widely-circulated DraftKings AH figure (-22.24%, citing
  an EBITDA-guidance cut) had no corresponding 8-K anywhere on EDGAR as of
  cutoff (the company's most recent 8-K on file was dated 25 Sept 2026) —
  dropped entirely, DraftKings' confirmed regular-session close (+1.77%) used
  instead; (2) a secondary aggregator attributed Natera's AH decline to "a
  new CEO" — no such disclosure exists in Natera's own 8-K, claim dropped;
  (3) a circulating "Thursday's biggest calls" analyst-action list had
  essentially every individual claim spot-checked and found unsupported or
  contradicted by verifiable rating history — the entire list was omitted
  rather than any part of it repeated. Prior flatly-wrong instances remain
  logged: JetBlue (edition 50, magnitude), Carvana/Barron's (edition 52,
  direction/framing), Tesla and NU Holdings (edition 49, magnitude), Marvell/
  Lumentum and Barclays/PayPal (edition 53), a misdated Reuters-style squib
  plus a wrong-year Trefis list (edition 54), Brent crude's disclosed
  settle-to-settle-vs-"more than 7%" methodology discrepancy (edition 55),
  and a claimed Oracle analyst-upgrade note (edition 56). **Edition 59
  added a fourth-edition-running caught instance**: a widely-surfaced
  secondary figure for Friday's index closes (Dow -3.44%, S&amp;P -4.30%,
  Nasdaq -5.52%) was checked against the price-history record and found to
  be a near-exact restatement of Thursday's actual close under Friday's
  date &mdash; the Nasdaq figure (24,315) matched Thursday's confirmed close
  digit-for-digit. Dropped entirely; the AP-wire-mirror figures (S&amp;P
  +0.3%, Dow -0.5%, Nasdaq +1.1%, Russell 2000 +0.9%) were used instead.
- **The edition-49 "forward-looking calendar aggregator" trap (names falsely
  listed as past or future reporters when the actual date differs) remains
  closed as a general pattern.** It gained two fresh instances at edition 57
  (Amdocs' Form 6-K date, Kyndryl's actual filing date), both caught via
  direct SEC EDGAR checks. **Not specifically re-tested at editions 58 or
  59** (no forward-looking aggregator date claim was investigated either
  edition) — resume the discipline whenever a day-ahead calendar entry
  rests on an aggregator's claimed date rather than a primary filing.
- **A megacap multi-name earnings cluster producing genuinely uncorrelated
  reactions is a standing, repeated pattern — now at least TWELVE distinct
  instances through edition 59 (editions 44, 47, 48, 49 x2, 50, 52, 53 x3,
  58, 59).** Edition 58 added a clean new pair: Atlassian fell -15.98% AH
  despite a clean Q1 FY27 beat (revenue +24%, EPS beat), and Natera fell
  -16.15% AH despite revenue +34% and a raised FY26 guide — both
  counter-examples to Cloudflare, JFrog and Airbnb all rising on beats the
  same evening. **Edition 59 reconfirmed the same split into the confirmed
  regular-session close rather than adding a fresh instance**: JFrog's
  beat-driven pop actually extended further (+35.33% confirmed vs. a smaller
  AH indication) and Natera's decline moderated slightly (-14.59% confirmed
  vs. -16.15% AH), but the underlying direction split held. Edition 57 had
  NOT added a new instance (a session where beats rose and misses fell
  across the board); edition 56 added a positive counter-example (AMD).
  Continue treating beat-and-raise (or a guidance cut) as having no
  *guaranteed* effect on the reaction without checking the actual outcome,
  and treating an AH snapshot as unconfirmed until the next regular-session
  close.
- **New production lesson from edition 53: CSS multi-column (`.cols3`/
  `.cols2`) pagination under Chromium print-to-PDF can plateau stubbornly on
  marginal content trims** — see the condensed mega-block below for the
  mechanics and the fix. **Not triggered at editions 54 through 59** —
  edition 59's first draft spilled two Section 6 bullets alone onto page 4
  (five pages); deleting the single forced break converged cleanly to four
  pages on the very next render, the same single-fix pattern as edition 54,
  not the multi-round plateau from edition 53 — further reinforcing that
  edition 53's plateau was content-volume-specific rather than a general
  property of the CSS approach.
- **MAJOR UPDATE at edition 59: both of the VIX feed's known bugs
  (duplicated `prev_day_close`, and a `price_change_percent` that divides
  by the wrong price) RECURRED on all six series, breaking a four-edition
  clean streak (55-58).** The feed's own reported percentages diverged from
  an independently-recalculated manual figure by roughly 1-4 points on
  every series (e.g. VIX: feed reported -9.9064%, true change against
  Thursday's logged 28.18 close is -9.01%). `prev_day_close` was again
  duplicated to equal the current price on all six series, though the true
  prior close remained recoverable arithmetically from `current_price -
  price_change`, which did match the logged Thursday base exactly &mdash;
  so `price_change` itself stayed correct even when `prev_day_close` and
  `price_change_percent` did not. **Continue the manual-calculation
  discipline unconditionally regardless of how many bug-free editions might
  follow** — this is now the second time a clean streak (previously four
  editions, 55-58) has ended without warning.
- **New at edition 54: a markup-correctness self-check caught three
  instances of the `</td><sup` table trap (documented under Production
  notes below) before rendering.** Editions 55 through 59 all ran the same
  proactive `grep -n '</td><sup'` check and found **ZERO instances for a
  fifth consecutive edition** — worth continuing on every edition with a
  table that has an empty trailing cell or a cell containing only a
  citation.
- **New at edition 54: the CFTC Asset-Manager-vs-Leveraged-Funds grouped-bar
  chart was reused for a fifth time (editions 34, 39, 44, 49, 54 — a clean
  Monday/weekend-window pattern) with the same figsize (9.8, 2.15), `h=0.32`
  bar offset and figure-level legend technique documented under Production
  Notes.** **Editions 55 through 59 did not use the chart.** Fresh CFTC
  data (covering Tuesday 3 Nov) did land inside edition 59's window &mdash;
  the first fresh data since edition 54 &mdash; but the session's
  payrolls-beat-and-chip-relief-rally story was judged more dominant; the
  data was summarized in prose/a small table in Section 5 instead (asset
  managers net long and leveraged funds net short in ES by a wide margin
  relative to OI, both cohorts modestly net long in NQ, a more mixed RTY
  picture), consistent with edition 57's and 58's same judgment calls.
  **The next report is due Friday 13 November 2026, covering Tuesday 10
  November data** (the CFTC's planned move to twice-weekly releases still
  has no confirmed start date, so the old weekly cadence held again at
  edition 59) — this falls inside edition 64's plausible window (one
  edition per weekday: 60 Mon 9, 61 Tue 10, 62 Wed 11, 63 Thu 12, 64 Fri
  13); check cftc.gov directly then.

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
  **Editions 54 through 59 have all now converged cleanly within one or two
  renders** (54 and 59 after deleting the one forced break; 55 through 58
  all on the very first render with the break retained, sections 1-6
  ending within page 3 every time) — reinforcing that content density alone
  does not predict whether a trim marathon will be needed; check the actual
  render before assuming one is. Edition 58 remains the strongest
  single-render data point: a double central-bank surprise, a sharp
  FOMC-odds swing, a 0-of-11-sector selloff day, a VIX term-structure
  inversion and a 12-plus-name earnings cluster all converged on the first
  render. Edition 59's two-bullet spillover onto page 4, fixed by the usual
  break-deletion, was the more common pattern.
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
  potentially-misleading citation, or to cite the single shared source if
  all values genuinely share one (edition 58's movers chart used `[3]`,
  the shared SEC-filing/market-pricing citation, since all seven values used
  the same method). **Also watch for a stray bracket typed outside a
  `<sup>` tag entirely** — `check_refs.py` will not flag it since its regex
  only matches inside `sup class="ref"` tags, so a bare `[n]` slips through
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
  `check_refs.py` only checks presence/absence, not uniqueness of use;
  edition 58 did this deliberately for source [3] (SEC EDGAR filings
  cross-checked against market pricing, reused across all seven movers-table
  rows and the movers chart) and [10] (Investing.com, reused across WTI/
  Brent/Henry Hub/gold/silver futures/COMEX copper/the DXY proxy) — both
  caught cleanly by `check_refs.py` with no issue. **Citing the prior
  edition itself as a source** (e.g. "logged prior-session baseline
  figures," or re-citing a prior edition's own already-primary-confirmed
  fact) is a legitimate, already-used pattern — edition 58 used this for the
  Qualcomm AH-snapshot-supersession note in Annex A, citing "Daily Economic
  Briefing, edition 57" directly.
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
  corrects nothing**, which will be most of them. **Editions 54 through 59
  have all omitted the box** — in each case nothing published in a prior
  edition was found to be wrong. (Edition 58's own Qualcomm AH-snapshot
  supersession was treated as new information arriving on schedule, not a
  correction, since the prior edition correctly labeled the figure as an
  unconfirmed snapshot rather than asserting it as a close — consistent with
  how edition 57 itself handled the WTI/vendor-revision items. Edition 59's
  Atlassian/Natera AH-to-confirmed-close updates were treated the same way.)
- **All sector and ETF material belongs to Section 1 — by request since
  edition 49.** Section 1 keeps its snap-grid tiles and recap paragraph and
  gains the sector-ETF chart plus the narration of how each sector did in
  the session. **Section 2 is purely single-stock**: movers chart, movers
  table, earnings, guidance, analyst actions. The test is simple — if a
  sentence is about a sector rather than about a named company, it goes in
  Section 1. **Edition 58 handled the semiconductor-sector-wide decline as a
  Section 2 item** (named companies — Nvidia, AMD, Micron, Marvell, Broadcom,
  Intel — even though the driver was thematic/macro rather than
  individual-company news), consistent with the rule's own test ("about a
  named company" governs, not whether the driver happens to be sector-wide).
  **Edition 59 applied the same test to the complex's relief rally** (same
  six named companies recovering part of Thursday's loss, again on no
  company-specific news) — reinforcing that the test runs on the sentence's
  subject, not the direction of the move or whether the driver is
  thematic. Section 6's "sector setup we take into [session]" bullets stay
  where they are; they are forward-looking, not a recap of what happened.
- **Section 3 carries a central-bank policy-rate table.** Columns: **Central
  bank | Policy rate | Last change | Next decision**. The Fed goes first as
  the anchor to compare against, then whichever of the BoE, BoJ, ECB, SNB,
  Norges Bank, Riksbank, RBA, BoC and Banxico the window actually touches —
  eight to ten rows is the working range. A bank whose current rate could
  not be verified still gets its row, with that cell marked unavailable and
  a matching Annex B entry. **Editions 54 through 59 have all run the same
  full 10-row table** (Fed, BoJ, BoE, ECB, BoC, RBA, SNB, Norges Bank,
  Riksbank, Banxico). **Edition 59 closed the table's last open
  sub-question**: the ECB's next-meeting cell moved from an unverified
  estimate to primary-confirmed (16-17 Dec 2026). Only Banxico's rate and
  next-decision date remain imperfectly (secondary-only) sourced as of
  edition 59 — unchanged from edition 58, still the smallest
  "unavailable/imperfect" footprint this table has carried since it was
  introduced. Follow the usual table convention — plain `<tr>` header rows,
  no `<thead>`.
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
  editions 34, 39, 44, 49, 54). **Editions 55 through 59 did not use a third
  chart.** Fresh CFTC data did land inside edition 59's window (the first
  since edition 54), but the payrolls-beat-and-chip-relief-rally story was
  judged more dominant, continuing the same pattern as 55-58 (a kinked VIX
  term structure at 55, its narrowing at 56, a dramatic one-day collapse at
  57, a full contango-to-backwardation inversion at 58, and a partial
  unwind of that inversion at 59), each time with the
  equity/earnings/macro story judged more dominant and the secondary story
  covered fully in prose instead. Next CFTC report due **Friday 13 November
  2026**, covering Tuesday 10 November data — check cftc.gov directly
  whichever edition's window includes it, likely edition 64.
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
  of this rule was found needing a fix at editions 56 through 58 — edition
  58 did cite one aggregate figure (Bloomberg's own "approx. $2tn of market
  value erased" characterization of the Nasdaq's decline), but it was
  directly attributed to Bloomberg's own reporting rather than computed
  in-house, which satisfies the rule rather than violating it.
- Where sources disagree, use the more authoritative one **and** disclose
  the disagreement. AP's "How major US stock indexes fared" and the Reuters
  market wrap are normally the most reliable for index closes — but check
  they're actually indexed for the target date before relying on them.
  **Editions 48 through 53 all found neither wire indexed/fetchable** (with a
  single one-edition exception at edition 51 via a syndicated mirror).
  **Edition 54 found a NEW, cleaner variant of the same workaround: an
  AP-wire mirror syndicated through an international outlet (lanacion.com.ar)
  carried the full wire content and matched two independent US secondary
  sources exactly.** Edition 57 added a second independent mirror (WTOP, a US
  radio-station website). **Editions 55 through 59 have all successfully used
  the dual La Naci&oacute;n/WTOP mirror approach — now SIX consecutive
  successes** (edition 59 used the La Naci&oacute;n mirror alone, successfully).
  This is the established first-choice workaround; try it
  before the Yahoo-Finance-plus-secondary-recap fallback, while still
  re-attempting apnews.com/Reuters directly every edition regardless.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Always check a dated article's own claimed magnitude AND
  direction against the underlying price-history table or primary filing,
  not just its date, before repeating it** — this trap has now hit
  magnitude (J.B. Hunt ed.44, Tesla/NU Holdings ed.49, JetBlue ed.50),
  direction/framing (Carvana/Barron's ed.52), claimed drivers that don't
  hold up (Marvell/Lumentum ed.53; **Natera's "new CEO" claim, ed.58**), a
  claimed analyst action that appears outright fabricated (Barclays/PayPal
  ed.53; Oracle ed.56; **a full "biggest calls" list, ed.58**), the claimed
  DATE/YEAR itself (edition 54's Reuters-squib/Trefis exclusions; edition
  56's Caterpillar date; edition 57's Amdocs and Kyndryl reporting-date
  aggregator errors), a disclosed cross-source percentage-methodology
  discrepancy (edition 55's Brent crude move), **a figure with no
  corroborating primary filing at all (DraftKings' circulated -22.24% AH
  claim, ed.58, excluded entirely rather than hedged)**, and **a wholesale
  stale-date republish (a circulated Friday-dated index-close figure,
  ed.59, that was actually Thursday's own close restated verbatim — the
  Nasdaq figure matched digit-for-digit)** — treat ANY surprising secondary
  claim (price move, driver, analyst action, date, or computed percentage)
  as needing this same verification discipline.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  **Edition 55 exercised this discipline directly on Apple's earnings date;
  edition 56 had no cross-pass disagreement requiring a dedicated
  verification pass; edition 57 exercised it on the session's single biggest
  story (the election outcome and the Riksbank surprise).** **Edition 58's
  macro research pass independently primary-sourced the Bank of England
  decision directly against bankofengland.co.uk (rather than relying on
  secondary wire coverage alone) given how consequential and surprising the
  hike was**, and cross-checked Banxico's cut against six independent
  Mexican outlets given the inability to reach banxico.org.mx directly. This
  discipline is specifically recommended for any edition carrying a
  surprising, highly consequential single finding, not only for cross-pass
  disagreements. **Edition 59 applied it to October's payrolls print**
  (fetched directly against bls.gov's own Employment Situation Summary
  rather than relying on a secondary recap, given it was the session's
  single biggest macro surprise and the proximate driver of the rate-odds
  reversal) and to the Dec FOMC-odds reversal itself (cross-checked against
  both Polymarket's Gamma API and DeFi Rate's refreshed blended
  aggregator).
- **Premarket is not the close, and the close is not the after-hours
  earnings reaction — and an after-hours reaction does not necessarily hold
  into the next regular session, uniformly or at all. A strong beat-and-raise
  does not guarantee a positive reaction even within the SAME session —
  though it does not guarantee a negative one either.** Reinforced at
  essentially every edition since 44; edition 53 remains the
  largest-magnitude same-session negative instance (ServiceNow, -26.95%
  despite a clean beat-and-raise); edition 56 added AMD as a positive
  counter-example. **Edition 58 added a clean new pair the same evening**:
  Atlassian -15.98% AH and Natera -16.15% AH, both despite clean beats,
  while Cloudflare, JFrog and Airbnb all rose on beats the same evening —
  see the megacap-cluster Standing Facts entry above. Always fetch the
  verified close, the after-hours reaction, AND (when the window allows) the
  next regular session's close as three separate, clearly labelled figures.
  A premarket-only figure that cannot be confirmed to have held into the
  regular close should be excluded rather than reported as a close-of-day
  mover — edition 55 excluded EchoStar's premarket approx. +5% read on
  exactly this basis. **Edition 58 extended this discipline to AH-only
  figures too: Cloudflare, JFrog, Airbnb, Atlassian and Natera's AH
  reactions were all reported explicitly labelled "AH snapshot, not yet
  confirmed to hold," not folded into the formal movers table/chart**, which
  was reserved for confirmed regular-session closes (Qualcomm's AH snapshot
  from edition 57 having itself just been superseded by its own confirmed
  close is the clearest illustration yet of why this distinction matters).
  **Edition 59 closed out exactly that loop**: all five of edition 58's AH
  snapshots (Cloudflare, JFrog, Airbnb, Atlassian, Natera) got their
  confirmed Friday regular-session close, and the direction held for all
  five even as the magnitude moved in both directions (JFrog's gain
  extended further, Natera's decline moderated slightly) — the cleanest
  full-resolution instance of this pattern logged yet.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent —
  RESOLVED cleanly again at edition 59** after recurring at edition 58.
  Yahoo Finance's DX-Y.NYB and an Investing.com futures-style DXY proxy both
  agreed Friday was up approx. 0.74%, with absolute levels differing by
  only approx. 12bp (102.30 vs. 102.179) — consistent with the
  methodology-continuity flag raised at edition 58 (the two series may
  track closely related underlying indices rather than being genuinely
  independent). Keep disclosing the DXY-vs-FX-crosses comparison every
  edition regardless of which way it goes.
- **The Kitco live-spot-vs-headline cross-check hit a new, more severe
  failure mode at edition 59 — total inaccessibility rather than a
  conflict** — see the dedicated Standing Facts entry above: a fourth
  distinct problem mode in four editions (sign conflict at 56, magnitude
  gap at 57, sign-plus-magnitude-plus-internal-baseline conflict at 58, now
  total inaccessibility at 59). No Kitco spot figure is reported for Friday
  as a result; disclose whichever form the problem takes explicitly rather
  than estimating a figure.
- **GBP/USD, EUR/USD and USD/JPY all reconciled cleanly again at edition 59**
  against their logged Thursday base, with no revision on any of the three
  — the vendor-revision trap this edition hit WTI, gold, silver (with a
  sign flip) and COMEX copper, but not the FX crosses or Treasuries.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for twenty-four further editions (37-59)** — edition 59 again found the
  full Treasury curve reconciled cleanly against the official
  home.treasury.gov TextView page (2-year 4.51%, 10-year 4.86%, 30-year
  5.26%, up 1-5bp across the curve on the day, a partial unwind of
  Thursday's flight-to-quality rally consistent with the payrolls-driven
  hawkish repricing), with the prior Thursday base matching the previous
  edition exactly. Treat as resolved/noise unless a fresh conflict appears.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 59 have all run clean (or
  clean after quick fixes) — **edition 54 needed one fix; edition 55 needed
  two fixes; edition 56 needed one fix; edition 57 needed one fix; edition
  58 needed ZERO fixes; edition 59 ALSO needed zero fixes — clean on the
  very first check for a second consecutive edition.**
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 55 rendered with zero stray tildes on the first
  draft; edition 56 needed one fix; edition 57 also needed one fix; editions
  58 and 59 both again rendered with zero stray tildes on the first draft**
  — a reminder that the fix/no-fix pattern doesn't correlate cleanly with
  content density.
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
  interest. **Edition 59 used the same normalization in Section 5 prose
  rather than a chart** (ES asset managers +46.75% of OI net long,
  leveraged funds -18.75% net short; NQ both cohorts modestly net long;
  RTY asset managers only marginally net long against a more meaningfully
  net-short leveraged-fund base), since the session's dominant story was
  judged to be elsewhere. The next CFTC report (due Fri 13 Nov, covering
  Tue 10 Nov data) falls inside edition 64's plausible window — check
  cftc.gov directly then.
- **The diffuse-overflow lesson from editions 44-45 and the duplicated-
  content lesson from edition 47 are both still worth checking first on any
  overflow** — but **edition 53 showed overflow can also be genuinely dense
  content requiring real trimming, while editions 54 through 58 all showed
  the opposite: heavy content does NOT automatically mean a multi-round
  trim.** Edition 58 is the strongest data point for this yet — a double
  central-bank surprise, a sharp FOMC-odds swing, a 0-of-11-sector selloff
  day, a VIX contango-to-backwardation inversion and a 12-plus-name earnings
  cluster all converged on the very first render with the forced break
  retained. Always check which situation you're in (stray break vs. genuine
  overflow vs. spillover that just needs the break deleted vs. a dense day
  that simply fits) before assuming a trim marathon is required.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — **specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation.** Edition 56's
  movers chart had a ratio of only approx. 1.06x, the tightest logged
  through edition 57. **Edition 58's movers chart (7 categories, MNTN
  -54.68% largest, VCYT -54.30% second largest) had a ratio of approx.
  1.007x — the tightest yet logged, comfortably beating edition 56's
  record.** Edition 59's movers chart (9 categories, FROG +35.33% largest,
  TEAM -16.15% second largest) had a ratio of approx. 2.19x — no capping
  needed in any edition since 45. Used `pad_frac=0.24` for edition 58's
  movers chart (figsize (9.8, 1.75), 7 categories, max abs value approx.
  54.68%, range -54.68% to +31.04%) and `pad_frac=0.26` for edition 59's
  (figsize (9.8, 1.85), 9 categories, range -16.15% to +35.33%); `pad_frac=
  0.30` for the 11-category sector panel (figsize (9.8, 1.95)) has now
  rendered cleanly with no label crowding across both editions.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 59 have all got a fresh,
  same-day-timestamped sweep** — thirty-two consecutive fresh sweeps now.
  **The feed's two known bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) appeared on ALL SIX series at edition 54, were ABSENT on all six
  series at editions 55 through 58, then RECURRED on all six series again
  at edition 59** (the feed's own reported percent-change diverged from an
  independent manual calculation by roughly 1-4 points on every series).
  **Always compute day-over-day % change manually regardless of how many
  consecutive bug-free reads preceded the current one — a four-edition
  clean streak just ended without warning.** Edition 58 saw the VIX complex
  spike sharply (the mirror image of edition 57's record decline) on the
  AI-capex/data-center selloff: VIX +69.66% to 28.18, VIX9D +115.01% to
  32.66, VIX3M +35.90% to 25.55, VIX6M +22.29% to 25.29, VVIX +49.31% to
  134.99, SKEW -1.01% to 149.37 — the sharpest one-day VIX *increase*
  logged in this report's history. **Edition 59 partially unwound that
  spike**: VIX -9.01% to 25.64 (manually recalculated), VIX9D -16.78% to
  27.18, VIX3M -3.72% to 24.60, VIX6M -2.33% to 24.70, VVIX -9.67% to
  121.94, SKEW +2.80% to 153.55. The term structure only partly
  renormalized: the front end stayed inverted (VIX9D 27.18 > VIX 25.64 >
  VIX3M 24.60), but the back end flipped to slight contango (VIX6M 24.70
  just above VIX3M 24.60) — a mixed, transitional shape.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 59 fetched all 11 directly again**
  (Technology +1.45% the leader on the chip relief rally, Communication
  Services +0.43% and Industrials +0.12% the only other advancers; Consumer
  Staples -1.28% the laggard, Materials -0.73% and Real Estate -0.68% also
  notably weak; only 3 of 11 green, a rotation back toward Thursday's worst
  performers rather than a broad risk-on day) — continue this
  direct-fetch-by-default method.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (0 of 11 at edition 58, the
  starkest reading logged to date; 3 of 11 at edition 59) — no competing
  secondary-aggregator breadth figure was checked either edition.
- **Dealer gamma:** zerogex.io hit a **TWENTIETH consecutive edition of
  failure at edition 59** (all widgets still show placeholder dashes with no
  timestamped data). SpotGamma logged a **FOURTEENTH straight failure at
  edition 59** (HTTP 403, Cloudflare block). Both sources remain fully
  unusable for structured data.
- **Official CME FedWatch probabilities:** the page blocks fetching
  (edition 59's direct attempt timed out again, a **NINETEENTH** consecutive
  failure, 41-59) — use secondary citations (Polymarket, Kalshi, Reuters/
  other economist polls, desk notes) and give a range rather than a single
  invented number. **Polymarket direct, tried via its Gamma API
  (`gamma-api.polymarket.com/public-search`) rather than a plain site visit,
  succeeded again at edition 59 — a sixth consecutive success** — this
  remains the preferred first approach; try it before reverting to a plain
  site visit. **DeFi Rate's blended aggregator refreshed past its stale
  late-September snapshot for the first time at edition 59** — resume the
  cross-check discipline against it going forward.
- **Kalshi direct fetch:** rate-limited or blocked across every edition it
  has been attempted, now **TWENTY-THREE consecutive failures (37-59)** — a
  confirmed structural gap, not transient (edition 59's specific failure
  mode was again HTTP 429). Resume the attempt-every-edition discipline at
  edition 60 regardless, but expect a block of some kind. Use Kalshi's own
  secondary reporting or DeFi Rate's blended aggregator as the workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **westmetall.com (LME copper)'s
  edition-58 missing-row problem resolved cleanly at edition 59** — see the
  dedicated Standing Facts entry above (a one-off publication lag, not a
  new recurring problem; both the Thursday and Friday rows are now posted).
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **remained clean at edition 59** (2-yr
  4.51%, 10-yr 4.86%, 30-yr 5.26%, all 6 Nov, with the prior Thursday base
  matching the previous edition exactly), extending the clean streak to
  **twenty-four editions (37-59)** with no repeat of the edition-36 33bp gap.
  Continue scoping the TextView URL to the specific month
  (`field_tdr_date_value_month=202611`-style parameter) rather than the
  full year.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). **The Friday 6 November report, covering Tuesday 3
  November data, was released on schedule at edition 59** — confirmed via
  `Last-Modified` header (15:27 ET), full ES/NQ/RTY Asset-Manager/
  Leveraged-Funds breakdowns extracted and summarized in Section 5 prose
  (no chart; see the dedicated Standing Facts entry above). **The next
  report is due Friday 13 November 2026, 3:30pm ET, covering Tuesday 10
  November data** — this falls inside edition 64's plausible window (if no
  gap) — check cftc.gov directly then. The CFTC release-schedule change
  (moving to twice-weekly releases by end of 2026, per a 27 Oct 2026 CFTC
  announcement, Press Release 9316-26) still has **no confirmed start
  date** as of edition 59 — the Friday 6 Nov report confirmed the old
  weekly, three-day-lag cadence was still in effect; worth a one-line check
  on the 13 November report too, in case the covered-data convention
  shifts by then.
- **GBP/USD, EUR/USD, USD/JPY clean close:** all remain fully resolved,
  reconciling cleanly again at edition 59 (EUR/USD 1.1144 -0.67%, GBP/USD
  1.3350 -0.75%, USD/JPY 158.48 +0.51%, all single-sourced to Investing.com's
  close-to-close history table, Thursday base matching this edition's own
  fresh re-fetch exactly). **DXY itself resolved cleanly at edition 59**
  after flipping to an unresolved cross-source direction conflict the
  edition before — see the dedicated Standing Facts and Hard Rules entries
  above.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot cross-check hit total inaccessibility at edition 59** — see
  the dedicated Standing Facts and Hard Rules entries above (a fourth
  distinct problem mode in four editions; no Kitco spot figure is reported
  this edition). Friday 6 Nov futures base figures: gold futures $4,074.90
  (-0.94%), silver futures $51.942 (-0.83%), both on vendor-revised
  Thursday bases (see the vendor-retroactive-revision-trap entry above).
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is also a closed thread as of
  edition 45. **US GDP, PCE, import/export prices and industrial
  production:** all closed threads — see Standing Facts above. **University
  of Michigan October consumer sentiment** is a closed thread as of edition
  49. **China's October PMI** is a closed thread as of edition 54. **October
  ISM Services PMI** is a closed thread as of edition 57 (headline only;
  sub-index detail remains an Annex B item).
- **Henry Hub natural gas:** the front-month-contract-identity question
  remains resolved (NGZ6/December, no roll to NGF7/January yet as of 6 Nov).
  **The base-price reliability problem — this report's historically
  worst-performing data-quality issue — stayed substantially CLOSED at
  edition 59**, a fourth consecutive clean two-source reconciliation
  (Investing.com, Yahoo Finance NG=F, matching almost exactly at edition 59)
  following the edition-56 breakthrough. Resume only occasional spot-checks
  rather than a dedicated every-edition reconciliation effort unless a
  fresh conflict appears.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 59 again found no usable
  single-name implied-move or options-flow figure** (optionslam.com exposes
  only the current day's data, not a historical date; zerogex.io and
  SpotGamma both remained unusable) — continuing the pattern from edition
  58. Treat the general sub-item as still reliably low-yield most editions,
  but worth a genuine attempt around any single dominant earnings story.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. **Q3's
  approx. 14 November 2026 deadline falls on a Saturday** — the natural lead
  item for whichever edition covers the following Monday, 16 November 2026
  (a weekend-gap edition), now about five days out from edition 59's own
  date.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22, not attempted
  again since). Revisit only if a future edition has spare research
  bandwidth on an FOMC day specifically — not relevant to most editions.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully at
  editions 39, 44-49, 54 and now **59** (the Friday 6 Nov report, covering
  Tuesday 3 Nov data: ES OI 1,986,532; NQ OI 292,587; RTY OI 449,399). No
  new report fell inside editions 55 through 58's windows. Repeat the
  three-instrument fetch whichever edition's window extends past Friday 13
  November, 3:30pm ET (likely edition 64), watching for the
  micro-vs-full-size naming trap each time, and for a possible
  release-schedule change (see the CFTC CoT entry above).
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 58 went
  further than prior editions on this sub-item: no analyst action at all
  from the session could be independently verified — a circulating
  "biggest calls" list was spot-checked and found entirely unsupported, and
  was omitted in full rather than any individual claim from it being
  repeated. **Edition 59 found the same result for a second straight
  edition** — a dedicated search for Friday's session returned no
  analyst-action item tied to a named analyst/firm and the correct date;
  none is reported. Watch each edition independently rather than assuming
  a trend, but this is now a two-edition pattern.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** This discipline has now caught: Tesla/NU Holdings
  (ed.49, magnitude), JetBlue (ed.50, magnitude), Carvana/Barron's (ed.52,
  direction/framing), Marvell/Lumentum and Barclays/PayPal (ed.53), two more
  exclusions at edition 54, a claimed Oracle analyst-upgrade note at edition
  56, two forward-looking-calendar-aggregator date errors at edition 57, and
  **at edition 58: a fabricated DraftKings AH figure (no 8-K anywhere on
  EDGAR), an unsupported Natera driver claim, and an entire "biggest calls"
  analyst-action list found unsupported on spot-check**; and **at edition
  59: a wholesale stale-date-republish of Thursday's index closes under
  Friday's date.** At both editions 58 and 59, every reported single-stock
  mover was individually cross-checked against its own primary SEC filing
  (8-K or 6-K) rather than accepted from an aggregator list alone — continue
  this direct-verification discipline on every edition.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted at editions 48 through 59 (out of scope each time); try
  an alternate DOL page or a secondary economic-calendar aggregator for the
  consensus figure at edition 60.
- **federalregister.gov's direct search interface is blocked, re-tested
  directly again at edition 59 and still blocked** (a prior search attempt
  302-redirected to `unblock.federalregister.gov`, an apparent bot/rate-limit
  gate, first logged at edition 48). govinfo.gov continues to be the known
  working alternative route for at least some Federal Register content.
- **SEC EDGAR's `cgi-bin/browse-edgar` company-search page (filtered by CIK
  and form type 8-K) is a highly reliable, fast way to confirm both WHETHER
  a company has reported on a given date and to find the accession number
  for the underlying exhibit** — used again at edition 59 for JFrog,
  Atlassian, Natera, Cloudflare and Airbnb. Edition 58 demonstrated a
  valuable NEGATIVE use case (the absence of a matching 8-K disproved a
  circulated claim) — worth remembering this tool is just as useful for
  debunking an unverifiable claim as for confirming a verifiable one.
- **Riksbank's primary policy-rate/next-meeting page:** fully resolved as of
  edition 57 (hiked to 2.00% on 4 Nov 2026) — see the dedicated Standing
  Facts entry above. The vote split from that decision remained unresolved
  at edition 59 too; minutes due 10 November 2026 had not posted by this
  window's close, likely landing inside edition 61's window (covering
  Tuesday 10 Nov) rather than edition 60's.
- **ECB's current policy rate: SETTLED since edition 55** (reconfirmed
  directly for a third consecutive edition — 53, 54, 55 — unchanged through
  the 28-29 October 2026 meeting: deposit facility 2.50%, main refi 2.65%,
  marginal lending 2.90%); not re-attempted at editions 56 through 59 (no
  fetch needed). Do not spend a fetch on the rate level itself going
  forward; it reopens on contradiction, the next Governing Council decision,
  or the monthly audit. Its exact Governing Council press-conference
  content/vote-split remains unobtainable and was not specifically
  re-attempted at edition 59 (out of scope) — low priority. **The Council's
  own next-meeting date, previously the ECB's one outstanding live
  sub-question, was resolved directly at edition 59: 16-17 December 2026**
  (ecb.europa.eu) — now SETTLED, see the dedicated Standing Facts entry
  above.
- **Banxico's own primary site (banxico.org.mx) remains unreachable** for a
  further edition — at edition 59 every path tried (including the English
  boletines page and a guessed PDF path) 302-redirected to an
  "anterior.banxico.org.mx" subdomain that itself 404'd, a different
  failure signature than editions 56-58's straight 404/redirect-loop — now
  a confirmed structural gap across multiple editions, not transient.
  Continue the attempt-every-edition discipline with yet another fresh URL
  path, but rely on the consistent multi-outlet Mexican financial press as
  the working alternative when it fails.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel —
  confirmed clean again at edition 59 (twenty editions total: 37-43, 45-50,
  52-59). For charts with fewer categories, scale the height down: roughly
  `(9.8, 1.65-1.95)` for 3-9 categories. Edition 58 used `(9.8, 1.75)` for a
  7-category movers chart with `pad_frac=0.24`, rendering cleanly despite a
  wide range (-54.68% to +31.04%) and the tightest largest-to-second-largest
  ratio logged to date (approx. 1.007x). **Edition 59 used `(9.8, 1.85)`
  for a 9-category movers chart with `pad_frac=0.26`**, rendering cleanly
  across a -16.15% to +35.33% range (ratio approx. 2.19x). **Always render
  and visually inspect (via the Read tool) the actual PNG at or near full
  resolution before embedding it**, regardless of what a past edition's
  success might suggest. **Default to pad_frac=0.30 from the start for an
  11-category sector-ETF panel** — now confirmed across fourteen straight
  small-magnitude 11-category panels (45-50, 52-59). For any movers chart
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
  threshold, including edition 58's approx. 1.007x, the tightest logged) —
  reinforcing that the trigger is the ratio to the next-largest bar, not the
  largest bar's absolute size.
- **A grouped (two-series) horizontal bar chart — needed for the CFTC
  Asset-Manager-vs-Leveraged-Funds positioning chart — requires custom chart
  code, not the standard single-series `barh()` helper used for the
  movers/sector charts** (first built at edition 44, reused successfully at
  editions 49 and 54; not needed at editions 55 through 58 since no fresh
  CFTC data fell inside any of those windows). The standard helper only
  plots one value per category; the CFTC chart needs two bars (Asset
  Manager, Leveraged Funds) per category (ES/NQ/RTY), offset vertically by a
  fixed height fraction (`h=0.32` worked cleanly at edition 54) around each
  category's tick position. **Fix that worked for the legend:** use a
  FIGURE-level legend (`fig.legend(..., loc="lower center",
  bbox_to_anchor=(0.5, 0.0), ...)`) combined with `fig.tight_layout(rect=(0,
  0.1, 1, 1))` to reserve the bottom 10% of the figure for the legend.
  Figsize `(9.8, 2.15)` rendered cleanly at edition 54. **Reuse this exact
  pattern** for any future grouped/multi-series chart rather than
  re-deriving the legend-placement fix from scratch.
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
      annex opens a clean page 4, exactly as before. **Editions 55 through
      58 all landed here**, with sections 1-6 ending partway through page 3
      and the annex opening cleanly on page 4 every time (page 4 itself had
      some unused space at the bottom in each case — acceptable; the
      "Filling a short page 3/4" guidance is optional padding, not a
      requirement, when the content is already precise and complete).
    - Sections 1-6 spill onto page 4 → **delete the `pagebreak` div and
      re-render**, so the annex follows the spillover down page 4 instead of
      starting a fifth page. **Edition 54's case** — a stray fourth bullet in
      Section 6's sector-setup list spilled alone onto an otherwise-blank
      page 4 when the break was still present (producing a 5-page draft);
      deleting the break let the annex flow up right after it, converging to
      a clean 4 pages on the very next render with no further trimming
      needed. **Edition 59 hit the identical symptom** — two Section 6
      sector-setup bullets spilled alone onto page 4 — and the identical
      fix converged it to 4 pages on the next render.
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
  break safely — this is expected behavior, not a bug to fix. **Edition 57's
  Section 2 movers table reflowed across the page 1/2 boundary this way.**
  Edition 58's own movers table and chart both stayed cleanly within page 1,
  with only the long Section 2 prose paragraphs carrying over onto page 2 —
  also expected, not a defect.
- **A markup-correctness trap, logged at edition 47: a `<sup class="ref">`
  citation tag placed immediately after a table row's last `</td>` but still
  inside the `<tr>` (i.e. not nested inside any `<td>`) is invalid table
  structure.** `check_refs.py` will NOT catch this. **Always nest every
  `<sup class="ref">` tag inside a `<td>...</td>` pair, never as a sibling of
  one inside a `<tr>`** — grep for `</td><sup` as a quick self-check if a
  table was built with a lot of copy-paste. **Edition 54 actually TRIGGERED
  this trap three times** and caught all three via a proactive grep before
  rendering. **Editions 55 through 59 all ran the same proactive grep and
  found zero instances, a fifth consecutive clean sweep.** Run the grep on
  every edition with such a table, not just when troubleshooting a layout
  problem.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Edition 53 needed this discipline more than almost any prior edition.
  **Editions 55 through 58 all rendered cleanly on the first attempt; edition
  59 needed one break-deletion re-render** (the known spillover pattern,
  not a new symptom) — the page images were still read in full as standard
  practice every time, confirming no broken tables, no overlapping chart
  labels, and no cut-off content on any of the 4 pages.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across many editions'
genuinely different content volumes, including editions 53's through 59's.
Treat as the durable default; the lever to pull on a high-volume or
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
  runs short — editions 44 through 59 have all folded commodities, FX and
  Treasuries into ONE combined table (10-17 rows; edition 58 used 17,
  edition 59 used 16) as the PRIMARY commodities table rather than padding,
  now the standing default.
  **Always re-render immediately after adding (or removing) any content to
  confirm the page count.**

**Chart selection guidance.** Placement is not editorial for the first two
charts:

- **Sector-ETF performance chart → Section 1 (Market recap), every
  edition.** Same-day closes by default; a grouped day-over-day bar instead
  on a multi-session or weekend window, or on a genuine multi-sector
  broadening selloff across consecutive sessions. **Editions 54 through 59
  all used a single-day bar** (only one NYSE session fell inside any of
  those windows, even edition 59's weekend-extended one).
- **Single-stock movers bar → Section 2 (Equities), every edition.**
- **A third chart only when positioning or volatility is genuinely the
  day's dominant story**, never to fill a page, placed in the section it
  belongs to:
  - Fresh CFTC CoT data → the ES/NQ/RTY asset-manager-vs-leveraged-funds
    positioning chart, normalized as % of open interest, built with the
    grouped-bar technique documented under Production notes, in **Section
    5**. Editions 24, 34, 39, 44, 49 and 54 have all placed it there; none
    of editions 55 through 59 had the chart placed there, though edition 59
    did have fresh data available (the Friday 6 Nov report, covering
    Tuesday 3 Nov data) and judged the payrolls/chip-rally story more
    dominant, summarizing the data in prose/a small table instead. The next
    opportunity (Friday 13 Nov report, covering Tuesday 10 Nov data) falls
    inside edition 64's plausible window.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully. Not used at editions 55
    (Apple), 56 (AMD), 57 (Qualcomm), 58 or 59 (no single name had a clean,
    uncontested, chartable implied-move figure in either of the latter two
    editions — optionslam.com's fetch failed outright both times).
  - A holiday-window preview edition with no fresher data → VIX futures
    term structure with event annotations, in **Section 5**. Not used at
    editions 55 through 59 — in each case the VIX term structure was
    genuinely newsworthy (a kink, its narrowing, a dramatic one-day collapse
    at 57, a full contango-to-backwardation inversion at 58, then a partial
    unwind of that inversion at 59) but was judged secondary to the
    session's dominant equity/macro story each time and was covered fully
    in prose instead.

**Edition 60 (expected to cover Monday 9 November 2026, assuming no gap)
has a lighter but still live calendar load — mostly watch-and-confirm
rather than a dense fresh-print day.** Watch directly rather than assuming:
**whether Friday's semiconductor relief rally extends into Monday or
Thursday's selloff reasserts** (none of the six chip names tracked had
regained its pre-selloff level as of edition 59's cutoff); **whether
December FOMC hike odds (snapped back to approx. 76-77% at edition 59) hold
at that level, extend further, or ease again** (a priority fresh pull given
this is now a two-edition round-trip); **midterm-election certification
status**, still unconfirmed after two straight editions of searching;
**government funding status**, direct against whitehouse.gov (downgraded
to secondary at edition 59, retry directly); and **Banxico's primary
site**, via yet another fresh URL path. Note that the Section 301
178-product exclusion lapse itself (whether operative at 11:59pm ET Monday
9 Nov, per the primary notice's own DATES section, or effectively Tuesday
10 Nov, per its background text and USTR's press release), October's CPI
print, and the Riksbank's vote-split minutes are all expected to land
**after** edition 60's own window closes (its cutoff falls around 8:15pm
ET Monday, before either stated lapse moment) — likely inside **edition
61's** window (covering Tuesday 10 Nov) instead; don't go looking for them
early at edition 60.
The La Naci&oacute;n/WTOP double AP-wire-mirror approach and the Polymarket
Gamma-API approach are both now on six-edition clean streaks — use them
first rather than their respective fallbacks.

**Remember the figsize-scales-to-category-count guidance above
(ceiling `(9.8, 1.95)` for an 11-category panel, `(9.8, 2.15)` for the
3-category grouped CFTC chart, scale down for fewer single-series
categories), that an 11-category sector-ETF panel should default to
pad_frac=0.30 from the start (now confirmed across fourteen editions,
including 59), a movers chart with a double-digit-percent outlier should
try pad_frac in the 0.22-0.30 range from the start (edition 58 used 0.24
for a 7-category panel spanning -54.68% to +31.04%, ratio approx. 1.007x,
the tightest logged to date; edition 59 used 0.26 for a 9-category panel
spanning -16.15% to +35.33%, ratio approx. 2.19x), and the capped-outlier
asterisk/footnote fix when a spread crosses the approx. 5x RATIO
threshold** (it has not since edition 45).

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

**Edition 58's carried-forward spec was 124,962 bytes, over the
100,000-byte threshold — this run (producing edition 59's spec) condenses
the log.** Editions 56 and 57 had each been left as their own separate
condensed paragraphs rather than actually folded into the mega-block
despite a prior run's note claiming otherwise; this run corrects that by
folding both into the running mega-block (now "Editions 1-57"), condensing
edition 58's own full-detail entry down to a medium paragraph, and adding
edition 59 in full detail, per the log's own standard rotation. There is no
maximum size; condensing is housekeeping done by the run itself, not a
check to pass — there is no penalty for the file staying somewhat large if
the alternative is losing information.

**Editions 1–57 (condensed):** established the format (edition 1 baseline;
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
odds eased slightly despite it. Alphabet lost approx. $500bn of market
value in a single session (-12.64%), extending Wednesday's AH
mark-to-market-loss reaction even as Search and Cloud both beat, dragging
Communication Services to the day's sector laggard even as 9 of 11 sectors
closed higher. Amazon's Q3 was a "double miss on the surface" masking real
AWS/margin strength (shares -4.25% regular, -7.30% AH). "Beat-and-raise
guarantees nothing" produced its largest cases yet: ServiceNow -26.95%,
Intel -23.04% AH, Caterpillar -9.25%, all on clean beats. Smaller movers:
Xerox -40.32%, Glaukos +33.65%, ADT +33.20%, Marvell -13.24% (a claimed
Lumentum-acquisition-talks driver found unsubstantiated — a claim that,
strikingly, became real M&A four sessions later at edition 55), Carvana
+15.68%. The vendor-retroactive-revision trap hit gold/silver a second
straight edition and Henry Hub a third, the latter now this report's
worst-performing series (at that time — since substantially resolved, see
Standing Facts). A claimed Barclays PayPal downgrade was investigated and
found fabricated, dropped entirely. First draft ran a genuine 6 pages;
converged to 4 after deleting the forced break and a dozen rounds of
trimming/citation-merging (54 sources to 41), surfacing a new CSS
multi-column pagination lesson documented under Production notes. **Edition
54 (Mon 2 Nov, covering Fri 30 Oct, a weekend-gap edition):** a tech-led
selloff dropped the major indices broadly (S&P -1.82% to 7,580.07, Nasdaq
-2.86% to 25,437.00, worst session since June) on Intel's historic -28.58%
collapse to $65.76 (worst day since 1974) following a weak Q4 guide despite
beating Q3; Nvidia -4.22% the single largest index-point drag. A record
approx. $6.3bn Binance hack roiled crypto-adjacent names: Coinbase -10.62%,
Strategy -7.84%, Bitcoin below $77,000. Two long-running Asia threads
resolved the same session: the BoJ held its rate at approx. 1.25% (8-1
vote, dissenter Takata Hajime), and China's October PMI slipped back below
50 on both gauges. Four previously-pending earnings reports (Chevron, Exxon
Mobil, AbbVie, Newell Brands) all beat and rose; a fresh CFTC CoT report
powered the third positioning chart. The VIX complex jumped sharply
(+12.91% to 19.42) but stayed in clean contango. The November monthly
settled-facts audit completed cleanly across all ten central-bank rows.
First draft ran 5 pages on a single orphaned Section 6 bullet spilling
alone onto page 4; deleting the break converged to a clean 4 pages. 44/44
sources clean after one fix; zero stray tildes. **Edition 55 (Tue 3 Nov,
covering Mon 2 Nov, the window's one NYSE session):** equities diverged
sharply on composition — Dow +0.41% (third straight advance) while S&P
-0.51% and Nasdaq -1.07% as Technology (-2.95%) and Energy (-3.96%) dragged
the cap-weighted indices down even though 8 of 11 sectors closed higher.
Crude collapsed 7-11% on an Iran/US diplomatic-thaw signal (WTI -7.40%,
Brent -10.94%). Apple's FQ4 (revenue $114.5bn +12%, EPS $2.10 +14%) fell
1.83%/-2.75% AH on a soft margin outlook; Intel extended its collapse
-8.80%; Oracle fell -8.76% on a disclosed $20bn AI-capex raise; Marvell
agreed to acquire Lumentum (Marvell -12.72%, Lumentum -18.59%) — the prior
edition's rejected Marvell-Lumentum rumor becoming real four sessions
later. Palantir beat-and-raised yet fell. BoJ's and SNB's next-meeting
dates both resolved directly; the ECB's rate complex was promoted to
SETTLED. The CBOE VIX feed's two known bugs were absent on all six series
for the first time in recent memory. VIX jumped +8.91% to 21.15 with a
genuinely kinked term structure. December FOMC hike odds firmed to approx.
72-73%. First draft converged cleanly to 4 pages; 41/41 sources clean after
two fixes.

**Edition 56** (Wed 4 Nov, covering Tue 3 Nov, the window's one NYSE
session): equities diverged on composition, not breadth (S&P +0.36% to
7,568.92, Nasdaq +0.83% to 25,372.01 on a megacap/AI bounce; Dow -0.38% to
51,786.72; only 4 of 11 sector ETFs higher). The RBA delivered its fifth
2026 hike (25bp to 4.85%) on a first-ever split 6-3 vote. AMD's fiscal Q3
(revenue $13.4bn +45% y/y) drew a genuinely positive AH reaction (+5.02%),
a counter-example to the week's muted-to-negative beat-and-raise pattern.
A claimed Oracle analyst-upgrade note was investigated and rejected as
unreliable; the Bank of England's 5 November decision date was upgraded to
primary-sourced; Henry Hub reconciled cleanly across two sources for the
first time in six editions; the VIX feed's two known bugs were absent for
a second consecutive edition. Rate-path odds firmed to approx. 74-75%
hike. First draft converged cleanly to 4 pages on the first render; 29/29
sources clean after one fix.

**Edition 57** (Thu 5 Nov, covering Wed 4 Nov): dominant story was the 3
November 2026 US midterm elections, called for Democrats in both chambers
by Wednesday morning, ending unified Republican control — Dow +3.03% to
53,356.12 (then this report's largest one-day move), S&P +1.58% to
7,688.62, Nasdaq +1.44% to 25,736.51; WTI crashed 8.3% to $88.12, Brent
-8.67% to $94.62; VIX posted its then-sharpest one-day decline, -20.26% to
16.61, resolving a term-structure kink into clean ascending contango. Nine
of 11 sector ETFs closed higher. Seven single-stock movers, each verified
against primary filings: Amdocs -30.07% (shock guidance cut), Qualcomm
+5.33% regular/-7.52% AH (a late snapshot, later superseded — see edition
58), Uber +4.91%, Helen of Troy +25.39% (rejected a buyout), Duolingo
+25.99%, Kyndryl +30.14%, Cricut +48.74%. Two forward-looking-calendar-
aggregator date errors (Amdocs, Kyndryl) were caught and corrected
pre-publication via SEC EDGAR. Sweden's Riksbank delivered a surprise 25bp
hike to 2.00%, its first since 2023; the RBA's next decision resolved to
7-8 December 2026; October's ISM Services PMI printed 54.5. December FOMC
hike odds firmed to approx. 77-80% (since reversed sharply, then reversed
back — see editions 58-59). A Federal Register filing resolved the
Section 301 178-product exclusion lapse date (later found internally
inconsistent — see edition 59). Henry Hub posted a second consecutive
clean reconciliation; Veterans Day (11 Nov) was independently confirmed as
an equities-open/bonds-closed holiday. First draft converged cleanly to 4
pages on the first render; 33/33 sources clean after one fix. A dedicated
verification pass was run on the election outcome and the Riksbank
decision given how consequential and surprising both were.

**Edition 58 (condensed)** — Friday 6 November 2026 report covering
Thursday 5 November 2026, the window's one NYSE session. Dominant story:
a full, sharp reversal of Wednesday's election rally, driven by an
AI-capex/data-center-moratorium scare (local ballot measures tied to the
midterms rejected data-center buildouts in 40 of 41 votes; UBS flagged
approx. 30% of 2028 data-center capacity as at risk). S&P fell 4.4% to
7,353.73, Dow fell 3.4% to 51,523.06, Nasdaq fell 5.5% to 24,315.00
(correction territory, approx. $2tn of value erased per Bloomberg),
Russell 2000 fell 4.4% to 2,729.89; zero of 11 sector ETFs closed higher,
Technology (XLK -8.00%) the clear laggard. The semiconductor complex
(Micron, AMD, Marvell, Broadcom, Intel, Nvidia) all fell double digits on
no company-specific news. VIX posted its sharpest one-day increase on
record (+69.66% to 28.18), fully inverting contango into backwardation;
both feed bugs stayed absent for a fourth consecutive edition. A dense
earnings cluster, each verified against primary filings: Qualcomm -9.49%
confirmed close (superseding edition 57's AH snapshot — a supersession,
not a correction), Arm -13.08%, Tripadvisor -27.65% (goodwill impairment
plus same-day CEO/CFO departures), AppLovin +31.04%, Krispy Kreme +30.68%,
Veracyte -54.30%, MNTN -54.68%; a second AH wave (Cloudflare, JFrog,
Airbnb up; Atlassian, Natera down) was reported as unconfirmed snapshots
only. Three "named secondary outlet flatly wrong" instances were caught
and excluded: a fabricated DraftKings AH figure (no 8-K anywhere on
EDGAR), an unsupported Natera "new CEO" driver claim, and an entire
circulating "biggest calls" analyst-action list found unsupported on
spot-check. Two central banks delivered opposite surprises the same
session — the Bank of England hiked 25bp to 4.00% (8-1, Mann dissenting
for 50bp), confirmed directly against bankofengland.co.uk; Banxico
reportedly cut 25bp to 6.25% (3-2 vote), secondary-sourced only. December
8-9 FOMC hike odds eased sharply to approx. 66.5% (from approx. 77-80% at
edition 57), coincident with a 3-12bp Treasury rally. Oil partially
rebounded off Wednesday's crash (WTI +3.56%, Brent +3.88%); Henry Hub
posted a third consecutive clean reconciliation; gold/silver split
futures-vs-spot again; DXY's two benchmarks disagreed on direction again;
LME copper's Thursday settlement had not posted at westmetall.com at
research time. No correction box; first draft converged cleanly to 4
pages on the first render, forced break retained; **21/21 sources clean
on check_refs.py with ZERO fixes needed — the first edition in the recent
run to need no correction at all.** Zero stray tildes; zero `</td><sup`
instances. The macro research pass independently primary-sourced the Bank
of England decision directly and cross-verified Banxico's cut against six
independent outlets.

**Edition 59 (most recent — full detail)** — Monday 9 November 2026
report covering Friday 6 November 2026, research window Thu 5 Nov 2026
20:00 ET through Sun 8 Nov 2026 20:21 ET (the window's one NYSE session,
plus the weekend).

**The dominant story was a much-stronger-than-expected October jobs
report snapping December FOMC hike odds back toward their hawkish range,
against a narrow, chip-led equity relief rally that only partly reversed
Thursday's AI-capex rout.** Nonfarm payrolls rose 165,000 against a
FactSet-polled consensus of 65,000 (found this edition after three prior
failed attempts), unemployment held at 4.1%, average hourly earnings rose
0.4% m/m/3.1% y/y, and August/September were revised up a combined
84,000 — confirmed directly against bls.gov. December 8-9 FOMC hike odds
snapped from edition 58's approx. 66.5% back to approx. 76.5-77% per a
fresh Polymarket Gamma-API pull, corroborated by DeFi Rate's blended
aggregator refreshing past its stale late-September snapshot for the
first time — effectively a full round-trip in two editions. Treasury
yields rose 1-5bp across the curve and the dollar firmed (DXY +0.74% on
both tracked benchmarks, resolving their edition-58 direction conflict),
both consistent with the hawkish repricing.

**Equities closed mixed-but-higher on narrow breadth.** The S&P 500 added
0.3% to 7,376.86, the Nasdaq Composite added 1.1% to 24,579.42 and the
Russell 2000 added 0.9% to 2,754.11, while the Dow — lacking the same
semiconductor weighting — fell 0.5% to 51,285.73, all confirmed via an
AP-wire mirror (lanacion.com.ar). Only 3 of 11 SPDR sector ETFs closed
higher (Technology +1.45%, Communication Services +0.43%, Industrials
+0.12%); Consumer Staples (-1.28%) was the laggard. The semiconductor
complex that collapsed double-digit Thursday on no company-specific news
staged a relief rally Friday on, again, no identifiable fresh news: AMD
+11.04%, Intel +7.71%, Micron +5.12%, Marvell +5.73%, Nvidia +2.78%,
Broadcom +0.74% — none regained its pre-selloff level. A widely-surfaced
secondary figure for Friday's close (Dow -3.44%, S&P -4.30%, Nasdaq
-5.52%) was found to be a near-exact restatement of Thursday's actual
close under Friday's date — excluded as a stale-date-republishing trap,
the fourth such caught instance in four editions.

**Thursday evening's second wave of AH earnings snapshots all got their
confirmed Friday regular-session close, and the direction held for all
five.** JFrog +35.33% (extending its AH pop on a clean Q3 beat-and-raise),
Airbnb +11.67% and Cloudflare +9.91% all held/extended their beat
reactions; Atlassian -16.15% (a soft FY27 growth guide despite a Q1 beat)
and Natera -14.59% (a surprise CEO transition from Steve Chapman to
Solomon Moshkevich, plus a wider GAAP loss, despite a 34.1% revenue beat)
both confirmed Thursday's declines, though Natera's moderated slightly
from its AH snapshot. No Friday analyst action could be independently
verified against a named analyst or firm.

**VIX partially unwound Thursday's record spike, and the feed's two known
bugs recurred after four clean editions.** VIX fell 9.01% (manually
recalculated against the feed's own diverging figure) to 25.64, VIX9D fell
16.78% to 27.18, VIX3M fell 3.72% to 24.60, VIX6M fell 2.33% to 24.70,
VVIX fell 9.67% to 121.94, SKEW rose 2.80% to 153.55. The term structure
only partly renormalized: the front end stayed inverted while the back
end flipped to slight contango — a mixed, transitional shape. The CFTC's
Commitment of Traders report (covering Tuesday 3 Nov data) released on
schedule; the data was summarized in Section 5 prose rather than charted,
since the payrolls-and-chip-rally story was judged more dominant.

**Commodities and FX saw a fresh round of the vendor-retroactive-revision
trap, hitting four of seven tracked series.** WTI, gold futures, silver
futures (with an outright sign flip on Thursday's own logged figure) and
COMEX copper all showed a revised Thursday base on fresh re-pull; Brent,
EUR/USD, GBP/USD, USD/JPY and Treasury yields all reconciled cleanly with
no revision. LME copper's edition-58 missing-row problem resolved as a
one-off publication lag, not a new recurring problem. Kitco's historical
spot-close pages became totally inaccessible (a new, fourth failure mode
in four editions) — no Kitco spot figure is reported. The ECB's long-open
next-meeting-date sub-question was resolved directly (16-17 December
2026); Banxico's primary site failed again via a new failure signature
(redirect to a dead "anterior" mirror). Government funding status
downgraded to secondary-sourced this edition after whitehouse.gov's pages
failed to surface relevant content. Midterm-election certification status
remained unconfirmed.

**Format:** no correction box. First draft spilled two Section 6
sector-setup bullets alone onto page 4 (five pages); deleting the single
forced break converged cleanly to 4 pages on the next render. **19/19
sources clean on check_refs.py with ZERO fixes needed — a second
consecutive edition with no correction needed.** Zero stray tildes; zero
`</td><sup` instances. A dedicated verification pass was run directly
against bls.gov on the payrolls print and against both Polymarket and
DeFi Rate on the rate-odds reversal, given how consequential and
surprising the swing was.

**Open threads for edition 60.** Edition 60 covers **Monday 9 November
2026** (if no gap) — a lighter calendar load, mostly watch-and-confirm.
Watch directly rather than assuming: **whether Friday's semiconductor
relief rally extends or Thursday's selloff reasserts** (none of the six
chip names tracked had regained its pre-selloff level); **whether
December FOMC hike odds (approx. 76-77%) hold, extend, or ease again**
(a priority fresh pull, given this is now a two-edition round-trip);
**midterm-election certification status**, unconfirmed for a second
straight edition; **government funding status**, direct against
whitehouse.gov (downgraded to secondary at edition 59); and **Banxico's
primary site**, via yet another fresh URL path. **Not due inside edition
60's own window — expected instead inside edition 61's (covering Tuesday
10 Nov), since edition 60's cutoff falls before either candidate lapse
moment:** the Section 301 178-product exclusion lapse (11:59pm ET Monday
9 Nov per the notice's own DATES section, or effectively Tuesday 10 Nov
per its background text and USTR's press release — the notice itself is
internally inconsistent, watch which date it ultimately treats as
operative), October's CPI print, and the Riksbank's 4 November vote-split
minutes (due 10 Nov). **Still open and unchanged:** Brent crude's Friday
23 October close three-way split (not re-attempted since edition 53); New
Mexico v. Meta's formal notice of appeal (unconfirmed for a fourteenth
straight edition); the "preview-consensus-only miss/beat framing" caution
(dormant since edition 41); the DOL weekly jobless-claims parsing problem;
a fresh federalregister.gov search-interface attempt (govinfo.gov remains
the working fallback, re-confirmed blocked again at edition 59). **Dates
to hold on to** (one edition per weekday now assumed: 60 Mon 9, 61 Tue 10,
62 Wed 11, 63 Thu 12, 64 Fri 13). October CPI and Riksbank minutes both
due Tue 10 Nov 2026 (edition 61), alongside the Section 301
rate-resumption's visible effect. Veterans Day (equities-open,
bonds-closed, confirmed) Wed 11 Nov 2026 (edition 62). October PPI and
the next CFTC CoT report (covering Tue 10 Nov data) both due Fri 13
November 2026, 3:30pm ET for the CFTC report (edition 64). 13F filings
due approx. 14 November 2026 (a Saturday) — the natural lead item for
whichever edition covers the following Monday, 16 November 2026, now
about five days out. BoE and Banxico next decisions both 17 Dec 2026; the
ECB's next meeting 16-17 Dec 2026; the Fed's next meeting 8-9 Dec 2026;
the next monthly settled-facts audit falls on the first edition of
December 2026.
