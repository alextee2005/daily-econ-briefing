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
figure cannot be verified, it goes in Annex A.

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
  through 41 have all applied this correctly** ("Friday 2 October 2026"
  through "Wednesday 14 October 2026" as the date line in each respective
  edition, with the window line carrying the session(s) covered) — now
  confirmed stable across nine consecutive editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 41 all reused the
  same pattern for single-session (or single-session-plus-weekend) windows —
  now confirmed clean across thirteen consecutive editions (29 through 41;
  edition 41 phrased it "Window: Mon 12 Oct 2026 20:00 ET – Tue 13 Oct 2026
  20:21 ET (Tue 13 Oct close/AH)"). No further confirmation needed; treat
  this as settled.

## Schedule
Run every weekday. Pick the trigger's local time so the effective research
cutoff lands roughly 4 hours after the US market close (20:15 ET) — during
US daylight time that's 00:00 UTC; adjust for standard time. On Mondays
(or after any gap), cover the full window back to the previous edition's
cutoff, including the weekend.

## Standing facts — verify fresh every edition, never from memory
- **The September 2026 FOMC meeting (15–16 Sept) is fully resolved and does
  not need re-verifying again:** the Committee raised the federal funds target
  range 25bp to 3.75%–4.00% on Wednesday 16 Sept 2026, unanimous 12-0, the
  first hike since 2023.
- **FOMC minutes from the Sept 15-16 meeting — closed thread as of edition 37,
  do not re-derive:** released Wednesday 7 October 2026, 2:00pm ET, read
  directly against federalreserve.gov. Vote was unanimous 12-0 with no dissent
  recorded ("all participants viewed a higher target range... as
  appropriate"). The one internal-division signal: "most participants" (not
  all) assessed that another increase would likely be appropriate by year-end,
  with the Committee stressing data-dependency meeting to meeting. No overt
  October-specific debate was named in the text.
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 41
  directly against federalreserve.gov's own FOMC calendar page — now under
  two weeks out, continue re-confirming every edition until then. Decision
  and press conference both land 28 Oct, 2:30pm ET. The following meeting is
  December 8-9, 2026 (an SEP meeting).
- **October-hike odds jumped sharply at edition 42 on a hot September CPI
  print — the modestly hawkish drift tracked across editions 39-41 turned
  into a genuine repricing, not just a continuation of drift:** DeFi Rate's
  Kalshi/Polymarket-blended aggregator, fresh snapshot Wednesday 14 Oct 2026
  7:06pm ET (post-CPI), shows **October 27-28 hike odds approx. 29%** (hold
  approx. 70%, cut approx. 2%) and **December 8-9 hike odds approx. 78%** —
  up from Tuesday 13 Oct's approx. 19% Oct / approx. 75-77% Dec (edition 41's
  read). The October figure very nearly doubled intraday-equivalent (19%→29%)
  on the CPI beat (headline +3.7% y/y vs. approx. 3.6% consensus, core +2.6%
  vs. approx. 2.5%) — treat this explicitly as a level-shift event tied to a
  dated catalyst, not noise. **A conflicting secondary claim (Seeking Alpha,
  citing CME FedWatch) put the October hike probability at 49.3% post-CPI —
  this could NOT be independently verified at edition 42 and conflicts
  sharply with the directly-fetched DeFi Rate figure (29%); do not cite the
  49.3% figure without independent corroboration.** The composite "at least
  one more hike in 2026" read has still not been freshly re-pulled since
  edition 38 (last known approx. 80%) — don't cite without a fresh pull.
  Kalshi's own direct fetch failed again at edition 42 (429/timeout), now a
  confirmed standing failure mode across six consecutive attempts (37-42).
  Official CME FedWatch also failed again directly (429/timeout) at edition
  42.
- **US-China "30-for-30" tariff framework — closed thread as of edition 37, do
  not re-open:** the list-size reversal flagged at edition 36 (a secondary
  source describing China's list at ~1,619 items and the US list at 77, the
  opposite of the long-standing primary-confirmed framing) is resolved. A
  direct whitehouse.gov fetch of the framework's own Terms of Reference
  document, confirmed at edition 37, shows the original assignment is
  correct: **77 US product categories (household goods, textiles, appliances,
  toys, sporting goods, vacuum flasks) and 1,619 Chinese categories (dominated
  by food/farm goods — beef, pork, poultry, seafood, grains, dairy,
  wine/whiskey — plus some medical devices; soybeans, chips, EVs and batteries
  excluded from both sides)**, each side's treatment benchmarked at approx.
  $30bn against 2024 bilateral trade. Still pending each side's domestic legal
  processes for actual implementation — no Federal Register/USTR
  implementation notice has been found through edition 41 (only unrelated
  routine Section 301 product-exclusion conforming amendments) — watch for a
  formal implementation/effective date in a future edition. No fresh US-China
  tariff/trade news of any kind was found dated specifically to 13 October at
  edition 41 either. The two whitehouse.gov PDF copies carrying different
  dates (Sept 23 vs Sept 27, 2026) remains an unresolved minor wrinkle, not
  worth chasing unless load-bearing.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch,
  rba.gov.au, etc.) every edition, exactly like any other data point. Edition
  42 re-confirmed Kevin Warsh as Fed Chair directly against
  federalreserve.gov's Board of Governors bios page — **a twelfth straight
  direct re-confirmation.** The BoE's next decision (Thursday 5 November) was
  freshly re-touched at edition 42 via a direct bankofengland.co.uk fetch —
  unchanged, now confirmed directly for four straight editions (39-42) inside
  the roughly 3-week window. **The shutdown/CR status check regressed at
  edition 42**: a direct whitehouse.gov briefing-room fetch did not surface
  funding-specific content either way (unlike edition 41's genuine direct
  hit), so edition 42's "funded through 11 December 2026, no shutdown" read
  relies on secondary corroboration (news coverage of H.R. 6500's signing)
  rather than a clean primary-source confirmation — **re-attempt a genuine
  direct whitehouse.gov hit at edition 43 rather than treating this
  secondary-only method as the new normal.** The BoJ's next-meeting-date
  primary source stayed confirmed via direct read at edition 42: a direct
  boj.or.jp fetch of its Monetary Policy Meeting schedule page confirmed Oct
  29 (Thu) – Oct 30 (Fri), 2026 in plain text, unchanged, now two straight
  editions on the restored direct-fetch method (41, 42). **The FOMC's own
  decision/press-conference time (2:30pm ET, 28 Oct) was not re-displayed on
  federalreserve.gov's calendar page at edition 42's fetch** — the date
  itself (27-28 Oct) was confirmed directly, but the specific time sub-detail
  was carried forward unverified this pass; re-confirm the time directly next
  edition rather than letting this lapse further.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed directly
  again at edition 42 (following decision 17 December 2026). Continue the
  direct-fetch discipline every edition given the meeting is now about three
  weeks out.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano), both primary-sourced as of edition 37 — closed thread, do
  not re-derive. **The next policy meeting date (Oct 29-30, 2026) was
  re-confirmed via a direct boj.or.jp plain-text fetch again at edition 42**,
  now two straight editions (41, 42) on the stronger direct-fetch method
  after edition 40's one-edition secondary-only step-down. No doubt has ever
  existed about the underlying fact — only the method varied — and the
  method has stayed on the preferred standard since.
- **The four-central-bank Thursday 24 September 2026 cluster remains fully
  resolved — closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% (matching an 18-economist
  Bloomberg survey) but signalled a greater chance of a Q4 hike; Banxico held
  at 6.50% unanimously; SNB held at 0% and raised its inflation forecasts
  (0.7%/0.8%/0.8% for 2026-28), confirmed directly against snb.ch. No fifth
  central-bank decision was identified in this window either.
- **The Reserve Bank of Australia's Tuesday 29 September 2026 decision remains
  fully resolved — closed thread, do not re-open:** hiked 25bp to **4.60%,
  unanimous**, a 15-year high and its fourth hike of 2026, confirmed directly
  against rba.gov.au's own Statement by the Monetary Policy Board.
