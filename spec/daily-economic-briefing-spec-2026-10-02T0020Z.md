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
  is where the sessions covered belong, not the date line. **Edition 33 applied
  this correctly again** ("Friday 2 October 2026" as the date line, with the
  window line carrying "Thu 1 Oct close/AH, the window's one NYSE session").
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
  weekend edition. **Editions 32 and 33 both reused the identical pattern**
  ("Window: Wed 30 Sept 2026 20:00 ET – Thu 1 Oct 2026 20:20 ET (Thu 1 Oct
  close/AH, the window's one NYSE session)" at edition 33) — now confirmed
  clean across five consecutive single-session editions (29 through 33,
  adjusting phrasing for the weekend case at 29). No further confirmation
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
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 33
  directly against federalreserve.gov's own FOMC calendar page (Dec 8-9 is the
  next SEP meeting after that). The meeting is now about four weeks out —
  continue re-confirming every edition between now and then.
- **October-hike odds split sharply across venues at edition 33 for the first
  time since edition 32's unified collapse — re-verify fresh every edition:**
  after all three venues converged in the mid-30s% through edition 32
  (Wednesday 30 Sept), edition 33 (Thursday 1 Oct) saw **Polymarket drift
  further dovish to approx. 25–26% (no-change 75%, direct fetch)** while
  **Kalshi's secondary citations held near 36–37%** and **CME FedWatch's
  secondary citations clustered near 36–38% hike / approx. 62% hold** — i.e.
  Kalshi and CME were roughly flat-to-firmer from Wednesday while Polymarket
  alone drifted lower, reopening a cross-venue spread after the brief
  edition-32 unification. Treat the honest range going into edition 34 as
  "approx. 25–38% depending on venue," not a single consensus number, and
  keep watching whether Polymarket's divergence from Kalshi/CME is itself
  signal or noise. September's jobs report (Fri 2 Oct, due right after edition
  33's cutoff) is the next scheduled catalyst that could move this materially.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch,
  rba.gov.au, etc.) every edition, exactly like any other data point. **Edition
  33 reconfirmed Kevin Warsh as Fed Chair directly against federalreserve.gov's
  Board of Governors bios page** (Senate-confirmed 54-45 on 13 May 2026, sworn
  in 22 May 2026) — worth citing explicitly in copy when the Chair is
  referenced, not just carrying it silently.
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026**, re-confirmed again at
  edition 33 directly against bankofengland.co.uk's own MPC-dates page — about
  five weeks out; re-confirm again next edition or two as it approaches.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus — resolved, does not need re-verifying.
  **The Bank of Japan's next policy meeting is confirmed for October 29-30,
  2026**, re-confirmed again at edition 33 direct from boj.or.jp's own
  Monetary Policy Meeting schedule page — about four weeks out; re-confirm
  again next edition or two as it approaches. **Note: edition 33 only
  re-checked the meeting date, not the current policy rate level itself** —
  re-verify the approx. 1.25% figure directly next edition rather than assuming
  it is still current.
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
- **The US-China "30-for-30" tariff framework remains at the list-
  identification stage, unchanged since edition 30's primary-source
  confirmation** (re-checked fresh again at edition 33, no new implementation
  news found): USTR.gov and whitehouse.gov confirm a framework recommending
  reduced tariff treatment for $30bn of goods on each side (77 Chinese
  products, 1,600+ US products — edition 32 separately logged updated list
  sizes of 77/1,619 post-Trump-Xi-summit), administered via the new US-China
  Board of Trade. Still pending each side's domestic legal processes — watch
  for a formal implementation/effective date in a future edition.
