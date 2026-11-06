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
  applied correctly for thirty-six straight editions (33 through 58) — treat
  as settled; edition 58 read "Friday 6 November 2026" as the date line,
  covering the Thursday 5 November session in the window line.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 58 all reused the
  same pattern — now confirmed clean across thirty consecutive editions;
  edition 58 phrased it "Window: Wed 4 Nov 2026 20:00 ET – Thu 5 Nov 2026
  20:21 ET (Thu 5 Nov close/AH, the window's one NYSE session)." No further
  confirmation needed; treat this as settled.

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
- **Rate-path odds — MAJOR SWING at edition 58.** A fresh Polymarket Gamma-API
  pull (`gamma-api.polymarket.com/public-search`, snapshot 5-6 Nov 2026) put
  December 8-9 odds at **approx. 66.5% hike / 31.5% no change / cut near
  zero** — a sharp easing from approx. 77-80% hike at edition 57, the first
  reversal after four straight editions of hardening hike odds. The swing
  coincided with Thursday's broad risk-off equity selloff (AI-capex/
  data-center fears) and a 3-12bp Treasury rally, consistent with a
  flight-to-quality/softening-hawkish-conviction read, though this report
  does not claim a specific causal mechanism beyond the coincident timing.
  **DeFi Rate's own blended Kalshi/Polymarket aggregator returned no snapshot
  newer than 30 Sept 2026 at edition 58** (stale, showing a 67-79% hike
  range) — not usable as a fresh cross-check this edition; worth retrying
  next edition to see if it has refreshed. The ten-straight-edition (47-56)
  internal Kalshi-vs-Polymarket inconsistency inside that aggregator was last
  noted as unresolved at edition 56 and could not be re-examined at edition
  58 given the stale snapshot. **Kalshi's own direct fetch failed again at
  edition 58 — HTTP 429 (rate-limited) again — now TWENTY-TWO consecutive
  failures (37-58).** CME FedWatch also failed again directly (timeout), an
  **EIGHTEENTH** consecutive failure (41-58). The composite "at least one
  more hike in 2026" read has still not been freshly re-pulled since edition
  38 (last known approx. 80%) — don't cite without a fresh pull. **Given the
  magnitude of this edition's swing, a fresh read at edition 59 is a
  priority, not routine upkeep** — confirm whether the move holds, extends,
  or partially reverses.
- **US-China "30-for-30" tariff framework — remains a closed thread, do not
  re-open absent a genuine dated Federal Register filing.** Resolved at
  edition 37 (framework) and edition 47 (implementation-notice sub-question:
  no effective date, no set timeline, none imminent). No new development was
  found at editions 54-58 either (light-touch checks only); the
  federalregister.gov search-interface block (302-redirect to
  `unblock.federalregister.gov`, logged at edition 48) was re-tested directly
  again at edition 58 and remains blocked — govinfo.gov continues to be the
  working mirror. Separately: secondary reporting (a Thomson Reuters
  regulatory-insight piece) describes a Busan truce extension to **10 January
  2027**, but this remains **NOT confirmed via any published Federal Register
  notice** as of edition 58 — treat the January 2027 date as
  reported-not-verified, not settled law, if cited. **The separate
  reciprocal-tariff suspension / Section 301 exclusion question for 178
  Chinese products, substantially resolved at edition 57, saw no further
  development at edition 58**: the Federal Register filing (Doc 2025-21671,
  originally published 1 Dec 2025, located via govinfo.gov and a USTR PDF)
  still has the 178 exclusions lapsing at **11:59pm ET on Monday 9 November
  2026**, with the standard Section 301 rate (approx. 25%, per multiple
  trade-law secondary sources) resuming **Tuesday 10 November 2026** absent a
  further extension. No new USTR extension had been filed as of edition 58's
  check. **This now falls inside edition 60's plausible window (the Monday 9
  Nov session, if no gap) for the lapse itself, with the rate-resumption
  taking visible effect inside edition 61's window (Tuesday 10 Nov)** — check
  federalregister.gov/govinfo.gov directly for any last-minute extension
  filing across both.
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
  status not specifically re-checked at edition 58, watch again.** Democrats
  won control of both the House and Senate — called by AP/CNBC/NBC/PBS by
  Wednesday 4 November morning — ending unified Republican control of
  Washington. Democrats flipped at least seven Senate seats (Iowa, Kansas,
  Ohio, North Carolina, New Hampshire, South Carolina, Texas); a handful of
  races were still uncalled as of edition 57's cutoff and this was not
  independently re-checked at edition 58 — do not cite a final seat count
  without re-checking. **The election's second-order market effect dominated
  edition 58's own session**: Tuesday's local ballot measures rejected
  data-center buildouts in 40 of 41 votes, and UBS flagged approx. 30% of
  2028 data-center capacity additions as at risk under the incoming
  Democratic Congress — this drove Thursday 5 November's broad AI-capex
  selloff (S&P -4.4%, Nasdaq -5.5% into correction territory, VIX +69.66% to
  28.18), a near-complete reversal of Wednesday's election-rally session.
  **Re-verify certification status and watch for any further policy response
  (fiscal, trade, AI/data-center regulation, Iran) in the next several
  editions' macro passes.**
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
  - **European Central Bank:** rate complex (deposit facility 2.50%, main
    refi 2.65%, marginal lending 2.90%) remains **SETTLED** (promoted at
    edition 55 after a third consecutive direct reconfirmation) — not
    re-attempted at edition 56, 57 or 58 (no fetch needed). It reopens on
    contradiction, the next Governing Council decision, or the monthly audit.
    The press-conference-content/vote-split sub-question and the exact
    next-meeting date both remain unconfirmed/unreachable (not re-attempted at
    edition 58, out of scope) — still estimated mid-December by typical
    six-weekly cadence, not verified; this remains the ECB's one outstanding
    live sub-question, worth a dedicated check once a window approaches that
    date.
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
    split/dissent from the 4 Nov decision was not stated in the release and
    remained unresolved at edition 58** — minutes are due **10 November
    2026** (likely landing inside edition 60's window) — treat the vote
    detail as a live open sub-question until then.
  - **Banxico — MAJOR UPDATE at edition 58, a surprise cut.** Per consistent
    multi-outlet Mexican financial press (Milenio, El CEO, Exc&eacute;lsior-
    affiliate, PorEsto, Grupo Animal, Almomento), Banxico **cut its
    overnight interbank rate 25bp, from 6.50% to 6.25%**, effective 6
    November 2026, against a consensus expectation of a hold — a **3-2
    vote**, Deputy Governors Galia Borja G&oacute;mez and Jonathan Heath
    dissenting in favor of holding. Headline inflation rose to 3.62% y/y in
    October (from 3.42% in September); Banxico raised its Q4 2026 inflation
    forecast but signaled intent to hold the new rate for a prolonged period.
    Minutes due 19 November 2026; **next decision 17 December 2026**
    (secondary-sourced, same convergence date as several other banks this
    cycle). **banxico.org.mx and its anterior mirror both failed again
    (404/redirect) on every path tried at edition 58** — this remains
    secondary-sourced only, not directly primary-confirmed, for a further
    edition. Try a fresh URL path or the English-language IR site again at
    edition 59.
  - **Government funding/shutdown status:** H.R. 6500 funds federal agencies
    through 11 December 2026, no shutdown in effect — **a direct
    whitehouse.gov fetch succeeded cleanly at edition 58** (an upgrade from
    edition 57's one-edition sourcing-tier downgrade, which had returned
    inconclusive content), confirming the President signed H.R. 6500 on 2
    September 2026. Continue the standard re-check-every-edition discipline
    regardless.
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
  Situation Summary. **October's employment report is expected Friday 6
  November 2026** (if on the normal schedule) — a consensus figure still has
  not been found despite repeated attempts across editions 55, 57 and 58
  (various vendors searched each time); appears genuinely not yet published
  ahead of the release. **This lands inside edition 59's window** (if no
  gap) — the actual print, not just the consensus, should be sought then.
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
  notice of appeal is still unconfirmed for a THIRTEENTH straight edition
  (47-58).** Meta owes **$25bn** in civil penalties for the jury's
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
  re-attempted at editions 55 through 58 (out of scope); no new development
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
- **The vendor-retroactive-revision trap continued at edition 58, mixed
  results — mostly clean this time.** WTI and Brent both reconciled cleanly:
  a fresh Investing.com pull of Wednesday 4 Nov's own base matched edition
  57's logged figures almost exactly (WTI $88.12/-8.29%, Brent $94.62/
  -8.67%), resolving the more substantive WTI discrepancy flagged at edition
  57 without further action needed (it appears to have been a one-off). FX
  crosses (EUR/USD, GBP/USD, USD/JPY) also matched the prior edition's logged
  Wednesday base exactly, no revision. A mild variance recurred on gold/
  silver futures Wednesday bases (approx. 0.05-0.10 percentage points,
  immaterial) — consistent with the small-variance pattern seen at editions
  56-57. **Treasury yields matched the prior edition's logged Wednesday base
  exactly**, extending that series' clean streak. Keep the every-edition
  re-fetch-and-compare discipline regardless.
