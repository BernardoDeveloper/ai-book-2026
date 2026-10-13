# Triage: EN reader pass, 1.0.0-preview.2

Six reports (`part1-front.yml` … `part6-appendices.yml`), 208 items, read
after the EN edition was re-synced with the copyedited PT. Item ids are
`<part>.<n>`. **Default: accepted as suggested** (calques, grammar, unclear
sentences, glossary wording).

## Book-wide rulings

- **Quotation punctuation**: American style, periods and commas inside the
  closing quote; no period after a quoted question. Applied mechanically by
  `scripts/en_quote_punct.rb` to every EN unit (1.1, 1.4 and the `?".` cases).
- **"pull request" / "issue"**: use the glossary terms (with `.gls` on first
  use in a unit) instead of circumlocutions like "change request" or
  "complaints and suggestions" (5.2, 5.3).
- No Portuguese left in English prose unless it is the point (code comments,
  "and something similar in Portuguese", R$ amounts without a dollar
  equivalent, the Portuguese scam example glossed as such) (1.8, 2.x, 4.30,
  6.2, 6.40).

## Checked against the sources (editor), with PT changes

- 3.4 ch13 "the top of the table was tied": wrong in PT too (94 and 92.5 vs
  seven models at 100 in ch11). PT now: "Ficaram a poucos pontos dos sete
  modelos mais caros que empataram no topo."
- 3.17 ch13 GLM 4.7 Flash on the RTX 5090: 60 GB at 16-bit can't fit 32 GB;
  the 09/15 post ran it through llama-swap, so a quantized build. PT adds
  "numa versão quantizada que cabia na placa".
- 4.19 ch16 "a million lines": Andrew Kelley's own figure for the Rust
  result ("1 million lines of unreviewed slop", andrewkelley.me); the 535
  thousand is the Zig code. PT now attributes the number and says it is the
  Rust code.
- 5.15 ch18 "53 of 53 valid attempts": the 10/11 post says the 3 other
  attempts failed on infrastructure. PT now says so.
- 5.1 epilogue "cartaz" vs ch01 "cartão": PT fixed to "cartão"; EN "card".
- 3.14 ch12 digit run: the text is right (Qwen and DeepSeek both count 200;
  193 and 255 are summed distances, per the 09/30 post); the PT alt text now
  says "na distância somada de todos os textos".
- 6.8 apA: "23 de setembro" moved before the "Fim de setembro" entries in
  both editions.

## No change

- 2.3 (25 vs 30 years), 2.4 (five vs six times): settled in the PT pass
  (`../pt/triage.md`).
- 4.18 ch16 "about five days of work, between March 10 and 16": the 03/16
  post's own wording (working days); EN may say "about five working days".
- 1.18 ch03 "the rest of the year": fine as narrative time.
- 3.18 ch13 2-3 vs 2-8 tokens/s: two different situations (one model vs the
  general range).
- 3.30 interlude2 citation: Wang et al. do describe KataGo as superhuman.
- 5.30 ch19 "hundreds of people using it": users, not contributors.
- Pacing items (3.11, 4.31, 2.35) and structural repetition between chapters
  that the PT pass already handled: left for the author's read.
