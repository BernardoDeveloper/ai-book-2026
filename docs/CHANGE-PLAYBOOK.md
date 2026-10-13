# Change playbook: structural changes without breaking the book

Learned from the February cut-off change (2026-10-13): the author moved the
book's start from January to February, which removed ten source posts. Three
chapters needed new scenes, about a dozen units needed small repairs, and the
damage that is easy to miss was elsewhere: callbacks in untouched chapters
("os cinco revisores de @sec-ch05"), hand-offs between chapters, timeline and
project appendices, figure labels, the afterword's examples, and every
translated unit. This is the procedure that keeps such a change safe.

## 1. Encode the decision as data first

Policy lives in `book/outline.yml`, where scripts can enforce it:

- `meta.source_from`: the earliest post date the book may use;
- `excluded`: posts left out, each with a `reason`; `borrowed_by: [unit]`
  lists units allowed to use a narrow part of an excluded post;
- chapter `sources`, `scene`, `arc`: the new plan for affected chapters.

`ruby scripts/outline_check.rb` must pass.

## 2. Map the impact before editing

```sh
ruby scripts/impact.rb posts-before 2026-02-01   # or: post <id> | unit <id> | term "<name>"
```

It lists, per post, the marked paragraphs (with word counts and lines) in
each unit, figures and chart scripts citing it, references noted as cited by
it, and lineage entries; per unit, the callbacks into it, its hand-offs, its
figures and the translation that will go stale. Sort the units into:

- **rebuild**: a scene or most of the chapter depends on the change (needs a
  new brief in the outline);
- **repair**: a few paragraphs, a hook, a callback;
- **derived**: appendices, generated pages, figures, translations.

## 3. Edit in parallel without overlapping files

One agent per group of units, each owning disjoint files; tell each agent
which neighbouring hooks and callbacks it must keep working, and to *report*
(not fix) breakage it finds in units it doesn't own. Rebuild agents start
from `docs/DRAFTING.md`; repair agents from `docs/INTEGRATION.md`.

## 4. Verify mechanically, then by reading

```sh
ruby scripts/inventory.rb && ruby scripts/drift.rb   # provenance in sync
rake check            # outline, lint, doctor (refs, citations, glossary,
                      # figures, provenance + cut-off, callback heuristic)
ruby scripts/impact.rb posts-before <date>           # must report 0 posts
rake build            # all formats, epubcheck, page audit, doctor --output
```

Then read `build/<lang>/seams.md` (every unit's closing paragraph next to the
next unit's opening) and the doctor's callback warnings: each warning is a
sentence that points at another chapter by names that chapter no longer
contains. Spelled-out numbers ("sessenta e nove") are a known false
positive.

## 5. Propagate to the other edition

```sh
ruby scripts/drift.rb --lang en --diff   # word-level PT diff since each translation
```

Re-sync only the changed paragraphs (docs/TRANSLATING.md, "Re-sync");
retranslate rebuilt units in full. `rake check build BOOK_LANG=en`.

## 6. Release

`rake release_check` (strict: placeholders and stale translations are
errors) for each language, CHANGELOG entry, `vX.Y.Z` tag.

## Tools and what they guarantee

| Tool | Guarantees |
|---|---|
| `scripts/outline_check.rb` | every AI post is placed or excluded with a reason; ids exist |
| `scripts/drift.rb [--lang] [--diff]` | the book matches the blog; translations match the PT units |
| `scripts/impact.rb` | the full blast radius of a change, before making it |
| `scripts/doctor.rb [--output] [--release]` | cross-references, citations, glossary keys, figures and credits resolve; provenance consistent; cut-off and exclusions respected; callbacks plausible; translation parity; no unresolved references in the built PDF |
| `scripts/lint_chapter.rb` | voice bans, paragraph length, raw URLs, unknown keys, provenance markers |
| `scripts/page_audit.rb` | no split blocks, stranded headings, gaps, runts, oversized images, overfull lines |
| `epubcheck` | valid EPUB |
| `test/` (`rake test`) | the tools themselves keep doing the above |
