---
id: apbolhas
chapter: "Three Bubbles"
sources:
  - {post: 2018/12/26/akitando-34-voce-nao-sabe-nada-de-enterprise-conhecendo-a-sap, sha256: "46691d1aa6f8602ea97cfb27c0610c79945c18d19fdf844aed3011108f5150fb"}
  - {post: 2019/06/11/akitando-50-a-bolha-de-startups-vai-estourar-winter-is-coming, sha256: "ef99201b54eac4d40fa676dd8c2b21cba025e15843c437512218e253bc570a94", commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"}
  - {post: 2021/06/22/akitando-100-mercado-financeiro-pos-pandemia-a-tempestade-perfeita, sha256: "04d2af19a6d40c3915c19ae146e71b3806843b736d6c932abd86444429784740", commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"}
  - {post: 2022/11/22/akitando-132-rant-a-bolha-de-startups-estourou, sha256: "0ab9f5cdffe6b1d0ce41ca3642c8c17c3369c25f7e244e99e4384ae46d183fc7", commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"}
  - {post: 2023/02/14/akitando-138-meu-comeco-de-carreira-durante-a-bolha-1997-a-2002-bug-do-milenio-crash, sha256: "79a02c73df595ddf8952c7bfbbd8023f51a3297b259610afa65901112dfe4160", commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"}
refs_projects: []
blog_commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"
translated_from: {file: book/pt/apbolhas.md, sha256: "fced13b84d28f49d610ca99547807f99dc02dbb0ffa613a3cbe9ff3100a9ac08"}
---

# Three Bubbles {#sec-apbolhas}

<!-- src: original -->
One question kept coming back all through 2026: is the career over? I don't have a crystal ball, but I have something that helps more: I've watched the cycle up close three times, from inside the tech market, and all three left numbers behind.

This appendix puts the three side by side. For each one: what happened, what was left afterward and what I did in the middle of it. The story of the second, the programming bubble, is told in @sec-ch18; here it sits next to the other two, which is where the pattern becomes visible.

![Three bubbles on a single line, from 1995 to 2026, with my own path underneath.](assets/figures/en/apbolhas-linha.png){#fig-apbolhas-linha fig-alt="Timeline from 1995 to 2026 with three bands." fig-desc="Timeline from 1995 to 2026 with three bands. The internet, 1995 to 2002: Nasdaq peak on 10 March 2000 and bottom on 9 October 2002, 78% lower. Free money, 2010 to 2022, with two hatched stretches of rates near zero, December 2008 to December 2015 and March 2020 to March 2022, and the tech layoffs right after: about 165 thousand in 2022 and 263 thousand in 2023. AI, from ChatGPT on 30 November 2022, still open. Underneath, my own line: first job in 1996, the dot-com closes and I move to SAP in 2001, Rails in 2007, Codeminer 42 in 2011, Akitando from 2018 to 2023 and this book in 2026."}

## The Internet, 1995 to 2002

<!-- src: 2023/02/14/akitando-138-meu-comeco-de-carreira-durante-a-bolha-1997-a-2002-bug-do-milenio-crash -->
The Nasdaq index, which concentrates the tech companies on the American stock exchange, closed at its peak on March 10, 2000. From there it fell until October 9, 2002, losing about 78% along the way [@fred2026nasdaq]. It only returned to the peak value in 2015. In between, hundreds of dot-coms shut their doors.

<!-- src: 2019/06/11/akitando-50-a-bolha-de-startups-vai-estourar-winter-is-coming -->
What was left was the infrastructure. In the euphoria, companies buried so much optical fiber that a good part of it sat unused for years, and that excess is what made the internet of the following decade cheaper [@wikipedia2026darkfibre]. The internet didn't stop: Google and Amazon became giants precisely in the dry years that came after the crash.

<!-- src: 2023/02/14/akitando-138-meu-comeco-de-carreira-durante-a-bolha-1997-a-2002-bug-do-milenio-crash -->
I went through that bubble from the inside. Between 1996 and 2001 I passed through an agency, an internet provider and a dot-com, and in 2001 the dot-com I worked at closed. A week later I was at a small consultancy that worked with SAP; @sec-ch18 tells about that week [@akitando138].

<!-- src: 2018/12/26/akitando-34-voce-nao-sabe-nada-de-enterprise-conhecendo-a-sap -->
I stayed about five years there, integrating systems at large companies. It's where I learned that the business rules of a big company can't be guessed from the outside, a lesson that returns in @sec-ch20.

<!-- src: 2023/02/14/akitando-138-meu-comeco-de-carreira-durante-a-bolha-1997-a-2002-bug-do-milenio-crash -->
In 2023, looking back, I summed up what got me through that time without major damage:

> I never defined myself as an "ASP programmer" or a "Java programmer" or a "SQL Server administrator." My specialty wasn't any of those tools.

## Free Money, 2010 to 2022

<!-- src: 2021/06/22/akitando-100-mercado-financeiro-pos-pandemia-a-tempestade-perfeita -->
After the 2008 crisis, the American central bank kept interest rates between zero and 0.25% from December 2008 to December 2015, and went back to them from March 2020 to March 2022 [@fed2026openmarket]. With fixed income paying almost nothing, money went chasing risk: tech stocks, startup investment funds and whatever else promised growth. From 2010 or so, the programming market lived through a decade of easy hiring.

The clearest symptom came at the end. The shell companies created just to buy another company and take it public without the usual scrutiny, the SPACs, numbered 59 in 2019, 248 in 2020 and 613 in 2021 [@spacinsider2026stats].

<!-- src: 2022/11/22/akitando-132-rant-a-bolha-de-startups-estourou -->
Then inflation came back, and rates rose from nearly zero to 4.25% to 4.50% in 2022 alone [@fed2026openmarket]. Money went back to fixed income and tech companies laid people off: about 165,000 in 2022 and more than 260,000 in 2023, by the count of layoffs.fyi, which tracks layoffs in the sector worldwide [@layoffsfyi2026tracker].

What that bubble left was a whole generation of programmers, some of them trained in a hurry in courses lasting weeks, and companies used to solving everything by hiring more people. @sec-ch18 tells what happened to volume without value when the money dried up.

<!-- src: 2019/06/11/akitando-50-a-bolha-de-startups-vai-estourar-winter-is-coming -->
In this one I did something else: I warned. Akitando, my channel from 2018 to 2023, was born to teach what survives bubbles, and the warnings, from June 2019 to November 2022, are told with dates in @sec-ch18.

<!-- src: 2021/06/22/akitando-100-mercado-financeiro-pos-pandemia-a-tempestade-perfeita -->
The signs of a company fattening itself up to be sold, which I described on the channel in 2021, return in @sec-ch14 for reading the 2026 prospectuses.

<!-- src: 2022/11/22/akitando-132-rant-a-bolha-de-startups-estourou -->
And I got the calendar wrong twice. The turn I guessed for 2021 came in 2022, pushed back by the pandemic. And the second leg of the fall, which I expected for 2023, never came: the Nasdaq rose about 43% that year, pulled up by the big companies and the AI wave, while employment in the sector stayed weak [@fred2026nasdaq; @layoffsfyi2026tracker]. A warning is for getting prepared; nobody gets the calendar right.

## AI, Since November 2022

<!-- src: original -->
ChatGPT came out on November 30, 2022 [@openai2022chatgpt], eight days after I published the episode about the crash. The money that had fled the startups came running back, now for those who sell models, graphics cards and data centers. @sec-ch14 shows how much money that is and who profits from the rush.

This third one isn't over, and I can't tell whether it will burst like the others, or when. I do know what it has already left: models that work, several of them open and running on a machine at home (@sec-ch13). Whether the data centers will be the optical fiber this time, left over and cheap after a crash, is an open question.

<!-- src: original -->
What I did in this one is the book you're reading. In January 2023 I said on the channel that the excitement about AI is inversely proportional to the knowledge about AI (@sec-ch01). In 2026 I went to measure: I spent the year using, testing and breaking these tools on real work, and noted where they pay off and where they mislead.

## Is the Career Over?

<!-- src: original -->
Three cycles don't make a law, and I won't pretend they do. But they repeat a pattern you can check in each one.

The companies that lived off the bubble died, and the technology stayed: the internet after 2002, apps and the cloud after 2022. Work that was only volume disappeared, whether the website cataloger or the programmer who only assembled forms. And those who defined themselves by the fashionable tool suffered more than those who defined themselves by the problem they knew how to solve.

<!-- src: original -->
The pattern guarantees nothing for anyone in particular. Good people lost their jobs in both crashes too, and I was lucky to get a phone call in the right week. What the cycles show is which side of the transition usually makes it across.

> From what I've seen three times, the bubble ends the shortcut. The profession has gone on, changing tools, in the hands of those who learn to solve the problem underneath it.
