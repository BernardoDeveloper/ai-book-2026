#show: akita-book.with(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(by-author)$
  author: "$for(by-author)$$it.name.literal$$sep$, $endfor$",
$endif$
$if(lang)$
  lang: "$lang$",
$endif$
$if(region)$
  region: "$region$",
$endif$
  toc: $if(toc)$true$else$false$endif$,
$if(toc-title)$
  toc-title: [$toc-title$],
$endif$
$if(quarto.language.crossref-ch-prefix)$
  chapter-label: "$quarto.language.crossref-ch-prefix$",
$endif$
$if(quarto.language.crossref-apx-prefix)$
  appendix-label: "$quarto.language.crossref-apx-prefix$",
$endif$
$if(colophon)$
$if(colophon-paperback)$
  colophon: if sys.inputs.at("binding", default: "hardcover") == "paperback" {
    [$colophon-paperback$]
  } else {
    [$colophon$]
  },
$else$
  colophon: [$colophon$],
$endif$
$endif$
$if(pdf-cover)$
  cover: "$pdf-cover$",
  cover-alt: "$if(pdf-cover-alt)$$pdf-cover-alt$$else$$title$$endif$",
$endif$
)
