"""ch09-fatias: a giant file read in slices vs. a small file read whole.

Content: book/pt/ch09.md, "Como o agente lê" (source post 2026/04/20
clean-code-para-agentes-de-ia): "Em abril de 2026, o Claude Code lia por padrão 2 mil
linhas de um arquivo por vez. Um arquivo gigante não entra inteiro; o agente pede
pedaço por pedaço e monta um quadro fragmentado."

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch09-fatias.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"big": "arquivo gigante", "small": "arquivo pequeno", "view": "campo de visão",
           "slice": "2 mil linhas por vez\n(abril de 2026)", "agent": "agente"},
    "en": {"big": "giant file", "small": "small file", "view": "field of view",
           "slice": "2,000 lines at a time\n(April 2026)", "agent": "agent"},
}[LANG]

W, H = 6.4, 4.1
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

def rbox(x, y, w, h, fill, r=0.05, lw=1.2, ls="-", z=3, ec=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fill, ec=ec,
                                lw=lw, linestyle=ls, zorder=z))

def page(x, y, w, h, fill, lines=3, z=3):
    rbox(x, y, w, h, fill, z=z)
    step = h / (lines + 1)
    for i in range(lines):
        frac = (0.8, 0.6, 0.72, 0.5, 0.66)[i % 5]
        yy = y + h - step * (i + 1)
        ax.plot([x + 0.1, x + 0.1 + (w - 0.2) * frac], [yy, yy], color=INK, lw=0.9, zorder=z + 0.1,
                solid_capstyle="round")

def agent(cx, cy, s=1.0):
    rbox(cx - 0.3 * s, cy - 0.26 * s, 0.6 * s, 0.52 * s, GRAY, r=0.11 * s, lw=1.3, z=5)
    for dx in (-0.12, 0.12):
        ax.add_patch(Circle((cx + dx * s, cy + 0.02 * s), 0.055 * s, fc=PAPER, ec="none", zorder=6))
    ax.plot([cx, cx], [cy + 0.26 * s, cy + 0.38 * s], color=INK, lw=1.3, zorder=5)
    ax.add_patch(Circle((cx, cy + 0.41 * s), 0.045 * s, fc=INK, zorder=5))

# ---------- left: giant file in slices ----------
ax.text(1.55, H - 0.2, L["big"], ha="center", va="center", fontsize=13.5, fontweight="semibold")
sx, sw, sh, gap = 0.3, 0.95, 0.34, 0.0
n, pick = 9, 3
top = H - 0.45
ys = [top - (i + 1) * sh for i in range(n)]
rbox(sx, ys[-1], sw, n * sh, PAPER, lw=1.4)  # one long file...
for i, y in enumerate(ys):
    if i == pick:
        ax.add_patch(plt.Rectangle((sx, y), sw, sh, fc=AMBER, ec="none", zorder=3.05))
    for k, frac in enumerate((0.75, 0.5)):
        yy = y + sh * (0.66 - 0.32 * k)
        ax.plot([sx + 0.1, sx + 0.1 + (sw - 0.2) * frac], [yy, yy], color=INK, lw=0.9, zorder=3.1,
                solid_capstyle="round")
    if i:  # ...cut into slices
        ax.plot([sx - 0.08, sx + sw + 0.08], [y + sh, y + sh], color=INK, lw=1.1, linestyle=(0, (3, 2)), zorder=3.2)
# field of view with the agent holding one slice
vx, vy, vw, vh = 1.5, 1.2, 1.5, 1.75
rbox(vx, vy, vw, vh, "none", r=0.1, lw=1.4, ls=(0, (4, 3)), z=2)
ax.text(vx + vw / 2, vy + vh + 0.14, L["view"], ha="center", va="center", fontsize=11.5, style="italic")
page(vx + 0.27, vy + 1.05, sw, sh, AMBER, lines=2, z=4)
agent(vx + vw / 2, vy + 0.45)
ax.add_patch(FancyArrowPatch((sx + sw + 0.03, ys[pick] + sh / 2), (vx + 0.25, vy + 1.05 + sh / 2),
                             arrowstyle="-|>,head_length=6,head_width=3.5", color=INK, lw=1.5,
                             connectionstyle="arc3,rad=-0.2", zorder=2, shrinkA=0, shrinkB=0))
ax.text(vx + vw / 2, vy - 0.42, L["slice"], ha="center", va="center", fontsize=11, linespacing=1.15)

ax.plot([3.35, 3.35], [0.3, H - 0.3], color=GRAY, lw=0.8, linestyle=(0, (2, 3)))

# ---------- right: small file, whole ----------
ax.text(4.85, H - 0.2, L["small"], ha="center", va="center", fontsize=13.5, fontweight="semibold")
vx2, vw2 = 3.95, 1.8
rbox(vx2, vy, vw2, vh, "none", r=0.1, lw=1.4, ls=(0, (4, 3)), z=2)
ax.text(vx2 + vw2 / 2, vy + vh + 0.14, L["view"], ha="center", va="center", fontsize=11.5, style="italic")
page(vx2 + 0.42, vy + 0.95, sw, 0.68, PAPER, lines=5, z=4)
agent(vx2 + vw2 / 2, vy + 0.45)

out = ROOT / "assets" / "figures" / "ch09-fatias.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
