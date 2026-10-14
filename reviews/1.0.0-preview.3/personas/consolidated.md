# Target-reader proof-read and balance check (PT, 1.0.0-preview.3 + Genesys note)

Five simulated readers from "Pra quem eu escrevi" read the PT book straight
through (preface to afterword, appendices as each would): Marina
(profissional, accountant), Roberto (pai), Carla (gerente), Lucas (junior
developer) and Helena (curiosa). Raw reports: `<persona>.yml` in this folder.
Balance data: `scripts/balance_report.rb` -> `build/pt/balance.md`.
Nothing in the book was edited.

Votes below are "n/5 readers raised it". Logic items were checked against the
text and the source posts by the editor before being listed.

## 1. Engagement by unit (1-5)

| unit | prof | pai | ger | jun | cur | avg |
|---|---|---|---|---|---|---|
| prefácio | 4 | 4 | 4 | 4 | 4 | 4.0 |
| como-ler | 3 | 3 | 3 | 3 | 3 | 3.0 |
| antes | 2 | 2 | 3 | 3 | 2 | **2.4** |
| ch01 | 4 | 5 | 3 | 4 | 4 | 4.0 |
| ch02 | 3 | 3 | 3 | 5 | 3 | 3.4 |
| ch03 | 3 | 2 | 4 | 4 | 3 | 3.2 |
| ch04 | 5 | 4 | 3 | 4 | 4 | 4.0 |
| ch05 | 4 | 3 | 3 | 5 | 5 | 4.0 |
| ch06 | 2 | 2 | 4 | 4 | 3 | 3.0 |
| ch07 | 3 | 3 | 3 | 4 | 3 | 3.2 |
| ch08 | 2 | 3 | 2 | 5 | 4 | 3.2 |
| ch09 | 4 | 4 | 4 | 3 | 3 | 3.6 |
| ch10 | 3 | 3 | 3 | 4 | 3 | 3.2 |
| interlúdio 1 | 4 | 4 | 3 | 4 | 5 | 4.0 |
| ch11 | 2 | 2 | 3 | 3 | 2 | **2.4** |
| ch12 | 2 | 2 | 2 | 2 | 3 | **2.2** |
| ch13 | 2 | 2 | 3 | 2 | 2 | **2.2** |
| ch14 | 4 | 4 | 4 | 3 | 4 | 3.8 |
| interlúdio 2 | 3 | 3 | 2 | 4 | 5 | 3.4 |
| ch15 | 4 | 4 | 3 | 5 | 5 | **4.2** |
| ch16 | 2 | 2 | 3 | 4 | 3 | 2.8 |
| ch17 | 4 | 4 | 3 | 4 | 3 | 3.6 |
| ch18 | 3 | 3 | 3 | 4 | 3 | 3.2 |
| ch19 | 2 | 2 | 5 | 3 | 3 | 3.0 |
| ch20 | 3 | 4 | 4 | 4 | 3 | 3.6 |
| epílogo | 4 | 4 | 4 | 3 | 3 | 3.6 |
| posfácio | 3 | 3 | 3 | 4 | 4 | 3.4 |

Pattern: the stories and the practical tools work for everyone (ch01, ch04,
ch05, ch15, interludes, ch14's announcement checklist, apC). The book loses
non-programmers whenever it reports measurements in detail: Part III (ch11-13)
is the low point for 4 of 5 readers, followed by ch16 and the front-matter
reading list. "Sharp when he tells what happened to him, loses me when he
tells what he measured" (Helena) sums up all five.

Best-loved, to protect in any edit: ch04 coffee report (two questions, two
answers) and the eight rules; ch09 health-plan letter; ch15 empty protection
list + habits; ch03 same model 24 vs 91 by harness; ch01 Eliza and the phone
autocomplete; ch07 "zero e nada"; ch17 flattery scam + family code word;
ch19 "Antes de renovar a licença"; ch18 "exoesqueleto ou muleta"; both
interludes; ch14 eight questions; apC.

## 2. Logic and fact (fix regardless of votes)

Ranked by how many readers hit it and how central the claim is.

1. **ch20's conclusion overreaches (5/5).** "Os números dizem que ela não
   vai [ficar mais inteligente que você]" rests on a programming benchmark the
   same chapter calls saturated ("não enxerga nada acima da nota máxima").
   Three readers add that METR's task length "dobrando a cada sete meses" is
   left unreconciled, and that what scares them is tasks being automated, not
   the model getting smarter. Lucas also notes ch01 calls reasoning "mera
   otimização" while ch20 calls o1 "a última revolução da inteligência de
   base". *Fix:* scope the claim to what was measured (base capability on
   tests that still discriminate, plus the pre-training reports); say plainly
   that a saturated test can't show a ceiling; give METR its paragraph (the
   gain is real and comes from harness + tools, which is why it matters for
   jobs); align ch01's wording with ch20.
