"""ch04-marca-dagua: a statistical text watermark (synonym forks nudged by a secret key).

Data: none. Schematic of book/pt/ch04.md ("Como se marca um texto sem mudar o
texto"), from akitaonrails.com 2026/08/16/entendendo-ia-watermark-da-anthropic:
at synonym forks ("nublado" / "cinzento") the secret key tilts the choice a bit;
a long text repeats the fork hundreds of times and the tilt becomes a signature;
a full rewrite by another model removes it. The grids are illustrative
(fixed random seed), not measurements.

Usage: uv run --with matplotlib python -I assets/charts/ch04-marca-dagua.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import random
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Polygon
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
MUTED = "#5E636C"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK})

L = {
    "pt": {"seg": ["O céu estava", "e a rua,", "…"], "f1": ("nublado", "cinzento"), "f2": ("vazia", "deserta"),
           "chave": "chave secreta", "muitas": "centenas de escolhas", "assin": "assinatura",
           "reesc": "reescrito por outro modelo", "some": "sinal some"},
    "en": {"seg": ["The sky was", "and the street,", "…"], "f1": ("cloudy", "overcast"), "f2": ("empty", "deserted"),
           "chave": "secret key", "muitas": "hundreds of choices", "assin": "signature",
           "reesc": "rewritten by another model", "some": "signal gone"},
}[LANG]

fig, ax = plt.subplots(figsize=(6.8, 4.9), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 12.4)
ax.set_ylim(0, 8.9)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)


def word(x, y, text, w, chosen=True, fc=PAPER, bold=False):
    ax.add_patch(FancyBboxPatch((x, y - 0.33), w, 0.66, boxstyle="round,pad=0,rounding_size=0.15", fc=fc,
                                ec=INK if chosen else GRAY, lw=1.6 if chosen else 1.0,
                                linestyle="-" if chosen else (0, (3, 2)), zorder=3))
    ax.text(x + w / 2, y, text, ha="center", va="center", fontsize=11.5, color=INK if chosen else MUTED,
            fontweight="semibold" if bold else "normal", zorder=4)


def link(p, q, chosen):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=INK if chosen else GRAY, lw=2.2 if chosen else 1.0,
            ls="-" if chosen else (0, (3, 2)), solid_capstyle="round", zorder=2)


def key(x, y, s=1.0):
    ax.add_patch(Circle((x, y), 0.2 * s, fc=AMBER, ec=INK, lw=1.4, zorder=6))
    ax.add_patch(Circle((x, y), 0.07 * s, fc=PAPER, ec=INK, lw=1.0, zorder=7))
    ax.add_patch(Polygon([(x + 0.18 * s, y - 0.05 * s), (x + 0.7 * s, y - 0.05 * s), (x + 0.7 * s, y - 0.2 * s),
                          (x + 0.6 * s, y - 0.2 * s), (x + 0.6 * s, y - 0.12 * s), (x + 0.5 * s, y - 0.12 * s),
                          (x + 0.5 * s, y - 0.2 * s), (x + 0.42 * s, y - 0.2 * s), (x + 0.42 * s, y + 0.05 * s),
                          (x + 0.18 * s, y + 0.05 * s)], closed=True, fc=AMBER, ec=INK, lw=1.2,
                         joinstyle="round", zorder=5))


# --- the sentence with two forks ---------------------------------------------
Y, UP, DN = 6.75, 7.75, 5.75
word(0.15, Y, L["seg"][0], 2.2)
fork1 = [(L["f1"][0], UP, True), (L["f1"][1], DN, False)]
fork2 = [(L["f2"][0], UP, False), (L["f2"][1], DN, True)]
for (w, y, ch) in fork1:
    link((2.35, Y), (3.25, y), ch)
    word(3.25, y, w, 1.75, ch, fc=SAND if ch else PAPER, bold=ch)
    link((5.0, y), (5.75, Y), ch)
word(5.75, Y, L["seg"][1], 1.65)
for (w, y, ch) in fork2:
    link((7.4, Y), (8.2, y), ch)
    word(8.2, y, w, 1.6, ch, fc=SAND if ch else PAPER, bold=ch)
    link((9.8, y), (10.55, Y), ch)
ax.text(10.75, Y, L["seg"][2], ha="left", va="center", fontsize=13, color=INK)

# keys nudging each fork toward one side
for kx, target in ((3.75, UP), (8.6, DN)):
    key(kx, Y, 0.9)
    ax.add_patch(FancyArrowPatch((kx + 0.35, Y + (0.2 if target > Y else -0.25)),
                                 (kx + 0.35, target + (-0.38 if target > Y else 0.38)), arrowstyle="-|>",
                                 mutation_scale=11, lw=1.4, color=INK, zorder=5))
ax.text(1.25, 5.7, L["chave"], ha="center", va="center", fontsize=11, style="italic")
ax.add_patch(FancyArrowPatch((2.15, 5.85), (3.55, Y - 0.2), arrowstyle="-", lw=0.9, color=INK,
                             connectionstyle="arc3,rad=0.25", zorder=4))

# --- many sentences: signature vs noise --------------------------------------
ax.plot([0.2, 12.2], [4.8, 4.8], color=GRAY, lw=0.8, ls=(0, (3, 3)))
COLS, ROWS, S, G = 12, 6, 0.32, 0.07


def grid(x0, y0, share, seed, alpha=1.0):
    rnd = random.Random(seed)
    cells = [rnd.random() < share for _ in range(COLS * ROWS)]
    for i, fav in enumerate(cells):
        cx = x0 + (i % COLS) * (S + G)
        cy = y0 + (ROWS - 1 - i // COLS) * (S + G)
        ax.add_patch(FancyBboxPatch((cx, cy), S, S, boxstyle="round,pad=0,rounding_size=0.05",
                                    fc=AMBER if fav else PAPER, ec=INK if fav else GRAY, lw=0.9, alpha=alpha,
                                    zorder=3))
    return x0 + COLS * (S + G) - G


GY = 1.35
x1 = grid(0.45, GY, 0.8, 7)
ax.text((0.45 + x1) / 2, 4.35, L["muitas"], ha="center", va="center", fontsize=11.5, fontweight="semibold")
ax.text((0.45 + x1) / 2, 0.85, L["assin"], ha="center", va="center", fontsize=12, fontweight="semibold",
        bbox=dict(boxstyle="round,pad=0.3", fc=SAND, ec=INK, lw=1.2))

x2 = grid(7.15, GY, 0.5, 11, alpha=0.55)
ax.text((7.15 + x2) / 2, 4.35, L["reesc"], ha="center", va="center", fontsize=11.5, color=MUTED)
ax.text((7.15 + x2) / 2, 0.85, L["some"], ha="center", va="center", fontsize=12, color=MUTED, style="italic")
ax.add_patch(FancyArrowPatch((x1 + 0.2, GY + 1.2), (7.0, GY + 1.2), arrowstyle="-|>", mutation_scale=14, lw=1.6,
                             color=GRAY, linestyle=(0, (4, 3)), zorder=3))

buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
out = ROOT / "assets" / "figures" / "ch04-marca-dagua.png"
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
