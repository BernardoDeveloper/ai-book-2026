# New chapter: scoped persona review

Date: 2026-10-16. Chapter: `book/pt/ch19b.md`, "O mundo não vai esperar".
Reviewed SHA-256: `948c3ecd0c093c88376ddfea1a3c105a71e8ee4f3bfe826495fa3c74ae1271fa`.

Five independent simulated readers, using `reviews/persona-brief.md` and the
scoped procedure in `docs/PERSONA-REVIEW.md`. Each read the complete chapter,
with the end of ch19 and beginning of ch20 as context. Reviewers did not see
each other's findings. These are model-generated reading hypotheses, not
human audience research or evidence of market reception. No manuscript edits
were made in this review.

## Scores and interpretation

| Reader | Score / 5 | Main reaction |
|---|---:|---|
| Marina, accountant | 3 | Credible employment warning; wants an accessible first action. |
| Roberto, father/shop owner | 3 | Understandable analogies and useful discount exercise; middle drags. |
| Carla, operations manager | 4 | Billing example and bounded redesign account work; wants a decision she can take. |
| Lucas, junior developer | 4 | Learning argument helps; needs a connection to assigned work. |
| Helena, retired history teacher | 3 | Strong opening and film scene; repeated explanations reduce momentum. |

Mean: 3.4/5. This is one scoped round, not an improvement over an earlier
baseline. Scores are noisy; recurring observations are the useful result.
All five mention repetition in the sequence of analogies/explanations. Four
explicitly identify cooking after cinema as an extra pass over a familiar
point; Lucas identifies the broader sequence and the final Nolan callback.

## Protect in any revision

- The concrete late-night opening and six **existing** sites, with limits on
  what that personal experience establishes.
- Explicit acknowledgment that competent workers can lose jobs and that new
  opportunities do not necessarily arrive in time for displaced individuals.
- Both author-requested analogies. Cinema should explain direction and
  integration; cooking should explain practice and repeatable performance.
- The prolonged-silence example: a small creative decision affects the whole
  film. Helena singled it out as effective narrative.
- Billing and discount/return examples. These connect judgment to observable
  decisions rather than a prestigious job title.
- Credit for specialist crafts and the distinction between human collaborators
  and a fallible model. Condensing must not restore the inaccurate suggestion
  that Nolan never participates in camera or editing decisions.

## Findings checked against the text

### 1. Repeated explanations slow the middle (5/5)

Accepted. The chapter states the direction/execution distinction before the
film-role list, explains collaboration afterward, restates credit versus sole
authorship after the Oscar example, applies it to software, then revisits
authorship and recipes. These have distinct purposes but overlapping setup.
The final section returns to Nolan again after the learning argument has landed.

Recommendation: condense connective explanation, not the requested subjects.
Retain the six specialist roles, the concrete film scene and a short accurate
award example. Let the cooking section move promptly from recipe to repeated
practice, without reintroducing the entire judgment/execution argument. Remove
or shorten the final Nolan recap. Do not replace either analogy with another.

### 2. The next action could fit ordinary employment better (3/5)

Accepted with scope limits. Marina, Carla and Lucas want a more immediate
workplace action. The chapter already supplies a discount/return exercise,
so it does not lack practical content. What is missing is a short connection
to work assigned by somebody else, rather than a self-directed project.

Recommendation: make the exercise explicitly usable in an ordinary review:
choose one existing rule, state the expected result before asking the agent,
change one condition, then compare and discuss the discrepancy with a colleague
or reviewer. An accountant can use the same rule-checking pattern without
writing software. Keep this to a short paragraph, not a new checklist.

The epilogue already owns role-specific Monday actions; ch19 owns managerial
questions, and apestudar owns the study method. Add a direct epilogue pointer
if needed. Do not duplicate those sections or turn this chapter into a manual.

### 3. Make prediction in the discount exercise explicit (2/5)

