// akita-book: a sober trade-paperback template for Typst (Quarto partial).
//
// Two editions come out of the same .typ, selected with
// `typst compile --input edition=ebook|print` (default print):
//   print  6 x 9 in trim, mirrored margins (inner > outer), parts and
//          chapters open on a recto, no cover (the print cover is a separate
//          file for KDP).
//   ebook  same trim and text block, symmetric margins, full-bleed cover
//          page, chapters open on the next page (no blank pages).
//
// Structure conventions (see akita-book.lua):
//   - level-1 headings labelled <akita-part> are part / appendix dividers;
//   - other level-1 headings are chapters; numbered ones step the chapter
//     counter, unnumbered ones (front matter, interludes, back matter) don't;
//   - titles "Parte II: X", "Interlúdio: X", "Apêndice A: X"... are split
//     into a small label and the title proper.
//
// NB: this file is a Pandoc template partial, so a literal dollar sign must
// be doubled. There are none below; keep it that way.

#let akita-edition = sys.inputs.at("edition", default: "print")
#let akita-ebook = akita-edition == "ebook"

#let ak-serif = ("Source Serif 4",)
#let ak-sans = ("Source Sans 3",)
#let ak-ink = rgb("#1B2238")
#let ak-muted = rgb("#4A5060")
#let ak-rule = rgb("#8A8F98")

#let ak-body-size = 10.5pt
#let ak-blank = state("ak-blank", false)
#let ak-running = state("ak-running", none)
#let ak-labels = ("Parte", "Interlúdio", "Epílogo", "Posfácio", "Apêndice",
                  "Part", "Interlude", "Epilogue", "Afterword", "Appendix")

// Plain text of a heading body (headings here are plain strings).
#let ak-str(c) = {
  if c == none { "" }
  else if type(c) == str { c }
  else if c.has("text") { c.text }
  else if c.has("children") { c.children.map(ak-str).join("") }
  else if c.has("body") { ak-str(c.body) }
  else if c == [ ] { " " }
  else if c.func() == smartquote { if c.at("double", default: true) { "\"" } else { "'" } }
  else { "" }
}

// "Interlúdio: Vinte anos..." -> ("Interlúdio", "Vinte anos..."); else (none, body)
#let ak-split(body) = {
  let s = ak-str(body)
  let i = s.position(": ")
  if i != none and ak-labels.any(l => s.starts-with(l)) {
    (s.slice(0, i), s.slice(i + 2))
  } else {
    (none, body)
  }
}

#let ak-in-appendix = state("ak-in-appendix", false)
#let ak-appendix-label = state("ak-appendix-label", "Apêndice")

// Switched on by akita-book.lua right after the appendix divider page:
// appendices restart the heading counter and are lettered (A, B, ...).
// State, not a scoped show rule, so it survives the per-chapter wrappers.
#let ak-start-appendices() = {
  counter(heading).update(0)
  ak-in-appendix.update(true)
}
#let ak-heading-numbering(..n) = numbering(if ak-in-appendix.get() { "A.1" } else { "1.1" }, ..n)

// Invisible layout records for scripts/page_audit.rb, read back with
// `typst query index.typ metadata --field value`. Each is a dictionary with
// key `ak`; they take no space.
#let ak-audit(kind, ..fields) = context metadata((ak: kind, page: here().page(),
  y: here().position().y.pt(), ..fields.named()))

// Keep a block on one page when it fits in `limit` (default: most of the
// text block); taller ones may break (tables then repeat their header row).
// Records start/end for the audit's SPLIT check.
#let ak-blk = counter("ak-blk")
#let ak-text-w = 4.5in
#let ak-keep(kind, body, limit: 6.9in, ..block-args) = {
  ak-blk.step()
  context {
    let id = ak-blk.get().first()
    let tall = measure(body, width: ak-text-w).height > limit
    block(breakable: tall, width: 100%, ..block-args.named(), {
      ak-audit("blk", id: id, kind: kind, edge: "start", allowed: tall)
      body
      ak-audit("blk", id: id, kind: kind, edge: "end")
    })
  }
}

// Per-chapter body wrapper emitted by akita-book.lua. `--input
// tighten=ch01,interlude1:2` sets those chapters a hair tighter (per level:
// tracking -0.004em and line pitch -0.12pt, i.e. under 1% and invisible at
// reading size) so a last page holding one to three lines folds back. `rake build` derives
// the list from scripts/page_audit.rb's RUNT-END findings.
#let ak-tighten = {
  let d = (:)
  for e in sys.inputs.at("tighten", default: "").split(",").map(str.trim).filter(s => s != "") {
    let parts = e.split(":")
    d.insert(parts.first(), if parts.len() > 1 { int(parts.at(1)) } else { 1 })
  }
  d
}
#let ak-unit(id, body) = {
  let level = ak-tighten.at(id, default: 0)
  if level > 0 {
    set text(tracking: -0.004em * level)
    set par(leading: 0.62em - 0.12pt * level, spacing: 0.62em - 0.12pt * level)
    body
  } else { body }
}

