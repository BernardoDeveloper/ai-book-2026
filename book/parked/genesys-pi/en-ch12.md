<!--
PARKED (author decision, 2026-10-13; ledger: book/integration.yml, Genesys PI entry).
Origin: book/en/ch12.md, section "## The Brazilian Mystery", which sat between
"### The Size of What I Proved" (end of the Kimi case) and "## What You Can Know from the Outside".
Translation of book/parked/genesys-pi/pt-ch12.md; the block below is verbatim, with its provenance markers and figure.
Restore: paste it back at that spot; re-add posts
2026/09/23/llm-benchmark-v4-genesys-pi-novo-competidor-brasileiro and
2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro
to ch12's front-matter sources (and remove them from `excluded` in book/outline.yml);
restore "as with Kimi and Genesys PI" in the closing section.
Also restore the ch12 refs_projects entries lua-forensics/FINDINGS.md and
model-forensics/FINDINGS.md, the @fig-ch12-impressao-digital credit, and the apA entries.
-->

## The Brazilian Mystery

<!-- src: 2026/09/23/llm-benchmark-v4-genesys-pi-novo-competidor-brasileiro -->
Two weeks later, the same question caught up with me from an unexpected direction. In September 2026, people from LUA Vision, a São Paulo company founded in late 2025, reached out on LinkedIn offering test access to Genesys PI, their model, launched in April [@luavision2026empresa]. The pitch was that they trained their own model for Brazilian reality, with labor law, the CLT versus PJ split (salaried employee versus contractor) and the local tax structure, instead of reselling a foreign model with a Portuguese layer on top.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Before any numbers, what I put on record in the two pieces I wrote about the case. I have no business relationship with LUA Vision. I'm not a partner or an investor, I signed no contract and no NDA, and I received nothing beyond a free evaluation key. Nothing I published went through them first.

<!-- src: original -->
And a word of caution, because the case is still open: there isn't enough information for a conclusion about Genesys PI or LUA Vision. What follows is a record of the tests I ran, and it shouldn't be read as a recommendation or an endorsement of any product, company or investment.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
I never saw any internal data; everything that follows is black-box testing on the API, plus public information.

### What the Model Did

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
In the first round, on September 23, I ran both tiers of the model, called House and Enterprise, on the version of my benchmark with security traps planted along the project, which @sec-ch11 explains. House scored 83.5, tied with Grok 4.7, in the middle of the pack. Enterprise landed one step below.

<!-- src: 2026/09/23/llm-benchmark-v4-genesys-pi-novo-competidor-brasileiro -->
That day I wrote, excited, that I had always figured training a [frontier model]{.gls key=modelo-de-fronteira} from scratch in Brazil wasn't viable, and that LUA had proved me wrong. A week later, with more tests in hand, I was separating far more carefully what I had measured from what the company said.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
The company fixed a defect in the API and I ran it again. House climbed to 95.5, tied with some of the best in the table. But Enterprise stayed practically the same, and in the same week GPT-5.5 fell from 100 to 91 on an identical repeat, with nothing changed. A single round can't tell improvement from noise (that's the subject of @sec-ch11), so I kept the first round as the official table entry, precisely so as not to reward an isolated run.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
I also asked it to audit the security of my open-source sandbox, the one from @sec-ch15, in parallel with another model. In a small comparison, one project and one round, Genesys PI's report was the stronger of the two, and I went off to fix its list.

The model exists, works and is good at what I measured. The question everyone sent me was a different one.

### "Isn't This Just a Qwen with a Sticker?"

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
I asked that question too. The industry consensus is that training a frontier model costs tens or hundreds of millions of dollars, and a small company, without a billion-dollar funding round, shouldn't get anywhere close. The cheapest hypothesis is that there's another model underneath.

Three versions of the suspicion reached me:

- it's a Qwen or a DeepSeek, Chinese open models, under another name;
- it's gpt-oss, OpenAI's open model, in different clothes;
- the API is just a middleman passing the requests along to Claude or GPT.

In a black box, without access to the weights, it's impossible to state with certainty where a model came from. What you can do is rule out hypotheses, one at a time.

### The Fingerprint

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Before processing any text, every model breaks it into pieces, the [tokens]{.gls key=token} from @sec-ch01. What does the breaking is the [tokenizer]{.gls key=tokenizador}, a vocabulary with its own rules, and each model family has its own. The same sentence in Chinese, the same run of digits, the same compound emoji turn into different numbers of tokens in different families.

And here's the decisive point: whoever fine-tunes or keeps training a model inherits its tokenizer. Swapping the vocabulary means training again from scratch. That's why the tokenizer works as a fingerprint of lineage.

<!-- src: ref:llm-coding-benchmark/lua-forensics/FINDINGS.md -->
I measured how many tokens LUA's API charged for a battery of texts: Chinese, accented Portuguese, English, runs of digits, compound emojis. I subtracted the system prompt they inject and compared against the tokenizers of the main families, running on my machine. A digit run that Qwen and DeepSeek count as 200 tokens, LUA counted as 67. Adding up the differences across all the texts, OpenAI's public tokenizer, called o200k, came in 2 tokens away.

The next closest, Llama 3's, came in at 68. Qwen's, at almost 200.

