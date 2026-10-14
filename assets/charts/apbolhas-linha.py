"""apbolhas-linha: three bubbles on one timeline, 1995-2026, with the narrator's lane.

Content: book/pt/apbolhas.md and book/pt/index.md ("Sobre o autor"); dates
checked in reviews/akitando/factcheck.yml (anchor facts):
  - internet: Nasdaq closing peak 10 Mar 2000, bottom 9 Oct 2002, ~78% down;
    the appendix's section dates the bubble 1995-2002.
  - free money: Fed funds 0-0.25% from 16 Dec 2008 to 16 Dec 2015 and from
    15 Mar 2020 to 16 Mar 2022; the hiring boom "a partir de 2010" to 2022;
    tech layoffs ~165 thousand in 2022 and ~263 thousand in 2023 (layoffs.fyi).
  - AI: ChatGPT released 30 Nov 2022; the wave runs on past 2026 (open end).
  - narrator: first job 1996; the dot-com closes and he moves to SAP in 2001;
    Rails 2007; Codeminer 42 2011; Akitando 2018-2023; this book 2026.
Bands are drawn at those dates; nothing else is plotted (no index values).

Usage: uv run --with matplotlib python -I scripts/chart_check.py assets/charts/apbolhas-linha.py pt
House style: docs/research/IMAGES.md §4.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER, RUST = ("#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B",
                                                   "#E9DFC9", "#FBF9F4", "#B5523B")
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK, "hatch.color": NAVY, "hatch.linewidth": 1.0})

L = {
    "pt": {"b1": "a internet", "b2": "o dinheiro de graça", "b3": "a IA",
           "peak": "pico da Nasdaq: 10 mar. 2000", "bottom": "fundo: 9 out. 2002, −78%",
           "zero": "juro perto de zero", "lay": "demissões: ~165 mil (2022), ~263 mil (2023)",
           "gpt": "ChatGPT: 30 nov. 2022",
           "me": "eu", "job": "1º emprego", "sap": "pontocom fecha; SAP", "rails": "Rails",
           "cm": "Codeminer 42", "akitando": "Akitando", "book": "este livro"},
    "en": {"b1": "the internet", "b2": "free money", "b3": "AI",
           "peak": "Nasdaq peak: 10 Mar 2000", "bottom": "bottom: 9 Oct 2002, −78%",
           "zero": "rates near zero", "lay": "layoffs: ~165k (2022), ~263k (2023)",
           "gpt": "ChatGPT: 30 Nov 2022",
           "me": "me", "job": "first job", "sap": "dot-com closes; SAP", "rails": "Rails",
           "cm": "Codeminer 42", "akitando": "Akitando", "book": "this book"},
}[LANG]

W, H = 7.2, 4.15
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes((0, 0, 1, 1))
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

X0, K = 0.2, (W - 0.4) / 32.0      # 1995.0 .. 2027.0
def X(year):
    return X0 + (year - 1995) * K

FS = 11.5


def band(a, b, y, h, fc=SAND, open_end=False):
    ax.add_patch(FancyBboxPatch((X(a), y), X(b) - X(a), h, boxstyle="round,pad=0,rounding_size=0.05",
                                fc=fc, ec="none", zorder=0, gid="nocheck"))
    if open_end:   # the wave has not ended: a soft arrow tip past 2026
        ax.add_patch(Polygon([(X(b), y), (X(b) + 0.16, y + h / 2), (X(b), y + h)], closed=True, fc=fc, ec="none",
                             zorder=0))


def lbl(x, y, s, **kw):
    t = ax.text(x, y, s, fontsize=kw.pop("fontsize", FS), zorder=4, **kw)
    t.set_gid("nocheck")    # labels hang off dates and may cross the era bands
    return t


def dot(x, y, color=NAVY, r=0.055):
    ax.add_patch(Circle((x, y), r, fc=color, ec=INK, lw=1.0, zorder=3))


# ---------- row 1: the internet, 1995-2002 ----------
R1, RH = 3.3, 0.72
band(1995, 2002.77, R1, RH)
lbl(X(1995) + 0.08, R1 + 0.08, L["b1"], ha="left", va="bottom", fontweight="semibold")
for yr, key, yy in ((2000.19, "peak", R1 + RH - 0.2), (2002.77, "bottom", R1 + 0.2)):
    dot(X(yr), yy, color=RUST if key == "bottom" else NAVY)
    lbl(X(2002.77) + 0.12, yy, L[key], ha="left", va="center")
ax.plot([X(2000.19), X(2002.77) + 0.08], [R1 + RH - 0.2] * 2, color=INK, lw=0.7, ls=(0, (1.5, 2)), zorder=2)

# ---------- row 2: free money, 2010-2022 ----------
R2 = 2.3
band(2010, 2022.2, R2, RH)
lbl(X(2010) + 0.08, R2 + RH - 0.08, L["b2"], ha="left", va="top", fontweight="semibold")
for a, b in ((2008.96, 2015.96), (2020.2, 2022.2)):
    ax.add_patch(Rectangle((X(a), R2 + 0.08), X(b) - X(a), 0.17, fc=PAPER, ec=NAVY, lw=1.0, hatch="////",
                           zorder=1, gid="nocheck"))
lbl(X(2008.96) - 0.08, R2 + 0.165, L["zero"], ha="right", va="center", style="italic")
for yr in (2022.5, 2023.5):
    dot(X(yr), R2 + RH - 0.1, color=RUST)
lbl(X(2023.5) + 0.1, R2 + RH + 0.1, L["lay"], ha="right", va="bottom")

# ---------- row 3: AI, from 30 Nov 2022 ----------
R3 = 1.32
band(2022.91, 2026.95, R3, RH, open_end=True)
lbl(X(2022.91) + 0.08, R3 + RH - 0.08, L["b3"], ha="left", va="top", fontweight="semibold")
dot(X(2022.91), R3 + 0.2, color=AMBER, r=0.07)
lbl(X(2022.91) - 0.12, R3 + 0.2, L["gpt"], ha="right", va="center")

# ---------- year axis ----------
YA = 0.36
ax.plot([X(1995), X(2027)], [YA, YA], color=INK, lw=1.2, zorder=2)
for yr in range(1995, 2028, 5):
    ax.plot([X(yr)] * 2, [YA, YA - 0.06], color=INK, lw=1.0)
    lbl(X(yr), YA - 0.1, str(yr), ha="center", va="top", fontsize=11.2)

# ---------- narrator lane ----------
YM = 0.85
ax.plot([X(1996), X(2026)], [YM, YM], color=GRAY, lw=1.6, zorder=1, solid_capstyle="round")
ax.add_patch(FancyBboxPatch((X(2018), YM - 0.07), X(2023.9) - X(2018), 0.14, boxstyle="round,pad=0,rounding_size=0.05",
                            fc=TEAL, ec=INK, lw=1.0, zorder=2, gid="nocheck"))
lbl(X(1995), YM, L["me"], ha="left", va="center", fontweight="semibold", style="italic")
events = [(1996.5, "job", "left"), (2001.9, "sap", "left"), (2007.5, "rails", "center"),
          (2011.7, "cm", "center"), (2026.5, "book", "right")]
for yr, key, ha in events:
    dot(X(yr), YM, color=AMBER if key == "book" else NAVY, r=0.05)
xs = {"job": X(1996.5) + 0.08, "sap": X(2001.9) + 0.08, "rails": X(2007.5), "cm": X(2011.7), "book": X(2026.5) + 0.06}
lbl(xs["job"], YM + 0.09, L["job"], ha="left", va="bottom", fontsize=11.2)
lbl(xs["sap"], YM - 0.09, L["sap"], ha="left", va="top", fontsize=11.2)
lbl(xs["rails"], YM + 0.09, L["rails"], ha="center", va="bottom", fontsize=11.2)
lbl(xs["cm"] - 0.06, YM - 0.09, L["cm"], ha="left", va="top", fontsize=11.2)
lbl(X(2020.95), YM + 0.11, L["akitando"], ha="center", va="bottom", fontsize=11.2)
lbl(xs["book"], YM - 0.09, L["book"], ha="right", va="top", fontsize=11.2)

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "apbolhas-linha.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
