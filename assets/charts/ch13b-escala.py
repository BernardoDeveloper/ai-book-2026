"""ch13b-escala: tokens seen in pre-training, log scale; the microgpt model vs public models.

Content: book/pt/ch13b.md. Data from the post 2026/10/14/treinei-meu-proprio-
modelo-de-ia-spoiler-e-so-pra-estudo (table "As dimensões do problema") and
~/Projects/microgpt/docs/report/experiment-closeout.md:
  - this model: 10 billion foundation tokens (10B milestone);
  - SmolLM2-360M: 4 trillion (model card, cited in the report, line ~502);
  - Llama 3.1: 15 trillion; Qwen3: 36 trillion (post's table).
SmolLM2-360M is about the same size as the 337M model: 4T / 10B = 400x.

Usage: uv run --with matplotlib python -I scripts/chart_check.py assets/charts/ch13b-escala.py pt
House style: docs/research/IMAGES.md §4.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER, RUST = ("#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B",
                                                   "#E9DFC9", "#FBF9F4", "#B5523B")
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK, "axes.edgecolor": INK,
                     "xtick.color": INK, "ytick.color": INK})

FIG = "ch13b-escala"
L = {
    "pt": {"rows": ["Este modelo\n(337 mi de parâmetros)", "SmolLM2\n(360 mi de parâmetros)", "Llama 3.1", "Qwen3"],
           "vals": ["10 bilhões", "4 trilhões", "15 trilhões", "36 trilhões"],
           "x": "tokens vistos no pré-treino (escala logarítmica)", "same": "mesmo tamanho,\n400 vezes mais texto"},
    "en": {"rows": ["This model\n(337M parameters)", "SmolLM2\n(360M parameters)", "Llama 3.1", "Qwen3"],
           "vals": ["10 billion", "4 trillion", "15 trillion", "36 trillion"],
           "x": "tokens seen in pre-training (log scale)", "same": "same size,\n400 times more text"},
}[LANG]
TOK = [10e9, 4e12, 15e12, 36e12]

fig = plt.figure(figsize=(6.4, 3.3), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes((0.29, 0.2, 0.66, 0.76))
ax.set_facecolor(PAPER)
y = [4.6, 2.6, 1.3, 0]
colors = [AMBER, NAVY, GRAY, GRAY]
ax.barh(y, TOK, height=0.75, color=colors, edgecolor=INK, linewidth=1.0, left=1e9)
ax.set_xscale("log")
ax.set_xlim(1e9, 4e14)
ax.set_yticks(y, L["rows"], fontsize=10.5)
for yy, v, lab in zip(y, TOK, L["vals"]):
    ax.text(v * 1.25, yy, lab, va="center", ha="left", fontsize=10.5, fontweight="semibold")
ax.set_xticks([1e9, 1e10, 1e11, 1e12, 1e13, 1e14])
ax.set_xticklabels(["1 bi" if LANG == "pt" else "1B", "10 bi" if LANG == "pt" else "10B",
                    "100 bi" if LANG == "pt" else "100B", "1 tri" if LANG == "pt" else "1T",
                    "10 tri" if LANG == "pt" else "10T", "100 tri" if LANG == "pt" else "100T"], fontsize=9.5)
ax.set_xlabel(L["x"], fontsize=10.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
# the same-size comparison: a bracket from our bar's end to SmolLM2's
ax.set_ylim(-0.6, 5.2)
ax.annotate("", xy=(4e12, 4.05), xytext=(10e9, 4.05),
            arrowprops=dict(arrowstyle="<->", color=RUST, lw=1.4))
ax.text(2e11, 3.95, L["same"], ha="center", va="top", fontsize=9.5, color=RUST, style="italic", linespacing=1.05)

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / f"{FIG}.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
