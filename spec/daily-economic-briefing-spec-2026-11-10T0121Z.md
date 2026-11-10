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
  applied correctly for thirty-eight straight editions (33 through 60) —
  treat as settled; edition 60 read "Tuesday 10 November 2026" as the date
  line, covering the Monday 9 November session in the window line.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 60 all reused the
  same pattern — now confirmed clean across thirty-two consecutive editions;
  edition 60 phrased it "Window: Sun 8 Nov 2026 20:00 ET – Mon 9 Nov 2026
  20:21 ET (Mon 9 Nov close/AH, the window's one NYSE session)." No further
  confirmation needed; treat this as settled.

## Schedule
Run every weekday. Pick the trigger's local time so the effective research
cutoff lands roughly 4 hours after the US market close (20:15 ET) — during
US daylight time that's 00:00 UTC; adjust for standard time. **US daylight
time ended Sunday 1 November 2026, as scheduled — now a resolved, settled
transition, not a forward-looking watch item.** Edition 54's own window closed
at 2026-11-01 20:21 ET, which converts to 2026-11-02 01:21 UTC — consistent
with EST (UTC-5) already being in effect; editions 55 through 60's window
closes have all confirmed the same conversion again, now seven straight (most
recently edition 60: 2026-11-09 20:21 ET → 2026-11-10 01:21 UTC). **From
edition 54 onward, use EST (UTC-5) for all ET/UTC conversions** until DST
resumes — conventionally the second Sunday in March (expected March 2027; this
specific future date is a general calendar convention, not yet independently
verified, so don't cite it as a confirmed fact until closer to the event). On
Mondays (or after any gap), cover the full window back to the previous
edition's cutoff, including the weekend. **Thanksgiving (Thursday 26 November
2026) and the following half-day session (Friday 27 November) are now close
enough (about two and a half weeks out from edition 60) to flag as a forward
calendar item** — unlike Veterans Day's "equities-open/bonds-closed" pattern,
Thanksgiving is a full closure for both equities and bonds, and the Friday
after is a half-day for equities with an early bond close. Not independently
verified yet; re-confirm directly against nyse.com's holiday calendar and
sifma.org's bond-market calendar whichever edition's window first reaches it
(roughly edition 73-74 if no gaps, not a precise estimate this far out).

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
  edition 53 and were not re-attempted at editions 54-60 — stale news now,
  not worth a dedicated search. Blackout (Oct 17-29, 2026) held clean through
  the decision, as expected. **Next meeting: 8-9 December 2026, an SEP
  meeting.**
- **Rate-path odds — extended further at edition 60 rather than reversing,
  the third consecutive directional read the same way.** A fresh Polymarket
  Gamma-API pull (snapshot approx. 8:26pm ET 9 Nov 2026) put a
  December-hike-specific market at approx. **77%**, a broader "any hike by
  Dec 2026" market at approx. **82.5%**, and a separate cut-odds market at
  just approx. **1%** — extending edition 59's approx. 76.5-77% read rather
  than unwinding it. DeFi Rate's blended Kalshi/Polymarket aggregator agreed
  closely at the same snapshot: approx. 80% hike / 19% hold / 2% cut.
  **Kalshi's own direct fetch failed again at edition 60 — a NEW failure
  signature, HTTP 401 instead of the long-running 429 — now TWENTY-FOUR
  consecutive failures (37-60).** CME FedWatch also failed again directly
  (timeout), a **TWENTIETH** consecutive failure (41-60). The composite "at
  least one more hike in 2026" read has still not been freshly re-pulled
  since edition 38 (last known approx. 80%) — don't cite without a fresh
  pull. Edition 59's own full round-trip (sharp reversal then snap-back)
  appears to have settled into a genuine hawkish drift rather than continued
  whipsawing — worth a fresh check at edition 61 to see if 77-82% holds,
  extends toward the upper end of that range, or eases.
- **US-China "30-for-30" tariff framework — remains a closed thread, do not
  re-open absent a genuine dated Federal Register filing.** Resolved at
  edition 37 (framework) and edition 47 (implementation-notice sub-question:
  no effective date, no set timeline, none imminent). No new development was
  found at editions 54-60 either (light-touch checks only); the
  federalregister.gov search-interface block (302-redirect to
  `unblock.federalregister.gov`, logged at edition 48) was re-tested directly
  again at edition 60 and remains blocked — govinfo.gov continues to be the
  working mirror, and **edition 60 tried a new approach, the Federal
  Register's own developer API (`federalregister.gov/api/v1/documents.json`),
  which returned results (unlike the blocked search UI) but nothing relevant
  to the specific sub-question below** — worth trying again, it is a
  genuinely different access path from the blocked search page. Separately:
  secondary reporting (a Thomson Reuters regulatory-insight piece) describes a
  Busan truce extension to **10 January 2027**, but this remains **NOT
  confirmed via any published Federal Register notice** as of edition 60 —
  treat the January 2027 date as reported-not-verified, not settled law, if
  cited. **The separate reciprocal-tariff suspension / Section 301 exclusion
  question for 178 Chinese products remains unresolved through edition 60's
  own window close too — still genuinely live, not yet resolved either way.**
  The underlying Federal Register notice (Doc 2025-21671, govinfo.gov mirror)
  remains internally inconsistent about its own lapse date: its DATES section
  states the 178 exclusions lapse at **11:59pm ET on Monday 9 November
  2026**, while its own background narrative, and a separate USTR press
  release, both instead say the exclusions are "extended until **November
  10, 2026**." No new USTR extension filing had been found as of edition 60's
  window close (Mon 9 Nov 20:21 ET) — notably, this is now right at or just
  before the *earlier* of the two candidate lapse moments itself, so the
  question of which date (if either) the notice ultimately treats as
  operative is still **not yet resolvable even in principle** from this
  edition's own window; **it now falls inside edition 61's window (covering
  Tuesday 10 Nov)**, not edition 60's. Check federalregister.gov/govinfo.gov,
  the FR developer API, and ustr.gov directly for any last-minute extension
  filing, and note which of the two dates the notice ultimately treats as
  operative. **A possibly-related adjacent item surfaced at edition 60, not
  yet independently verified: a secondary source (Trading Economics) describes
  a separate IEEPA/reciprocal "fentanyl tariff" rate cut on China (reportedly
  20%→10%) also keyed to the same midnight ET Nov 9/10 boundary.** This is a
  different legal mechanism from the Section 301 178-product exclusions —
  don't conflate the two — and has not been checked against any primary US
  government source. Worth a dedicated check at edition 61 alongside the
  Section 301 question.
- **Fed Chair: Kevin Warsh — SETTLED, stop re-verifying it every run.** No
  contradiction surfaced through edition 60; **directly re-confirmed via
  federalreserve.gov's own bios page at edition 54's November monthly
  audit**, closing that housekeeping item cleanly; not re-attempted at
  editions 55 through 60 (settled, no fetch needed). His Chairman term ends 21
  May 2030 (took office 22 May 2026, a four-year term); his separate term as a
  Board of Governors member runs to 31 January 2040. The Chairmanship
  re-opens as a live fact only on a successor nominated/confirmed, a
  resignation or removal, or that 21 May 2030 term-end date actually arriving,
  or the **next monthly audit (first edition of December 2026)**.
- **The 3 November 2026 US midterm elections — still LIVE, certification
  status not confirmed at edition 60 either, watch again.** Democrats
  won control of both the House and Senate — called by AP/CNBC/NBC/PBS by
  Wednesday 4 November morning — ending unified Republican control of
  Washington. Democrats flipped at least seven Senate seats (Iowa, Kansas,
  Ohio, North Carolina, New Hampshire, South Carolina, Texas); a handful of
  races were still uncalled as of edition 57's cutoff and this was not
  independently re-checked at editions 58 through 60 — do not cite a final
  seat count without re-checking. **A dedicated search at edition 60 again
  found no official national certification news either way, only
  state-level future certification deadlines** (California statewide results
  due by 11 Dec 2026; Sacramento County certification "not sooner than" 1 Dec
  2026; Multnomah County, OR, final results "no later than" 30 Nov 2026;
  Massachusetts governor cannot certify before 5pm 18 Nov) — consistent with
  certification being a genuinely weeks-long process distinct from the
  networks' early-November race calls, not a contradiction of the "Democrats
  won both chambers" fact. **The election's second-order market effect (the
  AI-capex/data-center selloff of edition 58 and its partial edition-59
  relief rally) continued resolving at edition 60**: the chip complex (ex-
  Nvidia) fully round-tripped back above its pre-selloff levels Monday — see
  the dedicated Nvidia/semiconductor bullet below. Re-verify certification
  status again in the next several editions' macro passes.
- **NEW at edition 60, LIVE thread — Nvidia / Jensen Huang / Alice Huang /
  Megaspeed China-intelligence story, and a sharp lesson in not over-reading
  it.** The real, multiply-corroborated story: the New York Times reported
  29 October 2026, citing unnamed US intelligence sources, that Alice Huang
  (Huang Le), an executive at Megaspeed (a Singapore-based Nvidia customer
  previously investigated by Commerce/DOJ over possible export-control
  circumvention), was assessed to have been cultivated by China's Ministry
  of State Security, and had maintained a close relationship with Nvidia CEO
  Jensen Huang — a relationship a Financial Times-sourced account separately
  characterized as romantic. Nvidia said the contacts were routine and
  business-related and that the Megaspeed export-diversion allegation was
  investigated and found unsubstantiated previously; China called the claims
  "groundless speculation." Senator Elizabeth Warren and a House China-policy
  committee have pressed for answers/a hearing — this is real congressional
  interest, confirmed via multiple outlets (TipRanks/TheFly, ForkLog, and
  independent WebSearch corroboration). **What is NOT corroborated and must
  not be reported as fact: a widely-circulated claim that Nvidia's board
  formally announced an independent investigation into Huang on 8 November
  2026, including a staff apology email to employees, and a board statement
  of continued confidence in him.** Two independent edition-60 research
  passes returned conflicting reads on this specific claim — one found no
  wire-service coverage, no SEC 8-K, and flagged its own WebFetch tool as
  having likely hallucinated a fabricated "NVIDIA newsroom" page matching the
  leading query; the other, researching market-wrap pieces for Monday's
  session, reported the board-investigation framing as if confirmed, citing
  Axios/SCMP/The Hill/Tom's Guide. A dedicated follow-up WebSearch (run
  directly, not delegated) found the real 29 Oct NYT/FT story and its
  aftermath (Nvidia's denial, China's denial, Warren's letter, a House
  hearing request) but **no genuine, dated, reputable-outlet confirmation of
  a board-announced investigation or an apology email** — this is the
  correct, more skeptical read, and is what the edition 60 briefing
  published. **Lesson: a bizarre, dramatic claim that sits one inferential
  step beyond an already-real story is exactly the kind of thing that gets
  fabricated/embellished by a research pass under a leading prompt — verify
  the SPECIFIC claim being made, not just whether the general topic is real,
  and be willing to run your own direct check rather than trusting a
  subagent's confident-sounding citation list when two passes disagree.**
  NVDA itself genuinely fell -4.27% Monday (confirmed via stockanalysis.com,
  cross-checked twice) even as the rest of the chip complex (AMD, Intel,
  Marvell, Broadcom, Micron) rallied hard — the published briefing attributed
  this to the real, older (29 Oct) story as an ongoing overhang, not to the
  unconfirmed 8 Nov board-investigation claim. **Watch for genuine
  developments** (an actual SEC filing, a dated wire-service report of board
  action, or a scheduled congressional hearing) in future editions' equities
  passes — do not assume the fabricated version was secretly right just
  because it keeps circulating.
