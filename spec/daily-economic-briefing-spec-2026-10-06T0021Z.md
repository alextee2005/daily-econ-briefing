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
  is where the sessions covered belong, not the date line. **Editions 33, 34
  and 35 have all applied this correctly** ("Friday 2 October 2026," "Monday 5
  October 2026" and "Tuesday 6 October 2026" respectively as the date line,
  with the window line carrying the session(s) covered).
- **The window line must start at the given research-window start, not
  earlier.** Edition 23 was given a window starting 2026-09-16 20:00 ET and
  printed "Tue 15 Sept close/AH," which claimed a session the previous edition
  already covered. Edition 29 phrased this as "Window: Thu 24 Sept 20:00 ET –
  Sun 27 Sept 20:22 ET (Fri 25 Sept close/AH + weekend)" — stating the given
  window bounds first and the actual session covered in parenthetical, which
  reads cleanly and avoids both traps. Editions 30, 32-35 reused the same
  pattern for single-session windows, and edition 34 reused it for a
  single-session-plus-weekend window too — now confirmed clean across seven
  consecutive single-session or single-session-plus-weekend editions (29
  through 35). No further confirmation needed; treat this as settled.

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
- **Next FOMC meeting: October 27–28, 2026**, re-confirmed again at edition 35
  directly against federalreserve.gov's own FOMC calendar page
  (federalreserve.gov/newsevents/2026-october.htm). The meeting is now about
  three weeks out — continue re-confirming every edition between now and then.
  **FOMC minutes from the 15-16 Sept meeting are due Wednesday 7 October 2026,
  2:00pm ET** — this will land after edition 35's cutoff; whichever edition's
  window next spans that time should read them for hints of October-hike
  dissent/debate.
- **October-hike odds held roughly steady at edition 35, little changed from
  edition 34's sharp post-jobs-report convergence — re-verify fresh every
  edition regardless:** Polymarket approx. 16.5-20%, Kalshi approx. 16-23%,
  secondary CME FedWatch citations approx. 21% (the official FedWatch page
  remains unreachable by direct fetch). This is now the second straight
  edition at a tight, stable band after the September jobs-report-driven
  collapse from Thursday 1 Oct's 25-38% split — do not assume permanence, but
  the regime looks more settled than the volatile late-September period.
  **December-hike odds, first surfaced as an unconfirmed secondary range at
  edition 34 (approx. 65% Kalshi to 75%+ CME FedWatch), firmed somewhat at
  edition 35 to approx. 65-75%** (Kalshi approx. 65-70%, Polymarket approx.
  73.5-75%); a CME-attributed figure as high as 90-100% also circulated at
  edition 35 but reads as implausible and was discarded. Still unconfirmed
  against any primary venue — keep attempting a firmer check when it's
  load-bearing.
- General principle: do not assume any routine macro-calendar fact (Fed
  personnel, meeting dates, symposium schedules, other central banks' policy
  rates) from memory or from the prompt's own framing — verify it fresh from a
  primary source (federalreserve.gov, bankofengland.co.uk, boj.or.jp,
  kansascityfed.org, norges-bank.no, riksbank.se, banxico.org.mx, snb.ch,
  rba.gov.au, etc.) every edition, exactly like any other data point. Edition
  34 reconfirmed Kevin Warsh as Fed Chair directly against federalreserve.gov's
  Board of Governors bios page; **edition 35 re-confirmed the same page again
  — still Kevin Warsh, unchanged.** **Open gap from edition 35, worth closing
  next edition: the BoE and BoJ facts below, and the shutdown/CR status, were
  each re-confirmed via secondary citations only this round (direct fetches to
  bankofengland.co.uk, boj.or.jp, whitehouse.gov and congress.gov were not
  repeated) — re-verify each directly against its primary source next edition
  rather than letting secondary-only confirmation become the new default.**
- **Bank of England: held at 3.75% on Thursday 17 Sept 2026, a 6-3 vote**
  (same three dissenters as 30 July, all favoring a hike to 4.00%) — resolved,
  does not need re-confirming again unless a new decision date has passed.
  **Next BoE decision: Thursday 5 November 2026** — re-confirmed again at
  edition 35, but via secondary citations (cambridgecurrencies.com,
  financecalendar.com) rather than a direct bankofengland.co.uk fetch; a
  circulating "88% hike probability" figure for that meeting could not be
  corroborated against a primary venue and was discarded as unreliable. Do a
  direct primary-source fetch next edition or two as the date approaches.
- **Bank of Japan: hiked 25bp to approx. 1.25% on 18 September 2026**
  (effective 24 Sept), a 31-year high, on a 7-2 split vote against a
  unanimous 52/52-analyst consensus. **The Bank of Japan's next policy
  meeting is confirmed for October 29-30, 2026** — re-confirmed again at
  edition 35, but again via secondary citations rather than a direct boj.or.jp
  fetch (rate level treated as high-confidence given multiple consistent
  sources, meeting-odds color flagged as secondary-sourced only). Do a direct
  primary-source re-fetch next edition or two as the meeting approaches.
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
  edition 35, do not re-derive:** headline 54.9% (down from August's 55.4%,
  against an approx. 55.0% secondary-aggregator consensus — no firm
  economist-poll consensus was located, same gap as last edition). Sub-indices:
  Business Activity 56.5% (-5.2pt), New Orders 59.8% (-1.1pt), Employment 50.1%
  (+2.3pt, back into expansion), Supplier Deliveries 53.2% (+1.9pt), and
  **Prices Paid 74.0% (+1.4pt), the highest since July 2022** — the sixth month
  in seven above 70%, per ISM Chair Steve Miller. Confirmed directly against
  ISM's own press release (PR Newswire). The hot Prices Paid sub-index, not the
  soft headline, drove the session's rates reaction — see edition 35's log
  entry below.
- **The US-China "30-for-30" tariff framework remains at the list-
  identification stage, unchanged since edition 30's primary-source
  confirmation** (re-checked fresh again at edition 35, no new implementation
  news found): USTR.gov and whitehouse.gov confirm a framework recommending
  reduced tariff treatment for $30bn of goods on each side (77 Chinese
  products, 1,600+ US products — edition 32 separately logged updated list
  sizes of 77/1,619 post-Trump-Xi-summit), administered via the new US-China
  Board of Trade. Still pending each side's domestic legal processes — watch
  for a formal implementation/effective date in a future edition.