- **August 2026 PCE inflation — closed thread, resolved at edition 32, do not
  re-open:** headline +0.3% m/m/+3.4% y/y (down from 3.7% in July), core +0.2%
  m/m/+3.0% y/y (down from 3.3% in July) — a clean disinflation signal that was
  the proximate trigger (with NY Fed Williams' remarks) for edition 32's
  October-hike-odds collapse. One minor sub-item never resolved and remains a
  standing Annex-A-level gap if it ever matters again: the precise quantified
  effect of BEA's concurrent annual benchmark revision on the y/y base was not
  isolated from the release text.
- **September 2026 jobs report — closed thread since edition 34, do not
  re-derive, but watch for revisions in later BLS releases:** nonfarm payrolls
  +29,000 (the weakest print of the cycle) vs. approx. 84,000-90,000
  consensus; unemployment rate 4.2% (up from 4.1%); average hourly earnings
  +0.1% m/m / +3.0% y/y; July revised from +21,000 to an outright -10,000,
  August revised from +162,000 to +133,000 (a combined -60,000 revision),
  confirmed directly against bls.gov's Employment Situation Summary. This was
  the single biggest catalyst of edition 34's window — see the October-hike
  odds entry above for how the market reaction has since evolved.
- **September 2026 ISM Services/Non-Manufacturing PMI — closed thread as of
  edition 35, do not re-derive:** headline 54.9% (down from August's 55.4%),
  Prices Paid 74.0% (+1.4pt, highest since July 2022), the sixth month in
  seven above 70%. Confirmed directly against ISM's own press release.
- **September 2026 US CPI — closed thread as of edition 42, do not re-derive,
  but watch for its effect on rate-path odds in subsequent editions:**
  headline **+0.6% m/m / +3.7% y/y** (prior +0.4% m/m), core **+0.3% m/m /
  +2.6% y/y** (up from 2.4% in August), both above the Dow Jones consensus of
  approx. 3.6%/2.5% — a genuine upside surprise on both measures, confirmed
  directly against bls.gov's CPI Summary release. Gasoline (+9.1% m/m)
  accounted for over half of the monthly all-items increase. **This was the
  proximate trigger for edition 42's broad equity selloff, VIX spike (+10.5%)
  and the sharp October-hike-odds repricing (approx. 19%→29%)** — see the
  rate-path-odds entry above. One minor sourcing note: a secondary preview
  (Admiral Markets) had cited a slightly different consensus range (approx.
  3.6-3.7%/2.4%) than the CNBC/Dow-Jones figure used above — disclosed, not
  resolved, low-priority given the print itself is primary-sourced and
  unambiguous.
- **No US federal government shutdown is in effect — status unchanged, but
  edition 42's confirmation method regressed to secondary-only** (see general
  principle entry above). H.R. 6500, the Continuing Appropriations and
  Extensions Act, 2027, signed into law 2 September 2026, funds the
  government through **11 December 2026**. Re-attempt a genuine direct
  whitehouse.gov hit at edition 43 (either the dated-permalink or
  briefing-room-index pattern, both previously confirmed working) rather than
  settling for secondary corroboration two editions running. Watch for
  shutdown risk resurfacing as 11 December 2026 approaches.
- **University of Michigan preliminary October 2026 consumer sentiment —
  still not yet a "closed thread," watch for the final reading:** 46.3, a
  five-month low (current conditions 44.7, expectations 47.3, year-ahead
  inflation expectations 4.7% from 4.6%, long-run 3.5% from 3.4%), confirmed
  via investinglive.com and advisorperspectives.com (dshort), both dated 9
  Oct 2026. Consensus estimates disagreed sharply across outlets (approx.
  47.6-50.5) — no single consensus figure should be cited without disclosing
  the range. **Final October reading due 23 October 2026** — watch for it;
  not yet re-touched since edition 40 (now under 9 days out).
- **China September 2026 CPI/PPI — RESOLVED at edition 42, closed thread, do
  not re-derive:** CPI **+0.9% y/y** (+0.2% m/m, up from +0.8% in August),
  PPI **+5.0% y/y** (up sharply from +3.8% in August, the fastest PPI rise
  since June 2022), driven by fuel costs (gasoline +16.6% y/y); food prices
  -1.7% y/y. **Sourcing caveat worth carrying forward: a direct stats.gov.cn
  fetch again failed at edition 42** (stale, August-data-only listing) — the
  print above is sourced to gov.cn's English-language, NBS-attributed news
  release (a quasi-primary government portal, not stats.gov.cn itself),
  corroborated by CNBC. If stats.gov.cn remains unreachable in future
  editions, continue treating the gov.cn English release as an acceptable
  near-primary substitute rather than marking China CPI/PPI unavailable.
- **New calendar-awareness item from edition 40, reconfirmed relevant at
  edition 41: "equities-open, bonds-closed" US holidays need an explicit
  check every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed (SIFMA-recommended bond holiday). Edition 41 confirmed the knock-on
  effects directly: Tuesday 13 Oct's Treasury-yield print was the first fresh
  one since Friday 9 Oct (2-yr eased to 4.79% from 4.80%, 10-yr to 5.21% from
  5.24%, 30-yr to 5.56% from 5.60%), and the SOFR overnight fixing published
  Tuesday carried an *effective date* of 9 October (rate unchanged at 3.87%)
  because the normal Oct-9-covering publish day (Monday Oct 12) was the
  holiday — Tuesday 13 Oct's own SOFR fixing had not yet posted as of
  edition 41's cutoff and was expected around 8am ET Wednesday 14 Oct (the
  NY Fed publishes each day's SOFR at ~8am ET the following business day).
  This was confirmed via a direct NY Fed Markets Data API fetch this time,
  not just inferred circumstantially as at edition 40 — treat the mechanism
  as fully understood now. **Next candidate to verify when it lands: Veterans
  Day, Wed 11 Nov 2026 — confirm whether that is also bonds-only before
  assuming.**
- **New data-quality item from edition 41: a vendor can retroactively revise a
  previously-logged prior-session close.** Investing.com's historical-data
  tables for WTI and Brent now show Monday 12 October's own day-over-day %
  change with the *opposite sign* from what this report logged in the
  edition-40 briefing (now shown as approx. +2.06%/+1.84% vs. the
  logged -0.92%/-0.86%); the same table also quietly revised Henry Hub's
  logged Monday close from $3.180 to $3.167. The most likely mechanism is a
  post-hoc settlement-data correction tied to Monday's Columbus Day holiday
  session, but this was not independently adjudicated — it does not change
  Tuesday's own figures, which reconcile cleanly against either Monday base,
  but it is a genuinely new trap class (distinct from stale-date
  republishing, snapshot-mistaken-for-close, and carried-forward-assumption)
  worth naming explicitly: **a vendor's own historical table is not
  guaranteed to still match what this report logged for a prior session,
  even days later** — when doing the standard prior-close reconciliation, if
  a vendor's current table disagrees with this report's own logged figure
  for the base date, disclose it rather than silently trusting either one.
  Henry Hub's Tuesday 13 Oct change is left ambiguous between +4.80% (the
  vendor's revised base) and +4.37% (this report's previously-logged base) —
  both reported, unresolved.
- **The vendor-retroactive-revision trap broadened significantly at edition
  42, worth treating as a durable, cross-instrument risk rather than an
  oil/gas-specific quirk.** Henry Hub's Tuesday base was revised a SECOND
  time (edition 41 logged $3.319; edition 42's fetch of the same vendor table
  showed $3.283) — the ambiguity on Wednesday's direction got WORSE, not
  better (computed change flips sign depending on base: +0.18% vs. -0.90%).
  WTI's Tuesday %-change was also revised again (edition 41 logged +1.10%;
  edition 42's fetch showed +0.43%). **For the first time, the same pattern
  hit FX**: Investing.com's own historical tables showed EUR/USD's and
  GBP/USD's logged Tuesday %-changes drift slightly (0.41%→0.39%,
  0.37%→0.35%) and USD/JPY's drift materially (-0.39%→-0.20%, nearly halving
  the logged magnitude). **Treat every instrument's prior-session base as
  provisional until re-confirmed, not just oil/gas** — continue disclosing
  any mismatch between a vendor's current table and this report's own
  previously-logged figure rather than silently resolving it, now across the
  full commodities/FX complex.
- **A new, distinct trap logged for the first time at edition 42: a vendor's
  live "spot" quote can lag or mistime a sharp single-session move captured
  cleanly by the futures settlement on the same page.** On a session where
  gold and silver futures both sold off hard (gold -1.06%, silver -6.14% —
  the latter the largest single-session commodity move logged by this report
  in recent editions), Kitco's own live spot ticker showed both metals UP
  (+0.83%/+0.75%) — directly contradicting Kitco's own published headlines
  on the same page ("gold falls below $4,100, silver plunges 6%"), which
  matched the futures move exactly. The most likely explanation is the spot
  ticker reflecting a later intraday rebound rather than Wednesday's
  settlement. **When a vendor's own live quote conflicts with that same
  vendor's own published headline/commentary, trust the headline-aligned
  figure (here, futures settlement) and disclose the live-quote conflict
  rather than averaging or silently picking the live figure** — this is
  distinct from the COMEX-settle-vs-continuous-spot divergence already
  documented (edition 22), which is a legitimate timing difference rather
  than one source contradicting itself.

## Role framing
Write as a top-tier economist / equity, commodity and derivatives investor,
sector-agnostic. Plain English. Single-stock focus (see coverage below).

## Coverage and weighting
Single stocks are the centre of gravity. Weight roughly: **~45% single
stocks & earnings, ~20% macro, ~20% commodities/FX, ~15% derivatives.**
1. **US equities & earnings (LEAD, largest section)** — index closes, sector
   rotation, single-stock movers, earnings since last cutoff, guidance
   changes, analyst actions. **Bias name selection toward:** Technology,
   SaaS/software, consumer staples, consumer discretionary, telcos, and
   large industrials. This is the section the user reads first — give it the
   most column space and the most "why it moved / read-across" depth.
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
- **Length:** 3 pages of briefing + 1-page annex. Do not exceed.
- **No "So what" lines.** Interpretation lives in the 60-second read at the
  top, and inline only where a number is meaningless without it — never as a
  standalone labelled line.
- **Sources:** numbered inline references `[n]` in a small blue superscript
  span, full list in Annex B. Never inline URLs in the body. **Each citation
  number gets its own `<sup class="ref">[n]</sup>` tag** — do not write
  `[26][27]` inside one sup tag; write `<sup class="ref">[26]</sup><sup
  class="ref">[27]</sup>`. `check_refs.py`'s regex only matches one bracket
  per sup tag, so combined-bracket citations silently fail the cross-check
  (this bit edition 22 — caught and fixed before render, avoid it from the
  start). Note that bracket text baked into a chart PNG's axis label (e.g.
  `[6]`) is NOT scanned by `check_refs.py` (it only reads the HTML, not image
  pixels) — keep those numbers consistent with Annex B by hand; the tool
  can't catch a mismatch there. **Also watch for a stray bracket typed outside
  a `<sup>` tag entirely** (e.g. `<sup class="ref">[27]</sup>[28]`) — edition
  27 caught one of these in its own draft before rendering; `check_refs.py`
  will not flag it since its regex only matches inside `sup class="ref"`
  tags, so a bare `[n]` slips through silently. Proofread citation-heavy
  sentences visually, not just via the script, when a sentence carries two or
  more consecutive citations. A related trap surfaced at edition 28's own
  draft, worth naming explicitly: placeholder ref text (e.g. `[note1]`) typed
  during drafting and never swapped for a real number. `check_refs.py`'s
  regex requires `\d+` inside the brackets, so a non-numeric placeholder like
  `[note1]` simply won't match either the inline or Annex-B regex — it won't
  show up as "missing" or "unused," it just silently doesn't count. **Never
  use a letter suffix to disambiguate a citation — always mint a new
  integer** (edition 30's `[9b]` near-miss). Annex B numbers do not need to
  be contiguous, only matched 1:1 against inline citations — deleting an
  unused reserved number and leaving a gap is completely fine and simpler
  than renumbering everything after it (edition 29). **Reusing the same
  Annex B number for multiple movers/figures citing the same outlet/method is
  fine and recommended** — `check_refs.py` only checks presence/absence, not
  uniqueness of use (editions 33-41 have all done this for stockanalysis.com
  single-stock closes and other repeatedly-used outlets, confirmed stable
  across eight editions).
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart 2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes). **Chart
  placement is editorial, not fixed to Section 2** — edition 24, edition 34
  and edition 39 all placed a CFTC-positioning chart #2 in Section 5
  (Derivatives) rather than Section 2, since that's where the content
  actually belongs. Editions 35 through 41 (seven straight) reverted to the
  sector-ETF-proxy default (no fresh CoT data due in any of those editions)
  and kept it in its default Section 2 placement.
- **Tilt:** market-wide. No portfolio tilt, no holdings commentary.
- **Window:** everything since the previous edition's cutoff. On Mondays
  (or after any gap) this includes the weekend/missed sessions.
- **Data gaps:** keep Annex A. State plainly what could not be verified.
  Never estimate, infer, or fill from memory.
- **Page margins:** 1 inch (25.4mm) top and bottom, 13mm left and right.
- **Text alignment:** body prose (paragraphs, bullet lists) justified.
  Tables, headers (h1/h2/h3), the snap-grid tiles, the meta line, and Annex
  B's narrow 3-column source list stay left-aligned — justifying short table
  cells or a dense multi-column list produces ugly ragged spacing.

## Hard rules
- Every data point needs a named source. If unverifiable, say so in Annex A
  rather than producing a plausible-sounding number.
