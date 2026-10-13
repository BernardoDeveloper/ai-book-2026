-- Removes <!-- src: ... --> provenance markers (docs/DESIGN.md) so they never
-- reach any output format. Any other HTML comment is dropped too: comments
-- in chapter sources are notes for editors, not for readers.
-- Exception: Quarto's own `<!-- quarto-file-metadata: ... -->` markers, which
-- tell later filters which book item (part, chapter, appendix) each heading
-- belongs to. Dropping them silently breaks part pages and unnumbered
-- chapters in the Typst book.
local function is_comment(el)
  return (el.format == 'html' or el.format == 'markdown')
    and el.text:match('^%s*<!%-%-') ~= nil
    and el.text:match('^%s*<!%-%-%s*quarto%-file%-metadata:') == nil
end
function RawBlock(el) if is_comment(el) then return {} end end
function RawInline(el) if is_comment(el) then return {} end end
