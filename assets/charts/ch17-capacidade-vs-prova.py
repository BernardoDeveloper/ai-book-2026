"""ch17-capacidade-vs-prova: static analysis reads the blueprint; only live capture shows what left.

Content: book/pt/ch17.md, "O que a planta não mostra" (source post 2026/07/08
fable-5-analisar-codigo-tiktok-clash-of-kings-govbr-fingerprint): static analysis
shows what the app can do (permissions, addresses it knows, identifiers it builds);
it does not show what actually leaves the phone. That needs dynamic analysis: run the
app on a prepared phone and intercept the connection, reading each packet; in TikTok
the sends go out encrypted, which widens the gap. Akita did not do the dynamic part.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch17-capacidade-vs-prova.py pt
"""
import sys
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Rectangle, Arc

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"static": "análise estática", "can": "o que ele pode fazer", "perm": "permissões",
           "addr": "endereços", "ids": "identificadores", "live": "captura ao vivo",
           "did": "o que de fato saiu", "enc": "criptografado", "icpt": "interceptador",
           "net": "internet"},
    "en": {"static": "static analysis", "can": "what it can do", "perm": "permissions",
           "addr": "addresses", "ids": "identifiers", "live": "live capture",
           "did": "what actually left", "enc": "encrypted", "icpt": "interceptor",
           "net": "internet"},
}[LANG]

W, H = 7.0, 3.9
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")


def rbox(x, y, w, h, fc, r=0.07, lw=1.4, z=3, ls="-", ec=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw,
                                linestyle=ls, zorder=z))


