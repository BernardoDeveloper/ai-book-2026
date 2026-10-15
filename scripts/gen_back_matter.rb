#!/usr/bin/env ruby
# frozen_string_literal: true

# Generates the machine-made back-matter pages for a language edition:
#   book/<lang>/glossario.md     placeholder div filled by filters/glossary.lua
#   book/<lang>/bibliografia.md  placeholder div filled by citeproc
#   book/<lang>/fontes.md        the original blog posts behind each chapter,
#                                built from chapter front matter `sources`
#                                (provenance made visible to readers)
#
# Usage: scripts/gen_back_matter.rb [lang]

require "yaml"
require "date"

ROOT = File.expand_path("..", __dir__)
lang = ARGV[0] || "pt"
dir = File.join(ROOT, "book", lang)
outline = YAML.load_file(File.join(ROOT, "book", "outline.yml"))
posts = YAML.load_file(File.join(ROOT, "inventory", "posts.yml"))["posts"].to_h { [_1["id"], _1] }

T = {
  "pt" => { gls: "Glossário", refs: "Referências", src: "Fontes: os artigos originais",
            bg: "Episódios anteriores citados (Akitando, 2018-2023)",
            src_intro: "Este livro nasceu de artigos publicados em akitaonrails.com ao longo de 2026. Cada capítulo abaixo lista os artigos de que deriva, para quem quiser ler a versão original, com o contexto e as datas em que foram escritos." },
  "en" => { gls: "Glossary", refs: "References", src: "Sources: the original articles",
            bg: "Earlier episodes cited (Akitando, 2018-2023)",
            src_intro: "This book grew out of articles published on akitaonrails.com during 2026. Each chapter below lists the articles it derives from, so readers can find the originals with their context and dates." },
}.fetch(lang)

def front_matter(path)
  text = File.read(path)
  return {} unless text.start_with?("---") # a chapter still being written

  YAML.safe_load(text.split(/^---[ \t]*$/, 3)[1], permitted_classes: [Date, Time]) || {}
end

File.write(File.join(dir, "glossario.md"), "# #{T[:gls]} {#sec-glossario .unnumbered}\n\n::: {#glossary}\n:::\n")
File.write(File.join(dir, "bibliografia.md"), "# #{T[:refs]} {#sec-bibliografia .unnumbered}\n\n::: {#refs}\n:::\n")

units = outline["front"] + outline["parts"].flat_map { _1["chapters"] || [_1] } + outline["back"]
lines = ["# #{T[:src]} {#sec-fontes .unnumbered}", "", T[:src_intro], ""]
cited_background = []
units.each do |u|
  file = File.join(dir, u["id"] == "prefacio" ? "index.md" : "#{u['id']}.md")
  next unless File.exist?(file)

  fm = front_matter(file)
  srcs = Array(fm["sources"]).map { _1["post"] }.uniq
  cited_background.concat(srcs.select { posts.dig(_1, "background") })
  srcs.reject! { posts.dig(_1, "background") }
  next if srcs.empty?

  # Plain titles: Typst can't cross-reference unnumbered units (preface, interludes).
  lines << "**#{fm['chapter'] || fm['title'] || u['title']}**" << ""
  srcs.sort.each do |id|
    p = posts[id] or next
    title = (lang == "en" && p["en"] ? p["en"]["title"] : p["pt"]["title"]).to_s
    url = lang == "en" && p["url_en"] ? p["url_en"] : p["url_pt"]
    date = Date.parse(p["date"]).strftime("%d/%m/%Y")
    lines << "- #{date}: *#{title.gsub('*', '')}*. <#{url}>"
  end
  lines << ""
end
unless cited_background.empty?
  lines << "**#{T[:bg]}**" << ""
  cited_background.uniq.sort.each do |id|
    p = posts[id]
    title = (lang == "en" && p["en"] ? p["en"]["title"] : p["pt"]["title"]).to_s
    url = lang == "en" && p["url_en"] ? p["url_en"] : p["url_pt"]
    lines << "- #{Date.parse(p['date']).strftime('%d/%m/%Y')}: *#{title.gsub('*', '')}*. <#{url}>"
  end
  lines << ""
end
File.write(File.join(dir, "fontes.md"), lines.join("\n"))

