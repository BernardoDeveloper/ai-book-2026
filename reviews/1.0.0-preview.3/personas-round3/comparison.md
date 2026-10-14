# Persona round 3 (PT, after the round-3 edits) and stopping point

Same five personas, fresh reads. Compare: `ruby scripts/persona_compare.rb
../personas ../personas-round3`.

## Trend across the three rounds

| | round 1 | round 2 | round 3 |
|---|---|---|---|
| book average (units scored by 2+ readers) | 3.32 | 3.38 | 3.41 |
| logic annotations | 73 | 53 | 51 |
| boring | 51 | 64 | 61 |

Biggest gains from round 1 to round 3: ch12 2.2 -> 3.0, ch13 2.2 -> 2.8,
epílogo 3.6 -> 4.2, ch02 3.4 -> 4.0, antes 2.4 -> 3.0, ch18 3.2 -> 3.6.
Still the lowest: ch16 (2.4), ch11 (2.6), ch19 (2.6, aimed at managers: 4 for
the manager, 2 for the others).

The curve has flattened: round 3 found mostly narrower or single-reader
points. Per `docs/PERSONA-REVIEW.md`, this is the stopping point; the rest
goes to the author's read.

## Fixed before 1.0.0-preview.4 (logic, clear and cheap)

- ch20 "Nada disso entrou no treino": now "com toda a probabilidade ficou fora
  do treino; ninguém de fora sabe ao certo" (R1).
- epílogo: the card's rule extended to fear no longer implies that people who
  know don't fear (R4; ch14 shows experts who do).
- ch08: Yomik is "the one I treated as a failure from the start", and the
  oracle story says the NES converter ended up paused (@sec-ch20).
- ch14 "Software não tem mãos" -> "O modelo sozinho não tem mãos; quem dá as
  mãos é o harness" (consistent with ch03).
- ch19 "O cliente é o revisor mais barato e mais confiável" -> real use shows
  what tests don't, without skipping the review before it (R5 with ch16).
- ch03: the brain/hands line is blurrier than the image (tool use is trained
  into the model); the claim is narrower: base reasoning changed little, the
  ability to act grew.

## Backlog for the author's read (not done)

- Move the practical answers earlier for non-programmers: a "what to tell
  your kid" and a "Monday path" pointer near the start (preface or como-ler),
  not only in ch20 and the epilogue (pai, profissional).
- ch16 and ch11 remain the hardest chapters for non-programmers; a further
  cut would mean shortening the OpenClaw/FrankClaw story and the benchmark
  narrative again (several readers).
- ch19 serves managers well and others poorly; consider an opening note
  saying who the chapter is for.
- ch14: put the "quem é quem" summary before the names, not after (pai,
  junior).
- ch13/ch14: the Jev story is split between two chapters (junior).
- ch17: the opening disclaimer weakens the findings; the chapter covers four
  subjects under a title about apps (curioso).
- ch04 privacy paragraph as a highlighted box (profissional).
- The "espelho" line still reads as a refrain to one reader (ch06, ch07,
  ch20 are its registered homes).
- ch03 "15 a 20 pontos" computed against a 69 the chapter calls mixed
  authorship (gerente): check the source and restate the baseline.
- ch14 "Quem esperou um mês... quase sempre economizou": generalizes from
  four episodes (gerente).
