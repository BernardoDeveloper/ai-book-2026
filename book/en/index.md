---
id: prefacio
chapter: "Preface"
sources:
  - {post: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia, sha256: "71bce137854c76e643c64c2888ff44ef33b12b3bd3cd7dc3214ade44a46d0f27"}
  - {post: 2026/02/08/rant-ia-acabou-com-programadores, sha256: "309b129d7a93fb9b17e4efaefe75a56b8b85e95568adc2ecc9809306dab8b434"}
  - {post: 2026/05/14/terminando-maratona-ia-sucesso-ou-fracasso, sha256: "ce4d26c715008a4e0b0034c9af56433844c8db43f9b7e035e2b45c5258d1ceae"}
  - {post: 2026/06/11/llm-benchmark-fable-5-e-a-novela-da-anthropic, sha256: "ab900c522b1e3798b82f918c636213aa8290807a14ce39300a21f4fda68ef9a8"}
  - {post: 2026/10/12/llms-agentes-competente-o-suficiente, sha256: "0178f4ea75a7f6b79e7ae1878ccf3ccfd7fe7c0c4edf57d4cfd3bac2dee3e921"}
  - {post: 2026/02/01/vibe-code-fiz-um-editor-de-markdown-do-zero-com-claude-code-frankmd-parte-2, sha256: "65b3ce93900a46d8fe0b9cb7fdc627978e0e220926745dd8c5e4453edc2b3690"}
refs_projects: []
blog_commit: "b9c029231693369b8f895576b491c878aea3e8da"
translated_from: {file: book/pt/index.md, sha256: "4ee804b47a7eadbfd028d4bd46c75591cd2401eb85d0dfbe624522714421c55e"}
---

# Preface {#sec-prefacio .unnumbered}

<!-- src: original -->
In 1939, anyone who visited the New York World's Fair, whose theme was "the world of tomorrow," could meet Elektro. He was a Westinghouse robot about seven feet tall who walked on voice command, spoke some 700 words recorded on a disc, blew up balloons and smoked cigarettes [@wikipedia2026elektro]. At the General Motors pavilion, a giant scale model showed the United States of 1960, with automated highways and rooftop platforms for flying machines [@wikipedia2026futurama].

Twelve years later, the movies showed the other side of the same coin. In *The Day the Earth Stood Still*, from 1951, a flying saucer lands in Washington and out steps a visitor, a giant robot in tow, to warn that humanity, now the proud owner of the atomic bomb, would be wiped out if it carried its aggression beyond its own planet [@wise1951day]. The whole decade filled the screens with machines and invaders threatening the species.

The promise and the fear came out of the same shop window. The fair was put up by companies selling home appliances and automobiles, and the movies were selling tickets. The future that actually arrived brought no robot butler, no flying car and no invasion. It was stranger, more modest and a lot more useful than either version: a computer in almost everyone's pocket.

In 2026 I lived through the current edition of that fair, except I was looking backstage at the same time. It was like living in two worlds.

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
One was the world of the shop window. There, [artificial general intelligence]{.gls key=agi}, a machine able to think about any subject the way a person does, was just around the corner. Reports predicted the end of the world with a date on it, and business owners fired their entire programming staff because they thought the AI's code would come out better.

<!-- src: 2026/06/11/llm-benchmark-fable-5-e-a-novela-da-anthropic -->
In June, one of the biggest companies in the field, its paperwork to go public freshly filed, put on sale a model from the very family it had itself presented as too dangerous for the public. On my test, it tied with the previous model while costing almost twice as much.

<!-- src: 2026/05/14/terminando-maratona-ia-sucesso-ou-fracasso -->
The other world was my terminal. From February to May, I spent more than 500 hours programming almost entirely with AI [agents]{.gls key=agente}, the programs that let the model read files, run commands and work on its own for hours. That came to 24 projects, some that worked out, others that turned into garbage.

<!-- src: 2026/10/12/llms-agentes-competente-o-suficiente -->
Then came months of putting dozens of models through a programming test I built myself, checking the results one by one, month after month. When I put it all together, in October, the curve the ads drew shooting up to the sky showed up in my numbers as an almost flat line.

<!-- src: original -->
The distance between the two worlds ran both ways. In plenty of places the tool was better than the skeptics would admit: you can build real software with it, and I did. In others, it was much worse than the ads were selling. It gets things wrong with total confidence, agrees with whatever you already thought, forgets what was agreed an hour earlier, and needs someone experienced checking what comes out.

This book was born from that distance. It is the account of eight months putting artificial intelligence to the test, from February to October 2026, told by someone who had his hands on the keyboard.

## Who I Wrote This For

<!-- src: original -->
While writing, I had a few people in mind:

- the professional who read that her job will be gone in two years and doesn't know whether she should already be looking for another one;
- the father who watched a video about a superior intelligence about to arrive and didn't know what to say when his son asked if it was true;
- the manager being sold an "AI transformation" that nobody can quite explain;
- the junior programmer wondering if he picked the wrong career.