# Image credits, in reading order, from assets/credits/<fig>.yml. Required by
# the CC licences (full attribution) and by KDP (AI-generated disclosure).
CR = {
  "pt" => { title: "Créditos das imagens", intro: "Diagramas sem crédito foram desenhados para este livro. As ilustrações marcadas como geradas por IA foram produzidas com modelos de geração de imagem sob direção do autor; o registro completo de cada uma (modelo, instruções, data) está no repositório do livro.", diagram: "Diagrama original do livro.", ai: "Ilustração gerada por IA" },
  "en" => { title: "Image credits", intro: "Uncredited diagrams were drawn for this book. Illustrations marked as AI-generated were produced with image-generation models under the author's direction; each one's full record (model, prompt, date) is in the book's repository.", diagram: "Original diagram drawn for this book.", ai: "AI-generated illustration" },
}.fetch(lang)
credits = Dir[File.join(ROOT, "assets", "credits", "*.yml")].to_h { r = YAML.load_file(_1, permitted_classes: [Date, Time]); [r["file"], r] }
seen = []
credit_lines = ["# #{CR[:title]} {#sec-creditos .unnumbered}", "", CR[:intro], ""]
units.each do |u|
  file = File.join(dir, u["id"] == "prefacio" ? "index.md" : "#{u['id']}.md")
  next unless File.exist?(file)

  File.read(file).scan(/\]\((assets\/figures\/[^)\s]+)\)\{#(fig-[\w-]+)/).each do |path, fid|
    next if seen.include?(path)

    seen << path
    # Translated figures (assets/figures/<lang>/x.png) share the canonical record.
    rec = credits[path] || credits[path.sub(%r{figures/[a-z]{2}/}, "figures/")]
    text = case rec&.dig("kind")
           when "photo"
             if lang == "pt"
               rec.dig("credit", "backmatter")
             elsif rec.dig("credit", "backmatter_en")
               rec.dig("credit", "backmatter_en")
             else # built from the record's fields; the stored strings are Portuguese
               mods = { "redimensionada" => "resized", "recortada" => "cropped", "convertida de SVG para PNG" => "converted from SVG to PNG",
                        "em tons de cinza" => "converted to grayscale",
                        "montada lado a lado" => "placed side by side" }
               src = rec["source"] || {}
               licence_of = lambda do |r|
                 l = r.dig("license", "short").to_s
                 l.match?(/public domain|\APD|CC0/i) ? "Public domain." : "Licensed #{l}#{r.dig('license', 'url') ? ", #{r.dig('license', 'url')}" : ''}."
               end
               parts = if rec["composite_of"] # several photos in one figure: credit each
                         rec["composite_of"].map do |c|
                           %(#{c['subject']}: "#{c.dig('source', 'title')}", #{c['author']}. #{c.dig('source', 'page_url')}. #{licence_of.(c)})
                         end.join(" ")
                       else
                         %("#{src['title']}", #{rec['author']}. #{src['page_url']}. #{licence_of.(rec)})
                       end
               changes = Array(rec["modifications"]).map { m = _1.sub(/s(?= |\z)/, ""); mods.fetch(m, mods.fetch(_1, _1)) }
               %(#{parts}#{changes.empty? ? '' : " Changes: #{changes.join(', ')}."})
             end
           when "ai_illustration" then "#{CR[:ai]}: #{rec.dig('generation', 'model')}, #{rec.dig('generation', 'date').to_s[0, 10]}."
           else CR[:diagram]
           end
    credit_lines << "- @#{fid}: #{text}"
  end
end
cover = credits.values.find { _1["file"].to_s.start_with?("assets/cover/") }
if cover
  credit_lines.insert(4, "- #{lang == 'en' ? 'Cover' : 'Capa'}: #{CR[:ai]} (#{cover.dig('generation', 'model')}, #{cover.dig('generation', 'date').to_s[0, 10]}); #{lang == 'en' ? "typography by the author; author sticker: the author's official portrait illustration" : 'tipografia do autor; selo com o retrato oficial do autor (ilustração)'}.")
end
File.write(File.join(dir, "creditos.md"), credit_lines.join("\n") + "\n")
warn "wrote glossario.md, bibliografia.md, fontes.md, creditos.md for #{lang}"
