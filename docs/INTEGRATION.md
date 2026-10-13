# Integration and fact-check pass (contract for editor agents)

Drafting agents worked in parallel and each saw only part of the book. This
pass makes the book read as one book and re-verifies it with fresh eyes. You
are assigned a set of units; edit only those files (and their `_refs`/`_gls`
side files), never another unit's.

## Inputs

- `book/integration.yml`: the editor's ledger. Every item that names one of
  your units is binding; apply its ruling (or, if it has none, decide and
  record what you did).
- `book/pt/_notes/*.yml`: drafter notes. Act on notes addressed to your units.
- `book/continuity.yml` (who explains what), `docs/BOOK-VOICE.md`,
  `docs/DRAFTING.md` (Rulings), `inventory/lineage.yml` (superseded content and
  corrections).
- The whole book for context: read your units in full, and the opening and
  closing of the units before and after each one.

## What to do, per unit

1. **Ledger and notes.** Apply every item addressed to the unit.
2. **Continuity.** No concept explained twice: if your unit re-explains a term
   owned by another chapter, cut to a half-clause and `@sec-` pointer. No story
   told twice: if another chapter tells it in full, keep a one-line callback.
   Callbacks must match what the other chapter actually says (grep it).
   Hooks: the unit's last paragraph must lead into the next unit as it now
   opens; the first paragraph must not contradict the previous unit's hook.
3. **Adversarial fact check.** Assume the drafter was wrong. For every number,
   date, quote, name and attribution: open the source (the post at
   `~/Projects/akitaonrails-hugo/content/<id>/index.md`, the reference file,
   or the cited URL) and confirm. Online claims: re-verify the ones that carry
   weight (who said what, dates of events, figures about companies). Fix or
   cut what doesn't hold; prefer softening to inventing. Never introduce a
   new unsourced fact.
4. **Superseded content.** Nothing presented as current that `lineage.yml`
   marks superseded; corrections list applied.
5. **Privacy and fairness.** No private repo names, hostnames, IPs; the
   girlfriend unnamed; no allegations about real people beyond what sources
   support; the reader never insulted.
6. **Voice.** Re-run the humanizer and akita-finish checks on anything you
   rewrote. Keep the drafter's good prose; this is an edit, not a rewrite.
7. **Mechanics.** `ruby scripts/lint_chapter.rb <file>` at 0 errors; every
   `@sec-`/`@fig-` reference you add must exist; new citations go in the unit's
   `_refs` file with the conventions in DRAFTING.md; re-stamp nothing in
   `sources` unless you add a post (then add it with its sha256).

## Report

Append to `book/pt/_notes/<unit>.yml` under `integration:` a list of what you
changed (one line each) and anything you could not resolve. In your final
message: per unit, the ledger items resolved, facts corrected (old → new,
source), facts cut, open questions for the author.
