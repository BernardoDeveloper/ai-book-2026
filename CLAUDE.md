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
5. `rake check`, `rake build`, `rake audit`, look at the affected pages, then
   report to the author what changed and where. Commit only when asked.

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
