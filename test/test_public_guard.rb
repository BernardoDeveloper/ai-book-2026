# frozen_string_literal: true

require_relative "test_helper"

# scripts/public_guard.rb (pre-push hook): no private names in tracked files
# or commit messages of the public repository.
class TestPublicGuard < ToolTest
  SECRET = "casa-secreta.lan"

  def setup
    super
    fx.init_book_git!
  end

  def forbid
    fx.write("private/forbidden.txt", "# hosts\n\n#{SECRET}\n")
  end

  # Guards CI and fresh clones: without private/forbidden.txt it is a no-op (exit 0).
  def test_noop_without_forbidden_list
    fx.write("book/pt/notas.md", "servidor #{SECRET}\n")
    fx.book_git("add", "-A")
    fx.book_git("commit", "-q", "-m", "notes")
    res = fx.run("public_guard")
    assert_exit 0, res
    assert_empty res.out
  end

  # Guards the baseline: a clean repository passes.
  def test_clean_repository
    forbid
    res = fx.run("public_guard")
    assert_exit 0, res
    assert_includes res.out, "public guard: clean"
  end

  # Guards tracked files: a forbidden pattern (case-insensitive) blocks the push, with file:line.
  def test_blocks_tracked_file
    forbid
    fx.write("book/pt/notas.md", "linha um\nO servidor CASA-SECRETA.LAN caiu.\n")
    fx.book_git("add", "book/pt/notas.md")
    res = fx.run("public_guard")
    assert_exit 1, res
    assert_includes res.err, "push blocked"
    assert_includes res.err, "book/pt/notas.md:2"
  end

  # Guards untracked files being ignored (only what would be pushed matters).
  def test_ignores_untracked_file
    forbid
    fx.write("rascunho.md", SECRET)
    assert_exit 0, fx.run("public_guard")
  end

  # Guards commit messages: a forbidden pattern in any commit of the range blocks the push.
  def test_blocks_commit_message
    forbid
    fx.write("book/pt/ok.md", "nada\n")
    fx.book_git("add", "-A")
    fx.book_git("commit", "-q", "-m", "deploy to #{SECRET}")
    res = fx.run("public_guard")
    assert_exit 1, res
    assert_match(/commit message: .*#{Regexp.escape(SECRET)}/, res.err)
  end

  # Guards the inventory/ exemption: it mirrors the public blog.
  def test_inventory_exempt
    forbid
    fx.write("inventory/links.yml", "- url: https://#{SECRET}/x\n")
    fx.book_git("add", "-A")
    fx.book_git("commit", "-q", "-m", "links")
    assert_exit 0, fx.run("public_guard")
  end
end