#let ak-is-part(h) = h.at("label", default: none) == <akita-part>

#let ak-label-text(s) = text(font: ak-sans, size: 8.5pt, weight: "semibold",
  tracking: 0.18em, fill: ak-muted, upper(s))

// ---------------------------------------------------------------- openings

#let ak-part-page(it) = {
  let (label, title) = ak-split(it.body)
  set par(justify: false, first-line-indent: 0pt)
  ak-running.update(none)
  ak-chapter.update(none)
  v(2.1in)
  align(center)[
    #if label != none { ak-label-text(label); v(1.1em) }
    #line(length: 2.2em, stroke: 0.6pt + ak-rule)
    #v(1.1em)
    #block(width: 85%, text(font: ak-sans, size: 21pt, weight: "regular",
      hyphenate: false, fill: ak-ink, title))
  ]
}

#let ak-chapter-open(it, chapter-label, appendix-label) = context {
  let (label, title) = ak-split(it.body)
  let numbered = it.numbering != none
  let appendix = ak-in-appendix.get()
  let num = if numbered { numbering(if appendix { "A" } else { "1" }, counter(heading).get().first()) }
  set par(justify: false, first-line-indent: 0pt)
  ak-running.update(title)
  ak-chapter.update(num)
  v(1.15in)
  block(height: 2.2em, spacing: 0pt, {
    if numbered and not appendix {
      text(font: ak-sans, size: 30pt, weight: "light", fill: ak-muted, num)
    } else if numbered {
      v(1.2em)
      ak-label-text(appendix-label + " " + num)
    } else if label != none {
      v(1.2em)
      ak-label-text(label)
    }
  })
  v(0.9em)
  block(spacing: 0pt, {
    set par(leading: 0.45em)
    text(font: ak-sans, size: 19pt, weight: "semibold", hyphenate: false,
      fill: ak-ink, title)
  })
  v(0.9em)
  line(length: 2.2em, stroke: 0.6pt + ak-rule)
  v(2.4em)
}

// ---------------------------------------------------------------- page chrome

#let ak-opening-page() = {
  let p = here().page()
  query(heading.where(level: 1)).any(h => h.location().page() == p)
}

#let ak-header(book-title) = context {
  if not ak-blank.get() and not ak-opening-page() {
    let n = counter(page).get().first()
    let folio = counter(page).display()
    set text(font: ak-sans, size: 7.5pt, fill: ak-muted)
    let head(s) = text(tracking: 0.14em, upper(s))
    if calc.even(n) {
      folio; h(1.4em); head(book-title)
    } else {
      let r = ak-running.get()
      align(right)[#head(if r == none { book-title } else { r })#h(1.4em)#folio]
    }
  }
}

#let ak-footer() = context {
  if not ak-blank.get() and ak-opening-page() {
    let p = here().page()
    let is-part = query(heading.where(level: 1))
      .filter(h => h.location().page() == p).any(ak-is-part)
    if not is-part {
      align(center, text(font: ak-sans, size: 7.5pt, fill: ak-muted, counter(page).display()))
    }
  }
}

// ---------------------------------------------------------------- front matter

#let ak-cover(path, alt) = {
  if akita-ebook and path != none and path != "" {
    page(margin: 0pt, height: auto, header: none, footer: none, numbering: none,
      image(path, width: 100%, alt: alt))
  }
}

#let ak-front(title, subtitle, author, colophon) = {
  set par(justify: false, first-line-indent: 0pt)
  // i: half-title
  page({
    v(2.2in)
    align(center, text(font: ak-sans, size: 15pt, weight: "regular", fill: ak-ink, title))
  })
  // ii: blank verso (print only)
  if not akita-ebook { page([]) }
  // iii: title page
  page({
    v(1.3in)
    align(center)[
      #block(width: 92%, text(font: ak-sans, size: 27pt, weight: "semibold", fill: ak-ink,
        hyphenate: false, { set par(leading: 0.35em); title }))
      #v(1.4em)
      #line(length: 2.2em, stroke: 0.6pt + ak-rule)
      #v(1.4em)
      #if subtitle != none {
        block(width: 80%, text(font: ak-serif, size: 12pt, style: "italic", fill: ak-muted,
          hyphenate: false, subtitle))
      }
    ]
    v(1fr)
    align(center, text(font: ak-sans, size: 10pt, weight: "semibold", tracking: 0.22em,
      fill: ak-ink, upper(author)))
    v(0.4in)
  })
  // iv: copyright / colophon, set low on the page
  page({
    v(1fr)
    set text(size: 8pt, fill: ak-ink)
    set par(leading: 0.55em, spacing: 0.9em)
    colophon
  })
}

