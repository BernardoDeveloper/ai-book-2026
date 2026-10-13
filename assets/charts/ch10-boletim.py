"""ch10-boletim: the May 2026 scorecard of the marathon projects (score 1-10).

Data: book/pt/ch10.md ("O boletim"), from akitaonrails.com
2026/05/14/terminando-maratona-ia-sucesso-ou-fracasso (index.md, lines 37-79:
"Tier de cima (7-8/10)", "Tier do meio (5/10)", "Tier de baixo (3-4/10)",
"Fundo do poço (1-2/10)"). The six private repositories have no score and are left out.

Usage: uv run --with matplotlib python -I assets/charts/ch10-boletim.py pt
House style: docs/research/IMAGES.md §4 (drawn at 7.2 x 6.4 in, landscape-ish so the
book's height cap never shrinks it; printed at ~4.5 in wide, 12 pt drawn = 7.5 pt printed).
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
MUTED = "#5E636C"

for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK,
                     "axes.edgecolor": INK, "xtick.color": INK, "ytick.color": INK, "hatch.linewidth": 1.0})

# (project, score, tier) — from the 2026/05/14 post, in the post's order
DATA = [
    ("ai-jail", 8, "top"), ("The M.Akita Chronicles", 8, "top"),
    ("blog", 7, "top"), ("FrankMD", 7, "top"), ("easy-ffmpeg", 7, "top"),
    ("distrobox-gaming", 5, "mid"), ("llm-coding-benchmark", 5, "mid"),
    ("FrankMega", 5, "mid"), ("distrobox-llm", 5, "mid"),
    ("Frank Yomik", 4, "low"), ("NW-Omarchy", 4, "low"), ("Frank Investigator", 3, "low"),
    ("Frank FBI", 3, "low"), ("Frank Karaoke", 3, "low"),
    ("Frank Sherlock", 2, "bottom"), ("FrankClaw", 1, "bottom"),
    ("shadPS4", 1, "bottom"), ("easy-subtitle", 1, "bottom"),
]
L = {
    "pt": {"axis": "nota (1 a 10)", "top": "topo", "mid": "meio", "low": "baixo", "bottom": "fundo\ndo poço",
           "ten": "ninguém chegou a 10", "blog": "blog (código do site)", "shadPS4": "shadPS4 (estudo)"},
    "en": {"axis": "score (1 to 10)", "top": "top", "mid": "middle", "low": "low", "bottom": "rock\nbottom",
           "ten": "nobody reached 10", "blog": "blog (site code)", "shadPS4": "shadPS4 (study)"},
}[LANG]
STYLE = {  # fill, hatch — tiers differ by lightness and, for the two mid-greys, by hatch
    "top": (NAVY, None), "mid": (TEAL, None), "low": (GRAY, "///"), "bottom": (SAND, None),
}

fig, ax = plt.subplots(figsize=(7.2, 6.4), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)

# a small gap between tiers
ys, y, prev = [], 0.0, None
for _, _, tier in DATA:
    if prev and tier != prev:
        y += 0.45
    ys.append(y)
    y += 1
    prev = tier
ys = [ys[-1] - v for v in ys]  # first item at the top

for (name, score, tier), yy in zip(DATA, ys):
    fill, hatch = STYLE[tier]
    ax.barh(yy, score, height=0.72, color=fill, edgecolor=INK, linewidth=0.9, hatch=hatch)
    ax.text(score + 0.12, yy, str(score), va="center", ha="left", fontsize=12)

ax.set_yticks(ys)
ax.set_yticklabels([L.get(n, n) for n, _, _ in DATA], fontsize=12)
ax.tick_params(axis="y", length=0, pad=6)
ax.set_xlim(0, 12.6)
ax.set_xticks(range(0, 11, 2))
ax.tick_params(axis="x", labelsize=12, length=3)
ax.set_xlabel(L["axis"], fontsize=12.5, labelpad=6)
ax.xaxis.set_label_coords(10 / 12.6 / 2, -0.06)
ax.spines["bottom"].set_bounds(0, 10)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_ylim(min(ys) - 0.7, max(ys) + 1.3)

# the 10 that nobody reached
ax.axvline(10, color=INK, linewidth=1.3, linestyle=(0, (4, 3)), ymax=0.985)
ax.text(9.8, max(ys) + 0.95, L["ten"], ha="right", va="center", fontsize=12.5, style="italic")

# tier brackets on the right
for tier in ("top", "mid", "low", "bottom"):
    t = [yy for (_, _, tr), yy in zip(DATA, ys) if tr == tier]
    hi, lo = max(t) + 0.36, min(t) - 0.36
    x = 10.45
    ax.plot([x, x + 0.18, x + 0.18, x], [hi, hi, lo, lo], color=INK, linewidth=1.0, solid_capstyle="round")
    ax.text(x + 0.38, (hi + lo) / 2, L[tier], va="center", ha="left", fontsize=12.5, fontweight="semibold")

fig.tight_layout()
# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.
out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch10-boletim.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
