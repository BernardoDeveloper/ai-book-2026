# Changelog

Editions of *Competente o Suficiente*. Each version is a git tag (`vX.Y.Z`);
pushing the tag builds the book and publishes a GitHub Release with the
files.

## 1.0.0-preview.3

First copyedit pass, both languages.

- **Copyedit**: a straight-through reader pass over every unit of both
  editions (preface to glossary), with the findings triaged and applied: typos
  and agreement, one spelling for model names, repeated anecdotes turned into
  callbacks, chapter endings that no longer pre-tell the next opening, jargon
  glossed for lay readers. Reports in `reviews/1.0.0-preview.2/`.
- **Facts checked against the sources**: commit counts now state their scope,
  totals recomputed (the skills post's "mais de mil" is 984), the Frank
  Investigator voting example matches the code (figure redrawn), contributor
  counts for ai-memory say what they count, Stack Overflow's founding year.
- **Chapter 14 sources**: the David Sacks, Pirate Wires, Musk/Altman and
  OpenAI Navier-Stokes claims verified against the originals (podcast, posts,
  archived pages); Sacks's wording corrected and the Pirate Wires context
  completed.
- **Photo**: Sam Altman's portrait in chapter 14 is now from 2025.
- **Copyright page** lists AI Lair among the author's names.
- **English edition**: re-synced with the corrected Portuguese, then its own
  reader pass: calques and Portuguese leftovers rewritten, glossary terms used
  consistently, American quotation punctuation throughout, image credits for
  the chapter 14 composite fixed.
- **Tooling**: copyedit procedure with fact-checking against the sources
  (`docs/COPYEDIT.md`, reader and apply briefs in `reviews/`), EN quotation
  check in `rake check`, composite photo credits in the generator, 127 tests.
- Releases: only the two newest are kept on GitHub.

## 1.0.0-preview.2

Second preview, now in two languages.

- **English edition**: *Competent Enough*, a full translation of the
  Portuguese edition in the author's English voice, using his own English
  wording wherever the book follows his posts. EPUB, ebook PDF and print PDF.
- **Cut-off moved to February 2026**: the January articles are out. Chapter 5
  now opens with FrankMD, chapter 3 explains agents and harnesses with later
  evidence, chapter 13 opens on the March mini-PC; callbacks, timeline and
  project appendices repaired across the book.
- **New appendix**: ai-memory, why agent memory matters and how to start
  (aimemory.sh); ai-jail points to aijail.io.
- **Cover**: the robot now wears Marvin's face (the newsletter's character),
  and an author sticker sits beside the name.
- **Quality tooling**: integrity checker (cross-references, citations,
  glossary, figures, provenance, cut-off, callbacks, translation parity),
  change-impact map, chart layout checker, and a regression test suite
  (122 tests) run in CI before every build.

## 1.0.0-preview

First public edition, in Brazilian Portuguese, built from Fabio Akita's 2026
articles on akitaonrails.com (blog commit b9c0292).

- 20 chapters in five parts, two interludes, preface, "Como ler", "Antes de
  começar" (what the book doesn't explain, with a reading list), epilogue and
  afterword.
- Appendices: the machine inside without math, timeline, minimal kit for
  using agents safely, ai-memory (why agent memory matters, quick start), how to read a benchmark or an announcement, the year's
  projects.
- Glossary of 144 terms, 292 references (ABNT), 50 figures with credits,
  list of the original articles behind each chapter.
- Editions: EPUB 3 (epubcheck clean), ebook PDF with cover, print PDF (6 × 9 in).
