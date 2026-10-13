# frozen_string_literal: true

require_relative "test_helper"

# scripts/restamp.rb: after review, record that the book matches the post's
# current version (sha256 + the blog commit it was reviewed at).
class TestRestamp < ToolTest
  POST = "2026/03/05/segundo-post"
  OTHER = "2026/02/10/primeiro-post"

  def entry(text, post) = text[/^  - \{post: #{Regexp.escape(post)}, .*\}$/]

  # Guards PT restamp: only the matching entry changes (new sha256 + commit),
  # the other sources, the body and the chapter-level blog_commit stay; drift is clean afterwards.
  def test_pt_restamp_updates_only_matching_entry
    before = fx.read("book/pt/ch02.md")
    fx.edit_post(POST) { _1 + "\nMudança.\n" }
    fx.inventory!
    assert_exit 1, fx.run("drift")

    res = fx.run("restamp", POST)
    assert_exit 0, res
    after = fx.read("book/pt/ch02.md")
    new_sha = Fixture.sha(fx.post_path(POST))
    assert_equal %(  - {post: #{POST}, sha256: "#{new_sha}", commit: "#{fx.blog_head}"}), entry(after, POST)
    assert_equal entry(before, OTHER), entry(after, OTHER)
    assert_equal before[/^blog_commit: .*$/], after[/^blog_commit: .*$/]
    assert_equal before.split(/^---$/, 3)[2], after.split(/^---$/, 3)[2], "prose untouched"
    assert_equal fx.read("book/en/ch02.md").lines.grep(/segundo-post/).size, 2, "EN unit untouched"
    refute_includes fx.read("book/en/ch02.md"), new_sha
    assert_includes fx.read("inventory/analysis/2026__03__05__segundo-post.yml"), %(source_sha256: "#{new_sha}")
    assert_exit 0, fx.run("drift")
  end

  # Guards re-restamping an entry that already has a commit (no duplicate `commit:`).
  def test_restamp_twice
    fx.edit_post(POST) { _1 + "\nMudança.\n" }
    fx.inventory!
    fx.run("restamp", POST)
    fx.edit_post(POST) { _1 + "\nOutra.\n" }
    fx.inventory!
    assert_exit 0, fx.run("restamp", POST)
    assert_equal 1, fx.read("book/pt/ch02.md").scan(", commit:").size
    assert_exit 0, fx.run("drift")
  end

  # Guards --lang en: EN units get the index.en.md hash; analyses (of the PT post) are not touched.
  def test_en_restamp
    analysis = fx.read("inventory/analysis/2026__03__05__segundo-post.yml")
    pt_before = fx.read("book/pt/ch02.md")
    fx.edit_post(POST, "en") { _1 + "\nChange.\n" }
    fx.inventory!
    assert_exit 1, fx.run("drift", "--lang", "en")

    res = fx.run("restamp", "--lang", "en", POST)
    assert_exit 0, res
    en_sha = Fixture.sha(fx.post_path(POST, "en"))
    assert_equal %(  - {post: #{POST}, sha256: "#{en_sha}", commit: "#{fx.blog_head}"}), entry(fx.read("book/en/ch02.md"), POST)
    assert_equal pt_before, fx.read("book/pt/ch02.md")
    assert_equal analysis, fx.read("inventory/analysis/2026__03__05__segundo-post.yml")
    assert_exit 0, fx.run("drift", "--lang", "en")
  end

  # Guards every citing unit being restamped, not just the first one.
  def test_restamps_every_citing_unit
    fx.edit_post(OTHER) { _1 + "\nMudança.\n" }
    fx.inventory!
    res = fx.run("restamp", OTHER)
    %w[index.md ch01.md ch02.md].each { assert_includes res.err, "restamped #{_1} for #{OTHER}" }
    assert_exit 0, fx.run("drift")
  end

  # Guards typos: an unknown post id aborts without touching anything.
  def test_unknown_post
    res = fx.run("restamp", "2026/09/09/nada")
    refute res.ok?
    assert_includes res.err, "unknown post 2026/09/09/nada"
  end
end
