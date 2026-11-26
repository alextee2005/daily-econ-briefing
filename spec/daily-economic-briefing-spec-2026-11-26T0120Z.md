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
  applied correctly for **fifty straight editions (33 through 72)** —
  treat as settled; edition 70 read "Tuesday 24 November 2026," covering the
  Monday 23 November session. Edition 71 read "Wednesday 25 November 2026,"
  covering the Tuesday 24 November session. **Edition 72 read "Thursday 26
  November 2026," covering the Wednesday 25 November session** — the edition
  date itself is Thanksgiving Day (a full market closure), while the session
  covered is the prior day's normal trading session; this is the correct
  reading of the rule, not an exception to it.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 72 all reused the
  same pattern — now confirmed clean across **forty-four consecutive
  editions**; edition 71 phrased it "Window: Mon 23 Nov 2026 20:00 ET – Tue
  24 Nov 2026 20:21 ET (Tue 24 Nov close/AH, the window's one NYSE
  session)"; **edition 72 phrased it "Window: Tue 24 Nov 2026 20:00 ET – Wed
  25 Nov 2026 20:20 ET (Wed 25 Nov close/AH, the window's one NYSE
  session)."** No further confirmation needed; treat this as settled.
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
  edition 63's error immediately. Editions 66 through 71 all ran this check
  and found it clean every time. **Edition 72 ran it too** (`date -d
  "2026-11-26" +%A` returns Thursday, matching the date line "Thursday 26
  November 2026") and also found it clean. Continue running this check
  every edition.
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
  before publishing.** Editions 70 and 71 both applied this from the start on
  dense multi-name AI-capex clusters, with no swap or mismatch found either
  time. **Edition 72 continued the same discipline** on a nine-name AI-capex
  cluster (NVDA, MU, AMD, INTC, SMCI, AMAT, BE, GLW, AVGO) plus a four-name
  same-day earnings cluster (HP, Dell, Workday, Deere) — every figure came
  from either that ticker's own stockanalysis.com price-history page or a
  primary 8-K, not a bundled summary; no swap or mismatch found.

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
half-day session (Friday 27 November) remain SETTLED** — directly confirmed
at edition 65 via nyse.com's own 2026/2027/2028 holiday-calendar announcement
and sifma.org's 2026 holiday-schedule recommendation: Thursday 26 Nov is a
full closure for both equities and bonds; Friday 27 Nov is a half-day for
equities (1:00pm ET close, 1:15pm for eligible options) with an early bond
close recommended by SIFMA (non-binding on individual firms). **Edition 72
is itself dated Thursday 26 November 2026 (the holiday) while covering
Wednesday 25 November's normal session** — the holiday closure did not need
a fresh calendar check, only correct application of the already-settled fact
to the header. No further re-confirmation needed unless a contradiction
surfaces. **Veterans Day (Wednesday 11 November 2026) itself is resolved/
closed history, not a forward item any more** — directly observed at edition
62: equities traded a full normal session while Treasury cash markets and
the Federal Reserve were closed, exactly as expected.

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
holidays and potential gaps. **None of the ten central banks met or changed
their rate inside edition 72's window** — the table carries forward
unchanged with no fresh fetch needed, consistent with no scheduled meeting
landing between Tue 24 Nov and Wed 25 Nov.

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
- **Rate-path odds grew noticeably harder to pin to one clean number at
  edition 72 — likely a process gap, not necessarily a genuine reversal.**
  Edition 71 had read approx. 93% for a December 25bp hike via DeFi Rate's
  own blended snapshot. **Edition 72's macro research pass did not check
  DeFi Rate at all** and instead went directly to Kalshi and Polymarket,
  finding: Kalshi's own "fed rate odds" summary page (self-timestamped
  5:26am ET) read approx. **77%** hike / 25% hold (figures that don't sum
  cleanly to 100%, suggesting a snapshot artifact); other indexed Kalshi
  pages (undated/stale) ranged 70-92%; Polymarket's own tracking page
  (via CryptoSlate) carried only a stale 16 November snapshot at 87.5%.
  **CME FedWatch failed to load for a 33rd consecutive edition** (41-72), a
  timeout again, no secondary citation found. **Do not read this as a
  confirmed easing from edition 71's approx. 93% — retry DeFi Rate's own
  blended read directly at edition 73 before concluding anything shifted.**
  The corrected Kalshi query from edition 70 (`event_ticker=
  KXFEDDECISION-26DEC`, not `series_ticker=KXFED-26DEC`) was not explicitly
  re-used this edition's search-based approach; use it directly next time
  rather than relying on Kalshi's own summary page.
- **US-China tariff threads: the Section 301 178-product exclusion extension
  remains resolved with a precise deadline; the second, narrower USTR
  port-fee action remains resolved; the broader reciprocal-tariff truce
  remains unconfirmed by any US primary source for a TWELFTH straight
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
  2027) — still unconfirmed by any US primary document after twelve straight
  editions of trying (60-71). **Edition 72 repeated the check via the
  Federal Register developer API and whitehouse.gov's presidential-actions
  listing and again found nothing**: only one new Executive Order appeared
  in the window (an unrelated federal-contracting order, 25 Nov 2026, doc.
  2026-24114), and no USTR/Treasury statement extending EO 14358 itself was
  found. This exactly matches edition 71's finding — the US order (EO
  14358, which expired by its own terms on 10 Nov 2026) remains without a
  confirmed US-side extension document, while China's own extension (9 Nov
  2026) remains primary-confirmed on its side only. **Try at edition 73**: a
  different search angle again (e.g., Commerce/BIS press releases, a
  congressional-record mention, or a trade-press report citing a specific
  document number) rather than repeating the same federalregister.gov/
  whitehouse.gov sweep a sixth time.
- **Fed Chair: Kevin Warsh — SETTLED, stop re-verifying it every run.** No
  contradiction surfaced through edition 64; directly re-confirmed via
  federalreserve.gov's own bios page at edition 54's November monthly audit,
  closing that housekeeping item cleanly; not re-attempted since. His
  Chairman term ends 21 May 2030 (took office 22 May 2026, a four-year term);
  his separate term as a Board of Governors member runs to 31 January 2040.
  The Chairmanship re-opens as a live fact only on a successor nominated/
  confirmed, a resignation or removal, or that 21 May 2030 term-end date
  actually arriving, or the **next monthly audit (first edition of December
  2026)**.
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
  canvasses, all by 23 Nov, previously logged). Not independently re-attempted
  since edition 66 (no new state-certification news has fallen inside any
  window since); continue watching specific state deadlines as they land
  rather than searching for a single national resolution event that does not
  exist.
- **The NVIDIA/Huang governance thread: the board reinstated Huang as
  President/CEO/Board director Monday 23 November 2026, effective
  immediately; a testimony-schedule question and the WSJ's SEC-probe claim
  are the only live pieces now.** Background (settled history, do not
  re-derive): Huang resigned effective 11 Nov 2026 (8-K, accession
  0001045810-26-000082); CFO Colette Kress became interim CEO, director
  Harvey C. Jones became first-ever independent Board Chair; Q3 FY2027
  results (17 Nov, 8-K accession 0001045810-26-000088) crushed consensus
  (revenue $115.8bn +103% y/y, non-GAAP EPS $2.68, Q4 guidance $130.0bn
  &plusmn;3%); NVDA's AH pop fully round-tripped in the next regular session
  and the stock then fell nine of ten sessions into Friday 20 Nov's -14.01%
  close at $125.53, part of a broad AI-sector de-rating with no
  NVDA-specific news. **Monday 23 November's reinstatement** — confirmed
  directly via Nvidia's own 8-K (SEC EDGAR, CIK 0001045810, accession
  0001045810-26-000090) and press release, independently corroborated
  same-day by CNBC, Bloomberg, NBC News, Axios, CNN and Al Jazeera: the
  board's unanimous vote cited being "satisfied with respect to Mr. Huang's
  candor and ability to lead" and, after input from "senior levels of the
  United States government," said it is "confident that Mr. Huang's
  reinstatement poses no national security risk." Kress returns to
  CFO-only; Jones remains Board Chair. A new independent-directors
  committee continues investigating the original foreign-intelligence-
  targeting reports "to conclusion"; a separate National Security and Export
  Control Committee has been formed; Nvidia is searching for a first-ever
  Chief Compliance Officer. NVDA **+31.59% to $165.19** Monday — its best day
  since May 2003 — then gave back about a fifth of that pop Tuesday 24 Nov
  (-5.86% to $155.38) in a broad AI-capex-complex unwind, and continued
  decelerating Wednesday 25 Nov (-3.91% to $149.30, after falling as much as
  approx. 7-8% intraday before recovering). Two government-scrutiny threads
  remain open: (1) **confirmed, government-sourced** — a joint Commerce
  (BIS)/DOJ statement confirmed a criminal investigation into Nvidia
  customer Megaspeed, with no allegations against Nvidia itself (settled,
  do not re-derive); (2) **unconfirmed, single-sourced** — the Wall Street
  Journal's claim of an SEC civil inquiry into Nvidia's own disclosures,
  still not independently corroborated by Reuters, AP, Bloomberg, CNBC or
  the NYT as of edition 72 (checked again, no new corroboration found).
  Congressional testimony had been confirmed for Huang (1 Dec) and GC Tim
  Teter (2 Dec), both closed-door House Foreign Affairs/Intelligence/China
  Select Committee interviews. **NEW at edition 72**: CNBC reported (24 Nov
  2026) that a member of Congress (Rep. Gabe Amo) expects Huang's 1 December
  session to proceed as scheduled despite the reinstatement; Teter's 2
  December session was not separately reconfirmed in that same article, and
  a separately-mentioned Senate Banking Committee export-control hearing for
  3 December had no status update either. **Still genuinely open for edition
  73**: whether Teter's testimony date is reconfirmed; WSJ corroboration;
  severance/compensation disclosure for the resignation-to-reinstatement
  period; the Rosen Law Firm shareholder class action's status; and whether
  the AI-capex-complex giveback (NVDA, MU, AMD, INTC, SMCI, AMAT, BE, GLW,
  AVGO — all individually verified both Tue 24 Nov and Wed 25 Nov) continues
  decelerating into stabilization or reaccelerates. Keep checking SEC EDGAR
  and congressional press pages each edition.
- **NEW closed thread at edition 72 — Analog Devices' (ADI) -17.37% plunge
  from edition 71, flagged there as a "verified move, no confirmed driver"
  instance, now has a driver, resolving the open thread from the prior
  edition's own "Edition 72" preview section.** ADI's fiscal Q4 FY2026 beat
  (revenue $4.37bn +42% y/y; adjusted EPS $4.06 vs. a $3.88 consensus) was
  overshadowed by essentially flat Q1 FY2027 revenue guidance (approx.
  $4.4bn, in line with the $4.37bn just reported), an operating-margin
  shortfall and a sharply higher FY2027 capex plan ($1.6-1.9bn vs. $0.7bn in
  FY26) — read by investors as a signal the industrial chip cycle (roughly
  half of ADI's sales) may be peaking, with one desk specifically citing
  "crowded positioning" amplifying the reaction, even though the Q1 guide's
  approx. $4.4bn revenue figure technically beat an approx. $4.31bn Street
  consensus that was not locatable at edition 71 (likely same-day
  search-index lag, as edition 71 itself suspected). Confirmed via ADI's own
  8-K (SEC EDGAR) plus dated coverage (Benzinga, 24/7 Wall St, a TD Cowen
  note via Investing.com, all dated 25 Nov 2026). TD Cowen, Truist and
  Bernstein all cut price targets (to $375, $323 and $410 respectively)
  while maintaining their ratings — breaking ADI specifically out of this
  report's long analyst-action dry spell (see the dedicated
  Known-hard-to-source entry below). ADI rebounded +6.44% to $333.11
  Wednesday 25 Nov; the specific narrative for that rebound (oversold
  buying, renewed desk support), sourced only from one lower-tier
  aggregator, was NOT independently corroborated and should not be repeated
  as confirmed fact. **This is a positive instance of the "named secondary
  outlet" trap family worth logging alongside the negative ones**: a
  genuine data gap from a prior edition (not a wrong claim, just an
  unconfirmed driver) got filled by continued search effort one edition
  later, the mirror image of the NVIDIA board-investigation case (excluded
  as uncorroborated at edition 60, confirmed true at edition 61) and the
  Marvell-Lumentum case (unsubstantiated at edition 53, became real M&A at
  edition 55).
