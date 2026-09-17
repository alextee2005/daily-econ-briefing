"""Generate the briefing's two charts. Edit MOVERS and PANEL2 below, then run.

Sizing/dpi match the briefing's CSS baseline — changing them will throw off the
page budget. Chart 1 is always single-stock movers; see references/format.md for
how to pick chart 2 (the default here is the SPDR sector-ETF proxy).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 9.6
plt.rcParams["font.family"] = "DejaVu Serif"

POS, NEG, GRID, TXT = "#2f6f4f", "#9e2a2b", "#d9d9d9", "#1a1a1a"

# --- edit these two blocks each edition -------------------------------------
MOVERS = [("ENVA", -23.4), ("PLAY", -19.0), ("AXON", -9.8),
          ("APTV", -2.1), ("COHR", 1.8), ("ETSY", 2.3), ("RVTY", 5.6)]
MOVERS_TITLE = "Single-stock movers — Tuesday 15 Sept 2026"
MOVERS_XLABEL = "% change, Tuesday 15 Sept close [1]"

PANEL2 = [("Energy (XLE)", 2.17), ("Materials (XLB)", 0.48),
          ("Real Estate (XLRE)", -0.12), ("Health Care (XLV)", -0.05),
          ("Technology (XLK)", -0.29), ("Financials (XLF)", -0.32),
          ("Industrials (XLI)", -0.64), ("Cons. Staples (XLP)", -0.82),
          ("Comm. Svcs (XLC)", -0.90), ("Utilities (XLU)", -1.20),
          ("Cons. Discretionary (XLY)", -1.75)]
PANEL2_TITLE = "Sector rotation — Tuesday 15 Sept 2026"
PANEL2_XLABEL = "% change, SPDR sector ETF proxy [2]"
# ----------------------------------------------------------------------------


def barh(rows, title, xlabel, outfile, figsize, tick_fs=8.6, pad_frac=0.12,
         fmt="{:+.1f}%", cap=None):
    labels = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    # Cap an order-of-magnitude outlier so the rest of the bars stay readable.
    plot_vals = [max(min(v, cap), -cap) for v in vals] if cap else vals
    colors = [NEG if v < 0 else POS for v in vals]

    fig, ax = plt.subplots(figsize=figsize, dpi=210)
    bars = ax.barh(labels, plot_vals, color=colors, height=0.62, zorder=3)
    ax.axvline(0, color="#666666", linewidth=0.8, zorder=2)
    ax.set_xlabel(xlabel, fontsize=8.2, color=TXT)
    ax.set_title(title, fontsize=9.6, color=TXT, loc="left", pad=4)
    ax.grid(axis="x", color=GRID, linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#999999")
    ax.tick_params(axis="y", length=0, labelsize=tick_fs)
    ax.tick_params(axis="x", labelsize=7.6, colors="#444444")

    span = max(abs(min(plot_vals)), abs(max(plot_vals)))
    off = span * pad_frac * 0.5
    for bar, v, pv in zip(bars, vals, plot_vals):
        label = fmt.format(v) + (" (capped)" if cap and abs(v) > cap else "")
        ax.text(pv + (off if pv >= 0 else -off),
                bar.get_y() + bar.get_height() / 2, label,
                va="center", ha="left" if pv >= 0 else "right",
                fontsize=7.6, color=TXT)
    ax.set_xlim(min(plot_vals) - span * pad_frac, max(plot_vals) + span * pad_frac)
    fig.tight_layout(pad=0.4)
    fig.savefig(outfile, dpi=210, bbox_inches="tight")
    plt.close(fig)
    print("wrote", outfile)


if __name__ == "__main__":
    barh(MOVERS, MOVERS_TITLE, MOVERS_XLABEL, "chart1_movers.png", (9.8, 1.95))
    barh(PANEL2, PANEL2_TITLE, PANEL2_XLABEL, "chart2_panel.png", (9.8, 1.55),
         tick_fs=7.6, fmt="{:+.2f}%")
