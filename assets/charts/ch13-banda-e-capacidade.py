"""ch13-banda-e-capacidade: bandwidth sets the speed, capacity sets what fits.

Content: book/pt/ch13.md, "A largura do cano" and "A biblioteca e o corredor"
(source post 2026/03/31 review-minisforum-ms-s1-max-amd-ai-max-395; private-notes
benchmarks/BENCHMARK_REPORT.md): RTX 5090 has 32 GB at ~1,792 GB/s; the Strix Halo
mini-PC has up to 128 GB of unified memory at ~256 GB/s (ratio ~7, measured speed
gap 6.7x). The 122B model with 81 GB of weights runs on the mini-PC (~19 tok/s)
and does not fit on the RTX 5090.
Tank areas are proportional to capacity (32 : 128) and the model block to 81 GB;
pipe widths are proportional to bandwidth (1,792 : 256).

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch13-banda-e-capacidade.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"rtx": "RTX 5090: 32 GB", "strix": "Strix Halo: até 128 GB", "wide": "cano de\n1.792 GB/s",
           "narrow": "cano de\n256 GB/s", "model": "modelo\nde 81 GB", "nofit": "não cabe",
           "tps": "tokens por segundo", "fast": "rápido, mas pequeno", "slow": "cabe tudo, mas devagar"},
    "en": {"rtx": "RTX 5090: 32 GB", "strix": "Strix Halo: up to 128 GB", "wide": "1,792 GB/s\npipe",
           "narrow": "256 GB/s\npipe", "model": "81 GB\nmodel", "nofit": "does not fit",
           "tps": "tokens per second", "fast": "fast, but small", "slow": "fits it all, but slow"},
}[LANG]

W, H = 6.4, 5.0
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

TW = 1.7                       # tank width
UNIT = 2.1 / 128               # tank height per GB (area ∝ capacity)
BW = 1.45                      # model block width
BH = 81 * UNIT * TW / BW       # block area ∝ 81 GB
PIPE_PER_GBS = 0.42 / 1792     # pipe width ∝ bandwidth
TANK_Y = 2.15


def panel(x0, gb, gbs, tank_label, pipe_label, fill_frac, model_inside, verdict):
    pw = 3.05
    ax.add_patch(FancyBboxPatch((x0, 0.1), pw, H - 0.2, boxstyle="round,pad=0,rounding_size=0.1",
                                fc=SAND, ec="none", zorder=0))
    cx = x0 + 0.25 + TW / 2
    th = gb * UNIT
    tx = cx - TW / 2
    # pipe from tank bottom down to the cup
    pw_ = max(gbs * PIPE_PER_GBS, 0.05)
    ax.add_patch(Rectangle((cx - pw_ / 2, 1.35), pw_, TANK_Y - 1.35, fc=TEAL, ec=INK, lw=1.2, zorder=2))
    ax.text(cx + max(pw_ / 2, 0.05) + 0.12, 1.78, pipe_label, ha="left", va="center", fontsize=10.5,
            linespacing=1.1)
    # tank
    ax.add_patch(Rectangle((tx, TANK_Y), TW, th, fc=PAPER, ec=INK, lw=1.6, zorder=3))
    if model_inside:
        ax.add_patch(Rectangle((cx - BW / 2, TANK_Y + 0.04), BW, BH, fc=AMBER, ec=INK, lw=1.3, zorder=4))
        ax.text(cx, TANK_Y + 0.04 + BH / 2, L["model"], ha="center", va="center", fontsize=11.5, zorder=5,
                linespacing=1.1)
        ax.text(cx, TANK_Y + th - 0.17, tank_label, ha="center", va="center",
                fontsize=10.5 if len(tank_label) <= 22 else 9.5,
                fontweight="semibold", zorder=5)
    else:
        ax.text(cx, TANK_Y + th / 2, tank_label, ha="center", va="center", fontsize=10.5,
                fontweight="semibold", zorder=5)
        by = TANK_Y + th + 0.32
        ax.add_patch(Rectangle((cx - BW / 2, by), BW, BH, fc=PAPER, ec=INK, lw=1.3, ls=(0, (3, 2)), zorder=4))
        ax.text(cx, by + BH / 2 + 0.12, L["model"], ha="center", va="center", fontsize=11.5, zorder=5,
                linespacing=1.1)
        ax.text(cx, by + 0.2, L["nofit"], ha="center", va="center", fontsize=10.5, style="italic", zorder=5)
        # an X between block and tank
        mx, my = cx, TANK_Y + th + 0.16
        for s in (1, -1):
            ax.plot([mx - 0.1, mx + 0.1], [my - 0.1 * s, my + 0.1 * s], color=INK, lw=2, zorder=5,
                    solid_capstyle="round")
    # cup
    top_w, bot_w, cy0, ch = 0.95, 0.7, 0.62, 0.68
    cup = [(cx - bot_w / 2, cy0), (cx + bot_w / 2, cy0), (cx + top_w / 2, cy0 + ch), (cx - top_w / 2, cy0 + ch)]
    lvl = ch * fill_frac
    wl = bot_w + (top_w - bot_w) * fill_frac
    ax.add_patch(Polygon([(cx - bot_w / 2, cy0), (cx + bot_w / 2, cy0), (cx + wl / 2, cy0 + lvl),
                          (cx - wl / 2, cy0 + lvl)], closed=True, fc=TEAL, ec="none", zorder=3))
    ax.add_patch(Polygon(cup, closed=True, fc="none", ec=INK, lw=1.6, zorder=4, joinstyle="round"))
    ax.text(cx + top_w / 2 + 0.12, cy0 + ch / 2, L["tps"], ha="left", va="center", fontsize=10, color="#5E636C",
            linespacing=1.1, wrap=True)
    ax.text(x0 + pw / 2, 0.3, verdict, ha="center", va="center", fontsize=12, fontweight="semibold")


L["tps"] = L["tps"].replace(" por ", "\npor ").replace(" per ", "\nper ")
panel(0.12, 32, 1792, L["rtx"], L["wide"], 0.85, False, L["fast"])
panel(3.27, 128, 256, L["strix"], L["narrow"], 0.15, True, L["slow"])

out = ROOT / "assets" / "figures" / "ch13-banda-e-capacidade.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