- **NEW closed thread at edition 72 — a dense pre-Thanksgiving earnings
  cluster (HP, Dell, Workday, Deere), all confirmed via primary 8-Ks.** HP
  Inc. (Q4 FY2026, reported Tue 24 Nov): revenue $16.0bn (+9.3% y/y),
  non-GAAP EPS $0.83 beating its own prior outlook of $0.69-0.79 (down from
  $0.93 y/y); FY2027 non-GAAP EPS guide $3.15-3.45; Q1 FY27 guide $0.66-0.76
  (no revenue guidance given). Stock fell -3.32% the day it reported but
  rallied +11.49% the next session (Wed 25 Nov) — a one-session-delayed
  digestion of the beat with no specific mechanism identified for the
  timing. Dell Technologies (Q3 FY2027, 8-K dated 24 Nov): record quarterly
  revenue $54.9bn; AI backlog $132.3bn after $60.2bn of new orders; FY27
  guide raised to $202.0bn revenue (+78% y/y), EPS guide $28.24 GAAP/$29.68
  non-GAAP. Stock fell -11.83% the day it reported (a broad pre-earnings
  complex selloff), then fell a further approx. 7% in Wednesday's premarket
  despite the beat-and-raise before clawing back nearly all of it to close
  +0.60% — neither the premarket reaction nor the intraday reversal has a
  confirmed mechanism. Workday (Q3 FY2027, 8-K dated 24 Nov): revenue
  $2.705bn (+11.2% y/y), subscription revenue $2.532bn (+12.8%), non-GAAP
  EPS $2.82 (vs. $2.32 y/y) — a clean beat that drew a clean, if muted,
  positive reaction (+1.79% the report day, +0.68% the next session),
  notably NOT repeating the prior year's approx. -10% post-earnings slide on
  the same quarter. Deere & Co. (Q4 FY2026, 8-K filed 25 Nov, call 10am ET):
  revenue $12.115bn (-2% y/y), diluted EPS $3.89 (vs. $3.93 y/y, a slight
  decline against a single low-confidence pre-earnings consensus estimate
  of approx. $4.07 sourced only from an earnings-preview aggregator); FY2027
  guide $4.50-5.25bn net income (including a one-time pension charge of
  $0.25-0.40bn), segment sales up 5-15% (Production & Precision Ag), flat
  (Small Ag & Turf), flat-to-+10% (Construction & Forestry). Stock rallied
  +4.44% the same session it reported. Do not re-derive any of the four
  companies' figures; HP's rally-timing mechanism and Dell's premarket
  reaction remain genuinely open (Annex B items each edition until
  resolved, not standing open threads requiring dedicated re-search).
- **NEW closed thread at edition 72 — Q3 2026 GDP second estimate and
  corporate profits, released together with October durable goods orders
  and the Fed's Beige Book, all Wednesday 25 November 2026.** GDP: real GDP
  revised up sharply to **+4.3% annualized** (real GDI +4.4%) from the 3.4%
  advance estimate — the strongest print of this cycle — on upward
  revisions to investment and consumer goods spending; the gross-domestic-
  purchases price index was revised down to +2.7% (from +3.0% advance) while
  the PCE price index held at +2.1% headline/+2.5% core, both unchanged from
  the advance reading. Corporate profits (current-production basis) rose
  $206.0bn in Q3, decelerating from Q2's $384.0bn increase. No primary Dow
  Jones/Reuters consensus figure specifically for the second estimate could
  be located; secondary aggregators cited a roughly 3.4-3.5% bar, which the
  revision cleared regardless (resolved via bea.gov directly). Next release
  (third estimate): 23 December 2026. October durable goods orders rose
  **+0.2% m/m** (+0.5% ex-transportation, +0.4% ex-defense), matching the one
  sourced pre-release forecast found (Continuum Economics) — resolved via
  census.gov directly (release CB 26-185). The Fed's Beige Book (2:00pm ET)
  found 8 of 12 districts posting slight-to-moderate growth and 4 flat;
  prices rose moderately with pressure cited from energy, transportation,
  healthcare, insurance and tariffs, input costs generally outpacing selling
  prices; employment rose only slightly via replacement hiring; consumer
  spending was little changed, households "increasingly selective" on
  discretionary purchases, auto sales softer — resolved directly via
  federalreserve.gov. Do not re-derive any of these three releases.