- **No US federal government shutdown is in effect — re-confirmed again at
  edition 35 (via secondary wires, leadingage.org and govexec.com, rather than
  a direct whitehouse.gov/congress.gov fetch this round):** a continuing
  resolution (H.R. 6500 / P.L. 119-103), signed into law 2 September 2026,
  funds the government through **11 December 2026**. Re-confirm directly
  against whitehouse.gov/congress.gov next edition rather than letting
  secondary-only confirmation repeat. Watch for shutdown risk resurfacing as
  11 December 2026 approaches, and note that whitehouse.gov also hosts a
  separate generic "Government Shutdown Clock" page whose content has
  previously described an active-shutdown narrative inconsistent with the
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
  more consecutive citations. A related trap surfaced at edition 28's own
  draft, worth naming explicitly: placeholder ref text (e.g. `[note1]`) typed
  during drafting and never swapped for a real number. `check_refs.py`'s
  regex requires `\d+` inside the brackets, so a non-numeric placeholder like
  `[note1]` simply won't match either the inline or Annex-B regex — it won't
  show up as "missing" or "unused," it just silently doesn't count. A near
  miss of the same species at edition 30's own draft: a citation typed as
  `[9b]`** (meant to disambiguate a second source keyed to item "9") also
  fails the `\d+` regex for the same reason as `[note1]` — caught before
  rendering by re-running `check_refs.py` and seeing the citation count come
  up short, fixed by assigning it a fresh plain integer instead. **Never use
  a letter suffix to disambiguate a citation — always mint a new integer.**
  Edition 29 hit a related but distinct trap worth naming too: reserving
  Annex B numbers (e.g. `[32] (reserved)`) for sources planned but not used
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
  same source/method. **Edition 35 did the same again** (`[3]` for every
  stockanalysis.com single-stock close, `[30]` for every Investing.com
  historical-data pull across gold/silver/DXY/FX) and ran clean, 34/34, on
  the second pass after catching one unused Annex B placeholder before
  rendering (see below) — this pattern is now confirmed stable across three
  editions.
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
  since that's where the content actually belongs, and edition 34 did the
  same for its own CFTC-positioning chart #2. **Edition 35 reverted to the
  sector-ETF-proxy default (no fresh CoT data was due that edition) and kept
  it in its default Section 2 placement**, under the Equities heading — the
  asset/skill template's `chart2_panel` position is just a default for the
  common case (sector rotation), not a hard rule; use Section 5 placement
  again whenever a future CFTC-positioning chart #2 recurs.
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
  **Editions 27 through 35 are all clean counter-examples worth keeping in
  mind**: all nine posted a usable AP wire in time (edition 35's AP wire,
  syndicated via WTOP/KTVB/KRMG, gave S&P 500 7,773.95/+0.66%, cross-checked
  independently against a search-derived 7,773.99/+0.66% with no material
  conflict). Treat AP/Reuters as "try first, expect to sometimes need the
  fallback chain," not as unreliable by default. Always have Yahoo Finance +
  FRED/stockanalysis.com ready as the working fallback regardless of which
  way this edition goes. Edition 33's lesson stands: a WebSearch tool's own
  AI-generated summary can itself be a bad, uncorroborated source — verify
  via a direct instrument fetch (e.g. an ETF proxy) when a single
  search-summary claim conflicts with everything else.
- Watch for date confusion: aggregators routinely republish the prior
  session's data under the current date. Verify the session date on every
  figure. Edition 25 caught a live example (Trefis "Market Movers" re-serving
  Friday 18 Sept's figures under a Monday 21 Sept URL); edition 26 caught
  another; edition 27 caught a third; edition 28 caught a fourth and fifth in
  the same run; edition 32 caught a sixth and seventh (Rio Times republishing
  Tuesday's oil AND gold/silver wraps under a Wednesday dateline); edition 33
  caught an eighth and ninth (two more Rio Times mis-dates); edition 34 caught
  a tenth, eleventh and twelfth across Trefis, FXStreet and a live Kitco page.
  **Edition 35 caught a thirteenth, a distinct and clean example on analyst
  commentary rather than price data**: a wave of Nike price-target cuts
  (Goldman Sachs, Citigroup, JPMorgan, Jefferies and others) widely circulated
  as if they were Monday 5 Oct news were traced back to original publish
  dates of Friday 2 Oct or Saturday 3 Oct — a Yahoo Finance article itself
  timestamped Monday had republished Goldman's cut while citing NKE's stale
  Friday closing price ($33.87) rather than Monday's actual level. This is the
  first time the trap has hit analyst-note aggregation specifically rather
  than a price/level figure — worth remembering that stale-date republishing
  applies to qualitative "news" content too, not just prices. Rio Times has
  mis-dated content in at least four separate editions (32 twice, 33 twice);
  treat any Rio Times article with extra suspicion. Always check a dated
  article's own body text against the logged prior-session figures before
  trusting its date stamp, regardless of which outlet it is. A same-day close
  and a next-day after-hours-triggered move can legitimately combine into one
  large single-day % change — edition 24's Xenon Pharmaceuticals -30.7%
  Friday move is the reference example. Check whether a headline % move is
  measured close-to-close before assuming two reports conflict. The
  intraday-vs-close divergence trap (distinct from stale-dating) is still
  very much alive**: Worthington Enterprises (ed. 26), Paychex/Cracker Barrel
  (ed. 27), Oracle (ed. 28), Akamai and the STX/WDC/SNDK storage cluster (both
  ed. 29), MongoDB (ed. 30), Liquidia and Concentrix (both ed. 32), Concentrix
  again and a Citigroup options-wire mismatch (both ed. 33), Nike (ed. 34),
  and **at edition 35, SpaceX-exposure vehicle SPCX**: several outlets
  reported a mid/early-session move in the 5-6% range, but the
  stockanalysis.com-timestamped close was +7.63% — the lower intraday figures
  were from earlier in the session, not the final print. Resolved the same
  way as always: treat the stockanalysis.com (or equivalent timestamped)
  close as authoritative, and disclose explicitly when an earlier-session
  figure doesn't match the close.
- **A new, distinct trap logged for the first time at edition 35: a
  corporate-action (stock-split) data artifact mistaken for a genuine price
  move.** A premarket-gainers aggregator showed Paramount Skydance (PSKY)
  "+96%" Monday morning. This was not a real market move — PSKY executed a
  scheduled 2-for-1 stock split effective ahead of Monday's open (plus a
  Nasdaq-to-NYSE listing transfer and a warrant-distribution record date the
  same day), and a stale/unadjusted pre-split quote feeding into a
  post-split price produced a spurious approx. 100% "gain." This is distinct
  from both the stale-date-republishing trap (the date was correct; the
  adjustment basis was wrong) and the intraday-vs-close trap. Before
  reporting any single-stock move that looks like an outright magnitude error
  (roughly doubling, halving, or near-100%), check whether the company had a
  stock split, reverse split, or similar corporate action effective that
  session — and exclude the figure rather than reporting it if a stale
  unadjusted-quote explanation fits.
- Run a dedicated verification pass on any figure two research passes
  disagree on before publishing — cheap, and has caught real errors before.
  A same-day price split isn't always an error, though: edition 22's
  "gold conflict" turned out to be COMEX futures (settle 1:30pm ET) vs.
  continuously-traded spot — a genuine, explainable divergence, not a data
  error. Edition 32 hit the same pattern again (spot down, Dec futures up).
  Editions 33 and 34 converged cleanly (both spot and futures moved the same
  direction for both metals). **Edition 35 saw a mild version of the old
  pattern return**: gold spot ($4,137.70, -0.05%, Kitco) and gold futures
  ($4,161.30, -0.23%, Investing.com) both fell, directionally consistent, but
  a third source (Investrade, $4,156.80, -0.13%) sat between them, an
  unreconciled three-way split still explainable by instrument/timing
  differences rather than a vendor error — continue checking
  instrument/timestamp before calling a future gap anomalous. Similarly, **a
  price level can be correct while a vendor's stated %-change is wrong** if
  the vendor used a different prior-day base — always sanity-check that a
  stated price and stated % change reconcile arithmetically against the prior
  session's logged close. **Edition 35 hit exactly this pattern on oil**: a
  second aggregator's WTI figure ($89.22, -1.78%) did not arithmetically
  reconcile against its own implied prior-day base, while Investrade's figure
  ($89.43, -1.84%) reconciled cleanly against Friday's logged $91.11 close —
  Investrade's internally-consistent figure was used, the conflict disclosed
  in Annex A. Edition 34 surfaced a cleaner, more general version of this bug
  class in the CBOE vol-complex feed itself: the feed's own
  `price_change_percent` field was found to divide `price_change` by the
  *current* price rather than the *prior* close. **Edition 35's direct CBOE
  fetch showed neither of the feed's two previously-documented bugs (the
  duplicate-`prev_day_close` bug and the current-price-denominator bug) —
  the manually-recomputed VIX %-change matched the feed's own stated
  percentage exactly across all six series, confirming these bugs are
  intermittent, not constant.** Always compute day-over-day % change manually
  as `price_change ÷ (current_price − price_change)` and treat the feed's own
  `price_change_percent` field as unreliable until this is checked each time
  regardless of which pattern (or neither) shows up that day. The oil
  contract-month-roll trap (Brent Nov-to-Dec) was confirmed already resolved
  at edition 33; edition 34 confirmed no new roll had happened yet, and
  **edition 35 confirmed again via oilprice.com's futures curve that December
  remains Brent's front-month, with January trading as the next contract out
  — still no roll**, consistent with the still-unconfirmed hypothesized
  Dec-to-Jan roll around 31 Oct/1 Nov.
