-- @sec-<id> pointing at an unnumbered unit (preface, interludes, epilogue,
-- generated back matter) can't be resolved by Typst and renders as "?" in
-- other formats. scripts/gen_quarto.rb publishes `unnumbered-sections`
-- (id -> {title, file}); turn those citations into a link titled with the
-- unit's name. Multi-page HTML needs the target page in the URL.
local units = {}

local function load(meta)
  local m = meta['unnumbered-sections']
  if not m then return end
  for id, v in pairs(m) do
    units[id] = { title = pandoc.utils.stringify(v.title), file = pandoc.utils.stringify(v.file) }
  end
end

local function cite(el)
  if #el.citations ~= 1 then return nil end
  local u = units[el.citations[1].id]
  if not u then return nil end
  local target = '#' .. el.citations[1].id
  if FORMAT:match('^html') then target = u.file .. target end
  return pandoc.Link(pandoc.Inlines(u.title), target)
end

return { { Meta = load }, { Cite = cite } }
