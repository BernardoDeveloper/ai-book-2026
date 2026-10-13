"""ch04-duas-perguntas: same article, two questions, opposite answers.

Data: none. Schematic of book/pt/ch04.md (opening): a made-up story saying that
three cups of coffee a day protect memory. Asked "quais são os problemas desta
reportagem?", the chatbot finds problems (small sample, correlation treated as
cause, conclusion bigger than the study); asked "esta reportagem está correta?",
it finds merits (praises the source, the study was published, other research
points the same way). Fictional headline, no real outlet.

Usage: uv run --with matplotlib python -I assets/charts/ch04-duas-perguntas.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER, RUST = ("#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B",
                                                   "#E9DFC9", "#FBF9F4", "#B5523B")
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK})

L = {
    "pt": {"mesma": "a mesma reportagem", "head": "Três xícaras de café\npor dia protegem a memória",
           "q1": "quais são os problemas?", "q2": "está correta?", "crit": "críticas", "elog": "elogios",
           "c": ["amostra pequena", "correlação vira causa", "conclusão exagerada"],
           "e": ["fonte confiável", "estudo publicado", "outros estudos concordam"]},
    "en": {"mesma": "the same story", "head": "Three cups of coffee a day\nprotect your memory",
           "q1": "what are the problems?", "q2": "is it correct?", "crit": "criticism", "elog": "praise",
           "c": ["small sample", "correlation as cause", "overstated conclusion"],
           "e": ["reliable source", "published study", "other studies agree"]},
}[LANG]

fig, ax = plt.subplots(figsize=(6.6, 4.5), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 12)
ax.set_ylim(0.25, 8.4)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)


def box(x, y, w, h, fc, lw=1.6, r=0.18, z=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=INK, lw=lw,
                                zorder=z))


def cross(x, y, s=0.16):
    for d in (1, -1):
        ax.plot([x - s, x + s], [y - s * d, y + s * d], color=RUST, lw=2.6, solid_capstyle="round", zorder=6)


def check(x, y, s=0.17):
    ax.plot([x - s, x - s * 0.25, x + s * 1.1], [y, y - s * 0.8, y + s * 0.9], color=TEAL, lw=2.6,
            solid_capstyle="round", solid_joinstyle="round", zorder=6)


# the article
AX, AY, AW, AH = 3.9, 5.2, 4.2, 2.55
box(AX, AY, AW, AH, PAPER, lw=1.8)
ax.text(AX + 0.25, AY + AH - 0.25, L["head"], ha="left", va="top", fontsize=10, fontweight="semibold",
        linespacing=1.2, zorder=5)
for i in range(4):
    ax.plot([AX + 0.25, AX + AW - (0.25 if i % 3 else 0.9)], [AY + 1.2 - i * 0.27] * 2, color=GRAY, lw=1.6, zorder=4)
ax.text(AX + AW / 2, AY + AH + 0.2, L["mesma"], ha="center", va="bottom", fontsize=12, style="italic")

# two questions and two answers
for side, q, title, items, color, mark in ((-1, L["q1"], L["crit"], L["c"], RUST, cross),
                                          (1, L["q2"], L["elog"], L["e"], TEAL, check)):
    cx = 6 + side * 3.3
    # question typed in a chat box
    qw = 4.0 if side < 0 else 2.6
    box(cx - qw / 2, 4.05, qw, 0.62, "white", lw=1.3, r=0.3, z=4)
    ax.text(cx, 4.36, q, ha="center", va="center", fontsize=11, zorder=5)
    ax.add_patch(FancyArrowPatch((6 + side * 1.5, AY - 0.02), (cx, 4.72), arrowstyle="-|>", mutation_scale=16,
                                 lw=2.0, color=INK, connectionstyle=f"arc3,rad={0.18 * side}", shrinkA=0, shrinkB=0,
                                 zorder=3))
    ax.add_patch(FancyArrowPatch((cx, 4.0), (cx, 3.45), arrowstyle="-|>", mutation_scale=16, lw=2.0, color=INK,
                                 shrinkA=0, shrinkB=0, zorder=3))
    # answer bubble
    bx, bw = cx - 2.5, 5.0
    box(bx, 0.45, bw, 2.95, PAPER, lw=1.8)
    box(bx + 0.25, 2.65, 1.85, 0.5, color, lw=1.2, r=0.12, z=4)
    ax.text(bx + 0.25 + 0.925, 2.9, title, ha="center", va="center", fontsize=11.5, fontweight="semibold",
            color=PAPER, zorder=5)
    for i, it in enumerate(items):
        y = 2.15 - i * 0.6
        mark(bx + 0.5, y)
        ax.text(bx + 0.9, y, it, ha="left", va="center", fontsize=10.5, zorder=5)

buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.
out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch04-duas-perguntas.png"
out.parent.mkdir(parents=True, exist_ok=True)
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
