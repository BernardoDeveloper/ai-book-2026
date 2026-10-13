# Translating the book to English (contract for translation agents)

The PT-BR edition (`book/pt/`) is canonical and approved. The English edition
(`book/en/`) is a faithful translation of each PT unit, in the English voice
Akita uses on his blog. You translate the book's text, not the blog posts.

## Read first

1. `~/Projects/akitaonrails-hugo/WRITER.md`, section "Translating posts to
   English" and "Voice for the English version": faithful, never literal,
   New Yorker tone (dry, punchy, NYC idioms only when they land), tech terms in
   English, no "It's not A, it's B" negative parallels, no em dashes.
2. `docs/BOOK-VOICE.md` (the same book rules apply in English: scene-driven,
   paragraphs of at most ~4 sentences, blockquote takeaways, no blog-isms,
   absolute dates, the edge aimed at the propaganda, never at the reader).
3. The PT unit you translate, in full, and the units before and after it.
4. For every source post in the unit's front matter, the author's own English
   version at `~/Projects/akitaonrails-hugo/content/<id>/index.en.md`.
   Wherever the PT chapter quotes or closely follows Akita's words from a post,
   use his English wording from that file (adapted for the book only as much
   as the PT chapter adapted the PT post). His own translations win over yours.

## Write `book/en/<id>.md` (the preface: `book/en/index.md`)

Front matter:

```yaml
---
id: ch05
chapter: "The First Ten Percent"        # English title; title case like the blog's EN titles
sources:                                # same posts as the PT unit, EN hashes: en.sha256 in inventory/posts.yml
  - {post: 2026/01/28/vibe-code-..., sha256: "<en.sha256>"}
refs_projects: [...]                    # copy from the PT unit
blog_commit: "<blog_commit from inventory/posts.yml>"
translated_from: {file: book/pt/ch05.md, sha256: "<sha256 of the PT file as you read it>"}
---
```

Body rules:
- **One-to-one.** Every PT paragraph, list item, blockquote, figure and table
  has its English counterpart, in the same order. Don't add, cut or
  summarise. Where a sentence only makes sense to Brazilians (CREA, gov.br,
  ECA Digital, Pix, a Brazilian TV show), keep it and add the shortest
  clarifying clause an international reader needs; nothing more.
- **Keep markup exactly:** every `<!-- src: ... -->` marker in the same place;
  heading ids (`{#sec-ch05}`, `.unnumbered`); cross-references (`@sec-ch03`,
  `@fig-...`); citation keys (`[@key]`); glossary marks with the same keys.
  Glossary keys are Portuguese slugs, so in English always write the key
  explicitly unless the English text lowercased equals the key:
  `[context window]{.gls key=janela-de-contexto}`, `[LLM]{.gls}`.
- **Figures:** if `assets/figures/en/<fig>.png` exists, point the image at it
  (`assets/figures/en/<fig>.png`); otherwise keep the shared path (photos and
  label-free art). Translate the caption and `fig-alt`. Credit strings:
  "Foto:" → "Photo:", "Imagem:" → "Image:", "domínio público" → "public
  domain", "Ilustração gerada por IA." → "AI-generated illustration."
- **Titles:** "Interlúdio:" → "Interlude:", "Epílogo:" → "Epilogue:",
  "Posfácio:" → "Afterword:", "Prefácio" → "Preface", "Antes de começar" →
  "Before You Start", "Como ler este livro" → "How to Read This Book".
  Part names: see `title_en` in book/outline.yml.
- **Numbers and dates:** English conventions ("October 13, 2026", "1,349",
  "US$ 5.22" → "$5.22"; keep R$ amounts in reais). Rounded prose numbers stay
  rounded.
- **Code, commands, model and product names, quoted English sources:** as in PT
  (they are usually already English; restore the original English of quotes
  the PT chapter translated, from the cited source if you can open it).
- No URLs in prose (citations only), no curly quotes, no em/en dashes.

## Finish

1. Reread against the PT paragraph by paragraph: nothing missing, nothing
   added, numbers and names identical.
2. Humanizer pass (`~/Projects/my-skills/humanizer/SKILL.md`) on your English;
   it must not read as a translation.
3. `BOOK_LANG=en ruby scripts/lint_chapter.rb book/en/<id>.md` at 0 errors.
4. Notes for the editor (anything untranslatable, any PT passage you think is
   wrong): `book/en/_notes/<id>.yml`.

Report: units done, word counts, any quote where the EN post's wording
differed meaningfully from the PT chapter, open questions.

## Re-sync after the PT edition changes

`ruby scripts/drift.rb --lang en --diff` lists every EN unit whose PT source
changed since it was translated, with a word-level diff of the PT file since
the exact version that was translated (found by its `translated_from.sha256`).
For each stale unit:

1. Apply only the diff: find the corresponding EN paragraphs by their `src`
   markers and position, and re-translate those (added, removed or reworded
   paragraphs, changed markers, sources, figures). Leave untouched paragraphs
   alone; don't re-polish them.
2. Make the EN front matter match: `sources` (same posts as the PT unit, EN
   hashes), and `translated_from.sha256` set to the current PT file's sha256.
3. `BOOK_LANG=en ruby scripts/lint_chapter.rb <file>` and
   `ruby scripts/doctor.rb --lang en` (parity: same src-marker sequence as PT).
