"""ch13b-parametros: where the parameters went, vocabulary table vs transformer.

Content: book/pt/ch13b.md. Data from ~/Projects/microgpt/docs/report/
experiment-closeout.md:
  - 238,568,448-parameter capacity candidate (o200k vocabulary, width 768):
    "about 154M parameters were embedding/output and only 85M were
    transformer/norm";
  - final 337,167,360-parameter model (32,768-entry BPE, width 1,024): tied
    embedding/output 33,554,432; transformer/norm 303,612,928.

Usage: uv run --with matplotlib python -I scripts/chart_check.py assets/charts/ch13b-parametros.py pt
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

FIG = "ch13b-parametros"
L = {
    "pt": {"bars": ["modelo de 239 milhões\n(vocabulário de 200 mil)", "modelo final de 337 milhões\n(vocabulário de 32 mil)"],
           "vocab": "tabela de vocabulário", "tf": "camadas que pensam (transformer)",
           "x": "milhões de parâmetros", "fmt": lambda v: f"{v:.1f}".replace(".", ",").replace(",0", "")},
    "en": {"bars": ["239-million model\n(200k vocabulary)", "final 337-million model\n(32k vocabulary)"],
           "vocab": "vocabulary table", "tf": "layers that think (transformer)",
           "x": "millions of parameters", "fmt": lambda v: f"{v:.1f}".replace(".0", "")},
}[LANG]
VOCAB = [154.0, 33.6]
TF = [85.0, 303.6]

fig = plt.figure(figsize=(6.4, 2.9), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes((0.33, 0.33, 0.62, 0.62))
ax.set_facecolor(PAPER)
y = [1, 0]
ax.barh(y, VOCAB, height=0.55, color=GRAY, edgecolor=INK, linewidth=1.0, hatch="///", label=L["vocab"])
ax.barh(y, TF, height=0.55, left=VOCAB, color=TEAL, edgecolor=INK, linewidth=1.0, label=L["tf"])
for yy, v, t in zip(y, VOCAB, TF):
    ax.text(v / 2, yy, L["fmt"](v), ha="center", va="center", fontsize=10.5, fontweight="semibold",
            bbox=dict(boxstyle="round,pad=0.15", fc=PAPER, ec="none"))
    ax.text(v + t / 2, yy, L["fmt"](t), ha="center", va="center", fontsize=10.5, fontweight="semibold", color=PAPER)
ax.set_yticks(y, L["bars"], fontsize=10.5)
ax.set_xlim(0, 345)
ax.set_xlabel(L["x"], fontsize=10.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", labelsize=9.5)
fig.legend(loc="lower center", ncol=2, frameon=False, fontsize=10.5, bbox_to_anchor=(0.5, 0.0))

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / f"{FIG}.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
