"""ch19-camadas: the safeguards that make frequent deploys safe.

Content: book/pt/ch19.md, "As travas que tornam a velocidade segura" (source post
2026/09/22 parem-de-inventar-desculpas-e-facam-mais-deploy-a-premissa-mudou): automated
tests, a CI server running everything on every change, a suspicious automatic review,
a feature flag, a staging environment, and rollback "em minutos" plus monitoring "pra
saber quando algo quebrou".

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch19-camadas.py pt
"""
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
    "pt": {"change": "mudança", "tests": "testes\nautomatizados", "ci": "integração\ncontínua",
           "review": "revisão\nautomática", "flag": "feature flag", "staging": "staging", "prod": "produção",
           "rollback": "rollback: volta à versão\nanterior em minutos",
           "monitor": "o monitoramento avisa\nque algo quebrou"},
    "en": {"change": "change", "tests": "automated\ntests", "ci": "continuous\nintegration",
           "review": "automatic\nreview", "flag": "feature flag", "staging": "staging", "prod": "production",
           "rollback": "rollback: back to the previous\nversion in minutes",
           "monitor": "monitoring says\nsomething broke"},
}[LANG]

W, H = 6.4, 3.15
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

BW, BH = 1.32, 0.66

def box(cx, cy, fill, text, fs=11.5, weight="normal", ls="-"):
    ax.add_patch(FancyBboxPatch((cx - BW / 2, cy - BH / 2), BW, BH, boxstyle="round,pad=0,rounding_size=0.07",
                                fc=fill, ec=INK, lw=1.3, linestyle=ls, zorder=3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, fontweight=weight, zorder=4, linespacing=1.05,
            color=INK if fill in (SAND, PAPER, AMBER) else PAPER)

def arrow(p, q, rad=0.0, lw=1.5, ls="-", color=INK, z=2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=5,head_width=3", color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=z, shrinkA=0, shrinkB=0))

xs = [0.82, 2.4, 3.98, 5.56]
y1, y2 = 2.68, 1.33
# row 1, left to right
box(xs[0], y1, PAPER, L["change"], weight="semibold")
box(xs[1], y1, SAND, L["tests"])
box(xs[2], y1, SAND, L["ci"])
box(xs[3], y1, SAND, L["review"])
for i in range(3):
    arrow((xs[i] + BW / 2, y1), (xs[i + 1] - BW / 2, y1))
# turn down, row 2 right to left
box(xs[3], y2, SAND, L["flag"])
box(xs[2], y2, SAND, L["staging"])
box(xs[1], y2, NAVY, L["prod"], weight="semibold")
arrow((xs[3], y1 - BH / 2), (xs[3], y2 + BH / 2))
arrow((xs[3] - BW / 2, y2), (xs[2] + BW / 2, y2))
arrow((xs[2] - BW / 2, y2), (xs[1] + BW / 2, y2))

# monitoring: dotted, from production back to the start
arrow((xs[1] - BW / 2, y2), (xs[0], y1 - BH / 2), rad=-0.35, ls=(0, (2, 2)), lw=1.5)
ax.text(0.15, 0.5, L["monitor"], ha="left", va="center", fontsize=11, style="italic", linespacing=1.1)

# rollback: the one highlight, a U-turn under production
arrow((xs[1] + 0.42, y2 - BH / 2), (xs[1] - 0.42, y2 - BH / 2), rad=-1.1, lw=2.4, color=AMBER, z=5)
ax.text(xs[1] + 0.62, 0.54, L["rollback"], ha="left", va="center", fontsize=11, fontweight="semibold", linespacing=1.1)

out = ROOT / "assets" / "figures" / "ch19-camadas.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
