---
id: epilogo
chapter: "Epilogue: What I'd Tell You"
sources:
  - {post: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia, sha256: "71bce137854c76e643c64c2888ff44ef33b12b3bd3cd7dc3214ade44a46d0f27"}
  - {post: 2026/08/18/hot-take-harness-loop-engineering-graph-engineering-sao-bullshit, sha256: "3bf57210a84a838886736656f0a1991e08a8b59900b6109cb5b0b78dcd02c6ce"}
  - {post: 2026/04/11/vs-code-e-o-novo-cartao-perfurado, sha256: "c4a9ef44ff34e504686c7202868466c3a78ec86482a26890da501b4594920376"}
  - {post: 2026/07/19/llm-benchmark-devo-usar-o-que-tem-nota-maior, sha256: "8560b2c684a6bfd9a8def203ba00d507b77c2b8e0164b4f7168ca68bbcba3dc4"}
  - {post: 2026/02/08/rant-ia-acabou-com-programadores, sha256: "309b129d7a93fb9b17e4efaefe75a56b8b85e95568adc2ecc9809306dab8b434"}
refs_projects: []
blog_commit: "b9c029231693369b8f895576b491c878aea3e8da"
translated_from: {file: book/pt/epilogo.md, sha256: "e9e8823153cdd40716ac89a544b84ddcd3860e6691402c3be843508d30bf2f98"}
---

# Epilogue: What I'd Tell You {#sec-epilogo .unnumbered}

<!-- src: original -->
Monday, then. You've reached the end of the book, or nearly, and the question you brought on the first page is still there, maybe a little smaller: what do I do with all this?

I have no career plan to sell you, and no course. I have what a year of daily use taught me, and it fits in a few pages. A good part of it will sound obvious. The hard part is holding on to the obvious when the day's headline screams the opposite.

## Fear Sells

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
In @sec-ch01 you met the line on the poster: your hype about AI is inversely proportional to your knowledge of AI. After this year, I'd add that fear follows the same rule. The less a person knows about how the thing works, the more room is left to imagine the end of the world.

<!-- src: 2026/08/18/hot-take-harness-loop-engineering-graph-engineering-sao-bullshit -->
Fear and hype come out of the same factory. In August 2026 I wrote about the courses in "engineering" this and that which sprouted around agents, and the mechanism was an old one. First they make you anxious, thinking you're falling behind, that everyone else already migrated to the new paradigm and you haven't. Then they charge you to cure the anxiety they created.

That fear of being left out has an acronym, FOMO, the fear of missing out, and in this market it's the business model. The announcement that general intelligence arrives in two years works the same way, on a bigger scale (@sec-ch14). Whoever has stock to sell, graphics cards to sell or a funding round to close needs you to feel that the world is going to end, or start over, next Tuesday.

<!-- src: original -->
Fear gives bad advice because it decides fast and decides for you. Whoever buys in a panic buys whatever is in front of them, usually the course from whoever shouted loudest. And whoever freezes in fear stops using a tool that, as you saw throughout the book, really pays off in the hands of someone who knows what they're doing.

> Every time an announcement about AI speeds up your heart, ask who makes money from you feeling that way.

## What's Worth Learning

<!-- src: original -->
Three things, and none of them expires in six months.

### How the Thing Works

<!-- src: original -->
The first is the bare minimum about the machine. An [LLM]{.gls} generates the most likely text, piece by piece, from a frozen file that doesn't learn from you (@sec-ch01). Keeping just that in your head already defends you against half the promises: you don't expect consciousness from a text generator, you don't expect it to remember a conversation from the week before, and you get suspicious when it agrees with everything (@sec-ch04).

If you want to go deeper, @sec-apmecanica shows the mechanism without math, and @sec-antes has a reading list for several levels.

<!-- src: 2026/04/11/vs-code-e-o-novo-cartao-perfurado -->
The same goes for the fundamentals of your own trade. In April I wrote about the programmer with no foundation who watches the [agent]{.gls key=agente} put together a database query, tests it against 300 fake rows, thinks everything is fine and has no idea what happens with a million real rows. With an agent in hand, people with a foundation learn faster. People without one just outsource their own ignorance.

### Judgment

<!-- src: original -->
The second is judgment, the ability to look at an answer and know whether it's any good. The best test I know is the one in @sec-ch18: can you explain why the right answer is the right one? If you can, the machine types for you. If you can't, it types just the same, and you don't notice when it gets things wrong.

