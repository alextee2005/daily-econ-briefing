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
  through 39 have all applied this correctly** ("Friday 2 October 2026,"
  "Monday 5 October 2026," "Tuesday 6 October 2026," "Wednesday 7 October
  2026," "Thursday 8 October 2026," "Friday 9 October 2026" and "Monday 12
  October 2026" respectively as the date line, with the window line carrying
  the session(s) covered) — now confirmed stable across seven consecutive
  editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 39 all reused the
  same pattern for single-session (or single-session-plus-weekend) windows —
  now confirmed clean across eleven consecutive editions (29 through 39). No
  further confirmation needed; treat this as settled.

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
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 39
  directly against federalreserve.gov's own FOMC calendar page — now under
  three weeks out, continue re-confirming every edition until then. Decision
  and press conference both land 28 Oct, 2:30pm ET. The following meeting is
  December 8-9, 2026 (an SEP meeting).
- **October-hike odds — re-confirmed again at edition 39, still essentially
  flat:** DeFi Rate's Kalshi/Polymarket-blended aggregator, snapshot Sunday 11
  Oct 2026 approx. 7:59pm ET, shows **October 27-28 hike odds approx. 16%**
  (hold approx. 84%, cut approx. 2%; Kalshi approx. 15.5¢, Polymarket approx.
  16.5¢) and **December 8-9 hike odds approx. 73-74%** — materially unchanged
  from edition 38's first post-minutes read (approx. 16-17% Oct / approx.
  74-76% Dec). Three straight editions (37, 38, 39) now show this range
  holding steady post-minutes; treat as a settled near-term baseline, but keep
  refreshing the snapshot every edition since a CPI surprise (Sept CPI due 14
  Oct) could move it. The composite "at least one more hike in 2026" read was
  not freshly re-pulled at edition 39 (last known approx. 80%, edition 38) —
  don't cite without a fresh pull.
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
  processes for actual implementation — edition 39 searched again for a
  Federal Register/USTR implementation notice specifically and found none
  (only unrelated routine Section 301 product-exclusion conforming
  amendments) — watch for a formal implementation/effective date in a future
  edition. The two whitehouse.gov PDF copies carrying different dates (Sept 23
  vs Sept 27, 2026) remains an unresolved minor wrinkle, not worth chasing
  unless load-bearing.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch,
  rba.gov.au, etc.) every edition, exactly like any other data point. Edition
  39 re-confirmed Kevin Warsh as Fed Chair directly against
  federalreserve.gov's Board of Governors bios page — **a ninth straight
  direct re-confirmation.** The BoE's next decision (Thursday 5 November) was
  freshly re-touched at edition 39 via a direct bankofengland.co.uk fetch
  (deprioritized at edition 38, resumed now that the meeting is inside a
  roughly 3.5-week window) — unchanged. The shutdown/CR primary-source
  lapse flagged at edition 38 (two editions running on secondaries only) was
  **closed at edition 39 via a genuine direct whitehouse.gov fetch** — the
  working technique: the generic `/briefing-room/` and
  `/briefing-room/statements-releases/` index pages do **not** surface the
  H.R. 6500 statement; the dated permalink
  (`whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500/`)
  does. Use the dated-permalink approach directly next time rather than the
  generic index pages. **The BoJ's next-meeting-date primary source was
  re-confirmed a second consecutive time at edition 39** via
  boj.or.jp/en/mopo/mpmsche_minu/index.htm, again on the first attempt (no
  local-PDF-extraction workaround needed) — confirms October 29-30, 2026,
  followed by a Summary of Opinions November 10 and the October meeting's
  minutes December 23. This BoJ gap is now closed and stable across two
  straight direct re-confirmations (38, 39); routine re-touch each edition
  going forward, no special effort needed.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed directly at
  edition 39 (following decision 17 December 2026). Resume the direct-fetch
  discipline every edition from here given the meeting is now inside a
  roughly 3.5-week window.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano), both primary-sourced as of edition 37 — closed thread, do
  not re-derive. **The next policy meeting date (Oct 29-30, 2026) is now
  primary-sourced for a second consecutive edition (38, 39)** — this thread is
  fully closed and stable. No further action needed on BoJ facts unless a new
  meeting/decision supersedes the above.
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
- **No US federal government shutdown is in effect — re-confirmed at edition
  39 via a genuine direct whitehouse.gov fetch** (briefing statement on H.R.
  6500, the Continuing Appropriations and Extensions Act, 2027): signed into
  law 2 September 2026, funds the government through **11 December 2026**.
  This closes the primary-source lapse flagged at edition 38 (which had used
  two independent secondaries, AACOM/ASAHP, instead) — see the general
  principle entry above for the working URL pattern. Watch for shutdown risk
  resurfacing as 11 December 2026 approaches.
- **University of Michigan preliminary October 2026 consumer sentiment — new
  this edition, not yet a "closed thread," watch for the final reading:**
  46.3, a five-month low (current conditions 44.7, expectations 47.3,
  year-ahead inflation expectations 4.7% from 4.6%, long-run 3.5% from 3.4%),
  confirmed via investinglive.com and advisorperspectives.com (dshort), both
  dated 9 Oct 2026. Consensus estimates disagreed sharply across outlets
  (approx. 47.6-50.5) — no single consensus figure should be cited without
  disclosing the range. **Final October reading due 23 October 2026** — watch
  for it.
