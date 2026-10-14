# Edit brief: applying the target-reader pass (PT)

Project root: /mnt/data/Projects/ai-book-2026. You edit only the PT units you
are assigned (book/pt/<id>.md) plus the staging files named below. Other
agents edit other units in parallel. No git commands. No edits to book/en/.

## Read first

1. `reviews/1.0.0-preview.3/personas/consolidated.md`: the approved plan.
   Every item in sections 2-5 that touches your units is approved, except
   where this brief says otherwise.
2. `docs/EDITORIAL-RULES.md` (R1-R16): the rules behind the plan. Your edits
   must satisfy them.
3. `docs/BOOK-VOICE.md` (voice: Akita's informal first person, "pra", short
   paragraphs, no em dashes, no "não é X, é Y", comparatives with "do que")
   and `book/continuity.yml` (names, canonical_figures, signature_lines).
4. The ledger `book/integration.yml`: don't undo a recorded decision.
5. The persona files in the same folder (`<persona>.yml`) for the exact quotes
   and reasoning behind each item in your units.

## Provenance (non-negotiable)

- Every paragraph keeps the `<!-- src: ... -->` marker of the post it comes
  from. A condensed paragraph keeps its marker. New text with no post behind
  it gets `<!-- src: original -->`. Never leave a paragraph from one post
  under another post's marker (check the paragraph after anything you
  insert).
- Facts come from the sources: check the post (path from the marker:
  ~/Projects/akitaonrails-hugo/content/<id>/index.md) before rewording a
  claim; never add a number the post doesn't support (docs/COPYEDIT.md,
  "Facts: check them, don't ask").
- If, after your edits, a post listed in your unit's front-matter `sources`
  no longer has any marked paragraph in the unit, remove it from `sources`
  (and say so in your report). If you add a paragraph from a new post, add
  it to `sources` with its sha256 from inventory/posts.yml (pt).

## Moving detail to the technical appendix (R11)

The new appendix "Para quem programa: os bastidores" (unit id `aptecnico`) is
assembled by the editor from staging files. For material the plan moves
there, write it to `book/pt/_staging/aptecnico-<your-unit>.md`:

- one `## ` section per topic, with a heading a reader can scan, a first
  line of context (which chapter, what story) so it reads standalone, then
  the moved detail, edited to stand alone (not pasted fragments);
- keep every paragraph's `<!-- src: ... -->` marker; keep figures (with
  their `{#fig-...}` ids and alt text), citations and glossary marks;
- give each section an id `{#sec-aptecnico-<short>}` and leave in the
  chapter a one-line pointer like "Os detalhes técnicos estão em
  @sec-aptecnico-<short>." where the material was.

Material the plan says to cut (pure repetition) is cut, not moved.

## Done

`ruby scripts/lint_chapter.rb book/pt/<unit>.md` for each unit (0 errors;
fix warnings you introduced). Reply with: per consolidated item (number or
B-row), what you did; what moved to staging (section ids); sources removed
from or added to front matter; anything you couldn't do and why.