- **NEW closed thread at edition 72 — November 2026 Richmond Fed
  Manufacturing Index, with an unresolved internal-source caveat.** Headline
  composite rose to **3** from October's -2, with new orders and employment
  both improving — the headline figure is independently corroborated via
  Trading Economics, but richmondfed.org's own page showed a component-level
  breakdown inconsistent with its own narrative text (an internal data
  display issue on the bank's own site, not a cross-vendor conflict); not
  resolved this edition, and not worth a dedicated re-check unless it
  recurs on a future release.
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
  quirk. (October's PPI, resolved at edition 64, did NOT have this problem —
  its y/y comparison was intact — so the gap is CPI-specific, not a blanket
  BLS issue.)
- **NEW closed thread at edition 64 — October 2026 US PPI, a genuinely mixed
  print.** Released Friday 13 November 2026, 8:30am ET (BLS,
  bls.gov/news.release/ppi.htm): headline final demand **+0.3% m/m
  (seasonally adjusted) / +6.5% y/y (NSA)**; core (final demand less foods,
  energy, and trade services) **+0.5% m/m / +4.9% y/y**. Headline came in
  cooler than the approx. +0.4% m/m consensus; core came in hotter than the
  approx. +0.3% m/m estimate — a split print that left rate-path odds
  essentially unmoved at the time. Next PPI release: 15 December 2026.
- **September 2026 and October 2026 jobs reports — both closed threads, do not
  re-derive, but watch for revisions in later BLS releases:** September:
  nonfarm payrolls +29,000 (weakest of the cycle) vs. approx. 84,000-90,000
  consensus; unemployment 4.2%. October (resolved at edition 59): nonfarm
  payrolls **+165,000**, a 100,000 upside surprise against a FactSet median
  consensus of **+65,000**; unemployment held at **4.1%**; average hourly
  earnings **+0.4% m/m / +3.1% y/y**; August revised up 53,000, September
  revised up 31,000. This print was the proximate driver of edition 59's sharp
  hawkish rate-odds reversal.
- **University of Michigan FINAL November 2026 consumer sentiment — closed
  thread as of edition 69, primary-sourced to sca.isr.umich.edu.** Headline
  Index of Consumer Sentiment **51.5** (vs. the preliminary 51.0 and
  October's final 48.0); Current Economic Conditions 49.4; Index of
  Consumer Expectations 52.9; year-ahead inflation expectations eased to
  3.7% (from 4.7%), long-run 3.3% (from 3.5%).
- **November 2026 Conference Board Consumer Confidence — closed thread as of
  edition 71.** Headline **103.3**, up 11.4 points from October's 91.9;
  Present Situation Index 132.8 (+13.7), Expectations Index 83.6 (+9.9). No
  vendor conflict found.
- **General principle for everything still live: do not assume a routine
  macro-calendar fact (meeting dates, symposium schedules, other central
  banks' policy rates, government funding status) from memory or from the
  prompt's own framing — verify it fresh from a primary source
  (federalreserve.gov, bankofengland.co.uk, boj.or.jp, kansascityfed.org,
  norges-bank.no, riksbank.se, banxico.org.mx, snb.ch, rba.gov.au,
  ecb.europa.eu, bankofcanada.ca, whitehouse.gov, etc.) every edition, exactly
  like any other data point, until an entry below is marked SETTLED.** These
  are the rates and dates that feed Section 3's policy-rate table. Per-bank
  status as of edition 72 (none contradicted, no fresh meeting fell inside
  edition 72's window, so no fetch needed beyond a quick news check):
  - **Reserve Bank of Australia:** current rate **4.85%**, hiked 25bp on
    Tuesday 3 November 2026 (6-3 split vote, its fifth hike of 2026) —
    SETTLED pending the RBA's own next decision, **7-8 December 2026**.
  - **Bank of England:** rate **4.00%**, hiked 25bp on Thursday 5 November
    2026 (8-1 vote, Mann dissenting for +50bp) — SETTLED pending the next
    decision, **17 December 2026**.
  - **European Central Bank:** rate complex (deposit facility 2.50%, main
    refi 2.65%, marginal lending 2.90%) **SETTLED**; next Governing Council
    meeting **16-17 December 2026**.
  - **Bank of Japan:** current rate approx. 1.25%, SETTLED pending its own
    next meeting, **17-18 December 2026**.
  - **Bank of Canada:** SETTLED. Current rate 2.50%, hiked 25bp 28 October
    2026. Next decision **9 December 2026** (same date as the Fed's).
  - **Swiss National Bank:** current rate 0.00%, SETTLED. Next assessment
    **10 December 2026**.
  - **Norges Bank:** current rate **4.50%** (hiked 25bp 24 Sept 2026),
    SETTLED. Next full decision remains **17 December 2026**.
  - **Riksbank:** current rate **2.00%**, hiked 25bp on Wednesday 4 November
    2026, confirmed unanimous 5-0 via the bank's own primary minutes —
    SETTLED pending the next decision, **approx. 16 December 2026**.
  - **Banxico — the rate and vote remain primary-source confirmed; the
    next-decision date remains unresolved for a FOURTEENTH straight
    edition.** Banxico cut its overnight interbank rate 25bp, from 6.50% to
    6.25%, decision dated 5 November, effective 6 November 2026, a 3-2 vote
    — primary-confirmed via Banxico's own 5 November press-release PDF.
    banxico.org.mx's calendar viewer continues to show no 2027
    monetary-policy dates posted; de-prioritized per standing guidance, try
    again only briefly each edition until the bank actually publishes its
    2027 calendar (likely a December or January event).
  - **Government funding/shutdown status:** H.R. 6500 funds federal agencies
    through 11 December 2026, no shutdown in effect. As of edition 72, the
    Senate Appropriations Committee had released draft text for all twelve
    FY2027 bills but **neither chamber has passed any FY2027 bill on the
    Senate floor** — the funding-cliff risk still points to the 11 December
    deadline. Continue the standard re-check-every-edition discipline
    regardless.
- **China September 2026 CPI/PPI and October 2026 PMI — both RESOLVED, closed
  threads:** CPI +0.9% y/y (+0.2% m/m), PPI +5.0% y/y; October manufacturing
  PMI 49.3 (down from 50.1), non-manufacturing PMI 49.7 (down from 50.2), both
  back below the 50 threshold.
- **China Q3 2026 GDP — RESOLVED at edition 45, closed thread:** Q3 alone
  +4.5% y/y, +1.2% q/q; first-three-quarters cumulative +4.6% y/y.
- **New Mexico v. Meta — the $25bn civil-penalty ruling (Judge Francis
  Mathew, Wed 21 Oct 2026) remains substantially clarified but Meta's formal
  notice of appeal remains unconfirmed; this is a low-priority item
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
  directly observed at edition 62) are both now resolved/closed history.
  **Thanksgiving (26 Nov, full closure for both equities and bonds) and the
  Friday half-day (27 Nov) remain SETTLED** — see the Schedule section above;
  edition 72's own header correctly applied this (edition date falls on the
  holiday itself; session covered is the prior normal trading day). The DST
  transition (ended Sunday 1 November 2026) remains itself resolved/settled.
- **Materials (XLB) has led the SPDR sector-ETF panel for two straight
  sessions (Tue 24 Nov +0.54%, Wed 25 Nov +2.07%) with NO driver identified
  either time, despite a dedicated search both editions.** This has moved
  from a one-off unexplained reading to a recurring pattern worth a more
  deliberate push at edition 73 if it continues a third session — check
  commodity-linked constituents, M&A activity, and any sector-specific
  analyst action rather than repeating the same general news search.
- **The vendor-retroactive-revision trap continued at edition 72 across
  WTI, Brent, Henry Hub and gold, with WTI and Henry Hub showing genuine
  IMPROVEMENT this time.** WTI: Investing.com and Yahoo agreed on the exact
  same $83.68 prior-close base for the first time in several editions, with
  only a modest direction-consistent magnitude gap (+0.55% vs. +0.72%) —
  treat this as a possible, not yet confirmed, sign the WTI base-tracking
  issue is settling down. Henry Hub (front-month NGF7, January): both
  vendors referenced the SAME contract for the first time in recent
  editions (Investing.com's prior mis-keying problem did not recur), though
  a small (~1.8&cent;) base gap persists — a genuine partial improvement,
  not a full resolution. Brent remains the stickiest: Investing.com and
  Yahoo's prior-close bases continue to drift apart, and both vendors'
  current bases sit well above what this report's own hand-computed Tuesday
  figures would imply — the cross-vendor base-revision problem persists on
  this one leg specifically. Gold split three ways at edition 72:
  Investing.com (-0.15%) and Kitco's explicitly-dated live spot (-0.43%)
  both showed a modest decline; Yahoo's futures print (+0.99%) arrived
  bundled with a page-level display glitch (a conflicting "Market
  Open"/"U.S. markets closed" banner plus an error element) and was treated
  as the less reliable outlier rather than resolved into an average.
  Silver agreed on direction across all three sources (a rebound after
  Tuesday's selloff) but with sharply different magnitudes (Investing.com
  +2.38%, Yahoo +2.68%, Kitco's live spot a far more muted +0.34%) — a
  magnitude, not direction, disagreement. Continue expecting any of these
  four instruments to disagree or revise at any given edition; disclose as a
  vendor data-quality issue, not a reader-facing correction.
- **FX cross-vendor status improved materially at edition 72, continuing a
  partial recovery that began at edition 71.** EUR/USD's two-edition-standing
  cross-vendor DIRECTION conflict resolved: both Investing.com (-0.05%) and
  Yahoo (-0.09%) showed a modest decline Wednesday, though Yahoo's own
  prior-close base is still revised substantially upward from its own last-
  published Tuesday figure (an asymmetric base-drift pattern that persists
  even as direction agreement returned). GBP/USD was effectively flat on
  both vendors (+0.01% Investing.com, -0.01% Yahoo) — technically opposite
  signs but at rounding-noise magnitude with near-identical current prices,
  no longer a real conflict like Tuesday's. USD/JPY's direction agreement
  (modest further yen firming, -0.07% Investing.com, -0.03% Yahoo) HELD for
  a second straight edition, confirming it was not a one-off as edition 71
  had cautioned. DXY spot stayed flat and clean on both vendors as usual;
  the DXY futures-contract variant remains unreachable (404) on both
  vendors, a standing, multi-edition gap. Continue checking all four
  pairs/indices every edition regardless of which way any individual one
  goes, and keep retrying the DXY futures variant periodically even though
  it has never once resolved.
- **The CBOE delayed-quotes feed's total block at edition 71 (a full 403 on
  every path, distinct from the usual thin-series-staleness bug) was
  TRANSIENT, not a new standing failure mode — confirmed at edition 72.**
  Using the standard browser User-Agent plus Origin/Referer headers, the
  feed returned a clean HTTP 200 sweep across all six series (VIX, VIX9D,
  VIX3M, VIX6M, VVIX, SKEW) with genuine same-day `last_trade_time` values
  on every one — not merely VIX/VIX3M refreshing while the thinner series
  serve a stale snapshot, the usual partial-failure pattern. Cross-checked
  against Yahoo Finance (exact match on the close) and FRED's official
  VIXCLS series for Tuesday's prior close (26.36, matching). **Do not treat
  this one clean sweep as proof the feed is now reliably back** — continue
  checking `last_trade_time` on each series individually every edition, per
  the long-standing default discipline, since the thin-series-stale pattern
  has recurred unpredictably many times before (clean 55-58, recurred 59,
  clean 60-63, recurred 64, clean 65-68, recurred 69, clean 70, total block
  71, clean 72).
- **The Yahoo Finance duplicate-volume data-quality issue (first logged
  edition 65, recurred edition 67) was not specifically retested at edition
  72** — out of scope again this edition, bypassed in practice by always
  computing % change from price levels by hand regardless. Worth a direct
  retest at a future edition to see if it's still present.
- **westmetall.com (LME copper) at edition 72**: cash $11,703.00/t (-2.76%
  from Tuesday's $12,035.00/t); 3-month $11,758.00/t (approx. -2.46% against
  this report's own last-published Tuesday baseline, since the fetched table
  did not return a fresh Tuesday row this time). A sharp decline with **no
  driver identified despite a dedicated search** — worth checking again at
  edition 73 if the move doesn't reverse. lme.com itself remains
  unreachable (HTTP 403, not re-tested this specific edition but presumed
  unchanged); copper remains single-vendor-sourced.
- **Treasury par yields deepened Tuesday's bull-flattening at edition 72.**
  home.treasury.gov's official daily par-yield-curve TextView page posted a
  fresh Wednesday 25 Nov print: 2-yr **4.61%** (-2bp), 10-yr **4.85%** (-6bp),
  30-yr **5.24%** (-6bp) vs. Tuesday's prior print — the move was
  concentrated in the belly and long end rather than the front end,
  narrowing the 10s2s spread to 24bp from 28bp. Confirmed genuine (not a
  stale-duplicate scrape) by the differential movement across maturities.
  Continue scoping the TextView URL to the specific month
  (`field_tdr_date_value_month=202611`-style parameter) rather than the
  full year.
- **A markup-correctness self-check (`grep -n '</td><sup'`) caught three
  instances of an invalid-table-structure trap at edition 54 (documented
  under Production notes below), before rendering.** Editions 55 through 72
  all ran the same proactive check and found **ZERO instances for an
  EIGHTEENTH consecutive edition** — worth continuing on every edition with
  a table that has an empty trailing cell or a cell containing only a
  citation.
- **The CFTC Asset-Manager-vs-Leveraged-Funds grouped-bar chart was NOT
  needed at edition 72** — confirmed via cftc.gov's own release-schedule
  page that the report covering 24 November futures data remains due
  **Monday 30 November 2026** (the Thanksgiving-week holiday-adjusted date);
  no report posted early, exactly as expected. The chart was last used at
  edition 65 (figsize (9.8, 2.15), `h=0.32` bar offset, figure-level
  legend). The next chart opportunity is whichever edition's window reaches
  Monday 30 November.
- **The "named secondary outlet's own claim can be flatly wrong" trap family
  gained its latest instance — a POSITIVE one — at edition 72: see the
  dedicated Analog Devices closed-thread entry above.** This is the mirror
  image of the family's negative instances (a fabricated or wrong claim
  caught and rejected); here a genuine data gap from a prior edition (ADI's
  unconfirmed driver) got filled by continued search effort one edition
  later, joining the NVIDIA board-investigation case (edition 60→61) and the
  Marvell-Lumentum case (edition 53→55) as the family's prior positive
  examples. The family's full negative-instance list remains logged across
  editions 49-71 (not repeated here to avoid drift — see the prior spec's
  version if the full list is needed; the pattern itself, not the
  enumeration, is what matters going forward: treat any surprising
  secondary claim AND any surprisingly clean negative result as needing a
  genuine verification attempt before accepting or rejecting it).
- **A megacap multi-name earnings cluster producing genuinely uncorrelated
  reactions is a standing, repeated pattern, with the latest instance at
  edition 72 running the OPPOSITE way — mostly correlated, not
  uncorrelated.** HP (+11.49%, delayed-reaction beat), Dell (+0.60%, clean
  reaction despite a rocky premarket), Workday (+0.68%, clean beat) and
  Deere (+4.44%, beat) were all four positive reactions to four beats — a
  useful reminder the uncorrelated pattern (last added at edition 71's ADI/
  MDT/BBY cluster) is common but not universal either way; always check the
  actual outcome rather than assuming either a correlated or uncorrelated
  pattern by default.
- **New production lesson from edition 53: CSS multi-column (`.cols3`/
  `.cols2`) pagination under Chromium print-to-PDF can plateau stubbornly on
  marginal content trims; edition 60 hit the most severe version of this
  plateau and found a clearer fix (documented under Production Notes
  below).** Editions 61-64, 67 and 69 all needed none of this; editions 65
  and 70 both hit the exact edition-60 symptom again (fixed by trimming
  Annex C's own citations); editions 66, 68 and 71 were genuine spillover
  cases that converged cleanly as soon as the break was deleted, with NO
  Annex-C column-balance symptom. **Edition 72 needed none of this at all
  — sections 1-6 ended comfortably on page 3 with the forced break kept,
  converging on the FIRST render**, the common, no-overflow case.
- **The VIX feed's thin-series-stale bug status, updated through edition
  72: clean 55-58, recurred 59, clean 60-63, recurred 64, clean 65-68,
  recurred 69, clean 70, TOTAL BLOCK (not the thin-series bug) 71, clean
  72.** Continue the manual-calculation discipline unconditionally
  regardless of how many bug-free editions precede the current one; always
  hand-compute from the feed's own raw levels rather than trusting its
  percent field, and always check `last_trade_time` on each individual
  series.
- **A markup-correctness trap, logged at edition 47: a `<sup class="ref">`
  citation tag placed immediately after a table row's last `</td>` but still
  inside the `<tr>` (i.e. not nested inside any `<td>`) is invalid table
  structure.** `check_refs.py` will NOT catch this. **Always nest every
  `<sup class="ref">` tag inside a `<td>...</td>` pair, never as a sibling of
  one inside a `<tr>`** — grep for `</td><sup` as a quick self-check if a
  table was built with a lot of copy-paste.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear — BUT edition 72
  broke the dry spell for one specific name.** Editions 58 through 71 all
  found zero verifiable analyst actions on NVDA/AMD/AVGO/MU/ADI (a
  fourteen-edition dry spell on those names collectively). **Edition 72
  found genuine, dated analyst actions on ADI specifically** (TD Cowen cut
  PT to $375 from $475 maintaining Buy; Truist cut to $323 maintaining
  Hold; Bernstein adjusted to $410), issued in direct response to its 24 Nov
  earnings — but NVDA, AMD, AVGO and MU themselves still had zero
  verifiable actions found at edition 72 (now a fifteenth straight edition
  for those four names specifically). Treat the ADI dry-spell break as
  resolved for that name, not as evidence the broader four-name dry spell
  has lifted.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance — and a research pass's clean negative result needs the
  same scrutiny.** This discipline has now caught numerous fabrications and
  errors across editions 49-71 (full list in the prior spec's version, not
  repeated here). **Edition 72 continued the discipline on both an
  earnings cluster and an AI-capex cluster simultaneously**: HP, Dell,
  Workday and Deere were each verified against their own primary 8-K; NVDA,
  MU, AMD, INTC, SMCI, AMAT, BE, GLW, AVGO and ANT were each individually
  fetched from stockanalysis.com's own price-history pages rather than a
  bundled list. One unverified secondary claim (a purported S&amp;P Global
  CreditWatch Negative action on NVDA's credit rating) was checked,
  found uncorroborated anywhere beyond a single search-synthesis result from
  a paywalled/403'd source, and correctly EXCLUDED from the published
  edition rather than repeated — likely a conflation with Moody's genuine
  18 Nov action (Aa1 affirmed, outlook to stable, citing Huang's departure
  as credit-negative, itself a pre-window event not re-derived here).
- **The edition-49 "forward-looking calendar aggregator" trap (names falsely
  listed as past or future reporters when the actual date differs) remains
  closed as a general pattern.** Edition 72 hit one instance of the
  closely-related "stale-date republish" trap directly: a search for
  Autodesk/Urban Outfitters/Dollar Tree earnings for 25 Nov 2026 surfaced
  only an article dated 26 November **2025** (one year stale); it was
  correctly excluded rather than reported as this year's figures. Continue
  checking any carried-forward or search-surfaced calendar claim against its
  primary source before it becomes load-bearing.
- **The 2-year Treasury yield conflict from edition 36 remains resolved, and
  the every-edition reconciliation continued cleanly through edition 72** —
  see the dedicated Treasury-yields entry above for this edition's figures.
- **Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 72 have all run clean (or
  clean after quick fixes). **Edition 72 ran clean on the first check
  (28/28)** — a moderate source count reflecting a dense but not
  record-setting day (an AI-capex deceleration story, an ADI resolution, a
  four-name earnings cluster, and three fresh macro releases).
- **Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.**
  Editions 29 through 72 have all rendered with zero stray tildes on the
  first draft, bar editions 56 and 57 which each needed one fix. **Edition
  72 was clean on the first draft.** **Reminder: `grep -c` exits with status
  1 (not 0) when the count is zero, since no lines matched — don't chain it
  with `&&` into a longer command and assume a silent failure means the
  check itself failed; read the printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Not relevant at edition 72 (no third
  chart used). The next CFTC report to actually need this technique (should
  a denominator gap arise) remains whichever one lands after Monday 30
  November's report.
- **The diffuse-overflow lesson from editions 44-45 and the duplicated-
  content lesson from edition 47 are both still worth checking first on any
  overflow** — but edition 53 showed overflow can also be genuinely dense
  content requiring real trimming, edition 60 showed a third distinct cause
  (an Annex-C column-balance effect, recurred at 65 and 70), and several
  editions (66, 68, 71) showed a genuine page-4 spillover converging as soon
  as the break was deleted with no further symptom. **Edition 72 showed the
  common, no-overflow case**: sections 1-6 ended comfortably on page 3 with
  the forced break kept, converging on the FIRST render. Always check which
  situation you're in before assuming a particular fix is the answer.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest — specifically, when the RATIO
  between the largest and second-largest mover crosses approx. 5x, not when
  the largest mover's raw magnitude looks large in isolation. No capping
  has been needed in any edition since 45. **Edition 72's movers chart (10
  categories, HP +11.49% largest, ADI +6.44% second largest) had a ratio of
  approx. 1.78x**, comfortably under the 5x threshold. Used `pad_frac=0.27`
  with figsize (9.8, 1.95) for the movers chart and `pad_frac=0.30` with the
  same figsize for the 11-category sector panel, both rendering cleanly on
  the first attempt.

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
  first draft and needed roughly a dozen trim/merge rounds to converge. Most
  editions since have converged in one or two renders; see Production Notes
  for the full per-edition render-count history.
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
  table) purely so `check_refs.py` doesn't flag the Annex C entry as unused.
  **Also watch for a stray bracket typed outside a `<sup>` tag entirely** —
  `check_refs.py` will not flag it since its regex only matches inside `sup
  class="ref"` tags, so a bare `[n]` slips through silently. Proofread
  citation-heavy sentences visually, not just via the script, when a
  sentence carries two or more consecutive citations. A related trap, worth
  naming explicitly: placeholder ref text (e.g. `[note1]`) typed during
  drafting and never swapped for a real number. `check_refs.py`'s regex
  requires `\d+` inside the brackets, so a non-numeric placeholder simply
  won't match either the inline or Annex-B regex — it won't show up as
  "missing" or "unused," it just silently doesn't count. **Never use a
  letter suffix to disambiguate a citation — always mint a new integer.**
  Annex C numbers do not need to be contiguous, only matched 1:1 against
  inline citations — deleting an unused reserved number and leaving a gap is
  completely fine and simpler than renumbering everything after it.
  **Reusing the same Annex C number for multiple movers/figures citing the
  same outlet/method is fine and recommended** — `check_refs.py` only checks
  presence/absence, not uniqueness of use. **Citing the prior edition itself
  as a source** (e.g. "logged prior-session baseline figures," or re-citing a
  prior edition's own already-primary-confirmed fact) is a legitimate,
  already-used pattern — edition 72 used this for its central-bank table
  intro sentence, citing a dedicated "previously confirmed, carried forward"
  Annex C entry.
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
- **The disclosure box is a correction box.** Assumptions and status live in
  **Annex A**. What stays on page 1 is **corrections only**: a figure
  published in an earlier edition that turned out to be wrong, or a
  premise-level correction. Terse — what was published, what it should have
  been — with the full record in Annex A if it needs more than a line.
  **Omit the box entirely on an edition that corrects nothing**, which will
  be most of them. Editions 54 through 63, 65 through 67, and 69 through 72
  all omitted the box — in each case nothing published in a prior edition
  was found to be wrong. Editions 64 and 68 each used it once (edition 64:
  edition 63's own date-line weekday error; edition 68: edition 67's own
  AMD/Broadcom ticker swap) — both premise-level corrections about the
  document itself rather than a market figure, but still exactly the kind
  of thing the box exists for.
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
  a matching Annex B entry. Editions 54 through 72 have all run the same
  full 10-row table (Fed, BoJ, BoE, ECB, BoC, RBA, SNB, Norges Bank,
  Riksbank, Banxico). Banxico's rate and vote are primary-source confirmed;
  its next-decision date remains the table's one unavailable cell, now for a
  fourteenth straight edition. Follow the usual table convention — plain
  `<tr>` header rows, no `<thead>`.
- **Charts: two fixed, a third only when earned — changed at edition 49.**
  The **sector-ETF performance chart always goes in Section 1**, beside the
  sector narration it illustrates, and the **single-stock movers bar always
  goes in Section 2**, with the names. Neither may duplicate a table.
  A **third chart is allowed only when positioning or volatility is
  genuinely the day's dominant story** — not merely present, and never to
  fill a short page — and it goes in the section it belongs to: CFTC
  asset-manager vs. leveraged-funds positioning or a VIX term structure in
  Section 5, an implied-vs-realized earnings bar in Section 2. **Editions 66
  through 72 did not use a third chart** — no fresh CFTC report fell inside
  any of those windows (next due Monday 30 Nov 2026), and in each edition
  with a genuinely dominant single story (the Huang reinstatement at 70, the
  AI-capex giveback at 71, the whipsaw-then-GDP day at 72) that story was
  better served in prose/the two fixed charts than by a third chart.
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
  editions 56 through 72.
- Where sources disagree, use the more authoritative one **and** disclose
  the disagreement. AP's "How major US stock indexes fared" and the Reuters
  market wrap are normally the most reliable for index closes — but check
  they're actually indexed for the target date before relying on them. The
  WTOP.com/lanacion.com.ar AP-wire-mirror approach remains the established
  first-choice workaround when apnews.com/Reuters are blocked directly.
  **Edition 72 used the lanacion.com.ar mirror again, cross-checked against a
  second independent recap outlet plus SPY/DIA/QQQ/IWM ETF closes** — all
  fully consistent, and the reported Wednesday closes reconciled exactly
  against the prior edition's own published Tuesday figures (a useful
  built-in sanity check: Tuesday's close plus Wednesday's point change
  equals Wednesday's close, to the cent, across all four indices).
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Always check a dated article's own claimed magnitude AND
  direction against the underlying price-history table or primary filing,
  not just its date, before repeating it** — this trap has now hit
  magnitude, direction/framing, claimed drivers that don't hold up, a
  claimed analyst action that appears outright fabricated, the claimed
  DATE/YEAR itself, the claimed DAY-OF-WEEK NAME attached to a correct date,
  a disclosed cross-source percentage-methodology discrepancy, a figure with
  no corroborating primary filing at all, a wholesale stale-date republish,
  and a dramatic claim that one research pass reported as apparently true
  before a direct follow-up found no support — as well as the mirror-image
  lesson that a dramatic claim, re-checked with fuller search effort, turned
  out to be true after all. **Edition 72 hit two more instances**: a
  one-year-stale (26 Nov 2025) article surfaced when searching for Autodesk/
  Urban Outfitters/Dollar Tree earnings was correctly excluded rather than
  reported as current, and an unverified S&amp;P Global CreditWatch claim on
  NVDA (likely a conflation with a genuine Moody's action) was checked,
  found uncorroborated, and excluded. Treat ANY surprising secondary claim
  (price move, driver, analyst action, date, or computed percentage) — AND
  any surprisingly clean negative result for a single-session search — as
  needing a genuine, thorough verification attempt before either accepting
  or rejecting it.
- Run a dedicated verification pass on any figure two research passes
  disagree on, or any single surprising/highly-consequential finding, before
  publishing — cheap, and has caught real errors before.
- **Premarket is not the close, and the close is not the after-hours
  earnings reaction — and an after-hours reaction does not necessarily hold
  into the next regular session, uniformly or at all. A strong beat-and-raise
  does not guarantee a positive reaction even within the SAME session —
  though it does not guarantee a negative one either.** Reinforced at
  essentially every edition since 44. **Edition 72 again showed both sides**:
  HP's clean beat drew a -3.32% reaction the report day, then +11.49% the
  NEXT session (a one-day-lagged positive digestion); Dell's beat-and-raise
  drew an approx. -7% premarket reaction before an intraday round-trip to
  +0.60%; Workday and Deere both drew clean, same-direction positive
  reactions to clean beats — four different timing patterns from four
  reports in one cluster. Always fetch the verified close, the after-hours
  reaction, AND (when the window allows) the next regular session's close as
  three separate, clearly labelled figures.
- **FX cross-vendor status (DXY, EUR/USD, GBP/USD, USD/JPY) and the
  Investing.com Monday-reopen displayed-% mechanism are both tracked in ONE
  place each under Standing Facts above.** Check both dedicated entries
  every edition regardless of which way any pair goes.
- **The Kitco live-spot-vs-headline cross-check status is tracked under
  Standing Facts above.**
- **The 2-year Treasury yield conflict from edition 36 remains resolved, and
  the every-edition reconciliation continued cleanly through edition 72** —
  see the dedicated Treasury-yields entry under Standing Facts.
- **The distinct Yahoo Finance stale-%-field issue (logged edition 63) and
  duplicate/conflicting-row issue (logged edition 65, recurred 67) were not
  specifically retested at edition 72** — out of scope again this edition,
  bypassed in practice by always computing % change by hand regardless;
  worth a direct retest at a future edition.
- Cross-check every inline `[n]` reference against Annex C (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Edition 72 ran clean on the first check (28/28).
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Reminder: `grep -c` exits with status 1 (not 0) when the count is zero,
  since no lines matched — don't chain it with `&&` into a longer command
  and assume a silent failure means the check itself failed; read the
  printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Not relevant at edition 72 (no third
  chart). The next CFTC report to actually need this technique (should a
  denominator gap arise) is whichever one lands after Monday 30 November
  2026.
- **The diffuse-overflow lesson from editions 44-45 and the duplicated-
  content lesson from edition 47 are both still worth checking first on any
  overflow** — but several editions since have shown different causes
  (genuine dense-content trimming at 53, an Annex-C column-balance effect at
  60/65/70, clean page-4 spillovers converging on break-deletion alone at
  66/68/71). **Edition 72 showed the common, no-overflow case**: sections
  1-6 ended comfortably on page 3 with the forced break kept, converging on
  the first render. Always check which situation you're in before assuming
  a particular fix is the answer.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when the RATIO between the
  largest and second-largest mover crosses approx. 5x, not when the largest
  mover's raw magnitude looks large in isolation. No capping has been needed
  in any edition since 45; edition 72's ratio (approx. 1.78x) was again
  comfortably under threshold.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`, under the `quotes/` path
  specifically — `charts/_VIX.json` returns 403, `quotes/_VIX.json` works).
  The feed still requires a browser User-Agent plus an `Origin`/`Referer:
  https://www.cboe.com/` header to clear a Cloudflare 403 when it IS
  reachable — carry this forward as the default request shape. **Edition 71
  broke a long clean streak with a total, not partial, unreachability (403
  on every path); edition 72 found the feed fully clean again** — a genuine
  sweep across all six series with fresh same-day timestamps, cross-checked
  against Yahoo Finance and FRED's VIXCLS. Treat the edition-71 block as
  transient (egress-level, not a new standing failure mode) but continue
  checking `last_trade_time` on each series every edition regardless —
  the thin-series-stale pattern has recurred unpredictably many times
  before and could again. **Edition 72's own session (CBOE feed, hand-
  computed):** VIX 28.29 +7.32%, VIX9D 29.61 +10.98%, VIX3M 26.29 +3.22%,
  VIX6M 26.89 +2.67%, VVIX 115.38 +1.15%, SKEW 142.06 +2.08%. Term
  structure: front end inverted (VIX9D above spot VIX), back end mildly
  contangoed (VIX3M below VIX6M) — a short, sharp event-driven spike atop an
  otherwise calm medium-term curve.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table/chart. **Edition 72 fetched all 11 directly again** (8 of
  11 closed higher — Materials +2.07% the leader for a second straight
  session with no driver found either time; Technology -0.83%, Health Care
  -0.56% and Consumer Discretionary -0.20% lower) — continue this
  direct-fetch-by-default method. A secondary cross-check (MarketWatch) was
  not re-attempted at edition 72 — now a THIRTEENTH straight edition
  single-sourced; try the cross-check again at edition 73.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (9 of 11 at edition 70; 9 of 11
  at edition 71; **8 of 11 at edition 72**). No constituent-level breadth
  figure (e.g. "X% of S&amp;P 500 stocks advanced") was found in any wire
  checked at edition 72 either — keep checking for it each edition without
  relying on it being there.
- **Dealer gamma:** zerogex.io and SpotGamma both remain fully unusable,
  extending their respective failure streaks again at edition 72
  (placeholder dashes / article teasers only, no timestamped figures).
  **ANT's options market remained actively two-sided as of Tuesday 24 Nov's
  last confirmed read** (approx. 500,000 contracts, approx. $250m premium,
  implied vol approx. 96, puts approx. 300,000 ahead of calls approx.
  200,000) — a Wednesday 25 Nov-specific figure could NOT be verified
  despite multiple targeted searches and a direct Yahoo Finance options-chain
  attempt (HTTP 401, auth/crumb required). Treat any ANT options figure with
  caution unless it carries an explicit date/timestamp; the last confirmed
  read remains Tuesday's. NVDA's own single-day options figures were not
  independently pulled at edition 72 (deliberately, given the known
  single-day-vs-multi-day conflation risk) — no NVDA options figure is
  reported this edition to avoid repeating that error.
- **Official CME FedWatch probabilities:** the page blocks fetching — a
  **THIRTY-THIRD** consecutive failure at edition 72 (41-72), a timeout
  again, no secondary citation found. **Use Kalshi/Polymarket/DeFi Rate
  instead — and use the CORRECT Kalshi query, found at edition 70**:
  `event_ticker=KXFEDDECISION-26DEC` (not the previously-used
  `series_ticker=KXFED-26DEC`). **Edition 72's search-based approach did not
  explicitly re-use this corrected query** and instead relied on Kalshi's
  own summary page (approx. 77% hike) plus a stale 16 Nov Polymarket
  snapshot (approx. 87.5%) — a notably more scattered read than edition 71's
  approx. 93% DeFi Rate blend. **Retry DeFi Rate's own blended read directly
  at edition 73**, and use the corrected Kalshi query explicitly, before
  concluding odds have genuinely shifted from edition 71's reading.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **westmetall.com (LME copper) at edition
  72**: cash $11,703.00/t (-2.76% from Tuesday's $12,035.00/t); 3-month
  $11,758.00/t (approx. -2.46%, computed against this report's own
  last-published Tuesday baseline since the fetched table lacked a fresh
  Tuesday row this time). No driver found for the sharp decline despite a
  dedicated search. lme.com itself presumed still 403 (not re-tested this
  specific edition); copper remains single-vendor-sourced — keep checking
  both sites each edition.
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve TextView page **posted a fresh Wednesday 25 Nov print at
  edition 72, continuing the clean streak** — 2-yr 4.61% (-2bp), 10-yr 4.85%
  (-6bp), 30-yr 5.24% (-6bp) vs. Tuesday's prior print; confirmed genuine
  (not a stale-duplicate scrape) by the differential movement across
  maturities (belly/long end down more than the front end). Continue
  scoping the TextView URL to the specific month
  (`field_tdr_date_value_month=202611`-style parameter) rather than the
  full year.
- **CFTC CoT:** publishes with the prior Tuesday's data — always state the
  lag explicitly. `financial_lf.htm` works well for equity index futures
  (ES/NQ/RTY); note the correct legacy URL is
  `cftc.gov/dea/futures/financial_lf.htm`, NOT `/dea/newcot/financial_lf.htm`
  (which 404s). The report covering 24 November data remains confirmed due
  **Monday 30 November 2026** (a Thanksgiving-week holiday adjustment).
  **Confirmed at edition 72 that no report posted early**, exactly as
  expected; do not expect one inside edition 73's window either unless that
  window reaches Monday 30 Nov.
- **GBP/USD, EUR/USD, USD/JPY, DXY cross-vendor status — see the dedicated
  Standing Facts entry ("FX cross-vendor status improved materially at
  edition 72") rather than this entry, which is not being duplicated
  further.**
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. See the dedicated
  Standing Facts gold/silver entry above for edition 72's figures and the
  Kitco status (clean, internally consistent, for a third straight edition).
- **China CPI/PPI (monthly), China Q3 GDP, US GDP/PCE/import-export
  prices/industrial production, University of Michigan October/November
  consumer sentiment, China's October PMI and October ISM Services PMI, the
  November 2026 Philadelphia Fed Manufacturing Business Outlook Survey:**
  all closed threads — see Standing Facts above. **NEW closed threads as of
  edition 72: Q3 2026 GDP second estimate + corporate profits, October 2026
  durable goods orders, the 25 Nov 2026 Beige Book, and the November 2026
  Richmond Fed Manufacturing Index** — all detailed under Standing Facts
  above. Weekly US initial jobless claims: the most recent confirmed figure
  remains 203k for the week ended 14 Nov 2026 (released 19 Nov); **edition 72
  could not find a Thanksgiving-week release (week ended 21 Nov 2026)
  despite the DOL's usual holiday-week Wednesday schedule shift** — a
  genuine gap, not a fabricated figure; retry at edition 73. MBA weekly
  mortgage applications (week ended 20 Nov 2026) showed conflicting
  secondary figures at edition 72 (HousingWire: -4.5%; National Mortgage
  News: -3.2% SA, though one NMN piece also cited -4.5% SA with purchases
  +9.6% SA) with mba.org itself returning HTTP 403 — unresolved, a
  secondary data-quality item, not critical to this report's core coverage.
- **Henry Hub natural gas:** the front-month contract remains **NGF7
  (January)**, rolled at edition 69 — no further roll as of Wednesday 25
  Nov. **A genuine partial improvement at edition 72**: both Investing.com
  and Yahoo referenced the SAME contract for the first time in recent
  editions (Investing.com's prior mis-keying problem, this report's
  historically worst-performing data-quality issue, did not recur), though a
  small (~1.8&cent;) base gap persists between the two vendors. Continue
  the every-edition two-source reconciliation discipline regardless, since
  this toggles open/closed unpredictably.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. CoreWeave's Q3 2026 results and
  regular-session reaction are fully resolved (edition 62).
- **Weekend equities catalyst: 13F filings.** The Q3 2026 deadline has now
  passed, closed at edition 65 (nothing substantive reported, including a
  dedicated Berkshire Hathaway check). No further action needed on this
  deadline; the next 13F deadline is mid-February 2027 (Q4 2026 data).
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22, not attempted
  again since). Revisit only if a future edition has spare research
  bandwidth on an FOMC day specifically — not relevant to most editions.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully
  several times since, most recently at edition 69 (the Friday 20 Nov
  report, covering Tuesday 17 Nov data: ES OI 2,096,958; NQ futures-only OI
  296,423 [the separate "Nasdaq-100 Consolidated" line read 314,318 — still
  plausibly, not yet conclusively, explained as CFTC's futures-only vs.
  futures-and-options-combined convention]; RTY OI 459,730). Next report due
  Monday 30 Nov 2026 (the Thanksgiving-week holiday adjustment) — verify the
  timing directly when that window arrives, watching for the micro-vs-
  full-size naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Analyst price targets on NVDA/AMD/AVGO/MU:** now a FIFTEENTH straight
  edition with zero verifiable actions found (editions 58-72), despite ADI
  breaking its own dry spell at edition 72 specifically (see Standing
  Facts). This looks like a genuine, standing gap for these four
  megacap-chip names rather than search-index lag — de-prioritize slightly
  but keep checking each edition.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance — and a research pass's clean negative result needs the
  same scrutiny.** See the dedicated Standing Facts entry for edition 72's
  continuation of this discipline.
- **The DOL's weekly initial-jobless-claims release document could not be
  parsed at edition 47** (returned unreadable/binary data via direct fetch)
  — not re-attempted since (out of scope each time); try an alternate DOL
  page or a secondary economic-calendar aggregator for the consensus figure
  when next relevant. **Edition 72's gap was different in kind**: not a
  parsing failure but a genuine absence of any Thanksgiving-week (week
  ended 21 Nov) release found at all, despite the DOL's usual holiday-week
  Wednesday schedule shift — retry at edition 73.
- **federalregister.gov's direct search interface remains blocked** (a prior
  search attempt 302-redirected to `unblock.federalregister.gov`, an
  apparent bot/rate-limit gate, first logged at edition 48). govinfo.gov
  continues to be a known working alternative route for at least some
  Federal Register content. **The Federal Register's own developer API
  (`federalregister.gov/api/v1`) remains the clearly-established first
  approach whenever the search UI is blocked** — used again successfully at
  edition 72 for the tariff-thread check (see Standing Facts).
- **SEC EDGAR's `cgi-bin/browse-edgar` company-search page (filtered by CIK
  and form type 8-K) is a highly reliable, fast way to confirm both WHETHER
  a company has reported on a given date and to find the accession number
  for the underlying exhibit.** Reinforced again at edition 72 for ADI, HP,
  Dell, Workday and Deere's own 8-Ks — the default first tool for
  confirming any earnings or governance filing, and for confirming a clean
  negative just as reliably as a positive.
- **ECB's current policy rate: SETTLED since edition 55** (unchanged through
  the 28-29 October 2026 meeting: deposit facility 2.50%, main refi 2.65%,
  marginal lending 2.90%). It reopens on contradiction, the next Governing
  Council decision, or the monthly audit. The Council's own next-meeting
  date is SETTLED at 16-17 December 2026.
- **NFIB Small Business Optimism Index:** nfib.com returned HTTP 403 at
  direct fetch at edition 62; Trading Economics worked as a fallback,
  carrying the October reading (97.8, down 0.1pt from September). Not
  re-attempted since (no new monthly release inside any recent window);
  continue using Trading Economics as the default fallback when nfib.com
  blocks direct access.
- **Banxico's next policy-decision date — see the dedicated Standing Facts
  entry above (unresolved for a fourteenth straight edition as of edition
  72); not duplicated here further.**

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel —
  confirmed clean again at editions 66 through 72 (thirty-three editions
  total: 37-43, 45-50, 52-72). For charts with fewer categories, scale the
  height down: roughly `(9.8, 1.65-2.05)` for 3-9 categories. **Edition 72
  used `(9.8, 1.95)` for a 10-category movers chart with `pad_frac=0.27`**,
  rendering cleanly across a -4.53% to +11.49% range (ratio approx. 1.78x).
  **Always render and visually inspect (via the Read tool) the actual PNG at
  or near full resolution before embedding it**, regardless of what a past
  edition's success might suggest. **Default to pad_frac=0.30 from the start
  for an 11-category sector-ETF panel** — now confirmed across twenty-five
  straight small-magnitude 11-category panels (45-50, 52-72, edition 72's
  own panel spanning -0.83% to +2.07%). For any movers chart with a
  double-digit-percent outlier, continue trying pad_frac in the 0.22-0.30
  range from the start.
- **Capped-outlier label-overlap fix (from edition 45):** when a capped
  bar's value label uses a "(capped)" text suffix, the label text can be
  long enough to visually bleed into the y-axis tick-label margin even at a
  wide pad_frac, because matplotlib's `ax.text()` is unclipped by default.
  **Fix: shorten the per-bar suffix to a single trailing asterisk (`"*"`
  instead of `" (capped)"`) and add one footnote to the chart's x-axis label
  instead.** This remains the recommended default for any future
  capped-outlier chart. No edition since 45 has actually needed outlier
  capping — every spread has stayed well under the approx. 5x ratio
  threshold, including edition 72's approx. 1.78x.
- **A grouped (two-series) horizontal bar chart — needed for the CFTC
  Asset-Manager-vs-Leveraged-Funds positioning chart — requires custom chart
  code, not the standard single-series `barh()` helper used for the
  movers/sector charts** (first built at edition 44, reused successfully at
  editions 49, 54 and 65). The standard helper only plots one value per
  category; the CFTC chart needs two bars (Asset Manager, Leveraged Funds)
  per category (ES/NQ/RTY), offset vertically by a fixed height fraction
  (`h=0.32`) around each category's tick position. **Fix that worked for the
  legend:** use a FIGURE-level legend (`fig.legend(..., loc="lower center",
  bbox_to_anchor=(0.5, 0.0), ...)`) combined with `fig.tight_layout(rect=(0,
  0.1, 1, 1))` to reserve the bottom 10% of the figure for the legend.
  Figsize `(9.8, 2.15)` rendered cleanly at editions 54 and 65. **Reuse this
  exact pattern** for any future grouped/multi-series chart rather than
  re-deriving the legend-placement fix from scratch.
- PDF: HTML → Chromium print-to-PDF via Playwright. Launch Chromium with an
  explicit `executablePath` (check the environment for the installed
  Chromium build path) and `--no-sandbox`. Do not run `playwright install`.
- Set margins in **exactly one place** — either the CSS `@page` block or the
  Playwright `page.pdf()` margin option, never both (they stack and double
  the margin). Passing `{top:'1in', bottom:'1in', left:'13mm', right:'13mm'}`
  via `page.pdf()` with the HTML body at `margin:0; padding:0` and no CSS
  `@page` block is the pattern that has worked reliably — edition 72 used
  this exact pattern again with no issue, on a single render.
- **At most ONE forced `page-break-before` in the whole document:
  immediately before Annex A — and on a spillover edition, none at all.**
  Let sections 1-6 flow naturally; never add a break between them. The rule:
    - Sections 1-6 end on page 3 (the common case) → keep the break. The
      annex opens a clean page 4, exactly as before. **Edition 72 was this
      case**, converging on the first render.
    - Sections 1-6 spill onto page 4 → **delete the `pagebreak` div and
      re-render**, so the annex follows the spillover down page 4 instead of
      starting a fifth page. Editions 65, 66, 68 and 70 were all this case
      (65 and 70 needed a further Annex-C-trimming fix; 66 and 68 converged
      cleanly as soon as the break was deleted).
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
  **Edition 72 confirmed 1** — the common case, sections 1-6 ending
  comfortably on page 3 with meaningful room to spare.
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
  default (`balance`) remains the right choice. This symptom has recurred at
  editions 65 and 70 (both fixed by trimming Annex C's own citations) but
  did NOT recur at 66, 68 or 72 — a reminder it's a possibility to check for
  on a spillover, not a certainty, and not relevant at all on a clean
  (non-spillover) edition like 72.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix.
- **A markup-correctness trap, logged at edition 47: a `<sup class="ref">`
  citation tag placed immediately after a table row's last `</td>` but still
  inside the `<tr>` (i.e. not nested inside any `<td>`) is invalid table
  structure.** `check_refs.py` will NOT catch this. **Always nest every
  `<sup class="ref">` tag inside a `<td>...</td>` pair, never as a sibling of
  one inside a `<tr>`** — grep for `</td><sup` as a quick self-check if a
  table was built with a lot of copy-paste. Editions 55 through 72 all ran
  the same proactive grep and found zero instances, an EIGHTEENTH
  consecutive clean sweep.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count
  alone. **Edition 72 converged in ONE render** — sections 1-6 ended
  comfortably on page 3 with the forced break kept (the common case); final
  source count 28 (28/28 clean on the first check, zero stray tildes, zero
  `</td><sup` instances). Recent render-count history: edition 69 one
  render; 70 three renders (spillover, then the Annex-C symptom); 71 two
  renders (spillover, converged cleanly); **72 one render**.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across many editions'
genuinely different content volumes. Treat as the durable default; the lever
to pull on a high-volume or overflowing day is first checking for duplicated
content across sections, then merging/trimming redundant content across
whichever sections (or Annex C citations) are longest — not loosening the
CSS further.)
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
  runs short — editions 44 onward have folded commodities, FX and
  Treasuries into ONE combined table (10-17 rows) as the PRIMARY commodities
  table rather than padding, now the standing default. **Edition 72 used 14
  rows.**
  **Always re-render immediately after adding (or removing) any content to
  confirm the page count — and if a change to Annex A/B text doesn't move
  the page split at all, suspect the Annex C column-balance effect above
  before assuming the edit silently failed to save.**

**Chart selection guidance.** Placement is not editorial for the first two
charts:

- **Sector-ETF performance chart → Section 1 (Market recap), every
  edition.** Same-day closes by default; a grouped day-over-day bar instead
  on a multi-session or weekend window, or on a genuine multi-sector
  broadening selloff across consecutive sessions. **Edition 72 used a
  single-day bar** (the window held only one NYSE session).
- **Single-stock movers bar → Section 2 (Equities), every edition.**
  **Edition 72 used 10 categories** (HP, ADI, Deere, SMCI, GLW, AMD, BE,
  AMAT, NVDA, MU) — INTC and AVGO were deliberately excluded as too close to
  flat (-0.60% and -0.07%) to read as genuine "movers," and were instead
  covered in prose only.
- **A third chart only when positioning or volatility is genuinely the
  day's dominant story**, never to fill a page, placed in the section it
  belongs to:
  - Fresh CFTC CoT data → the ES/NQ/RTY asset-manager-vs-leveraged-funds
    positioning chart, normalized as % of open interest, built with the
    grouped-bar technique documented under Production notes, in **Section
    5**. Editions 24, 34, 39, 44, 49, 54 and 65 have all placed it there.
    Not used at editions 66 through 72 — the next opportunity is whichever
    edition's window reaches Monday 30 November 2026's holiday-adjusted
    report.
  - A single dominant earnings print with a clean, well-sourced
    implied-vs-realized-move story → a three-bar implied/historical-average/
    realized move chart in **Section 2**. Note the historical-average leg
    has never actually been sourced successfully. Not used at editions 55
    through 72 — edition 72's four-name earnings cluster (HP, Dell, Workday,
    Deere) didn't produce one single dominant print of that kind.
  - A holiday/preview edition with no fresher data → VIX futures term
    structure with event annotations, in **Section 5**. Not used at editions
    55 through 72 — the VIX complex has spiked sharply several times (63,
    65, 66, 68, 72) but was judged secondary to a larger dominant story
    each time and handled fully in prose instead (at edition 72: the
    GDP-revision/AI-whipsaw/ADI-resolution multi-story day).

**Edition 73 (expected to cover Friday 27 November 2026's half-day session,
OR — if the workflow decides a half-day session with no fresh scheduled data
doesn't warrant its own run — a Monday 30 November 2026 edition covering the
holiday-shortened multi-session stretch (Thu 26 Nov closure + Fri 27 Nov
half-day) in one window. Frame the window honestly against whichever the
actual prompt gives; do not assume either case from this note alone.)**
Edition 72 saw a sharp but mostly-reversed AI-capex morning selloff, a GDP
second-estimate revised up sharply to +4.3%, Analog Devices' open "no
driver" thread resolved, and a mostly-positive four-name pre-Thanksgiving
earnings cluster. Verify directly rather than assuming:
- **Whether the AI-capex-complex giveback (NVDA -3.91%, MU -4.53%, AMAT
  -3.89%, BE -2.25%, AMD -1.75%, GLW -1.60%, INTC -0.60%, AVGO -0.07%, SMCI
  +3.05%) continues decelerating into stabilization, or reaccelerates** when
  trading resumes — fetch each name individually, not a bundled list.
- **A driver for Materials (XLB)'s sector-leading performance** — now
  unexplained for two straight sessions (Tue 24 Nov +0.54%, Wed 25 Nov
  +2.07%); check commodity-linked constituents, M&amp;A activity, or a
  sector-specific analyst action rather than repeating the same general
  news search.
- **Retry DeFi Rate's own blended December-FOMC-odds read directly**
  (edition 72's macro pass skipped it entirely and relied on Kalshi's
  summary page plus a stale Polymarket snapshot, reading a more scattered
  approx. 77-87.5% versus edition 71's approx. 93%) — use the corrected
  Kalshi query (`event_ticker=KXFEDDECISION-26DEC`) explicitly before
  concluding anything genuinely shifted.
- **A driver for copper's sharp LME decline** (cash -2.76%, 3-month
  -2.46%) — no source checked at edition 72 found one.
- **The specific mechanism behind HP's one-session-delayed +11.49% rally**
  and **Dell's intraday round-trip from an approx. -7% premarket reaction to
  a +0.60% close** — both still unexplained.
- **Confirmation of general counsel Tim Teter's 2 December congressional
  testimony status post-Huang-reinstatement** — only Huang's 1 Dec session
  was explicitly reaffirmed (per CNBC) at edition 72.
- **Independent corroboration (or refutation) of the single-sourced WSJ
  claim that the SEC opened a civil probe into Nvidia's own disclosures** —
  still uncorroborated through edition 72.
- **A US primary-source document extending the reciprocal-tariff IEEPA
  suspension (EO 14358) past its 10 Nov 2026 expiry** — try a different
  search angle (Commerce/BIS press releases, a congressional-record
  mention, or a trade-press report citing a specific document number)
  rather than repeating the same federalregister.gov/whitehouse.gov sweep a
  sixth time.
- **Whether ANT's options market has fresher, dated data** — Wednesday's
  figure could not be verified at edition 72; the last confirmed read
  remains Tuesday's.
- **Weekly initial jobless claims for the Thanksgiving week** (week ended 21
  Nov 2026) — no release found at edition 72 despite the usual holiday-week
  shift; retry.
- **Whether the CBOE feed's full reachability at edition 72 holds, or
  whether edition 71's total block recurs** — check `last_trade_time` on
  each series individually regardless of which way it goes.
- **Banxico's next policy-decision date** — unresolved for fourteen straight
  editions; de-prioritized, but worth a quick check.
- **US Treasury par yields** — continue the normal every-edition
  reconciliation; Wednesday's deepened bull-flattening (belly/long end down
  6bp, front end down 2bp) is worth watching for continuation.
- **Government funding status (H.R. 6500)** — watch for any Senate floor
  action on the twelve FY2027 bills (all committee-reported in both
  chambers as of edition 72, none passed on either floor).
- **MBA mortgage applications** — conflicting secondary figures at edition
  72 (-4.5% vs. -3.2%), primary mba.org release inaccessible; low priority
  but worth a retry if easily reconciled.
- **The week-ahead calendar**: whatever lands inside edition 73's actual
  window (the half-day Friday session itself is historically very light on
  scheduled US data; no confirmed release was found for it at edition 72's
  own day-ahead check). The CFTC's next Commitment of Traders report
  (covering 24 Nov futures data) is confirmed due Monday 30 November 2026 —
  get it if the window reaches that far.
Dates to hold on to (edition-to-session mapping: 70 published Tue 24 Nov,
covering Mon 23 Nov; 71 published Wed 25 Nov, covering Tue 24 Nov; 72
published Thu 26 Nov (Thanksgiving, a market holiday), covering Wed 25 Nov;
73 expected to cover Fri 27 Nov's half-day session, or — if that session is
folded into a later multi-session catch-up — a Mon 30 Nov edition covering
Thu 26 Nov's closure plus Fri 27 Nov's half-day). RBA next decision 7-8 Dec
2026; the Fed and BoC both meet 8-9/9 Dec 2026; SNB 10 Dec 2026; Riksbank
approx. 16 Dec 2026; BoE 17 Dec 2026; the ECB and BoJ both meet 16-18 Dec
2026. The next monthly settled-facts audit falls on the first edition of
December 2026. Thanksgiving (26 Nov, full closure) and its Friday half-day
(27 Nov) are now resolved/closed history as of edition 72's own cutoff (the
closure/half-day lie immediately ahead of, not inside, edition 72's covered
session) — no further calendar check needed unless a contradiction
surfaces. The CFTC's next Commitment of Traders report (covering 24 Nov
data) remains confirmed due Monday 30 November 2026 — confirmed at edition
72 that no report posted early; do not expect one inside edition 73's
window either unless it reaches that Monday.

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

