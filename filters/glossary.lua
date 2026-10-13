-- Minimal glossary filter (pandoc / Quarto).
-- Source:   [LLM]{.gls}  or  [modelos]{.gls key=llm}
-- Output:   link to #gls-<key>; first use expands "Long (SHORT)".
-- Placeholder Div #glossary is replaced by a sorted definition list.
-- Glossary data: YAML file named by metadata `glossary-file`.

local entries, seen, used = {}, {}, {}
local multi_page_html = false

local function load(meta)
  local f = meta['glossary-file']
  if not f then return end
  local fh = assert(io.open(pandoc.utils.stringify(f), 'r'))
  local doc = pandoc.read('---\n' .. fh:read('a') .. '\n---\n', 'markdown')
  fh:close()
  for k, v in pairs(doc.meta) do entries[k] = v end
  multi_page_html = FORMAT:match('^html') ~= nil and meta['glossary-page'] ~= nil
  if multi_page_html then
    multi_page_html = pandoc.utils.stringify(meta['glossary-page'])
  end
end

local function target(key)
  if multi_page_html then return multi_page_html .. '#gls-' .. key end
  return '#gls-' .. key
end

local function span(el)
  if not el.classes:includes('gls') then return nil end
  local key = el.attributes.key or pandoc.utils.stringify(el.content):lower()
  local e = entries[key]
  if not e then
    io.stderr:write('[glossary] unknown key: ' .. key .. '\n')
    return nil
  end
  used[key] = true
  local content = el.content
  -- Expand "Long (SHORT)" only when the marked text is the acronym itself;
  -- "[placas de vídeo]{.gls key=gpu}" must not become "Graphics Processing
  -- Unit (placas de vídeo)". Such uses don't count as the first use either.
  local is_acronym = pandoc.text.lower(pandoc.utils.stringify(el.content))
                     == pandoc.text.lower(pandoc.utils.stringify(e.term))
  if e.long and is_acronym and not seen[key] then
    content = pandoc.Inlines(pandoc.utils.stringify(e.long) .. ' (')
    content:extend(el.content)
    content:insert(pandoc.Str(')'))
  end
  if is_acronym or not e.long then seen[key] = true end
  return pandoc.Link(content, target(key), '', pandoc.Attr('', {'gls'}))
end

local function glossary_div(el)
  if el.identifier ~= 'glossary' then return nil end
  local keys = {}
  for k in pairs(entries) do keys[#keys + 1] = k end
  -- Dictionary order: case- and accent-insensitive ("Código" sorts with "Co",
  -- not after "z"; Lua compares bytes, so fold accents before comparing).
  local folds = { ['á']='a', ['à']='a', ['â']='a', ['ã']='a', ['é']='e', ['ê']='e', ['í']='i',
                  ['ó']='o', ['ô']='o', ['õ']='o', ['ú']='u', ['ü']='u', ['ç']='c' }
  local function sort_key(k)
    local s = pandoc.text.lower(pandoc.utils.stringify(entries[k].term))
    for from, to in pairs(folds) do s = s:gsub(from, to) end
    return s
  end
  table.sort(keys, function(a, b) return sort_key(a) < sort_key(b) end)
  local items = {}
  for _, k in ipairs(keys) do
    local e = entries[k]
    local term = pandoc.Inlines{pandoc.Span(pandoc.utils.stringify(e.term), pandoc.Attr('gls-' .. k))}
    if e.long then term:insert(pandoc.Str(' (' .. pandoc.utils.stringify(e.long) .. ')')) end
    items[#items + 1] = {term, {pandoc.Plain(pandoc.Inlines(pandoc.utils.stringify(e.def)))}}
  end
  local dl = pandoc.DefinitionList(items)
  if FORMAT:match('epub') or FORMAT:match('html') then
    -- DPUB-ARIA semantics for EPUB accessibility / reading systems
    return pandoc.Div({dl}, pandoc.Attr('glossary', {}, {role = 'doc-glossary'}))
  end
  return dl
end

return {
  {Meta = load},
  {Span = span},
  {Div = glossary_div},
}
