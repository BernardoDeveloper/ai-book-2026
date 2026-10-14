---
id: apestudar
chapter: "How to Study with AI at Your Side"
sources:
  - {post: 2019/10/23/akitando-65-a-dor-de-aprender-que-cursos-livros, sha256: "2b05e6d3d26f3a619e53e6350dcbcd6a3f36c3ea7a77961ce845ddbe9561b322"}
  - {post: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r, sha256: "4c8343cf9487f3e389341a2e5654a423cb2ff2cced3ecbbddb5aed5385b544c1", commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"}
  - {post: 2021/01/06/akitando-90-o-que-os-cursos-nao-te-ensinam-sobre-mercados, sha256: "5a6b08a8fdebc6eac5511e470883960e1f763187351f8df54e684349eee446c1"}
refs_projects: ["microgpt/README.md"]
blog_commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"
translated_from: {file: book/pt/apestudar.md, sha256: "59f8180ccd01d957bcb29a194a6ab37e863a0fa57cc868055ba32fcb56fcc160"}
---

# How to Study with AI at Your Side {#sec-apestudar}

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
In April 2020, at the start of the pandemic, I recorded an episode called "Aprendendo a aprender" (Learning to learn). In it I summed up the right way to learn in three sentences [@akitando076]:

> 1) by giving problems to be solved 2) by having no official material, and instead forcing people to know how to find the materials they need 3) by having no supervisor or boss who hands it over pre-chewed, forcing a sense of autonomy and responsibility to develop.

<!-- src: original -->
Back then, the enemy was the step-by-step course. In 2026 a much friendlier adversary showed up: a machine that answers any question on the spot, with infinite patience and no charge per lesson. The three rules still hold, and each one got harder to follow, because the agent does for free exactly what they forbid.

## A Problem of Your Own

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
The first rule asks for a real problem, with no script. The tutorial takes you by the hand to a result someone already knew; the real problem leaves you alone with something nobody has solved your way.

With AI, the tutorial got even more comfortable, because now it adapts to you and even types the steps. That's why the problem has to be yours: a spreadsheet that irritates you at work, a little program you want to use, a doubt no video answers. That's how I spent four days hunting a defect in an emulator (@sec-ch08), and it's what turns the machine's answer into learning.

<!-- src: ref:microgpt/README.md -->
If the itch you want to scratch is AI itself, there's a good one to start with. The first lesson of my microgpt lab trains a model of under a million parameters on an ordinary CPU, in under a minute, and shows the whole cycle of @sec-ch13b in code you can actually read [@akita2026microgpt]. Run it, break it on purpose, change the size and see what happens before you ask any agent to explain it.

## Find the Material Yourself

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
The second rule seems the oldest. I learned to program before the internet, taking buses to photocopy borrowed material, and today material is everywhere. But the exercise was never collecting paper: it was choosing, comparing and discovering which source is any good.

The agent skips that step for you and hands over the finished summary. Use the summary as a map and go read the place it came from: the documentation, the code, the original paper. You've seen in @sec-ch04 what happens to those who trust the source the model cites without opening it.

## Nobody Chewing for You

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
The third rule is the one AI threatens most. The boss who hands over everything pre-chewed now lives in your pocket, and never gets tired of chewing.

<!-- src: original -->
The habit I recommend is simple to say and boring to follow: try on your own before asking the machine. Give yourself some time, half an hour, an afternoon, and only then ask. When you ask, request a hint instead of the solution, and then compare its answer with your attempt. Learning happens in the difference between the two.

<!-- src: 2019/10/23/akitando-65-a-dor-de-aprender-que-cursos-livros -->
It will hurt, and it's supposed to. In 2019 I wrote that "learning, at its core, is a fight between you and yourself" [@akitando065]. If the machine takes away all the pain, it takes the learning with it.

## The How and the Why

<!-- src: 2020/04/01/akitando-76-guia-definitivo-de-aprendendo-a-aprender-a-maior-bronca-da-sua-vida-rated-r -->
In that same 2020 episode I complained about people who switched languages and got lost:

> Since they only learned "how" to use the tool but never "why" the tool exists, every new tool confuses them.

<!-- src: original -->
With the agent, the "how" became free: it writes the code, the formula, the paragraph. The "why" stays entirely with you. For everything it does, ask why it's that way, and check whether you could explain it without it (@sec-ch18). If you couldn't, you haven't learned yet, you've just received.

## What Doesn't Age

<!-- src: 2021/01/06/akitando-90-o-que-os-cursos-nao-te-ensinam-sobre-mercados -->
Tools change every decade, sometimes every year. What I saw survive all the switches, from dBase to the agent, was a small foundation:

- algorithms and data structures, the subject that, in my opinion, separates the amateur from someone who will build a career [@akitando065];
- how the computer works underneath: memory, processes, network, what happens when a program runs [@akitando076];
- basic math, statistics and probability, which no tool course teaches [@akitando090] and which are the raw material of a language model (@sec-apmecanica).

<!-- src: 2019/10/23/akitando-65-a-dor-de-aprender-que-cursos-livros -->
With that foundation, a new language becomes a matter of weeks. In 2019 I told how I learned Elixir, Crystal and Rust in about 30 days each, to the point of being productive, because I had already programmed in many others [@akitando065], against the months my first languages cost me with no foundation at all (@sec-ch08).

<!-- src: original -->
Those who don't program can swap the list for the foundation of their own trade: the accounting behind the spreadsheet, the grammar behind the text, the law behind the contract. The rule is the same. The machine speeds up enormously someone who already has the map, and someone who doesn't just gets to the wrong place faster.

<!-- src: original -->
The epilogue's math, the 1% the course gives and the 99% you hunt down yourself (@sec-epilogo), still stands with the machine at your side. It can shorten the hunt a lot, as long as the one holding the flashlight is still you.
