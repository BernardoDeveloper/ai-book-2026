#!/usr/bin/env ruby
# frozen_string_literal: true

# Book integrity check. Run after any change, before building or releasing.
# Born from the February cut-off rewrite, where removing source material broke
# callbacks in chapters nobody touched ("os cinco revisores de @sec-ch05").
#
# Source checks (fast, no build needed):
#   ids        every @sec-/@fig- reference resolves to an id defined in the edition
#   citations  every [@key] exists in the bibliography; uncited entries (warning)
#   glossary   every {.gls} key exists; defined-but-unused keys (warning)
#   figures    every image exists, has a credits record, isn't a placeholder
#   provenance markers and front-matter sources agree; no source predates the
#              cut-off (outline meta.source_from) or is in outline `excluded`
#   callbacks  heuristic: a sentence that points at another unit (@sec-x) and
#              names something (quoted phrase, Capitalised Name, number) must
#              find at least one of those names in the target unit (warning)
#   parity     (non-PT editions) same src-marker sequence and the same
#              ids/citations/figures as the PT unit; translated_from is current
# Output checks (--output, after `rake build`):
#   the render log has no unresolved cross-references, unknown glossary keys
#   or missing citations; the PDF text has no "??" / "key?" artefacts
# Also writes build/<lang>/seams.md: each unit's last paragraph next to the
# next unit's first, for a quick human or agent review of the hand-offs.
#
# Usage: scripts/doctor.rb [--lang pt] [--output] [--release]
# Exit 1 on errors. --release turns placeholder figures and stale
# translations into errors.

require "yaml"
require "date"
require "digest"
require "optparse"

opts = { lang: "pt", output: false, release: false }
OptionParser.new do |o|
  o.on("--lang LANG") { opts[:lang] = _1 }
  o.on("--output") { opts[:output] = true }
  o.on("--release") { opts[:release] = true }
end.parse!

ROOT = File.expand_path("..", __dir__)
LANG = opts[:lang]
DIR = File.join(ROOT, "book", LANG)
GENERATED = %w[glossario bibliografia fontes creditos].freeze
outline = YAML.load_file(File.join(ROOT, "book", "outline.yml"))
errors = []
warnings = []
err = ->(where, msg) { errors << "#{where}: #{msg}" }
warn_ = ->(where, msg) { warnings << "#{where}: #{msg}" }

def split_fm(text)
  return [{}, text] unless text.start_with?("---")

  _, fm, body = text.split(/^---[ \t]*$/, 3)
  [YAML.safe_load(fm, permitted_classes: [Date, Time]) || {}, body.to_s]
end

def fold(s)
  s.unicode_normalize(:nfd).gsub(/\p{Mn}/, "").downcase
end

# Units in reading order, from the outline.
order = outline["front"].map { _1["id"] } +
        outline["parts"].flat_map { |p| p["chapters"] ? p["chapters"].map { _1["id"] } : [p["id"]] } +
        outline["back"].reject { _1["kind"] == "generated" }.map { _1["id"] }
file_of = ->(id, lang = LANG) { File.join(ROOT, "book", lang, id == "prefacio" ? "index.md" : "#{id}.md") }
units = order.select { File.exist?(file_of.(_1)) }.to_h do |id|
  fm, body = split_fm(File.read(file_of.(id)))
  [id, { fm: fm, body: body, text: body.gsub(/<!--.*?-->/m, "") }]
end
order.reject { File.exist?(file_of.(_1)) }.each { err.("outline", "unit #{_1} has no file book/#{LANG}/") }

