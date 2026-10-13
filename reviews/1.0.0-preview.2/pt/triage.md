# Triage: PT reader pass, 1.0.0-preview.2

Six reader reports (`part1-front.yml` … `part6-appendices.yml`), 175 items.
Item ids are `<part>.<n>`, n being the item's position in its file.
**Default: accepted as suggested.** Below: everything that is not a plain accept.

## Book-wide rulings (apply in every owned file)

- **OpenAI model names**: the blog is inconsistent; the book uses hyphen +
  capitalised tier: `GPT-5.5`, `GPT-5.4 Sol`, `GPT-5.6 Sol`, `GPT-5.6 Luna`,
  `GPT-5.6 Terra`, `GPT-6 Sol`, `GPT-6 Luna`, `GPT-6 Astra`. A tier alone is
  capitalised too ("o Sol", "o Terra"). (3.9, 4.7, 5.10, 6.19, 6.20)
- **Z.ai**, never "z.ai". (3.10)
- **sprint** is feminine ("a sprint"). (5.9)
- **Cross-references as subject or after "como/que/porque"** take the article:
  "o @sec-ch15 já fez", "como o @sec-ch02 mostrou". (3.7, 6.3–6.5)
- **Comparatives**: "mais/menos/pior/melhor … do que"; no conjugated verb after
  "do que" where a noun or infinitive works. (1.3, 1.6, 2.4, 2.5, 3.6, 4.6,
  5.4, 6.6–6.14)
- **"pra"** in narrative prose (not in quotations or titles). (1.9, 4.10)
- **No "não é X. É Y." rhetorical negation.** (6.15–6.17)

## Repetition between units: who keeps, who points back

| Material | Keeps the telling | Shortens to a callback |
|---|---|---|
| 1.279 sessões / três linhas (1.23, 4.11) | ch02 | ch16 |
| GPT-4o plan test, agent loop (1.24, 5.13, 5.15) | ch03 (and ch01 for GPT-4 size) | ch20 |
| Curva em S closing (5.14) | ch01 | ch20 (explicit callback) |
| DeepSeek-V3 cost asterisk (5.16) | ch19 | ch20 |
| ai-memory origin, tagline, 2.0/2.6.6 (5.17, 6.26, 6.27, 6.31) | ch20 | apB, apmemoria, apD |
| Production rule, snapshot "três da tarde", YOLO/VM lines (4.16, 6.28–6.30) | ch15 | apB (pointers; 4.16 wins over 6.28) |
| GLM 5.3 / DeepSeek V4.1 Flash September numbers (3.12) | ch11 | ch13 |
| Gemini cheating log (3.13) | ch11 | ch12 |
| Jev as classifier (3.14) | ch13 | ch14 |
| Five-fears map (1.21, 1.22) | prefácio | como-ler |
| Chapter-end hooks that pre-tell the next opening (1.25, 1.26, 2.23, 3.15, 4.12, 4.13, 5.18) | next unit | the hook (teaser only) |
| Interlúdio 2 news (4.14) | interlude2 | ch15 (retoma) |
| ch18 database example (5.21) | ch18 | epílogo |

## Verify against the source before editing

Fix from the source post (the paragraph's `src` marker, the post under
`~/Projects/akitaonrails-hugo/content/2026`). If the source doesn't settle it,
leave the text and record the item under "Author" below.

- 1.11 ch04 weighted vote example; 1.29 ch04 "uma leva de assinantes";
- 2.1 ch09 609 + 375 ("quase mil" if the numbers hold); 2.8 ch07 692 vs ch10 653
  commits; 2.10 ch06 percentages summing to 108% (chart script
  `assets/charts/`); 2.12 ch08 50 vs 262 lines; 2.15 FrankMD days; 2.17 five vs
  six times; 2.19 Frank Sherlock use; 2.21 test-line ratio; 2.7 ch06 broken
  sentence (restore the source's meaning);
- 3.4 ch13 "128 GB" for the 1-bit M3;
- 5.2 Stack Overflow (launched 2008: reword so the 2009 level isn't "o ano em
  que o site nasceu"); 5.8 ch19 120 people vs ch20 ~70 contributors (state
  each figure's population/date);
- 6.38 glossary `tipagem-forte` against ch18's usage.

## Rejected or deferred

- 1.10 rejected: "salto quântico" is the ordinary idiom; keep.
- 1.27 no change needed (as the reader concluded).
- 1.30, 2.32, 3.21, 4.23 rejected: pacing cuts of the author's material; left
  for the author's read.
- 5.30 and 2.11: resolved, see below.

## Resolved from the sources (after the first draft of this triage)

- **2.8** 692 vs 653 commits: two cuts of the same work. The 03/01 post counts
  4 projects including the newsletter repository (335 commits); the 03/05 post
  counts 8 projects but lists the private newsletter repository as "1+". ch07
  states its scope; ch10 now says the 653 excludes the newsletter history.
- **3.4** "1-bit" MiniMax M3 at ~128 GB: matches the 06/14 post's table and
  the Q4/Q3 sizes there (~4.9 and ~3.6 bits/param); dynamic "1-bit" quants keep
  sensitive layers at higher precision (~2.4 bits/param average). ch13 keeps
  128 GB and explains the name.
- **2.11** "mais de 25 anos" in ch08 is a critic's line quoted from the 04/23
  post ("25+ anos"); 30 (ch06, 02/20 post) is consistent with it. No change.
- **5.30** ai-memory section in ch20 kept: the author asked for ai-memory to be
  presented in the book.
- **2.17** "cinco vezes" (500% overclock) and "seis vezes" (frame budget) are
  two different measures in the source. No change.

## Blog errata (the book prints the correct figure)

- 2026/09/17 skills post: "609 PRs mergeados e 375 issues fechadas, mais de
  mil itens": the per-project lines add up to 984 ("quase mil").

## Outcome

Applied in book/pt (30 units, glossary-pt.yml) and the ch04 three-judges chart
(the Frank Investigator code sums confidence per verdict, so the example became
two models at 40% against one at 95%). `rake check build` (pt): 0 errors,
doctor warnings 27 -> 28 (the new one, ch20 -> ch19 "DeepSeek-V3", is a
heuristic false positive), page audit clean (466 print / 444 ebook pages),
epubcheck clean.
