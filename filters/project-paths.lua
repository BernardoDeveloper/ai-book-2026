-- Chapter sources reference images from the project root ("assets/figures/x.png")
-- because that is readable and grep-able. Quarto treats image paths as relative
-- to the chapter file (book/<lang>/):
--   * merged formats (PDF, EPUB, DOCX) arrive here already prefixed with the
--     chapter dir ("book/pt/assets/..."): strip the prefix back to the root path;
--   * multi-page HTML keeps one page per chapter under book/<lang>/: climb up.
function Image(img)
  local stripped = img.src:match('^book/[%w-]+/(assets/.*)$')
  if stripped then
    img.src = stripped
    return img
  end
  if img.src:match('^assets/') and FORMAT:match('^html') then
    img.src = '../../' .. img.src
    return img
  end
end