- General principle for everything still live: do not assume a routine
  macro-calendar fact (meeting dates, symposium schedules, other central
  banks' policy rates, government funding status) from memory or from the
  prompt's own framing — verify it fresh from a primary source
  (federalreserve.gov, bankofengland.co.uk, boj.or.jp, kansascityfed.org,
  norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, rba.gov.au,
  ecb.europa.eu, bankofcanada.ca, whitehouse.gov, etc.) every edition, exactly
  like any other data point, until an entry below is marked SETTLED. These
  are the rates and dates that feed Section 3's policy-rate table, so the
  table is the natural place to land them. Per-bank status as of edition 60:
  - **Reserve Bank of Australia:** current rate **4.85%**, hiked 25bp on
    Tuesday 3 November 2026 (6-3 split vote, its fifth hike of 2026) —
    SETTLED pending the RBA's own next decision, **7-8 December 2026**
    (confirmed directly at edition 57 against rba.gov.au's own meeting-dates
    release). Re-confirmed with no contradiction as part of edition 60's
    general bank sweep; no dedicated fetch needed going forward until that
    meeting.
  - **Bank of England:** rate **4.00%**, hiked 25bp on Thursday 5 November
    2026 (8-1 vote, Mann dissenting for +50bp) — SETTLED pending the next
    decision, **17 December 2026**. Re-confirmed with no contradiction as
    part of edition 60's general sweep.
  - **European Central Bank:** rate complex (deposit facility 2.50%, main
    refi 2.65%, marginal lending 2.90%) **SETTLED**; next Governing Council
    meeting **16-17 December 2026**, confirmed directly at edition 59 — also
    now SETTLED. Re-confirmed with no contradiction at edition 60's general
    sweep; the press-conference-content/vote-split sub-question from the
    28-29 October meeting remains unobtainable and was not specifically
    re-attempted at edition 60 (out of scope, low priority).
  - **Bank of Japan:** current rate approx. 1.25%, SETTLED pending its own
    next meeting, **17-18 December 2026**. Re-confirmed with no contradiction
    at edition 60's general sweep.
  - **Bank of Canada:** SETTLED. Current rate 2.50%, hiked 25bp 28 October
    2026. Next decision **9 December 2026** (same date as the Fed's).
    Re-confirmed with no contradiction at edition 60's general sweep.
  - **Swiss National Bank:** current rate 0.00%, SETTLED. Next assessment
    **10 December 2026**. Re-confirmed with no contradiction at edition 60's
    general sweep.
  - **Norges Bank — new data point at edition 60, reinforces rather than
    changes the settled fact.** Current rate **4.50%** (hiked 25bp 24 Sept
    2026), SETTLED. **A forecast-free interim policy review on 5 November
    2026 kept the rate unchanged at 4.50%** — confirmed directly against
    norges-bank.no's own press release ("Policy rate kept unchanged at 4.5
    percent"), a previously untracked decision point for this report. This
    is Norges Bank's normal pattern of interim reviews between full
    Monetary Policy Report meetings, not a new surprise. Next full decision
    remains **17 December 2026**, unchanged and still SETTLED.
  - **Riksbank:** current rate **2.00%**, hiked 25bp on Wednesday 4 November
    2026 (its first hike since 2023) — SETTLED pending the next decision,
    **approx. 16 December 2026** (inferred from the Riksbank's own Monetary
    Policy Report date, not an explicit "next decision" label). **The vote
    split/dissent from the 4 Nov decision remained unresolved at edition
    60, now directly confirmed via riksbank.se why**: the bank's own
    calendar lists the minutes' publication for **10 November 2026, 09:30
    CET** (after edition 60's own window closes), and a direct check of the
    minutes archive showed entries only through the 19 August 2026 meeting —
    no 4 Nov entry yet, consistent with the due date. Expect this inside
    **edition 61's** window (covering Tuesday 10 Nov).
  - **Banxico — rate itself settled by the edition-58 surprise cut;
    sourcing tier unchanged at edition 60, failure signature refined again.**
    Per consistent multi-outlet Mexican financial press, Banxico **cut its
    overnight interbank rate 25bp, from 6.50% to 6.25%**, decision dated 5
    November, effective 6 November 2026, a **3-2 vote** (Deputy Governors
    Galia Borja Gómez and Jonathan Heath dissenting in favor of holding).
    Minutes due 19 November 2026; next decision **17 December 2026**
    (secondary-sourced). **banxico.org.mx failed again at edition 60, via a
    further-refined failure signature**: every path tried 302-redirects to
    the "anterior.banxico.org.mx" subdomain, which is now live (not dead as
    at edition 59) but returns HTTP 404 on the specific sub-paths tried,
    while the subdomain's own root returns HTTP 403 — a structural,
    multi-stage block, not a transient outage. Remains secondary-sourced
    only. Try yet another fresh URL path at edition 61.
  - **Government funding/shutdown status:** H.R. 6500 funds federal agencies
    through 11 December 2026, no shutdown in effect — **re-confirmed
    cleanly and directly against whitehouse.gov at edition 60**
    (briefings-statements page for H.R. 6500), an upgrade back to primary
    sourcing after edition 59's one-edition dip to secondary-only. Continue
    the standard re-check-every-edition discipline regardless.
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
  of edition 59's sharp rate-odds reversal, and the hawkish repricing it
  started continued extending at edition 60 (see the dedicated Standing
  Facts bullet above).
- **September 2026 ISM Services/Non-Manufacturing PMI — closed thread as of
  edition 35, do not re-derive:** headline 54.9% (down from August's 55.4%),
  Prices Paid 74.0% (+1.4pt, highest since July 2022). **October's ISM
  Services PMI — RESOLVED at edition 57:** headline **54.5%**, below the
  **54.8%** consensus/forecast and a third straight month without
  acceleration, confirmed via Investing.com's Economic Calendar. Sub-index
  detail (Prices Paid, New Orders, Employment) remains an Annex B item, not
  re-attempted at editions 58 through 60.
- **September 2026 US CPI — closed thread as of edition 42, do not re-derive:**
  headline **+0.6% m/m / +3.7% y/y**, core **+0.3% m/m / +2.6% y/y**, both
  above the Dow Jones consensus of approx. 3.6%/2.5%, confirmed directly
  against bls.gov's CPI Summary release. This was the proximate trigger for
  edition 42's broad equity selloff, VIX spike and sharp October-hike-odds
  repricing. **October 2026's CPI is due Tuesday 10 November 2026**, inside
  edition 61's window — a live, not-yet-released figure, not a closed thread.
- **September 2026 US PPI — closed thread as of edition 43, do not
  re-derive:** final demand **+1.3% m/m / +6.3% y/y** (NSA), the largest
  monthly gain since March 2022 and largest 12-month rise since December
  2022; the trade-services-excluded measure was +0.5% m/m / +5.0% y/y.
  Energy (+10.8% m/m, gasoline +20.3%) drove over 80% of the goods-side
  increase. Confirmed directly against bls.gov. **October 2026's PPI is due
  Friday 13 November 2026**, a live, not-yet-released figure.
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
  watch for a level reset around that date (roughly two and a half weeks
  from edition 60, likely inside edition 70-71's window if no gaps, not a
  precise estimate this far out), not a genuine month-over-month signal.
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
  directly against whitehouse.gov at edition 60** (after a one-edition dip
  to secondary-only sourcing at edition 59). H.R. 6500 funds federal
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
  notice of appeal is still unconfirmed for a FIFTEENTH straight edition
  (47-60).** Meta owes **$25bn** in civil penalties for the jury's
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
  re-attempted at editions 55 through 60 (out of scope); no new development
  in the 48-state settlement or the Unfair Practices Act stay.
- **New calendar-awareness item, reconfirmed relevant across several
  editions: "equities-open, bonds-closed" US holidays need an explicit check
  every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. Veterans Day, Wednesday 11 November 2026, was independently
  verified at edition 57 and follows the same pattern — resolved/closed for
  Veterans Day 2026 specifically, not re-attempted at edition 60 (no new
  holiday fell inside that window). **A different-pattern holiday,
  Thanksgiving (26 Nov) plus the Friday half-day (27 Nov), is now close
  enough to flag — see the Schedule section above.** The DST transition
  (ended Sunday 1 November 2026) remains itself resolved/settled.
- **The vendor-retroactive-revision trap reversed direction sharply at
  edition 60 — a clean two-source reconciliation on almost every tracked
  series, the opposite of edition 59's 4-of-7 revision problem.** Fresh
  re-pulls of Friday 6 Nov's base for WTI, Brent, Henry Hub, gold futures,
  silver futures (Investing.com side only), COMEX copper, LME copper cash,
  DXY (Yahoo), EUR/USD, GBP/USD, USD/JPY and all three Treasury tenors all
  matched the previously-logged Friday figures exactly. **Two narrower
  exceptions did surface:** Investing.com's own DXY-proxy Friday figure
  revised from the previously-logged 102.179 to 102.30 — a genuine
  cross-edition revision, now converging exactly onto Yahoo's figure;
  separately, silver futures showed a **cross-vendor (not cross-edition)**
  Friday-base disagreement (Investing.com $51.942, unrevised from last
  edition; Yahoo Finance $51.803) even though neither vendor's own figure had
  moved from what it previously showed. **A separate, new, and more
  systemic data-quality issue surfaced at edition 60: Investing.com's own
  displayed "Change %" column diverged from a direct settle-to-settle
  calculation off its own two closing prices, by roughly 20-80 basis points,
  across nearly every tracked commodity and FX instrument** (WTI, Brent,
  Henry Hub, gold, silver, COMEX copper, the DXY proxy, and all three FX
  crosses) — not a vendor-vs-vendor or edition-vs-edition conflict, but the
  vendor's own displayed percentage disagreeing with its own two prices.
  **Always compute the percentage change directly from the vendor's own two
  closing prices rather than trusting its displayed change field, and
  disclose when the two diverge** — this looks like it may be a standing
  Investing.com quirk (possibly an intraday-reference-price artifact) rather
  than a one-off, so keep checking it every edition going forward.
- **Henry Hub: now a FIFTH consecutive clean two-source reconciliation at
  edition 60.** Investing.com's Monday close ($3.201/MMBtu) and Yahoo
  Finance's NG=F close ($3.213) matched closely (both up sharply, approx.
  +6.4% to +6.8% m/m on the session). Still NGZ6 (December); no roll to NGF7
  (January) yet as of Monday 9 Nov. Continue occasional spot-checks rather
  than a dedicated every-edition reconciliation effort unless a fresh
  conflict appears.
- **westmetall.com (LME copper) — the cash series stayed clean at edition
  60, but the 3-month series hit a new, narrower access problem.** Monday's
  cash settlement ($14,030.00/t) was confirmed directly, continuing the
  Friday base's clean match. **The 3-month series' Friday base could NOT be
  independently re-confirmed this session** — westmetall.com's table view
  returned only the single most-recent date regardless of the date-range
  query parameters tried, so Monday's 3-month level ($13,855.00/t) is
  reported on its own, without a day-over-day change computed against the
  uncorroborated carried-forward Friday figure. This is a different, milder
  problem than edition 58's missing-row issue (resolved cleanly at edition
  59) — a query/filtering limitation rather than a missing data point. Try a
  different query approach (e.g. no date parameters at all, or an explicit
  single-date lookup) at edition 61.
- **New sourcing-mechanics trap logged at edition 50, relevant to any
  Monday-dated (or any day-after-a-non-trading-day) edition: Investing.com
  inserts an electronic Sunday-evening re-open print as its own row for every
  24-hour-traded instrument.** Edition 60's window did reach back across the
  weekend close-to-reopen gap for 24-hour instruments — the discipline was
  applied (fetching Friday and Monday rows explicitly by date rather than by
  position) and no stray Sunday-print contamination was found. Continue
  applying this discipline on every post-weekend or post-gap edition.
- **The Kitco live-spot-vs-headline cross-check stayed in its fourth failure
  mode (total inaccessibility) for a second consecutive edition at edition
  60 — the same problem as edition 59, not a new one.** Both canonical
  historical-close URLs still 302-redirect to live-quote-only pages with no
  retained close row for any past date; `kitco.com/price/precious-metals`
  again showed only a real-time bid/ask and rolling-period performance
  widgets, no dated close. No Kitco spot figure is reported for Monday 9 Nov
  as a result — see Annex B. **Housekeeping note: edition 60's own published
  briefing described this in Annex B as "a fifth distinct problem mode in
  five editions," which overstates it slightly — it is the same (fourth)
  mode recurring for a second edition, not a new fifth mode. Not significant
  enough to warrant a reader-facing correction (no number was wrong, only an
  internal failure-mode tally), but worth getting right in this spec going
  forward.** Keep attempting it fresh every edition regardless.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company, IPO'd 1 July 2026 at
  $29/share. Logged here so a future edition doesn't waste effort
  re-verifying the ticker's legitimacy if it moves sharply again.
- **The "named secondary outlet's own claim can be flatly wrong" trap gained
  a dramatic new instance at edition 60 — see the dedicated Nvidia/Huang
  Standing Facts bullet above for the full account.** A circulating claim
  that Nvidia's board formally announced an independent investigation into
  CEO Jensen Huang on 8 November 2026, including a staff apology email, could
  not be corroborated by any dated wire-service report or SEC filing despite
  initially being reported as apparently-confirmed by one of two independent
  research passes (citing Axios/SCMP/The Hill/Tom's Guide) — a direct
  follow-up search found the real underlying 29 October NYT/FT story but no
  support for the specific board-investigation/apology-email claim, which was
  excluded from the published briefing. **This is the most severe instance
  of this trap logged to date**, precisely because it was initially
  corroborated-*looking* (named outlets cited, a plausible-sounding
  escalation of a real story) rather than obviously fabricated. **THREE
  instances were caught at edition 58** (a fabricated DraftKings AH figure
  with no corresponding 8-K, an unsupported Natera "new CEO" driver claim, a
  circulating "biggest calls" analyst-action list found unsupported on
  spot-check), and **one at edition 59** (a wholesale stale-date republish of
  Thursday's index closes under Friday's date, caught via digit-for-digit
  comparison against the price-history record). Prior instances remain
  logged: JetBlue (edition 50, magnitude), Carvana/Barron's (edition 52,
  direction/framing), Tesla and NU Holdings (edition 49, magnitude), Marvell/
  Lumentum and Barclays/PayPal (edition 53), a misdated Reuters-style squib
  plus a wrong-year Trefis list (edition 54), Brent crude's disclosed
  settle-to-settle-vs-"more than 7%" methodology discrepancy (edition 55),
  and a claimed Oracle analyst-upgrade note (edition 56). **Lesson
  reinforced at edition 60: the more dramatic and "almost certainly true
  because why would anyone make this up" a claim feels, the more it deserves
  a dedicated, skeptical, DIRECT verification pass** — not a delegated one
  that might itself be fooled by the same leading framing.
- **The edition-49 "forward-looking calendar aggregator" trap (names falsely
  listed as past or future reporters when the actual date differs) remains
  closed as a general pattern, and gained a related-but-distinct variant at
  edition 60: this report's OWN forward-looking calendar assumptions also
  need periodic re-verification against primary sources, not only external
  aggregators' claims.** Edition 60 found two of its own carried-forward
  assumptions were wrong: the next CFTC Commitments of Traders report,
  assumed due "Friday 13 November 2026," is actually due **Monday 16
  November 2026** per CFTC's own official release-schedule page (which lists
  November dates as the 6th, 16th, 20th and 30th, not a plain weekly Friday
  cadence); and the Q3 2026 13F filing deadline, assumed "approx. 14
  November 2026" (a Saturday), actually rolls to **Monday 16 November 2026**
  per the standard 45-day-after-quarter-end rule. Both are corrected
  throughout this spec and in edition 60's own Section 6. The earlier
  aggregator-date-error instances (Amdocs, Kyndryl at edition 57) remain
  logged; **resume the discipline of checking any calendar assumption —
  whether sourced from an aggregator or carried forward in this spec itself —
  against its primary source before it becomes load-bearing.**
- **A megacap multi-name earnings cluster producing genuinely uncorrelated
  reactions is a standing, repeated pattern — now at least THIRTEEN distinct
  instances through edition 60 (editions 44, 47, 48, 49 x2, 50, 52, 53 x3,
  58, 59, 60).** Edition 60 added a same-session pair: Constellation Energy
  rose 10.46% on a clean Q3 beat-and-raise, while monday.com fell 9.10%
  despite its own Q3 beat, dragged down by a Q4 guide implying growth
  decelerating to approx. 14% y/y from Q3's 19% — a split within the SAME
  earnings morning, not even requiring the AH-vs-regular-session distinction
  that most prior instances turned on. Continue treating beat-and-raise (or
  a guidance cut) as having no *guaranteed* effect on the reaction without
  checking the actual outcome.
- **New production lesson from edition 53: CSS multi-column (`.cols3`/
  `.cols2`) pagination under Chromium print-to-PDF can plateau stubbornly on
  marginal content trims — edition 60 hit the most severe version of this
  plateau yet, and found a clearer fix. See the dedicated Production Notes
  entry below for the full mechanics.**
- **MAJOR UPDATE at edition 59 (bug recurrence) now followed by a clean
  edition 60: both of the VIX feed's known bugs (duplicated
  `prev_day_close`, and a `price_change_percent` that divides by the wrong
  price) were ABSENT on all six series again at edition 60**, breaking
  edition 59's single-edition recurrence. The pattern to date: clean for
  four straight editions (55-58), recurred for one edition (59), clean again
  at edition 60 — i.e., the bug can toggle on and off unpredictably
  edition-to-edition, not just after a long clean streak. **Continue the
  manual-calculation discipline unconditionally regardless of how many
  bug-free editions precede the current one.**
