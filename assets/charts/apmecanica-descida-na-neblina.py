"""apmecanica-descida-na-neblina: gradient descent as walking downhill in fog.

Content: book/pt/apmecanica.md, "Descendo o morro na neblina": the hill is the size
of the error, each position of the billions of knobs is a point on the terrain; the
knobs start out randomly drawn ("sorteados"); at each step every knob turns a little
in the direction that makes the error smaller. Qualitative, no numeric axes.

Usage: uv run --with matplotlib --with numpy python -I assets/charts/apmecanica-descida-na-neblina.py pt
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon, Arc

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
FOG = "#D4D6DB"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"err": "tamanho do erro", "start": "botões sorteados", "low": "erro pequeno", "fog": "neblina",
           "knobs": "cada passo =\ntodos os botões\ngiram um pouquinho"},
    "en": {"err": "size of the error", "start": "knobs set at random", "low": "small error", "fog": "fog",
           "knobs": "each step =\nevery knob\nturns a tiny bit"},
}[LANG]

W, H = 6.4, 3.9
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

def terrain(x):
    # high start on the left, a small bump, a deep valley, a rise on the right
    return (0.55 + 2.35 * np.exp(-((x - 0.55) / 1.25) ** 2) + 0.35 * np.exp(-((x - 2.35) / 0.35) ** 2)
            + 0.9 * np.exp(-((x - 4.6) / 0.55) ** 2) - 0.1 * np.exp(-((x - 3.55) / 0.45) ** 2))

X0, X1 = 0.55, 4.55
x = np.linspace(X0, X1, 400)
y = terrain(x)
ax.fill_between(x, 0.32, y, color=SAND, zorder=1, lw=0)
ax.plot(x, y, color=INK, lw=2.4, zorder=2, solid_capstyle="round")
ax.plot([X0, X1], [0.32, 0.32], color=INK, lw=1.2, zorder=2)

# vertical "tamanho do erro" arrow
ax.add_patch(FancyArrowPatch((0.32, 0.32), (0.32, 3.55), arrowstyle="-|>,head_length=6,head_width=3.5",
                             color=INK, lw=1.4, zorder=2, shrinkA=0, shrinkB=0))
ax.text(0.16, 1.9, L["err"], rotation=90, ha="center", va="center", fontsize=12)

# walker position and the steps already taken
wx = 1.95
steps = np.linspace(0.62, wx - 0.12, 8)
wy = terrain(wx)
# fog: an image whose alpha is high everywhere except a small circle round the walker's feet,
# fading out softly at the edges of the landscape
gx, gy = np.meshgrid(np.linspace(0, W, 640), np.linspace(0, H, 390))
d = np.hypot(gx - wx, gy - (wy + 0.2))
alpha = np.clip((d - 0.4) / 0.2, 0, 1) * 0.8
edge = np.minimum.reduce([np.clip((gx - (X0 - 0.1)) / 0.25, 0, 1), np.clip(((X1 + 0.1) - gx) / 0.25, 0, 1),
                          np.clip((3.75 - gy) / 0.35, 0, 1), np.clip((gy - 0.15) / 0.2, 0, 1)])
alpha *= edge
rgba = np.zeros(gx.shape + (4,))
rgba[..., :3] = matplotlib.colors.to_rgb(FOG)
rgba[..., 3] = alpha
ax.imshow(rgba, extent=(0, W, 0, H), origin="lower", zorder=3, interpolation="bilinear")
ax.text(3.35, 3.05, L["fog"], ha="center", va="center", fontsize=12.5, style="italic", zorder=6, color=INK)

# dots for each step taken (above the fog so the reader sees the path)
for sx in steps:
    ax.add_patch(Circle((sx, terrain(sx) + 0.05), 0.04, fc=NAVY, ec=INK, lw=0.8, zorder=6))

# the walker: a tiny generic stick figure with an amber head (the one highlight), feet on the slope
lf, rf = (wx - 0.08, terrain(wx - 0.08)), (wx + 0.08, terrain(wx + 0.08))
hip = (wx - 0.01, lf[1] + 0.2)
neck = (wx + 0.02, hip[1] + 0.2)
head = (wx + 0.03, neck[1] + 0.07)
kw = dict(color=INK, lw=2.0, zorder=7, solid_capstyle="round")
ax.plot([hip[0], lf[0]], [hip[1], lf[1]], **kw)
ax.plot([hip[0], rf[0]], [hip[1], rf[1]], **kw)
ax.plot([hip[0], neck[0]], [hip[1], neck[1]], **kw)
ax.plot([neck[0] - 0.01, neck[0] - 0.11], [neck[1] - 0.04, neck[1] - 0.15], **kw)
ax.plot([neck[0] - 0.01, neck[0] + 0.1], [neck[1] - 0.04, neck[1] - 0.13], **kw)
ax.add_patch(Circle(head, 0.06, fc=AMBER, ec=INK, lw=1.2, zorder=8))

# labels on the terrain
sx0 = steps[0]
ax.text(sx0 + 0.2, terrain(sx0) + 0.18, L["start"], ha="left", va="bottom", fontsize=12, zorder=9)
vx = 3.6
ax.add_patch(Circle((vx, terrain(vx) + 0.06), 0.055, fc=PAPER, ec=INK, lw=1.2, zorder=6, linestyle=(0, (2, 1.5))))
ax.plot([vx, vx], [terrain(vx), 0.32], color=INK, lw=0.9, linestyle=(0, (2, 2)), zorder=5)
ax.text(vx, 0.24, L["low"], ha="center", va="top", fontsize=12, fontweight="semibold", zorder=9)

# inset: panel of knobs
px, py, pw, ph = 4.82, 1.45, 1.42, 1.65
ax.add_patch(FancyBboxPatch((px, py), pw, ph, boxstyle="round,pad=0,rounding_size=0.08", fc=PAPER, ec=INK, lw=1.4, zorder=4))
for i in range(3):
    for j in range(3):
        cx, cy = px + 0.28 + i * 0.43, py + 0.3 + j * 0.52
        ax.add_patch(Circle((cx, cy), 0.13, fc=NAVY, ec=INK, lw=1.1, zorder=5))
        a = np.radians(80 + 25 * ((i + j) % 3))
        ax.plot([cx, cx + 0.11 * np.cos(a)], [cy, cy + 0.11 * np.sin(a)], color=PAPER, lw=1.6, zorder=6, solid_capstyle="round")
        ax.add_patch(FancyArrowPatch((cx - 0.12, cy + 0.17), (cx + 0.12, cy + 0.17),
                                     arrowstyle="-|>,head_length=3,head_width=2", color=INK, lw=1.0,
                                     connectionstyle="arc3,rad=-0.5", zorder=6, shrinkA=0, shrinkB=0))
ax.text(px + pw / 2, py - 0.12, L["knobs"], ha="center", va="top", fontsize=11, linespacing=1.15)

out = ROOT / "assets" / "figures" / "apmecanica-descida-na-neblina.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
