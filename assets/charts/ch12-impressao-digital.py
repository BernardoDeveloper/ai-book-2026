"""ch12-impressao-digital: the token count works as a lineage fingerprint.

Content: book/pt/ch12.md, "A impressão digital" (source post 2026/09/30
o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro).
Data: llm-coding-benchmark lua-forensics/results/tokenizer_v2.latest.json
(2026-09-30), summarised in lua-forensics/FINDINGS.md, Test 1. Content-token
counts per probe string (CJK sentence, digits x20, ZWJ emoji run) for each local
tokenizer and for the LUA API ("API testada", enterprise tier; house is identical
but one token). "distância" = sum of |reference - API| over the five probe
strings (CJK, PT accents, English, digits, emoji): o200k 2, Llama 3 68,
cl100k 134, Qwen 193, DeepSeek 255, Mistral 289. The chapter quotes o200k 2,
Llama 3 68, Qwen "quase 200" and digits 200 (Qwen/DeepSeek) vs 67 (API).

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch12-impressao-digital.py pt
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"same": "mesmo texto, contado em tokens", "cols": ["chinês", "dígitos", "emoji"],
           "dist": "distância da API", "api": "API testada", "o200k": "o200k (OpenAI)",
           "foot": "distância: soma das diferenças em cinco textos de teste",
           "note": "mesma contagem não quer dizer mesmos pesos"},
    "en": {"same": "same text, counted in tokens", "cols": ["Chinese", "digits", "emoji"],
           "dist": "distance from the API", "api": "tested API", "o200k": "o200k (OpenAI)",
           "foot": "distance: sum of the differences over five test texts",
           "note": "same count does not mean same weights"},
}[LANG]

# name, (cjk, digits, emoji), distance
ROWS = [(L["api"], (42, 67, 168), None),
        (L["o200k"], (42, 67, 169), 2),
        ("Llama 3", (46, 67, 218), 68),
        ("cl100k", (82, 67, 248), 134),
        ("Qwen", (30, 200, 132), 193),
        ("DeepSeek", (34, 200, 248), 255),
        ("Mistral", (73, 201, 265), 289)]

W, H = 6.4, 4.5
fig = plt.figure(figsize=(W, H), dpi=300)
fig.patch.set_facecolor(PAPER)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal"); ax.axis("off")

NAME_R = 1.95
CX = [2.4, 3.08, 3.76]
CW, RH = 0.62, 0.42
BX0, BMAX = 4.3, 1.5
top = 3.55

ax.text((CX[0] + CX[-1]) / 2, top + 0.68, L["same"], ha="center", va="center", fontsize=11.5,
        fontweight="semibold")
for x, c in zip(CX, L["cols"]):
    ax.text(x, top + 0.3, c, ha="center", va="center", fontsize=11)
ax.text(BX0, top + 0.3, L["dist"], ha="left", va="center", fontsize=11, fontweight="semibold")

for i, (name, counts, dist) in enumerate(ROWS):
    y = top - i * RH - (0.12 if i > 0 else 0)  # small gap under the API row
    api, match = i == 0, i == 1
    if api or match:
        ax.add_patch(FancyBboxPatch((0.15, y - RH / 2 + 0.03), W - 0.3, RH - 0.06,
                                    boxstyle="round,pad=0,rounding_size=0.06",
                                    fc=SAND if api else AMBER, ec="none", zorder=0, alpha=1 if api else 0.55))
    ax.text(NAME_R, y, name, ha="right", va="center", fontsize=11.5,
            fontweight="semibold" if (api or match) else "normal")
    for x, v in zip(CX, counts):
        same = match and v == ROWS[0][1][CX.index(x)]
        ax.add_patch(Rectangle((x - CW / 2, y - RH / 2 + 0.05), CW, RH - 0.1,
                               fc=NAVY if api else PAPER, ec=INK, lw=1.1 if not same else 1.8, zorder=2))
        ax.text(x, y, str(v), ha="center", va="center", fontsize=11, zorder=3,
                color=PAPER if api else INK, fontweight="semibold" if same else "normal")
    if dist is not None:
        w = max(BMAX * dist / 289, 0.03)
        ax.add_patch(Rectangle((BX0, y - 0.11), w, 0.22, fc=AMBER if match else GRAY, ec=INK, lw=1.0, zorder=2))
        ax.text(BX0 + w + 0.08, y, str(dist), ha="left", va="center", fontsize=11,
                fontweight="semibold" if match else "normal")
    else:
        ax.text(BX0, y, "—", ha="left", va="center", fontsize=11, color="#5E636C")

ax.text(0.2, 0.42, L["note"], ha="left", va="center", fontsize=11, style="italic")
ax.text(0.2, 0.13, L["foot"], ha="left", va="center", fontsize=9, style="italic", color="#5E636C")

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch12-impressao-digital.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