- Where sources disagree, use the more authoritative one **and** disclose
  the disagreement. AP's "How major US stock indexes fared" and the Reuters
  market wrap are normally the most reliable for index closes — but check
  they're actually indexed for the target date before relying on them; this
  has occasionally failed to post in time (15 Sept gap at ed. 21, 22 Sept gap
  at ed. 26 requiring the Yahoo Finance/FRED fallback chain both times).
  **Editions 27 through 41 are all clean counter-examples worth keeping in
  mind**: all fifteen posted a usable AP wire eventually — editions 38 and
  39 both needed a syndication mirror (La Nación) rather than a direct
  AP fetch; edition 40 hit a harder version of the same problem (both a
  direct fetch and two syndication-mirror URLs returned HTTP 403) and
  recovered the figures via a search-engine snippet instead. **Edition 41
  reverted to a clean, easy case**: a direct AP wire wasn't attempted first,
  but two syndication mirrors (wtop.com, krmg.com) both posted the Tuesday
  wrap on time with matching figures, arithmetically reconciling against the
  prior edition's logged Monday closes with no gap or fallback needed.
  Treat "search-snippet recovery with multi-source reconciliation" as an
  acceptable fallback tier below a syndication mirror, not a reason to
  discard the figures, provided the reconciliation genuinely checks out.
  **Edition 37 is a useful cautionary tale about method, not about the source
  itself**: a general-purpose WebSearch AI-summary returned the correct AP
  figures attached to a *guessed* URL, and the research subagent — correctly
  following the standing caution about AI-summarized fetches inventing
  numbers — could not independently corroborate it and flagged it as
  possibly fabricated. **The lead/writer step then directly re-fetched the
  real article plus a second independent syndication mirror and got the
  exact same figures, confirming they were correct all along, not
  fabricated.** The lesson stands: the standing caution against AI-summary
  fabrication is about **unverified precision that conflicts with
  everything else** — a precise figure that *cannot yet be corroborated* is
  not automatically a fabrication, and the correct response is to attempt a
  direct, independent second fetch before discarding it, not to assume bad
  faith by default. Always have Yahoo Finance + FRED/stockanalysis.com ready
  as the working fallback regardless. **Edition 36's AMD-price-target and
  Novavax/Moderna-driver fabrications remain the clearer, more severe
  examples of the opposite failure mode** (a number that conflicted with
  independently-sourced reality) — both lessons stand side by side: verify
  before excluding AND verify before including.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. This has been caught at least thirteen times across editions 25
  through 34 (Trefis, Rio Times, FXStreet, Kitco and others re-serving prior-
  day data under a new dateline). **Edition 35 caught a distinct variant on
  analyst commentary rather than price data** (stale Nike price-target cuts
  recirculated as if dated Monday when they were Friday/Saturday originals).
  **Edition 41 surfaced a further distinct variant, worth tracking as its
  own trap class rather than folding into "stale-date republishing": a
  vendor can retroactively *revise* a previously-logged prior-session close
  days after the fact** (Investing.com's WTI/Brent/Henry Hub Monday 12 Oct
  figures all changed under the hood between edition 40 and edition 41's
  checks) — see the Standing Facts entry above for the full write-up. Always
  check a dated article's own body text against the logged prior-session
  figures before trusting its date stamp, regardless of which outlet it is,
  and when doing the standard prior-close reconciliation, disclose rather
  than silently resolve any gap between a vendor's current table and this
  report's own previously-logged figure for the base date. A same-day close
  and a next-day after-hours-triggered move can legitimately combine into
  one large single-day % change — edition 24's Xenon Pharmaceuticals -30.7%
  Friday move is the reference example. Check whether a headline % move is
  measured close-to-close before assuming two reports conflict. **The
  intraday-vs-close divergence trap is still very much alive**, caught across
  many editions (Worthington, Paychex/Cracker Barrel, Oracle, Akamai,
  STX/WDC/SNDK, MongoDB, Liquidia, Concentrix, Citigroup options-wire, Nike,
  SPCX, Moderna, AST SpaceMobile). **A distinct corporate-action
  (stock-split) data artifact trap was first logged at edition 35**
  (Paramount Skydance's spurious "+96%" premarket figure, actually a 2-for-1
  split artifact) — before reporting any single-stock move that looks like
  an outright magnitude error (roughly doubling, halving, or near-100%),
  check for a split/reverse-split/listing change and exclude the figure if a
  stale unadjusted-quote explanation fits. **Edition 41 hit a fresh
  candidate for this trap (Bumble +56.58% to $5.95) but could not positively
  confirm a split either way** given sparse coverage — excluded from the
  body and flagged in Annex A rather than reported as a verified move; check
  for a delayed explanation (split or otherwise) at edition 42. **A related
  but distinct ticker-change trap recurred at edition 36-37**: when Paramount
  Skydance/Warner Bros. Discovery's $110bn merger closed Tuesday 6 Oct and
  the surviving entity moved to ticker SKYD, no reliable same-day % figure
  was obtainable on the transition day itself — but by the very next
  session, stockanalysis.com had a clean, exchange-timestamped close under
  the new ticker, fully resolvable. **General technique worth keeping: when
  a ticker-change/listing-transition makes the transition day itself
  unsourceable, don't force it — but re-check the new ticker on the very
  next session, since the gap is often transition-day-only, not durable.**
  **The "driver not found same-session, found next session" pattern that
  first appeared at edition 37→38 (Caterpillar) recurred and mostly
  RESOLVED at edition 41**: the AI-optics/AI-hardware selloff cluster
  (AAOI, COHR, LITE, CIEN) that had gone unexplained across editions 39-40
  (and gained three more names at edition 40: Cerebras, Semtech, Ciena)
  finally found a dated driver at edition 41 — MarketWatch and corroborating
  coverage (TradingView/Stocktwits, 247wallst) tied Monday 12 Oct's sharp
  selloff to Broadcom CEO Hock Tan's remarks on capital-access constraints
  limiting AI infrastructure expansion, with Intel's CEO separately flagging
  higher borrowing costs and AI-return uncertainty. **This closes the thread
  for AAOI, COHR, LITE, CIEN, Cerebras and Semtech** — treat as resolved
  unless a fresh unexplained move recurs. **Fastly remains the one holdout,
  now unexplained for a FOURTH consecutive session** (edition 39's +15.86%
  spike, edition 40's -9.80% partial unwind, edition 41's +2.50%, edition
  42's -7.72%, still no driver found despite a genuine search each time) —
  a Sept 2 Schaeffer's Research short-squeeze-potential piece is suggestive
  context only, not a same-day driver. Keep checking at edition 43; this is
  now the longest-running unexplained-mover thread this report has carried.
  General technique worth keeping: when a same-day mover's driver can't be
  found despite a real search attempt, don't force a guess — report the
  move without a driver and explicitly flag it as an open thread, then
  re-search for a delayed explanation at the very next edition before
  assuming none exists.
- **The "preview-consensus-only miss/beat framing" caution (first logged at
  edition 41) remains open after a genuine follow-up attempt at edition 42:**
  neither JPMorgan's $5.57 EPS "miss" framing nor the Wells Fargo/Citigroup
  credit-provision-rationale inference could be confirmed or corrected by any
  dated article despite a targeted search — both are carried forward
  unresolved into edition 43. **A competing explanation for the
  Wells-Fargo/Citigroup selloff surfaced at edition 42**: multiple sources
  (TIKR, finviz) described a yields-driven, sector-wide bank selloff ahead of
  Tuesday's reports (10-year near 5.30%, the big-five banks down approx.
  $270bn combined from summer peaks) — this is at least as plausible as the
  credit-provision inference and itself not confirmed to the specific stock
  moves by name either. **Treat this as a case where two competing disclosed
  inferences coexist, neither confirmed** — report both, favor neither,
  and keep searching for a dated article that actually ties cause to effect.
  **The underlying caution (arithmetic comparison against preview-consensus
  aggregators, or a subagent's own inference from primary filings, is a
  disclosed inference, not a confirmed fact, until a dated post-earnings
  article corroborates it) applies identically to edition 42's own new
  preview-consensus comparisons**: Bank of America's GAAP EPS ($1.08) read
  as a miss against preview-consensus aggregators clustered near
  $1.11-1.18, and Morgan Stanley's EPS ($3.03) read as a beat against an
  Earnings Whispers consensus of $3.01 — both disclosed as inferences in the
  edition 42 body, neither independently confirmed by a dated "beat/miss"
  article.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. **Similarly, a price level can be correct while a vendor's stated
  %-change is wrong** if the vendor used a different prior-day base — always
  sanity-check that a stated price and stated % change reconcile
  arithmetically against the prior session's logged close. This exact pattern
  has now recurred repeatedly on oil across editions 35, 37 and 38, narrowed
  to WTI-only at edition 39, cleared for BOTH grades at editions 40, 41 and
  **42** (WTI +0.70%, Brent +0.35%, both matching vendor-stated exactly
  against the vendor's *own* current-table Tuesday base) — a third
  consecutive clean dual-grade reconciliation, though the Tuesday *base
  itself* was again flagged as retroactively revised (WTI's logged Tuesday
  change shifted from +1.10% at edition 41 to +0.43% as re-fetched at
  edition 42) — the base-revision wrinkle first spotted at edition 41 is now
  a recurring, not one-off, pattern. **Don't treat this as the underlying
  problem being fixed** — oil/gas/FX vendor data has now shown nearly every
  combination of clean and dirty reconciliation; keep computing and
  disclosing every edition regardless of how the last one went. **Edition 42
  found the vendor-%-vs-computed-%change gap on Henry Hub natural gas for a
  second straight edition** (the Tuesday base was revised again, $3.319→
  $3.283, leaving Wednesday's change ambiguous between +0.18% and -0.90% —
  worse than edition 41's single ambiguity, since the sign itself now
  flips) — and **for the first time, the same retroactive-base-revision
  mechanism hit FX**: EUR/USD, GBP/USD and USD/JPY's logged Tuesday
  %-changes all drifted from edition 41's figures (USD/JPY materially, -0.39%
  to -0.20%). Gold and silver futures reconciled cleanly against their own
  logged bases, but a NEW, distinct trap appeared on the spot side (see the
  Kitco entry in Known-hard-to-source). Broaden the standing guidance
  further: **compute every commodity and FX %-change directly off this
  report's own logged prior close, every edition, for every instrument, and
  treat every logged prior-session base itself as provisional until
  re-confirmed** — disclose the method explicitly in the text with a
  footnote (standard practice since edition 39). The oil contract-month-roll
  trap (Brent Nov-to-Dec) remains resolved; neither grade rolled at edition
  42 (WTI still Nov '26/CLX6, Brent still Dec '26/LCOZ6). Henry Hub also has
  not yet rolled to December (still Nov '26/NGX6 at edition 42). The CBOE
  vol-complex feed's two documented bugs (duplicate-`prev_day_close`, and
  `price_change_percent` dividing by current price instead of prior close)
  were **ABSENT again at edition 42 — a third consecutive clean edition
  (40-42)** after recurring at edition 39 following four clean editions
  (35-38), and this on the largest single-session VIX move logged all cycle.
  This does NOT mean the bugs are fixed: they are genuinely intermittent.
  Always compute day-over-day % change manually as `price_change ÷
  (current_price − price_change)` and treat the feed's own
  `price_change_percent` field as unreliable until checked each time
  regardless, even after consecutive clean reads.
- **The DXY-vs-its-own-FX-crosses conflict RESUMED at edition 42** after a
  three-session pause (39-41): Wednesday's DXY rose +0.36% while USD/JPY fell
  -0.21% — opposite directions, the classic USD/JPY-specific divergence
  pattern (DXY/EUR/GBP read broad dollar strength while the yen itself
  strengthened). This confirms the pattern is genuinely intermittent, not
  resolved — continue disclosing the DXY-vs-crosses comparison explicitly
  every edition regardless of which way it goes, and do not assume either
  continuation or reversal from one session's read.
- **The same-day silver sign conflict first flagged at edition 31 has
  technically recurred at edition 42, but with a disclosed, plausible
  explanation rather than a genuine data-integrity failure** — see the Kitco
  spot-vs-futures entry in Known-hard-to-source. The close-to-close FUTURES
  comparison specifically (the basis for the original edition-31 thread)
  remains clean; the conflict this time was spot-vs-futures on the same
  vendor's page, a distinct and newly-logged trap. Treat the original thread
  as still resolved; treat the new spot-ticker-lag trap as its own item to
  watch.
