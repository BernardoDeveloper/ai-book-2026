# Copyedit procedure (per release, while the book is open)

The book was written by many agents, each seeing a few units. Mechanical
checks (lint, doctor, page audit, tests) catch structural problems; they don't
catch what a multi-author book typically suffers from: the same phrase or
anecdote reused across chapters, tone drift, inconsistent terminology,
agreement slips. This is the procedure for that, cheapest first. It runs once
per release, on the PT edition first; EN follows only after PT is locked.

## Step 1: style report (mechanical, near-free)

```sh
ruby scripts/style_report.rb --lang pt     # writes build/<lang>/style-report.md
```

- **Repetition across units**: word sequences (7+ words) that appear in more
  than one unit, i.e. reused sentences, anecdotes retold, catchphrases.
- **Recurring phrases**: shorter set phrases (4-6 words) used in many units
  ("castelo de cartas", "espelho da sua competência"): fine as deliberate
  callbacks, worth a look when they become tics.
- **Overused words**: words used far more in one unit than across the book.
- **Terminology variants**: the same name written different ways (case,
  hyphenation, spacing: "e-mail"/"email", "Open AI"/"OpenAI").
- **PT agreement heuristics**: "do que" followed by a conjugated verb (WRITER.md
  wants the infinitive on both sides).

The report is a worklist for a human or an editor agent; nothing is changed.

## Step 2: reader pass (needs the author's go-ahead; costs tokens)

One read-only agent per part (front + Part I, II, III, IV, V, back matter),
each reading its units straight through in order with a shared style sheet
(`build/<lang>/style-sheet.md`: names, spellings, terms, recurring phrases
from step 1). Each produces a ranked report, not edits (shared instructions:
`reviews/reader-brief.md`; the apply agents get `reviews/apply-brief.md`):

1. errors (typos, grammar, agreement, wrong word);
2. inconsistencies with the style sheet or other chapters;
3. repetition the reader would notice;
4. passages a lay reader would stumble on;
5. pacing (only the worst cases).

Each part's findings land in `reviews/<version>/<lang>/part<N>-*.yml` (format:
`reviews/README.md`). Validate and summarise them before triage with
`rake review DIR=reviews/<version>/<lang>` (optionally `GREP=regex` over
problem and suggestion): it checks the schema, that every quote is really in
its unit (reporting the actual line when it moved), adds stable ids
`<part>.<n>` to the items, and prints one line per item with counts per
category and severity. After the apply agents are done,
`ruby scripts/review.rb status reviews/<version>/<lang>` lists the items whose
quote is still in the unit ("unchanged": not applied) and, apart, those the
triage rejected (ids under a "Rejected" or "No change" heading of `triage.md`).

The editor (Claude, with the author) triages the items into
`reviews/<version>/<lang>/triage.md`, applies them surgically
(`docs/INTEGRATION.md` rules; voice per `docs/BOOK-VOICE.md`), runs `rake check
build`, and propagates to EN with `scripts/drift.rb --lang en --diff` (per unit:
`--unit ch05`; then `scripts/restamp.rb --translation ch05`, never by hand).
Cheaper models handle the proofreading; flagged hard passages get the strong
model. Rough budget: 2-3M tokens per language.

### Facts: check them, don't ask

Any item that turns on a fact (a number, a date, a name, who said what, how a
tool behaves) is settled by the editor against the source of truth before it
reaches the author. Sources, in order:

1. the post named by the paragraph's `src` marker
   (`~/Projects/akitaonrails-hugo/content/2026/...`), including its tables and
   per-item breakdowns (recompute totals yourself);
2. the code or data behind the claim: the author's repositories under
   `~/Projects/` (README, source, git history), the chart scripts in
   `assets/charts/`, `book/back/references.yaml` and the cited pages;
3. public records (GitHub API via `gh`, Wikimedia, official docs) for
   anything outside the author's own work.

When two sources disagree, find out why (different scope, date or
population: "653 commits in 8 projects" vs "692 in 4" turned out to be two
cuts of the same work, one excluding the private newsletter repository) and
make the text state its scope rather than picking one number. When the blog
post itself is wrong, the book prints the correct figure and the error goes
to "Blog errata" in the triage for the author to fix at the source.

Only what no available source can settle goes to the author: unpublished
facts, intent ("is this meant ironically?"), preferences (cuts, titles,
tone), and contradictions between the author's own statements with no record
to break the tie. Each question names what was checked and what was found.
Reader and apply agents get the same instruction: verify against these
sources, and report "author question" only with that evidence attached.

## Step 3: the author's read

Last and most valuable. Notes can come as comments on any unit or as a list;
the same apply-check-propagate loop handles them.