- **No US federal government shutdown is in effect — confirmed fresh at
  edition 33, a new standing fact worth tracking going forward:** a continuing
  resolution (H.R. 6500 / P.L. 119-103), signed into law 2 September 2026,
  funds the government through **11 December 2026**, confirmed directly
  against a dated whitehouse.gov briefing, congress.gov CRS product R49353,
  and GovTrack.us. This matters because October 1 is a routine shutdown-risk
  date and this report nearly carried an unverified shutdown premise into
  print; it was checked and refuted against primary sources instead — exactly
  the discipline this report's "verify from primary sources, not memory or
  framing" rule exists for. **Watch for shutdown risk resurfacing as 11
  December 2026 approaches**, and note that whitehouse.gov also hosts a
  separate generic "Government Shutdown Clock" page whose content described an
  active shutdown narrative inconsistent with the dated CR evidence — treat
  that page as unreliable/stale rather than authoritative if it resurfaces.

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
  after it. **Edition 33 reused the same source number for multiple movers
  citing the same outlet (e.g. `[3]` for every stockanalysis.com single-stock
  close)** rather than minting a fresh number per ticker — this is fine and
  recommended: `check_refs.py` only checks presence/absence of each number,
  not uniqueness of use, so one Annex B entry can legitimately back many
  inline citations when it is genuinely the same source/method.
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
  **Editions 27 through 33 are all clean counter-examples worth keeping in
  mind**: all seven posted a usable AP wire in time and their figures
  cross-checked cleanly against an independent second pull (ETF proxies or
  Yahoo Finance/CNBC/TheStreet) — edition 33's S&P/Dow/Nasdaq figures all
  reconciled to the penny against two independent sources, and its Russell
  2000 figure was confirmed by direction (not exact level) via a second
  source (IWM) after a WebSearch AI-summary artifact claimed an obviously
  wrong -5.4% move that didn't match any other evidence and was discarded.
  Treat AP/Reuters as "try first, expect to sometimes need the fallback
  chain," not as unreliable by default. Always have Yahoo Finance + FRED/
  stockanalysis.com ready as the working fallback regardless of which way
  this edition goes. **Edition 33 lesson: a WebSearch tool's own AI-generated
  summary can itself be a bad, uncorroborated source** — it asserted a
  Russell 2000 move that no primary or secondary source backed and that
  contradicted the figure already in hand; when a single search-summary
  claim conflicts with everything else and cites no identifiable article,
  treat it as noise, not a second data point, and verify via a direct
  instrument fetch (e.g. the tracking ETF) instead.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example (Trefis "Market Movers" re-serving
  Friday 18 Sept's figures under a Monday 21 Sept URL); edition 26 caught
  another (several "AP" reposts of Monday 21 Sept's numbers under a Tuesday
  22 Sept dateline); edition 27 caught a third (a techflowpost article
  reproducing Tuesday's numbers under a Wednesday URL); edition 28 caught a
  fourth and fifth in the same run (a WebSearch AI summary mislabeling
  Wednesday's VIX close as Thursday's; a 24/7 Wall St. article restating
  Wednesday's Airbnb close as current). Edition 32 caught a sixth and
  seventh (Rio Times republishing Tuesday 29 Sept's oil AND gold/silver wraps
  under a Wednesday 30 Sept dateline). **Edition 33 caught an eighth and
  ninth**: a Rio Times Brent-roll article headlined for Thursday was
  confirmed via direct date-check to actually describe Wednesday's session,
  and a separate Rio Times copper article headlined "Thursday" likewise
  described Wednesday's LME print — both excluded in favor of same-day
  sources (Investrade, Westmetall, investing.com) once the figures were
  checked against the prior day's logged closes. This trap remains very much
  alive and Rio Times specifically has now mis-dated content in at least
  three separate editions (32 twice, 33 twice) — treat any Rio Times article
  with extra suspicion and always date-check its content against the
  previous edition's logged closes before using it. A same-day close and a
  next-day after-hours-triggered move can legitimately combine into one
  large single-day % change — edition 24's Xenon Pharmaceuticals -30.7%
  Friday move is the reference example. Check whether a headline % move is
  measured close-to-close before assuming two reports conflict. **The
  intraday-vs-close divergence trap (distinct from stale-dating) is still
  very much alive**: Worthington Enterprises (ed. 26), Paychex/Cracker
  Barrel (ed. 27), Oracle (ed. 28), Akamai and the STX/WDC/SNDK storage
  cluster (both ed. 29), MongoDB (ed. 30), Liquidia and Concentrix (both ed.
  32), and **at edition 33, Concentrix again (a Q3 revenue miss had the stock
  down approx. 10% premarket Wednesday before closing +0.28%, already logged
  at edition 32) and a genuinely new case: an options-flow wire's intraday/
  snapshot-derived claim that Citigroup fell -4.05% Thursday did not match
  the confirmed stockanalysis.com close of -1.92%** — resolved the same way
  as always, by treating the stockanalysis.com (or equivalent timestamped)
  close as authoritative over any other figure and disclosing the correction
  explicitly in the briefing's own disclosure box. **New trap variant to
  name from edition 33: a secondary options-flow/derivatives wire can itself
  misstate the underlying stock's price move** (not just premarket/intraday
  feeds) — when options-flow commentary cites a stock's day's move, treat
  that figure as needing the same stockanalysis.com-close cross-check as any
  other mover claim, don't take the derivatives wire's framing numbers at
  face value just because the options data itself is the point of the
  citation.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. Edition 32 hit the same pattern again (spot down, Dec futures up).
  **Edition 33's gold reading converged instead — both spot and futures rose
  Thursday** (spot +0.10%, Dec futures +0.37%), closing out the brief
  spot-vs-futures divergence as a one-session phenomenon rather than a
  recurring issue; continue checking instrument/timestamp before calling a
  future gap anomalous. Similarly, **a price level can be correct while a
  vendor's stated %-change is wrong** if the vendor used a different
  prior-day base — always sanity-check that a stated price and stated %
  change reconcile arithmetically against the prior session's logged close.
  Edition 30 hit a live example on the 2-year Treasury (disclosed, not
  re-chased since). **The oil contract-month-roll trap, carried as "imminent,
  approx. 16-20 October" since edition 31, was found at edition 33 to have
  already happened** — the November Brent contract expired Wednesday 30 Sept
  at $103.50 and December became front-month from Thursday 1 Oct, confirmed
  via two independent sources (financefeeds.com and investing.com) despite
  one of those sources itself carrying a stale/mislabeled dateline (see the
  date-confusion entry above) — the underlying figures still checked out
  against a third source, so the correction was published with confidence.
  **Lesson: a "roll window" estimate derived from a generic roll-calendar
  reference (as edition 31's approx. 16-20 October figure was) is not the
  same as checking the actual exchange data, and should be treated as a
  rough guess to be verified, not a fact to carry forward uncorrected.**
  Edition 33 also surfaced a plausible **forward-looking pattern worth
  testing, not yet confirmed as a rule**: Brent's actively-quoted contract
  appears to roll at each calendar month boundary to the contract
  approximately two months forward (November was front-month through
  September, December from October) — if this holds, the next roll
  (December to January) would fall around 31 October/1 November. Treat this
  as a hypothesis to check against actual exchange data when that date
  approaches, not as a confirmed mechanical rule.
- **The DXY-vs-its-own-FX-crosses conflict — open since edition 29, resolved
  at edition 31, reopened at edition 32 — RESOLVED CLEANLY AGAIN at edition
  33 and did not persist a second session, closing the thread without
  needing the heavier ICE-futures verification escalation that was on
  standby.** Thursday's reading: both DXY snapshots (approx. 101.6 and
  approx. 102.1 — still disagreeing on magnitude, but that is a secondary,
  disclosed issue) agreed in direction with GBP/USD (-0.51%), EUR/USD (below
  1.1300) and USD/JPY (158.05-158.33), all consistent with a broadly stronger
  dollar on the day's hot ISM prices-paid print and elevated yields. Given
  this conflict has now resolved within one session twice (editions 31 and
  33) against reopening twice (29→30 persisting, then 32), treat a future
  recurrence as *likely to resolve within a session* by default, but still
  verify explicitly rather than assuming — do not treat this as fully closed
  forever, just de-escalate the default response to a same-edition check
  rather than an automatic "carry forward as open" flag.
- **The same-day silver sign conflict first flagged at edition 31 (Kitco/
  USAGOLD up vs. an Investrade wrap down) RESOLVED at edition 32 and stayed
  resolved at edition 33** — silver rose across all sources Thursday
  (Dec futures +1.01% to $61.18), reversing Wednesday's decline with no sign
  conflict. Treat as closed unless a fresh mismatch appears.
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
  entry, not leave a gap marker. **Edition 33 ran `check_refs.py` clean
  (38/38 matched) on the very first pass** — worth noting that drafting
  citations sequentially as you write, rather than renumbering afterward,
  continues to prevent this class of error entirely.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  Edition 29 caught one stray `~` in a late-added disclosure-box bullet;
  **editions 30 through 33 all rendered clean at zero tildes on the first
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
  CoT chart. **No new CoT report posted within editions 30 through 33's
  windows** (the Tue 22 Sept report logged at edition 29 is still the most
  recent as of edition 33's cutoff; the next is due approx. Fri 2 Oct,
  covering Tue 29 Sept — this now lands immediately after edition 33's own
  cutoff, so it should very likely be available for edition 34). The lesson
  stands for whenever a fresh CoT report does land: check that a *consistent*
  normalization (or at least a consistent unit) is available across every
  instrument in the chart before committing to it, and fall back to prose
  plus the standing sector-proxy default if you can't. **Fetch OI/
  gross-long-short for ES, NQ and RTY all three up front for edition 34's
  check — don't assume one contract's availability implies the others'.**
- **When an "optional" filler element (e.g. a levels table) would just
  restate the same instrument list already in a main table with one extra
  column, that's still legitimate as long as the extra column is genuinely
  additive** (editions 25 and 28 both added a prior-session-baseline-vs-close
  levels table to a short page 3) — don't reject the idea purely because the
  instrument list overlaps; check whether the *added* column carries real
  information first. **Editions 26, 27, 29, 30 and 31 did not need this
  padding at all** — page 3 filled cleanly from content alone every time.
  Edition 32's first render ran genuinely short on page 3 and was fixed with
  additive prose rather than a filler table. **Edition 33 hit the opposite
  failure mode for the first time in many editions: the briefing content
  (sections 1-6) overflowed to a FOURTH page on the first render, rather than
  running short.** The fix was the mirror image of the usual one: iteratively
  tightening prose (shortening sentences, cutting redundant clauses),
  merging table rows that shared an identical driver/note (e.g. two
  optical-sector movers with the same one-line cause, or two FX crosses both
  simply confirming "dollar strength"), and cutting one lower-value bullet/
  table row per pass (a minor single-stock mover with low incremental
  information, a sector-setup bullet merged into another) — re-rendering
  after each round to check progress, rather than guessing how much to cut
  in one shot. It took five successive trim-and-re-render rounds to go from
  5 pages to 4. **Lesson for next time content runs long: trim depth of
  individual driver/note sentences before cutting whole rows or bullets —
  the per-sentence trims preserved every data point and source while the
  row/bullet cuts were reserved for genuinely lower-value content (e.g. a
  "continued slide, no new catalyst" mover with no fresh information).**
- **The single-stock movers bar-chart outlier-capping rule** was tested again
  at edition 33: Accenture (ACN) +15.78% vs. the next-largest mover, Synopsys
  (SNPS) +12.78% — about 1.23x, comfortably in the uncapped range already
  confirmed at editions 27, 29 and 31 (spreads of about 1.14x-1.6x). The
  mechanism continues to work as designed; no need to revisit the threshold
  absent a genuinely new edge case (e.g. something in the 5-10x range).

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly, but has (at least) three observed failure modes: (a) a full
  clean sweep with genuinely fresh timestamps on every series, (b) the more
  common "thin-series-stale" pattern, (c) total failure, where every series
  is stale. **Editions 28 through 33 all got a full clean sweep** — six
  consecutive clean sweeps now, every series carrying a same-day
  `last_trade_time`, verified individually per series via a raw `curl`/direct
  fetch (not a tool-summarized fetch — see Hard rules above for why) each
  time. Still not a guarantee — keep checking `last_trade_time` on each
  series every time. Also note a `prev_day_close` field bug, observed eight of
  ten editions from 22-29: it duplicates the day's own `close`/
  `current_price` rather than giving a real prior-day reference, corrupting
  the feed's own `price_change`/`price_change_percent` fields too. **The bug
  has now stayed absent for four straight editions (30-33)** — encouraging,
  but continue to treat as intermittent, not resolved, and **always compute
  day-over-day % change manually against the previous edition's logged close
  regardless of whether the feed's own fields look correct this time** (the
  manual calculation and the feed's own field have now agreed for two
  straight editions, 32 and 33 — still not yet a pattern to rely on blindly).
  The VIX9D-vs-spot-VIX front-end inversion first flagged at edition 28
  (resolved as noise at edition 29) recurred at edition 30, widened at
  edition 31 (-1.68 to -1.83), widened again at edition 32 (-2.14), and
  **widened yet again at edition 33 to -2.39 — a fourth consecutive session of
  persistence/widening.** Per the standing guidance this reads as a settled
  feature of the current vol regime; continue reporting it as a standing
  regime feature, re-opening the thread only if it genuinely narrows or
  flips.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table
  and (absent fresher CoT data or another dominant story) chart #2. Worked
  cleanly again at editions 27 through 33 (seven straight); no second
  same-day sector-ETF source has ever been found, so this remains a standing
  single-sourced item, disclosed each edition. **Stockanalysis.com
  single-stock pages are also the standing default for pinning an exact
  closing price/% change on any individual mover** — editions 26 through 33
  all used direct fetches to it to resolve conflicting intraday-move
  percentages (edition 32: Liquidia's close of -57.19% used as authoritative;
  **edition 33: used to correct an options-flow wire's erroneous -4.05%
  Citigroup figure to the confirmed -1.92% close, and to confirm eight other
  movers — ACN, SNPS, FICO, COHR, DHR, MKC, NFLX, GOOGL — all matched the
  research pass's figures exactly on independent re-fetch**). Worth doing
  proactively for any mover whose research-pass figures disagree by more
  than a rounding error, and — per edition 33's new lesson above — for any
  stock-move figure quoted inside options-flow/derivatives commentary too,
  not just equities-desk commentary. Note that a headline wire's own GICS
  sector-index percentages can differ slightly from the SPDR ETF
  price-change figures (a normal index-vs-ETF-price methodology gap); keep
  using the SPDR ETF figures as the table's primary numbers.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. Not chased at
  editions 30 through 32; **at edition 33 a single lower-tier aggregator
  (vittarthi.com) offered a specific breadth ratio but was not corroborated
  by AP/Reuters/WSJ and was correctly left out of the briefing** — continue
  treating an uncorroborated single-aggregator breadth figure as not usable.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — now recurred at editions 22, 24-33
  (eleven straight, still worth a quick attempt each time in case it
  recovers). **zerogex.io is now confirmed across seven straight clean
  editions (27-33)**: edition 30 flipped sign entirely, edition 31 moved
  further negative (-$17.19bn), edition 32 moved back toward zero (-$14.33bn)
  as spot narrowed its gap to the flip point, and **edition 33 continued that
  move-toward-zero trend (-$11.58bn) as the spot-to-flip-point gap narrowed
  further to 32 points** — a plausible, well-explained progression each time,
  and edition 33's own SPX spot snapshot (7,667) cross-checked to within a
  point against the independently-sourced SPX close (7,666.45). Continue
  treating zerogex.io as the standing default source for dealer gamma, and
  continue the discipline of checking each new reading's plausibility against
  the day's actual index move and gamma-flip distance. **Minor open item
  carried forward, still low priority**: zerogex's own stated wall levels
  (call/put wall) have still not been cross-checked against a secondary
  options note's implied walls — only the net GEX sign/magnitude has been
  verified so far; revisit only if a wall-level figure becomes load-bearing
  for a specific call.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. The
  secondary-citation split narrowed at edition 31 to approx. 68-77%, moved
  sharply to approx. 35% at edition 32, and **at edition 33 held roughly
  flat-to-firmer at approx. 36-38% hike / approx. 62% hold even as Polymarket
  (a different venue) drifted further to approx. 25-26%** — see Standing
  Facts above for the live cross-venue-divergence watch item. Keep treating
  CME FedWatch as needing a disclosed range from secondary sources, not a
  single figure.
- **Kalshi direct fetch:** now rate-limited (HTTP 429, served a "Vercel
  Security Checkpoint" page) for **twelve straight editions (23-33)** — a
  confirmed structural gap, not transient. Keep attempting each edition (it
  may recover), but a one-line "failed again, Nth straight edition" is
  sufficient prose; use Kalshi's own secondary reporting (its blog,
  prediction-market news aggregators) as a workaround, as recent editions
  have done.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). **LME's own site (lme.com) has now failed
  twelve editions running (22-33)** — treat as durable; default straight to
  the fallback chain. Shanghai Metals Market (metal.com) has also now failed
  essentially every edition it's been tried (returns template/header content
  only, no price data) — go straight to Westmetall.com, which has now worked
  cleanly **twelve editions running** as the fallback. Disclose whichever was
  used. Because the fallback chain can change edition to edition, treat any
  day-over-day copper % change built across two different sourcing chains as
  approximate. **A standalone Investing.com Brent/WTI quote page also worked
  cleanly at edition 33** as a second independent confirmation of the
  Investrade-sourced Brent December-contract price — worth trying as a
  lightweight cross-check for oil specifically going forward, alongside the
  existing Investrade default.
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) worked
  cleanly again at edition 33 with no T+1 lag (2-year 4.78%, 10-year 5.24%,
  30-year 5.61%, all posted same-day). Prefer the CSV endpoint over the HTML
  TextView page — it has a known maturity-column mis-mapping bug the CSV does
  not share. **All three tenors eased slightly at edition 33's close even as
  all three set fresh multi-decade INTRADAY highs (10-year approx. 5.34%,
  highest since 2002; 30-year approx. 5.69%, highest since May 2002) on a hot
  ISM prices-paid print before retreating on haven demand** — a reminder to
  always check whether a "fresh high" headline refers to an intraday peak or
  the close, since they diverged materially this session.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. The most recent report remains the one
  published Fri 25 Sept, dated Tue 22 Sept: equity-index Asset Managers net
  long approx. 934,000-936,000 ES contracts vs. Leveraged Funds net short
  approx. 375,600-376,000; VIX futures non-commercial net short approx.
  79,300. **Confirmed again at edition 33 that no new report had posted as of
  Thursday's cutoff** (still the Tue 22 Sept data on file at cftc.gov). **The
  next report is due approx. Friday 2 October 2026 (covering Tuesday 29 Sept
  data) — this lands immediately after edition 33's own cutoff, so it should
  very likely already be posted by edition 34's research window. Check for it
  as the very first derivatives item next edition**, and fetch
  OI/gross-long-short for all three of ES, NQ and RTY up front this time, not
  just ES, if a CoT-based chart is wanted.