#let ak-toc(toc-title) = {
  heading(level: 1, numbering: none, outlined: false, toc-title)
  set par(justify: false, first-line-indent: 0pt)
  show outline.entry: it => {
    let el = it.element
    let (label, title) = ak-split(el.body)
    let pg = text(font: ak-sans, size: 9pt, fill: ak-muted, it.page())
    if ak-is-part(el) {
      v(1.5em, weak: true)
      link(el.location(), block(above: 0pt, below: 0.75em, breakable: false,
        text(font: ak-sans, size: 8.5pt, weight: "semibold", tracking: 0.16em, fill: ak-ink, {
          if label != none [#upper(label)#h(0.6em)·#h(0.6em)]
          upper(title)
        })))
    } else {
      let num = if el.numbering != none {
        text(font: ak-sans, size: 9.5pt, fill: ak-muted,
          numbering(if ak-in-appendix.at(el.location()) { "A" } else { "1" },
            counter(heading).at(el.location()).first()))
      }
      let shown = if label != none [#emph(label + ":") #title] else { title }
      link(el.location(), block(above: 0.55em, below: 0.55em,
        grid(columns: (1.9em, 1fr, 2.1em), column-gutter: 0pt, align: (left + top, left + bottom, right + bottom),
          num,
          [#shown #box(width: 1fr, inset: (x: 0.4em), repeat(gap: 0.25em, text(fill: ak-rule, size: 8pt)[.]))],
          pg)))
    }
  }
  outline(title: none, target: heading.where(level: 1), depth: 1)
}

// ---------------------------------------------------------------- the book

#let akita-book(
  title: none,
  subtitle: none,
  author: "",
  lang: "pt",
  region: "BR",
  toc: true,
  toc-title: [Sumário],
  chapter-label: "Capítulo",
  appendix-label: "Apêndice",
  colophon: [],
  cover: none,
  cover-alt: none,
  doc,
) = {
  set document(title: title, author: author)
  set text(font: ak-serif, size: ak-body-size, lang: lang, region: region,
    hyphenate: true, fill: black, number-type: "old-style",
    costs: (widow: 1000%, orphan: 1000%, runt: 200%, hyphenation: 100%))
  set par(justify: true, leading: 0.62em, spacing: 0.62em,
    first-line-indent: (amount: 1.2em, all: false))
  set page(
    width: 6in, height: 9in,
    margin: if akita-ebook {
      (x: 0.75in, top: 0.8in, bottom: 0.85in)
    } else {
      (inside: 0.875in, outside: 0.625in, top: 0.8in, bottom: 0.85in)
    },
    binding: left,
    header-ascent: 35%,
    footer-descent: 35%,
    numbering: "i",
    header: none,
    footer: none,
  )

  // --- headings
  set heading(numbering: ak-heading-numbering)
  show heading: set text(font: ak-sans, fill: ak-ink, hyphenate: false)
  show heading: set par(justify: false, first-line-indent: 0pt)
  show heading.where(level: 1): it => {
    // Pending floats go out before the break, so no figure drifts into the
    // next chapter.
    place.flush()
    ak-blank.update(true)
    pagebreak(weak: true, to: if akita-ebook { none } else { "odd" })
    ak-blank.update(false)
    ak-audit("h1", part: ak-is-part(it), numbered: it.numbering != none,
      label: if it.has("label") { str(it.label) } else { "" }, title: ak-str(it.body),
      num: if it.numbering != none { numbering(it.numbering, ..counter(heading).get()) } else { "" })
    if ak-is-part(it) { ak-part-page(it) } else { ak-chapter-open(it, chapter-label, appendix-label) }
  }
  show heading.where(level: 2): it => block(above: 1.9em, below: 0.85em, sticky: true,
    { ak-audit("h", level: 2, title: ak-str(it.body)); text(size: 12pt, weight: "semibold", it.body) })
  show heading.where(level: 3): it => block(above: 1.5em, below: 0.7em, sticky: true,
    { ak-audit("h", level: 3, title: ak-str(it.body)); text(size: 10.5pt, weight: "semibold", style: "italic", it.body) })
  show heading.where(level: 4): it => block(above: 1.2em, below: 0.6em, sticky: true,
    { ak-audit("h", level: 4, title: ak-str(it.body)); text(size: ak-body-size, weight: "regular", style: "italic", it.body) })

  // --- takeaways and quotations
  show quote.where(block: true): it => ak-keep("quote",
    above: 1.3em, below: 1.3em,
    inset: (left: 1.1em, right: 0.6em, y: 0.2em),
    stroke: (left: 1.6pt + ak-ink),
    {
      set par(justify: false, first-line-indent: 0pt, spacing: 0.75em)
      set text(size: 11pt, fill: ak-ink)
      it.body
    })

  // --- figures
  show figure: set block(above: 1.8em, below: 1.8em, breakable: false)
  show figure.where(kind: "quarto-float-fig"): set figure(numbering: n => ak-number("1", n))
  show figure.where(kind: "quarto-float-tbl"): set figure(numbering: n => ak-number("1", n))
  // Image size is set per image by akita-book.lua (text width, or a max
  // height of 4.4in for tall images); figures never break.
  // Figures float to the top or bottom of the page so the text keeps
  // filling pages instead of leaving a gap before a figure that didn't fit.
  show figure.where(kind: "quarto-float-fig"): set figure(placement: auto, scope: "column")
  set place(clearance: 1.6em)
  show figure.caption: it => {
    set text(font: ak-sans, size: 8.5pt, fill: ak-muted, number-type: "lining", hyphenate: false)
    set par(justify: false, first-line-indent: 0pt, leading: 0.5em)
    block(width: 100%, above: 0.9em, align(left)[
      #text(weight: "semibold", fill: ak-ink)[#it.supplement #context it.counter.display(it.numbering)]#h(0.7em)#it.body
    ])
  }

  // --- lists, glossary (definition lists), notes, code, tables
  set list(indent: 0.4em, body-indent: 0.6em, marker: ([–], [·]))
  set enum(indent: 0.4em, body-indent: 0.6em)
  show list: set par(justify: false)
  // Short lists (up to ~6 lines) stay on one page; long ones may break
  // between items (orphan/widow rules still apply inside items).
  show list: it => ak-keep("list", it, limit: 1.25in, above: 0.9em, below: 0.9em)
  show enum: it => ak-keep("list", it, limit: 1.25in, above: 0.9em, below: 0.9em)
  show terms.item: it => block(breakable: false, above: 0.95em, below: 0.95em, {
    set par(first-line-indent: 0pt, justify: true, leading: 0.55em)
    text(font: ak-sans, size: 9.5pt, weight: "semibold", fill: ak-ink, it.term)
    block(above: 0.35em, inset: (left: 1.2em), text(size: 9.5pt, it.description))
  })
  set footnote.entry(separator: line(length: 2.5em, stroke: 0.5pt + ak-rule), gap: 0.5em)
  show footnote.entry: set text(size: 8.5pt)
  show footnote.entry: set par(leading: 0.5em, first-line-indent: 0pt)
  show raw: set text(size: 0.88em)
  show raw.where(block: true): set block(fill: luma(244), inset: 7pt, radius: 0pt, width: 100%)
  show raw.where(block: true): set par(justify: false)
  show raw.where(block: true): it => ak-keep("code", it, above: 1.1em, below: 1.1em)
  // Tables: sans 9pt, rule under the header, hairlines between rows; whole
  // on one page when they fit, else broken between rows (never inside a
  // row) with the header repeated.
  set table(inset: (x: 4pt, y: 4.5pt), align: left + top,
    stroke: (x, y) => if y > 1 { (top: 0.3pt + luma(190)) })
  set table.cell(breakable: false)
  show table: set text(font: ak-sans, size: 8.5pt, number-type: "lining")
  show table: set par(justify: false, first-line-indent: 0pt, leading: 0.5em)
  show table.cell.where(y: 0): set text(weight: "semibold", fill: ak-ink)
  show table: it => ak-keep("table", it, above: 1.4em, below: 1.4em)

  // --- links: no colour in print; bare URLs (Fontes, Referências) set small
  show link: it => if type(it.dest) == str and ak-str(it.body) == it.dest {
    text(font: ak-sans, size: 0.86em, it)
  } else { it }

  // --- bibliography (citeproc output inside the #refs div)
  show <refs>: it => {
    set text(size: 9pt)
    set par(justify: false, first-line-indent: 0pt, hanging-indent: 1.5em, leading: 0.5em)
    set block(spacing: 0.85em)
    it
  }

  // --- front matter
  ak-cover(cover, cover-alt)
  counter(page).update(1)
  ak-front(title, subtitle, author, colophon)
  if toc { ak-toc(toc-title) }

  // --- main matter: arabic folios from the first recto
  if not akita-ebook { pagebreak(to: "odd", weak: true) }
  set page(numbering: "1", header: ak-header(ak-str(title)), footer: ak-footer())
  counter(page).update(1)
  doc
}
