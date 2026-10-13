"""ch15-verificar-na-origem: check the destination against the source, not the tool's log.

Content: book/pt/ch15.md, "Quem operou a recuperação" (source post 2026/10/06
desastre-no-meu-nas-como-quase-perdi-90-tb-de-dados): the NAS copy program reported
success, all green, but a 901 GB folder owned by another user (no permission) was
silently skipped; comparing the source inventory with the destination, item by item,
exposed the hole. Generic folders, no product names.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch15-verificar-na-origem.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle, Circle, Arc

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
RUST = "#B5523B"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"left": "relatório da ferramenta", "right": "inventário da origem", "src": "origem",
           "dst": "destino", "ok": "sucesso", "missing": "faltando"},
    "en": {"left": "the tool's report", "right": "source inventory", "src": "source",
           "dst": "destination", "ok": "success", "missing": "missing"},
}[LANG]

W, H = 6.4, 4.6
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

ROWS = [3.3, 2.78, 2.26, 1.74]
LOCKED = 2


def arrow(p, q, lw=1.4, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=5,head_width=3", color=color, lw=lw,
                                 zorder=2, shrinkA=0, shrinkB=0))


def folder(cx, cy, fill=NAVY, ec=INK, ls="-"):
    w, h = 0.56, 0.36
    x, y = cx - w / 2, cy - h / 2
    ax.add_patch(Polygon([(x, y + h), (x, y + h + 0.07), (x + 0.2, y + h + 0.07), (x + 0.25, y + h)], closed=True,
                         fc=fill, ec=ec, lw=1.2, zorder=3, ls=ls, joinstyle="round"))
    ax.add_patch(Rectangle((x, y), w, h, fc=fill, ec=ec, lw=1.2, zorder=3, ls=ls))


def padlock(cx, cy):
    ax.add_patch(Rectangle((cx - 0.08, cy - 0.09), 0.16, 0.12, fc=AMBER, ec=INK, lw=1.0, zorder=5))
    ax.add_patch(Arc((cx, cy + 0.03), 0.11, 0.14, theta1=0, theta2=180, ec=PAPER, lw=1.6, zorder=5))


def check(cx, cy, color=INK, s=1.0, lw=2.0):
    ax.plot([cx - 0.09 * s, cx - 0.02 * s, cx + 0.1 * s], [cy, cy - 0.08 * s, cy + 0.09 * s], color=color, lw=lw,
            solid_capstyle="round", solid_joinstyle="round", zorder=6)


def panel(x0, title):
    pw = 3.05
    ax.add_patch(FancyBboxPatch((x0, 0.1), pw, H - 0.2, boxstyle="round,pad=0,rounding_size=0.1",
                                fc=SAND, ec="none", zorder=0))
    ax.text(x0 + 0.2, H - 0.36, title, ha="left", va="center", fontsize=13.5, fontweight="semibold")
    sx, dx = x0 + 0.72, x0 + 2.3
    ax.text(sx, 3.82, L["src"], ha="center", va="center", fontsize=11.5)
    ax.text(dx, 3.82, L["dst"], ha="center", va="center", fontsize=11.5)
    for i, y in enumerate(ROWS):
        folder(sx, y)
        if i == LOCKED:
            padlock(sx, y - 0.01)
    return sx, dx


# ---- left: the tool only looks at its own report ----
sx, dx = panel(0.12, L["left"])
for i, y in enumerate(ROWS):
    if i != LOCKED:
        arrow((sx + 0.33, y), (dx - 0.33, y))
        folder(dx, y)
# the report card
cx, cy = 0.12 + 3.05 / 2, 0.78
ax.add_patch(FancyBboxPatch((cx - 0.95, cy - 0.36), 1.9, 0.72, boxstyle="round,pad=0,rounding_size=0.07",
                            fc=PAPER, ec=INK, lw=1.4, zorder=3))
ax.add_patch(Circle((cx - 0.5, cy), 0.21, fc=TEAL, ec=INK, lw=1.2, zorder=4))
check(cx - 0.5, cy, color=PAPER, s=1.1, lw=2.4)
ax.text(cx - 0.18, cy, L["ok"], ha="left", va="center", fontsize=13, fontweight="semibold", zorder=4)

# ---- right: compare the source inventory with the destination, item by item ----
sx, dx = panel(3.27, L["right"])
for i, y in enumerate(ROWS):
    if i == LOCKED:
        ax.plot([sx + 0.33, dx - 0.33], [y, y], color=RUST, lw=1.4, ls=(0, (3, 2)), zorder=2)
        folder(dx, y, fill=PAPER, ec=RUST, ls=(0, (3, 2)))
        ax.add_patch(Circle(((sx + dx) / 2, y), 0.15, fc=RUST, ec=INK, lw=1.0, zorder=5))
        m = (sx + dx) / 2
        for s in (1, -1):
            ax.plot([m - 0.06, m + 0.06], [y - 0.06 * s, y + 0.06 * s], color=PAPER, lw=1.8, zorder=6,
                    solid_capstyle="round")
    else:
        ax.plot([sx + 0.33, dx - 0.33], [y, y], color=INK, lw=1.0, ls=(0, (1, 2)), zorder=2)
        folder(dx, y)
        check((sx + dx) / 2, y + 0.02, color=INK, s=0.9, lw=1.8)
ax.add_patch(FancyBboxPatch((cx + 3.15 - 0.95, 0.78 - 0.36), 1.9, 0.72, boxstyle="round,pad=0,rounding_size=0.07",
                            fc=PAPER, ec=RUST, lw=1.8, zorder=3))
ax.text(cx + 3.15, 0.78, L["missing"], ha="center", va="center", fontsize=13, fontweight="semibold",
        color=RUST, zorder=4)

out = ROOT / "assets" / "figures" / "ch15-verificar-na-origem.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