Judgment is trained by doing, getting it wrong and checking. The agent makes the doing much cheaper, and you can test and throw out one hypothesis after another, as in @sec-ch08. The checking is still entirely yours.

### Your Domain

<!-- src: original -->
The third is your own trade. Remember the map in @sec-ch20: the model sees in detail what the world published and is blind to what stayed behind closed doors. Your company's unwritten rules, the difficult client, the exception only you know about, the reason that regulation exists: none of that went into training.

That's the part of the map that's blank for the machine and filled in inside your head. The deeper you know your trade, the more the tool pays off in your hands.

## What You Can Ignore

<!-- src: 2026/08/18/hot-take-harness-loop-engineering-graph-engineering-sao-bullshit -->
This list is longer, and it frees up more time:

- courses and certifications in the taxonomy of the month. When the technology becomes a commodity, the money migrates to the new name: five names for chaining API calls and a certification that expires in six months. Anyone working with method, tests and review already does what they teach;
- announcements of [AGI]{.gls key=agi}, of extinction, of a model too dangerous to release. The script has existed since at least 2019 (@sec-ch01), and @sec-ch14 shows who profits from it;
- ranking fights over a tenth of a point. At the top, the models form a pack, and the gap between them fits inside the [run-to-run noise]{.gls key=ruido-entre-execucoes} (@sec-ch11);
- the promise that the next model will fix it. The numbers in @sec-ch20 show a flat line up top, and what changes the result is the process around it;
- the video of the app built in ten minutes. The first few hours are the easy part, and the other ninety percent is in @sec-ch05.

## Check for Yourself

<!-- src: 2026/07/19/llm-benchmark-devo-usar-o-que-tem-nota-maior -->
In July, after months of publishing tables, I wrote the line I'd most like you to take away from here: don't trust a benchmark, don't trust influencers, don't trust me. It applies to this book. That's why I left in @sec-ch20 the list of what would make me change my mind, with things anyone can measure from the outside.

<!-- src: original -->
Checking takes less work than it seems, and the practical checklists are already in the book, each one where the subject called for it:

- for using a chatbot on serious matters, the eight rules in @sec-ch04, with the extra precautions for health, money and news;
- for reading a [benchmark]{.gls} table, @sec-ch11, and for reading an announcement, the questions in @sec-como-ler-anuncio, with both lists summarized in @sec-apC;
- for letting a program touch your files without losing anything, the habits in @sec-ch15 and the kit in @sec-apB;
- for deciding whether to trust software built with AI, the questions in @sec-ch16;
- against scams and [deepfakes]{.gls key=deepfake}, the habits in @sec-ch17.

<!-- src: original -->
Nearly all of them end with the same move, which is going up to the primary source: the study, the contract, the official data. And the most useful primary source for anyone using AI at work is a test of your own. Take a real task, one you already know how to solve, give it to two tools, run it more than once and compare with what you know is right. That's the benchmark that matters to you, and no announcement publishes it.

## Without Handing Over the Wheel

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
In February, in the middle of the fight over whether AI had killed programmers, I wrote a line I still use: never ask a hammer how you should run your company. The hammer from @sec-ch01 is excellent for a lot of nails, like the draft, the summary, the translation, the new report built from the old one and the first version of the code. Use it, and use it a lot.

<!-- src: original -->
The line I don't cross is the decision. The machine can propose, research, compare and write. Whoever answers for the result decides. In practice, that comes down to a few habits:

- only delegate what you can evaluate; if you can't tell whether the result is any good, the task isn't ready to leave your hands;
- read before you approve, and whatever you can't read, don't approve;
- every now and then, do yourself what you usually delegate, so you don't lose your touch;
- keep what you learned somewhere of your own, because the model keeps nothing (@sec-ch20).

> The tool does almost anything you ask. Knowing what to ask, and whether what came back is any good, is still your job.

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
I spent 2026 unafraid of this machine and suspicious of almost everything said about it, and that combination served me well. Nobody needs to glorify a hammer, or hate one.

<!-- src: original -->
If you'd like to see this discipline applied one last time, you don't have to go far. This book was put together with the same agents it examines, under the rules it recommends. How that was done, and what remained my work, is in the next few pages.
