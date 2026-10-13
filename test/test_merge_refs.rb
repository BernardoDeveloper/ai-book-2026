# frozen_string_literal: true

require_relative "test_helper"

# scripts/merge_refs.rb: merge per-chapter bibliography proposals into
# book/back/references.yaml, dedupe by URL, keep keys consistent book-wide.
class TestMergeRefs < ToolTest
  def propose(chapter, refs)
    fx.write("book/pt/_refs/#{chapter}.yaml", { "references" => refs }.to_yaml)
  end

  def bib = fx.yaml("book/back/references.yaml")["references"]
  def ids = bib.map { _1["id"] }

  def setup
    super
    # ch01 proposes the bibliography's smith2026ai under another key and URL
    # spelling; ch02 cites that alias without proposing it.
    propose("ch01", [{ "id" => "smith-ai", "title" => "Smith", "URL" => "http://www.example.com/ai/", "note" => "cited-by: 2026/02/10/primeiro-post" },
                     { "id" => "novo2026", "title" => "Novo", "URL" => "https://example.net/novo", "note" => "cited-by: 2026/02/10/primeiro-post" }])
    # ch02 proposes doe2026 for a different work than the bibliography's doe2026.
    propose("ch02", [{ "id" => "doe2026", "title" => "Another Doe", "URL" => "https://example.org/another-doe", "note" => "cited-by: 2026/03/05/segundo-post" }])
    fx.edit("book/pt/ch01.md") { _1.sub("[@smith2026ai]", "[@smith-ai; @novo2026]") + "\n<!-- src: original -->\nComo em [@doe2026].\n" }
    fx.edit("book/pt/ch02.md") { _1.sub("[@doe2026]", "[@doe2026; @smith-ai]") }
  end

  # Guards dedupe by normalized URL (scheme, www, trailing slash, case) and note union.
  def test_dedupe_by_url
    res = fx.run("merge_refs")
    assert_exit 0, res
    assert_equal %w[doe2026 doe2026b novo2026 smith2026ai], ids
    smith = bib.find { _1["id"] == "smith2026ai" }
    assert_equal "https://example.com/ai", smith["URL"], "the bibliography's entry wins"
  end

  # Guards aliases being rewritten book-wide, including a unit that cites
  # the alias but didn't propose it.
  def test_alias_rewritten_book_wide
    fx.run("merge_refs")
    assert_includes fx.read("book/pt/ch01.md"), "[@smith2026ai; @novo2026]"
    assert_includes fx.read("book/pt/ch02.md"), "@smith2026ai]"
    refute_includes fx.read("book/pt/ch02.md"), "@smith-ai"
  end

  # Guards key clashes: the newcomer is renamed only in the unit that proposed it.
  def test_key_clash_renamed_only_in_proposer
    res = fx.run("merge_refs")
    assert_includes res.err, "key clash doe2026 (ch02) -> doe2026b"
    assert_equal "https://example.org/another-doe", bib.find { _1["id"] == "doe2026b" }["URL"]
    assert_includes fx.read("book/pt/ch02.md"), "[@doe2026b;"
    assert_includes fx.read("book/pt/ch01.md"), "Como em [@doe2026]."
    assert_includes fx.read("book/pt/ch03.md"), "[@doe2026]"
  end

  # Guards idempotence: a second run (rake build always merges) must change
  # nothing. It used to treat the renamed clash as an alias and rewrite every
  # legitimate @doe2026 in the book to @doe2026b.
  def test_idempotent_second_run
    fx.run("merge_refs")
    snapshot = %w[book/back/references.yaml book/pt/ch01.md book/pt/ch02.md book/pt/ch03.md].to_h { [_1, fx.read(_1)] }
    res = fx.run("merge_refs")
    assert_exit 0, res
    snapshot.each { |file, text| assert_equal text, fx.read(file), "#{file} changed on the second run" }
  end

  # Guards notes: cited-by provenance from every proposer is kept (union).
  def test_notes_unioned
    propose("ch03", [{ "id" => "smith2026ai", "URL" => "https://example.com/ai", "note" => "cited-by: 2026/04/01/terceiro-post" }])
    fx.run("merge_refs")
    assert_equal "cited-by: 2026/02/10/primeiro-post, 2026/04/01/terceiro-post", bib.find { _1["id"] == "smith2026ai" }["note"]
  end

  # Guards key rewriting boundaries: @smith-ai must not touch @smith-ai2 or emails.
  def test_rewrite_respects_key_boundaries
    fx.edit("book/pt/ch03.md") { _1 + "\nVer [@smith-ai2].\n" }
    fx.run("merge_refs")
    assert_includes fx.read("book/pt/ch03.md"), "[@smith-ai2]"
  end
end
