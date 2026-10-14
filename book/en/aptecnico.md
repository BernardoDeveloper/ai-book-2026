---
id: aptecnico
chapter: "For Programmers: Behind the Scenes"
sources:
  - {post: 2026/03/31/codigo-fonte-do-claude-code-vazou-o-que-achamos-dentro, sha256: "163bf43bdcd13f66a49fba814324394e1158a23e490e2e1ad1300f845dfe01ab"}
  - {post: 2026/04/06/rag-esta-morto-contexto-longo, sha256: "3ef900794dc109d4ee2958f13bf712ad114a890c7822b72361ba81cf0ea3bd05"}
  - {post: 2026/08/16/entendendo-ia-watermark-da-anthropic, sha256: "86f9a0c1396e07ddf1e4074ad5bc17159e39fcb6d10f993d68803792545fa175"}
  - {post: 2026/04/23/driveclub-shadps4-e-ia-como-aprender, sha256: "83e46a5b3a5f612a08753d368772a9757cbb9289107337a26a5281030208a2c6"}
  - {post: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395, sha256: "c603cd2e1a6631994d48a83b4fdc1c4bd76469dff547455ad642b4cb3fa3b50b"}
  - {post: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus, sha256: "e11a74768b9f9489c03a5c822a9f1e1504733eddacf889fde00cb601650b93ab"}
  - {post: 2026/06/14/llm-benchmark-kimi-v2-7-code-glm-5-2-minimax-m3-local, sha256: "32af8112754812919bff36942ae980e28f3def39e6c106439f52d5036741c9cc"}
  - {post: 2026/10/10/qual-modelo-de-decisao-classificador-de-ia-tipo-jev-e-melhor, sha256: "9557e0d08cd5fa75de197b87ebeb0ebc632bc76d8a46e85041ad75a5ee9bb18c"}
  - {post: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito, sha256: "16e67160868d5583d7806ab19ba71c114315884f47f959a6e6f3d86b77b4f973"}
  - {post: 2026/02/09/ai-agents-qual-seria-a-melhor-linguagem-de-programacao-para-llms, sha256: "d93556fda3856a19b1c0baf917aa1cca83c3fc939198966005c7ffd6acfb396f"}
  - {post: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2, sha256: "81baa442ba97d9ab3271296295075168a97c6cb09e40de426ea29e648669ff03"}
  - {post: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms, sha256: "bee5a97eedf6feceda46af16d79f0fecdea5e75ac25a57130a7123113c4b1f1f"}
refs_projects:
  - "jev-docs/README.md"
  - "jev-docs/benchmark/reports/next-wave-comparison-v1/support-ticket-case-study.md"
  - "private-notes/benchmarks/BENCHMARK_REPORT.md"
  - "private-notes/benchmarks/FINDINGS.md"
blog_commit: "cc8b467dd4d6d3b5c57fad6bb6fae70ec5839a01"
translated_from: {file: book/pt/aptecnico.md, sha256: "a021d307b04dab33037331ee2b593a1dac5aed2db9cedfce577ff2cc798a5561"}
---

# For Programmers: Behind the Scenes {#sec-aptecnico}

<!-- src: original -->
This appendix keeps what I took out of the chapters so as not to wear out readers who don't program: the step-by-step of a debugging session, the memory math of a model running at home, the details of a language test. Each section starts by saying which chapter it came from and reads on its own. If you program, or just like to see the gears turn, this is the place.

## The Dream of Claude Code: How autoDream Would Consolidate Memory {#sec-aptecnico-autodream}

<!-- src: 2026/03/31/codigo-fonte-do-claude-code-vazou-o-que-achamos-dentro -->
In @sec-ch02, the leaked Claude Code showed that the agent's memory was text files in three layers: a short index always on the desk, topic files fetched when needed, and old transcripts searched only by word. The code also carried a process called autoDream, still switched off in the public version of March 2026, that would run in the background while you weren't using the tool, to consolidate that memory [@deeplearningai2026kairos].

For a dream to happen, three gates had to open at once: at least 24 hours since the last dream, at least five work sessions since then, and a lock guaranteeing that two dreams weren't running together. Then the process reread the index, looked for new signals in recent conversations, rewrote the topic files, swapped relative dates, like "last Tuesday," for absolute ones and deleted facts that had been contradicted later. At the end, it pruned the index to keep it short.

The dreamer could read the whole project, but it couldn't change anything in it. It only touched its own notes.

