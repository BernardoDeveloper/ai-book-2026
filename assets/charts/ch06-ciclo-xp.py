"""ch06-ciclo-xp: the XP loop with an AI agent as the pair.

Content: book/pt/ch06.md, "Um par que nunca diz não" / "Quem pilota e quem navega"
(source posts 2026/02/16 vibe-code-do-zero-a-producao-em-6-dias and 2026/02/20
bastidores-do-the-m-akita-chronicles): the human asks for a small step and says what
and why; the agent plans and the human reviews the plan; the agent writes code and
test; continuous integration runs every test; the human reviews and commits. The
human navigates, the agent drives.

Drawn with matplotlib (not D2) because the loop must be a circle and D2's free
layouts cannot pin node positions.
Usage: uv run --with matplotlib python -I assets/charts/ch06-ciclo-xp.py pt
"""
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"s1": ("humano", "pede um passo pequeno\n(o quê e o porquê)"),
           "s2": ("agente planeja", "humano revisa o plano"),
           "s3": ("agente", "escreve código + teste"),
           "s4": ("integração contínua", "roda todos os testes"),
           "s5": ("humano", "revisa e grava o commit"),
           "fail": "teste falhou", "nav": "humano: navega", "pil": "agente: pilota"},
    "en": {"s1": ("human", "asks for one small step\n(the what and the why)"),
           "s2": ("agent plans", "human reviews the plan"),
           "s3": ("agent", "writes code + test"),
           "s4": ("continuous integration", "runs every test"),
           "s5": ("human", "reviews and commits"),
           "fail": "test failed", "nav": "human: navigates", "pil": "agent: drives"},
}[LANG]

W, H = 6.4, 5.2
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

CX, CY, RX, RY = 3.2, 2.72, 2.12, 1.85
BW, LINE = 2.12, 0.25
STEPS = [("s1", 90, NAVY), ("s2", 18, TEAL), ("s3", -50, TEAL), ("s4", -130, SAND), ("s5", 162, NAVY)]
boxes = {}
for i, (key, ang, fill) in enumerate(STEPS, start=1):
    x = CX + RX * math.cos(math.radians(ang))
    y = CY + RY * math.sin(math.radians(ang))
    fg = INK if fill == SAND else PAPER
    head, body = L[key]
    lines = [f"{i}. {head}"] + body.split("\n")
    bh = 0.32 + LINE * len(lines)
    p = FancyBboxPatch((x - BW / 2, y - bh / 2), BW, bh, boxstyle="round,pad=0,rounding_size=0.08",
                       fc=fill, ec=INK, lw=1.4, zorder=3)
    ax.add_patch(p)
    boxes[key] = p
    top = y + LINE * (len(lines) - 1) / 2
    for j, line in enumerate(lines):
        ax.text(x, top - j * LINE, line, ha="center", va="center", zorder=4, color=fg,
                fontsize=12.5 if j == 0 else 11.5, fontweight="semibold" if j == 0 else "normal")

def arrow(a, b, rad, **kw):
    style = dict(arrowstyle="-|>,head_length=7,head_width=4", color=INK, lw=1.8,
                 shrinkA=4, shrinkB=4, connectionstyle=f"arc3,rad={rad}", zorder=2)
    style.update(kw)
    ax.add_patch(FancyArrowPatch(boxes[a].get_center() if False else _c(a), _c(b),
                                 patchA=boxes[a], patchB=boxes[b], **style))

def _c(k):
    b = boxes[k]
    return (b.get_x() + b.get_width() / 2, b.get_y() + b.get_height() / 2)

for a, b in [("s1", "s2"), ("s2", "s3"), ("s3", "s4"), ("s4", "s5"), ("s5", "s1")]:
    arrow(a, b, -0.28)
# failed test: back from CI to the agent, under the loop, dashed
arrow("s4", "s3", 0.55, linestyle=(0, (4, 3)), lw=1.4)
ax.text(CX, 0.3, L["fail"], ha="center", va="center", fontsize=11.5, style="italic")

# role key in the middle of the loop
for dy, fill, txt in [(0.25, NAVY, L["nav"]), (-0.25, TEAL, L["pil"])]:
    ax.add_patch(FancyBboxPatch((CX - 0.72, CY + dy - 0.1), 0.2, 0.2, boxstyle="round,pad=0,rounding_size=0.03",
                                fc=fill, ec=INK, lw=1.0))
    ax.text(CX - 0.42, CY + dy, txt, ha="left", va="center", fontsize=11.5)

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch06-ciclo-xp.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
