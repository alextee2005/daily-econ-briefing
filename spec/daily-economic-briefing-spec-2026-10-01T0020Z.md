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
  is where the sessions covered belong, not the date line.
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Edition 30 reused the same pattern for a
  single-session window: "Window: Mon 27 Sept 20:00 ET – Mon 28 Sept 20:20 ET
  (Mon 28 Sept close/AH, the window's one NYSE session)." Worth reusing this
  phrasing pattern going forward for any single-session or single-session-plus-
  weekend edition. **Edition 32 reused the identical pattern again** ("Window:
  Tue 29 Sept 20:00 ET – Wed 30 Sept 20:20 ET (Wed 30 Sept close/AH, the
  window's one NYSE session)") — now confirmed clean across four consecutive
  single-session editions (29 through 32, adjusting phrasing for the weekend
  case at 29). No further confirmation needed; treat this as settled.

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
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 32
  directly against federalreserve.gov's own FOMC calendar page (Dec 8-9 is the
  next SEP meeting after that). The meeting is now under four weeks out —
  continue re-confirming every edition between now and then.
- **October-hike odds moved sharply lower this edition — a genuine repricing,
  not noise, re-verify fresh every edition:** after holding hike-favored in the
  high-60s-to-high-70s% range through edition 31 (Tuesday 29 Sept), odds
  **roughly halved within edition 32's window (Wednesday 30 Sept)**: Polymarket
  fell to approx. 36.5-43.5% (from approx. 68-69%); Kalshi's secondary
  reporting put it at approx. 36-37% (direct fetch still **HTTP 429 for an
  eleventh straight edition, 23-32** — a firmly confirmed structural gap); CME
  FedWatch's secondary citations fell to approx. 35% (from approx. 68-77%),
  direct access still blocked as usual. The trigger: NY Fed President John
  Williams' dovish Tuesday-evening remarks ("no need for urgency," one more
  hike this year "likely enough," data-dependent) compounding into Wednesday's
  cooler-than-feared August PCE print (see below). All three venues now
  cluster in the mid-to-high-30s — the most unified and the largest one-session
  move this report has logged. Treat the true consensus as "hold-favored,
  mid-30s%" going into edition 33, but expect continued volatility: ISM
  Manufacturing (Thu 1 Oct) and the September jobs report (Fri 2 Oct) are both
  due before the next edition's cutoff and could move this materially again.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch,
  rba.gov.au, etc.) every edition, exactly like any other data point.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026**, re-confirmed again at
  edition 32 directly against bankofengland.co.uk's own MPC-dates page —
  about five weeks out; re-confirm again next edition or two as it approaches.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus — resolved, does not need re-verifying.
  **The Bank of Japan's next policy meeting is confirmed for October 29-30,
  2026**, re-confirmed again at edition 32 direct from boj.or.jp's own
  Monetary Policy Meeting schedule page — about four weeks out; re-confirm
  again next edition or two as it approaches.
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
- **August 2026 PCE inflation (Personal Income and Outlays) — RELEASED and
  CONFIRMED at edition 32, closing the thread carried since edition 31:**
  confirmed directly against bea.gov's own release. Headline **+0.3% m/m,
  +3.4% y/y** (down from 3.7% y/y in July); core **+0.2% m/m, +3.0% y/y**
  (down from 3.3% y/y in July). The core y/y print landed meaningfully below
  the approx. 3.4% carried consensus and well under the Cleveland Fed
  Nowcast's approx. 3.78% hot-print fear — a clear disinflation signal, and
  the proximate trigger (alongside Williams' remarks) for the October-hike-odds
  collapse above. **One item remains unresolved and belongs in Annex A, not
  here:** BEA's concurrent annual benchmark revision to the National Accounts
  was confirmed as included in the release, but its precise quantified effect
  on the y/y base could not be isolated from the published release text at
  edition 32 — if this matters for a future comparison, chase the revision
  detail specifically rather than assuming the headline y/y is on a clean,
  unrevised base.
- **The US-China "30-for-30" tariff framework remains at the
  list-identification stage, unchanged since edition 30's primary-source
  confirmation** (re-checked fresh again at edition 32, no new implementation
  news found): USTR.gov and whitehouse.gov confirm a framework recommending
  reduced tariff treatment for $30bn of goods on each side (77 Chinese
  products, 1,600+ US products), administered via the new US-China Board of
  Trade. Still pending each side's domestic legal processes — watch for a
  formal implementation/effective date in a future edition.

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
  a gap (e.g. jumping from [31] to [33], or edition 30's own gaps at [3],
  [4] and [28]) is completely fine and simpler than renumbering everything
  after it.
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
  since that's where the content actually belongs; the asset/skill template's
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
  **Editions 27 through 32 are all clean counter-examples worth keeping in
  mind**: all six posted a usable AP wire in time and their figures
  cross-checked cleanly against an independent second pull (ETF proxies or
  Yahoo Finance) — edition 32's S&P/Dow/Nasdaq/Russell figures all reconciled
  to the penny against both the AP wire and the prior edition's logged
  closes. Treat AP/Reuters as "try first, expect to sometimes need the
  fallback chain," not as unreliable by default. Always have Yahoo Finance +
  FRED/stockanalysis.com ready as the working fallback regardless of which
  way this edition goes.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example (Trefis "Market Movers" re-serving
  Friday 18 Sept's figures under a Monday 21 Sept URL); edition 26 caught
  another (several "AP" reposts of Monday 21 Sept's numbers under a Tuesday
  22 Sept dateline); edition 27 caught a third (a techflowpost article
  reproducing Tuesday's numbers under a Wednesday URL); edition 28 caught a
  fourth and fifth in the same run (a WebSearch AI summary mislabeling
  Wednesday's VIX close as Thursday's; a 24/7 Wall St. article restating
  Wednesday's Airbnb close as current). **Edition 32 caught a sixth and
  seventh: one outlet (Rio Times) republished Tuesday 29 Sept's oil wrap AND
  its gold/silver wrap under a Wednesday 30 Sept dateline/URL in the same
  research pass** — both discarded in favor of same-day sources once the
  figures were found to match Tuesday's logged closes exactly. This trap
  remains very much alive; keep checking every figure's session date against
  the previous edition's logged closes, not just against the vendor's own
  stated date. A same-day close and a next-day after-hours-triggered move can
  legitimately combine into one large single-day % change — edition 24's
  Xenon Pharmaceuticals -30.7% Friday move is the reference example. Check
  whether a headline % move is measured close-to-close before assuming two
  reports conflict. **The intraday-vs-close divergence trap (distinct from
  stale-dating) is still very much alive**: Worthington Enterprises (ed. 26),
  Paychex/Cracker Barrel (ed. 27), Oracle (ed. 28), Akamai and the
  STX/WDC/SNDK storage cluster (both ed. 29), MongoDB (ed. 30, resolved
  -15%-to-27% cross-aggregator spread to a confirmed -18.46% close), and at
  **edition 32, Liquidia (LQDA): intraday wire pickups understated its crash
  at various points (-25%, -48%, -52%) as the stock kept sliding through the
  session before closing -57.19%; Concentrix showed a premarket reaction of
  approx. -9.5% to -10% that fully reversed to close +0.28%** — both resolved
  by treating stockanalysis.com's confirmed close as authoritative over any
  pre-market or intraday figure, and reporting the premarket/close gap
  explicitly for Concentrix since the reversal itself was the story. Treat a
  stockanalysis.com (or equivalent timestamped) closing print as authoritative
  over any pre-market, intraday, or "ahead of the open" figure, and
  cross-check against a second independent source when available.
- Do not repeat items already carried in the previous edition.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. **Edition 32 hit the same pattern again**: Kitco spot gold fell
  0.60% (PM report) while the Dec COMEX futures settlement (Investrade) rose
  0.17% — a genuine spot-vs-futures split (futures priced in an earlier
  intraday rally to approx. $4,251 that faded by the spot close), not a
  sourcing failure. Check whether two conflicting prices are actually two
  different instruments/timestamps before treating it as a sourcing failure.
  Similarly, **a price level can be correct while a vendor's stated %-change
  is wrong** if the vendor used a different prior-day base — always
  sanity-check that a stated price and stated % change reconcile
  arithmetically against the prior session's logged close. Edition 30 hit a
  live example on the 2-year Treasury (disclosed, not re-chased since). The
  oil contract-month-roll trap was checked and found absent again at edition
  32 (Wednesday's WTI/Brent both still referenced the November contract, and
  the day's % change reconciled cleanly off Tuesday's logged close) — **the
  "imminent roll" flag carried from edition 31 was premature; a roll-calendar
  reference now puts the actual November-to-December roll window at approx.
  16-20 October**, about two and a half weeks out. Re-check again as that
  window approaches, not every edition between now and then.
- **The DXY-vs-its-own-FX-crosses conflict, which recurred at editions 29 and
  30 and was treated as substantially resolved at edition 31, REOPENED at
  edition 32 — do not treat as closed.** Wednesday's reads split: one DXY
  snapshot (approx. 101.26) implied a flat-to-weaker dollar, consistent with
  GBP/USD (+0.27%, dollar weaker); a second DXY snapshot (101.37, via
  Investrade) implied a stronger dollar, consistent with that same source's
  EUR/USD and USD/JPY prints — but 101.37 is suspiciously identical to
  Tuesday's already-logged close, raising a real possibility it is a stale
  duplicate rather than a fresh Wednesday print. The most plausible
  explanation offered was an intraday round trip (dollar/yields dipped on the
  soft PCE print, then recovered into the afternoon on strong ADP/Chicago PMI
  data) with the conflicting sources sampling different points in that
  arc — but this was disclosed as unresolved, not asserted as resolved.
  **Next edition: re-check whether Thursday's session resolves cleanly (all
  sources agree on direction) or whether the split persists; if it persists a
  second edition running, escalate to the heavier verification pass (ICE DXY
  futures settlement directly, or a fourth independent FX-crosses source)
  rather than logging a third "reopened" entry.**
- **The same-day silver sign conflict first flagged at edition 31 (Kitco/
  USAGOLD up vs. an Investrade wrap down) RESOLVED at edition 32** — every
  source checked (Kitco, Investrade futures, FXStreet, a TradingEconomics-
  style snapshot) agreed silver fell Wednesday (magnitudes -0.96% to -1.90%
  depending on spot vs. futures instrument). Treat as closed unless a fresh
  mismatch appears.
- Cross-check every inline `[n]` reference against Annex B (and vice versa)
  programmatically (compare sorted sets) rather than eyeballing it once
  source counts climb past ~30. **Run `check_refs.py` before, not just
  after, calling it done** — and if it reports 0 inline citations found
  while your Annex B clearly has entries, check for the combined-bracket
  `[n][m]` mistake above before assuming something else is wrong. Also
  remember it only scans HTML text — a citation number baked into a chart
  PNG's label is invisible to it, so is a bare `[n]` typed outside any
  `<sup>` tag, so is a non-numeric placeholder like `[note1]`, and so is a
  letter-suffixed citation like `[9b]` (edition 30 — see Sources section
  above). It DOES correctly catch an unused Annex B placeholder (as "listed
  but never cited," edition 29) — the fix there is to delete the unused
  entry, not leave a gap marker.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  Edition 29 caught one stray `~` in a late-added disclosure-box bullet;
  **editions 30, 31 and 32 all rendered clean at zero tildes on the first
  check** — writing "approx." consistently from the first draft, not just
  fixing it up after, is what actually prevents this.
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 24 needed CFTC leveraged-funds
  positioning normalized "as % of open interest" but couldn't source total OI
  for the exact CoT date; it substituted "net position as % of the
  leveraged-funds category's own gross long+short" instead. Edition 29 hit a
  milder version (only ES had a full OI/gross breakdown, not NQ/RTY) and
  fell back to prose plus the sector-proxy chart instead of a partial-data
  CoT chart. **No new CoT report posted within editions 30, 31 or 32's
  windows** (the Tue 22 Sept report logged at edition 29 is still the most
  recent; the next is due approx. Fri 2 Oct, covering Tue 29 Sept) — this
  scenario did not recur. The lesson stands for whenever a fresh CoT report
  does land: check that a *consistent* normalization (or at least a
  consistent unit) is available across every instrument in the chart before
  committing to it, and fall back to prose plus the standing sector-proxy
  default if you can't.
- **When an "optional" filler element (e.g. a levels table) would just
  restate the same instrument list already in a main table with one extra
  column, that's still legitimate as long as the extra column is genuinely
  additive** (editions 25 and 28 both added a prior-session-baseline-vs-close
  levels table to a short page 3) — don't reject the idea purely because the
  instrument list overlaps; check whether the *added* column carries real
  information first. **Editions 26, 27, 29, 30 and 31 did not need this
  padding at all** — page 3 filled cleanly from content alone every time.
  **Edition 32's first render ran genuinely short on page 3** despite a
  full-length Section 4 levels table — fixed not with the optional levels
  table (already present as the main Section 4 table) but by adding two
  prose paragraphs' worth of real content to Section 5 (restating the
  standing CFTC CoT positioning numbers for context, adding a one-line
  funding/SOFR note, and noting the Kalshi failure streak explicitly) plus
  one more "sector setup" bullet — all genuinely additive, not padding for
  its own sake. **Lesson restated**: when page 3 runs short, look first for
  real, already-researched content that didn't make the first draft (CoT
  context, a funding line, a day-ahead bullet) before reaching for a
  mechanical filler table.
- **The single-stock movers bar-chart outlier-capping rule** was tested again
  at edition 32: Liquidia Corp (LQDA) fell -57.19% on a patent-case loss,
  versus the next-largest mover (United Therapeutics, +12.55%, the
  counterparty that won the same case) — a approx. 4.56x spread. This is
  comfortably under the approx. 10x threshold established at edition 30 (the
  Kodiak Sciences 15x case, which WAS capped), and consistent with edition
  26's 4.7x VKTX/ONON case (left uncapped) — so LQDA was left uncapped per
  the existing rule, and the render stayed legible with the smaller bars
  (approx. 3.7-3.9%) still readable. The mechanism continues to work as
  designed in both the capped (10x+) and uncapped (under approx. 5x) regimes;
  no need to test the middle of the range until a real case presents one.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly, but has (at least) three observed failure modes: (a) a full
  clean sweep with genuinely fresh timestamps on every series, (b) the more
  common "thin-series-stale" pattern, (c) total failure, where every series
  is stale. **Editions 28 through 32 all got a full clean sweep** — five
  consecutive clean sweeps now, every series carrying a same-day
  `last_trade_time`, verified individually per series via a raw `curl` pull
  (not a tool-summarized fetch — see Hard rules above for why) each time.
  Still not a guarantee — keep checking `last_trade_time` on each series
  every time. Also note a `prev_day_close` field bug, observed eight of ten
  editions from 22-29: it duplicates the day's own `close`/`current_price`
  rather than giving a real prior-day reference, corrupting the feed's own
  `price_change`/`price_change_percent` fields too. **The bug has now stayed
  absent for three straight editions (30, 31, 32)** — encouraging, but
  continue to treat as intermittent, not resolved, and **always compute
  day-over-day % change manually against the previous edition's logged close
  regardless of whether the feed's own fields look correct this time** (at
  edition 32 the manual calculation and the feed's own field agreed for once,
  which is itself informative but not yet a pattern to rely on). The
  VIX9D-vs-spot-VIX front-end inversion first flagged at edition 28 (resolved
  as noise at edition 29) recurred at edition 30, widened at edition 31
  (-1.68 to -1.83), and **widened again at edition 32 to -2.14 — a third
  consecutive session of persistence/widening.** Per the standing guidance
  this now reads as a settled feature of the current vol regime rather than
  noise; **stop treating this as an open "watch for normalization" item and
  start reporting it as a standing regime feature, re-opening the thread
  only if it genuinely narrows or flips.**
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table
  and (absent fresher CoT data or another dominant story) chart #2. Worked
  cleanly again at editions 27 through 32 (six straight); no second same-day
  sector-ETF source has ever been found, so this remains a standing
  single-sourced item, disclosed each edition. **Stockanalysis.com
  single-stock pages are also the standing default for pinning an exact
  closing price/% change on any individual mover** — editions 26 through 32
  all used direct fetches to it to resolve conflicting intraday-move
  percentages (edition 30: MongoDB resolved to -18.46%; edition 31: Fair
  Isaac's close of -26.52% used as authoritative; **edition 32: Liquidia's
  close of -57.19% used as authoritative over intraday wire figures ranging
  -25% to -52%, and Concentrix's close of +0.28% used over a -9.5%-to-10%
  premarket figure**). Worth doing proactively for any mover whose
  research-pass figures disagree by more than a rounding error. Note that a
  headline wire's own GICS sector-index percentages can differ slightly from
  the SPDR ETF price-change figures (a normal index-vs-ETF-price methodology
  gap); keep using the SPDR ETF figures as the table's primary numbers.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. Not chased at
  editions 30, 31 or 32 — no research pass has flagged a need for it
  recently.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — now recurred at editions 22, 24-32
  (ten straight, still worth a quick attempt each time in case it recovers).
  **zerogex.io is now confirmed across six straight clean editions (27-32)**:
  edition 30 flipped sign entirely, edition 31 moved further negative still
  (-$17.19bn) as spot sat further below a higher flip point, and **edition 32
  moved back toward zero (-$14.33bn) as the gap between spot (7,652) and the
  flip point (7,695) narrowed to 43 points, with spot essentially pinned
  against the put wall (7,650)** — a plausible, well-explained progression
  each time, and edition 32's own SPX spot snapshot (7,652) cross-checked to
  within half a point against the independently-sourced CBOE SPX close
  (7,651.54). Continue treating zerogex.io as the standing default source for
  dealer gamma, and continue the discipline of checking each new reading's
  plausibility against the day's actual index move and gamma-flip distance.
  **Minor open item carried forward, still low priority**: zerogex's own
  stated wall levels (call/put wall) have still not been cross-checked
  against a secondary options note's implied walls — only the net GEX
  sign/magnitude has been verified so far; revisit only if a wall-level
  figure becomes load-bearing for a specific call.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. The
  secondary-citation split narrowed at edition 31 to approx. 68-77%, and then
  **moved sharply (not just narrowed) at edition 32 to approx. 35%**, in step
  with the broader October-hike-odds repricing described in Standing Facts
  above — this is a genuine, broadly-corroborated market move, not a
  stale-republish artifact (all three venues — Polymarket, Kalshi, CME
  secondary — moved together in the same direction and rough magnitude). Keep
  treating CME FedWatch as needing a disclosed range from secondary sources,
  not a single figure, and keep naming any recurring stale figure explicitly
  if one resurfaces.
- **Kalshi direct fetch:** now rate-limited (HTTP 429, served a "Vercel
  Security Checkpoint" page) for **eleven straight editions (23-32)** — a
  confirmed structural gap, not transient. Keep attempting each edition (it
  may recover), but a one-line "failed again, Nth straight edition" is
  sufficient prose; use Kalshi's own secondary reporting (its blog,
  prediction-market news aggregators) as a workaround, as recent editions
  have done.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  eleven editions running (22-32)** — treat as durable; default straight to
  the fallback chain. Shanghai Metals Market (metal.com) has also now failed
  essentially every edition it's been tried (returns template/header content
  only, no price data, confirmed again at edition 32) — go straight to
  Westmetall.com, which has now worked cleanly **eleven editions running** as
  the fallback. Disclose whichever was used. Because the fallback chain can
  change edition to edition, treat any day-over-day copper % change built
  across two different sourcing chains as approximate.
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) worked
  cleanly again at edition 32 with no T+1 lag (2-year 4.88%, 10-year 5.29%,
  both posted same-day). Prefer the CSV endpoint over the HTML TextView
  page — it has a known maturity-column mis-mapping bug the CSV does not
  share. **The 10-year pushed to a fresh approx. 5.29% at edition 32 (still a
  24-year high) and the 30-year to approx. 5.65% (highest since May 2002)** —
  worth noting that long-end yields are now the dominant cross-asset driver
  in this report's recent editions, outweighing Fed-odds moves on both gold
  and rate-sensitive equity sectors even on a day the Fed odds themselves
  collapsed.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. The most recent report remains the one
  published Fri 25 Sept, dated Tue 22 Sept: equity-index Asset Managers net
  long approx. 934,000-936,000 ES contracts vs. Leveraged Funds net short
  approx. 375,600-376,000; VIX futures non-commercial net short approx.
  79,300. **Confirmed again at edition 32 that no new report has posted**
  (still the Tue 22 Sept data on file at cftc.gov). **Next report due approx.
  Friday 2 October 2026, which would cover Tuesday 29 Sept data — this now
  lands right around edition 33's own cutoff (if edition 33 covers Thursday 1
  Oct), so check for it as the very first derivatives item next edition.** If
  a CoT-based chart is wanted once fresh data lands, try to get
  OI/gross-long-short for all three of ES/NQ/RTY up front this time, not
  just ES.