- **GBP/USD's two-edition data-quality problem (a minor two-source gap at
  edition 35, a genuine three-way level/direction conflict at edition 36)
  has now stayed resolved for six further editions (37-42)**, with edition
  42 again single-sourced cleanly to Investing.com's close-to-close history
  table (no conflict found, -0.19% computed) — consistent with the
  lighter-touch approach used since edition 39. Resume the fuller
  multi-source method if a fresh conflict reappears, or periodically to
  re-confirm the lighter method is still safe.
- **The 2-year Treasury yield conflict from edition 36 (TextView 4.46% vs.
  CSV 4.79%, a 33bp gap) has stayed resolved for six further editions
  (37-42)** — edition 42 again fetched both the TextView and CSV endpoints
  directly and found them in **full agreement** (2-yr 4.82%, 10-yr 5.19%,
  30-yr 5.52%, all 14 Oct — the curve flattened on the day, 2-yr +3bp while
  10-yr/30-yr eased -2bp/-4bp as hawkish front-end repricing met risk-off
  long-end demand). Treat as resolved/noise unless a fresh conflict appears;
  if one does, the standing advice stands — dig into which endpoint is wrong
  via a market-wrap secondary cross-check for the specific disputed
  maturity.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 42 have all run clean (or
  clean after one quick fix) — **edition 42 drafted clean at 47/49 on the
  first pass (two Annex-B-only orphans — a disclosure-box SPY cross-check
  mention and a Seeking Alpha claim — both caught and given inline citations
  before render)**, close to edition 40/41's clean-first-pass track record.
  Worth re-stating: table cells (and disclosure-box/tile-adjacent sentences)
  are a legitimate, already-used place to put a citation — use them rather
  than forcing an awkward prose mention just to attach a `<sup>` tag.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 42 have all rendered clean at zero tildes** on the
  first check. **Reminder: `grep -c` exits with status 1 (not 0) when the
  count is zero, since no lines matched — don't chain it with `&&` into a
  longer command and assume a silent failure means the check itself failed;
  read the printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 34 resolved this cleanly for
  CFTC CoT, with full OI and Asset-Manager/Leveraged-Funds breakdowns for
  ES, NQ and RTY. Edition 39 repeated this successfully. One naming note
  worth preserving: the CFTC's financial-futures table lists the full-size
  Russell 2000 E-mini ("RTY") as a separate line from the Micro E-mini
  Russell 2000, which has very different (much smaller) open interest and a
  different net-position sign at times — always confirm which line is being
  read before charting. **The next CFTC report is due Friday 16 October
  2026, 3:30pm ET, covering Tuesday 13 October data** — this did not fall
  inside edition 42's window either (re-confirmed directly against
  cftc.gov's own release schedule with no delay notice: October dates are
  the 2nd, 9th, 16th, 23rd and 30th, all Fridays), so edition 42 correctly
  reverted to the sector-ETF-proxy chart #2 default per standing guidance.
  **This report should land inside edition 43's window** (the edition
  covering Friday 16 October) — check cftc.gov directly at edition 43 and
  expect to finally pull it, rather than assuming another gap.
- **A genuinely new chart-layout bug surfaced at edition 37, worth fixing
  permanently in `make_charts.py`'s documented defaults: the sector-ETF-proxy
  panel2 chart at `figsize=(9.8, 1.55)` with `tick_fs=7.6` and 11 categories
  produced visibly overlapping y-axis category labels** (confirmed by
  rendering and visually inspecting the PNG directly, not just trusting the
  matplotlib call succeeded) — the 1.55-inch height does not give 11 rows
  enough vertical room at that font size in this environment. **Fixed by
  bumping panel2's figsize to `(9.8, 1.95)`**, which rendered cleanly with no
  overlap; editions 38 through 41 have all reused this for 11-category
  panels and confirmed it again each time. **Edition 39 refined this
  further: a fuller `figsize=(9.8, 1.95)` is NOT needed for
  lower-category-count charts** — scale figsize down for charts with fewer
  categories (roughly `(9.8, 1.95)` for 10-11 categories, `(9.8, 1.65-1.85)`
  for 3-8 categories), and always visually inspect the actual PNG at or near
  full resolution before embedding it regardless of category count. **Edition
  41 used `(9.8, 1.8)` for an 8-category single-stock movers chart** (JNJ,
  C, DPZ, WFC, AAOI, SMTC, CBRS, JPM) and reused `(9.8, 1.95)` for the
  11-category sector panel, both with `pad_frac=0.24` — both rendered
  cleanly on the first attempt with no label overlap. **Edition 42 repeated
  the identical pairing** (`(9.8, 1.8)` for an 8-category movers chart —
  CRWV, ORCL, FSLY, GEV, BAC, MS, FAST, BMBL — and `(9.8, 1.95)` for the
  11-category sector panel, both `pad_frac=0.24`), again clean on the first
  attempt — a further data point confirming the `(9.8, 1.65-1.85)`-ish range
  works for mid-sized category counts (8 specifically landed fine at 1.8
  twice running) and that `(9.8, 1.95)` remains a safe, if slightly
  generous, ceiling for 11.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at editions 33 through 42 (edition 41: JNJ -5.73% vs. C -5.60%, about
  1.02x; edition 42: CRWV -15.46% vs. ORCL -8.83%, about 1.75x), all left
  uncapped. Edition 30 remains the one genuine 10x+ case to date (about 15x,
  capped at a fixed axis max of 30). No need to revisit the threshold or
  mechanism absent a genuinely new edge case (e.g. something in the 5-10x
  range).
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists** — confirmed again at edition 35 (four
  analyst actions all traced to one Benzinga/Yahoo roundup, disclosed as
  such). Edition 37 hit the inverse problem (no roundup for any name could be
  located at all), edition 38 hit a milder version (only the session's own
  biggest earnings mover had dated activity), edition 39 broke that streak
  with a normal, well-corroborated result (Goldman/Palantir upgrade, two
  Humana PT raises), and **editions 40 through 42 all reverted to the
  empty-result pattern** — no analyst action dated specifically to 12, 13 or
  14 October could be independently confirmed for any name despite a
  genuine search each time (three consecutive empty editions now). **The
  pattern across 37-42 (empty, thin, normal, empty, empty, empty) is now
  tilted clearly toward empty, though still worth treating each edition's
  result on its own merits rather than assuming the search is broken** — an
  empty result remains a legitimate, disclosable gap, not a sign of a broken
  search.
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38**: a secondary aggregator (TheFly, via stockanalysis.com's news
  feed) cited Applied Digital's Q1 EPS as "+1¢ vs. a -30¢ consensus," which
  flatly conflicted with the GAAP figures in the company's own 8-K. The
  likely explanation is that the aggregator's figure is a non-GAAP/adjusted
  metric reported without stating its basis — **when a secondary-sourced EPS
  figure conflicts sharply with a primary filing's GAAP number, prefer the
  primary filing, exclude the conflicting secondary figure from the main
  text, and flag it in Annex A rather than trying to reconcile or silently
  picking one.** **Edition 39 encountered a related-but-distinct, non-trap
  scenario worth contrasting explicitly: Delta Air Lines' own 8-K disclosed
  BOTH a GAAP diluted EPS ($1.15) and an adjusted non-GAAP diluted EPS
  ($1.72), each clearly labelled with its own basis by the company itself.**
  This is NOT the edition-38 trap — when the *company's own primary filing*
  discloses both figures with clear labelling, report both; the trap is
  specifically about a *secondary-only* non-GAAP figure presented without a
  stated basis that conflicts with the primary filing. **Edition 41 logged
  two further non-trap confirmations of this same pattern**: both Johnson &
  Johnson (GAAP EPS $0.09 vs. adjusted $2.59, the gap driven by a one-time
  talc-settlement charge and M&A deal costs) and UnitedHealth (GAAP EPS
  $4.56 vs. adjusted $4.69) disclosed both figures clearly in their own
  primary 8-Ks — both reported in full per the Delta precedent, not treated
  as a conflict. **Edition 42 logged two more non-trap confirmations**: Bank
  of America's own 8-K disclosed GAAP EPS $1.08 (hit by a $1.2bn regulatory-
  settlement charge, -$0.17/share) alongside an adjusted EPS of approx.
  $1.25, and the gap was clearly explained by the company itself, not a
  secondary aggregator — reported in full. Morgan Stanley's 8-K did not
  carry a comparable GAAP/adjusted split this quarter (one clean EPS figure,
  $3.03). **Edition 39 also logged a new, distinct trap worth tracking
  separately: an EPS-consensus figure can be genuinely conflicted across
  sources due to a currency/share-basis mismatch, not a GAAP-basis
  mismatch** — TSMC's Oct 15 earnings call consensus showed approx. $4.39
  (USD ADR-equivalent) in one source, a dispersed NT$4.32-4.65 range
  (local-currency, per-ordinary-share) in another, and an apparent outlier
  of $0.88 likely reflecting a raw share-count mismatch in a third. When
  comparing EPS consensus figures across sources, check whether they're
  quoted in the same currency and on the same per-share basis (ADR vs.
  ordinary share, which for TSMC is a 1:5 ratio) before treating a gap as a
  genuine conflict — **TSMC's call itself (Thu 15 Oct, approx. 2:00am ET)
  fell just after edition 42's cutoff; its results and any read-across will
  land inside edition 43's window — watch for this currency/share-basis trap
  then.**
