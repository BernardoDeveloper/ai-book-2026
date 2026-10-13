# Book toolchain research (EPUB 3, print PDF, Kindle, web, DOCX)

Researched 2026-10-13. Versions were checked against GitHub releases, official docs, the Arch repos (`pacman -Si`) and the AUR RPC on that date. Claims marked **[tested]** were reproduced in a throwaway sample book built in the session scratchpad (Quarto 1.10.19, Pandoc 3.12.1, Typst 0.15.1, EPUBCheck 5.4.0). Nothing was installed system-wide.

---

## 1. Recommendation

| Layer | Choice | Pinned version |
|---|---|---|
| Source | Pandoc Markdown (`.md`) in `book/pt/` and `book/en/`, one file per chapter, converted from the Hugo posts | n/a |
| Orchestrator | **Quarto book project**, with one profile per language | 1.10.19 (official tarball under `tools/`) |
| Converter | Pandoc, bundled inside Quarto | 3.10.0 (bundled) |
| PDF engine | **Typst**, bundled inside Quarto, using a custom Typst book template based on Quarto's `orange-book` | 0.15.1 (bundled) |
| Citations | CSL-JSON (exported from Zotero/Better BibTeX) + citeproc (`citeproc: true` for every format), ABNT CSL for PT and Chicago/APA for EN | n/a |
| Glossary | Project Lua filter (prototype in §5) + per-language `glossary-*.yml` | n/a |
| Validation | EPUBCheck jar, DAISY Ace for accessibility, Kindle Previewer (Windows/macOS) or the KDP online previewer | 5.4.0 / 1.4.6 |
| Build | `Rakefile` (the repo already uses Ruby scripts) or a Makefile | n/a |
| Fallback | Plain Pandoc 3.12.1 + pandoc-crossref 0.3.26 + the same Lua filters + Make | AUR `pandoc-bin`, `pandoc-crossref-bin` |

Why this stack:

