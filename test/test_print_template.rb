# frozen_string_literal: true

require "minitest/autorun"
require "open3"

class TestPrintTemplate < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  PANDOC = Dir[File.join(ROOT, "tools/quarto-*/bin/tools/*/pandoc")].first

  def render(*metadata)
    skip "pinned Pandoc unavailable" unless PANDOC
    out, err, status = Open3.capture3(PANDOC, "-f", "markdown", "-t", "typst",
      "--template", File.join(ROOT, "_extensions/akita-book/typst-template.typ"),
      *metadata.flat_map { ["-M", _1] }, stdin_data: "Test\n")
    assert status.success?, err
    out
  end

  def test_amazon_defaults_are_preserved
    out = render
    assert_includes out, "#let ak-page-w = 6in"
    assert_includes out, "#let ak-page-h = 9in"
    assert_includes out, "#let ak-uiclap = false"
  end

  def test_uiclap_dimensions_and_margin_switch
    out = render("print-width=160mm", "print-height=230mm", "uiclap-print=true")
    assert_includes out, "#let ak-page-w = 160mm"
    assert_includes out, "#let ak-page-h = 230mm"
    assert_includes out, "#let ak-uiclap = true"
    assert_includes out, "inside: 25mm, outside: 20mm"
  end
end
