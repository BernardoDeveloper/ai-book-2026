# frozen_string_literal: true

require_relative "test_helper"

# scripts/inventory.rb + scripts/drift.rb: the book follows the blog, and the
# EN edition follows the PT units.
class TestDrift < ToolTest
  def drift(*args) = fx.run("drift", *args)

  # Guards inventory output: one entry per post with PT/EN hashes and the blog commit.
  def test_inventory_records_hashes_and_commit
    inv = fx.yaml("inventory/posts.yml")
    assert_equal fx.blog_head, inv["blog_commit"]
    assert_equal fx.blog, inv["generated_from"]
    post = inv["posts"].find { _1["id"] == "2026/02/10/primeiro-post" }
    assert_equal Fixture.sha(fx.post_path("2026/02/10/primeiro-post")), post.dig("pt", "sha256")
    assert_equal Fixture.sha(fx.post_path("2026/02/10/primeiro-post", "en")), post.dig("en", "sha256")
    assert_equal "https://www.akitaonrails.com/en/2026/02/10/first-post/", post["url_en"]
    assert_equal [{ "text" => "o artigo", "url" => "https://example.com/ai" }], post.dig("pt", "links")
    assert_nil inv["posts"].find { _1["id"] == "2026/01/15/post-janeiro" }["en"]
  end

  # Guards the baseline: an untouched blog means no drift (exit 0).
  def test_in_sync
    res = drift
    assert_exit 0, res
    assert_match(/OK: book is in sync with blog commit [0-9a-f]{12}/, res.out)
    assert_exit 0, drift("--lang", "en")
  end

  # Guards the core duty: editing a blog post makes the citing chapters STALE (exit 1).
  def test_edited_post_makes_chapter_stale
    fx.edit_post("2026/03/05/segundo-post") { _1 + "\nUm parágrafo novo sobre compactação.\n" }
    fx.inventory!
    res = drift
    assert_exit 1, res
    assert_includes res.out, "STALE    book/pt/ch02.md: 2026/03/05/segundo-post"
    assert_includes res.out, "STALE    2026__03__05__segundo-post.yml"
    refute_includes res.out, "ch01.md:"
    refute_includes res.out, "+Um parágrafo novo", "the diff is only printed with --diff"
    refute_includes drift("--lang", "en").out, "book/en/", "the EN post didn't change"
  end

  # Guards --diff: the blog diff since the commit the book reviewed is printed.
  def test_diff_prints_blog_diff
    fx.edit_post("2026/03/05/segundo-post") { _1.sub("Cada conversa começa do zero.", "Cada conversa começa do zero, sempre.") }
    fx.inventory!
    res = drift("--diff")
    assert_includes res.out, "-Cada conversa começa do zero."
    assert_includes res.out, "+Cada conversa começa do zero, sempre."
  end

  # Guards EN post drift: index.en.md changes make the EN unit stale, not the PT one.
  def test_en_post_change
    fx.edit_post("2026/03/05/segundo-post", "en") { _1 + "\nA new paragraph.\n" }
    fx.inventory!
    assert_exit 0, drift
    res = drift("--lang", "en")
    assert_exit 1, res
    assert_includes res.out, "STALE    book/en/ch02.md: 2026/03/05/segundo-post"
  end

  # Guards new posts being reported (they need an analysis and a place in the outline).
  def test_new_post_reported
    fx.write_post("2026/05/01/post-novo", "pt", "Post novo", "Novidade.\n")
    fx.blog_git("add", "-A")
    fx.blog_git("commit", "-q", "-m", "new post")
    fx.inventory!
    res = drift
    assert_exit 1, res
    assert_includes res.out, "NEW      2026/05/01/post-novo has no analysis yet"
  end

  # Guards a post that disappears from the blog being reported as MISSING.
  def test_removed_post_reported_missing
    fx.blog_git("rm", "-q", "-r", "content/2026/04/20/post-excluido")
    fx.blog_git("commit", "-q", "-m", "remove")
    fx.inventory!
    res = drift
    assert_exit 1, res
    assert_includes res.out, "MISSING  book/pt/ch03.md: 2026/04/20/post-excluido no longer exists in the blog"
  end

  # Guards UNUSED: core posts no chapter uses are reported, unless excluded in the outline.
  def test_excluded_posts_not_unused
    res = drift
    refute_includes res.out, "UNUSED", "post-janeiro is core but excluded"
    fx.edit("book/outline.yml") { _1.sub(/^  - \{post: 01\/15\/post-janeiro.*\n/, "") }
    res = drift
    assert_includes res.out, "UNUSED   2026/01/15/post-janeiro (core)"
  end

  # Guards translation staleness: a PT unit edited after translation makes the EN unit stale.
  def test_en_translation_stale_via_translated_from
    fx.edit("book/pt/ch01.md") { _1.sub("calcula a próxima palavra.", "calcula a próxima palavra provável.") }
    res = drift("--lang", "en")
    assert_exit 1, res
    assert_includes res.out, "STALE    book/en/ch01.md: book/pt/ch01.md changed since translation"
    refute_includes res.out, "book/en/ch02.md"
  end

  # Guards --diff for translations: it finds the PT version that was translated
  # in the book's git history and shows the word diff since then.
  def test_en_diff_shows_pt_changes_since_translation
    fx.init_book_git!
    fx.edit("book/pt/ch01.md") { _1.sub("calcula a próxima palavra.", "calcula a próxima palavra provável.") }
    fx.book_git("commit", "-q", "-am", "PT edit")
    res = drift("--lang", "en", "--diff")
    assert_exit 1, res
    assert_match(/PT changes since the translated version \([0-9a-f]{8}\)/, res.out)
    assert_includes res.out, "[-palavra.-]{+palavra provável.+}"
  end

  # Guards the fallback when the translated PT version isn't in git history.
  def test_en_diff_without_history
    fx.edit("book/pt/ch01.md") { _1.sub("calcula a próxima palavra.", "calcula a próxima palavra provável.") }
    res = drift("--lang", "en", "--diff")
    assert_includes res.out, "translated version not found in git history"
  end
end
