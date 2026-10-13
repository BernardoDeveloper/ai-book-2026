"""ch15-camadas: layers of protection around your files.

Content: book/pt/ch15.md, "Camadas", "O botão de desfazer", "A cópia que mora em
outro lugar" and "Agente não entra em produção" (source posts 2026/07/11
como-me-precaver-pros-meus-agentes-nao-apagarem-minhas-coisas and 2026/10/06
desastre-no-meu-nas-como-quase-perdi-90-tb-de-dados): the jail (sandbox) limits
what the agent sees; a snapshot undoes the recent mistake ("apagou às três da
tarde, o snapshot das duas ainda tem tudo"); the external backup lives on another
device (nightly copy) and survives the disk; production stays out of reach and a
human promotes changes. A wrong command that gets past the first ring is stopped
by the second, as with the eleven albums deleted outside any jail.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch15-camadas.py pt
"""
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle, FancyArrowPatch, Polygon
from matplotlib import patheffects as pe

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"files": "seus\narquivos", "wrong": "comando\nerrado",
           "rings": ["sandbox", "snapshot", "backup externo", "produção"],
           "notes": ["o agente só vê\no projeto", "volta ao estado\nde uma hora atrás",
                     "outro aparelho,\ncópia da noite\nanterior", "um humano aprova"]},
    "en": {"files": "your\nfiles", "wrong": "wrong\ncommand",
           "rings": ["sandbox", "snapshot", "external backup", "production"],
           "notes": ["the agent only sees\nthe project", "back to how it was\nan hour ago",
                     "another device,\nlast night's copy", "a human approves"]},
}[LANG]

W, H = 6.4, 5.0
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

C = (2.3, 2.5)
R0 = 0.5
STEP = 0.42
FILLS = [TEAL, SAND, GRAY, NAVY]          # sandbox, snapshot, backup, production (≥ 20 L* apart)
TXT = [PAPER, INK, PAPER, PAPER]

for i in reversed(range(4)):
    ax.add_patch(Circle(C, R0 + STEP * (i + 1), fc=FILLS[i], ec=INK, lw=1.4, zorder=1 + (3 - i) * 0.01))
ax.add_patch(Circle(C, R0, fc=PAPER, ec=INK, lw=1.4, zorder=2))

# ring names along the top of each band
for i, name in enumerate(L["rings"]):
    r = R0 + STEP * (i + 0.5)
    ax.text(C[0], C[1] + r, name, ha="center", va="center", fontsize=10, fontweight="semibold",
            color=TXT[i], zorder=5)

# notes on the right, horizontal leader lines from a dot inside each band
ys = [3.05, 2.3, 1.55, 0.8]
for i, y in enumerate(ys):
    r = R0 + STEP * (i + 0.5)
    px = C[0] + math.sqrt(r * r - (y - C[1]) ** 2)
    tx = 4.75
    ax.plot([px, tx - 0.1], [y, y], color=INK, lw=0.9, zorder=6,
            path_effects=[pe.Stroke(linewidth=3.2, foreground=PAPER), pe.Normal()])
    ax.add_patch(Circle((px, y), 0.045, fc=INK, ec=PAPER, lw=1.2, zorder=7))
    ax.text(tx, y, L["notes"][i], ha="left", va="center", fontsize=10, linespacing=1.1, zorder=6)

# the file icon at the centre
fx, fy, fw, fh, fold = C[0] - 0.12, C[1] + 0.02, 0.24, 0.29, 0.08
ax.add_patch(Polygon([(fx, fy), (fx + fw, fy), (fx + fw, fy + fh - fold), (fx + fw - fold, fy + fh), (fx, fy + fh)],
                     closed=True, fc=PAPER, ec=INK, lw=1.3, zorder=4, joinstyle="round"))
ax.text(C[0], C[1] - 0.2, L["files"], ha="center", va="center", fontsize=9.5, linespacing=1.0, zorder=4)

# a wrong command crosses the sandbox and is stopped at the snapshot ring
a = math.radians(212)
r1, r2 = R0 + 0.01, R0 + STEP * 1.45
p = (C[0] + r1 * math.cos(a), C[1] + r1 * math.sin(a))
q = (C[0] + r2 * math.cos(a), C[1] + r2 * math.sin(a))
ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-", color=INK, lw=2.6, zorder=8, shrinkA=0, shrinkB=0,
                             capstyle="round"))
# stop bar, perpendicular to the arrow
nx, ny = -math.sin(a), math.cos(a)
ax.plot([q[0] - nx * 0.2, q[0] + nx * 0.2], [q[1] - ny * 0.2, q[1] + ny * 0.2], color=AMBER, lw=6,
        solid_capstyle="butt", zorder=9)
ax.plot([q[0] - nx * 0.2, q[0] + nx * 0.2], [q[1] - ny * 0.2, q[1] + ny * 0.2], color=INK, lw=1.0,
        zorder=10)
ax.text(C[0] - 0.1, C[1] - (R0 + STEP * 1.42), L["wrong"].replace("\n", " "), ha="center", va="center",
        fontsize=10, style="italic", zorder=6)

out = ROOT / "assets" / "figures" / "ch15-camadas.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
