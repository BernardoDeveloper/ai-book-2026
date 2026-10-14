# The narrator's history (Akitando era, 2018-2023)

A lens for the first-person voice of the book, drawn from 22 Akitando posts
(`extract-*.yml` in this folder; facts checked in `factcheck.yml`). The book
stays an AI book: this history colors how the narrator speaks and backs his
2026 claims with lived experience. It does not add chapters.

## Who is speaking

Confirmed by the author (2026-10-14) unless marked otherwise:

- **Born in 1977; programming since 1990**, at 13, after a Basic course
  (MBasic), then dBase, Clipper, UNIX, learned by doing, not by career plan
  (ep. 61).
- **Computer science at USP (São Paulo), entered in 1995.** Don't state a
  degree (ep. 90 says he didn't finish; the author didn't say otherwise).
- **Late 1990s to early 2000s: advertising agencies and dot-com startups.**
  Learned about ten stacks between 1996 and 2001 without calling himself
  "programador ASP"; the companies of that period closed in the crash; one
  week unemployed (ep. 138).
- **2001-2006: SAP-based consultancy** (ep. 34, Dec 2018, "Você não sabe nada
  de enterprise"). His dot-com (sports sites for Latin America) closed in the
  2001 crash; the same week a mentor called him into a small SAP consultancy
  that needed someone who knew web technologies. About five years as an
  integrator (not a functional consultant), certified in SAP Enterprise
  Portals / NetWeaver, across sales, materials, projects, finance and HR
  modules in large companies (client names stay out of the book). His lesson:
  "nenhum programador tem como saber as regras de negócio de grandes empresas
  sem ter passado por elas"; the processes he later used in his own company
  came from there. Strongest hook: the private domain knowledge that never
  reaches a model's training (ch20 "mapa em branco", epilogue "O seu
  domínio", ch18 office/management examples, ch19 companies).
- **2007: moved to Ruby on Rails, freelancing and open-source communities**
  when there was barely a market for it (ep. 29 places the first interest in
  2005-2006; the move was 2007).
- **Organized RubyConf Brasil from 2008 to 2016** (up to about 1,200
  attendees), then two years of a smaller English-only conference, The Conf.
- **Founded Codeminer 42 in 2011**, still running, with clients in the US and
  Brazil.
- **Akitando, August 2018 to December 2023, 149 episodes** (YouTube channel
  and blog transcripts), most watched in the pandemic years.
- **Called the hiring bubble on video, with dates**: June 2019 (ep. 50, "a
  bolha de startups vai estourar"), February 2020 (ep. 72, before the
  pandemic: when it bursts, whoever doesn't deliver results loses the job),
  June 2021 (ep. 100), November 2022 (ep. 132, "estourou"). He also got a call
  wrong: in late 2022 he expected 2023 to be "um ano perdido" with a second
  leg of the crash; the AI wave lifted the market instead. The honest line is
  part of the voice: "avisei da bolha, errei o calendário".
- **Taught the long-lasting stuff on purpose**: Akitando (2018-2023, 149
  episodes) was a response to the bootcamp promise of easy money; it taught
  computer science fundamentals, markets, management and startups, "o
  conhecimento que sobrevive a crash e bolha".
- **Methods are decades old for him**: *The Mythical Man-Month* as "o melhor
  livro de software" (ep. 23), "Esqueça metodologias ágeis" (ep. 51, 2019),
  emergent design (ep. 106), tests/CI/estimation as order of magnitude
  (ep. 130, 2022), modeling a domain you know (ep. 144). The 2026 agent methods
  (small steps, tests as the judge, CI, rollback, deciding at the right time)
  are the same practices with a new tool.
- **Myth-busting is a trait**: "Não terceirize suas decisões" (ep. 63, 2019,
  his most known episode); "a quem essa mensagem beneficia?" (ep. 84, 2020);
  "empreendedorismo de palco" (ep. 52, 2019); "programação não é fácil"
  (ep. 72, 2020).

## Recurring positions (use his words, sparingly)

- "Não terceirize suas decisões": 100% of the merit and of the loss is yours.
- Seniority is deciding and owning the decision; junior, mid and senior solve
  the same problem, the difference is time and how many wrong attempts you can
  cut (ep. 64).
- The programmer was never the factory worker: the compiler is; the
  programmer was always the architect (ep. 120, June 2022, before ChatGPT).
- Fundamentals (algorithms, data structures, statistics) separate a career
  from a course; with them a new language takes weeks (ep. 65, ep. 90).
- Quantity of evidence is not quality of evidence (ep. 84); likes don't make
  a thing true (ep. 63).
- "O júnior de hoje é o sênior de amanhã": teams need juniors (ep. 104,
  ep. 120).
- Bubbles burst, technologies stay; follow the money (zero interest rates,
  free cash flow vs. stock compensation) (ep. 50, 100, 132).

## How to use it in the book (rules for drafting)

- **Sparingly.** About 25 touches in the whole book, one or two per chapter
  where the history is the evidence: never a recap of the channel, never a
  list of episodes.
- **Not every touch cites an episode.** Most are voice ("já vi isso na bolha
  de 2000"); cite the episode (title and year, linked in the bibliography) only
  where a dated warning or a direct quote is the point.
- **No showing off.** Round-1 readers distrusted lines that sounded like the
  author displaying volume or success; experience is offered as evidence or
  counsel, and failures and wrong calls are told too.
- **Facts are checked.** World facts from the transcripts (dates, numbers,
  companies) go in only as verified in `factcheck.yml`; bio facts the author
  hasn't confirmed are framed as memory or left out. No client names, no
  private finances, nothing about piracy.
- **Provenance.** Each touch carries `<!-- src: <yyyy/mm/dd/akitando-...> -->`;
  these posts are registered as background sources (allowed before the
  February 2026 cut-off) so drift tracks them.
