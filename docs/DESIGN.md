# Design: the 2026 AI book generator

## Goal

Turn Akita's 2026 AI posts (akitaonrails-hugo) into a narrative book for lay
readers, PT-BR first, EN later, with every paragraph traceable to its source so
that a later blog edit can be propagated to exactly the affected text.

## Layout

```
docs/
  DESIGN.md            this file
  BOOK-VOICE.md        blog voice → book voice rules (narrative, conversions)
  analysis-schema.yml  schema for per-post analyses
  research/            TOOLCHAIN.md, IMAGES.md, FURTHER-READING.md, LINKCHECK.md
private/               (gitignored) research on private reference projects, alias map for private provenance markers, public-guard patterns
inventory/             (machine-generated or machine-checked; never hand-prose)
  posts.yml            scripts/inventory.rb: every 2026 post, PT/EN sha256, links, blog commit
  links.yml            scripts/links.rb: all cited URLs, deduped, with citing posts
  analysis/*.yml       one structured analysis per post (agent-written, hash-stamped)
  lineage.yml          which post supersedes which; corrections from reference projects
book/
  outline.yml          SOURCE OF TRUTH for structure: parts, chapters, briefs, sources, exclusions
  pt/                  PT-BR chapter sources (Quarto markdown), one file per outline id
  en/                  EN edition, later, same ids
  back/references.yaml CSL-YAML bibliography shared by both editions
  back/glossary.yml    terms with PT/EN definitions and first-use chapter
assets/
  diagrams/            D2 sources + per-language label files → SVG/PNG
  illustrations/       generated concept art (label-free) + overlay specs
  photos/              fetched photos
  credits.yml          one record per image: source, license, prompt/model, attribution, KDP disclosure
scripts/               Ruby: inventory, links, analyses check, outline_check, drift, lint_chapter, build helpers
tools/                 pinned Quarto (bundles Pandoc + Typst), epubcheck, d2 (gitignored binaries, versions in tools/VERSIONS)
```

## Provenance model (three layers)

1. **Post level.** `inventory/posts.yml` holds the sha256 of each PT and EN
   post and the blog git commit. Analyses and chapters record the hash they
   were made from.
2. **Chapter level.** Chapter front matter lists `sources: [{post, sha256}]`,
   reference-project files used, and `blog_commit`.
3. **Paragraph level.** `<!-- src: 2026/MM/DD/slug -->` before each block
   derived from a post; `<!-- src: original -->` for new text;
   `<!-- src: ref:<project>/<path> -->` for reference-project facts. A Lua
   filter strips them at build.

**Background sources.** Older posts (Akitando, 2018-2023) may color the
narrator's history. They sit outside the 2026 corpus and before
`meta.source_from`, so they are listed in `book/outline.yml` under
`background_sources: [{post: yyyy/mm/dd/slug, why}]` (full id, with the year).
`inventory.rb` records them like any post, flagged `background: true`; units
cite them with the usual `src` markers and `sources` entries, so drift,
`--diff` and `restamp.rb` work unchanged. They need no analysis, are not
counted as used AI posts, are exempt from the cut-off check, and `fontes`
lists the cited ones in a group of their own. A marker pointing at a post that
is neither in the corpus nor in `background_sources` is a doctor error.

Images carry their own provenance in `assets/credits.yml`; bibliography
entries record `note: cited-by <post ids>`.

## Pipeline