**Edition 71's carried-forward spec was 162,947 bytes, over the
100,000-byte threshold — this run (producing edition 72's spec) condenses
the log again.** This run folds edition 70 into the mega-block (now
genuinely "Editions 1-70"); edition 71's own full-detail entry is condensed
down to a medium paragraph; edition 72 is added in full detail. There is no
maximum size; condensing is housekeeping done by the run itself, not a
check to pass — there is no penalty for the file staying somewhat large if
the alternative is losing information.

**Editions 1–70 (condensed):** established the format (edition 1 baseline;
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
Citigroup/UnitedHealth/J&amp;J all reported; JNJ's GAAP EPS collapsed to $0.09
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
equities extended a rally a second session; Netflix/AT&amp;T(-6.45%, disputed)/
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
Range Resources +17.66% on confirmed M&amp;A; BoJ's numeric rate, Riksbank's
rate and RBA's current rate all closed at once; the largest-yet Brent
vendor-revision trap hit ($116.72 vs. $111.70); the first genuine 5-page
overflow fixed via the new spillover mechanism. Edition 51 (Wed 28 Oct,
covering Tue 27 Oct, reconstructed by hand after the then-current
120,000-byte spec ceiling rejected and discarded the run's own update — the
ceiling has since been removed): a third straight up session on narrow
breadth (S&amp;P +0.60% to 7,722.60, Nasdaq to a fresh high of 26,477.81, only 5
of 11 sectors green), AP's recovered wire saying "most S&amp;P 500 stocks fell"
even as the index rose on a handful of megacaps; a dense pre-FOMC earnings
morning broke the beat/reaction logic repeatedly (Boeing -10.69% on a miss,
JetBlue +18.99% despite missing); Brent's Friday 23 Oct close became a
three-way split ($116.72/$111.70/$113.17), still unresolved. Edition 52
(Thu 29 Oct, covering Wed 28 Oct FOMC day): the Fed held at 3.75%-4.00% on a
10-2 hawkish dissent (Cook, Hammack); the Bank of Canada delivered the
bigger surprise with a genuine 25bp hike to 2.50%. Equities notched a
fourth straight up session on narrow leadership (S&amp;P +0.28%); Microsoft
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
unsubstantiated at the time — became real M&amp;A four sessions later at
edition 55), Carvana +15.68%. A claimed Barclays PayPal downgrade was
investigated and found fabricated, dropped entirely. First draft ran a
genuine 6 pages; converged to 4 after a dozen rounds of trimming/
citation-merging, surfacing a new CSS multi-column pagination lesson.
Edition 54 (Mon 2 Nov, weekend-gap): a tech-led selloff (S&amp;P -1.82%) on
Intel's historic -28.58% collapse (worst day since 1974); BoJ held at
approx. 1.25%; China's October PMI slipped below 50; the November monthly
settled-facts audit completed cleanly across all ten central-bank rows.
Edition 55 (Tue 3 Nov): equities diverged on composition (Dow +0.41%,
S&amp;P -0.51%, Nasdaq -1.07%) as crude collapsed 7-11% on an Iran/US thaw
signal; Apple fell on a soft margin outlook; Marvell agreed to acquire
Lumentum (Marvell -12.72%, Lumentum -18.59%); BoJ's/SNB's next-meeting
dates resolved, ECB's rate complex promoted to SETTLED. Edition 56 (Wed 4
Nov): a megacap/AI bounce (S&amp;P +0.36%, Nasdaq +0.83%, Dow -0.38%); RBA's
fifth 2026 hike (25bp to 4.85%, first-ever split vote); AMD's Q3 beat drew
a genuinely positive AH reaction. Edition 57 (Thu 5 Nov): the 3 November
US midterm elections (Democrats won both chambers) drove Dow +3.03% to
53,356.12 (then the largest one-day move logged), WTI -8.3%; Riksbank's
surprise 25bp hike to 2.00%. Edition 58 (Fri 6 Nov): a full reversal on an
AI-capex/data-center-moratorium scare — S&amp;P -4.4%, zero of 11 sectors
higher, VIX's sharpest one-day increase on record (+69.66%); BoE hiked 25bp
to 4.00% same session Banxico reportedly cut to 6.25% (later primary-
confirmed); December hike odds swung from approx. 77-80% to approx. 66.5%
within two editions, the first of several sharp rate-odds reversals this
stretch. Edition 59 (Mon 9 Nov): a much-stronger-than-expected October jobs
report (+165,000 vs. approx. +65,000 consensus) snapped December hike odds
from approx. 66.5% back to approx. 76.5-77%; a fresh vendor-revision trap
hit WTI/gold/silver/COMEX copper, Kitco's historical-close pages became
inaccessible for the first time. Edition 60 (Tue 10 Nov): an 11-of-11-sector
relief rally (S&amp;P +2.3%, best day since 8 April) on an Iran de-escalation
oil crash; Nvidia alone fell (-4.27%, the Megaspeed/Huang overhang) on a
dramatic board-investigation claim excluded as uncorroborated — overturned
as TRUE the very next edition; first Annex-C column-balance overflow
symptom, fixed by trimming Annex C directly. Edition 61 (Wed 11 Nov):
October's hot CPI (no y/y figures published, a 2025-appropriations-lapse
gap) firmed hike odds to approx. 85-86%; Nvidia's board-investigation
story was independently re-verified and found TRUE (NVDA -5.47%). Edition
62 (Thu 12 Nov, Veterans Day — equities open, Treasury/Fed closed): a
broad CoreWeave-led relief rally (S&amp;P +1.3%, 10 of 11 sectors higher);
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
2026," but 13 November 2026 is a Friday. Edition 64 (Mon 16 Nov, covering
Fri 13 Nov, weekend-gap): a sharp reversal of the week's rotation into
Nvidia's chip-sector rivals on profit-taking (AMD -8.75%, Broadcom -4.76%,
no company-specific news — the first "verify a clean negative" instance);
equities eased modestly (S&amp;P -0.41%); October PPI mixed; three different
reactions to three beats; first correction box since edition 53 (fixing
edition 63's date-line weekday error). Edition 65 (Tue 17 Nov, covering Mon
16 Nov): the post-Huang-resignation chip slide extended a third session
ahead of NVIDIA's own earnings (NVDA -4.12%, AMD -5.58%, AVGO -3.92%, plus
a wider sympathy decline); equities posted their worst session since 6 Nov
(S&amp;P -1.9%); VIX spiked +18.70% powering a fresh CFTC positioning chart;
Thanksgiving/Friday-half-day promoted to SETTLED. Edition 66 (Wed 18 Nov,
covering Tue 17 Nov): NVIDIA's Q3 FY2027 beat crushed consensus (revenue
$115.8bn +103% y/y) but the AH reaction was disputed across vendors
(approx. +2% to +5%); new Board Chair Harvey Jones said the board does not
intend to reinstate Huang; the regular session fell broadly (S&amp;P -1.0%,
zero of 11 sectors higher); Home Depot's beat-and-raise nonetheless fell
-2.45%; converged in two renders (genuine page-4 spillover). Edition 67
(Thu 19 Nov, covering Wed 18 Nov): NVIDIA's AH pop fully round-tripped in
its first full regular session (NVDA -2.89% to $150.96, a clean volatility
crush); the chip-sector read-across rally broadened (AMD +5.31%, Broadcom
+3.64% — these two tickers were originally published SWAPPED in edition
67's own text, corrected at edition 68); equities closed a diffuse,
composition-driven session (S&amp;P -0.23%, Nasdaq +0.42%); Target and Lowe's
beat; FOMC minutes flagged AI-capex as an inflation risk for the first
time; converged in one render, 24/24 sources clean. Edition 68 (Fri 20 Nov,
covering Thu 19 Nov): Anthropic's (ANT) record-breaking Nasdaq debut
($81.3bn raised, the largest IPO on record; priced $83, closed Thursday
+17.1% at $97.17 before easing in AH) was the dominant story, against which
the broader market sold off sharply — equities posted a sixth straight loss
and the stretch's worst breadth (S&amp;P -2.0% to 7,175.83, Dow -2.2% to
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
67's own AMD/Broadcom ticker swap. Edition 69 (Mon 23 Nov, covering Fri 20
Nov, weekend-gap): a severe, broad AI-sector capitulation put the S&amp;P and
Dow into correction territory (S&amp;P -3.7% to 6,910.39, Dow -1.9%, Nasdaq
-5.3% to 22,617.73, negative for the year, worst week since March 2020,
only 1 of 11 sectors higher); the PHLX Semiconductor Index fell 10.7% with
no single catalyst (Nvidia -14.01% to $125.53, Micron -13.89%, AMD -13.25%,
Broadcom -12.19%, Bloom Energy -15.30% largest mover); Intuit's clean beat
drew a one-session-delayed -12.77% decline; two new Nvidia government-
scrutiny threads surfaced (a confirmed Commerce/DOJ Megaspeed probe, an
unconfirmed WSJ SEC-probe claim); UMich final November sentiment rose
sharply to 51.5; December FOMC hike odds eased to approx. 90%; VIX spiked
+26.19% to 35.89. Converged in one render; 25/25 sources clean after one
quick fix. **Edition 70** (Tue 24 Nov, covering Mon 23 Nov): Nvidia's board
reinstated Jensen Huang as President/CEO effective immediately, reversing
the board's own 17 Nov position (confirmed via Nvidia's own 8-K and press
release, corroborated by CNBC, Bloomberg, NBC, Axios, CNN, Al Jazeera) —
NVDA surged +31.59% to $165.19, its best day since May 2003, powering this
report's largest single-session index reversal yet: S&amp;P +4.7% to 7,237.17,
Dow +3.0% to 49,595.31, Nasdaq +6.5% to 24,089.56, breadth flipping from
1-of-11 to 9 of 11 sectors higher. The whole AI-capex complex rallied in
sympathy (Micron +19.04%, Bloom Energy +18.09%, Intel +16.34%, Corning
+14.76%, Applied Materials +14.62%, Super Micro +13.30%, AMD +6.85%,
Broadcom +3.00%). UnitedHealth -1.11% and Anthropic -1.43% to $87.64 were
the only notable decliners. December FOMC hike odds re-firmed to approx.
94% (Kalshi's two-edition empty-array bug was root-caused and fixed: the
correct query is `event_ticker=KXFEDDECISION-26DEC`). VIX partially
unwound Friday's panic spike (-25.83% to 26.62). Gold (+3.28%) and silver
(+4.65%) rallied alongside equities. CFTC's next report was found
holiday-adjusted to Monday 30 Nov. Needed three renders (a genuine page-4
spillover, then the edition-60/65 lonely-trailing-block symptom, fixed by
trimming Annex C); 31/31 sources clean.