- **The DXY-vs-its-own-FX-crosses conflict — open since edition 29, resolved
  at edition 31, reopened at edition 32, resolved cleanly again at edition
  33, recurred again at edition 34 (resolved within the session), and
  resolved cleanly with no conflict at all at edition 35** — Monday's DXY gain
  (approx. 102.17-102.27, +0.26% to +0.33%) was fully consistent in direction
  with all three major crosses (EUR/USD -0.43% to -0.46%, GBP/USD -0.13% to
  -0.19%, USD/JPY +0.21% to +0.25%), a cleaner read than several recent
  editions' recurring mismatch, though the cross-vendor magnitude gap on DXY
  itself persisted. This conflict has now resolved within one session on
  every occurrence except the 29→30 persistence — treat a future recurrence
  as *likely to resolve within a session* by default, but still verify
  explicitly each time rather than assuming; do not treat this as fully
  closed forever.
- **The same-day silver sign conflict first flagged at edition 31 resolved at
  edition 32 and has now stayed resolved for four straight editions (32-35)**
  — silver rose across all sources Monday (spot approx. +1.04%, futures
  approx. +0.44%, a third aggregator approx. +1.46%), consistent in direction
  across instruments, with only a separate uncorroborated outlier figure
  (+2.24%) discarded. Treat as closed unless a fresh mismatch appears.
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
  there is to delete the unused entry, not leave a gap marker. Edition 33 ran
  clean (38/38) on the first pass; edition 34 initially drafted several
  uncited Annex B entries, caught and fixed before rendering. **Edition 35
  initially drafted one unused Annex B placeholder (`[2]`, the independent
  index-close cross-check, planned but not yet cited inline) — caught
  immediately by running `check_refs.py` right after drafting, fixed by
  adding the missing `<sup class="ref">[2]</sup>` tag into the disclosure box
  sentence that was already describing that exact cross-check, then
  re-running clean at 34/34.** Worth re-stating: table cells (and disclosure
  box bullets) are a legitimate, already-used place to put a citation — use
  them rather than forcing an awkward prose mention just to attach a `<sup>`
  tag.
- Run `grep -c '~' briefing.html` before rendering (expect 0) — write
  "approx." from the start rather than typing `~` and cleaning up after.
  **Editions 29 through 35 have all rendered clean at zero tildes** on the
  first check — writing "approx." consistently from the first draft is what
  actually prevents this. **Note for the next run of this check: `grep -c`
  exits with status 1 (not 0) when the count is zero, since no lines matched
  — don't chain it with `&&` into a longer command and assume a silent
  failure means the check itself failed; read the printed count, not just
  the exit code.**
