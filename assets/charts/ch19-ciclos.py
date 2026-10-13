"""ch19-ciclos: the two-week sprint loop vs. the same-day loop (a hypothesis).

Content: book/pt/ch19.md, "A cerimônia", "Uma especulação sobre o processo" and
"Quatro cadeiras na mesma mesa" (source post 2026/06/24 por-que-llms-vao-falhar-na-sua-
empresa): planning, two weeks of implementation, testing, review; "um mês depois, talvez
dois" the decision reaches the product. The proposal, framed in the chapter as hypothesis:
programmer + agent in short blocks with PO, QA and tech lead taking turns, the cycle
"idealmente dentro do mesmo dia".

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch19-ciclos.py pt
"""
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Wedge, Arc

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"sprint": "sprint", "plan": "planejamento", "code": "duas semanas\nde código", "test": "testes",
           "review": "revisão", "result": "resultado", "long": "um a dois\nmeses", "pair": "programador\n+ agente",
           "po": "PO", "qa": "QA", "lead": "líder técnico", "same": "no mesmo dia", "hyp": "hipótese"},
    "en": {"sprint": "sprint", "plan": "planning", "code": "two weeks\nof coding", "test": "testing",
           "review": "review", "result": "result", "long": "one to two\nmonths", "pair": "programmer\n+ agent",
           "po": "PO", "qa": "QA", "lead": "tech lead", "same": "the same day", "hyp": "hypothesis"},
}[LANG]

W, H = 6.4, 4.3
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

def box(cx, cy, w, h, fill, text="", fs=11.5, weight="normal", ls="-", z=3):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.07",
                                fc=fill, ec=INK, lw=1.3, linestyle=ls, zorder=z))
    if text:
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, zorder=z + 1, fontweight=weight,
                color=INK if fill in (SAND, PAPER, AMBER) else PAPER, linespacing=1.05)

def arrow(p, q, rad=0.0, lw=1.5, ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=5,head_width=3", color=INK, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2, shrinkA=0, shrinkB=0))

def loop(cx, cy, r, gaps, lw=1.6):
    """Clockwise ring drawn as arcs between nodes (angles in degrees), with arrowheads."""
    for a0, a1 in gaps:
        p = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
        q = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
        span = (a0 - a1) % 360
        rad = -2 * math.tan(math.radians(span) / 4) / 2  # follow the circle (clockwise)
        arrow(p, q, rad=rad, lw=lw)

# ---------- panels ----------
ax.add_patch(FancyBboxPatch((0.08, 0.08), 3.5, H - 0.16, boxstyle="round,pad=0,rounding_size=0.1", fc=SAND, ec="none", zorder=0))
ax.add_patch(FancyBboxPatch((3.7, 0.08), W - 3.78, H - 0.16, boxstyle="round,pad=0,rounding_size=0.1", fc=SAND, ec="none", zorder=0))
ax.text(0.28, H - 0.3, L["sprint"], ha="left", va="center", fontsize=13.5, fontweight="semibold")

# ---------- left: sprint loop ----------
cx, cy, r = 1.72, 2.6, 0.9
box(cx, cy + r, 1.25, 0.42, PAPER, L["plan"])
box(cx + r + 0.12, cy, 1.15, 0.62, NAVY, L["code"])
box(cx, cy - r, 0.9, 0.42, PAPER, L["test"])
box(cx - r, cy, 0.9, 0.42, PAPER, L["review"])
loop(cx, cy, r, [(68, 25), (-25, -68), (-112, -158), (158, 112)])
# long exit to the result
box(2.85, 0.45, 1.0, 0.42, GRAY, L["result"], weight="semibold")
arrow((cx - r - 0.1, cy - 0.23), (2.33, 0.45), rad=0.45, lw=1.6, ls=(0, (4, 2.5)))
ax.text(1.3, 1.05, L["long"], ha="left", va="center", fontsize=11.5, fontweight="semibold", linespacing=1.05)

# ---------- right: same-day loop ----------
tx = 3.9
ax.add_patch(FancyBboxPatch((tx, H - 0.47), 1.05, 0.32, boxstyle="round,pad=0,rounding_size=0.06", fc=AMBER, ec=INK, lw=1.2, zorder=3))
ax.text(tx + 0.525, H - 0.31, L["hyp"], ha="center", va="center", fontsize=11.5, fontweight="semibold", zorder=4)

px, py, pr = 5.0, 2.62, 0.9
box(px, py, 1.0, 0.5, NAVY, L["pair"], fs=11)

def person(x, y, s=0.17):
    ax.add_patch(Wedge((x, y - 0.06), s * 1.15, 0, 180, fc=TEAL, ec=INK, lw=1.2, zorder=3))
    ax.add_patch(Circle((x, y + s * 0.75), s * 0.55, fc=TEAL, ec=INK, lw=1.2, zorder=3))

seats = [(145, L["po"], (0, 0.4), "center"), (35, L["qa"], (0, 0.4), "center"), (270, L["lead"], (0, -0.36), "center")]
for ang, name, (dx, dy), ha in seats:
    x, y = px + pr * math.cos(math.radians(ang)), py + pr * math.sin(math.radians(ang))
    ax.add_patch(Circle((x, y + 0.02), 0.27, fc=PAPER, ec="none", zorder=2))
    person(x, y)
    ax.text(x + dx, y + dy, name, ha=ha, va="center", fontsize=11.5, fontweight="semibold", zorder=4)
# rotation arrows between seats
for a0, a1 in [(125, 55), (12, -62), (-118, 168)]:
    p = (px + (pr + 0.12) * math.cos(math.radians(a0)), py + (pr + 0.12) * math.sin(math.radians(a0)))
    q = (px + (pr + 0.12) * math.cos(math.radians(a1)), py + (pr + 0.12) * math.sin(math.radians(a1)))
    arrow(p, q, rad=-0.35, lw=1.3)

# short exit to the result
box(px, 0.45, 1.0, 0.42, GRAY, L["result"], weight="semibold")
arrow((px, 1.12), (px, 0.68), lw=1.6)
ax.text(px + 0.12, 0.9, L["same"], ha="left", va="center", fontsize=11.5, fontweight="semibold")

out = ROOT / "assets" / "figures" / "ch19-ciclos.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