- **Henry Hub: now a THIRD consecutive clean two-source reconciliation at
  edition 58 — per the plan set at edition 57, this thread can be treated as
  substantially closed going forward**, downgraded further from "elevated"
  priority. Edition 58 found Investing.com's Thursday close ($2.943/MMBtu,
  -0.54%) and Yahoo Finance's NG=F close ($2.946, -0.44%) within approx. 0.1%
  of each other, agreeing on direction and magnitude — tighter than either of
  the two prior clean editions. Still NGZ6 (December); watch for the roll to
  NGF7 (January) as November progresses. Resume only occasional spot-checks
  rather than the dedicated every-edition reconciliation effort, unless a
  fresh conflict appears.
- **westmetall.com (LME copper) — a NEW sourcing issue surfaced at edition
  58: the site had not yet posted Thursday 5 November's settlement row at
  research time**, a different failure mode from the historical "only
  exposes the current day's row" pattern documented at edition 54 (which
  remains a valid workaround for its own specific scenario). Most recent
  confirmed LME copper figure as of edition 58 is Wednesday 4 Nov (cash
  $14,201.00/t, 3-month $14,095.00/t, matching edition 57's own logged
  figure exactly, no revision) — carried forward and flagged unavailable for
  Thursday in Annex B. **Watch at edition 59 whether this is a one-off
  publication lag or a new recurring problem**; a COMEX cross-check
  (Investing.com, $6.2295/lb, -3.10% Wed→Thu) remains available as a
  fallback direction/magnitude indicator even when LME itself lags.
- **New sourcing-mechanics trap logged at edition 50, relevant to any
  Monday-dated (or any day-after-a-non-trading-day) edition: Investing.com
  inserts an electronic Sunday-evening re-open print as its own row for every
  24-hour-traded instrument.** Not applicable at edition 58 (a normal weekday
  session following a normal weekday session) — continue applying this
  discipline on every post-weekend or post-gap edition.
- **The Kitco live-spot-vs-headline cross-check's conflict mode changed AGAIN
  at edition 58 — now its third distinct conflict pattern in three
  editions.** Gold futures (+0.56%) and Kitco spot (-0.31%) disagreed on
  **direction** this time (not just magnitude, as at edition 57); silver
  futures (-1.06%) and Kitco spot (-0.08%) agreed on direction but with an
  approx. 13x magnitude gap, wider than the "roughly triple" pattern noted at
  edition 57. **A new wrinkle: Kitco's own self-reported prior-day baseline
  did not reconcile with the prior edition's logged Wednesday Kitco close**
  (implying a Kitco-internal reference-price inconsistency, not just a
  cross-source gap) — treat Kitco spot figures as directionally indicative
  only until this is better understood. Continue attempting both metals
  directly each edition and disclosing whichever conflict (sign, magnitude,
  or now internal-baseline) appears; this sub-item has not yet had a single
  fully clean edition.
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
  and a claimed Oracle analyst-upgrade note (edition 56).
- **The edition-49 "forward-looking calendar aggregator" trap (names falsely
  listed as past or future reporters when the actual date differs) remains
  closed as a general pattern.** It gained two fresh instances at edition 57
  (Amdocs' Form 6-K date, Kyndryl's actual filing date), both caught via
  direct SEC EDGAR checks. **Not specifically re-tested at edition 58**
  (no forward-looking aggregator date claim was investigated this edition) —
  resume the discipline whenever a day-ahead calendar entry rests on an
  aggregator's claimed date rather than a primary filing.
- **A megacap multi-name earnings cluster producing genuinely uncorrelated
  reactions is a standing, repeated pattern — now at least ELEVEN distinct
  instances through edition 58 (editions 44, 47, 48, 49 x2, 50, 52, 53 x3,
  58).** Edition 58 added a clean new pair: Atlassian fell -15.98% AH despite
  a clean Q1 FY27 beat (revenue +24%, EPS beat), and Natera fell -16.15% AH
  despite revenue +34% and a raised FY26 guide — both counter-examples to
  Cloudflare, JFrog and Airbnb all rising on beats the same evening. Edition
  57 had NOT added a new instance (a session where beats rose and misses
  fell across the board); edition 56 added a positive counter-example (AMD).
  Continue treating beat-and-raise (or a guidance cut) as having no
  *guaranteed* effect on the reaction without checking the actual outcome.
