# Book voice: from blog post to book chapter

This guide is a derivative of the blog's own rules. Everything in
`~/Projects/akitaonrails-hugo/WRITER.md` (voice section) and the `akita-finish`
and `humanizer` skills still applies, in full. Read them first. This file only
covers what changes when the text moves from a dated blog post to a book that a
lay reader holds in their hands.

## Who is reading

Someone curious about AI who is anxious or confused by the propaganda: a
professional afraid of being replaced, a parent who read that "AGI is two years
away", a manager being sold an AI transformation, a junior developer wondering if
the career is over. Most are not programmers. They are smart, busy, and have
been lied to by marketing. The book's job is to give them footing: how the thing
works, what it does well, where it fails, and how to tell a real claim from a
sales pitch.

Two consequences:

- **Aim the edge at the propaganda, never at the reader.** Akita's bluntness
  stays, and vendors, hype merchants and snake-oil sellers still get called what
  they are. A reader who believed the ads is the person we are trying to help;
  the text never calls them an idiot. (The blog title "Você é um idiota se
  acredita..." becomes a chapter about how the ads work.)
- **Explain before you use.** Every technical term gets a one-clause plain
  explanation on first use in the book (not per chapter), then a glossary entry.
  Mark the first use with `[termo]{.gls}` so the build can link it.

## Scope: intuitions, not textbook mechanics

The book does not teach how neural networks learn (gradient descent,
backpropagation), embeddings math, transformer/attention internals, or how
pretraining and RLHF work. It gives intuitions where the story needs them
(ch01) and the front-matter section "Antes de começar" (`@sec-antes`) tells
the reader this up front and recommends credible books to learn the
mechanisms. When a chapter brushes against one of those mechanisms, give the
one-line intuition and, if useful, point to `@sec-antes`; never drift into a
textbook explanation.

## Narrative, not encyclopedia

The book reads like a nonfiction story told in first person: one experienced
programmer spends 2026 putting AI through the wringer and reports what he found.
The year is the spine. Information arrives because the story needs it, at the
moment the reader wants it.

- **Open each chapter on a scene.** A date, a place, a concrete situation with
  stakes: the night the agent nearly deleted a folder, the 37th day of the
  vibe-coding marathon, the benchmark run where a model "won" by cheating. Never
  open with a definition or a thesis statement.
- **Tension before explanation.** Pose the question the reader is already
  carrying ("will this replace me?", "why did it lie?") and let the chapter earn
  the answer through what happened. Explanations come in the middle, as the
  thing that resolves the scene.
- **Characters.** Akita is the narrator. Recurring characters are the tools and
  models (introduced like people, with their quirks), the "Frank" projects, and
  real public figures when they matter. Keep them consistent across chapters.
- **Close on a forward hook.** The last paragraph opens the next door: a
  question left hanging, the next problem that appeared. No "summary box", no
  "neste capítulo vimos". A single takeaway blockquote inside the chapter, where
  the insight lands, does that job better.
- **Interludes.** Short pieces (2 to 4 pages) between parts, lighter in tone: a
  rant, an anecdote, a single surprising experiment. They give the reader a
  breather and keep the rhythm uneven, as a real book is.
- **Show the evidence, not the logs.** One well-chosen number or a short excerpt
  of what the model said beats a table of 39 models. Big tables move to an
  appendix or get cut; prose keeps the picture ("o dobro", "um erro a cada 40").

## Blog-to-book conversions (mechanical rules)

| Blog habit | In the book |
|---|---|
| Inline hyperlink to an external source | Citation `[@key]` resolved to the bibliography; the sentence must stand without the link |
| Link to another of Akita's posts | Cross-reference to the chapter that now covers it (`[capítulo](#sec-id)`), or drop it; never a URL |
| "Neste post", "no artigo de ontem", "atualização:", "como falei no vídeo" | Rewrite for a book; videos and podcasts become bibliography entries |
| "Hoje", "ontem", "semana passada", "recentemente" | Absolute time: "em março de 2026". The book is read in 2028 too |
| Model versions, prices, scores | Kept as a dated snapshot, framed as such ("em setembro de 2026, o melhor..."); when a later post superseded it, tell the story of the change rather than printing the stale number as current |
| Code dumps, install steps, config files | Cut. Keep at most a 3 to 8 line excerpt when the code itself is the point. Practical how-tos go to an appendix with a pointer |
| Screenshots of terminals/UIs | Replace with a described scene, a redrawn figure, or drop |
| Headings as SEO titles ("Vibe Code: Fiz X em 2 dias") | Chapter titles are literary and short; the subject goes in the subtitle |
| Repetition across posts (same thesis, many angles) | Say it once, well, at the right moment; later chapters build on it instead of restating it |
| Calls to action, self-promotion, "assine", "comente" | Cut |
| Private repos | Same rule as the blog: never named or linked |

## Superseded content

Posts were written over ten months, and Akita changed his mind, updated tools,
and reran benchmarks. The book reflects the latest position as of its cut-off
date, and treats the change itself as story when the change is instructive ("em
janeiro eu achava X; em julho os números diziam Y"). Never print an obsolete
ranking or tool behaviour as if it were current. `inventory/lineage.yml` records
which post supersedes which; drafters must check it.

## Language specifics (PT-BR edition)

- Brazilian Portuguese, Akita's register: informal ("pra", "tá", "a gente" are
  fine in moderation), technical terms in English when that is how Brazilian
  programmers say them (LLM, prompt, token, harness), each explained once.
- A book tolerates slightly more connective tissue than a blog post, so a scene
  can run several short paragraphs. The 4-sentence paragraph ceiling stays.
- Numbers follow akita-finish: PT-BR decimal comma, rounded in prose.
- No em dashes or en dashes, no curly quotes in the source (the typesetter makes
  quotes typographic).

## Provenance markers in chapter sources

Every chapter file starts with YAML front matter listing the posts it draws from
(id + sha256 at drafting time) and any reference-project files. Inside the text,
a paragraph or block derived from a specific post is preceded by
`<!-- src: 2026/MM/DD/slug -->`. New material written for the book (bridges,
preface, explanations) is marked `<!-- src: original -->`, and material checked
against a reference project is marked `<!-- src: ref:<project>/<path> -->`.
These comments are stripped at build time. They are how a blog edit gets traced
to the exact paragraphs that need revisiting.

## Finishing pipeline per chapter

1. Draft from the outline brief, the analyses and the original posts.
2. Fact-check new or changed claims (the `fact-check` skill's checker prompt).
3. `humanizer` pass.
4. `akita-finish` pass, adapted: skip "keep every inline link" (links became
   citations), keep everything else.
5. `scripts/lint_chapter.rb`: dashes, banned phrases, paragraph length,
   leftover URLs, unknown citation keys, missing provenance markers.
