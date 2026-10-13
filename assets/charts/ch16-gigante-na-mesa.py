"""ch16-gigante-na-mesa: a million lines don't fit on the desk.

Content: book/pt/ch16.md, "Reescrever um gigante, um pedaço por vez" (source post
2026/03/16 reescrevi-o-openclaw-em-rust-funcionou-frankclaw), calling back the desk of
ch02: "Um milhão de linhas não cabe na mesa. O agente lê um pedaço, esquece o anterior,
inventa o que não viu", and the skeleton it left behind, full of "a fazer" markers.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch16-gigante-na-mesa.py pt
"""
import sys
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"stack": "um milhão\nde linhas", "desk": "janela de contexto", "todo": "a fazer",
           "sees": "o agente vê\nsó isto", "forgets": "esquece\no anterior"},
    "en": {"stack": "a million\nlines", "desk": "context window", "todo": "to do",
           "sees": "the agent sees\nonly this", "forgets": "forgets what\ncame before"},
}[LANG]

W, H = 6.4, 4.6
Y0 = 0.3  # trim empty band under the floor
fig = plt.figure(figsize=(W, H - Y0), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(Y0, H); ax.set_aspect("equal"); ax.axis("off")


def arrow(p, q, rad=0.0, ls="-", lw=1.6, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2, shrinkA=0, shrinkB=0))


def sheet(cx, cy, w, h, angle=0.0, fill=PAPER, lines=3, z=3, lw=1.1):
    """A sheet of paper with a few grey text lines, rotated by angle (degrees)."""
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    rot = lambda x, y: (cx + x * ca - y * sa, cy + x * sa + y * ca)
    ax.add_patch(Polygon([rot(-w / 2, -h / 2), rot(w / 2, -h / 2), rot(w / 2, h / 2), rot(-w / 2, h / 2)],
                         closed=True, fc=fill, ec=INK, lw=lw, zorder=z, joinstyle="round"))
    for i in range(lines):
        y = h / 2 - h * (i + 1) / (lines + 1)
        x1 = w / 2 - w * (0.18 if i % 2 else 0.3)
        p, q = rot(-w / 2 + w * 0.18, y), rot(x1, y)
        ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, lw=1.0, zorder=z + 0.1, solid_capstyle="round")


floor_y = 0.55
ax.plot([0.15, W - 0.15], [floor_y, floor_y], color=INK, lw=1.4, solid_capstyle="round", zorder=1)

# ---------- left: the giant stack ----------
sx, sw = 0.45, 1.35
n = 46
th = 0.068
for i in range(n):
    off = 0.025 * math.sin(i * 1.7)
    ax.add_patch(Rectangle((sx + off, floor_y + i * th), sw, th, fc=PAPER if i % 2 else SAND, ec=INK, lw=0.7, zorder=2))
top = floor_y + n * th
ax.text(sx + sw / 2, top + 0.42, L["stack"], ha="center", va="center", fontsize=13.5, fontweight="semibold",
        linespacing=1.1)

# ---------- right: the small desk ----------
dx0, dx1, dy = 3.35, 5.55, 1.75
ax.add_patch(Rectangle((dx0, dy), dx1 - dx0, 0.13, fc=NAVY, ec=INK, lw=1.4, zorder=3))
for lx in (dx0 + 0.12, dx1 - 0.22):
    ax.add_patch(Rectangle((lx, floor_y), 0.1, dy - floor_y, fc=NAVY, ec=INK, lw=1.2, zorder=2))
ax.text((dx0 + dx1) / 2, dy - 0.28, L["desk"], ha="center", va="center", fontsize=12.5, fontweight="semibold",
        color=INK, bbox=dict(boxstyle="round,pad=0.25,rounding_size=0.15", fc=PAPER, ec="none"), zorder=6)
# the few sheets the agent can see right now (the one highlight)
for i, (cx, ang) in enumerate([(3.85, -4), (4.35, 3), (4.85, -2)]):
    sheet(cx, dy + 0.13 + 0.33, 0.44, 0.6, angle=ang, fill=AMBER, z=4 + i * 0.2)
ax.text(4.1, dy + 1.12, L["sees"], ha="center", va="center", fontsize=11.5, style="italic", linespacing=1.1)

# a sheet travelling from the stack to the desk
arrow((sx + sw + 0.12, top - 0.35), (3.6, dy + 0.95), rad=-0.25)
sheet(2.55, top - 0.2, 0.36, 0.46, angle=-14, z=5)

# sheets sliding off the right edge and falling
sheet(5.55, dy + 0.2, 0.44, 0.58, angle=-38, z=4)
sheet(5.9, 1.25, 0.4, 0.52, angle=-62, z=4)
arrow((5.75, dy - 0.05), (6.05, 1.65), rad=-0.3, lw=1.3)
ax.text(W - 0.12, dy + 1.12, L["forgets"], ha="right", va="center", fontsize=11, style="italic", linespacing=1.1)

# crumpled "a fazer" notes on the floor
def crumple(cx, cy, r, seed):
    pts = []
    for k in range(11):
        a = 2 * math.pi * k / 11
        rr = r * (0.72 + 0.28 * ((math.sin(seed * 7.3 + k * 2.1) + 1) / 2))
        pts.append((cx + rr * math.cos(a), cy + rr * 0.75 * math.sin(a)))
    ax.add_patch(Polygon(pts, closed=True, fc=PAPER, ec=INK, lw=1.1, zorder=3, joinstyle="round"))
    ax.plot([cx - r * 0.4, cx + r * 0.1, cx + r * 0.35], [cy + r * 0.1, cy - r * 0.15, cy + r * 0.25],
            color=GRAY, lw=0.9, zorder=3.1)

for i, (cx, s) in enumerate([(2.35, 0.17), (2.75, 0.15), (3.05, 0.16), (5.95, 0.15)]):
    crumple(cx, floor_y + s * 0.75, s, i + 1)
# tag "a fazer"
tx, ty = 2.7, floor_y + 0.62
ax.add_patch(FancyBboxPatch((tx - 0.42, ty - 0.14), 0.84, 0.28, boxstyle="round,pad=0,rounding_size=0.06",
                            fc=SAND, ec=INK, lw=1.1, zorder=5))
ax.text(tx, ty, L["todo"], ha="center", va="center", fontsize=11.5, fontweight="semibold", zorder=6)
ax.plot([tx, tx], [ty - 0.14, floor_y + 0.27], color=INK, lw=1.0, zorder=4)

out = ROOT / "assets" / "figures" / "ch16-gigante-na-mesa.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
