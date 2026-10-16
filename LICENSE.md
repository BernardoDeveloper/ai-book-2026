# Licenses

This repository contains a book and the software that builds it. They are
licensed differently.

## The book: all rights reserved

The text of *Competente o Suficiente* (everything under `book/`), its cover
and its original illustrations and diagrams (`assets/cover/`,
`assets/figures/` except the third-party photographs listed below, and the
sources in `assets/charts/` and `assets/diagrams/` insofar as they encode the
figures' content) are © 2026 Fabio Akita. All rights reserved.

You may read the book and share links to this repository and its releases.
Without the author's prior written permission you may not:

- reproduce, publish, sell or redistribute the book or any part of it, in
  any format (including copies of the released EPUB and PDF files);
- translate, adapt, abridge or create any derivative work from it;
- use the text, figures or cover in other works or products.

Brief quotations with attribution and a link, as allowed by law for
criticism, review and teaching, are fine.

**Text and data mining.** The author expressly reserves the rights of text
and data mining over this book, including its use to train, fine-tune or
evaluate machine-learning models (reservation under article 4(3) of Directive
(EU) 2019/790 and equivalent provisions elsewhere).

The names akitaonrails, Akitando, The M.Akita Chronicles, ai-memory, ai-jail,
ai-usagebar, ghpending and the "Frank" project series are the property of
Fabio Akita. The code of some of those projects is open source under the
licence stated in each project's repository; those licences cover the code,
not the names, and not this book.

## The build software: MIT

The scripts, filters, templates and configuration that build the book
(`scripts/`, `filters/`, `_extensions/`, `Rakefile`, `_quarto.yml`,
`assets/style/`, `.github/`) are released under the MIT License:

```
Copyright (c) 2026 Fabio Akita

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Third-party material

| What | Where | Licence |
|---|---|---|
| Source Serif 4, Source Sans 3 (Adobe) | `assets/fonts/` | SIL Open Font License 1.1 (`assets/fonts/SOURCES.md`) |
| Noto Sans | `assets/fonts/` | SIL Open Font License 1.1 (`assets/fonts/OFL-NotoSans.txt`) |
| Limelight (Sorkin Type) | `assets/fonts/` | SIL Open Font License 1.1 (`assets/fonts/OFL-Limelight.txt`) |
| ABNT citation style (patched) | `assets/csl/abnt-akita.csl` | CC BY-SA 3.0, Citation Style Language project (`assets/csl/SOURCES.md`) |
| Photographs and diagrams from Wikimedia Commons and other sources | `assets/figures/` | Each file's own rights status (including public domain, CC BY, CC BY-SA, or unverified reuse permission); available author, source and rights information in `assets/credits/<figure>.yml` and in the book's image credits |

The chapter 21 Roadster and Nolan photographs were selected for inclusion by
the author; commercial-book and public-repository reuse permissions have not
been verified. Their inclusion does not grant any downstream reuse licence.

AI-generated illustrations (including the cover art) are identified in
`assets/credits/` and in the book's "Créditos das imagens" page, with the
model and date used for each.
