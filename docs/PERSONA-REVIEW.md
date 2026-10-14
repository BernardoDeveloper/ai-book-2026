# Target-reader review (persona proof-reading)

A review by simulated readers: the people the preface says the book was
written for ("Pra quem eu escrevi"), each reading the whole book in order and
reporting where they got lost, bored, or unconvinced. It complements the
copyedit (`docs/COPYEDIT.md`), which checks the text; this checks the
reading experience and the argument. First run: 2026-10-13, on
1.0.0-preview.3 (`reviews/1.0.0-preview.3/personas/`).

## When to run it

- Before closing a version with structural or substantial content changes.
- On the changed parts only, after a round of cuts or rewrites, to confirm
  the scores moved (Part III after the 2026-10-13 condensation, for example).
- PT first. The EN edition gets it only if its own readers differ (they
  don't so far: it's a faithful translation).

## The personas

Defined in `reviews/persona-brief.md`, derived from the preface:

| slug | who | what they need from the book |
|---|---|---|
| profissional | Marina, 38, accountant, reads on her phone | will my job end; what to do Monday |
| pai | Roberto, 52, shop owner; his 15-year-old asked about superintelligence | what to tell his son; distrusts hype and jargon |
| gerente | Carla, 44, operations manager being sold an "AI transformation" | decisions; what to ask the consultants |
| junior | Lucas, 24, junior web developer | did I choose the wrong career; how do I grow |
| curioso | Helena, 61, retired history teacher | stories and context; no patience for manuals |

If the preface's list of readers changes, change the personas with it.

## How to run it

1. One read-only agent per persona (`reviews/persona-brief.md` + the
   persona slug), cheaper model, in parallel, each reading the PT units in
   reading order. Output: `reviews/<version>/personas/<slug>.yml` with a
   summary, best/worst moments, a 1-5 engagement score per unit, at most 35
   annotations (confusing, boring, rewrite, logic) and cut candidates.
   About 350k tokens per persona for the whole book.
2. Balance data: `ruby scripts/balance_report.rb` (`rake balance`) ->
   `build/pt/balance.md` (words per unit and per source post, overlap).
3. The editor consolidates into `reviews/<version>/personas/consolidated.md`:
   - score matrix (unit x persona) and the pattern behind it;
   - what readers loved (to protect in any edit);
   - logic and fact items, each **checked against the text and the source
     posts** before listing (R15); these are fixed regardless of votes;
   - clarity and structure items ranked by how many personas raised them;
     single-persona taste notes are dropped (no nitpicking);
   - gaps (additions) separated from cuts, since additions need new text;
   - balance table: candidate cuts with word counts, votes and a
     recommendation (cut, condense, move to an appendix, keep).
4. The author decides; the editor records one-off decisions in
   `book/integration.yml` and promotes recurring patterns to numbered rules
   in `docs/EDITORIAL-RULES.md`, with the source review and how each rule
   is enforced (brief, lint, doctor, style report).
5. Edits: `reviews/<version>/personas/edit-brief.md` (provenance rules,
   staging for the technical appendix, parking), one agent per group of
   units, then `rake check build`, page audit, EN propagation.

## Rounds: review, edit, re-read

One pass is not enough: edits fix the old problems and create new ones (an
apology added next to a contradiction made 5/5 readers notice it). Work in
rounds:

1. **Round N review** (step 1-3 above), output in
   `reviews/<version>/personas[-roundN]/`.
2. **Edit**: the approved items, through an edit brief per round
   (`edit-brief.md`, `edit-brief-round3.md`, ...) that lists the items by
   number and states the round's principles; PT first, one agent per group of
   units, staging for the technical appendix, then EN re-sync
   (`drift.rb --lang en --diff --unit X`, `restamp.rb --translation X`).
3. **Round N+1 review**: the same personas, fresh read, told not to open
   `reviews/` (so they don't anchor on round N). Compare with
   `ruby scripts/persona_compare.rb <old dir> <new dir> [--grep REGEX]` and
   write `comparison.md`: what moved, which round-N problems are gone, what
   still comes up from 3+ readers, what is new.
4. **New patterns become rules** in `docs/EDITORIAL-RULES.md` (R17-R20 came
   from round 2).

Reading the results:

- Scores are noisy: an unchanged chapter can move by 0.6. Don't chase the
  book average; check whether the specific problems recur
  (`--grep` on the old quotes and keywords).
- Logic findings are the best signal: fixed ones should not come back, and a
  new one raised by several readers is real.
- Stop when the targeted problems don't recur and nothing new reaches 3+
  readers; what remains is taste or the author's call (the author's own read,
  step 3 of `docs/COPYEDIT.md`).

Cost: about 350k tokens per persona per full read (five personas ~1.7M), plus
the edit and re-sync agents. A round on changed chapters only is cheaper.

## What the first run found (2026-10-13)

- Stories and practical tools worked for all five (ch01, ch04, ch05, ch15,
  interludes, ch14's checklist, apC); the measurement-heavy middle lost the
  non-programmers (ch11-ch13 averaged 2.2-2.4 of 5).
- All five caught the same argument flaws: ch20's conclusion beyond its
  evidence, ch09's unfalsifiable "the request was the problem", ch14's
  motive-reading line. These became rules R1-R5.
- Four of five were sent to the wrong chapter by "Como ler" (R14).
- Outcome: logic fixes, orienting openings, a per-reader Monday list in the
  epilogue, a privacy paragraph in ch04, about 8,000 words condensed, the
  programmer-only detail moved to a new technical appendix (`aptecnico`),
  the reading list moved to an appendix (`apleituras`), and the Genesys PI
  section parked (`book/parked/genesys-pi/`).

## Results of the three rounds (2026-10-13/14, released as 1.0.0-preview.4)

| | round 1 | round 2 | round 3 |
|---|---|---|---|
| book average | 3.32 | 3.38 | 3.41 |
| logic annotations | 73 | 53 | 51 |

Round 1 fixed the argument flaws all five readers caught and moved ~8,000
words of lab notebook out of the chapters. Round 2 showed the apology-next-
to-the-contradiction effect (R17) and the headline-evidence problem (R20).
Round 3 found mostly narrower points; the curve flattened and the review
stopped there, with a backlog for the author's read in
`reviews/1.0.0-preview.3/personas-round3/comparison.md`. Cost: about 5.2M
tokens of persona reads plus ~3M for edits and EN re-syncs across the three
rounds.
