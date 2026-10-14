"""ch20-duas-curvas: two schematic curves that measure different things.

Content: book/pt/ch20.md, "O que se mede de fora" and "A curva que sobe"
(source post 2026/10/12 llms-agentes-competente-o-suficiente):
  (a) base intelligence of the top models: the labs report smaller gains from
      pre-training, and Stanford's AI Index 2025 measured the gap between the
      1st and the 10th model shrinking from ~12% to ~5% in a year: the top
      bunches up and flattens.
  (b) METR: the length of the tasks an agent completes on its own (50% success)
      doubled every seven months since 2019; in the author's reading most of
      the recent gain comes from the harness and tools.
Both panels are SCHEMATIC: the shapes illustrate the text; there are no y
values and the lines are not data (the five lines in (a) stand for "the top
models", not for any particular model).

Usage: uv run --with matplotlib --with numpy python -I scripts/chart_check.py assets/charts/ch20-duas-curvas.py pt
House style: docs/research/IMAGES.md §4.
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = ("#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B",
                                             "#E9DFC9", "#FBF9F4")
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"ta": "inteligência de base\ndos modelos de ponta", "tb": "tamanho das tarefas que\no agente completa sozinho",
           "time": "tempo", "pre": "ganho menor\nno pré-treino", "pack": "pelotão de cima\nse apertando",
           "gap": "do 1º ao 10º:\nde ~12% pra ~5%\nem um ano", "metr": "dobra a cada\n7 meses (METR)",
           "since": "2019", "harness": "maior parte do ganho\nrecente: harness\ne ferramentas"},
    "en": {"ta": "base intelligence\nof the top models", "tb": "length of the tasks an\nagent completes alone",
           "time": "time", "pre": "smaller gains\nfrom pre-training", "pack": "the top of the\npack bunching up",
           "gap": "1st to 10th:\nfrom ~12% to ~5%\nin a year", "metr": "doubles every\n7 months (METR)",
           "since": "2019", "harness": "most of the recent\ngain: harness\nand tools"},
}[LANG]

W, H = 7.2, 3.7
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes((0, 0, 1, 1))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
FS = 11.5
PB, PT = 0.42, 2.82          # plot bottom / top (inches)


def axes(x0, x1):
    for p, q in (((x0, PB), (x1, PB)), ((x0, PB), (x0, PT))):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, lw=1.3, color=INK, shrinkA=0,
                                     shrinkB=0))
    ax.text(x1, PB - 0.1, L["time"], ha="right", va="top", fontsize=FS, style="italic")


# ---------- (a) base intelligence: top models rise, bunch up, flatten ----------
AX0, AX1 = 0.3, 3.35
axes(AX0, AX1)
ax.text(AX0, H - 0.08, L["ta"], ha="left", va="top", fontsize=12, fontweight="semibold", linespacing=1.15)
t = np.linspace(0, 1, 300)
for i, (k, c) in enumerate(((0.0, 0.18), (0.06, 0.24), (0.12, 0.30), (0.18, 0.36), (0.24, 0.42))):
    level = 0.86 - 0.012 * i                         # they end almost together
    y = level / (1 + np.exp(-(t - c) * 11))
    xs = AX0 + 0.08 + t * (AX1 - AX0 - 0.3)
    ys = PB + 0.08 + y * (PT - PB - 0.5)
    ax.plot(xs, ys, color=NAVY if i == 0 else GRAY, lw=2.2 if i == 0 else 1.6, solid_capstyle="round", zorder=3)
end_x = AX0 + 0.08 + (AX1 - AX0 - 0.3)
top_y = PB + 0.08 + 0.86 * (PT - PB - 0.5)
# bracket around the bunched-up ends
ax.plot([end_x + 0.06, end_x + 0.12, end_x + 0.12, end_x + 0.06], [top_y + 0.04, top_y + 0.04, top_y - 0.12,
        top_y - 0.12], color=INK, lw=1.0)
ax.text(end_x - 0.02, top_y + 0.17, L["pack"], ha="right", va="bottom", fontsize=FS, linespacing=1.15)
ax.text(AX0 + 1.58, PB + 1.1, L["pre"], ha="left", va="center", fontsize=FS, linespacing=1.15)
ax.text(AX0 + 1.58, PB + 0.42, L["gap"], ha="left", va="center", fontsize=11.2, style="italic", linespacing=1.15,
        color="#5E636C")

# ---------- (b) task length: keeps rising ----------
BX0, BX1 = 3.95, 6.95
axes(BX0, BX1)
ax.text(BX0, H - 0.08, L["tb"], ha="left", va="top", fontsize=12, fontweight="semibold", linespacing=1.15)
ax.text(BX0, PB - 0.1, L["since"], ha="left", va="top", fontsize=FS)
x = np.linspace(0, 1, 300)
y = (2 ** (x * 7) - 1) / (2 ** 7 - 1)                 # schematic exponential
xs = BX0 + 0.08 + x * (BX1 - BX0 - 0.3)
ys = PB + 0.08 + y * (PT - PB - 0.3)
ax.plot(xs, ys, color=TEAL, lw=2.6, solid_capstyle="round", zorder=3)
ax.text(BX0 + 0.2, PT - 0.3, L["metr"], ha="left", va="center", fontsize=FS, linespacing=1.15)
# the recent stretch, highlighted, with its label
k = x > 0.72
ax.plot(xs[k], ys[k], color=AMBER, lw=5.5, solid_capstyle="round", zorder=2)
ax.text(xs[k][0] - 0.25, ys[k][0] + 0.55, L["harness"], ha="right", va="center", fontsize=FS, linespacing=1.15)
ax.add_patch(FancyArrowPatch((xs[k][0] - 0.2, ys[k][0] + 0.6), (xs[k][0] + 0.1, ys[k][0] + 0.25),
                             arrowstyle="-|>", mutation_scale=10, lw=1.0, color=INK, connectionstyle="arc3,rad=-0.2"))

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch20-duas-curvas.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