- **China September 2026 CPI/PPI — still open as of edition 39's cutoff, now
  with a partially strengthened (but still unconfirmed) release-date
  estimate:** a direct fetch of stats.gov.cn's latest-releases page (checked
  again at edition 39) still showed August data only (+0.8% y/y CPI, +3.8%
  y/y PPI, both dated 9 Sept 2026) and did not forward-list a September
  release date; a deeper `/sj/zxfb/202610/` subpage attempt 403'd. One
  secondary source (financecalendar.com) continues to claim **14 October
  2026**. Edition 39's research turned up a plausible explanation for why
  September specifically (unlike other months) might land later than the
  usual 9th-10th pattern — National Day Golden Week (1-7 Oct) historically
  pushes NBS's September release later (reportedly 13 October in both 2023
  and 2024) — but this was NOT independently verified against a dated primary
  or near-primary source this edition and should **not** be cited as fact
  without first finding a citable source for it; treat it as a working
  hypothesis that raises the plausibility of the 14 Oct secondary estimate,
  not as confirmation. **Check stats.gov.cn directly again at edition 40**
  (and try to source the Golden-Week-delay pattern properly if it recurs as a
  live question) rather than assuming either date.

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
  uniqueness of use (editions 33-39 have all done this for stockanalysis.com
  single-stock closes and other repeatedly-used outlets, confirmed stable
  across seven editions).
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart 2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes). **Chart
  placement is editorial, not fixed to Section 2** — edition 24, edition 34
  and **edition 39** all placed a CFTC-positioning chart #2 in Section 5
  (Derivatives) rather than Section 2, since that's where the content
  actually belongs. Editions 35 through 38 reverted to the sector-ETF-proxy
  default (no fresh CoT data due in any of those editions) and kept it in
  its default Section 2 placement. **Edition 40 should revert to the
  sector-ETF-proxy default** (no fresh CoT data due until Friday 16 October,
  covering Tuesday 13 October) unless that report has already landed inside
  edition 40's window.
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
  **Editions 27 through 39 are all clean counter-examples worth keeping in
  mind**: all thirteen posted a usable AP wire eventually — editions 38 and
  **39** both needed a syndication mirror (La Nación) rather than a direct
  AP fetch, still a clean, dated, directly-attributable AP figure each time.
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
  Always check a dated article's own body text against the logged
  prior-session figures before trusting its date stamp, regardless of which
  outlet it is. A same-day close and a next-day after-hours-triggered move
  can legitimately combine into one large single-day % change — edition 24's
  Xenon Pharmaceuticals -30.7% Friday move is the reference example. Check
  whether a headline % move is measured close-to-close before assuming two
  reports conflict. **The intraday-vs-close divergence trap is still very
  much alive**, caught across many editions (Worthington, Paychex/Cracker
  Barrel, Oracle, Akamai, STX/WDC/SNDK, MongoDB, Liquidia, Concentrix,
  Citigroup options-wire, Nike, SPCX). **Edition 39 added two more names to
  this list**: Moderna (a secondary source's intraday magnitude of approx.
  8-11% didn't reconcile with the +14.21% close — disclosed, not resolved)
  and AST SpaceMobile (a secondary source's -13.6%/$49.20 figure didn't
  reconcile with stockanalysis.com's -10.48% close — the latter used as
  authoritative). Resolved the same way as always: treat the
  stockanalysis.com (or equivalent timestamped) close as authoritative, and
  disclose explicitly when an earlier-session figure doesn't match the
  close. **A distinct corporate-action (stock-split) data artifact trap was
  first logged at edition 35** (Paramount Skydance's spurious "+96%"
  premarket figure, actually a 2-for-1 split artifact) — before reporting any
  single-stock move that looks like an outright magnitude error (roughly
  doubling, halving, or near-100%), check for a split/reverse-split/listing
  change and exclude the figure if a stale unadjusted-quote explanation fits.
  **A related but distinct ticker-change trap recurred at edition 36-37**:
  when Paramount Skydance/Warner Bros. Discovery's $110bn merger closed
  Tuesday 6 Oct and the surviving entity moved to ticker SKYD, no reliable
  same-day % figure was obtainable on the transition day itself (edition 36,
  correctly left unreported) — but **by the very next session (edition 37),
  stockanalysis.com had a clean, exchange-timestamped close under the new
  ticker (SKYD $8.89, -6.72%)**, fully resolvable. **General technique worth
  keeping: when a ticker-change/listing-transition makes the transition day
  itself unsourceable, don't force it — but re-check the new ticker on the
  very next session, since the gap is often transition-day-only, not
  durable.** **A distinct "driver not found same-session" pattern recurred at
  edition 37→38: Caterpillar's Wednesday -5.75% move had no corroborated
  driver at edition 37's cutoff, but a dated FTC/USDA farm-equipment-inquiry
  article (published Wednesday, simply not yet indexed/discoverable within
  edition 37's research window) fully explained it by edition 38.** **Edition
  39 hit two fresh instances of this same pattern that remain OPEN, not yet
  resolved: a second consecutive session of unexplained AI-optics moves
  (AAOI +3.53%, COHR +3.40%, LITE +5.22%, rebounding Friday with no fresh
  catalyst found) and Fastly's +15.86% move with literally no driver found
  at all despite a real search attempt.** General technique worth keeping
  alongside the ticker-transition one above: when a same-day mover's driver
  can't be found despite a real search attempt, don't force a guess — report
  the move without a driver and explicitly flag it as an open thread, then
  re-search for a delayed explanation at the very next edition before
  assuming none exists. **Check AAOI/COHR/LITE and FSLY again at edition 40
  for a delayed explanation.**
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. **Similarly, a price level can be correct while a vendor's stated
  %-change is wrong** if the vendor used a different prior-day base — always
  sanity-check that a stated price and stated % change reconcile
  arithmetically against the prior session's logged close. This exact pattern
  has now recurred repeatedly on oil specifically (editions 35, 37, 38, and
  again, though more mildly, at **39**: WTI's vendor-stated base still didn't
  match the logged prior close, but **Brent reconciled cleanly at edition 39,
  the first clean Brent reconciliation in this run of editions** — treat the
  pattern as WTI-specific going forward rather than assuming it always hits
  both grades together). **Edition 39 additionally found the same
  vendor-%-vs-computed-%change gap, in milder form, on gold spot (vendor
  +1.44% vs. computed +1.19%), silver spot (vendor +2.44% vs. computed
  +2.29%) and DXY (vendor +0.07% vs. computed +0.11%) — this is the first
  time the pattern has appeared this broadly across multiple commodities/FX
  instruments in one edition, not just oil.** Broaden the standing guidance
  accordingly: **compute every commodity and FX %-change directly off this
  report's own logged prior close, every edition, for every instrument, not
  just oil and not just when something looks surprising** — disclose the
  method explicitly in the text (edition 39 marked these with a `*` and a
  footnote). The oil contract-month-roll trap (Brent Nov-to-Dec) remains
  resolved; not re-checked at edition 39 (no roll due). The CBOE vol-complex
  feed's two documented bugs (duplicate-`prev_day_close`, and
  `price_change_percent` dividing by current price instead of prior close)
  **recurred at edition 39 after four clean editions (35-38) — this is NOT a
  fixed/eradicated bug, it is intermittent and must be checked (and manually
  recomputed around) every single edition regardless of how many consecutive
  clean reads preceded it.** Always compute day-over-day % change manually as
  `price_change ÷ (current_price − price_change)` and treat the feed's own
  `price_change_percent` field as unreliable until checked each time
  regardless.
- **The DXY-vs-its-own-FX-crosses conflict** has now recurred, at least
  partially, in roughly half of all occurrences since edition 29 (resolved
  cleanly at 31, 33, 35; recurred at 32, 34, 36, 37, 38 — all three times via
  USD/JPY specifically breaking from DXY's direction). **This pattern PAUSED
  at edition 39**: USD/JPY (+0.29%) moved in the *same* direction as DXY
  (+0.11%) for the first time in four editions, breaking what had looked like
  a graduating-to-default-expectation streak. **Do not graduate this to
  "expected by default" — revert the framing to "worth watching whether the
  USD/JPY-specific divergence resumes," since it just broke after three
  straight occurrences.** Continue disclosing the DXY-vs-crosses comparison
  explicitly every edition regardless of which way it goes.
- **The same-day silver sign conflict first flagged at edition 31 has now
  stayed resolved for eight straight editions (32-39)** — silver rose/fell
  consistently across spot and futures at every session in that span. Treat
  as closed unless a fresh mismatch appears.
- **GBP/USD's two-edition data-quality problem (a minor two-source gap at
  edition 35, a genuine three-way level/direction conflict at edition 36)
  has now stayed resolved for three further editions (37, 38, 39)**, though
  **edition 39 used a lighter-touch single/partial-source method (Pound
  Sterling Live only, not the fuller four-source check used at 37-38) due to
  time constraints and found no conflict (+0.03%).** Resume the fuller
  four-source method the next time a conflict reappears, or periodically to
  re-confirm the lighter method is still safe. **Note this timing artifact
  for future editions: a live FX quote fetched near/after the NY 5pm close
  may reflect the *next* session's opening tick, with its own "previous
  close" already equal to the session just completed — don't mistake this
  near-zero "live" change for the day's actual close-to-close move. Use a
  dedicated close-to-close history source (Pound Sterling Live worked well)
  rather than a live snapshot when fetching this late in the window.**
- **The 2-year Treasury yield conflict from edition 36 (TextView 4.46% vs.
  CSV 4.79%, a 33bp gap) has stayed resolved for three further editions (37,
  38, 39)** — edition 39 fetched both the TextView and CSV endpoints directly
  again and found them in full agreement (2-yr 4.80%, 10-yr 5.24%, 30-yr
  5.60%, all Oct 9). Treat as resolved/noise unless a fresh conflict appears;
  if one does, the standing advice stands — dig into which endpoint is wrong
  via a market-wrap secondary cross-check for the specific disputed maturity.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 39 have all run clean (or
  clean after one quick fix) — **edition 39 drafted clean on the first pass
  at 40/40, then grew to 42/42 after two deliberate additions (tapeboard.com
  as a second index-close corroboration, and the archive.org Wayback
  Availability API citation for the USAGOLD check) were caught as
  Annex-B-only via the script and given inline citations immediately.** Worth
  re-stating: table cells (and disclosure-box/tile-adjacent sentences) are a
  legitimate, already-used place to put a citation — use them rather than
  forcing an awkward prose mention just to attach a `<sup>` tag.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 39 have all rendered clean at zero tildes** on the
  first check. **Reminder: `grep -c` exits with status 1 (not 0) when the
  count is zero, since no lines matched — don't chain it with `&&` into a
  longer command and assume a silent failure means the check itself failed;
  read the printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 34 resolved this cleanly for
  CFTC CoT, with full OI and Asset-Manager/Leveraged-Funds breakdowns for
  ES, NQ and RTY. **Edition 39 repeated this successfully** — full OI and
  Asset-Manager/Leveraged-Funds breakdowns for all three instruments again,
  plus a bonus CFE legacy-report pull for VIX futures positioning (not
  charted, reported in prose only). One naming note worth preserving: the
  CFTC's financial-futures table lists the full-size Russell 2000 E-mini
  ("RTY") as a separate line from the Micro E-mini Russell 2000, which has
  very different (much smaller) open interest and a different net-position
  sign at times — **edition 39 again explicitly confirmed it was reading the
  full-size RTY line (OI 425,152) and not the Micro line (OI 64,741) or the
  blended "NASDAQ-100 Consolidated" line for NQ** — always do this check
  before charting. **The next CFTC report is due Friday 16 October 2026,
  covering Tuesday 13 October data** — this will NOT fall inside edition 40's
  window (edition 39 covered through Fri 9 Oct; edition 40 will cover roughly
  Mon 12 Oct), so edition 40 should revert to the sector-ETF-proxy chart #2
  default per standing guidance, and the next CFTC-chart opportunity is more
  likely around edition 43-44 depending on scheduling.
- **A genuinely new chart-layout bug surfaced at edition 37, worth fixing
  permanently in `make_charts.py`'s documented defaults: the sector-ETF-proxy
  panel2 chart at `figsize=(9.8, 1.55)` with `tick_fs=7.6` and 11 categories
  produced visibly overlapping y-axis category labels** (confirmed by
  rendering and visually inspecting the PNG directly, not just trusting the
  matplotlib call succeeded) — the 1.55-inch height does not give 11 rows
  enough vertical room at that font size in this environment. **Fixed by
  bumping panel2's figsize to `(9.8, 1.95)`**, which rendered cleanly with no
  overlap; editions 38 reused this and confirmed it again. **Edition 39
  refined this further: a fuller `figsize=(9.8, 1.95)` is NOT needed for
  lower-category-count charts.** Edition 39 used `(9.8, 1.65)` for a
  7-category single-stock movers chart and `(9.8, 1.85)` for a 3-category
  grouped (Asset-Manager-vs-Leveraged-Funds) CFTC chart, both visually
  inspected at full resolution and confirmed clean with no label overlap or
  legend collision, and both saved meaningful vertical space versus the
  11-category-sized default — this was needed at edition 39 specifically
  because the day's content volume was unusually high (a dominant
  single-stock story plus fresh CFTC data plus a guidance-cut earnings print
  all in one session) and the document was overflowing to 5 pages at the
  11-category-sized chart heights. **Going forward: treat `(9.8, 1.95)` as
  the ceiling for an 11-category panel specifically, not a fixed default for
  every chart — scale figsize down for charts with fewer categories (roughly
  `(9.8, 1.95)` for 10-11 categories, `(9.8, 1.65-1.85)` for 3-8 categories),
  and always visually inspect the actual PNG at or near full resolution
  before embedding it regardless of category count.**
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at editions 33 through 39 (edition 39: NVAX +15.80% vs. VZ -8.75%, about
  1.8x), all left uncapped. Edition 30 remains the one genuine 10x+ case to
  date (about 15x, capped at a fixed axis max of 30). No need to revisit the
  threshold or mechanism absent a genuinely new edge case (e.g. something in
  the 5-10x range).
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists** — confirmed again at edition 35 (four
  analyst actions all traced to one Benzinga/Yahoo roundup, disclosed as
  such). Edition 37 hit the inverse problem (no roundup for any name could be
  located at all) and edition 38 hit a milder version of the same gap (only
  the session's own biggest earnings mover had dated analyst activity).
  **Edition 39 broke that two-edition streak of empty/near-empty results**:
  a genuine, well-corroborated Goldman Sachs upgrade of Palantir (Buy from
  Neutral, $230 PT, dated Thursday 8 Oct across multiple outlets) plus two
  Humana price-target raises tied directly to its Star Ratings beat (Cantor
  Fitzgerald, Barclays) were found. **Don't treat the edition 37-38 pattern
  as a durable new baseline** — a normal result (one or two well-sourced
  actions) remains the expected outcome in most editions; an empty result is
  a legitimate, disclosable gap when a genuine search comes up empty, not a
  sign something is broken.
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
  stated basis that conflicts with the primary filing. **Edition 39 also
  logged a new, distinct trap worth tracking separately: an EPS-consensus
  figure can be genuinely conflicted across sources due to a currency/
  share-basis mismatch, not a GAAP-basis mismatch** — TSMC's Oct 15 earnings
  call consensus showed approx. $4.39 (USD ADR-equivalent) in one source, a
  dispersed NT$4.32-4.65 range (local-currency, per-ordinary-share) in
  another, and an apparent outlier of $0.88 likely reflecting a raw
  share-count mismatch in a third. When comparing EPS consensus figures
  across sources, check whether they're quoted in the same currency and on
  the same per-share basis (ADR vs. ordinary share, which for TSMC is a 1:5
  ratio) before treating a gap as a genuine conflict.
- **Know when to treat a third-party data feed's own internal
  inconsistencies as a data-quality flag rather than a reportable trend.**
  Edition 38's zerogex (dealer-gamma) reads carried three separate
  within-session anomalies: a stale-snapshot caveat on the SPX page, a
  roughly 24x SPY net-GEX scale discontinuity vs. the prior session, and two
  conflicting QQQ figures on the same page. **Edition 39 resolved the
  ambiguity flagged at edition 38 about whether this was a one-off: the SPX
  stale-snapshot caveat RECURRED (now two straight editions, 38-39, with the
  page also showing two conflicting timestamps on itself this time) — treat
  this specifically as a structural, standing limitation of zerogex's SPX
  read, not an anomaly, going forward. The SPY scale discontinuity and QQQ
  internal conflict did NOT recur at edition 39 (checked across nine
  instances on the SPY page specifically) — treat those two as edition-38
  one-offs, resolved, no longer needing special scrutiny unless they
  reappear.** Continue reporting zerogex's directional headline with the SPX
  staleness caveat disclosed every edition; add it formally to the
  known-intermittent list below.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. **Editions 28 through 39 all got a full clean sweep** —
  twelve consecutive clean sweeps now, every series carrying a same-day
  `last_trade_time`, verified individually per series via a raw `curl`/direct
  fetch (not a tool-summarized fetch) each time. Still not a guarantee — keep
  checking `last_trade_time` on each series every time. **The feed's two
  known intermittent bugs (a duplicated `prev_day_close`, and a
  `price_change_percent` that divides by current price instead of prior
  close) RECURRED at edition 39 after four clean editions (35-38) — this
  confirms the bugs are not fixed/eradicated, they are genuinely
  intermittent.** Always compute day-over-day % change manually against the
  previous edition's logged close regardless of how many consecutive clean
  reads preceded the current one. The VIX9D-vs-spot-VIX front-end inversion
  (first flagged edition 28) narrowed at edition 38 (to -3.20 from -3.30) but
  **widened again at edition 39, to -3.58** — reversing that one-session
  narrowing. The pattern remains irregular/non-monotonic — don't assume
  either continuation or reversal by default in either direction.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table,
  and (absent fresher CoT data or another dominant story) chart #2. Editions
  35 through 38 all had no fresh CoT data due and used the sector-ETF-proxy
  default; **edition 39 had fresh CoT data and used the CFTC positioning
  chart instead (Section 5 placement), but still ran the full 11-row sector
  table in Section 2 as usual — the sector table and chart #2 choice are
  independent decisions, not coupled.** **Stockanalysis.com single-stock
  pages remain the standing default for pinning an exact closing price/%
  change on any individual mover** — editions 26 through 39 (fourteen
  straight) have all used direct fetches to it. Note that a headline wire's
  own GICS sector-index percentages can differ slightly from the SPDR ETF
  price-change figures (a normal index-vs-ETF-price methodology gap); keep
  using the SPDR ETF figures as the table's primary numbers. **Edition 40
  should revert to the sector-ETF-proxy chart #2 default** (next CFTC report
  not due until Fri 16 Oct, covering Tue 13 Oct data — outside edition 40's
  likely window).
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. Editions 38 and
  **39** both used the "X of 11 sectors closed higher" sector-ETF read as the
  best available breadth proxy (9 of 11 at edition 39), consistent with
  recent editions. Continue treating an uncorroborated single-aggregator (or
  unsourced search-summary) breadth figure as not usable — this has recurred
  enough times to treat as a durable, not occasional, gap.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — a recurring failure for many
  editions, not separately re-attempted at edition 39 (zerogex tried first
  per standing practice). **zerogex.io remains the only working source
  across thirteen straight editions (27-39)**, but carries a now-confirmed
  **structural (not one-off) data-quality limitation specific to its SPX
  read**: a stale-snapshot disclaimer recurred for a second straight edition
  (38, 39), this time with the page also showing two conflicting timestamps
  on itself. **Add this formally to the known-intermittent-bugs list
  alongside the CBOE feed's two documented bugs: zerogex's SPX page should be
  treated as carrying a standing staleness/timestamp-inconsistency caveat
  every edition, disclosed regardless of whether it's visually present that
  specific day.** By contrast, edition 38's SPY scale-discontinuity and QQQ
  internal-figure-conflict anomalies did NOT recur at edition 39 (checked
  across nine instances on the SPY page) — treat those two specifically as
  resolved/one-off, no longer needing extra scrutiny unless they reappear.
  The magnitude remains single-sourced (zerogex only; SpotGamma still yields
  no real numbers to cross-check against). Minor open item carried forward,
  still low priority: zerogex's own stated wall levels (call/put wall) have
  still not been cross-checked against a secondary options note's implied
  walls.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. Edition
  39 again used DeFi Rate's Kalshi/Polymarket-blended aggregator (now a
  stable, consistently-working source across editions 37-39) rather than a
  CME-attributed figure specifically — no fresh CME-attributed citation was
  sought this edition either. Keep treating CME FedWatch as needing a
  disclosed range from secondary sources, not a single figure.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, 23-35, 37, 38 and **39** (not attempted at edition 36) — a
  confirmed structural gap, not transient. The failure mode changed at
  edition 38 from a "Vercel Security Checkpoint" page to a plain HTTP 429
  (Too Many Requests); **edition 39 got the same HTTP 429 response again —
  now the confirmed standing failure mode across two consecutive attempts
  (38, 39), not session-to-session variance.** Resume the attempt-every-
  edition discipline at edition 40 regardless, but expect the 429. Use
  Kalshi's own secondary reporting (its blog, prediction-market news
  aggregators — news.kalshi.com, or DeFi Rate's own Kalshi/Polymarket-blended
  aggregator, which has now worked cleanly at editions 37, 38 and 39) as the
  workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has failed many
  editions running; not re-attempted at editions 35 through 39 (went straight
  to the Westmetall fallback per standing practice). **Westmetall.com has now
  worked cleanly eighteen editions running** as the fallback (copper +1.12%
  to $14,689.00/tonne cash settlement at edition 39, reconciling exactly
  against edition 38's logged $14,526.00 base — no reconciliation issue on
  copper specifically, unlike oil/gold/silver). A standalone Investing.com/
  oilprice.com/TradingEconomics-derived Brent/WTI page continues to work as a
  level-confirmation route, **but the oil level-vs-%-change-reconciliation
  pattern recurred again at edition 39, now narrowed specifically to WTI**
  (Brent reconciled cleanly for the first time in this run of editions) — see
  Hard Rules above for the broadened guidance to compute every
  commodity/FX %-change off the logged prior close, not just oil's.
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) has
  historically been preferred since TextView carries a known
  maturity-column mis-mapping bug, but edition 36 found a sharp 33bp
  disagreement between the two specifically on the 2-year. **Both endpoints
  have now agreed cleanly for four straight editions (36's fix confirmed at
  37, 38 and 39: 2-yr 4.80%, 10-yr 5.24%, 30-yr 5.60%, all Oct 9)** — treat
  the 33bp gap as resolved/noise, but keep fetching both endpoints and
  comparing rather than trusting either by default, since the gap has
  appeared once already without warning. Yield moves at edition 39 were a
  modest curve-wide rise (2-yr +5bp, 10-yr +2bp, 30-yr unchanged) after an
  AP-reported intraday spike to 5.24% on the 10-year.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. **Edition 39 successfully pulled fresh data
  for the first time since edition 34**: the report posted on schedule
  Friday 9 October 2026 (covering Tuesday 6 October data) — ES OI 1,932,227
  (Asset Mgr net +46.93% of OI, Leveraged Funds net -21.48%); NQ OI 283,586
  (Asset Mgr net +26.03%, Leveraged Funds net -6.78%); RTY (full-size,
  confirmed distinct from the Micro Russell line) OI 425,152 (Asset Mgr net
  +10.70%, Leveraged Funds net -24.77%); plus a bonus CFE legacy-report pull
  for VIX futures (OI 441,261, Non-Commercial net -20.69% of OI positioned
  for lower vol, Commercial net +20.53%). **The next report is due Friday 16
  October 2026, covering Tuesday 13 October data — this will NOT fall inside
  edition 40's window** (edition 39 covered through Fri 9 Oct; edition 40
  will cover roughly Mon 12 Oct only). Don't expect fresh CoT data again
  until around edition 43-44 depending on scheduling — check cftc.gov's
  release-schedule page each Monday/weekend-window edition regardless to
  confirm rather than assuming the gap.
