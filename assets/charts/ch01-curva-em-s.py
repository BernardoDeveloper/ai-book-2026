"""ch01-curva-em-s: the GPT family on a qualitative S-curve, with training cost.

Data: none. Qualitative sketch of book/pt/ch01.md ("A curva em S"), from
akitaonrails.com 2026/02/08/rant-ia-acabou-com-programadores: GPT-1 (2018) ->
GPT-2 a quantum leap, GPT-2 -> GPT-3 a giant leap, 3 -> 4 smaller, 4 -> 5 barely
noticed, while the cost of each generation keeps rising. Release years: GPT-1
2018, GPT-2 2019, GPT-3 2020, GPT-4 2023, GPT-5 2025. The y axis carries no
numbers on purpose: the shapes are illustrative, not measured.

Usage: uv run --with matplotlib python -I assets/charts/ch01-curva-em-s.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK})

L = {
    "pt": {"cap": "capacidade", "cost": "custo de treino", "infancia": "infância", "subida": "subida rápida",
           "maturidade": "maturidade", "tempo": "tempo", "note": "esquema qualitativo, fora de escala"},
    "en": {"cap": "capability", "cost": "training cost", "infancia": "infancy", "subida": "rapid rise",
           "maturidade": "maturity", "tempo": "time", "note": "qualitative sketch, not to scale"},
}[LANG]

MODELS = [("GPT-1", 2018), ("GPT-2", 2019), ("GPT-3", 2020), ("GPT-4", 2023), ("GPT-5", 2025)]
X0, X1 = 2016.6, 2025.8


def cap(x):  # logistic S, midpoint between GPT-2 and GPT-3
    return 0.06 + 0.84 / (1 + np.exp(-1.55 * (x - 2019.55)))


def cost(x):  # keeps accelerating, never flattens
    return 0.03 + 1.0 * (np.exp(0.62 * (x - X0)) - 1) / (np.exp(0.62 * (2025.7 - X0)) - 1)


fig, ax = plt.subplots(figsize=(6.6, 4.1), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# phase bands
phases = [(X0, 2018.3, L["infancia"]), (2018.3, 2021.6, L["subida"]), (2021.6, X1, L["maturidade"])]
for i, (a, b, name) in enumerate(phases):
    if i == 1:
        ax.axvspan(a, b, color=SAND, zorder=0, lw=0)
    ax.text((a + b) / 2, -0.115, name, ha="center", va="top", fontsize=12, fontweight="semibold",
            transform=ax.get_xaxis_transform())
for b in (2018.3, 2021.6):
    ax.axvline(b, color=GRAY, lw=0.8, ls=(0, (2, 3)), zorder=1)

x = np.linspace(X0, X1, 400)
xc = np.linspace(X0, 2025.62, 400)
ax.plot(xc, cost(xc), color=TEAL, lw=2.4, ls=(0, (6, 3)), solid_capstyle="round", zorder=2)
ax.annotate("", xy=(2025.72, cost(2025.72)), xytext=(2025.55, cost(2025.55)),
            arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.4, mutation_scale=16), zorder=2)
ax.plot(x, cap(x), color=NAVY, lw=3.0, solid_capstyle="round", zorder=3)

for name, yr in MODELS:
    y = cap(yr)
    ax.plot(yr, y, "o", ms=8.5, mfc=AMBER, mec=INK, mew=1.4, zorder=4)
    if yr == 2019:  # above-left would straddle the band edge; below-right keeps it inside the band
        ax.text(yr + 0.14, y - 0.02, name, ha="left", va="top", fontsize=11.5, fontweight="semibold", zorder=5)
    elif yr <= 2020:  # rising part: the curve is below-left, so the label goes above-left
        ax.text(yr - 0.08, y + 0.03, name, ha="right", va="bottom", fontsize=11.5, fontweight="semibold", zorder=5)
    else:
        ax.text(yr, y + 0.05, name, ha="center", va="bottom", fontsize=11.5, fontweight="semibold", zorder=5)

# direct labels on the curves
ax.text(2023.2, cap(2023.2) - 0.06, L["cap"], color=NAVY, fontsize=13, fontweight="semibold", ha="center", va="top")
ax.text(2024.0, 0.5, L["cost"], color=TEAL, fontsize=13, fontweight="semibold", ha="right", va="center")

ax.set_xlim(X0, X1)
ax.set_ylim(0, 1.1)
ax.set_xticks([yr for _, yr in MODELS])
ax.set_xticklabels([str(yr) for _, yr in MODELS], fontsize=10.5, color=INK)
ax.tick_params(axis="x", length=3, color=INK)
ax.set_yticks([])
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(1.3)
    ax.spines[s].set_color(INK)
ax.annotate("", xy=(X1, 0), xytext=(X1 - 0.01, 0), xycoords="data",
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.3, mutation_scale=14), annotation_clip=False)
ax.text(X1 - 0.05, 0.025, L["tempo"], ha="right", va="bottom", fontsize=11.5, style="italic")
ax.text(0.01, 0.99, L["note"], transform=ax.transAxes, ha="left", va="top", fontsize=9.5, style="italic",
        color="#5E636C")

fig.tight_layout()
buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.
out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch01-curva-em-s.png"
out.parent.mkdir(parents=True, exist_ok=True)
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
