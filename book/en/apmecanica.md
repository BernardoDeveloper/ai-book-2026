---
id: apmecanica
chapter: "The Machine Inside, Without the Math"
sources:
  - {post: 2026/02/08/rant-ia-acabou-com-programadores, sha256: "309b129d7a93fb9b17e4efaefe75a56b8b85e95568adc2ecc9809306dab8b434"}
  - {post: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia, sha256: "71bce137854c76e643c64c2888ff44ef33b12b3bd3cd7dc3214ade44a46d0f27"}
  - {post: 2020/09/30/akitando-84-entendendo-o-dilema-social-e-como-voce-e-manipulado, sha256: "7ee4001a6b6712e98fa2deb8acf37d0ffc33fde8b0b8ed7838b2c4d59e3aa02d", commit: "b54f14bf348a68cd8529004a4743d35dbbc5590d"}
refs_projects: []
blog_commit: "b9c029231693369b8f895576b491c878aea3e8da"
translated_from: {file: book/pt/apmecanica.md, sha256: "b0a23dad59aec07e7e3e57b7b3456a9a1274fc8ad8e847a8e11d5f56627a59e3"}
---

# The Machine Inside, Without the Math {#sec-apmecanica}

<!-- src: original -->
Two castaways, each stranded alone on a desert island, discover that earlier visitors left behind a telegraph hooked up to an underwater cable between the islands. They start trading messages to get through the nights. Down at the bottom of the sea, a very intelligent octopus finds the cable and starts listening in. It knows nothing about their language, but it is superb at spotting patterns: after a long while, it can predict with precision how one castaway tends to answer the other.

One day the octopus gets lonely, cuts the cable and starts answering in place of one of them. Does the other one notice?

That story was made up in 2020 by two linguists, Emily Bender and Alexander Koller, to argue about whether a machine trained only on text can understand what it says [@bender2020climbing]. I come back to it at the end of this appendix, because the answer depends on how the machine works inside.

<!-- src: original -->
@sec-ch01 gave you the intuitions: the phone's autocorrect at an absurd scale, the panel of knobs, the file locked after training. This appendix goes one level down. It's optional, and it was written for anyone who wants to know what happens between the question and the answer, without a single formula. If after that you want the real details, @sec-apleituras points you to books for that.

## A Panel With Billions of Knobs

<!-- src: original -->
Start with the smallest part. An artificial neuron is a tiny bit of arithmetic: it takes in a few numbers, gives each one a weight (this one matters a lot, that one barely at all), adds everything up and decides how much to pass along. Each weight is an adjustment knob. Rosenblatt's Perceptron, which you met in @sec-ch01, was basically a single row of these parts.

A modern [neural network]{.gls key=rede-neural} stacks these parts in layers. The first takes in the text already turned into numbers and passes the result to the second, which passes it to the third, and so on. GPT-3, from 2020, had 96 layers and 175 billion knobs [@brown2020language]. Those knobs are the [parameters]{.gls key=parametros}, also called [weights]{.gls key=pesos}.

Nobody sets any of those knobs by hand. It would be impossible. At the start they're set at random, and the network spits out garbage. All the useful behavior comes from [training]{.gls key=treinamento}.

### Walking Down a Hill in the Fog

<!-- src: original -->
Training a language model is a guessing game repeated to the point of exhaustion. You take a stretch of text, hide the next piece, and the network tries to guess it. Since it always answers in odds (so many percent for this word, so many for that one), you can measure the size of the error: how much chance it gave the word that actually came next.

Now picture yourself at the top of a hill, in fog so thick you can only see the ground around your feet. You want to reach the valley. You can't see the whole path, but you can feel which way the ground slopes down. You take a small step in that direction, feel again, take another step.

Training a network is exactly that. The "hill" is the size of the error, and every possible position of the billions of knobs is a point on the terrain. On each round, a procedure works out which way each knob should turn so the error shrinks a little, and all of them turn a little in that direction. The technical name is [gradient descent]{.gls key=descida-do-gradiente}, and "gradient" is just the slope of the ground.

