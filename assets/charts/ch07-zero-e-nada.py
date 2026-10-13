"""ch07-zero-e-nada: an empty field ("not available") vs. a measured zero.

Content: book/pt/ch07.md, "Zero e nada" (source post 2026/03/04
eu-fiz-um-sistema-de-data-mining-pra-minha-namorada-influencer-dicas-e-truques):
one network does not report shares, the field stays empty, and the model read the
empty field as zero and concluded nobody shared her posts. The fix: say "dado não
disponível" for empty fields and report zeros normally.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch07-zero-e-nada.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER, RUST = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4", "#B5523B"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"post": "post", "field": "compartilhamentos", "na": "dado não disponível", "measured": "medido",
           "note": "a fonte não informa este número", "wrong": "“ninguém compartilha seus posts”",
           "read0": "lido como zero"},
    "en": {"post": "post", "field": "shares", "na": "data not available", "measured": "measured",
           "note": "the source doesn't report this number", "wrong": "“nobody shares your posts”",
           "read0": "read as zero"},
}[LANG]

W, H = 6.4, 4.2
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

def rbox(x, y, w, h, fill, ec=INK, lw=1.4, r=0.07, ls="-", z=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fill, ec=ec,
                                lw=lw, linestyle=ls, zorder=z))

def card(x, y, w, h, empty):
    rbox(x, y, w, h, SAND)
    rbox(x, y + h - 0.38, w, 0.38, NAVY)  # header band
    ax.add_patch(FancyBboxPatch((x + 0.01, y + h - 0.38), w - 0.02, 0.1, boxstyle="square,pad=0", fc=NAVY, ec="none", zorder=3.1))
    ax.text(x + 0.18, y + h - 0.19, L["post"], ha="left", va="center", fontsize=12, color=PAPER, fontweight="semibold", zorder=4)
    fy = y + h - 0.82
    ax.text(x + 0.18, fy, L["field"], ha="left", va="center", fontsize=12, zorder=4)
    vx = x + w - 0.68
    rbox(vx, fy - 0.24, 0.5, 0.48, PAPER, ls=(0, (3, 2)) if empty else "-", lw=1.3, z=4)
    if empty:
        ax.text(vx + 0.25, fy, "?", ha="center", va="center", fontsize=17, color=GRAY, fontweight="semibold", zorder=5)
        tag, tagc, fg = L["na"], GRAY, PAPER
    else:
        ax.text(vx + 0.25, fy, "0", ha="center", va="center", fontsize=17, fontweight="semibold", zorder=5)
        tag, tagc, fg = L["measured"], TEAL, PAPER
    ty = fy - 0.58
    tw = 0.3 + 0.088 * len(tag) + (0.32 if not empty else 0)
    rbox(x + w - 0.18 - tw, ty - 0.17, tw, 0.34, tagc, r=0.17, lw=1.1, z=4)
    ax.text(x + w - 0.18 - tw / 2 + (0.16 if not empty else 0), ty, tag, ha="center", va="center", fontsize=11.5, color=fg, zorder=5)
    if not empty:  # check mark
        cx0 = x + w - 0.18 - tw + 0.17
        ax.plot([cx0, cx0 + 0.07, cx0 + 0.21], [ty, ty - 0.08, ty + 0.09], color=PAPER, lw=1.8, zorder=5,
                solid_capstyle="round", solid_joinstyle="round")
    return fy

h = 2.05
fy = card(0.25, 2.05, 2.85, h, empty=True)
ax.text(0.25 + 1.425, 2.05 + 0.24, L["note"], ha="center", va="center", fontsize=10.5, style="italic", zorder=5)
card(3.3, 2.05, 2.85, h, empty=False)

# chatbot + wrong conclusion
bx, by = 0.75, 0.75
rbox(bx - 0.32, by - 0.28, 0.64, 0.56, GRAY, r=0.12)
for dx in (-0.13, 0.13):
    ax.add_patch(Circle((bx + dx, by + 0.03), 0.06, fc=PAPER, ec="none", zorder=4))
ax.plot([bx, bx], [by + 0.28, by + 0.42], color=INK, lw=1.4, zorder=3)
ax.add_patch(Circle((bx, by + 0.45), 0.05, fc=INK, zorder=3))
# balloon
x0, y0, w, hh = 1.4, 0.4, 4.3, 0.66
ax.add_patch(Polygon([(x0 + 0.05, y0 + 0.22), (x0 + 0.05, y0 + 0.48), (x0 - 0.25, y0 + 0.3)], closed=True,
                     fc=PAPER, ec=INK, lw=1.3, zorder=2.9))
rbox(x0, y0, w, hh, PAPER, r=0.18, lw=1.3)
ax.add_patch(Polygon([(x0 + 0.08, y0 + 0.23), (x0 + 0.08, y0 + 0.47), (x0 - 0.03, y0 + 0.3)], closed=True,
                     fc=PAPER, ec="none", zorder=3.5))
ax.text(x0 + w / 2, y0 + hh / 2, L["wrong"], ha="center", va="center", fontsize=12.5, zorder=4)
ax.plot([x0 + 0.62, x0 + w - 0.62], [y0 + hh / 2 - 0.035, y0 + hh / 2 - 0.035], color=RUST, lw=1.7, zorder=5,
        solid_capstyle="round")
# dashed arrow from the empty field to the wrong conclusion
ax.add_patch(FancyArrowPatch((2.25, 2.02), (2.25, y0 + hh + 0.04), arrowstyle="-|>,head_length=6,head_width=3.5",
                             color=INK, lw=1.5, linestyle=(0, (4, 3)), zorder=2, shrinkA=0, shrinkB=0))
ax.text(2.4, (2.02 + y0 + hh) / 2, L["read0"], ha="left", va="center", fontsize=11.5, style="italic")

out = ROOT / "assets" / "figures" / "ch07-zero-e-nada.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
