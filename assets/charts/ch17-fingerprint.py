"""ch17-fingerprint: weak, common signals add up to a near-unique, sticky identity.

Content: book/pt/ch17.md, "Um número de série que você nunca autorizou" (source post
2026/07/08 fable-5-analisar-codigo-tiktok-clash-of-kings-govbr-fingerprint): the
fingerprint joins dozens of phone signals (model, screen, processor, time zone,
battery, nearby Wi-Fi and Bluetooth devices, motion sensors); none identifies you
alone, the combination does; "um fingerprint bem montado sobrevive a você limpar os
dados do aplicativo e a reinstalar".

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch17-fingerprint.py pt
"""
import sys
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.transforms import Affine2D
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon, Rectangle, Arc, Ellipse

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"model": "modelo", "battery": "bateria", "tz": "fuso horário", "wifi": "Wi-Fi por perto",
           "bt": "Bluetooth por perto", "screen": "tela", "cpu": "processador", "sensors": "sensores",
           "fp": "fingerprint", "wipe": "limpar dados\ne reinstalar", "same": "continua\no mesmo"},
    "en": {"model": "model", "battery": "battery", "tz": "time zone", "wifi": "nearby Wi-Fi",
           "bt": "nearby Bluetooth", "screen": "screen", "cpu": "processor", "sensors": "sensors",
           "fp": "fingerprint", "wipe": "clear data\nand reinstall", "same": "still\nthe same"},
}[LANG]

W, H = 7.0, 4.4
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")
LW = 1.4


def arrow(p, q, rad=0.0, ls="-", lw=1.4, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2, shrinkA=0, shrinkB=0))


def rbox(x, y, w, h, fc=PAPER, r=0.05, lw=LW, z=4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=INK, lw=lw, zorder=z))


# ---------- icons, each centred on (cx, cy), about 0.5 in tall ----------
def i_phone(cx, cy):
    rbox(cx - 0.15, cy - 0.26, 0.3, 0.52, fc=NAVY)
    ax.add_patch(Rectangle((cx - 0.1, cy - 0.17), 0.2, 0.36, fc=PAPER, ec="none", zorder=5))


def i_battery(cx, cy):
    rbox(cx - 0.26, cy - 0.13, 0.48, 0.26, r=0.03)
    ax.add_patch(Rectangle((cx + 0.22, cy - 0.05), 0.05, 0.1, fc=INK, ec=INK, zorder=4))
    ax.add_patch(Rectangle((cx - 0.21, cy - 0.08), 0.22, 0.16, fc=TEAL, ec="none", zorder=5))


def i_clock(cx, cy):
    ax.add_patch(Circle((cx, cy), 0.22, fc=PAPER, ec=INK, lw=LW, zorder=4))
    ax.plot([cx, cx], [cy, cy + 0.14], color=INK, lw=1.5, zorder=5, solid_capstyle="round")
    ax.plot([cx, cx + 0.1], [cy, cy - 0.04], color=INK, lw=1.5, zorder=5, solid_capstyle="round")


def i_wifi(cx, cy):
    base = cy - 0.17
    ax.add_patch(Circle((cx, base), 0.04, fc=INK, ec=INK, zorder=5))
    for r in (0.14, 0.25, 0.36):
        ax.add_patch(Arc((cx, base), 2 * r, 2 * r, theta1=45, theta2=135, ec=INK, lw=1.8, zorder=5))


def i_headphones(cx, cy):
    ax.add_patch(Arc((cx, cy - 0.02), 0.42, 0.44, theta1=0, theta2=180, ec=INK, lw=1.8, zorder=5))
    for sx in (-1, 1):
        rbox(cx + sx * 0.21 - 0.06, cy - 0.2, 0.12, 0.2, fc=NAVY, r=0.03)


def i_screen(cx, cy):
    rbox(cx - 0.28, cy - 0.18, 0.56, 0.36, r=0.03)
    # double-headed width marker drawn with plain lines (survives the icon transform)
    ax.plot([cx - 0.19, cx + 0.19], [cy, cy], color=INK, lw=1.3, zorder=5)
    for sx in (-1, 1):
        ax.plot([cx + sx * 0.11, cx + sx * 0.19, cx + sx * 0.11], [cy + 0.07, cy, cy - 0.07], color=INK, lw=1.3, zorder=5)


