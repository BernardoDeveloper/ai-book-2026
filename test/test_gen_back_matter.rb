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

  # A bespoke attribution can contain provenance the generic fields omit.
  # Keep its translated date and public-domain basis through regeneration.
  def test_creditos_en_preserves_translated_attribution
    attribution = '"Sala de máquinas", U.S. Navy photograph, 1960. ' \
                  'https://commons.wikimedia.org/wiki/File:Sala.jpg. ' \
                  'Public domain (work of the U.S. federal government). Changes: resized.'
    fx.edit("assets/credits/ch03-foto.yml") do |y|
      rec = YAML.safe_load(y)
      rec["credit"]["backmatter_en"] = attribution
      rec.to_yaml
    end
    assert_exit 0, gen("en")
    assert_includes fx.read("book/en/creditos.md"), "- @fig-ch03-foto: #{attribution}"
    assert_exit 0, gen("pt")
    assert_includes fx.read("book/pt/creditos.md"), %(- @fig-ch03-foto: "Sala de máquinas", Fulano de Tal. CC BY-SA 4.0. Modificações: redimensionada.)
  end

  # Guards composites (several photos in one figure, `composite_of`): the EN
  # page credits each photo by subject and translates plural modifications.
  # 1.0.0-preview.2 shipped an empty credit line for such a figure.
  def test_creditos_en_composite
    fx.edit("assets/credits/ch03-foto.yml") do |y|
      rec = YAML.safe_load(y)
      rec.delete("source")
      rec.delete("author")
      rec["modifications"] = ["recortadas", "montadas lado a lado"]
      rec["composite_of"] = [
        { "subject" => "Ana", "author" => "Foto A", "source" => { "title" => "Ana 2025", "page_url" => "https://commons.wikimedia.org/wiki/File:A.jpg" },
          "license" => { "short" => "CC BY 2.0", "url" => "https://creativecommons.org/licenses/by/2.0" } },
        { "subject" => "Bia", "author" => "Foto B", "source" => { "title" => "Bia 2024", "page_url" => "https://commons.wikimedia.org/wiki/File:B.jpg" },
          "license" => { "short" => "CC BY 4.0", "url" => "https://creativecommons.org/licenses/by/4.0" } },
      ]
      rec.to_yaml
    end
    gen("en")
    line = fx.read("book/en/creditos.md")[/^- @fig-ch03-foto: .*$/]
    expected = [%(- @fig-ch03-foto: Ana: "Ana 2025", Foto A. https://commons.wikimedia.org/wiki/File:A.jpg.),
                "Licensed CC BY 2.0, https://creativecommons.org/licenses/by/2.0.",
                %(Bia: "Bia 2024", Foto B. https://commons.wikimedia.org/wiki/File:B.jpg.),
                "Licensed CC BY 4.0, https://creativecommons.org/licenses/by/4.0.",
                "Changes: cropped, placed side by side."].join(" ")
    assert_equal expected, line
  end

  # Guards each figure being credited once, even when referenced twice.
  def test_figure_credited_once
    fx.edit("book/pt/ch03.md") { _1 + "\n![De novo.](assets/figures/ch02-diagrama.png){#fig-ch02-diagrama}\n" }
    gen
    assert_equal 1, fx.read("book/pt/creditos.md").scan("@fig-ch02-diagrama").size
  end

  # Guards the background group: only cited background posts, in their own group at the end.
  def test_fontes_background_group
    post = "2019/10/09/episodio-antigo"
    gen
    refute_includes fx.read("book/pt/fontes.md"), "Episódios anteriores"
    fx.edit(fx.unit_rel("ch02")) { _1.sub("sources:\n", %(sources:\n  - {post: #{post}, sha256: "#{Fixture.sha(fx.post_path(post))}"}\n)) }
    gen
    pt = fx.read("book/pt/fontes.md")
    assert_includes pt, "**Episódios anteriores citados (Akitando, 2018-2023)**\n\n- 09/10/2019: *Episódio antigo*. <https://www.akitaonrails.com/2019/10/09/episodio-antigo/>"
    assert_operator pt.index("**Números e propaganda**"), :<, pt.index("Episódios anteriores")
    refute_match(/\*\*A memória de um peixe\*\*\n\n- 09\/10\/2019/, pt)
    fx.edit(fx.unit_rel("ch02", "en")) { _1.sub("sources:\n", %(sources:\n  - {post: #{post}, sha256: "#{Fixture.sha(fx.post_path(post, 'en'))}"}\n)) }
    gen("en")
    assert_includes fx.read("book/en/fontes.md"), "**Earlier episodes cited (Akitando, 2018-2023)**\n\n- 09/10/2019: *Old episode*. <https://www.akitaonrails.com/en/2019/10/09/old-episode/>"
  end
end