- **GBP/USD and EUR/USD clean close:** both have now been fully resolved
  since edition 37 (EUR/USD since edition 26). **Edition 39 used a
  lighter-touch method for GBP/USD (Pound Sterling Live close-to-close
  history only) rather than the fuller four-source check used at 37-38, and
  EUR/USD was single-sourced to Investing.com** — both due to time
  constraints, not a data-quality concern, and no conflict was found either
  way. Resume the fuller multi-source method if a fresh conflict appears, or
  periodically to re-confirm the lighter method remains safe.
- **Gold/silver clean close on a non-event day:** USAGOLD's own history pages
  have now failed for **five editions running (35 through 39)** — edition 39
  tried a genuinely different access method per standing instruction (the
  Wayback Machine's own Availability API, queried for both the specific
  `/daily-gold-price-history` page and the bare homepage near the target
  dates) and got a clean, decisive negative result: **zero archived snapshots
  exist at all, not merely a blocked/403'd live fetch.** This is a materially
  stronger negative result than the four prior live-URL-path failures (which
  left open the possibility of a transient block). **Recommend formally
  closing USAGOLD as a standing, permanent gap — do not spend further research
  time attempting it in future editions unless a new URL/method becomes
  apparent from some other context.** Kitco, by contrast, **failed to yield
  a Friday-specific close for the first time in many editions at edition
  39** (returned only a Sunday 11 Oct snapshot despite several URL variants
  tried) — gold/silver spot figures were single-sourced to Investing.com
  this round. This is a new, notable data point on Kitco's reliability
  (previously described as "continues to work cleanly") — watch at edition
  40 whether this was a one-off timing issue (e.g. the fetch landing in a
  dead window) or a genuine degradation worth tracking. Gold futures continue
  to source cleanly via Investing.com. Silver's sign conflict (live since
  edition 31) has now stayed resolved for eight straight editions (32-39).
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month, but September's release had not posted as of edition 39's cutoff,
  and the release date itself remains disputed — one secondary source
  (financecalendar.com) cites 14 October; edition 39's research surfaced an
  unverified hypothesis (National Day Golden Week historically pushing the
  September release to the 13th in both 2023 and 2024) that would make the
  14 Oct estimate more plausible, but this was NOT independently sourced and
  should not be treated as confirming evidence — see Standing Facts above.
  Check stats.gov.cn directly at edition 40. **US import/export prices and
  industrial production:** frequently release mid-month on a Mon/Tue —
  confirm on the BLS/Fed release schedule rather than assuming a date;
  BLS's own schedule gives: **Sept CPI Wed 14 Oct 8:30am ET, Sept PPI Thu 15
  Oct 8:30am ET, Import/Export Price Indexes Fri 16 Oct 8:30am ET** (all
  re-confirmed via a direct bls.gov fetch of the dated monthly-schedule
  subpage — `bls.gov/schedule/2026/10_sched_list.htm` — at edition 39; note
  the generic `2026_sched.htm` URL 404's, use the dated monthly-list path),
  **Q3 Employment Cost Index Fri 30 Oct 8:30am ET**. **FOMC minutes from the
  15-16 September meeting are a closed thread** (see Standing Facts above).
  **US August 2026 trade deficit (BEA) widened to $132.6bn, released Tuesday
  6 October** — the headline direction is reasonably solid but the precise
  July baseline used by secondary sources was internally inconsistent across
  outlets ($118.9bn vs. $88.6bn) and was not resolved — treat the exact
  consensus comparison with caution if revisited; not revisited at editions
  37, 38 or 39. **University of Michigan preliminary October consumer
  sentiment** (new standing-facts item, see above): 46.3, final reading due
  23 October 2026 — watch for it at edition 40 or 41 depending on timing.
- **Henry Hub natural gas:** the October contract thread resolved at edition
  32 (final settlement $3.00/MMBtu). The November contract (NGX6) gave its
  cleanest-ever read at edition 38 (two vendors, Investing.com and
  TradingEconomics, both explicitly specifying the November 2026 contract
  month and agreeing closely) — **edition 39 found this did NOT persist**:
  TradingEconomics reverted to a generic/undated quote with no explicit
  contract-month label, leaving Henry Hub effectively single-sourced to
  Investing.com again this round (approx. $3.220/MMBtu, computed +2.68% off
  the logged prior close). **Do not promote the dual-vendor method to a
  standing default** — treat edition 38's clean dual-vendor read as a
  one-off rather than a durable improvement, and keep testing each edition.
  Still not labeled an official CME settlement print by either vendor.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. Not attempted at editions 33 through
  39 (secondary priority; options-flow colour has instead been sourced from
  dedicated options-flow wires or zerogex's broader snapshot). Edition 39
  again found no notable single-stock options-flow/skew commentary dated to
  its session on Applied Digital or AMD specifically (third consecutive
  empty edition on this sub-item, 37-39) — don't force this sub-item if
  nothing turns up, consistent with the derivatives section's own
  secondary-priority weighting. Consider whether this specific sub-item
  (APLD/AMD options flow) is worth continuing to check every edition given
  three straight empty results, or whether it should rotate to checking
  whichever name is that session's biggest single-stock mover instead.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable through edition 39;
  next due approx. 14 November 2026.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22). Not attempted again
  through edition 39.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, **repeated successfully
  again at edition 39** (see CFTC CoT entry above). Repeat this full
  three-instrument fetch whenever a fresh CoT-based chart is next used —
  next due Friday 16 October 2026 (covering Tuesday 13 October data), which
  will likely land inside edition 41's or 42's window rather than 40's —
  watching for the Micro-vs-full-size Russell naming trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Edition 37 hit the
  most extreme version yet (no roundup for any name could be located at
  all); edition 38 hit a milder version (only the session's biggest earnings
  mover had dated activity). **Edition 39 broke that streak with a normal,
  multi-name result** (Goldman/Palantir, Cantor Fitzgerald and Barclays/
  Humana, all with clear dollar price targets and dates) — treat the
  edition-37/38 pattern as having been a temporary dry spell, not a new
  durable baseline; report whatever a genuine search attempt turns up each
  edition, whether that's zero, one, or several actions.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29, recurred with milder
  versions through edition 36). Editions 37 through 39 did not hit a new
  instance of this specific trap on any NAMED mover reported in the body —
  edition 39's named movers (TMUS, T, VZ, ASTS, CCI, HUM, MRNA, NVAX, FSLY,
  AAOI/COHR/LITE) were all corroborated across at least two independent
  sources each (stockanalysis.com plus a dated news article), **except
  Palantir's specific Friday closing price, which WAS single-aggregator-
  sourced (tapeboard.com only) and was correctly excluded from the body as a
  result** — a clean example of the right call: report the well-corroborated
  parts (the Goldman upgrade itself), omit the single-sourced part (the
  specific Friday price), rather than publishing an unverified number. The
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
  edition 37, reused at edition 38) — this remains correct for 10-11
  categories specifically. For charts with fewer categories, scale the
  height down: edition 39 used `(9.8, 1.65)` for a 7-category single-stock
  movers chart and `(9.8, 1.85)` for a 3-category grouped
  (Asset-Manager-vs-Leveraged-Funds) CFTC chart, both visually inspected at
  full resolution and confirmed clean with no label overlap or legend
  collision. Use `font.size 9.6`, dpi 210, `width:100%` in the page. A
  shorter-category-count chart2 (e.g. 7-8 rows, such as a CFTC positioning
  chart) may still need 1.65-1.85in depending on whether it's a simple or
  grouped bar — **always render and visually inspect (via the Read tool) the
  actual PNG at or near full resolution before embedding it**, regardless of
  what a past edition's page-count success might suggest. For a grouped
  (multi-series) bar chart, such as edition 34's and edition 39's CFTC
  Asset-Manager-vs-Leveraged-Funds chart, the simple single-series `barh()`
  helper in `make_charts.py` doesn't apply — use a dedicated `grouped_bar()`
  function instead (vertical offset bars per category, two series, legend
  below the plot via `bbox_to_anchor` with enough negative y-offset and a
  matching `fig.subplots_adjust(bottom=...)` to avoid the legend colliding
  with the x-axis label — this collision was caught and fixed at edition 39
  specifically; don't rely on `tight_layout()` alone for a grouped chart with
  a below-axis legend, it doesn't reserve enough room by default).
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
  not always a stray break — editions 24, 28 and 33 all hit 5 pages with
  only the one correct pagebreak present; the cause was genuine copy
  overflow each time, and **edition 39 is a further example: the body
  content for a high-volume session (telecom-sector shock + fresh CFTC data
  + a guidance-cut earnings print + a biotech rally all in one window)
  genuinely overflowed 3 pages at the standing CSS baseline and needed both
  real content trims AND a deliberate, evidence-based tightening of the CSS
  baseline (see Working settings below) to fit — this was not a bug, it was
  a genuinely content-heavy edition.** Always re-render and re-check the
  page count after each trim/pad round rather than guessing how much is
  enough. **A large, suspicious blank area at the bottom of a page (as
  opposed to a page that's merely a bit short) is usually caused by an
  atomic block — most often a chart `<img>` — not fitting in the remaining
  space and being pushed whole to the next page, leaving the page that
  precedes it under-filled.** Edition 39 hit this on page 1 (the Section 2
  movers chart got pushed entirely to page 2, leaving roughly 40% of page 1
  blank) — the fix was trimming earlier content (the disclosure box, mainly)
  so the chart had room to start and finish on the same page as its
  preceding heading, not a layout bug in the chart itself. Check for this
  specific failure mode (a heading near the bottom of a page immediately
  followed by a large blank area, with the heading's content starting fresh
  on the next page) before assuming a page is simply "short."
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. The Commodities & FX table has split cleanly
  across page boundaries with no repeated header row in multiple recent
  editions (35 through 39) — plain-`<tr>` tables reflow across a page break
  safely; this is expected behavior, not a bug to fix.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  A visibly short page 3 has recurred at editions 25, 28, 32 and 36, each
  needing a genuinely additive fix (never a padding table that just repeats
  an existing table's rows). Editions 37 and 38 both rendered clean at 4
  pages on the first attempt. **Edition 39 is the counter-example worth
  remembering: it took six render-and-inspect rounds to go from 5 pages to 4,
  via a combination of real content trims (dropping a table row here, tightening
  a sentence there, merging adjacent commodities/FX rows, downsizing both
  chart figsizes) and a deliberate CSS tightening (see Working settings
  below) once the easy trims stopped moving the needle — don't be afraid to
  touch the CSS baseline when there's genuine evidence of overflow on an
  unusually content-heavy edition, but do it incrementally and re-render
  after every change, since the effect of any single small change can be
  hard to predict (several 0.1-0.3px tweaks in a row produced no visible
  change before a slightly larger change finally moved the break point).**
  Continue checking for both failure modes (short page 3, overflow) after
  every render regardless of recent-edition track record.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable for that edition's unusually
high content volume, treat as the new default and only loosen it back toward
the old values if a future edition renders with noticeably excessive
whitespace at these settings)
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
  doesn't fill the page. Needed at editions 25, 28 and 36 (the latter via a
  Treasury yield-curve table variant); not needed at most other editions,
  including 34, 35, 37, 38 and **39** (39 was the opposite problem — overflow,
  not a short page, so this padding table was never relevant). Always
  re-render immediately after adding (or removing) any content to confirm
  the page count, rather than assuming a change is safe. **If a future
  edition is short on page 3 at the new tightened CSS baseline, the first
  lever to pull is adding genuine content (the padding table above), not
  loosening the CSS back toward the old baseline — only loosen the CSS if
  several consecutive editions all run short, suggesting the tightening
  overshot.**

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across fourteen eligible
editions, 25 through 39, with editions 34 and 39 the exceptions when fresher
CFTC data was available). Fresh CFTC CoT data on a Monday/weekend-window
edition → the ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart,
normalized as % of open interest — this has now happened twice (edition 34,
edition 39); editions 35 through 38 all had no fresh CoT data due and
correctly reverted to the sector-ETF-proxy default. **Edition 40 should
revert to the sector-ETF-proxy default** (next CFTC report due Fri 16 Oct,
outside edition 40's likely window). A single dominant earnings print with a
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
well as genuinely independent, complementary stories.** Chart #2's placement
in the document should follow its content, not a fixed section — editions
24, 34 and **39** all placed a CFTC/positioning chart #2 in Section 5
(Derivatives) rather than Section 2; editions 35 through 38, all back on the
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

**Editions 1–37 (condensed):** established the format (edition 1 baseline;
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
overlapping y-axis labels were caught on visual inspection).

**Edition 38 (condensed)** — Friday 9 October 2026 report covering Thursday
8 October 2026, the window's one NYSE session. Equities fell for a second
straight session but breadth stayed strong (S&P 500 -0.5% to 7,765.36, Dow
+0.1% to 51,231.64 the only major average higher, Nasdaq Composite -1.3% to
27,193.34, Russell 2000 flat +0.03%); eight of eleven SPDR sectors closed
green, Technology (-1.79%) the sole real drag as a second straight session
of AI-optics profit-taking (AAOI -13.58%, COHR -9.63%, LITE -5.62%) extended
Wednesday's reversal; Caterpillar's Wednesday -5.75% mystery was resolved
(a joint FTC/USDA farm-equipment-dealer antitrust inquiry); Applied
Digital's blowout fiscal Q1 print (revenue +322% y/y) drew a muted +0.17%
reaction despite a wide GAAP loss, and a non-GAAP-vs-GAAP EPS conflict trap
was logged for the first time (a secondary aggregator's "+1¢" figure
excluded in favor of the 8-K's GAAP loss); Constellation Brands extended its
post-guidance-raise strength, +4.43% to $123.63. The first Fed-odds reading
obtained after Wednesday's FOMC-minutes release showed October hike odds
approx. 16-17%, essentially unchanged pre/post-minutes — closing the "top
open item" from edition 37; Kalshi's direct fetch returned a plain HTTP 429
for the first time (previously a Vercel checkpoint page); a primary-source
breakthrough closed the BoJ's last standing gap (next meeting confirmed
Oct 29-30 via a direct boj.or.jp fetch). Oil posted its sharpest move in
several editions (WTI approx. +2.3%, Brent approx. +3.1%) but vendor
%-changes again failed to reconcile against the logged prior close, now a
well-established durable pattern on oil specifically; gold and silver
sourced cleanly with no sign conflict; DXY was 3-source corroborated for the
first time in several editions; USD/JPY diverged from DXY for a third
consecutive session. CBOE gave an eleventh consecutive clean sweep (VIX
15.41, +2.19%); the VIX9D-VIX inversion narrowed to -3.20 from -3.30,
breaking a multi-session widening trend for the first time; zerogex's
dealer-gamma reads carried three separate within-session anomalies (a stale-
snapshot caveat on SPX, a roughly 24x SPY net-GEX scale discontinuity, two
conflicting QQQ figures) — reported directionally with explicit caveats
rather than as a clean trend, a new data-quality trap logged for future
tracking. No new CFTC CoT report was due. 28 sources, clean 28/28 on the
second `check_refs.py` pass, zero stray tildes, clean 4-page render on the
first attempt.

**Edition 39 (most recent — full detail)** — Monday 12 October 2026 report
covering Friday 9 October 2026, the window's one NYSE session, research
window Thu 8 Oct 2026 20:00 ET through Sun 11 Oct 2026 20:21 ET (a
weekend-window edition). Verified the two structural header rules again —
now clean across twelve consecutive single-session or weekend-window
editions (29-39).

The session's dominant story broke just after edition 38's Thursday cutoff
and was independently confirmed via multiple outlets: SpaceX agreed to buy
Grain Management's nationwide 800MHz low-band spectrum portfolio (approx.
$8bn per WSJ reporting, pending FCC approval) to build out Starlink Mobile
direct-to-cell service, rattling the telecom sector — T-Mobile -13.27%,
AT&T -9.81%, Verizon -8.75% — while tower REIT Crown Castle jumped +15.60%
on the infrastructure read-through (CCI's specific driver was sector-level
inference, not a name-specific article). Equities shrugged this off at the
index level, closing a record-setting week: S&P 500 +0.6% to 7,811.54 (just
shy of Tuesday 6 Oct's 7,818.93 closing high), Dow +0.8% to 51,654.95,
Nasdaq Composite +0.6% to 27,366.17, Russell 2000 +0.5% to 2,806.98; 9 of 11
SPDR sectors closed green, only Communication Services (-1.51%, diluted by
the carriers) and Energy (-0.25%) lower — confirmed via AP's wire (reached
via a La Nación syndication mirror again) cross-checked against a second
dated recap (tapeboard.com), with Thursday-to-Friday arithmetic reconciling
exactly against edition 38's logged closes. A second, independent storyline
was a broad biotech rally: Moderna +14.21% (joined the Nasdaq-100 before
Friday's open, replacing Warner Bros. Discovery — closing the loop on that
ticker's September 2026 merger/renaming saga), Novavax +15.80% (part of a
broader IBB rally, no company-specific catalyst found despite a real
search), Humana +11.56% (2027 Medicare Advantage Star Ratings beat fears,
Cantor Fitzgerald and Barclays both raised price targets same-day). Fastly
+15.86% and a second consecutive unexplained session for the AI-optics trio
(AAOI +3.53%, COHR +3.40%, LITE +5.22%, rebounding from Wed/Thu's
profit-taking) both remain open threads with no driver found despite real
search attempts — watch for a delayed explanation at edition 40, as
happened with Caterpillar between editions 37 and 38. Delta Air Lines
reported before Friday's open: GAAP diluted EPS $1.15, adjusted non-GAAP
EPS $1.72 (company's own 8-K disclosed both, contrasted explicitly in Hard
Rules with the edition-38 APLD trap, which involved a conflicting
secondary-only figure); FY2026 adjusted EPS guidance was slashed to
$5.10-5.60 from a prior $6.50-7.50, yet the stock closed essentially flat
(+0.04%). Goldman Sachs upgraded Palantir to Buy (Thursday 8 Oct, $230 PT) —
the first normal, well-sourced analyst-action result after two
near-empty editions (37, 38); Palantir's own Friday closing price was
single-aggregator-sourced and correctly omitted from the body as a result.

