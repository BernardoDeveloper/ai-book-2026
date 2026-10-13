-- Workaround: Quarto emits alt= on the figure wrapper <div>, invalid in EPUB XHTML.
function Div(d) if d.attributes.alt then d.attributes.alt = nil; return d end end