**Edition 71 (condensed)** — Wednesday 25 November 2026, covering Tuesday 24
November 2026: the dominant story was a broad reversal of Monday's
Huang-reinstatement rally in the AI-capex complex, even as the Dow closed
above 50,000 for the first time ever and breadth stayed firm (S&amp;P -0.5% to
7,201.09, Nasdaq -1.5% to 23,733.54, Dow +0.9% to 50,018.70, Russell 2000
+0.6% to 2,684.94, 9 of 11 sectors higher). NVDA gave back about a fifth of
Monday's pop (-5.86% to $155.38); the rest of the AI-capex complex unwound
harder still (Micron -11.01%, AMD -8.86%, Intel -8.15%, Super Micro -7.79%,
Applied Materials -6.66%, Bloom Energy -6.98%, Corning -5.95%, Broadcom
-3.98%), with no fresh negative news on any name. Analog Devices plunged
-17.37% to $312.95 despite beating on both current-quarter results and
forward guidance — the day's largest single-stock move and, at the time, an
unresolved "verified move, no confirmed driver" instance (resolved the
following edition — see Standing Facts). Medtronic fell -4.56%, Best Buy
rallied +2.70% on a clean beat-and-raise. Anthropic (ANT) fell a fourth
straight session (-6.54% to $81.91), closing below its $83 IPO price for
the first time, on heavy and genuinely two-sided newly-listed options
activity. December FOMC hike odds held roughly flat at approx. 93% (DeFi
Rate blend). Conference Board consumer confidence jumped to 103.3 from
October's 91.9. A sharper, dated gap opened in the US-China tariff picture:
the underlying US reciprocal-tariff suspension order (EO 14358) expired by
its own terms on 10 Nov 2026, and while China's State Council confirmed its
own extension on 9 Nov, no corresponding US document extending the US side
was found. CBOE's own delayed-quotes feed was completely unreachable this
session (a new full-block failure mode, resolved as transient the following
edition) — Yahoo Finance was used as a disclosed fallback. Gold and silver
both reversed Monday's rally cleanly. USD/JPY's three-edition-standing
cross-vendor direction conflict appeared to resolve (confirmed holding at
edition 72); EUR/USD and GBP/USD's conflicts persisted a second edition
(both resolved at edition 72). No third chart used. Converged in two
renders (one genuine page-4 spillover, fixed by deleting the forced break,
with no Annex-C column-balance symptom); 40/40 sources clean on the first
check — the largest source count logged to date.

