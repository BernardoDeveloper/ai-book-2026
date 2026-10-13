"""apmecanica-tres-etapas: from document continuer to assistant, three training stages.

Content: book/pt/apmecanica.md, "Da enciclopédia ao assistente", "Exemplos escritos
por gente", "Notas dadas por gente": pre-training on a huge pile of text yields a
document continuer; instruction tuning on thousands of question-and-answer examples
written by hired people teaches the assistant format; in RLHF people rank several
answers, a second model (an automatic judge) learns to predict their scores and the
main model learns what pleases. Then the knobs are frozen into a file (inference
only reads them). Stack sizes shrink from stage 1 to 3 on purpose.

Usage: uv run --with matplotlib --with numpy python -I assets/charts/apmecanica-tres-etapas.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon, Rectangle, Arc

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"s1": "1. pré-treino", "s2": "2. ajuste por\ninstruções", "s3": "3. RLHF",
           "o1": "continuador de\ndocumentos", "o2": "responde no formato\nde assistente", "o3": "aprende o\nque agrada",
           "judge": "juiz\nautomático", "frozen": "pesos\ncongelados", "q": "P", "a": "R"},
    "en": {"s1": "1. pre-training", "s2": "2. instruction\ntuning", "s3": "3. RLHF",
           "o1": "document\ncontinuer", "o2": "answers in\nassistant format", "o3": "learns what\npleases",
           "judge": "automatic\njudge", "frozen": "frozen\nweights", "q": "Q", "a": "A"},
}[LANG]

W, H = 6.4, 3.7
Y0 = 0.28  # crop the empty strip under the tags
fig = plt.figure(figsize=(W, H - Y0), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(Y0, H); ax.set_aspect("equal"); ax.axis("off")

BELT_Y = 1.25  # top surface of the conveyor belt

# conveyor belt with rollers
ax.add_patch(FancyBboxPatch((0.12, BELT_Y - 0.2), 5.25, 0.2, boxstyle="round,pad=0,rounding_size=0.1",
                            fc=GRAY, ec=INK, lw=1.4, zorder=1))
for rx in [0.3 + 0.45 * i for i in range(12)]:
    ax.add_patch(Circle((rx, BELT_Y - 0.1), 0.055, fc=PAPER, ec=INK, lw=0.9, zorder=2))
for lx in (0.3, 5.15):
    ax.plot([lx, lx], [BELT_Y - 0.2, 0.92], color=INK, lw=1.4, zorder=0.5)

def stack(cx, base, n, w=0.42, h=0.065, lines=True):
    """A pile of sheets: n thin rectangles."""
    for i in range(n):
        off = 0.02 * ((i * 7) % 3 - 1)
        ax.add_patch(Rectangle((cx - w / 2 + off, base + i * h), w, h, fc=PAPER, ec=INK, lw=0.8, zorder=3 + i * 0.01))
    return base + n * h

def station(x0, w, title):
    ax.add_patch(FancyBboxPatch((x0, BELT_Y + 0.02), w, 2.3, boxstyle="round,pad=0,rounding_size=0.08",
                                fc=SAND, ec="none", zorder=0.2))
    ax.text(x0 + w / 2, BELT_Y + 2.12, title, ha="center", va="top", fontsize=12.5, fontweight="semibold",
            linespacing=1.05, zorder=6)

def tag(cx, text):
    ax.text(cx, 0.82, text, ha="center", va="top", fontsize=11, style="italic", linespacing=1.1)

def arrow(p, q, lw=1.6, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=INK, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", zorder=5, shrinkA=0, shrinkB=0))

def person(cx, base, s=1.0):
    ax.add_patch(Circle((cx, base + 0.26 * s), 0.065 * s, fc=NAVY, ec=INK, lw=1.0, zorder=5))
    ax.add_patch(FancyBboxPatch((cx - 0.08 * s, base), 0.16 * s, 0.17 * s,
                                boxstyle=f"round,pad=0,rounding_size={0.06 * s}", fc=NAVY, ec=INK, lw=1.0, zorder=5))

# ---- station 1: huge stack of text
station(0.12, 1.55, L["s1"])
top = stack(0.9, BELT_Y + 0.02, 22, w=0.62)
tag(0.9, L["o1"])

# ---- station 2: smaller stack of Q/A cards written by people
station(1.8, 1.55, L["s2"])
top2 = stack(2.38, BELT_Y + 0.02, 8, w=0.5)
for i, (lbl, y) in enumerate([(L["q"], top2 + 0.36), (L["a"], top2 + 0.08)]):
    ax.add_patch(FancyBboxPatch((2.18, y), 0.4, 0.22, boxstyle="round,pad=0,rounding_size=0.04",
                                fc=PAPER if i == 0 else TEAL, ec=INK, lw=1.0, zorder=5))
    ax.text(2.38, y + 0.11, lbl, ha="center", va="center", fontsize=10.5, fontweight="semibold",
            color=INK if i == 0 else PAPER, zorder=6)
person(2.9, BELT_Y + 0.05)
person(3.15, BELT_Y + 0.05)
tag(2.57, L["o2"])

# ---- station 3: people rank answers A-D, a judge gives scores
station(3.48, 1.89, L["s3"])
stack(3.75, BELT_Y + 0.02, 3, w=0.34)
# ranked answers, a person ordering them, the judge that learns their scores
for i, lab in enumerate("ABCD"):
    y = BELT_Y + 1.5 - i * 0.24
    ax.add_patch(FancyBboxPatch((3.62, y), 0.3, 0.19, boxstyle="round,pad=0,rounding_size=0.04",
                                fc=PAPER, ec=INK, lw=0.9, zorder=5))
    ax.text(3.77, y + 0.095, lab, ha="center", va="center", fontsize=10, zorder=6)
person(4.13, BELT_Y + 1.0, 0.9)
person(4.13, BELT_Y + 0.6, 0.9)
ax.add_patch(FancyBboxPatch((4.45, BELT_Y + 0.88), 0.86, 0.6, boxstyle="round,pad=0,rounding_size=0.06",
                            fc=NAVY, ec=INK, lw=1.3, zorder=5))
ax.text(4.88, BELT_Y + 1.18, L["judge"], ha="center", va="center", fontsize=10.5, color=PAPER, zorder=6, linespacing=1.05)
arrow((4.26, BELT_Y + 1.18), (4.43, BELT_Y + 1.18), lw=1.3)
import math
for k in range(3):
    sx = 4.68 + k * 0.2
    pts = []
    for j in range(10):
        r = 0.075 if j % 2 == 0 else 0.032
        a = math.pi / 2 + j * math.pi / 5
        pts.append((sx + r * math.cos(a), BELT_Y + 0.62 + r * math.sin(a)))
    ax.add_patch(Polygon(pts, closed=True, fc=PAPER if k == 2 else INK, ec=INK, lw=0.8, zorder=5))
tag(4.42, L["o3"])

# ---- end of the belt: a locked file (amber padlock = the one highlight)
fx, fy = 5.55, BELT_Y - 0.15
fw, fh = 0.6, 0.78
ax.add_patch(Polygon([(fx, fy), (fx + fw, fy), (fx + fw, fy + fh - 0.18), (fx + fw - 0.18, fy + fh), (fx, fy + fh)],
                     closed=True, fc=PAPER, ec=INK, lw=1.4, zorder=4))
ax.add_patch(Polygon([(fx + fw - 0.18, fy + fh), (fx + fw - 0.18, fy + fh - 0.18), (fx + fw, fy + fh - 0.18)],
                     closed=True, fc=SAND, ec=INK, lw=1.1, zorder=4.5))
for k in range(3):
    ax.plot([fx + 0.1, fx + 0.38], [fy + fh - 0.16 - k * 0.11] * 2, color=GRAY, lw=1.2, zorder=4.6)
lx, ly = fx + fw / 2, fy + 0.1
ax.add_patch(Arc((lx, ly + 0.2), 0.2, 0.24, theta1=0, theta2=180, color=INK, lw=2.0, zorder=5.5))
ax.plot([lx - 0.1, lx - 0.1], [ly + 0.13, ly + 0.2], color=INK, lw=2.0, zorder=5.5)
ax.plot([lx + 0.1, lx + 0.1], [ly + 0.13, ly + 0.2], color=INK, lw=2.0, zorder=5.5)
ax.add_patch(FancyBboxPatch((lx - 0.15, ly - 0.02), 0.3, 0.2, boxstyle="round,pad=0,rounding_size=0.03",
                            fc=AMBER, ec=INK, lw=1.3, zorder=6))
arrow((5.38, BELT_Y + 0.1), (5.53, BELT_Y + 0.1), lw=1.4)
ax.text(fx + fw / 2, 0.82, L["frozen"], ha="center", va="top", fontsize=11, fontweight="semibold", linespacing=1.1)

out = ROOT / "assets" / "figures" / "apmecanica-tres-etapas.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