- **GBP/USD and EUR/USD clean close:** the underlying sourcing (Yahoo
  Finance/TradingEconomics/FXStreet as primary sources) remains fully
  resolved since edition 26, confirmed again through edition 33. This is
  distinct from the DXY-vs-FX-crosses directional-consistency check (see
  Hard Rules above), which has now resolved within-session twice (editions 31
  and 33) against reopening twice.
- **Gold/silver clean close on a non-event day:** the Kitco-vs-USAGOLD vendor
  gap itself has stayed quiet since normalizing at edition 31 (approx. $5).
  Edition 32's gold divergence (spot down vs. futures up) was a genuine
  different-instrument split, not a vendor disagreement, and **edition 33's
  gold reading converged — both spot and futures rose** — treat the
  spot-vs-futures split as a normal, occasionally-arising basis effect, not a
  sourcing problem, and keep matching timestamps/instruments before calling
  any future gap anomalous. Silver's sign conflict (live since edition 31)
  has now stayed resolved for two straight editions (32, 33).
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue — confirm on the BLS/Fed release schedule
  rather than assuming a date. **ISM Manufacturing (Sept 2026) released on
  schedule Thursday 1 Oct: 54.5%, a touch below the approx. 54.8-55.0%
  consensus, with Prices Paid jumping to 77.9 from 71.1 against an approx. 72
  estimate — this thread is now closed.** **September's jobs report (Fri 2
  Oct, consensus nonfarm payrolls approx. 84,000-90,000, unemployment approx.
  4.1%) is due immediately after edition 33's cutoff and was confirmed
  on-schedule (no shutdown delay) via bls.gov — this is the single biggest
  open data item for edition 34; verify the actual print, not consensus.**
  **ISM Services/Non-Manufacturing PMI for September is due Monday 5 October
  — August's reading was 55.4%; no September consensus figure had been
  published/located as of edition 33's cutoff, flag as a fresh search item
  next edition rather than assuming a number.**
