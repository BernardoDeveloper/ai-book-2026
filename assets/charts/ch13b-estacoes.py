"""ch13b-estacoes: the six stations of building an LLM, with the microgpt lab's numbers.

Content: book/pt/ch13b.md; numbers checked in ~/Projects/microgpt/docs/report/
experiment-closeout.md and training-time-ledger.md (post 2026/10/14/treinei-meu-
proprio-modelo-de-ia-spoiler-e-so-pra-estudo):
  - data: 14 raw-download manifests, 20.40 GB; final foundation corpus
    3,475,651,395 stored training tokens (~3.5 billion);
  - tokenizer: 32,768-entry byte-level BPE;
  - pre-training: 10 billion tokens; 136.68 h of foundation process intervals
    (~137 h) on one RTX 5090;
  - SFT: selected checkpoint at 4,000 updates;
  - server: OpenAI-compatible /v1/chat/completions;
  - evaluation: 100 reserved (holdout) programming tasks.

Usage: uv run --with matplotlib python -I scripts/chart_check.py assets/charts/ch13b-estacoes.py pt
House style: docs/research/IMAGES.md §4.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": [("Dados", "20 GB baixados,\n3,5 bi de tokens"),
           ("Tokenizador", "dicionário de\n32.768 entradas"),
           ("Pré-treino", "10 bi de tokens,\n137 h numa RTX 5090"),
           ("Ajuste (SFT)", "4.000 atualizações\ncom exemplos"),
           ("Servidor", "API compatível\ncom a da OpenAI"),
           ("Avaliação", "100 tarefas\nreservadas")],
    "en": [("Data", "20 GB downloaded,\n3.5B tokens"),
           ("Tokenizer", "a dictionary of\n32,768 entries"),
           ("Pre-training", "10B tokens,\n137 h on an RTX 5090"),
           ("Tuning (SFT)", "4,000 updates\non examples"),
           ("Server", "OpenAI-compatible\nAPI"),
           ("Evaluation", "100 held-out\ntasks")],
}[LANG]

W, H = 6.4, 3.55
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes((0, 0, 1, 1))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

BW, BH, GAP = 1.78, 1.32, 0.33
X0 = (W - 3 * BW - 2 * GAP) / 2
ROWS = (1.98, 0.22)  # bottom edge of each row


def arrow(p, q, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=INK, lw=1.5,
                                 connectionstyle=f"arc3,rad={rad}", zorder=1, shrinkA=0, shrinkB=0))


boxes = []
for i, (title, sub) in enumerate(L):
    r, c = divmod(i, 3)
    x, y = X0 + c * (BW + GAP), ROWS[r]
    fc = AMBER if i == 2 else SAND   # pre-training: where the 137 hours went
    ax.add_patch(FancyBboxPatch((x, y), BW, BH, boxstyle="round,pad=0,rounding_size=0.08", fc=fc, ec=INK, lw=1.2,
                                zorder=2))
    ax.add_patch(Circle((x + 0.2, y + BH - 0.2), 0.13, fc=NAVY, ec=INK, lw=1.0, zorder=3))
    ax.text(x + 0.2, y + BH - 0.2, str(i + 1), ha="center", va="center", fontsize=10.5, fontweight="semibold",
            color=PAPER, zorder=4)
    ax.text(x + 0.4, y + BH - 0.2, title, ha="left", va="center", fontsize=12, fontweight="semibold", zorder=4)
    ax.text(x + BW / 2, y + 0.46, sub, ha="center", va="center", fontsize=10.5, linespacing=1.15, zorder=4)
    boxes.append((x, y))

for i in (0, 1, 3, 4):
    x, y = boxes[i]
    arrow((x + BW + 0.03, y + BH / 2), (x + BW + GAP - 0.03, y + BH / 2))
# row 1 -> row 2: from the bottom of box 3 back to the top of box 4
x3, y3 = boxes[2]; x4, y4 = boxes[3]
ym = (y3 + y4 + BH) / 2
ax.plot([x3 + BW / 2, x3 + BW / 2, x4 + BW / 2], [y3 - 0.03, ym, ym], color=INK, lw=1.5, zorder=1,
        solid_joinstyle="round")
arrow((x4 + BW / 2, ym), (x4 + BW / 2, y4 + BH + 0.03))

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch13b-estacoes.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
