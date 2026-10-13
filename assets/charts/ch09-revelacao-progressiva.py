"""ch09-revelacao-progressiva: progressive disclosure of skills.

Content: book/pt/ch09.md, "Prompts com cicatriz" (source post 2026/09/17
falando-um-pouco-sobre-minhas-skills-de-ia): at session start only each skill's name
and description enter the agent's instructions; the body is loaded only when the agent
decides to use that skill ("progressive disclosure"). Same desk metaphor as ch02
(the context window as a desk). Skill names are generic examples.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch09-revelacao-progressiva.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"desk": "mesa (janela de contexto)", "drawer": "gaveta", "names": "só nome e descrição",
           "loaded": "conteúdo carregado\nsob demanda", "skills": ["auditar", "publicar versão", "revisar texto"]},
    "en": {"desk": "desk (context window)", "drawer": "drawer", "names": "name and description only",
           "loaded": "content loaded\non demand", "skills": ["audit", "release", "review text"]},
}[LANG]
PICK = 2

W, H = 6.4, 4.5
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

def rbox(x, y, w, h, fill, r=0.06, lw=1.3, ls="-", z=3, ec=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fill, ec=ec,
                                lw=lw, linestyle=ls, zorder=z))

def folder(x, y, w, h, fill=SAND, ls="-", z=3):
    t = 0.38 * w
    ax.add_patch(Polygon([(x, y), (x + w, y), (x + w, y + h), (x + t + 0.08, y + h), (x + t, y + h + 0.1),
                          (x, y + h + 0.1)], closed=True, fc=fill, ec=INK, lw=1.2, linestyle=ls, zorder=z,
                         joinstyle="round"))

# desk
dy0 = 1.75
rbox(0.1, dy0, W - 0.2, H - dy0 - 0.1, SAND, r=0.1, lw=0, z=0, ec="none")
ax.text(0.3, H - 0.35, L["desk"], ha="left", va="center", fontsize=13.5, fontweight="semibold")
# name tags (one per skill) + "..."
xs = [0.3, 1.55, 3.4]
widths = [1.05, 1.65, 1.6]
ty = H - 0.9
for i, (x, w, name) in enumerate(zip(xs, widths, L["skills"])):
    rbox(x, ty - 0.2, w, 0.4, PAPER, r=0.2, lw=2.0 if i == PICK else 1.2)
    ax.text(x + w / 2, ty, name, ha="center", va="center", fontsize=12, fontweight="semibold" if i == PICK else "normal", zorder=4)
ax.text(5.25, ty, "…", ha="center", va="center", fontsize=16)
ax.text(0.3, ty - 0.45, L["names"], ha="left", va="center", fontsize=11.5, style="italic")
# the opened skill on the desk
ox, oy, ow, oh = 3.4, dy0 + 0.18, 2.6, 1.25
rbox(ox, oy, ow, oh, AMBER, r=0.06, lw=1.4, z=3)
ax.text(ox + 0.15, oy + oh - 0.22, L["skills"][PICK], ha="left", va="center", fontsize=12, fontweight="semibold", zorder=4)
for k, frac in enumerate((0.85, 0.7, 0.9, 0.55)):
    yy = oy + oh - 0.5 - k * 0.2
    ax.plot([ox + 0.15, ox + 0.15 + (ow - 0.3) * frac], [yy, yy], color=INK, lw=1.0, zorder=4, solid_capstyle="round")
ax.text(ox - 0.15, oy + oh / 2 - 0.05, L["loaded"], ha="right", va="center", fontsize=11.5, style="italic", linespacing=1.15)

# drawer with closed folders
rbox(0.1, 0.1, W - 0.2, 1.45, GRAY, r=0.1, lw=1.3, z=1)
ax.text(0.3, 1.3, L["drawer"], ha="left", va="center", fontsize=13, fontweight="semibold", color=PAPER, zorder=2)
fxs = [0.4, 1.55, 2.7, 3.85, 5.0]
for i, fx in enumerate(fxs):
    if i == PICK:
        folder(fx, 0.3, 0.95, 0.65, fill=GRAY, ls=(0, (3, 2)))  # its folder is out, on the desk
    else:
        folder(fx, 0.3, 0.95, 0.65)
ax.add_patch(FancyArrowPatch((fxs[PICK] + 0.48, 1.1), (ox + 0.3, oy - 0.02), arrowstyle="-|>,head_length=6,head_width=3.5",
                             color=INK, lw=1.6, connectionstyle="arc3,rad=-0.25", zorder=5, shrinkA=0, shrinkB=0))

out = ROOT / "assets" / "figures" / "ch09-revelacao-progressiva.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