- **New production lesson from edition 53: CSS multi-column (`.cols3`/
  `.cols2`) pagination under Chromium print-to-PDF can plateau stubbornly on
  marginal content trims** — see the condensed mega-block below for the
  mechanics and the fix. **Not triggered at editions 54 through 58** — all
  five editions converged cleanly on the first render, including edition
  58's genuinely dense content (a double central-bank surprise, a sharp
  FOMC-odds swing, an AI-capex selloff with 0-of-11 sector breadth, a VIX
  contango-to-backwardation inversion, and a 12-plus-name earnings cluster) —
  further reinforcing that edition 53's plateau was content-volume-specific
  rather than a general property of the CSS approach.
- **New at edition 54: the VIX feed's two known bugs (duplicated
  `prev_day_close`, and a `price_change_percent` that divides by the wrong
  price) appeared on ALL SIX series at edition 54, not intermittently as
  several prior editions found. At editions 55 through 58, by contrast, BOTH
  bugs were ABSENT on all six series for four consecutive editions** — the
  feed's own reported `price_change_percent` matched an independently
  computed manual calculation to four decimal places on every series every
  time, including at edition 58 despite the VIX complex's extreme one-day
  move (+69.66% on VIX, +115.01% on VIX9D). **Continue the manual-calculation
  discipline unconditionally regardless of how many bug-free editions might
  follow** — four clean editions is still not evidence the bug is fixed for
  good.
- **New at edition 54: a markup-correctness self-check caught three
  instances of the `</td><sup` table trap (documented under Production
  notes below) before rendering.** Editions 55 through 58 all ran the same
  proactive `grep -n '</td><sup'` check and found **ZERO instances for a
  fourth consecutive edition** — worth continuing on every edition with a
  table that has an empty trailing cell or a cell containing only a
  citation.
- **New at edition 54: the CFTC Asset-Manager-vs-Leveraged-Funds grouped-bar
  chart was reused for a fifth time (editions 34, 39, 44, 49, 54 — a clean
  Monday/weekend-window pattern) with the same figsize (9.8, 2.15), `h=0.32`
  bar offset and figure-level legend technique documented under Production
  Notes.** **Editions 55 through 58 did not use the chart** — no fresh CFTC
  data fell inside any of those four single-session windows (the Friday 30
  Oct report, covering Tuesday 27 Oct data, remains the most recent as of
  edition 58's cutoff), and in each case a genuinely present alternative
  story was judged more dominant (VIX term structure at 55/56, election/
  earnings density at 57, the AI-capex selloff and VIX backwardation
  inversion at 58 — edition 58 specifically judged the chip-sector selloff
  and earnings cluster the dominant story over the VIX move, consistent with
  edition 57's same judgment call). **The next opportunity is the Friday 6
  November 2026 report (covering Tuesday 3 Nov data)** — this falls inside
  edition 59's window (if no gap); check cftc.gov directly then.

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
  **Editions 54 through 58 have all now converged cleanly within one or two
  renders** (54 after deleting the one forced break; 55 through 58 all on
  the very first render with the break retained, sections 1-6 ending within
  page 3 every time) — reinforcing that content density alone does not
  predict whether a trim marathon will be needed; check the actual render
  before assuming one is. Edition 58 is the strongest data point yet: a
  double central-bank surprise, a sharp FOMC-odds swing, a 0-of-11-sector
  selloff day, a VIX term-structure inversion and a 12-plus-name earnings
  cluster all converged on the first render.
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
  corrects nothing**, which will be most of them. **Editions 54 through 58
  have all omitted the box** — in each case nothing published in a prior
  edition was found to be wrong. (Edition 58's own Qualcomm AH-snapshot
  supersession was treated as new information arriving on schedule, not a
  correction, since the prior edition correctly labeled the figure as an
  unconfirmed snapshot rather than asserting it as a close — consistent with
  how edition 57 itself handled the WTI/vendor-revision items.)
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
  Section 6's "sector setup we take into [session]" bullets stay where they
  are; they are forward-looking, not a recap of what happened.
- **Section 3 carries a central-bank policy-rate table.** Columns: **Central
  bank | Policy rate | Last change | Next decision**. The Fed goes first as
  the anchor to compare against, then whichever of the BoE, BoJ, ECB, SNB,
  Norges Bank, Riksbank, RBA, BoC and Banxico the window actually touches —
  eight to ten rows is the working range. A bank whose current rate could
  not be verified still gets its row, with that cell marked unavailable and
  a matching Annex B entry. **Editions 54 through 58 have all run the same
  full 10-row table** (Fed, BoJ, BoE, ECB, BoC, RBA, SNB, Norges Bank,
  Riksbank, Banxico). **Edition 58 saw two cells change via genuine policy
  moves rather than sourcing breakthroughs**: BoE's rate (3.75%→4.00%,
  now primary-sourced following the 5 Nov hike) and Banxico's rate
  (6.50%→6.25%, still secondary-sourced following the surprise 5 Nov cut).
  Only Banxico's rate and next-decision date remain imperfectly
  (secondary-only) sourced as of edition 58 — the smallest "unavailable/
  imperfect" footprint this table has carried since the policy-rate table
  was introduced. Follow the usual table convention — plain `<tr>` header
  rows, no `<thead>`.
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
  editions 34, 39, 44, 49, 54). **Editions 55 through 58 did not use a third
  chart** — in each case no fresh CFTC data fell inside the window; a
  genuinely present VIX-complex story existed in all four (a kinked term
  structure at 55, its narrowing at 56, a dramatic one-day collapse at 57,
  and a full contango-to-backwardation inversion at 58), but the
  equity/earnings/central-bank story was judged more dominant each time,
  consistent with the general practice of covering a real-but-secondary VIX
  story fully in prose instead. Next CFTC report due **Friday 6 November
  2026**, covering Tuesday 3 November data — check cftc.gov directly
  whichever edition's window includes it, likely edition 59.
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
  radio-station website). **Editions 55 through 58 have all successfully used
  the dual La Naci&oacute;n/WTOP mirror approach — now FIVE consecutive
  successes.** This is the established first-choice workaround; try it
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
  discrepancy (edition 55's Brent crude move), and **a figure with no
  corroborating primary filing at all (DraftKings' circulated -22.24% AH
  claim, ed.58, excluded entirely rather than hedged)** — treat ANY
  surprising secondary claim (price move, driver, analyst action, date, or
  computed percentage) as needing this same verification discipline.
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
  disagreements.
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
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent —
  recurred again at edition 58** after resolving cleanly for edition 57's
  own session. Yahoo Finance's DX-Y.NYB (+0.10%) and an Investing.com
  futures-style DXY proxy (-0.05%) disagreed on direction; a
  methodology-continuity flag was raised (the Investing.com series used may
  track the same underlying index as Yahoo's rather than being genuinely
  independent) — worth a dedicated look at a future edition with spare
  research bandwidth. Keep disclosing the DXY-vs-FX-crosses comparison every
  edition regardless of which way it goes.
- **The Kitco live-spot-vs-headline cross-check changed conflict mode again
  at edition 58** — see the dedicated Standing Facts entry above: a third
  distinct pattern in three editions (sign conflict at 56, magnitude gap at
  57, sign conflict on gold plus a magnitude gap on silver plus an internal
  baseline inconsistency at 58). Disclose whichever form the conflict takes
  explicitly rather than picking one reading.
- **GBP/USD, EUR/USD and USD/JPY all reconciled cleanly again at edition 58**
  against their logged Wednesday base, with no revision on any of the three
  — the vendor-revision trap this edition hit gold/silver mildly again but
  not the FX crosses or Treasuries.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for twenty-three further editions (37-58)** — edition 58 again found the
  full Treasury curve reconciled cleanly against the official
  home.treasury.gov TextView page (2-year 4.46%, 10-year 4.84%, 30-year
  5.25%, down 3-12bp across the curve on the day, consistent with the
  equity-selloff flight-to-quality narrative), with the prior Wednesday base
  matching the previous edition exactly. Treat as resolved/noise unless a
  fresh conflict appears.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 58 have all run clean (or
  clean after quick fixes) — **edition 54 needed one fix; edition 55 needed
  two fixes; edition 56 needed one fix; edition 57 needed one fix; edition
  58 needed ZERO fixes — clean on the very first check**, the first edition
  in this recent run to need no correction at all.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 55 rendered with zero stray tildes on the first
  draft; edition 56 needed one fix; edition 57 also needed one fix; edition
  58 again rendered with zero stray tildes on the first draft** — a
  reminder that the fix/no-fix pattern doesn't correlate cleanly with
  content density (edition 58 was arguably the densest of the run).
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
  falls inside edition 59's plausible window — check cftc.gov directly then.
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
  record** — no capping needed in any edition since 45. Used `pad_frac=0.24`
  for edition 58's movers chart (figsize (9.8, 1.75), 7 categories, max abs
  value approx. 54.68%, range -54.68% to +31.04%) and `pad_frac=0.30` for
  the 11-category sector panel (figsize (9.8, 1.95)), both rendering
  cleanly with no label crowding.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 58 have all got a fresh,
  same-day-timestamped sweep** — thirty-one consecutive fresh sweeps now.
  **The feed's two known bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) appeared on ALL SIX series at edition 54 but were ABSENT on all six
  series at editions 55 through 58** (the feed's own reported percent-change
  matched an independent manual calculation to four decimal places all four
  times). **Always compute day-over-day % change manually regardless of how
  many consecutive bug-free reads preceded the current one.** Edition 58 saw
  the VIX complex spike sharply (the mirror image of edition 57's record
  decline) on the AI-capex/data-center selloff: VIX +69.66% to 28.18, VIX9D
  +115.01% to 32.66, VIX3M +35.90% to 25.55, VIX6M +22.29% to 25.29, VVIX
  +49.31% to 134.99, SKEW -1.01% to 149.37 — the sharpest one-day VIX
  *increase* logged in this report's history (mirroring edition 57's record
  decline the day before). Wednesday's clean ascending contango fully
  inverted into backwardation: VIX9D (32.66) > VIX (28.18) > VIX3M (25.55) >
  VIX6M (25.29).
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 58 fetched all 11 directly again**
  (Communication Services -0.59% the relative leader on a defensive
  rotation, Utilities -0.71% and Consumer Staples -0.75% also relatively
  resilient; Technology the clear laggard at -8.00%, nearly double the next
  worst sector, Industrials -4.12% and Consumer Discretionary -3.83% also
  hit; 0 of 11 green, a complete reversal of Thursday's... i.e. Wednesday's
  9-of-11 advance) — continue this direct-fetch-by-default method.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (0 of 11 at edition 58, the
  starkest reading logged to date) — no competing secondary-aggregator
  breadth figure was checked this edition.