- **Know when to treat a third-party data feed's own internal
  inconsistencies as a data-quality flag rather than a reportable trend.**
  Edition 38's zerogex (dealer-gamma) reads carried a stale-snapshot caveat
  on the SPX page plus two now-resolved one-off anomalies (SPY scale
  discontinuity, conflicting QQQ figures); edition 39 confirmed the SPX
  staleness caveat as a structural, standing limitation. **Edition 40 found
  a harder failure mode on the same source: the direct API call returned
  `{"error":"Authentication required"}`, and the public front-end rendered
  only blank placeholder values with no timestamp at all** — a step beyond
  staleness into total unavailability. Edition 41 confirmed this harder
  failure mode persisted for a second consecutive edition. **Edition 42
  found yet a THIRD distinct failure mode**: the front-end loaded a
  populated page shell (not blank) but every metric was an unresolved
  placeholder dash with no error text, and the API probe returned a plain
  404 rather than the auth-required error — treat zerogex as now carrying
  THREE documented failure modes (stale/timestamp-inconsistent SPX snapshot
  at 38-39; auth-gated blank pages at 40-41; populated-shell placeholder
  dashes at 42), and do not assume any one of them is the fixed baseline —
  the shape of the failure has now changed twice running. SpotGamma remains
  untried as an alternative per standing practice (it has failed for many
  editions).

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied, confirmed again at edition 42. **Editions 28
  through 42 all got a full clean sweep** — fifteen consecutive clean
  sweeps now, every series carrying a same-day `last_trade_time`, verified
  individually per series via a raw `curl`/direct fetch (not a
  tool-summarized fetch) each time, though at edition 42 only the VIX
  series' own JSON was fetched byte-for-byte verbatim — the other five were
  paraphrased by fetch tooling, so a silently-collapsed duplicate
  `prev_day_close` key could not be personally ruled out on those five even
  though the manual percent-recomputation matched cleanly; prefer a raw
  fetch over a tool-summarized one for this endpoint when feasible. Still
  not a guarantee — keep checking `last_trade_time` on each series every
  time. **The feed's two known intermittent bugs (a duplicated
  `prev_day_close`, and a `price_change_percent` that divides by current
  price instead of prior close) were ABSENT again at edition 42** — a third
  consecutive clean edition (40-42) — **and this on the single largest VIX
  move logged all cycle** (VIX +10.48% to 16.87, VIX9D +21.68% to 14.59,
  VVIX +10.62% to 94.45, SKEW +1.65% to 157.30, all driven by the hot
  September CPI print). This continues to confirm the bugs are genuinely
  intermittent, not fixed/eradicated or a monotonic trend. Always compute
  day-over-day % change manually against the previous edition's logged close
  regardless of how many consecutive clean reads preceded the current one.
  The VIX9D-vs-spot-VIX front-end inversion (first flagged edition 28)
  widened to -3.58 at edition 39, narrowed to -3.53 at edition 40, -3.28 at
  edition 41, and **narrowed further to -2.28 at edition 42** — now a third
  consecutive narrowing move, though this time driven by a sharp vol-spike
  session rather than a gentle drift; still not confirmed as a monotonic
  trend, keep watching rather than assuming continuation.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table,
  and (absent fresher CoT data or another dominant story) chart #2. **Edition
  41 again used the sector-ETF-proxy chart #2 default** (5 of 11 sectors
  green: Energy +1.80%, Comm. Svcs +0.74%, Utilities +0.58%, Materials
  +0.57%, Cons. Discretionary +0.08%; Technology -0.04%, Real Estate -0.21%,
  Cons. Staples -0.26%, Industrials -0.28%, Financials -0.42%, Health Care
  -1.35% the six laggards) — no fresh CFTC data was due this window as
  expected. **Stockanalysis.com single-stock pages remain the standing
  default for pinning an exact closing price/% change on any individual
  mover** — editions 26 through 41 (sixteen straight) have all used direct
  fetches to it. Note that a headline wire's own GICS sector-index
  percentages can differ slightly from the SPDR ETF price-change figures (a
  normal index-vs-ETF-price methodology gap); keep using the SPDR ETF
  figures as the table's primary numbers. **Editions 42 through (approx.) 43
  should also default to the sector-ETF-proxy chart #2** — the next CFTC
  report is due Fri 16 Oct, covering Tue 13 Oct data, and will most likely
  land inside the edition covering that Friday session (approx. edition 44
  if the daily cadence holds); check cftc.gov's schedule directly each
  edition rather than assuming the date.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. Editions 38
  through 42 all used the "X of 11 sectors closed higher" sector-ETF read as
  the best available breadth proxy (9 of 11 at edition 39, 8 of 11 at
  edition 40, 5 of 11 at edition 41, 3 of 11 at edition 42 — the lopsided
  CPI-driven defensive-vs-Tech split), consistent with recent editions.
  Continue treating an uncorroborated single-aggregator (or unsourced
  search-summary) breadth figure as not usable — this has recurred enough
  times to treat as a durable, not occasional, gap.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — a recurring failure for many
  editions, not re-attempted at editions 40 through 42 (zerogex tried first
  per standing practice). **zerogex.io changed failure mode a third time at
  edition 42**: after the auth-gated API error / genuinely blank page at
  editions 40-41, edition 42's front-end loaded a populated page shell (not
  blank) but every metric (Net GEX, Γ Flip, Call/Put Wall, Max Pain, P/C)
  was an unresolved placeholder dash with no timestamp or error text, and a
  direct API probe at `/api/gex` returned a plain 404 rather than the
  auth-required error. Still entirely unusable for a third straight edition,
  but **do not assume the auth-gated mode is the fixed baseline** — it has
  now changed shape twice running (40-41 vs. 42). zerogex carries three
  separate documented failure modes on its SPX read (stale/inconsistent
  timestamps at 38-39; auth-gated blank pages at 40-41; populated-shell
  placeholder dashes at 42). The magnitude remains single-sourced (zerogex
  only; SpotGamma still yields no real numbers to cross-check against).
  Minor open item carried forward, still low priority: zerogex's own stated
  wall levels (call/put wall) have still not been cross-checked against a
  secondary options note's implied walls — moot while zerogex itself is
  unusable.
- **Official CME FedWatch probabilities:** the page blocks fetching (edition
  42's direct attempt failed with 429/timeout, same as edition 41's timeout)
  — use secondary citations (Polymarket, Kalshi, Reuters/other economist
  polls, desk notes) and give a range rather than a single invented number.
  Edition 42 again used DeFi Rate's Kalshi/Polymarket-blended aggregator (now
  a stable, consistently-working source across editions 37-42) rather than a
  CME-attributed figure specifically. **A secondary (Seeking Alpha) claim
  attributed 49.3% October-hike odds to CME FedWatch post-CPI at edition
  42 — could not be independently verified, conflicts with DeFi Rate's
  directly-fetched approx. 29%; do not cite without independent
  corroboration.** Keep treating CME FedWatch as needing a disclosed range
  from secondary sources, not a single figure.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, 23-35, 37-42 (not attempted at edition 36) — a confirmed
  structural gap, not transient. The failure mode changed at edition 38 from
  a "Vercel Security Checkpoint" page to a plain HTTP 429 (Too Many
  Requests); edition 41 got a 404 on one URL pattern and a 429 on another;
  **edition 42 again failed with 429/timeout — now the confirmed standing
  failure mode across six consecutive attempts (37-42), not session-to-
  session variance.** Resume the attempt-every-edition discipline at edition
  43 regardless, but expect a block of some kind. Use Kalshi's own secondary
  reporting (its blog, prediction-market news aggregators —
  news.kalshi.com, or DeFi Rate's own Kalshi/Polymarket-blended aggregator,
  which has now worked cleanly at editions 37-42) as the workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has failed many
  editions running; not re-attempted at editions 35 through 42 (went straight
  to the Westmetall fallback per standing practice; edition 42 tried LME.com
  directly anyway and got 403 again). **Westmetall.com has now worked
  cleanly twenty-one editions running** as the fallback (copper +0.07% to
  $14,751.00/tonne cash settlement at edition 42, computed off edition 41's
  logged $14,741.00 base, which matched Westmetall's own current table
  exactly — no reconciliation issue on copper specifically, unlike
  oil/gas this edition). **The oil level-vs-%-change-reconciliation problem
  that has dogged WTI (and occasionally Brent) across editions 35, 37, 38 and
  39 stayed clear for BOTH grades at edition 42** (WTI +0.70%, Brent +0.35%,
  both matching vendor-stated exactly) — a third consecutive clean
  dual-grade reconciliation, though see the Standing Facts/Hard Rules entries
  above for the now-broadened wrinkle (the vendor's retroactively-revised
  Tuesday base hit WTI again, Henry Hub a second time, and for the first
  time EUR/USD, GBP/USD and USD/JPY — a different issue from the
  %-change-vs-level mismatch this guidance originally tracked). Neither oil
  grade rolled at edition 42 (WTI still Nov '26/CLX6, Brent still Dec
  '26/LCOZ6); Henry Hub also has not yet rolled to December (still Nov
  '26/NGX6).
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) has
  historically been preferred since TextView carries a known
  maturity-column mis-mapping bug, but edition 36 found a sharp 33bp
  disagreement between the two specifically on the 2-year. **Both endpoints
  agreed cleanly again at edition 42** (2-yr 4.82%, 10-yr 5.19%, 30-yr
  5.52%, all 14 Oct — curve flattened on the day: 2-yr +3bp, 10-yr -2bp,
  30-yr -4bp, consistent with hawkish front-end repricing on the hot CPI
  meeting risk-off long-end demand), extending the clean streak to seven
  editions (37-42, plus 39's confirmation) with no repeat of the 33bp gap.
  Keep fetching both endpoints and comparing rather than trusting either by
  default.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. Edition 39 pulled fresh data (Friday 9 Oct
  2026, covering Tuesday 6 October): ES OI 1,932,227 (Asset Mgr net +46.93%
  of OI, Leveraged Funds net -21.48%); NQ OI 283,586 (Asset Mgr net +26.03%,
  Leveraged Funds net -6.78%); RTY (full-size) OI 425,152 (Asset Mgr net
  +10.70%, Leveraged Funds net -24.77%). Editions 40 through 42 all
  confirmed via cftc.gov's own release schedule that no new report posted in
  their respective windows (release dates run the 2nd, 9th, 16th, 23rd and
  30th of October, all Fridays) — these edition-39 figures remain the latest
  available. **The next report is due Friday 16 October 2026, 3:30pm ET,
  covering Tuesday 13 October data** — re-confirmed directly against
  cftc.gov's release schedule at edition 42 with no delay notice; check
  again at edition 43 since this is the edition the report should land in.
- **GBP/USD and EUR/USD clean close:** both have now been fully resolved
  since edition 37 (EUR/USD since edition 26). **Edition 42 single-sourced
  both to Investing.com's close-to-close history table again** (GBP/USD
  -0.19%, EUR/USD -0.04%, both computed off the logged Tuesday close) — no
  conflict found, consistent with the lighter-touch approach used since
  edition 39. Note both instruments' logged Tuesday bases had themselves
  drifted slightly from what edition 41 logged (see the broadened
  vendor-revision trap in Standing Facts/Hard Rules) — disclosed, not a
  same-day conflict. Resume the fuller multi-source method if a fresh
  conflict appears, or periodically to re-confirm the lighter method remains
  safe.
- **Gold/silver clean close on a non-event day:** USAGOLD is now a confirmed
  **permanent standing gap** (zero archived Wayback snapshots found at
  edition 39) — not re-attempted since, per the edition 39 recommendation;
  continue not attempting it absent a new URL/method. **Kitco's live spot
  quote broke from Wednesday's futures settlement at edition 42** — not a
  clean secondary-color read this time: on a session where gold and silver
  futures both sold off hard on the hot CPI print (gold -1.06%, silver
  -6.14%), Kitco's own live spot ticker showed both UP (+0.83%/+0.75%),
  contradicting Kitco's own published headlines on the same page ("gold
  falls below $4,100, silver plunges 6%"), which matched the futures move.
  Treated as a mistimed/rebound quote rather than Wednesday's close; this is
  a new, distinct trap (see Hard Rules) from the two prior Kitco failure
  modes (two-edition outage at 38-39, clean reads at 40-41). **Silver's
  spot-vs-futures same-sign check technically broke this edition** (spot
  +0.75% vs. futures -6.14%) but with a plausible, disclosed explanation
  (Kitco's live quote lagging the session's sharp futures move) rather than
  a genuine data-integrity failure — do not treat this as a reopening of the
  edition-31 sign-conflict thread, which remains resolved for the
  close-to-close futures comparison specifically. Gold futures continue to
  source cleanly via Investing.com.
