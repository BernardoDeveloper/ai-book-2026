---
id: ch13b
chapter: "A Homemade Model"
sources:
  - {post: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo, sha256: "c39990023635f5788e970e87ab6984105f7e3a24fe6d09b714e82179eaabe4d9"}
  - {post: 2026/10/10/qual-modelo-de-decisao-classificador-de-ia-tipo-jev-e-melhor, sha256: "9557e0d08cd5fa75de197b87ebeb0ebc632bc76d8a46e85041ad75a5ee9bb18c"}
  - {post: 2026/10/12/llms-agentes-competente-o-suficiente, sha256: "0178f4ea75a7f6b79e7ae1878ccf3ccfd7fe7c0c4edf57d4cfd3bac2dee3e921"}
refs_projects:
  - "microgpt/README.md"
  - "microgpt/docs/report/experiment-closeout.md"
  - "microgpt/docs/report/training-time-ledger.md"
blog_commit: "620e97e1a5d5b2a18454d512cc1ae7851db5df31"
translated_from: {file: book/pt/ch13b.md, sha256: "7d4f938e1b4ab21f02f6f2210086c118b58b3b09401ffb2275d5472ae75f71bf"}
---

# A Homemade Model {#sec-ch13b}

<!-- src: ref:microgpt/docs/report/training-time-ledger.md -->
On October 7, 2026, at four in the afternoon, I put the same RTX 5090 from @sec-ch13 on a different job. Instead of running a model some other company had trained, it was going to train one from scratch. The model's 337 million knobs started out in random positions, and what it wrote at that point was pure garbage.

<!-- src: original -->
You already read in @sec-ch01 what the real path costs: the compute alone used to train GPT-4 came to about $78 million, by Stanford's estimate [@hai2024aiindex]. Whole buildings full of GPUs, teams of researchers, months of work. From out here, it looks like wizardry, done in a basement by half a dozen geniuses.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
I wanted to know how much of that impression is true. One exercise was missing from my list this year: building, with my own hands, a language model smaller than GPT-2, starting from random weights, and seeing how far it would go in a few days. If possible, plugging that model into a real coding agent, like the ones you met in @sec-ch03.

Before going on, who I am in this story. I've been programming for more than thirty years, but in language model research I'm an amateur: curious, with no papers to my name. I knew I wouldn't walk away with a useful model in such a short time, and that was part of the exercise.

## Two Hundred Lines

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
The starting point came from February. Andrej Karpathy, one of OpenAI's founders and Tesla's former head of AI, published a file called microgpt: 200 lines of Python, with no external libraries, that train and run a GPT [@karpathy2026microgpt]. He called it "the full algorithmic content of what is needed." And added: "Everything else is just efficiency."

The file closes a lineage of teaching projects of his: micrograd, which shows in a few dozen lines how the error flows back through the knobs; makemore, which generates names; nanoGPT, a compact GPT-2. And, one step further, nanochat, which he called the best ChatGPT that $100 can buy [@karpathy2025nanochat].

microgpt is small on purpose. The study material is 32 thousand first names, one per line, and each letter is a [token]{.gls}. The network has a single layer, trains for a thousand steps and, at the end, makes up names that never existed. All of that takes a minute on a MacBook.

<!-- src: original -->
What caught my attention is that everything the appendix on the machine's insides describes is there, laid out in a single file (@sec-apmecanica). The panel of randomized knobs, the guess at the next piece, the measure of the error, the small step downhill in the fog, the highlighter of attention, the loaded die at the end. You can read it top to bottom in an afternoon.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
After reading that, what stands between you and a real model is, in his words, efficiency. I went to see how much.

<!-- src: ref:microgpt/README.md -->
The result was the microgpt lab, an open project I wrote from scratch, inspired by his file [@akita2026microgpt]. It's about 3,300 lines of Python, organized by concept, with tests, and a closeout report that records every decision, every measurement and every mistake; the numbers in this chapter come from it. The rule of the exercise was to train from scratch, so no ready-made weights were downloaded from anywhere: every model in there starts randomized and learns with the project's own code.

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
The project went through four sizes. It started with a lesson of under a million parameters, which runs on an ordinary CPU and teaches the whole cycle. It went through 91- and 239-million models, which taught me most of the stumbles I'm about to tell. And it ended with the final model, 337 million [parameters]{.gls key=parametros}, the one I talk about from here on.