- **Henry Hub natural gas: the October contract thread resolved at edition
  32** (final settlement $3.00/MMBtu). **November became front-month from
  Thursday 1 Oct, but edition 33 could only source a midday (approx.
  12:02pm ET) intraday quote (approx. $2.98/MMBtu, down approx. 4.8 cents on
  the session) — no confirmed end-of-day settlement was found.** Try the CME
  settlements page directly again next edition (it has timed out in the
  past) before falling back to another midday-only quote; if a clean EOD
  settlement still can't be sourced, keep flagging the midday-quote caveat
  explicitly rather than presenting it as a close.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29 (the page hosts several stacked
  category tables per URL — Sum of All Products, Index Options, Equity
  Options, Exchange-Traded Products, instrument-specific tables — each with
  its own totals). At edition 30 the page would not yield Monday's data at
  all (served stale cached data instead). At edition 32, a direct query with
  an explicit `dt=` date parameter returned `optionsData: null` for the
  target date — confirming the page genuinely had not posted yet rather than
  a fetch/parsing failure. **Not attempted at edition 33** (secondary
  priority; options-flow colour was sourced from a dedicated options-flow
  wire instead — see Hard Rules above for a new trap that surfaced there).
  Going forward: always state which specific category/table a Cboe
  options-volume figure comes from, and expect the page to sometimes simply
  not have same-day data available via a plain fetch/curl approach at all —
  don't over-invest time here if it stalls, this is a secondary-priority item
  per the derivatives section's own weighting.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable at editions 30
  through 33.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22) — either find a citable
  benchmark before reaching for that chart type, or stick to describing
  implied-vs-realized in prose without the third bar. Not attempted again
  through edition 33.
