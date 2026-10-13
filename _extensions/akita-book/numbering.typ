// akita-book numbering. Floats, equations and callouts are numbered per
// chapter ("Figura 5.1"); in unnumbered chapters (prefácio, interlúdios) they
// are numbered plainly, and in appendices they take the appendix letter
// ("Figura A.1"). `ak-chapter` holds the current prefix and is updated by the
// chapter-opening show rule in typst-template.typ.
#let ak-chapter = state("ak-chapter", none)
// Called by Typst inside the numbered element's own context (also when a
// reference elsewhere displays it), so no `context` wrapper here: wrapping
// would read the state at the reference instead of at the figure.
#let ak-number(pattern-plain, n) = {
  let c = ak-chapter.get()
  if c == none { numbering(pattern-plain, n) } else { c + "." + numbering(pattern-plain, n) }
}
#let equation-numbering = n => [(#ak-number("1", n))]
#let callout-numbering = n => ak-number("1", n)
#let subfloat-numbering(n-super, subfloat-idx) = [#ak-number("1", n-super)#numbering("a", subfloat-idx)]
#let theorem-inherited-levels = 1
#let theorem-numbering(loc) = "1.1"
#let theorem-render(prefix: none, title: "", full-title: auto, body) = {
  block(width: 100%, inset: (left: 1em), stroke: (left: 1pt + black))[
    #if full-title != "" and full-title != auto and full-title != none {
      strong[#full-title]
      linebreak()
    }
    #body
  ]
}
