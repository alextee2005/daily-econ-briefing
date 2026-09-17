# Format, layout and charts

## Document structure (locked)

1. Title + meta line (date, window, research cutoff, edition number)
2. Disclosure box — assumptions, corrections carried from prior editions,
   status notes. Scales comfortably to ~8 items. This is where a correction to
   a previously-published figure belongs, and where a premise-level correction
   (a date, a person, an event that did/didn't happen) belongs too.
3. **60-second read** — exactly 5 ranked items, the interpretation layer
4. **1 Market recap** — snap-grid tiles + one paragraph
5. **2 Equities and earnings** — LEAD, largest section: sector rotation, movers
   table, earnings, analyst actions
6. **3 Macro, policy and rates** — condensed
7. **4 Commodities and FX** — levels table + prose. Hard assets and FX only
8. **5 Derivatives, volatility and positioning** — condensed, no credit
9. **6 The day ahead** — catalysts table + "sector setup we take into
   [session]" bullets
10. *(page break — the only forced one in the document)*
11. **Annex A** — what could not be verified, two columns
12. **Annex B** — numbered sources, three columns
13. Method note

Sources are numbered inline as small blue superscript `[n]` pointing to Annex B.
Never put URLs in the body.

## CSS baseline

Stable across many editions; don't tighten it without evidence of overflow.

- Letter; margins `1in` top/bottom, `13mm` left/right. **Set margins in exactly
  one place** — either CSS `@page` or Playwright's `page.pdf()` option, never
  both, or they stack and double.
- Body 8.0pt / line-height 1.20, serif, `text-align: justify`; `p` margin-bottom
  2.4px
- Reset `text-align: left` on h1/h2/h3, table cells, tiles, the meta line and
  the Annex column lists — justifying short cells or narrow multi-column lists
  looks worse, not cleaner
- h1 14.5pt; h2 9.1pt (margin 4px 0 1.6px 0); h3 7.9pt (margin 2.4px 0 1px 0)
- Tables 7.4pt, 1.8px cell padding, margin-bottom 3px
- Tiles: 7.4pt label / 9.4pt value / 7.3pt change; padding 2px 4px; grid
  margin-bottom 3.5px
- `ul.bullets li` margin-bottom 1.4px
- Annex A: 2 columns @ 7.1pt, `break-inside: avoid` per `li`
- Annex B: 3 columns @ 5.5pt

`assets/template.html` has this as a working skeleton.

## Layout traps

- **Only one forced `page-break-before` in the document** — immediately before
  Annex A. Sections 1–6 flow naturally. A stray extra break shows up as a
  5-page PDF where one page is mostly blank with a section starting fresh on the
  next despite obvious room remaining. `grep -n pagebreak` before troubleshooting
  anything else.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave header
  rows as plain `<tr>`.
- The `~` character renders as a minus-like glyph at these point sizes. Write
  "approx." from the start; the late-added line outside the main drafting pass
  is where a stray one usually slips in.

## Filling a short page 3

Two blocks belong at the end of Section 6 by default on any single-session or
weekend-window edition: the known-catalysts table and the sector-setup bullets.
If page 3 still runs short after those, add an optional "Commodities & FX
levels" table (~13 rows) at the end of Section 4. It's genuinely
general-purpose — reach for it when content alone doesn't fill the page, not on
a schedule.

## Chart selection

Chart 1 is always the single-stock movers bar. Cap an outlier bar at a fixed
axis max with a value-label annotation only when one mover is an order of
magnitude larger than the rest; a 2–3x spread doesn't need it.

Pick chart 2 by what the day's dominant story actually is:

| Situation | Chart 2 |
|---|---|
| Macro/rotation day, no fresher signal | SPDR sector-ETF proxy, single-day bar (the default) |
| Fresh CFTC CoT data (Mon/weekend window) | Asset-manager vs. leveraged-funds net position across ES/NQ/RTY, normalized as % of open interest so the indices are comparable |
| One dominant earnings print with clean implied-vs-realized data | Three-bar implied / historical-average / realized move |
| Multi-session broadening selloff | Sector-ETF proxy as a grouped day-over-day bar |
| Holiday/preview edition, no fresh data | VIX futures term structure with event annotations |

When chart 1 already covers the earnings story, the sector proxy complements it
well even on an earnings-heavy day.
