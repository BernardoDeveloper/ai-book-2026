# frozen_string_literal: true

require_relative "test_helper"

# scripts/chart_check.py: runs a chart script and refuses to save when a label
# spills out of its box or off the canvas; gid "nocheck" marks an intentional
# overlap (a text that may cross boxes, or a patch that is only a background).
class TestChartCheck < ToolTest
  CHART = "assets/charts/probe.py"
  OUT = "build/probe.png"

  # A wide label centred in a small box. MODE (argv[1]) decides which artist,
  # if any, carries gid "nocheck"; "offcanvas" also pushes the label off the page.
  SCRIPT = <<~PY
    import sys
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    mode = sys.argv[1]
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.add_patch(Rectangle((4, 4), 2, 2, gid="nocheck" if mode == "patch" else None))
    x = 12 if mode == "offcanvas" else 5
    t = ax.text(x, 5, "a label much wider than its box", ha="center", va="center", fontsize=12)
    if mode in ("text", "offcanvas"):
        t.set_gid("nocheck")
    fig.savefig("#{OUT}")
  PY

  def uv? = system("uv", "--version", out: File::NULL, err: File::NULL)

  def setup
    skip "`uv` not on PATH (the checker needs matplotlib via uv)" unless uv?
    super
    fx.write(CHART, SCRIPT)
    FileUtils.mkdir_p(fx.path("build"))
  end

  def check(mode)
    out, err, status = Open3.capture3("uv", "run", "--quiet", "--with", "matplotlib", "python", "-I",
                                      "scripts/chart_check.py", CHART, mode, chdir: fx.root)
    Fixture::Result.new(out, err, status)
  end

  # Guards the base rule: a label centred in a box must fit in it; nothing is saved.
  def test_spill_fails_without_gid
    res = check("none")
    assert_exit 1, res
    assert_includes res.err, "text spills out of its box: 'a label much wider than its box'"
    refute fx.exist?(OUT)
  end

  # Guards gid "nocheck" on a text: it may cross box edges.
  def test_nocheck_text_may_cross_boxes
    res = check("text")
    assert_exit 0, res
    assert fx.exist?(OUT)
  end

  # Guards gid "nocheck" on a patch: a background band is never a label's box.
  def test_nocheck_patch_is_not_a_box
    res = check("patch")
    assert_exit 0, res
    assert fx.exist?(OUT)
  end

  # Guards that "nocheck" only waives the box rule: the canvas rule still holds.
  def test_nocheck_text_still_on_canvas
    res = check("offcanvas")
    assert_exit 1, res
    assert_includes res.err, "text off the canvas"
    refute fx.exist?(OUT)
  end
end