Standing facts were all re-verified fresh: Kevin Warsh remains Fed Chair (a
ninth straight direct re-confirmation); next FOMC 27-28 October confirmed;
BoE's next decision (5 November) re-confirmed directly, resuming the
direct-fetch discipline now that the meeting is inside a roughly 3.5-week
window; BoJ's next meeting (29-30 October) re-confirmed directly for a
second consecutive edition. The shutdown/CR primary-source lapse flagged at
edition 38 was closed via a genuine direct whitehouse.gov fetch (the working
technique: use the dated statement permalink, not the generic briefing-room
index pages, which don't surface it) — still funded through 11 December
2026, unchanged. October hike odds held flat at approx. 16% (December
approx. 73-74%) per a Sunday evening DeFi Rate snapshot, materially
unchanged from edition 38's first post-minutes read — Kalshi's direct fetch
returned HTTP 429 for a third consecutive edition, now a confirmed standing
failure mode. China's September CPI/PPI still had not posted as of a direct
stats.gov.cn fetch; a secondary source's 14 October estimate remains
uncorroborated by any primary calendar, though edition 39's research
surfaced an unverified hypothesis (National Day Golden Week historically
delaying the September release) worth testing properly at a future edition.
University of Michigan's preliminary October consumer sentiment printed
46.3, a five-month low, with consensus estimates disputed sharply across
outlets (approx. 47.6-50.5) — final reading due 23 October.

Oil, gold spot, silver spot, DXY and Henry Hub all required computing
%-change off this report's own logged prior close rather than trusting
vendor-stated changes — a pattern that broadened this edition beyond oil
specifically (WTI's vendor base still didn't reconcile, but Brent reconciled
cleanly for the first time in this run; gold spot, silver spot and DXY all
showed milder versions of the same gap). Henry Hub's November contract
(NGX6) reverted to single-vendor sourcing after edition 38's unusually clean
dual-vendor read did not persist. USD/JPY moved in the same direction as
DXY this session, breaking a three-edition divergence streak (36-38) — a
pause, not a reversal of the "watch, don't assume by default" framing.
USAGOLD was tried via the Wayback Machine's own Availability API (a
genuinely different method from four prior live-URL attempts) and returned
zero archived snapshots — recommend closing this as a permanent standing
gap rather than re-attempting. Kitco, notably, failed to yield a
Friday-specific close for the first time in many editions — watch whether
this persists.

