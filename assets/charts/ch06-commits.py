"""ch06-commits: where the 274 commits of The M.Akita Chronicles went.

Data: book/pt/ch06.md ("O que tinha embaixo da demonstração"), from the table in
akitaonrails.com 2026/02/20/do-zero-a-pos-producao-em-1-semana-como-usar-ia-em-
projetos-de-verdade-bastidores-do-the-m-akita-chronicles (index.md, lines 35-43).
Percentages are of the 274 commits as published in the post; the post's categories
overlap a little (counts sum to 295), so the bars are not meant to add to 100%.

Usage: uv run --with matplotlib python -I assets/charts/ch06-commits.py pt
House style: docs/research/IMAGES.md §4. Figure drawn at 6.4 in wide (printed at
~4.75 in), so font sizes are scaled by ~1.35 from the print spec.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"

INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"

for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK,
                     "axes.edgecolor": INK, "xtick.color": INK, "ytick.color": INK})

# (key, commits, percent of 274) — from the 2026/02/20 post
DATA = [
    ("features", 101, 37),
    ("bugs", 45, 16),
    ("tests", 44, 16),
    ("infra", 30, 11),
    ("refactor", 27, 10),
    ("docs", 27, 10),
    ("security", 21, 8),
]
LABELS = {
    "pt": {"features": "funcionalidades novas", "bugs": "correção de bugs",
           "tests": "testes e integração contínua", "infra": "infraestrutura e colocar no ar",
           "refactor": "refatoração e reforço", "docs": "documentação", "security": "segurança",
           "hidden": "o que não aparece\nna demonstração", "unit": "commits"},
    "en": {"features": "new features", "bugs": "bug fixes",
           "tests": "tests and continuous integration", "infra": "infrastructure and deployment",
           "refactor": "refactoring and hardening", "docs": "documentation", "security": "security",
           "hidden": "what the demo\ndoesn't show", "unit": "commits"},
}[LANG]

fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

ys = list(range(len(DATA)))[::-1]
for (key, n, pct), y in zip(DATA, ys):
    color = AMBER if key == "features" else NAVY
    ax.barh(y, pct, height=0.66, color=color, edgecolor=INK, linewidth=1.0)
    t = ax.text(pct + 0.8, y, f"{pct}%", va="center", ha="left", fontsize=12,
                fontweight="semibold" if key == "features" else "normal")
    ax.annotate(f"({n})", xy=(1, 0.5), xycoords=t, xytext=(5, 0), textcoords="offset points",
                va="center", ha="left", fontsize=10.5, color="#5E636C")

ax.set_yticks(ys)
ax.set_yticklabels([LABELS[k] for k, _, _ in DATA], fontsize=12)
ax.get_yticklabels()[0].set_fontweight("semibold")
ax.tick_params(axis="y", length=0, pad=6)
ax.set_xticks([])
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_linewidth(1.2)
ax.set_xlim(0, 48)
ax.set_ylim(-0.6, len(DATA) - 0.4)

# bracket grouping the six "invisible" categories
x = 27.5
ax.plot([x, x + 0.8, x + 0.8, x], [ys[1] + 0.3, ys[1] + 0.3, ys[-1] - 0.3, ys[-1] - 0.3],
        color=INK, linewidth=1.0, solid_capstyle="round")
ax.text(x + 2.0, (ys[1] + ys[-1]) / 2, LABELS["hidden"],
        va="center", ha="left", fontsize=12, style="italic")

fig.tight_layout()
# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.
out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch06-commits.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