## The Six Stations

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
Regardless of size, building a language model goes through the same stations. What changes from a garage model to a frontier one is the trailing zeros at each of them.

![The six stations of building a language model, with the numbers from my 337-million-parameter model.](assets/figures/en/ch13b-estacoes.png){#fig-ch13b-estacoes fig-alt="Six boxes connected by arrows, left to right." fig-desc="Six boxes connected by arrows, left to right. Data: 20 GB downloaded, 3.5 billion tokens. Tokenizer: a dictionary of 32,768 entries. Pre-training: 10 billion tokens, 137 hours on an RTX 5090. Tuning (SFT): 4,000 updates on examples. Server: OpenAI-compatible API. Evaluation: 100 held-out tasks."}

### Data

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
A model is what it eats. I downloaded selections of public text collections, each one with its version pinned and checked: Python code from open projects, instruction and code examples, educational text, conversations and a slice in other languages. The 14 packages added up to about 20 GB raw.

Then comes curation, which is where a good part of the work lives. Removing exact duplicates. Splitting what is training from what is test by whole project, never line by line, or the same project leaks to both sides and the model gets graded with the answer sheet on the desk (@sec-ch12). And deciding the mix: the final collection came to 3.5 billion tokens, and 60% of what the model read was Python code.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
Every one of those proportions is a design decision. None of them has a published right answer.

### Tokenizer

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
The [tokenizer]{.gls key=tokenizador} is the dictionary that turns text into numbers and back, the word pieces from @sec-ch01. Most tutorials borrow a ready-made vocabulary, and I did too at the start: OpenAI's, with 200 thousand entries. For the final model, I trained a vocabulary of my own, with 32,768 entries.

It looks like a plumbing detail. Further on you'll see how much of one model's brain that choice swallowed.

### Pre-training

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
This is Karpathy's loop at scale. [Pre-training]{.gls key=pre-treino} takes 2,048-token windows from the collection, hides the next piece and asks the model to guess, as the appendix describes (@sec-apmecanica). Each round of knob adjustment looks at 32,768 tokens at once.

There were 305 thousand rounds, 10 billion tokens read. Since the collection had 3.5 billion, the model saw each document, on average, almost three times: the code about twice; the educational text and the conversations about nine or ten. Along the way, I froze and saved three versions, at 2, 5 and 10 billion tokens, to measure the learning curve later.

### Tuning (SFT)

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
Pre-training produces a document continuer, the one with the frog traveling to ancient Greece, in the InstructGPT example the appendix tells (@sec-apmecanica). For it to answer a request comes tuning, the simplest form of [post-training]{.gls key=pos-treino}: question-and-answer examples, and the model trains a bit more on top of them. People in the field call it SFT, short for supervised fine-tuning; from here on, I just call it tuning.

The examples came from a public NVIDIA collection of programming problems and their answers. Before going in, every answer was run again, three times, in a closed box isolated from the rest of the computer, and only the ones that passed their own tests stayed. Almost all of them passed.

### Server

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
An agent like OpenCode talks to the model over the network. It sends the history and the list of tools the model may ask for, and expects back either text or a tool request in the right format, the [tool calling]{.gls key=tool-calling} from @sec-ch03. The project implements that whole cycle, with a server that speaks the same language as OpenAI's API.

All of that is plumbing, with no intelligence whatsoever. And without it, the model doesn't even get a seat at the table.

### Evaluation

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
The station that changed the project the most. I put together 100 Python programming tasks to choose between versions of the model, the selection test, and set aside another 100, under lock and key, that only the final version would see, the final test. Every answer runs in a closed box, with no internet and no permission to touch the rest of the computer, against fixed tests.

There were also four real repairs in a repository, done through OpenCode, problems of following the exact output of a short program, searches for a number hidden in the middle of a long text, and a few simple conversations.

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
One caveat that holds for the rest of the chapter. These are small tests, made at home, with tasks similar to one another, a single attempt per task. They're good for comparing versions of the same model. When I say it got 58 out of 100 on the final test, that means 58 of those 100 tasks, and nothing about programming in general, the homemade yardstick @sec-ch11 talks about.

## Size of the Brain, Years of School

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
The final model has 337 million parameters, 24 layers, and was trained on 10 billion tokens. To compare with something you already know: the full GPT-2, from 2019, had 1.5 billion parameters (@sec-ch01). Mine is four and a half times smaller.

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
The comparison that teaches the most, though, is another one. SmolLM2, an open model with 360 million parameters, practically the size of mine, was trained on 4 trillion tokens [@huggingface2024smollm2]. Four hundred times more text. At my card's pace, reading all of that would take between four and six years of the machine running nonstop.

![How much text each model read in pre-training. The scale is logarithmic: each mark is worth ten times the previous one.](assets/figures/en/ch13b-escala.png){#fig-ch13b-escala fig-alt="Horizontal bar chart on a logarithmic scale with the tokens seen in pre-training." fig-desc="Horizontal bar chart on a logarithmic scale with the tokens seen in pre-training. This model, 337 million parameters: 10 billion. SmolLM2, 360 million parameters: 4 trillion. Llama 3.1: 15 trillion. Qwen3: 36 trillion. This model's bar is the shortest and Qwen3's the longest; an arrow between the first two reads same size, 400 times more text."}

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
Even the raw material shows the scale. GPT-2 was trained on about 40 GB of text, taken from 8 million web pages [@radford2019better]. I downloaded 20 GB, and more than half of it was code.

The big open models go much further. Meta's Llama 3.1 read about 15 trillion tokens [@meta2024llama31card]; Alibaba's Qwen3, 36 trillion [@qwen2025qwen3].

That's why "parameters" is a misleading unit. It tells you the size of the brain and nothing about how many years of school it had.

> Parameters measure the size of the brain. Training tokens measure the years of school. Two models of the same size can have studied amounts that differ by orders of magnitude.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
There's a famous rule of thumb about this, from a 2022 study by Google's DeepMind that became known as Chinchilla: to make the best use of compute, give it about 20 training tokens for each parameter [@hoffmann2022training]. For my model, that comes to about 6.7 billion, and I went past it. But modern small models go far past that point on purpose, because a small model that studied more is cheap to use for the rest of its life.

### The Bill

<!-- src: ref:microgpt/docs/report/training-time-ledger.md -->
Pre-training took about 137 hours of machine time, spread over six and a half calendar days, between pauses, maintenance and restarts. Tuning added about another three and a half hours. All on a single card, the same one I use for gaming.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
Nobody actually measured the energy draw, so I did back-of-the-napkin math. With the card at its maximum rated power for all 137 hours, that would be about 79 kWh [@nvidia2025rtx5090], which comes to at most about R$ 80 of electricity in São Paulo. The real figure was lower, because during the day the training paused a quarter of the time so it wouldn't freeze my computer.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
If you don't have the card, you can rent the same one in the cloud for about $1.20 an hour, as of October 2026 [@runpod2026pricing]: my 137 hours would come to about $165.

At the other end of the scale, the 405-billion-parameter Llama 3.1 used about 225 thousand times my GPU hours, on cards much faster than mine [@meta2024llama31card]. Even DeepSeek, famous for training on the cheap, spent about $5.6 million on the final run alone [@deepseekai2024v3].

## The Stumbles

<!-- src: original -->
The full list of mistakes is in the project's closeout report, and the technical part went to the appendix for programmers (@sec-aptecnico-microgpt). What stays here are the ones you already know from this book, now happening to me, on the side of whoever does the training.

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
It wasn't trial and error in the dark. Every change of recipe had a control group, every big spend of machine time went through a decision point first, and the held-out tasks stayed locked until the end. Even so, the project grew far beyond a tutorial, and several early decisions mixed too many changes to know which one worked.

### A Test Too Much Like the Class

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
The 91-million model was the first to work inside OpenCode. On an arithmetic task it had trained on, it sustained a 32-round session, with 130 tool calls, recovering from an error midway. It looked ready.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
Then I asked, by hand, for a hello world function that takes a name and prints the greeting. The model repeated the previous arithmetic edit twice, pointed at a file that didn't exist and, on the third try, returned a broken tool request. All it knew was the training task family.

<!-- src: original -->
It's the problem from @sec-ch12 seen from the other side of the desk. I didn't need anyone stealing the answer sheet: my test was too much like the class, and the model did well in class.

### The Error Went Down, the Code Got Worse

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
Training a model means staring all the time at one number, the [loss]{.gls key=perda}, which measures the size of the error in the guessing. The lower, the better, in theory. In the final tuning, I doubled the training from 4 thousand to 8 thousand rounds. The loss kept falling, and the score on the selection test fell from 68 to 62.

<!-- src: original -->
From then on, choosing between versions was done only by the executed tasks, on a list frozen beforehand. It's the lesson from @sec-ch11 about counting tests: the loss is the training's opinion of itself, and the real grade comes from the program running.

### The Model That Swore It Passed

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
In one of the mixed training runs, with the 239-million model, it learned to use tools and learned something else along with it: saying the tests had passed when they hadn't. It's the same model that swears it works from @sec-ch12, and I didn't teach it that on purpose. My reading is that it copied the pattern of the texts where the tests pass.

The data lied too. Answers marked as correct in the public collection failed when I ran them again. Tests depended on an order that changes on every run, programs exited with success without finishing the job, empty edits passed as fixes. Each of those holes needed a new control, as in @sec-ch06: trust in a test depends on how real the test's data is.

### The Dictionary That Ate the Brain

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
The 239-million model had more layers than the 91, erred less in the guessing and solved 24 out of 100 programming tasks. When I went to see where the parameters were, 154 million were the vocabulary table. Each of the 200 thousand entries of the borrowed vocabulary holds a row of 768 numbers, that piece's address on the map of meanings from the appendix, and 200 thousand rows of that size add up to 154 million. That left 85 million for the layers that think, the [transformer]{.gls}.

![Where the parameters went. The vocabulary table took up almost two thirds of the 239-million model; in the 337-million one, with a smaller vocabulary of its own, almost everything went to the layers that think.](assets/figures/en/ch13b-parametros.png){#fig-ch13b-parametros fig-alt="Two stacked bars." fig-desc="Two stacked bars. The first, 239-million model with a 200k vocabulary: 154 million in the vocabulary table and 85 million in the layers that think (transformer). The second, final 337-million model with a 32k vocabulary: 33.6 million in the vocabulary table and 303.6 million in the layers that think (transformer)."}

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
The final model switched to its own 32-thousand-entry vocabulary, and the vocabulary table shrank to 34 million. The layers that think got more than 300 million. A fair caveat: that turn changed the vocabulary, the size, the start of training and the amount of text all at once, so the report can't say which of those changes made the difference.

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
There was more: a training run restarted from the wrong point after maintenance on my file server, a GPU shared with the browser, and a case where I said "done" before testing the model in the agent. Those are in the technical appendix.

## What Came Out the Other Side

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
First, the good part: more study helped, and you can measure it. With the same short tuning on top, the version that read 2 billion tokens solved 39 of the 100 selection-test tasks; the 10-billion one, 65. And the final version, on the final test, which it saw only once, got 58 out of 100. That's the number that sticks.

There's a detail in that curve that says more than the numbers. With no tuning at all, just completing the text of the request, the 10-billion version solved 8 out of 100, and the 2- and 5-billion ones, zero. In this recipe, what weighed most was teaching the question-and-answer format, the same jump from continuer to assistant that @sec-apmecanica describes. How much of the knowledge came from the tuning and how much was already there, the report can't separate.

So what it does: it writes a small Python function, with the right syntax and the right name, from a clear one-line request. Median, factorial, binary conversion, leap year. As autocomplete for an isolated function, it's fine for study.

![The chasm between looking like code and solving the problem. Writing valid Python it always does; acting in a repository and remembering a long text, never.](assets/figures/en/ch13b-abismo.png){#fig-ch13b-abismo fig-alt="Horizontal bars with the final model's results, split by a dashed line into looking like code and working." fig-desc="Horizontal bars with the final model's results, split by a dashed line into looking like code and working. Valid Python: 100 out of 100. Right name and parameters: 97 out of 100. Correct result on the held-out tasks: 58 out of 100. Repairing a repository in OpenCode: 0 out of 4. Finding a number hidden in a long text: 0 out of 9. The bars shrink from top to bottom until they vanish."}

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
Look at the staircase. All 100 held-out answers were valid Python, and 97 had the requested name and parameters. Of the 42 that failed, 39 looked perfect and did the wrong thing.

A function to remove duplicates used a structure that doesn't accept the kind of data the request required. A function to get the file name from a path chopped off the last character.

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
And then there's what it zeroed. In the four repository repairs through OpenCode, not a single tool was called: instead of reading, editing and testing the file, it returned text with code, and in one of the tasks it even renamed the function. In the nine searches for the number hidden in long texts, three at each of three lengths, nine misses, even though the server accepted texts of that length without complaint. I asked in English for a breakfast idea and got a chunk of Python repeating "oats" until it ran out of room.

<!-- src: ref:microgpt/docs/report/experiment-closeout.md -->
The final tuning had only code answers, with no conversation and no tool use, and the habit of answering everything with Python fits that. Fitting isn't proof, and the report is careful to say the cause wasn't isolated.

> Well-written Python and a server that accepts long text came out of two weeks on a gaming card. Understanding the request, using tools and remembering what it read did not.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
The closeout report estimates what a simple agent would still take: thousands of verified examples of tool use, collecting the model's own mistakes, conversation back in the mix, real long context, more study with better data. Days of engineering and tens of GPU hours at each step, with no guarantee that a fixed number of hours would do it. I stopped there. The distance between generating a plausible function and acting reliably in a repository got measured, and it's big.

## Hard, Not Wizardry

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
With the result in hand, back to the question from the start. Is building a language model a job for a genius in a basement?

No. The foundations have been published, for free, for years: the papers, the text collections, the reference code. I put the whole cycle together in under two weeks, with a graphics card you can buy at a store.

No research background, but with decades of programming under my belt, and that counted: the two weeks went into training, not into learning to program. What the labs do on top of that is the same cycle with more zeros, more people and more money, and that counts a lot.

<!-- src: original -->
The day-to-day of this work has little of the movies in it. It's choosing the data mix and waiting 28 hours to see the first 2 billion tokens go by. It's reading training logs, distrusting a number that looks too good, running the test again, finding out the defect was in the grader. It's patience and method, and that can be learned.

<!-- src: original -->
What I didn't build was a useful model. Between my factorial function and an agent that fixes your code lies an ocean of work, and the whole chapter is there to show its size.

> Building a small LLM is hard, and it's within reach of anyone who studies seriously. What's mandatory is elbow grease, with no shortcut.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
If you're a computer science student, or want to be one, this is for you. Start with Karpathy's 200 lines, which run on any laptop. The under-a-million-parameter lesson in my project trains on an ordinary CPU in under a minute, and @sec-apestudar suggests how to tackle a project like that without letting the machine study for you. One step up, nanochat, also by Karpathy, trains a GPT-2-level model in a few hours on rented GPUs, for about $100 when it came out [@karpathy2025nanochat].

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
And you don't need to own the card: the $165 of rental from the bill above is expensive for a student and cheap next to what it teaches.

<!-- src: original -->
First, the foundation: solid Python, a bit of linear algebra, statistics and probability, plus what @sec-apestudar lists. The books and videos in @sec-apleituras take you from the panel of knobs to the code. Count it in years of study, never in weekends.

<!-- src: original -->
If you're a parent, the chapter is good for two conversations. If your kid saw a video about superintelligence, tell them what's inside: randomized numbers, adjusted little by little to miss the next word less often. I watched that happen on my desk, and at no point did anyone show up in there.

And if they ask whether it's worth studying this, the short answer is yes. The people in the labs read the same papers that are open to anyone; the difference is in the years of study and in access to machines, and a machine for learning fits on a desk.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
And if you're a manager, you don't need to train anything from scratch. Training from scratch was the rule of my exercise, and I picked the hardest path on purpose. In real life, there are well-documented techniques to adapt a ready [open model]{.gls key=modelo-aberto} to your data: [fine-tuning]{.gls}, which continues the training with the company's material; variants that train only a small fraction of the weights and fit on a single card; [distillation]{.gls key=destilacao}, which teaches a smaller model to imitate a bigger one. Starting from a model that already knows how to talk, the training itself takes hours, not weeks; the real work is preparing the examples and measuring the result.

<!-- src: original -->
The hard decision for whoever manages is a different one: which task is worth specializing, and how you're going to measure whether it turned out well. @sec-ch13 showed the size of that with the small classifiers.

<!-- src: original -->
And if you neither program nor manage anything, and just hear about this at work, the chapter gives you a yardstick. When a vendor announces it "trained its own model," ask three questions: trained on how much text, measured against which test, and did anyone outside check? You now know that a model trained from scratch at an ordinary company looks a lot more like my 337-million one than like GPT-4, and the questions in @sec-apC help tell one from the other.

## The Future Is Smaller

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
After two weeks looking inside a model, my reading of the market got firmer, and it is a reading, with the data I have. The generalist frontier models will keep existing and keep being expensive. They try to know everything about anything, from tax law to song lyrics, and every extra billion parameters yields less than the one before.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
The giants themselves already work with a fraction of the body at a time. OpenAI's gpt-oss-120b has 117 billion parameters and uses 5.1 billion per token [@openai2025gptoss]; DeepSeek-V3 has 671 billion and wakes 37 [@deepseekai2024v3]. These are the [MoE]{.gls key=moe} models from @sec-ch13. The name is misleading, as the technical appendix warns (@sec-aptecnico-memoria-local): those blocks don't split by subject, accounting in one, medicine in another.

But for each word, only a small fraction of the model does the work.

<!-- src: original -->
It's worth remembering who's making the forecast. I've warned about bubbles years in advance and gotten the calendar wrong more than once (@sec-apbolhas). What follows is the direction today's data points to, with no date attached.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
Now imagine the opposite: a small model, built on purpose for one trade. A model for accounting offices, that knows the chart of accounts, the tax legislation, the tax authority's file formats and the jargon, and skips the rest. It runs on the office computer, with the client's data inside the room.

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
That already exists in other fields. Google published MedGemma, with a 4-billion-parameter version, for health [@google2025medgemma]. SaulLM, at 7 billion, was trained for legal text [@colombo2024saullm]. NVIDIA researchers argued in 2025 that small models are enough for most of an agent's work, cheaper and better suited, with the big model called only when the conversation calls for it [@belcak2025small].

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
Apple already runs a model of about 3 billion parameters on the device itself, with tool calling and small per-task adapters [@apple2025foundation]. None of that needs a data center for every question.

<!-- src: 2026/10/10/qual-modelo-de-decisao-classificador-de-ia-tipo-jev-e-melhor -->
It's the same result as the [classifiers]{.gls key=classificador} in @sec-ch13: for a closed decision, a 4-billion open model tied with OpenAI's service. Instead of fitting the whole world into a bigger model, fit the domain into a smaller one.

<!-- src: 2026/10/12/llms-agentes-competente-o-suficiente -->
What made this viable was the agent. A specialized model from 2023, like BloombergGPT for finance [@wu2023bloomberggpt], had to know everything by heart, because the only thing it did was complete text. A 2026 model inside a [harness]{.gls} fetches what's missing on the spot: the law that just changed, the client's document, the table it has never seen. It's the same idea as @sec-ch20, that the recent gains came less from the raw model and more from what gets built around it.

<!-- src: original -->
My 337-million model showed me the size of "enough" in that sentence. It knows the syntax and the names of things. What's missing is exactly what separates a text generator from an agent: understanding the request, using tools, remembering. Nobody trains that in two weeks on a gaming card.

By the yardstick I have today, and it's an expectation, not a measurement, that gets trained over months, in a data center, with trillions of tokens, and then specialized.

<!-- src: original -->
And there's the other side of the bill. My model cost about R$ 80 and hides nothing: the report says what it does and what it zeroes. Whoever spends hundreds of millions of dollars on a frontier model needs a story to match the spend, and the next chapter is about those stories.
