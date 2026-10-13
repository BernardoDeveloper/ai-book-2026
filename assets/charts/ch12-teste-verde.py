"""ch12-teste-verde: green test, dead app.

Content: book/pt/ch12.md, "Teste verde, aplicativo morto" (source post
2026/07/01 llm-benchmark-sonnet-5-gemini-3-5-flash-sakana-fugu-ultra): the model
invented a RubyLLM command; it also wrote the mock (dublê) used by the tests, and
the mock had the same invented command, so the test asked "você aceita isso?",
the stand-in answered "aceito" and the test went green. The real library has no
such command, so the first real conversation breaks with an error.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch12-teste-verde.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
RUST = "#B5523B"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"test_lane": "no teste", "prod_lane": "em produção", "test": "teste", "app": "aplicativo",
           "mock": "dublê", "mock_note": "escrito pelo\nmesmo modelo", "lib": "biblioteca\nde verdade",
           "cmd": "comando inventado", "yes": "“aceito”", "no": "“não conheço”",
           "green": "verde", "error": "erro"},
    "en": {"test_lane": "in the test", "prod_lane": "in production", "test": "test", "app": "app",
           "mock": "mock", "mock_note": "written by the\nsame model", "lib": "real\nlibrary",
           "cmd": "invented command", "yes": "“accepted”", "no": "“unknown”",
           "green": "green", "error": "error"},
}[LANG]

W, H = 6.4, 4.6
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")


def box(x, y, w, h, fill, text="", fg=None, fs=12, ls="-", lw=1.4, weight="normal", z=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.07", fc=fill, ec=INK,
                                lw=lw, linestyle=ls, zorder=z))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=z + 1,
                color=fg or (INK if fill in (SAND, PAPER, AMBER) else PAPER), fontweight=weight, linespacing=1.1)


def arrow(p, q, lw=1.6, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=color, lw=lw,
                                 zorder=2, shrinkA=0, shrinkB=0))


def lane(x0, title, caller, callee, callee_fill, callee_ls, reply, ok):
    w = 2.98
    ax.add_patch(FancyBboxPatch((x0, 0.1), w, H - 0.2, boxstyle="round,pad=0,rounding_size=0.1",
                                fc=SAND, ec="none", zorder=0))
    ax.text(x0 + 0.2, H - 0.36, title, ha="left", va="center", fontsize=13.5, fontweight="semibold")
    cx = x0 + 1.05
    box(cx - 0.7, 3.25, 1.4, 0.55, NAVY, caller, fs=12)
    # invented command travels down
    arrow((cx, 3.22), (cx, 2.43))
    ax.add_patch(FancyBboxPatch((cx + 0.12, 2.68), 1.62, 0.34, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=AMBER, ec=INK, lw=1.1, zorder=3))
    ax.text(cx + 0.93, 2.85, L["cmd"], ha="center", va="center", fontsize=10.5, zorder=4)
    fg = INK if callee_fill in (PAPER, SAND) else PAPER
    box(cx - 0.7, 1.68, 1.4, 0.72, callee_fill, callee, fs=12, fg=fg, ls=callee_ls)
    ax.text(cx + 0.82, 2.04, reply, ha="left", va="center", fontsize=11, style="italic")
    arrow((cx, 1.65), (cx, 1.07))
    # light
    r = 0.32
    ly = 0.68
    ax.add_patch(Circle((cx, ly), r, fc=TEAL if ok else RUST, ec=INK, lw=1.4, zorder=3))
    if ok:
        ax.plot([cx - 0.14, cx - 0.03, cx + 0.16], [ly + 0.0, ly - 0.12, ly + 0.13], color=PAPER, lw=2.6,
                solid_capstyle="round", solid_joinstyle="round", zorder=4)
    else:
        for s in (1, -1):
            ax.plot([cx - 0.12, cx + 0.12], [ly - 0.12 * s, ly + 0.12 * s], color=PAPER, lw=2.6,
                    solid_capstyle="round", zorder=4)
    ax.text(cx + r + 0.15, ly, L["green"] if ok else L["error"], ha="left", va="center", fontsize=13,
            fontweight="semibold")
    return cx


cx = lane(0.12, L["test_lane"], L["test"], L["mock"], PAPER, (0, (3, 2)), L["yes"], True)
ax.text(cx + 0.82, 1.62, L["mock_note"], ha="left", va="top", fontsize=9.5, color="#5E636C", linespacing=1.1)
lane(3.3, L["prod_lane"], L["app"], L["lib"], GRAY, "-", L["no"], False)

out = ROOT / "assets" / "figures" / "ch12-teste-verde.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
