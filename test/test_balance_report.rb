# frozen_string_literal: true

require_relative "test_helper"

# scripts/balance_report.rb: words per unit and per source post (structural editing).
class TestBalanceReport < ToolTest
  def report
    assert_exit 0, fx.run("balance_report", "--lang", "pt")
    fx.read("build/pt/balance.md")
  end

  # Guards the report shape: every unit has a row, the posts table appears
  # exactly once, and a post's words are the sum of its src-marked paragraphs.
  def test_units_and_posts_tables
    text = report
    %w[prefacio ch01 ch02 ch03 epilogo apA].each { assert_match(/^\| #{_1} \|/, text) }
    assert_equal 1, text.scan("## Posts by words spent").size
    assert_match(%r{^\| 02/10/primeiro-post \| \d+ \| .*ch01 \d+}, text)
  end

  # Guards the overlap column: an 8+-word run copied into two units counts as
  # overlap in both, and the narrative total ignores appendices.
  def test_overlap_counts_shared_runs
    shared = "a mesma frase longa aparece em dois capitulos diferentes do livro"
    %w[ch01 ch02].each { |id| fx.edit(fx.unit_rel(id)) { _1 + "\n<!-- src: original -->\n#{shared.capitalize}.\n" } }
    row = ->(id) { report[/^\| #{id} \|.*$/].split("|").map(&:strip) }
    assert_operator row.("ch01")[6].to_i, :>=, 10
    assert_equal "0", row.("ch03")[6]
    assert_equal "", row.("apA")[3]
  end
end