- **CFTC total open interest by instrument/date** (needed to normalize
  positioning "as % of open interest"): partially resolved at edition 29 —
  ES's total OI (approx. 1.9mn contracts) was obtained directly from
  cftc.gov, but NQ's and RTY's were not pulled. No new CoT report posted
  within editions 30 through 33's windows, so this was not re-attempted.
  **The next report (due approx. Fri 2 Oct, covering Tue 29 Sept, likely
  already posted by edition 34) is the one to try this on — fetch
  OI/gross-long-short for all three of ES, NQ and RTY explicitly up front
  rather than assuming one contract's availability implies the others'.**
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear** — editions 27
  through 29 confirmed several rating changes without being able to pin an
  exact dollar price target for all of them. Editions 30 through 32 all had
  cleaner runs. **Edition 33 was mixed**: Guggenheim's Danaher ($250) and
  Tempus AI ($92) targets were both confirmed via MarketBeat/Yahoo Finance,
  but Bernstein's Coherent Outperform initiation carried no confirmed dollar
  target, a cited Citi AMC price-target raise (to $2.20 from $1.80) came only
  from a single lower-tier aggregator, and cited HSBC/Wells Fargo Netflix
  actions lacked both a confirmed prior rating/target and firm Oct-1 dating.
  Report the rating direction and firm with confidence; treat a missing
  dollar target or unclear dating as a normal gap to flag, not something to
  chase hard, unless the name is the edition's dominant story.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29). Editions 30-32 each hit
  milder versions. **Edition 33 hit it again**: AMC's cited Citi price-target
  raise and the Netflix HSBC/Wells Fargo downgrade mentions were each
  single-aggregator-sourced with no independently confirmed price target or
  precise dating — both flagged to Annex A rather than reported as fact.
  This remains the right call when time-constrained: a single aggregator's
  claim, especially for a smaller or less-covered name or a secondary
  analyst action, is not enough on its own — corroborate with a second source
  or flag it as unverified in Annex A.

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
  first try. **Edition 33 hit genuine copy overflow for the first time in
  several editions** (5 pages on the first render, correct single pagebreak
  confirmed present via `grep -n pagebreak` before touching anything else) —
  it took five rounds of trim-and-re-render (tightening prose sentence by
  sentence, merging near-duplicate table rows, cutting one lower-value bullet
  and one lower-value mover row) to reach 4 pages; see the Hard Rules entry
  above for the specific technique. **Always re-render and re-check the page
  count after each trim round rather than guessing how much is enough** — at
  edition 33 the first two trim rounds each looked substantial in the diff
  but moved the overflow by only a fraction of a page each time.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Editions 25 and 28 both hit a visibly short page 3 on the first render
  despite passing the 4-page check, fixed with an optional levels table.
  Edition 32 hit a visibly short page 3, fixed with additive prose instead of
  a new table. **Edition 33 hit the opposite problem (overflow, not
  shortfall) and only caught it by rendering and reading the page images —
  the page count alone (5) was the first signal, but reading the actual pages
  was what showed exactly which section/table/bullet was spilling onto the
  stray page each round, which is what made the targeted trims possible
  rather than cutting blindly.** This is now the second distinct failure
  mode this report has needed a fix pattern for (short page 3 vs. overflow
  past page 3) — diagnose which one you have before choosing a fix: check
  whether page 3 (or earlier) looks empty/short (→ add real content) or
  whether content is spilling onto an unwanted page 4/5 (→ trim prose depth
  first, then merge/cut lowest-value rows or bullets).

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
  29-31, or 33). Edition 32 needed page-3 padding via additive prose instead
  (Section 4's table was already full-length). **Edition 33 needed the
  opposite: active trimming, not padding** — see Hard Rules and Production
  Notes above. Always re-render immediately after adding (or removing) any
  content to confirm the page count, rather than assuming a change is safe —
  edition 28's first attempt at 12 levels-table rows overshot to 5 pages (10
  rows fixed it); edition 33 needed five successive trim rounds, each
  re-rendered, before confirming 4 pages. Conversely, **if page 3 overflows
  by a handful of lines**, the cheapest trims are: shortening day-ahead table
  cell text, cutting or merging "sector setup" bullets, tightening prose
  sentences in Sections 1-5 (especially closing-paragraph recaps that restate
  figures already shown in a table above), merging two single-stock-mover or
  FX-cross table rows that share an identical driver/note into one row, and
  trimming rows from the optional levels table if one was added.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at edition 26 (about 4.7x), edition 27 (about 1.14x), edition 28 (about
  2.4x), edition 29 (about 1.6x), edition 31 (about 1.2x), edition 32 (about
  4.56x), and **edition 33 (Accenture +15.78% vs. next-largest Synopsys
  +12.78%, about 1.23x, left uncapped)**. Edition 30 produced the one genuine
  10x+ case to date and confirmed the rule works as designed (about 15x,
  capped at a fixed axis max of 30 with a "(capped)" annotation). The
  mechanism has now been confirmed working at both extremes (uncapped under
  approx. 5x, capped at approx. 15x) across eight editions; no need to
  revisit the threshold or mechanism absent a genuinely new edge case (e.g.
  something in the 5-10x range).

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — **used for a ninth consecutive
edition at edition 33**, for a sector-rotation story where Energy and
Technology led (oil rally plus an AI-infrastructure/software earnings
cluster) while rate-sensitive and healthcare-adjacent sectors lagged despite
a cooler-than-expected ISM headline, because the Prices Paid sub-index and a
European gilt selloff pushed long-end yields to fresh intraday multi-decade
highs regardless; edition 32 used it for a Technology-only-green session;
edition 31 for a near-total reversal of the prior day's leadership; edition
30 for a broad risk-off session; edition 29 for a Friday relief-rally
rotation; edition 28 for a Meta-Muse-driven rotation; edition 27 for a
rate-spike-driven rotation into defensives; edition 26 for a financials-vs-
materials reversal; edition 25 for a chip-led rally — this remains a
reliable, low-risk default and has now covered a genuinely wide range of
underlying stories without needing to be replaced). Fresh CFTC CoT data on a
Monday/weekend-window edition → the ES/NQ/RTY asset-manager-vs-leveraged-
funds positioning chart, **normalized as % of open interest if that figure
can be sourced for all instruments being charted; if not, a category's own
net-position-as-%-of-its-own-gross-long+short is an acceptable,
honestly-labelled substitute — but check that a *consistent* normalization
(or at least a consistent unit) is available across every instrument in the
chart before committing to it.** No fresh CoT data posted within editions 30
through 33's windows, so this scenario did not arise; **the next report (due
approx. Fri 2 Oct, very likely already posted by edition 34) is the one to
watch for.** A single dominant earnings print with a clean, well-sourced
implied-vs-realized-move story → a three-bar implied/historical-average/
realized move chart (the historical-average leg has never actually been
sourced successfully — see Known-hard-to-source above; Micron's clean beat
at edition 32 and its modest follow-through at edition 33 were both
considered but neither carried a dedicated-chart-worthy implied-move story).
A genuine multi-sector broadening/deepening selloff across consecutive
sessions → the sector-ETF proxy rendered as a grouped (day-over-day) bar
instead of single-day. A holiday-window preview edition with no fresher data
→ VIX futures term structure with event annotations. When chart #1 (movers)
already covers the earnings/single-name story, the sector proxy is a good
complementary choice even on a stock-heavy day — editions 25 through 33 have
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

