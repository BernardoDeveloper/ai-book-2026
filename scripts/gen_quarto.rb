#!/usr/bin/env ruby
# frozen_string_literal: true

# Generates _quarto-<lang>.yml (Quarto profile) from book/outline.yml so the
# outline stays the single source of truth for structure and order.
# Chapter files are book/<lang>/<id>.md; the preface is index.md because
# Quarto books require an index page.
#
# Usage: scripts/gen_quarto.rb [lang]   (default: pt)

require "yaml"
require "fileutils"
require "date"

ROOT = File.expand_path("..", __dir__)
lang = ARGV[0] || "pt"
outline = YAML.load_file(File.join(ROOT, "book", "outline.yml"))
LANGS = {
  "pt" => { "lang" => "pt-BR", "title" => outline.dig("meta", "working_title"), "subtitle" => outline.dig("meta", "subtitle"), "csl" => "assets/csl/abnt-akita.csl" },
  "en" => { "lang" => "en-US", "title" => outline.dig("meta", "working_title_en") || outline.dig("meta", "working_title"), "subtitle" => outline.dig("meta", "subtitle_en"), "csl" => nil },
}.freeze
cfg = LANGS.fetch(lang)
edition = outline.dig("meta", "edition") || "1.0"
isbn = outline.dig("meta", "isbn")
isbn_line = isbn ? "\n\nISBN #{isbn}" : "" # hidden until the author sets meta.isbn
year = outline.dig("meta", "cutoff").to_s[0, 4]
# Revision printed on the copyright page so a reader can match a copy to a
# release: the tag on release builds (CI sets GITHUB_REF_NAME), otherwise
# `git describe` (last tag + commits since), plus the short commit and the
# build date. "+local" marks a build with uncommitted changes.
git = ->(*a) { IO.popen(["git", "-C", ROOT, *a], err: File::NULL, &:read).to_s.strip }
rev_tag = ENV["GITHUB_REF_TYPE"] == "tag" ? ENV["GITHUB_REF_NAME"].to_s : git.("describe", "--tags", "--abbrev=0")
rev_sha = git.("rev-parse", "--short", "HEAD")
ahead = rev_tag.empty? ? "" : git.("rev-list", "--count", "#{rev_tag}..HEAD")
rev_name = rev_tag.empty? ? rev_sha : (ahead.to_i.positive? ? "#{rev_tag}+#{ahead}" : rev_tag)
rev_name += "+local" unless ENV["CI"] || git.("status", "--porcelain", "--untracked-files=no").empty?
rev_date = Time.now.strftime("%d/%m/%Y")
releases = "https://github.com/akitaonrails/ai-book-2026/releases"
revision_line = {
  "pt" => "Revisão #{rev_name} (#{rev_sha}), gerada em #{rev_date}. Versões e correções: #{releases}",
  "en" => "Revision #{rev_name} (#{rev_sha}), built #{Time.now.strftime('%Y-%m-%d')}. Versions and corrections: #{releases}",
}
author = outline.dig("meta", "author")
owned = Array(outline.dig("meta", "owned_names"))
licenses = outline.dig("meta", "open_source_licenses") || {}
owned_pt = owned.size > 1 ? "#{owned[0..-2].join(', ')} e #{owned.last}" : owned.first.to_s
owned_en = owned.size > 1 ? "#{owned[0..-2].join(', ')} and #{owned.last.sub(' e demais projetos da série', ' and the rest of the series')}" : owned.first.to_s
lic_pt = licenses.map { |k, v| "#{k}: #{v}" }.join("; ")
RIGHTS = {
  "pt" => "© #{year} #{author}. Todos os direitos reservados.",
  "en" => "© #{year} #{author}. All rights reserved.",
}.freeze

