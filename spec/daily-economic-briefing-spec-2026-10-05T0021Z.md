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
  is where the sessions covered belong, not the date line. **Editions 33 and 34
  both applied this correctly again** ("Friday 2 October 2026" and "Monday 5
  October 2026" respectively as the date line, with the window line carrying
  the session covered).
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30 and 32-33 reused the same
  pattern for single-session windows, and **edition 34 reused it again for a
  single-session-plus-weekend window** ("Window: Thu 1 Oct 2026 20:00 ET – Sun
  4 Oct 2026 20:21 ET (Fri 2 Oct close/AH, the window's one NYSE session, plus
  the weekend)") — now confirmed clean across six consecutive single-session or
  single-session-plus-weekend editions (29 through 34). No further confirmation
  needed; treat this as settled.

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
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 34
  directly against federalreserve.gov's own FOMC calendar page (Dec 8-9 is the
  next SEP meeting after that). The meeting is now about three weeks out —
  continue re-confirming every edition between now and then.
- **October-hike odds converged sharply at edition 34, closing the cross-venue
  divergence that had reopened at edition 33 — re-verify fresh every edition
  regardless:** a badly-missed September jobs report (nonfarm payrolls
  +29,000 vs. approx. 84,000-90,000 consensus; unemployment 4.2%, up from
  4.1%; July revised to an outright -10,000) landed Friday 2 Oct and drove all
  three venues to a tight band within the session: **Polymarket approx. 17%,
  Kalshi secondary citations approx. 16-18%, CME FedWatch secondary citations
  approx. 17-21.6%** — down from Thursday 1 Oct's 25-38% cross-venue split.
  This is the second time in two editions a single data print has driven a
  large, unified same-session repricing (August PCE at edition 32, the jobs
  report at edition 34) — do not assume this convergence is stable; re-verify
  the full range fresh every edition through the Oct 27-28 FOMC meeting. A
  secondary-sourced **December-hike-odds range (approx. 65% Kalshi to 75%+
  CME FedWatch) surfaced for the first time at edition 34**, unconfirmed
  against any primary venue — treat with caution and attempt a primary-venue
  check next time it's load-bearing.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch,
  rba.gov.au, etc.) every edition, exactly like any other data point. **Edition
  34 reconfirmed Kevin Warsh as Fed Chair directly against federalreserve.gov's
  Board of Governors bios page** — worth citing explicitly in copy when the
  Chair is referenced, not just carrying it silently.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026**, re-confirmed again at
  edition 34 directly against bankofengland.co.uk's own MPC-dates page — about
  four-to-five weeks out; re-confirm again next edition or two as it
  approaches.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus. **Edition 34 re-verified the current rate
  level directly against the Bank of Japan's own 18 Sept 2026 policy statement
  (not just the meeting-date page)**, closing the re-verification gap flagged
  at edition 33 — confirmed still approx. 1.25% (7-2 vote, effective 24 Sept).
  **The Bank of Japan's next policy meeting is confirmed for October 29-30,
  2026**, re-confirmed again at edition 34 — about three-to-four weeks out;
  re-confirm again next edition or two as it approaches.
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
- **September 2026 jobs report — closed thread as of edition 34, do not
  re-derive, but watch for revisions in later BLS releases:** nonfarm payrolls
  +29,000 (the weakest print of the cycle) vs. approx. 84,000-90,000
  consensus; unemployment rate 4.2% (up from 4.1%); average hourly earnings
  +0.1% m/m / +3.0% y/y; July revised from +21,000 to an outright -10,000,
  August revised from +162,000 to +133,000 (a combined -60,000 revision),
  confirmed directly against bls.gov's Employment Situation Summary. This was
  the single biggest catalyst of edition 34's window — see the October-hike
  odds entry above for the market reaction.
- **The US-China "30-for-30" tariff framework remains at the list-
  identification stage, unchanged since edition 30's primary-source
  confirmation** (re-checked fresh again at edition 34, no new implementation
  news found): USTR.gov and whitehouse.gov confirm a framework recommending
  reduced tariff treatment for $30bn of goods on each side (77 Chinese
  products, 1,600+ US products — edition 32 separately logged updated list
  sizes of 77/1,619 post-Trump-Xi-summit), administered via the new US-China
  Board of Trade. Still pending each side's domestic legal processes — watch
  for a formal implementation/effective date in a future edition.
- **No US federal government shutdown is in effect — re-confirmed again at
  edition 34, no change over the weekend:** a continuing resolution (H.R. 6500
  / P.L. 119-103), signed into law 2 September 2026, funds the government
  through **11 December 2026**, confirmed against whitehouse.gov,
  congress.gov CRS product R49353, and GovTrack.us. Watch for shutdown risk
  resurfacing as 11 December 2026 approaches, and note that whitehouse.gov
  also hosts a separate generic "Government Shutdown Clock" page whose content
  has previously described an active-shutdown narrative inconsistent with the
  dated CR evidence — treat that page as unreliable/stale rather than
  authoritative if it resurfaces.

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
  more consecutive citations. **A related trap surfaced at edition 28's own
  draft, worth naming explicitly: placeholder ref text (e.g. `[note1]`) typed
  during drafting and never swapped for a real number.** `check_refs.py`'s
  regex requires `\d+` inside the brackets, so a non-numeric placeholder like
  `[note1]` simply won't match either the inline or Annex-B regex — it won't
  show up as "missing" or "unused," it just silently doesn't count. **A near
  miss of the same species at edition 30's own draft: a citation typed as
  `[9b]`** (meant to disambiguate a second source keyed to item "9") also
  fails the `\d+` regex for the same reason as `[note1]` — caught before
  rendering by re-running `check_refs.py` and seeing the citation count come
  up short, fixed by assigning it a fresh plain integer instead. **Never use
  a letter suffix to disambiguate a citation — always mint a new integer.**
  **Edition 29 hit a related but distinct trap worth naming too: reserving
  Annex B numbers (e.g. `[32] (reserved)`) for sources planned but not used**
  — these show up as "listed but never cited" in `check_refs.py`'s output
  (correctly flagged that time), but the fix is to delete the unused
  placeholder entries outright rather than leave reserved gaps in the
  numbering; Annex B numbers do not need to be contiguous, only matched 1:1
  against inline citations, so deleting an unused reserved number and leaving
  a gap is completely fine and simpler than renumbering everything after it.
  **Editions 33 and 34 both reused the same source number for multiple
  movers citing the same outlet** (e.g. edition 34's `[3]` for every
  stockanalysis.com single-stock close) rather than minting a fresh number
  per ticker — this is fine and recommended: `check_refs.py` only checks
  presence/absence of each number, not uniqueness of use, so one Annex B
  entry can legitimately back many inline citations when it is genuinely the
  same source/method.
- **Structure:** 60-second read (5 ranked items) → 1 Market recap → 2
  Equities and earnings (LEAD) → 3 Macro, policy and rates (condensed) → 4
  Commodities and FX (hard assets + FX only) → 5 Derivatives, volatility and
  positioning (condensed, no credit) → 6 The day ahead → Annex A (what could
  not be verified) → Annex B (sources) → Method note.