- **China CPI/PPI (monthly):** now resolved for September — see Standing
  Facts above, closed thread. Typically prints on the 9th-10th of the month;
  September's was a 14 October print (9:30am Beijing time), consistent with
  that cadence. **US import/export prices and industrial production:**
  frequently release mid-month on a Mon/Tue — confirm on the BLS/Fed release
  schedule rather than assuming a date; BLS's own schedule gives: **Sept PPI
  Thu 15 Oct 8:30am ET, Import/Export Price Indexes Fri 16 Oct 8:30am ET**
  (re-confirmed again via a direct bls.gov fetch of the dated monthly-
  schedule subpage — `bls.gov/schedule/2026/10_sched_list.htm` — at edition
  42, unchanged for a fourth straight direct re-confirmation; note the
  generic `2026_sched.htm` URL 404's, use the dated monthly-list path),
  **Q3 Employment Cost Index Fri 30 Oct 8:30am ET** (re-confirmed directly at
  edition 42 — note this is a FRIDAY, not Thursday; a subagent miscalculated
  the weekday at edition 42's research pass and this was caught and
  corrected before publication — double-check day-of-week arithmetic on any
  future-dated calendar item rather than trusting a subagent's stated
  weekday). **FOMC minutes from the 15-16 September meeting are a closed
  thread** (see Standing Facts above). **US August 2026 trade deficit (BEA)
  widened to $132.6bn, released Tuesday 6 October** — the headline direction
  is reasonably solid but the precise July baseline used by secondary
  sources was internally inconsistent across outlets and was not resolved;
  not revisited since edition 37. **University of Michigan preliminary
  October consumer sentiment** (see Standing Facts above): 46.3, final
  reading due 23 October 2026 — watch for it.
- **Henry Hub natural gas:** the October contract thread resolved at edition
  32 (final settlement $3.00/MMBtu). The November contract (NGX6) gave its
  cleanest-ever dual-vendor read at edition 38 but that did NOT persist at
  editions 39 through 42 — **edition 42 again single-sourced to
  Investing.com** (NGX6 still front-month, not yet rolled to December;
  $3.289/MMBtu Wednesday). **The vendor-revision wrinkle flagged at edition
  41 got WORSE at edition 42, not better**: the vendor's own historical
  table revised Tuesday's logged close a SECOND time (edition 41 logged
  $3.319; edition 42's fetch showed $3.283), leaving Wednesday's %-change
  genuinely ambiguous between +0.18% (off the newly-revised base) and -0.90%
  (off edition 41's previously-logged base) — the sign itself now flips
  depending on which base is used, not just the magnitude. Both disclosed,
  neither resolved; see the Standing Facts/Hard Rules entries for the
  general "vendor retroactively revises a logged close" trap this
  instantiates, now on its second consecutive recurrence for this specific
  instrument. **Treat the dual-vendor method as genuinely one-off** (only
  edition 38 in five attempts since) — keep testing each edition. Still not
  labeled an official CME settlement print by either vendor.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. Not attempted at editions 33 through
  42 (secondary priority; options-flow colour has instead been sourced from
  dedicated options-flow wires or zerogex's broader snapshot, itself now
  largely unusable). **Edition 42 found no notable Wednesday-dated
  single-stock options-flow/skew commentary for the reporting banks, JNJ,
  UnitedHealth or Fastly** (sixth consecutive empty edition on this general
  sub-item, 37-42) — treat this sub-item as reliably low-yield and keep it a
  brief, secondary effort rather than a sustained search each edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable through edition 42;
  next due approx. 14 November 2026.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22). Not attempted again
  through edition 42.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully
  again at edition 39 (see CFTC CoT entry above); not re-attempted at
  editions 40 through 42 since no new report was due in any of those
  windows. Repeat this full three-instrument fetch whenever a fresh
  CoT-based chart is next used — next due Friday 16 October 2026 (covering
  Tuesday 13 October data) — watching for the Micro-vs-full-size Russell
  naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 37 hit the
  most extreme version (no roundup for any name located at all); edition 38
  a milder version (only the biggest earnings mover had activity); edition 39
  broke that streak with a normal, multi-name result (Goldman/Palantir,
  Cantor Fitzgerald and Barclays/Humana, all with clear dollar price targets
  and dates). **Editions 40 through 42 all reverted to the empty-result end
  of the range**: no dollar-price-target action dated specifically to 12,
  13 or 14 October could be confirmed for any name. The pattern across 37-42
  (empty, thin, normal, empty, empty, empty) is now tilted toward empty but
  still looks genuinely intermittent rather than a structural change —
  report whatever a genuine search attempt turns up each edition, whether
  that's zero, one, or several actions, without treating any single result
  as the new baseline.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29, recurred with milder
  versions through edition 36). Editions 37 through 40 did not hit a new
  instance of this specific trap on any NAMED mover's price in the body.
  **Bumble (BMBL) — RESOLVED at edition 42, closed thread.** Edition 41's
  flagged +56.58% move (priced cleanly via stockanalysis.com but with no
  dated driver and an unconfirmed split-artifact risk) is now fully
  explained: a definitive $1.3bn all-cash acquisition by Ithaca Holdings at
  $6.05/share was announced 13 October 2026 (confirmed via the company's own
  merger-agreement 8-K), with the prior Monday's unexplained +49.61% jump
  also explained by an Oct 12 Reuters report of advanced deal talks.
  Confirmed NOT a stock split (zero historical splits per macrotrends.net).
  This is the model case for the discipline this bullet exists to enforce:
  the move was excluded from the body and flagged in Annex A rather than
  guessed at, and the real explanation surfaced the very next edition. The
  right call when time-constrained remains: corroborate with a second
  source, report the move without the unverified driver, or flag it as
  unverified in Annex A — never invent or infer a plausible-sounding
  explanation to fill the gap.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything** — this
  was refined at edition 39 after the previous fixed-size guidance caused a
  5-page overflow on a high-content-volume edition. Use `(9.8, 1.95)` as the
  ceiling for an 11-category sector-ETF-proxy panel (confirmed clean at
  editions 37 through 41) — this remains correct for 10-11 categories
  specifically. For charts with fewer categories, scale the height down:
  edition 39 used `(9.8, 1.65)` for a 7-category single-stock movers chart
  and `(9.8, 1.85)` for a 3-category grouped (Asset-Manager-vs-Leveraged-
  Funds) CFTC chart; **edition 41 used `(9.8, 1.8)` for an 8-category
  single-stock movers chart**, all visually inspected at full resolution and
  confirmed clean with no label overlap or legend collision. Use
  `font.size 9.6`, dpi 210, `width:100%` in the page. A shorter-category-
  count chart2 (e.g. 7-8 rows, such as a CFTC positioning chart) may still
  need 1.65-1.85in depending on whether it's a simple or grouped bar —
  **always render and visually inspect (via the Read tool) the actual PNG at
  or near full resolution before embedding it**, regardless of what a past
  edition's page-count success might suggest. For a grouped (multi-series)
  bar chart, such as edition 34's and edition 39's CFTC Asset-Manager-vs-
  Leveraged-Funds chart, the simple single-series `barh()` helper in
  `make_charts.py` doesn't apply — use a dedicated `grouped_bar()` function
  instead (vertical offset bars per category, two series, legend below the
  plot via `bbox_to_anchor` with enough negative y-offset and a matching
  `fig.subplots_adjust(bottom=...)` to avoid the legend colliding with the
  x-axis label — this collision was caught and fixed at edition 39
  specifically; don't rely on `tight_layout()` alone for a grouped chart with
  a below-axis legend, it doesn't reserve enough room by default). **A
  distinct label-overlap bug surfaced and was fixed at edition 40, in the
  simple `barh()` helper's default `pad_frac=0.12`:** when the longest bar in
  a chart (the one with the greatest |value|) approaches the computed xlim
  edge, its value-label text (placed just beyond the bar end) can overflow
  past the axis into the margin where the y-axis category tick labels sit,
  visually overlapping them. **Fixed by raising `pad_frac` to `0.26`** at
  edition 40; **edition 41 used `pad_frac=0.24` for both of its charts and
  confirmed clean rendering with no overlap on either**, a further data
  point narrowing the safe range to roughly `0.2-0.26`. Treat
  `pad_frac=0.12` (the script's literal default) as too tight whenever the
  data's max magnitude is large relative to the chart's category-label text
  width (longer tickers/names need more clearance) — `0.2-0.26` is a safer
  starting point, confirmed at editions 40 and 41 across three different
  charts now (single-series 8-category, single-series 11-category); always
  visually inspect the rendered PNG regardless, since the right value still
  depends on label text length and chart width.
- PDF: HTML → Chromium print-to-PDF via Playwright. Launch Chromium with an
  explicit `executablePath` (check the environment for the installed
  Chromium build path) and `--no-sandbox`. Do not run `playwright install`.
- Set margins in **exactly one place** — either the CSS `@page` block or the
  Playwright `page.pdf()` margin option, never both (they stack and double
  the margin). Passing `{top:'1in', bottom:'1in', left:'13mm', right:'13mm'}`
  via `page.pdf()` with the HTML body at `margin:0; padding:0` and no CSS
  `@page` block is the pattern that has worked reliably.
- **Only ONE forced `page-break-before` in the whole document: immediately
  before Annex A.** Let sections 1–6 flow naturally — a stray extra break
  produces a 5-page PDF with a mostly-blank orphan page. `grep -n
  'pagebreak'` before troubleshooting anything else if page count looks
  wrong — check specifically for `<div class="pagebreak">` occurrences (the
  CSS rule definition itself also contains the string "pagebreak," so a raw
  `grep -c` will show 2 for a correctly-built document). A 5-page render is
  not always a stray break — editions 24, 28, 33 and 39 all hit 5 pages with
  only the one correct pagebreak present; the cause was genuine copy
  overflow each time (edition 39's case needed both real content trims AND
  a deliberate CSS tightening, which is the current working baseline). Always
  re-render and re-check the page count after each trim/pad round rather
  than guessing how much is enough. **A large, suspicious blank area at the
  bottom of a page (as opposed to a page that's merely a bit short) is
  usually caused by an atomic block — most often a chart `<img>` — not
  fitting in the remaining space and being pushed whole to the next page,
  leaving the page that precedes it under-filled.** Edition 39 hit this on
  page 1 (the Section 2 movers chart got pushed entirely to page 2, leaving
  roughly 40% of page 1 blank) — the fix was trimming earlier content (the
  disclosure box, mainly) so the chart had room to start and finish on the
  same page as its preceding heading, not a layout bug in the chart itself.
  Check for this specific failure mode (a heading near the bottom of a page
  immediately followed by a large blank area, with the heading's content
  starting fresh on the next page) before assuming a page is simply "short."
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. The Commodities & FX table has split cleanly
  across page boundaries with no repeated header row in multiple recent
  editions (35 through 41) — plain-`<tr>` tables reflow across a page break
  safely; this is expected behavior, not a bug to fix.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  A visibly short page 3 has recurred at editions 25, 28, 32, 36 and 40,
  each needing a genuinely additive fix (never a padding table that just
  repeats an existing table's rows) — edition 40's fix was a new Treasury-
  yield-curve table at the end of Section 4. Editions 37 and 38 both
  rendered clean at 4 pages on the first attempt. **Edition 41 also rendered
  clean at 4 pages on the first attempt**, with page 3 filling naturally
  (bank-earnings detail, macro and commodities prose, and the day-ahead
  table/bullets were enough on their own) — no padding table was needed this
  time, unlike edition 40. Continue checking for both failure modes (short
  page 3, overflow) after every render regardless of recent-edition track
  record.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across editions 40 through
42's very different content volumes (40 needed a padding table to fill page
3, 41 and 42 both filled naturally with no padding needed), treat as the
durable default and only loosen it back toward the old values if a future
edition renders with noticeably excessive whitespace at these settings)
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
- Annex A: two columns at 7.1pt, `break-inside:avoid` per `li` (left-aligned
  — reads cleanly at this width; justify only if it still looks clean after
  testing).
- Annex B: three columns at 5.5pt, left-aligned.
- Content budget: 60-second read (5 items); equities as the largest block
  plus the movers table; macro/commodities/derivatives tighter; **a "This
  week's known catalysts" table plus a "Sector setup we take into [session]"
  bullet list at the end of Section 6 by default** for any single-session or
  weekend-window edition (skip only if a multi-session catch-up already fills
  3 pages). **An optional "Commodities & FX levels" table (~9-10 rows, not
  more)** at the end of Section 4 is available as padding if page 3 runs
  short after the two default blocks — reach for it only when content alone
  doesn't fill the page. Needed at editions 25, 28, 36 and 40 (36 and 40 both
  via a Treasury yield-curve table variant); not needed at most other
  editions, including 34, 35, 37, 38, **41 and 42** (42's page 3 filled
  naturally from genuine content volume — the commodities/FX table plus
  derivatives and day-ahead prose were enough on their own, no padding
  needed for a second straight edition). Always re-render immediately after
  adding (or removing) any content to confirm the page count, rather than
  assuming a change is safe. **If a future edition is short on page 3 at the
  tightened CSS baseline, the first lever to pull is adding genuine content
  (the padding table above), not loosening the CSS — only loosen the CSS if
  several consecutive editions all run short, suggesting the tightening
  overshot.**

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across seventeen eligible
editions, 25 through 42, with editions 34 and 39 the exceptions when fresher
CFTC data was available). Fresh CFTC CoT data on a Monday/weekend-window
edition → the ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart,
normalized as % of open interest — this has now happened twice (edition 34,
edition 39); editions 35 through 38 and 40 through 42 all had no fresh CoT
data due and correctly reverted to the sector-ETF-proxy default (edition 42:
Health Care +2.53% led, Technology -2.98% lagged, 3 of 11 sectors green — a
much sharper, more lopsided rotation than edition 41's 5-of-11 split, driven
by the CPI-triggered defensive-vs-Tech divergence). **Edition 43 should
default to the sector-ETF-proxy chart too** (the next CFTC report, due Fri
16 Oct covering Tue 13 Oct data, should land inside edition 43's window per
cftc.gov's own schedule — re-check CoT freshness first before assuming
either chart type by default). A single dominant earnings print with a
clean, well-sourced implied-vs-realized-move story → a three-bar implied/
historical-average/realized move chart (the historical-average leg has never
actually been sourced successfully). A genuine multi-sector broadening/
deepening selloff across consecutive sessions → the sector-ETF proxy
rendered as a grouped (day-over-day) bar instead of single-day. A holiday-
window preview edition with no fresher data → VIX futures term structure
with event annotations. When chart 1 (movers) already covers the earnings/
single-name story, the sector proxy (or, when fresh, the CFTC positioning
chart) is a good complementary choice even on a stock-heavy day, since the
two stories reinforce rather than duplicate each other — **edition 39 used
a dominant single-stock/sector story (SpaceX spectrum deal, telecom/tower
REITs) for chart 1 and the CFTC positioning data for chart 2, which worked
well as genuinely independent, complementary stories; editions 41 and 42
both used earnings/single-stock-driven movers for chart 1 and the
sector-ETF proxy for chart 2, a similarly complementary pairing each time
since the sector chart told a broader structural story (defensive rotation,
AI-capex stress) than the earnings-specific movers alone.** Chart #2's
placement in the document should follow its content, not a fixed section —
editions 24, 34 and 39 all placed a CFTC/positioning chart #2 in Section 5
(Derivatives) rather than Section 2; editions 35 through 42, all back on the
sector-proxy default, placed it back in its usual Section 2 spot. Continue
checking CoT freshness first each Monday/weekend-window edition rather than
assuming either chart type is now the permanent default for that edition
type. **Remember the figsize-scales-to-category-count guidance above
(ceiling `(9.8, 1.95)` for an 11-category panel, scale down for fewer
categories) regardless of which chart type is chosen.**

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–40 (condensed):** established the format (edition 1 baseline;
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
15-16 FOMC meeting and its aftermath (editions 21-23):** S&P 7,585.73
pre-decision; the Fed hiked 25bp to 3.75%-4.00% unanimous 12-0, equities
reversed hard (S&P 7,551.81, 10-year first closed above 5% since 2007); then
a sharp relief rally (S&P 7,637.76 +1.1%), BoE held at 3.75% (6-3). Edition
24 (triple witching + weekend): approx. $7tn September triple-witching
notional expired, Xenon Pharmaceuticals -30.7%, Buffett stepped down as
Berkshire chairman, BoJ hiked to approx. 1.25% (31-year high). Edition 25: a
broad chip rally pushed Nasdaq to a then-record 27,122.09; quarterly index
rebalances took effect. Edition 26: financials-led rotation, Viking
Therapeutics +35.67%, a genuine Kitco-vs-USAGOLD gold split (later
resolved). Edition 27: risk-off on a 19-year 10-year yield high, the "Meta
Muse" AI-agent theme rotated from banks into online travel names, VIX 15.18.
Edition 28: a whipsaw near-flat session, MGM Resorts -10.99% on a withdrawn
take-private bid, the Trump-Xi summit extended the US-China trade truce.
Edition 29: a relief rally, Meta -3.33% on the Cambridge Analytica verdict,
the US-China $30bn tariff-cut agreement first reported, zerogex's first
anomalous gamma jump. Edition 30: broad risk-off on a rejected Iran Hormuz
offer, Kodiak Sciences +177.96% (the movers-chart capping rule's first
genuine case), MongoDB -18.46%. Edition 31: DXY-vs-FX-crosses conflict
resolved cleanly; zerogex -$17.19bn. Edition 32: a volatile round-trip
close, Liquidia -57.19%, Micron beat with a muted AH reaction, gold
spot/futures split (later converged). Edition 33: yields (not equities)
drove the session on a hot ISM Prices Paid print, Accenture +15.78% and
Synopsys +12.78% led an AI-infra earnings cluster, Nike missed FQ1 guidance
(resolved edition 34); the document overflowed to 5 pages, needing five trim
rounds. Edition 34 (Mon 5 Oct, covering Fri 2 Oct + weekend): a badly-missed
September jobs report (nonfarm payrolls +29,000) drove a broad risk-on
rally and a sharp October-hike-odds collapse (to approx. 17-21.6%); S&P 500
+0.73% to 7,722.72; a fresh CFTC CoT report gave the first fully-consistent
ES/NQ/RTY OI normalization, powering a CFTC-positioning chart #2; zerogex
flipped decisively positive (+$22.96bn from -$11.58bn). Edition 35 (Tue 6
Oct, covering Mon 5 Oct): two same-day cash buyouts drove the tape
(Schneider Electric/PTC Inc, C.H. Robinson/RXO Inc) — PTC +33.49%, RXO
+22.54%; equities extended Friday's rally to a Nasdaq Composite record
(27,477.31); September's ISM Services PMI printed 54.9% with a hot 74.0%
Prices Paid sub-index driving the 10-year to a fresh 24-year high near
5.35%; two new sourcing traps logged (stale Nike price-target recirculation,
the Paramount Skydance stock-split "+96%" artifact); zerogex roughly doubled
to +$46.35bn. Edition 36 (Wed 7 Oct, covering Tue 6 Oct): equities extended
Monday's rally to fresh records with no single dominant catalyst (S&P 500
+0.58% to 7,818.93, Nasdaq +0.45% to 27,599.79, Dow +0.49% to 51,521.28) on
falling yields driving a clean rate-sensitive rotation (Utilities +2.98%
led, ten of eleven sectors green), though Russell 2000 bucked the trend
(-0.59%); Constellation Energy +12.25% on a reported Google nuclear PPA
(terms unconfirmed), AMD +2.80% to a fresh all-time high; two severe
sourcing traps hit (fabricated AMD price targets from a tool-summarized
fetch, an unverifiable "WHO" claim cited as the Novavax/Moderna driver,
both rejected); the Paramount Skydance/Warner Bros. Discovery $110bn merger
closed, renaming to Skydance Corporation under ticker SKYD with no reliable
same-day % figure obtainable given the ticker change (resolved the next
session); a secondary source reversed the US-China tariff list-size
assignment (resolved edition 37); the 2-year Treasury hit a 33bp
cross-endpoint gap (resolved edition 37); GBP/USD hit a genuine three-way
conflict (resolved edition 37); zerogex's SPX gamma hit a third consecutive
sharp step-up to +$74.26bn (reversed edition 37); BoJ's primary PDF was
located but unparseable by fetch tooling for a second straight edition
(resolved edition 37 via local text-extraction). Edition 37 (Thu 8 Oct,
covering Wed 7 Oct): the FOMC minutes (released 2:00pm ET inside the window)
showed a unanimous 12-0 September hike but only "most" not "all" backing a
further 2026 move; equities retreated broadly on a bond-market selloff (S&P
500 -0.2% to 7,801.77, Dow -0.7%, Nasdaq -0.2%, Russell -1.3%), Industrials
led losses on an unexplained Caterpillar -5.75% (driver resolved edition 38);
Skydance Corporation's first clean post-transition close under ticker SKYD
was -6.72%; Applied Digital -6.04% intraday ahead of an after-the-close
fiscal Q1 beat (revenue +322% y/y); the AI-optics trade (AAOI, COHR, LITE)
reversed Tuesday's rally with no fresh catalyst found; a primary-source
breakthrough on the Bank of Japan (local `pdftotext` extraction) revealed
the Sept 18 hike passed 7-2, not unanimous, with two named dissenters; three
standing conflicts were all resolved this edition (US-China tariff
list-size, the 2-year Treasury's 33bp gap, GBP/USD's three-way conflict);
WTI and Brent both hit a sharp level-vs-%-change reconciliation failure
across three independent vendors; a genuine chart-layout bug was found and
fixed (panel2's figsize bumped from `(9.8, 1.55)` to `(9.8, 1.95)` after
overlapping y-axis labels were caught on visual inspection). Edition 38 (Fri
9 Oct, covering Thu 8 Oct): equities fell a second straight session but
breadth stayed strong (S&P 500 -0.5% to 7,765.36, Dow +0.1% to 51,231.64 the
only major average higher, Nasdaq -1.3% to 27,193.34, Russell flat +0.03%);
a second straight session of AI-optics profit-taking (AAOI -13.58%, COHR
-9.63%, LITE -5.62%) was the main drag; Caterpillar's Wednesday -5.75%
mystery resolved (FTC/USDA farm-equipment antitrust inquiry); Applied
Digital's blowout fiscal Q1 print drew a muted reaction and logged the
first non-GAAP-vs-GAAP EPS conflict trap (a secondary "+1¢" figure excluded
in favor of the 8-K's GAAP loss); the first post-FOMC-minutes hike-odds read
showed approx. 16-17% Oct, essentially unchanged; Kalshi's failure mode
changed from a Vercel checkpoint page to a plain HTTP 429; a primary-source
breakthrough closed BoJ's last standing gap (next meeting Oct 29-30, direct
fetch); oil's vendor-%-reconciliation failure became a well-established
durable pattern; zerogex logged three within-session anomalies (stale SPX
snapshot, SPY scale discontinuity, QQQ conflict) as a new data-quality trap,
two of which (SPY, QQQ) later proved to be one-offs. 28 sources, clean
28/28 on the second `check_refs.py` pass, zero stray tildes, clean 4-page
render on the first attempt. Edition 39 (Mon 12 Oct, covering Fri 9 Oct +
weekend): SpaceX's approx. $8bn purchase of Grain Management's 800MHz
spectrum for Starlink Mobile rattled telecom (T-Mobile -13.27%, AT&T
-9.81%, Verizon -8.75%, Crown Castle +15.60%), but equities shrugged it off,
closing a record-setting week: S&P 500 +0.6% to 7,811.54, Dow +0.8% to
51,654.95, Nasdaq Composite +0.6% to 27,366.17, Russell 2000 +0.5% to
2,806.98, 9 of 11 sectors green. A parallel broad biotech rally ran
alongside it (Moderna +14.21% on joining the Nasdaq-100, Novavax +15.80%,
Humana +11.56%); Fastly (+15.86%) and a second unexplained AI-optics session
(AAOI/COHR/LITE) both remained open threads. Delta's 8-K cleanly disclosed
both GAAP ($1.15) and adjusted ($1.72) EPS alongside a guidance cut; Goldman
upgraded Palantir to Buy, the first normal analyst-action result after two
near-empty editions. Standing facts all re-verified unchanged; October-hike
odds flat at approx. 16%/Dec 73-74%; China Sept CPI/PPI still pending, with
an unverified Golden-Week-delay hypothesis surfacing. Oil, gold spot, silver
spot, DXY and Henry Hub all needed the logged-prior-close computation
method; USAGOLD confirmed a permanent dead end via the Wayback Machine's
Availability API; Kitco failed for the first time in many editions. CBOE's
two known bugs resurfaced after four clean editions; VIX9D-VIX inversion
widened back to -3.58; zerogex's SPX stale-snapshot caveat recurred for a
second edition; CFTC CoT posted fresh data for the first time since edition
34 (ES/NQ/RTY), powering a Section-5-placed positioning chart; SOFR 3.87%
(Oct 8). A chart-sizing refinement (figsize scaling to category count) and
a deliberate CSS retightening were needed to fix a genuine 5-page overflow
across six render-and-inspect rounds. 42 sources, clean 42/42 on
`check_refs.py` after two Annex-B-only additions were caught and given
inline citations, zero stray tildes. **Edition 40** (Tue 13 Oct, covering Mon
12 Oct, Columbus Day — equities traded, Treasury/SOFR closed): a value/growth
split (Dow +0.38% to a record 51,850.55 vs. Nasdaq -0.44%) on renewed
memory-chip/AI-hardware weakness (Micron, Sandisk, Marvell, Cerebras, Semtech,
Ciena, Lumentum, AAOI, Coherent all down hard, drivers resolved edition 41);
AP's wire needed search-snippet recovery after 403s; oil delivered its
cleanest-ever dual-grade reconciliation (later found to rest on a Monday base
that was itself retroactively revised, per edition 41); zerogex's SPX gamma
hit a harder auth-gated/blank failure mode than its prior staleness caveat; a
chart-label pad_frac bug (`0.12` too tight) was found and fixed by raising to
`0.26`; a short-page-3 recurrence was fixed with a new Treasury-yield-curve
table. 34 sources, clean 34/34, zero tildes, clean 4-page render.

