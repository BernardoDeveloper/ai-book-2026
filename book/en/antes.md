---
id: antes
chapter: "Before You Start: What This Book Doesn't Explain"
sources: []
refs_projects: ["docs/research/FURTHER-READING.md"]
blog_commit: "b9c029231693369b8f895576b491c878aea3e8da"
translated_from: {file: book/pt/antes.md, sha256: "b5430e97bc9d13d1fb45535ef42507decb736a29d3258e986dc2f8c2aeae0fc8"}
---

# Before You Start: What This Book Doesn't Explain {#sec-antes .unnumbered}

<!-- src: original -->
This book gives you intuitions about how these machines work, and stops there. @sec-ch01 explains what a language model is, why it works with pieces of words, the difference between training a model and using it, and why it learns nothing from you once it's done. They're everyday images, with no math at all, and they're enough to follow the story.

What I left out on purpose is the mechanics inside:

- how a [neural network]{.gls key=rede-neural} learns, with [gradient descent]{.gls key=descida-do-gradiente} and [backpropagation]{.gls key=retropropagacao};
- what [embeddings]{.gls key=embedding} are, the lists of numbers that represent the meaning of a piece of text;
- how a [transformer]{.gls}, the architecture behind all of these models, and its [attention]{.gls key=atencao} mechanism work;
- how [pretraining]{.gls key=pre-treino} and [RLHF]{.gls} (reinforcement learning from human feedback) turn a heap of text into a polite assistant.

<!-- src: original -->
Each of these subjects calls for a whole book, and those books exist, written by people who research or build these things. A narrative book that tried to do the same would turn into a textbook by page ten.

## Why It's Worth Knowing

<!-- src: original -->
Even so, this book gets better if you understand those mechanisms first. Several claims in Parts I and III rest on them. When I say the model doesn't learn from your conversation, that it agrees with you because it was trained to please, or that each new generation costs much more and improves much less, I'm summing up consequences of how training works.

<!-- src: original -->
Readers who know the mechanics read those sentences as conclusions. Readers who don't have to trust me, and the whole book is a plea not to trust anyone blindly, me included.

<!-- src: original -->
That said, nobody needs to do homework before turning the page. The book was written to be read without any of this, and the story stands on its own.

> You don't need to know how the engine works to understand why the car crashed. But if you ever want to pop the hood, the directions are here.

<!-- src: original -->
If you'd like a middle ground, there's an optional appendix, *The Machine Inside, Without the Math* (@sec-apmecanica). In a few pages and without a single formula, it shows the panel of knobs, the walk down a hill in the fog, the map of meanings and the highlighter of attention. And it ends by explaining where the nickname [stochastic parrot]{.gls key=papagaio-estocastico} came from, what it gets right and why I agree with it. You can read it now, halfway through or at the end.

## For Anyone Who Wants to Go Deeper

<!-- src: ref:docs/research/FURTHER-READING.md -->
The list below is short on purpose and runs from easiest to most technical. I checked every item in October 2026: author, publisher, and whether you can legally read it for free.

### Easiest First

- Timothy B. Lee and Sean Trott, *Large Language Models, Explained with a Minimum of Math and Jargon*: the shortest path, and free [@lee2024modelos].
- Stephen Wolfram, *What Is ChatGPT Doing ... and Why Does It Work?*: from the next word all the way to the transformer, with pictures; the full essay is free on the author's website [@wolfram2023chatgpt].
- Melanie Mitchell, *Artificial Intelligence: A Guide for Thinking Humans*: a researcher explains how networks learn and where they fail, against the hype; it predates ChatGPT [@mitchell2019guide].
- John D. Kelleher, *Deep Learning*: a pocket book that already explains gradient descent and backpropagation, a bridge to the next level [@kelleher2019deep].

### With a Little Math

- Michael Nielsen, *Neural Networks and Deep Learning*: the gentlest classic on neural networks and backpropagation, free online; it stops before transformers [@nielsen2015neural].
- François Fleuret, *The Little Book of Deep Learning*: under 200 pages, each the size of a phone screen, from training to the transformer; free PDF [@fleuret2023little].
- Simon J. D. Prince, *Understanding Deep Learning*: a modern, beautifully illustrated textbook, to consult after the two above; free PDF [@prince2023understanding].

### Hands-On (with Python)

- Sebastian Raschka, *Build a Large Language Model (From Scratch)*: builds a GPT-style model piece by piece; the book is paid, the code is free [@raschka2024build].
- Jay Alammar and Maarten Grootendorst, *Hands-On Large Language Models*: nearly 300 original illustrations [@alammar2024handson].

### Free Videos

- Grant Sanderson (3Blue1Brown), the *Neural networks* series: the clearest visual explanation of neurons, gradient descent, backpropagation and attention [@sanderson2017neural].
- Andrej Karpathy, *Intro to Large Language Models* and *Deep Dive into LLMs like ChatGPT*: pretraining, fine-tuning and RLHF explained for a general audience [@karpathy2023intro; @karpathy2025deepdive].
- Andrej Karpathy, *Neural Networks: Zero to Hero*: writes backpropagation and a small GPT live; requires solid Python [@karpathy2022zerotohero].
- Jay Alammar, *The Illustrated Transformer*: the diagrams a lot of people learned transformers from; free text [@alammar2018illustrated].

<!-- src: original -->
If you don't have time for any of this, start with the Lee and Trott piece or the first few 3Blue1Brown videos. And if not even that, no problem: turn the page. The story starts in February 2026, with a line I never said making the rounds on the internet under my name.
