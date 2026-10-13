"""ch04-tres-juizes: three models vote weighted by confidence; a primary source vetoes.

Data: the example in book/pt/ch04.md ("Três juízes e um veto"), from
akitaonrails.com 2026/03/27/ensinando-a-questionar-noticias-frank-investigator:
two models say "sustentado" at 70% and one says "misto" at 95%, and the "misto"
weighs more; a contrary primary source locks confidence at 60% at most and forces
"misto"; five outlets of the same group count as one voice; outlets citing each
other in a circle are flagged. Models are generic (no vendor names or logos).

Usage: uv run --with matplotlib python -I assets/charts/ch04-tres-juizes.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Arc
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER, RUST = ("#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B",
                                                   "#E9DFC9", "#FBF9F4", "#B5523B")
MUTED = "#5E636C"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK})

L = {
    "pt": {"models": [("modelo A", "sustentado 70%"), ("modelo B", "sustentado 70%"), ("modelo C", "misto 95%")],
           "sust": "sustentado", "misto": "misto", "fonte": "fonte\nprimária", "veto": "veto: no máximo 60%",
           "result": "misto, no máximo 60%", "grupo": "mesmo grupo = uma voz", "circ": "citação circular"},
    "en": {"models": [("model A", "supported 70%"), ("model B", "supported 70%"), ("model C", "mixed 95%")],
           "sust": "supported", "misto": "mixed", "fonte": "primary\nsource", "veto": "veto: 60% at most",
           "result": "mixed, 60% at most", "grupo": "same group = one voice", "circ": "circular citation"},
}[LANG]

fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 12.4)
ax.set_ylim(0.45, 9.1)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)


def box(x, y, w, h, fc, lw=1.6, r=0.15, z=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=INK, lw=lw,
                                zorder=z))


def arrow(p, q, rad=0.0, lw=1.8, color=INK, ms=14, z=2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=color,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=z))


def paper_icon(x, y, w=0.62, h=0.78, fc=PAPER, z=4):
    box(x, y, w, h, fc, lw=1.2, r=0.05, z=z)
    ax.plot([x + 0.1, x + w - 0.1], [y + h - 0.17] * 2, color=INK, lw=2.2, zorder=z + 1)
    for i in range(3):
        ax.plot([x + 0.1, x + w - 0.1], [y + h - 0.36 - i * 0.14] * 2, color=GRAY, lw=1.0, zorder=z + 1)


# --- the vote --------------------------------------------------------------
ys = [7.75, 6.35, 4.95]
for (name, vote), y in zip(L["models"], ys):
    box(0.2, y - 0.55, 2.85, 1.1, NAVY)
    ax.text(1.625, y + 0.2, name, ha="center", va="center", fontsize=11.5, fontweight="semibold", color=PAPER, zorder=5)
    ax.text(1.625, y - 0.22, vote, ha="center", va="center", fontsize=11, color=PAPER, zorder=5)

# balance: tilted toward "misto"
PX, PY = 6.05, 7.5          # pivot
half, tilt = 1.45, math.radians(-14)
lx, ly = PX - half * math.cos(tilt), PY - half * math.sin(tilt)
rx, ry = PX + half * math.cos(tilt), PY + half * math.sin(tilt)
ax.plot([PX, PX], [PY, 4.55], color=INK, lw=3.0, solid_capstyle="round", zorder=3)
ax.add_patch(Polygon([(PX - 0.6, 4.35), (PX + 0.6, 4.35), (PX, 4.8)], closed=True, fc=INK, ec=INK, lw=1, zorder=3))
ax.plot([lx, rx], [ly, ry], color=INK, lw=3.4, solid_capstyle="round", zorder=4)
ax.plot(PX, PY, "o", ms=7, mfc=AMBER, mec=INK, mew=1.2, zorder=5)


def pan(cx, top, label, weights):
    drop = 1.25
    by = top - drop
    ax.plot([cx, cx - 0.62], [top, by], color=INK, lw=1.1, zorder=3)
    ax.plot([cx, cx + 0.62], [top, by], color=INK, lw=1.1, zorder=3)
    ax.add_patch(Arc((cx, by), 1.5, 0.55, theta1=180, theta2=360, color=INK, lw=2.2, zorder=4))
    ax.plot([cx - 0.75, cx + 0.75], [by, by], color=INK, lw=2.2, zorder=4)
    x = cx - sum(w for w, _ in weights) / 2 - 0.05 * (len(weights) - 1) / 2
    for w, t in weights:
        box(x, by, w, w * 0.8, SAND, lw=1.2, r=0.06, z=5)
        ax.text(x + w / 2, by + w * 0.4, t, ha="center", va="center", fontsize=9 if w < 0.7 else 10,
                fontweight="semibold", zorder=6)
        x += w + 0.05
    ax.text(cx, by - 0.45, label, ha="center", va="top", fontsize=11.5, style="italic")
    return by


lby = pan(lx, ly, L["sust"], [(0.6, "70%"), (0.6, "70%")])
rby = pan(rx, ry, L["misto"], [(0.95, "95%")])
for y, (tx, ty) in zip(ys, ((lx - 0.55, lby + 0.6), (lx - 0.6, lby + 0.2), (rx - 0.78, rby - 0.2))):
    arrow((3.08, y), (tx, ty), rad=-0.1 if ty > y + 0.3 else 0.0)

# --- primary-source veto and result -----------------------------------------
RX0, RY0 = 8.75, 4.55
box(RX0, RY0, 3.55, 0.95, AMBER, lw=1.8)
ax.text(RX0 + 1.775, RY0 + 0.475, L["result"], ha="center", va="center", fontsize=11, fontweight="semibold", zorder=5)
arrow((rx + 0.95, rby + 0.1), (RX0 - 0.05, RY0 + 0.45), rad=0.15, lw=2.0)

# document with a veto stamp
DX, DY, DW, DH = 9.4, 6.4, 2.4, 2.5
ax.add_patch(Polygon([(DX, DY), (DX + DW, DY), (DX + DW, DY + DH - 0.35), (DX + DW - 0.35, DY + DH), (DX, DY + DH)],
                     closed=True, fc=PAPER, ec=INK, lw=1.6, joinstyle="round", zorder=3))
ax.text(DX + 0.2, DY + DH - 0.25, L["fonte"], ha="left", va="top", fontsize=11, fontweight="semibold",
        linespacing=1.1, zorder=4)
for i in range(2):
    ax.plot([DX + 0.2, DX + DW - 0.25], [DY + 1.25 - i * 0.22] * 2, color=GRAY, lw=1.0, zorder=4)
stamp = ax.text(DX + DW / 2, DY + 0.45, L["veto"], ha="center", va="center", fontsize=9.5, color=RUST,
                fontweight="semibold", rotation=6, zorder=6,
                bbox=dict(boxstyle="round,pad=0.25", fc=PAPER, ec=RUST, lw=1.8))
arrow((DX + DW / 2, DY - 0.05), (DX + DW / 2, RY0 + 1.0), lw=2.4, color=RUST, ms=16, z=5)

# --- inset: echoes are not evidence -----------------------------------------
ax.plot([0.2, 12.2], [3.3, 3.3], color=GRAY, lw=0.8, ls=(0, (3, 3)))
# five outlets of the same group -> one voice
for i in range(5):
    paper_icon(0.35 + i * 0.72, 1.75)
ax.plot([0.35, 0.35, 3.94, 3.94], [1.6, 1.45, 1.45, 1.6], color=INK, lw=1.0)
arrow((4.15, 2.15), (4.95, 2.15), lw=1.8)
paper_icon(5.1, 1.75, fc=SAND)
ax.text(2.15, 1.2, L["grupo"], ha="center", va="top", fontsize=11.5)

# outlets citing each other in a circle
CX, CY, CR = 8.0, 1.95, 0.95
angles = [90, 210, 330]
for a in angles:
    x = CX + CR * math.cos(math.radians(a)) - 0.31
    y = CY + CR * math.sin(math.radians(a)) - 0.39
    paper_icon(x, y)
for a in angles:
    a0, a1 = math.radians(a - 30), math.radians(a - 90)
    arrow((CX + CR * 1.18 * math.cos(a0), CY + CR * 1.18 * math.sin(a0)),
          (CX + CR * 1.18 * math.cos(a1), CY + CR * 1.18 * math.sin(a1)), rad=-0.35, lw=1.4, ms=11)
ax.text(CX + 1.6, CY, L["circ"], ha="left", va="center", fontsize=11.5)

buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.
out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch04-tres-juizes.png"
out.parent.mkdir(parents=True, exist_ok=True)
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
