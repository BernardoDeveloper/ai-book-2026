"""ch12-mescla: a merge is a weighted average of two finished models.

Content: book/pt/ch12.md, "A receita da prefeitura" and "Mesma base, outro modelo"
(source post 2026/06/15 controversia-llm-rio-3-5-plagio; Nex AGI issue #4):
Nex-N2-Pro is Qwen 3.5 plus agent post-training; the published Rio 3.5 checkpoint
would be ~60% Nex-N2-Pro + ~40% Qwen 3.5, number by number, with no new training.
Benchmark grades from the chapter: Qwen 3.5 raw 42/100 (tier C), Nex-N2-Pro 83 (tier A)
(source post 2026/07/01 llm-benchmark-sonnet-5-gemini-3-5-flash-sakana-fugu-ultra).
Arrow widths are proportional to the weights.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch12-mescla.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"qwen": "Qwen 3.5 (base)", "nex": "Nex-N2-Pro", "post": "pós-treino\npra agentes",
           "rio": "checkpoint\npublicado do\nRio 3.5", "avg": "média ponderada,\nsem treino novo",
           "g42": "nota 42", "g83": "nota 83"},
    "en": {"qwen": "Qwen 3.5 (base)", "nex": "Nex-N2-Pro", "post": "agent\npost-training",
           "rio": "published\nRio 3.5\ncheckpoint", "avg": "weighted average,\nno new training",
           "g42": "score 42", "g83": "score 83"},
}[LANG]

W, H = 6.4, 4.0
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")


def box(x, y, w, h, fill, text, sub):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.07", fc=fill, ec=INK,
                                lw=1.4, zorder=3))
    ax.text(x + w / 2, y + h * 0.62, text, ha="center", va="center", fontsize=12.5, color=PAPER, zorder=4,
            fontweight="semibold")
    ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center", fontsize=10.5, color=PAPER, zorder=4)


def arrow(p, q, rad=0.0, lw=1.6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=f"-|>,head_length={4 + lw * 1.3},head_width={2.5 + lw * 0.7}",
                                 color=INK, lw=lw, connectionstyle=f"arc3,rad={rad}", zorder=2,
                                 shrinkA=0, shrinkB=0))


bx, bw, bh = 0.7, 2.0, 0.8
box(bx, 2.95, bw, bh, NAVY, L["qwen"], L["g42"])
box(bx, 0.35, bw, bh, TEAL, L["nex"], L["g83"])
arrow((bx + bw / 2, 2.92), (bx + bw / 2, 1.18))
ax.text(bx + bw / 2 - 0.12, 2.05, L["post"], ha="right", va="center", fontsize=11, style="italic",
        linespacing=1.1)

# the published file, a document with a folded corner
fx, fy, fw, fh = 4.35, 1.05, 1.7, 1.75
fold = 0.32
ax.add_patch(Polygon([(fx, fy), (fx + fw, fy), (fx + fw, fy + fh - fold), (fx + fw - fold, fy + fh), (fx, fy + fh)],
                     closed=True, fc=AMBER, ec=INK, lw=1.4, zorder=3, joinstyle="round"))
ax.add_patch(Polygon([(fx + fw - fold, fy + fh), (fx + fw - fold, fy + fh - fold), (fx + fw, fy + fh - fold)],
                     closed=True, fc=PAPER, ec=INK, lw=1.2, zorder=4, joinstyle="round"))
ax.text(fx + fw / 2, fy + fh / 2 - 0.05, L["rio"], ha="center", va="center", fontsize=11.5, zorder=5,
        linespacing=1.1)
ax.text(fx + fw / 2, fy - 0.12, L["avg"], ha="center", va="top", fontsize=11, style="italic", linespacing=1.1)

# weighted arrows: 40% from Qwen, 60% from Nex (width proportional)
arrow((bx + bw + 0.03, 3.35), (fx + 0.5, fy + fh + 0.03), rad=-0.25, lw=2.0)
ax.text(3.55, 3.72, "40%", ha="center", va="center", fontsize=14, fontweight="semibold")
arrow((bx + bw + 0.03, 0.75), (fx - 0.03, fy + 0.5), rad=0.2, lw=3.0)
ax.text(3.3, 0.5, "60%", ha="left", va="center", fontsize=14, fontweight="semibold")

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch12-mescla.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