- **New at edition 54: a markup-correctness self-check caught three
  instances of the `</td><sup` table trap (documented under Production
  notes below) before rendering.** Editions 55 through 60 all ran the same
  proactive `grep -n '</td><sup'` check and found **ZERO instances for a
  sixth consecutive edition** — worth continuing on every edition with a
  table that has an empty trailing cell or a cell containing only a
  citation.
- **New at edition 54: the CFTC Asset-Manager-vs-Leveraged-Funds grouped-bar
  chart was reused for a fifth time (editions 34, 39, 44, 49, 54 — a clean
  Monday/weekend-window pattern) with the same figsize (9.8, 2.15), `h=0.32`
  bar offset and figure-level legend technique documented under Production
  Notes.** **Editions 55 through 60 did not use the chart** — no fresh CFTC
  data fell inside any of those windows (the Friday 6 Nov report, covering
  Tuesday 3 Nov data, was edition 59's; the next report is now confirmed due
  **Monday 16 November 2026**, covering Tuesday 10 Nov data — see the
  corrected CFTC entries under Known-hard-to-source below). **This falls
  inside edition 65's plausible window** (one edition per weekday, no gaps
  assumed: 61 Tue 10, 62 Wed 11, 63 Thu 12, 64 Fri 13, 65 Mon 16) — check
  cftc.gov directly then, and watch whether the irregular November spacing
  (6th, 16th, 20th, 30th — not a plain weekly cadence) is evidence that
  CFTC's previously-announced move to twice-weekly releases has actually
  begun, or is just holiday-adjusted spacing around Veterans Day; this is
  itself worth a one-line check at edition 65.

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
  **Editions 54 through 59 all converged cleanly within one or two
  renders** (54 and 59 after deleting the one forced break; 55 through 58
  all on the very first render with the break retained, sections 1-6
  ending within page 3 every time). **Edition 60 broke that quick-convergence
  streak, for a NEW reason distinct from genuine content density:** deleting
  the forced break (the usual, usually-sufficient fix for a page-4
  spillover) was necessary but not sufficient — sections 1-6 plus Annexes A
  and B landed fine on page 4, but Annex C's own three-column source block
  then repeatedly filled to within single-digit pixels of the page-4 bottom
  margin regardless of many small trims to the PRECEDING prose (Annex A/B),
  pushing only the trailing Method note onto an otherwise-blank page 5.
  Roughly eight render iterations were needed before the right lever
  (trimming Annex C's OWN entries, not the prose before it) converged it
  cleanly. **See the dedicated Production Notes entry below — this is a
  new, specific lesson, not a repeat of edition 53's genuine-density
  marathon.** Always check which situation you're in (stray break vs.
  genuine overflow vs. spillover that just needs the break deleted vs. a
  lonely trailing block pinned by a full-feeling preceding column box vs. a
  dense day that simply fits) before assuming any one fix is the answer.
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
  all values genuinely share one. **Also watch for a stray bracket typed
  outside a `<sup>` tag entirely** — `check_refs.py` will not flag it since
  its regex only matches inside `sup class="ref"` tags, so a bare `[n]` slips
  through silently. Proofread citation-heavy sentences visually, not just
  via the script, when a sentence carries two or more consecutive citations.
  A related trap, worth naming explicitly: placeholder ref text (e.g.
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
  **Edition 60 went further: it merged SEVEN separate central-bank-website
  citations (each bank's own site) into a single shared Annex C number**,
  since all nine non-Fed bank table cells were fresh-checked by the same
  "visit each bank's own site directly" method — this was done specifically
  as part of the Annex-C-trimming fix described under Production Notes, and
  is a legitimate, recommended pattern when several distinct URLs really do
  share one verification method, not just when they share an outlet.
  **Citing the prior edition itself as a source** (e.g. "logged prior-session
  baseline figures," or re-citing a prior edition's own already-primary-
  confirmed fact) is a legitimate, already-used pattern.
- **Structure:** correction box (only when there is one) → 60-second read
  (5 ranked items) → 1 Market recap, **including sector performance** → 2
  Equities and earnings (LEAD, **single stocks only**) → 3 Macro, policy and
  rates (condensed; policy-rate table + prose, see below) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A
  (assumptions, status, and the full record of any correction) → Annex B
  (what could not be verified) → Annex C (sources) → Method note. **Do not duplicate the
  day-ahead calendar as both a prose paragraph (e.g. at the end of Section 3)
  and the Section 6 table — Section 6's table is the one and only place the
  day-ahead calendar belongs.**
- **The disclosure box is now a correction box — new at edition 49, by
  request.** Assumptions and status live in **Annex A**. What stays on page
  1 is **corrections only**: a figure published in an earlier edition that
  turned out to be wrong, or a premise-level correction. Terse — what was
  published, what it should have been — with the full record in Annex A if
  it needs more than a line. **Omit the box entirely on an edition that
  corrects nothing**, which will be most of them. **Editions 54 through 60
  have all omitted the box** — in each case nothing published in a prior
  edition was found to be wrong. (Note: edition 60 corrected two of its OWN
  carried-forward *forward-looking calendar assumptions* in the spec — the
  CFTC report date and the 13F deadline — but since neither had been
  asserted to readers in a prior PUBLISHED edition as settled fact, this did
  not call for a correction box; it is handled as a quiet Section 6/Annex A
  update instead. A genuine published-figure correction would still get the
  box.)
- **All sector and ETF material belongs to Section 1 — by request since
  edition 49.** Section 1 keeps its snap-grid tiles and recap paragraph and
  gains the sector-ETF chart plus the narration of how each sector did in
  the session. **Section 2 is purely single-stock**: movers chart, movers
  table, earnings, guidance, analyst actions. The test is simple — if a
  sentence is about a sector rather than about a named company, it goes in
  Section 1. **Edition 60 applied this cleanly**: the chip complex's round-
  trip-except-Nvidia story (named companies — AMD, Intel, Marvell, Broadcom,
  Micron, Nvidia) stayed in Section 2 even though part of the driver (the
  broad risk-on rally) was macro/thematic, consistent with the rule's own
  test ("about a named company" governs, not whether the driver happens to
  be macro).
- **Section 3 carries a central-bank policy-rate table.** Columns: **Central
  bank | Policy rate | Last change | Next decision**. The Fed goes first as
  the anchor to compare against, then whichever of the BoE, BoJ, ECB, SNB,
  Norges Bank, Riksbank, RBA, BoC and Banxico the window actually touches —
  eight to ten rows is the working range. A bank whose current rate could
  not be verified still gets its row, with that cell marked unavailable and
  a matching Annex B entry. **Editions 54 through 60 have all run the same
  full 10-row table** (Fed, BoJ, BoE, ECB, BoC, RBA, SNB, Norges Bank,
  Riksbank, Banxico). Only Banxico's rate and next-decision date remain
  imperfectly (secondary-only) sourced as of edition 60 — unchanged from
  edition 58, still the smallest "unavailable/imperfect" footprint this
  table has carried since it was introduced. Follow the usual table
  convention — plain `<tr>` header rows, no `<thead>`.
- **Charts: two fixed, a third only when earned — changed at edition 49.**
  The **sector-ETF performance chart always goes in Section 1**, beside the
  sector narration it illustrates, and the **single-stock movers bar always
  goes in Section 2**, with the names. Neither may duplicate a table.
  A **third chart is allowed only when positioning or volatility is
  genuinely the day's dominant story** — not merely present, and never to
  fill a short page — and it goes in the section it belongs to: CFTC
  asset-manager vs. leveraged-funds positioning or a VIX term structure in
  Section 5, an implied-vs-realized earnings bar in Section 2. **Editions 55
  through 60 did not use a third chart.** Fresh CFTC data last landed inside
  edition 59's window; none fell inside edition 60's. The VIX complex's
  Monday move (a full un-inversion back into clean ascending contango) was
  genuinely newsworthy but judged secondary to the equity/oil/macro story
  and covered fully in prose. **Next CFTC report due Monday 16 November
  2026** (corrected from the previously-assumed Friday 13 Nov — see the
  Known-hard-to-source entry below), covering Tuesday 10 November data —
  check cftc.gov directly whichever edition's window includes it, likely
  edition 65.
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
  itself directly sourced** — treat any sentence that computes or combines
  two sourced figures into a new number as needing its own source or a cut,
  not an estimate. No violation of this rule was found needing a fix at
  editions 56 through 60.
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
  radio-station website). **Editions 55 through 60 have all successfully used
  the dual La Nación/WTOP mirror approach — now SEVEN consecutive
  successes** (edition 60 used the WTOP mirror alone, successfully, at a
  directly-guessed date-specific URL). This is the established first-choice
  workaround; try it before the Yahoo-Finance-plus-secondary-recap fallback,
  while still re-attempting apnews.com/Reuters directly every edition
  regardless.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Always check a dated article's own claimed magnitude AND
  direction against the underlying price-history table or primary filing,
  not just its date, before repeating it** — this trap has now hit
  magnitude, direction/framing, claimed drivers that don't hold up, a
  claimed analyst action that appears outright fabricated, the claimed
  DATE/YEAR itself, a disclosed cross-source percentage-methodology
  discrepancy, a figure with no corroborating primary filing at all, and a
  wholesale stale-date republish (full history logged in the Standing Facts
  "named secondary outlet" entry above). **Edition 60 added its most severe
  instance yet: a dramatic, specific, seemingly-corroborated claim (Nvidia's
  board formally investigating CEO Jensen Huang) that one research pass
  reported as apparently true, citing named outlets, before a dedicated
  direct follow-up found no genuine support for that specific claim** — see
  the dedicated Standing Facts bullet. Treat ANY surprising secondary claim
  (price move, driver, analyst action, date, or computed percentage) as
  needing this same verification discipline, and be especially suspicious of
  a claim that is one dramatic inferential step beyond an already-real
  story.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  **Edition 60 exercised this discipline directly (via the coordinator's own
  WebSearch, not a delegated pass) on the Nvidia/Huang board-investigation
  claim, precisely because two research passes had returned conflicting
  reads on it** — this is the clearest demonstration yet of why the
  discipline should run a genuinely independent check, not just ask a third
  subagent to adjudicate (which could be fooled by the same leading framing).
  This discipline is specifically recommended for any edition carrying a
  surprising, highly consequential single finding, not only for cross-pass
  disagreements.
- **Premarket is not the close, and the close is not the after-hours
  earnings reaction — and an after-hours reaction does not necessarily hold
  into the next regular session, uniformly or at all. A strong beat-and-raise
  does not guarantee a positive reaction even within the SAME session —
  though it does not guarantee a negative one either.** Reinforced at
  essentially every edition since 44. **Edition 60 added a same-session
  (not AH-vs-regular) instance**: Constellation Energy and monday.com both
  reported before Monday's open with clean Q3 beats, yet CEG rose 10.46%
  while MNDY fell 9.10% on its own Q4 guide — see the megacap-cluster
  Standing Facts entry above. Always fetch the verified close, the
  after-hours reaction, AND (when the window allows) the next regular
  session's close as three separate, clearly labelled figures. A
  premarket-only or regular-session-only figure that predates a same-evening
  earnings release should be labelled as such rather than implied to be a
  reaction to it — edition 60 did this explicitly for The Trade Desk and
  Hims & Hers, both of which moved sharply in the regular session for
  reasons unrelated to that evening's (after-the-close) earnings report.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent —
  RESOLVED cleanly again at edition 60.** Yahoo Finance's DX-Y.NYB and an
  Investing.com futures-style DXY proxy agreed Monday was down (approx.
  -0.6%), with levels differing by only approx. 3bp (101.66 vs. 101.69).
  Keep disclosing the DXY-vs-FX-crosses comparison every edition regardless
  of which way it goes.
- **The Kitco live-spot-vs-headline cross-check stayed in its fourth
  failure mode (total inaccessibility) for a second consecutive edition at
  edition 60 — not a new mode, see the dedicated Standing Facts entry
  above.** No Kitco spot figure is reported for Monday as a result.
- **GBP/USD, EUR/USD and USD/JPY all reconciled cleanly again at edition 60**
  against their logged Friday base, with no revision on any of the three.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for twenty-five further editions (37-60)** — edition 60 again found the
  full Treasury curve reconciled cleanly against the official
  home.treasury.gov TextView page (2-year 4.56%, 10-year 4.88%, 30-year
  5.26%, up 2-5bp across the curve on the day), with the prior Friday base
  matching the previous edition exactly. Treat as resolved/noise unless a
  fresh conflict appears.
- **New sourcing-mechanics lesson from edition 60: a vendor's own displayed
  percentage-change field can diverge from a direct settle-to-settle
  calculation off its own two closing prices.** Investing.com's displayed
  "Change %" column disagreed with (current close − prior close) / prior
  close by roughly 20-80bp across nearly every tracked commodity/FX
  instrument this edition — see the dedicated Standing Facts entry above.
  Compute the percentage directly from the two closing prices rather than
  trusting the vendor's own displayed field, going forward, and disclose
  when they diverge.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 60 have all run clean (or
  clean after quick fixes) — **edition 58 needed ZERO fixes; edition 59 ALSO
  needed zero fixes; edition 60 needed one fix** (a reserved Annex C number
  for westmetall.com that wasn't yet cited inline when first drafted — added
  a citation to the LME copper table rows).
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 60 have all rendered with zero stray tildes on the
  first draft, bar editions 56 and 57 which each needed one fix** — a
  reminder that the fix/no-fix pattern doesn't correlate cleanly with
  content density.
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39, 44, 49 and 54 have
  all resolved this cleanly for CFTC CoT. Not applicable at editions 55
  through 60 (no fresh CFTC data triggered the chart in any of those
  windows). The next report (due Mon 16 Nov, covering Tue 10 Nov data)
  falls inside edition 65's plausible window.
- **The diffuse-overflow lesson from editions 44-45 and the duplicated-
  content lesson from edition 47 are both still worth checking first on any
  overflow** — but **edition 53 showed overflow can also be genuinely dense
  content requiring real trimming, while editions 54 through 58 all showed
  the opposite, and edition 60 showed a THIRD distinct overflow cause: not
  stray break, not genuine density, but a trailing small element pinned by
  an Annex C column block that filled nearly the whole remaining page
  regardless of how much preceding prose was trimmed** (see Production
  Notes). Always check which situation you're in before assuming a
  particular fix is the answer.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — **specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation.** No capping
  has been needed in any edition since 45. Edition 60's movers chart (8
  categories, TTD +15.47% largest, HIMS -11.77% second largest) had a ratio
  of approx. 1.31x; used `pad_frac=0.26` with figsize (9.8, 1.80) — rendered
  cleanly. Edition 58 used `pad_frac=0.24` for a 7-category panel spanning
  -54.68% to +31.04% (ratio approx. 1.007x, the tightest logged to date);
  edition 59 used 0.26 for a 9-category panel spanning -16.15% to +35.33%
  (ratio approx. 2.19x). `pad_frac=0.30` for the 11-category sector panel
  has now rendered cleanly across fifteen editions (45-50, 52-60).

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`, under the `quotes/` path
  specifically — `charts/_VIX.json` returns 403, `quotes/_VIX.json` works).
  **Editions 28 through 60 have all got a fresh, same-day-timestamped
  sweep** — thirty-three consecutive fresh sweeps now. **The feed's two
  known bugs (a duplicated `prev_day_close`, and a `price_change_percent`
  that divides by current price instead of prior close) appeared on ALL SIX
  series at edition 54, were ABSENT on all six series at editions 55 through
  58, RECURRED on all six series at edition 59, then were ABSENT again at
  edition 60.** The bug can toggle unpredictably edition to edition — always
  compute day-over-day % change manually (current_price − price_change,
  then divide) regardless of how many consecutive bug-free reads preceded
  the current one. **Edition 60's own session: the complex fully
  un-inverted back into clean ascending contango** — VIX -22.3% to 19.92,
  VIX9D -26.9% to 19.88, VIX3M -15.2% to 20.85, VIX6M -10.0% to 22.22, VVIX
  -19.3% to 98.43, SKEW -2.1% to 150.34 — completely resolving Thursday 5
  Nov's record inversion and Friday 6 Nov's mixed, transitional shape within
  two sessions.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 60 fetched all 11 directly again**
  (Industrials +3.82% the leader, narrowly ahead of Technology +3.73%;
  Consumer Discretionary +2.92% and Communication Services +2.45% also
  outperforming; Energy +0.52% the clear laggard despite still closing
  higher, consistent with crude's own sharp decline the same session;
  Consumer Staples +0.90% the only other sector under 1%; 11 of 11 closed
  higher, a near-complete reversal of Friday's narrow 3-of-11 breadth) —
  continue this direct-fetch-by-default method. **A secondary cross-check
  (MarketWatch/WSJ) could not be fetched at edition 60** — single-sourced
  this edition, disclosed in Annex A; try the cross-check again at edition
  61 rather than assuming it will keep failing.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (0 of 11 at edition 58, the
  starkest down-day reading logged to date; 3 of 11 at edition 59; **11 of
  11 at edition 60, the strongest up-day reading logged to date — a mirror
  image of edition 58's washout just two editions earlier**) — no competing
  secondary-aggregator breadth figure was checked at edition 60 either.
- **Dealer gamma:** zerogex.io hit a **TWENTY-FIRST consecutive edition of
  failure at edition 60** (all widgets still show placeholder dashes with no
  timestamped data). SpotGamma logged a **FIFTEENTH straight failure at
  edition 60, via a NEW failure signature**: the main marketing page now
  returns HTTP 200 (not a 403/Cloudflare block) but carries no live
  gamma/skew numbers, while its `/dashboard` path redirects to a
  `wp-login.php` authentication wall — a different blocking mechanism than
  the Cloudflare 403 logged through edition 59, but still fully unusable for
  structured data. Both sources remain fully unusable.
- **Official CME FedWatch probabilities:** the page blocks fetching
  (edition 60's direct attempt timed out again, a **TWENTIETH** consecutive
  failure, 41-60) — use secondary citations (Polymarket, Kalshi, Reuters/
  other economist polls, desk notes) and give a range rather than a single
  invented number. **Polymarket direct, tried via its Gamma API
  (`gamma-api.polymarket.com/public-search`) rather than a plain site visit,
  succeeded again at edition 60 — a SEVENTH consecutive success** — this
  remains the preferred first approach; try it before reverting to a plain
  site visit. **DeFi Rate's blended aggregator also returned a fresh,
  same-day-timestamped read again at edition 60** — continue the
  cross-check discipline against it.
- **Kalshi direct fetch:** rate-limited or blocked across every edition it
  has been attempted, now **TWENTY-FOUR consecutive failures (37-60)** — a
  confirmed structural gap, not transient. **Edition 60's specific failure
  mode changed to HTTP 401 (Unauthorized), the first time it has NOT been
  HTTP 429** — worth noting in case this signals a different (e.g.
  authentication-based, rather than rate-limit-based) blocking mechanism
  going forward. Resume the attempt-every-edition discipline at edition 61
  regardless. Use Kalshi's own secondary reporting or DeFi Rate's blended
  aggregator as the workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **westmetall.com (LME copper): the cash
  series stayed clean at edition 60, but the 3-month series hit a new,
  narrower query-parameter problem** — see the dedicated Standing Facts
  entry above (its table view returned only the latest date regardless of
  the date-range parameters tried; not the same as edition 58's now-resolved
  missing-row issue).
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **remained clean at edition 60** (2-yr
  4.56%, 10-yr 4.88%, 30-yr 5.26%, all 9 Nov, with the prior Friday base
  matching the previous edition exactly), extending the clean streak to
  **twenty-five editions (37-60)** with no repeat of the edition-36 33bp gap.
  Continue scoping the TextView URL to the specific month
  (`field_tdr_date_value_month=202611`-style parameter) rather than the
  full year.
- **CFTC CoT:** publishes with the prior Tuesday's data — always state the
  lag explicitly. `financial_lf.htm` works well for equity index futures
  (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). **No new report fell inside edition 60's window** (the most
  recent, covering Tuesday 3 Nov data, was released Friday 6 Nov and fully
  summarized at edition 59). **MAJOR CORRECTION at edition 60: the next
  report is NOT due Friday 13 November 2026 as previously assumed.**
  CFTC's own official release-schedule page
  (`cftc.gov/MarketReports/CommitmentsofTraders/ReleaseSchedule/index.htm`)
  lists its tentative November 2026 dates as the **6th, 16th, 20th and
  30th** — an irregular spacing (not a plain weekly Friday cadence), with
  the 16th and 30th both flagged as holiday-delayed. **The next report is
  now due Monday 16 November 2026**, covering Tuesday 10 November data —
  this falls inside edition 65's plausible window (if no gap); check
  cftc.gov directly then. **Worth watching: is this irregular spacing
  evidence that CFTC's previously-announced move to twice-weekly releases
  (a 27 Oct 2026 CFTC announcement, Press Release 9316-26) has quietly
  begun, or is it simply holiday-driven spacing around Veterans Day (11
  Nov)?** Not resolved either way at edition 60 — a one-line check at
  edition 65 should help settle it.
- **GBP/USD, EUR/USD, USD/JPY clean close:** all remain fully resolved,
  reconciling cleanly again at edition 60 (EUR/USD 1.1224 +0.72%, GBP/USD
  1.3441 +0.68%, USD/JPY 157.91 -0.36%, all single-sourced to Investing.com's
  close-to-close history table, Friday base matching this edition's own
  fresh re-fetch exactly). **DXY itself also resolved cleanly at edition
  60** (Yahoo DX-Y.NYB and the Investing.com proxy agreeing within approx.
  3bp) — see the dedicated Standing Facts and Hard Rules entries above.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot cross-check stayed in its fourth failure mode (total
  inaccessibility) for a second consecutive edition at edition 60** — see
  the dedicated Standing Facts and Hard Rules entries above; no Kitco spot
  figure is reported this edition either. Monday 9 Nov futures base
  figures: gold futures $4,148.32 (+1.80%), silver futures $53.458 (+2.92%),
  both reconciled cleanly against their vendor-confirmed Friday bases (see
  the vendor-retroactive-revision-trap entry above for the one narrow
  cross-vendor silver-base exception).
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is also a closed thread as of
  edition 45. **US GDP, PCE, import/export prices and industrial
  production:** all closed threads — see Standing Facts above. **University
  of Michigan October consumer sentiment** is a closed thread as of edition
  49. **China's October PMI** is a closed thread as of edition 54. **October
  ISM Services PMI** is a closed thread as of edition 57 (headline only;
  sub-index detail remains an Annex B item). **October US CPI** is due
  Tuesday 10 November 2026 (edition 61's window) — a live, not-yet-released
  figure. **October US PPI** is due Friday 13 November 2026 — also live.
- **Henry Hub natural gas:** the front-month-contract-identity question
  remains resolved (NGZ6/December, no roll to NGF7/January yet as of 9 Nov).
  **The base-price reliability problem — this report's historically
  worst-performing data-quality issue — stayed substantially CLOSED at
  edition 60**, a fifth consecutive clean two-source reconciliation
  (Investing.com $3.201/MMBtu, Yahoo Finance NG=F $3.213, close agreement).
  Resume only occasional spot-checks rather than a dedicated every-edition
  reconciliation effort unless a fresh conflict appears.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 60 found optionslam.com
  DID return usable data this time** (implied moves for a range of smaller
  upcoming-earnings names: CEVA, PRAX, TDW, HRB, QLYS, ASTS, WGS, RKLB,
  ZETA, CEG, ADM, KMPR, LINE, TECH) — a change from editions 58-59's total
  failures — **but none of the exposed figures tied to Monday's own largest
  movers (TTD, CEG, MNDY, HIMS)**, so no chartable implied-vs-realized story
  resulted and no third chart was used. Treat the general sub-item as
  low-yield most editions but worth a genuine attempt every time, since the
  source itself is not always down — sometimes it simply doesn't cover the
  right names.
- **Weekend equities catalyst to watch: 13F filings.** **MAJOR CORRECTION
  at edition 60: the Q3 2026 deadline is NOT "approx. 14 November 2026" as
  previously assumed.** Multiple independent 13F-deadline-calculator sources
  confirm the actual rule is 45 days after the 30 September 2026 quarter-end,
  which falls on Saturday 14 November and rolls to the next business day —
  **Monday 16 November 2026**. This now coincides with the corrected CFTC
  CoT report date (also Monday 16 Nov) — both land in the same edition's
  window, likely edition 65 if no gaps. Factor 13F coverage into whichever
  edition covers that Monday.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22, not attempted
  again since). Revisit only if a future edition has spare research
  bandwidth on an FOMC day specifically — not relevant to most editions.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully at
  editions 39, 44-49, 54 and 59 (the Friday 6 Nov report, covering Tuesday 3
  Nov data: ES OI 1,986,532; NQ OI 292,587; RTY OI 449,399). No new report
  fell inside edition 60's window. Repeat the three-instrument fetch
  whichever edition's window extends past Monday 16 November 2026 (the
  corrected next-report date — likely edition 65), watching for the
  micro-vs-full-size naming trap each time, and for whether the
  twice-weekly-release schedule change has actually begun (see the CFTC CoT
  entry above).
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 58 went
  further than prior editions on this sub-item: no analyst action at all
  from the session could be independently verified. **Edition 59 found the
  same result for a second straight edition, and edition 60 extends this to
  a THIRD consecutive edition with zero verifiable analyst actions** — a
  dedicated search for Monday's session returned no analyst-action item tied
  to a named analyst/firm and the correct date; none is reported. Watch each
  edition independently rather than assuming a trend, but this is now a
  three-edition pattern.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** This discipline has now caught numerous fabrications
  and errors (full list in the Standing Facts "named secondary outlet" entry
  above), and **edition 60 added its most dramatic instance yet**: a
  circulated claim that Nvidia's board formally announced an independent
  investigation into CEO Jensen Huang, including a staff apology email,
  which could not be corroborated by any dated wire or SEC filing despite
  initially appearing confirmed by named-outlet citations in one research
  pass. Every reported single-stock mover at edition 60 (TTD, RKLB, CEG,
  LCID, TTWO, NVDA, MNDY, HIMS) was individually cross-checked against its
  own primary SEC filing where tied to earnings, or against a direct price
  history fetch otherwise — continue this direct-verification discipline on
  every edition.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted at editions 48 through 60 (out of scope each time); try
  an alternate DOL page or a secondary economic-calendar aggregator for the
  consensus figure at edition 61.
- **federalregister.gov's direct search interface is blocked, re-tested
  directly again at edition 60 and still blocked** (a prior search attempt
  302-redirected to `unblock.federalregister.gov`, an apparent bot/rate-limit
  gate, first logged at edition 48). govinfo.gov continues to be the known
  working alternative route for at least some Federal Register content.
  **Edition 60 tried a new approach: the Federal Register's own developer
  API (`federalregister.gov/api/v1/documents.json`), which returned actual
  results (unlike the blocked search UI) though nothing relevant to the
  specific Section 301 question searched** — this is a genuinely different
  access path from the blocked search page and worth trying again at
  edition 61 for other Federal Register lookups too.
- **SEC EDGAR's `cgi-bin/browse-edgar` company-search page (filtered by CIK
  and form type 8-K) is a highly reliable, fast way to confirm both WHETHER
  a company has reported on a given date and to find the accession number
  for the underlying exhibit** — used again at edition 60 for Constellation
  Energy, monday.com, The Trade Desk and Hims & Hers. Edition 58
  demonstrated a valuable NEGATIVE use case (the absence of a matching 8-K
  disproved a circulated claim) — worth remembering this tool is just as
  useful for debunking an unverifiable claim as for confirming a verifiable
  one; it would also have been the right next step to try against the
  Nvidia board-investigation claim at edition 60, had time allowed (a
  WebSearch-based check found no corroboration first, which was sufficient).
- **Riksbank's primary policy-rate/next-meeting page:** fully resolved as of
  edition 57 (hiked to 2.00% on 4 Nov 2026) — see the dedicated Standing
  Facts entry above. The vote split from that decision remained unresolved
  at edition 60 too; **now directly confirmed via riksbank.se's own calendar
  and minutes archive that the vote-split minutes are due 10 November 2026,
  09:30 CET** (after edition 60's own window closes) — likely landing inside
  edition 61's window (covering Tuesday 10 Nov).
- **ECB's current policy rate: SETTLED since edition 55** (unchanged through
  the 28-29 October 2026 meeting: deposit facility 2.50%, main refi 2.65%,
  marginal lending 2.90%); not re-attempted at editions 56 through 60 (no
  fetch needed). It reopens on contradiction, the next Governing Council
  decision, or the monthly audit. The Council's own next-meeting date is
  SETTLED at 16-17 December 2026 (confirmed directly at edition 59).
- **Banxico's own primary site (banxico.org.mx) remains unreachable** for a
  further edition — at edition 60 every path tried 302-redirected to the
  "anterior.banxico.org.mx" subdomain, which is now live (unlike edition
  59's dead redirect target) but returns HTTP 404 on the specific sub-paths
  tried, while the subdomain's own root returns HTTP 403 — a refined,
  multi-stage failure signature, now a confirmed structural gap across
  multiple editions, not transient. Continue the attempt-every-edition
  discipline with yet another fresh URL path, but rely on the consistent
  multi-outlet Mexican financial press as the working alternative when it
  fails.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel —
  confirmed clean again at edition 60 (twenty-one editions total: 37-43,
  45-50, 52-60). For charts with fewer categories, scale the height down:
  roughly `(9.8, 1.65-1.95)` for 3-9 categories. **Edition 60 used `(9.8,
  1.80)` for an 8-category movers chart with `pad_frac=0.26`**, rendering
  cleanly across a -11.77% to +15.47% range (ratio approx. 1.31x). **Always
  render and visually inspect (via the Read tool) the actual PNG at or near
  full resolution before embedding it**, regardless of what a past edition's
  success might suggest. **Default to pad_frac=0.30 from the start for an
  11-category sector-ETF panel** — now confirmed across fifteen straight
  small-magnitude 11-category panels (45-50, 52-60). For any movers chart
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
  threshold, including edition 60's approx. 1.31x) — reinforcing that the
  trigger is the ratio to the next-largest bar, not the largest bar's
  absolute size.
- **A grouped (two-series) horizontal bar chart — needed for the CFTC
  Asset-Manager-vs-Leveraged-Funds positioning chart — requires custom chart
  code, not the standard single-series `barh()` helper used for the
  movers/sector charts** (first built at edition 44, reused successfully at
  editions 49 and 54; not needed at editions 55 through 60 since no fresh
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
      annex opens a clean page 4, exactly as before.
    - Sections 1-6 spill onto page 4 → **delete the `pagebreak` div and
      re-render**, so the annex follows the spillover down page 4 instead of
      starting a fifth page. **Edition 60 hit this exact symptom** (two
      Section 6 sector-setup bullets' worth of content pushed sections 1-6
      past page 3) and the usual fix was necessary — but this time **not
      sufficient on its own**; see the new multi-column lesson immediately
      below for what else was needed.
    - Still five (or more) pages with the break gone → now trim, in this
      order: sector table rows with no news in the window, the third chart
      if there is one, then prose — **but if the specific symptom is a tiny
      trailing block (e.g. just the Method note, or one lonely Annex C
      entry) alone on an otherwise-blank extra page, check FIRST whether the
      immediately-preceding multi-column block (`.cols2`/`.cols3`) is itself
      already filling almost the entire remaining page, per the lesson
      below, before assuming more prose-trimming earlier in the document
      will help** — it usually won't.
  Note on the `grep -c 'pagebreak'` self-check: the CSS baseline defines a
  `.pagebreak` class rule AND the body uses one `<div class="pagebreak">` —
  a literal `grep -c 'pagebreak'` therefore normally returns **2** on a
  correctly-built edition (one CSS rule line, one div usage line), not 1.
  The actual check that matters is `grep -c 'class="pagebreak"'` (counts
  only div usages), which should be 1, or 0 on a spillover edition (0 at
  edition 60), never 2.
- **MAJOR NEW LESSON from edition 60: a CSS multi-column (`.cols2`/`.cols3`)
  block, laid out with the default `column-fill: balance` inside a
  Chromium-paginated print context, will often stretch to use nearly ALL of
  the remaining space on the current page — right up to the bottom margin —
  regardless of how little content it actually contains, as long as its
  natural (unconstrained) height is somewhere in the neighborhood of that
  remaining space.** This produces a specific, now-recognizable symptom:
  a small trailing element immediately after the multi-column block (in
  edition 60's case, the `.method` div) gets pushed onto its own near-blank
  extra page, and **trimming the PROSE THAT PRECEDES the multi-column block
  has little or no visible effect on this** — across roughly six separate
  render iterations at edition 60, repeated edits to Annex A and Annex B
  bullets (which come before Annex C in the document) produced a
  byte-identical page-4/page-5 split every time, because the balanced
  column box simply re-expanded to fill whatever space was freed up by the
  earlier trims. **What actually fixed it: trimming the multi-column
  block's OWN content** — specifically, shortening roughly fifteen of
  Annex C's individual source citations (dropping repeated "filed 9 Nov
  2026" boilerplate from each SEC EDGAR entry, merging seven separate
  central-bank-website citations into one shared entry, and cutting filler
  words from a dozen other entries) — which reduced the column block's own
  natural height enough to leave genuine room after it. **A `column-fill:
  auto` experiment was also tried** (filling each column to its natural
  content height sequentially, rather than balancing all three) **and made
  things WORSE, not better** — it produced a more lopsided distribution
  (two long columns, one short one) whose tallest column was taller than the
  balanced version's tallest column had been, pushing the trailing element
  even further down. **It was reverted; `column-fill`'s default (`balance`)
  remains the right choice and the CSS baseline was NOT changed in the
  published edition.** **Lesson for future editions: if a trailing element
  right after a `.cols2`/`.cols3` block is alone on an otherwise-blank extra
  page, first measure (e.g. with a quick Python/PIL pixel-row check on the
  rendered page PNGs, or just a careful visual read) whether the
  multi-column block itself is already using nearly the full remaining
  page. If so, trim THAT block's own list-item text, not the prose before
  it** — and expect that even fairly large cuts to the preceding prose will
  show zero visible effect until you do.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix.
- **A markup-correctness trap, logged at edition 47: a `<sup class="ref">`
  citation tag placed immediately after a table row's last `</td>` but still
  inside the `<tr>` (i.e. not nested inside any `<td>`) is invalid table
  structure.** `check_refs.py` will NOT catch this. **Always nest every
  `<sup class="ref">` tag inside a `<td>...</td>` pair, never as a sibling of
  one inside a `<tr>`** — grep for `</td><sup` as a quick self-check if a
  table was built with a lot of copy-paste. **Editions 55 through 60 all ran
  the same proactive grep and found zero instances, a sixth consecutive
  clean sweep.** Run the grep on every edition with such a table, not just
  when troubleshooting a layout problem.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  **Edition 60 needed this discipline more than almost any prior edition
  except 53** — roughly eight render iterations were needed (see the
  multi-column lesson above), and the page images were read in full at every
  single iteration, which is precisely how the "byte-identical page split
  despite edits" pattern was noticed and correctly diagnosed rather than
  mistaken for the edits simply not having rendered.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across many editions'
genuinely different content volumes, including editions 53's through 60's.
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
- Annex C: three columns at 5.5pt, left-aligned, **default `column-fill`
  (`balance`) — do not switch to `auto`, confirmed worse at edition 60 (see
  the Production Notes lesson above).**
- Content budget: 60-second read (5 items); equities as the largest block
  plus the movers table; macro/commodities/derivatives tighter; **a "This
  week's known catalysts" table plus a "Sector setup we take into [session]"
  bullet list at the end of Section 6 by default** for any single-session or
  weekend-window edition. **An optional "Commodities & FX levels" table
  (~9-13 rows)** at the end of Section 4 is available as padding if page 3
  runs short — editions 44 through 60 have all folded commodities, FX and
  Treasuries into ONE combined table (10-17 rows; edition 60 used 15) as the
  PRIMARY commodities table rather than padding, now the standing default.
  **Always re-render immediately after adding (or removing) any content to
  confirm the page count — and if a change to Annex A/B text doesn't move
  the page split at all, suspect the Annex C column-balance effect above
  before assuming the edit silently failed to save.**

**Chart selection guidance.** Placement is not editorial for the first two
charts:

- **Sector-ETF performance chart → Section 1 (Market recap), every
  edition.** Same-day closes by default; a grouped day-over-day bar instead
  on a multi-session or weekend window, or on a genuine multi-sector
  broadening selloff across consecutive sessions. **Edition 60 used a
  single-day bar** (only one NYSE session fell inside its window).
- **Single-stock movers bar → Section 2 (Equities), every edition.**
- **A third chart only when positioning or volatility is genuinely the
  day's dominant story**, never to fill a page, placed in the section it
  belongs to:
  - Fresh CFTC CoT data → the ES/NQ/RTY asset-manager-vs-leveraged-funds
    positioning chart, normalized as % of open interest, built with the
    grouped-bar technique documented under Production notes, in **Section
    5**. Editions 24, 34, 39, 44, 49 and 54 have all placed it there; none
    of editions 55 through 60 had fresh data available inside their own
    windows. The next opportunity (the corrected Monday 16 Nov report) falls
    inside edition 65's plausible window.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully. Not used at editions 55
    through 60 — edition 60's optionslam.com fetch actually returned data
    this time (a change from 58-59's outright failures) but none of it tied
    to Monday's own largest movers.
  - A holiday-window preview edition with no fresher data → VIX futures
    term structure with event annotations, in **Section 5**. Not used at
    editions 55 through 60 — in each case the VIX term structure was
    genuinely newsworthy (a kink, its narrowing, a dramatic one-day collapse
    at 57, a full contango-to-backwardation inversion at 58, a partial
    unwind at 59, then a full return to clean ascending contango at 60) but
    was judged secondary to the session's dominant equity/macro story each
    time and was covered fully in prose instead.

**Edition 61 (expected to cover Tuesday 10 November 2026, assuming no gap)
has a genuinely live, dense calendar load — several items are specifically
expected to land inside this window rather than being routine watch-and-
confirm.** Verify directly rather than assuming:
- **October US CPI**, due 8:30am ET Tuesday — the next hard data point for
  the already-firming December hike odds (approx. 77-82% as of edition 60);
  no reliable consensus figure was found at edition 60 (secondary
  aggregators gave contradictory 2.7%-3.7% range figures and were
  discarded) — try again for a genuine consensus at edition 61, from a
  single clearly-named source (e.g. a specific Dow Jones/FactSet-attributed
  figure) rather than an unattributed aggregator number.
- **Riksbank's 4 November vote-split minutes**, due 10 Nov 09:30 CET —
  confirmed not yet posted as of edition 60's own window close; check
  riksbank.se directly.
- **The Section 301 178-product China tariff-exclusion lapse** — whether
  operative at 11:59pm ET Monday 9 Nov (per the notice's own DATES section)
  or effectively Tuesday 10 Nov (per its background text and USTR's press
  release); check federalregister.gov/govinfo.gov, the FR developer API, and
  ustr.gov directly for any last-minute extension filing, and note which
  date the notice ultimately treats as operative. **Also check the
  adjacent, not-yet-primary-verified IEEPA/reciprocal "fentanyl tariff"
  China rate cut**, reportedly keyed to the same midnight boundary per a
  secondary (Trading Economics) source — a different legal mechanism, don't
  conflate the two.
- **Midterm-election certification status** — still unconfirmed after three
  straight editions of searching; try again.
- **Banxico's primary site** — via yet another fresh URL path.
- **Whether December FOMC hike odds (approx. 77-82% as of edition 60) hold,
  extend further, or ease** — a fresh Polymarket/DeFi Rate pull.
- **Whether the chip complex (now fully round-tripped above pre-selloff
  levels for AMD/Intel, still below for Marvell/Broadcom/Micron) continues
  higher, and whether Nvidia specifically stabilizes or falls further** amid
  the ongoing Huang/Megaspeed overhang — watch for any GENUINE dated
  development (an SEC filing, a wire-service report of board action, a
  scheduled hearing), not a repeat of the unconfirmed 8 Nov claim.
The WTOP/La Nación AP-wire-mirror approach and the Polymarket Gamma-API
approach are both now on seven-edition clean streaks — use them first rather
than their respective fallbacks. **Remember the new Annex-C-trimming lesson
above if a trailing element gets pinned alone on an extra page again** — it
is now a recognized, specific failure mode with a specific fix, not a
mystery to re-diagnose from scratch.

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

**Edition 59's carried-forward spec was 131,705 bytes, over the
100,000-byte threshold — this run (producing edition 60's spec) condenses
the log.** Edition 58's own full-detail entry (previously left as a separate
condensed paragraph) is folded into the running mega-block (now "Editions
1-58"); edition 59's own full-detail entry is condensed down to a medium
paragraph; edition 60 is added in full detail. There is no maximum size;
condensing is housekeeping done by the run itself, not a check to pass —
there is no penalty for the file staying somewhat large if the alternative
is losing information.

**Editions 1–58 (condensed):** established the format (edition 1 baseline;
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
two fixes. **Edition 56** (Wed 4 Nov, covering Tue 3 Nov): equities diverged
on composition, not breadth (S&P +0.36% to 7,568.92, Nasdaq +0.83% to
25,372.01 on a megacap/AI bounce; Dow -0.38% to 51,786.72; only 4 of 11
sector ETFs higher). The RBA delivered its fifth 2026 hike (25bp to 4.85%)
on a first-ever split 6-3 vote. AMD's fiscal Q3 (revenue $13.4bn +45% y/y)
drew a genuinely positive AH reaction (+5.02%), a counter-example to the
week's muted-to-negative beat-and-raise pattern. A claimed Oracle
analyst-upgrade note was investigated and rejected as unreliable; the Bank
of England's 5 November decision date was upgraded to primary-sourced;
Henry Hub reconciled cleanly across two sources for the first time in six
editions; the VIX feed's two known bugs were absent for a second
consecutive edition. Rate-path odds firmed to approx. 74-75% hike. First
draft converged cleanly to 4 pages on the first render; 29/29 sources clean
after one fix. **Edition 57** (Thu 5 Nov, covering Wed 4 Nov): dominant
story was the 3 November 2026 US midterm elections, called for Democrats in
both chambers by Wednesday morning, ending unified Republican control — Dow
+3.03% to 53,356.12 (then this report's largest one-day move), S&P +1.58% to
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
back — see editions 58-60). A Federal Register filing resolved the
Section 301 178-product exclusion lapse date (later found internally
inconsistent — see edition 59). Henry Hub posted a second consecutive
clean reconciliation; Veterans Day (11 Nov) was independently confirmed as
an equities-open/bonds-closed holiday. First draft converged cleanly to 4
pages on the first render; 33/33 sources clean after one fix. A dedicated
verification pass was run on the election outcome and the Riksbank
decision given how consequential and surprising both were. **Edition 58**
(Fri 6 Nov, covering Thu 5 Nov, the window's one NYSE session): a full,
sharp reversal of Wednesday's election rally, driven by an AI-capex/
data-center-moratorium scare (local ballot measures tied to the midterms
rejected data-center buildouts in 40 of 41 votes; UBS flagged approx. 30%
of 2028 data-center capacity as at risk). S&P fell 4.4% to 7,353.73, Dow
fell 3.4% to 51,523.06, Nasdaq fell 5.5% to 24,315.00 (correction
territory), Russell 2000 fell 4.4% to 2,729.89; zero of 11 sector ETFs
closed higher. The semiconductor complex (Micron, AMD, Marvell, Broadcom,
Intel, Nvidia) all fell double digits on no company-specific news. VIX
posted its sharpest one-day increase on record (+69.66% to 28.18), fully
inverting contango into backwardation. A dense earnings cluster, each
verified against primary filings: Qualcomm -9.49% confirmed close
(superseding edition 57's AH snapshot), Arm -13.08%, Tripadvisor -27.65%
(goodwill impairment plus same-day CEO/CFO departures), AppLovin +31.04%,
Krispy Kreme +30.68%, Veracyte -54.30%, MNTN -54.68%; a second AH wave
(Cloudflare, JFrog, Airbnb up; Atlassian, Natera down) was reported as
unconfirmed snapshots only. Three "named secondary outlet flatly wrong"
instances were caught and excluded (a fabricated DraftKings AH figure, an
unsupported Natera "new CEO" claim, an entire "biggest calls" list found
unsupported). Two central banks delivered opposite surprises the same
session — the Bank of England hiked 25bp to 4.00% (8-1, Mann dissenting for
50bp); Banxico reportedly cut 25bp to 6.25% (3-2 vote), secondary-sourced
only. December 8-9 FOMC hike odds eased sharply to approx. 66.5%. First
draft converged cleanly to 4 pages on the first render; 21/21 sources clean
with zero fixes needed.

**Edition 59 (condensed)** — Monday 9 November 2026 report covering Friday
6 November 2026, research window Thu 5 Nov 2026 20:00 ET through Sun 8 Nov
2026 20:21 ET (the window's one NYSE session, plus the weekend). Dominant
story: a much-stronger-than-expected October jobs report (nonfarm payrolls
+165,000 vs. a FactSet-polled consensus of +65,000, unemployment 4.1%,
August/September revised up a combined +84,000) snapped December FOMC hike
odds back from edition 58's approx. 66.5% to approx. 76.5-77%, against a
narrow, chip-led equity relief rally that only partly reversed Thursday's
AI-capex rout. S&P +0.3% to 7,376.86, Nasdaq +1.1% to 24,579.42, Russell
+0.9% to 2,754.11, Dow -0.5% to 51,285.73 (lacking the same chip weighting);
only 3 of 11 sector ETFs closed higher (Technology the leader, Consumer
Staples the laggard). The chip complex staged a relief rally on no fresh
company-specific news (AMD +11.04%, Intel +7.71%, Micron +5.12%, Marvell
+5.73%, Nvidia +2.78%, Broadcom +0.74%), none regaining its pre-selloff
level yet. Thursday's second AH earnings wave all got confirmed Friday
closes holding direction (JFrog +35.33%, Airbnb +11.67%, Cloudflare +9.91%,
Atlassian -16.15%, Natera -14.59%). A widely-surfaced "Friday close" figure
was found to be a stale-date restatement of Thursday's actual close,
excluded. VIX partially unwound Thursday's record spike (-9.01% to 25.64)
in a mixed, transitional term-structure shape; the CBOE feed's two known
bugs recurred after four clean editions. A fresh round of the
vendor-retroactive-revision trap hit WTI/gold/silver/COMEX copper; Kitco's
historical-close pages became totally inaccessible for the first time. The
ECB's next-meeting date resolved (16-17 Dec); Banxico's primary site failed
via a new signature; government funding was downgraded to secondary-sourced
for one edition. Midterm certification remained unconfirmed. No correction
box; first draft spilled two Section 6 bullets onto page 4, fixed by
deleting the break; 19/19 sources clean with zero fixes; zero stray tildes.

**Edition 60 (most recent — full detail)** — Tuesday 10 November 2026
report covering Monday 9 November 2026, research window Sun 8 Nov 2026
20:00 ET through Mon 9 Nov 2026 20:21 ET (the window's one NYSE session).

**The dominant story was a broad, 11-of-11-sector equity relief rally
coinciding with a sharp oil-price crash, against a backdrop of December
FOMC hike odds extending further hawkish rather than reversing.** The S&P
500 rose 2.3% to 7,549.94 (AP's wire called it the S&P's best day since 8
April), the Dow gained 1,104.02 points (+2.2%) to 52,389.75, the Nasdaq
Composite added 2.7% to 25,253.14 and the Russell 2000 rose 3.1% to
2,840.81 — confirmed via a WTOP.com AP-wire mirror, with CNBC's live blog
corroborating direction/magnitude but giving the S&P at +2.4% (a
rounding-level discrepancy, disclosed). WTI crude fell approx. 4.8% to
$86.44 and Brent fell approx. 5.9% to $92.57, on Trump indicating further
US strikes on Iran were "highly unlikely" while talks continue, reinforced
by a Reuters-reported OPEC October output increase (approx. +1.38 million
bpd m/m) pointing to a global surplus — a genuine, named, multiply-sourced
catalyst, not an unexplained move. December 8-9 FOMC hike odds extended to
approx. 77-82% across Polymarket and DeFi Rate (from edition 59's approx.
76.5-77%), the third consecutive directional read the same way.

**The chip complex's relief rally extended for every name except Nvidia.**
AMD (+13.26% to $508.58) and Intel (+5.49% to $59.37) are now above their
pre-selloff (Wed 4 Nov) levels; Marvell (+9.49%), Broadcom (+8.78%) and
Micron (+6.25%) remain below. Nvidia alone fell again (-4.27% to $178.67,
now -10.72% below pre-selloff), attributed in the published briefing to the
ongoing overhang of the real, 29 October NYT/FT-reported story about
Megaspeed executive Alice Huang's alleged China-intelligence ties and her
relationship with CEO Jensen Huang. **A widely-circulated, more dramatic
claim — that Nvidia's board formally announced an investigation into Huang
on 8 November, including a staff apology email — was investigated via two
conflicting research-pass reads and a dedicated direct follow-up search,
and found uncorroborated by any dated wire, SEC filing, or reputable
outlet; it was excluded from the published briefing.** See the dedicated
Standing Facts entry for the full account — this is the sharpest instance
yet of the "named secondary outlet can be flatly wrong" trap, precisely
because it initially looked corroborated.

**Single-stock movers:** The Trade Desk +15.47% (predates its after-the-
close Q3 report), Rocket Lab +10.91% (no identified driver), Constellation
Energy +10.46% (Q3 beat-and-raise), Lucid +9.42% (no identified driver),
Take-Two -3.48% (no identified driver, reports after close), Nvidia -4.27%
(above), monday.com -9.10% (Q3 beat but a decelerating Q4 guide), Hims &
Hers -11.77% (predates its after-the-close Q3 report). All four earnings
reports (CEG, MNDY, TTD, HIMS) verified against primary SEC 8-K/6-K
filings. No analyst action could be independently verified — a third
straight edition with none.

**The VIX complex fully un-inverted** (VIX -22.3% to 19.92, clean ascending
contango restored), both CBOE feed bugs absent again after recurring last
edition. No new CFTC CoT report fell inside the window; **the previously-
assumed "next report due Friday 13 Nov" was found wrong** — CFTC's own
schedule lists 6/16/20/30 Nov, so the next report is due **Monday 16
November 2026**, which also happens to be the corrected Q3 13F filing
deadline (also previously mis-assumed as "approx. 14 Nov"). Government
funding was re-confirmed directly against whitehouse.gov (recovering from
edition 59's one-edition dip). The Section 301 178-product tariff-exclusion
lapse remains unresolved through this window's close, now also checked via
the Federal Register's developer API with no result; it is expected to
resolve, one way or the other, inside edition 61's window. Midterm
certification remains unconfirmed. Norges Bank's 5 November interim
forecast-free hold (4.50%, unchanged) was newly confirmed, reinforcing
rather than contradicting its settled status. The vendor-retroactive-
revision trap reversed direction from last edition (a clean reconciliation
on almost every series), but a new, separate issue surfaced: Investing.com's
own displayed "% change" field diverged from direct settle-to-settle math
by 20-80bp across nearly every tracked instrument — a new standing
data-quality flag.

**Format:** no correction box. First draft hit a genuinely new overflow
symptom: deleting the forced page break (the usual spillover fix) got
sections 1-6 plus Annexes A and B onto page 4, but Annex C's own
three-column source block then repeatedly filled to within single-digit
pixels of the page-4 bottom margin regardless of preceding-prose trims,
stranding only the trailing Method note on page 5 across roughly eight
render iterations. A `column-fill:auto` experiment made it worse and was
reverted; the fix that worked was trimming Annex C's own entries directly
(merging seven central-bank-site citations into one, dropping repeated
"filed" boilerplate from SEC EDGAR entries, cutting filler words) — see the
dedicated Production Notes lesson. 27/27 sources clean after one fix; zero
stray tildes; zero `</td><sup` instances. A dedicated direct verification
pass (run by the coordinator itself via WebSearch, not delegated) resolved
the Nvidia board-investigation claim conflict between two research passes.

**Open threads for edition 61.** Edition 61 covers **Tuesday 10 November
2026** (if no gap) — a genuinely dense, live calendar load, not routine
watch-and-confirm. Expected to land inside this window specifically:
**October US CPI** (8:30am ET, no reliable consensus found yet — try again
for a single named-source figure); **Riksbank's 4 Nov vote-split minutes**
(due 10 Nov 09:30 CET); **the Section 301 178-product tariff-exclusion
lapse**, and the adjacent, not-yet-primary-verified IEEPA/fentanyl-tariff
China rate cut reportedly keyed to the same midnight boundary. Also watch
directly: **midterm-election certification status**, unconfirmed for a
third straight edition; **Banxico's primary site**, via yet another fresh
URL path; **whether December FOMC hike odds (approx. 77-82%) hold, extend,
or ease**; and **whether the chip complex continues higher and whether
Nvidia stabilizes**, watching specifically for any GENUINE dated
development on the Huang/Megaspeed story rather than a repeat of the
unconfirmed board-investigation claim. **Still open and unchanged:** Brent
crude's Friday 23 October close three-way split (dormant since edition 53);
New Mexico v. Meta's formal notice of appeal (unconfirmed for a fifteenth
straight edition); the DOL weekly jobless-claims parsing problem; a fresh
federalregister.gov search-interface attempt (the FR developer API is a
promising new access path, worth trying again for other lookups too).
**Dates to hold on to** (one edition per weekday assumed: 61 Tue 10, 62 Wed
11, 63 Thu 12, 64 Fri 13, 65 Mon 16). October CPI and Riksbank minutes both
due Tue 10 Nov 2026 (edition 61), alongside the Section 301 rate-resumption
question. Veterans Day (equities-open, bonds-closed, confirmed) Wed 11 Nov
2026 (edition 62). October PPI due Fri 13 November 2026 (edition 64). **The
next CFTC CoT report AND the Q3 13F filing deadline both now fall on the
SAME corrected date, Monday 16 November 2026** (edition 65) — a change from
the previously-assumed Fri 13 Nov / approx. 14 Nov. BoE and Banxico next
decisions both 17 Dec 2026; the ECB's next meeting 16-17 Dec 2026; the
Fed's next meeting 8-9 Dec 2026; the next monthly settled-facts audit falls
on the first edition of December 2026. Thanksgiving (26 Nov, full closure)
and its Friday half-day (27 Nov) are now worth a direct calendar check
roughly two and a half weeks out (likely edition 73-74 if no gaps).