- **Dealer gamma:** zerogex.io hit a **NINETEENTH consecutive edition of
  failure at edition 58** (all widgets still show placeholder dashes with no
  timestamped data). SpotGamma logged a **THIRTEENTH straight failure at
  edition 58**, confirmed again as a client-side React single-page app with
  zero server-rendered data behind its dashboard.spotgamma.com login. Both
  sources remain fully unusable for structured data.
- **Official CME FedWatch probabilities:** the page blocks fetching
  (edition 58's direct attempt timed out again, an **EIGHTEENTH** consecutive
  failure, 41-58) — use secondary citations (Polymarket, Kalshi, Reuters/
  other economist polls, desk notes) and give a range rather than a single
  invented number. **Polymarket direct, tried via its Gamma API
  (`gamma-api.polymarket.com/public-search`) rather than a plain site visit,
  succeeded again at edition 58 — a fifth consecutive success** — this
  remains the preferred first approach; try it before reverting to a plain
  site visit. DeFi Rate's blended aggregator returned a stale (late-Sept)
  snapshot at edition 58 — worth retrying at edition 59 to see if it has
  refreshed; if it has, resume the cross-check discipline.
- **Kalshi direct fetch:** rate-limited or blocked across every edition it
  has been attempted, now **TWENTY-TWO consecutive failures (37-58)** — a
  confirmed structural gap, not transient (edition 58's specific failure
  mode was again HTTP 429). Resume the attempt-every-edition discipline at
  edition 59 regardless, but expect a block of some kind. Use Kalshi's own
  secondary reporting or DeFi Rate's blended aggregator as the workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **westmetall.com (LME copper) remains
  the standing primary source but hit a new, different failure mode at
  edition 58** — see the dedicated Standing Facts entry above (the site
  simply hadn't posted Thursday's row yet, as opposed to its historical
  "exposes only the current day" behavior).
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **remained clean at edition 58** (2-yr
  4.46%, 10-yr 4.84%, 30-yr 5.25%, all 5 Nov, with the prior Wednesday base
  matching the previous edition exactly), extending the clean streak to
  **twenty-three editions (37-58)** with no repeat of the edition-36 33bp gap.
  Continue scoping the TextView URL to the specific month
  (`field_tdr_date_value_month=202611`-style parameter) rather than the
  full year.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). **No new report fell inside edition 58's single-session
  window** (the Friday 30 Oct report, covering Tuesday 27 Oct data, remains
  the most recent) — confirmed nothing posted early. **The next report is
  due Friday 6 November 2026, 3:30pm ET, covering Tuesday 3 November data**
  — this falls inside edition 59's plausible window (if no gap) — check
  cftc.gov directly then. The CFTC release-schedule change (moving to
  twice-weekly releases by end of 2026, per a 27 Oct 2026 CFTC announcement,
  Press Release 9316-26) still has **no confirmed start date** as of edition
  58 — proposed structure: Monday data published Wednesday, Wednesday data
  published Friday, both at 3:30pm ET; worth a one-line check when the 6
  November report actually lands, in case the covered-data convention has
  shifted by then.
