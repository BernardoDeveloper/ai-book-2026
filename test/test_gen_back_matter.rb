# frozen_string_literal: true

require_relative "test_helper"

# scripts/gen_back_matter.rb: glossary/bibliography placeholders, the sources
# page (fontes) and the image credits page (creditos).
class TestGenBackMatter < ToolTest
  def gen(lang = "pt") = fx.run("gen_back_matter", lang)

  # Guards the generated pages' ids: other units and filters cross-reference them.
  def test_generated_page_ids
    %w[pt en].each do |lang|
      assert_exit 0, gen(lang)
      { "glossario" => "sec-glossario", "bibliografia" => "sec-bibliografia",
        "fontes" => "sec-fontes", "creditos" => "sec-creditos" }.each do |file, id|
        assert_match(/\A# .+ \{##{id} \.unnumbered\}/, fx.read("book/#{lang}/#{file}.md"))
      end
    end
    assert_includes fx.read("book/pt/glossario.md"), "::: {#glossary}"
    assert_includes fx.read("book/pt/bibliografia.md"), "::: {#refs}"
    assert_includes fx.read("book/en/glossario.md"), "# Glossary {#sec-glossario"
  end

  # Guards fontes: each unit (in reading order) lists its posts, sorted, with
  # date, title and URL; units without sources are skipped.
  def test_fontes_lists_posts_per_unit
    gen
    text = fx.read("book/pt/fontes.md")
    assert_includes text, "**Prefácio**\n\n- 10/02/2026: *Primeiro post*. <https://www.akitaonrails.com/2026/02/10/primeiro-post/>"
    assert_includes text, "**A memória de um peixe**\n\n- 10/02/2026: *Primeiro post*. " \
                          "<https://www.akitaonrails.com/2026/02/10/primeiro-post/>\n- 05/03/2026: *Segundo post*."
    assert_operator text.index("**Um gerador de texto**"), :<, text.index("**Interlúdio: Pausa**")
    assert_operator text.index("**Interlúdio: Pausa**"), :<, text.index("**Números e propaganda**")
    refute_includes text, "**Epílogo**"
  end

  # Guards the EN sources page: English titles and URLs of the author's EN posts.
  def test_fontes_en
    gen("en")
    text = fx.read("book/en/fontes.md")
    assert_includes text, "**A Text Generator**\n\n- 10/02/2026: *First post*. <https://www.akitaonrails.com/en/2026/02/10/first-post/>"
  end

  # Guards creditos: AI illustrations disclose the model, diagrams get the
  # default line, photos use the stored Portuguese attribution, plus the cover line.
  def test_creditos_pt
    gen
    text = fx.read("book/pt/creditos.md")
    assert_includes text, "- @fig-ch01-arte: Ilustração gerada por IA: gpt-image-test, 2026-10-01."
    assert_includes text, "- @fig-ch02-diagrama: Diagrama original do livro."
    assert_includes text, %(- @fig-ch03-foto: "Sala de máquinas", Fulano de Tal. CC BY-SA 4.0. Modificações: redimensionada.)
    assert_match(/^- Capa: Ilustração gerada por IA \(gpt-image-cover, 2026-10-02\); tipografia do autor/, text)
  end

  # Guards translated figure paths (assets/figures/en/x.png) using the canonical
  # record, and photo credits composed in English from the record's fields.
  def test_creditos_en
    gen("en")
    text = fx.read("book/en/creditos.md")
    assert_includes text, "- @fig-ch01-arte: AI-generated illustration: gpt-image-test, 2026-10-01."
    assert_includes text, %(- @fig-ch03-foto: "Sala de máquinas", Fulano de Tal. https://commons.wikimedia.org/wiki/File:Sala.jpg. ) +
                          "Licensed CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0. Changes: resized, converted to grayscale."
    refute_match(/Modificações|redimensionada/, text)
    assert_match(/^- Cover: AI-generated illustration \(gpt-image-cover, 2026-10-02\); typography by the author/, text)
  end

  # Guards public-domain photos: no "Licensed" wording for PD/CC0.
  def test_creditos_en_public_domain
    fx.edit("assets/credits/ch03-foto.yml") { _1.sub("short: CC BY-SA 4.0", "short: Public domain") }
    gen("en")
    assert_includes fx.read("book/en/creditos.md"), "File:Sala.jpg. Public domain. Changes:"
  end

  # Guards each figure being credited once, even when referenced twice.
  def test_figure_credited_once
    fx.edit("book/pt/ch03.md") { _1 + "\n![De novo.](assets/figures/ch02-diagrama.png){#fig-ch02-diagrama}\n" }
    gen
    assert_equal 1, fx.read("book/pt/creditos.md").scan("@fig-ch02-diagrama").size
  end
end