- **GBP/USD and EUR/USD clean close:** the underlying sourcing (Yahoo
  Finance/TradingEconomics/FXStreet as primary sources) remains fully
  resolved since edition 26, confirmed again through edition 32. **This is
  distinct from the DXY-vs-FX-crosses directional-consistency check, which
  reopened at edition 32 — see Hard rules above.** Don't conflate "can we get
  a clean GBP/EUR close" (yes, resolved) with "does DXY's stated direction
  match what the crosses imply" (live open thread again as of edition 32).
- **Gold/silver clean close on a non-event day:** the Kitco-vs-USAGOLD vendor
  gap itself has stayed quiet since normalizing at edition 31 (approx. $5).
  **Edition 32's gold divergence was a different, well-explained
  phenomenon — spot (Kitco) down vs. Dec COMEX futures (Investrade) up on
  the same day, a genuine different-instrument split, not a vendor
  disagreement on the same instrument** (see Hard rules above). **Silver's
  sign conflict, live since edition 31, resolved cleanly at edition 32** — see
  Hard rules above. Continue to insist on matching timestamps/instruments
  before calling any future gap anomalous.
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue — confirm on the BLS/Fed release schedule
  rather than assuming a date. **PCE inflation: the August 2026 print closed
  at edition 32 (see Standing Facts above) — this thread is now fully
  resolved.** The next data risk items are ISM Manufacturing (Thu 1 Oct,
  consensus approx. 54.8) and the September jobs report (Fri 2 Oct,
  consensus nonfarm payrolls approx. 84,000-90,000, unemployment 4.1%) — both
  due before edition 33's likely cutoff; verify the actual prints rather than
  the consensus once they land.
