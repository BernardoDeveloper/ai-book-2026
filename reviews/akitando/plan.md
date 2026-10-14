# Plan: coloring the narrator with the Akitando history

Sources: `extract-*.yml` (23 episodes read in full), `factcheck.yml`
(141 claims checked), the author's confirmed bio (`profile.md`). Rules:
`profile.md`, "How to use it". Every touch cites only what those episodes
say; conclusions drawn from them stay within what they support.

Target: about 25-30 touches across the book, most of them one to three
sentences. Episodes are cited (title, year, link in the bibliography) only
where a dated warning or a direct quote is the point; elsewhere the history
shows up as voice.

## A. Corrections the history exposes (do regardless)

1. ch18 "A bolha que estourou antes": the hiring bubble started "a partir de
   2010, com juro perto de zero" (fact-check; the author's own ep. 72, 90,
   100, 132), not "por volta de 2014"; Akitando ran "de 2018 ao fim de 2023"
   (149 episodes), not "até o começo de 2024"; the dot-com bubble burst
   "entre 2000 e 2002" (Nasdaq peak March 2000); 2022 layoffs "uns 165 mil"
   (layoffs.fyi). Blog errata for the 02/08 post.

## B. Touches, by unit

| # | unit / section | touch (what the sentence says) | from | facts |
|---|---|---|---|---|
| 1 | prefácio, "De que lado eu estou" | who is speaking, in two sentences: programming since 1990, the dot-com crash from inside, five years integrating SAP in large companies, Rails since 2007, RubyConf Brasil 2008-2016, Codeminer 42 since 2011, Akitando 2018-2023 made to teach what survives bubbles | bio, ep. 138, 34 | confirmed by the author |
| 2 | ch01, "Bolhas estouram, tecnologias ficam" | lived it: the dot-com companies died, the internet didn't; Google and Amazon grew in the dry years | ep. 138 | Nasdaq 2000-2002 verified |
| 3 | ch01, LLM is statistics | "Em 2020 eu já dizia que machine learning é basicamente estatística e probabilidade" (one line, no quote block) | ep. 84 | quote verbatim |
| 4 | ch04, evidence | "quantidade de evidência não é qualidade": why the primary source overrides three agreeing models; the 99%-accurate-test example in one sentence | ep. 84 | base-rate math checked |
| 5 | ch05, the 200-hour estimate | estimates as order of magnitude, a view he defended in 2022 | ep. 130 | - |
| 6 | ch06, tests | "só porque compila não significa que bugs não foram introduzidos" (2022): the agent's green test is the same illusion | ep. 130 | - |
| 7 | ch07, software never done | "design emerge do software", never done at 1.0 (2021) | ep. 104 | - |
| 8 | ch08, "Como se aprende agora" | learning in 1990 meant a 100-page manual and months on dBase; with fundamentals a new language takes weeks; the pain of learning can't be outsourced (+ ep. 76 if its extract supports it) | ep. 61, 65, 90, 76 | author memory, framed as such |
| 9 | ch12, cheating | any metric becomes a target: the workplace that measured bugs fixed rewarded people who create bugs | ep. 120 | - |
| 10 | ch14, "A fábrica de propaganda" | "a quem essa mensagem beneficia?" is a question he has asked since 2019-2020 (stage entrepreneurship, the Social Dilemma ex-executives selling regulation) | ep. 52, 84 | - |
| 11 | ch14, money | the pattern he described in June 2021 (expenses relabeled as investment, mass hiring before profit, SPACs: 59 in 2019, 248 in 2020, 613 in 2021), "engordar o porco antes do abate" | ep. 100 | SPAC counts corrected |
| 12 | ch16, review | no code is immune to review, whoever wrote it (2019); the spiral of more people, more bugs (2022): swap people for agents | ep. 64, 130 | - |
| 13 | ch18, "A bolha que estourou antes" | the dated warnings: June 2019 ("vai estourar"), February 2020, before the pandemic ("quem não souber entregar resultados... vai ficar sem emprego"), November 2022 ("estourou"); the mechanism (money near zero interest pushed into startups, then rates rose: 0-0.25% until March 2022, 4.25-4.50% by December 2022); and the honest line: he expected a second leg of the crash in 2023 that didn't come (the AI wave lifted the market) | ep. 50, 72, 132 | Fed dates verified |
| 14 | ch18, same section | the dot-com crash from inside: his dot-com closed in 2001, one week out of work, a mentor's call into SAP; never called himself "programador ASP" | ep. 138, 34 | author confirmed |
| 15 | ch18, "Os engenheiros de bootcamp" | the 2020 arithmetic: ~1,400 hours to a first junior level; an 80-100 hour workshop is ~5% of it | ep. 72 | - |
| 16 | ch18, "O que sobra quando a digitação some" | June 2022, before ChatGPT: the programmer was never the factory worker, the compiler is | ep. 120 | ChatGPT 30 Nov 2022 verified |
| 17 | ch18, "Como alguém vira sênior" | junior, mid and senior solve the same problem; the difference is time and how many wrong attempts you cut; seniority is deciding and owning it | ep. 64 | - |
| 18 | ch18, "Continue contratando júniors" | "o júnior de hoje é o sênior de amanhã" (2021) | ep. 104, 120 | - |
| 19 | ch18, "Que linguagem aprender" | 1996-2001: about ten stacks without being "programador de" any; Bell's Law (1972) and the ten-year cycle of dominant tech | ep. 138, 37 | Bell 1972 verified |
| 20 | ch19, "Gente treinada pra não decidir" | identify the "vídeos de 2019" the chapter already cites: "Esqueça metodologias ágeis" and "Não terceirize suas decisões" | ep. 51, 63 | - |
| 21 | ch19, "A premissa mudou" | the economics of fixing changed the method before: design-first made sense when debugging was expensive (1960s-80s) | ep. 106 | - |
| 22 | ch19, "Jogar código fora" | Brooks, 1975: "plan to throw one away"; the agent made the second version cheap | ep. 23 | MMM 1975/1995 verified |
| 23 | ch19, owners | five years integrating SAP across sales, finance, HR and logistics taught that no programmer knows a big company's rules without living them: why the decision stays in-house | ep. 34, 104 | author confirmed |
| 24 | ch20, "mapa em branco" / epílogo "O seu domínio" | the same enterprise experience backs the claim that the model is blind to private domain knowledge | ep. 34, 144 | - |
| 25 | ch20 "O que é seu" / epílogo "Sem entregar o volante" | "Não terceirize suas decisões" (2019), his most known episode: 100% of the merit and of the loss is yours; outsourcing to the model is the new version | ep. 63 | - |
| 27 | ch18, "O esconderijo acabou" | "Aprendendo a aprender" (2020, his most watched episode): people who learned only the "como" of a tool and never the "por que" get confused by every new tool; the agent is the newest tool | ep. 76 | quote verbatim |
| 28 | ch08, "Como se aprende agora" | the 80/20 trap: 20% of the knowledge lets you deliver, the rest needs what you don't have; the agent hands you the first 20% free and hides the gap | ep. 76 | framed as his teaching |
| 29 | epílogo, "Pra esta semana" / "O que vale aprender" | the course gives 1%, you hunt the other 99%; a small problem with no tutorial, tried alone before asking the machine | ep. 76 | - |
| 26 | epílogo, "Medo vende" | in 2022 he told a young viewer to drop the influencer course and study for real; the 2026 course has a new name, the mechanism is the same | ep. 132 | - |

