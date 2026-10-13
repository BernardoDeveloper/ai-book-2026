"""ch08-regras-vs-modelo: hand-written filters vs. one pre-trained model.

Content: book/pt/ch08.md, "A coisa mais parecida com um balão", "A conta da versão 0.1"
and "A pergunta do primeiro dia" (source post 2026/03/05
meu-primeiro-fracasso-com-vibe-code-e-como-consertei-frank-yomik): seven layers of
hand-written filters, each added after a specific error, still let faces through as
balloons; a detector trained on about 11 thousand comic images (ogkalu) finds the
balloons and leaves faces alone.

Drawn with matplotlib (generic shapes, no real manga art). Usage:
  uv run --with matplotlib python -I assets/charts/ch08-regras-vs-modelo.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Ellipse, Rectangle, Arc, Polygon

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"rules": "7 filtros escritos à mão", "q": "balão?", "model": "modelo treinado\ncom 11 mil imagens",
           "found": "balões encontrados", "left": "regras", "right": "modelo"},
    "en": {"rules": "7 hand-written filters", "q": "balloon?", "model": "model trained\non 11 thousand images",
           "found": "balloons found", "left": "rules", "right": "model"},
}[LANG]

W, H = 6.4, 4.6
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

def arrow(p, q, lw=1.6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=INK, lw=lw,
                                 zorder=2, shrinkA=0, shrinkB=0))

def face(cx, cy, r, z=4):
    ax.add_patch(Circle((cx, cy), r, fc=PAPER, ec=INK, lw=1.2, zorder=z))
    ax.add_patch(Arc((cx, cy + r * 0.15), 2.1 * r, 2.0 * r, theta1=10, theta2=170, ec=INK, lw=2.4, zorder=z + 0.1))  # hair
    for dx in (-0.35, 0.35):
        ax.add_patch(Circle((cx + dx * r, cy - 0.05 * r), 0.11 * r, fc=INK, ec="none", zorder=z + 0.1))
    ax.add_patch(Arc((cx, cy - 0.35 * r), 0.5 * r, 0.25 * r, theta1=200, theta2=340, ec=INK, lw=1.0, zorder=z + 0.1))

def page(x, y, w, h, marked=False):
    """A generic comic page: two panels, one speech balloon, one face."""
    ax.add_patch(Rectangle((x, y), w, h, fc=PAPER, ec=INK, lw=1.4, zorder=3))
    ax.plot([x + 0.06, x + w - 0.06], [y + h * 0.52] * 2, color=INK, lw=1.0, zorder=3.1)
    ax.plot([x + w * 0.5] * 2, [y + 0.06, y + h * 0.52 - 0.04], color=INK, lw=1.0, zorder=3.1)
    bx, by, bw, bh = x + w * 0.7, y + h * 0.76, w * 0.42, h * 0.24
    ax.add_patch(Ellipse((bx, by), bw, bh, fc=PAPER, ec=INK, lw=1.1, zorder=3.2))
    for i, frac in enumerate((0.55, 0.4)):
        ax.plot([bx - bw * frac / 2, bx + bw * frac / 2], [by + 0.035 - i * 0.07] * 2, color=INK, lw=0.9, zorder=3.3)
    face(x + w * 0.24, y + h * 0.75, h * 0.12, z=3.2)
    bx2, by2 = x + w * 0.74, y + h * 0.27
    ax.add_patch(Ellipse((bx2, by2), w * 0.36, h * 0.2, fc=PAPER, ec=INK, lw=1.1, zorder=3.2))
    ax.plot([bx2 - 0.1, bx2 + 0.1], [by2, by2], color=INK, lw=0.9, zorder=3.3)
    if marked:
        for (cx, cy, ww, hh) in [(bx, by, bw, bh), (bx2, by2, w * 0.36, h * 0.2)]:
            ax.add_patch(Rectangle((cx - ww / 2 - 0.03, cy - hh / 2 - 0.03), ww + 0.06, hh + 0.06, fc="none",
                                   ec=AMBER, lw=2.4, zorder=3.4))

# ---------- left: stacked filters ----------
lx = 1.38  # centre of the left column
ax.text(lx, H - 0.22, L["left"], ha="center", va="center", fontsize=13.5, fontweight="semibold")
page(lx - 0.48, H - 1.42, 0.96, 1.0)
arrow((lx, H - 1.46), (lx, H - 1.68))
top = H - 1.78
fw, fh, gap = 2.1, 0.15, 0.085
for i in range(7):
    y = top - i * (fh + gap) - fh
    ax.add_patch(FancyBboxPatch((lx - fw / 2, y), fw, fh, boxstyle="round,pad=0,rounding_size=0.04",
                                fc=GRAY, ec=INK, lw=1.0, zorder=3))
    for k in range(9):  # sieve holes
        ax.add_patch(Circle((lx - fw / 2 + 0.17 + k * 0.22, y + fh / 2), 0.035, fc=PAPER, ec="none", zorder=3.1))
    px = lx - fw / 2 + 0.3 + ((i * 0.83) % 1.5)  # one patch per filter
    ax.add_patch(Rectangle((px, y - 0.03), 0.2, fh + 0.06, fc=SAND, ec=INK, lw=0.9, zorder=3.2,
                           angle=(-8 if i % 2 else 8)))
bottom = top - 7 * (fh + gap) + gap
ax.plot([lx + fw / 2 + 0.1, lx + fw / 2 + 0.16, lx + fw / 2 + 0.16, lx + fw / 2 + 0.1],
        [top, top, bottom, bottom], color=INK, lw=1.0)
ax.text(lx + fw / 2 + 0.24, (top + bottom) / 2, L["rules"].replace(" escritos", "\nescritos"), ha="left",
        va="center", fontsize=11.5, rotation=0)
# a face slips through the last filter
fy = bottom - 0.62
ax.add_patch(FancyArrowPatch((lx - 0.55, bottom - 0.03), (lx - 0.55, fy + 0.36), arrowstyle="-|>,head_length=5,head_width=3",
                             color=INK, lw=1.2, linestyle=(0, (3, 2)), zorder=2, shrinkA=0, shrinkB=0))
face(lx - 0.55, fy, 0.24)
ax.add_patch(Rectangle((lx - 0.55 - 0.32, fy - 0.3), 0.64, 0.64, fc="none", ec=AMBER, lw=2.4, linestyle=(0, (3, 2)), zorder=5))
ax.text(lx - 0.12, fy, L["q"], ha="left", va="center", fontsize=13, fontweight="semibold")

# divider
ax.plot([4.08, 4.08], [0.3, H - 0.3], color=GRAY, lw=0.8, linestyle=(0, (2, 3)))

# ---------- right: one model ----------
rx = 5.25
ax.text(rx, H - 0.22, L["right"], ha="center", va="center", fontsize=13.5, fontweight="semibold")
page(rx - 0.48, H - 1.42, 0.96, 1.0)
arrow((rx, H - 1.46), (rx, H - 1.68))
ax.add_patch(FancyBboxPatch((rx - 1.05, H - 2.62), 2.1, 0.9, boxstyle="round,pad=0,rounding_size=0.08",
                            fc=NAVY, ec=INK, lw=1.4, zorder=3))
ax.text(rx, H - 2.17, L["model"], ha="center", va="center", fontsize=12, color=PAPER, zorder=4, linespacing=1.15)
arrow((rx, H - 2.66), (rx, H - 2.88))
page(rx - 0.48, H - 3.95, 0.96, 1.0, marked=True)
ax.text(rx, H - 4.18, L["found"], ha="center", va="center", fontsize=12, fontweight="semibold")

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch08-regras-vs-modelo.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
