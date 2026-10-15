# Accessibility research and implementation plan

**Status:** research and artifact audit, 2026-10-15

**Scope:** PT-BR and EN EPUB, HTML, PDF, DOCX, and print outputs

**Recommended target:** EPUB Accessibility 1.2 and WCAG 2.2 Level AA

## Conclusion

The book is already in a better position than most small-publisher titles. It
is a reflowable EPUB, not a fixed-layout or image-only book; both editions have
real headings, lists, Unicode text, declared document languages, navigable
tables of contents, glossary semantics, and descriptions for every content
figure. The generated PDFs are tagged, identify their language and title, and
declare PDF/UA-1. The figure pipeline already checks grayscale legibility and
forbids colour as the only signal.

The largest gap is not a wholesale redesign. It is turning accessibility from
good incidental output into an explicit, tested release contract. The current
release gate runs EPUBCheck, which tests EPUB structure, but not DAISY Ace,
manual WCAG checks, screen-reader behaviour, or the accuracy of the
accessibility metadata. The current EPUBs should therefore **not yet claim
formal conformance**.

The practical recommendation is:

1. Make the final EPUB the primary accessible edition.
2. Add automated accessibility gates and honest, localized accessibility
   metadata now.
3. Split the existing long image descriptions into concise alt text plus
   extended descriptions.
4. Perform a manual audit and a small paid test with disabled readers before
   making a conformance claim.
5. Keep tagged PDF as a useful secondary format; do not present the print PDF
   as the preferred accessible edition.

This is a tractable project. Most high-value work is pipeline and metadata
work. The only large editorial task is revisiting the 55 figures in each
language.

## What “accessible” means for this book

No single format serves every disability. The goal is to preserve the same
information and navigation while letting readers choose how it is presented.

| Reader need | Best support in this project | What matters |
|---|---|---|
| Blindness | Reflowable EPUB with screen reader or Braille display | Semantic structure, correct reading order, short alternatives plus full descriptions, language metadata |
| Low vision and colour-vision differences | EPUB/HTML with user-controlled size, font, spacing, colours, and contrast | Relative sizing, reflow, no information conveyed by colour alone, sharp scalable figures |
| Dyslexia and other print disabilities | EPUB in a reader such as Thorium | User-selectable font and themes, generous line spacing, short sections, descriptive headings, text-to-speech |
| Cognitive and learning disabilities | All editions | Predictable hierarchy, plain explanations, glossary, summaries, consistent terminology, alternatives to dense diagrams and tables |
| Motor disabilities | EPUB/HTML | Complete keyboard navigation, logical focus order, links with useful names, no pointer-only interaction |
| Deafness or hearing loss | No current special requirement | The book contains no audio or video. Any future media needs captions/transcripts; meaningful silent video also needs a text or audio description. |
| Photosensitive disabilities | Already low risk | The book has no animation, flashing, or autoplay. Keep it that way unless an accessible control and hazard review are added. |

The EPUB is especially important in Brazil. Article 68 of the Lei Brasileira
de Inclusão defines accessible formats as digital files usable by screen
readers and other assistive technologies, allowing synthesized speech,
enlargement, different contrast, and Braille printing. A well-structured EPUB
does all of these more naturally than a fixed PDF.

## Standards and legal context

### Technical target

- [EPUB Accessibility 1.2](https://www.w3.org/TR/epub-a11y-12/) is the current
  W3C Recommendation (12 September 2026). It applies WCAG to EPUB and adds
  EPUB-specific discoverability, navigation, and conformance requirements.
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) is the current W3C Recommendation.
  Target Level AA. Conformance to 2.2 also conforms to WCAG 2.1 and 2.0.
