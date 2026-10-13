"""ch05-revezamento: five reviewers in a row; the pile of problems shrinks but never empties.

Data: book/pt/ch05.md ("Cinco revisores e nenhum ponto final"), from
akitaonrails.com 2026/01/29/vibe-code-qual-llm-é-a-melhor-vamos-falar-a-real.
Order of the relay: Opus 4.5, GPT-5.2 Codex, Kimi K2.5, Gemini 3 Pro Preview,
MiniMax M2.1, on top of the code GLM 4.7 left. Each found something the others
missed; Opus (improved dead code), GPT (started re-implementing the removed
crypto), Kimi (brought back the cleanup routine) and Gemini (kept and optimised
it) also created work; MiniMax is not reported creating any. The counts are
illustrative: the chapter gives no numbers, only that the pile never reached zero.

Usage: uv run --with matplotlib python -I assets/charts/ch05-revezamento.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER, RUST = ("#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B",
                                                   "#E9DFC9", "#FBF9F4", "#B5523B")
MUTED = "#5E636C"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK, "hatch.color": PAPER,
                     "hatch.linewidth": 1.2})

L = {
    "pt": {"start": "código\ndo GLM", "found": "problemas encontrados", "created": "problemas criados",
           "left": "ainda no código", "sobra": "sobra"},
    "en": {"start": "GLM's\ncode", "found": "problems found", "created": "problems created",
           "left": "still in the code", "sobra": "left over"},
}[LANG]
# (name, found this round, created this round); starting pile = 10 (illustrative)
RELAY = [("Opus\n4.5", 4, 1), ("GPT-5.2\nCodex", 3, 1), ("Kimi\nK2.5", 2, 1), ("Gemini 3\nPro Preview", 2, 1),
         ("MiniMax\nM2.1", 1, 0)]
START = 10

fig, ax = plt.subplots(figsize=(6.8, 4.15), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 12.6)
ax.set_ylim(-0.35, 7.35)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)

S, STEP, BASE = 0.4, 0.45, 0.85
COLW = 2.05


def square(x, y, kind):
    if kind == "left":
        ax.add_patch(FancyBboxPatch((x, y), S, S, boxstyle="round,pad=0,rounding_size=0.05", fc=NAVY, ec=INK, lw=0.9))
    elif kind == "created":
        ax.add_patch(FancyBboxPatch((x, y), S, S, boxstyle="round,pad=0,rounding_size=0.05", fc=RUST, ec=INK, lw=0.9,
                                    hatch="////"))
    else:  # found and removed
        ax.add_patch(FancyBboxPatch((x, y), S, S, boxstyle="round,pad=0,rounding_size=0.05", fc=PAPER, ec=GRAY,
                                    lw=1.0, linestyle=(0, (2, 1.5))))


def stack(cx, kinds):
    for i, k in enumerate(kinds):
        square(cx - S / 2, BASE + i * STEP, k)


# column 0: the pile the relay starts from
cx0 = 0.75
stack(cx0, ["left"] * START)
ax.text(cx0, BASE + START * STEP + 0.1, L["start"], ha="center", va="bottom", fontsize=10.5, style="italic",
        linespacing=1.1)

remaining = START
for i, (name, found, created) in enumerate(RELAY):
    cx = 2.45 + i * COLW
    kept = remaining - found
    stack(cx, ["left"] * kept + ["created"] * created + ["found"] * found)
    remaining = kept + created
    # reviewer box under the pile
    ax.add_patch(FancyBboxPatch((cx - 0.88, BASE - 1.15), 1.76, 0.95, boxstyle="round,pad=0,rounding_size=0.15",
                                fc=SAND, ec=INK, lw=1.4))
    ax.text(cx, BASE - 0.675, name, ha="center", va="center", fontsize=10, fontweight="semibold", linespacing=1.1)
    prev = cx0 + 0.35 if i == 0 else cx - COLW + 0.92
    ax.add_patch(FancyArrowPatch((prev, BASE - 0.675), (cx - 0.92, BASE - 0.675), arrowstyle="-|>",
                                 mutation_scale=12, lw=1.5, color=INK, shrinkA=0, shrinkB=0))

# "sobra" bracket on the last pile
lx = 2.45 + 4 * COLW + 0.35
top = BASE + remaining * STEP - 0.05
ax.plot([lx, lx + 0.15, lx + 0.15, lx], [BASE, BASE, top, top], color=INK, lw=1.3, solid_capstyle="round")
ax.text(lx + 0.3, (BASE + top) / 2, L["sobra"], ha="left", va="center", fontsize=12, fontweight="semibold")

# legend (top right, where the piles are short)
for j, (kind, text) in enumerate((("found", L["found"]), ("created", L["created"]), ("left", L["left"]))):
    y = 6.85 - j * 0.6
    square(7.6, y - S / 2, kind)
    ax.text(8.15, y, text, ha="left", va="center", fontsize=11)

buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.
out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch05-revezamento.png"
out.parent.mkdir(parents=True, exist_ok=True)
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
