"""ch18-interfaces: the interface changes at every step, the judgment underneath never breaks.

Content: book/pt/ch18.md, "Uma interface atrás da outra" (source post 2026/04/11
vs-code-e-o-novo-cartao-perfurado): front-panel switches (Altair 8800), punched cards,
Assembly, compilers, the code editor, and now agents. "Repare no padrão": first you had
to type the instruction, then order the card deck, then convince the compiler, then
stitch framework/HTML/CSS/cloud..., now orchestrate an agent. What stays is the list
under "sobra justamente a parte que separa o amador do profissional" (domain, architecture,
judgment). Steps are deliberately undated (cards and Assembly overlapped).

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch18-interfaces.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"steps": ["chaves\nno painel", "cartões\nperfurados", "Assembly", "compiladores", "editor\nde código", "agentes\nde IA"],
           "ops": ["subir e descer\ncada bit", "ordenar\no maço", "economizar\ncada byte", "convencer\no compilador",
                   "costurar\ndezenas de\ncamadas", "orquestrar\num agente"],
           "top": "o que muda: a interface",
           "band": "o que fica: julgamento, fundamentos, conhecimento do domínio"},
    "en": {"steps": ["front-panel\nswitches", "punched\ncards", "Assembly", "compilers", "code\neditor", "AI\nagents"],
           "ops": ["flip every\nbit", "order the\ndeck", "save every\nbyte", "convince the\ncompiler",
                   "stitch dozens\nof layers", "orchestrate\nan agent"],
           "top": "what changes: the interface",
           "band": "what stays: judgment, fundamentals, domain knowledge"},
}[LANG]

W, H = 6.4, 4.0
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

N = 6
x0, colw = 0.2, (W - 0.4) / N
cx = [x0 + colw * (i + 0.5) for i in range(N)]

# title of the changing layer
ax.text(W / 2, H - 0.22, L["top"], ha="center", va="center", fontsize=13, fontweight="semibold")

# what the person had to operate (top row, italic)
for i, t in enumerate(L["ops"]):
    ax.text(cx[i], H - 0.55, t, ha="center", va="top", fontsize=10.5, style="italic", linespacing=1.05)

# step tiles, rising like stairs
base = 1.6
tile_w, tile_h = colw - 0.12, 0.85
icon_y = []
for i in range(N):
    y = base
    fill = AMBER if i == N - 1 else SAND
    ax.add_patch(FancyBboxPatch((cx[i] - tile_w / 2, y), tile_w, tile_h + (N - 1 - i) * 0.0,
                                boxstyle="round,pad=0,rounding_size=0.06", fc=fill, ec=INK, lw=1.3, zorder=2))
    icon_y.append(y + tile_h / 2)
    # arrow between steps
    if i < N - 1:
        ax.add_patch(FancyArrowPatch((cx[i] + tile_w / 2 + 0.005, y + tile_h / 2),
                                     (cx[i + 1] - tile_w / 2 - 0.005, y + tile_h / 2),
                                     arrowstyle="-|>,head_length=3,head_width=2", color=INK, lw=1.0, zorder=3,
                                     shrinkA=0, shrinkB=0))

def ln(xs, ys, lw=1.3, color=INK, z=4):
    ax.plot(xs, ys, color=color, lw=lw, zorder=z, solid_capstyle="round")

# icon 1: panel with toggle switches
c, y = cx[0], icon_y[0]
ax.add_patch(Rectangle((c - 0.33, y - 0.2), 0.66, 0.4, fc=NAVY, ec=INK, lw=1.2, zorder=3))
for k in range(5):
    sx = c - 0.24 + k * 0.12
    up = k % 2 == 0
    ax.add_patch(Circle((sx, y - 0.08), 0.03, fc=PAPER, ec=INK, lw=0.8, zorder=4))
    ln([sx, sx], [y - 0.08, y + (0.1 if up else -0.16)], lw=1.6, color=PAPER, z=5)
    ax.add_patch(Circle((sx, y + 0.11), 0.022, fc=PAPER if up else GRAY, ec="none", zorder=4))

# icon 2: punched card (cut corner, holes)
c, y = cx[1], icon_y[1]
w_, h_ = 0.66, 0.38
pts = [(c - w_ / 2 + 0.08, y + h_ / 2), (c + w_ / 2, y + h_ / 2), (c + w_ / 2, y - h_ / 2), (c - w_ / 2, y - h_ / 2),
       (c - w_ / 2, y + h_ / 2 - 0.08)]
ax.add_patch(Polygon(pts, closed=True, fc=PAPER, ec=INK, lw=1.2, zorder=3))
import random
random.seed(4)
for col in range(9):
    for row in range(4):
        if random.random() < 0.35:
            ax.add_patch(Rectangle((c - 0.25 + col * 0.058, y - 0.13 + row * 0.08), 0.022, 0.04, fc=INK, ec="none", zorder=4))

# icon 3: chip (Assembly: talking to the processor)
c, y = cx[2], icon_y[2]
ax.add_patch(Rectangle((c - 0.2, y - 0.2), 0.4, 0.4, fc=NAVY, ec=INK, lw=1.2, zorder=4))
ax.add_patch(Rectangle((c - 0.09, y - 0.09), 0.18, 0.18, fc=GRAY, ec=INK, lw=0.8, zorder=5))
for k in range(4):
    o = -0.15 + k * 0.1
    ln([c + o, c + o], [y + 0.2, y + 0.28], lw=1.2)
    ln([c + o, c + o], [y - 0.2, y - 0.28], lw=1.2)
    ln([c - 0.2, c - 0.28], [y + o, y + o], lw=1.2)
    ln([c + 0.2, c + 0.28], [y + o, y + o], lw=1.2)

# icon 4: compiler = page of text funnelled into bits
c, y = cx[3], icon_y[3]
ax.add_patch(Rectangle((c - 0.34, y - 0.2), 0.3, 0.4, fc=PAPER, ec=INK, lw=1.1, zorder=4))
for k in range(4):
    ln([c - 0.29, c - 0.09 - (k % 2) * 0.06], [y + 0.12 - k * 0.08] * 2, lw=1.0, z=5)
ax.add_patch(FancyArrowPatch((c - 0.02, y), (c + 0.1, y), arrowstyle="-|>,head_length=2.5,head_width=1.8",
                             color=INK, lw=1.1, zorder=5, shrinkA=0, shrinkB=0))
for k in range(3):
    for j in range(2):
        ax.add_patch(Rectangle((c + 0.14 + j * 0.1, y + 0.1 - k * 0.1), 0.06, 0.06,
                               fc=INK if (k + j) % 2 else PAPER, ec=INK, lw=0.7, zorder=5))

# icon 5: code editor window
c, y = cx[4], icon_y[4]
ax.add_patch(Rectangle((c - 0.33, y - 0.21), 0.66, 0.42, fc=PAPER, ec=INK, lw=1.2, zorder=4))
ax.add_patch(Rectangle((c - 0.33, y + 0.13), 0.66, 0.08, fc=NAVY, ec=INK, lw=1.2, zorder=4))
for k, (ind, ln_) in enumerate([(0, 0.32), (0.08, 0.28), (0.08, 0.2), (0.16, 0.22), (0, 0.12)]):
    ln([c - 0.27 + ind, c - 0.27 + ind + ln_], [y + 0.06 - k * 0.055] * 2, lw=1.0, color=TEAL if k % 2 else INK, z=5)

# icon 6: agent = window with a spark, working on its own
c, y = cx[5], icon_y[5]
ax.add_patch(Rectangle((c - 0.33, y - 0.21), 0.66, 0.42, fc=PAPER, ec=INK, lw=1.2, zorder=4))
ax.add_patch(Rectangle((c - 0.33, y + 0.13), 0.66, 0.08, fc=NAVY, ec=INK, lw=1.2, zorder=4))
sx, sy, r = c, y - 0.04, 0.12
star = [(sx, sy + r), (sx + 0.03, sy + 0.03), (sx + r, sy), (sx + 0.03, sy - 0.03),
        (sx, sy - r), (sx - 0.03, sy - 0.03), (sx - r, sy), (sx - 0.03, sy + 0.03)]
ax.add_patch(Polygon(star, closed=True, fc=INK, ec=INK, lw=0.8, zorder=5))

# step names under each tile
for i, t in enumerate(L["steps"]):
    ax.text(cx[i], base - 0.08, t, ha="center", va="top", fontsize=11, fontweight="semibold", linespacing=1.05)

# the band that never breaks
ax.add_patch(FancyBboxPatch((0.15, 0.18), W - 0.3, 0.5, boxstyle="round,pad=0,rounding_size=0.08",
                            fc=NAVY, ec=INK, lw=1.4, zorder=2))
ax.text(W / 2, 0.43, L["band"], ha="center", va="center", fontsize=11.5, color=PAPER, fontweight="semibold", zorder=3)

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch18-interfaces.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
