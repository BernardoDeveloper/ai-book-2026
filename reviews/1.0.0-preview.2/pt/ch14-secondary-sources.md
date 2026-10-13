# ch14: claims resting on secondary coverage (REVIEW-1.0 item 4)

Checked 2026-10-13. Scope: the four claims flagged in `docs/REVIEW-1.0.md`
item 4. All four paragraphs carry
`<!-- src: 2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia -->`.
No book file was edited.

| # | Claim | Cite key | Verdict |
|---|-------|----------|---------|
| 1 | Sacks called the viral moment a "psychological operation" | `benzinga2026sacks` | Needs softening (small) |
| 2 | Pirate Wires report on the PR agency | `piratewires2026coxon` | Confirmed; add one clause for fairness |
| 3 | Musk "Dario is right" / Altman "pace the frontier" | `mediaite2026pace` | Confirmed |
| 4 | OpenAI's Navier-Stokes page | `openai2026navierstokes` (+ `kahn2026navierstokes`) | Confirmed |

Every primary source below was reached, either directly or through the
Wayback Machine or archive.today. Nothing is left unverifiable.

---

## 1. David Sacks and the "psyop" (ch14.md:167)

**Book:**

> David Sacks, que tinha sido o czar de IA da Casa Branca até março e seguia
> conselheiro do presidente, chamou a viralização de operação psicológica e
> apontou grupos de defesa da segurança de IA amplificando as postagens nos
> primeiros minutos [@benzinga2026sacks].

**Sources reached:**

- Benzinga (cited). Live URL returns 403 to plain clients. Wayback copies exist:
  https://web.archive.org/web/20260913145647/https://www.benzinga.com/markets/tech/26/09/61753920/david-sacks-jacob-coxon-anthropic-ai-safety
  The article never has Sacks saying "psyop". Its quotes are "calling him a
  whistleblower, but what evidence has he brought forward that we didn't
  have?" and "This is all just vibes from him." It reports that "He named
  three advocacy groups that he said helped spread the post within its first
  15 minutes". The word "Psyop" appears only in the embedded episode title.
  The visible headline is "David Sacks Slams 'Whistleblower' Jacob Coxon's
  Claims on AI Risk to Humans, Raises Questions Ahead of Anthropic IPO". "David
  Sacks Accuses Jacob Coxon of AI Safety Campaign", the title our reference
  uses, is only the HTML `<title>`.
  Side note: Benzinga says Sacks tied the groups to Dustin Moskovitz. In the
  episode he names Jaan Tallinn ("funded by Yan Talon" in the auto-captions),
  which matches the blog post. Ch14 doesn't make this claim, so nothing
  changes.
- **Primary: the All-In episode**, "AI Kills Everybody or Doomer Psyop?
  OpenAI's Math Breakthrough, Nike's $200B Collapse", uploaded 2026-09-12,
  https://www.youtube.com/watch?v=cvxjqbfLVk0 (I checked the YouTube
  auto-captions). Sacks's own words, from about 00:03:24:
  > "In fact, as Chamath was alluding to, this appears to be an op. How do we
  > know that? ... we also know who amplified it in the first 15 minutes. So
  > there were basically three of these well organized, well funded doomer
  > groups who amplified it ... This was something that was orchestrated."

  At about 00:28:33 he adds:
  > "it doesn't all have to be a conspiracy ... there was an organized PR
  > campaign here".

  In the captions, "psyop" itself (transcribed as "scop") comes from his
  co-hosts, not from Sacks.
- **Primary: Sacks on X**, 2026-09-13 03:14 UTC (evening of Sept 12 in the
  US), https://x.com/DavidSacks/status/2098973625252708460 (text read through
  the fxtwitter API; Wayback has a capture dated 20260913204739). This is
  where Sacks writes "psyop" himself, but about the labs' push to slow down,
  not about Coxon's posts:
  > "If you do, you'll buy goodwill for the next conversation. If you don't,
  > we'll know this was just another bid for regulatory capture — or an
  > election-season psyop."
- His title is confirmed by Axios, 2026-09-23 (Wayback 20260924025026). Sacks
  "spent Trump's first year as his AI czar" and now shapes policy "as co-chair
  of the president's science council". "Seguia conselheiro do presidente"
  holds.

