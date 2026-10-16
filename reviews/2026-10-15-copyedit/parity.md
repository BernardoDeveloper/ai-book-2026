# PT/EN copyedit and content parity, 15 October 2026

Both editions received a complete paired reading for prose, grammar, continuity and meaning. The review covered all 38 active authored units and all 146 glossary definitions, including lists, tables, quotations, code examples, figure captions, alternative text and long descriptions. The four generated back-matter pages were also compared. PT remains canonical. Accepted corrections to shared defects were applied to both editions; the author's informal first-person register was preserved.

After the corrections, the paired reading found no remaining substantive content omission or contradiction between the editions in the reviewed material. Matching structure alone did not establish this result: several missing qualifiers and examples occurred inside otherwise matching paragraphs.

## Coverage and findings

The per-language `part*.yml` files record the original exact quotes and proposed corrections. Quotes and schemas were validated before application. The language-specific triage files record decisions and expected surviving quote anchors; use `review.rb status` after application, rather than expecting historical quotes to remain in the edited manuscript.

| Paired reading | Complete units | PT findings | EN findings |
|---|---|---:|---:|
| Front matter and Part I | index (preface), como-ler, antes, ch01–ch04 | 8 | 20 |
| Part II and interludes | ch05–ch10, interlude1, interlude2 | 11 | 23 |
| Part III | ch11, ch12, ch13, ch13b, ch14 | 12 | 18 |
| Part IV | ch15–ch17 | 9 | 19 |
| Part V | ch18–ch20 | 12 | 16 |
| Back matter | epilogo, posfacio, apfeito, apmecanica, apleituras, apestudar, apbolhas, apA, apB, apmemoria, apC, aptecnico | 24 | 31 |
| Glossary | Every term, expansion and definition | 3 | 9 |
| Generated pages | Sources and image credits, plus glossary/reference generation | 0 | 2 |
| **Total** | **38 authored pairs, four generated pairs and 146 glossary pairs** | **79** | **138** |

Shared defects appear in both language reports. These totals are edition-specific findings, not distinct underlying errors. EN 5.15 was intentionally left unchanged: its paragraph split preserves the complete PT meaning. All other findings were accepted, with the scoped refinements recorded in triage.

## Restored parity and continuity

- Restore omitted English qualifiers, quantities and examples: primary-source weighting, hallucination conditions, ten summaries, the up-to-sixteen-hour pace, manga examples, Portuguese reading availability, the 2019 research date and the three-hour memory example.
- Retain Brazilian references such as CPF, correct literal translations such as database, life sentence and outsourced-services provider, and restore the canonical novel-capacity example. Remove unsupported EN-only currency conversion and translation-process assurance.
- Keep callbacks consistent: nine elapsed days, newsletter launch versus later development tally, initial drafting versus subsequent chapter additions, March versus April GPU allocation, 146 dubbed episodes as a subset of 149 total, and May Bun work versus the July report.
- Correct shared reasoning and terminology: contaminated benchmark baseline, limits of negative identity tests, GPU-electricity estimate versus total cost, profit versus revenue, the DMCA partial retraction, keylogging versus input injection, static typing, GCC as output oracle, and the assumptions behind the Bayes example.
- Preserve the limits of evidence, agent persistence and backup access. Scope claims about training costs, VRAM, reinforcement learning, oracle feedback and user responsibility to the book's own examples. Record coordinated decisions in `book/integration.yml`.
- Preserve the context clause in the generated source-page introduction and the full 1960 Navy photograph attribution in English. The credit generator now accepts a localized bespoke attribution alongside its existing computed fallback.

English retains four extra paragraph breaks in ch13, ch14, ch16 and ch20. Every sentence and source marker in those passages has its counterpart. Decimal separators, written-out thousands, clock formats and permitted cultural explanations were compared for meaning. Two EN-only glossary links were removed to match the canonical link locations without changing visible content.

