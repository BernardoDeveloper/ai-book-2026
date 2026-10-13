# frozen_string_literal: true

require_relative "test_helper"

# scripts/fix_front_matter.rb: front-matter `title:` -> `chapter:` (Quarto
# would print a `title:` as a second heading).
class TestFixFrontMatter < ToolTest
  TEXT = <<~MD
    ---
    id: chx
    title: "Um título"
    sources: []
    ---

    # Um título {#sec-chx}

    title: isto é prosa e fica como está.
  MD

  # Guards the rename touching only the front matter, and being idempotent.
  def test_title_to_chapter_idempotent
    fx.write("book/pt/chx.md", TEXT)
    res = fx.run("fix_front_matter", fx.path("book/pt/chx.md"))
    assert_exit 0, res
    expected = TEXT.sub("title: \"Um", "chapter: \"Um")
    assert_equal expected, fx.read("book/pt/chx.md")
    assert_includes res.err, "renamed title -> chapter"

    res = fx.run("fix_front_matter", fx.path("book/pt/chx.md"))
    assert_exit 0, res
    assert_equal expected, fx.read("book/pt/chx.md")
    assert_empty res.err
  end

  # Guards files without front matter (or already fixed) being left alone.
  def test_leaves_other_files_alone
    fx.write("book/pt/solto.md", "title: sem front matter\n")
    before = fx.read("book/pt/ch01.md")
    fx.run("fix_front_matter", fx.path("book/pt/solto.md"), fx.path("book/pt/ch01.md"))
    assert_equal "title: sem front matter\n", fx.read("book/pt/solto.md")
    assert_equal before, fx.read("book/pt/ch01.md")
  end
end
