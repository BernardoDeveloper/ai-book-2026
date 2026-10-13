"""ch10-fosso: the moat moved — conceptual, not to scale, no numbers.

Content: book/pt/ch10.md, "A morte da startup fácil" and "O que o agente não fez por
mim" (source post 2026/03/05 37-dias-de-imersão-em-vibe-coding-conclusão-quanto-a-
modelos-de-negócio): in 2026 the cost of building software collapsed and code stopped
being a moat ("esse fosso secou"), while the cost of training models and gathering
exclusive data kept rising (Epoch AI: ~2.4x a year for frontier training since 2016,
cited in the chapter as [@cottier2024rising]). The curves are illustrative shapes only,
deliberately unlabelled on the y axis.

Usage: uv run --with matplotlib python -I assets/charts/ch10-fosso.py pt
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon, Rectangle, Ellipse, Wedge

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"code": "custo de escrever código", "train": "custo de treinar modelos\ne reunir dados exclusivos",
           "time": "tempo", "cost": "custo", "dry": "fosso seco", "full": "fosso cheio"},
    "en": {"code": "cost of writing code", "train": "cost of training models\nand gathering exclusive data",
           "time": "time", "cost": "cost", "dry": "dry moat", "full": "full moat"},
}[LANG]

W, H = 6.4, 4.2
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0.07, 0.1, 0.9, 0.86])
ax.set_facecolor(PAPER)
ax.set_xlim(0, 10.3); ax.set_ylim(0, 10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_linewidth(1.4); ax.spines[s].set_color(INK)
ax.set_xticks([]); ax.set_yticks([])
ax.plot(10.3, 0, ">", color=INK, ms=7, clip_on=False, transform=ax.transData)
ax.plot(0, 10, "^", color=INK, ms=7, clip_on=False)
ax.set_xlabel(L["time"], fontsize=12, loc="right", labelpad=4)
ax.set_ylabel(L["cost"], fontsize=12, loc="top", labelpad=4)

x = np.linspace(0.2, 9.6, 200)
code = 6.0 * np.exp(-0.42 * x) + 0.35
train = 0.75 * np.exp(0.255 * x)
ax.plot(x, code, color=NAVY, lw=2.6, linestyle=(0, (5, 2.5)), solid_capstyle="round")
ax.plot(x, train, color=TEAL, lw=2.8, solid_capstyle="round")
ax.text(0.75, 6.05, L["code"], fontsize=12, ha="left", va="center")
ax.text(3.2, 7.4, L["train"], fontsize=12, ha="left", va="center", linespacing=1.15)

def castle(cx, base, s, full):
    """Small castle on a mound with a moat; drawn in data coords (aspect corrected)."""
    k = (10.3 / 10) * (0.86 * H) / (0.9 * W)  # x units per y unit, to keep shapes square
    def P(dx, dy):
        return (cx + dx * s * k, base + dy * s)
    # moat
    if full:
        ax.add_patch(Ellipse(P(0, 0.05), 3.0 * s * k, 0.55 * s, fc=TEAL, ec=INK, lw=1.2, zorder=3))
    else:
        ax.add_patch(Ellipse(P(0, 0.05), 3.0 * s * k, 0.55 * s, fc=SAND, ec=INK, lw=1.2, linestyle=(0, (3, 2)), zorder=3))
    # island + walls with battlements
    ax.add_patch(Ellipse(P(0, 0.12), 1.7 * s * k, 0.3 * s, fc=SAND, ec=INK, lw=1.2, zorder=3.2))
    pts = [P(-0.6, 0.15), P(-0.6, 1.05)]
    for i in range(5):
        x0 = -0.6 + i * 0.24
        pts += [P(x0, 1.2), P(x0 + 0.12, 1.2), P(x0 + 0.12, 1.05), P(x0 + 0.24, 1.05)]
    pts[-1] = P(0.6, 1.05)
    pts += [P(0.6, 1.2), P(0.6, 0.15)]
    ax.add_patch(Polygon(pts, closed=True, fc=PAPER, ec=INK, lw=1.3, zorder=3.3, joinstyle="round"))
    ax.add_patch(Rectangle(P(-0.13, 0.15), 0.26 * s * k, 0.38 * s, fc=INK, ec=INK, zorder=3.4))

castle(8.9, 1.25, 1.15, full=False)
ax.text(7.6, 1.3, L["dry"], ha="right", va="center", fontsize=11.5, style="italic")
castle(8.3, 8.25, 0.95, full=True)

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch10-fosso.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
