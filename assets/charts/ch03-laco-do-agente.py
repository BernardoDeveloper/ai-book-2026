"""ch03-laco-do-agente: the agent loop (model thinks, asks for a tool, harness runs it, result returns).

Data: none. Schematic of book/pt/ch03.md ("O laço"): the model only writes
text; the harness recognises the tool request, really executes it (compile,
run a test, read a file) and pastes the result back as text; the model decides
again, until the result matches the request. "O modelo só escreve texto. Quem
tem as mãos é o harness."

Usage: uv run --with matplotlib python -I assets/charts/ch03-laco-do-agente.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
MUTED = "#5E636C"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK})

L = {
    "pt": {"pensa": "o modelo pensa", "pede": "pede uma\nferramenta", "executa": "o harness executa",
           "volta": "o resultado volta\ncomo texto", "tarefa": "tarefa", "pronto": "pronto",
           "bate": "quando o resultado\nbate com o pedido",
           "tools": ["compilar", "rodar teste", "ler arquivo"],
           "leg_m": "modelo: só escreve texto", "leg_h": "harness: tem as mãos"},
    "en": {"pensa": "the model thinks", "pede": "asks for\na tool", "executa": "the harness runs it",
           "volta": "the result\ncomes back as text", "tarefa": "task", "pronto": "done",
           "bate": "when the result\nmatches the request",
           "tools": ["compile", "run tests", "read a file"],
           "leg_m": "model: only writes text", "leg_h": "harness: has the hands"},
}[LANG]

fig, ax = plt.subplots(figsize=(6.6, 4.9), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 12.4)
ax.set_ylim(-1.0, 8.2)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)

CX, CY, R = 5.3, 4.1, 2.75


def pt(deg, r=R):
    a = math.radians(deg)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def fit_text(t, max_w, min_size=10.0):
    """Shrink a text artist until it fits max_w (data units). Labels change
    length between languages; only the type size gives way, never below
    min_size (10 pt here is ~7 pt once the 6.6 in figure is set at text width)."""
    fig.canvas.draw()
    inv = ax.transData.inverted()
    while t.get_fontsize() > min_size:
        bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
        (x0, _), (x1, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
        if x1 - x0 <= max_w:
            break
        t.set_fontsize(t.get_fontsize() - 0.25)
    return t


def station(deg, text, fc, w, h=0.95):
    x, y = pt(deg)
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.2", fc=fc,
                                ec=INK, lw=1.6, zorder=4))
    fit_text(ax.text(x, y, text, ha="center", va="center", fontsize=12, fontweight="semibold", color=PAPER, zorder=5,
                     linespacing=1.15), w - 0.3)


def arc(a0, a1):  # clockwise arc on the ring from angle a0 to a1 (degrees)
    phi = math.radians(abs(a0 - a1))
    rad = (1 - math.cos(phi / 2)) / (2 * math.sin(phi / 2)) * 2
    ax.add_patch(FancyArrowPatch(pt(a0), pt(a1), arrowstyle="-|>", mutation_scale=17, lw=2.2, color=INK,
                                 connectionstyle=f"arc3,rad={-rad}", shrinkA=0, shrinkB=0, zorder=3))


# ring segments, clockwise: top -> right -> bottom -> left -> top
for a0, a1 in ((90 - 33, 0 + 22), (0 - 22, -90 + 40), (-90 - 40, -180 + 22), (180 - 22, 90 + 33)):
    arc(a0, a1)

station(90, L["pensa"], NAVY, 3.1)
station(0, L["pede"], NAVY, 2.3, 1.15)
station(-90, L["executa"], TEAL, 3.3)
station(180, L["volta"], TEAL, 3.2, 1.15)

# centre
ax.add_patch(Circle((CX, CY), 0.95, fc=SAND, ec=INK, lw=1.5, zorder=2))
ax.text(CX, CY, L["tarefa"], ha="center", va="center", fontsize=13, fontweight="semibold", zorder=3)

# tools the harness can run
bx, by = pt(-90)
tw = [1.55, 1.85, 1.85]
gap = 0.18
x = bx - (sum(tw) + gap * 2) / 2
for w, t in zip(tw, L["tools"]):
    ax.add_patch(FancyBboxPatch((x, by - 1.35), w, 0.58, boxstyle="round,pad=0,rounding_size=0.12", fc=SAND, ec=INK,
                                lw=1.1, zorder=4))
    ax.text(x + w / 2, by - 1.06, t, ha="center", va="center", fontsize=10.5, zorder=5)
    ax.plot([x + w / 2, x + w / 2], [by - 0.77, by - 0.48], color=INK, lw=1.0, zorder=3)
    x += w + gap

# exit
tx, ty = pt(90)
PX, PY = 10.2, ty + 0.15
ax.add_patch(FancyArrowPatch((tx + 1.6, ty + 0.05), (PX - 0.9, PY), arrowstyle="-|>", mutation_scale=17, lw=2.2,
                             color=INK, shrinkA=0, shrinkB=0, zorder=3))
ax.add_patch(FancyBboxPatch((PX - 0.85, PY - 0.45), 1.9, 0.9, boxstyle="round,pad=0,rounding_size=0.2", fc=AMBER,
                            ec=INK, lw=1.6, zorder=4))
ax.text(PX + 0.1, PY, L["pronto"], ha="center", va="center", fontsize=12.5, fontweight="semibold", zorder=5)
ax.text(PX + 0.1, PY - 0.7, L["bate"], ha="center", va="top", fontsize=10.5, style="italic", color=MUTED,
        linespacing=1.2)

# legend: who does what
for i, (fc, key) in enumerate(((NAVY, "leg_m"), (TEAL, "leg_h"))):
    lx = 1.3 + i * 5.3
    ax.add_patch(FancyBboxPatch((lx, -0.75), 0.42, 0.42, boxstyle="round,pad=0,rounding_size=0.08", fc=fc, ec=INK,
                                lw=1.1))
    ax.text(lx + 0.6, -0.54, L[key], ha="left", va="center", fontsize=11.5)

buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.
out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch03-laco-do-agente.png"
out.parent.mkdir(parents=True, exist_ok=True)
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
