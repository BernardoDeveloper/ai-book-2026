# Accessibility contract

The EPUB and HTML editions target WCAG 2.2 AA and EPUB Accessibility 1.2.
The PDF interiors remain visually identical, but retain their existing tagged
PDF/UA structure and full semantic descriptions. Conformance metadata is only
published when a qualified manual audit supports it.

## Writing a chapter

Use real headings in order, ordinary Markdown lists and links whose words make
sense out of context. Never encode meaning with color alone. Avoid instructions
that depend only on position, shape or color ("the red item on the right").

Every meaningful figure needs three separate pieces of text:

```markdown
![Visible caption.](assets/figures/example.png){#fig-example
  fig-alt="Concise replacement text, no more than 140 characters."
  fig-desc="Complete description of the information, relationships and relevant labels in the image."}
```

- The caption tells every reader why the figure is here.
- `fig-alt` identifies its essential content quickly. Do not begin with
  "image of" or repeat the caption word for word.
- `fig-desc` carries every fact needed to understand or replace the visual.
  Describe relationships, axes, trends, labels and conclusions; omit decoration.

The build exposes `fig-desc` below the figure in EPUB/HTML. In PDF it becomes
the image's semantic replacement without adding visible text, preserving the
print layout. A decorative image should be rare and requires an explicit empty
alternative plus review; do not silently omit either field.

Give each table a sentence-style caption on the line immediately after it:

```markdown
| Item | Result |
|---|---|
| Example | 42 |

: Results discussed in this section.
```

Keep tables simple: one header row, no merged cells, and no layout tables. Put
the conclusion in prose as well when the exact visual comparison matters.

## Release checks

`rake check` rejects missing or overlong alternatives in current and future
chapters. `rake build` validates EPUB packaging and accessibility, then audits
both PDFs. Before release, also inspect keyboard navigation and screen-reader
reading order in the HTML/EPUB, check zoom and reflow, and manually review every
complex figure description. Automated checks cannot establish full WCAG or
EPUB Accessibility conformance.

The longer rationale, standards baseline and implementation priorities live in
[`docs/research/ACCESSIBILITY.md`](research/ACCESSIBILITY.md).