- **When a chart needs a normalized/relative figure (e.g. "% of open
  interest") and the underlying denominator can't be sourced, use a
  different, honestly-labelled normalization rather than dropping the chart
  or fabricating the missing figure.** Edition 24 needed this workaround;
  edition 29 hit a milder version (only ES had a full OI/gross breakdown).
  Edition 34 resolved this cleanly for the first time, with a fresh CFTC CoT
  report yielding full OI and Asset-Manager/Leveraged-Funds breakdowns for
  all three of ES, NQ and RTY. One naming note worth preserving: the CFTC's
  financial-futures table lists the full-size Russell 2000 E-mini ("RTY") as
  a separate line from the Micro E-mini Russell 2000, which has very
  different (much smaller) open interest and a different net-position sign
  at times — always confirm which of the two lines is being read before
  charting "RTY." **No new CFTC report was due within edition 35's window
  (Tuesday 29 Sept data, posted Friday 2 Oct, remained current); the chart #2
  slot reverted to the sector-ETF-proxy default accordingly — see Chart #2
  selection guidance below.**
- **When an "optional" filler element (e.g. a levels table) would just
  restate the same instrument list already in a main table with one extra
  column, that's still legitimate as long as the extra column is genuinely
  additive** (editions 25 and 28 both added this) — don't reject the idea
  purely because the instrument list overlaps; check whether the *added*
  column carries real information first. Editions 26, 27, 29, 30, 31, 33, 34
  and **35 did not need this padding at all** — page 3 filled cleanly from
  content alone every time. Edition 32 needed additive prose instead of a
  table. Edition 33 hit the opposite failure mode (genuine copy overflow to 5
  pages, fixed with five rounds of trim-and-re-render). Edition 34 and
  **edition 35 both rendered clean at 4 pages on the very first attempt**,
  with content filling pages 1-3 closely and no trimming or padding needed —
  a reminder that both failure modes (short page 3 and overflow) remain
  possible edition to edition and should be checked for specifically after
  every render, not assumed away just because recent editions have been
  clean.
- **Movers-chart outlier capping:** cap an extreme outlier bar at a fixed
  axis max with a value-label annotation only when one mover is a genuine
  order of magnitude larger than the rest. A spread under approx. 5x between
  the largest and next-largest mover does not need capping — confirmed again
  at edition 33 (Accenture +15.78% vs. Synopsys +12.78%, about 1.23x),
  edition 34 (Applied Optoelectronics +7.71% vs. Accenture -6.31%, about
  1.22x), and **edition 35 (PTC +33.49% vs. RXO +22.54%, about 1.49x)**, all
  left uncapped. Edition 30 remains the one genuine 10x+ case to date (about
  15x, capped at a fixed axis max of 30). The mechanism has now been
  confirmed working at both extremes across ten editions; no need to revisit
  the threshold or mechanism absent a genuinely new edge case (e.g. something
  in the 5-10x range).
- **Single-aggregator-only analyst-action roundups need the same scrutiny as
  single-aggregator movers lists (see below) — confirmed again at edition
  35**: a batch of four analyst actions (Harley-Davidson upgrade, Microsoft
  upgrade, Ryder System upgrade, Align Technology downgrade) were all sourced
  to a single Benzinga/Yahoo "Top Wall Street Calls" roundup rather than a
  primary sell-side note or two independent aggregators — reported with the
  single-aggregator caveat disclosed explicitly in the prose, consistent with
  how this report already treats single-aggregator movers lists.

## Known-hard-to-source (expect to mark unavailable, or use the workaround below)
- **VVIX, VIX9D, VIX6M, SKEW, MOVE index, CBOE daily put/call ratio:** try
  CBOE's own `cdn.cboe.com` (redirects to `cdn-api.cboe.com`) delayed-quotes
  JSON endpoint first — it often returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
  SKEW directly, but has (at least) three observed failure modes: (a) a full
  clean sweep with genuinely fresh timestamps on every series, (b) the more
  common "thin-series-stale" pattern, (c) total failure, where every series
  is stale. **Editions 28 through 35 all got a full clean sweep** — eight
  consecutive clean sweeps now, every series carrying a same-day
  `last_trade_time`, verified individually per series via a raw `curl`/direct
  fetch (not a tool-summarized fetch — see Hard rules above for why) each
  time. Still not a guarantee — keep checking `last_trade_time` on each
  series every time. Also note a `prev_day_close` field bug, observed eight of
  ten editions from 22-29: it duplicates the day's own `close`/
  `current_price` rather than giving a real prior-day reference, corrupting
  the feed's own `price_change`/`price_change_percent` fields too. The bug
  stayed absent for four straight editions (30-33). Edition 34 found a
  related but distinct bug in the same feed instead: the `price_change_percent`
  field divides by the current price rather than the prior close. **Edition
  35's direct fetch showed neither bug** — manual recomputation matched the
  feed's own stated percentages across all six series exactly, confirming
  both known bug patterns are intermittent rather than constant. **Always
  compute day-over-day % change manually against the previous edition's
  logged close, regardless of which of these two bug patterns (or neither)
  the feed's own fields appear to show this time.** The VIX9D-vs-spot-VIX
  front-end inversion first flagged at edition 28 (resolved as noise at
  edition 29) recurred at edition 30, and widened for five straight sessions
  through edition 34 (-1.68 → -1.83 → -2.14 → -2.39 → -3.25). **Edition 35
  broke that streak: the gap narrowed to -2.67** (still inverted, but by
  about 0.58 less than Friday). Continue reporting the inversion as a
  standing regime feature, but the narrowing means it is no longer a
  monotonic widening trend — watch whether it keeps narrowing, stabilizes, or
  resumes widening.
- **Dated GICS 11-sector tables / same-day sector performance:**
  Stockanalysis.com's ETF price-history pages return same-day closing price
  and % change for the SPDR Select Sector ETFs (XLE, XLK, XLC, XLY, XLP,
  XLRE, XLF, XLB, XLI, XLU, XLV) — the standing default for the sector table,
  and (absent fresher CoT data or another dominant story) chart #2. Edition 34
  used a fresh CFTC CoT dataset for chart #2 instead (ending the sector-proxy's
  nine-edition streak as chart #2), but the sector-ETF-proxy source itself
  continued working cleanly for the Section-2 TABLE. **Edition 35 had no fresh
  CoT data due in its window, so chart #2 reverted to the sector-ETF-proxy
  default** (Materials +1.31% led, Real Estate -0.34% the only sector down) —
  nine of now ten eligible editions have used this source cleanly for the
  table, the sole exception being the one edition a fresher CFTC dataset took
  the chart slot. No second same-day sector-ETF source has ever been found,
  so this remains a standing single-sourced item, disclosed each edition.
  **Stockanalysis.com single-stock pages are also the standing default for
  pinning an exact closing price/% change on any individual mover** — editions
  26 through 35 (ten straight) have all used direct fetches to it to resolve
  conflicting intraday-move percentages; **edition 35 used it to confirm all
  seven movers-table names plus Intel, Nike, Cisco and Align Technology**,
  catching a genuine unresolved Cisco conflict (stockanalysis.com +0.55% vs. a
  Yahoo/TheStreet claim of +3.6%) along the way. Note that a headline wire's
  own GICS sector-index percentages can differ slightly from the SPDR ETF
  price-change figures (a normal index-vs-ETF-price methodology gap); keep
  using the SPDR ETF figures as the table's primary numbers.
- **NYSE/Nasdaq closing breadth:** not obtainable as an official statistics
  table; Reuters' final wrap drops the breadth block. Mark unavailable **for
  the formal table**; wire commentary sometimes gives a usable qualitative
  breadth read in prose even when the table isn't available. Editions 33 and
  34 both hit an uncorroborated single-aggregator breadth figure and correctly
  excluded it — not separately attempted at edition 35 (ten of eleven SPDR
  sectors green made a formal breadth figure less load-bearing this time).
  Continue treating an uncorroborated single-aggregator (or unsourced
  search-summary) breadth figure as not usable — this has recurred enough
  times to treat as a durable, not occasional, gap.
- **Dealer gamma:** SpotGamma's own substack/site articles return either 403
  or an empty static/boilerplate page — now recurred at twelve-plus straight
  editions (edition 35's attempt returned HTTP 200 but still no usable dated
  data, a 12th straight failure to yield real figures), still worth a quick
  attempt each time in case it recovers. **zerogex.io is now confirmed across
  nine straight clean editions (27-35)**: after edition 34's regime flip to
  decisively positive (+$22.96bn, the largest single-session swing on record
  at the time), **edition 35 roughly doubled that again, to +$46.35bn** —
  plausibility-checked against the day's rally (SPX closed well above both
  Friday's close and the approx. 7,661 gamma-flip level, approaching the
  7,800 call wall) and directionally consistent, though the precise magnitude
  remains single-sourced (zerogex only; SpotGamma still yields no real
  numbers to cross-check against). Continue treating zerogex.io as the
  standing default source for dealer gamma, and continue checking each new
  reading's plausibility against the day's actual index move and
  gamma-flip distance. **Minor open item carried forward, still low
  priority**: zerogex's own stated wall levels (call/put wall) have still not
  been cross-checked against a secondary options note's implied walls —
  revisit only if a wall-level figure becomes load-bearing for a specific
  call.
- **Official CME FedWatch probabilities:** the page blocks fetching — use
  secondary citations (Polymarket, Kalshi, Reuters/other economist polls,
  desk notes) and give a range rather than a single invented number. At
  edition 34, secondary CME FedWatch citations collapsed from approx. 36-38%
  to approx. 17-21.6% within the session on the weak jobs report. **At
  edition 35, secondary CME FedWatch citations for October held roughly
  stable at approx. 21%; a December-decision figure as extreme as 90-100%
  also circulated and was judged implausible and discarded** — keep treating
  CME FedWatch as needing a disclosed range from secondary sources, not a
  single figure, and keep sanity-checking any secondary CME figure that looks
  like an outlier against the other venues before using it.
- **Kalshi direct fetch:** now rate-limited (HTTP 429, served a "Vercel
  Security Checkpoint" page) for **fourteen straight editions (23-35)** — a
  confirmed structural gap, not transient. Keep attempting each edition (it
  may recover), but a one-line "failed again, Nth straight edition" is
  sufficient prose; use Kalshi's own secondary reporting (its blog,
  prediction-market news aggregators — news.kalshi.com worked cleanly again
  at edition 35) as a workaround, as recent editions have done.
- **Official CME/ICE/Comex settlement prices:** frequently unobtainable via
  direct fetch (JS-rendered pages). LME's own site (lme.com) has failed
  thirteen editions running (22-34); **not re-attempted at edition 35** (went
  straight to the Westmetall fallback per standing practice, so the streak
  count is paused rather than extended — resume counting attempts if lme.com
  is tried again). Shanghai Metals Market (metal.com) failed again at edition
  35 (HTTP 404), continuing its near-total failure record. Westmetall.com has
  now worked cleanly **fourteen editions running** as the fallback (copper
  +0.52% to $14,430/tonne cash settlement at edition 35). Disclose whichever
  was used. Because the fallback chain can change edition to edition, treat
  any day-over-day copper % change built across two different sourcing
  chains as approximate. A standalone Investing.com or oilprice.com-derived
  Brent/WTI settlement page has now worked cleanly at editions 33, 34 and 35
  as a second independent confirmation route for oil specifically; **edition
  35 also used Investrade's Market Review as the primary oil/DXY source,
  reconciling cleanly against the prior edition's logged closes, while a
  separate Investing.com WTI figure did not arithmetically reconcile and was
  set aside** — see Hard Rules above for the reconciliation discipline this
  surfaced.