## RAG, Embeddings and the Return of Word Search {#sec-aptecnico-rag}

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
@sec-ch02 tells how, between 2023 and 2025, anyone who wanted a chatbot that answered questions about their own documents was told they needed [RAG]{.gls key=rag} and a [vector database]{.gls key=banco-vetorial}, and how the Claude Code of 2026 used neither. This section keeps the technical side of that story.

The classic way of doing the RAG search took work:

- cut every document into small chunks, of a few hundred words;
- turn each chunk into an [embedding]{.gls}, a list of numbers that represents the "meaning" of the text;
- store those numbers in a vector database, a kind of database built to find similar lists of numbers;
- at question time, turn the question into numbers too, fetch the five most similar chunks and pray they were the right ones.

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
It became an industry. Pinecone, Weaviate, Qdrant, Chroma, LangChain, LlamaIndex: a product and a library for every stage of the plumbing, tutorials everywhere, entire consultancies living off "build your chatbot with your PDFs."

### What Claude Code Used Instead

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
Claude Code's memory was a text index, topic files and transcripts searched by keyword, with the oldest and dumbest tool there is for the job: looking for where the word appears, letter by letter. No embedding, no vector database. Navigating the projects' code worked the same way: list files, search for words, open the whole file.

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
My reading is that the equation flipped. When the window was tiny, the reader (the model) was expensive and limited, so the retriever had to be smart and selective. Once the window could hold an entire novel, the reader became the smartest piece of the system, and the retriever could go back to being dumb: it only needs to bring in plenty of possibly relevant stuff, and the model sorts out what matters.

### The Flaws the Tutorials Didn't Show

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
The vector database confuses similar with relevant. You ask how the system handles an authentication error and it returns every chunk that talks about authentication. The chunk that actually answers may be in tenth place, or not show up at all, because whoever wrote the manual said "login."

Cutting into chunks destroys whatever sits on the boundary. The important table got split down the middle, the definition ended up in one chunk and the example in another, and the boundary almost always lands exactly where the answer was living.

And when it's wrong, it's wrong without leaving a trace. If a word search finds nothing, you know why: the word isn't in the document. If the vector database returns a plausible, wrong passage, there's no sign of where the process failed. On top of that, every time a document changes, the numbers have to be recalculated, and there's always a window in which the index and the document disagree.

### The Cost Math

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
The classic argument for RAG was cost: sending the whole document to the model would be too expensive. In April 2026 I ran the numbers. A question with 200,000 tokens on the desk, a whole big novel, cost about 60 cents on Claude Sonnet 4.6, even less on follow-up questions about the same documents, thanks to discounts for repetition.

Building and maintaining a vector search pipeline, on the other hand, eats up weeks of engineering work, and engineers are expensive. These prices are from April 2026 and change with every release, almost always downward. The reasoning stands: tokens became the cheap part of the bill.

### Where RAG Still Wins

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
None of this means RAG is dead. It still wins in well-defined cases:

- gigantic collections, hundreds of gigabytes of text, where not even word search can cope without an index built ahead of time;
- very different vocabulary between the person asking and the person who wrote it, like the customer who types "my wifi's down" and the manual that says "loss of connectivity";
- images and audio, where there's no word to search for;
- answers that have to come out in fractions of a second, with no room for a big desk;
- auditing, when you have to prove exactly which passage was consulted.

<!-- src: 2026/04/06/rag-esta-morto-contexto-longo -->
Academic research tells the same story, with no silver bullet. A 2024 Google DeepMind study concluded that, when resources allow, the big window tends to win on quality, while RAG stays much cheaper in tokens [@li2024rag]. Search evaluations have shown for years that good old keyword search remains hard to beat outside the domain the embeddings were trained on [@thakur2021beir].

Anthropic itself published in 2024 that attaching a sentence of context to each chunk and combining keyword search with vector search cut retrieval failures almost in half, and that an extra step of reranking the results reduced them further [@anthropic2024contextual]. The combination that holds up is hybrid. If you can only pick one, pick keyword search and you'll still get far.

## The Statistical Watermark in Claude, Up Close {#sec-aptecnico-watermark}

<!-- src: 2026/08/16/entendendo-ia-watermark-da-anthropic -->
@sec-ch04 tells how, since August 2, 2026, Anthropic has been invisibly marking the text of Claude models, to comply with Article 50 of the European AI Act, and explains what that mark proves and what it doesn't. This section shows how the mark is made and why it comes off so easily.

