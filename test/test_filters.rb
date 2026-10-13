# frozen_string_literal: true

require_relative "test_helper"

# filters/*.lua, run through the Pandoc bundled with the pinned Quarto
# (tools/quarto-*/bin/tools/*/pandoc; `rake tools` installs it). Skipped when
# the toolchain isn't unpacked.
class TestFilters < ToolTest
  PANDOC = Dir[File.join(FixtureData::REPO_ROOT, "tools", "quarto-*", "bin", "tools", "*", "pandoc")].first

  def setup
    skip "Pandoc not found under tools/quarto-*/bin/tools/*/pandoc (run `rake tools`)" unless PANDOC
    super
  end

  # Runs Pandoc on `input` with one filter; returns [stdout, stderr].
  def pandoc(filter, input, to: "markdown", args: [])
    out, err, status = Open3.capture3(PANDOC, "-f", "markdown", "-t", to, "-L", fx.path("filters/#{filter}.lua"), *args,
                                      stdin_data: input)
    assert status.success?, "pandoc failed: #{err}"
    [out, err]
  end

  # Guards provenance markers and editor comments never reaching readers,
  # while Quarto's own file-metadata comments survive (part pages need them).
  def test_strip_provenance
    out, = pandoc("strip-provenance", <<~MD, to: "html")
      <!-- src: 2026/02/10/primeiro-post -->
      Texto com <!-- nota do editor --> comentário.

      <!-- quarto-file-metadata: eyJyZXNvdXJjZURpciI6Ii4ifQ== -->
    MD
    refute_includes out, "src:"
    refute_includes out, "nota do editor"
    assert_includes out, "Texto com"
    assert_includes out, "quarto-file-metadata"
  end

  def glossary_file
    fx.write("gls.yml", <<~YAML)
      # header comment
      gpu:
        term: GPU
        long: Graphics Processing Unit
        def: A placa de vídeo.
      zebra:
        term: Zebra
        def: Um animal.
      codigo:
        term: Código
        def: Texto de programa.
      arvore:
        term: Árvore
        def: Uma planta.
      beta:
        term: beta
        def: Uma letra.
    YAML
    fx.path("gls.yml")
  end

  # Guards acronym expansion: "Long (SHORT)" only on the first use of the
  # acronym itself; a descriptive span with key= neither expands nor counts as the first use.
  def test_glossary_expands_acronym_once
    out, = pandoc("glossary", "[placas de vídeo]{.gls key=gpu}, depois [GPU]{.gls} e de novo [GPU]{.gls}.\n",
                  to: "plain", args: ["-M", "glossary-file=#{glossary_file}"])
    assert_includes out, "placas de vídeo, depois Graphics Processing Unit (GPU) e de novo GPU."
    assert_equal 1, out.scan("Graphics Processing Unit").size
    refute_includes out, "Graphics Processing Unit (placas"
  end

  # Guards glossary links and unknown keys being reported on stderr (the
  # doctor's --output check greps the render log for this exact message).
  def test_glossary_links_and_unknown_key
    out, err = pandoc("glossary", "[GPU]{.gls} e [nada]{.gls}.\n", to: "html", args: ["-M", "glossary-file=#{glossary_file}"])
    assert_includes out, %(href="#gls-gpu")
    assert_includes err, "[glossary] unknown key: nada"
  end

  # Guards dictionary order in the generated glossary: case- and accent-insensitive.
  def test_glossary_sorts_accented_terms
    out, = pandoc("glossary", "::: {#glossary}\n:::\n", to: "plain", args: ["-M", "glossary-file=#{glossary_file}"])
    order = %w[Árvore beta Código GPU Zebra].map { out.index(_1) }
    assert order.all?, "every term listed: #{out}"
    assert_equal order.sort, order, "expected Árvore, beta, Código, GPU, Zebra in:\n#{out}"
    assert_includes out, "GPU (Graphics Processing Unit)"
  end

  def unnumbered_meta
    fx.write("meta.yml", <<~YAML)
      unnumbered-sections:
        sec-prefacio: {title: "Prefácio", file: index.html}
    YAML
    ["--metadata-file", fx.path("meta.yml")]
  end

  # Guards @sec-x of an unnumbered unit becoming a link titled with the unit's
  # name (Typst can't number it), while numbered units stay cross-references.
  def test_unnumbered_refs
    out, = pandoc("unnumbered-refs", "Veja @sec-prefacio e @sec-ch01.\n", args: unnumbered_meta)
    assert_includes out, "[Prefácio](#sec-prefacio)"
    assert_includes out, "@sec-ch01"
  end

  # Guards multi-page HTML needing the target page in the link.
  def test_unnumbered_refs_html_points_at_page
    out, = pandoc("unnumbered-refs", "Veja @sec-prefacio.\n", to: "html", args: unnumbered_meta)
    assert_includes out, %(href="index.html#sec-prefacio")
  end

  # Guards image paths: merged formats arrive prefixed with the chapter dir
  # (strip it); multi-page HTML lives under book/<lang>/ (climb up).
  def test_project_paths
    input = "![a](book/pt/assets/figures/x.png)\n\n![b](assets/figures/y.png)\n"
    md, = pandoc("project-paths", input)
    assert_includes md, "(assets/figures/x.png)"
    assert_includes md, "(assets/figures/y.png)"
    refute_includes md, "book/pt/"
    html, = pandoc("project-paths", input, to: "html")
    assert_includes html, %(src="assets/figures/x.png")
    assert_includes html, %(src="../../assets/figures/y.png")
  end

  # Guards the EPUB XHTML workaround: alt= on a div is dropped.
  def test_strip_div_alt
    out, = pandoc("strip-div-alt", "::: {#fig-x alt=\"texto\"}\nconteúdo\n:::\n", to: "html")
    refute_includes out, "alt="
    assert_includes out, %(id="fig-x")
  end
end
