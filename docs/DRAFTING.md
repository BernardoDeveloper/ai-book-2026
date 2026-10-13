# Drafting a chapter (contract for drafting agents)

You are writing one unit (chapter, interlude, front/back matter) of the book.
Language: Brazilian Portuguese, Akita's voice. You work alone; other agents
write other chapters in parallel, so stick to this contract.

## Read first (in this order)

1. `docs/BOOK-VOICE.md` — the book voice; it inherits the blog rules.
2. `~/Projects/akitaonrails-hugo/WRITER.md` — voice section (rule 1) and rule 11.
3. `~/Projects/my-skills/akita-finish/SKILL.md` and `~/Projects/my-skills/humanizer/SKILL.md`.
4. `book/outline.yml` — the whole thing (know what other chapters cover), then your unit's entry.
5. `book/continuity.yml` — who explains what; don't re-explain concepts owned by other chapters.
6. `inventory/lineage.yml` — if any of your posts is superseded, use only what `keep_from_old` allows and tell the latest state.
7. For every source post: `inventory/analysis/<id with / as __>.yml`, then the FULL post at `~/Projects/akitaonrails-hugo/content/<id>/index.md`.
8. Any `ref:` files listed for your unit (reference projects under `~/Projects/`). Never name private repos or reveal hostnames/IPs.
9. Seed glossary `book/back/glossary-pt.yml`.

## Write

`book/pt/<id>.md` (the preface is `book/pt/index.md`). Front matter:

```yaml
---
id: ch05
chapter: "Os primeiros dez por cento"   # NOT `title:` (Quarto would print the heading twice)
sources:                      # every post you drew from, sha256 from inventory/posts.yml (pt.sha256)
  - {post: 2026/01/28/vibe-code-..., sha256: "..."}
refs_projects: []             # reference-project files used, e.g. "ai-jail/README.md"
blog_commit: "<blog_commit from inventory/posts.yml>"
---

# Os primeiros dez por cento {#sec-ch05}
```

Interludes and front/back matter use `{#sec-<id> .unnumbered}` on the H1.

Body:
- Length: chapters 3,500 to 5,000 words; interludes 1,000 to 1,800; front/back matter as briefed.
- Follow the unit's `scene`, `question`, `arc` from the outline. Open on the scene; close on a hook toward the next unit (read the next unit's outline entry).
- `##` for sections (3 to 6 per chapter, literary titles, sentence case), `###` sparingly.
- Provenance: put `<!-- src: 2026/MM/DD/slug -->` on its own line before each block derived from a post; `<!-- src: original -->` before new material; `<!-- src: ref:<project>/<path> -->` before reference-project facts. A marker applies until the next marker.
- Facts: only from the posts, the reference projects, or sources you verify online (WebSearch/WebFetch). Never invent numbers, dates, quotes. Apply `lineage.yml` corrections.
- 2 to 4 blockquote takeaways per chapter, where the insight lands.
- Glossary: mark the first use IN YOUR CHAPTER of each technical term with `[termo]{.gls}` or `[texto]{.gls key=chave}` using keys from the seed glossary. If a term you need has no key, propose it in `book/pt/_gls/<id>.yml` (same format as the seed: key → term, long?, def).
- Citations: every external fact that the blog backed with a link gets `[@key]`. Put the CSL-YAML entries in `book/pt/_refs/<id>.yaml` under `references:`. Key convention: `<lowercase author family name or org><year><one-word>`, e.g. `vaswani2017attention`, `anthropic2024mcp`, `metr2025tasks`. Required fields: id, type (article-journal, paper-conference, webpage, post-weblog, motion_picture for videos, software, report, article-newspaper), title, author (or publisher/org as `author: [{literal: Anthropic}]`), issued (date-parts), URL, accessed (date-parts [[2026,10,13]]), and `note: "cited-by: <post id>"`. Akita's own videos/podcasts may be cited; his blog posts are not cited (the generated "Fontes" appendix lists them).
- Figures: where the outline lists illustration ideas (or you see a strong need), insert
  `![Legenda curta.](assets/figures/<fig-id>.png){#fig-<fig-id> fig-alt="descrição para leitores de tela"}`
  with fig-id `<chapter>-<slug>` (e.g. `ch02-janela-de-contexto`) and describe it in `book/pt/_figs/<id>.yml`:
  `- {fig: ch02-janela-de-contexto, kind: diagram|concept-art|photo|chart, idea: "...", labels_pt: [...], caption: "...", alt: "...", photo_query: "for photos: subject and event"}`.
  Max 3 figures per chapter. Never request generated images of real people.
- No URLs in prose, no code blocks longer than 8 lines, no install steps, no tables over 8 rows.

## Finish (do these as explicit passes, not "kept in mind")

1. Fact pass: reread every number, date, name and quote against its source. Fix or cut.
2. Humanizer pass (humanizer SKILL.md, file mode).
3. akita-finish pass (except "keep inline links": links became citations).
4. `ruby scripts/lint_chapter.rb book/pt/<id>.md` until 0 errors; fix paragraph warnings too.
5. Validate your YAML side files with `ruby -ryaml -e 'YAML.load_file(ARGV[0])' FILE`.

## Rulings (settled during the pilot chapter)

- **Glossing order.** The chapter that owns a concept (continuity.yml `explained_in`) explains it properly. If the term shows up in an earlier chapter in reading order, give it a half-clause gloss there and move on; never a second full explanation.
- **Cite verified facts even when the blog had no link.** If you verify a fact online, cite the source you used.
- **Source beats outline.** When the outline brief and the post disagree on a detail, follow the post.
- **Paragraph ceiling** is a reading-comfort guide: split at natural beats. A lint warning left on a scene paragraph is acceptable when splitting would hurt it. Don't turn a run of questions into a list just to satisfy the linter.
- **Model and product names** in the vendor's spelling (Kimi K2.5, GPT-5.2 Codex), even when the blog abbreviated them.
- **Blockquotes:** the 2 to 4 limit counts takeaways only; quoted dialogue or documents don't count.
- **Hooks** may borrow a fact from the next unit's post; list that post in your `sources` too.
- **Frank projects** are named after Frank Rosenblatt (continuity.yml).
- **Shared citation keys.** Before inventing a key, grep `book/pt/_refs/` for the same URL; reuse the key if another chapter already has it. The merge step dedupes anyway, but shared keys keep chapters readable.

## Report back

Word count; sources used; any lineage decisions; facts you could not verify (and what you did); glossary keys proposed; figures requested; anything another chapter should know (append it under a `notes:` list in `book/pt/_notes/<id>.yml`, never edit continuity.yml or outline.yml yourself).
