"""Run a chart script and check its text layout before it saves.

Usage: python -I scripts/chart_check.py assets/charts/<fig>.py <lang>

Labels change length between languages, and two English figures shipped with
text spilling out of their boxes. This wrapper runs the chart script as-is,
but intercepts Figure.savefig to check, for every visible text:
  - it lies inside the figure canvas;
  - if its centre is inside a box (FancyBboxPatch/Rectangle), it fits in that
    box entirely (a label that belongs to a box must not spill past its edge).
On a problem it prints the offending labels and exits 1 without saving.
"""

import runpy
import sys

import matplotlib

matplotlib.use("Agg")
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

TOL = 1.5  # pixels of slack for antialiasing and rounded corners

_original_savefig = Figure.savefig
SCRIPT = sys.argv[1] if len(sys.argv) > 1 else "?"
LANG = sys.argv[2] if len(sys.argv) > 2 else "pt"
problems = []


def _check(fig):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    canvas = fig.bbox
    for ax in fig.axes:
        boxes = [p.get_window_extent(renderer) for p in ax.patches
                 if isinstance(p, (FancyBboxPatch, Rectangle)) and p.get_visible() and p is not ax.patch]
        for t in ax.texts + list(fig.texts):
            if not t.get_visible() or not t.get_text().strip():
                continue
            bb = t.get_window_extent(renderer)
            label = t.get_text().replace("\n", " ")[:50]
            if bb.x0 < canvas.x0 - TOL or bb.x1 > canvas.x1 + TOL or bb.y0 < canvas.y0 - TOL or bb.y1 > canvas.y1 + TOL:
                problems.append(f"text off the canvas: {label!r}")
                continue
            cx, cy = (bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2
            # The smallest box containing the label's centre is the box it belongs to.
            owners = [b for b in boxes if b.x0 <= cx <= b.x1 and b.y0 <= cy <= b.y1]
            if not owners:
                continue
            owner = min(owners, key=lambda b: b.width * b.height)
            if bb.x0 < owner.x0 - TOL or bb.x1 > owner.x1 + TOL or bb.y0 < owner.y0 - TOL or bb.y1 > owner.y1 + TOL:
                problems.append(f"text spills out of its box: {label!r}")


def _checked_savefig(self, *args, **kwargs):
    _check(self)
    if problems:
        print(f"chart_check: {SCRIPT} [{LANG}]: {len(problems)} problem(s)", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        sys.exit(1)
    return _original_savefig(self, *args, **kwargs)


Figure.savefig = _checked_savefig

if __name__ == "__main__":
    script = sys.argv[1]
    sys.argv = [script] + sys.argv[2:]  # the chart sees its usual argv (lang)
    runpy.run_path(script, run_name="__main__")
