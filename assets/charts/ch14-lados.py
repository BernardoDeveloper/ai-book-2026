"""ch14-lados: who stands where on AI risk, in the chapter's own three groups.

Content: book/pt/ch14.md, "Desacelerar, mas nem tanto", the summary sentence
"Pra quem perdeu a conta dos nomes, os lados ficam assim." The three group
labels and the names under each are copied from that sentence (and from the
EN unit for the English version); nothing else is added. Names only, no photos.

Usage: uv run --with matplotlib python -I scripts/chart_check.py assets/charts/ch14-lados.py pt
House style: docs/research/IMAGES.md §4.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = ("#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B",
                                             "#E9DFC9", "#FBF9F4")
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": [("Levando a sério\no risco de a IA\nescapar do controle", ["Coxon", "Amodei", "Hinton"]),
           ("Concordando\nem frear, enquanto\ntocam laboratórios\nna mesma corrida", ["Altman", "Musk"]),
           ("Chamando o medo\nde exagero ou\nde jogada", ["Sacks", "Huang", "LeCun", "Ng"])],
    "en": [("Taking seriously\nthe risk of AI\nescaping control", ["Coxon", "Amodei", "Hinton"]),
           ("Agreeing to brake,\nwhile running labs\nin the same race", ["Altman", "Musk"]),
           ("Calling the fear\nexaggeration\nor a ploy", ["Sacks", "Huang", "LeCun", "Ng"])],
}[LANG]

W, H = 7.0, 3.85
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes((0, 0, 1, 1))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

COLW, GAP, X0 = 2.12, 0.17, 0.12
FILLS = [NAVY, TEAL, GRAY]
HEAD_Y0, HEAD_H = 2.45, 1.22          # header block
NAME_H, NAME_GAP = 0.44, 0.1
for i, (head, names) in enumerate(L):
    x = X0 + i * (COLW + GAP)
    # column panel (background band, not a label box)
    ax.add_patch(FancyBboxPatch((x, 0.15), COLW, H - 0.25, boxstyle="round,pad=0,rounding_size=0.08",
                                fc=SAND, ec="none", zorder=0, gid="nocheck"))
    ax.add_patch(FancyBboxPatch((x + 0.1, HEAD_Y0), COLW - 0.2, HEAD_H, boxstyle="round,pad=0,rounding_size=0.07",
                                fc=FILLS[i], ec=INK, lw=1.6, zorder=2))
    ax.text(x + COLW / 2, HEAD_Y0 + HEAD_H / 2, head, ha="center", va="center", fontsize=12,
            fontweight="semibold", color=PAPER, linespacing=1.2, zorder=3)
    y = HEAD_Y0 - 0.22 - NAME_H
    for n in names:
        ax.add_patch(FancyBboxPatch((x + 0.3, y), COLW - 0.6, NAME_H, boxstyle="round,pad=0,rounding_size=0.06",
                                    fc=PAPER, ec=INK, lw=1.2, zorder=2))
        ax.text(x + COLW / 2, y + NAME_H / 2, n, ha="center", va="center", fontsize=13, zorder=3)
        y -= NAME_H + NAME_GAP

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch14-lados.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
