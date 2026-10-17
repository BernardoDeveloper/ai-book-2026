-- akita-book.lua: book structure for the akita-book Typst format.
--
-- Quarto marks every book item with file metadata (bookItemType = part,
-- chapter or appendix). Quarto delegates part/appendix rendering in Typst to
-- the book extension, so this filter does it:
--   * part headings and the synthetic "Apêndices" divider become unnumbered
--     level-1 headings labelled <akita-part>; the template renders them as
--     divider pages and lists them in the Sumário as part lines;
--   * right after the appendix divider it switches the template to appendix
--     mode (`#ak-start-appendices()`): the heading counter restarts and numbered
--     appendix chapters are lettered A, B, C... ("Apêndice A"), while
--     generated back matter whose H1 carries .unnumbered stays unlettered.
-- Chapters keep Quarto's numbering: a chapter whose H1 carries .unnumbered
-- (front matter, interludes, epilogue, back matter) does not step the
-- Typst heading counter, so numbering is continuous (1..N) across parts.

local in_appendix = false

local function typst_inlines(inlines)
  local out = pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), 'typst')
  return (out:gsub('%s+$', ''))
end

local function part_heading(el)
  return pandoc.RawBlock('typst',
    '#heading(level: 1, numbering: none)[' .. typst_inlines(el.content) .. '] <akita-part>')
end

local function header(el)
  if not quarto.doc.is_format('typst') or el.level ~= 1 then return nil end
  local fs = quarto.doc.file_metadata()
  local file = fs and fs.file
  local kind = file and file.bookItemType

  if kind == 'part' then return part_heading(el) end
  if kind == 'appendix' and el.classes:includes('unnumbered') and not in_appendix then
    in_appendix = true
    return { part_heading(el), pandoc.RawBlock('typst', '#ak-start-appendices()') }
  end
  return nil
end

-- Citations missing from the bibliography: citeproc renders them as "key?"
-- but, with link-citations, also links them to <ref-key>, a label that does
-- not exist, and Typst aborts the whole PDF. Unlink them here (citeproc still
-- warns) so a half-merged references.yaml can't break the book build.
local function unlink_missing_citations(doc)
  if not quarto.doc.is_format('typst') then return nil end
  local ok, refs = pcall(pandoc.utils.references, doc)
  if not ok then return nil end
  local known = {}
  for _, r in ipairs(refs) do known[r.id] = true end
  return doc:walk({
    Cite = function(c)
      local missing = false
      for _, ct in ipairs(c.citations) do
        if not known[ct.id] then missing = true end
      end
      if not missing then return nil end
      local out = pandoc.Inlines({})
      for i, ct in ipairs(c.citations) do
        if i > 1 then out:insert(pandoc.Str('; ')) end
        if known[ct.id] then
          out:insert(pandoc.Cite({ pandoc.Str('@' .. ct.id) }, { ct }))
        else
          out:insert(pandoc.Strong({ pandoc.Str(ct.id .. '?') }))
        end
      end
      return out
    end,
  })
end

-- Figure sizing. Images in figures fill the text width, except when that
-- would make them taller than MAX_H (60% of the 7.35in text block): then
-- they get that height and keep their aspect ratio (centred by the figure).
-- An explicit width in the source (e.g. {width=60%}) is respected, with the
-- same height cap. Pixel sizes are read from the PNG/JPEG header.
local TEXT_W, MAX_H = 4.5, 4.4  -- inches

local function be(s, i, n)
  local v = 0
  for k = i, i + n - 1 do v = v * 256 + s:byte(k) end
  return v
end

local function image_size(path)
  local f = io.open(path, 'rb')
  if not f then return nil end
  local s = f:read(65536) or ''
  f:close()
  if s:sub(1, 8) == '\137PNG\r\n\26\n' then
    return be(s, 17, 4), be(s, 21, 4)
  end
  if s:sub(1, 2) == '\255\216' then
    local i = 3
    while i + 8 < #s do
      if s:byte(i) ~= 0xFF then return nil end
      local marker, len = s:byte(i + 1), be(s, i + 2, 2)
      if marker >= 0xC0 and marker <= 0xCF and marker ~= 0xC4 and marker ~= 0xC8 and marker ~= 0xCC then
        return be(s, i + 7, 2), be(s, i + 5, 2)
      end
      i = i + 2 + len
    end
  end
  return nil
end

-- Pipe tables whose source rows are long get equal column widths from
-- Pandoc (33/33/33), which wastes the narrow date column. When all widths
-- are equal, let Typst size the columns to their content instead.
local function table_widths(tbl)
  if not quarto.doc.is_format('typst') then return nil end
  local first = tbl.colspecs[1] and tbl.colspecs[1][2]
  if type(first) ~= 'number' then return nil end
  for _, cs in ipairs(tbl.colspecs) do
    if type(cs[2]) ~= 'number' or math.abs(cs[2] - first) > 0.001 then return nil end
  end
  for i, cs in ipairs(tbl.colspecs) do
    tbl.colspecs[i] = { cs[1], pandoc.ColWidthDefault }
  end
  return tbl
end

local function size_image(img)
  if not quarto.doc.is_format('typst') then return nil end
  local w, h = image_size(img.src)
  if not w or w == 0 then return nil end
  local frac = 1.0
  local wattr = img.attributes.width
  if wattr then
    local pct = wattr:match('^([%d.]+)%%$')
    if not pct then return nil end  -- absolute sizes are the author's call
    frac = tonumber(pct) / 100
  end
  if img.attributes.height then return nil end
  local natural_h = TEXT_W * frac * h / w
  if natural_h > MAX_H then
    img.attributes.width = nil
    img.attributes.height = string.format('%.2fin', MAX_H)
  else
    img.attributes.width = string.format('%g%%', frac * 100)
  end
  return img
end

-- Wrap each chapter's body (after its H1, up to the next H1) in
-- `#ak-unit("<id>")[...]` so the template can apply per-chapter settings.
-- Used to pull up a chapter whose last page would hold only a few lines:
-- `rake build` compiles again with `--input tighten=<ids>` for the chapters
-- scripts/page_audit.rb reports as RUNT-END (tracking -0.006em, invisible).
local function wrap_units(doc)
  if not quarto.doc.is_format('typst') then return nil end
  local out, open = pandoc.Blocks({}), false
  for _, b in ipairs(doc.blocks) do
    local h1 = b.t == 'Header' and b.level == 1
    if h1 and open then
      out:insert(pandoc.RawBlock('typst', ']'))
      open = false
    end
    out:insert(b)
    if b.t == 'Header' and b.level == 1 then
      local id = b.identifier:gsub('^sec%-', '')
      out:insert(pandoc.RawBlock('typst', '#ak-unit("' .. id .. '")['))
      open = true
    end
  end
  if open then out:insert(pandoc.RawBlock('typst', ']')) end
  doc.blocks = out
  return doc
end

return {
  { Meta = function(meta)
      -- UICLAP has a shorter text block after its print safety margins.
      TEXT_W = meta['uiclap-print'] and (115 / 25.4) or 4.5
      MAX_H = meta['uiclap-print'] and 4.2 or 4.4
    end },
  { Pandoc = unlink_missing_citations },
  quarto.utils.combineFilters({
  quarto.utils.file_metadata_filter(),
  { Header = header, Image = size_image, Table = table_widths },
  }),
  { Pandoc = wrap_units },
}