| Stage | Tool | Parallel? | Output |
|---|---|---|---|
| 0. Inventory | `rake inventory` (inventory.rb, links.rb) | n/a | posts.yml, links.yml |
| 1. Analyse posts | agents, schema-bound | yes, by batch | analysis/*.yml |
| 2. Lineage + outline | human-approved | no | lineage.yml, outline.yml |
| 3. Draft chapters | one agent per chapter, brief from outline + analyses + posts + lineage | yes, by chapter | book/pt/chNN.md |
| 4. Citations | per-chapter agent turns cited URLs into CSL entries | yes | references.yaml (merged, deduped) |
| 5. Glossary | collect `[x]{.gls}` marks, draft definitions | yes | glossary.yml |
| 6. Fact-check | `fact-check` checker prompt on new/changed claims, reference projects for local facts | yes | corrections applied |
| 7. Humanizer + akita-finish | per chapter | yes | final prose |
| 8. Lint | `rake lint` (lint_chapter.rb) | n/a | zero errors |
| 9. Figures | D2 diagrams, generated art, Commons photos | yes | assets/ + credits.yml |
| 10. Build | `rake build` → Quarto profiles | n/a | EPUB, PDF, HTML (+DOCX for editors) |
| 11. Validate | epubcheck, DAISY Ace | n/a | reports in build/ |

Continuity across parallel drafters: drafters get the full outline, the
voice guide, and a shared `book/continuity.yml` (recurring characters, terms
already explained and where, running facts) that the integration pass
updates between drafting waves. Chapters are drafted in two waves (Parts
I-II, then III-V) so later chapters can build on earlier ones.

## Workflows

### Build
`rake build` (or `rake build:pt`, `build:epub`, `build:pdf`). Deterministic
from the repo plus pinned tools; no network.

### "I edited a blog post, update the book"
1. `rake drift` re-inventories and lists stale chapters and analyses, with
   the blog diff since the recorded commit (`--diff`).
2. For each stale chapter: an agent gets the diff and only the paragraphs
   tagged with that post's `src` marker, edits them, re-stamps the sha256.
3. If the change is new material rather than an edit, update the analysis
   and check `outline.yml` placement.
4. When the affected paragraphs are updated (or the change turns out not to
   touch anything the book uses), `scripts/restamp.rb <post-id>` records the
   new sha256 and the blog commit it was reviewed at, per source.
5. `rake check build audit`.

Worked example (2026-10-13): the author removed a Linus Tech Tips video
paragraph from the 10/13 post. `rake drift` flagged ch19 and apA; the diff
showed the passage was never used in the book; `restamp.rb` re-stamped both.

### New post published
`rake drift` reports it as NEW; run its analysis; decide placement in
`outline.yml` (or exclude with a reason); `rake outline:check`.

### EN edition
After PT approval: translate chapter by chapter into `book/en/` keeping ids,
`src` markers and citation keys; voice per WRITER.md's EN section; glossary
and diagram labels have EN fields already. Drift works per language
(`scripts/drift.rb --lang en` compares against `index.en.md` hashes).

## Tests

`rake test` (Minitest, stdlib only; also a CI step before the build) guards
the tools in `scripts/` and `filters/`. `test/test_helper.rb` builds, once
per run, a tiny self-consistent book in a temp dir (outline with front unit,
two parts, an interlude, an appendix, `excluded` with `borrowed_by`; PT and EN
units with markers, refs, citations and glossary marks; credits, PNGs,
inventory) next to a fake blog git repository, and copies it for each test.
Scripts run with `ruby` inside that copy (they compute ROOT from their own
location), so the real book is never touched and no Quarto render happens.
The base fixture passes lint, outline_check, doctor and drift; each test makes
one change and asserts the tool notices it. Filter tests use the Pandoc in
`tools/` and skip without it; placeholder creation skips without ImageMagick.
One file per tool (`test/test_<tool>.rb`); when a tool changes or a bug is
fixed, add the case that would have caught it, with a comment naming the
regression it guards against.

## Decisions

- PT-BR first, EN later (user, 2026-10-13).
- Scope: posts where AI is central; tangential posts only for a specific
  lesson (user, 2026-10-13).
- Narrative over encyclopedia: scene openings, the year as spine (user).
- Superseded content follows lineage.yml; latest state is told as current.
- Toolchain: Quarto (Pandoc + Typst) pinned in tools/, see research/TOOLCHAIN.md.
- Images: diagrams as code (D2); concept art without text; real people only
  via licensed photos; see research/IMAGES.md.
- Ruby for scripts (user's default stack).
