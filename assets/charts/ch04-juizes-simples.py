"""ch04-juizes-simples: the Frank Investigator idea in plain form, with no numbers.

Content: book/pt/ch04.md, "Três empresas na mesma mesa" and "A fonte primária
manda" (source post 2026/03/27 ensinando-a-questionar-noticias-frank-investigator):
each claim is judged by three models from three different companies; if a
primary source contradicts the claim, it does not come out as "sustentada",
even if all three models say yes. "A fonte primária manda." Models are generic
(no vendor names or logos). The detailed version with confidence numbers is
ch04-tres-juizes, in the technical appendix.

Usage: uv run --with matplotlib python -I scripts/chart_check.py assets/charts/ch04-juizes-simples.py pt
House style: docs/research/IMAGES.md §4.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER, RUST = ("#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B",
                                                   "#E9DFC9", "#FBF9F4", "#B5523B")
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"claim": "a afirmação", "models": ["modelo da\nempresa A", "modelo da\nempresa B", "modelo da\nempresa C"],
           "yes": "sim", "votes": "os três dizem:\nsustentada", "source": "fonte\nprimária",
           "contra": "contradiz", "result": "não sai como\n“sustentada”", "rule": "a fonte primária manda"},
    "en": {"claim": "the claim", "models": ["model from\ncompany A", "model from\ncompany B", "model from\ncompany C"],
           "yes": "yes", "votes": "all three say:\nsupported", "source": "primary\nsource",
           "contra": "contradicts", "result": "doesn't come out\nas “supported”", "rule": "the primary source rules"},
}[LANG]

W, H = 7.0, 4.2
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes((0, 0, 1, 1))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")


def box(x, y, w, h, fc, lw=1.6, r=0.08, z=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=INK, lw=lw,
                                zorder=z))


def arrow(p, q, rad=0.0, lw=1.6, color=INK, ms=13, z=2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=color,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=z))


MID = 1.85
# the claim
box(0.15, MID - 0.4, 1.25, 0.8, SAND)
ax.text(0.775, MID, L["claim"], ha="center", va="center", fontsize=12, fontweight="semibold", zorder=4)

# three judges
ys = [MID + 0.95, MID, MID - 0.95]
MX, MW, MH = 1.95, 1.45, 0.72
for name, y in zip(L["models"], ys):
    arrow((1.42, MID), (MX - 0.03, y), rad=0.0)
    box(MX, y - MH / 2, MW, MH, NAVY)
    ax.text(MX + 0.1, y, name, ha="left", va="center", fontsize=11, color=PAPER, linespacing=1.1, zorder=4)
    # the vote, a small tag on the box's right edge
    ax.text(MX + MW - 0.12, y, L["yes"], ha="right", va="center", fontsize=11, fontweight="semibold", color=NAVY,
            zorder=5, bbox=dict(boxstyle="round,pad=0.18", fc=PAPER, ec="none"))

# the vote tally
VX, VW, VH = 3.95, 1.3, 0.8
for y in ys:
    arrow((MX + MW + 0.03, y), (VX - 0.03, MID + (y - MID) * 0.25), rad=0.0)
box(VX, MID - VH / 2, VW, VH, GRAY)
ax.text(VX + VW / 2, MID, L["votes"], ha="center", va="center", fontsize=11, color=PAPER, linespacing=1.15, zorder=4)

# result
RX, RW, RH = 5.4, 1.5, 0.8
arrow((VX + VW + 0.03, MID), (RX - 0.03, MID), lw=1.6)
box(RX, MID - RH / 2, RW, RH, AMBER, lw=1.8)
ax.text(RX + RW / 2, MID, L["result"], ha="center", va="center", fontsize=11, fontweight="semibold",
        linespacing=1.15, zorder=4)

# primary source above the result, with a veto arrow
DX, DY, DW, DH = RX + 0.23, 3.0, 1.05, 1.1
ax.add_patch(Polygon([(DX, DY), (DX + DW, DY), (DX + DW, DY + DH - 0.22), (DX + DW - 0.22, DY + DH), (DX, DY + DH)],
                     closed=True, fc=PAPER, ec=INK, lw=1.6, joinstyle="round", zorder=3))
ax.text(DX + 0.12, DY + DH - 0.14, L["source"], ha="left", va="top", fontsize=11, fontweight="semibold",
        linespacing=1.1, zorder=4)
for i in range(2):
    ax.plot([DX + 0.12, DX + DW - 0.15], [DY + 0.32 - i * 0.13] * 2, color=GRAY, lw=1.0, zorder=4)
arrow((RX + RW / 2, DY - 0.04), (RX + RW / 2, MID + RH / 2 + 0.04), lw=2.4, color=RUST, ms=15, z=5)
t = ax.text(RX + RW / 2 - 0.12, (DY + MID + RH / 2) / 2, L["contra"], ha="right", va="center", fontsize=11, color=RUST,
            fontweight="semibold")

# the rule, as a takeaway under the row
ax.text(W / 2, 0.2, L["rule"], ha="center", va="center", fontsize=12.5, style="italic")

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch04-juizes-simples.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
