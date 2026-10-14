# Edit brief, round 3 (PT): what the second persona pass still found

Follow `reviews/1.0.0-preview.3/personas/edit-brief.md` (provenance rules,
staging for the technical appendix, lint) and `docs/EDITORIAL-RULES.md`.
The items are in `reviews/1.0.0-preview.3/personas-round2/comparison.md`
(numbered 1-13); the persona files in the same folder have the exact quotes.
The ledger `book/integration.yml` still applies (the ch15 "Minha
hipótese"/"Três meses depois" pair stays as is).

Principles for this round:
- When the text contradicts a lesson of the book, fix the design of the
  passage (move the mechanics out, change the claim) instead of adding an
  apology next to it; apologies draw attention to the contradiction.
- A claim from one person's experience is framed as that ("no meu caso",
  "na minha experiência"), never as a law.
- Detail only a programmer uses goes to the technical appendix (staging),
  with a one-line pointer; the chapter keeps the story and the lesson.
- Appendix staging: append new sections to book/pt/_staging/aptecnico-<unit>.md
  with ids {#sec-aptecnico-<short>}; the existing appendix is
  book/pt/aptecnico.md (don't edit it; the editor merges).
