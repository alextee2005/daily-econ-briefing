# Format, layout and charts

## Document structure (locked)

1. Title + meta line (date, window, research cutoff, edition number)
2. Correction box — **corrections only**, and only on an edition that has one.
   A figure published in an earlier edition that turned out to be wrong, or a
   premise-level correction (a date, a person, an event that did or didn't
   happen). Terse: what was published, what it should have been. Most
   editions omit the box entirely. Assumptions and status notes do **not**
   belong here any more — they go to Annex A, where a reader can find them if
   they want them. A correction stays on page 1 because a reader who acted on
   yesterday's wrong number will not go looking in an annex for the news.
3. **60-second read** — exactly 5 ranked items, the interpretation layer
4. **1 Market recap** — snap-grid tiles + paragraph, then **sector
   performance**: the SPDR sector-ETF chart and the narration of how each
   sector did. All sector and ETF material lives here.
5. **2 Equities and earnings** — LEAD, largest section, and **purely
   single-stock**: movers chart, movers table, earnings, guidance, analyst
   actions. No sector or ETF commentary — if a sentence is about a sector
   rather than a name, it belongs in section 1.
6. **3 Macro, policy and rates** — condensed: policy-rate table + prose
7. **4 Commodities and FX** — levels table + prose. Hard assets and FX only
8. **5 Derivatives, volatility and positioning** — condensed, no credit
9. **6 The day ahead** — catalysts table + "sector setup we take into
   [session]" bullets. Forward-looking, so it stays here rather than moving
   to section 1 with the rest of the sector material.
10. *(page break — see "Where the annex starts" below; present on most
    editions, dropped on a spillover edition)*
11. **Annex A** — assumptions, status notes, and the full record of any
    correction, two columns
12. **Annex B** — what could not be verified, two columns
13. **Annex C** — numbered sources, three columns
14. Method note

Sources are numbered inline as small blue superscript `[n]` pointing to Annex C.
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
- Annex A and Annex B: 2 columns @ 7.1pt, `break-inside: avoid` per `li`
- Annex C: 3 columns @ 5.5pt

`assets/template.html` has this as a working skeleton.

## Layout traps

- **At most one forced `page-break-before` in the document** — immediately
  before Annex A, and on a spillover edition not even that (see "Where the
  annex starts"). Sections 1–6 always flow naturally. A stray *extra* break
  shows up as a 5-page PDF where one page is mostly blank with a section
  starting fresh on the next despite obvious room remaining. `grep -n
  pagebreak` before troubleshooting anything else: the count should be 1, or 0
  on a spillover edition, never 2.
- `<thead>` on the two-column tables pushes the layout to 5 pages — leave header
  rows as plain `<tr>`.
- The `~` character renders as a minus-like glyph at these point sizes. Write
  "approx." from the start; the late-added line outside the main drafting pass
  is where a stray one usually slips in.

## The policy-rate table (Section 3)

Other central banks' rates go in a table, not in prose. A paragraph that walks
the reader through six banks' levels is the least readable thing in the
document and the easiest to leave stale.

| Central bank | Policy rate | Last change | Next decision |
|---|---|---|---|

The Fed goes first as the anchor to compare against, then whichever of the
BoE, BoJ, ECB, SNB, Norges Bank, Riksbank, RBA, BoC and Banxico the window
actually touches. Eight to ten rows is the working range. A bank with no
verified current rate gets the row with that cell marked unavailable and an
Annex B entry — dropping the row hides the gap.

**This replaces the prose that used to carry those levels; it is not added on
top of it.** Section 3's prose keeps what a table cannot hold: what moved
inside the window, vote splits, the divergence that matters, the one bank
whose guidance changed. Net page impact should be roughly neutral. If page 3
overflows anyway, cut rows that had no news in the window before cutting any
prose.

Policy rate and next decision are live facts — verify both fresh every run.
Last change is settled history once its date has passed, so it carries
forward. See "Verify before you build" in SKILL.md.

## Where the annex starts

Four pages is the hard limit, and it has not moved. What has changed is where
the briefing is allowed to put them.

- **Sections 1–6 end on page 3** (the common case): keep the forced break. The
  annex opens a clean page 4, exactly as before.
- **Sections 1–6 spill onto page 4**: **delete the `pagebreak` div and
  re-render.** The annex then follows the spillover down the same page instead
  of being shoved onto a fifth. Space on page 4 is shared between the two
  rather than reserved for the annex.
- **Still five pages with the break gone**: now trim, in this order — sector
  table rows with no news in the window, then the optional third chart, then
  prose. Trimming is the last resort, not the first.

This cannot be expressed in CSS: no print rule says "break only if what
follows would otherwise start a new page anyway". It is a decision taken at
render time, which is why step 5 of the workflow reads the page images rather
than trusting the page count. Get it the wrong way round and the failure is
quiet — a 5-page PDF with a half-empty page 4, which is also what a stray
extra break looks like.

## Filling a short page 3

Two blocks belong at the end of Section 6 by default on any single-session or
weekend-window edition: the known-catalysts table and the sector-setup bullets.
If page 3 still runs short after those, add an optional "Commodities & FX
levels" table (~13 rows) at the end of Section 4. It's genuinely
general-purpose — reach for it when content alone doesn't fill the page, not on
a schedule.

Expect to need this less often now that section 1 carries the sector chart and
narration. A short page 3 and a spillover onto page 4 are opposite problems
with opposite fixes, and this section is only ever the answer to the first.

## Chart selection

Two charts are fixed, and their placement is no longer editorial:

| Chart | Section | Always? |
|---|---|---|
| SPDR sector-ETF performance | **1 Market recap** | yes |
| Single-stock movers bar | **2 Equities** | yes |

The sector chart lives with the sector narration, which is the whole point of
it being in section 1. The movers bar stays with the names.

Cap an outlier movers bar at a fixed axis max with a value-label annotation
only when one mover is an order of magnitude larger than the rest; a 2–3x
spread doesn't need it. For the sector chart, a single-day bar is the default;
use a grouped day-over-day bar on a multi-session or weekend window.

### The optional third chart

Only when positioning or volatility is genuinely the day's dominant story —
not merely present, and not as a way to fill a short page. It goes in the
section it belongs to, not in section 1 or 2:

| Situation | Third chart | Section |
|---|---|---|
| Fresh CFTC CoT data (Mon/weekend window) | Asset-manager vs. leveraged-funds net position across ES/NQ/RTY, normalized as % of open interest so the indices are comparable | 5 Derivatives |
| One dominant earnings print with clean implied-vs-realized data | Three-bar implied / historical-average / realized move | 2 Equities |
| Holiday/preview edition, no fresh data | VIX futures term structure with event annotations | 5 Derivatives |

Three charts is real pressure on a four-page document. It is the first thing
to drop when the page budget is tight — before any prose, after sector table
rows with no news. No chart may duplicate a table, which applies to the third
one most of all.