- **Henry Hub natural gas: RESOLVED at edition 32, closing a thread open
  since edition 31.** The October 2026 NYMEX contract expired Wednesday 30
  Sept at a two-source-confirmed final settlement of $3.000/MMBtu (Rigzone,
  NaturalGasIntel), down from Tuesday's $3.011 close. November becomes the
  front-month contract from Thursday 1 Oct — **when pricing natural gas next
  edition, confirm which contract (November) is now front-month and don't
  compare its level directly against the old October settlement without
  noting the rollover.** Direct CME settlements page fetch still timed out;
  the two independent editorial sources were sufficient per house sourcing
  rules.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29 (the page hosts several stacked
  category tables per URL — Sum of All Products, Index Options, Equity
  Options, Exchange-Traded Products, instrument-specific tables — each with
  its own totals). At edition 30 the page would not yield Monday's data at
  all (served stale cached data instead). **At edition 32, a direct query
  with an explicit `dt=` date parameter returned `optionsData: null` for the
  target date — confirming the page genuinely had not posted Wednesday's
  figures yet as of the research cutoff, rather than a fetch/parsing failure
  on our end.** This is a useful distinction going forward: when the dated
  query returns a clean null rather than an error or stale substitute, report
  it confidently as "not yet posted" rather than as an unexplained gap.
  Going forward: always state which specific category/table a Cboe
  options-volume figure comes from, and expect the page to sometimes simply
  not have same-day data available via a plain fetch/curl approach at all —
  don't over-invest time here if it stalls, this is a secondary-priority item
  per the derivatives section's own weighting.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable at editions 30, 31 or
  32.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22) — either find a citable
  benchmark before reaching for that chart type, or stick to describing
  implied-vs-realized in prose without the third bar. Not attempted again
  through edition 32.
