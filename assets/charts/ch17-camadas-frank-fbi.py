"""ch17-camadas-frank-fbi: the suspicious e-mail goes through six weighted layers.

Content: book/pt/ch17.md, "Frank FBI" (source post 2026/03/09
atacando-fraudes-via-email-frank-fbi, whose layer headings give the weights:
header authentication 15%, sender reputation 15%, content 15%, external malicious-link
APIs 15%, entity verification 10%, LLM analysis 30%). The chapter: three models from
different companies read the e-mail independently and a voting system weighs them;
their claims are checked against the concrete data of the non-AI layers (e.g. domain
registration date); the result is a risk report.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch17-camadas-frank-fbi.py pt
"""
import sys
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Wedge, Circle

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"layers": ["autenticação do remetente", "reputação do remetente", "conteúdo",
                      "links maliciosos conhecidos", "identidade de quem assina", "análise por LLM"],
           "vote": "votação", "check": "conferência", "risk": "risco de 0 a 100", "email": "e-mail suspeito"},
    "en": {"layers": ["sender authentication", "sender reputation", "content",
                      "known malicious links", "identity of the signer", "LLM analysis"],
           "vote": "voting", "check": "cross-check", "risk": "risk from 0 to 100", "email": "suspicious e-mail"},
}[LANG]
WEIGHTS = [15, 15, 15, 15, 10, 30]

# Landscape layout (7.0 x 5.35 in) so the book's height cap never shrinks it: the envelope
# enters from the top, the cross-check rail runs down the left side, and the risk gauge
# sits to the right of the LLM band. Printed at ~4.5 in wide, 11.5 pt drawn = 7.4 pt.
W, H = 7.0, 5.35
FS = 11.5
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")


def box(x, y, w, h, fill, text="", fg=None, fs=FS, ls="-", lw=1.4, weight="normal", z=3, r=0.07):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fill, ec=INK,
                                lw=lw, linestyle=ls, zorder=z))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=z + 1,
                color=fg or (INK if fill in (SAND, PAPER, AMBER) else PAPER), fontweight=weight, linespacing=1.1)


def arrow(p, q, rad=0.0, ls="-", lw=1.6, color=INK, z=2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=z, shrinkA=0, shrinkB=0))


# ---------- six bands ----------
X0, X1 = 0.75, 4.95
BAR0, SCALE = 3.28, 0.95 / 30  # weight bar start and inches per percentage point
bh, gap = 0.5, 0.11
TOP = 4.45

# ---------- envelope (top, centred on the stack) ----------
ew, eh = 0.72, 0.47
ex, ey = (X0 + X1) / 2 - ew / 2, TOP + 0.3
box(ex, ey, ew, eh, PAPER, r=0.03)
ax.plot([ex + 0.03, ex + ew / 2, ex + ew - 0.03], [ey + eh - 0.03, ey + 0.18, ey + eh - 0.03], color=INK, lw=1.4, zorder=4)
ax.text(ex + ew + 0.16, ey + eh / 2, L["email"], ha="left", va="center", fontsize=12, style="italic")
arrow((ex + ew / 2, ey - 0.03), (ex + ew / 2, TOP + 0.04))

tops = []
y = TOP
for i, (name, wt) in enumerate(zip(L["layers"], WEIGHTS)):
    llm = i == 5
    h = 1.12 if llm else bh
    y0 = y - h
    box(X0, y0, X1 - X0, h, AMBER if llm else (SAND if i % 2 == 0 else PAPER), r=0.06)
    ty = y0 + h - 0.25
    ax.text(X0 + 0.18, ty, name, ha="left", va="center", fontsize=FS,
            fontweight="semibold" if llm else "normal", zorder=5)
    ax.add_patch(FancyBboxPatch((BAR0, ty - 0.09), wt * SCALE, 0.18, boxstyle="round,pad=0,rounding_size=0.03",
                                fc=NAVY, ec=INK, lw=1.0, zorder=5))
    ax.text(BAR0 + wt * SCALE + 0.09, ty, f"{wt}%", ha="left", va="center", fontsize=FS, fontweight="semibold", zorder=5)
    tops.append((y0, h))
    y = y0 - gap

