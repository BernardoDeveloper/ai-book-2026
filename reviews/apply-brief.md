# Apply brief (copyedit step 2): shared instructions for apply agents

You are applying accepted copyedit findings to one edition of Fabio Akita's book "Competente o Suficiente". Project root: /mnt/data/Projects/ai-book-2026.

Read first:
- reviews/<version>/<lang>/triage.md: the editor's rulings. Default is "accept as suggested"; the triage lists book-wide rulings, who keeps/who shortens repeated material, items to verify against sources, and rejected items.
- reviews/README.md (finding format) and your findings file(s) listed below. Item id `<part>.<n>` = the n-th item (1-based) in part<part>-*.yml.
- docs/BOOK-VOICE.md and docs/INTEGRATION.md (edit rules). Voice: Akita's informal first person, "pra", short paragraphs, no em dashes, no "não é X, é Y", comparatives with "do que".

Rules:
- Edit ONLY the files you own (listed below). Other agents are editing the other units in parallel. If an item needs a change in a file you don't own, skip it and report it.
- Surgical edits: change the sentence/paragraph the item names, nothing else. Keep `<!-- src: ... -->` markers, `[term]{.gls key=...}`, `[@cite]`, `@sec-`/`@fig-` refs and `{#id}` attributes intact. Line numbers in the findings may have shifted slightly; locate by the quote.
- The suggestion is a proposal, not a script: make it read naturally in context and in Akita's voice. Where the reader misread the text, don't apply; note why.
- Facts (numbers, dates, names, quotes, tool behaviour) are yours to check, whether or not triage.md marks them: follow docs/COPYEDIT.md "Facts: check them, don't ask" (source post via the src marker, recompute totals from its tables; the author's repos under ~/Projects/ and the chart scripts; public records). When sources disagree, find the reason (scope, date, population) and make the text state it. Report an author question only when no available source settles it, with what you checked.
- Apply the book-wide rulings (GPT model names, Z.ai, sprint feminine, article before @sec- refs, comparatives, "pra", no rhetorical negation) to every occurrence in your files, even ones the readers didn't flag; grep for them.
- Never edit `translated_from.sha256` or any other hash in front matter by hand; the hashes are recorded by `ruby scripts/restamp.rb --translation <unit>` (EN, after re-syncing from PT) and `restamp.rb <post-id>` (posts). Use `ruby scripts/drift.rb --lang en --diff --unit <unit>` to see what changed in the PT unit you are following.
- Don't touch the other edition, the outline, front matter, or anything outside your files. No git commands.
- When done: run `ruby scripts/lint_chapter.rb book/<lang>/<file>.md` for each file you changed (fix anything you introduced), then reply with: per item id, applied / modified (how) / skipped (why); the author questions with evidence; cross-file items you couldn't do.