**Edition 72 (most recent — full detail)** — Thursday 26 November 2026
report (the edition date falls on Thanksgiving Day, a full US market
closure), covering Wednesday 25 November 2026, the window's one NYSE
session (research window Tue 24 Nov 2026 20:00 ET through Wed 25 Nov 2026
20:20 ET).

**The dominant story was a violent but short-lived intraday AI-capex
whipsaw that mostly reversed into a calm close, overlapping with a
sharply-revised-up GDP print and a resolved "no driver" open thread from
the prior edition.** Per AP's wire (via the lanacion.com.ar mirror,
cross-checked against a second independent recap outlet and SPY/DIA/QQQ/IWM
ETF closes — all fully consistent, and reconciling exactly against edition
71's own published Tuesday closes): the S&amp;P 500 fell as much as approx.
3.2% intraday and the Nasdaq as much as approx. 4% at the open (Nvidia down
approx. 7-8% intraday per Forbes/mlq.ai), before both largely recovered
into the close — S&amp;P 500 -0.3% to 7,182.78, Nasdaq Composite -0.6% to
23,585.80 (the S&amp;P's eighth decline in nine sessions) — while the Dow
Jones Industrial Average, carrying far less AI-capex weight, closed above
50,000 for the first time ever (+0.3% to 50,182.95) and the Russell 2000
added +0.7% to 2,704.06. Breadth broadened to 8 of 11 SPDR sector ETFs
higher (Materials +2.07% led for a second straight session with no driver
found either time; Technology -0.83% and Health Care -0.56% lagged). The
AI-capex complex that cratered Tuesday mostly decelerated rather than
reversed: Micron (-4.53%) and Nvidia (-3.91%) led Wednesday's losses, both
far short of Tuesday's double-digit declines, while Intel (-0.60%) and
Broadcom (-0.07%) effectively flattened out and Super Micro (+3.05%) swung
to a gain — every figure individually verified against its own
price-history page, no fresh negative catalyst found on any name.

**Analog Devices' prior-session "-17.37% with no driver" mystery is
resolved**: Tuesday's plunge followed an outright beat but arrived with
essentially flat Q1 FY2027 revenue guidance, an operating-margin shortfall
and a sharply higher FY2027 capex plan, read by investors as a signal the
industrial chip cycle may be peaking; three desks cut price targets while
maintaining ratings (breaking ADI specifically out of this report's long
analyst-action dry spell); the stock rebounded +6.44% Wednesday to
$333.11. A busy pre-Thanksgiving four-name earnings cluster (HP, Dell,
Workday, Deere), all confirmed via primary 8-Ks, drew four correlated
positive reactions from four beats — the opposite pattern from edition
71's own three-name cluster. HP rallied +11.49% a full session after
reporting (mechanism unexplained); Dell clawed back an approx. -7%
premarket reaction to close +0.60% despite a record AI backlog (mechanism
unexplained); Workday and Deere both drew clean, same-direction positive
reactions. Anthropic's (ANT) four-session post-IPO slide paused (+1.08% to
$82.79) but closed below its $83 IPO price for a second straight session;
Wednesday-specific options data could not be verified.

