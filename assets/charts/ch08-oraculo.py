"""ch08-oraculo: blind translation vs. translation checked by an oracle.

Content: book/pt/ch08.md, "Traduzir no escuro" and "O oráculo" (source post
2026/09/07 desafio-pra-ia-converter-roms-de-nes-pra-master-system-sms): without a
way to measure, the model generated translated code without knowing whether it was
right; with the oracle, original and translation run side by side on the same button
script, memory is compared byte by byte every frame, processor time is measured, and
the differences go back to the model.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch08-oraculo.py pt
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
    "pt": {"blind": "tradução cega", "oracle": "tradução com oráculo", "orig": "jogo original", "trad": "tradução",
           "model": "modelo", "q": "parece certo?", "buttons": "mesmos\nbotões", "emu": "emulador",
           "comp": "compara a memória\na cada quadro", "time": "mede o tempo",
           "back": "diferenças voltam\npro modelo", "new": "nova versão"},
    "en": {"blind": "blind translation", "oracle": "translation with an oracle", "orig": "original game",
           "trad": "translation", "model": "model", "q": "looks right?", "buttons": "same\nbuttons",
           "emu": "emulator", "comp": "compares memory\nevery frame", "time": "measures time",
           "back": "differences go back\nto the model", "new": "new version"},
}[LANG]

W, H = 6.4, 4.75
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

def box(cx, cy, w, h, fill, text, fs=12, weight="normal"):
    p = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0,rounding_size=0.07",
                       fc=fill, ec=INK, lw=1.4, zorder=3)
    ax.add_patch(p)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, zorder=4, linespacing=1.15, fontweight=weight,
            color=INK if fill in (SAND, PAPER, AMBER) else PAPER)
    return p

def arrow(a, b, rad=0.0, ls="-", pa=None, pb=None, lw=1.6):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>,head_length=6,head_width=3.5", color=INK, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2,
                                 patchA=pa, patchB=pb, shrinkA=2, shrinkB=2))

def panel(y0, h, title):
    ax.add_patch(FancyBboxPatch((0.08, y0), W - 0.16, h, boxstyle="round,pad=0,rounding_size=0.1",
                                fc=SAND, ec="none", zorder=0))
    ax.text(0.3, y0 + h - 0.25, title, ha="left", va="center", fontsize=13.5, fontweight="semibold")

# ---------- top: blind ----------
y0, h = 3.3, 1.38
panel(y0, h, L["blind"])
cy = y0 + 0.5
a = box(0.95, cy, 1.3, 0.5, NAVY, L["orig"])
b = box(2.45, cy, 1.0, 0.5, TEAL, L["model"])
c = box(3.85, cy, 1.15, 0.5, NAVY, L["trad"])
arrow((0, 0), (0, 0), pa=a, pb=b)
for (p, q) in [(a, b), (b, c)]:
    arrow((p.get_x() + p.get_width(), cy), (q.get_x(), cy))
arrow((c.get_x() + c.get_width(), cy), (4.95, cy), ls=(0, (3, 2.5)))
ax.text(5.0, cy, L["q"], ha="left", va="center", fontsize=12.5, style="italic")

# ---------- bottom: oracle ----------
y0, h = 0.1, 3.05
panel(y0, h, L["oracle"])
e1y, e2y = y0 + 2.2, y0 + 1.35
bt = box(0.75, (e1y + e2y) / 2, 0.85, 0.65, GRAY, L["buttons"])
e1 = box(2.35, e1y, 1.6, 0.6, NAVY, f"{L['emu']}:\n{L['orig']}", fs=11.5)
e2 = box(2.35, e2y, 1.6, 0.6, NAVY, f"{L['emu']}:\n{L['trad']}", fs=11.5)
cmp_ = FancyBboxPatch((3.7, (e1y + e2y) / 2 - 0.55), 2.4, 1.1, boxstyle="round,pad=0,rounding_size=0.07",
                      fc=AMBER, ec=INK, lw=1.4, zorder=3)
ax.add_patch(cmp_)
mid = (e1y + e2y) / 2
ax.text(4.9, mid + 0.18, L["comp"], ha="center", va="center", fontsize=12, zorder=4, linespacing=1.15)
ax.plot([3.95, 5.85], [mid - 0.2, mid - 0.2], color=INK, lw=0.8, zorder=4)
ax.text(4.9, mid - 0.37, L["time"], ha="center", va="center", fontsize=12, zorder=4)
for e, ey in [(e1, e1y), (e2, e2y)]:
    arrow((1.18, mid + (0.12 if ey == e1y else -0.12)), (1.55, ey))
    arrow((3.15, ey), (3.7, mid + (0.25 if ey == e1y else -0.25)))
mo = box(4.3, y0 + 0.42, 1.0, 0.5, TEAL, L["model"])
arrow((4.3, mid - 0.55), (4.3, y0 + 0.67))
ax.text(4.45, (mid - 0.55 + y0 + 0.67) / 2, L["back"], ha="left", va="center", fontsize=11.5, style="italic",
        linespacing=1.1)
arrow((3.8, y0 + 0.42), (2.35, e2y - 0.3), rad=-0.35)
ax.text(2.0, y0 + 0.42, L["new"], ha="center", va="center", fontsize=11.5, style="italic")

out = ROOT / "assets" / "figures" / "ch08-oraculo.png"
fig.savefig(out, dpi=300, facecolor=PAPER)
# Flatten to RGB (no alpha), keep 300 dpi metadata
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
