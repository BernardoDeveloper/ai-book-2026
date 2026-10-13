"""ch01-proximo-token: one turn of next-token prediction, and the loop.

Data: none. Schematic of book/pt/ch01.md ("Uma peça de cada vez"): the model
looks at the whole text, computes the chance of every possible next piece,
draws one among the few most likely, appends it and starts again with the
longer text. Bar lengths are illustrative, not real model probabilities.

Usage: uv run --with matplotlib python -I assets/charts/ch01-proximo-token.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
MUTED = "#5E636C"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK})

L = {
    "pt": {"prompt": "O gato subiu no", "s1": "olha o texto todo", "s2": "calcula as chances",
           "s3": "sorteia entre\nos mais prováveis", "s4": "cola no fim\ne repete",
           "cands": ["telhado", "muro", "sofá", "…", "…"], "next": ["e", "quando", "de"]},
    "en": {"prompt": "The cat sat on the", "s1": "looks at the whole text", "s2": "computes the chances",
           "s3": "draws among\nthe most likely", "s4": "appends it\nand repeats",
           "cands": ["roof", "wall", "sofa", "…", "…"], "next": ["and", "when", "to"]},
}[LANG]
PROBS = [2.5, 1.0, 0.68, 0.12, 0.06]  # illustrative bar lengths

fig, ax = plt.subplots(figsize=(6.8, 4.3), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 12)
ax.set_ylim(0.5, 6.85)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)


def badge(x, y, n):
    ax.add_patch(Circle((x, y), 0.22, fc=INK, ec=INK, zorder=6))
    ax.text(x, y - 0.01, str(n), ha="center", va="center", color=PAPER, fontsize=10, fontweight="semibold", zorder=7)


def arrow(p, q, color=INK, lw=1.4, rad=0.0, ms=12, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=3))



def fit_text(t, max_w, min_size=7.0):
    """Shrink a text artist until it fits max_w (data units). Labels change
    length between languages; the layout stays fixed and only the type size
    gives way, never below min_size (house minimum ~7 pt)."""
    fig.canvas.draw()
    inv = ax.transData.inverted()
    while t.get_fontsize() > min_size:
        bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
        (x0, _), (x1, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        if x1 - x0 <= max_w:
            break
        t.set_fontsize(t.get_fontsize() - 0.25)
    return t

# 1 - the prompt
PY = 4.25
ax.add_patch(FancyBboxPatch((0.15, PY - 0.42), 2.55, 0.84, boxstyle="round,pad=0,rounding_size=0.12",
                            fc=SAND, ec=INK, lw=1.5, zorder=2))
fit_text(ax.text(1.425, PY, L["prompt"], ha="center", va="center", fontsize=12, fontweight="semibold", zorder=3), 2.55 - 0.3)
badge(0.32, PY + 0.85, 1)
ax.text(0.62, PY + 0.85, L["s1"], ha="left", va="center", fontsize=11.5)

# 2 - candidates with chance bars
ys = [5.65, 4.95, 4.25, 3.6, 3.05]
WX, BX = 4.8, 4.95
for i, (w, p, y) in enumerate(zip(L["cands"], PROBS, ys)):
    top = i < 3
    arrow((2.72, PY), (3.4, y), color=INK if top else GRAY, lw=1.2 if top else 0.8, ms=9)
    ax.text(WX, y, w, ha="right", va="center", fontsize=12 if top else 11, color=INK if top else MUTED,
            fontweight="semibold" if i == 0 else "normal")
    ax.add_patch(FancyBboxPatch((BX, y - 0.2), p, 0.4, boxstyle="round,pad=0,rounding_size=0.05",
                                fc=AMBER if i == 0 else (NAVY if top else GRAY), ec=INK, lw=1.0, zorder=2))
badge(3.75, 6.45, 2)
ax.text(4.05, 6.45, L["s2"], ha="left", va="center", fontsize=11.5)

# 3 - bracket around the top three + die
bx = 7.7
ax.plot([bx, bx + 0.18, bx + 0.18, bx], [ys[0] + 0.28, ys[0] + 0.28, ys[2] - 0.28, ys[2] - 0.28], color=INK, lw=1.3,
        solid_capstyle="round", solid_joinstyle="round")
DX, DY, DS = 8.15, ys[1] - 0.33, 0.66  # die (lower-left corner, size)
ax.add_patch(FancyBboxPatch((DX, DY), DS, DS, boxstyle="round,pad=0,rounding_size=0.1", fc=PAPER, ec=INK, lw=1.6,
                            zorder=4))
for px, py in ((0.25, 0.75), (0.5, 0.5), (0.75, 0.25), (0.25, 0.25), (0.75, 0.75)):
    ax.add_patch(Circle((DX + px * DS, DY + py * DS), 0.055, fc=INK, ec="none", zorder=5))
badge(9.2, ys[1], 3)
ax.text(9.5, ys[1], L["s3"], ha="left", va="center", fontsize=11.5, linespacing=1.25)

# 4 - the chosen piece is appended
RY = 1.35
x0 = 1.2
t1 = ax.text(x0 + 0.25, RY, L["prompt"], ha="left", va="center", fontsize=12, fontweight="semibold", zorder=3)
fig.canvas.draw()
bb = t1.get_window_extent().transformed(ax.transData.inverted())
chip_x = bb.x1 + 0.15
t2 = ax.text(chip_x + 0.12, RY, L["cands"][0], ha="left", va="center", fontsize=12, fontweight="semibold", zorder=4)
bb2 = t2.get_window_extent().transformed(ax.transData.inverted())
ax.add_patch(FancyBboxPatch((chip_x, RY - 0.27), bb2.x1 - chip_x + 0.12, 0.54, boxstyle="round,pad=0,rounding_size=0.08",
                            fc=AMBER, ec=INK, lw=1.0, zorder=3))
RX1 = bb2.x1 + 0.3
ax.add_patch(FancyBboxPatch((x0, RY - 0.42), RX1 - x0, 0.84, boxstyle="round,pad=0,rounding_size=0.12",
                            fc=SAND, ec=INK, lw=1.5, zorder=2))
arrow((DX + DS / 2, DY - 0.08), ((chip_x + bb2.x1) / 2 + 0.3, RY + 0.47), rad=-0.25, lw=1.6, ms=14)
badge(8.6, 2.6, 4)
ax.text(8.9, 2.6, L["s4"], ha="left", va="center", fontsize=11.5, linespacing=1.25)

# loop back to step 1 with the longer text
arrow((x0 - 0.05, RY), (0.6, PY - 0.47), rad=-0.35, lw=1.6, ms=14)

# the path keeps branching (faded)
for w, y, ln in zip(L["next"], (RY + 0.55, RY, RY - 0.55), (0.55, 0.3, 0.18)):
    arrow((RX1 + 0.05, RY), (RX1 + 0.55, y), color=GRAY, lw=0.8, ms=8)
    ax.text(RX1 + 0.62, y, w, ha="left", va="center", fontsize=10, color=MUTED)

buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.
out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch01-proximo-token.png"
out.parent.mkdir(parents=True, exist_ok=True)
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
