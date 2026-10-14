# Parked: the appendix of projects and the side-project detail

## What is parked

The author's decision of 2026-10-14: the appendix "Os projetos do ano" (a
catalogue of every 2026 project) is cut, and the side projects of the
Frank series (Investigator, FBI, Sherlock, Lyrics, Karaoke, Mega and the
like) are footnote-worthy, not appendix material. FrankClaw stays in ch16 as
the experiment it was, now marked as stopped at version 0.1. Investigator
and FBI are not discontinued but got little effort and almost no outside
contributions, so the book no longer frames them as "projects" with users.

- the whole appendix `apD` ("Os projetos do ano"), PT and EN, with its
  bibliography file (all its references were cited only there) and notes;
- two technical-appendix sections: "Frank Investigator: como os três
  modelos votam" (with the figure `@fig-ch04-tres-juizes`, whose asset and
  credit record stay in `assets/`) and "Frank Sherlock: o teste dos modelos
  de visão e a publicação em três sistemas";
- ch04 "Três juízes e um veto", trimmed from ~940 to ~500 words (the full
  section as it stood is kept here);
- ch17's Frank FBI subsections, trimmed from ~950 to ~390 words (kept here);
- timeline entries: FrankMega and Frank Sherlock going live, Frank FBI,
  Frank Investigator; the July "pequenas coceiras" entry lost the project
  names, and the FrankClaw entry now says it stopped at version 0.1.

Source posts now listed as excluded ("parked") in `book/outline.yml`, used
only by the appendix:

- `2026/03/07/crystal-e-um-wrapper-inteligente-pro-ffmpeg-feito-em-3-horas-easy-ffmpeg`
- `2026/04/05/transformando-youtube-num-app-de-karaoke-frank-karaoke`

The other posts the appendix cited stay in the book through other units.

## Files

| file | what | origin |
|---|---|---|
| `pt-apD.md`, `en-apD.md` | the appendix, verbatim | `book/pt/apD.md`, `book/en/apD.md` |
| `refs-pt-apD.yaml` | the appendix's references | `book/pt/_refs/apD.yaml` |
| `notes-pt-apD.yml`, `notes-en-apD.yml` | drafting notes | `book/pt/_notes/apD.yml`, `book/en/_notes/apD.yml` |
| `pt-aptecnico-secoes.md` | the two technical-appendix sections, verbatim | `book/pt/aptecnico.md` |
| `pt-ch04-tres-juizes.md` | ch04's section before the trim | `book/pt/ch04.md` |
| `pt-ch17-frank-fbi.md` | ch17's Frank FBI subsections before the trim | `book/pt/ch17.md` |
| `pt-apA-entradas.md` | removed and reworded timeline entries | `book/pt/apA.md` |

## How to restore

1. apD: move `pt-apD.md` back to `book/pt/apD.md` (and `en-apD.md`,
   `refs-pt-apD.yaml` to `book/pt/_refs/apD.yaml`, notes to `_notes/`), add
   the `apD` entry back to `book/outline.yml` after `apC`, remove the two
   posts above from `excluded`, and restore ch10's pointer to `@sec-apD`
   ("A lista completa ... está em @sec-apD").
2. aptecnico: paste the sections from `pt-aptecnico-secoes.md` back (the
   Investigator one before "A marca d'água estatística do Claude", the
   Sherlock one before "A tela preta do Driveclub"), re-add the posts
   03/27 (Investigator), 02/23 (indexador) and 03/01 (software nunca está
   pronto) to its front matter, and restore the callbacks in ch04 ("Como os
   votos são contados ... está em @sec-aptecnico-investigator") and ch07
   ("... estão em @sec-aptecnico-sherlock").
3. ch04/ch17/apA: replace the trimmed text with the parked versions; re-add
   the posts 02/21, 03/09 and 03/27 to apA's front matter.
4. Ledger: record the restore in `book/integration.yml`.
5. `rake check build`, page audit; then EN after the author's approval.