# ---- ids --------------------------------------------------------------------
defined = units.flat_map { |_, u| u[:body].scan(/\{#((?:sec|fig|tbl)-[\w-]+)/).flatten }
defined += GENERATED.map { "sec-#{_1}" } + %w[sec-como-ler-anuncio]
defined += units.flat_map { |_, u| u[:body].scan(/\{#(sec-[\w-]+)/).flatten }
units.each do |id, u|
  u[:text].scan(/(?<![\w.\/])@((?:sec|fig|tbl)-[\w-]*\w)/).flatten.uniq.each do |ref|
    err.("#{id}", "@#{ref} doesn't resolve") unless defined.include?(ref)
  end
end

# ---- citations --------------------------------------------------------------
refs = Array((YAML.load_file(File.join(ROOT, "book", "back", "references.yaml")) || {})["references"]).map { _1["id"] }
cited = units.flat_map { |_, u| u[:text].scan(/(?<![\w.\/])@([\w:.-]*\w)/).flatten }.reject { _1.start_with?("sec-", "fig-", "tbl-") }.uniq
(cited - refs).each { err.("citations", "@#{_1} not in book/back/references.yaml (run scripts/merge_refs.rb)") }
if LANG == "pt"
  (refs - cited).each { warn_.("citations", "#{_1} is in the bibliography but no unit cites it") }
end

# ---- glossary ---------------------------------------------------------------
gfile = File.join(ROOT, "book", "back", "glossary-#{LANG}.yml")
gkeys = File.exist?(gfile) ? YAML.load_file(gfile).keys : []
err.("glossary", "#{gfile.delete_prefix(ROOT + '/')} missing") if gkeys.empty?
used = units.flat_map { |_, u| u[:text].scan(/\[([^\]]+)\]\{\.gls(?:\s+key=([\w-]+))?\}/).map { |t, k| k || t.downcase } }.uniq
(used - gkeys).each { err.("glossary", "key #{_1} used but not defined") }
(gkeys - used).each { warn_.("glossary", "key #{_1} defined but never used") }

# ---- figures ----------------------------------------------------------------
credits = Dir[File.join(ROOT, "assets", "credits", "*.yml")].to_h { r = YAML.load_file(_1, permitted_classes: [Date, Time]); [r["file"], r] }
placeholders = File.exist?(f = File.join(ROOT, "assets", "figures", ".placeholders")) ? File.readlines(f, chomp: true) : []
units.each do |id, u|
  u[:text].scan(%r{\]\((assets/[^)\s]+)\)}).flatten.each do |path|
    err.(id, "image #{path} missing") unless File.exist?(File.join(ROOT, path))
    canonical = path.sub(%r{figures/[a-z]{2}/}, "figures/")
    err.(id, "image #{path} has no assets/credits record") unless credits.key?(path) || credits.key?(canonical)
    if placeholders.include?(File.basename(path))
      (opts[:release] ? err : warn_).(id, "image #{path} is still a placeholder")
    end
  end
end

# ---- provenance and cut-off -------------------------------------------------
cutoff = outline.dig("meta", "source_from") && Date.parse(outline.dig("meta", "source_from").to_s)
excluded = Array(outline["excluded"]).to_h { ["2026/#{_1['post']}", Array(_1["borrowed_by"])] }
units.each do |id, u|
  sources = Array(u[:fm]["sources"]).map { _1["post"] }
  markers = u[:body].scan(%r{<!-- src: (\d{4}/\d\d/\d\d/[^ ]+) -->}).flatten.uniq
  (markers - sources).each { err.(id, "src marker #{_1} not listed in front-matter sources") }
  (sources - markers).each { warn_.(id, "source #{_1} listed but no paragraph is marked with it") }
  (sources | markers).each do |post|
    date = Date.parse(post[0, 10].tr("/", "-")) rescue nil
    err.(id, "#{post} predates the cut-off #{cutoff}") if cutoff && date && date < cutoff
    err.(id, "#{post} is in outline `excluded`") if excluded.key?(post) && !excluded[post].include?(id)
  end
end

# ---- callbacks (heuristic) --------------------------------------------------
# A sentence pointing at other units (@sec-x) usually names what it points
# at: a quoted phrase, a proper name, a number. If none of those occur in
# any of the target units, the callback probably points at removed material.
STOP = %w[Parte Part Capítulo Chapter Apêndice Appendix Interlúdio Interlude II III IV VI].freeze
names_in = lambda do |sentence|
  # A leading bold label ("**Março.** Compro...") ends a "sentence": the next
  # word is capitalised by grammar, not because it's a name. Glossary spans
  # keep their text.
  plain = sentence.sub(/\A\s*\*\*[^*]+\*\*\s*/, "").gsub(/\[([^\]]*)\]\{[^}]*\}/) { Regexp.last_match(1) }
                  .gsub(/[*_`]/, "").gsub(/@sec-[\w-]+|\[@[^\]]*\]/, "")
  words = plain.split(/\s+/)
  quoted = plain.scan(/"([^"]{3,60})"/).flatten
  proper = words.drop(1).each_cons(1).map(&:first).map { _1.gsub(/\A[^\p{L}\d]+|[^\p{L}\d+]+\z/, "") }
                .select { _1.match?(/\A\p{Lu}[\p{L}\d+.-]{2,}\z/) }
  numbers = plain.scan(/\b(\d{2,}(?:[.,]\d+)*)\b/).flatten.reject { _1.match?(/\A20\d\d\z/) }
  (quoted + proper + numbers).uniq.reject { STOP.include?(_1) }
end
units.each do |id, u|
  # Headings, images, tables and divs aren't prose; split the rest into sentences.
  prose = u[:text].split(/\n{2,}/).reject { _1.lstrip.start_with?("#", "!", "|", ":::") }.join("\n\n")
  prose.split(/(?<=[.!?:])\s+|\n{2,}/).each do |sentence|
    targets = sentence.scan(/@sec-([\w-]+)/).flatten.uniq.reject { _1 == id }.select { units.key?(_1) }
    next if targets.empty?

    names = names_in.(sentence)
    next if names.empty?

    hay = targets.map { fold(units[_1][:text]) }.join("\n")
    next if names.any? { hay.include?(fold(_1)) }

    warn_.(id, "callback to #{targets.map { "@sec-#{_1}" }.join('/')} names #{names.first(4).join(', ')}, none found there: \"#{sentence.strip[0, 110]}\"")
  end
end

# ---- translation parity -----------------------------------------------------
unless LANG == "pt"
  units.each do |id, u|
    pt_file = file_of.(id, "pt")
    next unless File.exist?(pt_file)

    tf = u[:fm]["translated_from"]
    if tf.nil?
      err.(id, "no translated_from in front matter")
    elsif Digest::SHA256.file(pt_file).hexdigest != tf["sha256"]
      (opts[:release] ? err : warn_).(id, "PT unit changed since translation (scripts/drift.rb --lang #{LANG} --diff)")
    end
    _, pt_body = split_fm(File.read(pt_file))
    pt_markers = pt_body.scan(/<!-- src: ([^ ]+) -->/).flatten
    markers = u[:body].scan(/<!-- src: ([^ ]+) -->/).flatten
    err.(id, "src markers differ from PT (#{markers.size} vs #{pt_markers.size})") if markers != pt_markers
    { "references" => /(?<![\w.\/])@([\w:.-]*\w)/, "ids" => /\{#((?:sec|fig|tbl)-[\w-]+)/ }.each do |what, re|
      a = pt_body.gsub(/<!--.*?-->/m, "").scan(re).flatten.sort
      b = u[:text].scan(re).flatten.sort
      warn_.(id, "#{what} differ from PT: #{(a - b).first(3)} / #{(b - a).first(3)}") if a != b
    end
  end
end

# ---- seams ------------------------------------------------------------------
paras = ->(text) { text.split(/\n{2,}/).map(&:strip).reject { _1.empty? || _1.start_with?("#", "!", ":::", "{", "|") } }
seams = ["# Seams (#{LANG}): how each unit ends and the next begins", ""]
order.each_cons(2) do |a, b|
  next unless units[a] && units[b]

  seams << "## #{a} → #{b}" << "" << "> …#{paras.(units[a][:text]).last.to_s[-400..] || paras.(units[a][:text]).last}" << "" <<
    "> #{paras.(units[b][:text]).first.to_s[0, 400]}…" << ""
end
FileUtils_mkdir = ->(d) { Dir.mkdir(d) unless Dir.exist?(d) }
FileUtils_mkdir.(File.join(ROOT, "build"))
FileUtils_mkdir.(File.join(ROOT, "build", LANG))
File.write(File.join(ROOT, "build", LANG, "seams.md"), seams.join("\n"))

# ---- output checks ----------------------------------------------------------
if opts[:output]
  log = File.join(ROOT, "build", LANG, "render.log")
  if File.exist?(log)
    text = File.read(log).gsub(/\e\[[0-9;]*m/, "")
    text.scan(/Unable to resolve crossref @?([\w-]+)/).flatten.uniq.each { err.("render", "unresolved cross-reference #{_1}") }
    text.scan(/\[glossary\] unknown key: (\S+)/).flatten.uniq.each { err.("render", "unknown glossary key #{_1}") }
    text.scan(/[Cc]itation (?:not found|missing)[: ]+(\S+)/).flatten.uniq.each { err.("render", "missing citation #{_1}") }
  else
    warn_.("render", "no build/#{LANG}/render.log (rake build writes it)")
  end
  Dir[File.join(ROOT, "build", LANG, "*.pdf")].each do |pdf|
    txt = `pdftotext -q #{pdf} - 2>/dev/null`
    { /\?\?/ => "'??' (unresolved reference)", /\b[\w-]+\?\)/ => "'key?)' (missing citation)",
      /(Se[cç][aã]o|Section|Figura|Figure) \?/ => "unresolved numbered reference" }.each do |re, what|
      hits = txt.scan(re).size
      err.(File.basename(pdf), "#{hits}× #{what}") if hits.positive?
    end
  end
end

puts "doctor (#{LANG}): #{units.size} units, #{errors.size} error(s), #{warnings.size} warning(s)"
errors.each { puts "  ERROR #{_1}" }
warnings.each { puts "  warn  #{_1}" }
puts "  seams: build/#{LANG}/seams.md"
exit(errors.empty? ? 0 : 1)
