# frozen_string_literal: true

require_relative "test_helper"

# scripts/persona_compare.rb: compares two persona review rounds.
class TestPersonaCompare < ToolTest
  def persona(dir, name, scores, annotations = [])
    fx.write("#{dir}/#{name}.yml", { "persona" => name, "units" => scores.map { |u, s| { "unit" => u, "score" => s } },
                                     "annotations" => annotations }.to_yaml)
  end

  # Guards the comparison: per-unit means and deltas, book average, units
  # scored by a single reader skipped, annotation counts and --grep.
  def test_compare_rounds
    persona("r1", "pai", { "ch01" => 2, "ch02" => 4, "apC" => 5 }, [{ "unit" => "ch01", "type" => "logic", "why" => "linha reta" }])
    persona("r1", "curioso", { "ch01" => 4, "ch02" => 4 })
    persona("r2", "pai", { "ch01" => 4, "ch02" => 4 }, [{ "unit" => "ch02", "type" => "boring", "why" => "vetorial" }])
    persona("r2", "curioso", { "ch01" => 4, "ch02" => 2 })
    res = fx.run("persona_compare", fx.path("r1"), fx.path("r2"), "--grep", "vetorial")
    assert_exit 0, res
    assert_match(/^ch01 .*3\.0  4\.0  \+1\.0$/, res.out)
    assert_match(/^ch02 .*4\.0  3\.0  -1\.0$/, res.out)
    refute_match(/^apC/, res.out)
    assert_includes res.out, "book average: 3.50 -> 3.50"
    assert_includes res.out, %(annotations old: {"logic" => 1})
    assert_match(/pai\s+ch02 boring: vetorial/, res.out)
  end
end