**Edition 41 (condensed)** — Wednesday 14 October 2026, covering Tuesday 13
October 2026, the opening day of Q3 bank/healthcare earnings season. Equities
finished essentially flat (S&P 500 -0.02% to 7,805.45, Dow -0.35%, Nasdaq
-0.15%, Russell -0.40%) via a clean AP wire recovered through two syndication
mirrors. Four banks plus JNJ and UNH reported before the open: JPMorgan EPS
$5.57 (appeared to trail preview consensus, unconfirmed by a dated article,
stock -0.86%); Goldman Sachs EPS $17.01 (clean beat, -0.23%); Wells Fargo EPS
$1.87 (beat yet -3.10%, provision for credit losses +51% y/y); Citigroup EPS
$2.85 (beat yet -5.60%, provision approx. $2.6bn); UnitedHealth beat and
raised FY26 guidance (flat -0.20%); Johnson & Johnson's GAAP EPS collapsed to
$0.09 on a one-time talc-settlement charge (-5.73%, the day's biggest
large-cap decliner) while adjusted EPS ($2.59) and raised sales guidance were
both disclosed cleanly in the same 8-K. A correction was issued to edition
40's day-ahead note: Bank of America and Morgan Stanley actually report
Wednesday 14 October, not Tuesday. Bumble jumped +56.58% to $5.95 with no
dated driver found (resolved edition 42: a $1.3bn Ithaca Holdings buyout).
The AI-optics/AI-hardware selloff cluster (AAOI, COHR, LITE, CIEN, Cerebras,
Semtech) finally found a delayed driver (Broadcom CEO Hock Tan's remarks on
AI-infrastructure capital-access constraints); Fastly alone remained
unexplained for a third session. Standing facts re-verified clean across the
board; rate-path odds drifted modestly hawkish for a third straight edition
(approx. 19% Oct/75-77% Dec); China's Sept CPI/PPI release date was pinned to
14 Oct but the print itself hadn't posted yet. Commodities/FX mostly
reconciled cleanly except a new "vendor retroactively revises a logged
close" trap hit WTI, Brent and Henry Hub (Monday's base quietly revised).
CBOE's feed gave a clean sweep (VIX 15.27 +0.39%); zerogex's SPX gamma
stayed in the hard auth-gated/blank failure mode for a second edition. 49
sources, clean 49/49 on the first `check_refs.py` pass, zero stray tildes,
clean 4-page render.

