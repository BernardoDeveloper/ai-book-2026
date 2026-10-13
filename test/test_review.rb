# frozen_string_literal: true

require_relative "test_helper"

# scripts/review.rb: copyedit findings files (reviews/<version>/<lang>/part*.yml):
# schema + quote validation, stable ids, summary, post-apply status.
class TestReview < ToolTest
  DIR = "reviews/v1/pt"

  def review(cmd, *args) = fx.run("review", cmd, fx.path(DIR), *args)

  def line_of(rel, needle) = fx.read(rel).lines.index { _1.include?(needle) } + 1

  def item(unit: "ch01", quote: "calcula a próxima palavra", line: nil, **over)
    { "unit" => unit, "line" => line || line_of("book/pt/#{unit == 'prefacio' ? 'index' : unit}.md", quote), "quote" => quote,
      "category" => "clarity", "severity" => "low", "problem" => "Obscuro.", "suggestion" => "Reescrever." }.merge(over.transform_keys(&:to_s))
  end

  def write_part(name, items, wrap: nil)
    doc = wrap ? { wrap => items } : items
    fx.write("#{DIR}/#{name}", doc.to_yaml)
  end

  # Guards the happy path: valid items pass, and ids "<part>.<n>" are added in
  # file order (part = digit after "part" in the file name), the file staying valid YAML.
  def test_validate_adds_ids
    write_part("part2-meio.yml", [item, item(unit: "ch02", quote: "Cada conversa começa do zero")])
    res = review("validate")
    assert_exit 0, res
    assert_includes res.out, "2 item(s), 0 error(s)"
    assert_equal %w[2.1 2.2], YAML.load_file(fx.path("#{DIR}/part2-meio.yml")).map { _1["id"] }
  end

  # Guards idempotence: a file that already has ids is not rewritten, and a hash
  # wrapper (findings:/items:) survives the rewrite.
  def test_validate_rewrites_only_when_ids_missing
    write_part("part1-a.yml", [item], wrap: "findings")
    write_part("part3-c.yml", [item(id: "3.1")], wrap: "items")
    before = fx.read("#{DIR}/part3-c.yml")
    assert_exit 0, review("validate")
    assert_equal before, fx.read("#{DIR}/part3-c.yml")
    assert_equal "1.1", YAML.load_file(fx.path("#{DIR}/part1-a.yml")).fetch("findings").first["id"]
    again = fx.read("#{DIR}/part1-a.yml")
    assert_exit 0, review("validate")
    assert_equal again, fx.read("#{DIR}/part1-a.yml")
  end

  # Guards schema errors: missing fields and bad category/severity exit 1.
  def test_validate_schema_errors
    bad = item.tap { _1.delete("problem") }
    write_part("part1-a.yml", [bad, item(category: "typo"), item(severity: "urgent")])
    res = review("validate")
    assert_exit 1, res
    assert_includes res.out, "#1.1: missing problem"
    assert_includes res.out, "category 'typo' not one of"
    assert_includes res.out, "severity 'urgent' not one of"
  end

  # Guards quote lookup: a quote absent from the unit fails; one that moved is
  # reported with its actual line but is not an error.
  def test_validate_quote_not_found_and_moved
    write_part("part1-a.yml", [item(quote: "frase que não existe", line: 3)])
    res = review("validate")
    assert_exit 1, res
    assert_includes res.out, "quote not found in book/pt/ch01.md: frase que não existe"

    actual = line_of("book/pt/ch01.md", "calcula a próxima palavra")
    write_part("part1-a.yml", [item(line: actual + 7)])
    res = review("validate")
    assert_exit 0, res
    assert_includes res.out, "moved, line #{actual + 7} -> #{actual}"
  end

  # Guards unit mapping: prefacio -> index.md, glossary -> glossary-<lang>.yml
  # (quote is the key, no line needed), unknown units fail.
  def test_validate_prefacio_glossary_and_unknown_unit
    write_part("part1-a.yml", [item(unit: "prefacio", quote: "começou num blog"),
                               item(unit: "glossary", quote: "token", line: 0).tap { _1.delete("line") }])
    assert_exit 0, review("validate")
    write_part("part1-a.yml", [item(unit: "glossary", quote: "sem-chave", line: 0).tap { _1.delete("line") }, item.merge("unit" => "ch99")])
    res = review("validate")
    assert_exit 1, res
    assert_includes res.out, "glossary key 'sem-chave' not in book/back/glossary-pt.yml"
    assert_includes res.out, "unit ch99 has no book/pt/ch99.md"
  end

  # Guards summary: one compact line per item, --grep over problem + suggestion, counts by category/severity.
  def test_summary_grep_and_counts
    write_part("part1-a.yml", [item(problem: "Comparativo quebrado", category: "error", severity: "high"),
                               item(unit: "ch02", quote: "Cada conversa começa do zero", suggestion: "Cortar")])
    res = review("summary")
    assert_exit 0, res
    assert_match(/^1\.1\s+error\/high\s+ch01:\d+\s+"calcula a próxima palavra"\s+Comparativo quebrado/, res.out)
    assert_includes res.out, "2 of 2 item(s)"
    assert_includes res.out, "by category: clarity 1, error 1"
    res = review("summary", "--grep", "cortar")
    assert_includes res.out, "1 of 2 item(s)"
    refute_includes res.out, "Comparativo"
  end

  # Guards status: items whose quote is still verbatim are "unchanged"; ids under
  # a "Rejected"/"No change" triage heading (ranges too) are "rejected"; edited ones vanish.
  def test_status_unchanged_and_rejected
    write_part("part1-a.yml", [item, item(quote: "Cada conversa", unit: "ch02"), item(quote: "Perceptron", unit: "ch02"),
                               item(quote: "Traduzi vinte anos", unit: "interlude1")])
    fx.write("#{DIR}/triage.md", <<~MD)
      # Triage

      Default: accept. See 1.1 for the first (this is not a rejection).

      ## Rejected or deferred

      - 1.2-1.3 rejected: keep.

      ## Outcome

      Item 1.4 was fine.
    MD
    fx.edit("book/pt/interlude1.md") { _1.sub("Traduzi vinte anos", "Eu traduzi vinte anos") }
    res = review("status")
    assert_exit 0, res
    assert_match(/^unchanged\s+1\.1\s+ch01/, res.out)
    assert_match(/^rejected\s+1\.2\s+ch02/, res.out)
    assert_match(/^rejected\s+1\.3\s+ch02/, res.out)
    refute_includes res.out, "1.4 "
    assert_includes res.out, "1 unchanged (quote still present), 0 glossary to check by hand, 2 rejected, 1 edited away"
  end
end