- **CFTC total open interest by instrument/date** (needed to normalize
  positioning "as % of open interest"): partially resolved at edition 29 —
  ES's total OI (approx. 1.9mn contracts) was obtained directly from
  cftc.gov, but NQ's and RTY's were not pulled. No new CoT report posted
  within editions 30, 31 or 32's windows, so this was not re-attempted. **The
  next report (due approx. Fri 2 Oct, covering Tue 29 Sept) is the one to try
  this on — fetch OI/gross-long-short for all three of ES, NQ and RTY
  explicitly up front rather than assuming one contract's availability
  implies the others'.**
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear** — editions 27
  through 29 confirmed several rating changes without being able to pin an
  exact dollar price target for all of them. Editions 30, 31 and **32 all had
  cleaner runs** — edition 32 got exact targets for the BofA/FICO ($700),
  HSBC/Target ($190), Citigroup/Moderna ($80), TD Cowen/Accelerant Holdings
  ($20.25), Roth/SoundThinking ($9) and Citigroup/Dow Inc. ($30) actions, with
  only two smaller names (Wells Fargo/Pinnacle Financial, BofA/Grocery
  Outlet) lacking a confirmed target — flagged to Annex A rather than
  asserted. Report the rating direction and firm with confidence; treat a
  missing dollar target or unclear dating as a normal gap to flag, not
  something to chase hard, unless the name is the edition's dominant story.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29). Edition 30 hit a milder
  version; edition 31 hit it again (Iovance, Concentrix consensus figures).
  **Edition 32 hit the same pattern again**: the Wells Fargo/Pinnacle
  Financial and BofA/Grocery Outlet upgrades were picked up only via a single
  aggregator summary, with no price target or close-reaction data
  independently confirmed — flagged to Annex A rather than reported as fact,
  as were two single-Benzinga-sourced downgrades (TD Cowen/Accelerant,
  Roth/SoundThinking, though both of those did at least carry confirmed price
  targets from that one source). **This remains the right call when
  time-constrained**: a single aggregator's claim, especially for a smaller
  or less-covered name, is not enough on its own — corroborate with a second
  source or flag it as unverified in Annex A.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. `figsize=(9.8, 1.95)` and
  `(9.8, 1.55)`, `font.size 9.6`, dpi 210, `width:100%` in the page.
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
  not always a stray break** — editions 24 and 28 both hit 5 pages with only
  the one correct pagebreak present; the cause was genuine copy overflow in
  both cases. Editions 29 through 32 all rendered clean at 4 pages on the
  first try with the standard single pagebreak (edition 32 needed a second,
  content-driven pass to fix a short page 3 — see Hard rules above — but did
  not need a structural fix).
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Editions 25 and 28 both hit a visibly short page 3 on the first render
  despite passing the 4-page check, fixed with an optional levels table.
  **Edition 32 also hit a visibly short page 3 on the first render** (despite
  already having a full Section 4 levels table) — fixed this time not with a
  new table but by adding genuinely additive prose (CFTC CoT context, a
  funding one-liner) to Section 5 and one more bullet to Section 6, then
  re-rendering to confirm. **This is now the second distinct fix pattern for
  a short page 3** (optional levels table vs. additive prose elsewhere) —
  pick whichever fits the actual gap: a table if Section 4 itself is thin, or
  prose/bullets elsewhere if Section 4 is already full but the rest of the
  page is short.

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
  29, 30 or 31). **Edition 32 needed page-3 padding again but took the
  additive-prose route instead (Section 4's table was already full-length)**
  — see Production notes above for the distinction. Always re-render
  immediately after adding any filler to confirm the page count, rather than
  assuming a "moderate" addition is safe (edition 28's first attempt at 12
  levels-table rows overshot to 5 pages; 10 rows fixed it). Conversely, **if
  page 3 overflows by a handful of lines**, the cheapest trims are:
  shortening day-ahead table cell text, cutting one "sector setup" bullet or
  merging two into one, tightening the last prose paragraph in Section 5, or
  trimming rows from the optional levels table if one was added.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at edition 26 (VKTX +35.67% vs. next-largest ONON +7.58%, about 4.7x),
  edition 27 (about 1.14x), edition 28 (about 2.4x), edition 29 (about 1.6x),
  edition 31 (about 1.2x), and **edition 32 (Liquidia -57.19% vs.
  next-largest United Therapeutics +12.55%, about 4.56x, left uncapped)**.
  Edition 30 produced the one genuine 10x+ case to date and confirmed the
  rule works as designed (Kodiak Sciences +177.96% vs. next-largest AMC
  +11.90%, about 15x, capped at a fixed axis max of 30 with a "(capped)"
  annotation). The mechanism has now been confirmed working at both extremes
  (uncapped under approx. 5x, capped at approx. 15x) across seven editions;
  no need to revisit the threshold or mechanism absent a genuinely new edge
  case (e.g. something in the 5-10x range).

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — **used for an eighth consecutive
edition at edition 32**, for a sector-rotation story where Technology was the
lone green sector on a chip-demand rally while rate-sensitive sectors lagged
despite a cooler inflation print, because long-end yields pushed to fresh
highs regardless; edition 31 used it for a near-total reversal of the prior
day's leadership; edition 30 for a broad risk-off session; edition 29 for a
Friday relief-rally rotation; edition 28 for a Meta-Muse-driven rotation;
edition 27 for a rate-spike-driven rotation into defensives; edition 26 for a
financials-vs-materials reversal; edition 25 for a chip-led rally — this
remains a reliable, low-risk default and has now covered a genuinely wide
range of underlying stories without needing to be replaced). Fresh CFTC CoT
data on a Monday/weekend-window edition → the ES/NQ/RTY asset-manager-vs-
leveraged-funds positioning chart, **normalized as % of open interest if
that figure can be sourced for all instruments being charted; if not, a
category's own net-position-as-%-of-its-own-gross-long+short is an
acceptable, honestly-labelled substitute — but check that a *consistent*
normalization (or at least a consistent unit) is available across every
instrument in the chart before committing to it.** No fresh CoT data posted
within editions 30, 31 or 32's windows, so this scenario did not arise;
**the next report (due approx. Fri 2 Oct) is the one to watch for.** A single
dominant earnings print with a clean, well-sourced implied-vs-realized-move
story → a three-bar implied/historical-average/realized move chart (the
historical-average leg has never actually been sourced successfully — see
Known-hard-to-source above; Micron's clean beat at edition 32 was considered
but its after-hours reaction was too muted to carry a dedicated chart). A
genuine multi-sector broadening/deepening selloff across consecutive sessions
→ the sector-ETF proxy rendered as a grouped (day-over-day) bar instead of
single-day. A holiday-window preview edition with no fresher data → VIX
futures term structure with event annotations. When chart #1 (movers)
already covers the earnings/single-name story, the sector proxy is a good
complementary choice even on a stock-heavy day — editions 25 through 32 have
all used exactly this combination (movers as chart #1, sector rotation as
chart #2) with the two stories reinforcing rather than duplicating each
other every time. **Chart #2's placement in the document should follow its
content, not a fixed section** — a CFTC/positioning chart reads better in
Section 5 than Section 2 (edition 24).

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–30 (condensed):** established the format (edition 1 baseline;
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
27,244.28 (+0.45%); Viking Therapeutics +35.67% was the standout mover; the
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
effect. **Edition 30** (Tue 29 Sept, covering Mon 28 Sept, the window's one
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
DXY-vs-FX-crosses conflict recurred for a second session (later resolved at
edition 31, reopened again at edition 32); VIX 16.07 (+8.07%); zerogex.io's
SPX gamma flipped to -$9.33bn.

**Edition 31 (condensed)** — Wed 30 Sept 2026 report covering Tuesday 29
September 2026, the window's one NYSE session. A quiet mean-reversion
session after Monday's risk-off shock: S&P 500 -0.16% to 7,670.84, Dow
-0.26% to 51,349.92, Nasdaq Composite -0.09% to 26,797.54, Russell 2000
-0.35% to 2,807.92; sector leadership was a near-total reversal of Monday
(Utilities led, Energy lagged as oil gave back most of its Hormuz-driven
spike: Brent -2.6% to $102.59, WTI -3.48% to $89.38). Fair Isaac (FICO)
-26.52% was the dominant mover (FHFA/Fannie-Freddie mortgage-scoring-model
news threatening its credit-scoring monopoly); Iovance Biotherapeutics
+31.48%; Carnival +13.41%; Bloom Energy +10.80%; CarMax +4.74%; Meta +3.24%
(new "Muse for Small Business" launch, even as the Cambridge Analytica
penalty hearing and Muse privacy-complaint threads stayed live);
Monday.com -3.80%; Concentrix -2.24%. The RBA's previewed Tuesday decision
was confirmed (+25bp to 4.60%); Fed Chair/FOMC/BoE/BoJ dates re-confirmed;
October-hike odds held hike-favored (Polymarket approx. 68-69%, CME
secondary approx. 68-77%); the carried-forward Wednesday-PCE consensus was
corrected (not just re-dated) to headline approx. +0.3% m/m / approx. 2.7%
survey vs. approx. 3.78% Nowcast y/y, core approx. +0.2-0.3% m/m / approx.
3.4% y/y — superseded by the actual print at edition 32. Gold's
Kitco-vs-USAGOLD gap normalized to approx. $5; a new silver sign conflict
emerged (resolved at edition 32); the DXY-vs-FX-crosses conflict was treated
as substantially resolved (reopened at edition 32); Henry Hub natural gas
could not be pinned to a clean settlement (resolved at edition 32); Treasury
2-year eased to 4.89%, 10-year pushed to a fresh approx. 5.26% 24-year high.
VIX 16.04 (-0.19%, fourth consecutive CBOE full clean sweep); VIX9D's
inversion widened to -1.83 (persisted/widened again at edition 32);
zerogex.io's SPX gamma moved further negative to -$17.19bn. 39 sources, zero
mismatches, clean 4-page render on the first attempt.

**Edition 32 (most recent — full detail)** — Thursday 1 October 2026 report
covering Wednesday 30 September 2026, the window's one NYSE session,
research window Tue 29 Sept 20:00 ET through Wed 30 Sept 20:20 ET. Verified
the two structural header rules again: date line reads the edition date
(Thursday 1 October 2026), not the session date; window line states the
given research-window start (Tue 29 Sept 20:00 ET) with the actual session
covered noted parenthetically — now confirmed clean across four consecutive
single-session editions (29-32), treat this pattern as settled.

A volatile round-trip session: the S&P 500 traded up as much as 0.7%
intraday on a cooler-than-feared August PCE print before fading into a
late-day reversal with no single cited catalyst (Micron's after-the-bell
earnings and quarter-end positioning were floated), closing -0.25% at
7,651.54 — reconciling to the penny against Tuesday's logged 7,670.84 close
via both the AP wire and an independent SPX pull from the CBOE feed. Dow
-0.86% to 50,906.05 (Northrop Grumman's defense-contract loss weighed);
Nasdaq Composite +0.24% to 26,861.06 (chip-stock rally offsetting broader
weakness); Russell 2000 -0.39% to 2,796.86 — all four indices cross-checked
cleanly against the prior edition's logged closes. Sector leadership:
Technology (XLK +0.64%) was the only green sector, carried by Intel (+3.71%,
CEO cited unmet AI/agentic CPU demand) and Hewlett Packard Enterprise
(+3.90%, a $1.2bn AMD "Helios" AI-rack order from Vultr); Consumer Staples
(XLP -1.53%) lagged, with Health Care, Industrials, Financials, Real Estate
and Utilities all underperforming despite the soft inflation print because
long-end Treasury yields pushed to fresh cycle highs regardless.

Single-name stories: Liquidia Corp (LQDA) -57.19%, the largest single-day
move logged by this report since Kodiak Sciences, after a Delaware federal
court found its Yutrepia inhaler infringes a United Therapeutics patent,
threatening Liquidia's lead pulmonary-hypertension drug; United Therapeutics
(UTHR) +12.55% on the win (left uncapped in chart 1 at approx. 4.56x the
next-largest mover, under the approx. 10x capping threshold); Rogers Corp
(ROG) +10.73% (Investor Day guidance raise plus new long-term targets); FICO
-4.11% (a fresh, distinct BofA downgrade layered on Tuesday's already-
reported -26.52% FHFA-driven crash); Northrop Grumman -4.19% (lost the
F/A-XX sixth-gen fighter contract to Boeing, which itself closed only
-0.87% after an early gain faded); Moderna -5.35% (Citigroup downgrade to
Sell despite a raised price target); Concentrix +0.28% at the close despite
a Q3 revenue miss that had the stock down approx. 10% premarket. Micron
reported after the close: a clean beat (EPS $33.42 vs. $31.16 est., revenue
$54.23bn vs. $50.45bn est.) but only a modest -0.78% after-hours reaction on
capex concerns.

Macro: August PCE (released 8:30am ET Wednesday) came in at headline +0.3%
m/m/+3.4% y/y, core +0.2% m/m/+3.0% y/y — a clear cooling print versus the
carried consensus, closing the thread open since edition 31. NY Fed
President John Williams' Tuesday-evening dovish remarks compounded with the
soft PCE to roughly halve October-hike odds within the session: Polymarket
to approx. 36.5-43.5%, Kalshi secondary to approx. 36-37%, CME secondary to
approx. 35% (all three down from the high-60s/70s% range logged Tuesday) —
the largest, most unified one-session repricing this report has logged. Fed
Chair/FOMC/BoE/BoJ dates all re-confirmed unchanged. US-China "30-for-30"
tariff framework unchanged, still pending implementation.

Commodities/FX: oil rallied (Brent +0.91% to $103.53, WTI +1.16% to $90.42)
on Trump denying willingness to ease Iran sanctions; an explicit roll-check
found no roll (still referencing November; the actual roll window is now
identified at approx. 16-20 October, pushing out edition 31's "imminent"
flag). Henry Hub's October contract expired at a clean, two-source-confirmed
$3.00/MMBtu final settlement, resolving a two-edition sourcing gap. Gold
diverged by instrument (spot down 0.60%, Dec COMEX futures up 0.17% — a
genuine, well-explained split, not a vendor error) as long yields offset the
dovish Fed repricing; silver's sign conflict from edition 31 fully resolved
(all sources agreed down). Copper +0.09% via Westmetall (LME/metal.com
failed an eleventh straight edition). The DXY-vs-FX-crosses conflict
**reopened**: GBP/USD diverged from EUR/USD and USD/JPY on dollar direction,
and one of two DXY prints is suspected stale — disclosed as unresolved, to
be re-checked next edition. Treasury 2-year eased slightly to 4.88%, 10-year
pushed to a fresh approx. 5.29% (24-year high), 30-year to approx. 5.65%
(highest since May 2002).

Derivatives: the CBOE feed gave a fifth consecutive full clean sweep (VIX
16.34, +1.87%, matching the feed's own computed figure for once); the
`prev_day_close` bug stayed absent a third straight edition. VIX9D's
inversion below spot VIX persisted and widened for a third consecutive
session (-1.68 → -1.83 → -2.14) — now treated as a settled vol-regime
feature per the standing guidance rather than a live "watch for
normalization" item. zerogex.io's SPX net dealer gamma moved back toward
zero (-$14.33bn, from -$17.19bn) as spot's gap to the gamma flip point
narrowed to 43 points, internally consistent with the independently-sourced
SPX close. CFTC CoT confirmed unchanged since the Tue 22 Sept report (next
due approx. Fri 2 Oct, covering Tue 29 Sept data — check first thing next
edition). 40 sources, zero mismatches on the first `check_refs.py` run; zero
stray tildes on the first check; page 3 ran short on the first render and
was filled with genuinely additive content (CFTC CoT context, a funding
one-liner, one more day-ahead bullet) rather than a mechanical filler table;
clean 4-page render confirmed after that fix.

**Open threads for edition 33:** The DXY-vs-FX-crosses conflict reopened
this edition — re-check whether Thursday's session resolves cleanly or
whether the split persists a second edition running (if it persists,
escalate to the heavier verification pass: ICE DXY futures settlement
directly, or a fourth independent FX-crosses source). ISM Manufacturing (Thu
1 Oct, consensus approx. 54.8) and the September jobs report (Fri 2 Oct,
consensus nonfarm payrolls approx. 84,000-90,000, unemployment 4.1%) are
both due before the likely next cutoff and are the week's key remaining data
risk, especially given how sharply Wednesday's PCE print moved Fed odds —
verify the actual prints, not consensus. Watch for the outcome of Meta's
Cambridge Analytica penalty hearing (Thu 1 Oct, Judge Francis Mathew) — Meta
still carries this plus the separate Muse privacy-complaint fallout as two
live negative threads. The next CFTC CoT report (due approx. Fri 2 Oct,
covering Tue 29 Sept data) should be checked first thing — if a CoT chart is
wanted, fetch OI/gross-long-short for ES, NQ and RTY all three up front.
VIX9D's inversion is now being reported as a settled regime feature, not an
open "watch for normalization" item — only re-open if it genuinely narrows
or flips. Henry Hub pricing should reference the November contract (now
front-month) going forward, not be compared directly against the expired
October settlement. FICO's mortgage-scoring-monopoly threat remains worth
watching for read-across moves in Equifax and TransUnion. The Wells
Fargo/Pinnacle Financial and BofA/Grocery Outlet upgrades remain unverified
(single-aggregator-sourced, no price targets) if they resurface. Threads
closed after resolution rather than carried further: August PCE (confirmed
print replaces the carried consensus); the WTI/Brent contract-roll watch
(no roll, window now dated to approx. 16-20 Oct); Henry Hub natural gas
sourcing (resolved with a clean settlement); the silver sign conflict
(resolved, all sources agree); the RBA's October decision preview (already
closed at edition 31).
