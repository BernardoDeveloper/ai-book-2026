# CSL sources

Citation styles used by the book (`csl:` in the profile written by
`scripts/gen_quarto.rb`). CSL styles are licensed under
[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/); adapted
files keep that licence and credit the original authors in their `<info>`.

| File | Edition | Source | Upstream commit | Modified |
|---|---|---|---|---|
| `abnt-akita.csl` | PT | https://github.com/citation-style-language/styles/blob/6ba2e9c6aa6e0dab87d3a20b833ed8ff6500f698/associacao-brasileira-de-normas-tecnicas.csl | `6ba2e9c6aa6e0dab87d3a20b833ed8ff6500f698` (2026-10-13; file `<updated>` 2023-08-20) | yes, see the changelog comment at the top of the file |

The EN edition uses Pandoc's built-in Chicago author-date style (no file here).

Upstream file SHA-256 (identical to `tools/cache/abnt.csl`, fetched by
`rake tools`): `4f3f2eadb94c314476608e070acb889253f7007fbbe3e2c251ffc90e2163eaae`.

## Why a patched copy

Upstream `associacao-brasileira-de-normas-tecnicas.csl` omits, for online
documents, what NBR 6023:2018 requires: no "Disponível em/Acesso em" for
newspaper, magazine and journal articles or books, no date or site name for
`webpage`, no DOI, no `note`, and no final period on the default layout. It
also puts the 2024a/2024b year suffix on the access date of web pages.

The other ABNT variants in the styles repository (the Zotero style repository
serves the same files) were rendered on 2026-10-13 against 30 entries covering
every type in `book/back/references.yaml`. None prints `note`, so none shows the
"Arquivado em" links, and each has other defects:

- `instituto-brasileiro-de-informacao-em-ciencia-e-tecnologia-abnt`: closest;
  prints the title twice for `motion_picture`, ignores the container for
  `software` ("[S. l.]: [S.n.]" instead of GitHub), "2024 a" with a space.
- `associacao-brasileira-de-normas-tecnicas-ufrgs`: lowercases titles
  ("Deepclaude"), uses "[s. d.]" as publisher, no DOI.
- `universidade-de-sao-paulo-escola-de-comunicacoes-e-artes-abnt`,
  `universidade-estadual-de-alagoas-abnt`: title-first entries for videos and
  podcasts (out of sync with the author-based in-text citation), missing commas.
- `-eceme`, `-instituto-meira-mattos`, `-ufmg-face-full`, `-ufpr`, `-usp-fmvz`,
  `universidade-do-estado-do-rio-de-janeiro-abnt`,
  `universidade-federal-do-espirito-santo-abnt`: no date for `webpage`.
- `-ipea`, `-numerico`, `-ufs`: same gaps as upstream.
- `pontificia-universidade-catolica-do-parana-abnt`: no final period, no DOI.
- `-unirio-eipp`, `universidade-estadual-paulista-campus-de-dracena-abnt`,
  `universidade-federal-de-pernambuco-abnt`: missing final periods or book URLs.

## `note` and the public bibliography

`abnt-akita.csl` prints `note`, but in `references.yaml` that field also holds
editorial provenance ("cited-by: ..."). `scripts/gen_quarto.rb` therefore
writes `build/references-pt.yaml`, a copy whose `note` keeps only
"Arquivado em: <url>", and points the PT profile's `bibliography` at it.
