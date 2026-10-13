"""ch16-laco-adversarial: the loop of the Bun rewrite from Zig to Rust.

Content: book/pt/ch16.md, "Uma reescrita que deu certo" (source post 2026/07/09
resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito, citing Sumner 2026):
the ~16k compile errors became a work queue; for each change one Claude instance
implements, two others attack the result as adversarial reviewers, each with a clean
context and only the change on the desk, a fourth applies the fixes; Bun's own
TypeScript test suite and then CI on several platforms are the judge.

Drawn with matplotlib (shapes + live text). Usage:
  uv run --with matplotlib python -I assets/charts/ch16-laco-adversarial.py pt
"""
import sys
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[2]
LANG = sys.argv[1] if len(sys.argv) > 1 else "pt"
INK, NAVY, TEAL, GRAY, AMBER, SAND, PAPER = "#1B2238", "#2B3A67", "#2F7F86", "#8A8F98", "#E3A23B", "#E9DFC9", "#FBF9F4"
for f in ("NotoSans-Regular.ttf", "NotoSans-SemiBold.ttf", "NotoSans-Italic.ttf"):
    font_manager.fontManager.addfont(str(ROOT / "assets" / "fonts" / f))
plt.rcParams.update({"font.family": "Noto Sans", "text.color": INK})

L = {
    "pt": {"queue": "fila de tarefas", "impl": "implementador", "rev": "revisor\nadversarial", "fix": "corretor",
           "tests": "testes e CI", "clean": "contexto limpo,\nsó a mudança na mesa", "fail": "reprovou",
           "pass": "passou", "next": "próxima\ntarefa"},
    "en": {"queue": "task queue", "impl": "implementer", "rev": "adversarial\nreviewer", "fix": "fixer",
           "tests": "tests and CI", "clean": "clean context,\nonly the change on the desk", "fail": "failed",
           "pass": "passed", "next": "next\ntask"},
}[LANG]

W, H = 6.4, 4.5
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


def arrow(p, q, rad=0.0, ls="-", lw=1.6, color=INK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>,head_length=6,head_width=3.5", color=color, lw=lw,
                                 linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=2, shrinkA=0, shrinkB=0))


def magnifier(cx, cy, r=0.14):
    ax.add_patch(Circle((cx, cy), r, fc=PAPER, ec=INK, lw=1.5, zorder=6))
    a = math.radians(-45)
    ax.plot([cx + r * math.cos(a), cx + 2.1 * r * math.cos(a)], [cy + r * math.sin(a), cy + 2.1 * r * math.sin(a)],
            color=INK, lw=3.0, solid_capstyle="round", zorder=6)


# ---------- task queue: a column of cards ----------
qx, qy = 0.25, 1.75
for i in range(5):
    box(qx + 0.06 * (4 - i), qy + 0.13 * i, 1.05, 0.32, PAPER if i % 2 else SAND, lw=1.1, z=3 + i * 0.1)
ax.text(qx + 0.62, qy + 0.95, L["queue"], ha="center", va="center", fontsize=12, fontweight="semibold")

# ---------- implementer ----------
ix, iy, iw, ih = 1.85, 3.35, 1.55, 0.62
box(ix, iy, iw, ih, NAVY, L["impl"], fs=12.5, weight="semibold")
arrow((qx + 1.4, qy + 0.45), (ix + 0.35, iy - 0.05), rad=0.25)

# ---------- two adversarial reviewers ----------
rx, rw, rh = 4.15, 1.75, 0.7
ry = (3.55, 2.6)
for y in ry:
    box(rx, y, rw, rh, TEAL)
    ax.text(rx + rw / 2 + 0.2, y + rh / 2, L["rev"], ha="center", va="center", fontsize=12, color=PAPER,
            fontweight="semibold", linespacing=1.1, zorder=5)
    magnifier(rx + 0.25, y + rh / 2 + 0.06, r=0.12)
    arrow((ix + iw + 0.05, iy + ih / 2), (rx - 0.05, y + rh / 2), rad=0.0)
ax.text(rx + 0.1, 2.3, L["clean"], ha="right", va="center", fontsize=10.5, style="italic", linespacing=1.1)

# ---------- fixer ----------
fx, fy, fw, fh = 4.35, 1.2, 1.3, 0.6
box(fx, fy, fw, fh, NAVY, L["fix"], fs=12.5, weight="semibold")
arrow((rx + rw + 0.05, ry[0] + rh / 2), (fx + fw + 0.05, fy + fh / 2), rad=-0.45)
arrow((rx + rw / 2 - 0.1, ry[1] - 0.05), (fx + fw / 2 - 0.1, fy + fh + 0.05))

# ---------- tests and CI: the judge (one highlight) ----------
tx, ty, tw, th = 1.75, 0.3, 1.75, 1.1
box(tx, ty, tw, th, AMBER, z=3)
# scale icon
sx, sy = tx + tw / 2, ty + 0.62
ax.plot([sx, sx], [sy - 0.22, sy + 0.2], color=INK, lw=1.6, zorder=5, solid_capstyle="round")
ax.plot([sx - 0.42, sx + 0.42], [sy + 0.2, sy + 0.2], color=INK, lw=1.6, zorder=5, solid_capstyle="round")
ax.add_patch(Polygon([(sx - 0.14, sy - 0.24), (sx + 0.14, sy - 0.24), (sx, sy - 0.16)], closed=True, fc=INK, ec=INK, zorder=5))
for px in (sx - 0.42, sx + 0.42):
    ax.plot([px - 0.1, px, px + 0.1], [sy - 0.02, sy + 0.2, sy - 0.02], color=INK, lw=1.0, zorder=5)
    ax.add_patch(Polygon([(px - 0.14, sy - 0.02), (px + 0.14, sy - 0.02), (px + 0.08, sy - 0.1), (px - 0.08, sy - 0.1)],
                         closed=True, fc=PAPER, ec=INK, lw=1.1, zorder=5))
ax.text(sx, ty + 0.2, L["tests"], ha="center", va="center", fontsize=12.5, fontweight="semibold", zorder=6)
arrow((fx - 0.05, fy + fh / 2), (tx + tw + 0.05, ty + th / 2 + 0.25))

# failed -> back to the queue
arrow((tx - 0.05, ty + th / 2), (qx + 0.45, qy - 0.06), rad=-0.3, ls=(0, (4, 2.5)))
ax.text(0.75, 0.62, L["fail"], ha="center", va="center", fontsize=11.5, style="italic")
# passed -> next task
arrow((tx + tw + 0.05, ty + 0.25), (fx + 0.1, 0.32))
ax.text(fx + 0.15, 0.32, L["pass"], ha="left", va="center", fontsize=11.5, style="italic")

# PT is the canonical edition at assets/figures/; other languages get assets/figures/<lang>/.

out = ROOT / "assets" / "figures" / ("" if LANG == "pt" else LANG) / "ch16-laco-adversarial.png"

out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=300, facecolor=PAPER)
from PIL import Image
Image.open(out).convert("RGB").save(out, dpi=(300, 300))
print(out)
