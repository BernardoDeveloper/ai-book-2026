# Edit brief: coloring the narrator (PT)

Project root /mnt/data/Projects/ai-book-2026. Approved by the author
2026-10-14: `reviews/akitando/plan.md` (all touches, corrections in A, all
four appendix suggestions in C).

## Read first

- `reviews/akitando/plan.md`: your touches by number.
- `reviews/akitando/profile.md`: who the narrator is (bio confirmed by the
  author; it wins over any date in the transcripts) and the rules of use.
- `reviews/akitando/extract-*.yml`: the verbatim quotes and the hooks behind
  each touch; `reviews/akitando/factcheck.yml`: use only verified world facts,
  with the corrected values.
- `docs/EDITORIAL-RULES.md` and `docs/BOOK-VOICE.md`; ledger
  `book/integration.yml`.
- The Akitando post itself (~/Projects/akitaonrails-hugo/content/<id>/index.md)
  for every quote you use.

## The goal of this round

Make the book's important points stronger with the narrator's history: a
touch earns its place when it backs the chapter's key claim with lived
experience (a warning made years before, a method practiced for decades, a
crash lived from inside). It is not decoration and not a channel recap.

- One to three sentences per touch, in the existing paragraph or a new short
  one; no new sections in chapters.
- Most touches are voice ("vi isso por dentro na bolha de 2000"); cite an
  episode only where a dated warning or a direct quote is the point, as
  "(Akitando #63, 2019)" plus the citation key.
- No bragging, no volume ("mais de 40 repositórios"-style lines); tell the
  wrong calls too ("avisei da bolha, errei o calendário").
- Conclusions only where the episodes support them; nothing beyond what the
  extracts and the posts say. Bio facts only as confirmed in profile.md. No
  client names, nothing private.
- Keep the chapter's flow: read the whole section before inserting; the
  paragraph after your insertion must still follow.

## Provenance and citations

- A paragraph that uses an episode gets `<!-- src: <yyyy/mm/dd/slug> -->`
  (the episode's full id, from `book/outline.yml` background_sources). If
  you add an episode sentence to an existing paragraph from another post,
  put it in its own short paragraph with its own marker instead.
- Add every episode you mark to the unit's front-matter `sources` with its
  pt sha256 from `inventory/posts.yml`.
- Inline citations use the key `akitando<NNN>` (three digits: akitando063).
  Add the entry to `book/pt/_refs/<unit>.yaml` (create the file if missing)
  in the same shape as existing entries: type post-weblog, title (the post
  title), author Akita/Fabio, container-title AkitaOnRails.com, issued
  date-parts, URL https://akitaonrails.com/<yyyy>/<mm>/<dd>/<slug>/.

## Done

`ruby scripts/lint_chapter.rb book/pt/<unit>.md` (0 errors, fix warnings you
introduced). Reply per touch number: what you wrote (the new sentences in
full), where, sources and refs added. No git commands; no book/en edits.
