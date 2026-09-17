# Sourcing playbook

Every figure needs a named, dated source. If it can't be verified, it goes in
Annex A — a plausible-sounding number is worse than an admitted gap.

## The three recurring traps

**Stale-date republishing.** Aggregators routinely serve the prior session's
data under the current date. Verify the session date on every figure, not just
the vendor. A figure that matches the prior close exactly is the tell.

**Snapshot mistaken for close.** Mid-session and pre-close quotes get published
as "the close" by at least one vendor on a regular basis. Multiple real errors
have come from this. Cross-check any close that looks surprising against a
second source, and prefer sources that expose a timestamp.

**Carried-forward assumption.** A fact that was true three editions ago (who
chairs the Fed, when a meeting lands, whether a keynote already happened) is
not evidence. Re-verify from the primary source every run. The prompt's own
framing doesn't count as a source either.

## What works

| Need | Source |
|---|---|
| Index closes | AP "How major US stock indexes fared"; Reuters' *updated* wrap (not the preliminary). Check it's actually indexed for the date — it occasionally doesn't post in time |
| Index closes, fallback | Corroborated secondary source + ETF-proxy triangulation (SPY/DIA/QQQ/IWM vs. their tracked indices). Note QQQ tracks the Nasdaq-100, not the Composite |
| Same-day sector performance | Stockanalysis.com ETF price-history pages for the SPDR sector ETFs (XLE, XLK, XLC, XLY, XLP, XLRE, XLF, XLB, XLI, XLU, XLV) |
| Single-stock closes | Stockanalysis.com history tables, cross-checked against news coverage |
| VIX complex | CBOE's `cdn.cboe.com` delayed-quotes JSON — see below |
| Treasury yields | Trading Economics for secondary-market levels; official H.15 par yields don't post by cutoff |
| LME metals settlement | lme.com directly — this works, unlike most exchange sites |
| Rate-path odds | Kalshi, Polymarket, economist polls, desk notes. Give a range across venues |
| CFTC CoT | cftc.gov — publishes Friday with the prior Tuesday's data |

## The CBOE vol feed

The delayed-quotes JSON endpoint returns VIX, VIX9D, VIX3M, VIX6M, VVIX and
SKEW. It has three observed behaviors and you cannot tell which you got from
whether the endpoint responded:

1. Full clean sweep, every series genuinely fresh (happens occasionally)
2. Thin-series-stale — VIX/VIX3M refresh, the thinner series silently serve a
   prior-session snapshot (most common)
3. Total failure — every series stale

**Check `last_trade_time` on each individual series, every time.** When a series
is stale, fall back to news coverage for at least the headline VIX close and
disclose it as single-sourced. Note that an intraday timestamp is fresh but is
still not a close.

## Reliably unobtainable — mark unavailable rather than hunting

- NYSE/Nasdaq closing breadth (Reuters' final wrap drops the block)
- Dealer gamma (third-party estimates only)
- Official CME FedWatch probabilities — the page blocks fetching; cite
  secondary references and give a range
- Official CME/Comex settlement prices — JS-rendered, no usable data via fetch
- Official Treasury par yields before the cutoff

## Calendar notes

- China CPI/PPI: prints around the 9th–10th monthly
- US import/export prices and industrial production: mid-month, often Mon/Tue —
  confirm on the BLS/Fed schedule rather than assuming they ride with retail sales
- 13F filings: ~May 15, Aug 14, Nov 14, Feb 14 — lead a Monday edition with them
  when the window includes one
- CoT lag: always state it explicitly rather than presenting Tuesday-old
  positioning as current
