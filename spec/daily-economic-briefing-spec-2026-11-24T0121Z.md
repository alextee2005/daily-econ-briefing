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
  applied correctly for **forty-eight straight editions (33 through 70)** —
  treat as settled; edition 68 read "Friday 20 November 2026," covering the
  Thursday 19 November session. Edition 69 read "Monday 23 November 2026,"
  covering the Friday 20 November session (a weekend-gap edition). Edition 70
  read "Tuesday 24 November 2026," covering the Monday 23 November session.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 70 all reused the
  same pattern — now confirmed clean across **forty-two consecutive
  editions**; edition 69 phrased it "Window: Thu 19 Nov 2026 20:00 ET – Sun
  22 Nov 2026 20:21 ET (Fri 20 Nov close/AH + weekend, the window's one NYSE
  session)"; edition 70 phrased it "Window: Sun 22 Nov 2026 20:00 ET – Mon 23
  Nov 2026 20:21 ET (Mon 23 Nov close/AH, the window's one NYSE session)." No
  further confirmation needed; treat this as settled.
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
  edition 63's error immediately. **Edition 66 ran this check** (`date -d
  "2026-11-18" +%A` returns Wednesday, matching the date line "Wednesday 18
  November 2026") and found it clean. **Edition 67 ran it too** (`date -d
  "2026-11-19" +%A` returns Thursday, matching the date line "Thursday 19
  November 2026") and also found it clean. **Edition 68 ran it too** (`date
  -d "2026-11-20" +%A` returns Friday, matching the date line "Friday 20
  November 2026") and also found it clean. **Edition 69 ran it too** (`date
  -d "2026-11-23" +%A` returns Monday, matching the date line "Monday 23
  November 2026") and also found it clean. **Edition 70 ran it too** (`date
  -d "2026-11-24" +%A` returns Tuesday, matching the date line "Tuesday 24
  November 2026") and also found it clean. Continue running this check every
  edition.
- **NEW trap caught at edition 68: this report's own drafting process can
  swap two similarly-sized single-stock movers' tickers, not just mis-cite a
  secondary outlet.** Edition 67 reported Wednesday 18 November's chip-rally
  movers as "Broadcom +5.31% to $530.14 and AMD +3.64% to $354.05." A direct
  ticker-by-ticker re-fetch of stockanalysis.com's own price-history pages at
  edition 68, done before reusing the prior edition's numbers as the Wed-vs-Thu
  base, found the two names were **swapped**: AMD actually closed +5.31% to
  $530.14, and Broadcom (AVGO) closed +3.64% to $354.05. The cause is not
  established (most likely a copy-paste mix-up while drafting, not a vendor
  error — both figures were individually correct, just attached to the wrong
  ticker). Disclosed via edition 68's correction box and Annex A. **Lesson for
  every future edition: when two names in the same cluster move by similar
  magnitudes, fetch each ticker's own price-history page individually rather
  than trusting a bundled one-line summary carried over from drafting notes —
  and spot-check at least one surprising same-session pairing by ticker
  before publishing.** **Edition 70 applied this from the start** on a
  nine-name AI-capex-complex rally cluster (NVDA, MU, BE, INTC, GLW, AMAT,
  SMCI, AMD, AVGO) — every figure came from that ticker's own
  stockanalysis.com price-history page, not a bundled summary; no swap or
  mismatch found.

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
half-day session (Friday 27 November) are now SETTLED, not a forward flag —
directly confirmed at edition 65** via a direct check of nyse.com's own
2026/2027/2028 holiday-calendar announcement and sifma.org's 2026
holiday-schedule recommendation: Thursday 26 Nov is a full closure for both
equities and bonds; Friday 27 Nov is a half-day for equities (1:00pm ET
close, 1:15pm for eligible options) with an early bond close recommended by
SIFMA (non-binding on individual firms). No further re-confirmation needed
unless a contradiction surfaces. **Veterans Day (Wednesday 11 November 2026)
itself is resolved/closed history, not a forward item any more** — directly
observed at edition 62: equities traded a full normal session while Treasury
cash markets and the Federal Reserve were closed, exactly as expected.

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
- **SETTLED (historical) — FOMC minutes from the 27-28 October meeting,
  closed as of edition 67, do not re-derive.** Released on schedule
  Wednesday 18 November 2026, 2:00pm ET, confirmed directly against
  federalreserve.gov. Beyond the already-known 10-2 vote (Cook/Hammack
  hawkish dissent, both named), the minutes describe most participants
  supporting the hold while "some" favored a 25bp hike as insufficiently
  restrictive; a few hike-leaning participants said they could have accepted
  a hold if markets understood further tightening was likely, and a few
  hold-backers called it a "close call" — this broader internal-division
  language is not attributed to named individuals beyond the two formal
  dissenters. The "vast majority" saw inflation upside risks, and **many
  participants explicitly flagged the AI capital-spending buildout as a
  material inflation risk** — a new detail. "Almost all" judged further
  hikes broadly consistent with the September dot plot would likely be
  appropriate under their baselines; the Desk's own dealer survey showed a
  median expectation of one more hike in December.
- **Rate-path odds re-firmed sharply at edition 70, reversing edition 69's
  pullback — and the Kalshi API's two-edition-standing empty-array bug was
  root-caused and fixed.** DeFi Rate's own blended snapshot (defirate.com,
  timestamped Mon 23 Nov 8:07pm ET) read approx. **94%** for a December 25bp
  hike (hike 94% / hold 3%), up from edition 69's approx. 90% — the first
  firming after several easing editions, plausibly consistent with Monday's
  broad risk-on reversal (Section 1 of edition 70's own briefing). **The
  Kalshi API's empty-markets-array problem (series `KXFED-26DEC`), standing
  for two editions, was found at edition 70 to be a wrong-identifier bug on
  this report's side, not a Kalshi-side fault**: the correct query uses
  `event_ticker=KXFEDDECISION-26DEC`, not `series_ticker=KXFED-26DEC`. Queried
  correctly, Kalshi's API returned clean fresh data directly: hike 25bp last
  price $0.93 (93%), hold $0.03 (3%), hike >25bp $0.04, cut 25bp $0.01, cut
  >25bp $0.01 — consistent with the DeFi Rate blend. **CME FedWatch failed to
  load directly again, a THIRTY-FIRST consecutive failure (41-70)** — a
  timeout again, no secondary citation found this edition either. **Use the
  corrected `event_ticker=KXFEDDECISION-26DEC` query for Kalshi going
  forward**; treat approx. 94% (DeFi Rate blend, corroborated by Kalshi's own
  direct read) as the solid read, and keep trying CME FedWatch and a
  non-stale Polymarket query every edition.
- **US-China tariff threads: the Section 301 178-product exclusion extension
  remains resolved with a precise deadline; the second, narrower USTR
  port-fee action remains resolved; the broader reciprocal-tariff truce
  remains unconfirmed by any US primary source for an ELEVENTH straight
  edition.** Four distinct threads, do not conflate: (1) the Section 301
  178-product exclusion extension (Federal Register Doc. 2026-22925,
  resolved at edition 61, cited to 91 FR 72610 at edition 64) — stands,
  settled; (2) edition 63's second, narrower Federal Register filing (Doc.
  2026-22867, the maritime/port-fee Section 301 action, suspended through
  9-10 Jan 2027) — stands, settled; (3) a related but DISTINCT Bureau of
  Industry and Security export-control suspension through 10 Jan 2027,
  identified at edition 66 — settled, not conflated with (2); (4) **the
  broader 10%-rate "reciprocal tariff" IEEPA truce with China** (reportedly
  extended by Treasury Secretary Bessent on 23 September to 10 January
  2027) — still unconfirmed by any US primary document after eleven straight
  editions of trying (60-70). Attempts tried across editions 65-70 and all
  negative: Treasury's and USTR's own press-release archives (404s/nothing
  on-topic), repeat Federal Register developer-API sweeps, a
  whitehouse.gov presidential-actions check, the trade-press/
  congressional-record angle (Trading Economics, AJOT, S&P Global, World
  Trade Scanner, Supply Chain Dive, Bloomberg Government all still only cite
  Bessent's own verbal announcement and describe the implementing notice as
  "to-be-published"), and **edition 70's FOIA-reading-room/USTR-docket
  angle** (a direct regulations.gov/USTR docket search surfaced only
  already-settled adjacent dockets — USTR-2026-0265/0266, a June 2026
  reciprocal-managed-trade RFC, and USTR-2026-0694, the already-known
  narrower maritime Section 301 suspension; federalregister.gov's
  public-inspection page returned HTTP 403 again). **Try at edition 71**:
  every angle tried so far (five now) has failed; consider a direct
  Treasury OFAC/International Affairs press-release archive sweep, or
  searching by the implementing notice's likely subject-matter heading
  rather than by issuing agency.
- **Fed Chair: Kevin Warsh — SETTLED, stop re-verifying it every run.** No
  contradiction surfaced through edition 64; directly re-confirmed via
  federalreserve.gov's own bios page at edition 54's November monthly audit,
  closing that housekeeping item cleanly; not re-attempted at editions 55
  through 66 (settled, no fetch needed). His Chairman term ends 21 May 2030
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
  re-attempted at editions 64 through 66** (no new state-certification news
  fell inside any of those windows, consistent with the structural
  explanation above); continue watching specific state deadlines as they
  land rather than searching for a single national resolution event that
  does not exist.
- **The NVIDIA/Huang governance thread reversed dramatically at edition 70:
  the board reinstated Huang as President/CEO/Board director Monday 23
  November 2026, effective immediately.** Read this as the board reversing
  its own prior public position, not as a correction of this report's past
  reporting of that position — edition 69's "does not intend to reinstate"
  was an accurate account of the board's stated position at the time, so no
  correction box applies. Background (settled history, do not re-derive):
  Huang resigned effective 11 Nov 2026 (8-K, accession 0001045810-26-000082);
  CFO Colette Kress became interim CEO, director Harvey C. Jones became
  first-ever independent Board Chair; Q3 FY2027 results (17 Nov, 8-K
  accession 0001045810-26-000088) crushed consensus (revenue $115.8bn +103%
  y/y, non-GAAP EPS $2.68, Q4 guidance $130.0bn &plusmn;3%); NVDA's AH pop
  fully round-tripped in the next regular session and the stock then fell
  nine of ten sessions into **Friday 20 Nov's -14.01% close at $125.53**,
  part of a broad AI-sector de-rating with no NVDA-specific news (full
  account in Section 2 of edition 69's own briefing). Two government-scrutiny
  threads surfaced at edition 69, both dated 16-17 Nov: (1) **confirmed,
  government-sourced** — a joint Commerce(BIS)/DOJ statement confirmed a
  criminal investigation into Nvidia customer Megaspeed, with **no
  allegations against Nvidia itself**; (2) **unconfirmed, single-sourced** —
  the Wall Street Journal's claim of an SEC civil inquiry into Nvidia's own
  disclosures, still **not independently corroborated by Reuters, AP,
  Bloomberg, CNBC or the NYT at edition 70 either** (a repeat search found
  nothing new). Congressional testimony had been confirmed for Huang (1 Dec)
  and GC Tim Teter (2 Dec), both closed-door House Foreign
  Affairs/Intelligence/China Select Committee interviews.
  **Monday 23 November's reinstatement** — confirmed directly via Nvidia's
  own 8-K (SEC EDGAR, CIK 0001045810, accession 0001045810-26-000090, filed
  8:57:54am ET) and Nvidia's own press release (nvidianews.nvidia.com),
  independently corroborated same-day by CNBC, Bloomberg, NBC News, Axios,
  CNN and Al Jazeera: the board's unanimous vote cited being "satisfied with
  respect to Mr. Huang's candor and ability to lead" and, after input from
  "senior levels of the United States government," said it is "confident
  that Mr. Huang's reinstatement poses no national security risk." Kress
  returns to CFO-only; Jones remains Board Chair. A new independent-directors
  committee continues investigating the original foreign-intelligence-
  targeting reports "to conclusion"; a separate National Security and Export
  Control Committee has been formed; Nvidia is searching for a first-ever
  Chief Compliance Officer. President Trump told CNBC he spoke with the
  board and "convinced" it to reinstate Huang. NVDA **+31.59% to $165.19**
  Monday (CNBC independently put the move at +31.48%, within rounding of
  this report's own close-to-close computation) — its best day since May
  2003 — powering a broad market-wide relief rally (full account in Section
  1/2 of edition 70's own briefing).
  **Still genuinely open for edition 71**: whether the 1-2 December
  congressional testimony dates still proceed now that Huang is reinstated
  as CEO (no outlet has addressed this question yet); whether the WSJ's
  SEC-probe claim gets independent corroboration; severance/compensation
  disclosure for the resignation-to-reinstatement period; the
  previously-logged shareholder class action's (Rosen Law Firm, investor
  Mark Kistenmacher) status; and whether Monday's rally holds, extends, or
  fades. Keep checking SEC EDGAR and congressional press pages each edition.
- General principle for everything still live: do not assume a routine
  macro-calendar fact (meeting dates, symposium schedules, other central
  banks' policy rates, government funding status) from memory or from the
  prompt's own framing — verify it fresh from a primary source
  (federalreserve.gov, bankofengland.co.uk, boj.or.jp, kansascityfed.org,
  norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, rba.gov.au,
  ecb.europa.eu, bankofcanada.ca, whitehouse.gov, etc.) every edition, exactly
  like any other data point, until an entry below is marked SETTLED. These
  are the rates and dates that feed Section 3's policy-rate table, so the
  table is the natural place to land them. Per-bank status as of edition 67
  (none contradicted, none re-attempted unless noted — no fresh central-bank
  news touched any of them inside editions 65, 66 or 67's windows):
  - **Reserve Bank of Australia:** current rate **4.85%**, hiked 25bp on
    Tuesday 3 November 2026 (6-3 split vote, its fifth hike of 2026) —
    SETTLED pending the RBA's own next decision, **7-8 December 2026**. Not
    re-attempted at editions 65-68.
  - **Bank of England:** rate **4.00%**, hiked 25bp on Thursday 5 November
    2026 (8-1 vote, Mann dissenting for +50bp) — SETTLED pending the next
    decision, **17 December 2026**. Not re-attempted at editions 65-70.
  - **European Central Bank:** rate complex (deposit facility 2.50%, main
    refi 2.65%, marginal lending 2.90%) **SETTLED**; next Governing Council
    meeting **16-17 December 2026**. Not re-attempted at editions 65-70.
  - **Bank of Japan:** current rate approx. 1.25%, SETTLED pending its own
    next meeting, **17-18 December 2026**. Not re-attempted at editions 65-70.
  - **Bank of Canada:** SETTLED. Current rate 2.50%, hiked 25bp 28 October
    2026. Next decision **9 December 2026** (same date as the Fed's). Not
    re-attempted at editions 65-68.
  - **Swiss National Bank:** current rate 0.00%, SETTLED. Next assessment
    **10 December 2026**. Not re-attempted at editions 65-70.
  - **Norges Bank:** current rate **4.50%** (hiked 25bp 24 Sept 2026),
    SETTLED; a forecast-free interim review on 5 November 2026 kept the rate
    unchanged, confirmed directly at edition 60. Next full decision remains
    **17 December 2026**. Not re-attempted at editions 65-70.
  - **Riksbank:** current rate **2.00%**, hiked 25bp on Wednesday 4 November
    2026, confirmed unanimous 5-0 via the bank's own primary minutes at
    edition 62 — SETTLED pending the next decision, **approx. 16 December
    2026**. Not re-attempted at editions 65-70.
  - **Banxico — the rate and vote remain primary-source confirmed; the
    next-decision date remains unresolved for a TWELFTH straight edition.**
    Banxico cut its overnight interbank rate 25bp, from 6.50% to 6.25%,
    decision dated 5 November, effective 6 November 2026, a 3-2 vote —
    primary-confirmed via Banxico's own 5 November press-release PDF at
    edition 62. **Edition 70's direct fetch of banxico.org.mx's calendar
    viewer (viewers2/JSP/calendarioDifusion_es.jsp) found 2027 is now a
    selectable filter year again (the edition-69 404 was apparently
    transient), but an automated query returned "No se encontraron
    publicaciones"** — the page is an interactive form, not reliably
    scrapable, and genuinely has no 2027 monetary-policy dates posted yet.
    No named research desk's 2027 calendar (BBVA/Scotiabank/Itaú) was found
    either. **Still de-prioritized per the standing guidance** — try again
    at edition 71, but do not spend further research-pass time on this
    beyond a quick check until Banxico actually publishes its 2027 calendar
    (likely a December or January event).
  - **Government funding/shutdown status:** H.R. 6500 funds federal agencies
    through 11 December 2026, no shutdown in effect. **Edition 70 got a fresh
    direct primary-source re-confirmation** via whitehouse.gov (ending two
    editions of absence-of-news-only carrying-forward). The Senate
    Appropriations Committee has released draft text for all twelve FY2027
    bills (appropriations.senate.gov, matching the House committee's prior
    pace); **neither chamber has passed any FY2027 bill on the Senate
    floor** as of edition 70 — the funding-cliff risk still points to the 11
    December deadline. Continue the standard re-check-every-edition
    discipline regardless.
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
- **NEW closed threads at edition 69 — Intuit's (INTU) F1Q27 and Ross Stores'
  (ROST) Q3 FY2026 results, both only partially confirmed at edition 68, are
  now fully resolved via their own 8-Ks.** Intuit (8-K Exhibit 99.01, SEC
  EDGAR accession 0000896878-26-000043): Q1 FY2027 (quarter ended 31 Oct
  2026) total net revenue $4,354m (+12% y/y); GAAP diluted EPS $2.59 (+63%);
  non-GAAP diluted EPS $2.91 (+56%); FY27 revenue guidance raised to
  $23,081-23,365m (reflecting a Credit Karma change), FY27 EPS guidance
  reiterated at $20.12-20.36 GAAP; the Mailchimp sale to Bending Spoons
  (approx. $3.68bn) is excluded from guidance pending close. The stock fell
  -2.35% (18 Nov), -1.03% (19 Nov), then **-12.77% (20 Nov)** — the bulk of
  the "beat guarantees nothing" decline landed a full session after the
  report, not in the immediate AH print edition 68 flagged (as large as
  -14.6% AH that edition). Ross Stores (8-K Exhibit 99.1, SEC EDGAR): Q3
  FY2026 sales +12% y/y to $6.3bn, comparable sales +8%, operating margin
  12.3% (+70bp y/y), EPS $1.91 beating its own $1.75-1.83 guidance, FY26 EPS
  guidance raised to $8.75-8.84 (includes a non-recurring approx.
  $0.60/share benefit from a $253m IEEPA tariff refund booked in Q2). The
  stock fell -3.41% (19 Nov) then -2.92% (20 Nov) despite the clean
  beat-and-raise. Do not re-derive either company's figures.
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
  m/m / +2.2% y/y, capacity utilization 76.9%. **CORRECTION (edition 70):**
  this report's own prior spec had flagged an annual G.17 benchmark revision
  "due 24 November 2026." A direct check of the Fed's own release-dates page
  (federalreserve.gov/releases/g17/release_dates.htm) at edition 70 found no
  such 2026 date — only the regular monthly schedule (last release 17 Nov
  2026, next 16 Dec 2026) — and the Fed's "current revision" page in fact
  describes the **2025** vintage (published 24 November 2025). This was a
  one-year misdate in this report's own prior research, not a reader-facing
  figure, so no correction box was used when disclosing it; do not repeat
  the "24 Nov 2026" framing going forward. No G.17 annual revision is
  expected to land before the regular 16 December 2026 release.
- **US Q3 2026 GDP (advance estimate) and September 2026 PCE/core PCE — both
  closed threads as of edition 53, released together Thursday 29 October
  2026:** real GDP **+3.4% annualized**; PCE headline **+0.5% m/m / +3.6%
  y/y**, core **+0.3% m/m / +3.1% y/y**. Next GDP release (2nd estimate +
  corporate profits): 25 November 2026.
- **University of Michigan October 2026 consumer sentiment — CLOSED thread as
  of edition 49:** preliminary 46.3 (five-month low); final 48.0 (vs.
  September's 48.1). Final sub-indices: current conditions 46.7, expectations
  48.8; year-ahead inflation expectations 4.7%, long-run 3.5%.
- **NEW closed thread at edition 69 — University of Michigan FINAL November
  2026 consumer sentiment, released Friday 20 Nov 2026, primary-sourced
  directly to sca.isr.umich.edu.** Headline Index of Consumer Sentiment
  **51.5** (vs. the preliminary 51.0 and October's final 48.0) — a notably
  large m/m improvement; Current Economic Conditions 49.4; Index of Consumer
  Expectations 52.9; year-ahead inflation expectations eased to 3.7% (from
  4.7%), long-run 3.3% (from 3.5%). No dated numeric consensus specifically
  for the FINAL reading was located (only the preliminary's own approx. 48.0
  Bloomberg consensus, which the preliminary already beat) — Annex B item if
  a consensus comparison is wanted. Note this reading sits in some tension
  with the same session's sharp equity selloff (Section 1 of edition 69's own
  briefing); reported as-is from the primary source, tension not resolved.
- **NEW closed thread at edition 69 — the Friday 20 November Fed-speaker
  calendar dispute flagged at edition 68 (Waller/Cook reportedly scheduled
  per one calendar, absent from another) is RESOLVED: both calendars were
  partly right.** Per the Federal Reserve's own events calendar
  (federalreserve.gov/newsevents/2026-November.htm): Governor Christopher
  Waller gave non-policy welcoming remarks at the College Fed Challenge
  student competition (8:25am ET) — no policy content found. Governor Lisa
  Cook gave a substantive, hawkish-leaning speech at the Central Bank of
  Chile's annual conference in Santiago (12:15pm ET; full text read directly
  at federalreserve.gov/newsevents/speech/cook20261120a.htm): she cited her
  own preliminary estimate of October PCE inflation (3.8% y/y headline / 3.2%
  y/y core — her own estimate, not yet an official BEA release), said
  inflation has been above target for 67 months "with no clear sign it is
  declining," and reaffirmed her October FOMC dissent (preferred a 25bp
  hike). Treat this as a live, one-off data point (a Fed speaker's own
  remarks), not a standing fact to re-verify.
- **China September 2026 CPI/PPI and October 2026 PMI — both RESOLVED, closed
  threads:** CPI +0.9% y/y (+0.2% m/m), PPI +5.0% y/y; October manufacturing
  PMI 49.3 (down from 50.1), non-manufacturing PMI 49.7 (down from 50.2), both
  back below the 50 threshold.
- **China Q3 2026 GDP — RESOLVED at edition 45, closed thread:** Q3 alone
  +4.5% y/y, +1.2% q/q; first-three-quarters cumulative +4.6% y/y.
- **New Mexico v. Meta — the $25bn civil-penalty ruling (Judge Francis
  Mathew, Wed 21 Oct 2026) remains substantially clarified but Meta's formal
  notice of appeal remains unconfirmed; this is now a low-priority item
  re-checked only occasionally (most recently edition 70, still no filing
  found), not every edition.** Meta owes **$25bn** in civil penalties — above
  the 48-other-state $18bn settlement Meta already reached elsewhere, well
  below New Mexico's $35-40bn ask. This judgment is **distinct** from: (1) a
  separate, earlier New Mexico Unfair Practices Act matter (approx. $942m,
  Meta posted an $1.8bn bond, unopposed stay around 9 Oct 2026); (2) the March
  2026 child-safety jury verdict ($375m); (3) the August 2026 abatement ruling
  ($567m, under appeal); (4) Meta's own Q3 2026 earnings charge (a separate
  $9.89bn one-time charge tied to an August 2026, 52-state-AG teen-safety
  settlement that excludes New Mexico). Don't conflate any of these four.
  Out of scope for most editions; no new development found or sought.
- **Calendar-awareness item: "equities-open, bonds-closed" US holidays need an
  explicit check every time they land in the window, not an assumption from
  memory.** Columbus Day (Mon 12 Oct 2026) and Veterans Day (Wed 11 Nov 2026,
  directly observed at edition 62) are both now resolved/closed history. **The
  only still-open calendar flag of this kind is Thanksgiving (26 Nov) plus
  the Friday half-day (27 Nov)** — see the Schedule section above. The DST
  transition (ended Sunday 1 November 2026) remains itself resolved/settled.
- **The vendor-retroactive-revision trap persisted at edition 70 across
  WTI, Brent AND (newly) Henry Hub — three series now, not two.** WTI:
  Investing.com's Friday 20 Nov base ($83.41) and Yahoo's ($83.98) already
  disagreed by $0.57 before Monday's move even began; Monday 23 Nov close
  $80.47 (Investing.com, -3.52% hand-computed) vs. $80.12 (Yahoo, -4.60%) —
  both down, a real magnitude gap on top of the disagreeing bases. Brent:
  Friday bases disagreed by $2.62 (Investing.com $89.95 vs. Yahoo $92.57,
  approx. 2.9%, the largest base gap yet); Monday close $86.68 (Investing.com,
  -3.64%) vs. $86.60 (Yahoo, -6.45%, Yahoo's row flagged low-volume/"Market
  Open," treated as a possible late snapshot rather than a confirmed settle).
  **Henry Hub developed a NEW, distinct problem at edition 70**:
  Investing.com's own Friday-base print ($3.748) does not match the
  previously-established baseline ($3.411, which Yahoo's Friday figure
  matches exactly) — Investing.com's Henry Hub row looked mis-keyed or stale
  this edition; its derived Monday change was excluded as unreliable, and
  Yahoo's figure (+3.96% to $3.546) was used as primary instead. Continue
  expecting any of WTI, Brent or Henry Hub to disagree or revise at any given
  edition; disclose as a vendor data-quality issue, not a reader-facing
  correction.
- **Gold and silver's cross-vendor pattern was clean on direction at edition
  70, and Kitco's live-quote widget was internally consistent this time —
  no repeat of edition 67's display bug.** Monday 23 Nov: gold $3,630.60
  (Investing.com, +3.28% hand-computed) vs. $3,658.50 (Yahoo, +4.07%) — both
  up sharply, agreeing on direction. Silver $42.980 (Investing.com, +4.65%)
  vs. $43.30 (Yahoo, +5.53%, Yahoo's row flagged low-volume/late) — also
  both up. Kitco's live-spot quote (two fetches approx. 1 minute apart) was
  internally consistent with its own headline text ("gold, silver prices see
  sharp rebounds") and day range — no contradictory display-bug reading this
  time. Kitco's historical-performance table remains broken, now an
  ELEVENTH straight edition. **Gold/silver rallying sharply on the SAME
  session equities also rallied sharply is a different pairing from
  Friday's** (when gold/silver fell alongside equities on apparent
  deleveraging) — more consistent with a broad risk-on unwind than either
  classic flight-to-quality or margin-driven deleveraging; keep watching
  which pairing recurs.
- **The Yahoo Finance duplicate-volume data-quality issue (first logged
  edition 65, recurred edition 67) was not specifically retested at edition
  70** — out of scope this edition, bypassed in practice by always computing
  % change from price levels by hand regardless. Worth a direct retest at a
  future edition to see if it's still present.
- **Henry Hub's base-price reliability — this report's historically
  worst-performing data-quality issue — broke again at edition 70; see the
  dedicated vendor-revision-trap entry above for the full account**
  (Investing.com's Friday base inconsistent with the established baseline;
  Yahoo used as primary). The front-month contract remains NGF7 (January,
  rolled at edition 69); no further roll as of Monday 23 Nov.
- **westmetall.com (LME copper) — the apparent historical-3-month capability
  flagged at edition 65 is RESOLVED at edition 66: it was an artifact of the
  combined cash/3-month table endpoint, not a standalone capability.** A
  direct re-test of the dedicated 3-month-specific field query
  (`field=LME_Cu_3m`) returned only the current day's figure, confirming the
  long-held assumption (only a current-day 3-month print is available via
  that specific query) still holds; edition 65's apparent multi-day 3-month
  read came from hitting the combined cash-table endpoint
  (`field=LME_Cu_cash`), which happens to carry both columns. **This closes
  the open thread — no further re-testing needed unless a contradiction
  surfaces.** Tuesday 17 Nov: LME cash $13,225.50/t (-1.12%), 3-month
  $13,211.00/t (-0.71%). **Edition 70: cash $12,165.00/t (-0.54% from
  Friday's $12,230.50), 3-month $12,170.00/t (Monday only) — the Friday
  3-month base could not be obtained despite four retries, a new, narrower
  gap than the resolved query-parameter issue above.** lme.com direct access
  still returns HTTP 403; copper remains single-vendor-sourced via
  westmetall.com.
- **New sourcing-mechanics trap logged at edition 50, relevant to any
  Monday-dated (or any day-after-a-non-trading-day) edition: Investing.com
  inserts an electronic Sunday-evening re-open print as its own row for every
  24-hour-traded instrument.** On any post-weekend edition, Investing.com's
  Monday-dated row computes its own displayed "% change" against that
  inserted Sunday reopen print, not Friday's actual close, even though the
  row is dated Monday (root cause identified at edition 65). **Edition 70
  (also a post-weekend Monday edition) reconfirmed this exactly**: hand
  computation from each vendor's own Friday-close to Monday-close was used
  throughout Section 4, rather than any vendor's own displayed percentage
  field. This mechanism does NOT apply on non-post-weekend editions. Keep
  computing hand % from the actual prior close on every post-weekend
  edition regardless.
- **FX cross-vendor data quality widened significantly at edition 70: EUR/USD
  and GBP/USD both developed genuine NEW direction conflicts, joining
  USD/JPY's now-three-straight-edition conflict.** Monday 23 Nov: EUR/USD
  -0.60% to 1.0902 (Investing.com) vs. +0.02% to 1.0972 (Yahoo, essentially
  flat) — previously clean/trivial, now a real split. GBP/USD -0.39% to
  1.3032 (Investing.com) vs. +0.07% to 1.3095 (Yahoo) — previously only a
  structural level gap with agreeing direction (confirmed recurring since
  edition 67), now also split on direction. USD/JPY +0.30% to 159.01
  (Investing.com, yen weakens) vs. -0.49% to 158.931 (Yahoo, yen strengthens)
  — the conflict persists a third straight edition, but which vendor favors
  which direction flipped again (Friday: Investing said yen strengthens,
  Yahoo said yen weakens; Monday: reversed). DXY's own spot-index variant
  stayed clean (+0.48% Investing.com vs. +0.44% Yahoo, good agreement); the
  DXY futures-contract variant remains unreachable on both vendors (404 on
  every URL variant tried), now a multi-edition-standing gap. **All four
  pairs/indices need checking every edition regardless of which way any
  individual one goes** — this is now a genuinely volatile, unresolved data-
  quality picture across the whole FX comparison, not a single-pair quirk.
- **The Kitco live-spot-vs-headline cross-check was clean at edition 70**
  (see the dedicated gold/silver entry above — no repeat of edition 67's
  display-bug reading). The historical-performance table remains broken,
  now an **ELEVENTH** straight edition of that specific sub-failure. Keep
  attempting both the historical table and a sanity-check on the live
  widget's displayed % field fresh every edition.
- **Bending Spoons (ticker BSP) is a legitimate new name, not a data error,
  if it recurs as a single-stock mover:** a Nasdaq Global Select
  Market-listed Italian software holding company, IPO'd 1 July 2026 at
  $29/share. Logged here so a future edition doesn't waste effort
  re-verifying the ticker's legitimacy if it moves sharply again. Not
  referenced at editions 64 through 66.
- **NEW at edition 68 — Anthropic (ticker ANT) completed the largest IPO on
  record Thursday 19 November 2026; logged here with full pricing/trading-day
  detail so a future edition doesn't need to re-derive it.** Priced
  Wednesday evening 18 Nov at $83/share (above a $70-78 marketed range) on
  approx. 980 million shares, raising approx. $81.3bn and valuing the
  company at approx. $1.5tn at the offer price (one outlet, Fox Business,
  cited $1.4tn — treat as cross-outlet variance, not a real conflict).
  Google and Nvidia were among seven strategic partners separately buying
  $26bn of non-voting shares at the IPO price. Thursday's first regular
  session: opened $111.50 (+34%), high $114.99, low $92.72, closed $97.17
  (+17.1% from the IPO price, approx. $1.76tn fully diluted), then eased to
  $92.60 (-4.7%) in after-hours trading. Multiple outlets tie the broader
  market's same-day risk-off to a "sell the news" dynamic once the
  long-anticipated debut was priced and trading. Friday 20 Nov (second
  trading day): -8.50% to $88.91, still above the $83 IPO price. Monday 23
  Nov (third trading day): -1.43% to $87.64, a mild continuation of the
  post-IPO fade even on a day the broader market rallied sharply — notably
  NOT following the market's own Huang-driven relief rally, worth watching.
  **ANT's first options listing, expected around Monday 23 Nov per Cboe's
  own rule on timing (2 business days after debut), did NOT appear to go
  live by Monday's close** — Barchart, Yahoo and Cboe's own delayed-quotes
  options tab all showed no calls or puts listed as of edition 70's cutoff.
  **Open for edition 71:** whether ANT options list, and the first
  implied-vol read if so; whether the post-IPO fade continues, stabilizes,
  or reverses; any lockup, index-inclusion, or analyst-initiation news.
- **The "named secondary outlet's own claim can be flatly wrong" trap family
  gained two more instances at edition 65, both confirming the discipline is
  now working proactively, not just as a post-hoc catch.** First: applying
  the edition-64 lesson from the start (rather than after a negative came
  back), edition 65's equities pass went directly to price-history pages for
  the chip complex and caught a wider, previously-unflagged sympathy decline
  (INTC -7.02%, SMCI -6.85%, IREN -9.80%, AMAT -5.47%) before publication,
  with no company-specific news behind any of the four — the preventative
  version of the lesson, not a correction. Second: an AP wire's claim that
  L3Harris fell on the Transportation Secretary publicly blaming the
  company for Friday 13 Nov's nationwide FAA ground stop looked like a
  single-sourced, consequential claim worth independent verification; a
  dedicated check found it corroborated across five-plus independent outlets
  (NPR, CNN, Al Jazeera, CBS News, Yahoo News), though the underlying
  technical root cause (L3Harris vs. the router manufacturer) remains
  genuinely disputed between the parties — disclosed as corroborated on the
  attribution, disputed on the cause. Third, a further "verified move, no
  confirmed driver" instance: Strategy/MSTR's -7.70% decline could not be
  tied to bitcoin's own modest (-1.7%) same-day move despite the plausible
  mechanism (MSTR's bitcoin treasury) — disclosed as unconfirmed rather than
  asserted. Prior instances in this family remain logged: JetBlue (edition
  50, magnitude), Carvana/Barron's (edition 52, direction/framing), Tesla and
  NU Holdings (edition 49, magnitude), Marvell/Lumentum and Barclays/PayPal
  (edition 53), a misdated Reuters-style squib plus a wrong-year Trefis list
  (edition 54), Brent crude's disclosed settle-to-settle-vs-"more than 7%"
  methodology discrepancy (edition 55), a claimed Oracle analyst-upgrade note
  (edition 56), three instances at edition 58 (a fabricated DraftKings AH
  figure, an unsupported Natera claim, an unsupported "biggest calls" list), a
  stale-date index-close republish at edition 59, a claimed International
  Money Express/Western Union tie to the Intermex deal's drop-dead date at
  edition 62, Rocket Lab/Lucid premarket-snapshot-mistaken-for-close
  instances at edition 61, five instances at edition 63 of reporting a
  verified price move with NO confirmed driver, and edition 64's inverse-
  direction "clean negative overturned by direct fetch" instance (AMD,
  Broadcom). **Edition 66 added a further instance, this time of genuine
  cross-vendor AH-move-magnitude disagreement rather than a single wrong
  claim**: NVIDIA's own after-hours reaction to its Q3 FY2027 beat had no
  single settled print across Reuters/Investing.com/Decrypt (approx. +2%),
  Motley Fool (approx. +1.3% early) and NBC/Decrypt (gains "as much as
  4-5%" later in the call) — disclosed as a range rather than resolved to
  one figure, the same discipline as the Brent methodology case at edition
  55.
- **The edition-49 "forward-looking calendar aggregator" trap (names falsely
  listed as past or future reporters when the actual date differs) remains
  closed as a general pattern.** Not independently re-tested at editions 61
  through 66 (no new instance found or needed); continue checking any
  carried-forward calendar assumption against its primary source before it
  becomes load-bearing.
- **A megacap multi-name earnings cluster producing genuinely uncorrelated
  reactions is a standing, repeated pattern — SIXTEEN distinct instances
  through edition 64 (editions 44, 47, 48, 49 x2, 50, 52, 53 x3, 58, 59, 60,
  61, 63, 64).** Edition 65's own earnings cluster (Tyson, Powell
  Industries, Aramark) did NOT add a new instance — all three beats drew
  directionally consistent (positive) reactions that time. **Edition 66 DID
  add one**: Home Depot's Q3 FY2026 beat-and-raise ("results... exceeded our
  expectations," incoming CEO Richard McPhail) nonetheless drew a -2.45%
  decline — a single-name instance of the same "beat guarantees nothing"
  principle (see also the dedicated rule under Hard Rules). Continue
  treating beat-and-raise (or a guidance cut) as having no *guaranteed*
  effect on the reaction without checking the actual outcome.
- **New production lesson from edition 53: CSS multi-column (`.cols3`/
  `.cols2`) pagination under Chromium print-to-PDF can plateau stubbornly on
  marginal content trims; edition 60 hit the most severe version of this
  plateau and found a clearer fix (documented under Production Notes
  below).** Editions 61 through 64 all needed none of this; edition 65 hit
  the exact edition-60 symptom again (a lonely trailing Method note stranded
  on page 5, fixed by trimming Annex C's own citations). **Edition 66 was a
  genuine spillover case (sections 1-6 ending partway down page 4) that
  converged cleanly in just two renders with NO Annex-C column-balance
  symptom** — deleting the forced break was sufficient on its own this time,
  a useful reminder that the edition-60/65 symptom is not automatic on every
  spillover, just a recognizable pattern to check for if a lonely trailing
  block does appear.
- **The VIX feed's bug was CLEAN at edition 70, after recurring at edition
  69.** The feed's `prev_day_close` matched the true prior close and its own
  `price_change_percent` field matched hand computation exactly across all
  six series (VIX, VIX9D, VIX3M, VIX6M, VVIX, SKEW); VIX's own prior close
  (35.89) was independently cross-checked against FRED's official VIXCLS
  series and matched. Pattern to date: clean 55-58, recurred 59, clean
  60-63, recurred 64, clean 65-68, recurred 69, **clean 70** — continue the
  manual-calculation discipline unconditionally regardless of how many
  bug-free editions precede the current one; always hand-compute from the
  feed's own raw levels rather than trusting its percent field. A
  CBOE-reported intraday VIX low of 15.39 on Monday could not be
  corroborated against any second source and was treated as a likely bad
  tick, not used.
- **A markup-correctness self-check (`grep -n '</td><sup'`) caught three
  instances of an invalid-table-structure trap at edition 54 (documented
  under Production notes below), before rendering.** Editions 55 through 70
  all ran the same proactive check and found **ZERO instances for a
  SIXTEENTH consecutive edition** — worth continuing on every edition with a
  table that has an empty trailing cell or a cell containing only a
  citation.
- **The CFTC Asset-Manager-vs-Leveraged-Funds grouped-bar chart was NOT
  needed at edition 70** — no new CFTC report posted inside this edition's
  window (the report covering 17 Nov data, last used for the chart at
  edition 65, already posted Friday 20 Nov and was covered at edition 69);
  the session's dominant story (Huang reinstatement) left no case for the
  chart regardless. The chart itself was last used at edition 65 (sixth time
  overall: editions 34, 39, 44, 49, 54, 65) with figsize (9.8, 2.15),
  `h=0.32` bar offset and the figure-level legend technique documented under
  Production Notes. **IMPORTANT SCHEDULE CORRECTION at edition 70**: a
  direct check of cftc.gov's own release-schedule page
  (CommitmentsofTraders/ReleaseSchedule) found the report covering 24
  November data is due **Monday 30 November 2026**, not the following Friday
  (27 Nov) as this report had previously assumed — a Thanksgiving-week
  holiday adjustment. **Do not expect a fresh CoT report inside edition 71's
  window** (which should cover Tuesday 24 Nov); the next chart opportunity is
  whichever edition's window reaches Monday 30 November.
- **The Investing.com displayed-%-vs-computed-% divergence mechanism (root
  cause identified at edition 65) was reconfirmed again at edition 70 — see
  the dedicated "New sourcing-mechanics trap" entry under Standing Facts
  above; not re-detailed here to avoid the two entries drifting apart, as
  they had across editions 66-69.** Keep computing by hand from actual
  session closes on every post-weekend edition regardless.
- **The USD/JPY, EUR/USD, GBP/USD and DXY cross-vendor status is tracked in
  ONE place now — see the dedicated "FX cross-vendor data quality widened
  significantly at edition 70" entry under Standing Facts above.** (This
  pointer replaces what had been two separately-drifting FX-status entries
  in this section and in Known-hard-to-source below, which had fallen out
  of sync with each other across editions 66-69; consolidating here going
  forward.)

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
  prose. **Edition 65 DID use the third chart**: fresh CFTC CoT data
  (covering Tuesday 10 Nov, posted Monday 16 Nov as expected) powered the
  Asset-Manager-vs-Leveraged-Funds grouped bar in Section 5 — judged ahead
  of the VIX term-structure option even though VIX itself spiked +18.70%
  with a genuine front-end inversion, since the CFTC data was the fresher,
  more dominant positioning story. **Editions 66 through 70 did not use a
  third chart** (no fresh CFTC report inside 66-68's windows; edition 69's
  fresh report was judged secondary to its own dominant equity story;
  edition 70 had no fresh report at all and an even more dominant single
  story, the Huang reinstatement). **CFTC's next report is now confirmed due
  Monday 30 November 2026** (a Thanksgiving-week holiday adjustment,
  confirmed directly via cftc.gov's own release-schedule page at edition
  70), not the following Friday as previously assumed — the next chart
  opportunity is whichever edition's window reaches that date.
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
  editions 56 through 65 (edition 63's reported approx. $500bn NVDA
  weekly-value figure is NBC's own reported aggregate, cited as such, not
  independently recomputed by this report).
- Where sources disagree, use the more authoritative one **and** disclose
  the disagreement. AP's "How major US stock indexes fared" and the Reuters
  market wrap are normally the most reliable for index closes — but check
  they're actually indexed for the target date before relying on them. The
  WTOP.com/lanacion.com.ar AP-wire-mirror approach remains the established
  first-choice workaround when apnews.com/Reuters are blocked directly.
  **Edition 70 used both mirrors together again** (identical figures from
  each), cross-checked against SPY's own price history and Yahoo Finance's
  live-quote sidebar. apnews.com and Reuters were both tried directly again
  at edition 70 and remain unreachable — keep re-attempting the primary
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
  true after all (edition 61), refined at edition 64 by the inverse case
  (a research pass's clean NEGATIVE result for single-stock movers
  overturned by a direct coordinator follow-up fetch), and applied
  PROACTIVELY for the first time at edition 65 (the equities pass went
  straight to price-history pages for the chip complex from the start,
  catching a wider sympathy decline before any negative needed overturning).
  Treat ANY surprising secondary claim (price move, driver, analyst action,
  date, or computed percentage) — AND any surprisingly clean negative result
  for a single-session search — as needing a genuine, thorough verification
  attempt before either accepting or rejecting it.
- Run a dedicated verification pass on any figure two research passes
  disagree on, or any single surprising/highly-consequential finding, before
  publishing — cheap, and has caught real errors before. **Edition 65 ran
  this discipline on a single-sourced, consequential claim**: an AP wire's
  claim that L3Harris fell because the Transportation Secretary publicly
  blamed the company for Friday 13 Nov's nationwide FAA ground stop looked
  single-sourced and worth independent verification; a dedicated check found
  it corroborated across five-plus independent outlets (NPR, CNN, Al
  Jazeera, CBS News), though the underlying technical root cause remains
  genuinely disputed between the parties. (Edition 64's own instance of this
  discipline — AMD/Broadcom's clean negative overturned by a direct fetch —
  remains logged above as the complementary, inverse-direction case.)
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
  three beats). **Edition 65's own earnings cluster (Tyson, Powell
  Industries, Aramark) was the opposite case — all three beat and rallied,
  directionally consistent.** **Edition 66 returned a single-name instance**:
  Home Depot's clean Q3 FY2026 beat-and-raise drew a -2.45% decline — a
  useful reminder that the divergent pattern is common, not universal;
  always check the actual outcome rather than assuming either way. Always
  fetch the verified close, the after-hours reaction, AND (when the window
  allows) the next regular session's close as three separate, clearly
  labelled figures — **edition 66 applied this fully to NVIDIA's own Q3
  FY2027 report**: Tuesday's regular-session close ($155.46, -0.44%, set
  before the print) was reported separately from the disputed AH range
  (roughly +2%, swings to +4-5%), with Wednesday's reaction explicitly left
  for edition 67 rather than assumed. A premarket-only or
  regular-session-only figure that predates a same-evening earnings release
  should be labelled as such rather than implied to be a reaction to it.
- **FX cross-vendor status (DXY, EUR/USD, GBP/USD, USD/JPY) and the
  Investing.com Monday-reopen displayed-% mechanism are both tracked in ONE
  place each under Standing Facts above — not duplicated here, to prevent
  the drift that let this section and the Standing Facts section disagree
  across editions 66-69.** Check both dedicated entries every edition
  regardless of which way any pair goes.
- **The Kitco live-spot-vs-headline cross-check status is tracked under
  Standing Facts above — see that entry rather than this one.**
- **The 2-year Treasury yield conflict from edition 36 remains resolved, and
  the every-edition reconciliation continued cleanly at edition 70**:
  Monday 23 Nov's official par-yield print (home.treasury.gov) showed 2-year
  4.63% (unchanged), 10-year 4.92% (unchanged), 30-year 5.29% (-2bp) vs.
  Friday's prior print — confirmed as a genuine (if coincidental) flat print
  on the 2yr/10yr, not a stale-duplicate scrape, by checking that surrounding
  maturities moved independently (front end backed up 1-7bp, consistent with
  re-firming hike odds). No cross-source conflict found.
- **The distinct Yahoo Finance stale-%-field issue (logged edition 63) and
  duplicate/conflicting-row issue (logged edition 65, recurred 67) were both
  NOT specifically retested at edition 70** — out of scope this edition,
  bypassed in practice by always computing % change by hand regardless;
  worth a direct retest at a future edition.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 69 have all run clean (or
  clean after quick fixes) — edition 67 ran clean on the first check (24/24),
  edition 68 needed a quick fix (26/26 after), and **edition 69 needed one
  quick fix too**: six Annex C entries were initially unused (a second-vendor
  citation, an EDGAR-check citation, the Banxico-calendar citation, the Kitco
  citation, the dealer-gamma citation and the CMS-source citation) — adding
  the missing inline `<sup>` tags for each resolved it cleanly (25/25
  matched).
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 69 have all rendered with zero stray tildes on the
  first draft, bar editions 56 and 57 which each needed one fix.**
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Editions 34, 39, 44, 49, 54 and 65
  have all resolved this cleanly for CFTC CoT (edition 65's own ES/NQ/RTY
  open-interest figures all came directly from cftc.gov, so no denominator
  gap actually arose that edition — the technique remains documented for the
  day it does). The next CFTC report to actually need this technique (should
  a denominator gap arise) is whichever one lands after the Thanksgiving-week
  half-day session — watch for it at edition 70 or later.
- **The diffuse-overflow lesson from editions 44-45 and the duplicated-
  content lesson from edition 47 are both still worth checking first on any
  overflow** — but edition 53 showed overflow can also be genuinely dense
  content requiring real trimming, edition 54-58 showed the opposite, edition
  60 showed a third distinct cause (an Annex-C column-balance effect), edition
  65 showed that same edition-60 cause recurring (fixed by trimming Annex
  C's own citations), edition 66 showed a genuine page-4 spillover that
  converged with neither real trimming nor the Annex-C symptom needed
  (deleting the forced break alone was sufficient), and **edition 69 showed
  the common, no-overflow case**: sections 1-6 ended comfortably on page 3
  with meaningful room to spare despite an unusually large single-stock
  movers section, converging on the FIRST render with the forced break kept.
  Always check which situation you're in before assuming a particular fix is
  the answer.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — **specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation.** No capping
  has been needed in any edition since 45. Edition 69's movers chart (9
  categories, BE -15.30% largest, NVDA -14.01% second largest) had a ratio of
  approx. 1.09x, among the tightest yet; **edition 70's (11 categories, NVDA
  +31.59% largest, MU +19.04% second largest) had a ratio of approx. 1.66x**,
  comfortably under the 5x threshold despite the largest raw move this report
  has logged. Used `pad_frac=0.25` with figsize (9.8, 1.95), rendered
  cleanly. `pad_frac=0.30` for the 11-category sector panel has now rendered
  cleanly across twenty-five editions (45-50, 52-70).

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`, under the `quotes/` path
  specifically — `charts/_VIX.json` returns 403, `quotes/_VIX.json` works).
  **Editions 28 through 69 have all got a fresh, same-day-timestamped
  sweep** — forty-three consecutive fresh sweeps now, including a clean one
  at edition 70 (see the dedicated Standing Facts entry above for the bug
  pattern to date: clean 55-58, recurred 59, clean 60-63, recurred 64, clean
  65-68, recurred 69, clean 70). Always compute day-over-day % change
  manually from the raw levels regardless of how many consecutive bug-free
  reads preceded the current one. The feed still requires a browser
  User-Agent plus an `Origin`/`Referer: https://www.cboe.com/` header to
  clear a Cloudflare 403; carry this forward as the default request shape.
  **Edition 70's own session (hand-computed from raw levels):** VIX -25.83%
  to 26.62, VIX9D -31.83% to 27.76, VIX3M -17.58% to 25.50, VIX6M -12.12% to
  25.96, VVIX -14.98% to 117.36, SKEW +1.10% to 140.37 (all six timestamped
  Monday). Term structure partially unwound Friday's full-length
  backwardation: the front end remains inverted (VIX9D>spot VIX>VIX3M) but
  the back end flipped into slight contango (VIX6M>VIX3M) — a partial, not
  complete, relief rally in vol terms.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 70 fetched all 11 directly again** (9 of
  11 closed higher — Technology +8.97% the clear leader; only Energy -1.06%
  and Cons. Staples -0.09% lower, a complete breadth reversal from Friday's
  1-of-11) — continue this direct-fetch-by-default method. A secondary
  cross-check (MarketWatch) was attempted and blocked again at edition 70 —
  now a TWELFTH straight edition single-sourced; try the cross-check again
  at edition 71.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (0 of 11 at edition 66; 5 of 11 at
  edition 67; 0 of 11 at edition 68; 1 of 11 at edition 69; **9 of 11 at
  edition 70**). No constituent-level breadth figure (e.g. "X% of S&P 500
  stocks advanced") was found in any wire checked at edition 70 — keep
  checking for it each edition without relying on it being there.
- **Dealer gamma:** zerogex.io and SpotGamma both remain fully unusable,
  extending their respective failure streaks again at edition 70 (placeholder
  dashes / article teasers only, no timestamped figures). No AMD- or
  ANT-specific options-flow commentary of usable quality was found at
  edition 70 either. **ANT's first options listing, expected around Monday
  23 Nov per Cboe's own timing rule, did NOT appear to go live by Monday's
  close** (Barchart, Yahoo and Cboe's own options tab all showed no calls or
  puts) — check again at edition 71.
- **Official CME FedWatch probabilities:** the page blocks fetching — a
  **THIRTY-FIRST** consecutive failure at edition 70 (41-70), a timeout
  again, no secondary citation found. **Use Kalshi/Polymarket/DeFi Rate
  instead — and use the CORRECT Kalshi query, found at edition 70**:
  `event_ticker=KXFEDDECISION-26DEC` (not the previously-used
  `series_ticker=KXFED-26DEC`, which was simply the wrong identifier and the
  actual cause of two editions of empty results, not a Kalshi-side bug).
  Queried correctly, Kalshi returned clean fresh data (hike 93%, hold 3%);
  DeFi Rate's blend read approx. 94%, up from edition 69's approx. 90%.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **westmetall.com (LME copper) at edition
  70**: cash $12,165.00/t (-0.54% from Friday's $12,230.50); 3-month
  available for Monday only ($12,170.00/t), Friday's 3-month base
  unobtainable despite four retries. lme.com itself still returns HTTP 403,
  so copper remains single-vendor-sourced — keep checking both sites each
  edition.
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **posted a fresh Monday 23 Nov print at
  edition 70, continuing the clean streak** — 2-yr 4.63% (unchanged), 10-yr
  4.92% (unchanged), 30-yr 5.29% (-2bp) vs. Friday's prior print; confirmed
  genuine (not a stale-duplicate scrape) by checking surrounding maturities
  moved independently (front end backed up 1-7bp). Continue scoping the
  TextView URL to the specific month
  (`field_tdr_date_value_month=202611`-style parameter) rather than the
  full year.
- **CFTC CoT:** publishes with the prior Tuesday's data — always state the
  lag explicitly. `financial_lf.htm` works well for equity index futures
  (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). **The report covering Tuesday 17 November data POSTED
  Friday 20 November 2026 as scheduled**, confirmed at edition 69; nothing
  new applied at edition 70. **SCHEDULE CORRECTION, confirmed directly via
  cftc.gov's own release-schedule page at edition 70**: the report covering
  24 November data is due **Monday 30 November 2026**, not the following
  Friday (27 Nov) — a Thanksgiving-week holiday adjustment. Do not expect a
  fresh report inside edition 71's window.
- **GBP/USD, EUR/USD, USD/JPY, DXY cross-vendor status — see the dedicated
  Standing Facts entry ("FX cross-vendor data quality widened significantly
  at edition 70") rather than this entry, which had drifted out of sync with
  it across editions 66-69 and is not being duplicated further.**
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. See the dedicated
  Standing Facts gold/silver entry above for edition 70's figures and the
  Kitco status.
- **China CPI/PPI (monthly), China Q3 GDP, US GDP/PCE/import-export
  prices/industrial production, University of Michigan October consumer
  sentiment, China's October PMI and October ISM Services PMI:** all closed
  threads — see Standing Facts above. **October US CPI** is a closed thread
  as of edition 61 (including the missing-y/y wrinkle). **October US PPI**
  is a closed thread as of edition 64 (headline cooler, core hotter than
  consensus; y/y comparison intact, unlike CPI's). **NEW closed thread as of
  edition 68: the November 2026 Philadelphia Fed Manufacturing Business
  Outlook Survey** (headline general-activity index 6.3, down sharply from
  October's 20.9, lowest since May 2026; new orders -0.4; prices paid 58.2;
  future capex 18.9) — directly sourced to philadelphiafed.org, no vendor
  conflict. Weekly US initial jobless claims (203k for the week ended 14
  Nov, vs. approx. 197k consensus) remain a recurring weekly print, not a
  closed thread in the same sense, but note DOL's own release document is
  still unparseable via direct fetch — Reuters-sourced wire coverage (via a
  secondary outlet) was the only route this edition, a single-sourced
  result worth a second source next time if easily available.
- **Henry Hub natural gas:** the front-month contract remains **NGF7
  (January)**, rolled at edition 69 — no further roll as of Monday 23 Nov.
  **The base-price reliability problem — this report's historically
  worst-performing data-quality issue — reopened at edition 70** after one
  clean edition: Investing.com's own Friday-base print ($3.748) did not
  match the established baseline ($3.411, which Yahoo matched exactly);
  Yahoo was used as primary, Investing.com's figure excluded as unreliable.
  Continue the every-edition two-source reconciliation discipline, since
  this toggles open/closed unpredictably.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. CoreWeave's Q3 2026 results and
  regular-session reaction are fully resolved (edition 62); not re-attempted
  at editions 64 through 66.
- **Weekend equities catalyst: 13F filings.** The Q3 2026 deadline has now
  passed, closed at edition 65 (nothing substantive reported, including a
  dedicated Berkshire Hathaway check). No further action needed on this
  deadline; the next 13F deadline is mid-February 2027 (Q4 2026 data).
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22, not attempted
  again since). Revisit only if a future edition has spare research
  bandwidth on an FOMC day specifically — not relevant to most editions.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully at
  editions 39, 44-49, 54, 59, 65 and **69** (the Friday 20 Nov report,
  covering Tuesday 17 Nov data: ES OI 2,096,958; NQ futures-only OI 296,423
  [the separate "Nasdaq-100 Consolidated" line read 314,318 — still
  plausibly, not yet conclusively, explained as CFTC's futures-only vs.
  futures-and-options-combined convention]; RTY OI 459,730). Next report due
  the Friday after (27 Nov, Thanksgiving-week half-day) — verify the
  holiday-adjusted timing directly at edition 70 rather than assuming the
  normal cadence, watching for the micro-vs-full-size naming trap each
  time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Editions 58
  through 70 all found zero verifiable analyst actions — **a THIRTEENTH
  consecutive edition with none found at edition 70, though this time with a
  specific caveat: edition 70's search ran only hours after the Huang
  reinstatement broke, and may simply reflect same-day search-index lag on
  breaking news rather than a genuine absence of sell-side reaction** —
  worth a fresh check at edition 71 for analyst actions dated 23-24 Nov
  specifically before assuming none exists. Stale pre-reinstatement NVDA/AMD
  analyst actions from mid-November should not be repeated as current.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance — and a research pass's clean negative result needs the
  same scrutiny.** This discipline has now caught numerous fabrications and
  errors (full list in the Standing Facts "named secondary outlet" entry
  above). Edition 65 applied the discipline PROACTIVELY for the first time
  (direct price-history pages for the chip complex from the start, catching
  a wider sympathy decline before publication). **Edition 66 continued this
  discipline**: every reported single-stock mover was individually verified
  against either a primary SEC/EDGAR filing (NVIDIA's own 8-K for its Q3
  FY2027 results; Home Depot's own 8-K for its Q3 FY2026 results) or a
  two-source price-history fetch (NVDA, AMD, AVGO, INTC, SMCI, IREN, AMAT),
  and the NVIDIA AH-move magnitude disagreement across vendors was
  disclosed as a range rather than resolved to a single number rather than
  silently picking one outlet's claim. **Edition 68 extended the discipline
  to catching the report's OWN prior-edition error, not just a secondary
  outlet's**: before reusing edition 67's reported Wednesday 18 Nov AMD/AVGO
  figures as a Wed-vs-Thu base, a direct ticker-by-ticker re-fetch of
  stockanalysis.com found the two names had been swapped in edition 67's own
  text (see the dedicated trap entry near the top of this spec and the
  correction box used at edition 68). Every other reported Thursday mover
  was individually verified against a primary SEC/EDGAR 8-K (Palo Alto
  Networks, Lowe's, Williams-Sonoma) or a two-source price-history fetch
  (AMD, AVGO, NVDA, INTC, AMAT, SMCI, WMT, UNH), and the AMD-specific
  Hunterbrook short-report claim was corroborated against CNBC directly
  (which itself disclosed it had not independently verified Hunterbrook's
  underlying factual claims, and that Hunterbrook had disclosed its own
  short position — a conflict of interest in the primary claim-maker,
  separate from the well-corroborated fact of the price move and the
  report's existence). Continue this direct-verification discipline,
  including the proactive direct-fetch approach and now also a spot-check
  of the PRIOR edition's own carried-forward figures, on every edition.
  **Edition 69 extended the discipline to a consequential NEWS claim, not
  just a price figure**: a dramatic secondary-sourced claim (the WSJ's
  reported SEC civil probe into Nvidia's own disclosures) was put through a
  dedicated independent-corroboration check before publication, found to
  be single-sourced, and disclosed as such rather than upgraded to fact —
  while a RELATED but distinct claim in the same story (the Commerce/DOJ
  Megaspeed criminal-investigation statement) was confirmed as
  government-sourced and published as fact. Every reported Friday mover was
  again individually verified against either a primary SEC/EDGAR 8-K
  (Intuit, Ross Stores) or a two-source price-history fetch (NVDA, AMD,
  AVGO, MU, INTC, AMAT, SMCI, BE, GLW, ANT, UNH). **Edition 70 applied the
  same discipline to the edition's own headline claim**: Nvidia's board
  reinstating Huang was verified directly against Nvidia's own press release
  and 8-K (not just a secondary summary) before being treated as fact, and
  independently cross-checked against CNBC, Bloomberg, NBC, Axios, CNN and
  Al Jazeera's own same-day coverage; every AI-capex-complex mover (NVDA, MU,
  BE, INTC, GLW, AMAT, SMCI, AMD, AVGO) was individually fetched from its own
  stockanalysis.com price-history page rather than a bundled CNBC list, and
  the WSJ's single-sourced SEC-probe claim was re-checked and again found
  uncorroborated rather than silently repeated as settled.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted since (out of scope each time); try an alternate DOL
  page or a secondary economic-calendar aggregator for the consensus figure
  when next relevant.
- **federalregister.gov's direct search interface remains blocked** (a prior
  search attempt 302-redirected to `unblock.federalregister.gov`, an
  apparent bot/rate-limit gate, first logged at edition 48) — **edition 66's
  attempt would have hit the same gate (not separately re-attempted; edition
  66 went straight to the developer API and the presidential-documents
  feed instead).** govinfo.gov continues to be a known working alternative
  route for at least some Federal Register content. **The Federal Register's
  own developer API (`federalregister.gov/api/v1`) scored another success at
  edition 66** (located the already-known 178-product Section 301 notice,
  dated 10 Nov 2026) — this API remains the clearly-established first
  approach whenever the search UI is blocked. **Edition 66 also tried the
  Federal Register's presidential-documents feed AND whitehouse.gov's own
  presidential-actions listing directly** (searching for an EO modifying the
  China reciprocal-tariff truce) — both came back clean negatives, not
  found; see the dedicated tariff-thread entry in Standing Facts above.
  **Edition 70's public-inspection.federalregister.gov attempt (part of the
  FOIA/docket angle) also returned HTTP 403**, consistent with the search UI
  being blocked; regulations.gov/USTR docket search was used instead (also
  negative — see the tariff-thread entry above).
- **SEC EDGAR's `cgi-bin/browse-edgar` company-search page (filtered by CIK
  and form type 8-K) is a highly reliable, fast way to confirm both WHETHER
  a company has reported on a given date and to find the accession number
  for the underlying exhibit.** **Edition 70 used it again for NVIDIA**,
  finding the fresh 23 Nov 8:57am ET 8-K (accession 0001045810-26-000090)
  confirming the Huang reinstatement — reinforcing that this is the default
  first tool for confirming any earnings or governance filing, and for
  confirming a clean negative just as reliably as a positive.
- **ECB's current policy rate: SETTLED since edition 55** (unchanged through
  the 28-29 October 2026 meeting: deposit facility 2.50%, main refi 2.65%,
  marginal lending 2.90%); not re-attempted at editions 56 through 70 (no
  fetch needed). It reopens on contradiction, the next Governing Council
  decision, or the monthly audit. The Council's own next-meeting date is
  SETTLED at 16-17 December 2026.
- **NFIB Small Business Optimism Index:** nfib.com returned HTTP 403 at
  direct fetch at edition 62; Trading Economics worked as a fallback,
  carrying the October reading (97.8, down 0.1pt from September). Not
  re-attempted at editions 63 through 66 (no new monthly release inside any
  of those windows); continue using Trading Economics as the default
  fallback when nfib.com blocks direct access.
- **Banxico's next policy-decision date — see the dedicated Standing Facts
  entry above (unresolved for a twelfth straight edition as of edition 70);
  not duplicated here further** to avoid the two entries drifting out of
  sync the way they had across editions 66-69 (this entry had gone stale,
  still reading "FIFTH straight edition... try at edition 67" as of edition
  69's carried-forward spec).

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel —
  confirmed clean again at editions 66 through 69 (thirty editions
  total: 37-43, 45-50, 52-69). For charts with fewer categories, scale the
  height down: roughly `(9.8, 1.65-2.05)` for 3-9 categories. **Edition 69
  used `(9.8, 1.95)` for a 9-category movers chart with `pad_frac=0.25`**,
  rendering cleanly across a -15.30% to +2.84% range (ratio approx. 1.09x).
  **Always render and visually inspect (via the Read tool) the actual PNG at
  or near full resolution before embedding it**, regardless of what a past
  edition's success might suggest. **Default to pad_frac=0.30 from the start
  for an 11-category sector-ETF panel** — now confirmed across twenty-four
  straight small-magnitude 11-category panels (45-50, 52-69). For any
  movers chart with a double-digit-percent outlier, continue trying
  pad_frac in the 0.22-0.30 range from the start.
- **Capped-outlier label-overlap fix (from edition 45):** when a capped
  bar's value label uses a "(capped)" text suffix, the label text can be
  long enough to visually bleed into the y-axis tick-label margin even at a
  wide pad_frac, because matplotlib's `ax.text()` is unclipped by default.
  **Fix: shorten the per-bar suffix to a single trailing asterisk (`"*"`
  instead of `" (capped)"`) and add one footnote to the chart's x-axis label
  instead.** This remains the recommended default for any future
  capped-outlier chart. No edition since 45 has actually needed outlier
  capping (every spread has stayed well under the approx. 5x ratio
  threshold, including edition 64's approx. 1.61x, edition 65's approx.
  1.12x, and edition 66's approx. 1.01x) — reinforcing that the trigger is
  the ratio to the next-largest bar, not the largest bar's absolute size.
- **A grouped (two-series) horizontal bar chart — needed for the CFTC
  Asset-Manager-vs-Leveraged-Funds positioning chart — requires custom chart
  code, not the standard single-series `barh()` helper used for the
  movers/sector charts** (first built at edition 44, reused successfully at
  editions 49, 54 and — after an 11-edition gap with no fresh CFTC data —
  **65**. The standard helper only plots one value per category; the CFTC
  chart needs two bars (Asset Manager, Leveraged Funds) per category
  (ES/NQ/RTY), offset vertically by a fixed height fraction (`h=0.32`,
  reconfirmed clean at edition 65) around each category's tick position.
  **Fix that worked for the legend:** use a FIGURE-level legend
  (`fig.legend(..., loc="lower center", bbox_to_anchor=(0.5, 0.0), ...)`)
  combined with `fig.tight_layout(rect=(0, 0.1, 1, 1))` to reserve the
  bottom 10% of the figure for the legend. Figsize `(9.8, 2.15)` rendered
  cleanly at editions 54 and 65. **Reuse this exact pattern** for any future
  grouped/multi-series chart rather than re-deriving the legend-placement
  fix from scratch.
- PDF: HTML → Chromium print-to-PDF via Playwright. Launch Chromium with an
  explicit `executablePath` (check the environment for the installed
  Chromium build path) and `--no-sandbox`. Do not run `playwright install`.
- Set margins in **exactly one place** — either the CSS `@page` block or the
  Playwright `page.pdf()` margin option, never both (they stack and double
  the margin). Passing `{top:'1in', bottom:'1in', left:'13mm', right:'13mm'}`
  via `page.pdf()` with the HTML body at `margin:0; padding:0` and no CSS
  `@page` block is the pattern that has worked reliably — edition 65 used
  this exact pattern again with no issue, across four renders.
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
      starting a fifth page. **Editions 65 and 66 were both this case.**
      Edition 65 needed the Annex-C-trimming fix afterward (see below);
      **edition 66 converged cleanly as soon as the break was deleted, with
      comfortable room to spare on page 4** — a reminder that the spillover
      case does not always need a second fix.
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
  **Editions 61 through 64 all confirmed 1**, the common case; **editions 65
  and 66 both confirmed 0**, the spillover case; **edition 67 confirmed 1
  again** — sections 1-6 ended comfortably on page 3 that edition; **edition
  68 confirmed 0** — a genuine spillover, resolved cleanly by deleting the
  break on the second render with no Annex-C column-balance symptom; **edition
  69 confirmed 1 again** — sections 1-6 ended comfortably on page 3 with
  meaningful room to spare (an unusually large single-stock movers section
  notwithstanding), converging on the first render. **Edition 70 confirmed
  0** — a genuine spillover that also needed the Annex-C-trimming fix (see
  below) before converging on the third render.
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
  through 64 (all four were clean convergences). **The exact symptom
  recurred at edition 65** after a genuine spillover (the forced break was
  correctly deleted, but a lonely Method note was still stranded alone on
  page 5 with Annex C's `.cols3` block nearly filling page 4). Trimming
  Section 2/4 prose and two Annex A entries first had essentially no effect
  — exactly as this lesson predicts — and only shortening roughly twenty of
  Annex C's own citation entries converged it cleanly to 4 pages. **The
  symptom recurred a third time at edition 70**, again after deleting the
  break on a genuine spillover left the Method note stranded alone on page 5
  with Annex C's `.cols3` block nearly filling page 4; shortening roughly 30
  of Annex C's own entries down to outlet/date only converged it cleanly on
  the third render. This is now confirmed a recurring, recognizable pattern
  (60, 65, 70), not a one-off: when a lonely trailing block is stranded
  alone on an extra page, go straight to trimming Annex C's own citations
  rather than preceding prose. **Edition 66, also a genuine spillover, did
  NOT hit this symptom** — deleting the break alone converged cleanly with
  page 4 well under capacity, confirming the edition-60/65/70 symptom is
  a possibility to check for on a spillover, not a certainty.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix.
- **A markup-correctness trap, logged at edition 47: a `<sup class="ref">`
  citation tag placed immediately after a table row's last `</td>` but still
  inside the `<tr>` (i.e. not nested inside any `<td>`) is invalid table
  structure.** `check_refs.py` will NOT catch this. **Always nest every
  `<sup class="ref">` tag inside a `<td>...</td>` pair, never as a sibling of
  one inside a `<tr>`** — grep for `</td><sup` as a quick self-check if a
  table was built with a lot of copy-paste. **Editions 55 through 70 all ran
  the same proactive grep and found zero instances, a SIXTEENTH consecutive
  clean sweep.** Run the grep on every edition with such a table, not just
  when troubleshooting a layout problem.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count
  alone. **Edition 67 converged in ONE render** — sections 1-6 ended
  comfortably on page 3 with the forced break kept (the common case); final
  source count 24. **Edition 68 needed TWO renders**, the same pattern as
  edition 66: the first (forced break retained) hit a genuine page-4
  spillover; deleting the break converged cleanly on the second render, page
  4 comfortably under capacity, no Annex-C column-balance symptom; final
  source count 26. **Edition 69 converged in ONE render** — sections 1-6
  ended comfortably on page 3 with meaningful room to spare, the forced
  break kept, despite an unusually large (13-row) single-stock-movers table;
  final source count 25 (25/25 clean after one quick fix — see the
  check_refs.py entry above). **Edition 70 needed THREE renders, combining
  two distinct causes in sequence — a useful reminder these can stack.**
  First render (forced break kept): a genuine page-4 spillover (sections 1-6
  ran past page 3). Second render (break deleted): still 5 pages — the
  edition-60/65 lonely-trailing-block symptom recurred, with Annex C's
  `.cols3` block filling nearly all of page 4 and stranding the Method note
  alone on page 5. Third render (after shortening roughly 30 of Annex C's
  own citation entries to their outlet/date only, per the edition-60/65
  fix): converged cleanly to 4 pages, Method note fitting at the bottom of
  page 4 with room to spare. Final source count 31 (31/31 clean on the very
  first check, no fix needed — zero stray tildes and zero `</td><sup`
  instances throughout).

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
  runs short — editions 44 through 68 have all folded commodities, FX and
  Treasuries into ONE combined table (10-17 rows; edition 62 used 14,
  edition 63 used 13, edition 64 used 15, edition 65 used 14, edition 68
  used 14) as the PRIMARY commodities table rather than padding, now the
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
  broadening selloff across consecutive sessions. **Editions 61 through 68
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
    5**. Editions 24, 34, 39, 44, 49, 54 and 65 have all placed it there.
    **Not used at edition 66, 67 or 68** — no new CFTC report had posted in
    any of the three (still the Monday 16 Nov data); the next opportunity
    is Friday 20 November 2026's report under the normal weekly cadence,
    which should now land inside edition 69's window.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully. Not used at editions 55
    through 68 — edition 68 had no single dominant earnings print of that
    kind (the session's dominant stories, Anthropic's IPO and AMD's
    short-report decline, don't fit this chart's implied-vs-realized shape).
  - A holiday-window preview edition with no fresher data → VIX futures
    term structure with event annotations, in **Section 5**. Not used at
    editions 55 through 68 — the VIX complex has spiked sharply at editions
    63, 65, 66 and 68 but was judged secondary to a larger dominant story
    each time (NVIDIA leadership at 63, the chip-complex selloff and CFTC
    chart at 65, NVIDIA's own earnings at 66, Anthropic's IPO/AMD's
    short-report decline at 68) and handled fully in prose instead.

**Edition 71 (expected to cover Tuesday 24 November 2026, assuming no gap —
a normal full session, no holiday).** The dominant story reversed completely
at edition 70 (Nvidia's board reinstating Huang, powering a broad relief
rally); several of edition 69's open threads resolved or were superseded.
Verify directly rather than assuming:
- **Whether Monday's broad relief rally (S&P +4.7%, Nasdaq +6.5%, 9 of 11
  sectors higher) holds, extends, or fades** — and specifically whether
  NVDA's +31.59% pop round-trips the way its 17 November earnings pop did,
  or holds. Watch the whole AI-capex complex (MU, BE, INTC, GLW, AMAT, SMCI)
  for the same pattern.
- **Whether Nvidia's confirmed 1-2 December congressional testimony dates
  still proceed now that Huang is reinstated as CEO** — no outlet has
  addressed this yet; check directly.
- **Independent corroboration (or refutation) of the single-sourced WSJ
  claim that the SEC opened a civil probe into Nvidia's own disclosures** —
  check Reuters, AP, Bloomberg, CNBC and the NYT directly again; a fresh
  EDGAR check (CIK 0001045810) was clean through edition 70 beyond the 23
  Nov reinstatement 8-K itself.
- **Whether ANT's first options listing goes live** (expected around Monday
  23 Nov per Cboe's timing rule but not confirmed live as of edition 70's
  cutoff) — get the first implied-vol read if so. Also watch whether ANT's
  post-IPO fade (now three straight sessions, including Monday's -1.43%
  taken against the broader market's own rally) continues, stabilizes, or
  reverses.
- **AMD's Hunterbrook-driven decline** — no new developments found at
  edition 70 (the stock's Monday gain was attributed to the broad rally
  alone); watch for any fuller company rebuttal or read-across.
- **UnitedHealth's (UNH) CMS Medicare Advantage RADV-audit overhang** —
  Monday's -1.11% reversed Friday's unexplained +2.84% bounce with no fresh
  catalyst found either way; watch for continuation.
- **Whether December FOMC hike odds (approx. 94% on DeFi Rate's blend /
  Kalshi's own direct read as of edition 70, up from approx. 90%) continue
  to re-firm, stabilize, or ease** — pull all three again using the
  corrected Kalshi query (`event_ticker=KXFEDDECISION-26DEC`); keep trying
  CME FedWatch (failed 31 straight editions) and a non-stale Polymarket
  query too.
- **Banxico's next policy-decision date** — unresolved for twelve straight
  editions; the calendar viewer itself works again (2027 is selectable) but
  returns no entries. De-prioritized, but worth a quick check.
- **A primary-source document for the reciprocal-tariff-truce extension to
  10 January 2027** — unconfirmed by any US primary source for eleven
  straight editions; every angle tried so far has failed (see the dedicated
  Standing Facts entry for what to try next).
- **EUR/USD and GBP/USD's new direction conflicts, and USD/JPY's
  three-edition-standing one** — check whether any resolve or all three
  persist; also re-attempt the DXY futures-contract variant, still
  unreachable on both vendors.
- **US Treasury par yields** — continue the normal every-edition
  reconciliation; Monday's partial reversal of Friday's rally (front end up,
  long end down slightly) is worth watching for continuation.
- **Government funding status (H.R. 6500)** — edition 70 got a fresh direct
  primary confirmation via whitehouse.gov; watch for any Senate floor action
  on the twelve FY2027 bills (all now committee-reported in both chambers).
- **The week-ahead calendar**: Q3 2026 GDP's second estimate plus corporate
  profits (Wed 25 Nov, 8:30am ET) lands inside edition 71's likely window —
  get the actual print. Note the previously-flagged "G.17 benchmark revision
  due 24 Nov 2026" was a one-year misdate in this report's own research
  (corrected at edition 70) — do not expect or look for it. Thanksgiving
  (Thu 26 Nov, full closure) and its Friday half-day (27 Nov) remain
  SETTLED, just ahead on the calendar.
- **LME copper's 3-month Friday base** — unobtainable at edition 70 despite
  four retries; try again, and keep checking whether lme.com's 403 block
  lifts.
Dates to hold on to (edition-to-session mapping: 68 published Fri 20 Nov,
covering Thu 19 Nov; 69 published Mon 23 Nov, covering Fri 20 Nov, a
weekend-gap edition; 70 published Tue 24 Nov, covering Mon 23 Nov; 71
expected to cover Tue 24 Nov). RBA next decision 7-8 Dec 2026; the Fed and
BoC both meet 8-9/9 Dec 2026; SNB 10 Dec 2026; Riksbank approx. 16 Dec 2026;
BoE 17 Dec 2026; the ECB and BoJ both meet 16-18 Dec 2026. The next monthly
settled-facts audit falls on the first edition of December 2026.
Thanksgiving (26 Nov, full closure) and its Friday half-day (27 Nov) remain
SETTLED — no further calendar check needed unless a contradiction surfaces;
the window will reach these dates around edition 72-73 if no gaps. **The
CFTC's next Commitment of Traders report (covering 24 Nov data) is now
confirmed due Monday 30 November 2026** (a Thanksgiving-week holiday
adjustment, confirmed directly via cftc.gov's own release-schedule page at
edition 70, correcting the previous assumption of a normal Friday 27 Nov
cadence) — do not expect a fresh report inside edition 71's window.

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

**Edition 69's carried-forward spec was 157,745 bytes, over the
100,000-byte threshold — this run (producing edition 70's spec) condenses
the log again.** This run folds edition 68 into the mega-block (now
genuinely "Editions 1-68"); edition 69's own full-detail entry is condensed
down to a medium paragraph; edition 70 is added in full detail. There is no
maximum size; condensing is housekeeping done by the run itself, not a
check to pass — there is no penalty for the file staying somewhat large if
the alternative is losing information.

**Editions 1–68 (condensed):** established the format (edition 1 baseline;
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
Edition 54 (Mon 2 Nov, weekend-gap): a tech-led selloff (S&P -1.82%) on
Intel's historic -28.58% collapse (worst day since 1974); BoJ held at
approx. 1.25%; China's October PMI slipped below 50; the November monthly
settled-facts audit completed cleanly across all ten central-bank rows.
Edition 55 (Tue 3 Nov): equities diverged on composition (Dow +0.41%,
S&P -0.51%, Nasdaq -1.07%) as crude collapsed 7-11% on an Iran/US thaw
signal; Apple fell on a soft margin outlook; Marvell agreed to acquire
Lumentum (Marvell -12.72%, Lumentum -18.59%); BoJ's/SNB's next-meeting
dates resolved, ECB's rate complex promoted to SETTLED. Edition 56 (Wed 4
Nov): a megacap/AI bounce (S&P +0.36%, Nasdaq +0.83%, Dow -0.38%); RBA's
fifth 2026 hike (25bp to 4.85%, first-ever split vote); AMD's Q3 beat drew
a genuinely positive AH reaction. Edition 57 (Thu 5 Nov): the 3 November
US midterm elections (Democrats won both chambers) drove Dow +3.03% to
53,356.12 (then the largest one-day move logged), WTI -8.3%; Riksbank's
surprise 25bp hike to 2.00%. Edition 58 (Fri 6 Nov): a full reversal on an
AI-capex/data-center-moratorium scare — S&P -4.4%, zero of 11 sectors
higher, VIX's sharpest one-day increase on record (+69.66%); BoE hiked 25bp
to 4.00% same session Banxico reportedly cut to 6.25% (later primary-
confirmed); December hike odds swung from approx. 77-80% to approx. 66.5%
within two editions, the first of several sharp rate-odds reversals this
stretch.
Edition 59 (Mon 9 Nov): a much-stronger-than-expected October jobs report
(+165,000 vs. approx. +65,000 consensus) snapped December hike odds from
approx. 66.5% back to approx. 76.5-77%; a fresh vendor-revision trap hit
WTI/gold/silver/COMEX copper, Kitco's historical-close pages became
inaccessible for the first time. Edition 60 (Tue 10 Nov): an 11-of-11-sector
relief rally (S&P +2.3%, best day since 8 April) on an Iran de-escalation
oil crash; Nvidia alone fell (-4.27%, the Megaspeed/Huang overhang) on a
dramatic board-investigation claim excluded as uncorroborated — overturned
as TRUE the very next edition; first Annex-C column-balance overflow
symptom, fixed by trimming Annex C directly. Edition 61 (Wed 11 Nov):
October's hot CPI (no y/y figures published, a 2025-appropriations-lapse
gap) firmed hike odds to approx. 85-86%; Nvidia's board-investigation
story was independently re-verified and found TRUE (NVDA -5.47%). Edition
62 (Thu 12 Nov, Veterans Day — equities open, Treasury/Fed closed): a
broad CoreWeave-led relief rally (S&P +1.3%, 10 of 11 sectors higher);
CoreWeave's Q3 (revenue $3.661bn +168% y/y) drove +24.71%; SEC EDGAR
resolved the SKYD/PSKY ticker-identity confusion; US midterm-election
certification clarified as having no single national step at all.
**Edition 63** (Fri 13 Nov, covering Thu 12 Nov): NVIDIA's own 8-K
confirmed **Jensen Huang's resignation** as President/CEO/board member
effective immediately — the dominant story by a wide margin, tied in press
reporting to Huang's own disclosed extramarital relationships; CFO Colette
Kress became interim CEO, director Harvey C. Jones became first-ever
independent Board Chair; NVDA closed -4.34% to $166.19. December hike odds
firmed to approx. 85-88.5%. This edition's own date line contained an
error, caught and corrected at edition 64: it read "Thursday 13 November
2026," but 13 November 2026 is a Friday (see the dedicated header-details
entry near the top of this spec).

**Editions 64 through 68 (folded into the mega-block above at edition 70):**
Edition 64 (Mon 16 Nov, covering Fri 13 Nov, weekend-gap): a sharp reversal
of the week's rotation into Nvidia's chip-sector rivals on profit-taking
(AMD -8.75%, Broadcom -4.76%, no company-specific news — the first "verify
a clean negative" instance); equities eased modestly (S&P -0.41%); October
PPI mixed; three different reactions to three beats; first correction box
since edition 53. Edition 65 (Tue 17 Nov, covering Mon 16 Nov): the
post-Huang-resignation chip slide extended a third session ahead of
NVIDIA's own earnings (NVDA -4.12%, AMD -5.58%, AVGO -3.92%, plus a wider
sympathy decline); equities posted their worst session since 6 Nov (S&P
-1.9%); VIX spiked +18.70% powering a fresh CFTC positioning chart;
Thanksgiving/Friday-half-day promoted to SETTLED. Edition 66 (Wed 18 Nov,
covering Tue 17 Nov): NVIDIA's Q3 FY2027 beat crushed consensus (revenue
$115.8bn +103% y/y) but the AH reaction was disputed across vendors
(approx. +2% to +5%); new Board Chair Harvey Jones said the board does not
intend to reinstate Huang; the regular session fell broadly (S&P -1.0%,
zero of 11 sectors higher); Home Depot's beat-and-raise nonetheless fell
-2.45%; converged in two renders (genuine page-4 spillover). Edition 67
(Thu 19 Nov, covering Wed 18 Nov): NVIDIA's AH pop fully round-tripped in
its first full regular session (NVDA -2.89% to $150.96, a clean volatility
crush); the chip-sector read-across rally broadened (AMD +5.31%, Broadcom
+3.64% — these two tickers were originally published SWAPPED in edition
67's own text, corrected at edition 68); equities closed a diffuse,
composition-driven session (S&P -0.23%, Nasdaq +0.42%); Target and Lowe's
beat; FOMC minutes flagged AI-capex as an inflation risk for the first
time; converged in one render, 24/24 sources clean. Edition 68 (Fri 20 Nov,
covering Thu 19 Nov): Anthropic's (ANT) record-breaking Nasdaq debut
($81.3bn raised, the largest IPO on record; priced $83, closed Thursday
+17.1% at $97.17 before easing in AH) was the dominant story, against which
the broader market sold off sharply — equities posted a sixth straight loss
and the stretch's worst breadth (S&P -2.0% to 7,175.83, Dow -2.2% to
49,097.06, first sub-50,000 close since June, Nasdaq -2.3%, 0 of 11 sector
ETFs higher). AMD fell -7.72% to $489.19 on short-seller Hunterbrook's
China/IEIT Entity-List allegations; the chip complex fell in sympathy.
Earnings produced divergent reactions to similar beats: Palo Alto Networks
+6.42%, Lowe's -1.63%, Walmart -1.04%, Williams-Sonoma -15.16%, UnitedHealth
a further -5.55% on its CMS RADV-audit overhang. Macro ran uniformly soft
(jobless claims 203k, Philly Fed collapsed to 6.3 from 20.9); December FOMC
hike odds held near approx. 92%; VIX spiked into full-length backwardation
(+15.80% to 28.44). Needed two renders (genuine page-4 spillover); 26/26
sources clean. Correction box used (second since edition 64) to fix edition
67's own AMD/Broadcom ticker swap.

**Edition 69 (condensed)** — Monday 23 Nov, covering Friday 20 Nov (a
weekend-gap edition): a severe, broad AI-sector capitulation put the S&P
and Dow into correction territory — S&P 500 -3.7% to 6,910.39, Dow -1.9% to
48,147.33, Nasdaq Composite -5.3% to 22,617.73 (negative for the year, worst
week since March 2020), a seventh straight S&P losing session; only 1 of 11
sector ETFs higher (Consumer Staples). The PHLX Semiconductor Index fell
10.7% with no single catalyst beyond a broad AI-capex repricing: Nvidia
-14.01% to $125.53 (ninth decline in ten sessions), Micron -13.89%, AMD
-13.25% (extending Thursday's Hunterbrook decline, cumulative approx. -20%
over two sessions), Broadcom -12.19%, Applied Materials -10.71%, Corning
-10.94%, Super Micro -9.19%, Intel -7.97%, Bloom Energy -15.30% (largest
mover); Anthropic (ANT) -8.50% to $88.91 on its second trading day. Earnings
again showed "beat guarantees nothing": Intuit's clean beat drew a
one-session-delayed -12.77% decline; Ross Stores fell -2.92% despite a
beat-and-raise; UnitedHealth bounced +2.84% with no identified catalyst.
Two new Nvidia-adjacent government-scrutiny threads surfaced (dated 16-17
Nov, disclosed as a catch-up): a confirmed Commerce/DOJ criminal probe into
customer Megaspeed (no allegations against Nvidia), and an unconfirmed,
single-sourced WSJ claim of an SEC civil probe into Nvidia's own
disclosures; congressional testimony confirmed for 1-2 December. UMich's
final November sentiment rose sharply to 51.5; Fed Governor Cook gave a
hawkish-leaning speech; December FOMC hike odds eased to approx. 90%
(DeFi Rate), down from approx. 92%; Treasury yields fell sharply across the
curve (10-yr -12bp) even as gold (-4.62%) and silver (-7.41%) also sold off
hard; the VIX complex spiked +26.19% to 35.89 (a newly diagnosed CBOE feed
bug understated the feed's own displayed percentages). No third chart used.
Converged in one render; 25/25 sources clean after one quick fix.

**Edition 70 (most recent — full detail)** — Tuesday 24 November 2026
report covering Monday 23 November 2026, the window's one NYSE session
(research window Sun 22 Nov 2026 20:00 ET through Mon 23 Nov 2026 20:21 ET).

**The dominant story was Nvidia's board reinstating Jensen Huang as
President and CEO, effective immediately Monday morning — a reversal of
the board's own 17 November position — which powered this report's largest
single-session index reversal yet.** Confirmed directly via Nvidia's own
8-K (SEC EDGAR, CIK 0001045810, accession 0001045810-26-000090) and press
release, independently corroborated same-day by CNBC, Bloomberg, NBC News,
Axios, CNN and Al Jazeera. The board's unanimous vote cited being
"satisfied with respect to Mr. Huang's candor and ability to lead" and,
after input from "senior levels of the United States government," said it
is "confident" reinstatement poses no national security risk; Colette
Kress returns to CFO-only; a new independent-directors committee continues
investigating the original foreign-intelligence-targeting reports "to
conclusion," and a National Security and Export Control Committee has been
formed. President Trump told CNBC he "convinced" the board to reinstate
Huang. NVDA surged +31.59% to $165.19 — its best day since May 2003 — and
the broader market rallied sharply in sympathy: S&P 500 +4.7% to 7,237.17,
Dow +3.0% to 49,595.31, Nasdaq Composite +6.5% to 24,089.56 (its best day
since 9 April 2025), Russell 2000 +3.4% to 2,669.66, confirmed via AP's wire
(wtop.com/lanacion.com.ar mirrors) and cross-checked against SPY's own
price history and Yahoo Finance's live-quote sidebar. Breadth flipped from
Friday's 1-of-11 to **9 of 11 SPDR sector ETFs higher**, Technology
(+8.97%) the clear leader; only Energy (-1.06%) and Cons. Staples (-0.09%)
lagged. The whole AI-capex complex rallied in sympathy: Micron +19.04%,
Bloom Energy +18.09%, Intel +16.34%, Corning +14.76%, Applied Materials
+14.62%, Super Micro +13.30%, AMD +6.85% (its Hunterbrook-driven decline
halted with no new news), Broadcom +3.00%. Every figure was individually
verified against each ticker's own stockanalysis.com price-history page,
not a bundled summary. UnitedHealth -1.11% (reversed Friday's unexplained
bounce) and Anthropic (ANT) -1.43% to $87.64 (a mild continuation of its
post-IPO fade, notably NOT following the broader rally) were the session's
only notable decliners; ANT's expected Monday options listing did not
appear to go live. Zoom Communications and Symbotic both reported
after Monday's close (both beat; Zoom's regular-session gain was
rally-driven, not an earnings reaction, and it eased -0.55% AH; Symbotic
similarly eased -0.23% AH). December FOMC hike odds re-firmed sharply to
approx. 94% (DeFi Rate blend; Kalshi's own two-edition-standing empty-array
API bug was root-caused and fixed — the series ticker was simply wrong).
Government funding (H.R. 6500) got a fresh direct primary re-confirmation.
The VIX complex partially unwound Friday's panic spike (VIX -25.83% to
26.62), the feed's bug clean this edition; the front end of the term
structure remains inverted even as the back end eased into slight contango.
Gold (+3.28%) and silver (+4.65%) rallied sharply on the SAME session
equities also rallied — a different pairing from Friday's deleveraging.
EUR/USD and GBP/USD both developed fresh cross-vendor direction conflicts,
joining USD/JPY's three-straight-edition one. CFTC's next report was found
to be holiday-adjusted to Monday 30 November, not Friday 27 as previously
assumed. A standing forward-flag about a "24 November 2026 G.17 benchmark
revision" was found to be a one-year misdate in this report's own prior
research and corrected (no such 2026 date exists on the Fed's own
schedule). No third chart used (the equity story dominated the page
budget). Needed THREE renders — a genuine page-4 spillover, then a
recurrence of the edition-60/65 lonely-trailing-block symptom (fixed by
trimming Annex C's own citations) — converging cleanly to 4 pages; 31/31
sources clean on the first check.

**Open threads for edition 71** are listed in the dedicated "Edition 71
(expected to cover...)" section earlier in this spec — not repeated here
to avoid duplication.
