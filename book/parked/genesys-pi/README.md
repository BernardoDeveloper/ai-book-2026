# Parked: the Genesys PI material

## What is parked

Everything the book said about the Genesys PI, the model LUA Vision (São
Paulo) launched in April 2026, and about the author's black-box tests of
its origin:

- ch12's section "## O mistério brasileiro" (fingerprinting by tokenizer,
  the proxy test, the checked/claimed/open list), with its figure
  `@fig-ch12-impressao-digital`;
- two apA timeline entries (April: the launch; 23 September: the first
  benchmark round);
- the glossary entries `proxy` and `tokenizador`, which only that section
  used;
- the references `luavision2026empresa` and `livebench2026issue370`.

Source posts now listed as excluded ("parked") in `book/outline.yml`:

- `2026/09/23/llm-benchmark-v4-genesys-pi-novo-competidor-brasileiro`
- `2026/09/30/o-misterio-do-genesys-pi-da-lua-vision-modelo-frontier-brasileiro`

## Why

Author decision, 2026-10-13 (ledger: `book/integration.yml`). Vendor due
diligence is still pending, and in the target-reader pass
(`reviews/1.0.0-preview.3/personas/consolidated.md`, row B5) 4 of the 5
readers found the section tangential: inconclusive by its own account.
The lesson it carried, separating an announcement into what outsiders
measured, what only the seller claims and what nobody knows, stays in ch12
through the Rio 3.5 and Kimi cases. apC keeps that habit, now marked
`<!-- src: original -->`.

## Files

| file | what | origin |
|---|---|---|
| `pt-ch12.md` | the ch12 section, verbatim, with markers and figure | `book/pt/ch12.md` |
| `pt-apA.md` | the two timeline entries, verbatim, with markers | `book/pt/apA.md` |
| `glossary-pt.yml` | `proxy` and `tokenizador` | `book/back/glossary-pt.yml` and `book/pt/_gls/ch12.yml` |
| `refs.yaml` | the two references (added by the editor) | the bibliography |
| `en-apA.md` | the two EN timeline entries, verbatim, with markers | `book/en/apA.md` |
| `glossary-en.yml` | EN `proxy` and `tokenizador` | `book/back/glossary-en.yml` |
| EN ch12 section and references | added by the editor | `book/en/` |

## How to restore

1. ch12: paste the block from `pt-ch12.md` back into `book/pt/ch12.md`
   right before "## O que dá pra saber de fora", and follow the notes at
   the top of that file (closing-section wording, refs_projects, figure
   credit).
2. apA: put the two entries in `pt-apA.md` back in their months (positions
   in the file's header comment).
3. Front matter: re-add both posts (with their sha256 from
   `inventory/posts.yml`) to the `sources` of ch12, apA and apC; in apC,
   the paragraph "Antes das perguntas, um hábito que eu trouxe dos testes
   de origem de modelos" goes back to the 09/30 post's marker if the
   section returns. Remove both posts from `excluded` in `book/outline.yml`.
4. Glossary: put `proxy` and `tokenizador` back in alphabetical order in
   `book/back/glossary-pt.yml` and in `book/pt/_gls/ch12.yml` (`rake build`
   runs `rake merge`, which reads the `_gls` proposals).
5. References: restore the entries in `refs.yaml` to the bibliography.
6. Ledger: record the restore in `book/integration.yml`.
7. `rake check build`, page audit, and look at ch12, apA and apC.
8. Only after the author approves the PT edition: the same for EN
   (`docs/TRANSLATING.md`), then `rake check build BOOK_LANG=en`.