**Verdict: needs softening.** The substance holds: he called it an "op", said
it was orchestrated, and named groups amplifying it in the first 15 minutes.
What the book can't support is "operação psicológica" as Sacks's own label for
the Coxon wave. On the podcast he said "an op". He used the word "psyop" in a
different post, about the slowdown pact. "Primeiros minutos" is fine, though
"primeiros 15 minutos" is more precise.

**Proposed PT (minimal edit):**

> David Sacks, que tinha sido o czar de IA da Casa Branca até março e seguia
> conselheiro do presidente, foi ao podcast All-In dizer que aquilo parecia
> "uma operação" orquestrada e apontou três grupos de defesa da segurança de
> IA amplificando as postagens nos primeiros 15 minutos [@allin2026psyop].

**Optional version** that keeps the "psyop" word with its real target. It fits
better at the end of the "Desacelerar, mas nem tanto" section, after the
Musk/Altman paragraph:

> Dias depois, quando o Dario pediu pra desacelerar, o Sacks respondeu no X
> que, se os laboratórios não freassem por conta própria, ficaria claro que
> era só mais uma tentativa de captura regulatória "ou uma psyop de época de
> eleição" [@sacks2026pace].

**CSL-YAML.** Add the primary source. Keep `benzinga2026sacks` or replace it.

```yaml
- id: allin2026psyop
  type: broadcast
  title: AI Kills Everybody or Doomer Psyop? OpenAI's Math Breakthrough, Nike's $200B Collapse
  author:
  - literal: All-In Podcast
  container-title: YouTube
  issued:
    date-parts:
    - - 2026
      - 9
      - 12
  URL: https://www.youtube.com/watch?v=cvxjqbfLVk0
  accessed:
    date-parts:
    - - 2026
      - 10
      - 13
  note: 'cited-by: 2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia (Sacks segment at ~00:03:20)'
- id: sacks2026pace
  type: post
  title: Dario has written that we need to "pace the frontier," and Sam has agreed
  author:
  - family: Sacks
    given: David
  container-title: X
  issued:
    date-parts:
    - - 2026
      - 9
      - 12
  URL: https://x.com/DavidSacks/status/2098973625252708460
  accessed:
    date-parts:
    - - 2026
      - 10
      - 13
  note: 'cited-by: 2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia (posted 2026-09-13 03:14 UTC). Arquivado em: https://web.archive.org/web/20260913204739/https://x.com/DavidSacks/status/2098973625252708460'
```

If `benzinga2026sacks` stays, fix its fields:

```yaml
  title: David Sacks Slams 'Whistleblower' Jacob Coxon's Claims on AI Risk to Humans, Raises Questions Ahead of Anthropic IPO
  note: 'cited-by: 2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia. Arquivado em: https://web.archive.org/web/20260913145647/https://www.benzinga.com/markets/tech/26/09/61753920/david-sacks-jacob-coxon-anthropic-ai-safety'
```

---

## 2. Pirate Wires report (ch14.md:167)

**Book:**

> A Pirate Wires noticiou um e-mail de 9 de setembro, um dia depois das
> postagens, em que uma agência de comunicação já tentava marcar entrevistas
> pra ele, enquanto Coxon tinha dito na TV que não trabalhou com terceiros
> [@piratewires2026coxon]. A própria reportagem não estabelece quando essa
> relação começou.