**Edition 42 (most recent — full detail)** — Thursday 15 October 2026 report
covering Wednesday 14 October 2026, the window's one NYSE session, research
window Tue 13 Oct 2026 20:00 ET through Wed 14 Oct 2026 20:20 ET. Verified
the two structural header rules again — now clean across ten (date-line) and
fourteen (window-line) consecutive applicable editions respectively.

**September CPI printed hot and dominated the session**: headline +0.6% m/m
/ +3.7% y/y, core +0.3% m/m / +2.6% y/y, both above the approx. 3.6%/2.5%
consensus, confirmed directly against bls.gov. It triggered the broadest
risk-off session in weeks — S&P 500 -1.11% to 7,718.94, Nasdaq Composite
-1.88% to 26,692.87, Russell 2000 -1.90% to 2,729.53 — but the Dow held
almost flat (-0.09% to 51,621.48) on a sharp defensive rotation: Health Care
(XLV +2.53%) and Consumer Staples (XLP +2.22%) led, Technology (XLK -2.98%)
lagged, only 3 of 11 sectors closed green. AP's wire again returned HTTP 403;
the closes were recovered via CNBC's live wrap and a Yahoo Finance/TheStreet
recap, cross-checked against SPY and reconciled arithmetically against
Tuesday's logged closes. Bank earnings diverged: Bank of America's GAAP EPS
fell to $1.08 on a $1.2bn regulatory-settlement charge (adjusted approx.
$1.25, both disclosed by the company) and the stock fell -4.76%; Morgan
Stanley beat cleanly on both EPS ($3.03) and revenue ($20.3bn) yet still fell
-2.75% with the broad market. CoreWeave (-15.46%) and Oracle (-8.83%) led
single-stock decliners on a renewed AI-infrastructure-funding-stress theme;
Fastly (-7.72%) and GE Vernova (-6.20%) both remained unexplained. **Bumble's
mystery move resolved**: a definitive $1.3bn all-cash buyout by Ithaca
Holdings at $6.05/share, confirmed via the company's own merger-agreement
8-K — not a stock split. No analyst action dated specifically to 14 October
was found for any name.

Rate-path odds repriced sharply hawkish on the CPI print: DeFi Rate's fresh
snapshot (7:06pm ET) showed October hike odds approx. 29% (up from Tuesday's
approx. 19%), December little-changed near 78%. A conflicting Seeking
Alpha claim of 49.3% (attributed to CME FedWatch) could not be verified and
is disclosed as unconfirmed. **China's September CPI/PPI finally posted**
(CPI +0.9% y/y, PPI +5.0% y/y, the fastest PPI rise since June 2022) via
gov.cn's English NBS-sourced release — direct stats.gov.cn access failed
again. The US shutdown/funding re-confirmation regressed to secondary-only
corroboration this edition (still funded through 11 Dec, status unchanged,
method weaker). Commodities swung hard: silver futures -6.14% (the sharpest
single-session commodity move logged by this report in recent editions),
gold futures -1.06%, both contradicted by a mistimed Kitco live spot quote
that itself conflicted with Kitco's own published headlines — a new,
distinct sourcing trap. The Treasury curve flattened (2-yr +3bp to 4.82%,
10-yr -2bp to 5.19%, 30-yr -4bp to 5.52%). The "vendor retroactively revises
a logged close" trap broadened further: WTI's and Henry Hub's Tuesday bases
were both revised AGAIN (Henry Hub's ambiguity got worse, now flipping
sign), and for the first time hit FX (EUR/USD, GBP/USD, USD/JPY all drifted,
USD/JPY materially). The DXY-vs-USD/JPY divergence pattern resumed after a
3-session pause. The VIX complex spiked hard (VIX +10.48% to 16.87, VIX9D
+21.68%, VVIX +10.62%) with neither CBOE feed bug recurring despite the
large move. zerogex hit a third, distinct failure mode (populated page shell,
all-placeholder values, no error text) — now three different failure modes
logged across three editions. CFTC CoT confirmed no fresh data as expected
(next due Fri 16 Oct, should land inside edition 43's window). 49 sources,
clean 47/49 on the first `check_refs.py` pass (two Annex-B-only orphans
caught and given inline citations before render), zero stray tildes, clean
4-page render on the first attempt with both charts rendering cleanly at
`(9.8, 1.8)`/`(9.8, 1.95)`, `pad_frac=0.24`.

**Open threads for edition 43:** Fastly remains unexplained for a FOURTH
consecutive session — the longest-running unexplained-mover thread this
report has carried; keep searching for a delayed driver. GE Vernova's
-6.20% Wednesday move also needs a delayed-driver check. TSMC's Q3 earnings
call (Thu 15 Oct, approx. 2:00am ET) fell just after this edition's cutoff —
its results and the currency/share-basis consensus-mismatch risk flagged at
edition 39 will land inside edition 43's window. The next CFTC CoT report
(Fri 16 Oct, covering Tue 13 Oct) should also land inside edition 43 —
check cftc.gov first thing and expect to finally pull fresh data, ending the
sector-ETF-proxy chart #2 default's run (confirm CoT freshness before
assuming either chart type). September PPI (Thu 15 Oct) and import/export
price indexes (Fri 16 Oct) are the week's remaining scheduled macro prints —
watch for any further rate-path-odds movement after CPI's sharp repricing.
The shutdown/funding status re-confirmation regressed to secondary-only this
edition — attempt a genuine direct whitehouse.gov hit again at edition 43.
JPMorgan's EPS-vs-consensus "miss" framing and the Wells Fargo/Citigroup
credit-provision selloff rationale remain unconfirmed disclosed inferences
for a second edition running, now with a competing yield-driven explanation
also unconfirmed — keep searching for a dated article that resolves either.
The Seeking Alpha 49.3% CME FedWatch claim remains unverified against the
directly-fetched DeFi Rate figure — don't cite it without independent
corroboration. zerogex's failure mode has now changed shape twice running
(auth-gated/blank at 40-41, populated-shell placeholders at 42) — watch
whether it stabilizes or changes again. The FOMC's exact decision/
press-conference time (2:30pm ET, 28 Oct) was not re-displayed on the Fed's
calendar page this pass — re-confirm directly next edition. University of
Michigan's final October consumer-sentiment reading is due 23 October. The
New Mexico v. Meta penalty ruling (expected approx. 22 Oct) remains a
flagged catalyst, not yet revisited. Threads closed after resolution rather
than carried further: China's September CPI/PPI (closed, both figures now
in hand); Bumble's unexplained rally (closed, a confirmed M&A deal, not a
split); the silver same-sign-conflict reopening (closed, explained by a
mistimed Kitco spot quote, not a genuine data failure).
