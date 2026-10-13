# Edition 1.0 (PT-BR): review packet for the author

Built 2026-10-13 from blog commit `b9c0292`. Files in `build/pt/`:

| File | What |
|---|---|
| `Competente-o-Suficiente.pdf` | Print edition, 6x9 in, 473 pages (blank versos, chapters open on the right) |
| `Competente-o-Suficiente-ebook.pdf` | Ebook PDF with the cover, 448 pages |
| `Competente-o-Suficiente.epub` | EPUB 3 (epubcheck 5.4.0: 0 errors, 0 warnings), for KDP and other stores |
| `index.html` (+ `book/`) | Web edition |
| `Competente-o-Suficiente.docx` | For editors who want Word |

Size: about 100,000 words of main text plus about 20,000 in appendices; 20
chapters, 2 interludes, front matter (preface, how to read, "Antes de
começar"), epilogue, afterword, 5 appendices, sources, image credits,
glossary (144 terms), references (292). 50 figures, all with provenance
records. 91 of the 96 AI-centred posts are used; 11 AI posts are excluded
with reasons (book/outline.yml).

Checks passing: provenance in sync with the blog, outline coverage, voice
lint on every unit, epubcheck, page audit (no split blocks, stranded
headings, gap pages, runt endings, oversized images or overfull lines).

## Status after 1.0.0-preview.2 (2026-10-13)

Settled from the sources or by the author's earlier answers:
2 (ch08's "mais de 25" quotes a critic from the 04/23 post; consistent with
30), 5 and 6 (cover and title shipped in both previews unchanged by the
author), 8 ("AI Lair" is the author's site, ai-toolkit-web; added to
`owned_names`), 9 (Altman photo replaced by a 2025 TED photo, CC BY 2.0),
10 (NBR 10520:2023 kept), 12 (aliases + `public_guard`), ai-jail README
(fixed upstream: "On by default"). Item 4 is being checked against archived
originals (`reviews/1.0.0-preview.2/pt/ch14-secondary-sources.md`).
Author's answers (2026-10-13): 1, Genesys PI stays, with a prudence
paragraph in ch12 (not enough information; not a recommendation or
endorsement of product, company or investment); 3, the NAS hypothesis
paragraphs in ch15 stay as they are; 11, the ISBN line is hidden until
`meta.isbn` is set. Item 7 (length) waits for the author's read.

Watch in future edits: the Genesys PI section (due diligence pending; any
new information or the author's change of mind may mean parking it, see
the impact map in the 2026-10-13 session: ch12 "O mistério brasileiro",
apA two entries, apC marker, refs luavision2026empresa and
livebench2026issue370, glossary proxy and tokenizador), and the ch15
"Minha hipótese" / "Três meses depois" pair, whose last sentence reads as
a contradiction (hypothesis vs conclusion) if it gets touched again.

## Decisions only you can make

1. **Unpublished research in ch12.** One paragraph on Genesys PI uses your
   October model-forensics findings that aren't on the blog yet (more
   cautious than the 30 Sep post: token counts match the OpenAI vocabulary
   but prove nothing about origin). It is self-contained and deletable.
   Keep it, or publish on the blog first?
2. **Years of experience.** ch06 says "30 anos" (02/20 post), ch08 says
   "mais de 25" (04/23 post). Pick one, or keep both.
3. **ch15 framing.** The October deletion incident is presented as not
   fitting your July hypothesis that vague prompts cause destructive agent
   actions (it came from an unchecked premise). Comfortable with that?
4. **ch14 claims resting on secondary coverage** (originals blocked or
   offline): David Sacks's "psyop", the Pirate Wires report, the
   Musk/Altman replies, OpenAI's own Navier-Stokes page. Keep as is, soften,
   or cut?
5. **Cover.** 1.0 uses concept D (kneeling robot, World's Fair crowd).
   Alternatives in `assets/cover/concepts/`. The title is set in Limelight.
6. **Title.** "Competente o Suficiente" was a working title from your
   10/12 post. Keep?
7. **Length.** 473 print pages. Chapters average ~5,000 words; a 10-15%
   tightening pass is possible if you want a slimmer book.
8. **"ai-lair".** You listed it among your owned names; no such project was
   found. Typo for ai-jail, or a project to add to the copyright page?
9. **Photo of Sam Altman** (ch14) is from 2017; newer CC BY options exist.
10. **Citation style.** In-text citations follow NBR 10520:2023
    ("(Kaplan et al., 2020)"); switch to the older ALL-CAPS convention?
11. **ISBN** is "[a definir]" on the copyright page.
12. **Source-tree privacy.** Hidden provenance comments and front matter in
    ch13/ch15 name your private homelab notes repo and file names. They never
    reach the book, but would be visible if this repository were published.

## Things to fix in your own projects (found while fact-checking)

- **ai-jail README** says `--agent-state ... (default off)` in the usage
  block (~line 513) while the code and the defaults section say it is on.

## Blog errata (the book corrects these; you may want to fix the posts)

| Post | Blog says | Verified |
|---|---|---|
| 06/11 Fable 5 | ties Opus 4.8 at "ten times the price" | ~US$11 vs ~US$6.40 per run after the July pricing audit: a bit under 2x |
| benchmark posts before 2026-08-01 | OpenCode run costs | understated 40-90x by a metrics bug |
| June benchmark posts | Opus 4.7/4.8 ~US$1.10 per run | ~US$7 / ~US$6.40 (cache reads uncounted) |
| 03/31 MS-S1 Max review | 96 GB VRAM | 64 GB allocated since 8 April |
| 01/22 GLM 4.7 Flash | "the same GLM 4.7, quantized" | a separate, smaller 30B MoE model (Z.ai model card) |
| 03/31 Claude Code leak | DRM broken "the same night" | announced ~30 hours after the leak |
| 03/31 Claude Code leak | Anthropic bought Bun "late 2024" | December 2025 (Bun's own posts) |
| 09/28 limits of LLMs | METR study used private repositories | mature open-source repositories |
| 04/09 20 years of blog | "the 10% that refused" | 6 posts refused (~2%); the 90% was translation quality |
| 02/08 rant | "George Hinton"; AlexNet by Hinton, LeCun, Sutskever | Geoffrey Hinton; AlexNet by Krizhevsky, Sutskever, Hinton |
| 02/08 rant (via ch18) | Amodei said engineers will be "obsolete" | WEF 20 Jan 2026: "6-12 months away from models doing all of what software engineers do end-to-end" |
| 03/05 Frank Yomik | 16 GB GPU at the top, 8 GB at the end | inconsistent within the post |
| 02/20 Chronicles | weekday labels in the daily table | off by one against the calendar |
| 02/23 Frank Sherlock | 21/02 called both Saturday and Friday | Saturday |
| 09/09 propaganda | several quotes (Tao, Buckmaster, Coxon "pause", HF credentials) | see ch14 notes in book/pt/_notes/ch14.yml for each correction |

## How to send changes

Edit the blog as usual and tell me; `rake drift` finds affected chapters.
For book-only changes, point at the chapter (book/pt/chNN.md) or describe
the change; the ledger (book/integration.yml) records decisions.
