"""ch05-iceberg: the part that works vs. the part under water.

Data: book/pt/ch05.md ("Os outros noventa"), from akitaonrails.com
2026/02/01/vibe-code-fiz-um-editor-de-markdown-do-zero-com-claude-code-frankmd-parte-2:
FrankMD's first ten commits took about an hour and a half to "already work";
almost 30 more hours went to the rest (refactoring, which the post calls the
largest part of vibe coding; bug fixes; tests; performance; security checks).
Layer sizes are illustrative; refactoring is drawn largest because the post
says most of the work is refactoring.

Usage: uv run --with matplotlib python -I assets/charts/ch05-iceberg.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Polygon, Rectangle, Circle, Wedge
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK})

L = {
    "pt": {"tip": "já funciona", "layers": ["refatoração", "consertos de bugs", "testes",
                                         "desempenho", "segurança"],
           "h1": "1 hora e meia", "h10": "quase\n30 horas"},
    "en": {"tip": "it already\nworks", "layers": ["refactoring", "bug fixes", "tests",
                                                "performance", "security"],
           "h1": "an hour and a half", "h10": "almost\n30 hours"},
}[LANG]

fig, ax = plt.subplots(figsize=(6.4, 4.9), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 12)
ax.set_ylim(0, 9.2)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)

WATER = 7.0
# water
ax.add_patch(Rectangle((0, 0), 12, WATER, fc=SAND, ec="none", zorder=0))
x = np.linspace(0, 12, 400)
ax.plot(x, WATER + 0.06 * np.sin(x * 5.0), color=INK, lw=1.6, zorder=1)

berg = [(4.4, 7.0), (4.85, 8.05), (5.25, 8.75), (5.75, 8.2), (6.2, 7.0), (8.4, 6.45), (9.55, 5.2), (9.45, 3.5),
        (8.7, 2.0), (7.5, 0.85), (5.7, 0.35), (3.9, 0.55), (2.6, 1.6), (1.85, 3.3), (1.75, 5.1), (2.6, 6.35)]
clip = Polygon(berg, closed=True, transform=ax.transData)

bands = [(WATER, 9.5, AMBER, None, INK)]
edges = [WATER, 4.55, 3.4, 2.35, 1.45, 0.0]
fills = [NAVY, TEAL, NAVY, GRAY, NAVY]
txt = [PAPER, PAPER, PAPER, INK, PAPER]
for i, name in enumerate(L["layers"]):
    bands.append((edges[i + 1], edges[i], fills[i], name, txt[i]))
for lo, hi, fc, name, tc in bands:
    r = Rectangle((0, lo), 12, hi - lo, fc=fc, ec="none", zorder=2)
    ax.add_patch(r)
    r.set_clip_path(clip)
    if lo < WATER:
        ln, = ax.plot([0, 12], [hi, hi], color=PAPER, lw=2.4, zorder=3)
        ln.set_clip_path(clip)
    if name:
        ax.text(5.65, (lo + hi) / 2 + (0.15 if lo > 4 else 0), name, ha="center", va="center", fontsize=12.5,
                fontweight="semibold", color=tc, zorder=4)
ax.add_patch(Polygon(berg, closed=True, fc="none", ec=INK, lw=2.0, joinstyle="round", zorder=5))

ax.text(4.3, 8.1, L["tip"], ha="right", va="center", fontsize=12, fontweight="semibold", linespacing=1.15)


def clock(cx, cy, r, hours, label, beside=False):
    ax.add_patch(Circle((cx, cy), r, fc=PAPER, ec=INK, lw=1.6, zorder=6))
    for k in range(12):
        a = math.radians(90 - k * 30)
        ax.plot([cx + 0.8 * r * math.cos(a), cx + 0.92 * r * math.cos(a)],
                [cy + 0.8 * r * math.sin(a), cy + 0.92 * r * math.sin(a)], color=INK, lw=0.8, zorder=7)
    # filled wedge for the elapsed share of a 12-hour face
    ax.add_patch(Wedge((cx, cy), r * 0.72, 90 - hours * 30, 90, fc=AMBER if hours <= 2 else TEAL, ec=INK, lw=0.8,
                       zorder=7))
    ax.plot([cx, cx], [cy, cy + 0.72 * r], color=INK, lw=1.6, zorder=8, solid_capstyle="round")
    if beside:
        ax.text(cx + r + 0.25, cy, label, ha="left", va="center", fontsize=12, fontweight="semibold")
    else:
        ax.text(cx, cy - r - 0.3, label, ha="center", va="top", fontsize=12, fontweight="semibold")


clock(7.3, 8.1, 0.5, 1.5, L["h1"], beside=True)
clock(10.75, 4.3, 0.62, 12, L["h10"])

buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.
out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch05-iceberg.png"
out.parent.mkdir(parents=True, exist_ok=True)
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