Q3 2026 GDP's second estimate was revised up sharply to **+4.3%**
annualized (from the 3.4% advance) on upward investment/consumption
revisions; corporate profits rose $206.0bn, decelerating from Q2's $384.0bn
increase. October durable goods orders rose +0.2% m/m. The Fed's Beige
Book described moderate, tariff/energy/healthcare-driven price pressure
across most of its 12 districts and only slight employment growth.
Richmond Fed's November Manufacturing Index rose to 3 from -2 (with an
unresolved internal-source data-display inconsistency on richmondfed.org's
own page). December FOMC hike odds grew harder to pin to one number this
edition — Kalshi's own summary page read approx. 77%, a stale Polymarket
snapshot approx. 87.5%, versus edition 71's approx. 93% DeFi Rate blend
(not re-checked this edition) — flagged as a likely process gap to resolve
at edition 73, not a confirmed reversal. The US-China tariff truce (EO
14358) remained unresolved for a twelfth straight edition. CBOE's feed
returned to full reachability after edition 71's total block, now treated
as transient. Treasury yields deepened Tuesday's bull-flattening (10-year
-6bp to 4.85%). WTI and Henry Hub both showed genuine cross-vendor
improvement; Brent remained the stickiest vendor-revision case; gold split
three ways (Yahoo's +0.99% treated as an outlier against a page-display
glitch); EUR/USD's and GBP/USD's cross-vendor conflicts both resolved,
USD/JPY's direction agreement held a second straight edition. Copper fell
sharply (-2.76% cash) with no driver found. No third chart used. Converged
in ONE render (sections 1-6 ended comfortably on page 3, the common case);
28/28 sources clean on the first check, zero stray tildes, zero
`</td><sup` instances.

**Open threads for edition 73** are listed in the dedicated "Edition 73
(expected to cover...)" section earlier in this spec — not repeated here
to avoid duplication.
