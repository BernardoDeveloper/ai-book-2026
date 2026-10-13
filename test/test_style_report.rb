# frozen_string_literal: true

require_relative "test_helper"

# scripts/style_report.rb: copyedit step 1 (docs/COPYEDIT.md).
class TestStyleReport < ToolTest
  # Guards the repetition finder: a passage reused in two units is reported
  # once, as one maximal span (not as many overlapping windows), with both units.
  def test_repeated_passage_reported_once_with_units
    shared = "a mesma frase longa aparece em dois capitulos diferentes do livro sem querer"
    %w[ch01 ch02].each do |id|
      path = File.join(fx.root, "book", "pt", "#{id}.md")
      File.write(path, File.read(path) + "\n<!-- src: original -->\n#{shared.capitalize}.\n")
    end
    res = fx.run("style_report", "--lang", "pt")
    assert_exit 0, res
    report = File.read(File.join(fx.root, "build", "pt", "style-report.md"))
    lines = report.lines.grep(/sem querer/)
    assert_equal 1, lines.size, "one entry per repeated passage"
    assert_match(/ch01, ch02|ch02, ch01/, lines.first)
  end

  # Guards the report against leaking non-prose: provenance comments and
  # front matter must not count as repeated text.
  def test_markup_is_not_prose
    res = fx.run("style_report", "--lang", "pt")
    assert_exit 0, res
    report = File.read(File.join(fx.root, "build", "pt", "style-report.md"))
    refute_match(/src: original|sha256|blog_commit/, report)
  end
end
