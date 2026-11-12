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
  applied correctly for **forty straight editions (33 through 62)** —
  treat as settled; edition 62 read "Thursday 12 November 2026" as the date
  line, covering the Wednesday 11 November session in the window line.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 62 all reused the
  same pattern — now confirmed clean across **thirty-four consecutive
  editions**; edition 62 phrased it "Window: Tue 10 Nov 2026 20:00 ET – Wed 11
  Nov 2026 20:23 ET (Wed 11 Nov close/AH, the window's one NYSE session —
  Veterans Day: equities traded a full normal session, Treasury cash markets
  and the Federal Reserve were closed)." No further confirmation needed; treat
  this as settled.

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
— now under two weeks out from edition 62. Thanksgiving is a full closure for
both equities and bonds; the Friday after is a half-day for equities with an
early bond close. Not independently re-verified at edition 62 (still too far
out to be inside any research pass's window) — re-confirm directly against
nyse.com's holiday calendar and sifma.org's bond-market calendar whichever
edition's window first reaches it (roughly edition 73-74 if no gaps). **Veterans
Day (Wednesday 11 November 2026) itself is now resolved/closed history, not a
forward item any more** — edition 62 directly confirmed equities traded a full
normal session while Treasury cash markets and the Federal Reserve were
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
  61, no change). Kevin Warsh's actual press-conference remarks remain
  unverified and not worth a dedicated search this far out. Blackout (Oct
  17-29, 2026) held clean through the decision, as expected. **Next meeting:
  8-9 December 2026, an SEP meeting.**
- **Rate-path odds — HELD STEADY at edition 62, breaking the run of
  consecutive hawkish extensions (editions 59-61) without reversing.** A fresh
  Polymarket Gamma-API pull (11 Nov 2026, approx. 8:23pm ET) put the
  December-hike-specific (25bp) market at approx. **85.5%**, essentially
  unchanged from edition 61's reading, with a 50bp+ market at approx. **10.6%**.
  DeFi Rate's blended Kalshi/Polymarket aggregator read approx. **86%** at the
  same snapshot (11 Nov, 8:28pm ET), also unchanged. The CPI print is now
  fully priced in; conviction neither firmed further nor eased despite a broad
  equity rally the same session — a useful datapoint that the rally reflected
  risk appetite (CoreWeave's earnings, an AI/chip rebound) rather than any
  dovish repricing. **Kalshi's own direct fetch failed again at edition 62 —
  HTTP 000/connection failure** — now **TWENTY-SIX consecutive failures
  (37-62).** CME FedWatch also failed again directly (HTTP 403 this time, a
  new signature vs. the prior timeout), a **TWENTY-SECOND** consecutive
  failure (41-62). The composite "at least one more hike in 2026" read has
  still not been freshly re-pulled since edition 38 (last known approx. 80%) —
  don't cite without a fresh pull. Worth a fresh check at edition 63 to see if
  the approx. 85-86% read holds into a second quiet edition or finally moves.
- **US-China Section 301 178-product tariff-exclusion lapse — RESOLVED at
  edition 61, closed thread, do not re-open absent a new dated filing.** A new
  USTR notice (Federal Register Doc. 2026-22925, 91 FR 72610, published 10
  November 2026 — fetched directly via the Federal Register's own developer
  API, `federalregister.gov/api/v1/documents/2026-22925.json`) extends **all
  178 exclusions through 11:59pm ET 9 January 2027**, superseding the prior
  notice's internally inconsistent 9-vs-10-November lapse dates that had been
  open since edition 57. **This is the first time the FR developer API —
  flagged at edition 60 as a promising alternate access path after the search
  UI's long-standing block — actually resolved the live question it was
  tried against; worth defaulting to it first for any future Federal Register
  lookup when the search UI (still blocked, redirecting to
  unblock.federalregister.gov) is unavailable.** Separately, and NOT to be
  conflated with the above: a different legal mechanism — a "reciprocal
  tariff" truce with China holding a 10% rate — was reportedly due to expire
  around the same boundary. Secondary reporting (Bloomberg Government,
  investinglive, other outlets) describes Treasury Secretary Bessent
  announcing on 23 September 2026 a two-month extension of that truce to 10
  January 2027, but **no primary USTR/White House/Federal Register document
  codifying this specific extension has been found through edition 62**
  (edition 62 re-tried via a direct Federal Register API query of USTR's
  recent filings specifically, and still found nothing) —
  treat the January 2027 date for the reciprocal-tariff truce as
  reported-not-verified if cited, distinct from the now-primary-confirmed
  Section 301 exclusion extension. Also clarified at edition 61: a separately
  circulating claim about a 20%→10% IEEPA "fentanyl tariff" cut keyed to the
  same Nov 9/10 boundary was a **misdating** — that cut actually took effect
  for goods entered on/after 10 November **2025**, a year earlier, and is not
  a live November 2026 question at all. Drop this fentanyl-tariff sub-thread
  entirely going forward; it does not need to be watched.
- **Fed Chair: Kevin Warsh — SETTLED, stop re-verifying it every run.** No
  contradiction surfaced through edition 62; directly re-confirmed via
  federalreserve.gov's own bios page at edition 54's November monthly audit,
  closing that housekeeping item cleanly; not re-attempted at editions 55
  through 62 (settled, no fetch needed). His Chairman term ends 21 May 2030
  (took office 22 May 2026, a four-year term); his separate term as a Board of
  Governors member runs to 31 January 2040. The Chairmanship re-opens as a
  live fact only on a successor nominated/confirmed, a resignation or
  removal, or that 21 May 2030 term-end date actually arriving, or the **next
  monthly audit (first edition of December 2026)**.
- **The 3 November 2026 US midterm elections — certification is now
  STRUCTURALLY EXPLAINED at edition 62, which changes what "watch again" even
  means going forward.** Democrats won control of both the House and Senate —
  called by AP/CNBC/NBC/PBS by Wednesday 4 November morning — ending unified
  Republican control of Washington. Democrats flipped at least seven Senate
  seats (Iowa, Kansas, Ohio, North Carolina, New Hampshire, South Carolina,
  Texas); a handful of races were still uncalled as of edition 57's cutoff and
  this was not independently re-checked since — do not cite a final seat count
  without re-checking. **Edition 62's dedicated search (via USAFacts,
  ProtectDemocracy and Brennan Center state-certification trackers) found
  there is no single national certification step for midterm elections at all
  — unlike a presidential election, there is no electoral-college-style
  national certification event to wait for.** Certification is inherently
  state-by-state, with deadlines running into December (e.g., Georgia, 18 Dec
  2026; Pennsylvania county certification and Arizona/Michigan statewide
  canvasses, all by 23 Nov, previously logged). **This means "certification
  status unconfirmed" will likely remain true for weeks more as a matter of
  structure, not as an open research failure** — future editions should watch
  specific state deadlines as they land rather than searching for a single
  national resolution event that does not exist.
