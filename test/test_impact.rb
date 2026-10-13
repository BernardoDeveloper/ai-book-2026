# frozen_string_literal: true

require_relative "test_helper"

# scripts/impact.rb: the blast radius of a change, before making it.
class TestImpact < ToolTest
  def impact(*args) = fx.run("impact", *args)

  # Guards `post`: marked blocks per unit (with line numbers), credits,
  # bibliography notes and lineage that mention the post.
  def test_post
    res = impact("post", "2026/02/10/primeiro-post")
    assert_exit 0, res
    ch01_lines = fx.read("book/pt/ch01.md").lines.each_index.select { fx.read("book/pt/ch01.md").lines[_1].include?("src: 2026/02/10") }.map { _1 + 1 }
    assert_includes res.out, "  ch01: 2 marked block(s), ~"
    assert_includes res.out, "lines #{ch01_lines.join(', ')}"
    assert_match(/^  prefacio: 1 marked block/, res.out, "index.md is reported as prefacio")
    assert_match(/^  ch02: 1 marked block/, res.out)
    refute_match(/^  ch03:/, res.out)
    assert_includes res.out, "figure ch01-arte mentions it"
    assert_includes res.out, "references noted as cited-by it: smith2026ai"
    assert_includes res.out, "appears in inventory/lineage.yml"
  end

  # Guards marked-but-unlisted posts being flagged (provenance out of sync).
  def test_post_marked_but_not_listed
    fx.edit("book/pt/epilogo.md") { _1 + "\n<!-- src: 2026/03/05/segundo-post -->\nO agente esquece.\n" }
    res = impact("post", "2026/03/05/segundo-post")
    assert_match(/^  epilogo: 1 marked block\(s\), ~3 words \(NOT in front-matter sources\)/, res.out)
  end

  # Guards `posts-before`: every used post older than the date (the cut-off move).
  def test_posts_before
    res = impact("posts-before", "2026-04-01")
    assert_exit 0, res
    assert_includes res.out, "2 post(s) before 2026-04-01 are used"
    assert_includes res.out, "== 2026/02/10/primeiro-post"
    assert_includes res.out, "== 2026/03/05/segundo-post"
    refute_includes res.out, "== 2026/04/01/terceiro-post"
  end

  # Guards `unit`: callbacks into the unit, hand-offs around it, its figures and the EN translation.
  def test_unit
    res = impact("unit", "ch01")
    assert_exit 0, res
    assert_includes res.out, "== callbacks into ch01"
    assert_includes res.out, "  ch02: Como contei em @sec-ch01, o Perceptron já prometia demais."
    assert_includes res.out, "== hand-offs: prefacio → ch01 → ch02"
    assert_includes res.out, "== figures: assets/figures/ch01-arte.png"
    assert_includes res.out, "== translation: book/en/ch01.md will go stale"
  end

  # Guards the hand-offs at both ends of the book: the first unit has no
  # predecessor (it used to wrap around to the last unit) and the last no successor.
  def test_unit_hand_offs_at_book_edges
    first = impact("unit", "prefacio")
    assert_includes first.out, "== hand-offs: (start) → prefacio → ch01"
    last = impact("unit", "apA")
    assert_includes last.out, "== hand-offs: epilogo → apA → (end)"
  end

  # Guards interludes being part of the reading order.
  def test_unit_interlude_hand_offs
    assert_includes impact("unit", "interlude1").out, "== hand-offs: ch02 → interlude1 → ch03"
  end

  # Guards `term`: every unit line mentioning a term, case-insensitive, comments excluded.
  def test_term
    res = impact("term", "perceptron")
    assert_exit 0, res
    assert_match(/^  ch01:\d+: O Perceptron de 1958/, res.out)
    assert_match(/^  ch02:\d+: Como contei em @sec-ch01/, res.out)
    refute_includes res.out, "prefacio"
  end

  # Guards --lang: the EN edition is searched instead.
  def test_term_en
    res = impact("term", "perceptron", "--lang", "en")
    assert_match(/^  ch01:\d+: The 1958 Perceptron/, res.out)
  end

  # Guards usage errors: no mode prints the usage and fails.
  def test_usage
    res = impact
    refute res.ok?
    assert_includes res.err, "scripts/impact.rb post"
  end
end