# Copyright / colophon page of the PDF (verso of the title page), as Markdown.
COLOPHON = {
  "pt" => <<~MD,
    **#{cfg['title']}**\\
    #{cfg['subtitle']}

    #{RIGHTS['pt']} Nenhuma parte deste livro pode ser reproduzida ou transmitida, por qualquer meio, sem autorização por escrito do autor, exceto em citações breves com indicação da fonte. É proibida a tradução, adaptação ou criação de obras derivadas. O autor reserva expressamente os direitos de mineração de textos e dados sobre esta obra, inclusive para treinar ou avaliar modelos de aprendizado de máquina.

    Os nomes #{owned_pt} são de propriedade de #{author}. O código de alguns desses projetos é aberto, sob a licença indicada em cada repositório (#{lic_pt}); essas licenças cobrem o código e não se estendem aos nomes nem a este livro. Os demais nomes de produtos e empresas citados pertencem a seus respectivos donos e aparecem apenas para identificação.

    Edição #{edition}, #{year}.#{isbn_line}

    #{revision_line['pt']}

    As figuras criadas com inteligência artificial estão identificadas como tal nos créditos das imagens, com a ferramenta usada em cada uma.

    Composto em Source Serif 4 e Source Sans 3; título da capa em Limelight (todas sob a SIL Open Font License).

    akitaonrails.com
  MD
  "en" => <<~MD,
    **#{cfg['title']}**\\
    #{cfg['subtitle']}

    #{RIGHTS['en']} No part of this book may be reproduced or transmitted in any form without the author's written permission, except for brief quotations with attribution. Translation, adaptation and derivative works are prohibited. The author expressly reserves text and data mining rights over this work, including its use to train or evaluate machine-learning models.

    The names #{owned_en} are the property of #{author}. Some of these projects' code is open source under the licence stated in each repository (#{lic_pt}); those licences cover the code and do not extend to the names or to this book. Other product and company names belong to their respective owners and appear for identification only.

    Edition #{edition}, #{year}.#{isbn_line}

    #{revision_line['en']}

    Figures made with artificial intelligence are disclosed as such in the image credits, with the tool used for each one.

    Set in Source Serif 4 and Source Sans 3; cover title in Limelight (all under the SIL Open Font License).

    akitaonrails.com
  MD
}.freeze

# PARTIAL=1 builds with whatever chapters exist (for previews mid-drafting);
# the root index.md is a stub if the preface isn't written yet.
partial = ENV["PARTIAL"] == "1"
file_for = ->(id) { id == "prefacio" ? "book/#{lang}/index.md" : "book/#{lang}/#{id}.md" }
missing = []
want = lambda do |id|
  path = file_for.(id)
  if File.exist?(File.join(ROOT, path))
    # Quarto only accepts a home page whose path starts with "index.", i.e. at
    # the project root, so the edition's preface is copied there (gitignored).
    next path unless id == "prefacio"

    FileUtils.cp(File.join(ROOT, path), File.join(ROOT, "index.md"))
    next "index.md"
  end

  missing << path
  if partial && id == "prefacio"
    File.write(File.join(ROOT, "index.md"), "# Prévia {#sec-prefacio .unnumbered}\n\nEdição parcial, gerada durante a redação.\n")
    next "index.md"
  end
  partial ? nil : path
end

chapters = outline["front"].map { want.(_1["id"]) }.compact
outline["parts"].each do |part|
  if part["chapters"]
    chs = part["chapters"].map { want.(_1["id"]) }.compact
    title = lang == "pt" ? part["title"] : (part["title_#{lang}"] || part["title"])
    chapters << { "part" => title, "chapters" => chs } unless chs.empty?
  elsif chapters.last.is_a?(Hash)
    # Interludes ride at the end of the preceding part (Quarto parts can't
    # be followed by loose chapters); they are unnumbered in their files.
    chapters.last["chapters"] << want.(part["id"])
  else
    chapters << want.(part["id"])
  end
  chapters.compact!
  chapters.last["chapters"].compact! if chapters.last.is_a?(Hash)
end
back = outline["back"]
chapters.concat(back.reject { _1["kind"] == "appendix" || _1["kind"] == "generated" }.map { want.(_1["id"]) }.compact)
appendices = back.select { %w[appendix generated].include?(_1["kind"]) }.map { want.(_1["id"]) }.compact

