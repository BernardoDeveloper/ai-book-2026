"""ch13b-abismo: looking like code vs working; the final microgpt model's results.

Content: book/pt/ch13b.md. Data from ~/Projects/microgpt/docs/report/
experiment-closeout.md, summary table (final selected model, one greedy
attempt per case):
  - holdout outputs that parse as Python: 100/100;
  - holdout outputs with requested function and parameter names: 97/100;
  - reserved programming holdout: 58/100;
  - actual OpenCode repository-repair smoke suite: 0/4, zero tool calls;
  - synthetic retrieval at 8K/16K/32K: 0/3 each, 0/9 in total.

Usage: uv run --with matplotlib python -I scripts/chart_check.py assets/charts/ch13b-abismo.py pt
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

FIG = "ch13b-abismo"
L = {
    "pt": {"rows": ["Python válido", "nome e parâmetros certos", "resultado correto\n(tarefas reservadas)",
                    "consertar um repositório\nno OpenCode", "achar um número escondido\nnum texto longo"],
           "g1": "parecer código", "g2": "funcionar", "x": "acertos (%)"},
    "en": {"rows": ["valid Python", "right name and parameters", "correct result\n(held-out tasks)",
                    "repair a repository\nin OpenCode", "find a number hidden\nin a long text"],
           "g1": "looking like code", "g2": "working", "x": "passed (%)"},
}[LANG]
HIT = [100, 97, 58, 0, 0]
OF = [100, 100, 100, 4, 9]

fig = plt.figure(figsize=(6.4, 3.6), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes((0.37, 0.15, 0.5, 0.8))
ax.set_facecolor(PAPER)
y = [5.6, 4.6, 2.6, 1.6, 0.6]   # a gap between the two groups
pct = [h / o * 100 for h, o in zip(HIT, OF)]
colors = [TEAL, TEAL, AMBER, RUST, RUST]
ax.barh(y, [max(p, 0.8) for p in pct], height=0.62,  # a sliver keeps the zeros visible
        color=colors, edgecolor=INK, linewidth=1.0)
for yy, p, h, o in zip(y, pct, HIT, OF):
    ax.text(max(p, 0.8) + 2, yy, f"{h}/{o}", va="center", ha="left", fontsize=10.5, fontweight="semibold")
ax.set_yticks(y, L["rows"], fontsize=10)
ax.set_xlim(0, 112)
ax.set_ylim(0, 6.6)
ax.set_xticks([0, 25, 50, 75, 100])
ax.tick_params(axis="x", labelsize=9.5)
ax.set_xlabel(L["x"], fontsize=10.5)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.axhline(3.6, color=GRAY, lw=1.0, ls=(0, (4, 3)))
ax.text(111, 6.25, L["g1"], ha="right", va="center", fontsize=10.5, style="italic", color=TEAL, fontweight="semibold")
ax.text(111, 3.3, L["g2"], ha="right", va="center", fontsize=10.5, style="italic", color=RUST, fontweight="semibold")

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / f"{FIG}.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
