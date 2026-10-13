"""apmecanica-mapa-de-sentidos: embeddings as a city map of meanings.

Content: book/pt/apmecanica.md, "Um mapa de sentidos": words used in similar situations
live close together ("cachorro" in the same neighbourhood as "gato", far from
"imposto"; "segunda-feira" near "terça"), and some relations become directions: the
path from "homem" to "mulher" is almost the same as from "rei" to "rainha"
(Mikolov et al. 2013). The real map has thousands of directions (over 12 thousand in
GPT-3). Positions are illustrative; no axes, no numbers.

Usage: uv run --with matplotlib --with numpy python -I assets/charts/apmecanica-mapa-de-sentidos.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Ellipse

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"animals": "animais", "days": "dias da semana", "money": "dinheiro e impostos",
           "cachorro": "cachorro", "gato": "gato", "cavalo": "cavalo",
           "segunda": "segunda", "terca": "terça", "quarta": "quarta",
           "imposto": "imposto", "salario": "salário", "boleto": "boleto",
           "homem": "homem", "mulher": "mulher", "rei": "rei", "rainha": "rainha",
           "note": "o mapa real tem milhares de direções"},
    "en": {"animals": "animals", "days": "weekdays", "money": "money and taxes",
           "cachorro": "dog", "gato": "cat", "cavalo": "horse",
           "segunda": "Monday", "terca": "Tuesday", "quarta": "Wednesday",
           "imposto": "tax", "salario": "salary", "boleto": "bill",
           "homem": "man", "mulher": "woman", "rei": "king", "rainha": "queen",
           "note": "the real map has thousands of directions"},
}[LANG]

W, H = 6.4, 4.4
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

# the "city": a rounded sheet with a faint street grid
ax.add_patch(FancyBboxPatch((0.12, 0.42), W - 0.24, H - 0.54, boxstyle="round,pad=0,rounding_size=0.12",
                            fc=PAPER, ec=INK, lw=1.4, zorder=0))
for gx in [0.9, 1.75, 2.6, 3.45, 4.3, 5.15]:
    ax.plot([gx, gx + 0.15], [0.47, H - 0.17], color=GRAY, lw=0.6, alpha=0.45, zorder=0.5)
for gy in [1.05, 1.75, 2.45, 3.15, 3.8]:
    ax.plot([0.17, W - 0.17], [gy, gy - 0.12], color=GRAY, lw=0.6, alpha=0.45, zorder=0.5)

def hood(cx, cy, w, h, angle, title, tx, ty, hatch=None):
    ax.add_patch(Ellipse((cx, cy), w, h, angle=angle, fc=SAND, ec=INK, lw=1.0, linestyle=(0, (3, 2)),
                         hatch=hatch, zorder=1))
    ax.text(tx, ty, title, ha="center", va="center", fontsize=11.5, style="italic", zorder=4)

def word(x, y, text, fill=NAVY, dx=0.11, ha="left", va="center", weight="normal"):
    ax.add_patch(Circle((x, y), 0.065, fc=fill, ec=INK, lw=1.0, zorder=3))
    ax.text(x + dx, y, text, ha=ha, va=va, fontsize=12, zorder=4, fontweight=weight)

# animals, top left
hood(1.35, 3.22, 2.0, 1.15, 8, L["animals"], 1.3, 3.92)
word(0.75, 3.25, L["cachorro"])
word(1.6, 3.4, L["gato"])
word(1.3, 2.9, L["cavalo"])
# weekdays, bottom left
hood(1.5, 1.35, 2.5, 1.05, -6, L["days"], 1.45, 0.66)
word(0.5, 1.5, L["segunda"], fill=TEAL)
word(1.2, 1.15, L["terca"], fill=TEAL)
word(1.68, 1.6, L["quarta"], fill=TEAL)
# money/taxes, top right (far from the animals)
hood(5.05, 3.3, 2.05, 1.05, -5, L["money"], 5.05, 3.98)
word(4.3, 3.38, L["imposto"], fill=GRAY)
word(5.15, 3.12, L["salario"], fill=GRAY)
word(5.05, 3.55, L["boleto"], fill=GRAY)

# parallelogram corner: homem -> mulher, rei -> rainha (same direction, amber)
hm, ml = (3.35, 1.0), (4.75, 1.3)
re, ra = (3.55, 2.05), (4.95, 2.35)
for p, q in [(hm, ml), (re, ra)]:
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=7,head_width=4", color=AMBER, lw=2.6,
                                 zorder=2.5, shrinkA=6, shrinkB=6))
for p, q in [(hm, re), (ml, ra)]:
    ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, lw=1.0, linestyle=(0, (2, 2)), zorder=2)
word(*hm, L["homem"], dx=0, ha="center", va="top")
word(*ml, L["mulher"], dx=0, ha="center", va="top")
word(*re, L["rei"], dx=0, ha="center", va="bottom")
word(*ra, L["rainha"], dx=0, ha="center", va="bottom")
# nudge the labels off the dots
for t in ax.texts[-4:]:
    x, y = t.get_position()
    t.set_position((x, y - 0.12 if t.get_va() == "top" else y + 0.12))

ax.text(W / 2, 0.2, L["note"], ha="center", va="center", fontsize=11.5, style="italic")

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "apmecanica-mapa-de-sentidos.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
