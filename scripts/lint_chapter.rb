#!/usr/bin/env ruby
# frozen_string_literal: true

# Mechanical checks for book chapter sources (docs/BOOK-VOICE.md). Catches what
# a reread misses: dashes, banned phrases, long paragraphs, raw URLs, unknown
# citation or glossary keys, missing provenance. Judgment calls stay with the
# humanizer and akita-finish passes.
#
# Usage: scripts/lint_chapter.rb FILE...   (BOOK_LANG=pt by default)
# Exit 1 on errors; warnings don't fail.

require "yaml"
require "date"

ROOT = File.expand_path("..", __dir__)
LANG = ENV.fetch("BOOK_LANG", "pt")
LANG_DIR = File.join(ROOT, "book", LANG)

def yaml_or_empty(path)
  (File.exist?(path) && YAML.load_file(path, permitted_classes: [Date])) || {}
end

# Citation keys: merged bibliography + per-chapter proposals (book/<lang>/_refs/*.yaml).
ref_keys = [File.join(ROOT, "book", "back", "references.yaml"), *Dir[File.join(LANG_DIR, "_refs", "*.yaml")]]
           .flat_map { Array(yaml_or_empty(_1)["references"]).map { |r| r["id"] } }
# Glossary keys: book/back/glossary-<lang>.yml + per-chapter proposals (book/<lang>/_gls/*.yml).
glossary_keys = [File.join(ROOT, "book", "back", "glossary-#{LANG}.yml"), *Dir[File.join(LANG_DIR, "_gls", "*.yml")]]
                .flat_map { yaml_or_empty(_1).keys }

BANNED = {
  /[—–]/ => "em/en dash",
  /[“”‘’]/ => "curly quote (typesetter handles quotes)",
  /\bnão é [^.]{1,60}, é /i => "negative parallelism 'não é X, é Y'",
  /, e não [^.]{1,40}\./i => "negative tail ', e não Y'",
  /pra ser (honest|sincer|franc)|vou ser direto|preciso ser direto|sem rodeios|verdade seja dita|devo admitir|justiça seja/i => "directness/honesty signaling",
  /\bhonest[ao]s?\b|honestidade/i => "'honesto' as ornament",
  /cirúrgic/i => "'cirúrgico' as praise",
  /assino embaixo|suculent|cutuc|lindo de/i => "effusive flourish",
  /neste (post|artigo)|no (post|artigo) (de|anterior)|atualização:|\bUPDATE\b/i => "blog-ism",
  /\b(ontem|semana passada|mês passado)\b/i => "relative time (use absolute dates)",
  /\b(delve|tapestry|testament|pivotal|underscore)\b/i => "stock AI word",
}.freeze
NON_PROSE = /\A\s*(#|>|[-*+] |\d+\. |\||<!--|!\[|:::|\{)/

errors = 0
warnings = 0
report = lambda do |level, file, line, msg|
  puts "#{file}:#{line}: #{level}: #{msg}"
  level == "error" ? errors += 1 : warnings += 1
end

ARGV.each do |path|
  rel = path.delete_prefix(ROOT + "/")
  text = File.read(path)
  unless text.start_with?("---")
    report.("error", rel, 1, "missing YAML front matter")
    next
  end
  _, fm_raw, body = text.split(/^---[ \t]*$/, 3)
  fm = YAML.safe_load(fm_raw, permitted_classes: [Date, Time]) || {}
  offset = fm_raw.lines.size + 1

  %w[id sources blog_commit].each do |k|
    report.("error", rel, 1, "front matter lacks '#{k}'") unless fm.key?(k)
  end
  # `title:` would make Quarto print the chapter heading twice; the H1 is the
  # title and `chapter:` carries the same text for scripts. (Wave A drafts used
  # `title:`; scripts/fix_front_matter.rb renames it.)
  report.("error", rel, 1, "front matter needs 'chapter' (not 'title')") unless fm.key?("chapter") || fm.key?("title")
  Array(fm["sources"]).each do |s|
    report.("error", rel, 1, "source #{s.inspect} needs post + sha256") unless s.is_a?(Hash) && s["post"] && s["sha256"]
  end

  in_code = false
  para = []
  para_start = 0
  check_para = lambda do
    unless para.empty?
      prose = para.join(" ").gsub(/\b(Sr|Dr|etc|ex|vs|p\.ex|cap|fig)\./i, "").gsub(/\d+\.\d+/, "0")
      sentences = prose.scan(/[^.!?]+[.!?]+(\s|\z)/).size
      report.("warning", rel, para_start, "paragraph has #{sentences} sentences (ceiling 4)") if sentences > 4
    end
    para.clear
  end

  srcs_seen = false
  body.lines.each_with_index do |line, i|
    n = i + offset
    if line.start_with?("```")
      in_code = !in_code
      next
    end
    next if in_code

    srcs_seen = true if line.include?("<!-- src:")
    next if line.include?("<!--")

    BANNED.each { |re, msg| report.("error", rel, n, "#{msg}: #{line.strip[0, 80]}") if line =~ re }
    report.("error", rel, n, "raw URL in prose; use a citation [@key]") if line =~ %r{https?://}
    line.scan(%r{(?<![\w./])@([\w:.-]*\w)}).flatten.each do |key|
      next if key.start_with?("fig-", "sec-", "tbl-")

      report.("error", rel, n, "unknown citation key @#{key} (add it to _refs/)") unless ref_keys.include?(key)
    end
    line.scan(/\[([^\]]+)\]\{\.gls(?:\s+key=([\w-]+))?\}/).each do |term, key|
      key ||= term.downcase
      report.("error", rel, n, "glossary key '#{key}' unknown (use key= or propose it in _gls/)") unless glossary_keys.include?(key)
    end

    if line.strip.empty? || line =~ NON_PROSE
      check_para.()
    else
      para_start = n if para.empty?
      para << line.strip
    end
  end
  check_para.()
  report.("error", rel, 1, "no <!-- src: ... --> provenance markers") unless srcs_seen
end

puts "#{errors} error(s), #{warnings} warning(s)"
exit(errors.zero? ? 0 : 1)