- **GBP/USD, EUR/USD, USD/JPY clean close:** all remain fully resolved,
  reconciling cleanly again at edition 58 (EUR/USD 1.1219 -0.09%, GBP/USD
  1.3451 -0.16%, USD/JPY 157.68 -0.49%, all single-sourced to Investing.com's
  close-to-close history table, Wednesday base matching this edition's own
  fresh re-fetch exactly). **DXY itself has now flipped back to an
  unresolved cross-source direction conflict for edition 58's own session**
  — see the dedicated Standing Facts and Hard Rules entries above.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot cross-check changed conflict mode again at edition 58** — see
  the dedicated Standing Facts and Hard Rules entries above (now a third
  distinct conflict pattern in three editions, plus a new internal Kitco
  baseline-inconsistency wrinkle). Thursday 5 Nov base figures: gold futures
  $4,095.85 (+0.56%), silver futures $51.730 (-1.06%); Kitco spot gold
  $4,074.60 (-0.31%), spot silver $51.63 (-0.08%).
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is also a closed thread as of
  edition 45. **US GDP, PCE, import/export prices and industrial
  production:** all closed threads — see Standing Facts above. **University
  of Michigan October consumer sentiment** is a closed thread as of edition
  49. **China's October PMI** is a closed thread as of edition 54. **October
  ISM Services PMI** is a closed thread as of edition 57 (headline only;
  sub-index detail remains an Annex B item).
- **Henry Hub natural gas:** the front-month-contract-identity question
  remains resolved (NGZ6/December, watch for the roll to NGF7/January as
  November progresses). **The base-price reliability problem — this report's
  historically worst-performing data-quality issue — is now substantially
  CLOSED as of edition 58**, following a third consecutive clean two-source
  reconciliation (Investing.com, Yahoo Finance NG=F, within approx. 0.1% at
  edition 58) after the edition-56 breakthrough and edition-57's second
  clean read. Resume only occasional spot-checks rather than a dedicated
  every-edition reconciliation effort unless a fresh conflict appears.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 58 found no usable
  single-name implied-move or options-flow figure** (optionslam.com's fetch
  failed; zerogex.io and SpotGamma both remained unusable) — a quieter
  edition on this sub-item than edition 57's partial Qualcomm success.
  Treat the general sub-item as still reliably low-yield most editions, but
  worth a genuine attempt around any single dominant earnings story.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. **Q3's
  approx. 14 November 2026 deadline falls on a Saturday** — the natural lead
  item for whichever edition covers the following Monday, 16 November 2026
  (a weekend-gap edition), now about eight days out from edition 58's own
  date.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22, not attempted
  again since). Revisit only if a future edition has spare research
  bandwidth on an FOMC day specifically — not relevant to most editions.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully at
  editions 39, 44-49 and 54 (the Friday 30 Oct report, covering Tuesday 27
  Oct data). No new report fell inside editions 55 through 58's windows.
  Repeat the three-instrument fetch whichever edition's window extends past
  Friday 6 November, 3:30pm ET (likely edition 59), watching for the
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
  repeated. Watch each edition independently rather than assuming a trend.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** This discipline has now caught: Tesla/NU Holdings
  (ed.49, magnitude), JetBlue (ed.50, magnitude), Carvana/Barron's (ed.52,
  direction/framing), Marvell/Lumentum and Barclays/PayPal (ed.53), two more
  exclusions at edition 54, a claimed Oracle analyst-upgrade note at edition
  56, two forward-looking-calendar-aggregator date errors at edition 57, and
  **at edition 58: a fabricated DraftKings AH figure (no 8-K anywhere on
  EDGAR), an unsupported Natera driver claim, and an entire "biggest calls"
  analyst-action list found unsupported on spot-check.** At edition 58,
  every reported mover (Qualcomm, Arm, Tripadvisor, AppLovin, Krispy Kreme,
  Veracyte, MNTN, plus the semiconductor complex and the second-wave AH
  batch) was individually cross-checked against its own primary SEC filing
  (8-K or 6-K) rather than accepted from an aggregator list alone — continue
  this direct-verification discipline on every edition.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted at editions 48 through 58 (out of scope each time); try
  an alternate DOL page or a secondary economic-calendar aggregator for the
  consensus figure at edition 59.
- **federalregister.gov's direct search interface is blocked, re-tested
  directly again at edition 58 and still blocked** (a prior search attempt
  302-redirected to `unblock.federalregister.gov`, an apparent bot/rate-limit
  gate, first logged at edition 48). govinfo.gov continues to be the known
  working alternative route for at least some Federal Register content.
- **SEC EDGAR's `cgi-bin/browse-edgar` company-search page (filtered by CIK
  and form type 8-K) is a highly reliable, fast way to confirm both WHETHER
  a company has reported on a given date and to find the accession number
  for the underlying exhibit** — used again at edition 58 for Qualcomm, Arm
  (via its Form 6-K), Tripadvisor, AppLovin, Krispy Kreme, Veracyte, MNTN,
  Cloudflare, JFrog, Airbnb, Atlassian and Natera. **Edition 58 also
  demonstrated a valuable NEGATIVE use case**: the absence of any matching
  8-K for the circulated DraftKings AH figure was itself the evidence that
  disproved the claim, rather than merely confirming a true one — worth
  remembering that this tool is just as useful for debunking an unverifiable
  claim as for confirming a verifiable one.
- **Riksbank's primary policy-rate/next-meeting page:** fully resolved as of
  edition 57 (hiked to 2.00% on 4 Nov 2026) — see the dedicated Standing
  Facts entry above. The vote split from that decision remains unresolved
  pending minutes due 10 November 2026, likely landing inside edition 60's
  window.
- **ECB's current policy rate: SETTLED since edition 55** (reconfirmed
  directly for a third consecutive edition — 53, 54, 55 — unchanged through
  the 28-29 October 2026 meeting: deposit facility 2.50%, main refi 2.65%,
  marginal lending 2.90%); not re-attempted at edition 56, 57 or 58 (no
  fetch needed). Do not spend a fetch on the rate level itself going
  forward; it reopens on contradiction, the next Governing Council decision,
  or the monthly audit. **Its exact Governing Council press-conference
  content/vote-split remains unobtainable** and was not specifically
  re-attempted at edition 58 (out of scope) — low priority. **The Council's
  own next-meeting date is not yet known** — this remains the ECB's one
  outstanding live sub-question, worth a dedicated check once a window
  approaches the plausible next date (likely mid-December).