If you recognized yourself in any of them, start by knowing that the confusion has a known source: advertising. For years it has come from people who profit from your anxiety: companies on their way to the stock market, chipmakers, course sellers with a new name for an old thing. Whoever believed an ad did exactly what the ad was designed to make them do.

And if you got here out of plain curiosity, with no fear at all, great. You'll get a kick out of some of this year's stories.

You don't need to know how to program. I'm a programmer, and a lot of what I tell involves code, but every technical term is explained the first time it shows up and stays in the glossary at the back of the book. When I tell a programming story, it's because it answers a question that matters to anyone who uses these tools.

## Whose Side I'm On

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
I've been programming since the late 1980s, blogging since 2006, and I spent six years teaching programming on a video channel. I watched the dot-com bubble burst and the internet keep right on existing. I watched entire professions appear and vanish. That memory helps when you hear an ad for a "revolution" and want to keep your head.

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
A lot of people know me for a line about hype and knowledge, which you'll find right in the first chapter. Because of it, one crowd thinks I hate AI. Because of what I did in 2026, another crowd thinks I caved to it. Both get it wrong for the same reason: they imagine those are the only two sides.

I've been using AI to write code since early 2023. I like the tool, I use it every day, and it took part in almost everything you're about to read. At the same time, I spent all those months documenting its limits, because that's the part that disappears from the public conversation.

<!-- src: original -->
The over-hyped and the over-haters have one thing in common: both usually talk without having measured anything. That's why this book's method is to measure. When I say a model did well, it's because it passed a test whose setup you'll get to see. When I say it got something wrong, you'll see the mistake.

And when the mistake was mine, the book tells that too. There was a ranking I published, found out was wrong and marked as obsolete, with the notice at the top, for anyone who cared to look.

> Faced with any promise about AI, it's worth asking: good for what, checked by whom, at what cost?

## The Fears You Brought Along

<!-- src: 2026/02/01/vibe-code-fiz-um-editor-de-markdown-do-zero-com-claude-code-frankmd-parte-2 -->
The book follows my year, more or less in the order things happened. Each of its five parts answers a fear I've heard many, many times.

The first is the oldest: is there someone in there? Part I opens the box, with no math. It shows why the text coming out of a chatbot seems to come from someone, why it forgets what the two of you agreed on, what changes when it gets tools to mess with your computer, and why it tends to agree with you and make up sources to back that up. Just understanding that mechanism already goes a long way toward protecting you.

The second fear is the opposite of the first: what if it's all just a demo? In Part II I tell the story of the marathon. There's the text editor that looked done in an hour and a half and needed about thirty hours to really work, the product that went from zero to live in under a week, and the project that failed even with the machine doing everything I asked. It works, just in a very different way from what you see in those "I built an app in ten minutes" videos.

The third comes as a question: which one is the best? Is it getting exponentially smarter? Should I believe the ads? Part III is the fight with the numbers: how you measure an AI, the models I caught cheating on the test, what you can run on your computer at home, and how the propaganda factory around all of it works.

The fourth is about trust: is it dangerous to let this thing touch my stuff? Is it spying on me? Part IV has the day an agent deleted some of my files (and how they came back), the software that goes live without anyone having read it, and what the apps on your phone know about you.

The last is the one that keeps people up at night: what about my job? Part V talks about work and careers, explains why so many companies spend fortunes on AI without seeing results, and ends with the year's balance sheet: where this technology really stood in October 2026, and what that means for you.

Between the parts there are two lighter interludes, to catch your breath. And for anyone who wants to go deeper into how the machine works, there's an appendix that explains the mechanism without a single formula (@sec-apmecanica) and a reading list at the end of the book (@sec-apleituras).

## How This Book Was Made

<!-- src: original -->
Everything here started as writing on my blog over the course of 2026, almost always in the heat of the experiment: dozens of pieces in which AI was the main subject or a big part of it. To turn them into a book, I did what the whole book recommends. AI agents did the grunt work of reorganizing and rewriting, following written rules about my voice and checking every claim against its source. The final word is mine: no chapter goes into the book unless I read and approve it, the same way I do with the code an agent writes for me.

> The machine does the grunt work, something outside checks it, and someone who knows the subject decides.

That's the method you'll see work, and fail when one of the three pieces is missing, throughout the whole book. Making this book that way was the last experiment of my year, and the afterword tells how it went, including what the checking caught (@sec-posfacio).

## Where to Start

<!-- src: original -->
The model names in here will age fast, the way car models age in an old novel. That's why I put the date next to every number. What doesn't age so fast is how these things work and how they get sold, and that's what I wanted to leave you with.

Elektro never became anyone's butler, and the robot from the movie never landed. The AI that arrived in 2026 is also smaller than the shop window and smaller than the horror movie. And it's a lot more useful than both, for anyone who knows what it is.

Start at the beginning. In early February 2026, clips from a podcast I had recorded months before started making the rounds with a line I never said, and two crowds started fighting with an Akita who didn't exist. To explain what I had really said, I had to open the box and show how this thing works inside.

That's where the first chapter begins.

*October 2026*