- **Charts:** 2 per edition, neither duplicating a table. Keep the
  single-stock movers bar chart. Pick chart 2 by what the day's dominant
  story actually is (see Chart #2 guidance under Production notes). **Chart
  placement is editorial, not fixed to Section 2** — edition 24 placed a
  CFTC-positioning chart #2 in Section 5 (Derivatives) rather than Section 2,
  since that's where the content actually belongs, and **edition 34 did the
  same** for its own CFTC-positioning chart #2. The asset/skill template's
  `chart2_panel` position under the Equities heading is just a default for the
  common case (sector rotation), not a hard rule.
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
  **Editions 27 through 34 are all clean counter-examples worth keeping in
  mind**: all eight posted a usable AP wire in time. **Edition 34 hit a
  genuine small two-source conflict worth naming as a fresh example of the
  discipline working**: a secondary market-wrap source (derivatives-pass
  sourcing, thestreet.com/CNBC/gulfnews-derived) gave the S&P 500 close as
  7,720.44 (+0.70%), while the AP wire plus an independent SPY/VOO ETF-proxy
  cross-check (both +0.74%) converged on 7,722.72 (+0.73%) — resolved via a
  direct WebFetch cross-check of SPY and VOO specifically (not just trusting
  either research pass), and disclosed as a correction in the briefing's own
  disclosure box rather than silently picking one. Treat AP/Reuters as "try
  first, expect to sometimes need the fallback chain," not as unreliable by
  default. Always have Yahoo Finance + FRED/stockanalysis.com ready as the
  working fallback regardless of which way this edition goes. **Edition 33's
  lesson stands: a WebSearch tool's own AI-generated summary can itself be a
  bad, uncorroborated source** — verify via a direct instrument fetch (e.g.
  an ETF proxy) when a single search-summary claim conflicts with everything
  else.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example (Trefis "Market Movers" re-serving
  Friday 18 Sept's figures under a Monday 21 Sept URL); edition 26 caught
  another; edition 27 caught a third; edition 28 caught a fourth and fifth in
  the same run; edition 32 caught a sixth and seventh (Rio Times republishing
  Tuesday's oil AND gold/silver wraps under a Wednesday dateline); edition 33
  caught an eighth and ninth (two more Rio Times mis-dates). **Edition 34
  caught a tenth, eleventh and twelfth, on three different outlets**: a
  Trefis "S&P 500 Movers" article URL-dated Friday 2 Oct actually described
  Thursday 1 Oct's session (confirmed by the article's own text, "The S&P 500
  ticked up 0.2% on Thursday, October 1"); an FXStreet article with a
  Friday-looking URL timestamp actually described Thursday's FX/DXY levels
  (confirmed by its own "new 2026 highs above 102.20" / "below 1.1300"
  language, which matches Thursday's logged figures, not Friday's); and a
  live (non-archival) Kitco precious-metals page returned figures that were
  almost certainly *today's* (real-world) live price mislabeled as the
  research-window date — the opposite-direction version of this trap (a
  live/current page contaminating a historical pull, rather than a
  prior-session page masquerading as current). Rio Times has now mis-dated
  content in at least four separate editions (32 twice, 33 twice); treat any
  Rio Times article with extra suspicion. **Lesson reinforced at edition 34:
  this trap is not vendor-specific — it has now hit Trefis, AP-reposts,
  techflowpost, a WebSearch AI summary, Rio Times (x4), FXStreet, and a live
  Kitco page. Always check a dated article's own body text against the
  logged prior-session figures before trusting its date stamp, regardless of
  which outlet it is.** A same-day close and a next-day after-hours-triggered
  move can legitimately combine into one large single-day % change — edition
  24's Xenon Pharmaceuticals -30.7% Friday move is the reference example.
  Check whether a headline % move is measured close-to-close before assuming
  two reports conflict. **The intraday-vs-close divergence trap (distinct
  from stale-dating) is still very much alive**: Worthington Enterprises (ed.
  26), Paychex/Cracker Barrel (ed. 27), Oracle (ed. 28), Akamai and the
  STX/WDC/SNDK storage cluster (both ed. 29), MongoDB (ed. 30), Liquidia and
  Concentrix (both ed. 32), Concentrix again and a Citigroup options-wire
  mismatch (both ed. 33), and **at edition 34, Nike**: the stock's approx.
  -8.7% Thursday after-hours drop did not simply persist into Friday's close
  — Nike recovered somewhat intraday before still closing down a further
  -3.64% versus Thursday's regular-session close, a genuinely two-sided move
  that needed a timestamped Friday close (not the Thursday AH figure) to
  report correctly. Resolved the same way as always: treat the
  stockanalysis.com (or equivalent timestamped) close as authoritative, and
  disclose explicitly when an after-hours figure from the prior edition did
  not simply carry through. **New variant at edition 34: a derivatives-flow
  wire's cited option strike ($370 on what was claimed to be a Nike put) was
  numerically impossible for a sub-$34 stock, and almost certainly belonged
  to a different, unrelated ticker (Tesla closed at $370.59 the same day) —
  a sign that aggregated options-flow summaries can misattribute a strike or
  ticker entirely, not just mis-state a price move.** When an options-flow
  figure looks numerically implausible against the underlying's actual price
  level, treat the whole data point as unreliable and exclude it rather than
  trying to salvage a partial reading.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. Edition 32 hit the same pattern again (spot down, Dec futures up).
  Edition 33's gold reading converged (both spot and futures rose), and
  **edition 34's gold and silver readings converged again (both fell across
  spot and futures alike)** — continue checking instrument/timestamp before
  calling a future gap anomalous, but the spot-vs-futures split now reads as
  an occasional, explainable basis effect rather than a sourcing problem.
  Similarly, **a price level can be correct while a vendor's stated
  %-change is wrong** if the vendor used a different prior-day base — always
  sanity-check that a stated price and stated % change reconcile
  arithmetically against the prior session's logged close. **Edition 34
  surfaced a cleaner, more general version of this same class of bug in the
  CBOE vol-complex feed itself**: the feed's own `price_change_percent`
  field was found to divide `price_change` by the *current* price rather
  than the *prior* close (verified arithmetically: e.g. VIX's field showed
  -7.05%, but -1.08 ÷ 16.39 [the correct prior close, confirmed against the
  previous edition's own logged figure] gives the true -6.59%). **Always
  compute day-over-day % change manually as `price_change ÷ (current_price −
  price_change)` and treat the feed's own `price_change_percent` field as
  unreliable until this is checked each time** — this is a different,
  previously-undocumented bug from the longstanding `prev_day_close`
  duplication issue (see Known-hard-to-source below), caught only because
  the manually-recomputed VIX figure was cross-checked against both the
  prior edition's logged close and an independent news citation (-6.53%,
  closely matching the recomputed -6.59%). The oil contract-month-roll trap
  (Brent Nov-to-Dec) was confirmed already resolved at edition 33; edition 34
  confirmed no new roll has happened yet (Brent's December contract remained
  front-month Friday, as expected ahead of the still-unconfirmed hypothesized
  Dec-to-Jan roll around 31 Oct/1 Nov).
- **The DXY-vs-its-own-FX-crosses conflict — open since edition 29, resolved
  at edition 31, reopened at edition 32, resolved cleanly again at edition
  33, and recurred again (same pattern: magnitude unreconciled, direction
  consistent) at edition 34 without needing escalation.** Friday's reading:
  both DXY snapshots (approx. 101.6 and approx. 101.9) disagreed on
  magnitude but agreed in direction (dollar weaker) with GBP/USD (+0.35%),
  EUR/USD (+0.09%) and USD/JPY (-0.15%), all consistent with the jobs-miss
  dollar selloff (Bloomberg: "Dollar Falls as Traders Pare Fed-Hike Bets
  After Soft Jobs Data"). This conflict has now resolved within one session
  on every occurrence except the 29→30 persistence — treat a future
  recurrence as *likely to resolve within a session* by default, but still
  verify explicitly each time rather than assuming; do not treat this as
  fully closed forever.
- **The same-day silver sign conflict first flagged at edition 31 resolved at
  edition 32 and has now stayed resolved for three straight editions (32-34)**
  — silver fell across all sources Friday (spot approx. -0.97% to -1.04%,
  Dec futures -1.24%), consistent in direction across instruments. Treat as
  closed unless a fresh mismatch appears.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done** — and if it reports 0 inline citations found
  while your Annex B clearly has entries, check for the combined-bracket
  `[n][m]` mistake above before assuming something else is wrong. Also
  remember it only scans HTML text — a citation number baked into a chart
  PNG's label is invisible to it, so is a bare `[n]` typed outside any
  `<sup>` tag, so is a non-numeric placeholder like `[note1]`, and so is a
  letter-suffixed citation like `[9b]`. It DOES correctly catch an unused
  Annex B placeholder (as "listed but never cited," edition 29) — the fix
  there is to delete the unused entry, not leave a gap marker. **Edition 33
  ran clean (38/38) on the first pass; edition 34 initially drafted several
  Annex B entries ([7]-[11], [14], [35]) that were only cited in the chart
  PNG label or not yet cited inline at all** — caught before rendering by
  running `check_refs.py` immediately after drafting (not after render) and
  seeing a mismatch, then adding the missing `<sup class="ref">` tags into
  the relevant table driver cells before re-running clean at 40/40. Worth
  re-stating: table cells are a legitimate, already-used place to put a
  citation (the Annex A/B structure doesn't require citations to live only
  in prose paragraphs) — use them rather than forcing an awkward prose
  mention just to attach a `<sup>` tag.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 34 have all rendered clean at zero tildes** on the
  first check — writing "approx." consistently from the first draft is what
  actually prevents this.
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 24 needed this workaround;
  edition 29 hit a milder version (only ES had a full OI/gross breakdown).
  **Edition 34 resolved this cleanly for the first time**: a fresh CFTC CoT
  report (data through Tue 29 Sept, posted Fri 2 Oct) yielded total open
  interest AND the Asset-Manager/Leveraged-Funds net-position breakdown for
  all three of ES, NQ and RTY (fetched up front per the standing instruction
  from edition 33), letting the "net position as % of open interest" chart
  run with a fully consistent normalization across all three instruments for
  the first time — closing the partial-coverage gap open since edition 29.
  One naming note worth preserving: the CFTC's financial-futures table lists
  the full-size Russell 2000 E-mini ("RTY") as a separate line from the
  Micro E-mini Russell 2000, which has very different (much smaller) open
  interest and a different net-position sign at times — always confirm which
  of the two lines is being read before charting "RTY."
- **When an "optional" filler element (e.g. a levels table) would just
  restate the same instrument list already in a main table with one extra
  column, that's still legitimate as long as the extra column is genuinely
  additive** (editions 25 and 28 both added this) — don't reject the idea
  purely because the instrument list overlaps; check whether the *added*
  column carries real information first. Editions 26, 27, 29, 30, 31, 33 and
  **34 did not need this padding at all** — page 3 filled cleanly from
  content alone every time, including edition 34's CFTC-chart-plus-prose
  Section 5. Edition 32 needed additive prose instead of a table. Edition 33
  hit the opposite failure mode (genuine copy overflow to 5 pages, fixed
  with five rounds of trim-and-re-render). **Edition 34 rendered clean at 4
  pages on the very first attempt**, with content filling pages 1-3 almost
  exactly and no trimming or padding needed — a reminder that both failure
  modes (short page 3 and overflow) remain possible edition to edition and
  should be checked for specifically after every render, not assumed away
  just because recent editions have been clean.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed
  again at edition 33 (Accenture +15.78% vs. Synopsys +12.78%, about 1.23x)
  and **edition 34 (Applied Optoelectronics +7.71% vs. the next-largest
  absolute mover, Accenture -6.31%, about 1.22x)**, both left uncapped.
  Edition 30 remains the one genuine 10x+ case to date (about 15x, capped at
  a fixed axis max of 30). The mechanism has now been confirmed working at
  both extremes across nine editions; no need to revisit the threshold or
  mechanism absent a genuinely new edge case (e.g. something in the 5-10x
  range).

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly, but has (at least) three observed failure modes: (a) a full
  clean sweep with genuinely fresh timestamps on every series, (b) the more
  common "thin-series-stale" pattern, (c) total failure, where every series
  is stale. **Editions 28 through 34 all got a full clean sweep** — seven
  consecutive clean sweeps now, every series carrying a same-day
  `last_trade_time`, verified individually per series via a raw `curl`/direct
  fetch (not a tool-summarized fetch — see Hard rules above for why) each
  time. Still not a guarantee — keep checking `last_trade_time` on each
  series every time. Also note a `prev_day_close` field bug, observed eight of
  ten editions from 22-29: it duplicates the day's own `close`/
  `current_price` rather than giving a real prior-day reference, corrupting
  the feed's own `price_change`/`price_change_percent` fields too. The bug
  stayed absent for four straight editions (30-33). **Edition 34 found a
  related but distinct bug in the same feed instead: the `price_change_percent`
  field divides by the current price rather than the prior close**, giving a
  systematically-too-negative (or too-positive) % on every series — see Hard
  Rules above for the full description and the manual-recomputation
  workaround. **Always compute day-over-day % change manually against the
  previous edition's logged close, regardless of which of these two bug
  patterns (or neither) the feed's own fields appear to show this time** —
  two distinct bugs have now hit this feed's derived fields across different
  editions, so don't assume the feed's own math is trustworthy by default.
  The VIX9D-vs-spot-VIX front-end inversion first flagged at edition 28
  (resolved as noise at edition 29) recurred at edition 30, widened at
  edition 31 (-1.68 to -1.83), widened again at edition 32 (-2.14), widened
  again at edition 33 (-2.39), and **widened yet again at edition 34 to
  -3.25 — a fifth consecutive session of persistence/widening.** Per the
  standing guidance this reads as a settled feature of the current vol
  regime; continue reporting it as a standing regime feature, re-opening the
  thread only if it genuinely narrows or flips.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table,
  and (absent fresher CoT data or another dominant story) chart #2. **At
  edition 34 a fresh CFTC CoT report took the chart #2 slot instead (see
  Chart #2 selection guidance below), but the sector-ETF-proxy source itself
  continued working cleanly for the Section-2 TABLE** (eight straight
  editions, 27-34, for this specific use). No second same-day sector-ETF
  source has ever been found, so this remains a standing single-sourced
  item, disclosed each edition. **Stockanalysis.com single-stock pages are
  also the standing default for pinning an exact closing price/% change on
  any individual mover** — editions 26 through 34 (nine straight) have all
  used direct fetches to it to resolve conflicting intraday-move
  percentages; **edition 34 used it to confirm all seven movers-table names
  plus three additional "flat-closer" names (SNPS, FICO, EFX/TRU) against
  Friday's timestamped close.** Worth doing proactively for any mover whose
  research-pass figures disagree by more than a rounding error, and for any
  stock-move figure quoted inside options-flow/derivatives commentary too.
  Note that a headline wire's own GICS sector-index percentages can differ
  slightly from the SPDR ETF price-change figures (a normal index-vs-ETF-
  price methodology gap); keep using the SPDR ETF figures as the table's
  primary numbers.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. At edition 33 a
  single lower-tier aggregator offered a specific breadth ratio but was not
  corroborated and was correctly left out. **Edition 34 hit the identical
  pattern again** — a breadth figure (NYSE 1,676 advancing vs. 1,077
  declining) surfaced via an aggregated search summary with no clean,
  citable single-source attribution, and was again correctly excluded.
  Continue treating an uncorroborated single-aggregator (or unsourced
  search-summary) breadth figure as not usable — this has now recurred
  enough times to treat as a durable, not occasional, gap.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — now recurred at eleven-plus straight
  editions, still worth a quick attempt each time in case it recovers.
  **zerogex.io is now confirmed across eight straight clean editions
  (27-34)**: after several editions of gradual movement toward zero (-$17.19bn
  at edition 31 to -$11.58bn at edition 33), **edition 34 saw the regime flip
  decisively positive, to +$22.96bn, the largest single-session swing
  recorded in this report's history** — plausibility-checked two ways: the
  page's own spot snapshot (7,723 at 3:59pm ET) landed within a point of the
  independently-confirmed SPX close (7,722.72), and the move is directionally
  consistent with Friday's rally plus a sharp vol crush pushing spot well
  above the gamma-flip point (7,667, roughly 56 points below spot). Continue
  treating zerogex.io as the standing default source for dealer gamma, and
  continue checking each new reading's plausibility against the day's actual
  index move and gamma-flip distance — this was a dramatic swing, not an
  anomalous/implausible one, precisely because both cross-checks held.
  **Minor open item carried forward, still low priority**: zerogex's own
  stated wall levels (call/put wall) have still not been cross-checked
  against a secondary options note's implied walls — revisit only if a
  wall-level figure becomes load-bearing for a specific call.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. **At
  edition 34, secondary CME FedWatch citations collapsed from approx. 36-38%
  to approx. 17-21.6% within the session on the weak jobs report** — see
  Standing Facts above. Keep treating CME FedWatch as needing a disclosed
  range from secondary sources, not a single figure.
- **Kalshi direct fetch:** now rate-limited (HTTP 429, served a "Vercel
  Security Checkpoint" page) for **thirteen straight editions (23-34)** — a
  confirmed structural gap, not transient. Keep attempting each edition (it
  may recover), but a one-line "failed again, Nth straight edition" is
  sufficient prose; use Kalshi's own secondary reporting (its blog,
  prediction-market news aggregators) as a workaround, as recent editions
  have done.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  thirteen editions running (22-34)** — treat as durable; default straight to
  the fallback chain. Shanghai Metals Market (metal.com) has also now failed
  essentially every edition it's been tried — go straight to
  Westmetall.com, which has now worked cleanly **thirteen editions running**
  as the fallback. Disclose whichever was used. Because the fallback chain
  can change edition to edition, treat any day-over-day copper % change
  built across two different sourcing chains as approximate. A standalone
  Investing.com or oilprice.com-derived Brent/WTI settlement page has now
  worked cleanly at both editions 33 and 34 as a second independent
  confirmation route for oil specifically, alongside the existing Investrade
  default.
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) worked
  cleanly again at edition 34 with no lag (2-year 4.83%, 10-year 5.28%,
  30-year 5.63%, all posted same-day). Prefer the CSV endpoint over the HTML
  TextView page — it has a known maturity-column mis-mapping bug the CSV does
  not share. **Edition 34 logged a genuinely new pattern worth watching for
  again: all three tenors dove sharply intraday on the weak jobs report
  (10-year briefly near 5.18%, 2-year near 4.73%, 30-year near 5.57%) before
  fully reversing to close HIGHER than the prior session** — the mirror
  image of edition 33's "fresh intraday high that eased into the close"
  pattern. Together these two editions reinforce the same lesson: always
  check whether a "yields spike/dive" headline refers to an intraday extreme
  or the close, since the two can diverge materially and even point in
  opposite net directions by session end.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. **A new report posted Friday 2 October 2026,
  covering Tuesday 29 September 2026 data, exactly on the schedule predicted
  at edition 33** — fetched successfully, and independently cross-confirmed
  between two separate research passes that each fetched cftc.gov directly
  and arrived at identical figures (high confidence). Headline results: ES
  Asset Managers net long 904,003 (47.7% of OI 1,895,922) vs. Leveraged Funds
  net short 372,489 (-19.6% of OI); NQ Asset Managers net long 69,744 (25.8%
  of OI 270,554) vs. Leveraged Funds net short 24,723 (-9.1% of OI); RTY
  (full-size Russell 2000 E-mini, distinct from the Micro Russell line)
  Asset Managers net long 39,768 (9.3% of OI 428,048) vs. Leveraged Funds net
  short 114,554 (-26.8% of OI, the most lopsided of the three) — this closes
  the partial-coverage gap (ES-only) that had persisted since edition 29.
  The CFE legacy report shows VIX futures non-commercial net short 79,610
  contracts against 421,113 total open interest, also dated Tue 29 Sept.
  **The next report is due approx. Friday 9 October 2026 (covering Tuesday 6
  Oct data)** — check for it first thing next edition, and continue fetching
  OI/gross-long-short for all three of ES, NQ and RTY up front (this worked
  cleanly at edition 34; no reason to revert to ES-only).
- **GBP/USD and EUR/USD clean close:** the underlying sourcing (Yahoo
  Finance/TradingEconomics/FXStreet as primary sources) remains fully
  resolved since edition 26, confirmed again through edition 34. This is
  distinct from the DXY-vs-FX-crosses directional-consistency check (see
  Hard Rules above), which continues to resolve within-session on every
  occurrence except the 29→30 persistence.
- **Gold/silver clean close on a non-event day:** the Kitco-vs-USAGOLD vendor
  gap itself has stayed quiet since normalizing at edition 31 (approx. $5).
  Edition 32's gold divergence (spot down vs. futures up) was a genuine
  different-instrument split, not a vendor disagreement; edition 33's gold
  reading converged, and **edition 34's gold and silver readings both
  converged again (spot and futures fell together for both metals)** — treat
  the spot-vs-futures split as a normal, occasionally-arising basis effect,
  not a sourcing problem, and keep matching timestamps/instruments before
  calling any future gap anomalous. Silver's sign conflict (live since
  edition 31) has now stayed resolved for three straight editions (32-34).
  **Watch for a live/current-page-contamination trap in the opposite
  direction from normal stale-dating, first caught at edition 34**: a
  non-archival Kitco precious-metals page returned figures inconsistent with
  the dated PM Report article for the same metals — almost certainly because
  the non-archival page was serving real-time (i.e. the actual run-date's)
  prices rather than the historical session being researched. Always prefer
  a dated article/report over a live/current quote page when researching a
  past session.
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue — confirm on the BLS/Fed release schedule
  rather than assuming a date. **ISM Manufacturing (Sept 2026) and the
  September jobs report are both now closed threads** — see Standing Facts
  above for the jobs-report figures. **ISM Services/Non-Manufacturing PMI for
  September is due Monday 5 October** — August's reading was 55.4%; edition
  34 located only a secondary-aggregator consensus estimate (approx.
  55.0-55.1%), not an official economist-poll consensus — verify the actual
  print AND look for a firmer consensus figure next edition rather than
  reusing the secondary-aggregator number uncritically. **FOMC minutes from
  the 15-16 September meeting are due Wednesday 7 October, 2:00pm ET** — the
  most relevant scheduled macro item of the upcoming week given the live
  October-hike debate; read for any hints of committee dissent/debate on a
  potential October move.
- **Henry Hub natural gas: the October contract thread resolved at edition
  32** (final settlement $3.00/MMBtu). November became front-month from
  Thursday 1 Oct; **edition 33 could only source a midday intraday quote, and
  edition 34 still could not obtain a confirmed CME end-of-day settlement for
  a second consecutive edition** — two independent aggregator routes
  converged on approx. $3.03-3.04/MMBtu (+2.29%) at edition 34, but two
  separate direct-fetch attempts at CME's own settlements page timed out or
  returned empty content. Try the CME settlements page directly again next
  edition; if a clean EOD settlement still can't be sourced after three
  consecutive attempts, consider this a durable gap (like LME.com) rather
  than a transient one, and keep flagging the aggregator-quote caveat
  explicitly rather than presenting it as a confirmed close.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29 (the page hosts several stacked
  category tables per URL). At edition 30 the page would not yield Monday's
  data at all; at edition 32 a direct query with an explicit `dt=` parameter
  returned `optionsData: null`. Not attempted at editions 33 or 34 (secondary
  priority; options-flow colour was sourced from dedicated options-flow wires
  instead, though edition 34 found none of its candidate wires clean enough
  to use — see Hard Rules above). Going forward: always state which specific
  category/table a Cboe options-volume figure comes from, and don't
  over-invest time here if it stalls, this is a secondary-priority item per
  the derivatives section's own weighting.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable at editions 30
  through 34; next due approx. 14 November 2026.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22) — either find a citable
  benchmark before reaching for that chart type, or stick to describing
  implied-vs-realized in prose without the third bar. Not attempted again
  through edition 34.
- **CFTC total open interest by instrument/date** (needed to normalize
  positioning "as % of open interest"): **fully resolved at edition 34** — OI
  for all three of ES (1,895,922), NQ (270,554) and RTY (428,048, full-size
  Russell E-mini) were all obtained directly from cftc.gov in the same pull,
  closing the partial-coverage gap (ES-only) open since edition 29. Repeat
  this full three-instrument fetch for every future CoT-based chart rather
  than assuming it needs to be re-solved from scratch; see the Hard Rules
  entry above for the Micro-vs-full-size Russell naming trap to watch for
  each time.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear** — editions 27
  through 32 had mostly clean runs; edition 33 was mixed. **Edition 34 hit a
  milder version again**: Argus's Accenture price-target raise (to $260 from
  $220, Buy maintained) was confirmed via only one aggregator
  (Investing.com) rather than two independent sources — reported with
  confidence on the rating direction/firm/dollar figure since the single
  source was itself reasonably authoritative (a named analyst/firm with a
  specific dollar figure, not a vague "sources say"), but flagged here as a
  single-source item per the next bullet's standing guidance. Report the
  rating direction and firm with confidence; treat a missing dollar target
  or unclear dating as a normal gap to flag, not something to chase hard,
  unless the name is the edition's dominant story.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29). Editions 30-33 each hit
  milder versions. **Edition 34's clearest instance: the Wells Fargo
  BP/ExxonMobil actions and the Barclays Mobileye cut were sourced via two
  aggregator-style outlets (dailytradealert.com and Investing.com) rather
  than a primary sell-side note** — reported with confidence since the two
  sources were independent of each other and agreed, but neither is a
  bulge-bracket primary source; worth remembering that "two aggregators that
  agree" is a meaningfully different confidence tier from "one aggregator
  alone" (the Accenture PT case above) even though neither is a true primary
  source. This remains the right call when time-constrained: corroborate
  with a second source or flag it as unverified in Annex A.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. `figsize=(9.8, 1.95)` and
  `(9.8, 1.55)`–`(9.8, 1.75)` depending on chart type, `font.size 9.6`, dpi
  210, `width:100%` in the page. **For a grouped (multi-series) bar chart,
  such as edition 34's CFTC Asset-Manager-vs-Leveraged-Funds chart, the
  simple single-series `barh()` helper in `make_charts.py` doesn't apply —
  write a dedicated `grouped_bar()` function instead** (vertical bars, two
  series per category, legend below the plot). Watch for two specific layout
  traps with grouped/legend charts that don't arise with the simple
  single-series helper: (1) a legend placed directly below the x-axis tick
  labels can overlap them — fix by adding `tick_params(axis="x", pad=...)`
  to push the category labels down and placing the legend between the axis
  and the labels, or further below with enough reserved bottom margin; (2) a
  rotated/long y-axis label can get clipped at the figure's left edge when
  using a fixed `fig.subplots_adjust(left=...)` instead of
  `bbox_inches="tight"` — either shorten the label text or increase the left
  margin fraction until it stops clipping, and always visually inspect the
  rendered PNG (via the Read tool) before embedding it in the HTML rather
  than assuming the matplotlib call succeeded cleanly.
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
  `grep -c` will show 2 for a correctly-built document). **A 5-page render is
  not always a stray break** — editions 24, 28 and 33 all hit 5 pages with
  only the one correct pagebreak present; the cause was genuine copy
  overflow each time. **Edition 34 rendered clean at 4 pages on the very
  first attempt** — content filled pages 1-3 closely without overflowing,
  and page 4 (the annex) had the usual comfortable amount of white space.
  Always re-render and re-check the page count after each trim/pad round
  rather than guessing how much is enough.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Editions 25 and 28 both hit a visibly short page 3 on the first render
  despite passing the 4-page check, fixed with an optional levels table.
  Edition 32 hit a visibly short page 3, fixed with additive prose instead of
  a new table. Edition 33 hit the opposite problem (overflow) and needed
  five trim rounds. **Edition 34's first render needed no fixes at all** —
  all four pages read cleanly with good content density on inspection, the
  best first-attempt outcome logged to date — but this was confirmed by
  actually reading the rendered page images (via the Read tool), not
  inferred from the page count alone, consistent with the standing
  discipline.

