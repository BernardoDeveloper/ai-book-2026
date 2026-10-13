<p align="center">
  <img src="assets/cover/cover-readme.jpg" alt="Cover of Competente o Suficiente: a giant retro-futurist robot with a round, weary face kneels at a 1950s World's Fair, studying its own open hand, while a crowd watches" width="360">
</p>

<h1 align="center">Competente o Suficiente</h1>

<p align="center"><em>Um ano colocando a inteligência artificial à prova, sem medo e sem propaganda</em><br>
Fabio Akita</p>

---

A book for people who are anxious or confused about AI: the professional
afraid of being replaced, the parent who read that AGI is two years away, the
manager being sold an "AI transformation". It follows one veteran programmer
through 2026 as he builds real software with AI agents, measures dozens of
models in his own benchmark, gets things wrong, corrects them in public, and
reads the industry's announcements against the evidence.

The book grew out of the year's articles on
[akitaonrails.com](https://www.akitaonrails.com), reorganised and rewritten
as one narrative, fact-checked again, and illustrated.

## Read it

Download the latest edition from
[Releases](https://github.com/akitaonrails/ai-book-2026/releases):

| File | For |
|---|---|
| `Competente-o-Suficiente.epub` | Kindle, Kobo, Apple Books, any e-reader |
| `Competente-o-Suficiente-ebook.pdf` | Reading on a screen |
| `Competente-o-Suficiente.pdf` | Print (6 × 9 in) |

**Status:** 1.0-preview, in Brazilian Portuguese. An English edition is in
progress.

## What's inside

| Part | The question it answers |
|---|---|
| I. O que é essa coisa, afinal | Is it intelligent? Is AGI coming? |
| II. A maratona | Does it actually work, or is it all demo? |
| III. Números e propaganda | Which AI is best? Should I believe the announcements? |
| IV. Quem fica com as chaves | Is it dangerous to let it touch my things? |
| V. E o meu emprego? | Will it take my job? What comes next? |

Plus two interludes, an optional no-math appendix on how the machine works
inside, a timeline, practical checklists, a glossary of 144 terms and 292
references.

## Em português

Um livro pra quem está ansioso ou confuso com a inteligência artificial. Um
programador veterano passa 2026 construindo software de verdade com agentes de
IA, mede dezenas de modelos no próprio benchmark, erra, corrige em público e
confronta os anúncios da indústria com as evidências. Baixe a edição mais
recente em [Releases](https://github.com/akitaonrails/ai-book-2026/releases).

## How it's made

This repository is the book's source and the machinery that keeps it in sync
with the blog. Every paragraph records which article it came from; when an
article changes, `rake drift` shows which chapters are affected and the diff.
Diagrams are drawn as code, AI-generated illustrations are disclosed in the
image credits, and real photos carry their licences. The details are in
[docs/DESIGN.md](docs/DESIGN.md).

```sh
rake tools    # fetch the pinned toolchain (Quarto with Pandoc and Typst, epubcheck)
rake build    # EPUB, PDF, web and DOCX editions in build/pt/, with epubcheck and a page audit
rake drift    # what in the book is out of date with the blog
```

Requires Ruby, Java (for epubcheck) and poppler-utils.

## License

The book's text, cover and illustrations are © 2026 Fabio Akita, all rights
reserved; see [LICENSE.md](LICENSE.md). The build scripts and templates are
MIT-licensed. Fonts, the citation style and the photographs keep their own
licences, listed in the same file.