def i_chip(cx, cy):
    for k in range(3):
        o = -0.09 + k * 0.09
        for (x0, y0, x1, y1) in [(o, 0.15, o, 0.22), (o, -0.15, o, -0.22), (0.15, o, 0.22, o), (-0.15, o, -0.22, o)]:
            ax.plot([cx + x0, cx + x1], [cy + y0, cy + y1], color=INK, lw=1.3, zorder=3)
    rbox(cx - 0.15, cy - 0.15, 0.3, 0.3, fc=NAVY, r=0.03)


def i_motion(cx, cy):
    ax.add_patch(Polygon([(cx - 0.12, cy - 0.23), (cx + 0.05, cy - 0.27), (cx + 0.15, cy + 0.2), (cx - 0.02, cy + 0.24)],
                         closed=True, fc=PAPER, ec=INK, lw=LW, zorder=4, joinstyle="round"))
    for r in (0.28, 0.36):
        ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=110, theta2=160, ec=INK, lw=1.4, zorder=4))
        ax.add_patch(Arc((cx, cy), 2 * r, 2 * r, theta1=-70, theta2=-20, ec=INK, lw=1.4, zorder=4))


def fingerprint(cx, cy, s=1.0, fill=AMBER):
    ax.add_patch(Ellipse((cx, cy), 1.0 * s, 1.3 * s, fc=fill, ec=INK, lw=1.6, zorder=4))
    for k, r in enumerate([0.08, 0.15, 0.22, 0.29, 0.36, 0.43]):
        gap = 25 + 18 * (k % 3)
        start = -90 + gap / 2 + 30 * (k % 2)
        ax.add_patch(Arc((cx, cy - 0.04 * s), 2 * r * s * 0.95, 2 * r * s * 1.25, theta1=start,
                         theta2=start + 360 - gap, ec=INK, lw=1.5 * s + 0.2, zorder=5))


# signals: one column of icon + label rows, arrows converging on the fingerprint
signals = [(i_phone, "model"), (i_screen, "screen"), (i_chip, "cpu"), (i_battery, "battery"),
           (i_clock, "tz"), (i_wifi, "wifi"), (i_headphones, "bt"), (i_motion, "sensors")]
fpx, fpy = 3.75, 2.2
for i, (icon, key) in enumerate(signals):
    cy = 4.0 - i * 0.52
    n_p, n_l = len(ax.patches), len(ax.lines)
    icon(0, 0)
    tr = Affine2D().scale(0.72).translate(0.45, cy) + ax.transData
    for a in ax.patches[n_p:] + ax.lines[n_l:]:
        a.set_transform(tr)
    ax.text(0.82, cy, L[key], ha="left", va="center", fontsize=11)
    src = (2.45, cy)
    ang = math.atan2(fpy - src[1], fpx - src[0])
    dst = (fpx - 0.6 * math.cos(ang), fpy - 0.75 * math.sin(ang))
    arrow(src, dst, lw=1.0, color=GRAY)

fingerprint(fpx, fpy)
ax.text(fpx, fpy - 0.98, L["fp"], ha="center", va="center", fontsize=13, fontweight="semibold")

# trash can: clear data and reinstall
tx, ty = 5.15, 2.0
ax.add_patch(Polygon([(tx - 0.3, ty + 0.35), (tx + 0.3, ty + 0.35), (tx + 0.24, ty - 0.4), (tx - 0.24, ty - 0.4)],
                     closed=True, fc=SAND, ec=INK, lw=LW, zorder=4, joinstyle="round"))
rbox(tx - 0.36, ty + 0.35, 0.72, 0.1, fc=SAND, r=0.02)
ax.add_patch(Rectangle((tx - 0.08, ty + 0.45), 0.16, 0.06, fc=SAND, ec=INK, lw=1.2, zorder=4))
for dx in (-0.12, 0, 0.12):
    ax.plot([tx + dx, tx + dx * 0.85], [ty + 0.25, ty - 0.3], color=INK, lw=1.1, zorder=5)
ax.text(tx, ty - 0.68, L["wipe"], ha="center", va="center", fontsize=11, linespacing=1.1)
arrow((fpx + 0.58, fpy), (tx - 0.4, fpy))

# the same fingerprint comes out the other side
ox, oy = 6.45, 2.2
arrow((tx + 0.4, fpy), (ox - 0.36, oy))
fingerprint(ox, oy, s=0.6)
ax.text(ox, oy - 0.75, L["same"], ha="center", va="center", fontsize=11, style="italic", linespacing=1.1)

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch17-fingerprint.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
