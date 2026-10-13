---
id: posfacio
chapter: "Afterword: How This Book Was Made"
sources:
  - {post: 2026/10/12/llms-agentes-competente-o-suficiente, sha256: "0178f4ea75a7f6b79e7ae1878ccf3ccfd7fe7c0c4edf57d4cfd3bac2dee3e921"}
  - {post: 2026/04/15/como-falar-com-o-claude-code-efetivamente, sha256: "cb59a9bf2d015a6660ea6fc2ade02b2447f0cc15172c8e0d47847c7a6e4dfc18"}
  - {post: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo, sha256: "c6451afc1d26d440a2364ebee3249330f54d9e0ddcb493aa7fdba4c9ff72d8c4"}
refs_projects: []
blog_commit: "b9c029231693369b8f895576b491c878aea3e8da"
translated_from: {file: book/pt/posfacio.md, sha256: "f3bfa1c83bfd693953942599301b2334c45b295b4a95cfcb52344ca400daaa52"}
---

# Afterword: How This Book Was Made {#sec-posfacio .unnumbered}

<!-- src: 2026/10/12/llms-agentes-competente-o-suficiente -->
On October 12, 2026, I published the year's synthesis on the blog, the piece that became @sec-ch20. The next day I started turning the whole year into a book. The first [commit]{.gls} in this book's repository is dated October 13.

<!-- src: original -->
I had written 131 posts on the blog in 2026, almost half a million words, on subjects ranging from model [benchmarks]{.gls key=benchmark} to bitcoin wallets. Reorganizing all that by hand, alone, would have taken months I didn't have. So I did what this whole book describes: I handed the grunt work to [agents]{.gls key=agente} and kept the deciding, the setting up of the process and the checking for myself.

It's worth telling how it went, for two reasons. You have the right to know how the text you just read was produced. And the process itself is the last example of the book's thesis.

## A Sealed Inventory

<!-- src: original -->
The first step was an inventory. A script read the 131 posts and stored, for each one, a code computed from the exact content of the file. If a comma changes in the post, the code changes with it. I also recorded the exact point in the blog's history from which everything was read.

Then an agent read each post and filled out a fixed form: the thesis in one or two sentences, the claims a book would need to check, which of them go stale quickly, which lay reader's fear the post answers, what to cut. Of the 131, 96 had AI as their central subject or gave it significant weight. The rest only made it in when they taught something specific, and every AI post left out has the reason written down.

<!-- src: original -->
A lot of what I wrote in February no longer held in September. I reran my benchmark several times during the year, corrected costs, changed my mind about tools. That's why the process has a lineage map, which says which post superseded which and what can still be salvaged from the older one. The chapters tell the most recent state and, when the change teaches something, they tell the change.

From the analyses came a proposed structure: five parts, each answering a reader's fear, twenty chapters and two interludes. I read it, changed it and approved it. Some pieces went in at my request, like @sec-antes and the appendix on the machine's insides (@sec-apmecanica), because I wanted readers to know what the book leaves unexplained and where to learn it.

## The Contract

<!-- src: original -->
Before scaling up, a pilot chapter. The one chosen was @sec-ch05, and it served to calibrate the voice and uncover the questions an agent would have along the way. Every question resolved became a written rule. One of them: when the chapter summary and the post disagree on a detail, the post wins.

Those rules went into a document every agent read before writing, along with the voice guide, which inherits the rules of my blog, and a continuity file saying which chapter explains each concept and what each character is called. It's the [project instruction file]{.gls key=agents-md} from @sec-ch09, at the scale of a book.

<!-- src: original -->
With the contract ready, the chapters were drafted in parallel, in waves, one agent per chapter. Agents working at the same time contradict each other, and that happened.

One chapter said FrankMD had about 130 commits in three days; another, that it had 212 in 19 days. Both numbers came from the posts and were right, they just covered different windows. An integration log collected these conflicts, and the rule became to make the window explicit in each chapter.

On top of everything runs an automatic checker, the equivalent of the [continuous integration]{.gls key=ci} from @sec-ch06. It rejects dashes, phrases banned by the voice guide, stray links in the middle of the text, citations that don't exist in the bibliography and chapters without provenance markers. A chapter with errors doesn't pass.

## What the Checking Caught

