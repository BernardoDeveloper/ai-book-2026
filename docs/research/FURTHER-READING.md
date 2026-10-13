# Leituras prévias: como funcionam redes neurais e LLMs

Research for the front-matter note ("antes de começar") that tells readers the book
does not teach the mechanisms (neural networks, gradient descent, backpropagation,
embeddings, transformers/attention, pretraining/RLHF) and points them to where they
can learn those basics first.

- Researched: 2026-10-13. Every claim below was checked against the source linked
  next to it (publisher page, author site, official repo, or a bookstore page when
  no publisher page carried the detail). Where a fact could not be confirmed, the
  table says so.
- Rule followed: no Portuguese edition is listed unless a publisher or bookstore page
  shows it. "No PT edition found" means none was found on the publisher's own
  translations list (when it has one) or in searches of Brazilian/Portuguese stores.
- CSL entries for the short list live in `book/pt/_refs/antes.yaml`.

## Recommended short list

Three tiers. Tier 1 needs no math. Tier 2 has some high-school math. Tier 3 needs
Python. Items marked FREE are legally online at no cost; PT means a Portuguese
edition or translation exists.

### Tier 1: no math (a total beginner can start here)

| # | Work | PT | Free | Why |
|---|------|----|------|-----|
| 1 | Timothy B. Lee & Sean Trott, "Grandes modelos de linguagem, explicados com o mínimo de matemática e jargão" (2023; PT translation 2024) `[@lee2024modelos]` | **Yes** (official PT translation on the authors' site) | **Yes** | The shortest honest path through word vectors, attention, feed-forward layers and next-word training, in Portuguese, no equations. |
| 2 | Melanie Mitchell, *Artificial Intelligence: A Guide for Thinking Humans* (FSG, 2019) `[@mitchell2019guide]` | No | No | A working AI researcher explains how neural networks learn and where they fail, explicitly against hype. Pre-dates ChatGPT, so pair it with #1 or #3. |
| 3 | Stephen Wolfram, *What Is ChatGPT Doing ... and Why Does It Work?* (Wolfram Media, 2023) `[@wolfram2023chatgpt]` | **Yes**, PT-PT: *O Que Faz o ChatGPT e Como Funciona* (Casa das Letras, 2023) | **Yes** (the full essay is on his site) | Walks from "predict the next word" through embeddings, neural nets, training and transformers with pictures, aimed at a curious non-specialist. |
| 4 | John D. Kelleher, *Deep Learning* (MIT Press Essential Knowledge, 2019) `[@kelleher2019deep]` | No | No | Pocket-size and conceptual, yet it actually explains gradient descent and backpropagation; the bridge from tier 1 to tier 2. |

### Tier 2: some math, free online

| # | Work | PT | Free | Why |
|---|------|----|------|-----|
| 5 | Michael Nielsen, *Neural Networks and Deep Learning* (Determination Press, 2015) `[@nielsen2015neural]` | No | **Yes** | The classic gentle derivation of a neural network, gradient descent and backpropagation, built around one digit-recognition example. Stops before transformers. |
| 6 | François Fleuret, *The Little Book of Deep Learning* (2023; v1.3, 2026) `[@fleuret2023little]` | No | **Yes** (PDF, CC BY-NC-SA) | Under 200 phone-sized pages (189 in v1.3) covering everything from training to attention and transformers; dense, but the most compact complete map. |
| 7 | Simon J. D. Prince, *Understanding Deep Learning* (MIT Press, 2023) `[@prince2023understanding]` | No | **Yes** (PDF, updated 2026) | A carefully illustrated modern textbook covering training, transformers and generative models, with figures and Python notebooks. Use it as the reference after #5 or #6. |

### Tier 3: hands-on (Python)

| # | Work | PT | Free | Why |
|---|------|----|------|-----|
| 8 | Sebastian Raschka, *Build a Large Language Model (From Scratch)* (Manning, 2024) `[@raschka2024build]` | No | No (code is free on GitHub) | Builds a GPT-style model step by step: tokenizer, embeddings, attention, pretraining, fine-tuning. Nothing stays a black box. |
| 9 | Jay Alammar & Maarten Grootendorst, *Hands-On Large Language Models* (O'Reilly, 2024) `[@alammar2024handson]` | **Yes**, AI-assisted: *Modelos de linguagem grandes e práticos* (O'Reilly, 2025) | No | Almost 300 original illustrations of tokens, embeddings and attention, then practical use of pretrained models. |

### Companions (video and illustrated web pages)

| Work | PT | Free | Why |
|------|----|------|-----|
| 3Blue1Brown (Grant Sanderson), "Neural networks" / "Deep Learning" series, chapters 1-7 (2017-2024) `[@sanderson2017neural]` | Partly: PT-BR dubbed audio on the transformer chapters and on "LLMs explained briefly"; PT-BR subtitles on chapter 1 | **Yes** | The clearest visual explanation of neurons, gradient descent, backprop, embeddings and attention. A total beginner can watch chapters 1, 5 and "LLMs explained briefly". |
| Andrej Karpathy, "[1hr Talk] Intro to Large Language Models" (2023) `[@karpathy2023intro]` and "Deep Dive into LLMs like ChatGPT" (2025) `[@karpathy2025deepdive]` | No (YouTube auto-translated captions only) | **Yes** | A builder of GPT-class models explains pretraining, fine-tuning and RLHF to a general audience. |
| Andrej Karpathy, "Neural Networks: Zero to Hero" (2022-) `[@karpathy2022zerotohero]` | No | **Yes** | Tier-3 companion: writes backprop and a small GPT live in Python. Needs solid Python. |
| Jay Alammar, "The Illustrated Transformer" (2018) `[@alammar2018illustrated]` | No PT translation listed (11 other languages are) | **Yes** | The diagram set most people learned transformers from; chapter 3 of #9 is its updated version. |

Beginner coverage: #1, #2, #3 and the 3Blue1Brown videos need no math. Free: #1, #3,
#5, #6, #7 and all companions. In Portuguese: #1 (PT-BR), #3 (PT-PT), #9 (AI-assisted).

## Full verification table

Level: L = lay, I = intermediate, T = technical/hands-on.

| Work | Authors | Publisher, year (latest ed.) | Free / where | Portuguese edition | Lvl | Verdict |
|------|---------|------------------------------|--------------|--------------------|-----|---------|
| *Artificial Intelligence: A Guide for Thinking Humans* | Melanie Mitchell | Farrar, Straus and Giroux, 2019 (UK: Pelican, 2020; Picador pb) | No | **None found.** Author's page lists Chinese, Japanese, Spanish, French, Italian, Russian only. Spanish: *Inteligencia artificial. Guía para seres pensantes* (Capitán Swing, 2024). | L | Short list |
| *What Is ChatGPT Doing ... and Why Does It Work?* | Stephen Wolfram | Wolfram Media, 2023 (print ISBN 978-1-57955-081-3; ebook 978-1-57955-082-0) | Yes: full essay at writings.stephenwolfram.com (14 Feb 2023) | **Yes (PT-PT):** *O Que Faz o ChatGPT e Como Funciona*, Casa das Letras, Aug 2023, 144 pp., ISBN 978-989-661-831-5; ebook ISBN 978-989-661-832-2. No Brazilian edition found. | L | Short list |
| "Large language models, explained with a minimum of math and jargon" | Timothy B. Lee, Sean Trott | Understanding AI (newsletter), 27 Jul 2023 | Yes | **Yes (PT-BR):** "Grandes modelos de linguagem, explicados com o mínimo de matemática e jargão", 15 Apr 2024, translated by Carlos Dutra, reviewed by Gabriel Adriano de Melo, on understandingai.org | L | Short list (added) |
| *Deep Learning* (Essential Knowledge) | John D. Kelleher | MIT Press, 2019, ISBN 978-0-262-53755-1; no revised edition found | No | **None found** (an English audiobook is sold on audible.com.br) | L/I | Short list |
| *AI Snake Oil* | Arvind Narayanan, Sayash Kapoor | Princeton University Press, 2024; paperback with new preface and epilogue 23 Sep 2025 (ISBN 978-0-691-24914-8) | No | **None found** (Wook.pt sells only the English edition) | L | Table only: excellent against hype, but it is about what AI can and cannot do, not how it works. Good for a different note. |
| *A Brief History of Intelligence* | Max S. Bennett | Mariner Books, 2023 | No | **Yes (PT-BR):** *Uma Breve História da Inteligência: Evolução, IA e os cinco avanços que nosso cérebro fez*, Alta Cult (Alta Books), Rio de Janeiro, 2024, 432 pp., ISBN 978-85-508-2426-0, trans. Eveline Machado. Ebook not confirmed. | L | Table only: credible and in PT, but it is about brain evolution with AI comparisons, not about how neural nets or LLMs work. |
| *Why Machines Learn: The Elegant Math Behind Modern AI* | Anil Ananthaswamy | Dutton, 2024 (paperback adds an afterword on transformers) | No | **None found** | I | Table only: good math-history route; Publishers Weekly found it hard for general readers. |
| *Inteligência Artificial* (Ensaios da Fundação n.º 90) | Arlindo Oliveira (IST, Lisbon) | Fundação Francisco Manuel dos Santos, Jan 2019, ISBN 978-989-8943-30-9; ebook and audiobook exist | No (cheap: about 3.50 EUR) | Original in PT-PT | L | Table only: credible native-PT primer, but pre-LLM. |
| *A Inteligência Artificial Generativa* | Arlindo Oliveira | Fundação Francisco Manuel dos Santos, early 2025 (IST news item 24 Feb 2025) | No | Original in PT-PT | L | Table only: the most relevant native-PT lay book found; ISBN and exact date not confirmed (FFMS page did not render). |
| *Desmistificando a inteligência artificial* | Dora Kaufman | Autêntica, 2022 (2nd ed., ISBN 978-65-5928-158-9 per a bookstore listing) | No | Original in PT-BR | L | Dropped: credible author, but a collection of Época Negócios columns on social impact, not mechanisms. |
| *Inteligência Artificial: uma abordagem de aprendizado de máquina* | Katti Faceli, Ana Carolina Lorena, João Gama, Tiago A. de Almeida, André C. P. L. F. de Carvalho | LTC, 2nd ed. 2021 (ISBN 978-85-216-3749-3); an LTC listing mentions a 3rd ed. (2025) that I did not confirm | No | Original in PT-BR (1st ed. won the 2012 Jabuti, technology) | I/T | Table only: a solid Brazilian university ML textbook, mostly classic ML rather than LLMs. |
| *Neural Networks and Deep Learning* | Michael Nielsen | Determination Press, 2015 (site last updated Dec 2019) | Yes: neuralnetworksanddeeplearning.com, CC BY-NC 3.0 | **None found** | I | Short list |
| *The Little Book of Deep Learning* | François Fleuret | Self-published, Apr 2023; v1.3, 12 May 2026; $9 print on Lulu (author warns pricier Amazon copies are unauthorized) | Yes: fleuret.org/public/lbdl.pdf, CC BY-NC-SA 4.0 | **None found** (license would allow one) | I | Short list |
| *Understanding Deep Learning* | Simon J. D. Prince | MIT Press, 2023 (ISBN 978-0-262-04864-4); PDF v5.0.3, 9 Feb 2026 | Yes: udlbook.github.io/udlbook, CC BY-NC-ND | **None found** | I/T | Short list |
| *Dive into Deep Learning* | Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola | Cambridge University Press, 2023; online v1.0.3 | Yes: d2l.ai | **Partial community translation** at pt.d2l.ai (repo d2l-ai/d2l-pt), based on English v0.17.1, last site update Dec 2021; some chapter titles still in English. d2l.ai lists it as "in progress". | I/T | Table only: free and partly in Portuguese, but stale and uneven. |
| *Deep Learning Book* (deeplearningbook.com.br) | "Equipe DSA" (Data Science Academy) | Online series of 100 chapters, site active in 2026 | Yes | Original in PT-BR | I | Dropped: unsigned, no editorial review, published by a course-selling company; chapters cite Nielsen among their sources. Better to send readers to Nielsen directly. |
| *Build a Large Language Model (From Scratch)* | Sebastian Raschka | Manning, Sep 2024, 368 pp., ISBN 978-1-63343-716-6; code at github.com/rasbt/LLMs-from-scratch | No (code free) | **None found.** Manning lists 9 translations (Chinese x2, German, Italian, Japanese, Korean, Polish, Russian, Spanish), no Portuguese. | T | Short list |
| *Hands-On Large Language Models* | Jay Alammar, Maarten Grootendorst | O'Reilly, Sep 2024, 428 pp., ISBN 978-1-098-15096-9 | No | **Yes, AI-assisted translation:** *Modelos de linguagem grandes e práticos*, O'Reilly Media, Mar 2025, O'Reilly ID 9798341637504; chapter pages carry an AI-translation notice and use PT-PT wording ("línguas de grande dimensão"). Seen only on the O'Reilly Learning platform (subscription); no Brazilian print edition found. | T | Short list |
| *Deep Learning* | Ian Goodfellow, Yoshua Bengio, Aaron Courville | MIT Press, 2016 | Yes: deeplearningbook.org (complete HTML) | **None found** (site lists a Chinese translation; a French one exists) | T | Table only: the canonical reference, but heavy math and it predates transformers. |
| 3Blue1Brown "Neural networks" playlist (Deep Learning ch. 1-7, plus "LLMs explained briefly") | Grant Sanderson | YouTube, ch. 1 on 5 Oct 2017; ch. 5 (transformers) 1 Apr 2024; ch. 6 (attention) 7 Apr 2024; "LLMs explained briefly" 20 Nov 2024 | Yes | PT-BR dubbed audio on ch. 5 and "LLMs explained briefly"; PT-BR caption track on ch. 1 (checked in the YouTube player data) | L/I | Companion |
| "[1hr Talk] Intro to Large Language Models" | Andrej Karpathy | YouTube, 22 Nov 2023 | Yes | Auto-translated captions only | L | Companion |
| "Deep Dive into LLMs like ChatGPT" | Andrej Karpathy | YouTube, 5 Feb 2025 (about 3.5 h) | Yes | Auto-translated captions only | L | Companion |
| "Neural Networks: Zero to Hero" | Andrej Karpathy | YouTube playlist + karpathy.ai, from 16 Aug 2022; 8 lectures, "ongoing" | Yes | No | T | Companion |
| "The Illustrated Transformer" | Jay Alammar | Blog, 27 Jun 2018 (updated 2020, 2025) | Yes | **None listed** (11 other languages are) | I | Companion |

## Sources

Lay
- Mitchell: author's book page https://melaniemitchell.me/aibook/ (publisher, translations list); Spanish edition https://capitanswing.com/libros/inteligencia-artificial/
- Wolfram: essay https://writings.stephenwolfram.com/2023/02/what-is-chatgpt-doing-and-why-does-it-work/ ; book https://www.wolfram-media.com/products/what-is-chatgpt-doing-and-why-does-it-work/ ; PT-PT print https://www.wook.pt/livro/o-que-faz-o-chatgpt-e-como-funciona-stephen-wolfram/29210181 ; PT-PT ebook https://www.wook.pt/ebook/o-que-faz-o-chatgpt-e-como-funciona-stephen-wolfram/29263019 ; also https://www.martinsfontespaulista.com.br/o-que-faz-o-chatgpt-e-como-funciona-1088074/p
- Lee & Trott: original https://www.understandingai.org/p/large-language-models-explained-with ; PT https://www.understandingai.org/p/grandes-modelos-de-linguagem-explicados
- Kelleher: https://mitpress.mit.edu/9780262537551/deep-learning/ (403 to scripts; data confirmed via https://mitpressbookstore.mit.edu/book/9780262537551 and Apple Books listing)
- Narayanan & Kapoor: https://press.princeton.edu/books/paperback/9780691249148/ai-snake-oil ; https://www.wook.pt/livro/ai-snake-oil-sayash-kapoor/32002585
- Bennett PT: Alta Books sample https://altabooks.com.br/wp-content/uploads/2024/11/AMOSTRA_UmaBreveHistoriadaInteligencia.pdf ; bookstore record https://www.martinsfontespaulista.com.br/uma-breve-historia-da-inteligencia-1120930/p
- Ananthaswamy: https://publishersweekly.com/9780593185742
- Arlindo Oliveira: https://www.ffms.pt/publicacoes/detalhe/2878/inteligencia-artificial ; https://dei.tecnico.ulisboa.pt/en/news/public/professor-arlindo-oliveira-released-a-book-on-artificial-intelligence ; https://ffms.pt/pt-pt/livraria/inteligencia-artificial-generativa
- Kaufman: https://www.martinsfontespaulista.com.br/desmistificando-a-inteligencia-artificial-995143/p
- Faceli et al.: https://www.servidores.ufscar.br/talmeida/publications/ ; https://minhabiblioteca.com.br/catalogo/livro/109041/intelig-ncia-artificial

Intermediate
- Nielsen: http://neuralnetworksanddeeplearning.com/ (citation metadata: Determination Press, 2015; CC BY-NC 3.0; last update 26 Dec 2019)
- Fleuret: https://fleuret.org/francois/lbdl.html (version history, license, Lulu print); PDF https://fleuret.org/public/lbdl.pdf
- Prince: https://udlbook.github.io/udlbook/ ; release v5.0.3 (2026-02-09) at https://github.com/udlbook/udlbook/releases
- D2L: https://d2l.ai/ (CUP 2023, "translations in progress" list); https://pt.d2l.ai/ (v0.17.1, Last-Modified 12 Dec 2021); https://github.com/d2l-ai/d2l-pt
- DSA: https://www.deeplearningbook.com.br/ (author "Equipe DSA", "Em Português, Online e Gratuito"); chapter 6 references list https://www.deeplearningbook.com.br/o-perceptron-parte-1/

Technical
- Raschka: https://www.manning.com/books/build-a-large-language-model-from-scratch (date, ISBN, translations list)
- Alammar & Grootendorst: https://www.oreilly.com/library/view/hands-on-large-language/9781098150952/ ; PT https://www.oreilly.com/library/view/modelos-de-linguagem/9798341637504/ (seen via search-engine snapshot; O'Reilly returns 403 to scripts); https://maartengrootendorst.com/Hands-on%20LLMs
- Goodfellow et al.: https://www.deeplearningbook.org/

Companions
- 3Blue1Brown: playlist https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi ; lessons https://www.3blue1brown.com/topics/neural-networks ; dates from YouTube page metadata for aircAruvnKk, wjZofJX0v4M, eMlx5fFNoYc, LPZh9BOjkQs
- Karpathy: https://www.youtube.com/watch?v=zjkBMFhNj_g ; https://www.youtube.com/watch?v=7xTGNNLPyMI ; https://karpathy.ai/zero-to-hero.html ; playlist https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ
- Alammar: https://jalammar.github.io/illustrated-transformer/

## Open points

- Arlindo Oliveira's *A Inteligência Artificial Generativa* (FFMS, 2025) may be worth a
  look by someone with the book in hand: the only native-Portuguese, post-ChatGPT lay
  book by a credible researcher found. ISBN and exact date are not confirmed.
- The O'Reilly Portuguese edition of *Hands-On LLMs* is a machine-assisted translation
  on a subscription platform; recommend it with that caveat.
- Mitchell has no Portuguese edition. If a Brazilian edition appears before
  publication, update `mitchell2019guide`.