- **Banxico's own primary site (banxico.org.mx) remains unreachable** for a
  further edition (all paths tried, including the anterior mirror, 404'd or
  redirect-looped at edition 58) — now a confirmed structural gap across
  multiple editions, not transient. Continue the attempt-every-edition
  discipline, but rely on the consistent multi-outlet Mexican financial
  press as the working alternative when it fails.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel —
  confirmed clean again at edition 58 (nineteen editions total: 37-43,
  45-50, 52-58). For charts with fewer categories, scale the height down:
  roughly `(9.8, 1.65-1.95)` for 3-9 categories. **Edition 58 used `(9.8,
  1.75)` for a 7-category movers chart with `pad_frac=0.24`**, rendering
  cleanly with no label crowding despite a wide range (-54.68% to +31.04%)
  and the tightest largest-to-second-largest ratio logged to date (approx.
  1.007x). **Always render and visually inspect (via the Read tool) the
  actual PNG at or near full resolution before embedding it**, regardless of
  what a past edition's success might suggest. **Default to pad_frac=0.30
  from the start for an 11-category sector-ETF panel** — now confirmed
  across thirteen straight small-magnitude 11-category panels (45-50,
  52-58). For any movers chart with a double-digit-percent outlier, continue
  trying pad_frac in the 0.22-0.30 range from the start.
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
  rendering. **Editions 55 through 58 all ran the same proactive grep and
  found zero instances, a fourth consecutive clean sweep.** Run the grep on
  every edition with such a table, not just when troubleshooting a layout
  problem.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Edition 53 needed this discipline more than almost any prior edition.
  **Editions 55 through 58 all rendered cleanly on the first attempt** (no
  symptom to catch any time), but the page images were still read in full
  as standard practice every time, confirming no broken tables, no
  overlapping chart labels, and no cut-off content on any of the 4 pages.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across many editions'
genuinely different content volumes, including editions 53's through 58's.
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
  runs short — editions 44 through 58 have all folded commodities, FX and
  Treasuries into ONE combined table (10-17 rows; edition 58 used 17) as the
  PRIMARY commodities table rather than padding, now the standing default.
  **Always re-render immediately after adding (or removing) any content to
  confirm the page count.**

**Chart selection guidance.** Placement is not editorial for the first two
charts:

- **Sector-ETF performance chart → Section 1 (Market recap), every
  edition.** Same-day closes by default; a grouped day-over-day bar instead
  on a multi-session or weekend window, or on a genuine multi-sector
  broadening selloff across consecutive sessions. **Editions 54 through 58
  all used a single-day bar** (only one NYSE session fell inside any of
  those windows).
- **Single-stock movers bar → Section 2 (Equities), every edition.**
- **A third chart only when positioning or volatility is genuinely the
  day's dominant story**, never to fill a page, placed in the section it
  belongs to:
  - Fresh CFTC CoT data → the ES/NQ/RTY asset-manager-vs-leveraged-funds
    positioning chart, normalized as % of open interest, built with the
    grouped-bar technique documented under Production notes, in **Section
    5**. Editions 24, 34, 39, 44, 49 and 54 have all placed it there; none
    of editions 55 through 58 had fresh data to place it with. The next
    opportunity (Friday 6 Nov report, covering Tuesday 3 Nov data) falls
    inside edition 59's plausible window.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully. Not used at editions 55
    (Apple), 56 (AMD), 57 (Qualcomm) or 58 (no single name had a clean,
    uncontested, chartable implied-move figure this edition either —
    optionslam.com's fetch failed outright).
  - A holiday-window preview edition with no fresher data → VIX futures
    term structure with event annotations, in **Section 5**. Not used at
    editions 55 through 58 — in each case the VIX term structure was
    genuinely newsworthy (a kink, its narrowing, a dramatic one-day collapse
    at 57, then a full contango-to-backwardation inversion at 58) but was
    judged secondary to the session's dominant equity/macro story each time
    and was covered fully in prose instead.

**Edition 59 (expected to cover Friday 6 November 2026, assuming no gap)
has a real, contained macro-calendar load.** Watch directly rather than
assuming: **the October 2026 US nonfarm payrolls report** (8:30am ET Fri 6
Nov, lands inside edition 59's own window — this report has still not found
a consensus figure despite repeated attempts at editions 55, 57 and 58;
prioritize finding the actual print over the elusive consensus); **the next
CFTC Commitment of Traders report** (3:30pm ET Fri 6 Nov, covering Tuesday 3
Nov data — also lands inside edition 59's window, the first fresh CFTC data
since edition 54, a genuine opportunity for the third positioning chart if
the day's other news doesn't crowd it out); **whether December FOMC hike
odds continue to ease, stabilize, or partially reverse** from edition 58's
sharp approx. 66.5% read (a priority fresh pull, not routine upkeep, given
the magnitude of the swing); **whether DeFi Rate's blended aggregator has
refreshed** past its stale late-September snapshot; **whether Thursday's
AI-capex selloff extends, stabilizes, or reverses** in the semiconductor
complex and Technology sector specifically; and **whether the VIX
backwardation shape persists or renormalizes into contango**. It should also
retry: a fresh federalregister.gov search-interface attempt (still blocked
as of edition 58, govinfo.gov used as the workaround); westmetall.com's LME
copper settlement (watch whether Thursday's missing row was a one-off lag
or a new recurring problem); and Banxico's own primary site (unreachable
again at edition 58, try a fresh URL path). The La Naci&oacute;n/WTOP
double AP-wire-mirror approach and the Polymarket Gamma-API approach are
both now on five-edition clean streaks — use them first rather than their
respective fallbacks.

