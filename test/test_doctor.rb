# frozen_string_literal: true

require_relative "test_helper"

# scripts/doctor.rb: book-wide integrity (ids, citations, glossary, figures,
# provenance, cut-off, exclusions, callbacks, translation parity, render log).
class TestDoctor < ToolTest
  def doctor(*args) = fx.run("doctor", *args)

  # Appends a paragraph to a unit (before nothing else: at the end of the file).
  def append(id, text, lang: "pt")
    fx.edit(fx.unit_rel(id, lang)) { "#{_1}\n#{text}\n" }
  end

  def add_source(id, post, lang: "pt")
    fx.edit(fx.unit_rel(id, lang)) { _1.sub("sources:\n", %(sources:\n  - {post: #{post}, sha256: "#{'0' * 64}"}\n)) }
  end

  # Guards the baseline: the fixture resolves every id, citation, glossary key
  # and figure, so any error in the tests below comes from the change made.
  def test_clean_fixture_resolves_everything
    %w[pt en].each do |lang|
      res = doctor("--lang", lang)
      assert_exit 0, res
      assert_includes res.out, "doctor (#{lang}): 7 units, 0 error(s)"
    end
  end

  # Guards @sec-/@fig- resolution (the February cut-off broke callbacks nobody touched).
  def test_unresolved_sec_and_fig
    append("ch01", "<!-- src: original -->\nVeja @sec-sumiu e a @fig-sumiu, e @sec-como-ler-anuncio.")
    res = doctor
    assert_exit 1, res
    assert_includes res.out, "ERROR ch01: @sec-sumiu doesn't resolve"
    assert_includes res.out, "ERROR ch01: @fig-sumiu doesn't resolve"
    refute_includes res.out, "como-ler-anuncio doesn't resolve"
  end

  # Guards ids defined in headings, figures and generated back matter all counting.
  def test_generated_back_matter_ids_resolve
    append("ch01", "<!-- src: original -->\nO glossário (@sec-glossario) e as fontes (@sec-fontes) e @fig-ch02-diagrama.")
    assert_exit 0, doctor
  end

  # Guards citation keys being checked against the merged bibliography.
  def test_unknown_citation
    append("ch02", "<!-- src: original -->\nSegundo [@ninguem2026], sim.")
    res = doctor
    assert_exit 1, res
    assert_includes res.out, "ERROR citations: @ninguem2026 not in book/back/references.yaml"
  end

  # Guards uncited bibliography entries being reported (PT only, as a warning).
  def test_uncited_entry_warning
    fx.edit("book/pt/ch02.md") { _1.sub(" [@doe2026]", "") }
    fx.edit("book/pt/ch03.md") { _1.sub(" [@doe2026]", "") }
    res = doctor
    assert_exit 0, res
    assert_includes res.out, "warn  citations: doe2026 is in the bibliography but no unit cites it"
  end

  # Guards unknown glossary keys (by text and by key=).
  def test_unknown_glossary_key
    append("ch01", "<!-- src: original -->\nUm [Foo]{.gls} e [bar]{.gls key=baz}.")
    res = doctor
    assert_exit 1, res
    assert_includes res.out, "ERROR glossary: key foo used but not defined"
    assert_includes res.out, "ERROR glossary: key baz used but not defined"
  end

  # Guards image checks: a missing file is an error, and so is a missing credits record.
  def test_missing_image_and_credit
    append("ch01", "<!-- src: original -->\n![Nada.](assets/figures/nada.png){#fig-nada}")
    res = doctor
    assert_exit 1, res
    assert_includes res.out, "ERROR ch01: image assets/figures/nada.png missing"
    assert_includes res.out, "ERROR ch01: image assets/figures/nada.png has no assets/credits record"
  end

  # Guards the credits requirement on its own: the file exists but nobody recorded where it came from.
  def test_image_without_credit_record
    fx.write("assets/figures/sem-credito.png", Fixture::PNG)
    append("ch01", "<!-- src: original -->\n![X.](assets/figures/sem-credito.png){#fig-sem-credito}")
    res = doctor
    assert_exit 1, res
    assert_includes res.out, "sem-credito.png has no assets/credits record"
    refute_includes res.out, "sem-credito.png missing"
  end

  # Guards translated figures (assets/figures/<lang>/x.png) sharing the canonical credits record.
  def test_translated_figure_uses_canonical_credit
    res = doctor("--lang", "en")
    refute_includes res.out, "figures/en/ch01-arte.png has no assets/credits record"
  end

  # Guards placeholders: a warning while drafting, an error in --release.
  def test_placeholder_warning_vs_release_error
    fx.write("assets/figures/.placeholders", "ch02-diagrama.png\n")
    res = doctor
    assert_exit 0, res
    assert_includes res.out, "warn  ch02: image assets/figures/ch02-diagrama.png is still a placeholder"
    res = doctor("--release")
    assert_exit 1, res
    assert_includes res.out, "ERROR ch02: image assets/figures/ch02-diagrama.png is still a placeholder"
  end

  # Guards provenance: a paragraph marked with a post the unit doesn't list in `sources`.
  def test_marker_not_in_sources
    append("ch01", "<!-- src: 2026/03/05/segundo-post -->\nO agente esquece.")
    res = doctor
    assert_exit 1, res
    assert_includes res.out, "ERROR ch01: src marker 2026/03/05/segundo-post not listed in front-matter sources"
  end

  # Guards the reverse direction: a listed source no paragraph uses is only a warning.
  def test_listed_source_without_marker_warns
    add_source("ch01", "2026/03/05/segundo-post")
    res = doctor
    assert_exit 0, res
    assert_includes res.out, "warn  ch01: source 2026/03/05/segundo-post listed but no paragraph is marked with it"
  end

  # Guards the cut-off (outline meta.source_from): no source may predate it.
  def test_cutoff_violation
    add_source("ch01", "2026/01/20/outro-de-janeiro")
    append("ch01", "<!-- src: 2026/01/20/outro-de-janeiro -->\nAlgo de janeiro.")
    res = doctor
    assert_exit 1, res
    assert_includes res.out, "ERROR ch01: 2026/01/20/outro-de-janeiro predates the cut-off 2026-02-01"
  end

  # Guards outline `excluded`: a unit may only use an excluded post if listed in borrowed_by.
  def test_excluded_post_and_borrowed_by
    base = doctor
    refute_match(/ch03: .*post-excluido is in outline `excluded`/, base.out, "ch03 is in borrowed_by")

    add_source("ch02", "2026/04/20/post-excluido")
    append("ch02", "<!-- src: 2026/04/20/post-excluido -->\nA memória de vídeo limita.")
    res = doctor
    assert_exit 1, res
    assert_includes res.out, "ERROR ch02: 2026/04/20/post-excluido is in outline `excluded`"
    refute_includes res.out, "ERROR ch03:"
  end

  # Guards the callback heuristic: a sentence pointing at @sec-x that names
  # something absent from x warns (removed material); one naming something present doesn't.
  def test_callback_names_absent_thing_warns
    append("ch02", "<!-- src: original -->\nComo vimos em @sec-ch01, o Zeppelin caiu.")
    res = doctor
    assert_exit 0, res
    assert_match(/warn  ch02: callback to @sec-ch01 names Zeppelin, none found there/, res.out)
    refute_match(/callback .* names Perceptron/, res.out, "Perceptron is in ch01")
  end

  # Guards quoted phrases and numbers as callback names.
  def test_callback_quotes_and_numbers
    append("ch02", %(<!-- src: original -->\nEm @sec-ch01 falei de "uma frase inventada" e de 37 revisores.))
    res = doctor
    assert_match(/callback to @sec-ch01 names uma frase inventada, 37/, res.out)
    fx.edit("book/pt/ch02.md") { _1.sub("37 revisores", "1958 revisores").sub(%("uma frase inventada"), "algo") }
    refute_match(/callback to @sec-ch01/, doctor.out, "1958 occurs in ch01")
  end

  # Guards false positives: sentence-initial words, bold labels and Roman
  # numerals are capitalised by grammar, not because they name something.
  def test_callback_ignores_initial_words_bold_labels_and_roman_numerals
    append("ch02", <<~MD)
      <!-- src: original -->
      Zeppelin aparece em @sec-ch01.

      **Março.** Zeppelin voltou em @sec-ch01.

      Na Parte III e na parte VII, como em @sec-ch01, nada muda.
    MD
    res = doctor
    refute_match(/callback/, res.out)
  end

  # Guards the stem rule: "DeepSeek-V3" / "GPT-4o" in a callback count as found
  # when "DeepSeek" / "GPT" is in the target unit (the version is rarely repeated).
  def test_callback_versioned_name_matches_by_stem
    append("ch02", "<!-- src: original -->\nComo vimos em @sec-ch01, o DeepSeek-V3 saiu barato, e o GPT-4o também.")
    res = doctor
    assert_match(/callback to @sec-ch01 names DeepSeek-V3, GPT-4o/, res.out)
    append("ch01", "<!-- src: original -->\nO DeepSeek e o GPT apareceram.")
    refute_match(/callback/, doctor.out)
  end

  # Guards callbacks into the unit itself and into unknown units being ignored.
  def test_callback_self_reference_ignored
    append("ch02", "<!-- src: original -->\nAqui em @sec-ch02 falo do Zeppelin.")
    refute_match(/callback/, doctor.out)
  end

  # Guards EN parity: a different src-marker sequence than the PT unit is an error.
  def test_en_marker_sequence_mismatch
    append("ch01", "<!-- src: original -->\nAn extra paragraph.", lang: "en")
    res = doctor("--lang", "en")
    assert_exit 1, res
    assert_includes res.out, "ERROR ch01: src markers differ from PT (4 vs 3)"
  end

  # Guards EN parity: a stale translated_from is a warning, an error with --release.
  def test_stale_translation_warning_vs_release_error
    append("ch02", "<!-- src: original -->\nUm parágrafo novo no PT.")
    res = doctor("--lang", "en")
    assert_exit 1, res, "the new PT marker also breaks the marker sequence"
    fx.edit("book/pt/ch02.md") { _1.sub("<!-- src: original -->\nUm parágrafo novo no PT.", "") }
    fx.edit("book/pt/ch02.md") { _1.sub("prometia demais.", "prometia demais, e muito.") }
    res = doctor("--lang", "en")
    assert_exit 0, res
    assert_includes res.out, "warn  ch02: PT unit changed since translation"
    res = doctor("--lang", "en", "--release")
    assert_exit 1, res
    assert_includes res.out, "ERROR ch02: PT unit changed since translation"
  end

  # Guards EN units without translated_from being flagged.
  def test_en_without_translated_from
    fx.edit("book/en/ch03.md") { _1.sub(/^translated_from: .*\n/, "") }
    res = doctor("--lang", "en")
    assert_exit 1, res
    assert_includes res.out, "ERROR ch03: no translated_from in front matter"
  end

  # Guards a unit listed in the outline but missing in the edition.
  def test_missing_unit_file
    File.delete(fx.path("book/en/apA.md"))
    res = doctor("--lang", "en")
    assert_exit 1, res
    assert_includes res.out, "ERROR outline: unit apA has no file book/en/"
  end

  # Guards build/<lang>/seams.md: each hand-off in reading order, last paragraph then first.
  def test_seams_written
    doctor
    seams = fx.read("build/pt/seams.md")
    assert_includes seams, "## prefacio → ch01"
    assert_includes seams, "## ch02 → interlude1"
    assert_includes seams, "## interlude1 → ch03"
    assert_includes seams, "## epilogo → apA"
    assert_match(/## ch01 → ch02\n\n> …A memória fica para @sec-ch02\.\n\n> O agente esquece tudo/, seams)
  end

  # Guards the --output checks reading Quarto's render log (Quarto only warns).
  # The log lives in build/logs/, outside the output dir that Quarto wipes.
  def test_output_reads_render_log
    fx.write("build/logs/render-pt.log", <<~LOG)
      \e[33mWARNING (/x/filters/quarto.lua:1) Unable to resolve crossref @sec-sumiu\e[0m
      [glossary] unknown key: chave-x
      Citation not found: fantasma2026
      Output created: build/pt/book.pdf
    LOG
    res = doctor("--output")
    assert_exit 1, res
    assert_includes res.out, "ERROR render: unresolved cross-reference sec-sumiu"
    assert_includes res.out, "ERROR render: unknown glossary key chave-x"
    assert_includes res.out, "ERROR render: missing citation fantasma2026"
  end

  # Guards --output without a render log: a warning, not a crash.
  def test_output_without_render_log
    res = doctor("--output")
    assert_exit 0, res
    assert_includes res.out, "warn  render: no build/logs/render-pt.log"
  end
  # Guards the PDF "??" check: a post title like "Bend Over for AI??" in the
  # Fontes page is text, while a standalone "??" is an unresolved reference.
  # Needs the bundled Typst to make a real PDF; skipped without the toolchain.
  def test_output_pdf_unresolved_reference_pattern
    typst = Dir[File.join(FixtureData::REPO_ROOT, "tools", "quarto-*", "bin", "tools", "*", "typst")].first
    skip "bundled typst not found (run rake tools)" unless typst
    skip "pdftotext not found" unless system("command -v pdftotext >/dev/null 2>&1")

    fx.write("build/logs/render-pt.log", "Output created: book.pdf\n")
    FileUtils.mkdir_p(File.join(fx.root, "build", "pt"))
    src = File.join(fx.root, "build", "t.typ")
    File.write(src, "RANT: Did Akita Bend Over for AI?? A real question. Projetos, TESTES e Estimativa??? | Rated-R.\n")
    assert system(typst, "compile", src, File.join(fx.root, "build", "pt", "book.pdf"), out: File::NULL, err: File::NULL)
    res = doctor("--output")
    refute_match(/unresolved reference/, res.out, "a title ending in ?? must not count")

    File.write(src, "See section ?? for details.\n")
    assert system(typst, "compile", src, File.join(fx.root, "build", "pt", "book.pdf"), out: File::NULL, err: File::NULL)
    res = doctor("--output")
    assert_exit 1, res
    assert_match(/1× '\?\?' \(unresolved reference\)/, res.out)
  end

  def timeline(lang, body)
    fx.edit(fx.unit_rel("apA", lang)) { "#{_1}\n#{body}\n" }
    doctor("--lang", lang)
  end

  # Guards the apA timeline order: dated entries out of day order in a month warn (PT and EN).
  def test_timeline_out_of_order_warns
    res = timeline("pt", "### Abril\n\n<!-- src: original -->\n**7 de abril.** A.\n\n**6 a 9 de abril.** B.\n\n**1º de abril.** C.\n")
    assert_exit 0, res
    assert_includes res.out, %(warn  apA: Abril: "1º de abril" is out of order after "6 a 9 de abril")
    assert_includes res.out, 'apA: Abril: "6 a 9 de abril" is out of order after "7 de abril"'
    res = timeline("en", "### April\n\n<!-- src: original -->\n**April 7.** A.\n\n**April 6 to 9.** B.\n")
    assert_includes res.out, %(warn  apA: April: "April 6 to 9" is out of order after "April 7")
  end

  # Guards loose labels as day ranges: "Fim de"/"Late" (21-31) before an early
  # date warns; before the 30th, or repeated after it, does not.
  def test_timeline_loose_labels_are_ranges
    res = timeline("pt", "### Maio\n\n<!-- src: original -->\n**Fim de maio.** A.\n\n**10 de maio.** B.\n")
    assert_includes res.out, %(warn  apA: Maio: "10 de maio" is out of order after "Fim de maio")
    res = timeline("en", "### May\n\n<!-- src: original -->\n**Late May.** A.\n\n**May 3.** B.\n")
    assert_includes res.out, %(warn  apA: May: "May 3" is out of order after "Late May")
    # timeline() appends to the same apA, so check only the new section's entries
    res = timeline("pt", "### Junho\n\n<!-- src: original -->\n**Fim de junho.** A.\n\n**30 de junho.** B.\n\n**Fim de junho.** C.\n")
    refute_match(/Junho: .* out of order/, res.out)
  end

  # Guards no false positives on a well-ordered timeline (undated entries, equal days, new month sections).
  def test_timeline_ordered_is_quiet
    body = "### Junho\n\n<!-- src: original -->\n**Começo de junho.** A.\n\n**3 de junho.** B.\n\n**Junho.** C.\n\n**3 de junho.** D.\n\n**Fim de junho.** E.\n\n### Julho\n\n**2 de julho.** F.\n"
    refute_match(/apA: \w+: /, timeline("pt", body).out)
    en = "### June\n\n<!-- src: original -->\n**Early June.** A.\n\n**June 3.** B.\n\n**June.** C.\n\n**Late June.** E.\n\n### July\n\n**July 2.** F.\n"
    refute_match(/apA: \w+: /, timeline("en", en).out)
  end

  def registry(figures) = fx.write("book/continuity.yml", { "canonical_figures" => figures }.to_yaml)

  SPEEDUP = { "speedup" => [{ "value" => "umas cinco vezes", "scope" => "x" }, { "value" => "seis a sete vezes", "scope" => "y" }] }.freeze

  # Guards R6: a speed-up the author states about his own work (first person)
  # that is not in the registry warns (warning only); registered values, other
  # scopes ("duas vezes"), thousands separators and someone else's claim
  # ("prometia ... 193 vezes") stay quiet.
  def test_canonical_figures_speedup
    registry(SPEEDUP)
    append("ch01", "<!-- src: original -->\nEu fiquei dez vezes mais rápido. Outra vez eu fiquei 5x mais rápido, não, mas cinco vezes mais rápido sim. Rodei duas vezes. Eu fiquei 8.100 vezes mais rápido que nada. A empresa prometia um modelo 193 vezes mais rápido.")
    res = doctor
    assert_exit 0, res
    assert_includes res.out, %(warn  ch01: figure 'speedup': states "dez vezes mais rápid")
    assert_equal 2, res.out.scan("figure 'speedup'").size, res.out
    refute_includes res.out, %(states "cinco vezes)
  end

  # Guards R6 for repositories and hours: only plausible counts are checked
  # (10+ repositories, 300-900 hours); registered numbers pass.
  def test_canonical_figures_repositories_and_hours
    registry("repositories" => [{ "value" => "24" }, { "value" => "mais de 30" }], "hours" => [{ "value" => "mais de 500 horas" }])
    append("ch01", "<!-- src: original -->\nEu mantenho 24 repositórios, ou 35 repositórios, ou seis repositórios. Foram 500 horas, ou 620 horas, ou 40 horas. A ordem derrubou 8.100 repositórios.")
    out = doctor.out
    assert_includes out, %(states "35 repositórios")
    assert_includes out, %(states "620 horas")
    assert_equal 2, out.scan("figure '").size, out
  end

  # Guards R8: a chapter whose first paragraph carries inline code or three
  # glossary marks warns; two marks (a scene that names known terms), or a later
  # paragraph, do not; non-chapters are exempt.
  def test_opening_jargon
    fx.edit(fx.unit_rel("ch02")) { _1.sub("O agente esquece tudo", "O agente `reasoning_content` esquece tudo") }
    res = doctor
    assert_exit 0, res
    assert_includes res.out, "warn  ch02: opening paragraph uses jargon before orienting the reader (R8): 1 code span(s)"
    refute_includes res.out, "warn  ch01: opening", "two glossary marks are fine"
    refute_match(/warn  (prefacio|ch03|interlude1): opening/, res.out)
    fx.edit(fx.unit_rel("ch01")) { _1.sub("Os [modelos grandes]{.gls key=llm}", "Os [modelos grandes]{.gls key=llm} e o [token]{.gls}") }
    assert_includes doctor.out, "warn  ch01: opening paragraph uses jargon", "three marks warn"
  end

  # Guards background sources: exempt from the cut-off; an unlisted old post stays an error.
  def test_background_source_allowed_but_unlisted_post_is_error
    post = "2019/10/09/episodio-antigo"
    fx.edit(fx.unit_rel("ch01")) { _1.sub("sources:\n", %(sources:\n  - {post: #{post}, sha256: "#{Fixture.sha(fx.post_path(post))}"}\n)) }
    append("ch01", "<!-- src: #{post} -->\nEu terceirizava decisões demais.")
    res = doctor
    refute_match(/ch01: #{post}/, res.out)
    assert_exit 0, res

    fx.edit("book/outline.yml") { _1.sub(/^background_sources:\n.*\n/, "background_sources: []\n") }
    res = doctor
    assert_exit 1, res
    assert_includes res.out, "ERROR ch01: #{post} predates the cut-off 2026-02-01"
    assert_includes res.out, "ERROR ch01: #{post} is neither in the corpus nor in outline `background_sources`"
  end
end
