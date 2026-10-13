"""ch20-linha-do-tempo: 2019-2026 in four phases, plus base intelligence vs. model + harness.

Content: book/pt/ch20.md, "Sete anos numa página" (source post 2026/10/12
llms-agentes-competente-o-suficiente). Every milestone and number below is the one the
chapter prints:
  GPT-2 2019, 1,5 bi; Kaplan's scaling law and GPT-3 (175 bi) in 2020; Chinchilla 2022,
  70 bi beating Gopher's 280 bi; GPT-4 2023, size withheld; o1 Sept 2024, "a última
  revolução da inteligência de base"; Mixtral end of 2023 (~47 bi total, ~13 bi active);
  DeepSeek-V3 a year later (671 bi / 37 bi active); prompt caching up to 90% cheaper
  (2024); DeepSeek-R1(-Zero) Jan 2025; tool calling June 2023; MCP end of 2024;
  Claude Code and Codex 2025; METR: task length doubling every seven months since 2019.
Events sit at their real dates; each lane's sand band marks the year(s) the chapter
assigns to that phase ("o último grande salto em 2024, 2025 foi o ano de otimizar a
arquitetura, e 2026, o de refinar o harness"). The two curves on top are illustrative
shapes only: no y values.

Usage: uv run --with matplotlib --with numpy python -I assets/charts/ch20-linha-do-tempo.py pt
"""
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Circle

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {
        "base": "inteligência de base", "harness": "modelo + harness",
        "lanes": ["guerra dos parâmetros", "raciocínio", "otimização", "agentes"],
        "gpt2": "GPT-2\n1,5 bi", "scaling": "lei de escala", "gpt3": "GPT-3, 175 bi",
        "chin": "Chinchilla, 70 bi,\nbate o Gopher, 280 bi", "gpt4": "GPT-4, tamanho secreto",
        "o1": "o1, set. 2024: o último grande salto",
        "mixtral": "Mixtral, 47 bi, 13 bi ativos", "cache": "prompt caching, até −90%",
        "v3": "DeepSeek-V3\n671 bi, 37 bi ativos", "r1": "DeepSeek-R1",
        "tools": "chamada de ferramentas", "mcp": "MCP", "cc": "Claude Code\ne Codex",
        "metr": "METR: o tamanho das tarefas\ndobra a cada 7 meses",
        "bi": "bi = bilhões de parâmetros",
    },
    "en": {
        "base": "base intelligence", "harness": "model + harness",
        "lanes": ["parameter war", "reasoning", "optimisation", "agents"],
        "gpt2": "GPT-2\n1.5 B", "scaling": "scaling law", "gpt3": "GPT-3, 175 B",
        "chin": "Chinchilla, 70 B,\nbeats Gopher, 280 B", "gpt4": "GPT-4, size withheld",
        "o1": "o1, Sept 2024: the last big leap",
        "mixtral": "Mixtral, 47 B, 13 B active", "cache": "prompt caching, up to −90%",
        "v3": "DeepSeek-V3\n671 B, 37 B active", "r1": "DeepSeek-R1",
        "tools": "tool calling", "mcp": "MCP", "cc": "Claude Code\nand Codex",
        "metr": "METR: task length doubles\nevery 7 months",
        "bi": "B = billion parameters",
    },
}[LANG]

# Landscape-ish layout (7.2 x 6.4 in) so the book's height cap never shrinks it; printed at
# ~4.5 in wide, 11.5 pt drawn = 7.2 pt. Labels are packed into 3+1+3+3 levels.
W, H = 7.2, 6.4
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

X0, K = 0.2, 0.85            # x = X0 + (year - 2019) * K ; 2019.0 .. 2026.99
def X(year):
    return X0 + (year - 2019) * K
XEND = X(2027)

# ---------- lanes ----------
FS = 11.5
STEP = 0.235                      # vertical step between label levels
LEVELS = [3, 1, 3, 3]             # label levels used per lane
eras = [(2019, 2023), (2024, 2025), (2025, 2026), (2026, 2027)]
AXIS_Y = 0.42
heights = [0.4 + n * STEP + 0.1 for n in LEVELS]
bottoms = []
y = AXIS_Y + 0.08
for h in reversed(heights):
    bottoms.insert(0, y)
    y += h
LANE_TOP = y
lines = [b + 0.34 for b in bottoms]

for i, (a, b) in enumerate(eras):
    ax.add_patch(FancyBboxPatch((X(a) + 0.02, bottoms[i] + 0.03), X(b) - X(a) - 0.04, heights[i] - 0.06,
                                boxstyle="round,pad=0,rounding_size=0.06", fc=SAND, ec="none", zorder=0))
    ax.plot([X(2019), XEND], [lines[i], lines[i]], color=GRAY, lw=1.0, zorder=1)
    ax.text(X(a) + 0.08, lines[i] - 0.18, L["lanes"][i], ha="left", va="center", fontsize=12,
            fontweight="semibold", zorder=4)

