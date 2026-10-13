# frozen_string_literal: true

require_relative "test_helper"

# scripts/outline_check.rb: every AI post placed or excluded; outline ids exist.
class TestOutlineCheck < ToolTest
  def check = fx.run("outline_check")

  # Guards the baseline: every analysed core post is placed or excluded.
  def test_clean_outline
    res = check
    assert_exit 0, res
    assert_includes res.out, "3 posts used, 2 excluded, 0 error(s)"
  end

  # Guards coverage: a core post with an analysis but no place in the outline is an error.
  def test_unplaced_core_post
    fx.write("inventory/analysis/2026__05__01__novo.yml", %(id: "2026/05/01/novo"\nsource_sha256: "x"\nai_relevance: core\n))
    res = check
    assert_exit 1, res
    assert_includes res.out, "UNPLACED 2026/05/01/novo (core)"
  end

  # Guards tangential posts not needing a place.
  def test_tangential_post_not_required
    fx.write("inventory/analysis/2026__05__01__novo.yml", %(id: "2026/05/01/novo"\nsource_sha256: "x"\nai_relevance: tangential\n))
    assert_exit 0, check
  end

  # Guards typos in post ids (sources and excluded) that would silently drop a post.
  def test_unknown_id
    fx.edit("book/outline.yml") { _1.sub("primary: [03/05/segundo-post]", "primary: [03/05/segundo-pots]") }
    res = check
    assert_exit 1, res
    assert_includes res.out, "UNKNOWN 2026/03/05/segundo-pots"
  end

  # Guards against a post being both placed and excluded.
  def test_used_and_excluded
    fx.edit("book/outline.yml") { _1.sub("primary: [04/01/terceiro-post]", "primary: [04/01/terceiro-post, 04/20/post-excluido]") }
    res = check
    assert_includes res.out, "BOTH used+excluded 2026/04/20/post-excluido: ch03(p)"
  end
end
