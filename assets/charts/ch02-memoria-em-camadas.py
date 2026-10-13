"""ch02-memoria-em-camadas: the three memory tiers of Claude Code (March 2026 leak).

Data: none. Schematic of book/pt/ch02.md ("Memória é um arquivo de texto" and
"O agente que sonha"), from akitaonrails.com 2026/03/31/codigo-fonte-do-claude-
code-vazou-o-que-achamos-dentro: a short index (MEMORY.md) always on the desk,
topic files pulled in only when needed, raw transcripts never loaded whole,
only searched by keyword; the autoDream process rewrites the topic files.

Usage: uv run --with matplotlib python -I assets/charts/ch02-memoria-em-camadas.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Circle
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
MUTED = "#5E636C"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK})

L = {
    "pt": {"janela": "janela de contexto", "indice": "índice", "sempre": "sempre carregado",
           "topicos": "arquivos de tópico", "sob": "sob demanda", "transc": "transcrições antigas",
           "busca": "só pesquisadas por palavra", "trecho": "só o trecho achado",
           "sonho": "sonho: consolidação", "sonho2": "em segundo plano", "reescreve": "reescreve"},
    "en": {"janela": "context window", "indice": "index", "sempre": "always loaded",
           "topicos": "topic files", "sob": "on demand", "transc": "old transcripts",
           "busca": "only searched by keyword", "trecho": "only the matching snippet",
           "sonho": "dream: consolidation", "sonho2": "in the background", "reescreve": "rewrites"},
}[LANG]

fig, ax = plt.subplots(figsize=(6.0, 5.15), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(0, 10.4)
ax.set_ylim(0, 8.9)
ax.set_aspect("equal")
ax.axis("off")
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)


def page(x, y, w, h, fc, lw=1.4, ear=0.28, z=3):
    ax.add_patch(Polygon([(x, y), (x + w, y), (x + w, y + h - ear), (x + w - ear, y + h), (x, y + h)], closed=True,
                         fc=fc, ec=INK, lw=lw, joinstyle="round", zorder=z))
    ax.add_patch(Polygon([(x + w - ear, y + h), (x + w - ear, y + h - ear), (x + w, y + h - ear)], closed=True,
                         fc=PAPER, ec=INK, lw=lw * 0.8, joinstyle="round", zorder=z))


def folder(x, y, w, h, fc, z):
    tab = [(x, y + h), (x + 0.12, y + h + 0.22), (x + w * 0.38, y + h + 0.22), (x + w * 0.45, y + h)]
    ax.add_patch(Polygon(tab, closed=True, fc=fc, ec=INK, lw=1.3, joinstyle="round", zorder=z))
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.06", fc=fc, ec=INK, lw=1.3,
                                zorder=z))


def arrow(p, q, color=INK, lw=1.8, ls="-", rad=0.0, ms=15):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, lw=lw, color=color, linestyle=ls,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=6))


# tier 1: the context window with the index inside
ax.add_patch(FancyBboxPatch((0.2, 6.35), 7.4, 2.1, boxstyle="round,pad=0,rounding_size=0.15", fc=SAND, ec=INK,
                            lw=1.8, zorder=1))
ax.text(0.45, 8.15, L["janela"], ha="left", va="center", fontsize=12.5, fontweight="semibold")
page(0.6, 6.6, 1.25, 1.3, AMBER)
for i in range(4):
    ax.plot([0.8, 1.45 if i % 2 else 1.6], [7.5 - i * 0.22] * 2, color=INK, lw=1.0, zorder=4)
ax.text(2.15, 7.42, L["indice"], ha="left", va="center", fontsize=13, fontweight="semibold")
ax.text(2.15, 6.95, L["sempre"], ha="left", va="center", fontsize=11.5, style="italic")

# tier 2: topic files
for i, (dx, dy) in enumerate(((0.0, 0.0), (0.35, -0.3), (0.7, -0.6))):
    folder(0.6 + dx, 4.25 + dy, 1.45, 1.0, NAVY, 3 + i)
ax.text(1.7, 3.2, L["topicos"], ha="center", va="center", fontsize=12.5, fontweight="semibold")
arrow((1.6, 5.35), (1.6, 6.32), lw=2.2)
ax.text(1.8, 5.83, L["sob"], ha="left", va="center", fontsize=11.5, style="italic")

# tier 3: a big pile of transcripts with a magnifying glass
for i in range(6):
    page(0.5 + i * 0.13, 0.35 + i * 0.12, 2.6, 1.55, GRAY if i < 5 else PAPER, lw=1.1, ear=0.3, z=2 + i)
for j in range(5):
    ax.plot([0.5 + 5 * 0.13 + 0.25, 0.5 + 5 * 0.13 + (2.0 if j % 2 else 2.25)], [1.75 - j * 0.24] * 2, color=GRAY,
            lw=1.0, zorder=8)
ax.add_patch(Circle((3.3, 1.3), 0.42, fc=PAPER, ec=INK, lw=2.2, zorder=9))
ax.plot([3.6, 3.95], [1.0, 0.62], color=INK, lw=4.0, solid_capstyle="round", zorder=9)
ax.text(4.3, 1.45, L["transc"], ha="left", va="center", fontsize=12.5, fontweight="semibold")
ax.text(4.3, 0.98, L["busca"], ha="left", va="center", fontsize=11.5, style="italic")
# only the matching snippet reaches the window
arrow((7.0, 2.0), (7.0, 6.32), lw=1.5, ls=(0, (4, 3)), ms=13)
ax.text(7.2, 3.6, L["trecho"], ha="left", va="center", fontsize=11, style="italic", color=MUTED)

# beside the topic files: the dream that rewrites them
MX, MY = 5.0, 5.05
ax.add_patch(Circle((MX, MY), 0.45, fc=TEAL, ec=INK, lw=1.5, zorder=3))
ax.add_patch(Circle((MX + 0.27, MY + 0.18), 0.4, fc=PAPER, ec="none", zorder=4))
ax.text(MX, MY - 0.8, L["sonho"], ha="center", va="center", fontsize=11.5, fontweight="semibold")
ax.text(MX, MY - 1.22, L["sonho2"], ha="center", va="center", fontsize=11, style="italic")
arrow((MX - 0.6, MY - 0.1), (3.0, MY - 0.1), color=TEAL, lw=1.8, ls=(0, (4, 3)), ms=13)
ax.text((MX - 0.6 + 3.0) / 2, MY + 0.2, L["reescreve"], ha="center", va="bottom", fontsize=11, style="italic",
        color=TEAL)

buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
out = ROOT / "assets" / "figures" / "ch02-memoria-em-camadas.png"
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