![The same sentence becomes a different number of tokens in each model family; the count works as a fingerprint.](assets/figures/en/ch12-impressao-digital.png){#fig-ch12-impressao-digital fig-alt="Table showing how many tokens the same Chinese passage, the same digit run and the same compound emoji become in each tokenizer. The tested API counts 42, 67 and 168. OpenAI's o200k counts 42, 67 and 169, and lands 2 tokens away summed over all texts. Llama 3 lands at 68, cl100k at 134, Qwen at 193, DeepSeek at 255 and Mistral at 289. At the bottom, the note: same count doesn't mean same weights."}

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
In September, that knocked down the first suspicion. No Qwen, DeepSeek, Llama or Mistral uses that vocabulary, and no fine-tune on top of them could acquire it.

The second one weakened too. gpt-oss uses a variant of the same vocabulary with its own special markers, and on LUA's API each of those markers cost about 4 tokens, like ordinary text. On top of that, gpt-oss couldn't even finish my benchmark, in the same program where Genesys PI got through all seven stages. A light sticker on top of gpt-oss doesn't do that.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
The third suspicion, the middleman, was tested through the API's behavior. It rejects a series of configuration parameters that OpenAI's API accepts, and others that any ordinary open-model server would accept. A transparent [proxy]{.gls}, one that just passes the request along, would accept those parameters and leave a trail.

And there's the performance argument. GPT-5.5 and GPT-6 Luna caught, unprompted, two very well disguised traps in my test. Genesys PI missed those same two, consistently, in every round. A relay doesn't end up consistently weaker than the model behind it, on one specific point.

### Three Different Directions

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
The result that interested me most was a different one. I compared Genesys PI's error signature with that of all the models in the table.

The tail of errors looked like Qwen's, but that was an effect of the score band: every model in the 80s misses those two traps, from any family. One rare fix looked like GPT-6 Luna's. The tokenizer looked like OpenAI.

A clone or a relay resembles a single model on every axis at once. Genesys PI didn't resemble any model in the table on every axis.

> A black-box test rules out hypotheses. It doesn't prove where anything came from.

### What No API Test Gets Past

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Here's the limit. A new model, with its own weights and OpenAI's public vocabulary, may have been trained from scratch on its own data. Or it may have been trained from scratch imitating answers from Claude and GPT, which is distillation. Both stories produce exactly the same observations I made.

A grid of 20 questions comparing the style of the answers with that of several possible "teachers" gave a null result, consistent with both stories.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
Another limit is the size of the list: "I found no kinship" means "I found none among the models I tested," and there are dozens I didn't test.

I also recorded an inconsistency, the first question I'd put to the company.

LUA's published research deals with the "token tax," the extra cost that a vocabulary optimized for English charges Portuguese. Except the API I measured breaks up Portuguese exactly the way that OpenAI vocabulary does. Adopting it is the cheap, professional choice any small lab would make, and it says nothing about lineage; but the research and the product tell different stories on this point.

<!-- src: ref:llm-coding-benchmark/model-forensics/FINDINGS.md -->
In October, I ran a more rigorous battery, with hundreds of texts I hadn't used before and known control models, and it left me more cautious. The API's token count matched the OpenAI vocabulary on all 768 new texts.

But that only describes how the API counts tokens. Which weights sit behind it is another question, and the same vocabulary shows up in other open models I didn't even have on the list, including some from other companies.

Genesys PI's answers landed far from the GPT-4o versions I tested, a hint against a simple relay of those versions, but the positive and negative controls overlapped and the protocol didn't allow any formal classification. No origin was proved, none was conclusively ruled out, and I can't put a probability number on any origin hypothesis.

### Checked, Claimed, Open

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
The most useful tool to come out of this case is a habit: separating what I measured from what I was told. It works for any AI announcement, from a big company or a small one.

Checked by me:

- Genesys PI exists, responds and completes a hard benchmark in the tier A and B range of my table;
- the API's token count matches OpenAI's public vocabulary and diverges from Qwen, DeepSeek, Llama and Mistral;
- the API doesn't behave like a transparent relay, and the model has stable weaknesses of its own;
- stock gpt-oss doesn't explain the result.

Not checked, only the company's word:

- that the model was trained from scratch, not distilled;
- that the architecture is new, a generation beyond the [transformer]{.gls};
- that training happened on ordinary hardware, AMD and ARM, without NVIDIA cards, in a few months;
- that a better model is on the way.

<!-- src: 2026/09/23/llm-benchmark-v4-genesys-pi-novo-competidor-brasileiro -->
The same standard applies to the public material: LUA's papers sit in a preprint repository, with no peer review, and the LiveBench score that shows up in its material was self-reported, in a request to be added to the leaderboard that, as of September, no maintainer had confirmed [@livebench2026issue370].

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
If the strongest claims are true, NVIDIA's grip on model training takes a serious blow. A claim of that size demands evidence of that size, and I don't have it. What would settle it is documents: the tokenizer file, the training recipe, the loss curve, a held-out test I run myself.

On the other side of the scale, fooling this analysis would take an enormous amount of work: adopting OpenAI's vocabulary, masking the model's identity, building an API that rejects exactly the right parameters, keeping stable weaknesses across several rounds and still completing a hard benchmark at a high level. Past a certain point, a convincing fake of a model is indistinguishable from having a model.

<!-- src: 2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro -->
My position, as I close this chapter, is the same as on September 30: a model that behaves like an independent one, on top of a public vocabulary, with an origin no outsider can certify. More than I expected from a company this size, less than their website sells.
