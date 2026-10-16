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
  through 43 have all applied this correctly** ("Friday 2 October 2026"
  through "Friday 16 October 2026" as the date line in each respective
  edition, with the window line carrying the session(s) covered) — now
  confirmed stable across eleven consecutive editions, treat as settled.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 through 43 all reused the
  same pattern for single-session (or single-session-plus-weekend) windows —
  now confirmed clean across fifteen consecutive editions (29 through 43;
  edition 43 phrased it "Window: Wed 14 Oct 2026 20:00 ET – Thu 15 Oct 2026
  20:21 ET (Thu 15 Oct close/AH)"). No further confirmation needed; treat
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
  with the Committee stressing data-dependency meeting to meeting.
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 43
  directly against federalreserve.gov's own FOMC calendar page — now under
  two weeks out, continue re-confirming every edition until then. Decision
  and press conference are expected 2:30pm ET on 28 Oct, but **the specific
  time has now failed to re-display on the Fed's own calendar page for TWO
  straight editions (42, 43)** — carried forward unverified rather than
  silently assumed; make a third direct attempt at edition 44 before treating
  this as a structural, not transient, gap. The following meeting is December
  8-9, 2026 (an SEP meeting).
- **Rate-path odds did NOT extend further hawkish on the hot September PPI
  print — worth noting as a genuine non-reaction, not a repricing:** DeFi
  Rate's Kalshi/Polymarket-blended aggregator, fresh snapshot Thursday 15 Oct
  2026 8:00pm ET (post-PPI), shows **October 27-28 hike odds approx. 28%**
  (hold approx. 71%, cut approx. 2%) and **December 8-9 hike odds approx.
  77%** — essentially flat to a touch softer than Wednesday 14 Oct's
  post-CPI read of approx. 29%/78% (edition 42). The blowout PPI print
  (headline +1.3% m/m/+6.3% y/y, the hottest since 2022) plausibly didn't move
  Fed odds further because PPI is a more volatile, less Fed-relevant series
  than CPI — the CPI-driven repricing from edition 42 had already done the
  level-shift work. **DeFi Rate's own page carried an internally inconsistent
  "meeting table" view this edition** (approx. 30% Oct/81% Dec, with a 21%
  hold that doesn't reconcile against an 81% hike) — the blended headline
  figures were used, the inconsistency disclosed; watch whether this
  resolves or recurs. Kalshi's own direct fetch failed again at edition 43
  (429/timeout), now a confirmed standing failure mode across **seven**
  consecutive attempts (37-43). Official CME FedWatch also failed again
  directly (timeout) at edition 43. The composite "at least one more hike in
  2026" read has still not been freshly re-pulled since edition 38 (last
  known approx. 80%) — don't cite without a fresh pull. The unverified
  Seeking Alpha 49.3% CME-FedWatch-attributed claim from edition 42 was not
  re-touched at edition 43 — still don't cite it without independent
  corroboration.
- **US-China "30-for-30" tariff framework — closed thread as of edition 37, do
  not re-open:** 77 US product categories (household goods, textiles,
  appliances, toys, sporting goods, vacuum flasks) and 1,619 Chinese
  categories (dominated by food/farm goods, plus some medical devices;
  soybeans, chips, EVs and batteries excluded from both sides), each side's
  treatment benchmarked at approx. $30bn against 2024 bilateral trade,
  confirmed directly against whitehouse.gov's own Terms of Reference
  document. Still pending each side's domestic legal processes for actual
  implementation — no Federal Register/USTR implementation notice has been
  found through edition 43 — watch for a formal implementation/effective date
  in a future edition.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates, government funding status) from memory or from the prompt's own
  framing — verify it fresh from a primary source (federalreserve.gov,
  bankofengland.co.uk, boj.or.jp, kansascityfed.org, norges-bank.no,
  riksbank.se, banxico.org.mx, snb.ch, rba.gov.au, whitehouse.gov, etc.) every
  edition, exactly like any other data point. **Edition 43 re-confirmed Kevin
  Warsh as Fed Chair directly against federalreserve.gov's Board of Governors
  bios page — a fourteenth straight direct re-confirmation.** The BoE's next
  decision (Thursday 5 November) was freshly re-touched at edition 43 via a
  direct bankofengland.co.uk fetch — unchanged, now confirmed directly for
  five straight editions (39-43). **The shutdown/CR status check was
  RESTORED to a clean direct primary-source footing at edition 43**, ending
  the two-edition (41-42) secondary-only regression: a direct whitehouse.gov
  fetch of `https://www.whitehouse.gov/briefings-statements/2026/09/congressional-bill-h-r-6500/`
  confirms H.R. 6500 (the Continuing Appropriations and Extensions Act, 2027,
  signed 2 September 2026) funds federal agencies through **11 December
  2026**, no shutdown in effect. **This exact URL pattern
  (`/briefings-statements/YYYY/MM/congressional-bill-h-r-NNNN/`) is confirmed
  working — reuse it directly at future editions rather than re-deriving a
  URL from scratch.** The BoJ's next-meeting-date primary source stayed
  confirmed via direct read at edition 43: a direct boj.or.jp fetch of its
  Monetary Policy Meeting schedule page confirmed Oct 29 (Thu) – Oct 30
  (Fri), 2026 in plain text, unchanged, now three straight editions (41-43)
  on the restored direct-fetch method.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed directly
  again at edition 43 (following decision 17 December 2026). Continue the
  direct-fetch discipline every edition given the meeting is now under three
  weeks out.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, a 7-2 vote (dissenters Asada Toichiro
  and Sato Ayano), both primary-sourced as of edition 37 — closed thread, do
  not re-derive. **The next policy meeting date (Oct 29-30, 2026) was
  re-confirmed via a direct boj.or.jp plain-text fetch again at edition 43**,
  now three straight editions (41-43) on the direct-fetch method.
- **The four-central-bank Thursday 24 September 2026 cluster remains fully
  resolved — closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% but signalled a greater chance of
  a Q4 hike; Banxico held at 6.50% unanimously; SNB held at 0% and raised its
  inflation forecasts, confirmed directly against snb.ch.
- **The Reserve Bank of Australia's Tuesday 29 September 2026 decision remains
  fully resolved — closed thread, do not re-open:** hiked 25bp to **4.60%,
  unanimous**, a 15-year high and its fourth hike of 2026, confirmed directly
  against rba.gov.au's own Statement by the Monetary Policy Board.
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
  Situation Summary.
