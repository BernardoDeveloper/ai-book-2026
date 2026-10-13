"""ch09-quatro-partes: the four parts of a good request.

Content: book/pt/ch09.md, "A estrutura por trás" (source post 2026/04/15
como-falar-com-o-claude-code-efetivamente): 1. o que eu quero; 2. como eu quero que
seja feito; 3. o que eu não quero ("a parte que mais gente pula e a mais
importante"); 4. como a gente sabe que deu certo. When the task can't be done under
those constraints, the model says so ("com essas restrições, não consigo seguir").

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch09-quatro-partes.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"card": "pedido", "parts": ["o que eu quero", "como", "o que eu não quero", "como saber que deu certo"],
           "skip": "a parte que mais gente pula", "agent": "agente", "nogo": "e se não der?"},
    "en": {"card": "request", "parts": ["what I want", "how", "what I don't want", "how to tell it worked"],
           "skip": "the part most people skip", "agent": "agent", "nogo": "what if it can't be done?"},
}[LANG]

W, H = 6.4, 3.7
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

def rbox(x, y, w, h, fill, r=0.07, lw=1.4, z=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fill, ec=INK, lw=lw, zorder=z))

# the request card
cx, cy, cw = 0.25, 0.2, 3.55
bh, gap = 0.56, 0.1
ch = 0.5 + 4 * bh + 5 * gap
rbox(cx, cy, cw, ch, SAND, r=0.1)
ax.text(cx + 0.2, cy + ch - 0.27, L["card"], ha="left", va="center", fontsize=13.5, fontweight="semibold")
for i, part in enumerate(L["parts"]):
    y = cy + ch - 0.5 - (i + 1) * (bh + gap) + 0.0
    hl = i == 2
    rbox(cx + 0.15, y, cw - 0.3, bh, AMBER if hl else PAPER, r=0.06, lw=1.8 if hl else 1.2, z=3.2)
    ax.add_patch(Circle((cx + 0.47, y + bh / 2), 0.17, fc=NAVY, ec=INK, lw=1.0, zorder=4))
    ax.text(cx + 0.47, y + bh / 2, str(i + 1), ha="center", va="center", fontsize=11.5, color=PAPER,
            fontweight="semibold", zorder=5)
    ax.text(cx + 0.78, y + bh / 2, part, ha="left", va="center", fontsize=12.5, zorder=5,
            fontweight="semibold" if hl else "normal")
    if hl:
        hy = y + bh / 2
# note for the highlighted band, outside the card, pointing in
ax.annotate(L["skip"].replace(" mais", "\nmais") if LANG == "pt" else L["skip"].replace(" most", "\nmost"),
            xy=(cx + cw + 0.04, hy), xytext=(cx + cw + 0.45, hy), fontsize=11.5, style="italic",
            ha="left", va="center", linespacing=1.1,
            arrowprops=dict(arrowstyle="-|>,head_length=0.45,head_width=0.22", color=INK, lw=1.2,
                            shrinkA=3, shrinkB=0))

# the agent
axc, ayc = 5.0, 2.95
rbox(axc - 0.36, ayc - 0.31, 0.72, 0.62, GRAY, r=0.13)
for dx in (-0.14, 0.14):
    ax.add_patch(Circle((axc + dx, ayc + 0.03), 0.065, fc=PAPER, ec="none", zorder=4))
ax.plot([axc, axc], [ayc + 0.31, ayc + 0.45], color=INK, lw=1.4, zorder=3)
ax.add_patch(Circle((axc, ayc + 0.48), 0.05, fc=INK, zorder=3))
ax.text(axc + 0.48, ayc, L["agent"], ha="left", va="center", fontsize=12)

def arrow(a, b, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>,head_length=6,head_width=3.5", color=INK, lw=1.7,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2, shrinkA=0, shrinkB=0))

arrow((cx + cw + 0.05, ayc + 0.05), (axc - 0.45, ayc + 0.05))
# the way back: the agent says when it can't
bx, by, bw, bh2 = 4.3, 1.9, 1.85, 0.5
ax.add_patch(Polygon([(axc - 0.12, by + bh2 - 0.05), (axc + 0.12, by + bh2 - 0.05), (axc, ayc - 0.36)], closed=True,
                     fc=PAPER, ec=INK, lw=1.3, zorder=4.9))
ax.add_patch(FancyBboxPatch((bx, by), bw, bh2, boxstyle="round,pad=0,rounding_size=0.2", fc=PAPER, ec=INK,
                            lw=1.3, zorder=5))
ax.add_patch(Polygon([(axc - 0.1, by + bh2 - 0.08), (axc + 0.1, by + bh2 - 0.08), (axc, by + bh2 + 0.03)], closed=True,
                     fc=PAPER, ec="none", zorder=5.5))
ax.text(bx + bw / 2, by + bh2 / 2, L["nogo"], ha="center", va="center", fontsize=12.5, style="italic", zorder=6)
arrow((bx - 0.05, by + bh2 / 2), (cx + cw + 0.05, by + bh2 / 2), ls=(0, (4, 3)))

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch09-quatro-partes.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