- **MAJOR UPDATE at edition 61 — the Nvidia / Jensen Huang / Alice Huang /
  Megaspeed China-intelligence story's most dramatic sub-claim, excluded as
  uncorroborated at edition 60, is now CONFIRMED TRUE.** Edition 60 had
  investigated a circulating claim — that Nvidia's board formally announced
  an independent investigation into CEO Jensen Huang on 8 November 2026,
  including a staff apology email — and found it uncorroborated by any dated
  wire or SEC filing at the time, excluding it from the published briefing as
  the correct, skeptical call given what was findable then. **Edition 61's
  own direct, independent re-check (run by the coordinator itself, precisely
  because of this claim's history) found the story is real**: NVIDIA's own
  newsroom carries a dated 8 November 2026 "Statement From NVIDIA Board of
  Directors" confirming the board is "initiating an independent
  investigation" after reporting that Huang was "the target of a foreign
  intelligence effort," overseen by "a committee of independent directors,
  assisted by outside independent counsel"; the board states it has "no
  reason to believe that either national security or NVIDIA secrets were
  compromised" and retains confidence in Huang. A companion 10 November
  statement from the board's independent members names the outside counsel:
  former acting US Attorney (SDNY) Joon H. Kim and his firm Wachtell, Lipton,
  Rosen & Katz. **Both statements are independently corroborated by multiple
  top-tier wires/outlets** — the Washington Post, NBC News, CBS News, Axios,
  TechCrunch and Fox Business all carried matching detail, including Huang's
  own internal message acknowledging the relationship (with Megaspeed
  executive Alice Huang, the subject of the 29 October NYT/FT reporting on
  alleged China-intelligence ties) and apologizing to colleagues. **As of
  edition 61's cutoff, NVIDIA has still filed no Form 8-K referencing the
  matter** — confirmed directly via SEC EDGAR's filing list and full-text
  search, a genuine ongoing disclosure gap distinct from the news itself
  being real. A reported shareholder lawsuit and an FBI-investigation
  characterization, and a specific 18 November congressional closed-door
  briefing request, all remain secondary-sourced only and were not repeated
  as fact. **The lesson to carry forward, refined from edition 60's version:
  the discipline is not to reflexively REJECT a dramatic, one-step-beyond-
  real claim — it is to independently, directly verify it before either
  accepting OR rejecting it.** Edition 60 correctly declined to publish an
  unconfirmable claim; edition 61 correctly confirmed the same claim once a
  fuller, differently-worded search surfaced the primary NVIDIA statements
  and top-tier wire corroboration that eluded the earlier attempt. Both calls
  were right for what each edition could verify at the time — the takeaway is
  about search persistence and trying varied query phrasing / direct primary
  URLs before settling on "unconfirmed," not about defaulting to suspicion
  forever. **Watch for further genuine developments** (an eventual 8-K, the
  investigation's outcome, a scheduled hearing actually occurring) in future
  editions — this is now a live, ongoing governance story, not a closed one.
  NVDA fell a third straight session at edition 61 (-5.47% to $168.89) even as
  chip peers paused rather than extended Monday's rally. **Edition 62 checked
  directly for any further primary-sourced development (a new 8-K, investigation
  findings, a hearing actually occurring) via a fresh SEC EDGAR filing-list
  check and found none** — NVIDIA's most recent 8-K on file remains dated 3
  September 2026, nothing new filed in the 8-12 November window. NVDA rebounded
  +2.87% to $173.73 at edition 62 alongside a broad chip/AI rally, with no
  stock-specific catalyst identified for the rebound itself; the governance
  story remains open and should keep being checked directly against EDGAR
  rather than assumed closed.
- General principle for everything still live: do not assume a routine
  macro-calendar fact (meeting dates, symposium schedules, other central
  banks' policy rates, government funding status) from memory or from the
  prompt's own framing — verify it fresh from a primary source
  (federalreserve.gov, bankofengland.co.uk, boj.or.jp, kansascityfed.org,
  norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, rba.gov.au,
  ecb.europa.eu, bankofcanada.ca, whitehouse.gov, etc.) every edition, exactly
  like any other data point, until an entry below is marked SETTLED. These
  are the rates and dates that feed Section 3's policy-rate table, so the
  table is the natural place to land them. Per-bank status as of edition 62:
  - **Reserve Bank of Australia:** current rate **4.85%**, hiked 25bp on
    Tuesday 3 November 2026 (6-3 split vote, its fifth hike of 2026) —
    SETTLED pending the RBA's own next decision, **7-8 December 2026**. Not
    re-attempted at edition 62 (no fetch needed; nothing in this window
    touched it).
  - **Bank of England:** rate **4.00%**, hiked 25bp on Thursday 5 November
    2026 (8-1 vote, Mann dissenting for +50bp) — SETTLED pending the next
    decision, **17 December 2026**. Not re-attempted at edition 62.
  - **European Central Bank:** rate complex (deposit facility 2.50%, main
    refi 2.65%, marginal lending 2.90%) **SETTLED**; next Governing Council
    meeting **16-17 December 2026**. Not re-attempted at edition 62.
  - **Bank of Japan:** current rate approx. 1.25%, SETTLED pending its own
    next meeting, **17-18 December 2026**. Not re-attempted at edition 62.
  - **Bank of Canada:** SETTLED. Current rate 2.50%, hiked 25bp 28 October
    2026. Next decision **9 December 2026** (same date as the Fed's). Not
    re-attempted at edition 62.
  - **Swiss National Bank:** current rate 0.00%, SETTLED. Next assessment
    **10 December 2026**. Not re-attempted at edition 62.
  - **Norges Bank:** current rate **4.50%** (hiked 25bp 24 Sept 2026),
    SETTLED; a forecast-free interim review on 5 November 2026 kept the rate
    unchanged, confirmed directly at edition 60. Next full decision remains
    **17 December 2026**. Not re-attempted at edition 62.
  - **Riksbank — the vote-split thread CLOSED at edition 62, resolved
    unanimous.** Current rate **2.00%**, hiked 25bp on Wednesday 4 November
    2026 (its first hike since 2023) — SETTLED pending the next decision,
    **approx. 16 December 2026** (inferred from the Riksbank's own Monetary
    Policy Report date). **Edition 62 fetched the bank's own primary minutes
    PDFs directly** (`protokollsbilaga-a-beslut-om-styrranta.pdf` and the
    22-page `bilaga-penningpolitiskt-protokoll...pdf`, both via riksbank.se)
    and found all five Executive Board members (Thedéen, Bunge, Jansson, Seim,
    Hjelm) individually recorded support for the hike, with no dissent
    language anywhere in the transcript and all five signing off — a
    **unanimous 5-0 decision**, closing a four-edition open thread. Do not
    re-derive; this is now closed meeting history.
  - **Banxico — the rate and vote are now BOTH primary-source confirmed as of
    edition 62, closing the sourcing-tier gap; the next-decision date is the
    new open item.** Banxico **cut its overnight interbank rate 25bp, from
    6.50% to 6.25%**, decision dated 5 November, effective 6 November 2026, a
    **3-2 vote** (Deputy Governors Galia Borja Gómez and Jonathan Heath
    dissenting in favor of holding; Governor Rodríguez Ceja and Deputy
    Governors Cuadra García and Mejía Castelazo voting for the cut). **Edition
    62 fetched Banxico's own 5 November
    press-release PDF directly**
    (`banxico.org.mx/publicaciones-y-prensa/anuncios-de-las-decisiones-de-politica-monetaria/{43236252-D06E-5231-27E8-058810A86A52}.pdf`,
    via `pdftotext`) and confirmed the rate, direction and vote split exactly
    as previously carried on secondary sourcing — **promote this specific
    decision to primary-confirmed, closing a long-running sourcing-tier gap.**
    **However, the release does not state a next-meeting date** — the
    previously-carried approx. 17 December 2026 figure (secondary-sourced)
    could not be reconfirmed from this primary document, so next-decision
    date is now a genuine open item (Annex B material) rather than settled;
    try to resolve it at edition 63, e.g. via Banxico's own published 2026/2027
    monetary-policy-decision calendar page rather than the decision release
    itself.
  - **Government funding/shutdown status:** H.R. 6500 funds federal agencies
    through 11 December 2026, no shutdown in effect — **re-confirmed cleanly
    and directly against whitehouse.gov again at edition 62.** Continue the
    standard re-check-every-edition discipline regardless.
- **NEW closed thread at edition 61 — October 2026 US CPI, with a genuinely
  unusual wrinkle worth remembering for future months.** Released 8:30am ET
  Tuesday 10 November 2026 (BLS release USDL-26-1685): headline CPI-U **+0.4%
  m/m seasonally adjusted** (+0.2% unadjusted), core (ex food/energy) **+0.3%
  m/m seasonally adjusted**, the same pace as the prior two months. **BLS
  published NO year-over-year figures for either series** — it did not
  collect October 2025 survey data because of that year's lapse in
  appropriations, so no valid 12-month comparison exists for October 2026
  against it. **This is a genuine, structural data gap, not a reporting
  failure — watch whether it recurs for November 2026 CPI (due roughly
  mid-December) and any other BLS series with an October-2025-vs-October-2026
  12-month-comparison dependency**, rather than assuming it was a one-month
  quirk. No single, clearly-attributed consensus forecast could be found for
  this release; contradictory unattributed-aggregator ranges were discarded
  rather than reported.
- **NEW closed thread at edition 62 — CoreWeave's (CRWV) Q3 2026 results,
  entirely unverified at edition 61's cutoff, are now fully resolved via the
  company's own 8-K.** Revenue $3.661bn (+168% y/y), beating CoreWeave's own
  $3.45-3.60bn guidance; GAAP net loss widened to $(709)m (EPS $(1.27), from
  $(0.22) a year earlier) on net interest expense surging to $(846)m; adjusted
  EBITDA $2,256m (62% margin); GAAP operating income turned positive at
  $207m; remaining performance obligations (backlog) approx. $132.5bn. FY2026
  revenue guidance raised to $13.0-13.3bn (from $12.4-13.2bn); exit-2026
  annualized revenue run-rate guided to $20-21bn. Confirmed directly against
  SEC EDGAR (8-K, Exhibit 99.1, accession 0001769628-26-000461). **The stock's
  Tuesday-night after-hours reaction is disclosed as genuinely disputed across
  vendors (approx. +2.4% to +7.9%)** — no single AH figure should be cited as
  fact; only the separate, confirmed Wednesday 11 Nov regular-session close
  ($60.77, +24.71% from Tuesday's $48.73, CoreWeave's best day since April
  2025) is solid. Do not re-derive the Q3 figures; do watch for Q4/FY2026
  actuals against this guidance in the normal course.
- **NEW closed thread at edition 62 — Skydance Corp (SKYD) and Paramount
  Skydance (PSKY) are the SAME legal entity, resolving a standing
  ticker-confusion thread that had blocked identifying SKYD's earnings driver
  since edition 61.** A direct SEC EDGAR company-filing-history check (CIK
  0002041610) shows the entity was named New Pluto Global, Inc., then
  Paramount Skydance Corp (through 2026-10-06), then renamed again to
  Skydance Corp — a single CIK's name/ticker history, not two separate
  companies (PSKY and SKYD most likely reflect different share classes rather
  than two issuers). Do not re-derive this; do keep treating SKYD's specific
  daily driver claims as needing their own verification, since this resolves
  only the identity confusion, not causation for any individual day's move
  (edition 61's 10 Nov -7.59% driver remains best-explained-but-not-primary-
  confirmed: Morgan Stanley/Citizens price-target cuts plus a flagged approx.
  $200m Q4 profit hit from a weak Warner Bros. film slate).
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
  Situation Summary. **October 2026's jobs report — RESOLVED at edition 59,
  closed thread, do not re-derive:** nonfarm payrolls **+165,000**, a 100,000
  upside surprise against a FactSet-polled median consensus of **+65,000**
  and a median unemployment-rate forecast of 4.2%; unemployment held at
  **4.1%**; average hourly earnings **+0.4% m/m / +3.1% y/y**; August revised
  up 53,000 (to +186,000) and September revised up 31,000 (to +60,000), a
  combined +84,000 — confirmed directly against bls.gov's Employment
  Situation Summary, released 6 November 2026, 8:30am ET. This print was the
  proximate driver of edition 59's sharp rate-odds reversal, and the hawkish
  repricing it started has continued extending through edition 61 (see the
  dedicated Standing Facts bullet above).
- **September 2026 ISM Services/Non-Manufacturing PMI — closed thread as of
  edition 35, do not re-derive:** headline 54.9% (down from August's 55.4%),
  Prices Paid 74.0% (+1.4pt, highest since July 2022). **October's ISM
  Services PMI — RESOLVED at edition 57:** headline **54.5%**, below the
  **54.8%** consensus/forecast and a third straight month without
  acceleration, confirmed via Investing.com's Economic Calendar. Sub-index
  detail (Prices Paid, New Orders, Employment) remains an Annex B item.
- **September 2026 US CPI — closed thread as of edition 42, do not re-derive:**
  headline **+0.6% m/m / +3.7% y/y**, core **+0.3% m/m / +2.6% y/y**, both
  above the Dow Jones consensus of approx. 3.6%/2.5%, confirmed directly
  against bls.gov's CPI Summary release. This was the proximate trigger for
  edition 42's broad equity selloff, VIX spike and sharp October-hike-odds
  repricing. **October 2026's CPI — now RESOLVED at edition 61** (see the
  dedicated NEW standing-facts bullet above for the full account, including
  the unusual missing-y/y wrinkle).
- **September 2026 US PPI — closed thread as of edition 43, do not
  re-derive:** final demand **+1.3% m/m / +6.3% y/y** (NSA), the largest
  monthly gain since March 2022 and largest 12-month rise since December
  2022; the trade-services-excluded measure was +0.5% m/m / +5.0% y/y.
  Energy (+10.8% m/m, gasoline +20.3%) drove over 80% of the goods-side
  increase. Confirmed directly against bls.gov. **October 2026's PPI is due
  Friday 13 November 2026**, a live, not-yet-released figure (edition 64's
  window if no gaps).
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
  watch for a level reset around that date (roughly two weeks from edition
  61, likely inside edition 70-71's window if no gaps), not a genuine
  month-over-month signal.
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
  directly against whitehouse.gov again at edition 62.** H.R. 6500 funds
  federal agencies through **11 December 2026**. Watch for shutdown risk
  resurfacing as that date approaches.
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
  notice of appeal is still unconfirmed for a SEVENTEENTH straight edition
  (47-62).** Meta owes **$25bn** in civil penalties for the jury's
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
  re-attempted at editions 55 through 61 (out of scope); no new development
  in the 48-state settlement or the Unfair Practices Act stay.
- **New calendar-awareness item, reconfirmed relevant across several
  editions: "equities-open, bonds-closed" US holidays need an explicit check
  every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day; Veterans Day, Wednesday 11 November
  2026, was independently verified at edition 57, re-confirmed again directly
  at edition 61, and **directly OBSERVED (not just pre-confirmed) at edition
  62 itself** — equities traded a full normal session while Treasury cash
  markets and the Federal Reserve were closed (confirmed via home.treasury.gov
  posting no new TextView row for 11 Nov) — this is now resolved/closed
  history, not a live watch item any more. **The only still-open calendar
  flag of this kind is Thanksgiving (26 Nov) plus the Friday half-day (27
  Nov) — see the Schedule section above.** The DST transition (ended Sunday 1
  November 2026) remains itself resolved/settled.
- **The vendor-retroactive-revision trap recurred AGAIN at edition 62, this
  time on gold and silver, confirming it is a recurring structural pattern
  across nearly every tracked instrument rather than a one-off.** Edition 61
  logged Tuesday 10 Nov's gold futures close as $4,046.20 (-1.66%) and silver
  as $51.563 (-2.14%); edition 62's fresh Investing.com re-fetch of that same
  10 Nov date instead showed gold at $4,030.20 (-2.05%) and silver at $51.225
  (-2.79%). As before, neither figure carries a flag indicating which is
  "right," and per established convention this is disclosed as a vendor
  revision in Annex A, not a reader-facing correction (edition 61's published
  figures were not traceably wrong when checked). Edition 61's own WTI
  instance (Monday 9 Nov base revised $86.44→$86.85) remains logged as the
  prior occurrence. **Henry Hub's cross-vendor gap, which broke a five-edition
  clean streak at edition 61 (Investing.com $3.293 vs. Yahoo $3.302, a 28bp
  gap), PERSISTED a second straight session at edition 62** (Investing.com
  $3.246 vs. Yahoo $3.264 for Wed 11 Nov, approx. 55bp gap on computed %
  change) **though Tuesday's own base also quietly smoothed to $3.296 on both
  vendors** (versus the $3.293/$3.302 split edition 61 reported) — resume the
  every-edition two-source reconciliation discipline for Henry Hub; do not
  revert to an occasional-spot-check cadence until a fresh multi-edition clean
  streak re-establishes. **Investing.com's own displayed "% change" field
  divergence from direct computation (flagged at edition 60, absent at
  edition 61) was not explicitly re-checked at edition 62** — worth a direct
  look again next edition rather than assuming either state persists.
- **Henry Hub: see the dedicated bullet above — the cross-vendor gap has now
  persisted TWO straight editions (61-62) after a prior five-edition clean
  streak (56-60).** Still NGZ6 (December); no roll to NGF7 (January) yet as of
  Wednesday 11 Nov.
- **westmetall.com (LME copper) — RESOLVED AT THE ROOT at edition 62: the
  3-month series' "query-parameter problem" was never a query problem at
  all.** The cash series stayed clean again (Wednesday 11 Nov $13,875.50/t vs.
  Tuesday's $13,992.00/t). Edition 62 pulled westmetall's own list of valid
  `field=` identifiers directly from its markdaten.php links and found **there
  is no separate field key for a historical 3-month series — only
  `LME_Cu_cash` is a valid historical parameter.** The site's current-day page
  happens to display a "3 months" column alongside the cash settlement, but
  only for the current date; there is no reachable historical 3-month archive
  via this site, full stop. **This is now a permanent, structural limitation,
  not an access problem to keep retrying with new URL variants** — future
  editions should simply report the current-day 3-month print (Wednesday's was
  $13,795.00/t) alongside the cash series, optionally cross-checked loosely
  against Yahoo Finance's COMEX HG=F converted to $/tonne (edition 62's cross-
  check: HG=F implied approx. $13,796/t, a close match). Stop trying
  alternative access methods for a historical 3-month series; there isn't one.
- **New sourcing-mechanics trap logged at edition 50, relevant to any
  Monday-dated (or any day-after-a-non-trading-day) edition: Investing.com
  inserts an electronic Sunday-evening re-open print as its own row for every
  24-hour-traded instrument.** Not directly relevant to edition 61 (a
  Tuesday-covering edition with no weekend gap in its window), but keep
  applying the discipline (fetching rows explicitly by date, not by position)
  on every post-weekend or post-gap edition going forward.
- **The Kitco live-spot-vs-headline cross-check remains in its fourth failure
  mode (total inaccessibility) for a FOURTH consecutive edition at edition
  62** — both canonical historical-close URLs (including a fresh attempt at
  `kitco.com/charts/historicalgold.html`) still redirect straight back to a
  live-quote-only page with no retained close row for any past date. This is
  now confirmed as a structural absence (no historical table is reachable at
  all), not an intermittent access hiccup. No Kitco historical spot figure is
  reported for Wednesday 11 Nov as a result. Keep attempting it fresh every
  edition regardless, in case the page is restructured.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company, IPO'd 1 July 2026 at
  $29/share. Logged here so a future edition doesn't waste effort
  re-verifying the ticker's legitimacy if it moves sharply again.
- **The "named secondary outlet's own claim can be flatly wrong" trap gained
  important nuance at edition 61 — read alongside the dedicated Nvidia
  Standing Facts bullet above, which is the most important update to this
  family of lessons to date.** Edition 60 excluded a dramatic, specific claim
  (Nvidia's board formally investigating CEO Jensen Huang, announced 8
  November, with a staff apology email) as uncorroborated after a direct
  follow-up search found no support. **Edition 61 found the SAME claim to be
  TRUE** once verified again with different search phrasing and direct fetches
  of NVIDIA's own newsroom URLs — primary board statements plus top-tier wire
  corroboration (Washington Post, NBC News, CBS News, Axios, TechCrunch, Fox
  Business) all confirmed it. **This does not invalidate edition 60's
  caution — it refines the lesson: a dramatic, one-step-beyond-real claim
  deserves a genuinely thorough, differently-phrased, primary-source-seeking
  verification attempt before either accepting OR rejecting it, not a single
  search attempt in either direction.** Separately, two smaller, more
  familiar instances of the related "premarket/aggregator snapshot mistaken
  for the session close, with a driver claim that doesn't hold up" trap
  recurred at edition 61: Rocket Lab (a claimed approx. -7% premarket "EPS
  miss" reaction, actually +6.54% at the regular close) and Lucid (a claimed
  approx. -3% premarket "miss" reaction, actually +4.72% at the regular
  close) — both excluded from the published movers' driver text and reported
  only as the verified regular-session outcome. Prior instances remain
  logged: JetBlue (edition 50, magnitude), Carvana/Barron's (edition 52,
  direction/framing), Tesla and NU Holdings (edition 49, magnitude), Marvell/
  Lumentum and Barclays/PayPal (edition 53), a misdated Reuters-style squib
  plus a wrong-year Trefis list (edition 54), Brent crude's disclosed
  settle-to-settle-vs-"more than 7%" methodology discrepancy (edition 55), a
  claimed Oracle analyst-upgrade note (edition 56), three instances at
  edition 58 (a fabricated DraftKings AH figure, an unsupported Natera
  claim, an unsupported "biggest calls" list), a stale-date index-close
  republish at edition 59, and at edition 62 a claimed tie between
  International Money Express (+6.08%) and Western Union (-3.03%) moves and
  the Intermex deal's contractual drop-dead date — the direction was itself
  counterintuitive for a reportedly-scrapped-deal target, no primary source
  confirmed the tie, and both were excluded from the published movers
  entirely rather than repeated with a hedge.
- **The edition-49 "forward-looking calendar aggregator" trap (names falsely
  listed as past or future reporters when the actual date differs) remains
  closed as a general pattern.** Not independently re-tested at edition 61
  (no new instance found or needed); continue checking any carried-forward
  calendar assumption against its primary source before it becomes
  load-bearing, as edition 60 did for the CFTC report date and the 13F
  deadline (both now correctly logged as Monday 16 November 2026 below).
- **A megacap multi-name earnings cluster producing genuinely uncorrelated
  reactions is a standing, repeated pattern — now at least FOURTEEN distinct
  instances through edition 61 (editions 44, 47, 48, 49 x2, 50, 52, 53 x3,
  58, 59, 60, 61).** Edition 61 added: Hims & Hers fell 16.61% on margin
  compression despite a revenue beat, while Rocket Lab rose 6.54% on a clean
  beat-and-raise — both reported the same Monday evening. Continue treating
  beat-and-raise (or a guidance cut) as having no *guaranteed* effect on the
  reaction without checking the actual outcome.
- **New production lesson from edition 53: CSS multi-column (`.cols3`/
  `.cols2`) pagination under Chromium print-to-PDF can plateau stubbornly on
  marginal content trims; edition 60 hit the most severe version of this
  plateau yet and found a clearer fix (documented under Production Notes
  below). Editions 61 and 62 both needed none of this** — both converged
  cleanly to 4 pages on the first render with the forced break kept, no
  overflow, no stray break, a reminder that most editions do NOT need
  multi-round trimming and the elaborate lessons from 53/60 are a toolkit for
  when genuine overflow happens, not a default expectation.
- **MAJOR UPDATE at edition 59 (bug recurrence) — the VIX feed's two known
  bugs continue to toggle unpredictably.** Pattern to date: clean for four
  straight editions (55-58), recurred for one edition (59), then clean again
  for FOUR straight editions (60-62 — re-verified by manual recomputation
  each time, absent each time). Continue the manual-calculation discipline
  unconditionally regardless of how many bug-free editions precede the
  current one.
- **New at edition 54: a markup-correctness self-check caught three
  instances of the `</td><sup` table trap (documented under Production
  notes below) before rendering.** Editions 55 through 62 all ran the same
  proactive `grep -n '</td><sup'` check and found **ZERO instances for an
  EIGHTH consecutive edition** — worth continuing on every edition with a
  table that has an empty trailing cell or a cell containing only a
  citation.
- **New at edition 54: the CFTC Asset-Manager-vs-Leveraged-Funds grouped-bar
  chart was reused for a fifth time (editions 34, 39, 44, 49, 54 — a clean
  Monday/weekend-window pattern) with the same figsize (9.8, 2.15), `h=0.32`
  bar offset and figure-level legend technique documented under Production
  Notes.** **No edition since 54 has used it** — no fresh CFTC data has
  fallen inside any window since (the Friday 6 Nov report, covering Tuesday 3
  Nov data, was edition 59's; edition 62 confirmed the current report on file
  still covers 3 Nov data, so nothing has changed). **The next report is due
  Monday 16 November 2026**, covering Tuesday 10 November data — this falls
  inside **edition 65's** plausible window (one edition per weekday, no gaps
  assumed: 62 Wed 11, 63 Thu 12, 64 Fri 13, 65 Mon 16). **The "is CFTC moving
  to twice-weekly releases" question is now RESOLVED at edition 62, via a
  direct fetch of cftc.gov's own release-schedule page: the 16th and 30th are
  both explicitly flagged on that page as holiday-delayed single weekly
  releases, not evidence of a schedule change.** Drop this sub-question from
  future watch lists; just check cftc.gov directly at edition 65 as usual for
  the report itself.

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
  **Editions 54 through 59 all converged cleanly within one or two renders**
  (54 and 59 after deleting the one forced break; 55 through 58 all on the
  very first render with the break retained). **Edition 60 broke that
  quick-convergence streak** for a new reason (an Annex-C column-balance
  effect, see Production Notes), needing roughly eight iterations. **Edition
  61 converged cleanly on the very first render**, break retained, sections
  1-6 ending within page 3 — back to the common, fast case. Always check
  which situation you're in (stray break vs. genuine overflow vs. spillover
  that just needs the break deleted vs. a lonely trailing block pinned by a
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
  **Edition 60 merged SEVEN separate central-bank-website citations into a
  single shared Annex C number**, since all nine non-Fed bank table cells
  were fresh-checked by the same "visit each bank's own site directly"
  method — a legitimate, recommended pattern when several distinct URLs
  really do share one verification method. **Citing the prior edition
  itself as a source** (e.g. "logged prior-session baseline figures," or
  re-citing a prior edition's own already-primary-confirmed fact) is a
  legitimate, already-used pattern.
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
  corrects nothing**, which will be most of them. **Editions 54 through 61
  have all omitted the box** — in each case nothing published in a prior
  edition was found to be wrong. (Edition 61 specifically: the Nvidia
  board-investigation story, excluded as uncorroborated at edition 60, was
  NOT a wrong publication to correct — edition 60's own published text never
  claimed it was false, only that it couldn't yet be confirmed. Edition 61
  simply confirmed it as a new development; see the dedicated Standing Facts
  entry. A genuine published-figure correction would still get the box.)
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
  a matching Annex B entry. **Editions 54 through 62 have all run the same
  full 10-row table** (Fed, BoJ, BoE, ECB, BoC, RBA, SNB, Norges Bank,
  Riksbank, Banxico). **Edition 62 narrowed the table's one remaining gap:**
  Banxico's rate and vote are now primary-source confirmed (closing a
  long-running secondary-only gap), leaving only its next-decision date
  unavailable — the smallest "unavailable/imperfect" footprint this table
  has carried since it was introduced. Follow the usual table convention —
  plain `<tr>` header rows, no `<thead>`.
- **Charts: two fixed, a third only when earned — changed at edition 49.**
  The **sector-ETF performance chart always goes in Section 1**, beside the
  sector narration it illustrates, and the **single-stock movers bar always
  goes in Section 2**, with the names. Neither may duplicate a table.
  A **third chart is allowed only when positioning or volatility is
  genuinely the day's dominant story** — not merely present, and never to
  fill a short page — and it goes in the section it belongs to: CFTC
  asset-manager vs. leveraged-funds positioning or a VIX term structure in
  Section 5, an implied-vs-realized earnings bar in Section 2. **Edition 61
  did not use a third chart** — the VIX complex eased modestly in clean
  contango (a continuation of Monday's un-inversion, not a fresh dominant
  story) and no fresh CFTC data fell inside the window; judged genuinely
  secondary and covered fully in prose. **Next CFTC report due Monday 16
  November 2026** (edition 65's likely window), covering Tuesday 10 November
  data — check cftc.gov directly then.
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
  editions 56 through 61.
- Where sources disagree, use the more authoritative one **and** disclose
  the disagreement. AP's "How major US stock indexes fared" and the Reuters
  market wrap are normally the most reliable for index closes — but check
  they're actually indexed for the target date before relying on them. The
  dual WTOP.com/lanacion.com.ar AP-wire-mirror approach remains the
  established first-choice workaround when apnews.com/Reuters are blocked
  directly — **now NINE consecutive successes (edition 62 again used both
  WTOP and lanacion.com.ar together, word-for-word identical, cross-checked
  further against Yahoo Finance)**. Try this before the Yahoo-Finance-plus-
  secondary-recap fallback, while still re-attempting apnews.com/Reuters
  directly every edition regardless.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Always check a dated article's own claimed magnitude AND
  direction against the underlying price-history table or primary filing,
  not just its date, before repeating it** — this trap has now hit
  magnitude, direction/framing, claimed drivers that don't hold up, a
  claimed analyst action that appears outright fabricated, the claimed
  DATE/YEAR itself, a disclosed cross-source percentage-methodology
  discrepancy, a figure with no corroborating primary filing at all, a
  wholesale stale-date republish, and (edition 60's most severe instance
  yet, see the dedicated Standing Facts entry) a dramatic claim that one
  research pass reported as apparently true before a direct follow-up found
  no support. **Edition 61 added the mirror-image lesson: the SAME dramatic
  claim, re-checked with fuller search effort, turned out to be true after
  all** — see the dedicated Standing Facts entry. Treat ANY surprising
  secondary claim (price move, driver, analyst action, date, or computed
  percentage) as needing a genuine, thorough verification attempt before
  either accepting or rejecting it — not a single search in either
  direction.
- Run a dedicated verification pass on any figure two research passes
  disagree on, or any single surprising/highly-consequential finding, before
  publishing — cheap, and has caught real errors (and, at edition 61,
  corrected an overly-cautious prior exclusion) before. **Edition 61
  exercised this discipline directly (via the coordinator's own WebSearch
  and WebFetch, not a delegated pass) on the Nvidia board-investigation
  claim specifically because of its history at edition 60** — this is the
  clearest demonstration yet that the discipline should run a genuinely
  independent, persistent check with varied phrasing, not just ask a third
  subagent to adjudicate or accept a single search's negative result as
  final.
- **Premarket is not the close, and the close is not the after-hours
  earnings reaction — and an after-hours reaction does not necessarily hold
  into the next regular session, uniformly or at all. A strong beat-and-raise
  does not guarantee a positive reaction even within the SAME session —
  though it does not guarantee a negative one either.** Reinforced at
  essentially every edition since 44, most recently at edition 61 (Hims &
  Hers fell 16.61% on margin compression despite a revenue beat; Rocket Lab
  rose 6.54% on a clean beat-and-raise, the same earnings morning). Always
  fetch the verified close, the after-hours reaction, AND (when the window
  allows) the next regular session's close as three separate, clearly
  labelled figures. A premarket-only or regular-session-only figure that
  predates a same-evening earnings release should be labelled as such rather
  than implied to be a reaction to it.
- **The DXY-vs-its-own-FX-crosses conflict is genuinely intermittent —** a
  minor cross-vendor gap persisted at edition 62 between Yahoo Finance's
  DX-Y.NYB (102.84) and an Investing.com futures-style DXY proxy (102.88),
  narrower (approx. 4bp) than edition 61's approx. 7bp gap, though both
  agreed closely on Tuesday's base. Keep disclosing the DXY-vs-FX-crosses
  comparison every edition regardless of which way it goes.
- **The Kitco live-spot-vs-headline cross-check remains in its fourth
  failure mode (total inaccessibility) for a FOURTH consecutive edition at
  edition 62** — not a new mode, see the dedicated Standing Facts entry
  above. No Kitco historical-close figure is reported for Wednesday 11 Nov as
  a result.
- **GBP/USD, EUR/USD and USD/JPY all reconciled cleanly again at edition 62**
  against their logged Tuesday base, with no revision on any of the three.
- **The 2-year Treasury yield conflict from edition 36 remains resolved, but
  edition 62 had nothing fresh to check against it** — Treasury cash markets
  were closed for Veterans Day, so home.treasury.gov posted no new TextView
  row for 11 Nov; Tuesday's curve (2-year 4.73%, 10-year 4.98%, 30-year
  5.35%) remains the most recent official print. Resume the normal
  every-edition reconciliation once Treasury markets reopen.
- **The Investing.com displayed-%-vs-computed-% divergence flagged as a new
  standing data-quality issue at edition 60, absent at edition 61, was NOT
  explicitly re-checked at edition 62** — worth a direct look again next
  edition rather than assuming either state persists, since it has
  previously toggled on/off.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 62 have all run clean (or
  clean after quick fixes) — **edition 62 needed ZERO fixes** (35/35 sources
  matched on the first check, the highest source count run yet, reflecting a
  dense multi-earnings session).
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 62 have all rendered with zero stray tildes on the
  first draft, bar editions 56 and 57 which each needed one fix** — a
  reminder that the fix/no-fix pattern doesn't correlate cleanly with
  content density (edition 62 had the densest content yet and still needed
  zero fixes).
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39, 44, 49 and 54 have
  all resolved this cleanly for CFTC CoT. Not applicable at editions 55
  through 61 (no fresh CFTC data triggered the chart in any of those
  windows). The next report (due Mon 16 Nov, covering Tue 10 Nov data)
  falls inside edition 65's plausible window.
- **The diffuse-overflow lesson from editions 44-45 and the duplicated-
  content lesson from edition 47 are both still worth checking first on any
  overflow** — but edition 53 showed overflow can also be genuinely dense
  content requiring real trimming, edition 54-58 showed the opposite, and
  edition 60 showed a third distinct cause (an Annex-C column-balance
  effect). **Edition 61 needed no overflow fix at all** — first render
  converged cleanly. Always check which situation you're in before assuming
  a particular fix is the answer.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — **specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation.** No capping
  has been needed in any edition since 45. Edition 61's movers chart (7
  categories, HIMS -16.61% largest, SKYD -7.59% second largest) had a ratio
  of approx. 2.19x; used `pad_frac=0.26` with figsize (9.8, 1.80) — rendered
  cleanly, same settings as edition 60's 8-category panel. Edition 62's
  movers chart (6 categories, CRWV +24.71% largest, SONO +12.85% second
  largest) had a ratio of approx. 1.92x; used `pad_frac=0.28` with figsize
  (9.8, 1.70) — rendered cleanly. `pad_frac=0.30` for the 11-category sector
  panel has now rendered cleanly across seventeen editions (45-50, 52-62).

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`, under the `quotes/` path
  specifically — `charts/_VIX.json` returns 403, `quotes/_VIX.json` works).
  **Editions 28 through 62 have all got a fresh, same-day-timestamped
  sweep** — thirty-five consecutive fresh sweeps now. **The feed's two known
  bugs (a duplicated `prev_day_close`, and a `price_change_percent` that
  divides by current price instead of prior close) toggle unpredictably:
  present at edition 54, absent 55-58, present at 59, absent again at 60, 61
  AND 62** (now a three-edition clean streak) — always compute day-over-day %
  change manually regardless of how many consecutive bug-free reads preceded
  the current one. **Edition 62's own session: a sharp easing across the
  curve in continued ascending contango, consistent with the broad equity
  rally** — VIX -10.12% to 17.49, VIX9D -13.48% to 16.04, VIX3M -6.78% to
  19.24, VIX6M -4.14% to 21.08, VVIX -6.37% to 90.47, SKEW -1.34% to 149.09
  (last_trade_time 16:15:01 ET for the first five, 17:00:19 ET for SKEW).
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 62 fetched all 11 directly again**
  (Technology +3.23% the leader on CoreWeave/Nvidia, Energy +1.86% and
  Industrials +1.33% also outperforming; Consumer Discretionary -0.05% the
  lone, barely-negative laggard; 10 of 11 closed higher, a materially
  broader advance than Tuesday's 6-of-11 split) — continue this
  direct-fetch-by-default method. **A secondary cross-check (MarketWatch/WSJ)
  could not be fetched at edition 62 either** — single-sourced for a third
  straight edition, disclosed in Annex A; try the cross-check again at
  edition 63.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (0 of 11 at edition 58; 3 of 11
  at edition 59; 11 of 11 at edition 60; 6 of 11 at edition 61; **10 of 11 at
  edition 62**, a materially broader advance) — no competing secondary-
  aggregator breadth figure was checked at edition 62 either.
- **Dealer gamma:** zerogex.io hit a **TWENTY-THIRD consecutive edition of
  failure at edition 62** (all widgets still show placeholder dashes with no
  timestamped data). SpotGamma logged a **SEVENTEENTH straight failure at
  edition 62** (no dated NVDA/SPX content specific to the session; most
  recent relevant note still dated 4 Nov). Both sources remain fully
  unusable.
- **Official CME FedWatch probabilities:** the page blocks fetching
  (edition 62's direct attempt returned HTTP 403, a new failure signature
  vs. the prior timeout, a **TWENTY-SECOND** consecutive failure, 41-62) —
  use secondary citations (Polymarket, Kalshi, Reuters/other economist
  polls, desk notes) and give a range rather than a single invented number.
  **Polymarket direct, tried via its Gamma API
  (`gamma-api.polymarket.com`) rather than a plain site visit, succeeded
  again at edition 62 — a NINTH consecutive success** — this remains the
  preferred first approach; try it before reverting to a plain site visit.
  **DeFi Rate's blended aggregator also returned a fresh,
  same-day-timestamped read again at edition 62** — continue the
  cross-check discipline against it.
- **Kalshi direct fetch:** rate-limited or blocked across every edition it
  has been attempted, now **TWENTY-SIX consecutive failures (37-62)** — a
  confirmed structural gap, not transient. **Edition 62's failure mode was
  HTTP 000/connection failure** (a third distinct signature, after HTTP 429
  and HTTP 401) — worth continuing to log the specific signature each time
  in case a pattern emerges. Resume the attempt-every-edition discipline at
  edition 63 regardless. Use Kalshi's own secondary reporting or DeFi Rate's
  blended aggregator as the workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **westmetall.com (LME copper): the cash
  series stayed clean at edition 62, and the 3-month series' long-standing
  "query-parameter problem" is now RESOLVED AT THE ROOT — there never was a
  queryable historical 3-month field.** See the dedicated Standing Facts
  entry above; stop trying new access variants, simply report the
  current-day 3-month print going forward.
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **had nothing fresh to check at edition 62**
  — Treasury cash markets were closed for Veterans Day, confirmed directly
  (no new row posted for 11 Nov). Tuesday's curve (2-yr 4.73%, 10-yr 4.98%,
  30-yr 5.35%) remains the most recent official print; the clean-streak
  count (twenty-six editions, 37-61, with no repeat of the edition-36 33bp
  gap) is paused, not extended, pending a fresh print once markets reopen.
  Continue scoping the TextView URL to the specific month
  (`field_tdr_date_value_month=202611`-style parameter) rather than the
  full year.
- **CFTC CoT:** publishes with the prior Tuesday's data — always state the
  lag explicitly. `financial_lf.htm` works well for equity index futures
  (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). **No new report fell inside edition 62's window** (the most
  recent, covering Tuesday 3 Nov data, was released Friday 6 Nov and fully
  summarized at edition 59) — confirmed directly against cftc.gov's index
  page, no early release occurred. **The next report is due Monday 16
  November 2026**, covering Tuesday 10 November data — this falls inside
  **edition 65's** plausible window (if no gap); check cftc.gov directly
  then. **RESOLVED at edition 62: the irregular November spacing (6th,
  16th, 20th, 30th) is confirmed, via cftc.gov's own release-schedule page,
  to be holiday-delayed single weekly releases — NOT evidence of a shift to
  a twice-weekly schedule.** Drop this sub-question from future watch lists.
- **GBP/USD, EUR/USD, USD/JPY clean close:** all remain fully resolved,
  reconciling cleanly again at edition 62 (EUR/USD 1.1090 -0.66%, GBP/USD
  1.3276 -0.51%, USD/JPY 159.78 +0.64%, all single-sourced to Investing.com's
  close-to-close history table, Tuesday base matching exactly). **DXY itself
  showed a narrower (approx. 4bp) renewed cross-vendor gap at edition 62** —
  see the dedicated Hard Rules entry above.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **The Kitco
  live-spot cross-check remains in its fourth failure mode (total
  inaccessibility) for a FOURTH consecutive edition at edition 62** — see the
  dedicated Standing Facts and Hard Rules entries above; no Kitco historical
  figure is reported this edition either. **A fresh vendor-retroactive-
  revision instance hit gold/silver's Tuesday base this edition** (gold
  revised $4,046.20→$4,030.20, silver $51.563→$51.225 — see the dedicated
  Standing Facts entry); Wednesday 11 Nov futures figures: gold futures
  $3,983.85 (-1.15%), silver futures $51.240 (+0.03%), both reconciled
  cleanly against the (revised) Tuesday base via Investing.com.
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **China Q3 GDP** is also a closed thread as of
  edition 45. **US GDP, PCE, import/export prices and industrial
  production:** all closed threads — see Standing Facts above. **University
  of Michigan October consumer sentiment** is a closed thread as of edition
  49. **China's October PMI** is a closed thread as of edition 54. **October
  ISM Services PMI** is a closed thread as of edition 57 (headline only;
  sub-index detail remains an Annex B item). **October US CPI** is now a
  closed thread as of edition 61 — see the dedicated NEW Standing Facts
  bullet above (including the unusual missing-y/y wrinkle). **October US
  PPI** is due Friday 13 November 2026, 8:30am ET, confirmed directly
  against the BLS's own release schedule (edition 64's likely window) —
  still live; a consensus figure found at edition 62 had internally
  inconsistent formatting and was not reported.
- **Henry Hub natural gas:** the front-month-contract-identity question
  remains resolved (NGZ6/December, no roll to NGF7/January yet as of 11
  Nov). **The base-price reliability problem — this report's historically
  worst-performing data-quality issue — has now stayed open for a SECOND
  straight edition at edition 62** (Wed 11 Nov: Investing.com $3.246 vs.
  Yahoo $3.264, approx. 55bp gap on computed % change), after breaking a
  five-edition clean streak at edition 61. Continue the every-edition
  two-source reconciliation discipline rather than the occasional-spot-check
  cadence, until a fresh clean streak re-establishes.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **CoreWeave's Q3 2026 results and
  regular-session reaction, unverified at edition 61's cutoff, were fully
  resolved at edition 62** (see the dedicated Standing Facts entry) — but
  **optionslam.com's CRWV figures remained unlabeled and unusable for an
  options-flow read at edition 62 too**: the page showed figures (approx.
  19.0%/4.81%) that could not be confirmed as the pre-earnings implied move,
  and no dated post-earnings options-flow/gamma commentary for CRWV could be
  found elsewhere either. Treat the general sub-item as low-yield most
  editions but worth a genuine attempt every time.
- **Weekend equities catalyst to watch: 13F filings.** The Q3 2026 deadline
  (corrected at edition 60 from the previously-assumed "approx. 14 Nov") is
  confirmed **Monday 16 November 2026** (45 days after the 30 Sept
  quarter-end, rolled from Saturday 14 Nov). This now coincides with the
  corrected CFTC CoT report date (also Monday 16 Nov) — both land in the
  same edition's window, likely edition 65 if no gaps.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22, not attempted
  again since). Revisit only if a future edition has spare research
  bandwidth on an FOMC day specifically — not relevant to most editions.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully at
  editions 39, 44-49, 54 and 59 (the Friday 6 Nov report, covering Tuesday 3
  Nov data: ES OI 1,986,532; NQ OI 292,587; RTY OI 449,399). No new report
  fell inside edition 61's window either. Repeat the three-instrument fetch
  whichever edition's window extends past Monday 16 November 2026 (likely
  edition 65), watching for the micro-vs-full-size naming trap each time,
  and for whether the twice-weekly-release schedule change has actually
  begun (see the CFTC CoT entry above).
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 58 found
  no analyst action at all from the session could be independently
  verified; edition 59 and edition 60 both repeated that result, edition 61
  extended this to a fourth straight edition, and **edition 62 extends it to
  a FIFTH consecutive edition with zero verifiable analyst actions** — a
  widely-circulated 24/7 Wall St. roundup's claimed upgrades were
  spot-checked against independent sourcing and found to contradict it
  (e.g., on Mercury Systems), so excluded entirely rather than repeated.
  Watch each edition independently rather than assuming a trend, but this is
  now a five-edition pattern.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** This discipline has now caught numerous fabrications
  and errors (full list in the Standing Facts "named secondary outlet"
  entry above), gained its most important nuance yet at edition 61 (a
  previously-excluded claim turning out to be TRUE on fuller re-verification
  — see the dedicated Nvidia Standing Facts entry), and caught another clean
  exclusion at edition 62. Every reported single-stock mover at edition 62
  (CRWV, SONO, TSM, NVDA, GO, RGTI) was individually cross-checked against
  its own primary SEC filing where tied to earnings, or against a direct
  price-history fetch otherwise — continue this direct-verification
  discipline on every edition. A claimed International Money Express/Western
  Union tie to the Intermex deal deadline was investigated and excluded
  entirely for lack of primary confirmation (and a counterintuitive
  direction), see the dedicated Standing Facts entry.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted since (out of scope each time); try an alternate DOL
  page or a secondary economic-calendar aggregator for the consensus figure
  when next relevant.
- **federalregister.gov's direct search interface remains blocked** (a prior
  search attempt 302-redirected to `unblock.federalregister.gov`, an
  apparent bot/rate-limit gate, first logged at edition 48) — not
  independently re-tested at edition 62 (the developer API route below made
  the search UI unnecessary again). govinfo.gov continues to be a known
  working alternative route for at least some Federal Register content.
  **The Federal Register's own developer API
  (`federalregister.gov/api/v1`) is now confirmed useful for more than single-
  document lookups**: edition 61 used `documents/<doc-id>.json` to resolve
  the Section 301 question decisively; **edition 62 used a date-range query
  of USTR's recent filings** to check for a reciprocal-tariff-truce document
  (found none, see Standing Facts) — a second consecutive success for this
  access path as the recommended first approach whenever the search UI is
  blocked, even for an open-ended "has anything been filed" question rather
  than a known document ID.
- **SEC EDGAR's `cgi-bin/browse-edgar` company-search page (filtered by CIK
  and form type 8-K) is a highly reliable, fast way to confirm both WHETHER
  a company has reported on a given date and to find the accession number
  for the underlying exhibit** — used again at edition 62 for CoreWeave,
  Sonos, Rigetti and Grocery Outlet, and again for confirming NVIDIA has
  filed NO new 8-K as of this cutoff (a genuine negative finding, not a
  failed fetch, for a second straight edition) — reinforcing edition 58's
  lesson that this tool is just as useful for debunking/confirming an
  absence as for confirming a presence. **Edition 62 also used EDGAR's
  company-filing-HISTORY view (not just an 8-K date check) to resolve the
  SKYD/PSKY ticker-identity confusion** — a new, generalizable use: when a
  ticker's identity itself is in question, EDGAR's own filer history (CIK
  name-change log) resolves it directly.
- **ECB's current policy rate: SETTLED since edition 55** (unchanged through
  the 28-29 October 2026 meeting: deposit facility 2.50%, main refi 2.65%,
  marginal lending 2.90%); not re-attempted at editions 56 through 62 (no
  fetch needed). It reopens on contradiction, the next Governing Council
  decision, or the monthly audit. The Council's own next-meeting date is
  SETTLED at 16-17 December 2026.
- **NFIB Small Business Optimism Index:** nfib.com returned HTTP 403 again
  at direct fetch at edition 62 — now a confirmed two-edition pattern, not a
  one-off. **The workaround that worked at edition 62: Trading Economics**,
  which carried the October reading (97.8, down 0.1pt from September,
  released 10 Nov per TE's own page) — use Trading Economics as the default
  fallback for this specific release when nfib.com blocks direct access.
- **Banxico's next policy-decision date** is now the one remaining Banxico
  gap (the rate and vote themselves were primary-confirmed at edition 62 —
  see the dedicated Standing Facts entry). The 5 Nov press release does not
  state a next-meeting date; the previously-carried approx. 17 Dec 2026
  figure was secondary-sourced only and could not be reconfirmed from the
  primary document. Try Banxico's own published monetary-policy-decision
  calendar page specifically (a distinct URL from the decision press
  release itself) at edition 63.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel —
  confirmed clean again at edition 62 (twenty-three editions total: 37-43,
  45-50, 52-62). For charts with fewer categories, scale the height down:
  roughly `(9.8, 1.65-1.95)` for 3-9 categories. **Edition 62 used `(9.8,
  1.70)` for a 6-category movers chart with `pad_frac=0.28`**, rendering
  cleanly across a -8.56% to +24.71% range (ratio approx. 1.92x). **Always
  render and visually inspect (via the Read tool) the actual PNG at or near
  full resolution before embedding it**, regardless of what a past edition's
  success might suggest. **Default to pad_frac=0.30 from the start for an
  11-category sector-ETF panel** — now confirmed across seventeen straight
  small-magnitude 11-category panels (45-50, 52-62). For any movers chart
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
  threshold, including edition 61's approx. 2.19x and edition 62's approx.
  1.92x) — reinforcing that the trigger is the ratio to the next-largest bar,
  not the largest bar's
  absolute size.
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
  `@page` block is the pattern that has worked reliably — edition 62 used
  this exact pattern again with no issue.
- **At most ONE forced `page-break-before` in the whole document:
  immediately before Annex A — and on a spillover edition, none at all.**
  Let sections 1-6 flow naturally; never add a break between them. The rule:
    - Sections 1-6 end on page 3 (the common case) → keep the break. The
      annex opens a clean page 4, exactly as before. **Editions 61 and 62
      were both this case**, each converging on the first render.
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
  **Editions 61 and 62 both confirmed 1**, the common case.
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
  default (`balance`) remains the right choice. **Lesson: if a trailing
  element right after a `.cols2`/`.cols3` block is alone on an otherwise-
  blank extra page, first measure (e.g. with a quick visual read of the
  rendered page PNGs) whether the multi-column block itself is already
  using nearly the full remaining page. If so, trim THAT block's own
  list-item text, not the prose before it** — and expect that even fairly
  large cuts to the preceding prose will show zero visible effect until you
  do. Not needed at editions 61 or 62 (both clean first-render convergence).
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix.
- **A markup-correctness trap, logged at edition 47: a `<sup class="ref">`
  citation tag placed immediately after a table row's last `</td>` but still
  inside the `<tr>` (i.e. not nested inside any `<td>`) is invalid table
  structure.** `check_refs.py` will NOT catch this. **Always nest every
  `<sup class="ref">` tag inside a `<td>...</td>` pair, never as a sibling of
  one inside a `<tr>`** — grep for `</td><sup` as a quick self-check if a
  table was built with a lot of copy-paste. **Editions 55 through 62 all ran
  the same proactive grep and found zero instances, an EIGHTH consecutive
  clean sweep.** Run the grep on every edition with such a table, not just
  when troubleshooting a layout problem.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count
  alone. **Editions 61 and 62 each needed only the standard single pass** —
  both first renders were 4 pages, all four page images read and confirmed
  clean each time (no overflow, no stray break, good margins, annex
  well-filled on page 4), no trim/fix iterations needed. Edition 62's source
  count (35) was the highest yet carried cleanly through check_refs on the
  first try, confirming the shared-citation-merging convention scales fine
  to a denser multi-earnings session.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across many editions'
genuinely different content volumes, including editions 53's through 62's.
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
  runs short — editions 44 through 62 have all folded commodities, FX and
  Treasuries into ONE combined table (10-17 rows; edition 61 used 15, edition
  62 used 14) as the PRIMARY commodities table rather than padding, now the
  standing default.
  **Always re-render immediately after adding (or removing) any content to
  confirm the page count — and if a change to Annex A/B text doesn't move
  the page split at all, suspect the Annex C column-balance effect above
  before assuming the edit silently failed to save.**

**Chart selection guidance.** Placement is not editorial for the first two
charts:

- **Sector-ETF performance chart → Section 1 (Market recap), every
  edition.** Same-day closes by default; a grouped day-over-day bar instead
  on a multi-session or weekend window, or on a genuine multi-sector
  broadening selloff across consecutive sessions. **Editions 61 and 62 both
  used a single-day bar** (each window held only one NYSE session).
- **Single-stock movers bar → Section 2 (Equities), every edition.**
- **A third chart only when positioning or volatility is genuinely the
  day's dominant story**, never to fill a page, placed in the section it
  belongs to:
  - Fresh CFTC CoT data → the ES/NQ/RTY asset-manager-vs-leveraged-funds
    positioning chart, normalized as % of open interest, built with the
    grouped-bar technique documented under Production notes, in **Section
    5**. Editions 24, 34, 39, 44, 49 and 54 have all placed it there; none
    of editions 55 through 62 had fresh data available inside their own
    windows. The next opportunity (the corrected Monday 16 Nov report) falls
    inside edition 65's plausible window.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully. Not used at editions 55
    through 62 — edition 61's optionslam.com fetch returned a CoreWeave
    implied-move figure but it appeared stale/pre-earnings; **edition 62
    confirmed CoreWeave's actual results and regular-session reaction
    (+24.71%) but optionslam.com's figures remained unlabeled/unusable as an
    implied-move source even after the earnings date passed**, so this
    chart still was not built.
  - A holiday-window preview edition with no fresher data → VIX futures
    term structure with event annotations, in **Section 5**. Not used at
    editions 55 through 62 — in each case the VIX term structure was
    genuinely newsworthy but judged secondary to the session's dominant
    equity/macro story each time and was covered fully in prose instead.

**Edition 63 (expected to cover Thursday 12 November 2026, assuming no gap —
a normal full session, no holiday).** Verify directly rather than assuming:
- **Whether December FOMC hike odds (approx. 85-86% as of editions 61-62,
  now unchanged across two straight reads) hold into a THIRD quiet edition,
  finally move, or get a fresh catalyst** — a fresh Polymarket/DeFi Rate pull.
- **Midterm-election certification status** — now structurally explained
  (no national step; state deadlines into December, see Standing Facts), but
  worth a quick check of any state deadline that lands inside edition 63's
  window specifically (none identified yet before 19-23 Nov).
- **Banxico's next policy-decision date** — the rate/vote are now primary-
  confirmed (edition 62), but the next-meeting date is a fresh gap; try
  Banxico's own monetary-policy-decision calendar page specifically.
- **A primary-source document for the reciprocal-tariff-truce extension to
  10 January 2027** (currently secondary-sourced only, attributed to
  Treasury Secretary Bessent) — try USTR/White House/Federal Register again;
  two straight editions of Federal Register API queries have found nothing.
- **Henry Hub's cross-vendor reconciliation** — resume the every-edition
  discipline; the gap has now persisted two straight editions (61-62) after
  a prior five-edition clean streak.
- **A secondary (MarketWatch/WSJ) cross-check for the sector-performance
  table** — unavailable for three straight editions now.
- **The Investing.com displayed-%-vs-computed-% divergence** (flagged at
  edition 60, absent at edition 61, not explicitly re-checked at edition 62)
  — worth a direct look given it has previously toggled on/off.
- **Any further genuine (primary-sourced) development on the Nvidia/Huang
  story** (an eventual 8-K, investigation findings, a hearing actually
  occurring) — edition 62's fresh EDGAR check again found nothing new;
  continue checking directly rather than assuming the story has gone quiet.
- **US Treasury par yields** — markets reopen Thursday after the Veterans
  Day closure; resume the normal every-edition reconciliation against
  home.treasury.gov.
- **October PPI** is due the following day, Friday 13 November 2026, 8:30am
  ET — confirmed on the BLS's own schedule; this is edition 64's window, not
  63's, but worth flagging in edition 63's day-ahead table.
The WTOP/La Nación AP-wire-mirror approach and the Polymarket Gamma-API
approach are both now on nine-edition clean streaks — use them first rather
than their respective fallbacks. **Remember the edition-60 Annex-C-trimming
lesson if a trailing element gets pinned alone on an extra page again** — it
is a recognized, specific failure mode with a specific fix, not a mystery to
re-diagnose from scratch. **Remember the edition-61 Nvidia lesson generally:
a dramatic claim, once directly and thoroughly checked, can turn out to be
true — don't default to permanent suspicion any more than to automatic
acceptance.** **Remember the edition-62 lesson on structural vs. researchable
gaps: not every "unconfirmed" item is a research failure waiting on more
effort — the midterm-certification and LME-3-month-copper threads both
turned out to be genuinely structural once investigated thoroughly enough to
tell the difference, and the fix was to stop re-trying and start reporting
the structural explanation instead.**

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

**Edition 61's carried-forward spec was 123,518 bytes, over the
100,000-byte threshold — this run (producing edition 62's spec) condenses
the log.** Edition 60's own medium-paragraph entry is folded into the
running mega-block (now "Editions 1-60"); edition 61's own full-detail entry
is condensed down to a medium paragraph; edition 62 is added in full detail.
There is no maximum size; condensing is housekeeping done by the run itself,
not a check to pass — there is no penalty for the file staying somewhat
large if the alternative is losing information.

**Editions 1–60 (condensed):** established the format (edition 1 baseline;
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

Edition 59 (Mon 9 Nov, covering Fri 6 Nov): a much-stronger-than-expected
October jobs report (nonfarm payrolls +165,000 vs. approx. +65,000
consensus, unemployment 4.1%) snapped December FOMC hike odds from edition
58's approx. 66.5% back to approx. 76.5-77%, against a narrow, chip-led
relief rally (S&P +0.3%, only 3 of 11 sectors higher) that only partly
reversed Thursday's AI-capex rout; a widely-surfaced "Friday close" figure
was found to be a stale Thursday republish and excluded; a fresh round of
the vendor-retroactive-revision trap hit WTI/gold/silver/COMEX copper, and
Kitco's historical-close pages became inaccessible for the first time.
Edition 60 (Tue 10 Nov, covering Mon 9 Nov): an 11-of-11-sector relief
rally (S&P +2.3% to 7,549.94, its best day since 8 April) coincided with a
sharp oil-price crash (WTI approx. -4.8%, Brent approx. -5.9%) on an Iran
de-escalation signal, while December hike odds extended further hawkish to
approx. 77-82%; the chip complex's rally lifted every name except Nvidia
(-4.27% to $178.67, tied to the Megaspeed/Alice Huang overhang), and a
dramatic board-investigation claim was investigated and excluded as
uncorroborated at the time — overturned as TRUE the very next edition (see
the dedicated Nvidia Standing Facts entry in the current spec). The CFTC's
assumed "next report" date was corrected from approx. 14 Nov to Monday 16
November 2026, also becoming the corrected Q3 13F deadline. First draft hit
a new Annex-C column-balance overflow symptom (a trailing Method note
stranded alone on page 5 despite the forced break being deleted), fixed by
trimming Annex C's own entries directly rather than preceding prose (see
Production Notes).

**Edition 61** (Wed 11 Nov, covering Tue 10 Nov): October's hot CPI print
(headline +0.4% m/m, core +0.3% m/m, but BLS published no y/y figures at
all — a genuine data gap tied to the 2025 appropriations lapse) firmed
December FOMC hike odds to approx. 85-86%, a fourth consecutive hawkish
extension, against a modest mirror-image pullback (S&P -0.4% to 7,520.93,
breadth close to even at 6 of 11 sectors higher, Technology the laggard at
-1.15%). The edition's most significant finding: Nvidia's board-
investigation story, excluded as uncorroborated at edition 60, was
independently re-verified and found TRUE via NVIDIA's own 8 and 10 November
newsroom statements and top-tier wire corroboration (Washington Post, NBC,
CBS, Axios, TechCrunch, Fox Business) — no 8-K filed on the matter as of
that cutoff; NVDA fell a third straight session (-5.47% to $168.89). Other
movers: Hims & Hers -16.61% (margin collapse despite a revenue beat),
Skydance Corp -7.59% (driver unverified, confounded with Paramount
Skydance/PSKY), Intel -2.09%, Broadcom +3.91%, Lucid +4.72%, Rocket Lab
+6.54% (record Q3, first positive operating cash flow quarter). The
Section 301 178-product tariff-exclusion lapse resolved via a fresh USTR
Federal Register notice; Henry Hub's five-edition clean cross-vendor
reconciliation streak broke; Riksbank's vote split and Banxico's
primary-source confirmation (both resolved the next edition) remained
open; CoreWeave's Tuesday-evening Q3 report was entirely unverified by
this cutoff (also resolved the next edition). First draft converged
cleanly to 4 pages on the first render; 26/26 sources clean, zero stray
tildes.

**Edition 62 (most recent — full detail)** — Thursday 12 November 2026
report covering Wednesday 11 November 2026, research window Tue 10 Nov
2026 20:00 ET through Wed 11 Nov 2026 20:23 ET (the window's one NYSE
session — Veterans Day: equities traded a full normal session, Treasury
cash markets and the Federal Reserve were closed).

**The dominant story was a broad, CoreWeave-led equity relief rally that
reversed Tuesday's hot-CPI pullback, even as December FOMC hike odds held
steady rather than easing.** The S&P 500 rose 1.3% to 7,619.38, the Dow
0.5% to 52,486.49, the Nasdaq Composite 1.6% to 25,466.19 and the Russell
2000 0.9% to 2,846.26 — confirmed via AP's wire (WTOP.com/lanacion.com.ar
mirrors, cross-checked against Yahoo Finance). Ten of 11 SPDR sector ETFs
closed higher, led decisively by Technology (+3.23%, swinging from
Tuesday's worst laggard to Wednesday's best performer). A fresh
Polymarket/DeFi Rate pull put December FOMC hike odds at approx. 85-86%,
essentially unchanged from Tuesday — confirming the rally reflected risk
appetite rather than any dovish repricing.

**CoreWeave's (CRWV) Q3 2026 results, entirely unverified at edition 61's
cutoff, were the session's dominant single-stock story.** Revenue $3.661bn
(+168% y/y, beating its own guidance), a widened GAAP net loss on surging
interest expense, and raised FY2026 revenue guidance to $13.0-13.3bn,
confirmed via the company's own 8-K. The stock closed +24.71% at $60.77,
its best day since April 2025; Tuesday evening's after-hours reaction is
disclosed as genuinely disputed across vendors (approx. +2.4% to +7.9%)
rather than reported as a single figure.

**Two standing central-bank sourcing gaps closed against primary
documents.** Riksbank's 4 November vote, unresolved for four straight
editions, is now confirmed unanimous 5-0 via the bank's own primary
minutes. Banxico's 5 November cut to 6.25% (3-2 vote) is now
primary-source confirmed, matching prior secondary reporting exactly —
though its next-decision date, previously carried on secondary sourcing,
could not be reconfirmed and is now a fresh open item.

**Single-stock movers:** CoreWeave +24.71% (above), Sonos +12.85% (return
to growth, FY2026 results), TSMC +4.25% (board-approved Anthropic/OpenAI
preferred-stock investments), Nvidia +2.87% (broad chip rebound; no new
primary development on the governance story, confirmed via a fresh EDGAR
check), Grocery Outlet -6.42% (margin compression, goodwill impairment) and
Rigetti Computing -8.56% (Q3 revenue decline, widened operating loss). A
claimed International Money Express/Western Union tie to the Intermex deal
deadline was investigated and excluded for lack of primary confirmation. No
analyst action could be independently verified for a fifth straight
edition.

**Other resolved threads:** SEC EDGAR confirmed Skydance Corp (SKYD) and
Paramount Skydance (PSKY) are the same legal entity, resolving a standing
ticker-confusion thread (SKYD's own 10 Nov -7.59% driver remains
best-explained, not primary-confirmed, by analyst price-target cuts and a
Warner Bros. guidance warning). The CFTC's irregular November release
spacing was resolved as routine holiday-adjusted scheduling via the
agency's own release-schedule page, not evidence of a shift to
twice-weekly releases. LME 3-month copper's long-standing
"query-parameter problem" was traced to its root: westmetall.com has no
historical field for the 3-month series at all, a permanent structural
limitation, not an access problem to keep retrying. US midterm-election
certification was clarified as having no single national step at all
(certification is state-by-state into December) — a structural, not a
research, gap going forward. Henry Hub's cross-vendor reconciliation gap
persisted a second straight session; a fresh vendor-retroactive-revision
instance hit gold/silver's Tuesday base.

**Format:** no correction box. First draft converged cleanly to 4 pages on
the very first render — break retained, no overflow, no stray break, all
four page images read and confirmed clean. 35/35 sources clean with zero
fixes (the highest source count run yet); zero stray tildes; zero
`</td><sup` instances.

**Open threads for edition 63.** Edition 63 covers **Thursday 12 November
2026** (a normal full session), if no gap. Priority items: **whether
December FOMC hike odds (approx. 85-86%, unchanged across two straight
editions) hold into a third quiet read or finally move**; **Banxico's
next-decision date** (a fresh gap after the rate/vote itself was
primary-confirmed); **a primary source for the reciprocal-tariff-truce
extension to 10 January 2027** (two straight editions of Federal Register
API queries have found nothing); **Henry Hub's cross-vendor
reconciliation** (now a two-edition open gap); **a secondary
sector-performance cross-check** (unavailable three straight editions);
**the Investing.com displayed-%-vs-computed-% divergence** (not explicitly
re-checked this edition); **any further primary-sourced Nvidia/Huang
development**; and **US Treasury par yields** resuming their normal
every-edition reconciliation once markets reopen Thursday. **Dates to hold
on to** (one edition per weekday assumed: 62 Wed 11, 63 Thu 12, 64 Fri 13,
65 Mon 16). October PPI due Fri 13 November 2026 (edition 64). **The next
CFTC CoT report AND the Q3 13F filing deadline both fall on Monday 16
November 2026** (edition 65). BoE next decision 17 Dec 2026; the ECB's next
meeting 16-17 Dec 2026; the Fed's next meeting 8-9 Dec 2026; the next
monthly settled-facts audit falls on the first edition of December 2026.
Thanksgiving (26 Nov, full closure) and its Friday half-day (27 Nov) are
now under two weeks out — worth a direct calendar check once the window
reaches them (likely edition 73-74 if no gaps).
