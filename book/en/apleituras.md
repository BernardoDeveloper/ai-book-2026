---
id: apleituras
chapter: "Further Reading"
sources:
  - {post: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo, sha256: "c39990023635f5788e970e87ab6984105f7e3a24fe6d09b714e82179eaabe4d9"}
refs_projects: ["docs/research/FURTHER-READING.md"]
blog_commit: "cc8b467dd4d6d3b5c57fad6bb6fae70ec5839a01"
translated_from: {file: book/pt/apleituras.md, sha256: "041cb7011e72208ac8ccad4914ea5877a3cde22f582d43ef1f4f9cbbb6f5e0c7"}
---

# Further Reading {#sec-apleituras}

<!-- src: ref:docs/research/FURTHER-READING.md -->
The list below is short on purpose and runs from easiest to most technical. I checked every item in October 2026: author, publisher, whether a Portuguese edition exists and whether you can legally read it for free. Most are available only in English; I point out the exceptions.

## For Anyone

- Timothy B. Lee and Sean Trott, *Large Language Models, Explained with a Minimum of Math and Jargon*: the shortest path, free and with an official Brazilian Portuguese translation [@lee2024modelos].
- Stephen Wolfram, *What Is ChatGPT Doing ... and Why Does It Work?*: from the next word all the way to the transformer, with pictures; the full essay is free on the author's website, and there is an edition from Portugal, *O Que Faz o ChatGPT e Como Funciona* [@wolfram2023chatgpt].
- Melanie Mitchell, *Artificial Intelligence: A Guide for Thinking Humans*: a researcher explains how networks learn and where they fail, against the hype; it predates ChatGPT [@mitchell2019guide].
- John D. Kelleher, *Deep Learning*: a pocket book that already explains gradient descent and backpropagation, a bridge to the next level [@kelleher2019deep].

## With a Little Math

- Michael Nielsen, *Neural Networks and Deep Learning*: the gentlest classic on neural networks and backpropagation, free online; it stops before transformers [@nielsen2015neural].
- François Fleuret, *The Little Book of Deep Learning*: under 200 pages, each the size of a phone screen, from training to the transformer; free PDF [@fleuret2023little].
- Simon J. D. Prince, *Understanding Deep Learning*: a modern, beautifully illustrated textbook, to consult after the two above; free PDF [@prince2023understanding].

## Hands-On (with Python)

- Sebastian Raschka, *Build a Large Language Model (From Scratch)*: builds a GPT-style model piece by piece; the book is paid, the code is free [@raschka2024build].
- Jay Alammar and Maarten Grootendorst, *Hands-On Large Language Models*: nearly 300 original illustrations; an AI-assisted Portuguese translation, *Modelos de linguagem grandes e práticos*, is available only on O'Reilly's subscription platform [@alammar2024handson].

<!-- src: 2026/10/14/treinei-meu-proprio-modelo-de-ia-spoiler-e-so-pra-estudo -->
- Andrej Karpathy, *microgpt*: a whole GPT in 200 lines of Python, no libraries at all, that trains in a minute on a laptop; the starting point of @sec-ch13b [@karpathy2026microgpt].
- Andrej Karpathy, *nanochat*: the next step, a GPT-2-level model trained in a few hours on rented GPUs; the code is free [@karpathy2025nanochat].
- My microgpt lab: the full cycle of @sec-ch13b, from data to evaluation, with a report on every stumble; the first lesson runs on an ordinary CPU [@akita2026microgpt].

## Free Videos and Visual Guides

- Grant Sanderson (3Blue1Brown), the *Neural networks* series: the clearest visual explanation of neurons, gradient descent, backpropagation and attention; parts have Brazilian Portuguese dubbing or subtitles [@sanderson2017neural].
- Andrej Karpathy, *Intro to Large Language Models* and *Deep Dive into LLMs like ChatGPT*: pretraining, fine-tuning and RLHF explained for a general audience; in English, with only automatic subtitles [@karpathy2023intro; @karpathy2025deepdive].
- Andrej Karpathy, *Neural Networks: Zero to Hero*: writes backpropagation and a small GPT live; requires solid Python [@karpathy2022zerotohero].
- Jay Alammar, *The Illustrated Transformer*: the diagrams a lot of people learned transformers from; free text, with no Portuguese translation [@alammar2018illustrated].

<!-- src: original -->
If you don't have time for any of this, start with the Lee and Trott piece or the first few 3Blue1Brown videos.