### Working settings (current baseline — confirmed stable across many editions under the 1in/1in/13mm/13mm margins)
- Letter size. Body **8.0pt** / line-height **1.20**, serif; `p`
  margin-bottom **2.4px**.
- h1 14.5pt; h2 **9.1pt, margin 4px 0 1.6px 0**; h3 **7.9pt, margin 2.4px 0
  1px 0**.
- Tables **7.4pt**, **1.8px cell padding**, table margin-bottom **3px**.
- Snap-grid tiles: 7.4pt label / 9.4pt value / 7.3pt change; tile padding
  **2px 4px**, snapgrid margin-bottom **3.5px**.
- Bullet lists (`ul.bullets`): **1.4px** margin-bottom per `li`.
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
  doesn't fill the page (needed at editions 25 and 28; not needed at 26, 27,
  29-31, 33 or 34). Edition 32 needed page-3 padding via additive prose
  instead. Edition 33 needed active trimming instead. Always re-render
  immediately after adding (or removing) any content to confirm the page
  count, rather than assuming a change is safe.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — **used for nine consecutive
editions, 25 through 33**, covering a genuinely wide range of underlying
stories). **Fresh CFTC CoT data on a Monday/weekend-window edition → the
ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart, normalized as
% of open interest** — this scenario finally materialized at **edition 34**
for the first time since the guidance was written, ending the sector-proxy's
nine-edition streak as chart #2 (the sector-ETF-proxy source itself
continued uninterrupted as the Section-2 TABLE's source, just not as the
chart). All three instruments (ES, NQ, RTY) had a consistent OI
normalization available this time — see Known-hard-to-source above — so no
fallback substitute normalization was needed. A single dominant earnings
print with a clean, well-sourced implied-vs-realized-move story → a
three-bar implied/historical-average/realized move chart (the
historical-average leg has never actually been sourced successfully). A
genuine multi-sector broadening/deepening selloff across consecutive
sessions → the sector-ETF proxy rendered as a grouped (day-over-day) bar
instead of single-day. A holiday-window preview edition with no fresher data
→ VIX futures term structure with event annotations. When chart #1 (movers)
already covers the earnings/single-name story, the sector proxy (or, as at
edition 34, the CFTC positioning chart) is a good complementary choice even
on a stock-heavy day, since the two stories reinforce rather than duplicate
each other. **Chart #2's placement in the document should follow its
content, not a fixed section** — edition 24 and **edition 34** both placed a
CFTC/positioning chart #2 in Section 5 (Derivatives) rather than Section 2.
**Next time a Mon/weekend-window edition arrives without fresh CoT data
available, revert to the sector-ETF-proxy default** — the CFTC scenario is
now confirmed to work cleanly when the data is available, but it is not
available every Monday/weekend edition (CoT only publishes weekly), so check
freshness first rather than assuming the CFTC chart is now the permanent
default for this edition type.

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–32 (condensed):** established the format (edition 1 baseline;
edition 2 revised weighting/sourcing; edition 3 fixed the ET-cutoff math and
introduced the multi-session-gap and duplicate-fire handling conventions);
corrected the Fed Chair premise to Kevin Warsh at edition 6 (re-verified
every edition since); tracked the Jackson Hole keynote (28 Aug, hawkish) and
the resulting rate-odds repricing through editions 10–18; resolved the
SPDR-sector-ETF-proxy and CBOE-feed (`last_trade_time` check) sourcing
techniques at editions 10–11; corrected the FOMC decision date to Wednesday
16 Sept at edition 18 (superseding editions 15–17's Tuesday assumption).
Major single-name events across editions 1-21: Moderna's melanoma-data spike
and unwind (ed. 4–5), Nvidia's Q2 FY27 beat and Hugging Face acquisition (ed.
8–9), Walmart/Advance Auto Parts/Deere earnings reactions (ed. 5), the
PayPal-Stripe deal collapse (ed. 10), California SB 492 hitting utilities
(ed. 11), an Iran/Hormuz escalation cycle running through the whole period
and repeatedly driving oil, Lululemon's guidance-slash collapse (ed. 15),
Canada's approx. $27.6bn retaliatory tariffs taking effect (ed. 16), Apple's
first Ternus-era product event (ed. 17), Oracle's Q1 FY27 beat with a
vol-crush AH reaction (ed. 18), the Fed debate flipping from "hold vs. cut"
to "hold vs. hike" on hot core CPI (ed. 19), Anthropic CEO Dario Amodei's
AI-safety essay driving a chip-selloff/cybersecurity-rally rotation (ed. 20),
edition 21's Tuesday 15 Sept report (day one of the two-day FOMC meeting):
S&P 7,585.73 (-0.45%), 10-year spiked intraday to approx. 5.045% (a 2007
high); edition 22 (Thu 17 Sept, covering Wed 16 Sept FOMC day): the Fed
hiked 25bp to 3.75%-4.00%, unanimous 12-0, equities reversed hard to close
lower (S&P 7,551.81 -0.4%), 10-year first closed above 5% since 2007;
edition 23 (Fri 18 Sept, covering Thu 17 Sept): equities reversed most of the
post-FOMC selloff (S&P 7,637.76 +1.1%), Bank of England held at 3.75% (6-3),
Generac +18.3%, Lucid +10.0%; edition 24 (Mon 21 Sept, covering Fri 18 Sept
triple witching + weekend catch-up): approx. $7tn September triple-witching
notional expired alongside the quarterly rebalance, Xenon Pharmaceuticals
-30.7%, Warren Buffett stepped down as Berkshire chairman, Bank of Japan
hiked 25bp to approx. 1.25% (31-year high, 7-2 split); edition 25 (Tue 22
Sept, covering Mon 21 Sept): a broad chip-stock rally (Intel +12.0%, AMD
above a $1tn market cap, Arm +16.6%) pushed the Nasdaq to a record 27,122.09
(+2.26%), the quarterly S&P 500/400/600 and Nasdaq-100 rebalance took effect;
edition 26 (Wed 23 Sept, covering Tue 22 Sept): a financials-led sector
rotation — S&P effectively flat at 7,764.64 (-0.00%), Dow -0.36% to
51,863.69 on a bank selloff, Nasdaq a second consecutive record close at
27,244.28 (+0.45%, this close remained the standing Nasdaq closing record as
of edition 34); Viking Therapeutics +35.67% was the standout mover; the
five-central-bank Thursday/Friday cluster was first dated here; gold showed
a genuine Kitco-vs-USAGOLD split (approx. $50 apart, later resolved). Edition
27 (Thu 24 Sept, covering Wed 23 Sept): a broad risk-off session — S&P -0.75%
to 7,706.03, Dow -0.68% to 51,511.59, Nasdaq -1.13% to 26,936.04, driven by
the 10-year spiking to a 19-year high (approx. 5.09-5.14%) after a hot flash
PMI and Fed Governor Barr's hawkish remarks; the "Meta Muse" AI-agent
disintermediation theme rotated from banks into online travel names (Expedia
-7.72%, Airbnb -7.56%, Booking -5.07%); Paychex -8.77%, Cracker Barrel +4.49%;
gold's Kitco-vs-USAGOLD split narrowed to about $7; VIX closed 15.18
(+6.83%); zerogex.io gave its first working dealer-gamma read. Edition 28
(Fri 25 Sept, covering Thu 24 Sept): a whipsaw session closed almost exactly
flat (S&P -0.1% to 7,704.13, Dow -0.3% to 51,349.98, Nasdaq +0.1% to
26,939.37); Communication Services led on a Meta rally; MGM Resorts -10.99%
(take-private bid withdrawn), Oracle -3.47%, Darden -3.02%; Thursday's
central-bank cluster confirmed (Norges Bank hike, Riksbank/SNB/Banxico
holds); the Trump-Xi Washington summit extended the US-China trade truce to
10 Jan 2027; gold's Kitco-vs-USAGOLD split closed to just $0.16. Edition 29
(Mon 28 Sept, covering Fri 25 Sept, the week's one session): a relief rally
closed the week higher (S&P +0.5% to 7,743.41, Dow +0.9%, Nasdaq +0.5%);
Meta -3.33% on the Cambridge Analytica verdict (theoretical exposure up to
approx. $219.5bn), Costco +2.93%, Twilio -7.96%; a new CFTC CoT report
posted (dated Tue 22 Sept); the US-China $30bn tariff-cut agreement was
first reported (confirmed at edition 30); a first DXY-vs-FX-crosses
directional mismatch surfaced; zerogex.io flagged an anomalous approx. 9x
dealer-gamma jump (+$32.56bn), later explained as a gamma-flip-crossing
effect. Edition 30 (Tue 29 Sept, covering Mon 28 Sept, the window's one
session): a broad risk-off reversal erased the prior week's relief rally —
S&P 500 -0.77% to 7,683.69, Dow -0.67% to 51,481.51, Nasdaq -0.92% to
26,820.38, driven by Trump rejecting an Iranian Hormuz-reopening offer and
the 10-year spiking to approx. 5.24%; Kodiak Sciences +177.96% (Phase 3 win,
the capping rule's first genuine 10x+ outlier), MongoDB -18.46% (CEO
resignation), Meta -4.79%, Roblox -9.86%, Boeing -6.91% (FAA 737 MAX 10
certification delay), Nvidia +1.68% ($150bn buyback); October-hike odds
jumped (Polymarket to 69%, CME dispersed to approx. 54-85%); the US-China
"30-for-30" framework confirmed via primary sources; the RBA's Tuesday
decision was previewed (+25bp to 4.60%, later confirmed correct); gold's
Kitco-vs-USAGOLD gap widened sharply to approx. $32 (later normalized); the
DXY-vs-FX-crosses conflict recurred for a second session; VIX 16.07
(+8.07%); zerogex.io's SPX gamma flipped to -$9.33bn. Edition 31 resolved
the DXY-vs-FX-crosses conflict cleanly and logged zerogex.io at -$17.19bn
(further negative). Edition 32 (Thu 1 Oct, covering Wed 30 Sept): a volatile
round-trip session closed slightly lower (S&P 7,651.54, -0.25%) after an
intraday high on a cooler August PCE print (headline +0.3% m/m/+3.4% y/y,
core +0.2% m/m/+3.0% y/y) faded into an unexplained late reversal; Technology
was the only green sector; Liquidia -57.19% (patent loss) was the standout
mover, FICO -4.11% extended Tuesday's FHFA-driven crash; Micron beat cleanly
after the close but drew only a modest AH reaction; oil rallied (Brent
+0.91%, WTI +1.16%) on Iran-sanctions comments; gold's spot/futures split
(later converged) and a reopened DXY-vs-crosses conflict (resolved again at
edition 33) both first appeared here; VIX 16.34 (+1.87%, a fifth clean CBOE
sweep); zerogex.io's gamma moved back toward zero (-$14.33bn). 40 sources,
zero mismatches, clean 4-page render after fixing a short page 3 with
additive prose.

**Edition 33 (condensed)** — Friday 2 October 2026 report covering Thursday
1 October 2026, the window's one NYSE session. Yields, not equities, drove
the session: a hot September ISM Manufacturing Prices Paid print (77.9 vs.
71.1 prior) alongside a European/UK gilt selloff spiked the 10-year
intraday to approx. 5.34% (highest since 2002) and the 30-year to approx.
5.69% before both eased into the close; equities recovered to close green
(S&P 500 +0.19% to 7,666.45, Dow +0.04% to 50,926.56, Nasdaq +0.04% to
26,871.60, Russell 2000 +0.35% to 2,806.63 — all cross-checked cleanly, with
a WebSearch AI-summary's false -5.4% Russell claim discarded). Energy and
Technology led sector rotation on an oil rally and an AI-infrastructure/
software earnings cluster; Accenture +15.78% (FQ4 beat) and Synopsys
+12.78% (Investor Day/OpenAI deal) led, with Coherent +10.90%, Lumentum
+7.67% and Applied Optoelectronics +8.12% riding an AI-optics theme; FICO
+11.69% at the close but gave back more than half after hours to -6.35%
(a still-unresolved two-sided story, later resolved at edition 34); Nike
missed FQ1 and guided FY27 sales down high-single-digits, falling a further
approx. 8.7% after hours (the dominant Friday-open setup, also resolved at
edition 34); McCormick -4.87%, Danaher -4.42%, Tempus AI -6.59%, AMC -8.00%,
Netflix -2.49%, Alphabet -1.70% (SDNY ad-tech ruling); an options-flow
wire's erroneous Citigroup -4.05% claim was corrected to the confirmed
-1.92% close. Macro: Fed Chair/funds-rate/next-FOMC all reconfirmed
unchanged; October-hike odds split sharply across venues for the first time
since Wednesday's unified collapse (Polymarket approx. 25-26% vs. Kalshi/CME
secondary approx. 36-38%, later reconverged at edition 34); BoE and BoJ
meeting dates reconfirmed; a checked-and-refuted shutdown premise closed
cleanly (CR funds government through 11 Dec 2026). Commodities/FX: WTI
+2.71% to $92.87; Brent's long-flagged contract roll turned out to have
already happened (November expired Wednesday at $103.50, December became
front-month Thursday at $102.31); Henry Hub's new November contract could
only be sourced as a midday quote; gold's Wednesday spot-vs-futures split
converged; silver rose across all sources; the DXY-vs-FX-crosses conflict
resolved cleanly again. Derivatives: CBOE feed's sixth consecutive clean
sweep (VIX 16.39, +0.31%); VIX9D inversion widened to -2.39 (fourth
consecutive session); zerogex.io's SPX gamma continued moving toward zero
(-$11.58bn). 38 sources, zero mismatches on the first `check_refs.py` run,
zero stray tildes. The document overflowed to 5 pages on the first render
(genuine copy overflow) and needed five rounds of trim-and-re-render to
reach a clean 4-page render.

**Edition 34 (most recent — full detail)** — Monday 5 October 2026 report
covering Friday 2 October 2026, the window's one NYSE session, plus the
weekend, research window Thu 1 Oct 2026 20:00 ET through Sun 4 Oct 2026
20:21 ET. Verified the two structural header rules again (date line =
edition date, window line states the given research-window start with the
session covered noted parenthetically) — now clean across six consecutive
single-session or single-session-plus-weekend editions (29-34).

A badly-missed September jobs report (BLS: nonfarm payrolls +29,000 vs.
approx. 84,000-90,000 consensus, unemployment 4.2% vs. approx. 4.1%
consensus, July revised to an outright -10,000) landed Friday morning and
drove a broad risk-on rally as October-hike odds collapsed together across
venues (Polymarket approx. 17%, Kalshi secondary approx. 16-18%, CME
FedWatch secondary approx. 17-21.6%, down from Thursday's 25-38%
cross-venue split): S&P 500 +0.73% to 7,722.72 (confirmed via AP plus an
independent SPY/VOO ETF-proxy cross-check, both +0.74%, after a secondary
source had initially logged a slightly lower +0.70%/7,720.44 figure — see
Hard Rules above for how this was resolved), Dow +0.49% to 51,176.96,
Nasdaq Composite +1.20% to an intraday-record-setting but not
closing-record 27,190.86 (the standing closing record, 27,244.28 from 23
Sept, was not broken), Russell 2000 +0.90% to 2,832.90. Ten of eleven SPDR
sectors closed green, led by Consumer Discretionary (+1.13%, Tesla-driven)
and Technology (+1.01%); only Health Care closed red (-0.01%, essentially
flat).

Single-name stories: Tesla +4.65% to $370.59 on a Q3 delivery beat (486,532
vehicles, beat an approx. 462,000-464,000 consensus despite a 2.1% y/y
decline); the AI-infrastructure/optics trade extended a second/third
straight session (Applied Optoelectronics +7.71%, Coherent +5.59%, Lumentum
+3.79%); Accenture reversed hard, -6.31%, on profit-taking after Thursday's
+15.78% earnings pop, even as Argus raised its PT to $260 (from $220, Buy);
Synopsys held Thursday's Investor Day gain essentially flat (-0.13%). Nike
extended its post-earnings slide to a 13-year low (-3.64% to $33.87),
resolving last edition's open question of whether Thursday's approx. -8.7%
after-hours drop would persist — it did, though Friday's regular session
partially recovered from the after-hours low first. FICO fully reversed its
Thursday after-hours plunge to close effectively flat (-0.08%), the other
side of last edition's open two-sided story; Equifax and TransUnion showed
only modest moves, no dramatic mortgage-scoring read-across yet. Paramount
Skydance +1.71%, a partial rebound from Thursday's debt-pricing-driven drop,
with the Warner Bros. Discovery deal's last legal hurdle cleared and closing
slated for 6 October. Analyst actions: Wells Fargo upgraded BP to
Overweight (PT $57) and cut ExxonMobil to Equal Weight (PT $182); Barclays
cut Mobileye to Equalweight (PT $9).

Macro: Kevin Warsh re-confirmed as Fed Chair, funds rate 3.75-4.00%, next
FOMC Oct 27-28 — all unchanged. BoJ's current policy rate was re-verified
directly against its own 18 Sept statement for the first time since the
rate was set, confirmed still approx. 1.25%; BoE and BoJ meeting dates both
reconfirmed (5 Nov, 29-30 Oct respectively). No shutdown; CR funds the
government through 11 Dec 2026, reconfirmed. US-China tariff framework
unchanged, no weekend news. A new CFTC CoT report posted Friday (data
through Tue 29 Sept) — see Derivatives. A Meta/Cambridge Analytica penalty
hearing produced no ruling; Judge Francis Mathew extended supplemental
briefs to Tue 6 Oct, signaled a decision roughly two weeks after.

Commodities/FX: WTI -1.90% to $91.11 (an emergency SPR release pressured
WTI harder than Brent); Brent -0.06% to $102.25, December still front-month,
no roll yet (consistent with the still-unconfirmed hypothesized
Dec-to-Jan roll around 31 Oct/1 Nov). Henry Hub's November contract still
lacks a confirmed CME settlement for a second consecutive edition (approx.
$3.03-3.04/MMBtu, two-source-corroborated only). Gold and silver both opened
higher on the jobs miss before fully reversing to close lower across spot
and futures alike (gold spot approx. -0.83% to -0.88%, futures -0.95%;
silver spot approx. -0.97% to -1.04%, futures -1.24%) — a clean
single-direction move, no spot/futures split this time. Copper +0.14% via
Westmetall. DXY -0.16% to -0.17% (magnitude still unreconciled across
vendors, approx. 101.6 vs. approx. 101.9) but directionally consistent with
GBP/USD +0.35%, EUR/USD +0.09% and USD/JPY -0.15%, all confirming a broadly
weaker dollar on the jobs miss. Treasury yields dove sharply intraday on the
jobs release before fully reversing to close HIGHER than Thursday (2-year
4.83% +5bp, 10-year 5.28% +4bp, 30-year 5.63% +2bp) — a notable
intraday-vs-close divergence in the opposite direction from edition 33's.

Derivatives: a new CFTC CoT report (data through Tue 29 Sept) gave, for the
first time, a fully consistent OI normalization across all three of ES
(Asset Managers +47.7% of OI, Leveraged Funds -19.6%), NQ (+25.8% / -9.1%)
and RTY (+9.3% / -26.8%, the most lopsided leveraged-fund short of the
three) — closing the partial-coverage gap open since edition 29 and
powering this edition's chart #2, the first time the CFTC-positioning chart
scenario has actually materialized since the guidance was written (ending
the sector-ETF-proxy's nine-edition streak as chart #2, though the sector
proxy continued as the Section-2 table's source). The CBOE feed gave a
seventh consecutive full clean sweep (VIX 15.31, -6.59% after correcting
for a newly-discovered feed-field bug — see Hard Rules); VIX9D's inversion
widened for a fifth consecutive session to -3.25; VVIX -5.42%. zerogex.io's
SPX net dealer gamma flipped decisively positive, to +$22.96bn from
Thursday's -$11.58bn, the largest single-session swing logged to date,
plausibility-checked against both the day's rally and a spot-snapshot
cross-check. No clean single-stock options-flow story could be verified for
Friday (Nike, FICO and Citigroup candidates all excluded — see Hard Rules
for the Nike/Tesla strike-misattribution trap specifically). 40 sources,
initially 7 Annex-B entries uncited inline (caught and fixed pre-render by
running `check_refs.py` before, not just after, finishing the draft), zero
stray tildes, clean 4-page render on the first attempt.

**Open threads for edition 35:** the next CFTC CoT report (due approx. Fri 9
Oct, covering Tue 6 Oct) should be checked first thing, continuing the
three-instrument (ES/NQ/RTY) fetch that worked cleanly this time. FOMC
minutes from the 15-16 Sept meeting are due Wed 7 Oct, 2:00pm ET — the
week's most relevant scheduled item given the live October-hike debate;
this will land just after edition 35's likely cutoff unless edition 35 is a
Thursday run, so it may be a Tuesday-edition item or may need to wait for
edition 36 depending on scheduling. ISM Services PMI for September is due
Mon 5 Oct — verify the actual print against the approx. 55.0-55.1%
secondary-aggregator consensus logged this edition (not a firm economist-poll
consensus; look for a better one too). The Meta/Cambridge Analytica ruling
remains outstanding; supplemental briefs are due Tue 6 Oct with a decision
signaled roughly two weeks after — watch for it. The secondary-sourced
December-FOMC hike-odds range (approx. 65% Kalshi to 75%+ FedWatch) is new
this edition and unconfirmed against any primary venue — attempt a firmer
source if it becomes load-bearing. Watch whether the AI-infrastructure/
optics trade (AAOI, COHR, LITE) extends a fourth session or needs fresh
news. Watch for follow-on Nike analyst price-target revisions after its
13-year-low close. The DXY cross-vendor magnitude gap remains open (though
it has resolved directionally every edition bar one) — keep verifying each
time rather than assuming resolution. Henry Hub's November-contract CME EOD
settlement has now failed two consecutive direct-fetch attempts — try once
more next edition; if it fails a third time, consider documenting it as a
durable gap like LME.com rather than attempting it every edition. Watch
whether zerogex.io's SPX dealer gamma holds its new decisively-positive
regime (+$22.96bn) or reverts, especially around Wednesday's FOMC minutes.
The hypothesized Brent Dec-to-Jan roll (around 31 Oct/1 Nov) is not yet due
— keep on the watch list, check when the date approaches. Threads closed
after resolution rather than carried further: the September jobs report
(actual print now on file, replaces consensus); the BoJ current-rate
re-verification (confirmed directly at approx. 1.25%); the October-hike
cross-venue divergence (reconverged, though the standing guidance is to
keep re-verifying rather than assume permanence); the Nike/FICO two-sided
after-hours stories (both resolved to their Friday closes); the CFTC
ES-only partial-coverage gap (all three of ES/NQ/RTY now obtained); the
gold/silver spot-vs-futures split (converged again, reads as a normal
occasional basis effect rather than a recurring problem).