- **Official Treasury par yields:** home.treasury.gov's official daily
  **par-yield-curve CSV** (not the rendered HTML TextView page) worked
  cleanly at edition 34 with no lag. **Edition 35 sourced Treasury yields
  from TheStreet/CNBC market-wrap coverage rather than a direct Treasury CSV
  fetch** (10-year approx. 5.35%, +7bp, a fresh high since April 2002;
  30-year approx. 5.70%, +6-7bp, also a 24-year high; 2-year 4.85%, +2bp) —
  try the official CSV endpoint again next edition as the preferred primary
  source; it has a known maturity-column mis-mapping bug the HTML TextView
  page does not share, so prefer CSV over TextView when attempting it.
  Editions 33 and 34 each logged a sharp intraday-vs-close divergence in
  opposite directions (fresh intraday high easing into the close at ed. 33;
  diving intraday before reversing higher at ed. 34). **Edition 35 logged a
  third, simpler pattern: yields rose on the hot ISM Prices Paid print and
  simply held the gain into the close, with no reversal** — together these
  three editions reinforce the same lesson: always check whether a
  "yields spike/dive" headline refers to an intraday extreme or the close,
  since the two can diverge materially, but they don't always diverge — a
  same-direction intraday-to-close move is also a normal outcome worth
  confirming rather than assuming away.
- **CFTC CoT:** publishes Fridays with the prior Tuesday's data — always
  state the lag explicitly. `financial_lf.htm` (Traders in Financial Futures,
  Asset Manager/Leveraged Funds categories) works well for equity index
  futures (ES/NQ/RTY); the legacy `deacboelf.htm`/`deacboesf.htm` (CFE
  non-commercial/commercial) report carries VIX futures positioning — don't
  expect one page to have both. The report posted Friday 2 October 2026,
  covering Tuesday 29 September 2026 data, closed the ES-only partial-coverage
  gap with a full three-instrument (ES/NQ/RTY) pull: ES Asset Managers net
  long 904,003 (47.7% of OI 1,895,922) vs. Leveraged Funds net short 372,489
  (-19.6%); NQ Asset Managers net long 69,744 (25.8% of OI 270,554) vs.
  Leveraged Funds net short 24,723 (-9.1%); RTY (full-size Russell 2000
  E-mini) Asset Managers net long 39,768 (9.3% of OI 428,048) vs. Leveraged
  Funds net short 114,554 (-26.8%). The CFE legacy report showed VIX futures
  non-commercial net short 79,610 contracts against 421,113 total OI, also
  dated Tue 29 Sept. **Edition 35 confirmed, directly against cftc.gov's own
  release schedule, that no new report had posted within its window (the
  Tue 29 Sept data remains current) — exactly as expected, since the next
  report is due Friday 9 October 2026, covering Tuesday 6 October data.**
  Check for it first thing next edition, and continue fetching
  OI/gross-long-short for all three of ES, NQ and RTY up front when a fresh
  report is available.
- **GBP/USD and EUR/USD clean close:** the underlying sourcing (Yahoo
  Finance/TradingEconomics/FXStreet as primary sources) remains fully
  resolved since edition 26, confirmed again through edition 35 for EUR/USD
  (close 3-source agreement at edition 35: 1.1204-1.1205, -0.43% to -0.46%).
  **GBP/USD hit a minor, genuine two-source conflict at edition 35** (1.3224
  /-0.13% vs. 1.3218/-0.19%, both pointing the same direction) — both figures
  reported, not reconciled; a low-priority open item, not evidence the
  underlying sourcing has broken. This is distinct from the
  DXY-vs-FX-crosses directional-consistency check (see Hard Rules above),
  which continues to resolve within-session on every occurrence except the
  29→30 persistence, and resolved with no conflict at all at edition 35.
- **Gold/silver clean close on a non-event day:** the Kitco-vs-USAGOLD vendor
  gap itself has stayed quiet since normalizing at edition 31. **USAGOLD's
  own history pages returned HTTP 403 at edition 35, so the usual vendor-gap
  cross-check could not run this time** — try again next edition. Edition
  32's gold divergence (spot down vs. futures up) was a genuine
  different-instrument split; editions 33 and 34's gold readings converged
  cleanly (spot and futures moved the same direction). **Edition 35 saw a
  mild three-way split again** (gold spot -0.05% Kitco, futures -0.23%
  Investing.com, a third aggregator -0.13% Investrade, all down) —
  directionally consistent and explainable by timing/instrument differences,
  not flagged as a vendor error. Keep matching timestamps/instruments before
  calling any future gap anomalous. Silver's sign conflict (live since
  edition 31) has now stayed resolved for four straight editions (32-35).
  The live/current-page-contamination trap first caught at edition 34 (a
  non-archival Kitco page serving real-time, not historical, prices) was
  avoided at edition 35 by using Kitco's own dated PM Report article
  specifically — continue preferring a dated article/report over a live
  quote page when researching a past session.
- **China CPI/PPI (monthly):** typically prints on the 9th–10th of the
  month. **US import/export prices and industrial production:** frequently
  release mid-month on a Mon/Tue — confirm on the BLS/Fed release schedule
  rather than assuming a date. **ISM Manufacturing (Sept 2026), the
  September jobs report, and the September ISM Services PMI are all now
  closed threads** — see Standing Facts above for figures. **FOMC minutes
  from the 15-16 September meeting are due Wednesday 7 October, 2:00pm ET** —
  this falls after edition 35's cutoff; the next edition whose window spans
  2:00pm ET Wednesday should read them for hints of committee
  dissent/debate on a potential October move. **PPI is next due Thursday 15
  October 2026** (per a secondary macro-calendar preview, not independently
  cross-checked against a primary BLS release calendar this edition — worth
  a direct confirmation closer to the date).
- **Henry Hub natural gas:** the October contract thread resolved at edition
  32 (final settlement $3.00/MMBtu). The November contract has now failed
  **three consecutive editions (33, 34, 35)** to yield a confirmed CME
  end-of-day settlement — direct fetches to CME's settlements page have
  timed out or returned empty content every time, including two more
  timeouts at edition 35. **Per this report's own threshold (three
  consecutive failed attempts), this is now a durable gap, like lme.com** —
  stop attempting the CME settlements page every single edition; a periodic
  check (e.g. when the contract month rolls again, or every several editions)
  is enough, with the aggregator-quote caveat (edition 35: approx.
  $3.03/MMBtu, single-sourced, not independently corroborated this round)
  disclosed explicitly whenever a figure is reported at all.
- **Philadelphia Fed Nonmanufacturing Business Outlook Survey:** resolved at
  edition 27. Closed thread — no action needed unless a future release date
  approaches.
- **VIX options volume from Cboe's US Options Daily Market Statistics page:**
  substantially resolved at edition 29. Not attempted at editions 33, 34 or
  35 (secondary priority; options-flow colour has instead been sourced from
  dedicated options-flow wires, though editions 34 and 35 both found none of
  their candidate wires clean enough to use — see Hard Rules above). Going
  forward: always state which specific category/table a Cboe options-volume
  figure comes from, and don't over-invest time here if it stalls, this is a
  secondary-priority item per the derivatives section's own weighting.
- **Weekend equities catalyst to watch: 13F filings** (Q1 ~May 15, Q2 ~Aug
  14, Q3 ~Nov 14, Q4 ~Feb 14) — factor into a Monday-briefing lead by
  default when the window includes one. Not applicable at editions 30
  through 35; next due approx. 14 November 2026.
- **A historical-average FOMC-day move benchmark** (for a three-bar
  implied/historical-average/realized chart) has not yet been sourced in any
  edition to date (tried and failed at edition 22) — either find a citable
  benchmark before reaching for that chart type, or stick to describing
  implied-vs-realized in prose without the third bar. Not attempted again
  through edition 35.
- **CFTC total open interest by instrument/date** (needed to normalize
  positioning "as % of open interest"): fully resolved at edition 34 for ES,
  NQ and RTY in one pull from cftc.gov. Repeat this full three-instrument
  fetch whenever a fresh CoT-based chart is next used, watching for the
  Micro-vs-full-size Russell naming trap each time (see Hard Rules).
- **Named-desk confirmation of individual index-fund passive-flow figures**
  tends to come from independent research Substacks/blogs rather than a
  sell-side desk by name — treat as citable but note it's not a
  bulge-bracket named source when it matters for confidence level.