<!-- src: original -->
Every number, date and name was checked against three things: the posts, the reference projects (the benchmark repository, the ai-memory one, the ai-jail one and my notes on the home server, which live in a private repository) and primary sources on the internet. A few examples of what that checking caught:

- in the March review of my mini PC with a Strix Halo chip, I had set aside 96 GB of memory for the graphics side. On April 8 I lowered it to 64 GB, and some later posts still said 96. The book uses 64 for everything after April (@sec-ch13);
- a counting bug in one of the benchmark's tools underestimated by 40 to 90 times the cost of the runs done with it before August (@sec-ch11). The book doesn't cite any of those costs;
- in the June post about Claude Fable 5, I wrote that it cost ten times more than Opus 4.8 per run. In July, redoing the benchmark's math, I found that the old estimates left out the tokens read from cache: Opus 4.8 came to about $6, not a little over one, and Fable cost almost double, not ten times. The June post still says ten times; the book tells the wrong number and the correction (@sec-ch14);
- in January I wrote that GLM 4.7 Flash was the same GLM 4.7, just compressed. The official page shows a separate, much smaller model, with 30 billion [parameters]{.gls key=parametros} [@zai2026glm47flash];
- a chapter summary, written by an agent, said that Claude Code's signing lock had fallen in less than a day after the code leak (@sec-ch16). The original announcement came out about 30 hours later, and the book says "the next day" [@guthrie2026drm];
- METR's productivity study, which I had described as done on private code, used large open source projects [@becker2025measuring].

<!-- src: original -->
Notice that many of these corrections are to my own blog. In some places, the book ended up more accurate than the posts it came from. And one of them corrected a summary written by an agent, because the source beats the summary, including when the summary comes from the machine.

> The drafts came out fast. Trust in the text came from the checking.

## A Trail for Every Paragraph

<!-- src: original -->
Every paragraph in this book, in the source file, carries an invisible marker saying where it came from: which post, which reference project, or whether it's new text written for the book. The marker disappears when the book is built, so you never see it.

It's there for maintenance. If tomorrow I correct a post, a script recomputes the code for each post, sees which one changed and points to the chapters that depend on it. The marker leads straight to the paragraphs that came from that post, and only those need revisiting. The bibliography plays the same role for outside sources: each reference notes which post cited it.

<!-- src: original -->
The images follow the same logic. The diagrams and charts were written as code, and each chart carries in its own code a note of the chapter its data came from. The AI-generated illustrations are labeled as such, and the prompt, the model and the date of each one are on record.

Real people only appear in freely licensed photos, credited in the caption and in @sec-creditos. No image of a real person was generated by AI.

## What's Still Mine

<!-- src: 2026/04/15/como-falar-com-o-claude-code-efetivamente -->
In @sec-ch09 I told how the blog post about talking to Claude Code was written by Claude itself, from a request of mine, and corrected by me while it wrote. This book was made the same way, on a larger scale. This afterword too: the draft came from Claude, running in Claude Code, from a request of mine. The English edition you're reading is a translation of the Portuguese text, made the same way, by agents working under the same rules, and reviewed by me.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
It wasn't the first time that year. In April, Claude Code translated twenty years of blog posts in a little over a day and a half (@sec-interlude1). Ninety percent went smoothly, and the other ten only got sorted because someone read the list of what had failed and went looking for another way.

<!-- src: 2026/10/12/llms-agentes-competente-o-suficiente -->
That's the point of @sec-ch20 applied to the book itself. Any of the good models of October 2026 would have written similar drafts, because the model became a commodity. What made the process work was what surrounds it: the inventory, the written contract, the automatic checker, the sources as [oracle]{.gls key=oraculo}, the trail for every paragraph. It's the same old engineering I defended all year, applied to text.

<!-- src: original -->
The repository records the first commit and the drafts of every chapter on the same day. That's the first hour from @sec-ch05: impressive, and it says almost nothing about the rest. The other ninety percent is reading, cutting and correcting.

And that part is mine. The experiences in the book are the ones I lived, and the opinions are the ones I wrote over the year, none invented to fill a chapter. I approved the structure. No chapter goes into the book without me reading and approving it, and whatever I send back for rework goes through the same process again.

<!-- src: original -->
The machine wrote fast. I answer for every sentence in this book, including the errors that slipped past the checking. When one turns up, the trail exists precisely so the correction reaches the right paragraph.

> The agents were competent enough to write the draft. Deciding what it said remained my job.