- **September 2026 ISM Services/Non-Manufacturing PMI — closed thread as of
  edition 35, do not re-derive:** headline 54.9% (down from August's 55.4%),
  Prices Paid 74.0% (+1.4pt, highest since July 2022). Confirmed directly
  against ISM's own press release.
- **September 2026 US CPI — closed thread as of edition 42, do not re-derive:**
  headline **+0.6% m/m / +3.7% y/y**, core **+0.3% m/m / +2.6% y/y**, both
  above the Dow Jones consensus of approx. 3.6%/2.5%, confirmed directly
  against bls.gov's CPI Summary release. This was the proximate trigger for
  edition 42's broad equity selloff, VIX spike and sharp October-hike-odds
  repricing.
- **September 2026 US PPI — NEW at edition 43, closed thread, do not
  re-derive:** final demand **+1.3% m/m / +6.3% y/y** (NSA), the largest
  monthly gain since March 2022 and largest 12-month rise since December
  2022; the trade-services-excluded measure (BLS's closest analog to "core,"
  since BLS's September release does not publish a conventional ex-food/
  -energy PPI) was +0.5% m/m / +5.0% y/y. Energy (+10.8% m/m, gasoline
  +20.3%) drove over 80% of the goods-side increase. Confirmed directly
  against bls.gov. **No Dow Jones/Reuters consensus estimate could be
  verified for this release at edition 43** — only a non-survey AI-generated
  forecast site was found and was not used; if a genuine consensus figure
  surfaces later, it can be added retroactively, but don't force one. Notably,
  this hot print barely moved Fed rate-path odds — see the rate-path-odds
  entry above.
- **No US federal government shutdown is in effect — status re-confirmed on a
  clean direct primary-source footing at edition 43** (see general principle
  entry above for the URL pattern). H.R. 6500 funds the government through
  **11 December 2026**. Watch for shutdown risk resurfacing as that date
  approaches.
- **University of Michigan preliminary October 2026 consumer sentiment —
  still not a "closed thread," watch for the final reading:** 46.3, a
  five-month low (current conditions 44.7, expectations 47.3, year-ahead
  inflation expectations 4.7%, long-run 3.5%), confirmed via
  investinglive.com and advisorperspectives.com, both dated 9 Oct 2026.
  **Final October reading due 23 October 2026** — watch for it; not yet
  re-touched since edition 40 (now under 8 days out).
- **China September 2026 CPI/PPI — RESOLVED at edition 42, closed thread, do
  not re-derive:** CPI **+0.9% y/y** (+0.2% m/m), PPI **+5.0% y/y** (the
  fastest PPI rise since June 2022), driven by fuel costs. Sourced to gov.cn's
  English-language NBS-attributed news release (stats.gov.cn itself remained
  stale/unreachable) — continue treating the gov.cn English release as an
  acceptable near-primary substitute if stats.gov.cn remains unreachable.
- **New Mexico v. Meta — CORRECTED at edition 43; the prior spec's "approx.
  22 Oct" expected-ruling date could not be corroborated by any outlet and is
  now retired.** The actual penalty-phase hearing (following the jury's
  late-September verdict that Meta violated the state's Unfair Practices Act
  roughly 43.9 million times, re: hate-speech policy and its Cambridge
  Analytica response) was held **Thursday 1 October 2026** before Judge
  Francis Mathew in Santa Fe. New Mexico is seeking **$35-40bn** in
  penalties (reduced from the statutory theoretical maximum of approx.
  $219bn at $5,000/violation); Meta is asking the judge to cap penalties at
  **$3.45bn**. Judge Mathew has indicated he expects to rule "later this
  month" (October 2026) — no outlet gives a specific date. **Still an open
  thread — watch for the actual ruling, do not re-cite a specific expected
  date until one is corroborated.** This is a distinct proceeding from the
  March 2026 child-safety jury verdict ($375m) and the August 2026 abatement
  ruling ($567m, under appeal) — don't conflate the three.
- **New calendar-awareness item from edition 40, reconfirmed relevant at
  edition 41: "equities-open, bonds-closed" US holidays need an explicit
  check every time they land in the window, not an assumption from memory.**
  Monday 12 Oct 2026 was Columbus Day — NYSE/Nasdaq traded a normal full
  session but the Treasury cash market and SOFR/EFFR/OBFR fixings were
  closed. **Next candidate to verify when it lands: Veterans Day, Wed 11 Nov
  2026 — confirm whether that is also bonds-only before assuming.**
- **The vendor-retroactive-revision trap (first logged edition 41, broadened
  at edition 42) widened FURTHER at edition 43 — now treat this as the
  expected default on most commodity/FX instruments every edition, not an
  occasional risk.** At edition 43, SIX of eleven commodity/FX/Treasury
  instruments showed a Wednesday 14 Oct base that had shifted again from what
  edition 42 itself logged: WTI (logged +0.70%, re-fetched +1.01%), Henry Hub
  (a THIRD conflicting figure, see below), gold futures (logged -1.06%,
  re-fetched -1.66%), EUR/USD (logged -0.04%, re-fetched -0.38%), GBP/USD
  (logged -0.19%, re-fetched -0.46%), USD/JPY (logged -0.21%, re-fetched
  0.00%). Only Brent, silver, copper, DXY and the Treasury curve reconciled
  cleanly against edition 42's logged Wednesday figures. **Recommendation
  for future editions, now acted on at edition 43: compute every
  commodity/FX/Treasury %-change off a freshly-refetched prior-session base
  from the same vendor table, never off the previously-logged figure, and
  disclose every divergence found — do not expect this to ever fully
  resolve.**
- **Henry Hub natural gas now carries a THIRD, worse conflict, worth
  tracking as its own escalating sub-thread:** at edition 43, three mutually
  inconsistent "Wednesday 14 Oct" reference points existed simultaneously —
  edition 42's own logged close ($3.289), a freshly-fetched historical-table
  close ($3.198, -2.59%), and a separate live-quote page's stated "previous
  close" ($3.240). Thursday 15 Oct's change (+0.50%) is reliable only
  relative to the $3.198 table base; it cannot be reconciled against either
  of the other two. This is now the fourth consecutive edition (40-43) with
  some form of Henry Hub base ambiguity — treat as a standing, not
  intermittent, data-quality issue for this specific instrument.
- **A new, distinct trap logged for the first time at edition 42: a vendor's
  live "spot" quote can lag or mistime a sharp single-session move captured
  cleanly by the futures settlement on the same page. CONFIRMED as genuinely
  intermittent (not one-directional) at edition 43, with the conflict
  recurring in the OPPOSITE direction.** At edition 42, gold/silver futures
  sold off hard but Kitco's live spot ticker showed both UP, contradicting
  Kitco's own headline. At edition 43, gold/silver futures ROSE but Kitco's
  live spot ticker showed gold DOWN (-0.36%), again contradicting Kitco's own
  concurrent headline ("Gold approaches $4,170, silver gains 3%..."), which
  matched the futures-based gain. **The rule stands unchanged: when a
  vendor's own live quote conflicts with that same vendor's own published
  headline/commentary, trust the headline-aligned figure (futures
  settlement) and disclose the live-quote conflict** — now confirmed across
  two editions in both directions, firmly establishing this as a recurring,
  not one-off, trap for Kitco specifically.
- **The DXY-vs-its-own-FX-crosses conflict did NOT recur at edition 43** —
  DXY (-0.48%) and USD/JPY (-0.11%) moved the SAME direction this time,
  continuing to confirm the divergence pattern (last seen at edition 42) is
  genuinely intermittent in both directions, not a standing feature. Keep
  disclosing the comparison every edition regardless of which way it goes.

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
  uniqueness of use (editions 33-43 have all done this for stockanalysis.com
  single-stock closes and other repeatedly-used outlets, confirmed stable
  across eleven editions). **Citing the prior edition itself as a source**
  (e.g. "[50] Daily Economic Briefing, edition 42, logged prior-session
  baseline figures") is a legitimate, already-used pattern when disclosing a
  divergence against a previously-logged figure — edition 43 did this for
  the first time and it worked cleanly with `check_refs.py`.
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
  actually belongs. Editions 35 through 43 (nine straight) reverted to the
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
  has occasionally failed to post in time. **Edition 43 hit a harder version
  of the AP-unavailable problem than any recent edition**: no direct AP
  fetch, no syndication mirror (La Nación 404'd), and no search-engine
  snippet of a usable AP figure either. **A new fallback tier was used
  successfully for the first time: a direct fetch of a named market-review
  site (Investrade), cross-checked against an ETF proxy (IWM vs. Russell
  2000) and two independent live-blog corroborations (CNBC, TheStreet), with
  every figure reconciled arithmetically against the prior edition's own
  logged closes.** All four index figures reconciled exactly off the given
  Wednesday baseline, giving high confidence despite no AP/Reuters/
  syndication-mirror source being available at all. One competing secondary
  source (247wallst) gave slightly different S&P/Dow figures and was
  disclosed, not used. **Treat "market-review site + ETF-proxy + multi-blog
  corroboration + arithmetic reconciliation" as an acceptable fallback tier,
  roughly equivalent to the existing "search-snippet recovery" tier, when
  AP/Reuters/syndication mirrors are all unavailable** — this is now a
  second genuinely distinct recovery path beyond the syndication-mirror and
  search-snippet methods already documented.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. **Edition 43 caught two further instances of this pattern on
  analyst/driver commentary rather than price data**: a Barclays
  Dell/HPE/NetApp downgrade note was mis-dated to 15 October by several
  secondary sources but was confirmed (via convergent dating across four
  independent outlets) to actually be dated 14 October — Thursday's
  continued declines in both names were correctly treated as a continuation
  of Wednesday's selloff, not a fresh Thursday catalyst. Separately, a
  MarketBeat "Fastly shares climb 4.9%" piece that superficially looked
  Thursday-relevant was confirmed dated 13 October and excluded. **Always
  check a dated article's own body text/URL/dateline against the session
  being reported, regardless of how prominently a secondary aggregator
  displays today's date.**
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  **Edition 43 is the clearest evidence yet that this needs to happen EVERY
  edition, not just when something looks surprising**: six of eleven
  commodity/FX/Treasury instruments (WTI, Henry Hub, gold, EUR/USD, GBP/USD,
  USD/JPY) showed a Wednesday base that had silently shifted since the prior
  edition logged it — see the Standing Facts entry above for the full
  write-up. **Broaden the standing guidance once more: assume by default
  that any given edition's commodity/FX/Treasury prior-close base will NOT
  match what the previous edition logged, fetch each one fresh every time,
  and disclose every divergence found rather than treating a clean match as
  the norm and a divergence as the exception.** The CBOE vol-complex feed's
  two documented bugs (duplicate `prev_day_close`, and `price_change_percent`
  dividing by current price instead of prior close) were **ABSENT again at
  edition 43 — a fourth consecutive clean edition (40-43)**. This does NOT
  mean the bugs are fixed: they are genuinely intermittent. Always compute
  day-over-day % change manually as `price_change ÷ (current_price −
  price_change)` and treat the feed's own `price_change_percent` field as
  unreliable until checked each time regardless.
- **The DXY-vs-its-own-FX-crosses conflict did NOT recur at edition 43** — see
  Standing Facts entry above. Continue disclosing the DXY-vs-USD/JPY
  directional comparison explicitly every edition regardless of which way it
  goes.
- **The Kitco live-spot-vs-headline conflict (first logged edition 42)
  RECURRED at edition 43, in the opposite direction** — see the Standing
  Facts entry above for the full write-up. This is now confirmed a
  genuinely recurring, bidirectional trap for Kitco's live spot ticker
  specifically, not a one-off. Keep checking Kitco's live quote against its
  own published headline every edition and trust the headline-aligned
  (futures) figure when they conflict.
- **GBP/USD's data-quality problem has now stayed resolved for seven further
  editions (37-43)**, with edition 43 again single-sourced cleanly to
  Investing.com's close-to-close history table (computed +0.58%, off a
  freshly-fetched, revised Wednesday base — see the broadened vendor-revision
  trap above; this is a base-revision disclosure, not a same-day conflict).
  Resume the fuller multi-source method if a fresh same-day conflict
  reappears.
- **The 2-year Treasury yield conflict from edition 36 has stayed resolved
  for seven further editions (37-43)** — edition 43 again fetched both the
  TextView and CSV endpoints directly and found them in full agreement (2-yr
  4.77%, 10-yr 5.10%, 30-yr 5.43%, all 15 Oct — a broad rally, 2s10s
  narrowed to 33bp from 37bp, mild bull flattening). The Wednesday base
  matched edition 42's logged figures exactly — Treasuries are the one
  commodity/FX-adjacent instrument that did NOT show the vendor-revision
  trap at edition 43. Treat as resolved/noise unless a fresh conflict
  appears.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done.** Editions 33 through 43 have all run clean (or
  clean after one quick fix) — **edition 43 drafted clean at 46/50 on the
  first pass (four Annex-B-only orphans — a disclosure-box outlier citation,
  a Huang-remarks secondary source, a bls.gov schedule citation, and the
  edition-42-baseline self-citation — all caught and given inline citations
  before render)**, consistent with the pattern of needing one quick fix pass.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 43 have all rendered clean at zero tildes** on the
  first check. **Reminder: `grep -c` exits with status 1 (not 0) when the
  count is zero, since no lines matched — don't chain it with `&&` into a
  longer command and assume a silent failure means the check itself failed;
  read the printed count, not just the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 34 and edition 39 both
  resolved this cleanly for CFTC CoT, with full OI and Asset-Manager/
  Leveraged-Funds breakdowns for ES, NQ and RTY. **The next CFTC report was
  due Friday 16 October 2026, 3:30pm ET, covering Tuesday 13 October data —
  this did NOT fall inside edition 43's window** (its research cutoff,
  Thursday 15 Oct 20:21 ET, is before Friday's 3:30pm release), re-confirmed
  by directly checking cftc.gov's financial-futures page, which still served
  the 9 Oct release at edition 43's fetch. **This report should land inside
  edition 44's window instead** (whichever edition covers Friday 16 October
  and/or the following weekend) — check cftc.gov directly at edition 44 and
  expect to finally pull genuinely fresh data this time, since Friday's
  3:30pm ET release will be well in the past by any plausible edition-44
  cutoff.
- **A genuinely new editorial lesson surfaced at edition 43, worth
  internalizing for any future high-earnings-volume session: a long,
  verbose single-stock-movers table (15 rows, several with multi-clause,
  multi-citation driver text wrapping to two lines each) can by itself push
  the whole document from a clean 4-page render to 5 pages, even when every
  individual section's prose is otherwise reasonably tight.** Edition 43's
  first render came out at 5 pages with the one correct pagebreak present
  (confirmed via `grep -n pagebreak`) — a genuine content-overflow case, not
  a stray break. The fix, in order of what worked: (1) merge movers-table
  rows that share an identical driver into one combined row (e.g. "NVDA /
  AMD" with both % figures in one cell, "DELL / HPE" similarly) rather than
  repeating the same driver sentence twice; (2) cut driver-cell text to a
  single clause/line wherever possible, moving fuller color into the prose
  paragraphs below the table instead of duplicating it in both places; (3)
  only as a last resort, trim the day-ahead table's row count (merging two
  minor same-week releases into one row) and shorten sector-setup bullets.
  Re-rendering after step (1)+(2) alone was enough to reach a clean 4-page
  render with no further CSS changes needed — **prefer trimming/merging
  redundant movers-table content over loosening CSS** when a
  high-single-stock-volume session threatens the page budget; the tightened
  CSS baseline itself was not the problem this time.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at edition 43 (Ericsson +11.80% vs. Intuit +6.36%, about 1.86x), left
  uncapped. Edition 30 remains the one genuine 10x+ case to date. No need to
  revisit the threshold or mechanism absent a genuinely new edge case.
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists.** Editions 40 through 42 all hit the
  empty-result pattern (three consecutive empty editions). **Edition 43
  broke that streak**, single-sourced to one aggregator (The Globe and
  Mail's "US Analyst Updates: October 15th, 2026" roundup, disclosed as such)
  with four named actions with clear targets (Albertsons double-downgrade,
  Casey's General Stores target trim, American Axle downgrade, Brighthouse
  Financial upgrade) — none at large-cap scale within this report's bias
  sectors. The pattern across 37-43 (empty, thin, normal, empty, empty,
  empty, thin-but-real) continues to look genuinely intermittent — report
  whatever a genuine search attempt turns up each edition.
- **A non-GAAP-vs-GAAP EPS conflict trap was logged for the first time at
  edition 38** — when a secondary-sourced EPS figure conflicts sharply with
  a primary filing's GAAP number without a stated basis, prefer the primary
  filing and flag the secondary figure in Annex A. **Edition 43 logged
  another clean non-trap confirmation of the contrasting, legitimate
  pattern**: Charles Schwab's own 8-K disclosed both GAAP EPS ($1.62) and
  adjusted EPS ($1.69, excluding $151mn of transaction-related costs)
  clearly labelled by the company itself — reported in full per the Delta/
  JNJ/UnitedHealth/Bank of America precedent, not treated as a conflict.
- **The EPS-consensus currency/share-basis trap first logged at edition 39
  (TSMC specifically) reconciled CLEANLY at edition 43** — TSMC's Q3 diluted
  EPS of NT$29.43/ordinary-share, multiplied by the ADR ratio (1:5), equals
  exactly the stated US$4.60/ADR figure the company itself reported; no
  currency/basis conflict this quarter. The general principle (check
  currency and per-share basis before treating a cross-source EPS gap as a
  genuine conflict) remains standing guidance for any future multi-listed
  name, even though TSMC's own specific instance is now resolved.
- **The "preview-consensus-only miss/beat framing" caution (first logged at
  edition 41, followed up without resolution at edition 42) was NOT actively
  re-chased at edition 43** — neither JPMorgan's $5.57 EPS "miss" framing nor
  the Wells Fargo/Citigroup credit-provision-rationale inference was
  revisited this round; both remain open, unconfirmed disclosed inferences
  carried forward from edition 42 without new information. Pick this thread
  back up at a future edition if bandwidth allows, but do not claim
  resolution that didn't happen.
- **Two new open single-stock-driver threads from edition 43, replacing
  Fastly (now closed — see below):** GE Vernova's Wednesday 14 Oct -6.20%
  decline remains fully unexplained after a second genuine search attempt at
  edition 43 (a same-day AI-datacenter gas-power deal with Venture
  Global/Baker Hughes was found for Thursday, but GEV fell despite, not
  because of, that news — the original Wednesday move itself is still
  unexplained). Rocket Lab's Thursday 15 Oct -6.64% decline also has no
  confirmed driver — a Neutron-launch-delay claim circulating in secondary
  coverage could not be dated to 15 October specifically. **Keep searching
  for delayed drivers on both at edition 44.**
- **Fastly's unexplained-mover streak — RESOLVED/CLOSED at edition 43, do not
  carry forward as an open thread.** After four consecutive unexplained
  sessions (edition 39's +15.86% spike through edition 42's -7.72%), Thursday
  15 October was a quiet, market-consistent +0.28% move with no driver search
  forced — the streak simply ended rather than being explained, which is an
  acceptable resolution per standing practice (a name reverting to
  unremarkable, in-line moves does not require a retroactive explanation for
  the earlier unexplained swings). Do not re-open unless a fresh large,
  unexplained Fastly move recurs.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly. Note the correct symbol format requires a leading
  underscore in the path (e.g. `_VIX.json`) — a bare `VIX9D.json` etc.
  returns 403 AccessDenied. **Editions 28 through 43 all got a full clean
  sweep** — sixteen consecutive clean sweeps now. **Edition 43 fetched all
  six series via raw `curl`, byte-for-byte, not tool-paraphrased, for the
  first time in several editions** — prefer this method going forward when
  feasible, since a tool-summarized fetch cannot rule out a silently-
  collapsed duplicate key. **The feed's two known intermittent bugs (a
  duplicated `prev_day_close`, and a `price_change_percent` that divides by
  current price instead of prior close) were ABSENT again at edition 43** —
  a fourth consecutive clean edition (40-43). Always compute day-over-day %
  change manually regardless of how many consecutive clean reads preceded
  the current one. **The VIX9D-vs-spot-VIX front-end inversion widened to
  -2.49 at edition 43, reversing the three-edition narrowing trend (39→42:
  -3.58→-3.53→-3.28→-2.28)** — not confirmed as a monotonic trend either
  way, keep watching rather than assuming continuation in either direction.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs — the standing default for
  the sector table, and (absent fresher CoT data) chart #2. **Edition 43
  again used the sector-ETF-proxy chart #2 default** (8 of 11 sectors green:
  Health Care +1.86%, Materials +1.79%, Cons. Discretionary +1.71%, Comm.
  Svcs +1.46%, Financials +1.38%, Real Estate +1.21%, Cons. Staples +0.72%,
  Industrials +0.51% the gainers; Utilities -0.17%, Technology -0.65%,
  Energy -1.58% the three laggards) — no fresh CFTC data was due this window
  as expected. **Edition 44 should check cftc.gov's schedule directly
  first** — the Friday 16 Oct CFTC report should have posted by any
  plausible edition-44 cutoff, which would end the sector-ETF-proxy default's
  current nine-edition run (35 through 43).
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable for
  the formal table; the "X of 11 sectors closed higher" sector-ETF read
  remains the best available breadth proxy (8 of 11 at edition 43, up from 3
  of 11 at edition 42's CPI-driven lopsided split) — continue treating an
  uncorroborated single-aggregator breadth figure as not usable.
- **Dealer gamma:** zerogex.io hit a **FOURTH distinct/hybrid failure mode**
  at edition 43: the front-end still shows the edition-42 populated-shell
  placeholder-dash pattern (no timestamp, no error text), but API probing
  this time found a MIX of responses across endpoints — `/api/gex` still
  404s (matching edition 42), while a more specific ticker-scoped path
  (`/api/gex/spx`) reverted to the edition-40/41 401 auth-required response.
  **zerogex now carries four separate documented failure modes across four
  consecutive editions (38-39 stale/inconsistent timestamps; 40-41 auth-
  gated blank pages; 42 populated-shell placeholder dashes; 43 a hybrid of
  42's front-end plus a mix of 40/41-style and 42-style API responses)** —
  do not assume any prior failure mode is the stable baseline; the shape has
  now changed on every single edition it's been checked. SpotGamma remains
  untried as an alternative per standing practice (it has failed for many
  editions).
- **Official CME FedWatch probabilities:** the page blocks fetching (edition
  43's direct attempt timed out again, same pattern as editions 41-42) — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. DeFi
  Rate's Kalshi/Polymarket-blended aggregator remains a stable, consistently
  working source across editions 37-43.
- **Kalshi direct fetch:** rate-limited across every edition it has been
  attempted, now **seven consecutive failures (37-43)** — a confirmed
  structural gap, not transient. Resume the attempt-every-edition discipline
  at edition 44 regardless, but expect a block of some kind. Use Kalshi's
  own secondary reporting or DeFi Rate's blended aggregator as the
  workaround.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) failed again at
  edition 43 (403, as expected — not re-attempted as primary since edition
  35 beyond a routine confirming try). **Westmetall.com has now worked
  cleanly TWENTY-TWO editions running** as the fallback (copper -1.44% to
  $14,539.00/tonne at edition 43, Wednesday base matched edition 42's logged
  figure exactly — the one commodity/FX instrument besides Treasuries that
  did NOT show the vendor-revision trap this edition).
- **Official Treasury par yields:** home.treasury.gov's official daily
  par-yield-curve CSV and the rendered HTML TextView page **agreed cleanly
  again at edition 43** (2-yr 4.77%, 10-yr 5.10%, 30-yr 5.43%, all 15 Oct),
  extending the clean streak to **eight editions (37-43, plus 39's
  confirmation)** with no repeat of the edition-36 33bp gap. Keep fetching
  both endpoints and comparing rather than trusting either by default.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` works well for equity index
  futures (ES/NQ/RTY); the legacy CFE report carries VIX futures
  positioning. Latest available data remains edition 39's Friday 9 Oct pull
  (covering Tuesday 6 October): ES OI 1,932,227 (Asset Mgr net +46.93% of
  OI, Leveraged Funds net -21.48%); NQ OI 283,586 (Asset Mgr net +26.03%,
  Leveraged Funds net -6.78%); RTY (full-size) OI 425,152 (Asset Mgr net
  +10.70%, Leveraged Funds net -24.77%). **The next report, due Friday 16
  October 2026 3:30pm ET covering Tuesday 13 October data, was re-confirmed
  directly at edition 43 as NOT yet posted** (cftc.gov's financial-futures
  page still served the 9 Oct release; edition 43's research cutoff,
  Thursday 15 Oct 20:21 ET, falls before Friday's release time). **This
  report should land inside edition 44's window — check cftc.gov directly
  and expect genuinely fresh data this time.**
- **GBP/USD and EUR/USD clean close:** both remain fully resolved since
  edition 37/26 respectively. **Edition 43 single-sourced both to
  Investing.com's close-to-close history table again** (EUR/USD +0.50%,
  GBP/USD +0.58%, both off freshly-fetched, revised Wednesday bases — see
  the broadened vendor-revision trap in Standing Facts) — no same-day
  conflict found, consistent with the lighter-touch approach used since
  edition 39.
- **Gold/silver clean close on a non-event day:** USAGOLD remains a confirmed
  permanent standing gap, not attempted since edition 39. **Kitco's live
  spot quote conflicted with its own published headline for a SECOND
  consecutive edition at edition 43, this time in the opposite direction**
  (see Standing Facts and Hard Rules above for the full write-up) — now
  firmly established as a recurring, bidirectional trap, not a one-off. Gold
  and silver futures continue to source cleanly via Investing.com, subject
  to the broadened vendor-revision caveat (gold's Wednesday base was
  revised at edition 43; silver's was not).
- **China CPI/PPI (monthly):** resolved for September — see Standing Facts
  above, closed thread. **US import/export prices and industrial
  production:** BLS's own schedule confirmed again (via direct
  `bls.gov/schedule/2026/10_sched_list.htm` fetch) at edition 43: **Import/
  Export Price Indexes Fri 16 Oct 8:30am ET** (falls just after edition 43's
  window, lands in edition 44's), **Q3 Employment Cost Index Fri 30 Oct
  8:30am ET**. **University of Michigan final October consumer sentiment**
  (see Standing Facts above): due 23 October 2026 — watch for it.
- **Henry Hub natural gas:** the November contract (NGX6) has NOT rolled to
  December as of edition 43 (still front-month). **The vendor-revision
  wrinkle has now escalated to a THIRD conflicting figure for Wednesday 14
  Oct's base** — see the dedicated Standing Facts entry above for the full
  write-up; this is now a four-edition-running (40-43) data-quality issue
  specific to this instrument, more severe than any other commodity/FX
  vendor-revision case logged to date. Still not labeled an official CME
  settlement print by any vendor checked.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. **Edition 43 found no notable
  Thursday-dated single-stock options-flow/skew commentary for TSMC,
  Netflix or the broader chip-read-across names** — a seventh consecutive
  empty edition on this general sub-item (37-43). Treat this sub-item as
  reliably low-yield and keep it a brief, secondary effort each edition.
- **Weekend equities catalyst to watch: 13F filings** (Q1 approx. May 15, Q2
  approx. Aug 14, Q3 approx. Nov 14, Q4 approx. Feb 14) — factor into a
  Monday-briefing lead by default when the window includes one. Not
  applicable through edition 43; next due approx. 14 November 2026.
- **A historical-average FOMC-day move benchmark** has not yet been sourced
  in any edition to date (tried and failed at edition 22). Not attempted
  again through edition 43.
- **CFTC total open interest by instrument/date:** fully resolved at edition
  34 for ES, NQ and RTY in one pull from cftc.gov, repeated successfully
  again at edition 39; not re-attempted at editions 40 through 43 since no
  new report was due in any of those windows. Repeat this full
  three-instrument fetch at edition 44, when the Friday 16 Oct report should
  finally be available — watching for the Micro-vs-full-size Russell naming
  trap each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear.** Editions 40
  through 42 all reverted to the empty-result end of the range. **Edition 43
  found a normal-ish, if thin, result**: four named actions with clear
  dollar targets (Albertsons $14/$13, Casey's General Stores $825, American
  Axle $5, Brighthouse Financial $55), single-sourced to one aggregator
  roundup. The pattern across 37-43 (empty, thin, normal, empty, empty,
  empty, thin-but-real) continues to look genuinely intermittent rather than
  a structural change.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance.** No new instance of this specific trap hit any NAMED
  mover's price at edition 43 — every price cited traced to
  stockanalysis.com's own history tables, cross-checked where a driver
  required independent corroboration.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. **Figsize should scale to
  the chart's category count, not use one fixed size for everything.** Use
  `(9.8, 1.95)` as the ceiling for an 11-category sector-ETF-proxy panel
  (confirmed clean at editions 37 through 43, seven straight) — this remains
  correct for 10-11 categories specifically. For charts with fewer
  categories, scale the height down: roughly `(9.8, 1.65-1.85)` for
  3-8 categories. **Edition 43 used `(9.8, 1.8)` for an 8-category
  single-stock movers chart** (HPE, DELL, RKLB, NFLX, CRWV, NOW, INTU, ERIC)
  and reused `(9.8, 1.95)` for the 11-category sector panel, both with
  `pad_frac=0.24`, both rendered cleanly on the first attempt with no label
  overlap — a further confirmation of the established pairing, now across
  three consecutive editions (41-43) using the identical `(9.8, 1.8)`/
  `(9.8, 1.95)`/`pad_frac=0.24` combination for 8-category and 11-category
  charts respectively. **Always render and visually inspect (via the Read
  tool) the actual PNG at or near full resolution before embedding it**,
  regardless of what a past edition's success might suggest.
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
  wrong. **A 5-page render is not always a stray break** — edition 43 hit 5
  pages with only the one correct pagebreak present; the cause was genuine
  copy overflow (a verbose 15-row movers table), fixed by merging
  same-driver rows and tightening driver-cell text rather than touching CSS
  — see the dedicated Hard Rules entry above for the full lesson. **A large,
  suspicious blank area at the bottom of a page (as opposed to a page that's
  merely a bit short) is usually caused by an atomic block** — most often a
  chart `<img>` — not fitting in the remaining space and being pushed whole
  to the next page. Edition 43's overflow looked different from this
  pattern (the orphan page-4 content was simply the tail end of a table plus
  bullets that had nowhere left to go on page 3, not a single pushed block)
  — both failure shapes are worth distinguishing when diagnosing a 5-page
  render.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. Plain-`<tr>` tables reflow across a page
  break safely — this is expected behavior, not a bug to fix.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  A visibly short page 3 has recurred at several earlier editions, each
  needing a genuinely additive fix (never a padding table that just repeats
  an existing table's rows). **Edition 43 hit the opposite problem (overflow,
  not shortfall) and needed a genuinely subtractive fix instead** — trimming
  and merging table content, not adding it. Check for both failure modes
  (short page 3, overflow to 5 pages) after every render regardless of
  recent-edition track record; which one you'll hit depends heavily on the
  session's single-stock-earnings volume.

### Working settings (current baseline — retightened at edition 39 under
genuine evidence of overflow; confirmed stable across editions 40 through
43's very different content volumes (40 needed a padding table to fill page
3, 41 and 42 both filled naturally with no padding needed, 43 needed a
content TRIM to avoid overflow on a very high single-stock-volume session).
Treat as the durable default; the lever to pull on a high-volume day is
merging/trimming redundant table content, not loosening the CSS further.)
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
  doesn't fill the page. **On a high-single-stock-volume earnings day (many
  reporters/movers in one session), the opposite problem is more likely —
  watch the movers table specifically for verbosity (multi-clause driver
  text, rows that could share a combined cell) before assuming the page
  budget is safe.** Always re-render immediately after adding (or removing)
  any content to confirm the page count, rather than assuming a change is
  safe.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across nineteen eligible
editions, 25 through 43, with editions 34 and 39 the exceptions when fresher
CFTC data was available). Fresh CFTC CoT data on a Monday/weekend-window
edition → the ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart,
normalized as % of open interest. **Edition 44 is the most likely candidate
in a long while to finally break the sector-ETF-proxy default's run** — the
CFTC report due Friday 16 Oct (covering Tue 13 Oct) should be posted by any
plausible edition-44 cutoff; check cftc.gov's freshness first before
assuming either chart type by default. A single dominant earnings print with
a clean, well-sourced implied-vs-realized-move story → a three-bar implied/
historical-average/realized move chart (the historical-average leg has never
actually been sourced successfully). A genuine multi-sector broadening/
deepening selloff across consecutive sessions → the sector-ETF proxy
rendered as a grouped (day-over-day) bar instead of single-day. A holiday-
window preview edition with no fresher data → VIX futures term structure
with event annotations. When chart 1 (movers) already covers the earnings/
single-name story, the sector proxy is a good complementary choice even on a
stock-heavy day, since the two stories reinforce rather than duplicate each
other — **edition 43 used an 8-ticker earnings/AI-infra-rebound-driven
movers chart for chart 1 and the sector-ETF proxy for chart 2, continuing
the same complementary pairing used at editions 41-42** (the sector chart
told the broader defensive-rotation story the single-name chart alone
couldn't). Chart #2's placement in the document should follow its content,
not a fixed section — editions 24, 34 and 39 all placed a CFTC/positioning
chart #2 in Section 5 (Derivatives) rather than Section 2; editions 35
through 43, all back on the sector-proxy default, placed it back in its
usual Section 2 spot. **Remember the figsize-scales-to-category-count
guidance above (ceiling `(9.8, 1.95)` for an 11-category panel, scale down
for fewer categories) regardless of which chart type is chosen.**

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–41 (condensed):** established the format (edition 1 baseline;
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
15-16 FOMC meeting and its aftermath (editions 21-23):** the Fed hiked 25bp
to 3.75%-4.00% unanimous 12-0, equities reversed hard then rallied sharply;
BoE held at 3.75% (6-3). Edition 24: approx. $7tn September triple-witching
notional expired, Xenon Pharmaceuticals -30.7%, Buffett stepped down as
Berkshire chairman, BoJ hiked to approx. 1.25% (31-year high). Edition 25:
chip rally to a then-record Nasdaq. Edition 26: financials-led rotation, a
genuine Kitco-vs-USAGOLD gold split (later resolved). Edition 27: risk-off on
a 19-year 10-year yield high. Edition 28: a whipsaw near-flat session, MGM
-10.99% on a withdrawn take-private bid, Trump-Xi summit extended the
US-China trade truce. Edition 29: relief rally, the US-China $30bn
tariff-cut agreement first reported. Edition 30: broad risk-off on a
rejected Iran Hormuz offer, Kodiak Sciences +177.96% (the movers-chart
capping rule's first genuine case). Edition 31: DXY-vs-FX-crosses conflict
resolved cleanly. Edition 32: a volatile round-trip close, gold spot/futures
split (later converged). Edition 33: yields drove the session on a hot ISM
Prices Paid print, an AI-infra earnings cluster, Nike missed FQ1 guidance
(resolved edition 34); the document overflowed to 5 pages, needing five trim
rounds. Edition 34 (Mon 5 Oct, covering Fri 2 Oct + weekend): a badly-missed
September jobs report drove a broad risk-on rally and sharp October-hike-odds
collapse; a fresh CFTC CoT report powered the first ES/NQ/RTY positioning
chart. Edition 35 (Tue 6 Oct): two same-day cash buyouts (PTC Inc, RXO Inc)
drove the tape; equities hit a Nasdaq Composite record; September ISM
Services PMI printed hot; two new sourcing traps logged (stale price-target
recirculation, a stock-split "+96%" artifact). Edition 36 (Wed 7 Oct):
equities extended records on falling yields (clean rate-sensitive rotation);
two severe sourcing traps hit (fabricated AMD price targets, an unverifiable
WHO claim, both rejected); the Paramount Skydance/Warner Bros. Discovery
merger closed (ticker SKYD); a secondary source reversed the US-China tariff
list-size assignment (resolved edition 37); the 2-year Treasury hit a 33bp
cross-endpoint gap (resolved edition 37); GBP/USD hit a three-way conflict
(resolved edition 37). Edition 37 (Thu 8 Oct): the FOMC minutes showed a
unanimous 12-0 September hike but only "most" backing a further 2026 move;
equities retreated on a bond-market selloff; three standing conflicts all
resolved this edition; WTI and Brent both hit a sharp level-vs-%-change
reconciliation failure; a chart-layout bug was found and fixed (panel2
figsize bumped to `(9.8, 1.95)`). Edition 38 (Fri 9 Oct): equities fell a
second straight session but breadth stayed strong; a second straight
AI-optics profit-taking session; Applied Digital's blowout print drew a
muted reaction and logged the first non-GAAP-vs-GAAP EPS conflict trap; a
primary-source breakthrough closed BoJ's last standing gap; oil's
vendor-%-reconciliation failure became well-established; zerogex logged
three within-session anomalies as a new data-quality trap. Edition 39 (Mon
12 Oct, covering Fri 9 Oct + weekend): SpaceX's approx. $8bn spectrum
purchase rattled telecom but equities shrugged it off, closing a
record-setting week; a parallel biotech rally ran alongside it; Delta's 8-K
cleanly disclosed both GAAP and adjusted EPS; Goldman upgraded Palantir, the
first normal analyst-action result after two near-empty editions; a
chart-sizing refinement and deliberate CSS retightening were needed to fix a
genuine 5-page overflow. Edition 40 (Tue 13 Oct, covering Mon 12 Oct,
Columbus Day): a value/growth split on renewed memory-chip/AI-hardware
weakness; AP's wire needed search-snippet recovery; oil delivered its
cleanest-ever dual-grade reconciliation (later found to rest on a Monday
base itself retroactively revised); zerogex's SPX gamma hit a harder
auth-gated/blank failure mode; a chart-label pad_frac bug was found and
fixed (raised to 0.26); a short-page-3 recurrence was fixed with a new
Treasury-yield-curve table. **Edition 41** (Wed 14 Oct, covering Tue 13 Oct,
the opening day of Q3 bank/healthcare earnings season): JPMorgan, Goldman,
Wells Fargo, Citigroup, UnitedHealth and Johnson & Johnson all reported;
JNJ's GAAP EPS collapsed to $0.09 on a one-time talc-settlement charge while
adjusted EPS and raised guidance were both disclosed cleanly; equities
finished essentially flat (S&P -0.02% to 7,805.45) via a clean AP wire
recovered through two syndication mirrors; Bumble's unexplained +56.58%
surfaced (resolved edition 42: a $1.3bn Ithaca Holdings buyout, not a
split); the AI-optics/AI-hardware selloff cluster finally found its delayed
driver (Broadcom CEO Hock Tan's remarks on AI-infrastructure capital-access
constraints); a new vendor-retroactive-revision trap hit WTI, Brent and
Henry Hub for the first time. 49 sources, clean 49/49 on the first
`check_refs.py` pass, zero stray tildes, clean 4-page render.

**Edition 42 (condensed)** — Thursday 15 October 2026 report covering
Wednesday 14 October 2026. September CPI printed hot (headline +0.6% m/m/
+3.7% y/y, core +0.3%/+2.6%), triggering the broadest risk-off session in
weeks (S&P -1.11% to 7,718.94, Nasdaq -1.88%, Russell -1.90%) with a sharp
defensive rotation (Health Care/Staples led, Tech lagged, only 3 of 11
sectors green); the Dow held almost flat (-0.09%). AP's wire 403'd again;
closes recovered via CNBC/Yahoo/TheStreet and reconciled arithmetically.
Bank of America's GAAP EPS fell to $1.08 on a $1.2bn regulatory-settlement
charge (adjusted approx. $1.25, both company-disclosed); Morgan Stanley beat
cleanly on EPS and revenue but still fell with the market. CoreWeave
(-15.46%) and Oracle (-8.83%) led single-stock decliners on renewed
AI-infrastructure-funding-stress; Fastly (-7.72%) and GE Vernova (-6.20%)
both went unexplained. Bumble's buyout mystery resolved (Ithaca Holdings,
$6.05/share, confirmed via 8-K, not a split). No analyst action dated to 14
October was found for any name. Rate-path odds repriced sharply hawkish on
the CPI print (DeFi Rate: Oct hike approx. 19%→29%, Dec approx. 78%); a
conflicting Seeking Alpha 49.3% CME-FedWatch-attributed claim could not be
verified. China's September CPI/PPI finally posted (CPI +0.9% y/y, PPI
+5.0% y/y) via gov.cn's English NBS release after stats.gov.cn failed again.
The US shutdown/funding re-confirmation regressed to secondary-only this
edition. Commodities swung hard: silver futures -6.14% (the sharpest
single-session commodity move logged all cycle), gold futures -1.06%, both
contradicted by a mistimed Kitco live spot quote conflicting with Kitco's
own headline — a new sourcing trap. The Treasury curve flattened (2-yr +3bp
to 4.82%, 10-yr -2bp to 5.19%, 30-yr -4bp to 5.52%). The vendor-
retroactive-revision trap broadened further (WTI, Henry Hub revised again;
for the first time hit FX — EUR/USD, GBP/USD, USD/JPY all drifted). The DXY-
vs-USD/JPY divergence pattern resumed after a 3-session pause. The VIX
complex spiked hard (VIX +10.48% to 16.87, VIX9D +21.68%, VVIX +10.62%) with
neither CBOE feed bug recurring despite the large move. zerogex hit a third,
distinct failure mode (populated page shell, all-placeholder values). CFTC
CoT confirmed no fresh data as expected. 49 sources, clean 47/49 on the
first `check_refs.py` pass (two Annex-B-only orphans fixed), zero stray
tildes, clean 4-page render on the first attempt.

**Edition 43 (most recent — full detail)** — Friday 16 October 2026 report
covering Thursday 15 October 2026, the window's one NYSE session, research
window Wed 14 Oct 2026 20:00 ET through Thu 15 Oct 2026 20:21 ET. Verified
the two structural header rules again — now clean across eleven (date-line)
and fifteen (window-line) consecutive applicable editions respectively.

**A second straight blowout inflation print (September PPI, +1.3% m/m/+6.3%
y/y, the hottest since March 2022) landed hours after Wednesday's hot CPI**,
confirmed directly against bls.gov; notably, Fed rate-path odds barely moved
(DeFi Rate: Oct hike approx. 28%, essentially flat vs. Wednesday's post-CPI
approx. 29%), a genuine non-reaction worth flagging. **An overnight
memory-chip rout (Kospi -8%) dragged the Nasdaq down as much as approx.
1.9% intraday before a sharp reversal**, fed by Nvidia CEO Jensen Huang's
on-record defense of CoreWeave's balance sheet (5-year CDS at a record
1,194.5bp) — all four major indices closed green (S&P 500 +0.33% to
7,744.10, Dow +1.08% to 52,177.81, Nasdaq Composite +0.08% to 26,713.03,
Russell 2000 +1.38% to 2,767.28), recovered via a new fallback sourcing tier
(Investrade market-review + ETF-proxy + multi-blog corroboration) after AP's
wire was unavailable with no syndication mirror either. The Dow's
outperformance reflected a clean defensive/value rotation (8 of 11 sector
ETFs green, Health Care/Materials led, Energy/Technology lagged). **TSMC
delivered a record Q3** (EPS $4.60/ADR, sixth straight record-profit
quarter, FY26 revenue guide lifted to "slightly above 40%," capex raised to
$60-64bn, beating on every line and reconciling cleanly on the
currency/share-basis check first flagged at edition 39) yet fell again on
cautious 2027 management commentary, dragging Nvidia and AMD lower too
before a partial recovery on Huang's remarks. CoreWeave (+5.94%) and Oracle
(+3.00%) partially rebounded off Wednesday's AI-infrastructure-funding-
stress selloff. Software snapped back on falling yields (Intuit +6.36% on
an acquisition announcement, ServiceNow +6.14% on a product launch) while
hardware extended Wednesday's Barclays-downgrade-driven selloff (Dell
-6.80%, HPE -7.10%, correctly dated to Wednesday despite several secondary
sources mis-dating it to Thursday). Bank earnings extended the "beat yet
fall" pattern to a fourth session: Charles Schwab's 8-K cleanly disclosed
both GAAP ($1.62) and adjusted ($1.69) EPS (not a GAAP/non-GAAP trap) with a
Bloomberg-confirmed deposit/NIM miss driving the stock down -2.73% despite
the beat; U.S. Bancorp beat cleanly and rose +2.01%. Ericsson's Q3 6-K beat
drove a +11.80% spike, the session's largest single-stock move. GE Vernova
(-1.63%) fell despite a reported up-to-$17.2bn AI-datacenter gas-power deal
— Wednesday's original -6.20% driver remains unexplained. Rocket Lab fell
-6.64% with no confirmed driver. Fastly's four-session unexplained-mover
streak ended quietly (+0.28%, closed as a resolved thread). Analyst actions
broke a three-edition empty streak with a thin, single-aggregator-sourced
result. Standing facts all re-verified unchanged except the government
shutdown/funding check, which was RESTORED to a clean direct-primary-source
footing after a two-edition regression, and a correction to a prior edition's
framing: New Mexico v. Meta's expected "approx. 22 Oct" ruling date could not
be corroborated — the actual hearing was 1 Oct, with a ruling only expected
"later in October," no specific date confirmed. Commodities/FX reconciliation
work broadened significantly: six of eleven instruments (WTI, Henry Hub,
gold, EUR/USD, GBP/USD, USD/JPY) showed a Wednesday base that had shifted
again since edition 42 logged it; Henry Hub specifically now carries a THIRD
conflicting Wednesday reference point, its worst data-quality state yet;
Kitco's live-spot-vs-headline conflict recurred for a second edition, this
time in the opposite direction, confirming it as a genuine bidirectional
trap rather than a one-off. The DXY-vs-USD/JPY divergence did not recur this
time (both fell together). Treasuries rallied broadly (2-yr -5bp to 4.77%,
10-yr -9bp to 5.10%, 30-yr -9bp to 5.43%) and were the one instrument class
that reconciled perfectly clean against the logged Wednesday base. The VIX
complex retreated across the board on a full clean raw-fetch sweep (VIX
-2.43% to 16.46) with neither feed bug recurring, a fourth consecutive clean
edition; the VIX9D-vs-VIX gap widened to -2.49, reversing a three-edition
narrowing trend. CFTC CoT was confirmed NOT yet posted (expected inside
edition 44's window instead). Dealer gamma (zerogex) hit a fourth distinct,
this time hybrid, failure mode — still fully unusable. **A new editorial
lesson**: the first HTML draft rendered at 5 pages despite only the one
correct pagebreak (genuine content overflow from a verbose 15-row movers
table), fixed by merging same-driver rows and tightening driver-cell text
rather than touching the CSS baseline — re-rendered clean at 4 pages
afterward. 50 sources, clean 46/50 on the first `check_refs.py` pass (four
Annex-B-only orphans caught and given inline citations before render), zero
stray tildes.

**Open threads for edition 44:** GE Vernova's Wednesday 14 Oct -6.20% decline
remains unexplained after a second search attempt — keep trying. Rocket
Lab's Thursday 15 Oct -6.64% decline has no confirmed driver (a Neutron-
delay claim could not be dated to 15 Oct) — keep searching. Henry Hub
natural gas's Wednesday base now has three mutually conflicting figures
across sources — the worst data-quality state of any instrument logged to
date; keep disclosing rather than attempting to force a resolution. The
CFTC CoT report due Friday 16 Oct (covering Tue 13 Oct) should finally land
inside edition 44's window — check cftc.gov first and expect fresh data,
ending the sector-ETF-proxy chart #2 default's nine-edition run if it
posts. September import/export price indexes (Fri 16 Oct, 8:30am ET) also
fall just after edition 43's window — cover them at edition 44. Truist and
M&T Bank's actual Friday 16 Oct earnings were not yet reportable inside this
window — cover at edition 44. Results for Thursday's after-the-close
reporters (Alcoa, Interactive Brokers, J.B. Hunt, WaFd, Independent Bank
Corp) could not be located at edition 43 — check again at edition 44. New
Mexico v. Meta's ruling is still pending, expected "later in October" per
the 1 Oct hearing — watch for the actual date/ruling, don't re-cite a
specific date until confirmed. The FOMC's exact decision/press-conference
time (2:30pm ET, 28 Oct) has now failed to re-display on the Fed's own
calendar page for two straight editions — make a third direct attempt at
edition 44. The JPMorgan EPS-miss-framing and Wells Fargo/Citigroup
credit-provision-selloff-rationale threads from editions 41-42 were not
actively re-chased at edition 43 and remain open, unconfirmed disclosed
inferences — revisit if bandwidth allows. University of Michigan's final
October consumer-sentiment reading is due 23 October. Q3 Employment Cost
Index is due 30 October. The FOMC meets 27-28 October — the next edition to
fall on/after that date should lead with the decision. Threads closed after
resolution rather than carried further: Fastly's four-session unexplained-
mover streak (closed — ended quietly with a small, market-consistent move,
no retroactive explanation required); the government shutdown/funding
status check (closed — restored to clean direct-source footing, with a
confirmed-working whitehouse.gov URL pattern now documented for reuse); the
TSMC currency/share-basis consensus check (closed — reconciled cleanly this
quarter).
