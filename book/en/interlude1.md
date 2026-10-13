---
id: interlude1
chapter: "Interlude: Twenty Years of Blogging in a Weekend"
sources:
  - {post: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo, sha256: "c6451afc1d26d440a2364ebee3249330f54d9e0ddcb493aa7fdba4c9ff72d8c4"}
refs_projects: []
blog_commit: "b9c029231693369b8f895576b491c878aea3e8da"
translated_from: {file: book/pt/interlude1.md, sha256: "c66a507dca01a4035b04420c1966c8042180a3f24953769a3f973dd5d261bda1"}
---

# Interlude: Twenty Years of Blogging in a Weekend {#sec-interlude1 .unnumbered}

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Monday, April 6, 2026, around six thirty in the evening. The day before, my blog had turned twenty, and I still hadn't written the anniversary post. I opened Claude Code inside the folder where the whole blog lives and typed, more or less, this: translate everything to English.

That was literally it. Then I went about my day.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
The blog started in 2006, on Google's Blogspot, like nearly every blog back then. It moved house several times: a ready-made system built in Ruby on Rails, then another one, then an engine I wrote myself in 2012 and dragged through years of upgrades, until it landed, in September 2025, on a static site generator called Hugo. Twenty years carrying the same posts from one format to the next, tossing the junk along the way.

And twenty years with the same debt.

## The Promise That Never Got Off the Ground

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Almost everything there was in Portuguese. For years I'd been getting messages from Brazilian readers living in Portugal, the United States, Japan, Germany, Canada, always with the same request: an English version, to show their coworkers. "I'd show this piece to my team, but it's only in Portuguese."

I always answered that one day I'd translate it. And I never did.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
The math didn't work. There were 727 posts in Portuguese. Translating them by hand, one by one, would take weeks, maybe months of dedicated work, and I was never going to find the stamina for it. Worse: every year, more posts joined the queue.

There was even an irony in the middle of it. Some posts were born in English, like a 2008 series of interviews with well-known programmers abroad, and a few posts from 2017 and 2018, when I tried writing in English first. Those were stuck on the other side, with no Portuguese version.

## Sleeping While the Agent Works

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
I left the [agent]{.gls key=agente} running and went to sleep. Woke up Tuesday and it was still going. Slept again. Early Wednesday morning, it was done.

From the first translation commit to the last, it took about 39 hours, counting the nights, the lunches and a coffee break somewhere in there. The title of this interlude takes some poetic license: in practice, it was a long weekend that happened to fall in the middle of the week.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
The project history shows the cadence: a batch of posts from a 2008 conference, another from a 2009 conference, one from 2011 on Objective-C, all of 2012, the 2015 series on Elixir. More than 80 commits, organized by year and by series.

At the end there were 354 posts in English alongside the 727 originals. Almost half the blog, in one shot.

For each post, the agent read the original, wrote the translation, and then ran a style pass over it to strip out the habits of machine-written text. Hundreds of times in a row.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
And the quality surprised me. About ninety percent came out good, natural and faithful to the way I write. I didn't expect it to work this well. With solid guidance on tone and style, the agent respected the original and didn't try to "correct" any of my technical ideas.

Worst case, I reviewed a few paragraphs. Best case, the English version read as if I'd written it directly in the other language.

> A job I put off for almost twenty years, because it was too big and too tedious, turned into a weekend problem.

## The Bill

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
It had a price. I subscribed to Anthropic's heavy-use plan, Max 20x, built for people who use Claude Code all day. I had never hit its ceiling, not even in the longest sessions of the marathon from the previous chapter.

That translation was the first time. By Thursday morning, my account dashboard showed 91% of the weekly quota burned and about R$ 280, close to $50, in extra usage charged on top of the monthly fee. And the agent started getting, more and more often, an error warning that I was sending too many requests.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
It tracks: reading a whole post, translating it, revising the style, and repeating that hundreds of times in a row eats a mountain of [tokens]{.gls key=token}, those little chunks of text the model reads and writes in (@sec-ch01). I thought it was fair. That's the price of using the tool hard precisely when it made a difference.

## The Six That Said No

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Not everything went through, though.

Half a dozen old posts refused to be translated. Both Claude and GPT, called directly through the [API]{.gls key=api}, bounced back an error with a content policy message. I tried several times, in fresh sessions, with clean context. Nothing.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Looking at the list, you could guess what had set off the alarm:

- a 2009 post about Steve Jobs's 2005 Stanford commencement speech, which mentions cancer because Jobs talked there about the diagnosis he had received [@jobs2005stanford];
- two Ayn Rand chapters I had translated years earlier, on the rights of man and on argument;
- a post about the money speech from *Atlas Shrugged*, also by Ayn Rand;
- an anti-Nazi post, blocked, by all appearances, just because the word "nazi" showed up in it, even though the whole text is a critique;
- an essay on democracy and ethics that broke on every attempt.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
None of those posts has anything dangerous in it. One talks about illness, another about political philosophy, another criticizes the Nazis. Apparently the companies' automatic filter measures with a thick ruler: brush up against a sensitive topic and it refuses, without weighing the context.

The way out came from home. I loaded onto my own computer Qwen 3.5 35B, an [open model]{.gls key=modelo-aberto} from China's Alibaba, the kind anyone can download and run without asking anybody's permission (@sec-ch13 covers what that takes) [@qwen2026qwen35]. With no corporate filter in the way, the model read the posts, understood the context and translated everything without drama.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
In other words: a Chinese model translated the posts that the Western models refused, including one against Nazism. I can't help finding this slightly hilarious.

Behind the joke there's a practical lesson. Commercial models will always carry the policy of the company selling them, and that policy is applied preemptively. For anyone using them in production, it's a real trade-off: you get fluency and capability, and you lose control the day your topic brushes up against whatever the company decided is sensitive.

> The only real wall that weekend was the companies' content filter, and the one that jumped it was a model running at home.

## The Way Back

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
Since I was already elbow-deep in it, I took the chance to solve the opposite side. The 2008 interviews and the 2017 and 2018 posts that were born in English got Portuguese versions, by the same route, just in reverse. The agent also adjusted the little program that builds the blog's index, so it generates one list per language.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
On April 9, when I finally published the anniversary post, half the blog was bilingual. What was left was mostly old tips about software versions that don't even exist anymore, stuff it made more sense to delete than to translate.

The barrier to reaching readers outside Brazil, which I had carried for two decades, had become cheap enough that I no longer had an excuse.

<!-- src: 2026/04/09/20-anos-de-blog-o-ano-em-que-a-ia-finalmente-me-deixou-traduzir-tudo -->
I knew the Qwen that rescued those six posts from somewhere else. In those same weeks, I had been pitting models against each other on a programming test I had built myself, trying to find out which one was best. It looked like a simple question, with the answer in a table. Over the following months I found out that measuring AI models is far trickier than translating twenty years of blog posts.