- **One source tree, every format.** Quarto book projects render HTML, PDF, EPUB, DOCX and Typst from the same chapter list ([Quarto book output](https://quarto.org/docs/books/book-output.html)). **[tested]** A single `quarto render` produced HTML, EPUB, Typst PDF and DOCX from one config.
- **Cross-references come built in.** Plain Pandoc does not number figures or resolve `@fig-x`. That needs pandoc-crossref. **[tested]** Plain Pandoc 3.12.1 left `@fig-diagrama` unresolved, and EPUBCheck then reported 3 × `RSC-012 Fragment identifier is not defined`. Quarto resolved figure and section refs, with localized "Figura 1.1" labels.
- **Pinned and self-contained.** One Quarto tarball pins Pandoc, Typst, Dart Sass and Deno together. `quarto check` reports Pandoc 3.10.0, Typst 0.15.1, Dart Sass 1.101.0 and Deno 2.7.14 for 1.10.19 **[tested]**, which matches the [1.10 changelog](https://github.com/quarto-dev/quarto-cli/blob/main/news/changelog-1.10.md) ("Typst updated to 0.15.1", "Pandoc updated to 3.10"). No TeX Live is needed.
- **Typst gives print-quality PDF without LaTeX.** Its PDFs are tagged by default and it can emit PDF/UA-1 (from v0.14.0, [Typst releases](https://github.com/typst/typst/releases)). It hyphenates by `lang` ([Typst text docs](https://typst.app/docs/reference/text/text/)), and ligatures are on by default (same page). **[tested]** With `lang: pt-BR`, Typst hyphenated "inconstitu-cionalissimamente" correctly in justified text, and `pdfinfo` reported `Tagged: yes`.
- **Bilingual editions are a config concern, not a code fork.** Quarto profiles (`_quarto-pt.yml`, `_quarto-en.yml`, chosen with `--profile`) are merged over `_quarto.yml`. They can set their own `book.chapters` and `output-dir` ([Quarto profiles](https://quarto.org/docs/projects/profiles.html)).
- **The escape hatch stays cheap.** Quarto is a Pandoc front end, so the content (Pandoc Markdown, CSL-JSON, Lua filters) moves to a plain Pandoc + Make pipeline without rewriting anything if Quarto gets in the way.

---

## 2. Version snapshot (2026-10-13)

| Tool | Latest upstream | Arch package | Maintenance signal | Source |
|---|---|---|---|---|
| Pandoc | 3.12.1 (2026-10-08) | `extra/pandoc-cli` 3.10.2; AUR `pandoc-bin` 3.12.1 | Releases roughly monthly | [releases](https://github.com/jgm/pandoc/releases) |
| pandoc-crossref | 0.3.26 (built with Pandoc 3.12.1) | `extra` 0.3.20; AUR `pandoc-crossref-bin` 0.3.26 | Tracks Pandoc releases | [releases](https://github.com/lierdakil/pandoc-crossref/releases) |
| Quarto | 1.10.19 stable (2026-10-06); 1.11.x pre-releases | AUR `quarto-cli-bin` 1.10.19 | Very active | [releases](https://github.com/quarto-dev/quarto-cli/releases) |
| Typst | 0.15.1 (2026-07-17) | `extra/typst` 0.15.1 | Active; 0.15.0 added multiple bibliographies | [releases](https://github.com/typst/typst/releases) |
| glossarium (Typst pkg) | 0.5.10 (2026-01-09), needs Typst ≥ 0.13 | n/a (Typst Universe) | Active | [Typst Universe](https://typst.app/universe/package/glossarium) |
| EPUBCheck | 5.4.0 (EPUB 3.4 CR rules) | `extra/epubcheck` 5.3.0 | Active (W3C) | [releases](https://github.com/w3c/epubcheck/releases) |
| DAISY Ace | 1.4.6 (2026-04-24) | npm `@daisy/ace` | Active | [npm registry](https://registry.npmjs.org/@daisy/ace) |
| TeX Live | 2026 | `extra/texlive-*` 2026.1, incl. `texlive-langportuguese` | Annual | `pacman -Si` |
| Asciidoctor | 2.0.26 (Arch) | `extra/asciidoctor` | Stable | `pacman -Si` |
| asciidoctor-pdf | 2.3.27 (2026-09) | gem | Active | [releases](https://github.com/asciidoctor/asciidoctor-pdf/releases) |
| asciidoctor-epub3 | 2.3.0 (2025-08-11) | gem | Slow; dropped MOBI/KF8 in 2.1.0 | [releases](https://github.com/asciidoctor/asciidoctor-epub3/releases) |
| mdBook | 0.5.4 | `extra/mdbook` 0.5.4 | Active (0.5 rewrite) | [releases](https://github.com/rust-lang/mdBook/releases) |
| Bookdown | 0.48 (2026-08-28) | needs R (`extra/r` 4.6.1) | Maintained | [CRAN](https://cran.r-project.org/package=bookdown) |
| Jupyter Book | 2.1.7 (MyST engine, myst-cli 1.11) | pip/npm | Active; v2 is a rewrite on MyST | [releases](https://github.com/jupyter-book/jupyter-book/releases) |
| Sphinx | 9.1.0 | pip | Active | [releases](https://github.com/sphinx-doc/sphinx/releases) |
| Calibre | 9.16 (2026-10-09) | `extra/calibre` 9.14.0 | Very active | [what's new](https://calibre-ebook.com/whats-new) |
| WeasyPrint | v70.0 (Sep); PDF/UA and PDF/A work in v66–v70 | `extra/python-weasyprint` 69.0 | Active | [releases](https://github.com/Kozea/WeasyPrint/releases) |
| Paged.js / pagedjs-cli | `latest` 0.4.3; `0.5.0-beta.2` (2025-09-06); no GitHub releases | npm | **Stagnant** stable line | [npm registry](https://registry.npmjs.org/pagedjs-cli), [GitHub releases (empty)](https://github.com/pagedjs/pagedjs/releases) |
| Vivliostyle CLI | 11.3.3 (2026-09-12) | npm | Active | [releases](https://github.com/vivliostyle/vivliostyle-cli/releases) |
| shiroa (Typst books) | 0.3.0 stable; 0.4.0-rc2 | cargo | Young; HTML-first | [releases](https://github.com/Myriad-Dreamin/shiroa/releases) |

---

## 3. Comparison against the requirements

Legend: ✅ native, 🟡 possible with a plugin/filter or extra work, ❌ not realistic.

| Tool | 1 Markdown + bilingual | 2 Bibliography | 3 Glossary/index | 4 Figures, xrefs, SVG | 5 Scriptable/pinnable on Arch | 6 PDF typography / partial rebuild | 7 EPUBCheck-valid EPUB 3 | Verdict |
|---|---|---|---|---|---|---|---|---|
| **Quarto (book) + Typst** | ✅ Pandoc MD; profiles per language | ✅ citeproc (CSL-JSON/BibTeX) | 🟡 Lua filter (§5) | ✅ built-in crossref, captions, `fig-alt` | ✅ single tarball | ✅ Typst: pt hyphenation, ligatures; 🟡 per-chapter HTML render | ✅ after one workaround (§8) | **Recommended** |
| Plain Pandoc + pandoc-crossref + Typst/LaTeX | ✅ | ✅ | 🟡 Lua filter | 🟡 needs pandoc-crossref | ✅ static binaries | ✅ (Typst or LuaLaTeX) | ✅ | Strong fallback |
| Pandoc + LuaLaTeX | ✅ | ✅ (citeproc or biblatex) | ✅ PDF (`glossaries`, `imakeidx`); 🟡 EPUB | ✅ with crossref | 🟡 multi-GB TeX Live | ✅ best-in-class; babel `lang` hyphenation ([Pandoc manual](https://pandoc.org/MANUAL.html)) | n/a (PDF only) | Use only if Typst falls short |
| Typst standalone | ❌ Typst markup, not Markdown | ✅ Hayagriva/CSL; `.bib`/`.yml` only | ✅ glossarium (first-use, back-refs) | ✅ | ✅ | ✅ | ❌ no EPUB; HTML export still behind a feature flag ([Typst HTML docs](https://typst.app/docs/reference/html/)) | PDF engine only |
| Asciidoctor + -epub3/-pdf | ❌ AsciiDoc source | 🟡 asciidoctor-bibtex | 🟡 `[glossary]` sections and index terms (PDF) | ✅ | ✅ gems | 🟡 Prawn typesetting is weaker for pt hyphenation | ✅ | Wrong source format |
| mdBook | ✅ Markdown | ❌ core has none | ❌ | 🟡 | ✅ | ❌ HTML-first; PDF/EPUB only via third-party backends | 🟡 | Web docs, not books |
| Bookdown | ✅ R Markdown | ✅ | 🟡 | ✅ | 🟡 needs R + LaTeX | ✅ via LaTeX | ✅ | Quarto is its successor in practice |
| Jupyter Book 2 / MyST | ✅ MyST Markdown | ✅ | 🟡 MyST glossary directive | ✅ | 🟡 Node/Python | 🟡 PDF via Typst/LaTeX templates | ❓ EPUB not mentioned in v2 releases | Notebook-centric |
| Sphinx | 🟡 MyST-parser | ✅ sphinxcontrib-bibtex | ✅ native `glossary` + index | ✅ | ✅ | ✅ via LaTeX | 🟡 EPUB builder is basic | Tech docs, heavy |
| Calibre `ebook-convert` | ❌ converter only | ❌ | ❌ | ❌ | ✅ CLI | ❌ | 🟡 | QA and side-loading only |
| Paged.js / WeasyPrint / Vivliostyle (CSS print) | 🟡 via Pandoc HTML | via Pandoc | via filter | ✅ CSS | 🟡 Chromium (Paged.js/Vivliostyle) or Python | 🟡 CSS `hyphens:auto` depends on engine | n/a (PDF) | Alternative PDF engine if the team prefers CSS |

Notes:
- Pandoc's `--pdf-engine` accepts `typst`, `weasyprint`, `pagedjs-cli`, `prince`, `lualatex`, `xelatex`, `tectonic` and others ([Pandoc manual](https://pandoc.org/MANUAL.html)). Swapping the PDF engine later does not touch the content.
- Pandoc's `epub` output is EPUB 3; `epub2` is separate ([Pandoc manual](https://pandoc.org/MANUAL.html)).

---

## 4. How each requirement is met

### R1. Markdown source and PT-BR + EN editions

Layout:

```
book/
  pt/  00-prefacio.md 01-....md  glossario.md  referencias.md
  en/  00-preface.md  01-....md  glossary.md   references.md
  shared/images/      # language-neutral figures; localized ones in images/pt, images/en
data/
  refs.json           # one CSL-JSON library for both editions
  glossary-pt.yml  glossary-en.yml
  csl/abnt.csl  csl/chicago-author-date.csl
_quarto.yml           # shared: filters, formats, crossref settings
_quarto-pt.yml        # lang: pt-BR, book.title, book.chapters (book/pt/...), output-dir: build/pt, csl, glossary-file
_quarto-en.yml        # lang: en-US, ... output-dir: build/en
```

- Build with `quarto render --profile pt` and `quarto render --profile en`. Profiles can override `book.chapters` and `output-dir` ([Quarto profiles](https://quarto.org/docs/projects/profiles.html)).
- Keep matching chapter IDs (`{#sec-agents}`) across languages, so `@sec-agents` works in both editions and the drift script can pair files.
- Hugo to Pandoc conversion is a one-time Ruby preprocessing step. Pandoc reads YAML metadata blocks (`---`), but Hugo posts may use TOML (`+++`) front matter and shortcodes (`{{< youtube >}}`, `{{< figure >}}`). Pandoc does not understand either, so strip or convert them when importing posts into `book/`. Do not point the build at the blog tree.

### R2. Bibliography

- One `data/refs.json` (CSL-JSON) shared by both editions. Cite with `[@vaswani2017]`, `@vaswani2017` or `[-@key]`.
- Set `citeproc: true` in the Typst format. By default, Pandoc's Typst writer emits native Typst citations ([Pandoc manual](https://pandoc.org/MANUAL.html), `citations` extension). **[tested]** Typst 0.15.1 then fails with `unknown bibliography format (must be .yaml/.yml or .bib)` on a `.json` library. With citeproc, all formats share the same CSL rendering.
- ABNT style: the `associacao-brasileira-de-normas-tecnicas.csl` file from the [CSL styles repo](https://github.com/citation-style-language/styles). **[tested]** It rendered "(Brown, 2020; Vaswani; Shazeer, 2017)" and an ABNT reference list. Superseded 2026-10-13: the PT edition uses `assets/csl/abnt-akita.csl`, a patched copy that adds what NBR 6023:2018 requires for online documents (see `assets/csl/SOURCES.md`).
- End-of-book bibliography: put a `::: {#refs} :::` div in `referencias.md` ([Quarto book structure](https://quarto.org/docs/books/book-structure.html)).
- Per-chapter bibliographies: use the [pandoc-ext/section-bibliographies](https://github.com/pandoc-ext/section-bibliographies) filter. It runs after `quarto`, and its README says to set `citeproc: false` for Quarto.
- Pandoc 3.12.1 changed citeproc particle handling ("de Gaulle" is now treated as the integral family name; [Pandoc releases](https://github.com/jgm/pandoc/releases)). This only matters if the bundled Pandoc moves past 3.12.

### R3. Glossary, first use and index

See §5 for the full design. In short:
- Terms live in `data/glossary-<lang>.yml` and are marked in text as `[LLM]{.gls}` or `[modelos de linguagem]{.gls key=llm}`.
- A Lua filter turns each mark into a link to `#gls-<key>`. On first use, it expands the term to "Large Language Model (LLM)". It then generates the glossary appendix as a definition list wrapped in `role="doc-glossary"` for EPUB.
- **[tested]** This worked in EPUB (cross-file links `ch003.xhtml#gls-llm`, EPUBCheck clean), multi-page HTML (`glossario.html#gls-llm`), Typst PDF and DOCX.
- Back-of-book index: no Markdown toolchain produces a good index for both EPUB and PDF. If you want an index in the print edition, emit Typst index markers from the same `.gls` spans (or a separate `{.idx}` class) in the Typst branch of the filter. Keep EPUB without a page index; the glossary plus reader search covers that use case. Decide this late.

### R4. Figures

- `![Caption. Crédito: X, licença.](images/x.svg){#fig-x fig-alt="Alt text" width=70%}` gives a numbered, localized caption ("Figura 1.1") and a working `@fig-x` reference in every format **[tested]**.
- Put the credit in the caption text, so it travels to every format. Keep a `credits.yml` if you also want a consolidated image-credits page.
- SVG and PNG both worked in EPUB, PDF and HTML **[tested]**. Kindle's support for SVG inside EPUB is weaker. Check SVG figures in Kindle Previewer, and keep a PNG fallback per figure if needed.
- An EPUB-specific bug needs a 2-line workaround; see Pitfalls.

### R5. Reproducible CLI build on Arch

- Download the Quarto 1.10.19 tarball into `tools/quarto/` from a `rake tools` task with a SHA-256 check. Pandoc and Typst come bundled and versioned with it. Put `epubcheck-5.4.0.jar` in `tools/` too. Java is already available through mise.
- Use no GUI at any step. Kindle Previewer is the exception, and it is optional (see §6).

### R6. Partial rebuilds, typography, cover

- EPUB, PDF and DOCX are single-file outputs and are always rebuilt whole. **[tested]** The small sample rendered all four formats in about 3 s, so full rebuilds stay cheap at book scale. Use `quarto preview` while writing HTML.
- Rake/Make handles incrementality at the edition level: rebuild `build/pt/*` only when `book/pt/**`, `data/*` or the filters change.
- Typography: Typst with `lang: pt-BR` gives Portuguese hyphenation **[tested]**. Standard ligatures are on by default ([Typst text docs](https://typst.app/docs/reference/text/text/)), and widow/orphan costs are tunable through `text.costs`. Pick a good OpenType font (e.g. Libertinus, which Quarto ships by default **[tested]**, or Source Serif 4 / Literata) and embed it in the EPUB with `--epub-embed-font` ([Pandoc manual](https://pandoc.org/MANUAL.html)).
- Cover: `book.cover-image` / `epub-cover-image` sets the EPUB cover (`properties="cover-image"` in the OPF **[tested]**). The Typst PDF did **not** get a cover page automatically **[tested]**. Add it in the custom Typst template for the ebook PDF. For a print edition, the cover is a separate file anyway.

### R7. EPUBCheck

- Run `java -jar tools/epubcheck-5.4.0.jar build/pt/*.epub` in the build and fail on any error. EPUBCheck 5.4.0 validates against EPUB 3.4 CR rules ([EPUBCheck releases](https://github.com/w3c/epubcheck/releases)).
- **[tested]** The Quarto EPUB passed with 0 errors and 0 warnings after the `alt` workaround.

---

## 5. Glossary design (the part no tool does natively)

Native options:
- LaTeX `glossaries` and Typst `glossarium` both do first-use expansion and back-references ([glossarium](https://github.com/typst-community/glossarium)), but they are PDF-only.
- Sphinx has a native `glossary` directive but is the wrong ecosystem.
- Existing Quarto glossary extensions are popup/table-oriented and HTML-centric ([debruine/quarto-glossary](https://github.com/debruine/quarto-glossary), [andrewpbray/glossary](https://github.com/andrewpbray/glossary)). Check their activity before adopting one; this research did not verify it against primary sources.

So own a small filter: about 70 lines of Lua, format-agnostic, one YAML file per language.

Data (`data/glossary-pt.yml`):

```yaml
llm:
  term: LLM
  long: Large Language Model
  def: Modelo de linguagem de grande porte treinado para prever o próximo token.
```

Source: `Um [LLM]{.gls} ...` or `[modelos]{.gls key=llm}`. Glossary chapter: `::: {#glossary} :::`.

Filter outline, a working prototype that was **[tested]** (keep it in `filters/glossary.lua`):

```lua
-- Meta: load YAML named by `glossary-file`; optional `glossary-page` (e.g. glossario.html)
--   is used only for multi-page HTML (FORMAT starts with "html"); EPUB/PDF/DOCX use "#gls-<key>".
-- Span.gls: key = attr `key` or lowercased text; first occurrence -> "Long (TEXT)";
--   return pandoc.Link(content, target, '', {class='gls'}); warn on unknown key (stderr).
-- Div#glossary: sorted DefinitionList; each term wrapped in Span{id='gls-<key>'};
--   for epub/html wrap in Div{role='doc-glossary'} (DPUB-ARIA, accepted by EPUBCheck).
```

Planned extensions, kept deliberately in the filter:
- **Back-references.** Collect the nearest preceding section id per use and append "→ cap. 3, 7" links to each entry.
- **Unused-term lint.** Warn when a YAML entry is never referenced, or a `.gls` key is unknown. This makes `rake check` catch drift between the PT and EN glossaries (compare key sets).
- **Typst branch.** Optionally emit `#gls("llm")` with glossarium for the PDF, to get page-numbered back-references. Note that glossarium expects its own `print-glossary` call, so keep the YAML as the single source.
- **First-use semantics.** In EPUB/PDF/DOCX the whole book is one Pandoc run, so "first use" is book-wide. In multi-page HTML, each chapter is a separate run, so expansion happens on first use per chapter. That is arguably right for the web edition.

---

## 6. Kindle / KDP

- **KDP accepts EPUB, DOCX and KPF for reflowable ebooks. MOBI has been rejected for reflowable books since 2021-08-01 and for fixed-layout since 2025-03-18** ([KDP MOBI FAQ](https://kdp.amazon.com/en_US/help/topic/GULSQMHU5MNH4EZM); [KDP supported formats](https://kdp.amazon.com/en_US/help/topic/G200634390)). Upload the EPUB that passed EPUBCheck. Amazon converts it, and Enhanced Typesetting applies to reflowable EPUB/DOCX/HTML uploads ([search summary of KDP Enhanced Typesetting help](https://kdp.amazon.com/en_US/help/topic/G202087570)).
- KPF is produced by Kindle Create (a GUI) and is preferred when you author in Kindle Create. There is no reason to go through it from a Pandoc pipeline. The KPF that Kindle Previewer emits is for previewing and cannot be side-loaded ([Kindle Previewer help](https://kdp.amazon.com/en_US/help/topic/G202131170)).
- **Kindle Previewer 4 runs only on Windows 10+ and macOS 12+. There is no Linux build** ([Kindle Previewer help](https://kdp.amazon.com/en_US/help/topic/G202131170)), and no AUR package turned up (AUR RPC query on 2026-10-13). On Arch, do the final Kindle check in a Windows/macOS VM or Wine (untested), or use the KDP online previewer after upload. This is a manual pre-release step, not part of `rake build`.
- Asciidoctor-epub3 dropped its KF8/MOBI path in 2.1.0 ([releases](https://github.com/asciidoctor/asciidoctor-epub3/releases)), which confirms the industry move to "just ship EPUB".
- Use Calibre (`ebook-convert book.epub book.azw3`) only to side-load test copies to a personal Kindle. Never use it for the KDP upload.

---

## 7. Accessibility (EPUB Accessibility 1.1 / European Accessibility Act)

- The EAA (Directive 2019/882) has applied since **28 June 2025** and covers e-books. The W3C Group Note maps its e-book requirements to **EPUB Accessibility 1.1** + WCAG ([W3C EPUB a11y–EAA mapping, 2025-08-18](https://www.w3.org/TR/2025/NOTE-epub-a11y-eaa-mapping-20250818/)). Sources disagree on whether the target is WCAG 2.1 or 2.2 AA ([Eden summary](https://about.eden.co.uk/resources/epub3-accessibility-european-accessibility-act-publishers), [Elsevier statement](https://www.elsevier.com/about/accessibility/eaa-statement)). Aim for WCAG 2.2 AA, which also satisfies 2.1.
- EPUB Accessibility 1.1 is a W3C Recommendation (2024-10-17). It requires `schema:accessMode`, `accessibilityFeature` and `accessibilityHazard`, recommends `accessibilitySummary`, and requires `dcterms:conformsTo` ("EPUB Accessibility 1.1 - WCAG 2.x Level AA") to claim conformance. The spec "strongly recommends" the latest WCAG 2 at AA ([EPUB Accessibility 1.1](https://www.w3.org/TR/epub-a11y-11/)).
- What Pandoc/Quarto emit **[tested]**: `accessMode=textual`, `accessModeSufficient=textual`, `accessibilityFeature` = alternativeText / readingOrder / structuralNavigation / tableOfContents, and `accessibilityHazard=none`. These are configurable through the metadata keys `accessModes`, `accessModeSufficient`, `accessibilityHazards` and `accessibilitySummary` ([Pandoc EPUB writer source](https://raw.githubusercontent.com/jgm/pandoc/main/src/Text/Pandoc/Writers/EPUB.hs)). **No `conformsTo` is emitted.** Add it, along with `a11y:certifiedBy` if desired, through `--epub-metadata` / `epub-metadata: epub-meta.xml`. Also set `accessModeSufficient` correctly for a book with informative images: `textual,visual` plus `textual` once every figure has real alt text.
- Required authoring habits: real `fig-alt` on every figure, `lang` set per edition, no heading-level skips, and meaningful link text. The glossary uses `role="doc-glossary"`.
- Check with **DAISY Ace** (`npx @daisy/ace@1.4.6 build/pt/book.epub`), version from the [npm registry](https://registry.npmjs.org/@daisy/ace). Do this alongside EPUBCheck, which validates structure but does not audit accessibility.
- PDF: Typst produces tagged PDFs by default and supports PDF/UA-1 from 0.14 ([Typst releases](https://github.com/typst/typst/releases)). Enable PDF/UA in the template for the downloadable PDF.

---

## 8. Pitfalls (most observed in the test build)

1. **Quarto EPUB puts `alt=` on the figure wrapper `<div>`** when `fig-alt` is used, and EPUBCheck reports `RSC-005 attribute "alt" not allowed here` **[tested, Quarto 1.10.19]**. The fix is a filter that runs after Quarto's own: `filters: [filters/glossary.lua, quarto, filters/strip-div-alt.lua]` with `function Div(d) if d.attributes.alt then d.attributes.alt=nil return d end end`. After that, EPUBCheck reported 0 errors and 0 warnings **[tested]**. Re-test whenever Quarto is bumped.
2. **Typst native citations reject CSL-JSON.** Set `citeproc: true` for the Typst format (§R2) **[tested]**.
3. **`quarto render --to html` wipes the output dir**, which deleted an EPUB built earlier with `--to epub` **[tested]**. Render all formats in one `quarto render --profile pt` call, or give each format its own output dir.
4. **`papersize: a5` under `format: typst` was ignored in the book project** (output stayed A4), and **no cover page was added to the PDF** **[tested]**. Plan on a custom Typst book template, starting from the bundled `orange-book` ([Quarto book output](https://quarto.org/docs/books/book-output.html)), that sets the trim size, cover, running heads and fonts.
5. Section cross-refs in Typst rendered as "a seção Capítulo 1.." (double period plus redundant noun) **[tested]**. Write `@sec-x` without a preceding noun in prose, or customize `crossref` titles per language.
6. **Profiles fail silently.** A typo in `--profile` is "silently ignored with no warning or error" ([Quarto profiles](https://quarto.org/docs/projects/profiles.html)). Have the Rakefile assert that `_quarto-#{lang}.yml` exists.
7. **Plain-Pandoc path:** `@fig-x` needs pandoc-crossref. Without it, Pandoc treats the refs as missing citations, and EPUBCheck flags `RSC-012` **[tested, Pandoc 3.12.1]**. Also, a YAML metadata file must be passed as `--metadata-file`, not as an input file **[tested]**.
8. **Arch repo lag:** `extra/pandoc-cli` is 3.10.2 versus upstream 3.12.1, and `extra/epubcheck` is 5.3.0 versus 5.4.0. Prefer the vendored tarballs/jars in `tools/` to keep CI and the laptop identical.
9. **Calibre on this machine is broken under mise's Python.** `/usr/bin/ebook-convert` uses `#!/usr/bin/env python3`, which resolves to mise Python 3.12, and fails with `SyntaxError: multiple exception types must be parenthesized`. Calibre 9.14 needs the system Python 3.14 **[tested]**. Call it as `PATH=/usr/bin:$PATH ebook-convert ...` in scripts.
10. **Paged.js is effectively frozen.** The stable npm line is 0.4.3, the 0.5 betas date from 2024–2025, and there are no GitHub releases ([npm](https://registry.npmjs.org/pagedjs-cli)). Do not build the PDF pipeline on it. If CSS-based PDF is ever wanted, WeasyPrint (v70, active, PDF/UA and PDF/A work; [releases](https://github.com/Kozea/WeasyPrint/releases)) or Vivliostyle CLI 11.3.3 are the live options.
11. **Typst HTML export is experimental** (`--features html`; [docs](https://typst.app/docs/reference/html/)) and Typst has no EPUB writer. Do not try to make Typst the single source format.
12. **Book parts are ignored in EPUB and Word** ([Quarto book structure](https://quarto.org/docs/books/book-structure.html)). If the book uses `part:` groupings, the EPUB TOC will be flat at chapter level.
13. **Kindle SVG and CSS:** test figures in Kindle Previewer before release. EPUBCheck-valid does not mean Kindle-perfect.

---

## 9. Arch Linux install (no system-wide install needed)

Project-local, pinned (recommended):

```bash
mkdir -p tools && cd tools
# Quarto (bundles Pandoc 3.10.0 + Typst 0.15.1 + Dart Sass + Deno)
curl -LO https://github.com/quarto-dev/quarto-cli/releases/download/v1.10.19/quarto-1.10.19-linux-amd64.tar.gz
tar xzf quarto-1.10.19-linux-amd64.tar.gz          # -> tools/quarto-1.10.19/bin/quarto
# EPUBCheck
curl -LO https://github.com/w3c/epubcheck/releases/download/v5.4.0/epubcheck-5.4.0.zip
unzip -q epubcheck-5.4.0.zip                         # -> tools/epubcheck-5.4.0/epubcheck.jar
# Optional standalone tools for the fallback path / experimentation
curl -LO https://github.com/jgm/pandoc/releases/download/3.12.1/pandoc-3.12.1-linux-amd64.tar.gz
curl -LO https://github.com/typst/typst/releases/download/v0.15.1/typst-x86_64-unknown-linux-musl.tar.xz
# Accessibility checker (no global install)
npx --yes @daisy/ace@1.4.6 --version
```

These exact URLs were used in the test build **[tested]**. Record SHA-256 sums in `tools/SHA256SUMS` and verify them in `rake tools`.

System packages, if preferred:

```bash
sudo pacman -S typst epubcheck jdk-openjdk       # typst 0.15.1, epubcheck 5.3.0 (one minor behind)
yay -S quarto-cli-bin                             # 1.10.19
yay -S pandoc-bin pandoc-crossref-bin             # 3.12.1 / 0.3.26 (fallback path; avoids Haskell dep tree of extra/pandoc-cli)
# Only if LuaLaTeX is ever needed:
sudo pacman -S texlive-basic texlive-latex texlive-latexrecommended texlive-luatex texlive-fontsrecommended texlive-langportuguese
```

Build sketch (Rake):

```ruby
QUARTO = "tools/quarto-1.10.19/bin/quarto"
EPUBCHECK = "java -jar tools/epubcheck-5.4.0/epubcheck.jar"
%w[pt en].each do |lang|
  namespace lang do
    task :build do
      raise "missing profile" unless File.exist?("_quarto-#{lang}.yml")
      sh "#{QUARTO} render --profile #{lang}"          # html + epub + typst pdf + docx in one pass
    end
    task check: :build do
      Dir["build/#{lang}/*.epub"].each { |f| sh "#{EPUBCHECK} --failonwarnings #{f}" }
      sh "npx --yes @daisy/ace@1.4.6 -o build/#{lang}/ace #{Dir["build/#{lang}/*.epub"].first}"
    end
  end
end
task default: %w[pt:check en:check]
```

---

## 10. Why not the others

- **Asciidoctor**: good tooling, but the source would have to move to AsciiDoc, away from the blog's Markdown. asciidoctor-epub3 releases are slow (2.3.0, Aug 2025) ([releases](https://github.com/asciidoctor/asciidoctor-epub3/releases)).
- **mdBook**: HTML-first documentation tool. No citations or glossary in core, and print/EPUB would rely on third-party backends ([releases](https://github.com/rust-lang/mdBook/releases)).
- **Bookdown**: still maintained (0.48, Aug 2026, [CRAN](https://cran.r-project.org/package=bookdown)), but it pulls in R and LaTeX for no benefit over Quarto, which comes from the same lineage.
- **Jupyter Book 2 / Sphinx**: built for executable or technical documentation. Jupyter Book 2 is a rewrite on the MyST engine ([releases](https://github.com/jupyter-book/jupyter-book/releases)), and its release notes don't mention EPUB.
- **Typst standalone / shiroa**: excellent PDF, but no Markdown and no EPUB. shiroa is HTML-first and pre-1.0 ([releases](https://github.com/Myriad-Dreamin/shiroa/releases)).
- **Calibre**: a converter and QA tool, not an authoring pipeline.
- **Paged.js**: stagnant (see Pitfall 10). WeasyPrint and Vivliostyle are viable CSS-print alternatives, but Typst gives better pt-BR typography with less CSS work.

---

## Sources

- Pandoc releases: https://github.com/jgm/pandoc/releases
- Pandoc manual: https://pandoc.org/MANUAL.html
- Pandoc EPUB writer source (accessibility metadata): https://raw.githubusercontent.com/jgm/pandoc/main/src/Text/Pandoc/Writers/EPUB.hs
- pandoc-crossref releases: https://github.com/lierdakil/pandoc-crossref/releases
- section-bibliographies: https://github.com/pandoc-ext/section-bibliographies
- Quarto releases: https://github.com/quarto-dev/quarto-cli/releases
- Quarto 1.10 changelog: https://github.com/quarto-dev/quarto-cli/blob/main/news/changelog-1.10.md
- Quarto book output: https://quarto.org/docs/books/book-output.html
- Quarto book structure: https://quarto.org/docs/books/book-structure.html
- Quarto profiles: https://quarto.org/docs/projects/profiles.html
- Quarto glossary extensions: https://github.com/andrewpbray/glossary, https://github.com/debruine/quarto-glossary
- Typst releases: https://github.com/typst/typst/releases
- Typst text (hyphenation/ligatures/costs): https://typst.app/docs/reference/text/text/
- Typst HTML export: https://typst.app/docs/reference/html/
- glossarium: https://github.com/typst-community/glossarium, https://typst.app/universe/package/glossarium
- EPUBCheck releases: https://github.com/w3c/epubcheck/releases
- DAISY Ace (npm): https://registry.npmjs.org/@daisy/ace
- EPUB Accessibility 1.1: https://www.w3.org/TR/epub-a11y-11/
- EPUB a11y ↔ EAA mapping: https://www.w3.org/TR/2025/NOTE-epub-a11y-eaa-mapping-20250818/
- EAA secondary summaries: https://about.eden.co.uk/resources/epub3-accessibility-european-accessibility-act-publishers, https://www.elsevier.com/about/accessibility/eaa-statement
- KDP formats: https://kdp.amazon.com/en_US/help/topic/G200634390
- KDP MOBI FAQ: https://kdp.amazon.com/en_US/help/topic/GULSQMHU5MNH4EZM
- Kindle Previewer: https://kdp.amazon.com/en_US/help/topic/G202131170
- KDP Enhanced Typesetting: https://kdp.amazon.com/en_US/help/topic/G202087570
- asciidoctor-epub3: https://github.com/asciidoctor/asciidoctor-epub3/releases
- asciidoctor-pdf: https://github.com/asciidoctor/asciidoctor-pdf/releases
- mdBook: https://github.com/rust-lang/mdBook/releases
- Bookdown: https://cran.r-project.org/package=bookdown
- Jupyter Book: https://github.com/jupyter-book/jupyter-book/releases
- Sphinx: https://github.com/sphinx-doc/sphinx/releases
- Calibre: https://calibre-ebook.com/whats-new
- WeasyPrint: https://github.com/Kozea/WeasyPrint/releases
- Paged.js: https://github.com/pagedjs/pagedjs/releases, https://registry.npmjs.org/pagedjs-cli
- Vivliostyle CLI: https://github.com/vivliostyle/vivliostyle-cli/releases
- shiroa: https://github.com/Myriad-Dreamin/shiroa/releases
- CSL styles (ABNT): https://github.com/citation-style-language/styles
- Arch package versions: `pacman -Si` and https://aur.archlinux.org/rpc/v5/info (queried 2026-10-13)