- **Dollar price targets on non-headline analyst actions are frequently
  unobtainable even when the rating direction is clear** — editions 27
  through 32 had mostly clean runs; edition 33 was mixed; edition 34 hit a
  milder version (Argus/Accenture, single-aggregator). **Edition 35 obtained
  clean dollar PTs for all four of its analyst actions** (Citigroup/HOG $33
  from $31; Melius/MSFT $665; JPMorgan/Ryder $298 from $296; Evercore
  ISI/ALGN cut to $155 from $220) but all four traced to a single
  Benzinga/Yahoo aggregator roundup rather than a primary sell-side note or
  two independent aggregators — see the new Hard Rules entry on
  single-aggregator analyst-action roundups above. Report the rating
  direction and firm with confidence; treat a missing dollar target or
  unclear dating as a normal gap to flag, not something to chase hard,
  unless the name is the edition's dominant story.
- **Single-aggregator-only movers lists need individual verification, not
  bulk acceptance** (first flagged at edition 29). Editions 30-34 each hit
  milder versions. **Edition 35's clearest instance: an AutoNation downgrade
  (to Equal Weight, PT $175) could not be traced to a named issuing firm** —
  excluded from the main copy and logged in Annex A rather than reported
  with an invented or unconfirmed firm name. Separately, three Monday
  single-stock moves (Nu Holdings +13.03%, MercadoLibre +9.67%, XP Inc
  approx. +33%) were single-sourced to a Yahoo Finance live blog and not
  independently corroborated at stockanalysis.com — excluded from the main
  movers table and logged in Annex A instead of being reported at face value.
  This remains the right call when time-constrained: corroborate with a
  second source or flag it as unverified in Annex A.

## Production notes (technical)
- Charts: matplotlib → PNG, referenced from HTML. `figsize=(9.8, 1.95)` and
  `(9.8, 1.55)`–`(9.8, 1.75)` depending on chart type, `font.size 9.6`, dpi
  210, `width:100%` in the page. For a grouped (multi-series) bar chart, such
  as edition 34's CFTC Asset-Manager-vs-Leveraged-Funds chart, the simple
  single-series `barh()` helper in `make_charts.py` doesn't apply — write a
  dedicated `grouped_bar()` function instead (vertical bars, two series per
  category, legend below the plot). Watch for two specific layout traps with
  grouped/legend charts that don't arise with the simple single-series
  helper: (1) a legend placed directly below the x-axis tick labels can
  overlap them — fix by adding `tick_params(axis="x", pad=...)` to push the
  category labels down and placing the legend between the axis and the
  labels, or further below with enough reserved bottom margin; (2) a
  rotated/long y-axis label can get clipped at the figure's left edge when
  using a fixed `fig.subplots_adjust(left=...)` instead of
  `bbox_inches="tight"` — either shorten the label text or increase the left
  margin fraction until it stops clipping, and always visually inspect the
  rendered PNG (via the Read tool) before embedding it in the HTML rather
  than assuming the matplotlib call succeeded cleanly. **Edition 35 reverted
  to the simple single-series `barh()` helper (sector-ETF-proxy chart #2),
  which continues to work cleanly with no layout issues.**
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
  overflow each time. **Editions 34 and 35 both rendered clean at 4 pages on
  the very first attempt** — content filled pages 1-3 closely without
  overflowing, and page 4 (the annex) had the usual comfortable amount of
  white space. Always re-render and re-check the page count after each
  trim/pad round rather than guessing how much is enough.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave
  header rows as plain `<tr>`. **Edition 35's Commodities & FX table ran long
  enough to split naturally across the page 2/3 boundary** (WTI through
  silver-futures on page 2, copper through USD/JPY on page 3) with no
  repeated header row and no layout problem — plain-`<tr>` tables reflow
  across a page break safely; this is expected behavior, not a bug to fix.
- Always verify the render: `pdftoppm -png -r 100` (or similar) and actually
  read the page images before delivering — don't trust the page count alone.
  Editions 25 and 28 both hit a visibly short page 3 on the first render
  despite passing the 4-page check, fixed with an optional levels table.
  Edition 32 hit a visibly short page 3, fixed with additive prose instead of
  a new table. Edition 33 hit the opposite problem (overflow) and needed
  five trim rounds. Editions 34 and **35 both needed no fixes at all** — all
  four pages read cleanly with good content density on inspection, confirmed
  by actually reading the rendered page images (via the Read tool), not
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
  29-31, 33, 34 or 35). Edition 32 needed page-3 padding via additive prose
  instead. Edition 33 needed active trimming instead. Always re-render
  immediately after adding (or removing) any content to confirm the page
  count, rather than assuming a change is safe.