## C. Appendix suggestions

1. **Recommended: "Três bolhas" (new, short appendix, ~1,200 words).** One
   page crossing the cycles the narrator lived with verified numbers: the
   dot-com bubble (Nasdaq peak March 2000, bottom October 2002), the
   zero-interest hiring bubble (2010-2022, rates near zero, SPACs, the 2022-23
   layoffs: ~165k and ~263k), and the AI wave since ChatGPT (November 2022).
   What each left behind (fiber and the web; a generation of programmers; the
   models) and what the narrator did in each. It answers "will the career
   end?" with history instead of opinion, and keeps ch18 from growing.
2. **Small addition to apmecanica:** the base-rate box (a 99%-accurate test
   for a 0.1% disease gives ~9% after a positive; a second independent test
   changes it): how to read any accuracy number, benchmarks included (ep. 84).
3. **Fold into apA (timeline):** the method lineage the book leans on: Brooks
   1975 and "No Silver Bullet" 1986, XP 1999, Agile Manifesto 2001, DDD 2003,
   Bell's Law 1972 (verified dates).
4. **Optional (author's call): "Como estudar com a IA do lado"** (~2 pages):
   the three rules of "Aprendendo a aprender" (ep. 76: real problems, your
   own material, autonomy) applied to a learner with an agent, plus the
   fundamentals that don't age and "try alone before asking the machine". It
   serves the junior and the parent directly; the risk is a how-to tone. If
   not an appendix, it stays as touches 8, 27-29.
5. **Not recommended as appendices** (fold or skip): the owner's checklist
   from ep. 104 (fits as two bullets in the epilogue's "gestor" list), the
   learning-to-learn method (stays a touch in ch08 and the epilogue).

## D. Blog errata found (for the author)

- 2026/02/08 post: "por volta de 2014", "até o começo de 2024".
- Older episodes (not cited in the book where wrong): Nasdaq peak 2000 not
  2001 (#138); SPAC counts (#100); Google Reader 2005 (#84); Milgram's
  advisor Allport (#84); Dunning-Kruger 1999 (#64); "4 em 5" small businesses
  vs IBGE ~6 in 10 (#64); 56k modems in 1995 (#37); others in `factcheck.yml`.