**Remember the figsize-scales-to-category-count guidance above
(ceiling `(9.8, 1.95)` for an 11-category panel, `(9.8, 2.15)` for the
3-category grouped CFTC chart, scale down for fewer single-series
categories), that an 11-category sector-ETF panel should default to
pad_frac=0.30 from the start (now confirmed across thirteen editions,
including 58), a movers chart with a double-digit-percent outlier should try
pad_frac in the 0.22-0.30 range from the start (edition 58 used 0.24 for a
7-category panel spanning -54.68% to +31.04%, ratio approx. 1.007x, the
tightest logged to date), and the capped-outlier asterisk/footnote fix when
a spread crosses the approx. 5x RATIO threshold** (it has not since edition
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

**Edition 57's carried-forward spec was 128,689 bytes, over the 100,000-byte
threshold — this run (producing edition 58's spec) folded edition 56's
condensed paragraph into the running mega-block (now "Editions 1-56") and
condensed edition 57's own full-detail entry down to a medium paragraph, per
the log's own standard rotation.** There is no maximum size; condensing is
housekeeping done by the run itself, not a check to pass — there is no
penalty for the file staying somewhat large if the alternative is losing
information.

**Editions 1–56 (condensed):** established the format (edition 1 baseline;
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

**Edition 56 (condensed)** — Wednesday 4 November 2026 report covering
Tuesday 3 November 2026, the window's one NYSE session. Equities diverged on
composition, not breadth: S&P +0.36% to 7,568.92 and Nasdaq +0.83% to
25,372.01 on a megacap/AI bounce (Nvidia +2.29%, Oracle +5.85%) even as the
Dow fell 0.38% to 51,786.72; only 4 of 11 sector ETFs closed higher. The RBA
delivered its fifth 2026 hike (25bp to 4.85%) on a first-ever split 6-3
vote. AMD's fiscal Q3 (revenue $13.4bn +45% y/y, Data Center +97%) drew a
genuinely positive AH reaction (+5.02%), a counter-example to the week's
muted-to-negative beat-and-raise reactions. Coinbase and Strategy partly
retraced Monday's Binance-hack selloff. A claimed Oracle analyst-upgrade
note was investigated and rejected as unreliable. The Bank of England's 5
November decision date was upgraded to primary-sourced; Henry Hub
reconciled cleanly across two sources for the first time in six editions;
the VIX feed's two known bugs were absent for a second consecutive edition;
a carried Caterpillar earnings-date planning assumption was corrected
before publication. Rate-path odds firmed to approx. 74-75% hike. No
shutdown in effect; Riksbank's rate value and Banxico's rate/next-decision
both remained unconfirmed directly, each for a further edition. First draft
converged cleanly to 4 pages on the first render; 29/29 sources clean after
one fix; zero stray tildes after one fix; zero `</td><sup` instances.

**Edition 57 (condensed)** — Thursday 5 November 2026 report covering
Wednesday 4 November 2026, the window's one NYSE session. **Dominant story:
the 3 November 2026 US midterm elections**, called for Democrats in both
chambers by Wednesday morning, ending unified Republican control — Dow
+3.03% to 53,356.12 (this report's then-largest one-day move), S&P +1.58%
to 7,688.62, Nasdaq +1.44% to 25,736.51; WTI crashed 8.3% to $88.12, Brent
-8.67% to $94.62; VIX posted its then-sharpest one-day decline, -20.26% to
16.61, fully resolving a term-structure kink into clean ascending contango.
Vice President Vance publicly blamed the loss on "the war" with Iran. Nine
of 11 sector ETFs closed higher (Consumer Discretionary +4.26% led; Energy
-4.74% and Industrials -1.09% the only decliners). Seven single-stock
movers, each verified against its own primary filing: Amdocs -30.07% on a
shock guidance cut (a T-Mobile contract dispute); Qualcomm +5.33%
regular/-7.52% AH (a late snapshot, later superseded — see edition 58) on
an FQ4 miss; Uber +4.91% on a beat; Helen of Troy +25.39% after rejecting a
$37.00/share buyout; Duolingo +25.99% on a beat; Kyndryl +30.14% on a beat;
Cricut +48.74% on a beat plus a special dividend. Two forward-looking-
calendar-aggregator date errors (Amdocs, Kyndryl) were caught and corrected
pre-publication via SEC EDGAR. Sweden's Riksbank delivered a surprise 25bp
hike to 2.00%, its first since 2023, resolving a three-edition rate-value
gap; the RBA's next decision was independently resolved at 7-8 December
2026. October's ISM Services PMI printed 54.5 (vs. 54.8 consensus).
December FOMC hike odds firmed to approx. 77-80% (since reversed sharply —
see edition 58). A Federal Register filing resolved the Section 301
178-product exclusion lapse date (9 Nov 2026, standard rate resuming 10
Nov). Henry Hub posted a second consecutive clean two-source reconciliation
(since closed — see edition 58); the DXY Yahoo-vs-Investing.com conflict
resolved for the session (recurred at edition 58); the Kitco spot-vs-futures
sign conflict from edition 56 did not recur, a magnitude gap took its place
instead (a third distinct pattern emerged at edition 58). A WTI Tuesday-base
continuity discrepancy was disclosed and not reconciled (resolved cleanly
at edition 58's own continuity check). Veterans Day (11 Nov) was
independently confirmed as an equities-open/bonds-closed holiday. Format:
no correction box; first draft converged cleanly to 4 pages on the first
render; 33/33 sources clean on check_refs.py after one fix; zero stray
tildes after one fix; zero `</td><sup` instances. A dedicated verification
pass was run on the election outcome and the Riksbank decision given how
consequential and surprising both were.

**Edition 58 (most recent — full detail)** — Friday 6 November 2026 report
covering Thursday 5 November 2026, research window Wed 4 Nov 2026 20:00 ET
through Thu 5 Nov 2026 20:21 ET (the window's one NYSE session).

**The session's dominant story was a full, sharp reversal of Wednesday's
election rally, driven by an AI-capex/data-center-moratorium scare.** Local
ballot measures tied to Tuesday's midterms rejected data-center buildouts in
40 of 41 votes, and UBS flagged approx. 30% of 2028 data-center capacity
additions as at risk under the incoming Democratic Congress — AP, Bloomberg
and Reuters/Investing.com's "Trading Day" column all converged on this as
the proximate driver. The S&P 500 fell 4.4% to 7,353.73 (-334.89 pts), the
Dow fell 3.4% to 51,523.06 (-1,833.06 pts), the Nasdaq Composite fell 5.5%
to 24,315.00 (its worst day since April 2025, into correction territory,
approx. $2tn of market value erased per Bloomberg), and the Russell 2000
fell 4.4% to 2,729.89, all confirmed via a dual AP-wire mirror (WTOP and La
Naci&oacute;n) plus ETF-proxy triangulation, with a six-cent/rounding-level
variance against an independent Reuters-sourced cross-check disclosed but
not treated as a genuine conflict. Zero of 11 SPDR sector ETFs closed
higher — a complete reversal of Wednesday's 9-of-11 advance — with
Technology (XLK -8.00%) by far the laggard, nearly double the next-worst
sector (Industrials -4.12%); defensives (Communication Services -0.59%,
Utilities -0.71%, Consumer Staples -0.75%) held up best in relative terms.
The semiconductor complex carried the sector story at the single-stock
level: Micron -17.46%, AMD -17.26%, Marvell -16.43%, Broadcom -10.43%,
Intel -10.33% and Nvidia -9.26%, with the Philadelphia Semiconductor Index
down more than 12%, its second-largest drop on record — none traced to
company-specific news in the window; AMD's own strong fiscal Q3 beat had
been reported 3 November, before this window opened.

**The VIX posted its sharpest one-day increase logged in this report's
history**, +69.66% to 28.18 — a near-mirror-image of Wednesday's own
record decline — fully inverting Wednesday's clean ascending contango into
backwardation (VIX9D 32.66 > VIX 28.18 > VIX3M 25.55 > VIX6M 25.29). All six
series carried a fresh same-session `last_trade_time`; both of the feed's
two historical bugs remained absent for a fourth consecutive edition; every
percentage was independently recomputed from raw levels and matched the
feed's own figures exactly, including through this extreme move.

**A dense single-stock earnings cluster, each move individually verified
against its own primary SEC filing (8-K, or Form 6-K for Arm Holdings):**
Qualcomm -9.49% confirmed regular-session close (superseding edition 57's
logged -7.52% AH snapshot — a supersession, not a correction, since the
prior figure was correctly labeled a snapshot at the time) on an FQ4 EPS
miss; Arm Holdings -13.08% on in-line-but-secondary-sourced revenue;
Tripadvisor -27.65% on a $369.5m goodwill impairment plus same-day CEO and
CFO departures; AppLovin +31.04% and Krispy Kreme +30.68% on strong
beats/guides; Veracyte -54.30% and MNTN -54.68% both on guidance cuts
despite revenue growth (magnitudes 8-K-confirmed but not independently
corroborated by a second outlet). A second wave of after-hours earnings
produced another "beat guarantees nothing" split: Cloudflare, JFrog and
Airbnb all rose on beats (AH snapshots, not yet confirmed to hold) while
Atlassian and Natera both fell despite clean beats of their own — reported
explicitly as unconfirmed AH snapshots rather than folded into the formal
movers table. Three new instances of the "named secondary outlet can be
flatly wrong" trap were caught and excluded: a widely-circulated DraftKings
AH figure (-22.24%) with no corresponding 8-K anywhere on EDGAR (DraftKings'
confirmed regular close was actually +1.77%), an unsupported "new CEO"
driver claim for Natera's decline, and an entire circulating "biggest
calls" analyst-action list that was spot-checked and found unsupported in
full.

**Two central banks delivered opposite surprises the same session — this
report's first-ever same-day hike/cut split.** The Bank of England raised
Bank Rate 25bp to 4.00% (8-1, Catherine Mann dissenting for a larger 50bp
move) — its first hike since August 2023 — confirmed directly against
bankofengland.co.uk, citing Middle East-conflict energy-price risk; next
decision 17 December 2026. Banxico reportedly cut 25bp to 6.25% against a
consensus hold (3-2 vote), secondary-sourced only via six independent
Mexican financial-press outlets after banxico.org.mx again failed every
URL path tried; next decision 17 December 2026 (also secondary-sourced).
December 8-9 FOMC hike odds eased sharply to approx. 66.5% (from approx.
77-80% at edition 57) per a fresh Polymarket Gamma-API pull, coincident
with the equity selloff and a 3-12bp Treasury rally (2-year -12bp to
4.46%); DeFi Rate's blended aggregator returned only a stale late-September
snapshot, not usable as a cross-check this edition. Oil partially rebounded
off Wednesday's crash (WTI +3.56% to $91.26, Brent +3.88% to $98.29)
without a confirmed fresh news catalyst. Henry Hub posted a third
consecutive clean two-source reconciliation, substantially closing that
historically troublesome thread. Gold and silver again split
futures-vs-spot, this time on direction for gold and a wide (approx. 13x)
magnitude gap for silver, with a new wrinkle: Kitco's own implied prior-day
baseline did not reconcile against the prior edition's logged figure. DXY's
two benchmarks (Yahoo, Investing.com) disagreed on direction again after
resolving cleanly for edition 57. LME copper's Thursday settlement had not
posted at westmetall.com at research time — a new failure mode, flagged in
Annex B, with Wednesday's figure carried forward. US government funding
status was cleanly re-confirmed directly against whitehouse.gov, an upgrade
from edition 57's one-edition sourcing-tier downgrade.

**Format:** no correction box (the Qualcomm AH-snapshot supersession was
treated as new information on schedule, not a formal correction, consistent
with how the prior edition's own snapshot caveats were handled). First
draft converged cleanly to 4 pages on the first render, with the forced
break retained (sections 1-6 ended within page 3; page 4 had some unused
space at the bottom). **21/21 sources clean on check_refs.py with ZERO
fixes needed — the first edition in this recent run to need no correction
at all.** Zero stray tildes on the first draft; zero `</td><sup` instances
found on a proactive grep. The macro research pass independently
primary-sourced the Bank of England decision directly and cross-verified
Banxico's cut against six independent outlets, given how consequential and
surprising both central-bank moves were.

**Open threads for edition 59.** Edition 59 covers **Friday 6 November
2026** (if no gap). Watch directly rather than assuming: **the October 2026
US nonfarm payrolls report** (8:30am ET, lands inside this edition's own
window; still no consensus figure found despite repeated attempts at
editions 55, 57 and 58 — prioritize the actual print); **the next CFTC
Commitment of Traders report** (3:30pm ET, covering Tuesday 3 Nov data,
also lands inside this edition's window — the first fresh CFTC data since
edition 54, a genuine opportunity for the third positioning chart);
**whether December FOMC hike odds continue to ease, stabilize, or partially
reverse** from edition 58's sharp approx. 66.5% read (treat as a priority
fresh pull); **whether Thursday's AI-capex selloff extends, stabilizes, or
reverses**, and whether the VIX backwardation shape persists or
renormalizes into contango; **whether westmetall.com's missing Thursday LME
copper row was a one-off lag or a new recurring problem**; and **whether
DeFi Rate's blended aggregator has refreshed** past its stale late-September
snapshot. **Still open and unchanged:** Brent crude's Friday 23 October
close three-way split (not re-attempted since edition 53); the ECB's exact
next-meeting date (unconfirmed, estimated mid-December); New Mexico v.
Meta's formal notice of appeal (unconfirmed for a thirteenth straight
edition); the "preview-consensus-only miss/beat framing" caution (dormant
since edition 41); the DOL weekly jobless-claims parsing problem; Banxico's
own primary site (unreachable again, try a fresh URL path); a fresh
federalregister.gov search-interface attempt (govinfo.gov remains the
working fallback). The 178-product Section 301 exclusion lapse (11:59pm ET
Mon 9 Nov, standard rate resuming Tue 10 Nov) now falls inside edition 60's
plausible window for the lapse itself and edition 61's for the
rate-resumption effect — check for any last-minute extension filing
directly across both. Riksbank's 4 November vote split (minutes due 10 Nov)
remains open, likely landing inside edition 60's window. **Dates to hold on
to.** October US jobs report and the next CFTC report both due Fri 6 Nov
2026 (edition 59). Riksbank minutes due 10 Nov 2026 (likely edition 60).
Section 301 exclusion lapse 9 Nov 2026, standard rate resumes 10 Nov 2026
(likely editions 60-61). Veterans Day (equities-open, bonds-closed,
confirmed) Wed 11 Nov 2026. 13F filings due approx. 14 November 2026 (a
Saturday) — the natural lead item for whichever edition covers the
following Monday, 16 November 2026, now about eight days out. BoE and
Banxico next decisions both 17 Dec 2026; the next monthly settled-facts
audit falls on the first edition of December 2026.
