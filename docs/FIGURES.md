# Producing figures (contract for figure agents)

Requests live in `book/pt/_figs/<chapter>.yml` (fig id, kind, idea, labels_pt,
caption, alt). The chapter already contains the image line
`![caption](assets/figures/<fig>.png){#fig-<fig> fig-alt="..."}`.
House style: docs/research/IMAGES.md §4 (palette, lines, grayscale-safe, no
text in AI art, no real people generated). Every figure ends as
`assets/figures/<fig>.png` (sRGB, no alpha, long side 1800-2400 px) with a
provenance record `assets/credits/<fig>.yml`.

## Pick the medium (you may change the requested kind if another serves better)

| Need | Medium | Tool |
|---|---|---|
| Boxes, arrows, loops, flows, layers, comparisons | D2 diagram | `assets/diagrams/<fig>.d2` starting with `...@_house` (classes navy/teal/sand/gray/accent/danger/note), labels as `{{key}}` in `assets/diagrams/<fig>.labels.yml` with `pt:` (and `en:` translated too, for the future EN edition); render `ruby scripts/render_diagram.rb assets/diagrams/<fig>.d2 pt tools/d2-v0.9.0/bin/d2` |
| Data (bar charts etc.) | matplotlib chart | `assets/charts/<fig>.py` (run with `uv run --with matplotlib python -I assets/charts/<fig>.py pt`), data inline with a comment citing the chapter/post it comes from, labels from a dict per language, house palette, Noto Sans from assets/fonts, paper background #FBF9F4, writes assets/figures/<fig>.png at 300 dpi |
| Metaphor / scene (desk, iceberg, relay) | AI concept art, label-free | `ruby scripts/gen_image.rb <fig> "<scene>" --size 1536x1024 --quality high --n 2`, then look at both drafts (build/genimg/) and `--select N` the better. If labels are essential, overlay them afterwards with ImageMagick `-annotate` using assets/fonts/NotoSans-SemiBold.ttf (record the overlay in post_processing). Budget: at most 3 generation calls per figure |
| Real person, object, event | Photo | `ruby scripts/commons_fetch.rb --search "<query>"`, pick a free-licence file with adequate resolution, then `ruby scripts/commons_fetch.rb <fig> "File:..."` |

Diagram and chart credit records: write `assets/credits/<fig>.yml` with
`id, kind: diagram_code|chart_code, file, source (the .d2/.py path), tool,
authored_by: "author+llm", kdp_disclosure: none, credit: null`.

## Quality bar

- Look at every output (Read the PNG). Check: labels legible at ~10 cm wide,
  nothing clipped, PT accents correct, no overlapping text, house palette,
  readable in grayscale (`magick in.png -colorspace Gray /tmp/...png`).
- One idea per figure. Fewer, larger labels beat many small ones.
- Labels must match the chapter text's terms exactly.

## Allowed edits to chapters

Only the image line of your figures: you may (a) append the credit to the
caption for photos and AI art (`Foto: Autor / Wikimedia Commons, CC BY-SA 4.0`
or `Ilustração gerada por IA.`), (b) fix the caption/alt so they match the
final figure, (c) change the file extension if the asset is .jpg. Nothing else.
