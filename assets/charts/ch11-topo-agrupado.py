"""ch11-topo-agrupado: the top of the v4 table is a cluster, not a ladder.

Content: book/pt/ch11.md, "O topo é um grupo" and "O ruído entre execuções".
Data: llm-coding-benchmark docs/success_report.v4.combined.md@HEAD (combined
ranking, 46 models, September 2026): every model at 90 or above, plus four
reference models further down. The shaded band is the one measured re-run in the
chapter: the same GPT 5.5, same harness, same configuration, scored 100 in the
official run and 91 in the repeat (end of September 2026). Tier A starts at 83.
Nex N2.5 Pro carries the report's asterisk (fixes left uncommitted on disk).

Usage: uv run --with matplotlib python -I assets/charts/ch11-topo-agrupado.py pt
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
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"axis": "nota (0 a 100)", "band": "o mesmo GPT 5.5 tirou 100\ne depois 91",
           "tier": "início do tier A (83)", "title": "quarta versão do benchmark, setembro de 2026",
           "refs": "mais abaixo na tabela", "rerun": "repetição",
           "note": "* correções deixadas sem salvar no histórico do projeto", "dec": ","},
    "en": {"axis": "score (0 to 100)", "band": "the same GPT 5.5 scored 100\nand then 91",
           "tier": "tier A starts (83)", "title": "fourth benchmark version, September 2026",
           "refs": "further down the table", "rerun": "re-run",
           "note": "* fixes left uncommitted in the project history", "dec": "."},
}[LANG]

TOP = [("GPT-6 Astra", 100), ("Claude Opus 5", 100), ("Claude Fable 5", 100), ("Claude Opus 5.5", 100),
       ("GPT 5.6 sol", 100), ("GPT 5.6 terra", 100), ("GPT 5.5", 100), ("Grok 4.6", 98.5),
       ("Claude Fable 5.1", 95.5), ("Sakana Fugu Ultra v2", 95.5), ("GPT 6 luna", 95.5), ("GPT 5.6 luna", 95.0),
       ("Nex N2.5 Pro*", 94.0), ("GLM 5.3", 94.0), ("DeepSeek V4.1 Flash", 92.5), ("Xiaomi MiMo V2.6 Pro", 92.0),
       ("Claude Sonnet 5", 91.0), ("GPT 6 sol", 91.0), ("Gemini 3.8 Flash high", 90.5)]
REFS = [("Claude Opus 4.8", 86.0), ("Grok 4.7", 83.5), ("MiniMax M3", 75.5), ("Mistral Large 3", 39.0)]
RERUN_MODEL, RERUN_SCORE = "GPT 5.5", 91.0

# Two side-by-side panels (8.0 x 6.6 in) so the book's height cap never shrinks the figure;
# printed at ~4.5 in wide, 13 pt drawn = 7.3 pt. Left: the first 12 of the top cluster;
# right: the other 7, then the reference models further down. Same x scale in both.
FS = 13
LEFT_ROWS = TOP[:12]
RIGHT_ROWS = TOP[12:] + [None] + REFS  # None = gap row
NROWS = max(len(LEFT_ROWS), len(RIGHT_ROWS))
X0 = 68  # zoomed; Mistral Large 3 (39) is drawn at the left edge with its value

fig = plt.figure(figsize=(8.0, 6.6), dpi=300)
fig.patch.set_facecolor(PAPER)
axes = [fig.add_axes([0.255, 0.155, 0.235, 0.70]), fig.add_axes([0.745, 0.155, 0.235, 0.70])]


def panel(ax, rows, first_index):
    ax.set_facecolor(PAPER)
    n = NROWS
    ax.set_xlim(X0, 101.5); ax.set_ylim(-0.6, n - 0.3)
    ax.axvspan(91, 100, color=AMBER, alpha=0.32, lw=0, zorder=0)
    ax.axvline(83, color=INK, lw=1.2, linestyle=(0, (5, 3)), zorder=1)
    ticks, labels = [], []
    for j, r in enumerate(rows):
        y = n - 1 - j
        if r is None:  # sub-heading row, set in the names column
            ax.text(-0.04, y, L["refs"], transform=ax.get_yaxis_transform(), ha="right", va="center",
                    fontsize=FS, style="italic", color="#5E636C")
            continue
        name, s = r
        ref = name in dict(REFS)
        shown = max(s, X0 + 0.7)
        if s < X0:
            ax.text(shown + 2.6, y, f"{s:.0f}", ha="left", va="center", fontsize=FS, color="#5E636C")
        ax.plot([X0, shown], [y, y], color=GRAY if ref else "#C9C4B8", lw=0.7, zorder=1)
        ax.scatter([shown], [y], s=70, zorder=4, marker="<" if s < X0 else "o",
                   facecolors=PAPER if ref else NAVY, edgecolors=GRAY if ref else INK, linewidths=1.4)
        if name == RERUN_MODEL:
            ax.plot([RERUN_SCORE, shown], [y, y], color=INK, lw=1.5, zorder=3)
            ax.scatter([RERUN_SCORE], [y], s=70, zorder=4, facecolors=PAPER, edgecolors=INK, linewidths=1.5)
            ax.text(RERUN_SCORE - 2.2, y, L["rerun"] + " 91", ha="right", va="center", fontsize=FS, style="italic",
                    zorder=5, bbox=dict(fc=PAPER, ec="none", pad=0.6))
        ticks.append(y); labels.append(name)
    ax.set_yticks(ticks)
    ax.set_yticklabels(labels, fontsize=FS)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.set_xticks([70, 80, 90, 100])
    ax.set_xticks([75, 85, 95], minor=True)
    ax.tick_params(axis="x", labelsize=FS, color=INK)
    ax.tick_params(axis="x", which="minor", length=2.5, color=INK)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(INK); ax.spines["bottom"].set_linewidth(1.2)
    ax.set_xlabel(L["axis"], fontsize=FS, labelpad=3)


panel(axes[0], LEFT_ROWS, 0)
panel(axes[1], RIGHT_ROWS, len(LEFT_ROWS))
# headers: the re-run band over the left panel, the tier A line over the right one
axes[0].text(100.6, NROWS - 0.22, L["band"].replace("\n", " "), ha="right", va="bottom", fontsize=FS, fontweight="semibold",
             linespacing=1.1)
axes[1].text(82.2, NROWS - 0.22, L["tier"], ha="right", va="bottom", fontsize=FS, style="italic")
fig.text(0.02, 0.962, L["title"], fontsize=15, fontweight="semibold", ha="left", va="center")
fig.text(0.02, 0.025, L["note"], fontsize=FS, style="italic", color="#5E636C", ha="left", va="center")

out = ROOT / "assets" / "figures" / "ch11-topo-agrupado.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