<!-- src: 2026/08/16/entendendo-ia-watermark-da-anthropic -->
The mark, a [watermark]{.gls}, uses no hidden character, invisible space or altered font. It's statistical. The model assembles text by choosing the next word from a list of likely candidates (@sec-ch01). When two or three work equally well, a random number settles it; with the watermark, that number now comes from a secret key combined with the preceding words.

![At every fork between synonyms, the key tilts the choice; in a long text, the tilts add up to a signature.](assets/figures/en/ch04-marca-dagua.png){#fig-ch04-marca-dagua fig-alt="A sentence that forks at two points: 'cloudy' or 'overcast', 'empty' or 'deserted'. At each fork, a small key pushes the choice to one side. Below, a grid with hundreds of choices, most of them marked, forms a pattern labeled signature. Beside it, the same grid after the text has been rewritten by another model, with the marks scattered at random: the signal is gone."}

"The sky was cloudy" and "the sky was overcast" say the same thing. At these synonym junctions, the key nudges Claude toward one of the two words more often than pure chance would. Each individual choice goes unnoticed, but a long text repeats this decision point hundreds of times, and the whole adds up to a signature only the keyholder can measure.

The method comes from SynthID-Text, which Google DeepMind published in 2024 [@dathathri2024synthid].

### Why It Comes Off Easily

<!-- src: 2026/08/16/entendendo-ia-watermark-da-anthropic -->
Since the signature lives in the word choices, it depends on there being a choice. On short or highly factual passages, where there are hardly any possible synonyms, the signal weakens. And when another model rewrites the text in full, the choices become that model's, and the pattern disappears. Anthropic itself admits that light retouching probably leaves part of the mark, and that a complete rewrite eliminates it.

<!-- src: 2026/08/16/entendendo-ia-watermark-da-anthropic -->
Academic tests of SynthID-Text point the same way: detection drops considerably after a paraphrase that preserves the meaning [@han2025synthid]. And rewriting a paragraph while keeping its meaning doesn't call for the smartest model on the market. A small open model, running on your own computer, does the job.

<!-- src: original -->
Checking is closed, too. The mark can only be measured by a detector that has Anthropic's key, and every vendor that adopts its own will have its own key and its own method.

## The Driveclub Black Screen, Step by Step {#sec-aptecnico-driveclub}

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
In @sec-ch08 I tell, in short form, the four days in April 2026 when I hunted a defect in Driveclub, a PlayStation 4 racing game, running on shadPS4, an open source [emulator]{.gls key=emulador} with no stable release yet [@shadps4]. In the night races, the screen dimmed right after the start until it went black, and only came back about a minute and a half later. It took 31 phases of investigation, 44 commits on my copy of the emulator and more than 15,000 lines of diagnostic code, and the fix was changing one integer in a config file. Here's the path from the inside.

### Information That Exists and Doesn't Help

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
The first thing anyone does is search the internet. Here's what turns up:

- guides from 2025 saying to always turn on a certain sync option;
- guides from a few months later saying to turn off that same option, because it kills performance;
- videos with modified versions of the emulator that nobody documented;
- a thread on the project's forum with three mutually incompatible explanations for the dimming;
- my own notes, written a few days earlier, recommending the opposite of what I found out later.

The information exists, but it's scattered, dated and contradictory.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
An AI agent, asked directly, hands you back exactly that material, organized and confident: it suggests a mod that makes the game run in slow motion, it suggests messing with brightness and color correction, which treats the symptom and hides the cause. Its source is the same forums, and the forums were wrong.

### What Was Going On

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Driveclub adjusts the scene's brightness the way the human eye adapts to the dark. The graphics card measures how bright the image is, and the main processor reads that measurement on the next frame to decide the exposure, like a photographer opening or closing the aperture.

The emulator, in its default configuration, didn't synchronize that read. The processor read a stale measurement, zeroed out, and concluded the scene was dark. It opened the aperture, and more, and more, until the image saturated in a way that turned everything black.

There's a stricter sync mode that fixes it. It's tucked away among the advanced options because it's expensive and, on some graphics cards, it tanks performance. Nobody had publicly connected that mode to Driveclub's dimming.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
None of this was knowledge I had on Sunday night. I didn't know the game ran that measure-and-correct loop, or that the option had three modes, or why the middle mode wasn't enough. If I had simply "turned on the option" the forums mentioned, I'd have picked the wrong mode and given up thinking it didn't work.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
What unblocked it was a list of seven suspects the investigation had turned up. One of them bugged me because it was the only one tied to *when* the information was read, while the others were about *whether* it was written correctly. I switched the sync mode, ran the night race in Canada, and night fell naturally.

### Taking Turns Between Two Agents

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
I used Claude Code and Codex, and neither of them knew more than I did about the problem. What they did well was aggregate: they read the emulator's code in parallel with me, cross-referenced, compiled, ran tests and parsed logs of dozens of megabytes much faster than I could have alone.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Neither of them, alone, cracked the problem. Several times Claude Code went in circles, repeating the same hypotheses without bringing anything new. When that happened, I'd spend a few hours in Codex to clear the air, with other ideas and another angle on reading the code, and then go back. The final fix came out of Claude Code, but the journey switched models several times.

There was also something I'd never seen in any agent: Codex started repeating the same "solution" it had just tried, over and over, without noticing what it was doing. I had to kill the session and start a fresh one from scratch.

That says a lot about long sessions. The more the conversation grows, the more the [context window]{.gls key=janela-de-contexto} gets cluttered with earlier attempts (@sec-ch02). The complexity and length of that investigation took down both models, each in its own way.

### The Shotgun Technique

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
Through most of the 31 phases, without knowing I was doing it, I used a technique that has a name: shotgun.

During the race, the game used more than a thousand textures, the images that cover the objects in the scene. If the suspicion was "the dimming comes from some texture" and each one took twenty minutes to examine, I'd spend days on a single branch of the tree. And maybe the answer wasn't even there.

Instead, you shoot at all of them at once. You alter every texture in one go, run the game and, in thirty seconds, you know whether any of them affects the dimming. If none did, you've just ruled out the entire category, and you move on to the next.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
I built 32 of these test mechanisms over the course of the investigation, and only one was actually used to find the bug. Even so, every round ruled out an entire family of hypotheses. And meanwhile, I was learning the system: every test that crashed the game told me where something critical lived, every strange color on screen told me which piece fed which.

When you don't know the system, shotgun probes are a map. You don't use them to find the answer. You use them to learn the terrain.

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
All of this depended on some preparation. Before the first phase, I made sure the defect showed up in 100% of attempts, always with the same timing pattern. If you can't reproduce the problem on demand, you're chasing ghosts, because every experiment needs a before and an after you can measure.

### One Integer and Seven Thousand Lines of Notes

<!-- src: 2026/04/23/driveclub-shadps4-e-ia-como-aprender -->
The final tally amuses me: more than 50 note documents, almost 7,000 lines of text describing hypotheses and rejections, against one integer in the config. Almost none of the 15,000 lines of code is any use as a contribution to the emulator, because it's instrumentation built for Driveclub under those conditions. The fix, by the way, had been sitting in the emulator's code for seven months.

## AI at Home: The Memory Math {#sec-aptecnico-memoria-local}

<!-- src: original -->
@sec-ch13 compares two home machines: a desktop with the RTX 5090, a 32 GB graphics card, and a mini-PC with the AMD Ryzen AI Max+ 395 chip, nicknamed Strix Halo. The chapter sums it all up in one picture, the writer who walks to the bookcase to consult the entire encyclopedia for every word: the size of the bookcase (the memory) decides what fits, and the width of the hallway (the bandwidth) decides the speed. This section keeps the math behind the picture.

### How Much a Model Takes

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
The math is back-of-the-envelope. Each parameter, stored at the normal 16-bit precision, takes 2 bytes. GLM 4.7 Flash, from the Chinese company Z.ai, has about 30 billion parameters [@zai2026glm47flash], and at that precision its weights take about 60 GB, almost twice the RTX 5090.

On the card, it doesn't fit. On the mini-PC, it fit whole, without cutting any precision, and ran at about 18 tokens per second.

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
[Quantization]{.gls key=quantizacao} shrinks that bill. A 70-billion-parameter model that would take about 140 GB at 16 bits fits in about 40 GB at 4 bits, with a quality loss small enough for practical use.

<!-- src: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus -->
At 8 bits the loss is almost imperceptible; at 4 you can already measure it; below 3 the model starts talking real nonsense. For programming and multi-step reasoning, my rule is never to go below 4.

### The Notebook

<!-- src: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus -->
The model's weights are half the bill. So it doesn't have to reread the whole [context]{.gls key=contexto} for every word it writes, the model keeps a notebook of notes on every piece it has already read. That notebook has a technical name, the [KV cache]{.gls key=kv-cache}, and it also lives in VRAM.

The notebook grows in step with the conversation. In a 70-billion-parameter model at normal precision, each token read adds about 0.3 MB of notes. Sounds like nothing, until you run the numbers on a 128-thousand-token conversation: about 40 GB of notebook alone, on top of the weights.

<!-- src: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus -->
And a coding agent fills the notebook fast. It lists files, reads code, compiles, takes in the output of every command, and all of that goes into the context. In my April tests, an agent session ate anywhere from about 40 thousand to more than 150 thousand tokens. With less than about 100 thousand of room, a real project goes nowhere.

<!-- src: 2026/04/05/testando-llms-open-source-e-comerciais-quem-consegue-bater-o-claude-opus -->
On the RTX 5090, the math doesn't work without a sacrifice. To fit a 27-billion-parameter model and a 128-thousand-token notebook into the card's 32 GB, I had to round the weights down to 3 bits, below my own rule.

### The Hallway in Numbers

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
Until March 2026, my home server was an old mini-PC with no graphics card, and any AI on it ran on the processor and turned unusable. The new chip has a single 128 GB block of unified memory, divided between processor and graphics however you like [@amd2025ryzenaimax]. In the March review, I set aside 96 GB for the graphics side.

<!-- src: ref:private-notes/server-notes.md -->
That split didn't last. On April 8 I dropped the graphics side to 64 GB, because the rest of the server, with dozens of services running, needed memory to breathe. Everything @sec-ch13 tells after April, from the September benchmark to the October classifiers, ran with 64 GB of VRAM. The boundary is a setting, and you can move it.

<!-- src: ref:private-notes/benchmarks/BENCHMARK_REPORT.md -->
The RTX 5090's memory delivers about 1,792 GB per second [@pcgamesn2025rtx5090]. The Strix Halo's delivers about 256 GB per second, and it still shares that hallway with the processor and the operating system. The ratio between the two is almost exactly seven, and the speed difference I measured was 6.7 times. A small model the RTX wrote at 155 tokens per second, the mini-PC wrote at 23.

The graphics card has compute to spare. What it's missing is hallway.

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
There's also no use cramming just a piece of the model onto the card and leaving the rest in the computer's memory. That back-and-forth goes through an even narrower channel, about 32 GB per second, and speed plummets from 150 tokens per second to somewhere between 2 and 8.

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
The 2025 Mac Studio, with the M3 Ultra chip, combined the two things: it went up to 512 GB of unified memory with more than 800 GB per second of bandwidth [@apple2025m3ultra]. By my estimate in March, with Brazilian import taxes, the maximum configuration went past 110,000 reais in Brazil.

### Many Experts, Few Awake

<!-- src: 2026/03/31/review-minisforum-ms-s1-max-amd-ai-max-395 -->
There was a mystery in my numbers. A 35-billion-parameter model ran at 43 tokens per second on the mini-PC. A 72-billion one, twice the size, ran at 4.5, almost ten times slower.

<!-- src: ref:private-notes/benchmarks/FINDINGS.md -->
The two are built differently. The 72-billion one is a dense model: for every token, it consults all of its weights, the whole encyclopedia. The 35-billion one is an [MoE]{.gls key=moe}, a mixture of experts.

An MoE splits a good part of the model into blocks, the so-called experts, and has a small router that picks, for each token, which few blocks get to work. In the 35-billion model, only about 3 billion are active per token. The writer consults just a few volumes of the encyclopedia, and the hallway stops being the bottleneck.

<!-- src: original -->
The name is a little misleading. Nobody trained one expert in medicine and another in law. When Mistral's researchers looked at how Mixtral's router distributed the work, they found no split by subject: what showed up looked more like types of words and punctuation [@jiang2024mixtral]. "Expert" here just means "the block the router woke up this time."

![In a dense model, the whole model works on every token; in an MoE, a router wakes up only a few blocks, but all of them have to be in memory.](assets/figures/en/ch13-especialistas.png){#fig-ch13-especialistas fig-alt="Two panels. In the first, dense model: a grid of blocks all lit up, captioned all weights read for every token. In the second, MoE: the same grid with only two blocks lit and a small router pointing at them, captioned only a few blocks work, but all of them take up memory."}

<!-- src: 2026/06/14/llm-benchmark-kimi-v2-7-code-glm-5-2-minimax-m3-local -->
There's a catch, and it caught me in June. The experts that are asleep still take up memory. To run an MoE, you have to fit the whole model, and you only gain speed because you read part of it.

When MiniMax published the weights for M3, an MoE of about 428 billion parameters with about 23 billion active, I ran the numbers for running it at home. Not even the most squashed version, the so-called "1-bit" one, which would already be useless for coding, would fit. On its own it would take about 128 GB, the mini-PC's entire unified memory and double the 64 GB reserved for video, leaving no room for the notebook or the operating system. The name is misleading, by the way: those versions keep the most sensitive parts of the model at higher precision, and the average lands near 2.4 bits per parameter.

## The Classifier Test, Up Close {#sec-aptecnico-classificadores}

<!-- src: original -->
@sec-ch13 tells the test I built in October 2026 for decision models from Jev's family, the [classifiers]{.gls key=classificador} that take a text, some rules and a list of options and pick one. The chapter keeps the lesson: a small, specialized model ties with paid services on a closed decision, and the rule you can write down stays in code. Here are the results in detail.

<!-- src: ref:jev-docs/README.md -->
The cases were support, refunds, moderation and routing, half written in English and half in Portuguese, each with the right answer frozen before any model ran. There were twenty-three configurations: five paid cloud services and eighteen open models running on the mini-PC.

The result, on October 12, 2026, was this:

- at the top, two 27-billion-parameter open models, Perplexity Decider and Decision 3.0, both with 99.4% accuracy on the compact cases and 100% in Portuguese; the two gave exactly the same answers on all 1,024 classifications;
- right behind, tied at 97.6%, Jev itself and Microsoft Decision-1, the latter being the cheapest paid service I measured, about 6 cents per 10 thousand decisions;
- the best 4-billion-parameter open models, like Jebadiah, landed between 87% and 90%, answering in about 200 milliseconds.

<!-- src: 2026/10/10/qual-modelo-de-decisao-classificador-de-ia-tipo-jev-e-melhor -->
A 4-billion-parameter model, which fits on an ordinary graphics card, tied with OpenAI's decision service, which debuted at 90.5%. And the best result in the entire table came from two models anyone can download and run at home.

<!-- src: ref:private-notes/decision-models.md -->
Decision 3.0 took about 49 GB of video memory, and at peak the total brushed 63.5 of the mini-PC's 64 GB. The two champions had to run alone, with everything else shut down, and each decision took close to a second and a half. The cloud services answered, almost all of them, in under half a second.

### The Coin

<!-- src: ref:jev-docs/README.md -->
The tasks had three or four options, so guessing at random would get about 31% right. Julia-1, the smallest model on the list, with 144 million parameters, got 31.5%. It answered in 12 milliseconds, the fastest of all, and got things right like a coin toss.

<!-- src: 2026/10/10/qual-modelo-de-decisao-classificador-de-ia-tipo-jev-e-melhor -->
Of the 71 guesses it gave with more than 90% confidence, 48 were wrong. These tiny models were built to be fine-tuned on the data of whoever is going to use them; out of the factory, applying rules they have never seen, they're no good.

### The Critical Ticket

<!-- src: ref:jev-docs/benchmark/reports/next-wave-comparison-v1/support-ticket-case-study.md -->
One case doesn't show up in any average. The severity rule said: ongoing data loss in production is critical, no matter how many customers it affects. The ticket described permanent data loss, confirmed by the engineers, for a single customer.

The right answer is "critical." Cloudflare's Clef, the 27-billion-parameter version, answered "degraded," along with several models of 4 to 9 billion. Jev got it right, and so did some much smaller models.

It's a single case, and synthetic. But it's exactly the error that costs the most, and the accuracy percentage doesn't show it. It's also the best argument for the severity rule to live in code, as the chapter argues.

## Bun's Rewrite and Zig's Answer {#sec-aptecnico-bun}

<!-- src: original -->
In @sec-ch16 I tell how Jarred Sumner rewrote Bun, the JavaScript runtime that Anthropic bought and that Claude Code runs on, from Zig to Rust with agents, in July 2026. The chapter keeps the method. Here is the fight that came after, between Zig's creator and the Bun team, and what I took from it.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
The day after Sumner's account, Andrew Kelley, Zig's creator, published his response [@kelley2026bun]. I wanted to read the best possible technical argument defending Zig. He makes a few, and they deserve a hearing:

- part of the performance gain Bun credited to the rewrite came from an optimization in the program's final link stage that Zig always offered and Bun hadn't switched on;
- the work of shrinking the executable didn't depend on the language and could have been done in the old code;
- if the test suite is enough to trust the new Rust code, which by his count ran past a million lines with no human review line by line, why wasn't it enough for the Zig code?

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
The third question is a good one and lands squarely on the theme of code nobody read. A large part of his text, however, leaves technical ground and turns into complaints about how Bun is run, the relationship between the two projects, and personal accusations he himself says he can't detail. I have no way to verify any of that, and none of it helps explain the technical decision. I was disappointed.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
So I did the exercise I had hoped to read. I asked two [frontier models]{.gls key=modelo-de-fronteira}, the strongest on the market that July, to play technical referee and write the answer Zig deserved, with Bun's code open in front of them. The result was more balanced than the fight on the internet.

Zig wasn't defenseless. It has explicit mechanisms for cleaning up resources when something goes wrong, and testing tools that flag leaks and memory freed twice, though only on the paths the tests exercise.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
And on one point Zig had a clear edge. A Bun routine that colors messages in the terminal relied on a Zig feature that runs code at compile time. The first Rust translation lost that guarantee and caused a regression in the test build, later fixed with a different mechanism [@bun2026issue30693]. Point for Zig.

The size and speed gains Bun showed, about 20% off the executable and 2% to 5% more in the performance tests, have mixed causes: language, build tooling, configuration, accumulated cleanup. You can believe the numbers without crediting all of it to Rust.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
There's also a conflict of interest: Anthropic owns Bun and sells Claude Code. The Bun team had every incentive to turn the rewrite into a showcase for their new employer's product. That doesn't prove bad faith or invalidate the technical result, but it weighs on how the story was told. Ignoring it would be as naive as ignoring Kelley's resentment.

<!-- src: 2026/07/09/resposta-sobre-bun-em-rust-que-andrew-kelly-deveria-ter-feito -->
My reading, in July, came out like this. Rust was a defensible choice for Bun at that moment: it traded part of the human discipline for compiler checks, and that counts for a lot when part of the code is being written by agents, which move forward by banging into compile errors.

But the evidence doesn't prove Zig was unworkable. An aggressive restructuring inside Zig itself might have solved a lot. We don't have the counterfactual.

What you can say is that the method mattered as much as the language. Language does not replace architecture. It only changes which errors become cheap to detect.

## A Language Made for AI: From PACT to Bend 2 {#sec-aptecnico-bend}

<!-- src: original -->
In @sec-ch18 I tell how the question about which language to learn ran through my year, from a hunch in February to a measurement in October. The chapter keeps the answer. Here are the two experiments with languages designed for AI that came in between.

<!-- src: 2026/02/09/ai-agents-qual-seria-a-melhor-linguagem-de-programacao-para-llms -->
On February 9, 2026, I ran a silly little exercise. I asked Claude and GPT Codex what a programming language made to be edited by LLMs would look like, without any concern for being friendly to humans. Languages are designed around human limits: readable names, indentation, shortcuts that make the code look nice. Python and Ruby take that a long way, and the price is usually efficiency for the machine.

<!-- src: 2026/02/09/ai-agents-qual-seria-a-melhor-linguagem-de-programacao-para-llms -->
Both models reached more or less the same conclusion. They described something similar to the tree structure the compiler builds inside a program, only loaded with annotations: contracts stating what each function promises, a list of everything it can affect outside itself, the origin of each line. The human would write only the specification of intent; the machine would take care of the rest. The sentence that summed up their reasoning was this: the ideal language for AI is the one humans keep rejecting.

<!-- src: 2026/02/09/ai-agents-qual-seria-a-melhor-linguagem-de-programacao-para-llms -->
I made it clear at the time that this was guesswork. It's what the model can deduce from its own probabilities, and asking the model is evidence of nothing. Still, I asked Claude for a prototype compiler for the language it had just described. It chose to write it in Rust, named the language PACT, and I published the project without even testing it [@akita2026pact].

An idea stayed hanging that I considered inevitable in the long run. If generating code becomes trivial, maybe it's worth going back to writing detailed specifications, something the industry abandoned as too unproductive. It was a hypothesis, and I had no way to test it yet.

<!-- src: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2 -->
On September 17, 2026, the Brazilian researcher Victor Taelin released Bend 2, pitched as a fast language that blocks AI mistakes through proof [@taelin2026bend2]. It was almost my February hypothesis in the flesh. The human writes the system's laws in a file, and the AI writes the proofs that the code obeys those laws. A checker, which runs in a tenth of a second, blocks any change whose proof doesn't close.

On launch day I pointed my agents at two of my programs written in Rust and told them to port them to Bend 2. What follows is a review from the language's second day of life, dated, and a lot may have changed since.

<!-- src: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2 -->
The good part was very good. I deliberately injected an off-by-one error into a routine that split an item budget across repositories. The three sample outputs stayed identical, so a test suite of that size would have passed it. The proof checker rejected it, pointing at the exact term that stopped matching.

<!-- src: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2 -->
The rest was still toy-grade:

- it took 93 lines of laws and proofs to guarantee two simple facts about a routine of some 30 lines;
- the part of the program that could be proven came to a few percent of the code; reading data, sorting, screen and network were left out;
- the standard library had no secure internet connection and no keyboard input in the terminal, and I needed eight functions hand-written in C to fill the holes;
- the language had nine releases in ten hours the day after launch.

<!-- src: 2026/09/19/nova-linguagem-voltada-pra-ia-bend-2 -->
It drew heavy criticism from specialists. One day after the launch, a programmer redid Bend's little demo game in SPARK, a mature [formal verification]{.gls key=verificacao-formal} tool from the Ada family, and proved the same properties automatically, without the hundreds of lines of manual proof [@powell2026bend]. My conclusion was that Bend's natural niche is small, critical cores, written by AI and proven by machine. And that I pick a language by the size of the ecosystem around it: I use Rust a ton, I hate the syntax, and I tolerate it, because the LLM is the one writing it.

## The Seven-Language Benchmark {#sec-aptecnico-linguagens}

<!-- src: original -->
In @sec-ch18 I sum up in one sentence the test I ran in October 2026 to find out whether any programming language pays off more with agents: tests helped more than the choice of language. Here are the discussion that motivated the test, its design and the numbers.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
In early October 2026, DHH, the creator of Ruby on Rails, converted his chat app to several languages using agents and posted the throughput results one by one on X [@dhh2026campfire]. Rust came out ahead of Elixir and Ruby, and the debate caught fire. Soon people noticed that the Rust version had gone through far more agent rounds than the others. One programmer took the Elixir version and, with obvious optimizations no first conversion does, made the main page ten times faster [@kurtome2026elixir].

A one-shot conversion done by an agent measures how well the model knows each language and how many rounds it ran on each one.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
That resurrected two beliefs that have been circulating since LLMs became work tools:

- a lean scripting language would be better for AI because it would spend fewer [tokens]{.gls key=token};
- a strongly typed language would be better for AI because the compiler would catch the errors, so the agent would need less repair.

The second is a first cousin of my February hypothesis (@sec-aptecnico-bend). Instead of arguing on X, I went and measured.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
I built a reproducible benchmark and published everything [@akita2026vibebench]. There was one task, hard on purpose: take a multi-tenant accounting ledger, one that serves several companies at once, from one version to a more demanding one, with rules that cut across several operations. Correctness was judged by 43 test scenarios, 16 of them hidden from the agent.

I crossed seven languages, from Rust and Haskell to Python and Ruby, with four model configurations: Kimi K3, GLM 5.3, Claude Opus 5.5 and GPT-6 Sol through Codex. Each combination ran with and without a public test suite in hand, twice. That came to 112 attempts.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
The results, that October:

- the two [frontier models]{.gls key=modelo-de-fronteira}, Opus and Sol, got 53 out of 53 valid attempts right, in every language (the other three attempts failed on infrastructure, not on the code); the task was too easy to separate the models, let alone the languages, so there was no ranking left to publish;
- in the weaker models, what changed the result was the presence of tests: 24 correct deliveries with the suite in hand, against 16 without it;
- Ruby, the leanest language in lines, spent practically the same tokens as Rust on Sol, and on Opus it was the most expensive of all, more than double C#;
- in the Opus attempts I audited, in Ruby, Rust and Haskell, there was not a single cycle of fixing compilation errors: the code compiled on the first try.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
Where the models erred, they erred on business rules: a property of the ledger that had to hold from one operation to the next. No compiler catches that kind of error, in typed or dynamic languages.

<!-- src: 2026/10/11/existem-linguagens-melhores-pra-programar-com-llms -->
The caveats are part of the result. It was a single task, with two repetitions per combination, and it measures the floor each language delivers under the same short effort, without showing the most a patient engineer would extract from it. A tie at the ceiling doesn't say which language would go further on a harder task either, only that none got in the way on this one. If your task doesn't look like a ledger, the numbers don't transfer.

And if you disagree, the right move is the one I made: run your own test.