**Chart #2 selection guidance:** pick by what the day's dominant story
actually is. Macro/rotation with no fresher signal → SPDR sector-ETF proxy
(same-day closes, the standing default — used across ten eligible editions,
25 through 35, with edition 34 the sole exception when fresher CFTC data was
available). Fresh CFTC CoT data on a Monday/weekend-window edition → the
ES/NQ/RTY asset-manager-vs-leveraged-funds positioning chart, normalized as
% of open interest — this materialized for the first (and so far only) time
at edition 34; **edition 35 had no fresh CoT data due in its window (the
Friday 9 Oct report wasn't due yet) and correctly reverted to the
sector-ETF-proxy default**, confirming the guidance's own instruction to
check freshness each time rather than assume the CFTC chart is now
permanent. A single dominant earnings print with a clean, well-sourced
implied-vs-realized-move story → a three-bar implied/historical-average/
realized move chart (the historical-average leg has never actually been
sourced successfully). A genuine multi-sector broadening/deepening selloff
across consecutive sessions → the sector-ETF proxy rendered as a grouped
(day-over-day) bar instead of single-day. A holiday-window preview edition
with no fresher data → VIX futures term structure with event annotations.
When chart 1 (movers) already covers the earnings/single-name story, the
sector proxy (or, when fresh, the CFTC positioning chart) is a good
complementary choice even on a stock-heavy day, since the two stories
reinforce rather than duplicate each other. Chart #2's placement in the
document should follow its content, not a fixed section — edition 24 and
edition 34 both placed a CFTC/positioning chart #2 in Section 5
(Derivatives) rather than Section 2; **edition 35, back on the sector-proxy
default, placed it back in its usual Section 2 spot.** Continue checking CoT
freshness first each Monday/weekend-window edition rather than assuming
either chart type is now the permanent default for that edition type.

## Edition log
Compact history for continuity — enough for the next edition to know the
last cutoff, avoid repeating items, and see any standing open threads. Older
editions are condensed; keep the most recent edition in full detail, the
prior one condensed to a medium paragraph, and fold editions further back
into the running mega-block once they've had their turn as the condensed
paragraph.

**Editions 1–33 (condensed):** established the format (edition 1 baseline;
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
27,244.28 (+0.45%, this close stood as the standing Nasdaq closing record
until edition 35 broke it); Viking Therapeutics +35.67% was the standout
mover; the five-central-bank Thursday/Friday cluster was first dated here;
gold showed a genuine Kitco-vs-USAGOLD split (approx. $50 apart, later
resolved). Edition 27 (Thu 24 Sept, covering Wed 23 Sept): a broad risk-off
session — S&P -0.75% to 7,706.03, Dow -0.68% to 51,511.59, Nasdaq -1.13% to
26,936.04, driven by the 10-year spiking to a 19-year high (approx. 5.09-5.14%)
after a hot flash PMI and Fed Governor Barr's hawkish remarks; the "Meta
Muse" AI-agent disintermediation theme rotated from banks into online travel
names (Expedia -7.72%, Airbnb -7.56%, Booking -5.07%); Paychex -8.77%,
Cracker Barrel +4.49%; gold's Kitco-vs-USAGOLD split narrowed to about $7;
VIX closed 15.18 (+6.83%); zerogex.io gave its first working dealer-gamma
read. Edition 28 (Fri 25 Sept, covering Thu 24 Sept): a whipsaw session
closed almost exactly flat (S&P -0.1% to 7,704.13, Dow -0.3% to 51,349.98,
Nasdaq +0.1% to 26,939.37); Communication Services led on a Meta rally; MGM
Resorts -10.99% (take-private bid withdrawn), Oracle -3.47%, Darden -3.02%;
Thursday's central-bank cluster confirmed (Norges Bank hike, Riksbank/SNB/
Banxico holds); the Trump-Xi Washington summit extended the US-China trade
truce to 10 Jan 2027; gold's Kitco-vs-USAGOLD split closed to just $0.16.
Edition 29 (Mon 28 Sept, covering Fri 25 Sept, the week's one session): a
relief rally closed the week higher (S&P +0.5% to 7,743.41, Dow +0.9%,
Nasdaq +0.5%); Meta -3.33% on the Cambridge Analytica verdict (theoretical
exposure up to approx. $219.5bn), Costco +2.93%, Twilio -7.96%; a new CFTC
CoT report posted (dated Tue 22 Sept); the US-China $30bn tariff-cut
agreement was first reported (confirmed at edition 30); a first
DXY-vs-FX-crosses directional mismatch surfaced; zerogex.io flagged an
anomalous approx. 9x dealer-gamma jump (+$32.56bn), later explained as a
gamma-flip-crossing effect. Edition 30 (Tue 29 Sept, covering Mon 28 Sept,
the window's one session): a broad risk-off reversal erased the prior week's
relief rally — S&P 500 -0.77% to 7,683.69, Dow -0.67% to 51,481.51, Nasdaq
-0.92% to 26,820.38, driven by Trump rejecting an Iranian Hormuz-reopening
offer and the 10-year spiking to approx. 5.24%; Kodiak Sciences +177.96%
(Phase 3 win, the capping rule's first genuine 10x+ outlier), MongoDB
-18.46% (CEO resignation), Meta -4.79%, Roblox -9.86%, Boeing -6.91% (FAA
737 MAX 10 certification delay), Nvidia +1.68% ($150bn buyback);
October-hike odds jumped (Polymarket to 69%, CME dispersed to approx.
54-85%); the US-China "30-for-30" framework confirmed via primary sources;
the RBA's Tuesday decision was previewed (+25bp to 4.60%, later confirmed
correct); gold's Kitco-vs-USAGOLD gap widened sharply to approx. $32 (later
normalized); the DXY-vs-FX-crosses conflict recurred for a second session;
VIX 16.07 (+8.07%); zerogex.io's SPX gamma flipped to -$9.33bn. Edition 31
resolved the DXY-vs-FX-crosses conflict cleanly and logged zerogex.io at
-$17.19bn (further negative). Edition 32 (Thu 1 Oct, covering Wed 30 Sept):
a volatile round-trip session closed slightly lower (S&P 7,651.54, -0.25%)
after an intraday high on a cooler August PCE print faded into an unexplained
late reversal; Technology was the only green sector; Liquidia -57.19%
(patent loss) was the standout mover, FICO -4.11% extended Tuesday's
FHFA-driven crash; Micron beat cleanly after the close but drew only a
modest AH reaction; oil rallied on Iran-sanctions comments; gold's
spot/futures split (later converged) and a reopened DXY-vs-crosses conflict
(resolved again at edition 33) both first appeared here; VIX 16.34 (+1.87%);
zerogex.io's gamma moved back toward zero (-$14.33bn). Edition 33 (Fri 2
Oct, covering Thu 1 Oct): yields, not equities, drove the session — a hot
September ISM Manufacturing Prices Paid print (77.9 vs. 71.1 prior) alongside
a European/UK gilt selloff spiked the 10-year intraday to approx. 5.34%
(highest since 2002) before easing into a green close (S&P +0.19% to
7,666.45, Dow +0.04%, Nasdaq +0.04%, Russell +0.35%); Accenture +15.78% (FQ4
beat) and Synopsys +12.78% (Investor Day/OpenAI deal) led an AI-infrastructure
earnings cluster alongside Coherent, Lumentum and Applied Optoelectronics;
Nike missed FQ1 and guided FY27 sales down high-single-digits, falling
approx. 8.7% after hours (resolved at edition 34); FICO's two-sided
after-hours story began (also resolved at edition 34); October-hike odds
split sharply across venues for the first time since the prior week's
unified collapse (later reconverged at edition 34); Brent's Nov-to-Dec
contract roll turned out to have already happened; Henry Hub's new November
contract could only be sourced as a midday quote, the first of what became
three straight failed editions; gold and silver each converged cleanly
across spot/futures; the DXY-vs-FX-crosses conflict resolved cleanly again;
VIX 16.39 (+0.31%, sixth consecutive clean CBOE sweep); VIX9D inversion
widened to -2.39. 38 sources, zero mismatches on the first `check_refs.py`
run, zero stray tildes. The document overflowed to 5 pages on the first
render (genuine copy overflow) and needed five rounds of trim-and-re-render
to reach a clean 4-page render.

**Edition 34 (condensed)** — Monday 5 October 2026 report covering Friday 2
October 2026, the window's one NYSE session, plus the weekend. A badly-missed
September jobs report (nonfarm payrolls +29,000 vs. approx. 84,000-90,000
consensus, unemployment 4.2%, July revised to an outright -10,000) drove a
broad risk-on rally and a sharp cross-venue collapse in October-hike odds
(to approx. 17-21.6%, from Thursday's 25-38% split): S&P 500 +0.73% to
7,722.72 (resolved a small two-source conflict via a direct SPY/VOO
cross-check), Dow +0.49% to 51,176.96, Nasdaq Composite +1.20% to an
intraday-record but not closing-record 27,190.86, Russell 2000 +0.90% to
2,832.90. Ten of eleven SPDR sectors closed green. Tesla +4.65% to $370.59
on a Q3 delivery beat; the AI-infrastructure/optics trade extended for a
second/third session (AAOI +7.71%, Coherent +5.59%, Lumentum +3.79%);
Accenture reversed -6.31% on profit-taking even as Argus raised its PT;
Nike extended its slide to a 13-year low (-3.64% to $33.87), resolving
Thursday's open question; FICO fully reversed Thursday's after-hours plunge
to close effectively flat. Wells Fargo upgraded BP/cut ExxonMobil; Barclays
cut Mobileye. Macro facts (Fed Chair, funds rate, next FOMC, BoE/BoJ dates,
shutdown status, US-China tariff framework) all reconfirmed unchanged via
direct primary-source fetches. A new CFTC CoT report (data through Tue 29
Sept) gave, for the first time, a fully consistent OI normalization across
ES/NQ/RTY, powering a CFTC-positioning chart #2 (ending the sector-proxy's
nine-edition streak in that slot). The CBOE feed gave a seventh consecutive
full clean sweep (VIX 15.31, -6.59% after correcting a newly-discovered
feed-field bug); VIX9D's inversion widened to -3.25 (fifth consecutive
session); zerogex.io's SPX gamma flipped decisively positive, to +$22.96bn
from -$11.58bn, the largest single-session swing logged to that point. WTI
-1.90% to $91.11 (SPR release), Brent -0.06% to $102.25 (December still
front-month); gold and silver both reversed from early gains to close lower
across spot and futures alike; DXY -0.16% to -0.17% (magnitude
cross-vendor gap, direction consistent with weaker-dollar crosses); Treasury
yields dove intraday before fully reversing to close higher. 40 sources,
clean 4-page render on the first attempt after catching several uncited
Annex B placeholders pre-render.