profile = {
  "project" => { "output-dir" => "build/#{lang}" },
  "lang" => cfg["lang"],
  "book" => { "title" => cfg["title"], "subtitle" => cfg["subtitle"], "chapters" => chapters, "appendices" => appendices }.compact,
  "glossary-file" => "book/back/glossary-#{lang}.yml",
  "glossary-page" => "glossario.html",
  # Quarto localizes the HTML appendix label but EPUB falls back to English
  # "Appendix" unless crossref.appendix-title is set explicitly.
  "crossref" => { "appendix-title" => { "pt" => "Apêndice", "en" => "Appendix" }.fetch(lang) },
  "toc-title" => { "pt" => "Sumário", "en" => "Contents" }.fetch(lang),
  "colophon" => COLOPHON.fetch(lang),
  "rights" => RIGHTS.fetch(lang), # EPUB dc:rights
}
profile["book"]["page-footer"] = { "center" => "#{RIGHTS.fetch(lang)} akitaonrails.com" } # HTML edition
profile["csl"] = cfg["csl"] if cfg["csl"]
begin # every edition reads a filtered copy of the bibliography
  # abnt-akita.csl prints the `note` field (NBR 6023 complements such as the
  # Wayback copy of a dead link), but in references.yaml `note` also carries
  # editorial provenance ("cited-by: <post> (...)") that must never reach
  # readers. Citeproc reads a copy whose note keeps only "Arquivado em: <url>".
  refs = YAML.load_file(File.join(ROOT, "book", "back", "references.yaml"))
  refs["references"].each do |ref|
    archived = ref["note"].to_s.scan(/Arquivado em:\s*(\S+)/).flatten
    label = lang == "pt" ? "Arquivado em" : "Archived at"
    archived.empty? ? ref.delete("note") : ref["note"] = "#{label}: #{archived.join(', ')}"
  end
  public_bib = "build/references-#{lang}.yaml"
  FileUtils.mkdir_p(File.join(ROOT, "build"))
  File.write(File.join(ROOT, public_bib),
             "# GENERATED by scripts/gen_quarto.rb from book/back/references.yaml. Do not edit.\n" + refs.to_yaml)
  profile["bibliography"] = public_bib
end
# Units whose H1 is .unnumbered, for filters/unnumbered-refs.lua.
unnumbered = (outline["front"] + outline["parts"].reject { _1["chapters"] } + outline["back"].reject { _1["kind"] == "appendix" })
profile["unnumbered-sections"] = unnumbered.to_h do |u|
  file = u["id"] == "prefacio" ? "index.html" : "#{u['id']}.html"
  # Link text is the unit's title in this edition (its file's `chapter:`).
  src = File.join(ROOT, "book", lang, u["id"] == "prefacio" ? "index.md" : "#{u['id']}.md")
  fm = File.exist?(src) && File.read(src)[/\A---\n(.*?)\n---/m, 1]
  title = (fm && YAML.safe_load(fm, permitted_classes: [Date, Time])&.dig("chapter")) || u["title"]
  ["sec-#{u['id']}", { "title" => title, "file" => file }]
end

# Each edition has its own cover, with the title typeset in its language.
if lang != "pt"
  cover = "assets/cover/cover-#{lang}.png"
  profile["book"]["cover-image"] = cover
  profile["format"] = { "epub" => { "epub-cover-image" => cover }, "akita-book-typst" => { "pdf-cover" => cover } }
end

File.write(File.join(ROOT, "_quarto-#{lang}.yml"),
           "# GENERATED by scripts/gen_quarto.rb from book/outline.yml. Do not edit.\n" + profile.to_yaml.sub(/\A---\n/, ""))
warn "wrote _quarto-#{lang}.yml (#{chapters.flatten.size} entries, #{appendices.size} appendices)"
if !missing.empty? && !partial
  warn "missing chapter files (#{missing.size}):"
  missing.each { warn "  #{_1}" }
  exit 2
end
