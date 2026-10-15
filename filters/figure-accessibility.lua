-- Keep one source contract for figures while serving each format correctly.
--
-- Authors provide:
--   fig-alt  = concise replacement text (140 characters or fewer)
--   fig-desc = the complete description needed to understand the figure
--
-- Reflowable editions expose the complete description immediately after the
-- figure. Typst/PDF receives it as the image's semantic alternative without
-- adding visible copy, preserving the print layout.

local language = "pt"

local function text_inlines(text)
  return pandoc.Inlines({ pandoc.Str(text) })
end

local function is_reflowable()
  return FORMAT:match("html") or FORMAT:match("epub")
end

local function has_class(element, wanted)
  for _, class in ipairs(element.classes) do
    if class == wanted then return true end
  end
  return false
end

function Meta(meta)
  local lang = pandoc.utils.stringify(meta.lang or "pt")
  language = lang:match("^en") and "en" or "pt"
  return meta
end

function Figure(figure)
  local description

  figure = pandoc.walk_block(figure, {
    Image = function(image)
      local short = image.attributes["fig-alt"]
      local long = image.attributes["fig-desc"]
      if not short or not long then
        return image
      end

      description = long
      local alternative = is_reflowable() and short or long
      image.caption = text_inlines(alternative)
      image.attributes["fig-alt"] = alternative
      image.attributes["fig-desc"] = nil
      return image
    end,
  })

  if not description or not is_reflowable() then
    return figure
  end

  local label = language == "en" and "Detailed image description: " or "Descrição detalhada da imagem: "
  local id = figure.identifier ~= "" and figure.identifier .. "-description" or ""
  local paragraph = pandoc.Para({ pandoc.Strong(text_inlines(label)), pandoc.Str(description) })
  return { figure, pandoc.Div({ paragraph }, pandoc.Attr(id, { "figure-description" })) }
end

-- Quarto turns figures into its own Div structure before post-Quarto filters.
-- Handle that representation too; keeping the Figure handler makes the filter
-- independently testable with Pandoc and protects against future Quarto AST
-- changes.
function Div(div)
  local description = div.attributes["fig-desc"]
  if not description or not has_class(div, "quarto-float") then
    return div
  end

  div.attributes["fig-desc"] = nil
  div = pandoc.walk_block(div, {
    Image = function(image)
      local alternative = is_reflowable() and image.attributes["fig-alt"] or description
      alternative = alternative or description
      image.caption = text_inlines(alternative)
      image.attributes["fig-alt"] = nil
      image.attributes["fig-desc"] = nil
      return image
    end,
  })

  if not is_reflowable() then
    return div
  end

  local label = language == "en" and "Detailed image description: " or "Descrição detalhada da imagem: "
  local id = div.identifier ~= "" and div.identifier .. "-description" or ""
  local paragraph = pandoc.Para({ pandoc.Strong(text_inlines(label)), pandoc.Str(description) })
  return { div, pandoc.Div({ paragraph }, pandoc.Attr(id, { "figure-description" })) }
end

-- Source captions make tables understandable when encountered out of context
-- in HTML and EPUB. They are suppressed only in Typst so the established
-- printable interiors do not reflow.
function Table(table)
  if FORMAT:match("typst") then
    table.caption = pandoc.Caption()
  end
  return table
end

-- Metadata must be read in a first pass; Pandoc otherwise visits document
-- blocks before the Meta callback in a single Lua filter.
return {
  { Meta = Meta },
  { Figure = Figure, Div = Div, Table = Table },
}