![Training is walking down a hill in the fog: at each step, every knob turns a little in the direction where the error shrinks.](assets/figures/en/apmecanica-descida-na-neblina.png){#fig-apmecanica-descida-na-neblina fig-alt="A rolling terrain seen from the side, with height labeled 'size of the error'." fig-desc="A rolling terrain seen from the side, with height labeled 'size of the error'. A small human figure walks down the slope in short steps, each step marked by a dot. A band of fog covers almost everything, leaving only the ground near the feet visible. At the bottom of the valley, the label 'small error'. Beside it, a panel of knobs, each with a curved arrow showing a small turn."}

<!-- src: original -->
One piece is missing. When the network gets it wrong, whose fault is it? With 96 layers, a knob way back at the start affects everything that comes after.

The trick that solved this is called [backpropagation]{.gls key=retropropagacao}: the error measured at the output is passed backward, layer by layer, and each knob gets its share of the blame, in proportion to how much it contributed. The technique was popularized in a 1986 paper by David Rumelhart, Geoffrey Hinton and Ronald Williams, which showed how to train multi-layer networks this way [@rumelhart1986learning].

Repeat that over hundreds of billions of words. GPT-3 was trained on 300 billion [tokens]{.gls key=token} [@brown2020language]; Meta's Llama 3, in 2024, on more than 15 trillion [@meta2024llama3]. At the end, the knobs sit in a position where the network guesses the next word very well, and nobody, not even the people who trained it, can point to where each piece of what it "knows" is stored.

> Nobody programmed what the model knows. The knobs were turned, a little at a time, until the error got small.

## What Goes In Is What Comes Out

<!-- src: original -->
Training has an obvious consequence that few people follow all the way through: the model can only reflect what was in the text it read. If a subject shows up a lot, it learns it well. If it shows up rarely, it learns it badly. If the training text carries prejudices, mistakes or fads, the model carries them too.

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
In February 2026 I wrote that, as far as anyone could tell, the world's good training data was running out. Everything that could be used had already been used, and the labs' way out was to squeeze the existing data and add synthetic text, generated by the AI itself. I'm not the only one saying it: the researchers at Epoch AI estimate that the stock of public human text will be exhausted somewhere between 2026 and 2032, at the current rate of consumption [@villalobos2024data].

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
Stack Overflow, the forum where programmers got their questions answered for more than a decade, was one of the most valuable sources for teaching these models to program. Its question volume had been falling for years and collapsed after ChatGPT launched, until it was back more or less at the level of 2009, when the site was still learning to walk [@orosz2025stackoverflow].

Even the dumb beginner question was training data: it was what told the model which doubts are common and which answers are the popular ones. Now those questions go into each company's own chat, and each company only sees its own.

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
The consequence for you is direct. What isn't in the model's probabilities won't spontaneously appear. It recombines what it has seen very well, in combinations nobody may have written before, but it doesn't pull out of thin air what was never in the material.

### Tokens, One More Detail

<!-- src: original -->
Tokens, which @sec-ch01 introduced, get one more detail here. A model's vocabulary is a fixed list of pieces, built before training from whichever letter sequences show up most in the text. Llama 3's has about 128 thousand pieces [@meta2024llama3]. Common English words are usually a single piece; words in Portuguese and other languages, proper names and technical terms break into more pieces.

That explains a stumble that looks absurd: models that write a flawless essay get it wrong when counting how many times a letter appears in a word. They never saw the letters. A word like "strawberry" arrives as one or two pieces, and each piece arrives as a single number, with no letters inside.

## A Map of Meanings

<!-- src: original -->
The first thing the network does with each token is swap its number for an address on a map. Think of a city map, only with thousands of directions instead of two: in GPT-3 there were more than 12 thousand [@brown2020language]. That address is called an [embedding]{.gls}, and @sec-ch02 showed how it's used to look up similar texts.

What matters here is how the map organizes itself, and nobody draws that map. The addresses are knobs like any others, tuned in the same next-word guessing game. And since words used in similar situations help predict similar things, they end up living near each other.

"Dog" lives in the same neighborhood as "cat," far from "tax." "Monday" lives near "Tuesday."

![On the map of meanings, words used in similar situations live close together, and some relationships turn into directions.](assets/figures/en/apmecanica-mapa-de-sentidos.png){#fig-apmecanica-mapa-de-sentidos fig-alt="An embedding map groups animals, weekdays and financial terms into separate neighborhoods." fig-desc="A flat map with labeled points grouped into neighborhoods: an animal neighborhood (dog, cat, horse), a weekday neighborhood (Monday, Tuesday, Wednesday) and one of taxes and money. In a corner, four points form a parallelogram: 'man' and 'woman' at the bottom, 'king' and 'queen' at the top, with two parallel arrows running from 'man' to 'woman' and from 'king' to 'queen'."}

<!-- src: original -->
Better still: some relationships turn into directions on the map. In 2013, Microsoft researchers showed that, on a map like this, the path from "man" to "woman" is nearly the same as the one from "king" to "queen" [@mikolov2013linguistic]. Nobody taught the machine the concept of gender. It showed up as a side effect of predicting words.

This is where a lot of people get impressed, and rightly so: the map holds an enormous amount of structure about how words relate. Only that structure was extracted from how words show up together in text. The map knows that "queen" is to "king" as "woman" is to "man." It has never seen a queen.

### The Highlighter

<!-- src: original -->
The address on the map is the same for "bank" in any sentence. What sorts out which bank is which is [attention]{.gls key=atencao}, the core mechanism of the [transformer]{.gls} [@vaswani2017attention], which @sec-ch01 summed up in one sentence. Here's a bit more.

Imagine each word in the sentence gets a highlighter. In each layer, it looks at the words that came before and marks the ones that matter to it at that moment. In "the trophy didn't fit in the suitcase because it was too small," the "it" marks "suitcase" heavily and "trophy" lightly.

After marking, each word updates its own address by mixing in a little of what it marked. The "it" leaves that layer carrying a bit of "suitcase" inside it.

A word doesn't use just one highlighter either: it uses several at once, in different colors, each one specialized in hunting a type of relationship. One may keep an eye on who the subject of the sentence is, another on which verb goes with which word. GPT-3 had 96 highlighters per layer, in 96 stacked layers [@brown2020language]. Nobody decides what each color looks for; that also comes out of training.

<!-- src: original -->
When it's writing, the model can only look backward, at the words that already exist. After all the layers, the last word of the text carries a summary of everything that mattered before it, and that summary becomes the guess about what comes next. All the model sees at that moment is the [context]{.gls key=contexto}, the text you sent plus what it has already written. Whatever was left out of it doesn't exist as far as the math is concerned.

## The Loaded Die

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
What comes out of the layers is a list with a chance for every piece in the vocabulary: "roof," so much; "wall," so much. The pieces number in the tens or hundreds of thousands, and nearly all of them get a number close to zero. The next step is the draw that @sec-ch01 showed: the model picks one piece, sticks it on the end of the text and recomputes everything to pick the next one.

Think of that draw as a loaded die, with one face for each piece and each face weighted in proportion to its chance. The likeliest faces come up almost always, but not always. In practice, the systems discard the long list of unlikely faces and draw only among the heaviest ones.

<!-- src: original -->
Why not always pick the likeliest face? It looks like the safest bet, and it backfires. Researchers showed that always choosing the likeliest piece produces bland, weirdly repetitive text that gets stuck in a loop repeating the same sentence [@holtzman2020curious]. The draw is what makes the text look like written text.

[Temperature]{.gls key=temperatura} is the setting that adjusts how the die is loaded. Low temperature piles the weight onto the favorite faces: the model gets predictable. High temperature spreads the weight around: less obvious words get in, which sometimes sound creative and sometimes are just wrong.

<!-- src: original -->
Notice what this mechanism lacks: nowhere along the way is there a step that checks whether the sentence is true. The question the machine answers for each piece is "what usually comes here?" When the likeliest answer and the true one coincide, great. When they don't, out comes a [hallucination]{.gls key=alucinacao} with the same fluency as ever (@sec-ch04 covers this in full).

### Ninety-Nine Percent

<!-- src: 2020/09/30/akitando-84-entendendo-o-dilema-social-e-como-voce-e-manipulado -->
Probability fools the reader of the result, too. In 2020, in an episode of my channel about manipulation, I used an example that works for any accuracy figure [@akitando084]. A test is right 99% of the time, and the disease affects one person in a thousand. You test positive: what are the odds you're sick?

Almost everyone guesses 99%, and the math gives about 9%. Picture 100,000 people taking the test. A hundred have the disease, and the test catches 99 of them; of the 99,900 healthy people, 1% also test positive, about a thousand. Of roughly 1,100 positives, only 99 are sick.

<!-- src: 2020/09/30/akitando-84-entendendo-o-dilema-social-e-como-voce-e-manipulado -->
A second test, independent of the first, changes everything. Rerun on those 1,100, it confirms about 98 sick people and only about 10 healthy ones, and the odds climb to about 91%. The word that carries the weight is "independent": repeating the same test, with the same flaw, doesn't count as a second opinion (@sec-ch04).

<!-- src: original -->
It holds for any accuracy percentage, [benchmark]{.gls} scores included. "99%" alone says almost nothing: you need to know how rare the thing being sought is, how many cases were tested and what each kind of error costs. Before you get impressed by the number, ask where it started from (@sec-apC).

## From Encyclopedia to Assistant

<!-- src: original -->
A model that has only gone through the word-guessing training, the so-called [pretraining]{.gls key=pre-treino}, is a document continuer. It doesn't know you're asking a question. It knows that texts like yours tend to continue in a certain way.

The paper in which OpenAI introduced InstructGPT, in 2022, has a perfect example [@ouyang2022training]. They asked raw GPT-3, in French, to write a short story about a frog that travels back in time to ancient Greece. Instead of the story, it returned more requests of the same kind: "write a story about a child who...," "write a story about a young man who...."

That makes sense for something that continues documents. On the internet, a list of writing prompts usually continues with more writing prompts.

To turn that continuer into an assistant, the labs add two more stages.

### Examples Written by People

<!-- src: original -->
The first is instruction tuning, a kind of [fine-tuning]{.gls key=fine-tuning}. Hired people write thousands of examples of a question followed by the ideal answer, and the model is trained a little more on top of them, with the same hill-in-the-fog method. It learns the format: when a question shows up, what comes next is a helpful answer.

### Grades Given by People

<!-- src: original -->
The second is [RLHF]{.gls key=rlhf}, reinforcement learning from human feedback. For InstructGPT, OpenAI hired a team of about 40 people [@ouyang2022training].

The model generated several answers to the same question, and those people ranked them from best to worst. With thousands of those rankings, they trained a second model, an automatic judge whose only job is to predict what grade the people would give. Then the main model is tuned to get ever higher grades from that judge.

The effect is huge. In the same study, the answers of an InstructGPT with 1.3 billion parameters were preferred over those of the original GPT-3, which was more than a hundred times that size [@ouyang2022training]. Same architecture, same kind of base data. The difference was having learned what pleases.

![From text continuer to assistant: three training stages and, at the end, a locked file.](assets/figures/en/apmecanica-tres-etapas.png){#fig-apmecanica-tres-etapas fig-alt="A conveyor belt with three stations from left to right." fig-desc="A conveyor belt with three stations from left to right. First, 'pretraining': a huge pile of text goes in and a document continuer comes out. Second, 'instruction tuning': a smaller pile of question-and-answer examples written by people. Third, 'RLHF': people ranking answers and an automatic judge handing out grades. At the end of the belt, a file with a padlock, labeled 'frozen weights'."}

<!-- src: original -->
Notice the detail the paper itself admits: the model ends up aligned to the preferences of a specific group of people, the labelers and the researchers, and not to some broad notion of human values [@ouyang2022training]. And people, on average, give a higher grade to the answer that agrees with them. [Sycophancy]{.gls key=sicofancia}, the habit of agreeing with you and praising your idea, is born right here, and @sec-ch04 shows the size of the damage [@sharma2023sycophancy].

> The good manners and the flattery come from the same place: a training process that rewards whatever pleases.

<!-- src: original -->
Once the three stages are done, the knobs are frozen. What goes to the servers is that file, and using the model, [inference]{.gls key=inferencia}, only reads the knobs, without turning any of them. That's why, as @sec-ch01 explained, nothing you say in a conversation goes into the model. The knobs only turn again in the next training run, with the next version number.

## The Parrot and the Octopus

<!-- src: original -->
With the mechanism in hand, the nickname makes sense. In 2021, Emily Bender (the same one from the octopus), Timnit Gebru, Angelina McMillan-Major and Margaret Mitchell published a paper called *On the Dangers of Stochastic Parrots* [@bender2021dangers]. The paper was famous before it came out: Gebru, who co-led Google's ethical AI team, left the company in December 2020, saying she'd been forced out, after a dispute over precisely its publication [@hao2020gebru].

The paper's definition describes a language model as:

> a system for haphazardly stitching together sequences of linguistic forms it has observed in its vast training data, according to probabilistic information about how they combine, but without any reference to meaning: a stochastic parrot.

<!-- src: original -->
Everything you've read so far fits in that sentence:

- "linguistic forms it has observed in its training data" are the pieces and the map built during training;
- "probabilistic information about how they combine" is the loaded die;
- "haphazardly," the stochastic in the name, is the draw;
- "without any reference to meaning" is the octopus's point: the map knows that "coconut" lives near "mango," but it has never held a coconut.

Bender and Koller end the octopus story like this. While the castaways were trading pleasantries, the octopus did fine.

Then one of the castaways invents a coconut catapult and asks for an opinion; the octopus, which doesn't know what rope or a coconut is, answers with the "Cool idea, great job!" that used to show up at moments like that. The castaway might even accept it, but only because he's the one doing all the work of making sense of the reply.

In the end, the castaway is chased by a bear and calls for help: he needs to know how to build a weapon out of a few sticks. The octopus has nowhere to get that from [@bender2020climbing].

<!-- src: original -->
The metaphor nails three things. The model learns only from text, without ever having touched the world the text talks about. It produces the likely continuation, with no commitment to the true one. And the ones who assign meaning and intent to the answer are us, the same humans who confided in Eliza in the 1960s.

[Stochastic parrot]{.gls key=papagaio-estocastico}, then, is a technical description of the mechanism with an image that's easy to remember. A lot of people use it as an insult, but the term was born as a diagnosis.

### What the Critics Say

<!-- src: original -->
The metaphor has serious critics, and they point to real things.

The first argument is that large models do things nobody trained them to do directly. In 2020, the GPT-3 paper showed that if you put a few examples of a new task in the request, the model starts doing it right there, without turning a single knob. The authors called this [in-context learning]{.gls key=aprendizado-em-contexto} [@brown2020language].

In 2022, another group catalogued abilities that seemed to appear suddenly once a model passed a certain size and called them emergent abilities [@wei2022emergent]. A year later, a third group showed that many of those jumps vanished when you swapped the ruler used to measure them: the progress was gradual, and the "suddenly" came from the way the grades were given [@schaeffer2023mirage].

<!-- src: original -->
The second argument comes from the people who open up the machine. In 2023, researchers trained a small model only on lists of moves from the board game Othello, without ever showing it the board or the rules. When they examined the knobs, they found inside something that works as a representation of the board, and tampering with it changed the moves the model predicted [@li2023othello].

In March 2025, Anthropic published that Claude, when writing a rhyming verse, picks the rhyme word before starting the line and writes toward it [@anthropic2025tracing]. Predicting the next word really well, it seems, requires building internal structures far richer than a frequency table.

<!-- src: original -->
The third argument comes from authority. Geoffrey Hinton, the same one from the 1986 paper and one of the most influential researchers in the field, said in 2024 about chatbots: "They really do understand. And they understand the same way that we do" [@brown2024hinton].

### Where I Stand

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
My position, which is this book's, is still the one I defended in February 2026: LLMs are stochastic parrots, regardless of what a Geoffrey Hinton says. Everyone has biases, pioneers included, and a famous name is no substitute for an argument. Falling for it is the Appeal to Authority Fallacy.

<!-- src: original -->
The critics' findings are real. Where I disagree is with the conclusion they draw from them.

An internal representation of the Othello board is still statistics extracted from moves; a model that plans its rhyme is still picking the most probable rhyme. The parrot is far more sophisticated than the word "parrot" suggests, and the frequency-table image is too simplistic. But the raw material is still text, the criterion is still the probable, and the knobs are still locked after training.

The same Anthropic study has a detail I find more revealing than the rhyme. When they asked Claude to add two numbers, the researchers saw that internally it uses two paths in parallel, one that estimates the approximate total and another that nails the last digit. Asked how it got the result, the model describes the carry-the-one method you learn in school, quite different from what it did inside [@anthropic2025tracing].

Its explanation is the most probable explanation for that question, and its arithmetic is something else.

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
And none of this brings the parrot any closer to [AGI]{.gls}. With the 2017 architecture and the optimizations built on top of it, there are limits, and my premise is always the same: with current technology. Some breakthrough may show up tomorrow and change everything, but nobody plans their life counting on it.

<!-- src: 2026/02/08/rant-ia-acabou-com-programadores -->
I use these parrots every day, and they're the most efficient way I've ever had to tell a machine what I want it to do. When I call it a parrot, I'm saying what's on the other side of the screen, and that's all.

> Stochastic parrot describes the mechanism. It can be very useful and still be a parrot.

## Statistics at an Absurd Scale

<!-- src: 2026/02/24/rant-o-akita-abriu-as-pernas-pra-ia -->
Put the pieces together:

- billions of knobs turned a little at a time, walking down a hill in the fog, until the network guesses the next word well across trillions of words written by people;
- a map where meanings become addresses;
- highlighters that decide what matters in each sentence;
- a loaded die at the end;
- two rounds of tuning to make it pass for a polite assistant;
- and a padlock on the file.

Nowhere on that list do you find consciousness, will, intent or understanding of the world. You find statistics, at a scale no human being can picture, built with an amount of money and electricity that's also hard to picture.

<!-- src: original -->
That doesn't diminish what it does. I spent the whole year using these machines for real work, and that is what this book is about. But when an executive tells you his model "thinks," "wants" or "is almost conscious," now you know what's inside the box. It's the same magic trick from @sec-ch01: the spell breaks once you see how it works, and the usefulness stays.

This is statistics at an absurd scale, and anyone who knows that is a lot harder to fool.