## Structural verification

The final comparison checked the ordered key sequences in every paired authored body, normalizing only per-language figure directories and glossary display text:

| Check | Result in each edition |
|---|---:|
| Source markers | 1,532, same order |
| Heading/figure IDs | 112, same order |
| Citation-key occurrences | 491, same order |
| Cross-reference occurrences | 662, same order |
| Figure references | 55, corresponding assets |
| Glossary links | 438, same ordered stable keys |
| Headings | 517, equal counts per unit |
| List items | 485, equal counts per unit |
| Table rows, including headers/separators | 58, equal counts per unit |

All 38 `translated_from.sha256` values match the current PT files. Both glossaries retain the same 146 ordered keys and matching optional expansion fields. Source-post provenance hashes were preserved. The integration ledger and all findings files parse; finding IDs, required fields, categories and severities pass schema checks.

All 38 front-matter source-post ID sequences and reference-project lists also match. The 310 merged bibliography records match after localizing the four archive-note labels. All 55 image-credit keys appear in the same reading order; the cover disclosure and photo attributions were compared directly. Source-page dates and article identities agree, with the inventory's corresponding translated titles and URLs. Edition-specific ISBNs and source snapshot commits retain their existing values.

## Validation scope

The review used the tracked manuscripts, editorial/translation guides, analyses, continuity ledger and targeted public primary sources cited in the findings. The author's local blog and reference-project checkouts were unavailable. The read-only drift check uses the recorded inventory snapshot; it does not establish live blog synchronization. Historical and experimental claims outside the concrete findings did not receive an exhaustive independent fact audit.

## Integrated checks and rendered output

- `rake check` passes for PT and EN: outline coverage and chapter lint have zero errors; chapter lint has zero warnings, and the English quotation-punctuation check passes.
- `scripts/doctor.rb --lang <pt|en> --release --output` passes with zero errors. The existing nonfatal bibliography/source-coverage and heuristic callback warnings remain: 27 PT and 21 EN. Reviewed callbacks retain their intended scope; an introductory mention need not repeat every detail of the later example.
- Both editions build to HTML, print PDF, ebook PDF, EPUB and DOCX with the pinned Quarto 1.10.19. EPUBCheck 5.4.0 reports zero errors/warnings for both EPUBs; the HTML/EPUB accessibility contract and DAISY Ace pass in both languages.
- After the normal per-unit fitting policy, both print/ebook page audits are clean. PT: 518 print pages and 490 ebook pages. EN: 505 print pages and 478 ebook pages. The initial PT run's three short final pages disappear after fitting.
- Rendered and visually inspected 141 PT and 201 EN print pages covering edited passages and unit boundaries, with individual full-page checks of representative corrections, the restored reading notes and generated credits. No clipping, overlapping text or broken figure/list layout was found in that inspection. This does not claim visual inspection of every page or every output format.
- `rake test`: 178 runs, 964 assertions, zero failures/errors, one skip. The skipped existing placeholder-image test needs ImageMagick, which was unavailable. The back-matter suite, including the translated-attribution regression, passes all 10 tests and 72 assertions.
- Final paired structural/hash audit, findings schema checks, glossary-key checks, snapshot translation drift check and `git diff --check` pass. The final style reports were reviewed alongside the original reports; informal register and deliberate callbacks were retained.

Local builds used Ruby 4.0.7 and the native macOS archive of the same pinned Quarto version. An ignored local wrapper bypassed the Linux-only bootstrap and invoked the existing fitting policy with argument-safe paths because the checkout directory contains spaces. No bootstrap, fitting policy or layout source was changed in this contribution. PDF/UA was requested by the existing compiler settings; independent veraPDF conformance validation was unavailable.

The two `part8-generated.yml` findings refer to generated EN pages: run the normal back-matter generation before checking their post-application status. Their canonical fixes live in the generator and image-credit record, rather than in disposable generated Markdown.