def arrow(p, q, rad=0.0, lw=1.4, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", zorder=7, shrinkA=0, shrinkB=0))


def panel(x0, w, title, sub):
    ax.add_patch(FancyBboxPatch((x0, 0.1), w, H - 0.2, boxstyle="round,pad=0,rounding_size=0.1", fc=SAND, ec="none", zorder=0))
    ax.text(x0 + 0.2, H - 0.36, title, ha="left", va="center", fontsize=13.5, fontweight="semibold")
    ax.text(x0 + 0.2, H - 0.68, sub, ha="left", va="center", fontsize=11.5, style="italic")


def padlock(cx, cy, s=1.0, z=8):
    ax.add_patch(Arc((cx, cy + 0.04 * s), 0.12 * s, 0.16 * s, theta1=0, theta2=180, ec=INK, lw=1.3, zorder=z))
    ax.plot([cx - 0.06 * s, cx - 0.06 * s], [cy + 0.04 * s, cy], color=INK, lw=1.3, zorder=z)
    ax.plot([cx + 0.06 * s, cx + 0.06 * s], [cy + 0.04 * s, cy], color=INK, lw=1.3, zorder=z)
    rbox(cx - 0.09 * s, cy - 0.1 * s, 0.18 * s, 0.13 * s, INK, r=0.02, lw=1.0, z=z)


# ---------- left: static analysis over a blueprint ----------
panel(0.08, 3.37, L["static"], L["can"])
bx, by, bw, bh = 0.35, 0.4, 1.75, 2.3
ax.add_patch(Rectangle((bx, by), bw, bh, fc=NAVY, ec=INK, lw=1.4, zorder=2))
for k in range(1, 10):  # fine grid
    ax.plot([bx + k * bw / 10] * 2, [by, by + bh], color=PAPER, lw=0.3, alpha=0.35, zorder=2.1)
for k in range(1, 12):
    ax.plot([bx, bx + bw], [by + k * bh / 12] * 2, color=PAPER, lw=0.3, alpha=0.35, zorder=2.1)
# rooms of the "app"
rooms = [(0.12, 1.35, 0.7, 0.8), (0.92, 1.35, 0.71, 0.8), (0.12, 0.15, 0.5, 1.05), (0.72, 0.15, 0.91, 0.5),
         (0.72, 0.75, 0.91, 0.45)]
for rx, ry, rw, rh in rooms:
    ax.add_patch(Rectangle((bx + rx, by + ry), rw, rh, fc="none", ec=PAPER, lw=1.3, zorder=2.2))
# tags pointing into rooms
tags = [("perm", (bx + 1.38, by + 1.85), 2.85), ("addr", (bx + 1.35, by + 0.97), 2.05), ("ids", (bx + 1.3, by + 0.4), 1.25)]
for key, (px, py), ty in tags:
    ax.add_patch(Circle((px, py), 0.045, fc=PAPER, ec=PAPER, zorder=3))
    rbox(2.22, ty - 0.17, 1.12, 0.34, PAPER, r=0.05, lw=1.1, z=5)
    ax.text(2.78, ty, L[key], ha="center", va="center", fontsize=10.5, zorder=6)
    ax.plot([px, 2.22], [py, ty], color=INK, lw=0.9, zorder=4)
# magnifier
mx, my, mr = 0.75, 1.75, 0.4
ax.add_patch(Circle((mx, my), mr, fc=(1, 1, 1, 0.12), ec=INK, lw=2.6, zorder=5))
ax.add_patch(Circle((mx, my), mr, fc="none", ec=PAPER, lw=1.0, zorder=5.1))
a = math.radians(-50)
ax.plot([mx + mr * math.cos(a), mx + 1.9 * mr * math.cos(a)], [my + mr * math.sin(a), my + 1.9 * mr * math.sin(a)],
        color=INK, lw=6, solid_capstyle="round", zorder=5)

# ---------- right: live capture ----------
x0 = 3.55
panel(x0, 3.37, L["live"], L["did"])
# phone
px, py = x0 + 0.25, 1.1
rbox(px, py, 0.5, 0.92, NAVY, r=0.08)
ax.add_patch(Rectangle((px + 0.07, py + 0.14), 0.36, 0.66, fc=PAPER, ec="none", zorder=4))
# pipe
p0, p1, pyc = px + 0.5, x0 + 2.75, py + 0.46
ix, iw = x0 + 1.45, 0.62
for dy in (0.2, -0.2):
    ax.plot([p0, p1], [pyc + dy, pyc + dy], color=INK, lw=1.6, zorder=3, solid_capstyle="round")
ax.add_patch(Rectangle((p0, pyc - 0.2), p1 - p0, 0.4, fc=PAPER, ec="none", zorder=2))
# network cloud at the end
for (cx, cy, r) in [(p1 + 0.12, pyc + 0.05, 0.22), (p1 + 0.3, pyc + 0.18, 0.2), (p1 + 0.33, pyc - 0.1, 0.19)]:
    ax.add_patch(Circle((cx, cy), r, fc=GRAY, ec=INK, lw=1.3, zorder=3))
for (cx, cy, r) in [(p1 + 0.12, pyc + 0.05, 0.22), (p1 + 0.3, pyc + 0.18, 0.2), (p1 + 0.33, pyc - 0.1, 0.19)]:
    ax.add_patch(Circle((cx, cy), r - 0.02, fc=GRAY, ec="none", zorder=3.1))
ax.text(p1 + 0.22, pyc - 0.5, L["net"], ha="center", va="center", fontsize=10.5)
# interceptor (the one highlight) sitting on the pipe
rbox(ix, pyc - 0.32, iw, 0.64, AMBER, r=0.06, z=6)
mx2, my2, r2 = ix + iw / 2 - 0.04, pyc + 0.04, 0.14
ax.add_patch(Circle((mx2, my2), r2, fc=PAPER, ec=INK, lw=1.5, zorder=7))
ax.plot([mx2 + r2 * 0.7, mx2 + r2 * 1.7], [my2 - r2 * 0.7, my2 - r2 * 1.7], color=INK, lw=2.6, solid_capstyle="round", zorder=7)
ax.text(ix + iw / 2, pyc + 0.55, L["icpt"], ha="center", va="center", fontsize=11, fontweight="semibold")
# packets: before and after the interceptor; some locked
packets = [(p0 + 0.1, False), (p0 + 0.42, True), (ix + iw + 0.08, True), (ix + iw + 0.38, False)]
for (qx, locked) in packets:
    rbox(qx, pyc - 0.11, 0.26, 0.22, PAPER if not locked else SAND, r=0.03, lw=1.1, z=5)
    if locked:
        padlock(qx + 0.13, pyc - 0.005, s=0.85)
# encrypted label pointing at a locked packet
ax.text(p0 + 0.55, pyc - 0.62, L["enc"], ha="center", va="center", fontsize=10.5, style="italic")
ax.plot([p0 + 0.55, p0 + 0.55], [pyc - 0.5, pyc - 0.14], color=INK, lw=0.9, zorder=4)

out = ROOT / "assets" / "figures" / "ch17-capacidade-vs-prova.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