**Primary reached:** the live URL returns HTTP 429. I read the article through
archive.today
(https://archive.ph/20260925223525/https://www.piratewires.com/p/jacob-coxon-worked-with-ai-doomer-firm)
and Wayback
(https://web.archive.org/web/20261002014046/https://www.piratewires.com/p/jacob-coxon-worked-with-ai-doomer-firm?ref=cybernauterne.dk).
It is "EXCLUSIVE: Jacob Coxon Worked With Doomer PR Firm" by Hunter Ryerson,
dated Sep 24, 2026. Key passages:

> "DEY. Ideas + Influence, a communications firm associated with prominent AI
> safetyists, has been working for Jacob, according to two people familiar with
> the matter as well as an email seen by Pirate Wires in which DEY. was looking
> to book Jacob for an interview on September 9."

> "'Did you work with any third parties as far as this whistleblowing and
> coming out?' he [Bret Baier] asked Jacob on-air on September 9. 'Not at
> all,' Jacob said."

> "We don't know when, exactly, Jacob's relationship with DEY. began. After
> publication, Nate said he introduced them when Jacob's initial post passed
> 100,000 likes, which would've been within 24 hours."

**Verdict: confirmed.** Every element in the book matches: the Sept 9 email,
the agency trying to book interviews, the on-air denial, and the report not
establishing when the relationship began.

One gap is worth closing. The updated article quotes Nate Soares (MIRI) saying
he introduced Coxon to the agency only after the post went viral. Leaving that
out makes the email read as evidence of advance coordination. Including it fits
the next paragraph ("Nada disso prova coordenação") and protects the book
against a fairness complaint.

**Proposed PT (replace the last sentence):**

> A própria reportagem não estabelece quando essa relação começou. Depois que
> ela saiu, Nate Soares, do MIRI, disse que apresentou o Coxon à agência
> quando o primeiro post passou de 100 mil curtidas, ou seja, com a
> viralização já em andamento.

**CSL-YAML (replace the existing fields):**

```yaml
- id: piratewires2026coxon
  type: article-newspaper
  title: 'EXCLUSIVE: Jacob Coxon Worked With Doomer PR Firm'
  author:
  - family: Ryerson
    given: Hunter
  container-title: Pirate Wires
  issued:
    date-parts:
    - - 2026
      - 9
      - 24
  URL: https://www.piratewires.com/p/jacob-coxon-worked-with-ai-doomer-firm
  accessed:
    date-parts:
    - - 2026
      - 10
      - 13
  note: 'cited-by: 2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia (live page rate-limited; read via archive). Arquivado em: https://archive.ph/20260925223525/https://www.piratewires.com/p/jacob-coxon-worked-with-ai-doomer-firm'
```

(The blog's update note dates the report 25/9. The article itself says Sep 24,
and archive.today captured it on 25/9 at 22:35 UTC. The book doesn't give a
date, so no text change is needed.)

---

## 3. Musk and Altman replies (ch14.md:176)

**Book:**

> No mesmo dia, Elon Musk escreveu "o Dario está certo" e Sam Altman disse
> concordar que era preciso dosar o ritmo da fronteira [@mediaite2026pace].

**Primaries reached.** I read the post texts through the fxtwitter API and
derived the times from the status IDs:

- Dario Amodei's post: https://x.com/DarioAmodei/status/2098773920774074715,
  2026-09-12 14:01 UTC.
- Musk, quoting Dario: https://x.com/elonmusk/status/2098789109980332057,
  2026-09-12 15:01 UTC. Text: "Dario is right". Wayback:
  https://web.archive.org/web/20261011091026/https://x.com/elonmusk/status/2098789109980332057
- Altman, quoting Dario: https://x.com/sama/status/2098811563415150910,
  2026-09-12 16:30 UTC. Text: "I agree with Dario that we need to pace the
  frontier. This has been a primary topic of discussions we've had at OpenAI in
  recent weeks. Committing to having independent evaluators with
  employee-like access is a great idea, and we will do the same. We'll have
  more to share soon." No Wayback capture exists.
- Mediaite (cited). The live URL returns 403. Wayback:
  https://web.archive.org/web/20260918012044/https://www.mediaite.com/media/elon-musk-and-sam-altman-agree-with-anthropic-boss-ai-must-slow-down-to-avoid-catastrophic-damage/
  It is by Sean James, Sep 12th 2026, and embeds both posts.

**Verdict: confirmed.** "No mesmo dia" is correct: all three posts went up
within 2.5 hours on Sept 12. The blog post's "no dia seguinte" is wrong, and
the book already corrected it. No text change needed.

**CSL-YAML.** Optionally cite the posts directly, and add author and archive to
Mediaite:

```yaml
- id: musk2026dario
  type: post
  title: Dario is right
  author:
  - family: Musk
    given: Elon
  container-title: X
  issued:
    date-parts:
    - - 2026
      - 9
      - 12
  URL: https://x.com/elonmusk/status/2098789109980332057
  note: 'cited-by: 2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia. Arquivado em: https://web.archive.org/web/20261011091026/https://x.com/elonmusk/status/2098789109980332057'
- id: altman2026pace
  type: post
  title: I agree with Dario that we need to pace the frontier
  author:
  - family: Altman
    given: Sam
  container-title: X
  issued:
    date-parts:
    - - 2026
      - 9
      - 12
  URL: https://x.com/sama/status/2098811563415150910
  note: 'cited-by: 2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia'
```

For `mediaite2026pace`, replace `author: literal: Mediaite` with
`author: [{family: James, given: Sean}]` and add
`note: '... Arquivado em: https://web.archive.org/web/20260918012044/https://www.mediaite.com/media/elon-musk-and-sam-altman-agree-with-anthropic-boss-ai-must-slow-down-to-avoid-catastrophic-damage/'`.

---

## 4. OpenAI's Navier-Stokes page (ch14.md:120 and 122; also apA.md:359)

**Book:**

> Em 8 de setembro, a OpenAI anunciou ter resolvido o problema
> [@openai2026navierstokes]. O detalhe que a manchete escondia: a prova trata
> da versão em que uma força externa suave empurra o fluido, uma das rotas
> aceitas no enunciado oficial, enquanto a pergunta famosa, sem força externa,
> continua aberta. Pra chegar lá, a empresa rodou uns 10 mil agentes em
> paralelo durante 88 horas, gastando uns 130 bilhões de tokens de saída só
> nesse problema e uns 300 bilhões na campanha inteira [...] A OpenAI disse a
> jornalistas que usou pelo menos mil vezes a computação [...] uns 2 milhões,
> e outras estimativas na imprensa passaram de 20 milhões
> [@kahn2026navierstokes].
> ... a OpenAI tinha avisado que não iria buscar o prêmio.

**Primary reached:** the live URL returns 403. Wayback copy:
https://web.archive.org/web/20261011143311/https://openai.com/index/navier-stokes-solution/
The page is titled "On the Navier–Stokes Millennium Prize Problem", dated
September 8, 2026, and carries an update dated September 10. The relevant
passages:

> "This resolves the Navier–Stokes Millennium Prize problem by establishing
> statement 'C' (and also 'D') in the official Millennium Prize formulation."

> "The fluid has a smooth force applied to it, and its energy remains finite
> through the entire dynamics"

> "the group that produced the Navier–Stokes resolution involved on the order
> of 10,000 concurrent agents"

> "The agents arrived at their resolution on Saturday, September 5, about 88
> hours after the first agents were launched."

> "Across all attempted problems, the agents sent 4.9 million messages and used
> about 300 billion output tokens. In the process of resolving the
> Navier–Stokes problem, the agents sent 2.7 million messages and used
> approximately 130 billion output tokens."

> "We do not intend to claim the Millennium Prize for this result."

The compute figures come from Fortune (`kahn2026navierstokes`), which I fetched
live (HTTP 200):

> "OpenAI told reporters in a briefing today that it had used computing
> resources that were at least 1,000 times greater than what it had used to
> solve some previous mathematical challenges for which it had used about
> $2,000 worth of compute—so that would be about $2 million—although other
> reports put the number at 10 times greater still, at $22.5 million"

**Verdict: confirmed.** Every figure and the forced-version framing match the
primary. "A pergunta famosa, sem força externa, continua aberta" is the book's
inference. The OpenAI page doesn't say it, but it follows from the C/D framing
and the Clay note already cited in the next paragraph. Keep it as is. The
compute and price figures are correctly attributed to Fortune, not to the
OpenAI page. No text change needed.

**CSL-YAML (fix the title, add the archive):**

```yaml
- id: openai2026navierstokes
  type: webpage
  title: On the Navier–Stokes Millennium Prize Problem
  author:
  - literal: OpenAI
  container-title: OpenAI
  issued:
    date-parts:
    - - 2026
      - 9
      - 8
  URL: https://openai.com/index/navier-stokes-solution/
  accessed:
    date-parts:
    - - 2026
      - 10
      - 13
  note: 'cited-by: 2026/09/09/propagandas-enganosas-da-openai-anthropic-nvidia (live page 403 to non-browser clients; updated by OpenAI 2026-09-10). Arquivado em: https://web.archive.org/web/20261011143311/https://openai.com/index/navier-stokes-solution/'
```

---

## Follow-ups if the author approves

- Apply the edits for items 1 and 2 to `book/pt/ch14.md:167`, then mirror them
  in `book/en/ch14.md:168` after PT approval.
- Update `references.yaml` as above, and refresh the matching rows in
  `docs/research/LINKCHECK.md` (they record mediaite 403, openai 403 and
  piratewires 429; archive copies now exist for all three).
- Optional: fix the blog post's "no dia seguinte ao ensaio do Dario" (line 188)
  and its 25/09 date for the Pirate Wires report, which was published 24/09.
  These are blog edits, so they're the author's call.
