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

  # Guards --unit: a re-sync agent sees only its own unit's stale translation and
  # diff (repeatable and comma-separated), not the other units'.
  def test_unit_filter_limits_translations
    fx.init_book_git!
    fx.edit("book/pt/ch01.md") { _1.sub("calcula a próxima palavra.", "calcula a próxima palavra provável.") }
    fx.edit("book/pt/ch02.md") { _1.sub("começa do zero", "começa do nada") }
    fx.book_git("commit", "-q", "-am", "PT edits")
    both = drift("--lang", "en", "--diff")
    assert_includes both.out, "book/en/ch01.md"
    assert_includes both.out, "book/en/ch02.md"

    one = drift("--lang", "en", "--diff", "--unit", "ch01")
    assert_includes one.out, "STALE    book/en/ch01.md"
    assert_includes one.out, "palavra provável"
    refute_includes one.out, "book/en/ch02.md"
    refute_includes one.out, "do nada"

    many = drift("--lang", "en", "--unit", "ch01", "--unit", "ch02,ch03")
    assert_includes many.out, "book/en/ch01.md"
    assert_includes many.out, "book/en/ch02.md"
  end

  # Guards --unit prefacio mapping to index.md.
  def test_unit_filter_prefacio
    fx.edit("book/pt/index.md") { _1.sub("começou num blog", "começou em um blog") }
    fx.edit("book/pt/ch01.md") { _1.sub("calcula a próxima palavra.", "calcula a próxima palavra provável.") }
    res = drift("--lang", "en", "--unit", "prefacio")
    assert_includes res.out, "book/en/index.md"
    refute_includes res.out, "book/en/ch01.md"
  end

  PARKED_POST = "2026/01/15/post-janeiro"

  def park!(sources: nil)
    fx.write("book/parked/tema/pt-ch03.md", "<!-- src: #{PARKED_POST} -->\nTexto estacionado.\n")
    fx.write("book/parked/tema/sources.yml", sources.to_yaml) if sources
  end

  # Guards the Parked section: posts cited only by parked material are listed as
  # untracked without sources.yml, flagged CHANGED when the hash differs from the
  # recorded one, and never count as a problem; _staging is not scanned.
  def test_parked_posts_are_informational
    park!
    fx.write("book/pt/_staging/x.md", "---\nid: x\nsources:\n  - {post: 2026/02/10/primeiro-post, sha256: \"#{'0' * 64}\"}\n---\n")
    res = fx.run("drift")
    assert_exit 0, res
    assert_includes res.out, "== Parked"
    assert_includes res.out, "untracked tema: #{PARKED_POST}"
    refute_includes res.out, "_staging"

    assert_exit 0, fx.run("restamp", "--parked", "tema")
    assert_equal [PARKED_POST], fx.yaml("book/parked/tema/sources.yml")["posts"].map { _1["post"] }
    refute_includes fx.run("drift").out, "tema: #{PARKED_POST}"

    fx.edit_post(PARKED_POST) { _1 + "\nMudou.\n" }
    fx.inventory!
    res = fx.run("drift", "--diff")
    assert_includes res.out, "1 item(s) need attention", "only the stale analysis counts, not the parked post"
    assert_includes res.out, "CHANGED   tema: #{PARKED_POST}"
    assert_includes res.out, "+Mudou."
  end

  def cite_background(unit = "ch01")
    post = "2019/10/09/episodio-antigo"
    fx.edit(fx.unit_rel(unit)) do |t|
      t.sub("sources:\n", %(sources:\n  - {post: #{post}, sha256: "#{Fixture.sha(fx.post_path(post))}"}\n))
    end
  end

  # Guards the inventory: background posts are recorded like any post, flagged.
  def test_inventory_records_background_post
    post = fx.yaml("inventory/posts.yml")["posts"].find { _1["id"] == "2019/10/09/episodio-antigo" }
    assert post["background"]
    assert_equal "Episódio antigo", post.dig("pt", "title")
    assert_equal Fixture.sha(fx.post_path(post["id"], "en")), post.dig("en", "sha256")
    assert_equal "https://www.akitaonrails.com/2019/10/09/episodio-antigo/", post["url_pt"]
    refute fx.yaml("inventory/posts.yml")["posts"].find { _1["id"] == "2026/02/10/primeiro-post" }["background"]
  end

  # Guards that a background post needs no analysis (no NEW) and is never UNUSED.
  def test_background_post_needs_no_analysis
    res = drift
    assert_exit 0, res
    refute_includes res.out, "episodio-antigo"
  end

  # Guards staleness: a unit citing a background post goes STALE when it changes, with --diff.
  def test_background_post_change_makes_citing_unit_stale
    cite_background
    assert_exit 0, drift
    fx.edit_post("2019/10/09/episodio-antigo") { _1.sub("demais", "demais, de verdade") }
    fx.inventory!
    res = drift("--diff")
    assert_exit 1, res
    assert_includes res.out, "STALE    book/pt/ch01.md: 2019/10/09/episodio-antigo"
    assert_includes res.out, "+Anos atrás eu terceirizava decisões demais, de verdade."
    refute_includes res.out, "NEW"
  end

  # Guards a post with no English version (background posts usually have none):
  # the EN edition tracks it by its PT text, so a PT-hash entry is current and
  # restamp writes the PT hash, never an empty one.
  def test_en_unit_tracks_post_without_english_version_by_pt
    post = "2019/10/09/episodio-antigo"
    pt_sha = Fixture.sha(fx.post_path(post))
    fx.edit("inventory/posts.yml") do |y|
      data = YAML.safe_load(y)
      data["posts"].find { _1["id"] == post }["en"] = {}
      data.to_yaml
    end
    fx.edit(fx.unit_rel("ch01", "en")) do |t|
      t.sub("sources:\n", %(sources:\n  - {post: #{post}, sha256: "#{pt_sha}"}\n))
    end
    refute_includes fx.run("drift", "--lang", "en").out, "STALE    book/en/ch01.md: #{post}"
    fx.edit(fx.unit_rel("ch01", "en")) { _1.sub(pt_sha, "0" * 64) }
    assert_exit 0, fx.run("restamp", "--lang", "en", post)
    assert_includes fx.read(fx.unit_rel("ch01", "en")), %({post: #{post}, sha256: "#{pt_sha}")
  end
end
