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

  def tf_line(rel) = fx.read(rel)[/^translated_from: .*$/]

  # Guards --translation: only the named EN unit's translated_from sha256 is set
  # to the current PT hash; other EN units, source hashes and prose stay.
  def test_translation_restamp_touches_only_that_hash
    fx.edit("book/pt/ch01.md") { _1.sub("calcula a próxima palavra.", "calcula a próxima palavra provável.") }
    fx.edit("book/pt/ch02.md") { _1.sub("começa do zero", "começa do nada") }
    assert_exit 1, fx.run("drift", "--lang", "en")
    before = fx.read("book/en/ch01.md")
    other = fx.read("book/en/ch02.md")

    assert_exit 0, fx.run("restamp", "--translation", "ch01")
    after = fx.read("book/en/ch01.md")
    assert_equal %(translated_from: {file: book/pt/ch01.md, sha256: "#{fx.sha('book/pt/ch01.md')}"}), tf_line("book/en/ch01.md")
    assert_equal before.sub(/^translated_from: .*$/, ""), after.sub(/^translated_from: .*$/, "")
    assert_equal other, fx.read("book/en/ch02.md")
    res = fx.run("drift", "--lang", "en")
    refute_includes res.out, "book/en/ch01.md"
    assert_includes res.out, "book/en/ch02.md"
  end

  # Guards the comma list, the prefacio -> index.md mapping and --all-translations.
  def test_translation_list_and_all
    fx.edit("book/pt/index.md") { _1.sub("começou num blog", "começou em um blog") }
    fx.edit("book/pt/ch01.md") { _1 + "\nMais.\n" }
    fx.edit("book/pt/ch02.md") { _1 + "\nMais.\n" }
    assert_exit 0, fx.run("restamp", "--translation", "prefacio,ch01")
    assert_equal %(translated_from: {file: book/pt/index.md, sha256: "#{fx.sha('book/pt/index.md')}"}), tf_line("book/en/index.md")
    assert_includes fx.run("drift", "--lang", "en").out, "book/en/ch02.md"
    assert_exit 0, fx.run("restamp", "--all-translations")
    assert_exit 0, fx.run("drift", "--lang", "en")
  end

  # Guards typos: an unknown unit aborts.
  def test_translation_unknown_unit
    res = fx.run("restamp", "--translation", "nada")
    refute res.ok?
    assert_includes res.err, "unknown unit nada"
  end
end