def event(i, year, key, level, side="left", color=NAVY, r=0.05, bg=None):
    """Dot on lane i's line; label lines stacked upward from `level` (0 = lowest)."""
    y0, x = lines[i], X(year)
    text = L[key]
    n = text.count("\n") + 1
    bottom = y0 + 0.17 + level * STEP
    ax.plot([x, x], [y0, bottom + (n - 1) * STEP + 0.17], color=INK, lw=0.8, zorder=2)
    ax.add_patch(Circle((x, y0), r, fc=color, ec=INK, lw=1.0, zorder=3))
    for k, line in enumerate(text.split("\n")):
        yy = bottom + (n - 1 - k) * STEP
        ax.text(x + (0.05 if side == "left" else -0.05), yy, line, ha=side, va="bottom", fontsize=FS,
                fontweight="semibold" if k == 0 else "normal", zorder=4,
                bbox=dict(fc=bg, ec="none", pad=1.5) if bg else None)

# lane 0: parameter war
event(0, 2019.15, "gpt2", 0)
event(0, 2020.05, "scaling", 1)
event(0, 2020.4, "gpt3", 0)
event(0, 2022.25, "chin", 1)
event(0, 2023.2, "gpt4", 0, bg=PAPER)  # masks the o1 guide line
# lane 1: reasoning
event(1, 2024.7, "o1", 0, side="right", color=AMBER, r=0.08)
# lane 2: optimisation
event(2, 2023.95, "mixtral", 0, side="right")
event(2, 2024.6, "cache", 1, side="right")
event(2, 2024.95, "v3", 1)
event(2, 2025.08, "r1", 0)
# lane 3: agents
event(3, 2023.45, "tools", 0, side="right")
event(3, 2024.9, "mcp", 1, side="right")
event(3, 2025.3, "cc", 0)
ax.text(X(2019) + 0.08, lines[3] + 0.17 + STEP, L["metr"], ha="left", va="bottom", fontsize=FS, style="italic",
        linespacing=1.3, zorder=4)

# ---------- year axis ----------
ya = AXIS_Y
ax.plot([X(2019), XEND], [ya, ya], color=INK, lw=1.3)
for yr in range(2019, 2028):
    ax.plot([X(yr), X(yr)], [ya, ya - 0.07], color=INK, lw=1.2)
for yr in range(2019, 2027):
    ax.text(X(yr + 0.5), ya - 0.19, str(yr), ha="center", va="center", fontsize=FS)
ax.text(X(2019) + 0.02, H - 0.2, L["bi"], ha="left", va="center", fontsize=FS, style="italic")

# ---------- curves (illustrative) ----------
cy0, cy1 = LANE_TOP + 0.1, H - 0.05
t = np.linspace(2019, 2026.95, 400)
base = 1 / (1 + np.exp(-(t - 2022.3) * 1.25))
base = np.where(t > 2024.7, base[np.searchsorted(t, 2024.7)] + (t - 2024.7) * 0.012, base)
extra = np.clip(t - 2023.2, 0, None) ** 1.6 * 0.12
harness = base + extra
lo, hi = 0, harness.max()
def Y(v):
    return cy0 + 0.1 + (v - lo) / (hi - lo) * (cy1 - cy0 - 0.35)
ax.plot([X(t[0])], [Y(0)], alpha=0)
ax.plot(X(t), Y(harness), color=TEAL, lw=2.6, solid_capstyle="round", zorder=3)
ax.plot(X(t), Y(base), color=NAVY, lw=2.6, linestyle=(0, (5, 2.5)), zorder=3)
# label above the rising curve, ending where the curve is still low, so no line crosses it
xl = 2025.4
ax.text(X(xl), Y(harness[np.searchsorted(t, xl)]) + 0.16, L["harness"], ha="right", va="bottom", fontsize=FS,
        fontweight="semibold")
ax.text(X(2026.95), Y(base[-1]) - 0.1, L["base"], ha="right", va="top", fontsize=FS, fontweight="semibold")
# the o1 peak, tied to its lane by a dotted line
yo1 = Y(base[np.searchsorted(t, 2024.7)])
ax.plot([X(2024.7)] * 2, [lines[1], yo1], color=INK, lw=0.9, linestyle=(0, (1.5, 2)), zorder=2)
ax.add_patch(Circle((X(2024.7), yo1), 0.075, fc=AMBER, ec=INK, lw=1.0, zorder=4))

out = ROOT / "assets" / "figures" / "ch20-linha-do-tempo.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
