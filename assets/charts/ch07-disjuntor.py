"""ch07-disjuntor: retrying forever vs. a circuit breaker.

Content: book/pt/ch07.md, "O disjuntor" (source post 2026/03/01
software-nunca-esta-pronto-4-projetos-a-vida-pos-deploy-e-por-que-one-shot-prompt-e-mito):
the web-search service answers "devagar, você está pedindo demais"; retrying with
growing waits piles up delayed requests; the breaker stops asking for two minutes and
the newsletter goes on with an empty section.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch07-disjuntor.py pt
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
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"retry": "tentar de novo", "breaker": "disjuntor", "prog": "programa", "svc": "serviço\nde busca",
           "slow": "“devagar, você está\npedindo demais”", "queue": "pedidos atrasados",
           "empty": "seção vazia", "two": "2 minutos", "reset": "religa", "goes": "a newsletter sai"},
    "en": {"retry": "retry", "breaker": "circuit breaker", "prog": "program", "svc": "search\nservice",
           "slow": "“slow down, you're\nasking too much”", "queue": "delayed requests",
           "empty": "empty section", "two": "2 minutes", "reset": "resets", "goes": "the newsletter goes out"},
}[LANG]

W, H = 6.4, 5.0
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

def box(x, y, w, h, fill, text="", fg=None, fs=12, ls="-", lw=1.4, weight="normal", z=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.07", fc=fill, ec=INK,
                                lw=lw, linestyle=ls, zorder=z))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=z + 1,
                color=fg or (INK if fill in (SAND, PAPER, AMBER) else PAPER), fontweight=weight, linespacing=1.1)

def arrow(p, q, rad=0.0, ls="-", lw=1.6, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2,
                                 shrinkA=0, shrinkB=0))

def panel(y0, h, title):
    ax.add_patch(FancyBboxPatch((0.08, y0), W - 0.16, h, boxstyle="round,pad=0,rounding_size=0.1",
                                fc=SAND, ec="none", zorder=0))
    ax.text(0.3, y0 + h - 0.25, title, ha="left", va="center", fontsize=13.5, fontweight="semibold")

# ---------- top: retry ----------
y0 = 2.62
panel(y0, 2.3, L["retry"])
box(0.3, y0 + 0.95, 1.25, 0.6, NAVY, L["prog"], fs=12)
box(4.75, y0 + 0.75, 1.35, 0.85, GRAY, L["svc"], fs=12, fg=PAPER)
for dy, rad in [(0.17, -0.12), (0.0, 0.0), (-0.17, 0.12)]:
    arrow((1.6, y0 + 1.25 + dy), (4.7, y0 + 1.17 + dy * 1.4), rad=rad)
# speech balloon from the service
bx, by, bw, bh = 2.55, y0 + 1.72, 2.55, 0.48
ax.add_patch(Polygon([(bx + bw - 0.45, by + 0.08), (bx + bw - 0.18, by + 0.08), (4.95, y0 + 1.6)], closed=True,
                     fc=PAPER, ec=INK, lw=1.2, zorder=2.9))
ax.add_patch(FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0,rounding_size=0.12", fc=PAPER, ec=INK, lw=1.2, zorder=3))
ax.add_patch(Polygon([(bx + bw - 0.44, by + 0.1), (bx + bw - 0.19, by + 0.1), (bx + bw - 0.3, by - 0.02)], closed=True,
                     fc=PAPER, ec="none", zorder=3.5))
ax.text(bx + bw / 2, by + bh / 2, L["slow"], ha="center", va="center", fontsize=11, style="italic", zorder=5, linespacing=1.05)
# growing queue under the program
xs, sizes = 0.32, [0.2, 0.24, 0.28, 0.32, 0.36, 0.40]
for i, s in enumerate(sizes):
    box(xs, y0 + 0.2, 0.22, s, PAPER, lw=1.1)
    xs += 0.3
arrow((0.95, y0 + 0.66), (0.95, y0 + 0.92), lw=1.3)
ax.text(xs + 0.1, y0 + 0.36, L["queue"], ha="left", va="center", fontsize=11.5)

# ---------- bottom: breaker ----------
y0 = 0.1
panel(y0, 2.4, L["breaker"])
box(0.3, y0 + 1.15, 1.25, 0.6, NAVY, L["prog"], fs=12)
box(4.75, y0 + 1.03, 1.35, 0.85, GRAY, L["svc"], fs=12, fg=PAPER)
# the breaker: a box with an open switch (lever up = tripped)
import math
cx, cy = 3.05, y0 + 1.45
ax.add_patch(FancyBboxPatch((cx - 0.42, cy - 0.38), 0.84, 0.76, boxstyle="round,pad=0,rounding_size=0.06",
                            fc=PAPER, ec=INK, lw=1.4, zorder=3))
lx, rx = cx - 0.24, cx + 0.24
ang = math.radians(38)
L_, T_ = 0.5, 0.075
dx, dy = math.cos(ang), math.sin(ang)
nx, ny = -dy * T_, dx * T_
ax.add_patch(Polygon([(lx + nx, cy + ny), (lx + dx * L_ + nx, cy + dy * L_ + ny),
                      (lx + dx * L_ - nx, cy + dy * L_ - ny), (lx - nx, cy - ny)], closed=True,
                     fc=AMBER, ec=INK, lw=1.2, zorder=4))
for px in (lx, rx):
    ax.add_patch(Circle((px, cy), 0.06, fc=INK, ec=INK, zorder=5))
ax.plot([1.6, cx - 0.42], [cy, cy], color=INK, lw=1.6, zorder=2)
ax.plot([lx, cx - 0.42], [cy, cy], color=INK, lw=1.6, zorder=4)
ax.plot([rx, cx + 0.42], [cy, cy], color=INK, lw=1.6, zorder=4)
ax.plot([cx + 0.42, 4.7], [cy, cy], color=GRAY, lw=1.6, linestyle=(0, (3, 3)), zorder=2)
mx = (cx + 0.42 + 4.7) / 2
ax.plot([mx - 0.09, mx + 0.09], [cy - 0.09, cy + 0.09], color=INK, lw=2, zorder=3, solid_capstyle="round")
ax.plot([mx - 0.09, mx + 0.09], [cy + 0.09, cy - 0.09], color=INK, lw=2, zorder=3, solid_capstyle="round")
# program goes on with an empty section
box(0.3, y0 + 0.2, 1.25, 0.55, PAPER, L["empty"], fs=11.5, ls=(0, (3, 2)), lw=1.3)
arrow((0.92, y0 + 1.12), (0.92, y0 + 0.8))
ax.text(1.7, y0 + 0.47, L["goes"], ha="left", va="center", fontsize=11.5, style="italic")
# clock + reset
kx, ky = 4.3, y0 + 0.5
ax.add_patch(Circle((kx, ky), 0.27, fc=PAPER, ec=INK, lw=1.4, zorder=3))
ax.plot([kx, kx], [ky, ky + 0.17], color=INK, lw=1.5, zorder=4, solid_capstyle="round")
ax.plot([kx, kx + 0.12], [ky, ky - 0.05], color=INK, lw=1.5, zorder=4, solid_capstyle="round")
ax.text(kx + 0.38, ky + 0.07, L["two"], ha="left", va="center", fontsize=11.5, fontweight="semibold")
ax.text(kx + 0.38, ky - 0.2, L["reset"], ha="left", va="center", fontsize=11.5)
arrow((kx - 0.22, ky + 0.22), (cx + 0.2, cy - 0.42), rad=-0.3, lw=1.3)

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch07-disjuntor.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
