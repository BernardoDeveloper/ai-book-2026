# Print covers

## UICLAP: PT-BR print only

`rake uiclap_pdf` builds a separate 160 x 230 mm paperback interior at
`build/uiclap/pt/Competente-o-Suficiente-uiclap-16x23.pdf`. It renders current
PT sources, adjusts chapter endings, and runs a strict page audit. It does
not build ebooks or English, or replace any Amazon output. Use
`ruby scripts/page_audit.rb --edition uiclap --strict` to repeat the audit.
The saved source is `index-pt-uiclap.typ`; its tightening settings live in
`build/uiclap/pt/.tighten`, separate from Amazon's 6x9 layout.

Amazon ISBNs are never inherited. Until the author supplies this edition's
ISBN in `meta.isbn_uiclap.pt` in `book/outline.yml`, the copyright page omits
the ISBN. Do not upload the KDP wraparound
cover: its dimensions and spine are specific to Amazon's production.
This target is local/opt-in and is not included in release automation.

Margins are 25 mm inside, 20 mm outside, and 25.4 mm top/bottom, with
mirrored pages. These retain the previously checked 16x23 layout unchanged.
The existing fonts and figure sizes are retained; the final page count is
reported by the audit, not assumed from the Amazon edition.

Local proof verified on 2026-10-17: 547 pages, 160 x 230 mm, strict page
audit clean. The interior was renamed from the abandoned Clube de Autores
target without rebuilding or changing its bytes. No UICLAP ISBN is configured.

`rake uiclap_cover` builds the upload file
`build/uiclap/pt/Competente-o-Suficiente-uiclap-cover.jpg`, plus a PDF proof
and preview/guide JPGs. Upload the full-resolution JPG, not the PDF or guides.
UICLAP accepts JPG up to 50 MB; its guidance recommends 600 dpi:
https://suporte.uiclap.com/support/solutions/articles/67000705782-capa-formato-tipo-de-arquivo-e-material

The supplied `assets/cover/uiclap-medidas-capa.jpg` is a schematic, NOT a
scale drawing. Use its printed values: 8409 x 5646 px at 600 dpi, 3874 px
per panel including outer bleed, 661 px (28 mm) spine, 5 mm bleed and 10 mm
panel safety margins. It labels the cover panels 159 x 229 mm, distinct
from the unchanged 160 x 230 mm PDF interior. Spine lettering is inset
3 mm from the folds. The lower back reserves 70 x 50 mm for UICLAP's
barcodes, 10 mm from the right fold and bottom trim (15 mm from the file's
bottom including bleed). Text ends above this box. UICLAP adds the codes:
https://suporte.uiclap.com/support/solutions/articles/67000463871-tenho-isbn-preciso-comprar-o-c%C3%B3digo-de-barras-
The build pins this template's hash and the 547-page count and refuses a
changed template/count until its geometry is reviewed. Reconfirm the portal
template after changes to page count or paper; do not infer spine width from KDP.

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
