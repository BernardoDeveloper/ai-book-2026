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
from step 1). Each produces a ranked report, not edits:

1. errors (typos, grammar, agreement, wrong word);
2. inconsistencies with the style sheet or other chapters;
3. repetition the reader would notice;
4. passages a lay reader would stumble on;
5. pacing (only the worst cases).

The editor (Claude, with the author) accepts items, applies them surgically
(`docs/INTEGRATION.md` rules; voice per `docs/BOOK-VOICE.md`), runs `rake check
build`, and propagates to EN with `scripts/drift.rb --lang en --diff`.
Cheaper models handle the proofreading; flagged hard passages get the strong
model. Rough budget: 2-3M tokens per language.

## Step 3: the author's read

Last and most valuable. Notes can come as comments on any unit or as a list;
the same apply-check-propagate loop handles them.
