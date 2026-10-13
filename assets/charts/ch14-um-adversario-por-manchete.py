"""ch14-um-adversario-por-manchete: one opponent per headline.

Content: book/pt/ch14.md, "Pra que ele serve, afinal". Data: blog post
2026/10/03 entendendo-o-hype-do-jev-pra-que-serve (Paulo Câmara's essay, numbers
recalculated from TypeSafe's public eval table, evals.typesafe.ai):
- 444.6x: cost of Opus 5, the most expensive model on TypeSafe's panel, / Jev cost
  (the homepage headline);
- ~8x: against Luna, the cheap model with similar agreement;
- ~4x: against a non-reasoning LLM, independent tests (jev-decision-bench, 49 tasks).
Log scale, because 444.6 and 4 do not fit on one linear axis.

Usage: uv run --with matplotlib python -I assets/charts/ch14-um-adversario-por-manchete.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FixedLocator, NullLocator

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"bars": ["contra o modelo mais caro\nda tabela da empresa", "contra um modelo barato\nde acerto parecido",
                    "contra um LLM sem raciocínio,\ntestes independentes"],
           "vals": ["444,6x", "~8x", "~4x"], "axis": "quantas vezes mais barato (escala logarítmica)",
           "headline": "a manchete"},
    "en": {"bars": ["against the most expensive\nmodel in the company's table", "against a cheap model\nwith similar accuracy",
                    "against a non-reasoning LLM,\nindependent tests"],
           "vals": ["444.6x", "~8x", "~4x"], "axis": "how many times cheaper (log scale)",
           "headline": "the headline"},
}[LANG]

VALS = [444.6, 8, 4]

fig, ax = plt.subplots(figsize=(6.4, 3.3), dpi=300)
fig.patch.set_facecolor(PAPER); ax.set_facecolor(PAPER)
ys = [2, 1, 0]
for y, v, i in zip(ys, VALS, range(3)):
    ax.barh(y, v - 1, left=1, height=0.58, color=AMBER if i == 0 else NAVY, edgecolor=INK, linewidth=1.2, zorder=3,
            hatch=None)
    ax.text(v * 1.15, y, L["vals"][i], ha="left", va="center", fontsize=13,
            fontweight="semibold" if i == 0 else "normal")
ax.text(444.6 * 1.12, 2 - 0.42, L["headline"], ha="left", va="center", fontsize=10, style="italic",
        color="#5E636C")
ax.set_xscale("log")
ax.set_xlim(1, 2500)
ax.set_ylim(-0.6, 2.6)
ax.xaxis.set_major_locator(FixedLocator([1, 10, 100, 1000]))
ax.xaxis.set_minor_locator(NullLocator())
ax.set_xticklabels(["1x", "10x", "100x", "1.000x" if LANG == "pt" else "1,000x"], fontsize=10.5)
ax.set_yticks(ys)
ax.set_yticklabels(L["bars"], fontsize=11, linespacing=1.1)
ax.tick_params(axis="y", length=0, pad=8)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(INK); ax.spines[s].set_linewidth(1.2)
ax.grid(axis="x", color="#D8D2C4", lw=0.7, zorder=0)
ax.set_xlabel(L["axis"], fontsize=11, labelpad=6)
fig.subplots_adjust(left=0.37, right=0.97, top=0.96, bottom=0.2)

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch14-um-adversario-por-manchete.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
