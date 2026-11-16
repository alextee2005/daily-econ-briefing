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

## Two header details worth re-stating (both got wrong in earlier editions, plus a third caught at edition 64)

- **The document's date line is the EDITION date, not the session it covers.**
  Editions 20 and 21 both read "Tuesday 15 September 2026" and "Wednesday 16
  September 2026" matching their filenames; edition 22 used the session date
  instead and so carried the same headline date as edition 21. The window line
  is where the sessions covered belong, not the date line. This has now been
  applied correctly for **forty-two straight editions (33 through 64)** —
  treat as settled; edition 64 read "Monday 16 November 2026" as the date
  line, covering the Friday 13 November session (the window's one NYSE
  session) in the window line.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 64 all reused the
  same pattern — now confirmed clean across **thirty-six consecutive
  editions**; edition 64 phrased it "Window: Thu 12 Nov 2026 20:00 ET – Sun 15
  Nov 2026 20:21 ET (Fri 13 Nov close/AH, the window's one NYSE session;
  weekend FX/commodities reopen also covered)." No further confirmation
  needed; treat this as settled.
- **NEW trap caught at edition 64: the date line's weekday NAME can be wrong
  even when the date itself and the date-vs-session rule above are both
  followed correctly.** Edition 63's own PDF (re-read directly at edition 64
  by extracting its first page) printed the date line "Thursday 13 November
  2026." 13 November 2026 is actually a **Friday**, confirmed directly via
  the system calendar (`date -d "2026-11-13" +%A`). The edition's choice of
  *date* was correct (13 Nov, its own edition date, not 12 Nov, the session
  it covered) and the window line was correct too — only the day-of-week word
  attached to that date was wrong. Editions 59 through 62's own date lines
  were checked directly (by extracting each PDF's first page) and all four
  correctly matched weekday to date, so this looks like a one-edition slip
  rather than a systemic bug in how the date line gets built. Edition 64
  disclosed this via a correction box on page 1 and the full record in Annex
  A — the first correction box used since edition 53. **Add a direct
  weekday-vs-date sanity check to the production checklist on every edition
  going forward, not just when something looks off:** before typing the date
  line, run `date -d "<edition-date>" +%A` and compare the result to the
  weekday word you are about to write. This is cheap and would have caught
  edition 63's error immediately.

## Schedule
Run every weekday. Pick the trigger's local time so the effective research
cutoff lands roughly 4 hours after the US market close (20:15 ET) — during
US daylight time that's 00:00 UTC; adjust for standard time. **US daylight
time ended Sunday 1 November 2026, as scheduled — remains a resolved, settled
transition.** **From edition 54 onward, use EST (UTC-5) for all ET/UTC
conversions** until DST resumes — conventionally the second Sunday in March
(expected March 2027; still not independently verified this far out, so don't
cite it as confirmed until closer to the event). On Mondays (or after any
gap), cover the full window back to the previous edition's cutoff, including
the weekend. **Thanksgiving (Thursday 26 November 2026) and the following
half-day session (Friday 27 November) remain a flagged forward calendar item**
— now only 10 days out from edition 64. Thanksgiving is a full closure for
both equities and bonds; the Friday after is a half-day for equities with an
early bond close. Not independently re-verified at edition 64 (still not
quite inside any research pass's window) — re-confirm directly against
nyse.com's holiday calendar and sifma.org's bond-market calendar whichever
edition's window first reaches it (likely edition 72-73 if no gaps, given one
edition per weekday — this is a rough estimate, not a confirmed count, since
Thanksgiving itself may cause a gap or a skipped/minimal edition). **Veterans
Day (Wednesday 11 November 2026) itself is resolved/closed history, not a
forward item any more** — directly observed at edition 62: equities traded a
full normal session while Treasury cash markets and the Federal Reserve were
closed, exactly as expected.

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
value (resolved genuinely at edition 57 via a real hike) and Banxico (resolved
genuinely at edition 58 via a real cut) — both are now settled on the rate
itself, though Banxico remains secondary-sourced on confirmation tier (see
below). **The next monthly audit falls on the first edition of December
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
  federalreserve.gov's own press release text at edition 52, re-confirmed
  again directly at edition 54's monthly audit, no change. Vote 10-2 — a
  hawkish dissent, the first dissent of either kind logged in this report's
  history: Governor Lisa Cook and Cleveland Fed President Beth Hammack both
  preferred raising the target range 25bp. Statement language: activity
  "expanding at a strong pace," inflation "remains elevated," further moves
  data-dependent. A companion implementation note set IORB at 3.90% (eff. 29
  Oct), ON RRP at 3.75%, primary credit rate 4.0%, standing repo rate 4.0%
  (re-confirmed again as the most recently-published funding print at edition
  64, no change). Kevin Warsh's actual press-conference remarks remain
  unverified and not worth a dedicated search this far out. Blackout (Oct
  17-29, 2026) held clean through the decision, as expected. **Next meeting:
  8-9 December 2026, an SEP meeting.**
- **Rate-path odds held essentially flat at edition 64, a mixed October PPI
  print notwithstanding.** A fresh Polymarket Gamma API pull (event
  `fed-decision-in-december-20260729232808632`, id 770450) put the December
  25bp-hike-specific market at approx. **87.5%** (little changed from edition
  63's approx. 88.5%), with a 50bp+ market at approx. **8.65%**. **Kalshi's
  official trading API (`api.elections.kalshi.com/trade-api/v2`, series
  `KXFED`, event `KXFED-26DEC`) worked again at edition 64 — a second
  consecutive success after resolving a 26-edition failure streak at edition
  63** — implying approx. **86-88%** for a 25bp hike (derived from the
  >4.00%/>4.25% strike spread) and approx. **9-12%** for 50bp+, consistent
  with Polymarket. **This official API endpoint remains the recommended first
  approach for Kalshi.** CME FedWatch failed again (connection
  failure/timeout), a **TWENTY-FOURTH** consecutive failure (41-64). DeFi
  Rate's blended aggregator again could not be freshly refreshed (still only a
  stale late-October snapshot) — a second straight edition of this specific
  failure; try again at edition 65. October's PPI (see the new closed-thread
  entry below) came in cooler on headline but hotter on core versus
  consensus — a genuinely mixed print — and left odds essentially where they
  were, rather than extending the hawkish drift of editions 61-63 or
  reversing it.
- **US-China tariff threads: the Section 301 178-product exclusion extension
  remains resolved with a newly-confirmed precise deadline; the second,
  narrower USTR port-fee action from edition 63 remains resolved; the
  broader reciprocal-tariff truce remains unconfirmed by any US primary
  source for a fifth straight edition, now with China's own confirmation of
  its side but still nothing from Washington.** The Section 301 178-product
  exclusion extension (Federal Register Doc. 2026-22925, resolved at edition
  61) stands; edition 64 found and directly read the notice's own official
  citation, **91 FR 72610**, which confirms the operative deadline as
  11:59pm ET **9 January 2027** (not 10 January) — this matches, and now
  precisely sources, this report's existing figure. Edition 63's second,
  narrower Federal Register filing (Doc. 2026-22867, the maritime/port-fee
  Section 301 action, suspended through 9-10 Jan 2027) was not re-touched at
  edition 64 and remains resolved. **The broader 10%-rate "reciprocal
  tariff" IEEPA truce with China** (reportedly extended by Treasury Secretary
  Bessent on 23 September to 10 January 2027) **remains unconfirmed by any
  US primary document for a fifth straight edition (60-64)** — edition 64's
  fresh Federal Register API and whitehouse.gov/USTR.gov search again found
  nothing. Two new, still-secondary data points surfaced at edition 64: a
  law-firm client alert (Valexander) claiming two further orders around 6 Nov
  2026 extended the IEEPA reciprocal rate at 10% through 10 Nov 2026 (which
  only restates the already-passed deadline, not evidence of anything
  beyond it); and China's own State Council confirming on 9 Nov 2026 that
  its 24% retaliatory tariff stays suspended for two months (to approx. 10
  Jan 2027) while its own 10% tariff continues — a foreign primary source
  confirming the Chinese side's intent, but still not a US primary document.
  Do not conflate any of these three (178-product exclusion / maritime
  port-fee suspension / broader reciprocal truce) with each other.
- **Fed Chair: Kevin Warsh — SETTLED, stop re-verifying it every run.** No
  contradiction surfaced through edition 64; directly re-confirmed via
  federalreserve.gov's own bios page at edition 54's November monthly audit,
  closing that housekeeping item cleanly; not re-attempted at editions 55
  through 64 (settled, no fetch needed). His Chairman term ends 21 May 2030
  (took office 22 May 2026, a four-year term); his separate term as a Board of
  Governors member runs to 31 January 2040. The Chairmanship re-opens as a
  live fact only on a successor nominated/confirmed, a resignation or
  removal, or that 21 May 2030 term-end date actually arriving, or the **next
  monthly audit (first edition of December 2026)**.
- **The 3 November 2026 US midterm elections — certification is STRUCTURALLY
  EXPLAINED as of edition 62, which changes what "watch again" even means
  going forward.** Democrats won control of both the House and Senate —
  called by AP/CNBC/NBC/PBS by Wednesday 4 November morning — ending unified
  Republican control of Washington. Democrats flipped at least seven Senate
  seats (Iowa, Kansas, Ohio, North Carolina, New Hampshire, South Carolina,
  Texas); a handful of races were still uncalled as of edition 57's cutoff and
  this was not independently re-checked since — do not cite a final seat count
  without re-checking. Edition 62's dedicated search (via USAFacts,
  ProtectDemocracy and Brennan Center state-certification trackers) found
  there is no single national certification step for midterm elections at all
  — unlike a presidential election, there is no electoral-college-style
  national certification event to wait for. Certification is inherently
  state-by-state, with deadlines running into December (e.g., Georgia, 18 Dec
  2026; Pennsylvania county certification and Arizona/Michigan statewide
  canvasses, all by 23 Nov, previously logged). **Not independently
  re-attempted at edition 64 either** (no new state-certification news fell
  inside its window, consistent with the structural explanation above);
  continue watching specific state deadlines as they land rather than
  searching for a single national resolution event that does not exist.
- **The NVIDIA/Huang governance thread's dramatic resolution from edition 63
  remains the dominant open story, with no new primary-source development
  found at edition 64 and the market reaction extending a second session.**
  NVIDIA's board accepted Jensen Huang's resignation as President, CEO and a
  board member effective 11 November 2026, announced via Form 8-K (accession
  0001045810-26-000082) on 12 November; CFO Colette Kress became interim CEO
  and director Harvey C. Jones became the company's first-ever independent
  Board Chair — all confirmed directly and independently corroborated across
  five top-tier wires at edition 63 (see that edition's own full account in
  the log below for the complete detail, including the press-reported
  extramarital-relationship context). **Edition 64 ran a direct SEC EDGAR
  check (CIK 0001045810) for any 8-K filed after 12 November and found
  none** — no severance disclosure, no permanent-CEO-search update, no board
  investigation findings have been filed as of edition 64's Sunday-evening
  cutoff. **The market reaction extended into a second session**: NVDA fell
  a further -2.01% to $162.85 on Friday 13 Nov (on top of Thursday's -4.34%),
  while the broader chip complex that had rallied Thursday on a rotation
  into Nvidia's rivals reversed sharply Friday on profit-taking — AMD -8.75%
  to $534.06, Broadcom -4.76% to $347.01, both with no company-specific news,
  confirmed via two independent sources (see the edition 64 log entry below
  for the full account and the sourcing lesson this produced). **Still
  open, exactly as at edition 63:** any severance disclosure, the
  permanent-CEO search's outcome or timeline, the board investigation's
  substantive findings, the reported shareholder class-action lawsuit, and
  the reported FBI/congressional investigation angles (all press-reported
  only, not primary-confirmed) — continue checking SEC EDGAR directly each
  edition. **NVIDIA's own Q3 FY2027 earnings, due Tuesday 17 November 2026
  after market close, is now the single most important near-term catalyst
  for this thread and for the chip complex generally** — this falls inside
  the edition covering Tuesday 17 Nov's session (expected edition 66 if no
  gaps), not edition 65.