# three models vote inside the LLM band
ly0, lh = tops[5]
my = ly0 + 0.13
for k in range(3):
    mx = X0 + 0.23 + k * 0.6
    box(mx, my, 0.44, 0.36, PAPER, r=0.05, lw=1.2, z=5)
    for j, ww in enumerate((0.26, 0.18)):  # two text lines: a generic "model answer" glyph
        ax.plot([mx + 0.09, mx + 0.09 + ww], [my + 0.23 - j * 0.11] * 2, color=INK, lw=1.4, zorder=6,
                solid_capstyle="round")
vx = BAR0
box(vx, my + 0.02, 1.1, 0.32, NAVY, L["vote"], fs=FS, z=5, r=0.05)
# orthogonal connector: each model drops onto a bus that feeds the vote
bus = my - 0.06
for k in range(3):
    cx = X0 + 0.23 + k * 0.6 + 0.22
    ax.plot([cx, cx], [my, bus], color=INK, lw=1.1, zorder=6)
ax.plot([X0 + 0.45, vx - 0.18, vx - 0.18], [bus, bus, my + 0.18], color=INK, lw=1.1, zorder=6,
        solid_joinstyle="round")
arrow((vx - 0.18, my + 0.18), (vx - 0.01, my + 0.18), lw=1.1, z=6)

# ---------- cross-check rail (left): LLM claims checked against the non-AI layers ----------
rx = X0 - 0.3
ly_mid = ly0 + lh / 2
ax.plot([X0, rx], [ly_mid, ly_mid], color=INK, lw=1.3, linestyle=(0, (2, 2)), zorder=2)
top_mid = tops[0][0] + bh / 2
ax.plot([rx, rx], [ly_mid, top_mid], color=INK, lw=1.3, linestyle=(0, (2, 2)), zorder=2)
for (y0, h) in tops[:5]:
    arrow((rx, y0 + h / 2), (X0 - 0.04, y0 + h / 2), ls=(0, (2, 2)), lw=1.3)
ax.text(rx - 0.2, (ly_mid + top_mid) / 2, L["check"], ha="center", va="center", rotation=90, fontsize=FS,
        style="italic")

# ---------- risk gauge (right of the stack, fed by all six layers) ----------
gr = 0.72
gx, gy = X1 + 0.5 + gr, (tops[0][0] + bh + ly0) / 2 - 0.3
stack_top, stack_bot = tops[0][0] + bh, ly0
# a bracket gathers the six bands, then one arrow goes to the gauge
bx = X1 + 0.16
ax.plot([X1 + 0.04, bx, bx, X1 + 0.04], [stack_top - 0.02, stack_top - 0.02, stack_bot + 0.02, stack_bot + 0.02],
        color=INK, lw=1.3, zorder=2, solid_joinstyle="round")
arrow((bx, gy + gr * 0.5), (gx - gr - 0.06, gy + gr * 0.5))
ax.add_patch(Wedge((gx, gy), gr, 0, 180, width=0.24, fc=SAND, ec=INK, lw=1.4, zorder=3))
for t in range(0, 101, 25):
    a = math.radians(180 - 1.8 * t)
    ax.plot([gx + (gr - 0.24) * math.cos(a), gx + gr * math.cos(a)], [gy + (gr - 0.24) * math.sin(a), gy + gr * math.sin(a)],
            color=INK, lw=1.0, zorder=4)
a = math.radians(180 - 1.8 * 78)
ax.plot([gx, gx + (gr - 0.1) * math.cos(a)], [gy, gy + (gr - 0.1) * math.sin(a)], color=INK, lw=2.4,
        solid_capstyle="round", zorder=5)
ax.add_patch(Circle((gx, gy), 0.06, fc=INK, ec=INK, zorder=6))
ax.text(gx - gr + 0.12, gy - 0.16, "0", ha="center", va="center", fontsize=FS)
ax.text(gx + gr - 0.12, gy - 0.16, "100", ha="center", va="center", fontsize=FS)
ax.text(gx, gy + gr + 0.22, L["risk"], ha="center", va="center", fontsize=12, fontweight="semibold")

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch17-camadas-frank-fbi.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
