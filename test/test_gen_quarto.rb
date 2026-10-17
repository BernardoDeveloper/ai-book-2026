# frozen_string_literal: true

require_relative "test_helper"

# scripts/gen_quarto.rb: the Quarto profile (_quarto-<lang>.yml) generated from book/outline.yml.
class TestGenQuarto < ToolTest
  def test_uiclap_is_isolated_pt_print_profile_without_amazon_isbn
    fx.edit("book/outline.yml") { _1.sub("meta:\n", "meta:\n  isbn:\n    pt: '9798162465683'\n  isbn_paperback:\n    pt: '9798162938088'\n") }
    gen
    original = fx.read("_quarto-pt.yml")
    assert_exit 0, fx.run("gen_quarto", "pt", "uiclap")
    uiclap = profile("pt-uiclap")
    assert_equal "build/uiclap/pt", uiclap.dig("project", "output-dir")
    assert_equal "Competente-o-Suficiente-uiclap-16x23", uiclap.dig("book", "output-file")
    assert_equal "160mm", uiclap["print-width"]
    assert_equal "230mm", uiclap["print-height"]
    refute_match(/9798162465683|9798162938088|ISBN/, uiclap["colophon"])
    refute uiclap.key?("colophon-paperback")
    assert_equal original, fx.read("_quarto-pt.yml")
    assert_exit 1, fx.run("gen_quarto", "en", "uiclap")
  end

  def test_uiclap_uses_only_its_configured_isbn
    fx.edit("book/outline.yml") { _1.sub("meta:\n", "meta:\n  isbn_uiclap:\n    pt: '9780000000002'\n") }
    fx.run("gen_back_matter", "pt")
    assert_exit 0, fx.run("gen_quarto", "pt", "uiclap")
    assert_includes profile("pt-uiclap")["colophon"], "ISBN 9780000000002 (edição em brochura, UICLAP)"
  end

  def gen(lang = "pt", env: {})
    fx.run("gen_back_matter", lang) # the generated appendices must exist
    fx.run("gen_quarto", lang, env: env)
  end

  def profile(lang = "pt") = fx.yaml("_quarto-#{lang}.yml")

  # Guards the chapter list: front, parts (with their chapters), interludes
  # riding inside the preceding part, back matter, appendices in order.
  def test_structure_pt
    res = gen
    assert_exit 0, res
    book = profile["book"]
    assert_equal "Livro de Teste", book["title"]
    assert_equal ["index.md",
                  { "part" => "Parte I: Começo", "chapters" => %w[book/pt/ch01.md book/pt/ch02.md book/pt/interlude1.md] },
                  { "part" => "Parte II: Meio", "chapters" => %w[book/pt/ch03.md] },
                  "book/pt/epilogo.md"], book["chapters"]
    assert_equal %w[book/pt/apA.md book/pt/fontes.md book/pt/creditos.md book/pt/glossario.md book/pt/bibliografia.md],
                 book["appendices"]
    assert_equal "build/pt", profile.dig("project", "output-dir")
    assert_equal "book/back/glossary-pt.yml", profile["glossary-file"]
    assert_equal "Apêndice", profile.dig("crossref", "appendix-title")
  end

  # Guards the home page: Quarto needs index.md at the root, copied from the edition's preface.
  def test_root_index_copied_from_preface
    gen
    assert_equal fx.read("book/pt/index.md"), fx.read("index.md")
    gen("en")
    assert_equal fx.read("book/en/index.md"), fx.read("index.md")
  end

  # Guards PARTIAL=1 previews: missing units are skipped and the preface becomes a stub.
  def test_partial_stub
    File.delete(fx.path("book/pt/index.md"))
    File.delete(fx.path("book/pt/ch02.md"))
    res = gen(env: { "PARTIAL" => "1" })
    assert_exit 0, res
    assert_includes fx.read("index.md"), "# Prévia {#sec-prefacio .unnumbered}"
    chapters = profile["book"]["chapters"]
    assert_equal "index.md", chapters.first
    assert_equal %w[book/pt/ch01.md book/pt/interlude1.md], chapters[1]["chapters"]
  end

  # Guards the full build failing loudly (exit 2) when a unit file is missing.
  def test_missing_file_exit_code
    File.delete(fx.path("book/pt/ch02.md"))
    res = gen
    assert_exit 2, res
    assert_includes res.err, "missing chapter files (1):"
    assert_includes res.err, "book/pt/ch02.md"
  end

  # Guards the EN edition: English part titles (title_en), title, labels and paths.
  def test_structure_en
    res = gen("en")
    assert_exit 0, res
    book = profile("en")["book"]
    assert_equal "Test Book", book["title"]
    assert_equal "A subtitle", book["subtitle"]
    assert_equal({ "part" => "Part I: Beginning", "chapters" => %w[book/en/ch01.md book/en/ch02.md book/en/interlude1.md] },
                 book["chapters"][1])
    assert_equal "Part II: Middle", book["chapters"][2]["part"]
    assert_equal "Appendix", profile("en").dig("crossref", "appendix-title")
    assert_equal "en-US", profile("en")["lang"]
  end

  # Guards unnumbered-sections (filters/unnumbered-refs.lua): front, interludes
  # and non-appendix back units, titled from the edition's own files.
  def test_unnumbered_sections
    gen
    gen("en")
    pt = profile["unnumbered-sections"]
    en = profile("en")["unnumbered-sections"]
    assert_equal %w[sec-bibliografia sec-creditos sec-epilogo sec-fontes sec-glossario sec-interlude1 sec-prefacio], pt.keys.sort
    refute pt.key?("sec-apA"), "appendices are numbered"
    refute pt.key?("sec-ch01")
    assert_equal({ "title" => "Prefácio", "file" => "index.html" }, pt["sec-prefacio"])
    assert_equal({ "title" => "Preface", "file" => "index.html" }, en["sec-prefacio"])
    assert_equal "Interlude: A Pause", en["sec-interlude1"]["title"]
    assert_equal({ "title" => "Fontes: os artigos originais", "file" => "fontes.html" }, pt["sec-fontes"])
  end

  # Guards the per-language cover: PT uses the shared config, EN overrides every format.
  def test_cover_override_per_language
    gen
    gen("en")
    refute profile["book"].key?("cover-image")
    refute profile.key?("format")
    assert_equal "Capa de Competente o Suficiente, de Fabio Akita.", profile.dig("book", "cover-image-alt")
    en = profile("en")
    assert_equal "Cover of Competent Enough, by Fabio Akita.", en.dig("book", "cover-image-alt")
    assert_equal "assets/cover/cover-en.png", en["book"]["cover-image"]
    assert_equal "assets/cover/cover-en.png", en.dig("format", "epub", "epub-cover-image")
    assert_equal "assets/cover/cover-en.png", en.dig("format", "akita-book-typst", "pdf-cover")
  end

  # Guards the public bibliography: notes keep only the archived copy (localized),
  # never the editorial "cited-by" provenance.
  def test_filtered_bibliography
    gen
    gen("en")
    assert_equal "build/references-pt.yaml", profile["bibliography"]
    pt_text = fx.read("build/references-pt.yaml")
    en_text = fx.read("build/references-en.yaml")
    refute_includes pt_text, "cited-by"
    refute_includes en_text, "cited-by"
    pt = YAML.safe_load(pt_text)["references"].to_h { [_1["id"], _1] }
    en = YAML.safe_load(en_text)["references"].to_h { [_1["id"], _1] }
    assert_equal "Arquivado em: https://web.archive.org/web/2026/example.org/doe", pt["doe2026"]["note"]
    assert_equal "Archived at: https://web.archive.org/web/2026/example.org/doe", en["doe2026"]["note"]
    refute pt["smith2026ai"].key?("note")
    assert_includes fx.read("book/back/references.yaml"), "cited-by", "the source bibliography is untouched"
  end

  # Guards the colophon/rights metadata being filled from the outline.
  def test_colophon_and_rights
    gen
    assert_equal "© 2026 Autor Teste. Todos os direitos reservados.", profile["rights"]
    assert_equal "Texto refluível com descrições de imagens.", profile["accessibilitySummary"]
    assert_includes profile["colophon"], "Os nomes akitaonrails e Frank são de propriedade de Autor Teste."
    assert_includes profile["colophon"], "ai-jail: GPL-3.0"
  end


  def test_accessibility_summary_is_localized
    gen("pt")
    gen("en")
    assert_equal "Texto refluível com descrições de imagens.", profile("pt")["accessibilitySummary"]
    assert_equal "Reflowable text with image descriptions.", profile("en")["accessibilitySummary"]
  end

  # Guards the revision line on the copyright page: the release tag on CI tag
  # builds, no "+local" in CI, and no ISBN line while meta.isbn is unset.
  def test_revision_and_isbn
    fx.run("gen_quarto", "pt", env: { "CI" => "1", "GITHUB_REF_TYPE" => "tag", "GITHUB_REF_NAME" => "v9.9.9" }) # exit 2: fixture lacks generated pages
    colophon = profile["colophon"]
    assert_match(/Revisão v9\.9\.9 \(\w*\), gerada em \d\d\/\d\d\/\d{4}\. Versões e correções: https:\/\/github\.com\/akitaonrails\/ai-book-2026\/releases/, colophon)
    refute_includes colophon, "+local"
    refute_includes colophon, "ISBN"
  end

  # Guards the per-edition ISBN: meta.isbn {pt: ...} prints only on the PT
  # copyright page, labeled as the hardcover's; the EN edition prints none.
  def test_isbn_per_edition
    fx.edit("book/outline.yml") { _1.sub("meta:\n", "meta:\n  isbn:\n    pt: \"9798162395362\"\n") }
    gen("pt")
    assert_includes profile("pt")["colophon"], "ISBN 9798162395362 (edição em capa dura)"
    gen("en")
    refute_includes profile("en")["colophon"], "ISBN"
  end

  def test_paperback_colophon_has_its_own_isbn_only
    fx.edit("book/outline.yml") do
      _1.sub("meta:\n", "meta:\n  isbn:\n    pt: '9798162465683'\n    en: '9798162395362'\n  isbn_paperback:\n    pt: '9798162938088'\n")
    end
    assert_exit 0, gen("pt")
    hc = profile("pt")["colophon"]
    pb = profile("pt")["colophon-paperback"]
    assert_includes hc, "ISBN 9798162465683 (edição em capa dura)"
    refute_includes hc, "9798162938088"
    assert_includes pb, "ISBN 9798162938088 (edição em brochura)"
    refute_includes pb, "9798162465683"
    assert_equal hc.sub("9798162465683 (edição em capa dura)", "9798162938088 (edição em brochura)"), pb
    assert_exit 0, gen("en")
    refute profile("en").key?("colophon-paperback")
    assert_includes profile("en")["colophon"], "9798162395362"
  end
end