- General principle for everything still live: do not assume a routine
  macro-calendar fact (meeting dates, symposium schedules, other central
  banks' policy rates, government funding status) from memory or from the
  prompt's own framing — verify it fresh from a primary source
  (federalreserve.gov, bankofengland.co.uk, boj.or.jp, kansascityfed.org,
  norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, rba.gov.au,
  ecb.europa.eu, bankofcanada.ca, whitehouse.gov, etc.) every edition, exactly
  like any other data point, until an entry below is marked SETTLED. These
  are the rates and dates that feed Section 3's policy-rate table, so the
  table is the natural place to land them. Per-bank status as of edition 64
  (none contradicted, none re-attempted unless noted — no fresh news touched
  any of them inside this edition's window):
  - **Reserve Bank of Australia:** current rate **4.85%**, hiked 25bp on
    Tuesday 3 November 2026 (6-3 split vote, its fifth hike of 2026) —
    SETTLED pending the RBA's own next decision, **7-8 December 2026**. Not
    re-attempted at edition 64.
  - **Bank of England:** rate **4.00%**, hiked 25bp on Thursday 5 November
    2026 (8-1 vote, Mann dissenting for +50bp) — SETTLED pending the next
    decision, **17 December 2026**. Not re-attempted at edition 64.
  - **European Central Bank:** rate complex (deposit facility 2.50%, main
    refi 2.65%, marginal lending 2.90%) **SETTLED**; next Governing Council
    meeting **16-17 December 2026**. Not re-attempted at edition 64.
  - **Bank of Japan:** current rate approx. 1.25%, SETTLED pending its own
    next meeting, **17-18 December 2026**. Not re-attempted at edition 64.
  - **Bank of Canada:** SETTLED. Current rate 2.50%, hiked 25bp 28 October
    2026. Next decision **9 December 2026** (same date as the Fed's). Not
    re-attempted at edition 64.
  - **Swiss National Bank:** current rate 0.00%, SETTLED. Next assessment
    **10 December 2026**. Not re-attempted at edition 64.
  - **Norges Bank:** current rate **4.50%** (hiked 25bp 24 Sept 2026),
    SETTLED; a forecast-free interim review on 5 November 2026 kept the rate
    unchanged, confirmed directly at edition 60. Next full decision remains
    **17 December 2026**. Not re-attempted at edition 64.
  - **Riksbank:** current rate **2.00%**, hiked 25bp on Wednesday 4 November
    2026, confirmed unanimous 5-0 via the bank's own primary minutes at
    edition 62 — SETTLED pending the next decision, **approx. 16 December
    2026**. Not re-attempted at edition 64.
  - **Banxico — the rate and vote remain primary-source confirmed; the
    next-decision date remains unresolved for a THIRD straight edition, and
    is now confirmed structurally absent rather than merely hard to find.**
    Banxico cut its overnight interbank rate 25bp, from 6.50% to 6.25%,
    decision dated 5 November, effective 6 November 2026, a 3-2 vote —
    primary-confirmed via Banxico's own 5 November press-release PDF at
    edition 62. **Edition 64 fetched Banxico's own forward-calendar page
    (`calendarioDifusion_es.jsp`) directly and it returned "No se
    encontraron publicaciones" (no publications found) for 2027** under
    "Anuncios de las decisiones de política monetaria" — a confirmed empty
    result, not just a dead link as found at edition 63. Extensive
    Spanish-language searches for an already-published 2027 calendar found
    nothing (a BBVA "Agenda Económica 2026" PDF only covers 2026 meetings).
    **Try a different angle at edition 65**: a named bank's own research-note
    forward calendar, or Banxico's own press-release archive for any
    announcement of a 2027 schedule, rather than repeating the same calendar-
    page fetch a fourth time.
  - **Government funding/shutdown status:** H.R. 6500 funds federal agencies
    through 11 December 2026, no shutdown in effect. **Re-confirmed again at
    edition 64** via whitehouse.gov (no contrary content found) and a direct
    check of the Continuing Appropriations Act 2027 / P.L. 119-103 deadline.
    Continue the standard re-check-every-edition discipline regardless.
- **NEW closed thread at edition 64 — October 2026 US PPI, a genuinely mixed
  print.** Released Friday 13 November 2026, 8:30am ET (BLS,
  bls.gov/news.release/ppi.htm): headline final demand **+0.3% m/m
  (seasonally adjusted) / +6.5% y/y (NSA)**; core (final demand less foods,
  energy, and trade services) **+0.5% m/m / +4.9% y/y**. Final demand goods
  +0.5% m/m; final demand services +0.2% m/m. Headline came in **cooler**
  than the approx. +0.4% m/m Dow Jones-survey consensus; core came in
  **hotter** than the approx. +0.3% m/m estimate — a split print that left
  rate-path odds essentially unmoved (see the rate-odds entry above). Unlike
  October CPI, which BLS could not give any year-over-year reading for due to
  the 2025 appropriations-lapse data gap, PPI's y/y comparison is intact.
  Next PPI release: 15 December 2026, 8:30am ET.
- **NEW closed thread at edition 61 — October 2026 US CPI, with a genuinely
  unusual wrinkle worth remembering for future months.** Released 8:30am ET
  Tuesday 10 November 2026 (BLS release USDL-26-1685): headline CPI-U **+0.4%
  m/m seasonally adjusted** (+0.2% unadjusted), core (ex food/energy) **+0.3%
  m/m seasonally adjusted**, the same pace as the prior two months. **BLS
  published NO year-over-year figures for either series** — it did not
  collect October 2025 survey data because of that year's lapse in
  appropriations, so no valid 12-month comparison exists for October 2026
  against it. Watch whether this recurs for November 2026 CPI (due roughly
  mid-December) and any other BLS series with an October-2025-vs-October-2026
  12-month-comparison dependency, rather than assuming it was a one-month
  quirk. (October's PPI, resolved above at edition 64, did NOT have this
  problem — its y/y comparison was intact — so the gap is CPI-specific, not a
  blanket BLS issue; worth testing again against any other October-2026 BLS
  series that still needs resolving.)
- **NEW closed thread at edition 62 — CoreWeave's (CRWV) Q3 2026 results,
  entirely unverified at edition 61's cutoff, are now fully resolved via the
  company's own 8-K.** Revenue $3.661bn (+168% y/y), beating CoreWeave's own
  $3.45-3.60bn guidance; GAAP net loss widened to $(709)m on net interest
  expense surging to $(846)m; adjusted EBITDA $2,256m (62% margin); FY2026
  revenue guidance raised to $13.0-13.3bn. Confirmed directly against SEC
  EDGAR (8-K, Exhibit 99.1, accession 0001769628-26-000461). The stock's
  Tuesday-night after-hours reaction is disclosed as genuinely disputed across
  vendors (approx. +2.4% to +7.9%); the confirmed Wednesday 11 Nov
  regular-session close ($60.77, +24.71%) is solid. CRWV pulled back -6.86%
  to $56.60 at edition 63 (apparent profit-taking after Wednesday's surge).
  Not re-attempted at edition 64. Do not re-derive the Q3 figures.
- **NEW closed thread at edition 62 — Skydance Corp (SKYD) and Paramount
  Skydance (PSKY) are the SAME legal entity.** A direct SEC EDGAR
  company-filing-history check (CIK 0002041610) shows the entity was named New
  Pluto Global, Inc., then Paramount Skydance Corp (through 2026-10-06), then
  renamed again to Skydance Corp — a single CIK's name/ticker history. Do not
  re-derive this; SKYD's specific daily driver claims still need their own
  verification.
- **SETTLED (historical) — Bank of England held at 3.75% on Thursday 17 Sept
  2026, a 6-3 vote.** Superseded by a subsequent decision: the MPC hiked 25bp
  to **4.00% on Thursday 5 November 2026** (8-1, Mann for 50bp) — see the
  dedicated per-bank bullet above for full detail.
- **SETTLED (the September decision only) — Bank of Japan hiked 25bp to
  approx. 1.25% on 18 September 2026** (effective 24 Sept), a 31-year high, a
  7-2 vote — closed thread. **The Bank's SUBSEQUENT 29-30 October 2026
  meeting HELD the rate at approx. 1.25%** (8-1 vote, dissenter Takata
  Hajime) — this is now resolved meeting history; the numeric rate is live
  again only pending BoJ's next meeting, confirmed for **17-18 December
  2026**.
- **SETTLED — the four-central-bank Thursday 24 September 2026 cluster,
  closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%; Riksbank
  held at 1.75% but signalled a greater chance of a Q4 hike (materialized at
  edition 57); Banxico held at 6.50% unanimously (since cut at edition 58);
  SNB held at 0% and raised its inflation forecasts.
- **SETTLED — the Reserve Bank of Australia's Tuesday 29 September 2026 and
  Tuesday 3 November 2026 decisions, both closed threads, do not re-open:**
  hiked 25bp to 4.60% (unanimous, fourth hike of 2026), then a further 25bp to
  4.85% (its fifth hike of 2026, a first-ever split 6-3 vote this cycle). The
  current numeric rate and next decision date (7-8 Dec 2026) are both SETTLED.
- **August 2026 PCE inflation — closed thread, resolved at edition 32:**
  headline +0.3% m/m/+3.4% y/y, core +0.2% m/m/+3.0% y/y.
- **September 2026 and October 2026 jobs reports — both closed threads, do not
  re-derive, but watch for revisions in later BLS releases:** September:
  nonfarm payrolls +29,000 (weakest of the cycle) vs. approx. 84,000-90,000
  consensus; unemployment 4.2%. October (resolved at edition 59): nonfarm
  payrolls **+165,000**, a 100,000 upside surprise against a FactSet median
  consensus of **+65,000**; unemployment held at **4.1%**; average hourly
  earnings **+0.4% m/m / +3.1% y/y**; August revised up 53,000, September
  revised up 31,000. This print was the proximate driver of edition 59's sharp
  hawkish rate-odds reversal, which continued extending through edition 63
  before leveling off at edition 64.
- **September 2026 and October 2026 ISM Services/Non-Manufacturing PMI — both
  closed threads:** September headline 54.9% (Prices Paid 74.0%, highest
  since July 2022). October headline **54.5%**, below the **54.8%**
  consensus, a third straight month without acceleration (resolved edition
  57). Sub-index detail remains an Annex B item.
- **September 2026 US CPI — closed thread as of edition 42:** headline **+0.6%
  m/m / +3.7% y/y**, core **+0.3% m/m / +2.6% y/y**, both above the approx.
  3.6%/2.5% consensus — the proximate trigger for edition 42's broad equity
  selloff. **October 2026's CPI is a separate, already-RESOLVED closed
  thread** — see the dedicated bullet above for the full account, including
  the missing-y/y wrinkle.
- **September 2026 US PPI — closed thread as of edition 43:** final demand
  **+1.3% m/m / +6.3% y/y** (NSA), the largest monthly gain since March 2022.
  **October 2026's PPI is now a separate, RESOLVED closed thread as of
  edition 64** — see the dedicated bullet above for the full account
  (headline cooler, core hotter than consensus).
- **September 2026 Import/Export Price Indexes and Industrial Production
  (G.17) — both closed threads as of edition 44:** import prices +1.1% m/m /
  +8.1% y/y, export prices +2.2% m/m / +11.6% y/y; industrial production +0.7%
  m/m / +2.2% y/y, capacity utilization 76.9%. The Fed flagged an annual
  benchmark revision to the G.17 series due 24 November 2026 — watch for a
  level reset around that date (likely inside edition 70-71's window), not a
  genuine month-over-month signal.
- **US Q3 2026 GDP (advance estimate) and September 2026 PCE/core PCE — both
  closed threads as of edition 53, released together Thursday 29 October
  2026:** real GDP **+3.4% annualized**; PCE headline **+0.5% m/m / +3.6%
  y/y**, core **+0.3% m/m / +3.1% y/y**. Next GDP release (2nd estimate +
  corporate profits): 25 November 2026.
- **University of Michigan October 2026 consumer sentiment — CLOSED thread as
  of edition 49:** preliminary 46.3 (five-month low); final 48.0 (vs.
  September's 48.1). Final sub-indices: current conditions 46.7, expectations
  48.8; year-ahead inflation expectations 4.7%, long-run 3.5%.
- **China September 2026 CPI/PPI and October 2026 PMI — both RESOLVED, closed
  threads:** CPI +0.9% y/y (+0.2% m/m), PPI +5.0% y/y; October manufacturing
  PMI 49.3 (down from 50.1), non-manufacturing PMI 49.7 (down from 50.2), both
  back below the 50 threshold.
- **China Q3 2026 GDP — RESOLVED at edition 45, closed thread:** Q3 alone
  +4.5% y/y, +1.2% q/q; first-three-quarters cumulative +4.6% y/y.
- **New Mexico v. Meta — the $25bn civil-penalty ruling (Judge Francis
  Mathew, Wed 21 Oct 2026) remains substantially clarified but Meta's formal
  notice of appeal is still unconfirmed for a NINETEENTH straight edition
  (47-64).** Meta owes **$25bn** in civil penalties — above the
  48-other-state $18bn settlement Meta already reached elsewhere, well below
  New Mexico's $35-40bn ask. This judgment is **distinct** from: (1) a
  separate, earlier New Mexico Unfair Practices Act matter (approx. $942m,
  Meta posted an $1.8bn bond, unopposed stay around 9 Oct 2026); (2) the March
  2026 child-safety jury verdict ($375m); (3) the August 2026 abatement ruling
  ($567m, under appeal); (4) Meta's own Q3 2026 earnings charge (a separate
  $9.89bn one-time charge tied to an August 2026, 52-state-AG teen-safety
  settlement that excludes New Mexico). Don't conflate any of these four. Not
  independently re-attempted at editions 55 through 64 (out of scope); no new
  development found or sought.
- **Calendar-awareness item: "equities-open, bonds-closed" US holidays need an
  explicit check every time they land in the window, not an assumption from
  memory.** Columbus Day (Mon 12 Oct 2026) and Veterans Day (Wed 11 Nov 2026,
  directly observed at edition 62) are both now resolved/closed history. **The
  only still-open calendar flag of this kind is Thanksgiving (26 Nov) plus
  the Friday half-day (27 Nov)** — see the Schedule section above. The DST
  transition (ended Sunday 1 November 2026) remains itself resolved/settled.
- **The vendor-retroactive-revision trap recurred AGAIN at edition 64, this
  time hitting WTI (a large upward restatement) and Henry Hub (a downward
  restatement), plus a minor gold move and a vendor-split on silver — now
  confirmed recurring at essentially every edition this report has checked
  for it, the established default expectation rather than an anomaly.**
  Edition 63 logged Thursday 12 Nov's bases (as then reported) as WTI approx.
  $86.53 (+2.53% session), Henry Hub $3.359 (Investing.com)/$3.362 (Yahoo),
  gold $3,884.67, silver $50.040. Edition 64's fresh re-fetch of those same
  Thursday figures instead found: **WTI $88.74 on both vendors** — a
  roughly $2.21 (2.6%) upward restatement; **Henry Hub $3.340 on both
  vendors** — a downward restatement of about $0.02 (0.6%) that also closed
  the two vendors onto the same figure; **gold $3,885.30 on both vendors** —
  a negligible $0.63 move; **silver vendor-split: Investing.com $50.065,
  Yahoo $49.97**, an approx. 19bp gap (Yahoo's restated figure is actually
  below the originally-published number). Brent, copper, DXY, EUR/USD,
  GBP/USD, USD/JPY and the Treasury par yields all showed **no revision** at
  edition 64. As before, none of these figures carries a flag for which was
  "right" at the time it was published — this is disclosed in Annex A as a
  vendor revision, not a reader-facing correction, since each edition's own
  published figure was not traceably wrong when checked at the time. Continue
  expecting this as the default case for oil/gas/metals at every edition.
- **Henry Hub: the cross-vendor base revision closed the gap again at edition
  64, exactly as it did at edition 63 — via joint revision, not organic
  convergence.** Both vendors moved to $3.340 for Thursday 12 Nov's base (see
  above); Friday 13 Nov's close was $3.230 on both vendors (-3.29% hand-
  computed), and the Sunday 15 Nov partial-reopen print was $3.167 (a further
  -1.95%). Still NGZ6 (December); no roll to NGF7 (January) yet as of Sunday
  15 Nov. Resume the every-edition reconciliation regardless of this clean
  read.
- **westmetall.com (LME copper) — stayed clean and uneventful at edition 64,
  continuing the root-cause resolution from edition 62.** Thursday 12 Nov's
  cash base ($13,712.00/t) carried NO revision this time; Friday 13 Nov's
  cash close was $13,610.00/t (-0.74% hand-computed), with the current-day
  3-month print at $13,545.00/t (per the site's permanent structural
  limitation — no historical 3-month field exists, only the current-day print
  is available). A COMEX cross-check (Yahoo Finance HG=F, converted to
  $/tonne) showed an approx. 1.5% COMEX-under-LME basis gap — a genuine
  cross-market spread, not a vendor data error.
- **New sourcing-mechanics trap logged at edition 50, relevant to any
  Monday-dated (or any day-after-a-non-trading-day) edition: Investing.com
  inserts an electronic Sunday-evening re-open print as its own row for every
  24-hour-traded instrument.** Directly relevant to edition 64 (a
  weekend-gap edition) and handled correctly: Sunday 15 Nov's partial-reopen
  rows for WTI, Brent, Henry Hub, gold and silver were fetched explicitly by
  date and reported as separate, clearly-labelled "Sunday reopen (partial
  session)" figures rather than being conflated with Friday 13 Nov's actual
  close. Keep applying this discipline on every post-weekend or post-gap
  edition.
- **The Kitco live-spot-vs-headline cross-check showed a partial change of
  failure mode at edition 64, after a fifth consecutive edition of total
  inaccessibility.** The live-quote page now loads and shows a genuine,
  timestamped live print (bid $3,869.70/ask $3,871.70, "last updated Nov 15,
  2026 8:25pm EST") — but its "Historical Performance" widget and
  date-picker-driven historical chart remain blank/non-extractable, a SIXTH
  straight edition of that specific sub-failure. The live print also
  diverged meaningfully from Investing.com's own Sunday-reopen gold figure
  and the two could not be reconciled — disclosed rather than resolved. Keep
  attempting it fresh every edition; the live-quote recovery suggests the
  page may be only partially restructured.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company, IPO'd 1 July 2026 at
  $29/share. Logged here so a future edition doesn't waste effort
  re-verifying the ticker's legitimacy if it moves sharply again. Not
  referenced at edition 64.
- **The "named secondary outlet's own claim can be flatly wrong" trap family
  gained an important new, inverse-direction instance at edition 64: this
  time it was a dedicated research pass's clean NEGATIVE finding that needed
  (and received) a direct follow-up, not a dramatic positive claim.** Edition
  64's equities research pass searched specifically for Friday 13 Nov
  single-stock movers and reported none beyond four names, explicitly
  flagging thin/unindexed aggregator coverage for that date. A direct
  coordinator follow-up — fetching AMD's and Broadcom's own price-history
  pages rather than running another news search — found two further large,
  genuinely newsworthy moves (AMD -8.75%, Broadcom -4.76%) that general web
  search had not yet surfaced for that specific date; both were independently
  cross-checked against a same-day quote on a secondary outlet (247wallst.com)
  that matched exactly. **The refined lesson: when a dedicated research pass
  reports a clean negative ("nothing else found") for a single-session
  window, a direct history-page fetch on names already known to be in play
  that week (here, the prior day's biggest rotation winners) is worth trying
  before accepting the negative** — this is the mirror image of the
  established "dramatic claim deserves thorough verification before
  accepting OR rejecting" discipline, applied to an absence rather than a
  presence. Prior instances in this family remain logged: JetBlue (edition
  50, magnitude), Carvana/Barron's (edition 52, direction/framing), Tesla and
  NU Holdings (edition 49, magnitude), Marvell/Lumentum and Barclays/PayPal
  (edition 53), a misdated Reuters-style squib plus a wrong-year Trefis list
  (edition 54), Brent crude's disclosed settle-to-settle-vs-"more than 7%"
  methodology discrepancy (edition 55), a claimed Oracle analyst-upgrade note
  (edition 56), three instances at edition 58 (a fabricated DraftKings AH
  figure, an unsupported Natera claim, an unsupported "biggest calls" list), a
  stale-date index-close republish at edition 59, a claimed International
  Money Express/Western Union tie to the Intermex deal's drop-dead date at
  edition 62 (excluded for lack of primary confirmation and a counterintuitive
  direction), Rocket Lab/Lucid premarket-snapshot-mistaken-for-close instances
  at edition 61, and five instances at edition 63 of reporting a verified
  price move with NO confirmed driver (Global Payments, Super Micro, YETI,
  Corteva's claimed MSCI tie, Strategy/MSTR's claimed MSCI tie) rather than
  repeating an unconfirmed claim.
- **The edition-49 "forward-looking calendar aggregator" trap (names falsely
  listed as past or future reporters when the actual date differs) remains
  closed as a general pattern.** Not independently re-tested at editions 61
  through 64 (no new instance found or needed); continue checking any
  carried-forward calendar assumption against its primary source before it
  becomes load-bearing.
- **A megacap multi-name earnings cluster producing genuinely uncorrelated
  reactions is a standing, repeated pattern — now at least SIXTEEN distinct
  instances through edition 64 (editions 44, 47, 48, 49 x2, 50, 52, 53 x3, 58,
  59, 60, 61, 63, 64).** Edition 64 added: Cisco's clean beat-and-raise drew
  only a muted -0.30% AH move Thursday night before falling a further -6.25%
  in Friday's regular session on sequentially flattish Q2 guidance, while
  Applied Materials beat on both lines yet sold off -2.74% with the CFO
  declining to give forward guidance, and Stantec's beat-and-raise drew a
  clean +14.06% rally the same session — three different reactions to three
  beats inside one session. Continue treating beat-and-raise (or a guidance
  cut) as having no *guaranteed* effect on the reaction without checking the
  actual outcome.
- **New production lesson from edition 53: CSS multi-column (`.cols3`/
  `.cols2`) pagination under Chromium print-to-PDF can plateau stubbornly on
  marginal content trims; edition 60 hit the most severe version of this
  plateau yet and found a clearer fix (documented under Production Notes
  below). Editions 61 through 64 all needed none of this** — all four
  converged cleanly to 4 pages with the forced break kept, no overflow, no
  stray break. Edition 64 specifically needed two renders (the first before
  a correction box and two extra movers rows were added, the second after)
  and both converged cleanly to 4 pages with no page-count change — a useful
  data point that a moderate mid-draft content addition does not reliably
  tip the page budget, so don't assume a content change requires a trim pass
  without actually re-rendering to check.
- **The VIX feed's two known bugs continue to toggle unpredictably — they
  RECURRED again at edition 64 after a five-edition clean streak.** Pattern
  to date: clean for four straight editions (55-58), recurred for one edition
  (59), clean again for five straight editions (60-64 minus the latest —
  correction: clean 60-63, recurred again at 64). Continue the
  manual-calculation discipline unconditionally regardless of how many
  bug-free editions precede the current one — edition 64's own VIX-complex
  figures were all computed by hand from raw levels, as always.
- **A markup-correctness self-check (`grep -n '</td><sup'`) caught three
  instances of an invalid-table-structure trap at edition 54 (documented
  under Production notes below), before rendering.** Editions 55 through 64
  all ran the same proactive check and found **ZERO instances for a TENTH
  consecutive edition** — worth continuing on every edition with a table that
  has an empty trailing cell or a cell containing only a citation.
- **The CFTC Asset-Manager-vs-Leveraged-Funds grouped-bar chart was reused for
  a fifth time (editions 34, 39, 44, 49, 54 — a clean Monday/weekend-window
  pattern) with the same figsize (9.8, 2.15), `h=0.32` bar offset and
  figure-level legend technique documented under Production Notes.** No
  edition since 54 has used it — no fresh CFTC data has fallen inside any
  window since, and edition 64's own check found the report covering
  Tuesday 10 November data **not yet posted** as of its Sunday-evening cutoff
  (cftc.gov's financial-futures page still showed positions as of 3 November).
  **The report is due later Monday 16 November 2026, now inside edition 65's
  own window** — check cftc.gov directly then, both for the report itself and
  for the chart opportunity.
- **A new Yahoo Finance data-quality issue was logged at edition 63, distinct
  from the long-tracked Investing.com displayed-%-vs-computed-% divergence
  below: Yahoo's own self-reported percentage-change fields
  (`regularMarketChangePercent`, `fulldayChangePercent` on its chart API) were
  found referencing a stale ~10-day-old baseline for every commodity/FX
  ticker checked at edition 63 (WTI, Brent, Henry Hub, gold, silver, DXY).**
  Not explicitly re-tested at edition 64 (the discipline of always computing %
  change by hand from two raw price levels made this moot in practice) —
  worth a direct re-test at a future edition to see if it has been fixed, but
  not urgent given the existing workaround is already standard practice.
- **The Investing.com displayed-%-vs-computed-% divergence, flagged as a new
  standing data-quality issue at edition 60, absent at edition 61, was NOT
  explicitly re-checked at either edition 62 or edition 63 — but WAS
  explicitly retested at edition 64 and found ABSENT.** Edition 64 compared
  Investing.com's own displayed % change against a hand computation from its
  own two raw price levels across nine commodity/FX series and eighteen
  total day-over-day comparisons (including the Sunday reopen prints) and
  found every single one matched to the nearest basis point. This issue has
  now toggled present (60), absent (61), unchecked (62-63), absent (64) — keep
  testing it directly every few editions rather than assuming either state.
- **A genuine cross-vendor DIRECTIONAL conflict on USD/JPY surfaced at edition
  64, a more serious instance of the FX cross-vendor gap than the
  magnitude-only disagreements seen before.** Investing.com's own series
  showed the yen strengthening on Friday 13 Nov (159.69, -0.11%), while
  Yahoo Finance's own series showed the yen weakening the same session
  (159.8750, +0.09%) — not just a different magnitude but the opposite sign.
  EUR/USD and GBP/USD showed the more familiar pattern (both vendors agree on
  direction, disagree on magnitude: EUR/USD -0.28% Investing vs. -0.41%
  Yahoo; GBP/USD -0.10% Investing vs. -0.35% Yahoo). Disclosed rather than
  resolved, as this report's convention requires when sources disagree and
  neither is clearly more authoritative for a specific FX cross; keep
  checking all three pairs against both vendors every edition regardless of
  outcome.

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
  **Editions 54 through 59 and 61 through 64 all converged cleanly within one
  or two renders** (54 and 59 after deleting the one forced break; 55-58 and
  61-64 all on the first or second render with the break retained — edition
  64 needed a second render only because of a genuine content addition
  mid-draft, not because of any overflow). **Edition 60 broke that quick-
  convergence streak** for a new reason (an Annex-C column-balance effect,
  see Production Notes), needing roughly eight iterations. Always check which
  situation you're in (stray break vs. genuine overflow vs. spillover that
  just needs the break deleted vs. a lonely trailing block pinned by a
  full-feeling preceding column box vs. a dense day that simply fits) before
  assuming any one fix is the answer.
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
  all values genuinely share one — and legitimate to additionally cite that
  same shared source inline (e.g. in the sentence introducing the movers
  table) purely so `check_refs.py` doesn't flag the Annex C entry as unused;
  edition 64 did this for its movers-chart price source. **Also watch for a
  stray bracket typed outside a `<sup>` tag entirely** — `check_refs.py` will
  not flag it since its regex only matches inside `sup class="ref"` tags, so
  a bare `[n]` slips through silently. Proofread citation-heavy sentences
  visually, not just via the script, when a sentence carries two or more
  consecutive citations. A related trap, worth naming explicitly: placeholder
  ref text (e.g. `[note1]`) typed during drafting and never swapped for a
  real number. `check_refs.py`'s regex requires `\d+` inside the brackets, so
  a non-numeric placeholder simply won't match either the inline or Annex-B
  regex — it won't show up as "missing" or "unused," it just silently
  doesn't count. **Never use a letter suffix to disambiguate a citation —
  always mint a new integer.** Annex C numbers do not need to be contiguous,
  only matched 1:1 against inline citations — deleting an unused reserved
  number and leaving a gap is completely fine and simpler than renumbering
  everything after it. **Reusing the same Annex C number for multiple
  movers/figures citing the same outlet/method is fine and recommended** —
  `check_refs.py` only checks presence/absence, not uniqueness of use.
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
  (what could not be verified) → Annex C (sources) → Method note. **Do not
  duplicate the day-ahead calendar as both a prose paragraph (e.g. at the end
  of Section 3) and the Section 6 table — Section 6's table is the one and
  only place the day-ahead calendar belongs.**
- **The disclosure box is now a correction box — new at edition 49, by
  request.** Assumptions and status live in **Annex A**. What stays on page
  1 is **corrections only**: a figure published in an earlier edition that
  turned out to be wrong, or a premise-level correction. Terse — what was
  published, what it should have been — with the full record in Annex A if
  it needs more than a line. **Omit the box entirely on an edition that
  corrects nothing**, which will be most of them. **Editions 54 through 63
  all omitted the box** — in each case nothing published in a prior edition
  was found to be wrong. **Edition 64 broke that streak**, using the box to
  correct edition 63's own date-line weekday error (see the dedicated
  header-details entry near the top of this spec) — a premise-level
  correction about the document itself rather than a market figure, but
  still exactly the kind of thing the box exists for. (Edition 61
  specifically remains an example of what does NOT need the box: the Nvidia
  board-investigation story, excluded as uncorroborated at edition 60, was
  NOT a wrong publication to correct — edition 60's own published text never
  claimed it was false, only that it couldn't yet be confirmed. Edition 63
  similarly: Huang's resignation is a new development, not a contradiction of
  edition 61/62's reporting that the board then retained confidence in him.
  A genuine published-figure or published-premise correction gets the box;
  a dramatic new development or a prior "unconfirmed" caveat being resolved
  either way does not.)
- **All sector and ETF material belongs to Section 1 — by request since
  edition 49.** Section 1 keeps its snap-grid tiles and recap paragraph and
  gains the sector-ETF chart plus the narration of how each sector did in
  the session. **Section 2 is purely single-stock**: movers chart, movers
  table, earnings, guidance, analyst actions. The test is simple — if a
  sentence is about a sector rather than about a named company, it goes in
  Section 1.
- **Section 3 carries a central-bank policy-rate table.** Columns: **Central
  bank | Policy rate | Last change | Next decision**. The Fed goes first as
  the anchor to compare against, then whichever of the BoE, BoJ, ECB, SNB,
  Norges Bank, Riksbank, RBA, BoC and Banxico the window actually touches —
  eight to ten rows is the working range. A bank whose current rate could
  not be verified still gets its row, with that cell marked unavailable and
  a matching Annex B entry. **Editions 54 through 64 have all run the same
  full 10-row table** (Fed, BoJ, BoE, ECB, BoC, RBA, SNB, Norges Bank,
  Riksbank, Banxico). Banxico's rate and vote are primary-source confirmed;
  its next-decision date remains the table's one unavailable cell, now for a
  third straight edition, and is now confirmed structurally absent (the
  bank's own calendar page returns no 2027 entries) rather than merely
  unreachable. Follow the usual table convention — plain `<tr>` header rows,
  no `<thead>`.
- **Charts: two fixed, a third only when earned — changed at edition 49.**
  The **sector-ETF performance chart always goes in Section 1**, beside the
  sector narration it illustrates, and the **single-stock movers bar always
  goes in Section 2**, with the names. Neither may duplicate a table.
  A **third chart is allowed only when positioning or volatility is
  genuinely the day's dominant story** — not merely present, and never to
  fill a short page — and it goes in the section it belongs to: CFTC
  asset-manager vs. leveraged-funds positioning or a VIX term structure in
  Section 5, an implied-vs-realized earnings bar in Section 2. **Editions 61
  through 64 did not use a third chart** — at edition 63 the VIX complex
  spiked sharply (+6.92%) and was genuinely newsworthy, but judged secondary
  to the NVIDIA-leadership dominant story and covered fully in prose instead;
  edition 64's VIX move (+3.21%) was more modest and likewise covered in
  prose. **Next CFTC report due Monday 16 November 2026** (now edition 65's
  own window, not yet posted as of edition 64's cutoff), covering Tuesday 10
  November data — check cftc.gov directly at edition 65.
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
  editions 56 through 64 (edition 63's reported approx. $500bn NVDA
  weekly-value figure is NBC's own reported aggregate, cited as such, not
  independently recomputed by this report).
- Where sources disagree, use the more authoritative one **and** disclose
  the disagreement. AP's "How major US stock indexes fared" and the Reuters
  market wrap are normally the most reliable for index closes — but check
  they're actually indexed for the target date before relying on them. The
  dual WTOP.com/lanacion.com.ar AP-wire-mirror approach remains the
  established first-choice workaround when apnews.com/Reuters are blocked
  directly — **now ELEVEN consecutive successes** (edition 64 used both
  mirrors together, finding identical figures, cross-checked exactly against
  Yahoo Finance and SPY's own price history). apnews.com/Reuters were not
  directly re-attempted at edition 64 either — keep re-attempting the primary
  wires every few editions to check whether the block has lifted.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Always check a dated article's own claimed magnitude AND
  direction against the underlying price-history table or primary filing,
  not just its date, before repeating it** — this trap has now hit
  magnitude, direction/framing, claimed drivers that don't hold up, a
  claimed analyst action that appears outright fabricated, the claimed
  DATE/YEAR itself, the claimed DAY-OF-WEEK NAME attached to a correct date
  (edition 63, caught and corrected at edition 64 — see the dedicated
  header-details entry), a disclosed cross-source percentage-methodology
  discrepancy, a figure with no corroborating primary filing at all, a
  wholesale stale-date republish, and a dramatic claim that one research
  pass reported as apparently true before a direct follow-up found no
  support (edition 60) — followed by the mirror-image lesson that the SAME
  dramatic claim, re-checked with fuller search effort, turned out to be
  true after all (edition 61), and further refined at edition 64 by the
  inverse case: a research pass's clean NEGATIVE result for single-stock
  movers was overturned by a direct coordinator follow-up fetch that found
  two large, genuine moves general search hadn't yet surfaced. Treat ANY
  surprising secondary claim (price move, driver, analyst action, date, or
  computed percentage) — AND any surprisingly clean negative result for a
  single-session search — as needing a genuine, thorough verification
  attempt before either accepting or rejecting it.
- Run a dedicated verification pass on any figure two research passes
  disagree on, or any single surprising/highly-consequential finding, before
  publishing — cheap, and has caught real errors before. **Edition 64
  exercised this discipline on an absence rather than a presence**: when the
  equities research pass reported no further Friday 13 Nov movers beyond
  four names, the coordinator directly fetched AMD's and Broadcom's own
  price-history pages (names already known to be volatile that week) rather
  than accepting the negative, and found two large, genuine, well-
  corroborated moves (-8.75% and -4.76%) that general web search had not yet
  surfaced for that date. Cross-checked against an independently-reported
  same-day quote (247wallst.com) before publishing. This is the clearest
  reminder yet that a dedicated pass's clean negative for a single-session
  window deserves the same direct-fetch scrutiny as a dramatic positive
  claim, not an automatic pass.
- **Premarket is not the close, and the close is not the after-hours
  earnings reaction — and an after-hours reaction does not necessarily hold
  into the next regular session, uniformly or at all. A strong beat-and-raise
  does not guarantee a positive reaction even within the SAME session —
  though it does not guarantee a negative one either.** Reinforced at
  essentially every edition since 44, most recently at edition 64 (Cisco's
  clean beat-and-raise drew a muted -0.30% AH move Thursday night before
  falling a further -6.25% in Friday's regular session; Applied Materials
  beat on both lines yet sold off -2.74%; Stantec's beat-and-raise drew a
  clean +14.06% rally the same session — three different outcomes from
  three beats). Always fetch the verified close, the after-hours reaction,
  AND (when the window allows) the next regular session's close as three
  separate, clearly labelled figures. A premarket-only or
  regular-session-only figure that predates a same-evening earnings release
  should be labelled as such rather than implied to be a reaction to it.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent, and
  gained a more serious variant at edition 64: a genuine DIRECTIONAL
  cross-vendor conflict on USD/JPY (not just magnitude).** DXY's own
  cross-vendor gap closed to 0bp at edition 64 (from approx. 7bp Thursday),
  while USD/JPY's Friday move showed Investing.com and Yahoo Finance
  disagreeing on the sign of the yen's move, not just its size; EUR/USD and
  GBP/USD showed the more familiar magnitude-only disagreement. Keep
  disclosing the DXY-vs-FX-crosses comparison, and each individual pair's
  own cross-vendor agreement/disagreement, every edition regardless of which
  way it goes.
- **The Kitco live-spot-vs-headline cross-check showed a partial recovery at
  edition 64 (the live-quote page now loads) but its historical-performance
  table remains broken for a sixth straight edition** — see the dedicated
  Standing Facts entry above.
- **GBP/USD, EUR/USD and USD/JPY reconciled with real, disclosed cross-vendor
  disagreement at edition 64** — a step up from edition 63's essentially
  clean reconciliation. See the dedicated Standing Facts entry above for the
  full detail; in short, EUR/USD and GBP/USD agreed on direction but
  disagreed on magnitude across Investing.com and Yahoo, while USD/JPY
  disagreed on direction itself.
- **The 2-year Treasury yield conflict from edition 36 remains resolved, and
  the every-edition reconciliation continued cleanly at edition 64**: Friday
  13 Nov's official par-yield print (home.treasury.gov) showed 2-year 4.88%
  (+2bp), 10-year 5.15% (+5bp), 30-year 5.47% (+4bp) vs. Thursday's prior
  print, with no cross-source conflict found — a further, smaller extension
  of the yield backup that began on Thursday's post-Veterans-Day reopening.
- **The Investing.com displayed-%-vs-computed-% divergence, flagged as a new
  standing data-quality issue at edition 60, absent at edition 61, unchecked
  at editions 62-63, was explicitly retested at edition 64 across nine
  series and eighteen comparisons and found absent.** See the dedicated
  Standing Facts entry above. **Separately, the distinct Yahoo Finance
  stale-%-field issue logged at edition 63 was not explicitly retested at
  edition 64** (bypassed in practice by always computing % change by hand) —
  worth a direct look at a future edition.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 64 have all run clean (or
  clean after quick fixes) — **edition 64 needed one quick fix** (three
  newly-added Annex C sources were initially uncited inline; fixed by adding
  inline citations rather than deleting the entries, and one Annex C entry
  was reassigned from an unrelated citation to the correct one for the
  Banxico table row it actually supported).
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 64 have all rendered with zero stray tildes on the
  first draft, bar editions 56 and 57 which each needed one fix.**
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39, 44, 49 and 54 have
  all resolved this cleanly for CFTC CoT. Not applicable at editions 55
  through 64 (no fresh CFTC data triggered the chart in any of those
  windows). The next report (due Mon 16 Nov, covering Tue 10 Nov data) falls
  inside edition 65's plausible window.
- **The diffuse-overflow lesson from editions 44-45 and the duplicated-
  content lesson from edition 47 are both still worth checking first on any
  overflow** — but edition 53 showed overflow can also be genuinely dense
  content requiring real trimming, edition 54-58 showed the opposite, and
  edition 60 showed a third distinct cause (an Annex-C column-balance
  effect). **Editions 61 through 64 all needed no overflow fix at all** —
  each render (edition 64 needed two, for content-addition reasons, not
  overflow) converged cleanly. Always check which situation you're in before
  assuming a particular fix is the answer.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — **specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation.** No capping
  has been needed in any edition since 45. Edition 64's movers chart (6
  categories, STN +14.06% largest, AMD -8.75% second largest) had a ratio of
  approx. 1.61x; used `pad_frac=0.25` with figsize (9.8, 1.65), rendered
  cleanly. `pad_frac=0.30` for the 11-category sector panel has now rendered
  cleanly across nineteen editions (45-50, 52-64).

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`, under the `quotes/` path
  specifically — `charts/_VIX.json` returns 403, `quotes/_VIX.json` works).
  **Editions 28 through 64 have all got a fresh, same-day-timestamped
  sweep** — thirty-seven consecutive fresh sweeps now. **The feed's two
  known bugs (a duplicated `prev_day_close`, and a `price_change_percent`
  that divides by current price instead of prior close) toggle
  unpredictably:** present at edition 54, absent 55-58, present at 59,
  absent 60-63 (a four-edition clean streak, not five as previously logged —
  correcting a minor prior miscount), **present again at edition 64** —
  always compute day-over-day % change manually regardless of how many
  consecutive bug-free reads preceded the current one. **Edition 64's own
  session:** VIX +3.21% to 19.30, VIX9D +1.77% to 17.82, VIX3M +2.79% to
  20.62, VIX6M +1.47% to 22.03, VVIX +4.98% to 101.53, SKEW -2.01% to 147.14
  (last_trade_time 16:15:01 ET for the first five, 17:00:47 ET for SKEW,
  again lagging). Term structure held Thursday's shape: VIX9D below spot
  VIX, with ascending contango from spot through VIX3M/VIX6M — a rise
  concentrated in at-the-money/near-term vol rather than tail-risk demand
  (SKEW actually eased).
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 64 fetched all 11 directly again**
  (Consumer Staples +1.42% the clear leader; Technology -2.01% the sole
  clear laggard, driven by the chip-complex reversal; 7 of 11 closed higher,
  a sharp improvement from Thursday's 1-of-11) — continue this
  direct-fetch-by-default method. A secondary cross-check (MarketWatch/WSJ)
  was not attempted at edition 64 either — a fifth straight edition
  single-sourced; try the cross-check again at edition 65.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (0 of 11 at edition 58; 3 of 11
  at edition 59; 11 of 11 at edition 60; 6 of 11 at edition 61; 10 of 11 at
  edition 62; 1 of 11 at edition 63; **7 of 11 at edition 64**) — no
  competing secondary-aggregator breadth figure was checked at edition 64
  either.
- **Dealer gamma:** zerogex.io hit a **TWENTY-FIFTH consecutive edition of
  failure at edition 64** (all widgets still show placeholder dashes with no
  timestamped data). SpotGamma logged a **NINETEENTH straight failure at
  edition 64** (resolves to a marketing/paywall landing page with teaser
  headlines only — edition 64's teasers referenced a post-selloff "vanna
  rally," NVDA earnings, November OPEX and "record OPEX put positioning,"
  but the underlying GEX/strike data sat behind a login and was not
  retrievable; not cited). Both sources remain fully unusable for actual
  figures.
- **Official CME FedWatch probabilities:** the page blocks fetching
  (edition 64's direct attempt again returned a connection failure/timeout, a
  **TWENTY-FOURTH** consecutive failure, 41-64) — use secondary citations
  (Polymarket, Kalshi, Reuters/other economist polls, desk notes) and give a
  range rather than a single invented number. **Polymarket direct, tried via
  its Gamma API (`gamma-api.polymarket.com`) rather than a plain site visit,
  succeeded again at edition 64 — an ELEVENTH consecutive success** — this
  remains the preferred first approach. **Kalshi's official trading API
  (`api.elections.kalshi.com/trade-api/v2`) worked again at edition 64, a
  SECOND consecutive success** after resolving a 26-edition failure streak
  at edition 63 — this specific endpoint, not the kalshi.com web front end
  (still HTTP 429), remains the recommended first approach for Kalshi.
  **DeFi Rate's blended aggregator could NOT be freshly refreshed at edition
  64 either** (still only a stale late-October snapshot) — a second straight
  edition of this specific failure; try again at edition 65.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **westmetall.com (LME copper): the cash
  series stayed clean at edition 64** (Friday $13,610.00/t vs. Thursday's
  $13,712.00/t, no revision this time), **and the 3-month series' long-
  standing "query-parameter problem" remains resolved at the root (edition
  62)** — simply report the current-day 3-month print going forward
  (edition 64's: $13,545.00/t).
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **posted a fresh Friday 13 Nov print at
  edition 64, continuing the clean streak resumed at edition 63 after the
  Veterans Day closure** — 2-yr 4.88% (+2bp), 10-yr 5.15% (+5bp), 30-yr
  5.47% (+4bp) vs. Thursday's prior print, with no cross-source conflict
  found. Continue scoping the TextView URL to the specific month
  (`field_tdr_date_value_month=202611`-style parameter) rather than the
  full year.
- **CFTC CoT:** publishes with the prior Tuesday's data — always state the
  lag explicitly. `financial_lf.htm` works well for equity index futures
  (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). **The report covering Tuesday 10 November data had NOT yet
  been posted as of edition 64's Sunday-evening cutoff** — cftc.gov's
  financial-futures page still showed positions as of 3 November. It is due
  later **Monday 16 November 2026**, now inside **edition 65's own window** —
  check cftc.gov directly then.
- **GBP/USD, EUR/USD, USD/JPY clean close:** reconciled with real, disclosed
  cross-vendor disagreement at edition 64 (see the dedicated Standing Facts
  and Hard Rules entries above for the full detail) — EUR/USD 1.1023
  (Investing)/1.1050 (Yahoo), GBP/USD 1.3217 (Investing)/1.3231 (Yahoo),
  USD/JPY 159.69 (Investing)/159.8750 (Yahoo, a genuine directional
  conflict). **DXY's own cross-vendor gap closed to 0bp at edition 64**, from
  approx. 7bp Thursday.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot cross-check showed a partial recovery at edition 64** (the
  live-quote page now loads with a genuine timestamp) **but its historical-
  performance table remains broken for a sixth straight edition** — see the
  dedicated Standing Facts and Hard Rules entries above. **A fresh vendor-
  retroactive-revision instance hit gold/silver's Thursday base again this
  edition** (gold $3,884.67→$3,885.30, negligible; silver vendor-split,
  Investing $50.065 vs. Yahoo $49.97 — see the dedicated Standing Facts
  entry); Friday 13 Nov futures figures: gold $3,886.30 (+0.03%), silver
  $49.12 (Investing, -1.89%)/$49.03 (Yahoo, -1.88%).
- **China CPI/PPI (monthly), China Q3 GDP, US GDP/PCE/import-export
  prices/industrial production, University of Michigan October consumer
  sentiment, China's October PMI and October ISM Services PMI:** all closed
  threads — see Standing Facts above. **October US CPI** is a closed thread
  as of edition 61 (including the missing-y/y wrinkle). **October US PPI is
  now also a closed thread as of edition 64** — see the dedicated Standing
  Facts entry (headline cooler, core hotter than consensus; y/y comparison
  intact, unlike CPI's).
- **Henry Hub natural gas:** the front-month-contract-identity question
  remains resolved (NGZ6/December, no roll to NGF7/January yet as of 15
  Nov). **The base-price reliability problem — this report's historically
  worst-performing data-quality issue — stayed closed at edition 64** via
  another joint cross-vendor revision of the Thursday base (see the
  dedicated Standing Facts entry); continue the every-edition two-source
  reconciliation discipline regardless, since this has toggled open/closed
  before.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. CoreWeave's Q3 2026 results and
  regular-session reaction are fully resolved (edition 62); not re-attempted
  at edition 64.
- **Weekend equities catalyst: 13F filings.** The Q3 2026 deadline is
  confirmed **Monday 16 November 2026** (45 days after the 30 Sept
  quarter-end, rolled from the Saturday 14 Nov statutory date). This
  coincides with the CFTC CoT report date (also Monday 16 Nov) — both land
  inside edition 65's own window; check both directly then.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22, not attempted
  again since). Revisit only if a future edition has spare research
  bandwidth on an FOMC day specifically — not relevant to most editions.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully at
  editions 39, 44-49, 54 and 59 (the Friday 6 Nov report, covering Tuesday 3
  Nov data: ES OI 1,986,532; NQ OI 292,587; RTY OI 449,399). No new report
  fell inside edition 64's window either (see the CFTC CoT entry above).
  Repeat the three-instrument fetch at edition 65, watching for the
  micro-vs-full-size naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Editions 58 through
  63 all found zero verifiable analyst actions; **edition 64 extends this to
  a SEVENTH consecutive edition with zero verifiable analyst actions.** Watch
  each edition independently rather than assuming a trend, but this is now a
  seven-edition pattern.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance — and a research pass's clean negative result needs the
  same scrutiny, per edition 64's new inverse-direction lesson.** This
  discipline has now caught numerous fabrications and errors (full list in
  the Standing Facts "named secondary outlet" entry above), gained its most
  important nuance yet at edition 61 (a previously-excluded claim turning
  out to be TRUE on fuller re-verification), caught five more clean
  exclusions at edition 63, and at edition 64 caught the opposite failure
  mode — a pass's reported absence of further movers was overturned by a
  direct coordinator fetch that found two large, genuine moves (AMD, AVGO).
  Every reported single-stock mover at edition 64 (Stantec, AMD, Cisco,
  Broadcom, Applied Materials, Nvidia) was individually verified against
  either a primary SEC filing (where tied to earnings) or a two-source price-
  history fetch plus an independent same-day quote (AMD, AVGO) — continue
  this direct-verification discipline, including the direct-fetch follow-up
  on a clean negative, on every edition.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted since (out of scope each time); try an alternate DOL
  page or a secondary economic-calendar aggregator for the consensus figure
  when next relevant.
- **federalregister.gov's direct search interface remains blocked** (a prior
  search attempt 302-redirected to `unblock.federalregister.gov`, an
  apparent bot/rate-limit gate, first logged at edition 48) — not
  independently re-tested recently (the developer API route makes the
  search UI unnecessary). govinfo.gov continues to be a known working
  alternative route for at least some Federal Register content. **The
  Federal Register's own developer API (`federalregister.gov/api/v1`) scored
  a FOURTH consecutive success at edition 64**: used to re-confirm Doc.
  2026-22925's own citation (91 FR 72610, pinning the exact 9 Jan 2027
  deadline) and to run another clean, negative sweep for anything addressing
  the broader reciprocal-tariff truce. This API remains the clearly-
  established first approach whenever the search UI is blocked.
- **SEC EDGAR's `cgi-bin/browse-edgar` company-search page (filtered by CIK
  and form type 8-K) is a highly reliable, fast way to confirm both WHETHER
  a company has reported on a given date and to find the accession number
  for the underlying exhibit.** **Edition 64 used it again for Stantec (Form
  6-K), Cisco and Applied Materials (Form 8-K), and NVIDIA** (confirming
  directly that no new 8-K had been filed after 12 November) — reinforcing
  that this is the default first tool for confirming any earnings or
  governance filing, and for confirming a clean negative just as reliably as
  a positive.
- **ECB's current policy rate: SETTLED since edition 55** (unchanged through
  the 28-29 October 2026 meeting: deposit facility 2.50%, main refi 2.65%,
  marginal lending 2.90%); not re-attempted at editions 56 through 64 (no
  fetch needed). It reopens on contradiction, the next Governing Council
  decision, or the monthly audit. The Council's own next-meeting date is
  SETTLED at 16-17 December 2026.
- **NFIB Small Business Optimism Index:** nfib.com returned HTTP 403 at
  direct fetch at edition 62; Trading Economics worked as a fallback,
  carrying the October reading (97.8, down 0.1pt from September). Not
  re-attempted at edition 63 or 64 (no new monthly release inside either
  window); continue using Trading Economics as the default fallback when
  nfib.com blocks direct access.
- **Banxico's next policy-decision date** remains the one open Banxico gap,
  now for a third straight edition and now confirmed structurally absent:
  edition 64 fetched Banxico's own calendar page directly and it returned
  "No se encontraron publicaciones" for 2027. Try a different angle at
  edition 65 — a named bank's own published forward calendar, or Banxico's
  press-release archive for a 2027-schedule announcement — rather than
  repeating the same calendar-page fetch again.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel —
  confirmed clean again at edition 64 (twenty-five editions total: 37-43,
  45-50, 52-64). For charts with fewer categories, scale the height down:
  roughly `(9.8, 1.65-2.05)` for 3-9 categories. **Edition 64 used `(9.8,
  1.65)` for a 6-category movers chart with `pad_frac=0.25`**, rendering
  cleanly across a -8.75% to +14.06% range (ratio approx. 1.61x). **Always
  render and visually inspect (via the Read tool) the actual PNG at or near
  full resolution before embedding it**, regardless of what a past edition's
  success might suggest. **Default to pad_frac=0.30 from the start for an
  11-category sector-ETF panel** — now confirmed across nineteen straight
  small-magnitude 11-category panels (45-50, 52-64). For any movers chart
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
  threshold, including edition 62's approx. 1.92x, edition 63's approx.
  2.02x, and edition 64's approx. 1.61x) — reinforcing that the trigger is
  the ratio to the next-largest bar, not the largest bar's absolute size.
- **A grouped (two-series) horizontal bar chart — needed for the CFTC
  Asset-Manager-vs-Leveraged-Funds positioning chart — requires custom chart
  code, not the standard single-series `barh()` helper used for the
  movers/sector charts** (first built at edition 44, reused successfully at
  editions 49 and 54; not needed since). The standard helper only plots one
  value per category; the CFTC chart needs two bars (Asset Manager,
  Leveraged Funds) per category (ES/NQ/RTY), offset vertically by a fixed
  height fraction (`h=0.32` worked cleanly at edition 54) around each
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
  `@page` block is the pattern that has worked reliably — edition 64 used
  this exact pattern again with no issue, across two renders.
- **At most ONE forced `page-break-before` in the whole document:
  immediately before Annex A — and on a spillover edition, none at all.**
  Let sections 1-6 flow naturally; never add a break between them. The rule:
    - Sections 1-6 end on page 3 (the common case) → keep the break. The
      annex opens a clean page 4, exactly as before. **Editions 61 through 64
      were all this case**, each converging on the first or second render
      (edition 64's second render was for content-addition reasons, not
      overflow).
    - Sections 1-6 spill onto page 4 → **delete the `pagebreak` div and
      re-render**, so the annex follows the spillover down page 4 instead of
      starting a fifth page.
    - Still five (or more) pages with the break gone → now trim, in this
      order: sector table rows with no news in the window, the third chart
      if there is one, then prose — **but if the specific symptom is a tiny
      trailing block (e.g. just the Method note, or one lonely Annex C
      entry) alone on an otherwise-blank extra page, check FIRST whether the
      immediately-preceding multi-column block (`.cols2`/`.cols3`) is itself
      already filling almost the entire remaining page, per the edition-60
      lesson below, before assuming more prose-trimming earlier in the
      document will help** — it usually won't.
  Note on the `grep -c 'pagebreak'` self-check: the CSS baseline defines a
  `.pagebreak` class rule AND the body uses one `<div class="pagebreak">` —
  a literal `grep -c 'pagebreak'` therefore normally returns **2** on a
  correctly-built edition (one CSS rule line, one div usage line), not 1.
  The actual check that matters is `grep -c 'class="pagebreak"'` (counts
  only div usages), which should be 1, or 0 on a spillover edition, never 2.
  **Editions 61 through 64 all confirmed 1**, the common case.
- **MAJOR LESSON from edition 60, still the right reference for any future
  trailing-block-stranded-alone symptom: a CSS multi-column (`.cols2`/
  `.cols3`) block, laid out with the default `column-fill: balance` inside a
  Chromium-paginated print context, will often stretch to use nearly ALL of
  the remaining space on the current page — right up to the bottom margin —
  regardless of how little content it actually contains, as long as its
  natural (unconstrained) height is somewhere in the neighborhood of that
  remaining space.** This produces a specific, now-recognizable symptom: a
  small trailing element immediately after the multi-column block gets
  pushed onto its own near-blank extra page, and trimming the PROSE THAT
  PRECEDES the multi-column block has little or no visible effect on this.
  **What actually fixes it: trimming the multi-column block's OWN content**
  — shortening individual Annex C citations, merging shared-method
  citations into one entry, cutting filler words. **A `column-fill: auto`
  experiment was tried at edition 60 and made things WORSE, not better** —
  it produced a more lopsided distribution whose tallest column was taller
  than the balanced version's had been. It was reverted; `column-fill`'s
  default (`balance`) remains the right choice. Not needed at editions 61
  through 64 (all four were clean convergences).
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix.
- **A markup-correctness trap, logged at edition 47: a `<sup class="ref">`
  citation tag placed immediately after a table row's last `</td>` but still
  inside the `<tr>` (i.e. not nested inside any `<td>`) is invalid table
  structure.** `check_refs.py` will NOT catch this. **Always nest every
  `<sup class="ref">` tag inside a `<td>...</td>` pair, never as a sibling of
  one inside a `<tr>`** — grep for `</td><sup` as a quick self-check if a
  table was built with a lot of copy-paste. **Editions 55 through 64 all ran
  the same proactive grep and found zero instances, a TENTH consecutive
  clean sweep.** Run the grep on every edition with such a table, not just
  when troubleshooting a layout problem.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count
  alone. **Edition 64 needed two renders** (the first before a correction
  box and two additional movers rows were added mid-draft, the second
  after) — both were 4 pages and all four page images were read and
  confirmed clean both times, a useful reminder that a moderate content
  addition partway through drafting does not reliably change the page
  count, so re-render and re-check rather than assuming either outcome.
  Edition 64's final source count (20) sits in the normal range for a
  single-session, moderately dense window.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across many editions'
genuinely different content volumes, including editions 53's through 64's.
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
  runs short — editions 44 through 64 have all folded commodities, FX and
  Treasuries into ONE combined table (10-17 rows; edition 62 used 14,
  edition 63 used 13, edition 64 used 15) as the PRIMARY commodities table
  rather than padding, now the standing default.
  **Always re-render immediately after adding (or removing) any content to
  confirm the page count — and if a change to Annex A/B text doesn't move
  the page split at all, suspect the Annex C column-balance effect above
  before assuming the edit silently failed to save.**

**Chart selection guidance.** Placement is not editorial for the first two
charts:

- **Sector-ETF performance chart → Section 1 (Market recap), every
  edition.** Same-day closes by default; a grouped day-over-day bar instead
  on a multi-session or weekend window, or on a genuine multi-sector
  broadening selloff across consecutive sessions. **Editions 61 through 64
  all used a single-day bar** (each window held only one NYSE session, even
  edition 64's weekend-gap window, since the weekend itself has no equities
  session to group against).
- **Single-stock movers bar → Section 2 (Equities), every edition.**
- **A third chart only when positioning or volatility is genuinely the
  day's dominant story**, never to fill a page, placed in the section it
  belongs to:
  - Fresh CFTC CoT data → the ES/NQ/RTY asset-manager-vs-leveraged-funds
    positioning chart, normalized as % of open interest, built with the
    grouped-bar technique documented under Production notes, in **Section
    5**. Editions 24, 34, 39, 44, 49 and 54 have all placed it there; none
    of editions 55 through 64 had fresh data available inside their own
    windows. The next opportunity (the Monday 16 Nov report) falls inside
    edition 65's plausible window.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully. Not used at editions 55
    through 64.
  - A holiday-window preview edition with no fresher data → VIX futures
    term structure with event annotations, in **Section 5**. Not used at
    editions 55 through 64 — at edition 63 the VIX complex spiked sharply
    (+6.92%) and was genuinely newsworthy but judged secondary to the
    NVIDIA-leadership dominant story; edition 64's own VIX move (+3.21%) was
    more modest and likewise handled fully in prose.

**Edition 65 (expected to cover Monday 16 November 2026, assuming no gap —
a normal full session, no holiday).** Verify directly rather than assuming:
- **The CFTC Commitment of Traders report** (covering Tuesday 10 November
  data) and **the Q3 2026 13F filing deadline** — both due Monday 16 Nov,
  not yet posted/passed as of edition 64's cutoff. Check cftc.gov directly
  for the CoT report (and the fresh positioning-chart opportunity it
  brings); check for any notable 13F-driven market chatter.
- **Whether December FOMC hike odds (approx. 86-88% as of edition 64,
  essentially flat since edition 63) continue to hold, firm, or ease** on
  Monday's fresh session — pull Kalshi's official trade-api/v2 endpoint and
  Polymarket again; re-attempt DeFi Rate (which has now failed to refresh
  for two straight editions).
- **Banxico's next policy-decision date** — unresolved for three straight
  editions, now confirmed structurally absent from the bank's own calendar
  page. Try a different angle this time (a named bank's own forward
  calendar, or Banxico's press-release archive) rather than the same
  calendar-page fetch again.
- **A primary-source document for the reciprocal-tariff-truce extension to
  10 January 2027** — unconfirmed by any US primary source for five straight
  editions now, even as China's own State Council has confirmed its side.
  Consider trying the specific implementing executive-order number or a
  direct USTR.gov Federal Register docket search rather than repeating the
  same whitehouse.gov/API sweep a sixth time.
- **The Investing.com displayed-%-vs-computed-% divergence** — found absent
  at edition 64 after being unchecked for two editions; keep testing it
  periodically rather than assuming either state now. **The distinct Yahoo
  Finance stale-%-field issue from edition 63** — not retested at edition 64
  either; worth a direct look.
- **US Treasury par yields** — continue the normal every-edition
  reconciliation now fully resumed since the Veterans Day closure.
- **Any further primary-sourced NVIDIA development** (severance disclosure,
  permanent-CEO search, board-investigation findings) via a fresh EDGAR
  check — and watch how the chip complex (especially AMD and Broadcom after
  Friday's sharp reversal) trades heading into NVIDIA's own 17 Nov earnings.
- **Drivers for Applied Materials' -2.74% decline** (beyond its declined Q1
  FY2027 guidance) if it moves again or a dated article surfaces; similarly
  for GPN, SMCI, YETI and MSTR's MSCI tie from edition 63, all still
  unconfirmed.
- **Apply the edition-64 sourcing lesson going forward**: when a research
  pass reports no further single-stock movers for a single-session window,
  try a direct price-history fetch on any name already known to be volatile
  that week before accepting the negative.
Dates to hold on to (edition-to-session mapping: 63 published Fri 13 Nov,
covering Thu 12 Nov; 64 published Mon 16 Nov, covering Fri 13 Nov as a
weekend-gap edition; 65 expected to publish Tue 17 Nov, covering Mon 16
Nov). RBA next decision 7-8 Dec 2026; the Fed
and BoC both meet 8-9/9 Dec 2026; SNB 10 Dec 2026; Riksbank approx. 16 Dec
2026; BoE 17 Dec 2026; the ECB and BoJ both meet 16-18 Dec 2026. The next
monthly settled-facts audit falls on the first edition of December 2026.
Thanksgiving (26 Nov, full closure) and its Friday half-day (27 Nov) are now
10 days out — worth a direct calendar check once the window reaches them
(likely edition 72-73 if no gaps, itself a rough estimate).

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

**Edition 63's carried-forward spec was 120,857 bytes, over the
100,000-byte threshold — this run (producing edition 64's spec) condenses
the log.** Edition 62's own medium-paragraph entry is folded into the
running mega-block (now "Editions 1-62"); edition 63's own full-detail entry
is condensed down to a medium paragraph; edition 64 is added in full detail.
There is no maximum size; condensing is housekeeping done by the run itself,
not a check to pass — there is no penalty for the file staying somewhat
large if the alternative is losing information.

**Editions 1–62 (condensed):** established the format (edition 1 baseline;
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
10-2 hawkish dissent (Cook, Hammack); the Bank of Canada delivered the
bigger surprise with a genuine 25bp hike to 2.50%. Equities notched a
fourth straight up session on narrow leadership (S&P +0.28%); Microsoft
beat and rose, Alphabet's GAAP EPS fell on a one-time mark-to-market loss
(approx. -10% AH), Fortinet beat-and-raised yet fell 5.90%, Carvana's clean
beat was wrongly headlined a "miss" by Barron's (corrected against the
8-K). Smaller movers: F5 -20.4%, Enphase -16.0%, Vertiv +16.5%, SK Hynix
+13.3%, Oracle +10.6%, Wendy's +15.1% (Trian take-private proposal). Vol
priced the decision as a non-event (VIX -3.48% to 16.91). First draft
spilled onto page 4, fixed via the spillover rule. **Edition 53 (Fri 30
Oct, covering Thu 29 Oct):** Q3 GDP (+3.4%) and September core PCE (+3.1%
y/y) both printed hot the same session the market largely shrugged off.
Alphabet lost approx. $500bn of market value in a single session (-12.64%);
Amazon's Q3 was a "double miss on the surface" masking real AWS/margin
strength (-4.25% regular, -7.30% AH). "Beat-and-raise guarantees nothing"
produced its largest cases yet: ServiceNow -26.95%, Intel -23.04% AH,
Caterpillar -9.25%. Smaller movers: Xerox -40.32%, Glaukos +33.65%, ADT
+33.20%, Marvell -13.24% (a claimed Lumentum-acquisition-talks driver found
unsubstantiated at the time — became real M&A four sessions later at
edition 55), Carvana +15.68%. A claimed Barclays PayPal downgrade was
investigated and found fabricated, dropped entirely. First draft ran a
genuine 6 pages; converged to 4 after a dozen rounds of trimming/
citation-merging, surfacing a new CSS multi-column pagination lesson.
**Edition 54 (Mon 2 Nov, covering Fri 30 Oct, a weekend-gap edition):** a
tech-led selloff dropped the major indices broadly (S&P -1.82% to
7,580.07, Nasdaq -2.86%, worst session since June) on Intel's historic
-28.58% collapse to $65.76 (worst day since 1974) following a weak Q4
guide; Nvidia -4.22% the single largest index-point drag. A record approx.
$6.3bn Binance hack roiled crypto-adjacent names. Two long-running Asia
threads resolved the same session: BoJ held at approx. 1.25% (8-1,
dissenter Takata Hajime), China's October PMI slipped back below 50 on both
gauges. Four previously-pending earnings reports (Chevron, Exxon Mobil,
AbbVie, Newell Brands) all beat and rose; a fresh CFTC CoT report powered
the third positioning chart. The November monthly settled-facts audit
completed cleanly across all ten central-bank rows. First draft ran 5 pages
on a single orphaned bullet; deleting the break converged to 4 pages.
**Edition 55 (Tue 3 Nov, covering Mon 2 Nov):** equities diverged sharply
on composition — Dow +0.41% while S&P -0.51% and Nasdaq -1.07% as
Technology (-2.95%) and Energy (-3.96%) dragged the cap-weighted indices
down even though 8 of 11 sectors closed higher. Crude collapsed 7-11% on an
Iran/US diplomatic-thaw signal. Apple's FQ4 beat but fell on a soft margin
outlook; Intel extended its collapse -8.80%; Oracle fell -8.76% on a
disclosed $20bn AI-capex raise; Marvell agreed to acquire Lumentum
(Marvell -12.72%, Lumentum -18.59%) — the prior edition's rejected rumor
becoming real. BoJ's and SNB's next-meeting dates both resolved directly;
the ECB's rate complex was promoted to SETTLED. VIX jumped +8.91% to
21.15. December FOMC hike odds firmed to approx. 72-73%. **Edition 56**
(Wed 4 Nov, covering Tue 3 Nov): equities diverged on composition, not
breadth (S&P +0.36%, Nasdaq +0.83% on a megacap/AI bounce; Dow -0.38%; only
4 of 11 sector ETFs higher). The RBA delivered its fifth 2026 hike (25bp to
4.85%) on a first-ever split 6-3 vote. AMD's Q3 (revenue $13.4bn +45% y/y)
drew a genuinely positive AH reaction (+5.02%). A claimed Oracle
analyst-upgrade note was rejected as unreliable; Henry Hub reconciled
cleanly across two sources for the first time in six editions. Rate-path
odds firmed to approx. 74-75% hike. **Edition 57** (Thu 5 Nov, covering Wed
4 Nov): dominant story was the 3 November 2026 US midterm elections,
called for Democrats in both chambers — Dow +3.03% to 53,356.12 (then this
report's largest one-day move), S&P +1.58%, Nasdaq +1.44%; WTI crashed
8.3%, Brent -8.67%; VIX posted its then-sharpest one-day decline, -20.26%
to 16.61. Nine of 11 sector ETFs closed higher. Seven single-stock movers:
Amdocs -30.07% (shock guidance cut), Qualcomm +5.33% regular/-7.52% AH (a
late snapshot, later superseded), Uber +4.91%, Helen of Troy +25.39%,
Duolingo +25.99%, Kyndryl +30.14%, Cricut +48.74%. Sweden's Riksbank
delivered a surprise 25bp hike to 2.00%, its first since 2023; October's
ISM Services PMI printed 54.5. December FOMC hike odds firmed to approx.
77-80% (since reversed sharply, then reversed back — see editions 58-61).
A Federal Register filing resolved the Section 301 178-product exclusion
lapse date (later found internally inconsistent — see edition 59; fully
resolved again at edition 61). **Edition 58** (Fri 6 Nov, covering Thu 5
Nov): a full, sharp reversal of Wednesday's election rally, driven by an
AI-capex/data-center-moratorium scare (local ballot measures tied to the
midterms rejected data-center buildouts in 40 of 41 votes). S&P fell 4.4%
to 7,353.73, Dow fell 3.4%, Nasdaq fell 5.5% (correction territory); zero
of 11 sector ETFs closed higher. The semiconductor complex all fell double
digits on no company-specific news. VIX posted its sharpest one-day
increase on record (+69.66% to 28.18), fully inverting contango into
backwardation. A dense earnings cluster: Qualcomm -9.49% confirmed close
(superseding edition 57's AH snapshot), Arm -13.08%, Tripadvisor -27.65%,
AppLovin +31.04%, Krispy Kreme +30.68%, Veracyte -54.30%, MNTN -54.68%.
Three "named secondary outlet flatly wrong" instances were caught and
excluded (a fabricated DraftKings AH figure, an unsupported Natera claim,
an unsupported "biggest calls" list). Two central banks delivered opposite
surprises the same session — BoE hiked 25bp to 4.00% (8-1, Mann dissenting
for 50bp); Banxico reportedly cut 25bp to 6.25% (3-2 vote), secondary-
sourced only. December 8-9 FOMC hike odds eased sharply to approx. 66.5%.
**Edition 59** (Mon 9 Nov, covering Fri 6 Nov): a much-stronger-than-expected
October jobs report (nonfarm payrolls +165,000 vs. approx. +65,000
consensus, unemployment 4.1%) snapped December FOMC hike odds from edition
58's approx. 66.5% back to approx. 76.5-77%, against a narrow, chip-led
relief rally (S&P +0.3%, only 3 of 11 sectors higher) that only partly
reversed Thursday's AI-capex rout; a widely-surfaced "Friday close" figure
was found to be a stale Thursday republish and excluded; a fresh round of
the vendor-retroactive-revision trap hit WTI/gold/silver/COMEX copper, and
Kitco's historical-close pages became inaccessible for the first time.
**Edition 60** (Tue 10 Nov, covering Mon 9 Nov): an 11-of-11-sector relief
rally (S&P +2.3% to 7,549.94, its best day since 8 April) coincided with a
sharp oil-price crash (WTI approx. -4.8%, Brent approx. -5.9%) on an Iran
de-escalation signal, while December hike odds extended further hawkish to
approx. 77-82%; the chip complex's rally lifted every name except Nvidia
(-4.27% to $178.67, tied to the Megaspeed/Alice Huang overhang), and a
dramatic board-investigation claim was investigated and excluded as
uncorroborated at the time — overturned as TRUE the very next edition. The
CFTC's assumed "next report" date was corrected from approx. 14 Nov to
Monday 16 November 2026, also becoming the corrected Q3 13F deadline. First
draft hit a new Annex-C column-balance overflow symptom (a trailing Method
note stranded alone on page 5 despite the forced break being deleted), fixed
by trimming Annex C's own entries directly rather than preceding prose.
**Edition 61** (Wed 11 Nov, covering Tue 10 Nov): October's hot CPI print
(headline +0.4% m/m, core +0.3% m/m, but BLS published no y/y figures at
all — a genuine data gap tied to the 2025 appropriations lapse) firmed
December FOMC hike odds to approx. 85-86%, a fourth consecutive hawkish
extension, against a modest mirror-image pullback (S&P -0.4% to 7,520.93,
breadth close to even at 6 of 11 sectors higher, Technology the laggard at
-1.15%). The edition's most significant finding: Nvidia's board-
investigation story, excluded as uncorroborated at edition 60, was
independently re-verified and found TRUE via NVIDIA's own 8 and 10 November
newsroom statements and top-tier wire corroboration — no 8-K filed on the
matter as of that cutoff; NVDA fell a third straight session (-5.47% to
$168.89). Other movers: Hims & Hers -16.61% (margin collapse despite a
revenue beat), Skydance Corp -7.59% (driver unverified, confounded with
Paramount Skydance/PSKY), Intel -2.09%, Broadcom +3.91%, Lucid +4.72%,
Rocket Lab +6.54% (record Q3). The Section 301 178-product tariff-exclusion
lapse resolved via a fresh USTR Federal Register notice; Henry Hub's
five-edition clean cross-vendor reconciliation streak broke; Riksbank's
vote split and Banxico's primary-source confirmation (both resolved the
next edition) remained open; CoreWeave's Tuesday-evening Q3 report was
entirely unverified by this cutoff (also resolved the next edition). First
draft converged cleanly to 4 pages on the first render; 26/26 sources clean,
zero stray tildes. **Edition 62** (Thu 12 Nov, covering Wed 11 Nov, the
window's one NYSE session — Veterans Day: equities traded a full normal
session, Treasury/Fed closed): a broad, CoreWeave-led relief rally reversed
Tuesday's hot-CPI pullback even as December FOMC hike odds held steady
(approx. 85-86%) — S&P +1.3% to 7,619.38, Dow +0.5% to 52,486.49, Nasdaq
+1.6% to 25,466.19, Russell 2000 +0.9% to 2,846.26, 10 of 11 sector ETFs
higher led by Technology (+3.23%). CoreWeave's Q3 2026 results (revenue
$3.661bn +168% y/y) drove the stock +24.71% to $60.77, confirmed via its
own 8-K. Other movers: Sonos +12.85%, TSMC +4.25% (Anthropic/OpenAI
preferred-stock investments), Nvidia +2.87% (broad chip rebound, no new
governance development per a fresh EDGAR check), Grocery Outlet -6.42%,
Rigetti -8.56%. Riksbank's 4 Nov vote confirmed unanimous 5-0 via primary
minutes; Banxico's 5 Nov cut to 6.25% (3-2) primary-source confirmed, next-
decision date became a fresh open item. SEC EDGAR resolved the SKYD/PSKY
ticker-identity confusion (same legal entity); the CFTC's irregular
November release spacing was confirmed as routine holiday-adjusted
scheduling; LME 3-month copper's "query-parameter problem" was traced to
its root (no historical field exists); US midterm-election certification
was clarified as having no single national step at all. No correction box.
First draft converged cleanly to 4 pages on the first render; 35/35 sources
clean (the highest count yet), zero stray tildes, zero `</td><sup`
instances.

**Edition 63 (Fri 13 Nov, covering Thu 12 Nov):** dominant story by a wide
margin was NVIDIA's own 8-K confirming Jensen Huang's resignation as
President, CEO and board member effective immediately — the board accepted
the resignation the evening of 11 Nov, announced 12 Nov; CFO Colette Kress
became interim CEO, director Harvey C. Jones became first-ever independent
Board Chair (8-K accession 0001045810-26-000082); independently corroborated
across five top-tier wires, with press reporting tying the resignation to
Huang's own disclosed extramarital relationships. NVDA closed -4.34% to
$166.19. Equities pulled back broadly (S&P -0.35% to 7,592.40, Dow -0.36% to
52,297.09, Nasdaq -0.39% to 25,366.09, Russell 2000 -1.66% to 2,799.06);
only 1 of 11 sector ETFs closed higher (Energy +1.51%). December FOMC hike
odds firmed further to approx. 85-88.5% (Kalshi's official API worked for
the first time in 26 editions) alongside a sharp Treasury selloff on the
first print since Veterans Day. A dense earnings session beyond NVIDIA:
Corteva -24.30% (guidance cut, 8-K confirmed), Cisco beat-and-raised yet
drew only a muted -0.30% AH move while Nu Holdings' clean beat drew +3.20%
AH the same evening; Global Payments -12.01%, Super Micro -11.30% and
YETI -10.49% all moved sharply with no independently verifiable driver;
Strategy/MSTR's -6.49% reported MSCI tie was disclosed as unconfirmed. VIX
jumped +6.92% to 18.70 (both CBOE feed bugs absent); oil rallied (WTI
+2.53%, Brent +3.30%) on no identified catalyst; gold/silver fell as yields
rose; a fresh vendor-revision trap hit WTI/Brent/Henry Hub/gold/silver
simultaneously. Banxico's next-decision date remained unresolved; a second,
narrower USTR tariff-suspension notice was found (not the broader
reciprocal truce, still unconfirmed, its reported 10 Nov expiry having
passed). No correction box. First draft converged cleanly to 4 pages on the
first render; 19/19 sources clean, zero stray tildes. **This edition's own
date line contained an error, caught and corrected at edition 64: it read
"Thursday 13 November 2026," but 13 November 2026 is a Friday** — see the
dedicated header-details entry near the top of this spec for the full
account; the edition's actual *date* (13 Nov) and window were both correct,
only the weekday word was wrong.

**Edition 64 (most recent — full detail)** — Monday 16 November 2026 report
covering Friday 13 November 2026 (the window's one NYSE session; a
weekend-gap edition, research window Thu 12 Nov 2026 20:00 ET through Sun 15
Nov 2026 20:21 ET).

**The dominant story was a sharp reversal of the week's rotation into
Nvidia's chip-sector rivals, on profit-taking, which did more damage to
Technology than Nvidia's own continued slide.** AMD fell -8.75% to $534.06
and Broadcom fell -4.76% to $347.01, both with no company-specific news,
unwinding a run that had taken AMD up as much as approx. 30% on the week
through Thursday on the rotation out of Nvidia and into its rivals after
Jensen Huang's resignation. **This was not surfaced by the dedicated
equities research pass** (which searched specifically for Friday 13 Nov
movers and found only four names, flagging thin aggregator coverage for
that date) **but was found via a direct coordinator follow-up fetch of
AMD's and Broadcom's own price-history pages**, cross-checked against an
independently-reported same-day quote (247wallst.com) that matched exactly
— logged as a new, inverse-direction instance of the "verify before
publishing" discipline (see the dedicated Standing Facts entry). NVDA
itself extended its post-resignation slide a second session, -2.01% to
$162.85 (-6.27% combined over Thu-Fri); a direct SEC EDGAR check found no
new 8-K filed over the weekend on severance, the CEO search or the board
investigation.

**Equities eased modestly on the session**, driven almost entirely by this
chip-complex reversal: S&P 500 -0.41% to 7,561.67, Nasdaq Composite -0.91%
to 25,136.27, Russell 2000 -0.31% to 2,790.49, Dow +0.10% to 52,347.55
(confirmed via AP's wire, wtop.com and lanacion.com.ar mirrors in exact
agreement, cross-checked against Yahoo Finance and SPY). 7 of 11 sector ETFs
closed higher — a sharp breadth improvement from Thursday's 1-of-11 — with
Technology (-2.01%) the only sector move of consequence; Consumer Staples
(+1.42%), Communication Services (+1.05%) and Energy (+0.98%) led. For the
week, all four indices still finished higher (S&P +2.5%, its first positive
week since early October).

**October's Producer Price Index, released Friday 8:30am ET, came in
genuinely mixed**: headline final demand +0.3% m/m (+6.5% y/y), cooler than
the approx. +0.4% m/m consensus; core +0.5% m/m (+4.9% y/y), hotter than the
approx. +0.3% m/m estimate — confirmed directly against bls.gov, with an
intact y/y comparison (unlike October CPI's data-gap problem). December
FOMC hike odds held essentially flat (approx. 86-88% on both Kalshi's
official API, working a second straight edition, and Polymarket), rather
than extending the hawkish drift of editions 61-63.

**A dense earnings session beyond the chip complex**: Stantec +14.06% on a
clean Q3 beat-and-raise (6-K confirmed); Cisco's clean beat-and-raise drew
only a muted -0.30% AH move Thursday night before falling a further -6.25%
Friday on sequentially flattish Q2 FY2027 guidance; Applied Materials beat
on both lines yet fell -2.74%, with the CFO declining to give forward
guidance — a further instance of "beat-and-raise guarantees nothing,"
producing three different outcomes from three beats in one session.

**Other findings:** the VIX complex extended Thursday's spike (VIX +3.21%
to 19.30, both CBOE feed bugs present again after a clean streak); oil
drifted modestly Friday (WTI -0.20%, Brent +0.02%) then extended losses
into Sunday's partial reopen; a fresh vendor-revision trap hit WTI
(Thursday's base restated up from approx. $86.53 to $88.74) and Henry Hub
(restated down to $3.340, closing the prior cross-vendor gap); a genuine
cross-vendor DIRECTIONAL conflict surfaced on USD/JPY's Friday move
(Investing.com: yen strengthens; Yahoo: yen weakens); the Investing.com
displayed-%-vs-computed-% divergence was retested across nine series and
found absent; Treasury yields extended Thursday's selloff (2-yr +2bp,
10-yr +5bp, 30-yr +4bp); the CFTC's Tuesday-10-Nov report had not yet
posted as of the Sunday cutoff (due later Monday, inside edition 65's
window, alongside the Q3 13F deadline); Banxico's own calendar page
confirmed empty for 2027, a third straight edition unresolved.

**Format:** edition 64 used the correction box (the first since edition 53)
to correct edition 63's own date-line weekday error (see the header-details
entry). First draft converged to 4 pages; a second render was needed only
because the AMD/Broadcom finding and the correction box were added
mid-draft, and the page count held at 4 both times. 20/20 sources clean
after one quick fix (three newly-added citations needed inline references;
one misassigned citation was corrected to point at the Banxico table row it
actually supported); zero stray tildes; zero `</td><sup` instances.

**Open threads for edition 65.** Edition 65 covers **Monday 16 November
2026** (a normal full session), if no gap. Priority items: **the CFTC
Commitment of Traders report** (covering Tue 10 Nov data) **and the Q3 2026
13F filing deadline**, both due that day and not yet posted/passed as of
edition 64's cutoff; **whether December FOMC hike odds (approx. 86-88%,
essentially flat since edition 63) hold, firm, or ease** on Monday's fresh
session; **Banxico's next-decision date**, unresolved for three straight
editions and now confirmed structurally absent from the bank's own
calendar — try a different angle (a named bank's forward calendar, or
Banxico's press-release archive); **a primary source for the broader
reciprocal-tariff-truce extension to 10 January 2027**, unconfirmed for five
straight editions even as China's own State Council has confirmed its side;
**any further primary-sourced NVIDIA development** via a fresh EDGAR check,
and how the chip complex (especially AMD and Broadcom after Friday's sharp
reversal) trades heading into NVIDIA's own 17 Nov earnings; **drivers for
Applied Materials, GPN, SMCI, YETI and MSTR's MSCI tie**, all still
unconfirmed if any move again; and **applying the edition-64 sourcing
lesson** — when a research pass reports a clean negative for single-stock
movers, try a direct price-history fetch on any name already known to be
volatile that week before accepting it.
Dates to hold on to (edition-to-session mapping: 63 published Fri 13 Nov,
covering Thu 12 Nov; 64 published Mon 16 Nov, covering Fri 13 Nov as a
weekend-gap edition; 65 expected to publish Tue 17 Nov, covering Mon 16
Nov). RBA next decision 7-8 Dec; the Fed and
BoC both meet 8-9/9 Dec; SNB 10 Dec; Riksbank approx. 16 Dec; BoE 17 Dec; the
ECB and BoJ both meet 16-18 Dec. The next monthly settled-facts audit falls
on the first edition of December 2026. Thanksgiving (26 Nov, full closure)
and its Friday half-day (27 Nov) are now 10 days out — worth a direct
calendar check once the window reaches them (likely edition 72-73 if no
gaps, a rough estimate).