CBOE's delayed-quotes feed gave a clean, fresh sweep (VIX 14.84, manually
computed -3.70%; VIX9D 11.26, -7.78%), but **both of the feed's known
calculation bugs resurfaced after four clean editions (35-38)** — confirms
they are intermittent, not fixed, and must be manually recomputed around
every edition regardless of recent clean streaks. The VIX9D-VIX inversion
widened back out to -3.58 from -3.20, reversing edition 38's one-session
narrowing. zerogex's SPX dealer-gamma read carried a stale-snapshot caveat
for a second consecutive edition (now treated as a structural, standing
limitation rather than a one-off, added formally to the known-intermittent
list); the SPY scale-discontinuity and QQQ internal-conflict anomalies from
edition 38 did NOT recur, treated as resolved one-offs. The CFTC's
Commitments of Traders report posted fresh data for the first time since
edition 34 (as of Tuesday 6 October, released Friday 9 October): Asset
Managers net long and Leveraged Funds net short across ES, NQ and RTY, short
skew deepest in Russell 2000 (-24.77% of OI) and shallowest in Nasdaq-100
(-6.78%), plus a bonus CFE legacy-report pull showing VIX futures positioned
for lower near-term volatility — this powered a CFTC-positioning chart #2,
placed in Section 5 per standing practice for a positioning chart. SOFR
printed 3.87% for Oct 8 (one-day lag).