2. **ch09 contradicts ch06 and argues unfalsifiably (5/5).** "Quase sempre
   ele me dizia isso antes, em vez de inventar" vs ch06 "O agente nunca diz
   não" and the invented facts of ch04/ch07/ch12; "quando a pessoa mostrava o
   pedido, o defeito estava ali" + "a resposta foi 42" blames every failure on
   the request. *Fix:* frame as his experience with well-specified tasks;
   acknowledge models invent and differ (cross-ref ch04, ch11, ch12); "muitas
   vezes" instead of "quase sempre".
3. **ch14's "quem acredita de verdade... fecha a fábrica" (5/5)** is a
   non sequitur (ignores the race argument; contradicts "medo sincero existe"
   two paragraphs earlier). "Gente que entende do assunto não está
   desesperada" cites only LeCun and Ng while the chapter itself reports
   alarmed researchers and ch18 cites Hinton (3/5). "Uma capacidade que
   ninguém de fora pode testar... é alegação" clashes with the 1,726 Mythos
   findings confirmed by outsiders (1/5). *Fix:* turn the line into the
   incentive argument it is ("quem lucra com o medo merece mais escrutínio"),
   acknowledge serious experts on the worried side and say why the book still
   lands where it does, reword the rule ("enquanto ninguém de fora puder
   testar").
4. **ch04's vote weighted by self-declared confidence (4/5)** conflicts with
   the book's own lesson that confident tone means nothing (ch04 itself,
   ch13's tiny model wrong at >90% confidence, ch14). It is a true
   description of Frank Investigator. *Fix:* one sentence: self-reported
   confidence is a weak signal, which is exactly why the primary-source veto
   overrides it.
5. **Productivity multipliers don't add up (4/5).** 6-7x (ch05), ~19x
   implied (ch06: 30 weeks vs 8 days), 3-4 weeks vs 7 days (ch07), "5x, talvez
   10" (ch10), and METR's controlled study at -19% (ch20). A manager can't
   tell which to use. *Fix:* one reconciling paragraph in ch10 (they are
   different measures: per-project guesses vs a controlled study of
   experienced devs on familiar code) and point back to it from ch05/ch06.
6. **ch18's reassurance cuts both ways (3/5).** The punch-card operators
   whose job vanished are exactly the reader's fear; the passage reassures
   programmers with it. Roberto: the Hinton disagreement ("o modelo entende?")
   is his son's question, deferred to ch20, which never returns to it.
   Carla: 53/53 at the ceiling is used to conclude "language doesn't matter".
   *Fix:* say what happened to the operators (the task vanished, the people
   who moved up the stack survived); answer the "entende?" question in ch20
   in two paragraphs or drop the promise; note the ceiling.
7. **Sweeping claims without data.** ch19 "a maioria dos profissionais foi
   treinada a não decidir" (4/5; readers felt accused); ch17 "cai por
   vaidade" (3/5, while the chapter's own example is fear/urgency); ch01 "do
   4 pro 5, a maioria das pessoas nem notou" (3/5, the S-curve's cornerstone,
   unsourced, and the figure has no axis values); ch01/ch14 "empresa que diz
   'perigoso demais' está fazendo marketing" stated as a rule right after
   "não tenho como saber o que pensavam" (2/5). *Fix:* mark them as the
   author's observation/opinion, and in ch17 say "vaidade, medo ou pressa".
