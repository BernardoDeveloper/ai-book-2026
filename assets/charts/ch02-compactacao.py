"""ch02-compactacao: the context window filling up and being compacted.

Data: none. Schematic of book/pt/ch02.md ("Notas que perdem detalhe"), from
akitaonrails.com 2026/05/18/como-memoria-de-agentes-funciona-e-como-melhorar:
near the limit, the agent asks the model for a summary of the old part,
throws the original away and keeps the recent messages whole. Block counts
are illustrative.

Usage: uv run --with matplotlib python -I assets/charts/ch02-compactacao.py pt
House style: docs/research/IMAGES.md §4.
"""
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER, RUST = ("#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B",
                                                   "#E9DFC9", "#FBF9F4", "#B5523B")
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "font.size": 12, "text.color": INK})

L = {
    "pt": {"janela": "janela de contexto", "antigas": "mensagens antigas", "recentes": "mensagens recentes",
           "limite": "limite", "compactacao": "compactação", "resumo": "resumo", "livre": "espaço livre",
           "s1": "início da conversa", "s2": "a janela enche", "s3": "depois da compactação"},
    "en": {"janela": "context window", "antigas": "old messages", "recentes": "recent messages",
           "limite": "limit", "compactacao": "compaction", "resumo": "summary", "livre": "free space",
           "s1": "start of the conversation", "s2": "the window fills up", "s3": "after compaction"},
}[LANG]

W = 10.0          # window capacity
LIMIT = 9.2       # compaction threshold
BW = 0.62         # block width
GAP = 0.08
H = 0.9           # bar height

fig, ax = plt.subplots(figsize=(6.6, 5.0), dpi=300)
fig.patch.set_facecolor(PAPER)
ax.set_facecolor(PAPER)
ax.set_xlim(-0.2, W + 0.35)
ax.set_ylim(-0.15, 7.25)
ax.axis("off")


def window(y):
    ax.add_patch(FancyBboxPatch((0, y), W, H, boxstyle="round,pad=0,rounding_size=0.12", fc=PAPER, ec=INK, lw=1.6,
                                zorder=1))


def blocks(y, x0, n, color):
    x = x0
    for _ in range(n):
        ax.add_patch(FancyBboxPatch((x + GAP / 2, y + 0.12), BW - GAP, H - 0.24,
                                    boxstyle="round,pad=0,rounding_size=0.06", fc=color, ec=INK, lw=0.9, zorder=2))
        x += BW
    return x


def bracket(x0, x1, y, text, above=True):
    d = 0.1 if above else -0.1
    ax.plot([x0, x0, x1, x1], [y, y + d, y + d, y], color=INK, lw=1.0, solid_capstyle="round")
    ax.text((x0 + x1) / 2, y + d + (0.05 if above else -0.05), text, ha="center", va="bottom" if above else "top",
            fontsize=11)


rows = [5.9, 3.5, 0.25]
# step titles
for y, key, num in zip(rows, ("s1", "s2", "s3"), "123"):
    ax.text(0, y + H + 0.38, f"{num}  {L[key]}", ha="left", va="bottom", fontsize=12, fontweight="semibold")

# 1: a few messages
window(rows[0])
end = blocks(rows[0], 0.08, 4, NAVY)
ax.text((end + W) / 2, rows[0] + H / 2, L["livre"], ha="center", va="center", fontsize=11.5, style="italic",
        color="#5E636C")
ax.text(W - 1.6, rows[0] + H + 0.38, L["janela"], ha="right", va="bottom", fontsize=11.5, style="italic")
ax.plot([W - 1.5, W - 1.0], [rows[0] + H + 0.5, rows[0] + H], color=INK, lw=1.0, solid_capstyle="round")

# 2: nearly full
window(rows[1])
x = blocks(rows[1], 0.08, 10, NAVY)
end2 = blocks(rows[1], x, 4, TEAL)
bracket(0.08, x - 0.02, rows[1] - 0.06, L["antigas"], above=False)
bracket(x + 0.02, end2, rows[1] - 0.06, L["recentes"], above=False)

# 3: summary + the same recent messages, free space back
window(rows[2])
ax.add_patch(FancyBboxPatch((0.08 + GAP / 2, rows[2] + 0.12), 1.15, H - 0.24, boxstyle="round,pad=0,rounding_size=0.06",
                            fc=AMBER, ec=INK, lw=1.2, zorder=2))
ax.text(0.08 + GAP / 2 + 0.575, rows[2] + H / 2, L["resumo"], ha="center", va="center", fontsize=11,
        fontweight="semibold", zorder=3)
end3 = blocks(rows[2], 1.27, 4, TEAL)
ax.text((end3 + W) / 2, rows[2] + H / 2, L["livre"], ha="center", va="center", fontsize=11.5, style="italic",
        color="#5E636C")

# limit line through all three windows
ax.plot([LIMIT, LIMIT], [rows[2] - 0.12, rows[0] + H + 0.12], color=RUST, lw=2.0, ls=(0, (4, 2.5)), zorder=4,
        solid_capstyle="round")
ax.text(LIMIT + 0.1, rows[1] + H + 0.22, L["limite"], ha="left", va="center", fontsize=11.5, color=RUST,
        fontweight="semibold")

# compaction arrow between 2 and 3
ax.add_patch(FancyArrowPatch((W / 2, rows[1] - 0.68), (W / 2, rows[2] + H + 0.95), arrowstyle="-|>",
                             mutation_scale=18, lw=1.8, color=INK))
ax.text(W / 2 + 0.2, (rows[1] - 0.68 + rows[2] + H + 0.95) / 2, L["compactacao"], ha="left", va="center",
        fontsize=12, fontweight="semibold")

fig.tight_layout(pad=0.4)
buf = io.BytesIO()
fig.savefig(buf, dpi=300, facecolor=PAPER, format="png")
out = ROOT / "assets" / "figures" / "ch02-compactacao.png"
Image.open(buf).convert("RGB").save(out, dpi=(300, 300))
print(out)
