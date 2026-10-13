"""ch13-especialistas: dense model vs mixture of experts (MoE).

Content: book/pt/ch13.md, "Muitos especialistas, poucos acordados" (source post
2026/03/31 review-minisforum-ms-s1-max-amd-ai-max-395; private-notes
benchmarks/FINDINGS.md; 2026/06/14 llm-benchmark-kimi-v2-7-code-glm-5-2-minimax-m3-local):
a dense model reads all its weights for every token; an MoE has a small router
that wakes only a few blocks per token (35B model, ~4B active), but the sleeping
blocks still occupy memory. Block counts are illustrative (16 blocks, 2 active).

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch13-especialistas.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"dense": "modelo denso", "moe": "MoE", "router": "roteador", "token": "token",
           "all": "todos os pesos lidos\na cada token", "few": "só alguns blocos trabalham",
           "mem": "todos ocupam memória"},
    "en": {"dense": "dense model", "moe": "MoE", "router": "router", "token": "token",
           "all": "all weights read\nfor every token", "few": "only a few blocks work",
           "mem": "all of them take up memory"},
}[LANG]

W, H = 6.4, 4.7
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

B, G = 0.36, 0.1
GW = 4 * B + 3 * G
GY0 = 1.75
ACTIVE = {(0, 3), (2, 3)}  # (col, row) of the blocks the router wakes


def arrow(p, q, lw=1.4, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=5,head_width=3", color=color, lw=lw,
                                 zorder=2, shrinkA=0, shrinkB=0))


def panel(x0, title, moe):
    pw = 3.05
    ax.add_patch(FancyBboxPatch((x0, 0.1), pw, H - 0.2, boxstyle="round,pad=0,rounding_size=0.1",
                                fc=SAND, ec="none", zorder=0))
    ax.text(x0 + 0.2, H - 0.36, title, ha="left", va="center", fontsize=13.5, fontweight="semibold")
    cx = x0 + pw / 2
    gx0 = cx - GW / 2
    tok = (cx, 1.12)
    if moe:
        ax.add_patch(FancyBboxPatch((gx0 - 0.14, GY0 - 0.14), GW + 0.28, GW + 0.28,
                                    boxstyle="round,pad=0,rounding_size=0.08", fc=PAPER, ec=INK, lw=1.2,
                                    ls=(0, (3, 2)), zorder=1))
    centers = {}
    for c in range(4):
        for r in range(4):
            x, y = gx0 + c * (B + G), GY0 + r * (B + G)
            on = (not moe) or (c, r) in ACTIVE
            ax.add_patch(Rectangle((x, y), B, B, fc=NAVY if on else PAPER, ec=INK if on else GRAY, lw=1.2,
                                   zorder=3))
            centers[(c, r)] = (x + B / 2, y + B / 2, on)
    arrow((cx, GY0 - (0.17 if moe else 0.04)), (tok[0], tok[1] + 0.22), lw=1.6)
    ax.add_patch(Circle(tok, 0.2, fc=PAPER, ec=INK, lw=1.4, zorder=4))
    ax.text(tok[0] + 0.3, tok[1], L["token"], ha="left", va="center", fontsize=11, zorder=5)
    if moe:
        ry = GY0 + GW + 0.42
        ax.add_patch(FancyBboxPatch((cx - 0.55, ry), 1.1, 0.36, boxstyle="round,pad=0,rounding_size=0.06",
                                    fc=AMBER, ec=INK, lw=1.3, zorder=4))
        ax.text(cx, ry + 0.18, L["router"], ha="center", va="center", fontsize=11, zorder=5)
        for k in sorted(ACTIVE):
            x, y, _ = centers[k]
            arrow((cx + (x - cx) * 0.35, ry - 0.01), (x, y + B / 2 + 0.03), lw=1.4)
        ax.text(cx, 0.6, L["few"], ha="center", va="center", fontsize=11, linespacing=1.1)
        ax.text(cx, 0.32, L["mem"], ha="center", va="center", fontsize=11, fontweight="semibold")
    else:
        ax.text(cx, 0.46, L["all"], ha="center", va="center", fontsize=11, linespacing=1.1)


panel(0.12, L["dense"], False)
panel(3.27, L["moe"], True)

out = ROOT / "assets" / "figures" / "ch13-especialistas.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