- [EPUB Accessibility Techniques 1.2](https://www.w3.org/TR/epub-a11y-tech-12/)
  explains EPUB-specific techniques such as landmarks, page navigation,
  document titles, language, and extended image descriptions.
- [PDF/UA-1](https://typst.app/docs/guides/accessibility/) is the practical PDF
  target supported by the pinned Typst toolchain. PDF/UA-2 is newer, but Typst
  does not support it yet.

The repository's earlier toolchain research targets EPUB Accessibility 1.1.
That was correct when written but is now stale; all new work should target 1.2.

### Distribution context, not legal advice

- Brazil's [Lei 13.146/2015, art. 68](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm)
  establishes accessible book formats and requires them in public book
  procurement.
- The [European Accessibility Act](https://eur-lex.europa.eu/eli/dir/2019/882)
  covers e-books and e-commerce services provided to EU consumers after 28
  June 2025. The directive exempts microenterprises providing services, but
  national implementation and the role of publisher/distributor still need
  legal interpretation. Accessibility remains worthwhile even if an exemption
  applies.
- [KDP's current accessibility guidance](https://kdp.amazon.com/en_US/help/topic/GBPE3QVZ2J3HLQ4B)
  asks publishers to declare accessibility features during title setup and
  recommends semantic headings, lists and tables, adequate contrast, and alt
  text of no more than 140 characters.

Do not turn these standards into a marketing badge without completing the
manual evaluation. `dcterms:conformsTo` is a claim about the complete book, not
an indication that an automated checker passed.

## Audit of the current artifacts

The audit used the built PT and EN artifacts present on 2026-10-15. Results can
change with the next build.

### EPUB

Strong foundations:

- Both editions are EPUB 3, reflowable, and correctly declare `pt-BR` or
  `en-US`.
- DAISY Ace 1.4.6 reported 46 passing automated assertions in each edition.
- Package metadata already declares `accessMode=textual`,
  `accessModeSufficient=textual`, `accessibilityHazard=none`, and the features
  `alternativeText`, `readingOrder`, `structuralNavigation`, and
  `tableOfContents`.
- All 55 content images in each edition have non-empty descriptions. Ace also
  sees the cover, for 56 images total.
- The EPUB includes a navigation document and a linear reading order.
- EPUB CSS uses relative sizes, 1.5 line spacing, left-aligned body text,
  scalable images, and no forced background colour. This allows reading-system
  customization.

Gaps found:

1. **Ace fails one moderate check in both languages:** no
   `schema:accessibilitySummary`.
2. **The descriptions are too long to function well as alt text.** All 55
   content-image `alt` values exceed Amazon's recommended 140 characters; the
   longest is 722 characters in PT and 680 in EN. Detailed descriptions are
   valuable, but W3C advises concise alt text and a separate extended
   description for complex images.
3. **No page navigation.** The package has no page-break markers or page-list.
   EPUB Accessibility 1.2 says publications produced alongside a static print
   edition should include page navigation when the workflow can retain the
   mapping. This is a `SHOULD`, not a blocker for the first accessibility pass.
4. **Landmarks are incomplete.** The landmark navigation contains only the
   title page and cover. It should at least identify start of body matter,
   table of contents, glossary, and bibliography.
5. **The four tables have real `<th>` header cells, but no captions or explicit
   `scope`.** Simple tables can still be understood from `<thead>`, but captions
   and explicit header relationships are more robust and are recommended by
   KDP.
6. **Conformance has not been manually evaluated.** Ace cannot judge whether
   alt text is accurate, reading order is sensible, headings are meaningful,
   links make sense out of context, or language changes are correctly marked.

### HTML

- Representative PT and EN pages (preface, an image-heavy chapter, and the
  timeline/table appendix) produced no automated WCAG 2 AA findings with
  Pa11y 9.0.1 using axe.
- All 55 content images per edition have accessible names.
- The cover image on each preface page has a `title` but no `alt` attribute.
  Some checkers accept the title as an accessible name, but `alt` is the
  interoperable mechanism and should be added.
- A complete 84-page automated run is not yet part of the build. Keyboard,
  200%/400% zoom, high-contrast, reflow, and screen-reader checks remain
  manual.

### PDF

- The four current PDFs (print and ebook, PT and EN) report `Tagged: yes`.
- XMP includes title, author, language, and `pdfuaid:part=1`; they therefore
  declare PDF/UA-1.
- Typst 0.15.1 compiled them with its strict `ua-1` target, which checks for
  missing titles, invalid heading structure, missing image alternatives, and
  other machine-detectable problems.
- Text extraction from the opening pages follows a plausible reading order.

This is strong evidence, but not independent certification. A conformance flag
does not prove the tags are semantically correct. The final PDFs still need a
run through the free Windows-only [PAC checker](https://pac.pdf-accessibility.org/en/download)
and manual review of reading order, figures, links, tables, and headings. The
[PDF Association](https://pdfa.org/resource/tagged-pdf-q-a/) explicitly notes
that automated and human checks are both necessary.

The print typography is a normal trade-book size (10.5 pt body), not a
large-print edition. That is not a defect when an accessible EPUB is offered,
but the print/PDF should not be described as suitable for every low-vision
reader.

### DOCX

DOCX is currently an editor artifact, not the recommended reader edition. It
was not audited. If it is distributed to readers, it needs Microsoft Word's
Accessibility Checker plus manual verification of heading styles, image
descriptions, table headers, link text, language, and reading order.

## Recommended changes

### Priority 0 — define an honest contract

Add `docs/ACCESSIBILITY.md` as the maintained policy/checklist (this research
file is the evidence and plan). State:

- Target: EPUB Accessibility 1.2 / WCAG 2.2 AA.
- Primary accessible artifact: reflowable EPUB.
- Known limitations and which formats were tested.
- A public way to report an accessibility problem.
- No formal conformance claim until automated **and manual** checks pass.

Add localized `accessibilitySummary` metadata now. It should say what is true,
including limitations. An initial summary could be:

> This reflowable publication includes a structured table of contents,
> headings, reading order, and text alternatives for all images. It contains
> no audio, video, animation, or flashing content. Complex-image descriptions
> have not yet been independently reviewed by disabled readers, and print-page
> navigation is not included.

Translate this naturally for PT-BR. Do not add `dcterms:conformsTo` yet.

### Priority 1 — make accessibility a release gate

Add a `rake a11y` task and call it from `release_check` **after all EPUB
post-processing**. It should:

1. Run EPUBCheck for structural validity.
2. Run a pinned DAISY Ace version on the final PT and EN EPUBs and fail on
   violations. Store its HTML and JSON reports under `build/<lang>/a11y/`.
3. Run axe or Pa11y over all generated HTML pages, not only samples.
4. Run project-specific semantic checks that generic tools cannot express:
   - every meaningful image has `fig-alt`;
   - concise alt is within the KDP limit;
   - complex figures have a long description;
   - decorative images use empty alt and are marked as artifacts where needed;
   - tables have captions and header cells;
   - package and content languages match the edition;
   - accessibility metadata uses only truthful features;
   - EPUB landmarks contain body matter, glossary, and bibliography;
   - final EPUB still passes after `epub_clean.rb` rewrites it.
5. Verify PDF metadata (`Tagged`, language, title, and PDF/UA identifier) on
   Linux. Keep PAC and screen-reader review as a documented release checklist
   because they cannot be reliably automated here.

Ace and axe are necessary but insufficient. DAISY's validation guidance says a
machine can detect that alt text exists, but only a person can decide whether
it conveys the image. Use [Ace SMART](https://kb.daisy.org/publishing/docs/epub/validation/smart.html)
or an equivalent checklist for the manual portion.

### Priority 2 — redesign figure descriptions once, in source

The existing descriptions contain the right raw material. Preserve it, but
split the authoring contract into:

- `fig-alt`: one short sentence giving the figure type and its main point,
  ideally no more than 140 characters;
- `fig-desc`: the full structured description, including labels, relationships,
  and data that are not already available in nearby prose;
- caption: visible identification/context, not a duplicate of either field.

The output filter should map these by format:

- **EPUB/HTML:** concise `alt`, followed by an accessible “Detailed image
  description” / “Descrição detalhada da imagem” disclosure or link in the
  same chapter;
- **PDF:** a properly tagged figure with a meaningful alternative; keep the
  extended description available in the tag structure or adjacent accessible
  content without forcing several paragraphs into the printed layout;
- **DOCX:** alt plus a nearby long description that survives Word export.

W3C's [image guidance](https://www.w3.org/WAI/tutorials/images/tips/) recommends
the most concise useful alt and a long-description method when more than a
short sentence is required. Do not discard detail merely to satisfy Amazon's
length recommendation.

Add PT/EN parity checks for both fields. The current descriptions already exist
in both languages, so this is editing and classification rather than writing
110 descriptions from nothing.

### Priority 3 — strengthen semantics and navigation

- Add `alt` to the web cover. In EPUB/PDF, “Book cover: title, subtitle, and
  author” is enough unless the cover art conveys information used by the text.
- Add captions to the four tables and explicit column/row header associations
  where the generated format supports them. Supply a prose summary for any
  table whose point is difficult to reconstruct cell by cell.
- Expand EPUB landmarks to cover, title page, TOC, body matter, glossary, image
  credits, and bibliography.
- Review heading levels across part/chapter boundaries. Ace currently finds no
  automated outline error, but EPUB 1.2 treats the book as one hierarchy across
  content files.
- Mark genuine foreign-language passages with Pandoc language spans. Do not
  mark product names, proper names, established loanwords, or ordinary
  technical terms mechanically; WCAG explicitly exempts many of these.
- Check link text from a screen reader's “links list.” Replace unexplained
  repeated “here/click here” links if any appear.
- Keep the current glossary expansion and DPUB-ARIA glossary role; they are
  useful to screen-reader users and readers with cognitive disabilities.

### Priority 4 — manual compatibility and user testing

Before a formal accessibility claim, test the final EPUB in at least:

- Thorium with keyboard only, text-to-speech, high contrast, large text, and a
  user-selected font;
- NVDA on Windows or Orca on Linux for heading, link, list, table, figure, and
  landmark navigation;
- VoiceOver on Apple Books if an Apple device is available;
- Kindle Previewer/device for the KDP rendition, because Amazon conversion can
  change markup.

Perform concrete tasks: start reading, jump to chapter and section headings,
find the glossary, follow and return from a glossary link, interpret one table,
understand the five most complex figures, and change font/size/colours without
losing content.

Pay at least two or three readers with different needs rather than asking for
free review: for example, an experienced screen-reader/Braille user, a
low-vision reader, and a reader with dyslexia or another cognitive/learning
disability. A small study will find real usability problems, but must not be
treated as proof for every disability. W3C recommends combining disabled-user
evaluation with standards review, not substituting one for the other.

### Priority 5 — optional formats and enhancements

These are valuable but should follow the core EPUB work:

- **Print page list in EPUB:** useful when readers cite pages or use print and
  digital copies together. It is technically difficult because Typst and EPUB
  paginate independently. Implement only after the basic audit, using stable
  markers derived from the final print PDF rather than hand-maintained page
  numbers.
- **Large-print edition:** a separate 16–18 pt layout with larger trim and
  reflowed tables/figures. Moderate editorial/layout cost and a much larger
  page count. Offer it only if there is reader demand; the EPUB already gives
  stronger magnification and reflow.
- **Audiobook:** high production and QA cost, especially in two languages.
  Synthetic read-aloud from accessible EPUB is available immediately; a
  narrated audiobook is a separate product, not a prerequisite for EPUB
  accessibility.
- **Synchronized EPUB media overlays:** useful for simultaneous text/audio but
  substantially more complex than a normal audiobook. Defer.
- **Braille or DAISY derivatives:** do not hand-author them first. A semantic,
  tested EPUB is the best master for an accessibility organization or library
  service to convert.
- **Libras version:** a complete signed-language translation would be a major
  separate edition. It is not a reasonable first adaptation for a text-only
  trade book.

## Effort and value

| Work | Expected effort | Accessibility value | Recommendation |
|---|---:|---:|---|
| Accessibility policy, localized summary, KDP disclosure | 0.5–1 day | High | Do now |
| Ace + full HTML audit + metadata/semantic lints in release gate | 1–2 days | Very high | Do now |
| Web cover alt, EPUB landmarks, table captions/headers | 1–2 days | Medium–high | Do now |
| Split/review 55 figure descriptions in PT, propagate to EN | 3–6 focused days | Very high | Do before conformance claim |
| Manual SMART, screen-reader, keyboard, zoom/reflow test | 1–2 days per release candidate | Very high | Required before claim |
| Paid disabled-reader review | Scheduling plus 1–3 test sessions | Very high | Required before calling the experience good |
| PAC audit of four PDFs | 0.5–1 day on Windows, plus remediation | Medium | Do before distributing PDFs as accessible |
| EPUB print-page navigation | Several days; technically fragile | Medium | Defer |
| Large-print edition | Several days plus recurring layout QA | Medium for a narrower audience | Demand-driven |
| Human audiobook, two languages | Weeks | High for some readers | Separate project |

## Proposed release acceptance checklist

Automated on every build:

- [ ] EPUBCheck: zero errors and warnings.
- [ ] Ace: zero violations on the final post-processed EPUB.
- [ ] Axe/Pa11y: zero agreed WCAG A/AA violations on all HTML pages.
- [ ] Every informative image has concise alt and, when complex, a long
      description; every decorative image has null alt.
- [ ] Tables have captions and correct headers.
- [ ] Heading hierarchy, languages, metadata, landmarks, and reading order pass
      project lints.
- [ ] PDFs are tagged and contain correct title, language, and PDF/UA metadata.

Manual for a release candidate:

- [ ] Ace SMART/WCAG 2.2 AA checklist completed and archived.
- [ ] Keyboard-only navigation and 200%/400% zoom/reflow tested.
- [ ] Screen-reader tasks completed on at least one desktop stack.
- [ ] Thorium and Kindle rendition tested with large text and custom colours.
- [ ] Five most complex figures and all four tables reviewed non-visually.
- [ ] PAC checks pass for PDFs that will be advertised as accessible.
- [ ] Accessibility summary and KDP declarations match what was actually
      tested.
- [ ] Formal `dcterms:conformsTo` is added only after all applicable checks
      pass and the evaluator is identified.

## Sources consulted

Primary and specialist sources used for this plan:

- W3C, [EPUB Accessibility 1.2](https://www.w3.org/TR/epub-a11y-12/)
- W3C, [EPUB Accessibility Techniques 1.2](https://www.w3.org/TR/epub-a11y-tech-12/)
- W3C, [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- W3C WAI, [Images tutorial](https://www.w3.org/WAI/tutorials/images/)
  and [alt-text tips](https://www.w3.org/WAI/tutorials/images/tips/)
- W3C WAI, [Language of Parts](https://www.w3.org/WAI/WCAG22/Understanding/language-of-parts)
- W3C WAI, [Involving users in accessibility evaluation](https://www.w3.org/WAI/test-evaluate/involving-users/)
- DAISY, [Ace](https://kb.daisy.org/publishing/docs/epub/validation/ace.html),
  [SMART](https://kb.daisy.org/publishing/docs/epub/validation/smart.html), and
  [validation process](https://kb.daisy.org/publishing/docs/epub/validation/overview.html)
- Amazon KDP, [Accessibility for eBooks](https://kdp.amazon.com/en_US/help/topic/GBPE3QVZ2J3HLQ4B)
- Typst, [Accessibility Guide](https://typst.app/docs/guides/accessibility/)
- PDF Association, [Tagged PDF Q&A](https://pdfa.org/resource/tagged-pdf-q-a/)
  and [Matterhorn Protocol](https://taggedpdfschool.pdfa.org/matterhorn)
- PAC, [PDF Accessibility Checker](https://pac.pdf-accessibility.org/en/download)
- Brasil, [Lei 13.146/2015](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm)
- European Union, [Directive 2019/882](https://eur-lex.europa.eu/eli/dir/2019/882)