Roberto needed a clearer definition of checking versus repeating the model's
explanation. Lucas wanted an ordinary workplace setting. Resolve both within
finding 2: state what the reader thinks should happen after a return before
consulting the tool. No separate expansion is necessary.

## Logic/fact triage and rejected findings

No confirmed new factual or logical defect emerged from this persona round.
That is not a fresh exhaustive fact-check of every external source; the
chapter's separate local/web fact pass remains recorded in `_notes/ch19b.yml`.

The editor checked quotes and context rather than counting every annotation:

- Marina attributed "Se você é funcionário" and the six-question checklist
  to ch19b. That passage is in **ch19**, not this chapter. Exclude this quote
  as evidence of a new-chapter defect. Her broader wish for a first action
  is independently supported by her comments on ch19b's ending.
- Carla's quote "Ter as tarefas existentes exigiria abrir mão justamente
  desse ganho" does not occur. The actual sentence is "Preservar todas as
  tarefas existentes exigiria abrir mão justamente desse ganho." Her
  summary also puts the license-renewal checklist in the next chapter; it
  is in **ch19**, the preceding chapter. Exclude both attribution errors.
- Roberto's Ramsay quote omits Markdown bold markers but matches the rendered
  prose. It is a valid quote, not fabricated wording.
- Roberto wants an answer to superintelligence here. This chapter addresses
  employment, authorship and learning; the closing handoff intentionally leads
  to ch20. Do not add a second treatment of model limits.
- Marina's concern about employer control over saved time is plausible, but
  the passage already says "Se a automação libera parte do seu tempo" and
  the job-loss section explicitly covers reductions in headcount. Not a
  factual contradiction. The workplace framing in finding 2 addresses the
  useful part without another defensive caveat.
- Carla's request for a company redistribution/retraining example is a
  single-reader addition and exceeds this chapter's purpose. The existing
  transition-cost paragraph and ch19 suffice for this pass.
- Marina's ambiguous "essa aposta", Carla's "gosto" terminology and Helena's
  wish to cut the explicit job-immunity rebuttal are isolated preferences.
  Do not prioritize them over the author's explicit brief.

Source checks: the October 16 article supports bounded redesign, simulated
review limitations, adaptation and transition costs. Akitando 76's transcript
supports deliberate practice (lines 508–512) and the legitimate use of courses
(line 340). The proposed workplace clarification develops an existing example;
it does not require inventing a new historical event or economic forecast.

## Balance and recommended scope

`ruby scripts/balance_report.rb` counts 3,467 chapter words after markup removal.
Approximate whitespace counts below include headings and citation markup, so
they are useful for relative size, not directly additive to that total.

| Passage | Approximate words | Reader signal | Recommendation |
|---|---:|---|---|
| Nolan section | 812 | 5/5 pacing concerns | Condense repeated framing; preserve roles, scene and collaboration. |
| AI authorship section | 461 | Part of broader repetition pattern | Keep the distinct quality/provenance argument; avoid re-proving direction. |
| Recipe plus learning section | 679 | 4/5 explicitly flag extra analogy | Keep recipe concise; protect deliberate practice and discount example. |
| Closing section | 306 | Lucas flags Nolan return | Shorten the recap; keep the forward hook. |

Suggested net cut: roughly 150–250 words, subject to the actual edit; add only
the compact workplace clarification and routing pointer. This is an editorial
estimate, not a measured result or an approved edit. The author explicitly
asked for both Nolan and Michelin, so proposals to delete an entire analogy
are rejected.

## Next step

Author decision on the two recommended changes: tighter middle and a more
workplace-grounded exercise. If approved, edit PT and run a fresh scoped
persona reread without showing the previous findings. Compare whether these
specific issues recur rather than chasing a higher average score.

No build, translation, commit, push or release. The two photographs remain
pending as recorded previously; this was a prose review, not image/layout QA.
The mandatory drift check found unrelated stale Jev and October 13 publishing
sources; none involves ch19b. Those updates were not folded into this review.
