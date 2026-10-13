# frozen_string_literal: true

require_relative "test_helper"

# scripts/merge_glossary.rb: merge per-chapter glossary proposals into
# book/back/glossary-<lang>.yml without touching curated definitions.
class TestMergeGlossary < ToolTest
  def propose(chapter, entries, lang: "pt")
    fx.write("book/#{lang}/_gls/#{chapter}.yml", entries.to_yaml)
  end

  def glossary(lang = "pt") = fx.yaml("book/back/glossary-#{lang}.yml")

  # Guards new keys being added, sorted, with the header comment preserved.
  def test_adds_new_keys
    propose("ch01", { "gpu" => { "term" => "GPU", "long" => "Graphics Processing Unit", "def" => "Placa de vídeo." } })
    res = fx.run("merge_glossary")
    assert_exit 0, res
    assert_includes res.err, "1 added (gpu); 4 total"
    assert_equal "Placa de vídeo.", glossary["gpu"]["def"]
    assert_equal %w[agente gpu llm token], glossary.keys
    assert fx.read("book/back/glossary-pt.yml").start_with?("# Glossário de teste.")
  end

  # Guards curated definitions: a conflicting proposal is reported, never applied.
  def test_never_overwrites_curated
    propose("ch02", { "llm" => { "term" => "LLM", "def" => "Outra definição." } })
    res = fx.run("merge_glossary")
    assert_includes res.err, "conflict llm (ch02.yml): keeping curated definition"
    assert_equal "Modelo de linguagem de grande porte.", glossary["llm"]["def"]
  end

  # Guards unused keys being reported (dead entries shouldn't ship).
  def test_reports_unused
    res = fx.run("merge_glossary")
    assert_exit 0, res
    assert_includes res.err, "unused glossary keys: agente"
  end

  # Guards unknown keys used in chapters: reported, exit 1.
  def test_reports_unknown
    fx.edit("book/pt/ch03.md") { _1 + "\nUma [GPU]{.gls} e [placas]{.gls key=placa}.\n" }
    res = fx.run("merge_glossary")
    assert_exit 1, res
    assert_includes res.err, "UNKNOWN keys used in chapters: gpu, placa"
  end

  # Guards per-language merging: EN proposals go to glossary-en.yml only.
  def test_en_edition
    propose("ch01", { "gpu" => { "term" => "GPU", "def" => "Graphics card." } }, lang: "en")
    fx.run("merge_glossary", "en")
    assert_equal "Graphics card.", glossary("en")["gpu"]["def"]
    refute glossary("pt").key?("gpu")
  end
end