A genuinely new chart-sizing refinement was made and confirmed by visual
inspection: figsize should scale to a chart's category count rather than
use one fixed size for everything — `(9.8, 1.65)` for the 7-category movers
chart and `(9.8, 1.85)` for the 3-category grouped CFTC chart, both well
below the previous `(9.8, 1.95)` default that is correct only for an
11-category panel. The document was a genuine 5-page overflow at the old
chart sizes and old CSS baseline, driven by unusually high content volume
(a dominant single-stock/sector story, fresh CFTC data, a guidance-cut
earnings print and a biotech rally all landing in one window); it took six
render-and-inspect rounds — a mix of real content trims and a deliberate,
evidence-based CSS retightening (table cell padding, paragraph and heading
margins, bullet-list spacing) — to reach a clean 4-page render. 42 sources,
clean 42/42 on `check_refs.py` after two Annex-B-only additions were caught
and given inline citations, zero stray tildes.

**Open threads for edition 40:** AAOI/COHR/LITE's second consecutive
unexplained session and Fastly's fully unexplained +15.86% move both need a
delayed-driver check, following the Caterpillar precedent (resolved one
edition late at 37→38). Kitco's failure to yield a Friday-specific gold/
silver close is new and needs a one-edition follow-up to determine if it's a
one-off or a genuine reliability change. The USD/JPY-vs-DXY divergence
paused after three editions (36-38) — watch whether it resumes or stays
paused; don't assume either. zerogex's SPX stale-snapshot caveat is now
formally a known-intermittent item — continue disclosing every edition
regardless of whether the caveat is visually present that day. China's
September CPI/PPI remains unresolved on both data and release date — check
stats.gov.cn directly at edition 40, and if time allows, try to properly
source the Golden-Week-delay hypothesis (unverified this edition) rather
than continuing to carry it as an unsourced aside. The next CFTC CoT report
(Friday 16 October, covering Tuesday 13 October) will not fall inside
edition 40's window — revert to the sector-ETF-proxy chart #2 default for
edition 40 unless circumstances change. TSMC's Oct 15 earnings call
(approx. 2:00am ET, consensus revenue approx. $45.8bn, EPS consensus
genuinely conflicted across sources due to an ADR-vs-local-currency
mismatch — see Hard Rules) and the New Mexico v. Meta penalty ruling
(expected approx. 22 Oct per a 1 Oct hearing where Judge Mathew took the
matter under advisement; a report describing a stay on the eventual
judgment could not be independently corroborated beyond one paywall-limited
snippet and was excluded, flagged in Annex A — try to corroborate or drop
this stay claim at edition 40) remain flagged catalysts. University of
Michigan's final October consumer-sentiment reading is due 23 October —
watch for it. Sept CPI (14 Oct), Sept PPI (15 Oct) and import/export prices
(16 Oct) are the next major data prints, all BLS-schedule-confirmed. Humana,
Moderna and the broader telecom-disruption trade (TMUS/T/VZ/CCI) are all
worth checking for Monday follow-through. Delta's guidance cut is a
single-name event, not flagged as needing sector-wide airline read-across
unless a future edition's research surfaces one. Threads closed after
resolution rather than carried further: the CFTC CoT data gap (closed, fresh
data obtained); the shutdown/CR primary-source lapse (closed via a direct
whitehouse.gov fetch); the zerogex SPY/QQQ edition-38 anomalies (closed,
treated as one-offs); USAGOLD (recommend closing permanently, see Known-
hard-to-source above).