**Editions 1–31 (condensed):** established the format (edition 1 baseline;
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
DXY-vs-FX-crosses conflict recurred for a second session (later resolved at
edition 31, reopened again at edition 32, resolved again at edition 33); VIX
16.07 (+8.07%); zerogex.io's SPX gamma flipped to -$9.33bn.

**Edition 32 (condensed)** — Thursday 1 October 2026 report covering
Wednesday 30 September 2026, the window's one NYSE session. A volatile
round-trip session: S&P 500 traded up as much as 0.7% intraday on a
cooler-than-feared August PCE print before fading into a late-day reversal
with no single cited catalyst, closing -0.25% at 7,651.54; Dow -0.86% to
50,906.05 (Northrop Grumman's defense-contract loss weighed); Nasdaq +0.24%
to 26,861.06 (chip rally); Russell 2000 -0.39% to 2,796.86. Technology
(XLK +0.64%) was the only green sector (Intel +3.71%, HPE +3.90% on an AMD
"Helios" AI-rack order). Liquidia Corp (LQDA) -57.19% (patent loss to United
Therapeutics, which rose +12.55%, left uncapped at approx. 4.56x); Rogers
Corp +10.73%; FICO -4.11% (fresh BofA downgrade on top of Tuesday's -26.52%
FHFA-driven crash); Northrop Grumman -4.19% (lost the F/A-XX fighter
contract to Boeing); Moderna -5.35% (Citigroup downgrade to Sell); Concentrix
+0.28% at the close despite an approx. -10% premarket reaction to a Q3
revenue miss. Micron reported after the close: a clean beat (EPS $33.42 vs.
$31.16 est., revenue $54.23bn vs. $50.45bn est.) but only a modest -0.78%
AH reaction. August PCE (released 8:30am ET Wednesday): headline +0.3%
m/m/+3.4% y/y, core +0.2% m/m/+3.0% y/y — a clear cooling print that,
combined with NY Fed Williams' dovish Tuesday-evening remarks, roughly
halved October-hike odds within the session (Polymarket to approx.
36.5-43.5%, Kalshi secondary to approx. 36-37%, CME secondary to approx.
35%) — the largest, most unified one-session repricing this report had
logged to that point. Oil rallied (Brent +0.91% to $103.53, WTI +1.16% to
$90.42) on Trump denying willingness to ease Iran sanctions; an oil-roll
check found no roll yet (later found at edition 33 to have actually already
happened). Henry Hub's October contract expired at a clean $3.00/MMBtu final
settlement. Gold diverged by instrument (spot down 0.60%, Dec COMEX futures
up 0.17% — a genuine spot/futures split, resolved/converged at edition 33);
silver's sign conflict from edition 31 fully resolved (down across sources).
Copper +0.09% via Westmetall. The DXY-vs-FX-crosses conflict reopened
(resolved cleanly again at edition 33). Treasury 2-year eased to 4.88%,
10-year to a fresh approx. 5.29% (24-year high), 30-year to approx. 5.65%
(highest since May 2002). VIX 16.34 (+1.87%, a fifth consecutive CBOE clean
sweep); VIX9D's inversion widened to -2.14 (a third consecutive session);
zerogex.io's SPX gamma moved back toward zero (-$14.33bn). 40 sources, zero
mismatches, clean 4-page render after fixing a short page 3 with additive
prose.

**Edition 33 (most recent — full detail)** — Friday 2 October 2026 report
covering Thursday 1 October 2026, the window's one NYSE session, research
window Wed 30 Sept 2026 20:00 ET through Thu 1 Oct 2026 20:20 ET. Verified
the two structural header rules again (date line = edition date, window line
states the given research-window start with the session covered noted
parenthetically) — now clean across five consecutive single-session
editions (29-33).

A volatile round-trip session with yields, not equities, in the driver's
seat: a hotter-than-expected September ISM Manufacturing Prices Paid print
(77.9, up from 71.1, vs. an approx. 72 estimate) landed alongside a sharp
European/UK gilt selloff, spiking the 10-year Treasury intraday to approx.
5.34% (highest since 2002) and the 30-year to approx. 5.69% (highest since
May 2002); both eased into the close (10-year to 5.24%, -5bp; 30-year to
5.61%, -3bp; 2-year to 4.78%, -10bp) as US haven demand picked up. Equities
opened on the back foot but recovered as yields retreated: S&P 500 +0.19% to
7,666.45 (snapping a three-day losing streak), Dow +0.04% to 50,926.56,
Nasdaq Composite +0.04% to 26,871.60, Russell 2000 +0.35% to 2,806.63 — all
four cross-checked cleanly against AP/CNBC/TheStreet, with the Russell
figure also confirmed by direction via IWM (+0.41%) after a WebSearch
AI-summary artifact wrongly claimed a -5.4% move that matched no other
evidence and was discarded. ISM Manufacturing's headline missed (54.5% vs.
approx. 54.8-55.0% consensus) but the Prices Paid inflation signal is what
actually drove the session. Sector leadership: Energy (XLE +1.95%) led on
the oil rally (continued Iran/Hormuz tension), Technology (XLK +1.05%) on an
AI-infrastructure/software earnings cluster, Industrials (+0.99%), Utilities
(+0.61%) and Financials (+0.11%) also green; Health Care (XLV -1.32%) lagged
on single-name news (Danaher, Tempus AI, Moderna), with Communication
Services, Real Estate, Consumer Staples and Materials also red.

Single-name stories: Accenture +15.78% (fiscal Q4 beat, guidance raised
above range) and Synopsys +12.78% (Investor Day: OpenAI partnership, >$1bn
AWS silicon-IP/EDA deal, raised FY27 guide, new buyback) led a broader
enterprise-software/AI-capex rally; an AI-datacenter-optics theme lifted
Coherent +10.90% ("PhotonLink" launch, Bernstein Outperform init, possible US
curbs on Chinese transceivers), Lumentum +7.67% and Applied Optoelectronics
+8.12%. FICO +11.69% at the close (FHFA approved its Direct License
mortgage-scoring program, a rebound off Wednesday's crash) but gave back
more than half the gain after hours to -6.35%, a genuinely two-sided,
still-unresolved story. Nike missed fiscal Q1 revenue and guided FY27 sales
to a high-single-digit percentage decline, falling a further approx. 8.7%
after hours on top of a -0.71% regular-session dip — the dominant
day-ahead-setup story for Friday. McCormick beat on both lines but fell
-4.87% on dividend-safety concerns; Danaher fell -4.42% on a CEO transition
despite a Guggenheim PT raise to $250; Tempus AI fell -6.59% on profit-taking
despite a Guggenheim PT raise to $92; AMC fell -8.00% on a debt
refinancing (notes + term loan); Netflix fell -2.49% on a decelerating
growth guide; Alphabet fell -1.70% on an adverse SDNY ad-tech jury-trial
ruling (Judge P. Kevin Castel, approx. $3.2bn at issue); an options-flow
wire's claimed -4.05% Citigroup move was corrected to the confirmed
stockanalysis.com close of -1.92% (heavy put skew was the real story there).
Boeing +3.35% and Micron +3.03% continued catching up on, respectively, the
F/A-XX contract win and Wednesday's earnings beat; Northrop Grumman was
roughly flat, stabilizing after Wednesday's contract-loss drop.

Macro: Kevin Warsh re-confirmed as Fed Chair, funds rate 3.75-4.00%, next
FOMC Oct 27-28 — all unchanged. October-hike odds split sharply across
venues for the first time since Wednesday's unified collapse: Polymarket
drifted further dovish to approx. 25-26% while Kalshi/CME secondary
citations held near 36-38% — see Standing Facts for the live watch item. BoE
(3.75%, next decision 5 Nov) and BoJ (next meeting Oct 29-30, rate level not
re-checked this edition) both re-confirmed. US-China tariff framework
unchanged. A checked-and-refuted government-shutdown premise closed cleanly:
a continuing resolution funds the government through 11 Dec 2026, confirmed
against whitehouse.gov/congress.gov/GovTrack, and Friday's jobs report
stayed on its normal BLS schedule. A Meta Cambridge Analytica penalty
hearing was held (Judge Francis Mathew); no ruling issued, expected within
weeks.

Commodities/FX: WTI +2.71% to $92.87 (clean reconciliation). Brent's
long-flagged contract roll turned out to have already happened — the
November contract expired Wednesday at $103.50 and December became
front-month Thursday, closing at $102.31 (+4.37% vs. December's own
Wednesday base of $98.03), correcting the prior edition's premature approx.
16-20 October estimate; a plausible (unconfirmed) forward pattern was noted
for a December-to-January roll around 31 Oct/1 Nov. Henry Hub's new
front-month November contract could only be sourced as a midday quote
(approx. $2.98/MMBtu), not a confirmed settlement. Gold's Wednesday
spot-vs-futures split converged (both up Thursday: spot +0.10%, Dec futures
+0.37%). Silver rose across all sources (+1.01% Dec futures), reversing
Wednesday's decline. Copper -1.02% via Westmetall. The DXY-vs-FX-crosses
conflict, reopened at edition 32, resolved cleanly again (dollar broadly
stronger across all crosses) without needing the heavier ICE-futures
verification pass that was on standby.

Derivatives: the CBOE feed gave a sixth consecutive full clean sweep (VIX
16.39, +0.31%); VIX9D's inversion widened for a fourth consecutive session
to -2.39; VVIX jumped +2.83%. Options flow showed heavy Citigroup put skew
despite its modest -1.92% close, and heavy Medtronic put buying attributed
to a put-spread structure. zerogex.io's SPX net dealer gamma continued
moving toward zero (-$11.58bn from -$14.33bn) as the spot-to-flip-point gap
narrowed to 32 points. CFTC CoT confirmed still unchanged since the Tue 22
Sept report; the next report (due approx. Fri 2 Oct, covering Tue 29 Sept)
lands immediately after this edition's cutoff and should be checked first
thing next edition. 38 sources, zero mismatches on the first `check_refs.py`
run, zero stray tildes on the first check. The document overflowed to 5
pages on the first render (genuine copy overflow, not a stray pagebreak) —
the first time in several editions content ran long rather than short — and
needed five rounds of trim-and-re-render (tightening prose, merging
near-duplicate table rows, cutting one lower-value mover and one sector-setup
bullet) to reach a clean 4-page render.

**Open threads for edition 34:** September's jobs report (Fri 2 Oct,
consensus nonfarm payrolls approx. 84,000-90,000, unemployment approx. 4.1%)
is due immediately after this edition's cutoff and is the single biggest
data item outstanding — verify the actual print, not consensus, and check
whether it moves the now-divergent cross-venue October-hike odds (Polymarket
approx. 25-26% vs. Kalshi/CME approx. 36-38%) back together or further
apart. The CFTC CoT report (due approx. Fri 2 Oct, covering Tue 29 Sept)
should also be checked first thing — fetch OI/gross-long-short for ES, NQ
and RTY all three up front if a positioning chart is wanted. ISM
Services/Non-Manufacturing PMI is due Monday 5 Oct (August was 55.4%, no
September consensus located yet). FICO's regular-session gain was more than
half erased after hours — genuinely two-sided, keep watching Equifax and
TransUnion for read-across on the mortgage-scoring-monopoly thread. Nike's
after-hours guidance cut is the dominant Friday-open setup story in
consumer discretionary/footwear-apparel. The AI-infrastructure/optics trade
(Coherent, Lumentum, Applied Optoelectronics, plus Accenture/Synopsys) was
Thursday's one clean risk-on pocket — watch whether it extends. Watch for
the Meta Cambridge Analytica ruling (Judge Mathew, expected "within weeks").
BoJ's current policy rate level (carried at approx. 1.25%) should be
re-verified directly next edition, since edition 33 only re-checked the
meeting date. The unconfirmed AMC Citi price-target raise and Netflix
HSBC/Wells Fargo downgrade mentions remain single-aggregator-sourced if they
resurface. A plausible-but-unconfirmed Brent roll pattern (front-month
rolling at each calendar-month boundary to the contract approx. two months
forward) is worth testing against actual data when the next roll
(December-to-January, hypothesized around 31 Oct/1 Nov) approaches. Threads
closed after resolution rather than carried further: ISM Manufacturing
(actual print replaces consensus); the government-shutdown premise (checked
and refuted); the Brent Nov-to-Dec roll (confirmed already done); the gold
spot-vs-futures split (converged); the DXY-vs-FX-crosses conflict (resolved
cleanly, without a second consecutive reopening); the Citigroup options-wire
stock-move discrepancy (corrected to the stockanalysis.com close).
