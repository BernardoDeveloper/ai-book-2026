# Print covers

## Interiors and ISBNs

`rake build BOOK_LANG=pt` produces both print interiors automatically:

- `build/pt/Competente-o-Suficiente.pdf`: hardcover, ISBN 9798162465683.
- `build/pt/Competente-o-Suficiente-paperback.pdf`: paperback, ISBN 9798162938088.

The unsuffixed filename remains the hardcover for compatibility with existing
release links. Each interior prints only its own binding's ISBN on the
copyright page. English remains hardcover-only (ISBN 9798162395362).
The ebook PDF and EPUB remain separate digital outputs.

Hardcover ISBNs live in `meta.isbn`, paperback ISBNs in `meta.isbn_paperback`,
keyed by language in `book/outline.yml`. `rake build` compiles and audits the
paperback only when that language has a configured paperback ISBN. CI's
existing PDF upload glob includes the additional interior automatically.
After a full build, `rake paperback_pdf BOOK_LANG=pt` can recompile just that
interior. Per-language `index-pt.typ`/`index-en.typ` files preserve the correct
rendered source; full Quarto builds still run sequentially in one checkout.

## Wraparound covers

Build covers separately from the interiors. Use the final interior PDF's
page count to download a KDP template for each binding, then extract its
PNG/PDF/readme under `assets/cover/kdp/<binding>-6x9-<pages>-bw/`.
The template filename's locale is the guide's language, not the book's.

```sh
rake kdp_cover BOOK_LANG=pt BINDING=hardcover
rake kdp_cover BOOK_LANG=pt BINDING=paperback
rake kdp_cover BOOK_LANG=en BINDING=hardcover
```

`BINDING` defaults to `hardcover` for existing commands. The selector checks
binding, page count, 6x9 trim, and BW/white paper. An explicit `TEMPLATE=...`
cannot bypass those checks. Paperback has two spine-fold guides; case-laminate
hardcover has those plus two hinge guides. Never substitute one for the other.

Outputs are `build/kdp/<title>-<binding>-cover.pdf`: flattened CMYK PDFs at
600 dpi. The accompanying `-preview.jpg` and `-guides.jpg` are for inspection,
not upload. Check all text against the live areas and leave the template's
barcode area free of text. KDP places the barcode; these files do not encode
an ISBN. Each binding has its own ISBN in KDP and in its corresponding interior.

## preview.9 templates verified on 2026-10-16

All use 6x9 trim, black-and-white interior and white paper.

| Edition/binding | Pages | Template overall size (inches) | Spine (inches) |
|---|---:|---:|---:|
| PT hardcover | 531 | 14.960 x 10.417 | 1.385 |
| PT paperback | 531 | 13.446 x 9.250 | 1.196 |
| EN hardcover | 517 | 14.928 x 10.417 | 1.353 |

Dimensions above are the rounded labels in the supplied KDP PDFs. Output
dimensions follow the accompanying 600-dpi PNG pixel grid, which can differ
by about one pixel from those labels. Regenerate after any page-count change.
