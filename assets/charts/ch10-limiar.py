"""ch10-limiar: the threshold for fixing small annoyances dropped.

Content: book/pt/ch10.md, "A economia das pequenas coceiras" and "Um relógio, um
e-mail, uma música" (source posts 2026/07/12 usando-ia-pra-resolver-meus-probleminhas-
do-dia-a-dia and 2026/06/08 brincando-tui-llms-ratatui-bubbletea): fixing an
irritation used to cost a whole weekend, so almost none was worth it; with agents the
cost fell so much that almost all are. The named dots are the irritations the chapter
fixes (desk clock, e-mail client, song lyric loop, typing practice, kanji readings in
manga, investments TUI); the unnamed ones stand for the rest. Positions are
illustrative, not measured.

Usage: uv run --with matplotlib python -I assets/charts/ch10-limiar.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"before": "antes", "after": "depois", "axis": "incômodo", "weekend": "custa um fim de semana",
           "agent": "com um agente", "unfixed": "fica sem conserto", "fixed": "vale consertar",
           "dots": {"clock": "relógio", "mail": "e-mail", "lyrics": "letra de música", "typing": "digitação",
                    "kanji": "kanji no mangá", "invest": "investimentos"}},
    "en": {"before": "before", "after": "after", "axis": "annoyance", "weekend": "costs a weekend",
           "agent": "with an agent", "unfixed": "stays unfixed", "fixed": "worth fixing",
           "dots": {"clock": "clock", "mail": "e-mail", "lyrics": "song lyric", "typing": "typing",
                    "kanji": "kanji in manga", "invest": "investments"}},
}[LANG]

# (key or None, x, annoyance) — illustrative positions
DOTS = [("kanji", 0.25, 6.4), ("mail", 0.62, 5.1), ("typing", 0.22, 4.0), ("invest", 0.6, 3.3),
        ("clock", 0.2, 2.6), ("lyrics", 0.6, 2.0), (None, 0.85, 4.6), (None, 1.25, 2.7),
        (None, 0.45, 7.3), (None, 0.4, 1.1), (None, 0.3, 9.2), (None, 0.12, 5.6)]
LINES = {"before": 8.4, "after": 1.55}

fig, axes = plt.subplots(1, 2, figsize=(6.4, 4.3), dpi=300, sharey=True)
fig.patch.set_facecolor(PAPER)
for ax, key in zip(axes, ("before", "after")):
    ax.set_facecolor(PAPER)
    ax.set_xlim(0, 1.45); ax.set_ylim(0, 10)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_linewidth(1.4); ax.spines["left"].set_color(INK)
    ax.plot(0, 10, "^", color=INK, ms=6, clip_on=False)
    ax.set_title(L[key], fontsize=13.5, fontweight="semibold", loc="left", pad=8)
    t = LINES[key]
    ax.axhline(t, color=INK, lw=1.6, linestyle=(0, (5, 3)))
    ax.text(1.45, t - 0.22, L["weekend" if key == "before" else "agent"], ha="right", va="top",
            fontsize=11.5, fontweight="semibold")
    for name, x, y in DOTS:
        fixed = y > t
        ax.scatter([x], [y], s=95, marker="o", zorder=3, linewidths=1.4,
                   facecolors=NAVY if fixed else PAPER, edgecolors=INK if fixed else GRAY)
        if name:
            ax.text(x + 0.07, y, L["dots"][name], ha="left", va="center", fontsize=10.5,
                    color=INK if fixed else "#5E636C")
axes[0].set_ylabel(L["axis"], fontsize=12, loc="top", labelpad=4)

handles = [Line2D([], [], marker="o", ls="", ms=9, mfc=NAVY, mec=INK, mew=1.4, label=L["fixed"]),
           Line2D([], [], marker="o", ls="", ms=9, mfc=PAPER, mec=GRAY, mew=1.4, label=L["unfixed"])]
fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, fontsize=11.5, handletextpad=0.3,
           columnspacing=2.0)
fig.subplots_adjust(left=0.07, right=0.98, top=0.9, bottom=0.12, wspace=0.12)

out = ROOT / "assets" / "figures" / "ch10-limiar.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
