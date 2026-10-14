# Akitando extraction brief

Context: the book (book/pt/, outline in book/outline.yml) is Fabio Akita's AI book built from his 2026 posts. The author wants the first-person narrator colored with his longer history from the Akitando era (YouTube channel 2018-2023, posts in ~/Projects/akitaonrails-hugo/content/<yyyy>/<mm>/<dd>/<slug>/index.md). NOT new chapters: short touches (a sentence, a short paragraph, a brief quote) where the narrator's experience backs a 2026 claim. The book's thesis: AI is a tool; the career doesn't end; bubbles and hype pass; deciding, checking and the fundamentals stay.

Read your assigned posts IN FULL (they are transcripts of videos; long). Then write reviews/akitando/extract-<group>.yml with:

```yaml
posts:
  - id: 2019/10/09/akitando-63-nao-terceirize-suas-decisoes-a-licao-mais-importante-da-sua-vida
    title: "..."
    one_line: "what the episode argues, one sentence"
    bio_facts:            # facts about the author's life/career stated in the post
      - claim: "..."      # e.g. "started programming at 13 in 1990"
        quote: "verbatim PT excerpt, short"
        check: "what would verify it (dates, names, public records) or 'author memory, frame as such'"
    world_facts:          # claims about the world (bubble dates, layoffs, market numbers, companies)
      - claim: "..."
        quote: "..."
        check: "what source would verify it"
    positions:            # the author's stances that recur, in his words
      - stance: "..."
        quote: "verbatim, max ~40 words, the most quotable line"
    book_hooks:           # where in THIS book (unit id + section or the claim it supports) a touch fits
      - unit: ch18
        where: "section heading or the claim in the 2026 text"
        touch: "what one or two sentences would add (in Portuguese, Akita's voice), citing the episode"
        strength: high|medium|low
    appendix_candidate: "optional: a subject that could become a short appendix (why it would serve the AI book's reader), or empty"
```

Be selective: the best 3-6 bio facts, positions and hooks per post, not everything. Quotes must be verbatim from the post (validate by grep). Prefer hooks that give the 2026 text authority from lived experience (bubbles called early, methods learned over decades, career counsel, "não terceirize suas decisões", debunking hype). Don't invent; if a claim in the post looks wrong or dated (e.g. a date or number), say so in `check`.
Validate YAML with ruby -ryaml. Reply with a short summary: the 5 strongest hooks and any appendix candidates.
