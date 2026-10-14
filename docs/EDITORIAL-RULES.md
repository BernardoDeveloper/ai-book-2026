# Editorial rules (learned from reviews)

Rules that came out of reader and copyedit reviews, so the same mistakes don't
come back in new chapters, re-syncs or edits. Each rule says where it came
from and how it is enforced. Voice and style rules stay in
`docs/BOOK-VOICE.md`; this file is about argument, structure and reader
experience. Read it before drafting (`docs/DRAFTING.md`), applying review
findings (`reviews/apply-brief.md`) or reviewing (`reviews/reader-brief.md`,
`reviews/persona-brief.md`).

How the files fit together:

- **this file**: general rules. A review pattern seen twice (or once, if it
  is an argument flaw) becomes a numbered rule here.
- **`book/integration.yml`**: the ledger of one-off decisions (a passage
  kept, a section parked, a figure reconciled), with date and reason. Check it
  before touching a passage it names.
- **`book/continuity.yml`**: facts and names the book must state the same way
  everywhere, including the machine-readable registries the tools check.
- **`reviews/<version>/<lang|personas>/`**: the raw findings and triage of
  each review; the evidence behind the rules.

## Argument

**R1. Scope every claim to what was measured.** A test where the top models
tie at the maximum cannot show a ceiling or a plateau; one benchmark cannot
support a claim about intelligence in general; one project cannot support a
rule about all projects. Say what was measured, on what, and what it can't
see. *Source:* persona pass 1.0.0-preview.3 (ch20 "os números dizem que ela
não vai", ch18 53/53, ch11 tie read as ceiling). *Enforced:* briefs.

**R2. No argument that can't lose.** If every failure is blamed on the user's
request and every success credited to it, the claim can't be checked. Present
the author's experience as experience, with the conditions it held under, and
acknowledge the cases elsewhere in the book that go the other way. *Source:*
ch09 "o defeito estava no pedido", "a resposta foi 42". *Enforced:* briefs.

**R3. Opinion is marked as opinion.** "A maioria dos profissionais", "a
maioria das pessoas", "ninguém", "todo mundo" need data or a frame ("na minha
experiência", "minha leitura é"). *Source:* ch19 "treinada a não decidir",
ch17 "cai por vaidade", ch01 "do 4 pro 5 ninguém notou". *Enforced:* briefs;
lint warns on the watch-list phrases in `continuity.yml`
(`generalization_watch`).

**R4. Steelman before rebutting.** Before dismissing a position, state its
strongest form and its best-known serious holder; argue from incentives
("quem lucra com o medo merece mais escrutínio"), not from guessed motives
("quem acredita de verdade fecha a fábrica"). Don't pick only the experts who
agree. *Source:* ch14, ch01 (GPT-2 "perigoso demais" as a rule). *Enforced:*
briefs.

**R5. The book obeys its own lessons.** When the book teaches something
(self-declared confidence means little; AI audits miss and invent; static
analysis shows capability, not behavior), any later passage that relies on
the opposite must say so and say why it is still used. *Source:* ch04
confidence-weighted vote, ch16 single AI audit, ch17 TikTok list. *Enforced:*
briefs.

**R6. One value per recurring figure.** Speed-ups, repository counts, hours,
commit totals and similar numbers that recur across chapters get one
canonical value with its scope in `continuity.yml` (`canonical_figures`); a
chapter that needs a different cut states its scope ("nos 8 projetos até 5 de
março, sem o repositório da newsletter"). *Source:* speed-ups 5x to 19x
(ch05-ch10), repositories 24 vs "mais de trinta" vs 40 (ch10, ch14, ch09).
*Enforced:* registry + doctor (`canonical_figures`).

**R7. Numbers add up where the reader can check them.** Don't sum two
different quantities into one ("uma diferença de 106 pontos" from +67 and
-39); per-episode costs say what they leave out (the subscription); totals
match their parts. *Source:* copyedit and persona passes (ch03, ch09 984,
ch13). *Enforced:* briefs; fact-check step in `docs/COPYEDIT.md`.

## Reader experience

**R8. Orient before the incident.** Opening on a scene is good; opening on an
unexplained error message, library name or score is not. Before the first
jargon term in a chapter, one or two sentences say what world we're in and
why it matters. *Source:* ch03 (`reasoning_content`), ch11 (`chat.complete`),
5/5 readers. *Enforced:* doctor warns when a chapter's first 150 words use a
glossary term before it is explained (`opening_jargon`).

**R9. No walls of names or numbers in prose.** Lists of model names, project
grades or measurements beyond three or four items go to a figure, a table or
an appendix; the prose keeps the lesson and a few examples. *Source:* ch11
top-7 list, ch10 report card, ch12 tokenizer distances, ch13 classifiers.
*Enforced:* lint warns on name-dense sentences and long bullet lists.

**R10. Signature lines have homes.** Recurring lines ("a IA é o espelho da
sua própria competência", "competente o suficiente") are registered in
`continuity.yml` (`signature_lines`) with the units allowed to state them;
elsewhere, call back in new words or not at all. *Source:* "espelho" in seven
units. *Enforced:* style report checks the registry.

**R11. Lab notebook goes to the technical appendix.** Detail that only a
programmer can use (debugging walkthroughs, hardware arithmetic, library
names, benchmark mechanics) goes to the technical appendix as a standalone
section, with a one-line pointer from the chapter. The chapter keeps the
story and the lesson. *Source:* persona pass (ch02, ch08, ch13, ch16, ch18).
*Enforced:* drafting contract; persona pass.

**R12. Don't retell; call back.** A story, a list or a timeline lives in one
unit; others point to it. Appendices keep the full timeline (apA) and project
list (apD); chapters don't repeat them. *Source:* copyedit passes, ch20
"Sete anos numa página", ch10 report card. *Enforced:* style report
(repetition across units); briefs.

**R13. Every reader type gets something concrete.** The book is for
non-programmers first (preface, "Pra quem eu escrevi"). Chapters that argue
from programming must translate the point for other work, and practical
promises ("o que fazer na segunda-feira") are kept with concrete steps.
*Source:* persona pass (accountant, manager, father). *Enforced:* persona
pass.

**R14. The reader's map follows the book.** "Como ler" routes readers by
question to the chapters that answer it; update it whenever chapters are
added, cut or reordered. *Source:* 4/5 personas misrouted. *Enforced:*
`docs/CHANGE-PLAYBOOK.md` checklist.

**R17. Fix the design, not the apology.** When a passage contradicts a
lesson of the book, change the passage (move the mechanics out, change the
claim). An apology placed next to the contradiction ("eu sei que isso parece
bater de frente...") draws every reader to it. *Source:* persona round 2,
ch04 confidence-weighted vote (5/5 readers after the apology was added).
*Enforced:* briefs.

**R18. The book's tests apply to the author.** "Quem ganha se você
acreditar?" applies to the author's own tools, projects and skepticism too;
say so where his projects are presented, and decide by evidence, not motive.
*Source:* persona round 2 (ch14 rule 1 vs ch20 ai-memory). *Enforced:*
briefs.

**R19. One owner per lesson.** A lesson ("teste verde com dado falso mente",
"o espelho") is taught once, in the unit that owns it
(`continuity.yml` explained_in / signature_lines); later units add only
their new case and call back. *Source:* persona round 2 (green-test lesson in
ch06, ch11 and ch12). *Enforced:* style report (repetition), briefs.

**R20. Headlines carry the strongest evidence.** A chapter's or the book's
headline finding leads with the evidence that can bear it (independent,
outside sources), with the author's own measurement as support and its
limits stated; a saturated or single test never carries a headline.
*Source:* persona rounds 1 and 2 (ch20 "linha reta", 5/5 both times).
*Enforced:* briefs.

## Process

**R15. Facts are checked, not asked.** See `docs/COPYEDIT.md`, "Facts:
check them, don't ask".

**R16. Parked, not deleted.** Material taken out for reasons other than
quality (pending verification, author decision) moves to `book/parked/<topic>/`
with its markers, references and a restore note, and gets a ledger entry.
Its posts go to `excluded` in the outline with reason "parked: ...".
