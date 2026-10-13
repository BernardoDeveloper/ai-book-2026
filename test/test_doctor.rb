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
  def test_output_reads_render_log
    fx.write("build/pt/render.log", <<~LOG)
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
    assert_includes res.out, "warn  render: no build/pt/render.log"
  end
end
