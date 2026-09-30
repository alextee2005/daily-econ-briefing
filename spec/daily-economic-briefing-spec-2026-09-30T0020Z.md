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
  weekend edition.

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
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed fresh again at
  edition 31 directly against federalreserve.gov's own FOMC calendar page
  (Dec 8-9 is the next SEP meeting after that). Re-confirm the date is still
  listed unchanged each edition as that meeting approaches — it is now under
  four weeks out, so keep checking every edition.
- **October-hike odds remain hike-favored and the CME dispersion narrowed
  somewhat at edition 31 — re-verify fresh every edition and expect continued
  volatility into the 27-28 Oct meeting:** Polymarket read approx. 68-69%
  hike Tuesday 29 Sept (essentially flat vs. Monday's approx. 69%). Kalshi's
  own reporting (its direct API/site again returned **HTTP 429 for a tenth
  straight edition, 23-31** — a firmly confirmed structural gap) put hike
  odds at approx. 65-69.5% via secondary citations. **CME FedWatch's
  secondary citations narrowed to approx. 68-77% at edition 31** (down from
  edition 30's approx. 54-85%) — the recurring stale approx. 54% figure that
  had persisted across three straight editions did not reappear this run,
  though this single data point shouldn't yet be read as the stale-republish
  problem being permanently resolved. Still too dispersed to cite a single
  CME figure; report the range. Treat the true consensus as "hike-favored,
  high-60s-to-high-70s%" — narrower than edition 30's read but still not a
  single clean number.
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
  edition 31 directly against bankofengland.co.uk's own MPC-dates page — the
  date is now about five weeks out, so re-confirm again next edition or two as
  it approaches.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus — resolved, does not need re-verifying.
  **The Bank of Japan's next policy meeting is confirmed for October 29-30,
  2026**, re-confirmed again at edition 31 direct from boj.or.jp's own
  Monetary Policy Meeting schedule page — now about a month out; re-confirm
  again next edition or two as it approaches.
- **The four-central-bank Thursday 24 September 2026 cluster remains fully
  resolved — closed thread, do not re-open:** Norges Bank hiked 25bp to 4.50%
  (hawkish surprise); Riksbank held at 1.75% (matching an 18-economist
  Bloomberg survey) but signalled a greater chance of a Q4 hike; Banxico held
  at 6.50% unanimously; SNB held at 0% and raised its inflation forecasts
  (0.7%/0.8%/0.8% for 2026-28), confirmed directly against snb.ch. No fifth
  central-bank decision was identified in this window either.
- **The Reserve Bank of Australia's Tuesday 29 September 2026 decision is now
  outcome-confirmed — closed thread, do not re-open:** edition 30's preview
  (+25bp to 4.60%) was correct. The RBA hiked 25bp to **4.60%, unanimous**, a
  15-year high and its fourth hike of 2026, confirmed directly against
  rba.gov.au's own Statement by the Monetary Policy Board. The Board cited
  inflation at 3.5% against a 2-3% target band and said it will raise further
  "if needed."
- **August 2026 PCE inflation (Personal Income and Outlays) is confirmed for
  Wednesday 30 September 2026, 8:30am ET** — this print lands the day after
  edition 31's cutoff and should be the first item verified at edition 32,
  against the actual release, not the consensus below. **The consensus
  figures were re-derived fresh at edition 31 (not just carried forward) and
  came in different from edition 30's carried-forward numbers — a correction,
  not a restatement:** forecaster surveys now cluster around headline approx.
  +0.3% m/m (down from the approx. +0.4% carried at edition 30) with y/y
  estimates split across two non-comparable measures (approx. 2.7% per
  survey consensus vs. approx. 3.78% per the Cleveland Fed's Nowcast — report
  both, don't blend them); core approx. +0.2-0.3% m/m and approx. 3.4% y/y
  (up slightly from edition 30's carried 3.3%). Re-verify these consensus
  figures fresh again at edition 32 if the print hasn't landed by cutoff, and
  once the actual print lands, replace this entire entry with the confirmed
  figures and close the thread. One desk (BofA) previously flagged that
  BEA's concurrent annual benchmark revisions could mechanically shave
  roughly 0.2pp off the y/y prints, worth a footnote if the actual print looks
  like a "beat" purely on a revised base.
- **The US-China "30-for-30" tariff framework remains at the
  list-identification stage, unchanged since edition 30's primary-source
  confirmation** (re-checked fresh at edition 31, no new implementation news
  found): USTR.gov and whitehouse.gov confirm a framework recommending
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
  **Editions 27, 28, 29 and 30 are all clean counter-examples worth keeping in
  mind**: all four posted an AP wire in time (ed. 28 via WTOP/ABC News, ed.
  29 and ed. 30 via similarly-timed syndication), and their figures
  cross-checked cleanly against an independent second pull (Yahoo Finance) —
  so treat AP/Reuters as "try first, expect to sometimes need the fallback
  chain," not as unreliable by default. Always have Yahoo Finance + FRED
  ready as the working fallback regardless of which way this edition goes.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example (Trefis "Market Movers" re-serving
  Friday 18 Sept's figures under a Monday 21 Sept URL); edition 26 caught
  another (several "AP" reposts of Monday 21 Sept's numbers under a Tuesday
  22 Sept dateline); edition 27 caught a third (a techflowpost article
  reproducing Tuesday's numbers under a Wednesday URL); edition 28 caught a
  fourth and fifth in the same run (a WebSearch AI summary mislabeling
  Wednesday's VIX close as Thursday's; a 24/7 Wall St. article restating
  Wednesday's Airbnb close as current). Edition 29 was the first clean
  edition in six straight on this specific trap. **Edition 30 surfaced a
  related but distinct case: Apple's $5.7bn+ Taction Technology patent
  verdict was delivered Friday 25 Sept (after that day's close) but was never
  picked up by edition 29** — not a stale-date repost, but a genuine gap
  where a real, dated event fell through the cracks of the prior edition's
  research pass entirely. It surfaced a session late at edition 30 via the
  equities pass's own broader search. **Lesson: an event missed by a prior
  edition should be surfaced as a dated catch-up item the moment it's found,
  not silently dropped for having "already happened."** A same-day close and
  a next-day after-hours-triggered move can legitimately combine into one
  large single-day % change — edition 24's Xenon Pharmaceuticals -30.7%
  Friday move is the reference example. Check whether a headline % move is
  measured close-to-close before assuming two reports conflict. **The
  intraday-vs-close divergence trap (distinct from stale-dating) is still
  very much alive**: Worthington Enterprises (ed. 26), Paychex/Cracker Barrel
  (ed. 27), Oracle (ed. 28), Akamai and the STX/WDC/SNDK storage cluster
  (both ed. 29), and **at edition 30, MongoDB's close was reported anywhere
  from -15% to -27% across aggregators depending on measurement window** —
  resolved by treating stockanalysis.com's confirmed close (-18.46%) as
  authoritative over any aggregator's intraday-low or open-to-close figure.
  Treat a stockanalysis.com (or equivalent timestamped) closing print as
  authoritative over any pre-market, intraday, or "ahead of the open" figure,
  and cross-check against a second independent source when available.
- Do not repeat items already carried in the previous edition.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. Check whether two conflicting prices are actually two different
  instruments/timestamps before treating it as a sourcing failure. The
  Kitco-vs-USAGOLD gap, which had narrowed to $0.16 by edition 28 and ticked
  up to approx. $4.78 at edition 29 (normal vendor noise), **widened sharply
  to approx. $32 at edition 30** during Monday's fast approx. 3-5%
  single-session gold/silver sell-off — most likely a vendor snapshot-timing
  artifact during a rapid move (backing out USAGOLD's implied Friday close
  showed the two vendors were tightly aligned on Friday, only diverging
  intraday Monday) rather than a reopened fundamental split, but the jump is
  large enough to re-check at the very next close before calling it resolved
  again. Similarly, **a price level can be correct while a vendor's stated
  %-change is wrong** if the vendor used a different prior-day base — always
  sanity-check that a stated price and stated % change reconcile
  arithmetically against the prior session's logged close. Edition 30 hit a
  live example: Treasury's own par-yield CSV implied the 2-year rose approx.
  +11bp Monday, while a secondary commodities-desk note's own quoted level
  implied only approx. +5bp off a different Friday baseline — both agreed on
  Monday's approx. 4.92% level, not on the size of the move; disclosed as
  unreconciled rather than picking one. Treasury's CSV showed the 2-year
  easing to 4.89% and the 10-year pushing to a fresh 24-year high (approx.
  5.26%) at Tuesday's close (edition 31) — the move-size mismatch itself was
  not re-chased, just the level. **The oil contract-month-roll trap** was
  checked and absent again at edition 30 and 31 (both Monday's and Tuesday's
  WTI/Brent settles reconciled to the penny against the prior day's logged
  close, implying no roll) — now absent in four of the last eight editions
  checked; keep checking every time regardless of recent history. **Both
  contracts are close enough to expiry that a roll to the December contract
  is plausible as soon as Wednesday — re-check explicitly at the next
  close, don't assume the pattern continues on inertia.**
- **The DXY-vs-its-own-FX-crosses conflict, which recurred at editions 29 and
  30, substantially resolved at edition 31 — treat as closed unless it
  recurs again.** Friday and Monday both showed a mismatch between DXY's
  stated direction and what EUR/GBP/JPY (roughly 83% of the basket) implied.
  **Tuesday's read reconciled cleanly**: DXY rose (four sources converged,
  approx. +0.16% to +0.30%) while EUR/USD and GBP/USD (together approx. 70%
  of the basket) both moved in the same dollar-strength direction; only
  USD/JPY (approx. 14% weight) diverged, too small to contradict the
  aggregate, and a rough weighted reconstruction landed inside the reported
  DXY range. **Do not re-open this as a live anomaly unless a fresh mismatch
  appears** — if it does, go straight to the heavier verification pass this
  entry previously called for (ICE DXY futures settlement directly, or a
  fourth independent FX-crosses source) rather than logging a third
  "first occurrence."
- **New at edition 31 — a same-day silver sign conflict**: Kitco and USAGOLD
  both showed Tuesday's silver modestly *up* (approx. +0.1% to +0.4%), while
  an Investrade end-of-day wrap showed it *down* approx. -0.92% off a
  seemingly different reference point. Dollar levels were tightly clustered
  (within about 40 cents) so this isn't a big level disagreement, just a
  sign/reference-point one — disclosed rather than resolved at edition 31;
  re-check at the next close to see whether it recurs.
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
  Edition 29 still caught one stray `~` in a late-added disclosure-box
  bullet. **Edition 30 rendered clean at zero tildes on the first check** —
  a reminder that writing "approx." consistently from the first draft, not
  just fixing it up after, is what actually prevents this, not luck.
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 24 needed CFTC leveraged-funds
  positioning normalized "as % of open interest" but couldn't source total OI
  for the exact CoT date; it substituted "net position as % of the
  leveraged-funds category's own gross long+short" instead. Edition 29 hit a
  milder version (only ES had a full OI/gross breakdown, not NQ/RTY) and
  fell back to prose plus the sector-proxy chart instead of a partial-data
  CoT chart. **No new CoT report posted within edition 30's window** (the
  Tue 22 Sept report logged at edition 29 is still the most recent; the next
  is due approx. Fri 2 Oct, covering Tue 29 Sept) — this scenario did not
  recur at edition 30, but the lesson stands for whenever it does: check that
  a *consistent* normalization (or at least a consistent unit) is available
  across every instrument in the chart before committing to it, and fall
  back to prose plus the standing sector-proxy default if you can't.
- **When an "optional" filler element (e.g. a levels table) would just
  restate the same instrument list already in a main table with one extra
  column, that's still legitimate as long as the extra column is genuinely
  additive** (editions 25 and 28 both added a prior-session-baseline-vs-close
  levels table to a short page 3) — don't reject the idea purely because the
  instrument list overlaps; check whether the *added* column carries real
  information first. **Editions 26, 27, 29 and now 30 did not need this
  padding at all** — page 3 filled cleanly from content alone every time.
  This is now four of the last five editions where no filler was needed —
  keep reaching for the optional levels table only when page 3 actually runs
  short after the two default end-of-Section-6 blocks, not as a routine
  addition.
- **The single-stock movers bar-chart outlier-capping rule finally hit a
  genuine order-of-magnitude case at edition 30**: Kodiak Sciences (KOD)
  spiked +177.96% on a Phase 3 trial win, versus the next-largest mover
  (AMC Entertainment) at +11.90% — roughly a 15x spread, comfortably past the
  approx. 10x threshold the rule was written for but had never actually been
  tested against. It was capped at a fixed axis max of 30 with a
  "(capped)" value-label annotation per the standing rule, and the render
  came out legible with the other six bars still readably scaled. **This
  confirms the capping mechanism works in the wild, not just in theory** —
  keep using the same approach (fixed cap, annotated label) the next time a
  10x+ outlier appears; there's no need to raise or lower the approx. 10x
  threshold based on this one data point.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` delayed-quotes JSON endpoint first — it often
  returns VIX, VIX9D, VIX3M, VIX6M, VVIX and SKEW directly, but has (at least)
  three observed failure modes: (a) a full clean sweep with genuinely fresh
  timestamps on every series, (b) the more common "thin-series-stale"
  pattern, (c) total failure, where every series is stale. **Editions 28, 29,
  30 and 31 all got a full clean sweep** — every series carried a same-day
  `last_trade_time`, verified individually per series via a raw `curl` pull
  (not a tool-summarized fetch — see Hard rules above for why) each time.
  Four consecutive clean sweeps is encouraging but not a guarantee — keep
  checking `last_trade_time` on each series every time. Also note a
  `prev_day_close` field bug, observed **eight of the last ten editions
  (22-29, not 30 or 31)**: it duplicates the day's own `close`/`current_price`
  rather than giving a real prior-day reference, corrupting the feed's own
  `price_change`/`price_change_percent` fields too. **The bug did not
  manifest at either edition 30 or 31** — two straight clean editions on this
  specific field now. Treat this as intermittent, not resolved — **always
  compute day-over-day % change manually against the previous edition's
  logged close regardless of whether the feed's own fields look correct this
  time**, since there's no way to tell in advance which behavior you'll get.
  Fall back to news coverage if a series is stale, and disclose it as
  single-sourced. The VIX9D-vs-spot-VIX front-end inversion first flagged at
  edition 28 (resolved as noise at edition 29) **recurred at edition 30 and
  persisted, even widening slightly, at edition 31** — Tuesday's VIX9D
  (14.21) sat further below spot VIX (16.04) than Monday's gap (-1.83 vs.
  -1.68), while VIX3M/VIX6M kept their normal upward slope both days. Two
  straight sessions of a widening (not narrowing) inversion makes this look
  less like noise and more like a genuine medium-dated repricing — keep
  watching whether the front end normalizes at the next close, and consider
  calling it a settled feature of the current vol regime if it persists a
  third session.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table
  and (absent fresher CoT data or another dominant story) chart #2. Worked
  cleanly again at editions 27, 28, 29, 30 and 31; no second same-day
  sector-ETF source has ever been found, so this remains a standing
  single-sourced item, disclosed each edition. **Stockanalysis.com
  single-stock pages are also the standing default for pinning an exact
  closing price/% change on any individual mover** — editions 26 through 31
  all used direct fetches to it to resolve conflicting intraday-move
  percentages (edition 30: MongoDB's -15% to -27% cross-aggregator spread,
  resolved to -18.46%; edition 31: Fair Isaac's close of -26.52% used as
  authoritative over an intraday "up to -27%" commentary reference, and
  Bloom Energy/CarMax pre-close snapshots rejected in favor of the 4pm
  close). Worth doing proactively for any mover whose research-pass figures
  disagree by more than a rounding error. Note that a headline wire's own
  GICS sector-index percentages can differ slightly from the SPDR ETF
  price-change figures (a normal index-vs-ETF-price methodology gap); keep
  using the SPDR ETF figures as the table's primary numbers.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. Not chased at
  editions 30 or 31 — no research pass has flagged a need for it recently.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — now recurred at editions 22, 24-31
  (nine straight, still worth a quick attempt each time in case it
  recovers). **zerogex.io is now confirmed across five straight clean
  editions (27-31)**: edition 29 gave a striking approx. 9x magnitude jump
  flagged as anomalous, edition 30 flipped sign entirely (Friday's
  +$32.56bn to Monday's -$9.33bn) but the swing was well-explained by spot
  crossing the gamma flip point, and **edition 31 moved further negative
  still (-$17.19bn) as spot (approx. 7,671) sat further below a higher flip
  point (approx. 7,709)** — a plausible progression, corroborated
  directionally by a secondary options-flow note describing negative gamma
  at nearly every strike. Continue treating zerogex.io as the standing
  default source for dealer gamma, and continue the discipline of checking
  each new reading's plausibility against the day's actual index move rather
  than passing it through uncritically. **Minor open item**: zerogex's own
  stated wall levels (call/put wall) have not reconciled cleanly against a
  secondary options note's implied walls at edition 31 — only the net
  GEX sign/magnitude has been cross-checked so far, not the individual wall
  levels; low priority, revisit only if a wall-level figure becomes
  load-bearing for a specific call.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. The
  secondary-citation split had widened for three straight editions (28-30,
  peaking at edition 30's approx. 54-85% range, anchored by a recurring
  stale approx. 54% figure) but **narrowed at edition 31 to approx. 68-77%,
  and the stale approx. 54% figure did not reappear** — encouraging, but
  treat as one data point, not confirmation the stale-republish problem is
  fixed; keep naming the stale-54% figure explicitly if it resurfaces. Keep
  treating CME FedWatch as needing a disclosed range, not a single figure.
- **Kalshi direct fetch:** now rate-limited (HTTP 429) for **ten straight
  editions (23-31)** — a confirmed structural gap, not transient. Keep
  attempting each edition (it may recover), but a one-line "failed again,
  Nth straight edition" is sufficient prose; use Kalshi's own secondary
  reporting (its blog, prediction-market news aggregators) as a workaround,
  as editions 30 and 31 did to get 65-69.5% reads.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  ten editions running (22-31)** — treat as durable; default straight to
  the fallback chain. Shanghai Metals Market (metal.com) has also now failed
  nine editions running (22-30, not re-attempted at 31 per the standing
  "skip it entirely" guidance) — go straight to Westmetall.com, which has now
  worked cleanly **ten editions running** as the fallback, including an
  exact match against the prior edition's logged close at both edition 30
  and edition 31 (two straight good continuity validations). Disclose
  whichever was used. Because the fallback chain can change edition to
  edition, treat any day-over-day copper % change built across two different
  sourcing chains as approximate.
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) worked
  cleanly again at edition 31 with no T+1 lag for Tuesday's print (2-year
  4.89%, 10-year approx. 5.26%, both posted same-day). Prefer the CSV
  endpoint over the HTML TextView page — edition 29 found the HTML page
  mis-maps values into the wrong maturity columns; the CSV does not have
  this problem. Edition 30's disclosed 2-year move-size mismatch (Treasury
  CSV +11bp vs. a secondary note's +5bp, same approx. 4.92% level) was not
  re-chased at edition 31, just the fresh level; treat the Treasury CSV as
  the primary/authoritative source for the level and flag any future
  move-size mismatch like this rather than silently picking one.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. The most recent report remains the one
  published Fri 25 Sept, dated Tue 22 Sept: equity-index Asset Managers net
  long approx. 934,000-936,000 ES contracts vs. Leveraged Funds net short
  approx. 375,600-376,000; VIX futures non-commercial net short approx.
  79,300. **Confirmed again at edition 31 that no new report has posted**
  (still the Tue 22 Sept data on file at cftc.gov). Next report due
  **approx. Friday 2 October 2026**, which would cover Tuesday 29 Sept (the
  session edition 31 itself just reported on) — check for it fresh next
  edition, and if a CoT-based chart is wanted again, try to get
  OI/gross-long-short for all three of ES/NQ/RTY up front this time, not
  just ES.
- **GBP/USD and EUR/USD clean close:** fully resolved since edition 26 —
  Yahoo Finance/TradingEconomics/FXStreet as primary sources work cleanly,
  confirmed again at editions 27 through 31. **The DXY-vs-FX-crosses
  directional conflict, the live open thread here for two straight editions,
  substantially resolved at edition 31** — see Hard rules above for the full
  writeup. Treat as closed unless a fresh mismatch appears.
- **Gold/silver clean close on a non-event day:** the Kitco-vs-USAGOLD gap
  that widened sharply to approx. $32 during Monday's fast selloff (edition
  30) **normalized back to approx. $5 at edition 31** when compared at
  matching snapshot timestamps — consistent with the "vendor
  snapshot-timing artifact" read, not a reopened structural split. Continue
  to insist on matching timestamps before calling any future gap anomalous.
  **New at edition 31**: silver's day-over-day *sign* (not just level)
  disagreed across sources — see the new Hard-rules entry above — worth a
  fresh check at the next close.
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue — confirm on the BLS/Fed release schedule
  rather than assuming a date. **PCE inflation:** confirmed for Wednesday 30
  September 2026, 8:30am ET (see Standing facts above) — this is the day
  immediately after edition 31's session, so it will be the first macro
  item to verify at edition 32; re-confirm the actual print once it lands
  (the fresh consensus re-derivation done at edition 31 revised the
  carried-forward figures — see the correction note above), then this
  thread can close.
- **New at edition 31 — Henry Hub natural gas could not be pinned to a
  clean two-source settlement figure.** Two partial extractions agreed only
  directionally (approx. -3% to approx. $3.09-3.10/MMBtu on the October
  contract), not to the cent, and one of the two sources also produced
  clearly stale/wrong oil figures in the same pull, undermining confidence
  in it generally. TradingEconomics' live commodity page returned
  internally inconsistent values across repeated samples (a continuously-
  updating page, not a clean daily print). Try CME's own settlements page
  directly, or a Reuters/Platts wire copy, next time this is chased — don't
  over-invest if it stalls again, this is a lower-priority commodity per
  the section's own weighting (no agriculture, and gas is not explicitly
  named in the coverage brief).
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29 (the page hosts several stacked
  category tables per URL — Sum of All Products, Index Options, Equity
  Options, Exchange-Traded Products, instrument-specific tables — each with
  its own totals; the "13.78m"-range figure is the Sum-of-All-Products
  category). **At edition 30, the page would not yield Monday's data at all**
  — the default view re-served Friday's cached Sum-of-All-Products figure
  (13,939,864, correctly dated 25 Sept in the page's own markup), and
  appending a `?dt=2026-09-28` date parameter returned only a client-rendered
  JS shell with no embedded table reproducible via a plain fetch. The
  902,421 figure from edition 28 **remains genuinely unattributed** to any
  category. Going forward: always state which specific category/table a
  Cboe options-volume figure comes from, and expect the page to sometimes
  simply not yield same-day data via a plain fetch/curl approach at all —
  don't over-invest time here if it stalls, this is a secondary-priority item
  per the derivatives section's own weighting.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable at editions 30 or 31.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22) — either find a citable
  benchmark before reaching for that chart type, or stick to describing
  implied-vs-realized in prose without the third bar. Not attempted again at
  editions 23-31.
- **CFTC total open interest by instrument/date** (needed to normalize
  positioning "as % of open interest"): partially resolved at edition 29 —
  ES's total OI (approx. 1.9mn contracts) was obtained directly from
  cftc.gov, but NQ's and RTY's were not pulled. No new CoT report posted
  within editions 30's or 31's windows, so this was not re-attempted. Next
  time an OI-normalized CoT chart is wanted, fetch OI/gross-long-short for
  all three of ES, NQ and RTY explicitly up front rather than assuming one
  contract's availability implies the others'.
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear** — editions 27
  through 29 confirmed several rating changes (direction + firm name)
  without being able to pin an exact dollar price target for all of them.
  Edition 30 had a cleaner run (Morgan Stanley/BTIG on PANW, Citigroup on
  AMC, UBS on GM, Piper Sandler on ADSK/TYL all came with exact targets), and
  **edition 31 likewise got exact targets for most named actions** (JPMorgan
  on PEP/MNDY/XPEV, Leerink on TWST/BRKR, Wells Fargo on TCPC) — but could
  not confirm whether Bloom Energy's RBC ($335)/Mizuho ($351) targets were
  dated specifically Tuesday or were earlier reiterations. Report the rating
  direction and firm with confidence; treat a missing dollar target or
  unclear dating as a normal gap to flag, not something to chase hard, unless
  the name is the edition's dominant story.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29, when a long unverified
  secondary movers list was correctly rejected wholesale after two spot-
  checked names came back wrong on direction). Edition 30 hit a milder
  version (American Eagle Outfitters and four smaller names flagged to
  Annex A rather than reported as fact). **Edition 31 hit the same pattern
  again**: Iovance's exact guidance figures and Concentrix's consensus EPS
  figure were both single-sourced/unreconciled across aggregators and
  flagged to Annex A rather than asserted. **This remains the right call
  when time-constrained**: a single aggregator's claim, especially for a
  smaller or less-covered
  name, is not enough on its own — corroborate with a second source or
  flag it as unverified in Annex A.

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
  both cases. Editions 29, 30 and 31 all rendered clean at 4 pages on the
  first try with the standard single pagebreak and no filler content needed.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Editions 25 and 28 both hit a visibly short page 3 on the first render
  despite passing the 4-page check, fixed with an optional levels table.
  **Editions 29, 30 and 31 did not have this problem** — page 3 filled
  naturally from Section 3-6 content each time. This is now five of the last
  six editions where no padding was needed — don't add the optional levels
  table reflexively; check whether page 3 actually runs short first.

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
  29, 30 or 31 — five of the last six editions have filled page 3 from
  content alone).  Always re-render immediately after adding this table to confirm
  the page count if it is used, rather than assuming a "moderate" row count
  is safe (edition 28's first attempt at 12 rows overshot to 5 pages; 10 rows
  fixed it). Conversely, **if page 3 overflows by a handful of lines**, the
  cheapest trims are: shortening day-ahead table cell text, cutting one
  "sector setup" bullet or merging two into one, tightening the last prose
  paragraph in Section 5, or trimming rows from the optional levels table if
  one was added.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 3x between
  the largest and next-largest mover does not need capping — confirmed again
  at edition 26 (VKTX +35.67% vs. next-largest ONON +7.58%, about 4.7x, left
  uncapped since "order of magnitude" (approx. 10x) is the real threshold),
  edition 27 (PAYX -8.77% vs. EXPE -7.72%, about 1.14x), edition 28 (MGM
  -10.99% vs. META +4.50%, about 2.4x), and edition 29 (TWLO -7.96% vs.
  next-largest DELL +5.01%, about 1.6x — also left uncapped). Edition 30
  finally produced a genuine 10x+ case and confirmed the rule works as
  designed: Kodiak Sciences +177.96% vs. next-largest AMC +11.90% (about
  15x) was capped at a fixed axis max of 30 with a "(capped)" annotation, and
  the resulting chart stayed legible for the other six bars. **Edition 31
  reverted to the normal case** — Iovance +31.48% vs. next-largest (in
  magnitude) Fair Isaac -26.52%, about 1.2x — comfortably under the approx.
  10x threshold, left uncapped. No need to revisit the threshold or the
  mechanism; it has now been confirmed both capped and uncapped in
  back-to-back editions.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — **used for a seventh consecutive
edition at edition 31**, for a near-total reversal of Monday's sector
leadership, Utilities leading and Energy lagging as oil gave back its war
premium; edition 30 used it for a broad risk-off session led lower by
Communication Services on Meta's drag; also used at edition 29 for a Friday
relief-rally rotation, edition 28 for a Meta-Muse-driven rotation, edition 27
for a rate-spike-driven rotation into defensives, edition 26 for a
financials-vs-materials reversal, and edition 25 for a chip-led rally — this
remains a reliable, low-risk default and has now covered a genuinely wide
range of underlying stories without needing to be replaced). Fresh CFTC CoT
data on a Monday/weekend-window edition → the ES/NQ/RTY asset-manager-vs-
leveraged-funds positioning chart, **normalized as % of open interest if
that figure can be sourced for all instruments being charted; if not, a
category's own net-position-as-%-of-its-own-gross-long+short is an
acceptable, honestly-labelled substitute — but check that a *consistent*
normalization (or at least a consistent unit) is available across every
instrument in the chart before committing to it.** No fresh CoT data posted
within edition 30's or 31's windows, so this scenario did not arise either
time. A single dominant earnings print with a clean, well-sourced
implied-vs-realized-move story → a three-bar implied/historical-average/
realized move chart (the historical-average leg has never actually been
sourced successfully — see Known-hard-to-source above). A genuine
multi-sector broadening/deepening selloff across consecutive sessions → the
sector-ETF proxy rendered as a grouped (day-over-day) bar instead of
single-day. A holiday-window preview edition with no fresher data → VIX
futures term structure with event annotations. When chart #1 (movers)
already covers the earnings/single-name story, the sector proxy is a good
complementary choice even on a stock-heavy day — editions 25 through 31 have
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

**Editions 1–29 (condensed):** established the format (edition 1 baseline;
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
-7.72%, Airbnb -7.56%, Booking -5.07%) and was independently corroborated;
Paychex -8.77% (earnings-quality concerns), Cracker Barrel +4.49% (EPS beat);
gold's Kitco-vs-USAGOLD split narrowed to about $7; VIX closed 15.18
(+6.83%) on a CBOE feed "full stale sweep" failure; zerogex.io gave its
first working dealer-gamma read. **Edition 28** (Fri 25 Sept, covering Thu 24
Sept): a whipsaw session closed almost exactly flat (S&P -0.1% to 7,704.13,
Dow -0.3% to 51,349.98, Nasdaq +0.1% to 26,939.37, Russell -0.1% to
2,835.57); Communication Services (XLC +1.27%) led on a Meta rally; MGM
Resorts -10.99% (Barry Diller's People Inc. withdrew its take-private bid),
Oracle -3.47% (Blue Owl/Stargate New Mexico force-majeure notice), Darden
-3.02% (EPS/revenue miss), Costco -0.91% in the regular session ahead of an
after-close beat; all four previewed Thursday central-bank decisions
(Norges Bank hike, Riksbank hold, SNB hold, Banxico hold) confirmed, closing
that thread; the Trump-Xi Washington summit culminated Thursday, with the
US-China trade truce extended to January 10, 2027 per Bessent; oil rallied
on a Houthi strike on Saudi Arabia before paring (Brent +3.4% to $106.60,
WTI +2.7% to $94.61); gold's Kitco-vs-USAGOLD split closed to just $0.16;
zerogex.io gave a second consecutive clean dealer-gamma read; Cboe's
options-volume page surfaced an unresolved 15x same-page discrepancy
(902,421 vs. 13,781,355), substantially explained at edition 29. Edition 29
(Mon 28 Sept, covering Fri 25 Sept, the week's one session): a relief rally
closed the week higher (S&P +0.5% to 7,743.41, Dow +0.9% to 51,828.62,
Nasdaq +0.5% to 27,068.72); Meta -3.33% on the Cambridge Analytica verdict
(theoretical exposure up to approx. $219.5bn), Costco +2.93%, Twilio -7.96%
(HSBC downgrade), Akamai +3.20%, Dell +5.01%; a new CFTC CoT report posted
(dated Tue 22 Sept, Asset Managers net long approx. 934-936k ES vs.
Leveraged Funds net short approx. 375.6-376k); the US-China $30bn
tariff-cut agreement was reported (unconfirmed via primary source at the
time, later confirmed at edition 30); a fresh Houthi attack on Riyadh and a
rejected Iranian Hormuz-reopening proposal kept an oil-risk premium alive
into Monday; a first DXY-vs-FX-crosses directional mismatch surfaced (later
recurred at edition 30, resolved at edition 31); zerogex.io flagged an
anomalous approx. 9x dealer-gamma jump (+$32.56bn), later explained at
edition 30 as a gamma-flip-crossing effect.

**Edition 30 (condensed)** — Tue 29 Sept 2026 report covering Monday 28
September 2026, the window's one NYSE session. A broad risk-off reversal
erased the prior week's relief rally: S&P 500 -0.77% to 7,683.69, Dow -0.67%
to 51,481.51, Nasdaq -0.92% to 26,820.38, Russell -0.69% to 2,817.91, driven
by Trump rejecting an Iranian Hormuz-reopening offer and the 10-year
spiking to approx. 5.24%; oil spiked intraday then pared to Brent $105.28
(+0.92%)/WTI $92.60 (+0.21%). Kodiak Sciences +177.96% (Phase 3 win, capped
in chart 1 as the capping rule's first genuine 10x+ outlier); MongoDB
-18.46% (CEO CJ Desai resigned to Meta, interim CEO Dev Ittycheria); Meta
-4.79% (MongoDB-hire optics + a new Muse AI privacy complaint); Roblox
-9.86%; Boeing -6.91% (FAA 737 MAX 10 certification delay); Palo Alto
Networks +4.63%; AMC +11.90%; Nvidia +1.68% ($150bn buyback authorization);
CrowdStrike +2.82% (DOJ probe closure); Apple's Friday Taction patent
verdict surfaced as a catch-up item missed by edition 29. Fed Chair/FOMC/
BoE/BoJ dates re-confirmed; October-hike odds jumped (Polymarket to 69%,
CME dispersed to approx. 54-85%); the US-China "30-for-30" tariff framework
was confirmed via primary sources (USTR.gov, whitehouse.gov); the RBA's
Tuesday decision was previewed (+25bp to 4.60%, later confirmed correct at
edition 31). Gold's Kitco-vs-USAGOLD gap widened sharply to approx. $32
(later normalized at edition 31); the DXY-vs-FX-crosses conflict recurred
for a second session (later substantially resolved at edition 31); VIX
16.07 (+8.07%); zerogex.io's SPX gamma flipped to -$9.33bn, explained by
spot crossing the gamma flip point. 47 sources, zero mismatches after fixing
one letter-suffixed citation (`[9b]`); clean 4-page render on the first
attempt.

**Edition 31 (most recent — full detail)** — Wed 30 Sept 2026 report
covering Tuesday 29 September 2026, the window's one NYSE session, research
window Mon 28 Sept 20:00 ET through Tue 29 Sept 20:20 ET. Verified the two
structural header rules again: date line reads the edition date (Wednesday
30 September 2026), not the session date; window line states the given
research-window start (Mon 28 Sept 20:00 ET) with the actual session
covered noted parenthetically.

A quiet mean-reversion session after Monday's risk-off shock: S&P 500 -0.16%
to 7,670.84, Dow -0.26% to 51,349.92, Nasdaq Composite -0.09% to 26,797.54,
Russell 2000 -0.35% to 2,807.92 — confirmed via AP (through wtop.com)
cross-checked against ETF proxies, with one AI-search-synthesis pass's
materially different ETF figures discarded in favor of direct
stockanalysis.com fetches with exposed "at close" timestamps. Nasdaq-100
(QQQ +0.19%) diverged positive against the Composite's small decline as
Meta's rally offset broader semiconductor/small-cap weakness. Sector
leadership was a near-total reversal of Monday: Utilities (XLU +1.17%) led,
Energy (XLE -0.90%) lagged as oil gave back most of Monday's Hormuz-driven
spike — Brent -2.6% to $102.59, WTI -3.48% to $89.38, both settles
reconciling to the penny against Monday's logged closes across two sources
(a competing approx. $96 Brent figure from one search result did not
reconcile and was rejected as a likely extraction error).

Single-name stories: Fair Isaac (FICO) -26.52%, the session's dominant
mover — FHFA Director Bill Pulte announced Fannie Mae/Freddie Mac will move
to a unified mortgage-pricing model blending VantageScore alongside FICO
scores, directly threatening FICO's credit-scoring monopoly (a potential
read-across risk for Equifax/TransUnion); Iovance Biotherapeutics +31.48%
(raised FY revenue guidance, primary release not located); Carnival +13.41%
(Q3 beat, record revenue, but Q4 EPS guide below consensus); Bloom Energy
+10.80% (AI-data-center power-demand rally); CarMax +4.74% (fiscal Q2 EPS
$1.16 vs. $0.73 consensus); Meta +3.24% on a new "Muse for Small Business"
launch even as two negative threads stayed live (a Cambridge Analytica
penalty hearing set for Thu 1 Oct; the Muse AI privacy-complaint fallout
continuing without a fresh Tuesday-specific escalation); Monday.com -3.80%
(JPMorgan downgrade); Concentrix -2.24% (Q3 EPS $2.92 primary-confirmed,
consensus comparison unreconciled across aggregators). PepsiCo (JPMorgan
downgrade, PT cut to $138 from $170) and Warner Bros. Discovery (Argus
downgrade to Sell) both barely moved, suggesting both cuts were priced in.
Boeing +1.78% (post-selloff stabilization, no new 737 MAX 10 news); MongoDB
+0.75% (Investor Day; interim President Ittycheria says the board is "not
in a rush" on a permanent CEO successor).

Macro: the RBA's previewed Tuesday decision is now outcome-confirmed — hiked
25bp to 4.60%, unanimous, a 15-year high, closing that thread. Fed Chair
Kevin Warsh, the Oct 27-28 FOMC date, the BoE's Nov 5 decision and the BoJ's
Oct 29-30 meeting were all re-confirmed fresh. October-hike odds held
hike-favored (Polymarket approx. 68-69%, Kalshi secondary approx. 65-69.5%)
while CME's secondary citations narrowed to approx. 68-77% (from edition
30's approx. 54-85%), and the recurring stale approx. 54% figure did not
reappear. The US-China "30-for-30" tariff framework remains unchanged,
still pending implementation. **The carried-forward Wednesday-PCE
consensus was corrected**, not just re-dated: fresh forecaster surveys now
show headline approx. +0.3% m/m (down from approx. +0.4%) with y/y split
across two non-comparable measures (approx. 2.7% survey vs. approx. 3.78%
Cleveland Fed Nowcast), core approx. +0.2-0.3% m/m/approx. 3.4% y/y (up
from approx. 3.3%).

Commodities/FX: gold's Kitco-vs-USAGOLD gap, which widened to approx. $32 at
edition 30, normalized back to approx. $5 at matching snapshot timestamps —
consistent with the vendor-timing-artifact read. A new silver sign conflict
emerged (Kitco/USAGOLD show Tuesday up approx. +0.1-0.4%; an Investrade
wrap shows -0.92%), disclosed unresolved. Copper via Westmetall $14,474.50/t
(-0.48%; LME.com failed a tenth straight edition). **The DXY-vs-FX-crosses
conflict, live for two straight editions, substantially resolved**: DXY
rose (four sources, approx. +0.16-0.30%) with EUR/USD and GBP/USD (approx.
70% of the basket) both consistent in direction; only USD/JPY diverged, too
small to contradict the aggregate. Henry Hub natural gas could not be
pinned to a clean two-source settlement figure (approx. -3% directionally
only). Treasury's CSV showed the 2-year easing to 4.89% (from 4.92%) and
the 10-year pushing to a fresh 24-year high (approx. 5.26%).

Derivatives: the CBOE feed gave a fourth consecutive full clean sweep (VIX
16.04 -0.19%, and for a second straight edition the `prev_day_close` bug did
not manifest); VIX9D's inversion below spot VIX persisted and widened
slightly (-1.68 to -1.83), now looking less like noise and more like a
genuine medium-dated repricing. zerogex.io's SPX net dealer gamma moved
further negative to -$17.19bn (from -$9.33bn) as spot sat further below a
higher gamma flip point — a plausible progression, corroborated
directionally by a secondary options-flow note. A Cboe Insights note was
again found referencing a stale, pre-Monday VIX level rather than a Tuesday
reading. CFTC CoT confirmed unchanged since the Tue 22 Sept report (next due
approx. Fri 2 Oct, covering today's Tue 29 Sept data). 39 sources, zero
mismatches on the first `check_refs.py` run; zero stray tildes on the first
check; page 3 filled cleanly from content alone; rendered a clean 4 pages on
the first attempt.

**Open threads for edition 32:** Wednesday 30 Sept's PCE print (8:30am ET)
is the week's key data risk and should be the first item verified — use the
corrected consensus above, and once the actual print lands, replace the
whole standing-facts entry with the confirmed figures and close the thread.
Watch for Meta's Cambridge Analytica penalty-hearing outcome (Thu 1 Oct,
Judge Francis Mathew) — Meta still carries two live negative threads (the
CA penalty path and the Muse privacy-complaint fallout) worth tracking
separately. ISM Manufacturing (Thu 1 Oct, consensus approx. 55.0, secondary
aggregator only) and the September jobs report (Fri 2 Oct, consensus
nonfarm payrolls approx. +90-100k, unemployment 4.1%) are also due. Re-check
whether Tuesday's silver sign conflict (Kitco/USAGOLD up vs. Investrade
down) recurs or resolves at the next close. Re-check whether WTI/Brent
rolled from the November to the December contract, since both were flagged
as close enough to expiry that a roll is plausible imminently. Watch
whether VIX9D's inversion below spot VIX normalizes or persists a third
session. Henry Hub natural gas still needs a clean two-source settlement
figure — try CME's settlements page directly or a Reuters/Platts wire copy
next time. FICO's mortgage-scoring-monopoly threat is worth watching for
read-across moves in Equifax/TransUnion and for any FHFA follow-through.
Bloom Energy's RBC/Mizuho price-target dating, and Concentrix's exact
consensus EPS figure, remain low-priority unverified items. The
DXY-vs-FX-crosses conflict is treated as closed after edition 31's
resolution — do not re-open unless a fresh mismatch actually appears.
Threads closed after resolution rather than carried further: the RBA's
actual Tuesday decision (confirmed +25bp to 4.60%, matching the preview);
Boeing's 737 MAX 10 situation (no new edition-31 news, treated as
post-selloff stabilization for now, but reopen if a certification-timeline
update surfaces).