8. **Smaller items, each verified:**
   - ch03 "uma diferença de 106 pontos" adds a +67 swing and a -39 swing of
     two different models (1/5): say "o plugin mexeu 67 pontos num e 39 no
     outro".
   - ch12 "a explicação estava no intermediário" (2/5): the 09/15 post says
     the most likely explanation is training-data contamination plus provider
     variation; the 14-provider test only rules out live routing. Align.
   - ch14 "mais de trinta repositórios públicos feitos na maratona" vs ch10's
     24 (6 private) by May: the 08/18 post says "entre janeiro e maio... mais
     de 30"; the 05/14 post says 24. Drop "na maratona" ("feitos desde
     janeiro").
   - ch06 180-200 stories from 274 commits of which 37% were new features
     (1/5): the source's estimate; add that one commit often carries several
     stories, or soften.
   - ch13 ElevenLabs 2.70/episode excludes the 99 dollars/month plan (1/5):
     say "em créditos, fora a assinatura".
   - ch10 "um clone do Mega em um dia... quanto vale uma startup" (2/5)
     overreaches after ch07's 22 security fixes: scope to "a primeira versão".
   - ch16 the decision not to run OpenClaw rests on one AI audit in a book
     that warns about AI audits (3/5); Rice's theorem stated too broadly
     (1/5). Add "que eu não conferi item por item" and tighten Rice.
   - epílogo extends the card's rule to fear ("quanto menos sabe, mais
     imagina o fim do mundo") while ch14 shows experts who fear (1/5).
   - ch17 TikTok's data list stated as fact although the chapter says static
     analysis shows capability, not behavior (1/5).

## 3. Clarity and structure (consensus)

9. **Chapter openings drop the reader into jargon** (ch03 5/5, ch11 5/5;
   ch02 and ch17 1/5 each). ch03 opens on `reasoning_content must be passed
   back to the API`, ch11 on `chat.complete`, before benchmark, tier or
   harness exist for the reader. *Fix:* keep the incident openings, add one
   orienting paragraph before them (what a benchmark is, what we are about
   to see); ch11's practical payoff ("Eu uso um ranking... pra três coisas")
   moves up.
10. **Walls of names and numbers** (ch11 top-7 list 4/5, ch10 18-project
    report card 3/5, ch12 tokenizer distances 3/5, ch13 classifier table
    2/5). *Fix:* keep the lesson and two or three examples; full lists live
    in apA/apD or a figure.
11. **"Como ler" sends readers to the wrong door (4/5).** "Cada parte começa
    num capítulo que dá pra ler sozinho" routes the job question to ch18
    (programmers), the manager to ch18 instead of ch14/ch19/apC, and Part III
    to ch11, the hardest chapter. *Fix:* route by fear: the job -> ch18,
    ch19, epilogue; superintelligence -> ch01, ch14, ch20; manager -> ch14,
    ch19, apC; safety -> ch15, ch17, apB.
12. **The "espelho" line is overused (3/5)**: ch06, ch07, ch10, ch18, ch19,
    ch20, epilogue. *Fix:* keep it in ch06/ch07 (birth) and ch20 (payoff);
    vary or drop elsewhere.
13. **The epilogue promises a Monday and gives principles (3/5).** *Fix:* a
    short concrete list, a few lines per reader type.
14. **Hard-to-follow sequences:** ch14's cast of names (2/5); ch15's
    timeline (opens Oct 10, jumps to Oct 5; "já chego nisso") (2/5); ch08's
    "first failure" frame with a solved bug and a working app inside, and the
    NES converter thread spread over ch03/ch08/ch20 (1/5); the "oráculo"
    idea, used in four later chapters, buried in Nintendo cycles (2/5).

## 4. Gaps for non-programmers (additions, not cuts)

- No word on whether it is safe to paste client/company data into a chatbot
  (Marina). apB covers agents on your machine, not this.
- The job question for other professions gets three paragraphs in ch18
  (Marina, Helena); ch19's examples are all software companies (Carla).
- "What do I tell my son" is never said in one place (Roberto).
- The junior's path is only implicit (Lucas: ch08 and ch18 come late, ch05
  reads as a verdict).

