# CLAUDE.md

Book generator for *Competente o Suficiente*, Fabio Akita's 2026 AI book, built
from his blog posts in `~/Projects/akitaonrails-hugo/content/2026`. PT-BR is
canonical; the EN edition starts only after the author approves the PT
edition. Read `docs/DESIGN.md` first (layout, provenance model, pipeline).

## The core duty: keep the book in sync with the blog

The author edits blog posts after publication and expects the book to follow.
Whenever asked to update the book, or at the start of any work session:

1. `rake drift` (or `ruby scripts/inventory.rb && ruby scripts/drift.rb --diff`)
   lists stale chapters/analyses and shows each post's diff since the commit
   the book last reviewed it at.
2. For each stale chapter, find the paragraphs marked
   `<!-- src: 2026/MM/DD/slug -->` for that post and decide: does the change
   touch anything the book says? Edit only those paragraphs (voice rules in
   `docs/BOOK-VOICE.md`; fact rules in `docs/INTEGRATION.md`), or record that
   the change doesn't affect the book.
3. `ruby scripts/restamp.rb <post-id>` records the new hash and commit.
4. New posts: `drift` reports them as NEW; write an analysis
   (`docs/analysis-schema.yml`), then place them in `book/outline.yml` or add
   them to `excluded` with a reason. Check `inventory/lineage.yml`: a new post
   may supersede what a chapter says.
5. `rake check`, `rake build` (includes the page audit and doctor), read
   `build/<lang>/seams.md` for the hand-offs, look at the affected pages, then
   report to the author what changed and where. Commit only when asked.

## Structural changes

Before removing, moving or replacing source material, follow
`docs/CHANGE-PLAYBOOK.md`: encode the decision in the outline, map the impact
(`scripts/impact.rb`), edit in parallel on disjoint files, verify with
`rake check build` and the doctor, then propagate to the EN edition.

## Two editions

PT-BR (`book/pt/`) is canonical; EN (`book/en/`) is a translation of each PT
unit (contract: `docs/TRANSLATING.md`). Each EN unit records
`translated_from: {file, sha256}` of its PT unit and tracks the author's
English posts (`index.en.md`) in `sources`. After any PT change:

1. `ruby scripts/drift.rb --lang en` lists EN units whose PT source changed
   (and EN posts that changed).
2. Re-translate only the changed paragraphs (same `src` markers), update
   `translated_from.sha256`, `ruby scripts/restamp.rb --lang en <post>` for
   EN-post changes.
3. Figures with text have per-language files: `rake charts BOOK_LANG=en`
   writes `assets/figures/en/`; the EN cover is
   `scripts/compose_cover.rb assets/cover/cover-d.png assets/cover/cover-en.png --lang en`.
4. `rake check build BOOK_LANG=en`.

PT changes land first and need the author's approval before EN follows.

## Rules

- Voice: `docs/BOOK-VOICE.md` (inherits the blog's WRITER.md, humanizer and
  akita-finish rules). Drafting contract: `docs/DRAFTING.md`.
- `book/outline.yml` is the source of truth for structure; `_quarto-*.yml`
  is generated (`scripts/gen_quarto.rb`).
- Never present superseded content as current (`inventory/lineage.yml`).
- Never name private repositories, hostnames or IPs in book text; the
  author's girlfriend is never named.
- Every image has a record in `assets/credits/`; AI images are disclosed.
- Layout must look professionally typeset: run `rake audit` and inspect the
  pages you touched after every build.
- Ledger of cross-chapter decisions and open author questions:
  `book/integration.yml`.

## Public repository

This repo is public (github.com/akitaonrails/ai-book-2026). Private
reference sources (the author's home-server notes, desktop config, newsletter
code) are cited in provenance markers only through aliases
(`ref:private-notes/...`, mapped in the gitignored `private/aliases.yml`);
research about them lives in `private/`. `scripts/public_guard.rb` runs as
the git pre-push hook and blocks any tracked file or commit message matching
`private/forbidden.txt`. Never put private repo names, hosts, IPs or the
author's email in tracked files or commit messages.

Releases: add a section to CHANGELOG.md, then push a `vX.Y.Z` tag; the
`book` workflow builds, validates and publishes the GitHub Release.
