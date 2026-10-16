# frozen_string_literal: true

require "minitest/autorun"
require "tmpdir"
require_relative "../scripts/print_editions"

class TestPrintEditions < Minitest::Test
  def test_print_master_is_not_another_binding
    Dir.mktmpdir do |dir|
      %w[Book-paperback.pdf Book-ebook.pdf Book.pdf].each { File.write(File.join(dir, _1), "fixture") }
      { "print" => "Book.pdf", "hardcover" => "Book.pdf", "paperback" => "Book-paperback.pdf", "ebook" => "Book-ebook.pdf" }.each do |edition, file|
        assert_equal File.join(dir, file), PrintEditions.pdf(dir, edition)
      end
      assert_raises(KeyError) { PrintEditions.pdf(dir, "invalid") }
    end
  end

  def test_missing_paperback_cannot_fall_back_to_hardcover
    Dir.mktmpdir do |dir|
      File.write(File.join(dir, "Book.pdf"), "fixture")
      assert_nil PrintEditions.pdf(dir, "paperback")
      assert_nil PrintEditions.pdf(dir, "ebook")
    end
  end

  def test_variants_alone_are_not_a_master
    Dir.mktmpdir do |dir|
      File.write(File.join(dir, "Book-paperback.pdf"), "fixture")
      assert_nil PrintEditions.pdf(dir)
    end
  end

  def test_each_language_keeps_its_own_typst_source
    assert_equal "/repo/index-pt.typ", PrintEditions.typ("/repo", "pt")
    assert_equal "/repo/index-en.typ", PrintEditions.typ("/repo", "en")
    assert_raises(ArgumentError) { PrintEditions.typ("/repo", "../pt") }
  end
end