These need new text the blog doesn't have (marked `src: original`), so they
are the author's call. Recommended minimum: one paragraph on data privacy in
ch04's "Dinheiro"/"Saúde" section and the per-reader Monday list in the
epilogue (item 13), which also answers the son and the junior.

## 5. Balance: redundant or tangential material

The book is evenly sized (chapters 3,500-5,100 words; narrative 97,900
words), so the question is weight, not length. Every candidate below keeps
its source post in the book (condensed, never dropped), so provenance and
blog sync are unaffected.

| # | where | words | readers | recommendation | saves |
|---|---|---:|---|---|---:|
| B1 | ch13 hardware ("A largura do cano", MoE, 1-bit) + classifier results | 1,115 + 525 + 834 | 5 | **condense** to the bandwidth-vs-capacity rule, the library/corridor image (moved earlier) and the verdict; classifiers to the "4B ties paid services, rule in code" point | ~1,300 |
| B2 | ch02 "A moda do banco vetorial" + "O agente que sonha" | 1,047 + 196 | 5 | **condense** RAG to its lesson ("a peça obrigatória de uma época vira opcional", ~250 words); autoDream to two sentences | ~950 |
| B3 | ch19 "O fosso e a Adobe" | 1,707 | 3 | **condense** to ~550: the Adobe clones as the latest proof of the ch10 moat argument | ~1,150 |
| B4 | ch18 programming-language detour (Feb question, Sept, Oct) | ~1,510 | 3 | **condense** to ~450 (question, method in one line, result, "tests matter more than the language") | ~1,050 |
| B5 | ch12 "O mistério brasileiro" (Genesys PI) | 1,928 | 4 | **author decided to keep.** Option: condense to ~700 (disclosure, prudence note, what was tested in plain words, the checked/claimed/open list), which also lowers exposure while due diligence is pending | (~1,200) |
| B6 | ch08 "Quatro dias no escuro" (Driveclub) | 1,062 | 3 | **condense** to ~500; surface the "oráculo" definition plainly | ~550 |
| B7 | ch20 "Sete anos numa página" | 862 | 2 | **condense** to ~300 + pointer to apA (repeats ch01/ch03) | ~550 |
| B8 | ch04 "O carimbo invisível" (watermarks) | 912 | 3 | **condense** to ~400 (what it is, what it proves, what it doesn't) | ~500 |
| B9 | ch14 Navier-Stokes mathematicians + resignations | ~870 | 3 | **condense** to ~400 (the headline hid a narrower result; fear got a press office) | ~470 |
| B10 | ch16 "O outro lado da briga" (Kelley/Zig) | 555 | 4 | **cut** to two sentences; keep the Bun method | ~450 |
| B11 | ch10 "O boletim" project list | 806 | 3 | **condense**: chart + pattern + three examples | ~450 |
| B12 | antes reading list | 495 | 2 (+3 notes) | **move** to an appendix ("Leituras"), keep one paragraph and a pointer | ~400 |
| B13 | ch06 "Dados de verdade" bug list | 242 | 3 | keep two bullets | ~150 |
| - | ch12 "A receita da prefeitura" (Rio 3.5) | 1,170 | 2 | keep (clearest attribution case; feeds the three-column lesson) | 0 |
| - | interlúdio 2 (Go) | 1,448 | 1 | keep (2 readers rated it 4-5; it is the book's breather) | 0 |
| - | ch01 Rosenblatt history | - | 1 | keep (loved by 2) | 0 |

Total without B5: about 8,000 words (~8% of the narrative, roughly 30 print
pages). With B5: about 9,200.

Nothing here argues for dropping a chapter or a post: every chapter has a
part readers valued. The weight problem is concentrated in Part III and in
"lab notebook" passages inside otherwise strong chapters.

## 6. Recommended order of work (if approved)

1. Logic/fact fixes 1-8 (small, high value, PT then EN).
2. Clarity 9-14 and the two minimal additions in section 4.
3. Condensations B1-B4, B6-B13 (one agent per chapter group, provenance
   markers kept), then `rake check build`, page audit, and a second persona
   pass on Part III only to confirm the scores moved.
