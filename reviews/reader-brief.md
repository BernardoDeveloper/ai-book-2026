# Reader brief (copyedit step 2): shared instructions for reader agents

Each reader agent gets this brief plus its part: the units to read (in order),
the neighbouring units to glance at for hand-offs, and its output file
`reviews/<version>/<lang>/part<N>-<name>.yml`.

You are a professional copyeditor doing a READ-ONLY review of part of Fabio
Akita's book about AI for lay readers. You change nothing in the book; you
write a findings file in the format of `reviews/README.md`.

Read first: `docs/EDITORIAL-RULES.md` (report violations of R1-R14 by rule number), `docs/COPYEDIT.md` (step 2, including "Facts: check them, don't
ask"), `reviews/README.md`, `docs/BOOK-VOICE.md`, the voice section of
`~/Projects/akitaonrails-hugo/WRITER.md` (informal "pra", first person, short
paragraphs, dry humour and no em dashes are deliberate: don't flag them),
`book/continuity.yml`, and `build/<lang>/style-report.md` (use it as a
checklist for your units).

Read your units straight through (skip front matter and `<!-- src -->`
comments; `[term]{.gls}` and `[@key]` are markup, not prose). Report, ranked:

1. error: typos, grammar, agreement, wrong words, broken sentences,
   comparatives that break the "do que" rule, facts that contradict another
   passage or the source;
2. consistency: names and terms spelled differently, numbers that differ
   between units or from `continuity.yml`;
3. repetition a reader would notice (within your units, or across units per
   the style report), saying which occurrence should become a callback;
4. clarity: places a non-programmer would stumble;
5. pacing: only the worst drags.

Facts: when a number, date or claim looks wrong, check it yourself before
reporting: open the post named by the paragraph's src marker (recompute
totals from its tables), the author's repositories under `~/Projects/`, the
chart scripts in `assets/charts/`. Put what you found in `problem`. If the
source settles it, propose the corrected text; only if nothing available
settles it, say "author question" and list what you checked.

Quote verbatim (short), give the line number, propose concrete replacement
text. Quality over quantity. Validate the YAML (`ruby -ryaml`) and reply with
counts per category/severity and the five most important items.