**Edition 35 (most recent — full detail)** — Tuesday 6 October 2026 report
covering Monday 5 October 2026, the window's one NYSE session, research
window Sun 4 Oct 2026 20:00 ET through Mon 5 Oct 2026 20:21 ET. Verified the
two structural header rules again (date line = edition date, window line
states the given research-window start with the session covered noted
parenthetically) — now clean across seven consecutive single-session or
single-session-plus-weekend editions (29-35).

Two same-day cash buyout announcements drove the tape rather than a broad
macro tailwind: Schneider Electric agreed to acquire PTC Inc for $22.6bn
($205/share cash, approx. 42% premium) and C.H. Robinson agreed to acquire
RXO Inc for $5.8bn (approx. $30.25/share, approx. 29% premium) — PTC +33.49%
to $192.26, RXO +22.54% to $28.65, while acquirer C.H. Robinson fell -10.85%
to $140.61 on dilution/financing concerns. Equities extended Friday's
post-jobs-report rally to a Nasdaq Composite record close of 27,477.31
(+1.05%), finally breaking 23 September's 27,244.28 record; S&P 500 +0.66%
to 7,773.95 (AP, cross-checked independently with no material conflict),
Dow +0.18% to 51,267.90, Russell 2000 +0.50% to 2,847.14. Ten of eleven
SPDR sectors closed green (Materials +1.31% led, Real Estate -0.34% the
only sector lower), reverting chart #2 to the sector-ETF-proxy default since
no fresh CFTC data was due this window.

September's ISM Services PMI printed 54.9% (Aug 55.4%, consensus approx.
55.0%), with a hot Prices Paid sub-index (74.0%, highest since July 2022)
driving the 10-year Treasury yield to a fresh 24-year high near 5.35% (30-year
also a 24-year high near 5.70%) — equities absorbed the move without a
risk-off reaction, a notable divergence from late-September sessions.
Single-name stories: Cerebras Systems +9.08% after Sam Altman reaffirmed the
OpenAI partnership, countering last week's approx. 20% slide; TSMC hit a
record high (+2.75%) and Intel fell -2.63% on reports Musk is in early talks
to bring TSMC into his Texas "Terafab" venture; the AI-optics trade was
mixed (AAOI +5.17% extended a fourth straight session, Coherent -1.01%
reversed, Lumentum +0.65% decelerated); Moderna +6.95% on Nasdaq-100
inclusion, a COO return, and cancer-vaccine trial optimism. A single-source
analyst-action roundup gave Citigroup/Harley-Davidson, Melius/Microsoft and
JPMorgan/Ryder System upgrades plus an Evercore ISI/Align Technology
downgrade (-2.15%, PT cut to $155 from $220). Two distinct new sourcing
traps were caught and disclosed: a wave of circulating "Monday" Nike
price-target cuts actually originated Friday/Saturday, with a Yahoo Finance
article republishing a stale Friday closing price as if current (NKE
actually closed flat, +0.27%); and a premarket feed's "+96%" Paramount
Skydance figure was a mechanical artifact of a same-day 2-for-1 stock split
feeding a stale unadjusted quote, not a real move — the first time this
report has documented a corporate-action data artifact as distinct from
stale-date republishing or intraday/close divergence.

Macro facts (Fed Chair, funds rate, next FOMC date, US-China tariff
framework) were reconfirmed via direct primary-source fetches; BoE and BoJ
rate/meeting-date facts and the shutdown/CR status were reconfirmed via
secondary citations only this round (flagged for direct primary re-checks
next edition). October-hike odds held roughly steady (approx. 17-23% across
venues); December-hike odds firmed somewhat to approx. 65-75%, still
unconfirmed against a primary venue, with an implausible 90-100% CME figure
discarded. WTI -1.84% to $89.43, Brent -1.89% to $100.32 (December still
front-month, no roll, via Investrade — reconciled cleanly against the prior
close, while a conflicting Investing.com figure did not reconcile and was
set aside); Henry Hub's November contract failed a third consecutive
edition to yield a clean CME settlement, now reclassified as a durable gap;
gold and silver both logged a small multi-way spot/futures/aggregator split,
directionally consistent and read as the recurring timing-basis effect;
copper +0.52% via Westmetall; DXY approx. +0.26-0.33% (vendor magnitude gap
persists) fully consistent in direction with all three major FX crosses for
the first time in several editions. CBOE's feed gave an eighth consecutive
full clean sweep with neither of its two previously-documented %-bugs
present (VIX 15.52, +1.37%, manually recomputed and cross-confirmed);
VIX9D's inversion narrowed to -2.67 from -3.25, breaking a five-session
widening streak. zerogex.io's SPX dealer gamma roughly doubled again, to
+$46.35bn from +$22.96bn, plausibility-checked against the index closing
well above the gamma-flip level and approaching the call wall. No new CFTC
CoT report was due (confirmed against cftc.gov's release schedule; next due
Fri 9 Oct). No clean single-stock options-flow story could be verified;
candidates traced to a Friday-dated Schwab update and were excluded. 34
sources, one initially-uncited Annex B placeholder caught and fixed before
rendering (34/34 clean on the second `check_refs.py` pass), zero stray
tildes, clean 4-page render on the first attempt.

**Open threads for edition 36:** the next CFTC CoT report is due Friday 9
October (covering Tuesday 6 Oct data) — check first thing, continuing the
three-instrument (ES/NQ/RTY) fetch. FOMC minutes from the 15-16 Sept meeting
are due Wednesday 7 October, 2:00pm ET — the week's most relevant scheduled
item given the live rate-path debate; read for hints of October-hike
dissent if the edition's window spans that time, otherwise note it as
already-published background. Bank of England and Bank of Japan
rate/meeting-date facts, and the shutdown/CR status, were confirmed via
secondary citations only at edition 35 — do a direct primary-source
re-fetch (bankofengland.co.uk, boj.or.jp, whitehouse.gov/congress.gov) next
edition rather than letting secondary-only confirmation repeat. USAGOLD's
history pages 403'd at edition 35 — retry for the gold/silver vendor-gap
cross-check. Henry Hub's November-contract CME settlement is now a durable
gap (three consecutive failures) — stop attempting every edition per the
report's own three-strikes threshold; revisit periodically instead. Watch
whether the AI-optics trade (AAOI/COHR/LITE) stabilizes, extends, or breaks
down further given Monday's mixed result, and whether Intel/TSMC's Terafab
story develops further news. Watch whether zerogex.io's SPX dealer gamma
continues climbing, holds, or reverts, especially around Wednesday's FOMC
minutes. Watch December-FOMC hike odds for a firmer primary-venue
confirmation as the range has now moved twice in two editions. The
Meta/Cambridge Analytica penalty hearing had supplemental briefs due Tuesday
6 October, with a decision signaled roughly two weeks after (approx. 20
October) — watch for it. Minor low-priority open items, revisit only if they
become load-bearing: Cisco's Monday % change conflict (stockanalysis.com
+0.55% vs. a Yahoo/TheStreet +3.6% claim, unresolved); GBP/USD's exact
Monday close (two sources disagree by a few bp); WTI's exact Monday
settlement (a second aggregator's figure didn't arithmetically reconcile);
AutoNation's downgrading firm (unconfirmed); Nu Holdings/MercadoLibre/XP Inc
Monday moves (single-sourced, excluded this edition). The hypothesized Brent
Dec-to-Jan roll (around 31 Oct/1 Nov) is not yet due — keep on the watch
list. Threads closed after resolution rather than carried further: the
September ISM Services PMI (actual print now on file); the Nike
stale-price-target-cut narrative (corrected, NKE's actual Monday move
logged); the Paramount Skydance split artifact (identified and excluded);
the CBOE feed's two documented %-bugs (confirmed intermittent, both absent
this edition); the VIX9D widening streak (broken, now narrowing).
