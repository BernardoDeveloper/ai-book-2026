#!/usr/bin/env ruby
# frozen_string_literal: true

# Page-level layout audit of the built PDF. Reports, as file:page lines:
#   HEADING-AT-FOOT  a heading with no body text after it on its page
#   GAP              a page under ~25% text and no image (not a blank, part
#                    page, chapter opening or chapter-final page)
#   RUNT-END         a chapter whose last page has <= 3 lines of text
#   FIG-OUTSIDE      a figure/table caption ("Figura 5.2") on a page outside
#                    its chapter's page range (a float that drifted)
#   SPLIT            a block that must stay whole (figure, table, quote,
#                    code, short list) starting and ending on different pages
#   OVERFULL         a line extending past the text block's left/right edge
#   OVERSIZED        an image taller than ~62% of the text block or wider
#                    than the text block
#
# Structure comes from invisible records the akita-book template writes
# (`ak-audit` metadata: headings, block starts/ends, with page and y),
# read with `typst query`; text and images come from poppler (pdftotext
# -bbox-layout, pdfimages -list). Pages are physical PDF pages; the folio
# printed on the page is shown as "fl. N".
#
# Usage: scripts/page_audit.rb [--lang pt] [--edition print|ebook] [--strict] [--verbose] [--runts]
#   --runts   print only the comma-separated ids of RUNT-END chapters (used by `rake fit`)
#   --strict  exit 1 when anything is reported (default: report only)

require "json"
require "open3"

ROOT = File.expand_path("..", __dir__)
# Quarto's bundled typst, called directly (`quarto typst query` sends the
# result to stderr when stdout is not a terminal).
TYPST = Dir[File.join(ROOT, "tools", "quarto-1.10.19", "bin", "tools", "*", "typst")].first
args = ARGV.dup
lang = (i = args.index("--lang")) ? args[i + 1] : "pt"
edition = (i = args.index("--edition")) ? args[i + 1] : "print"
strict = args.include?("--strict")
verbose = args.include?("--verbose") # also list blocks too tall to keep whole
runts_only = args.include?("--runts") # print only the ids of chapters ending in a runt page

pdf = Dir[File.join(ROOT, "build", lang, "*.pdf")].find { edition == "ebook" ? _1.end_with?("-ebook.pdf") : !_1.end_with?("-ebook.pdf") }
typ = File.join(ROOT, "index.typ")
abort "no #{edition} PDF in build/#{lang}; run `rake build`" unless pdf
abort "no #{typ} (keep-typ); run `rake build`" unless File.exist?(typ)

# Geometry, in pt, must match _extensions/akita-book/typst-template.typ.
PAGE_W = 432.0
PAGE_H = 648.0
TOP = 0.8 * 72
BOTTOM = PAGE_H - 0.85 * 72
INSIDE = edition == "ebook" ? 54.0 : 63.0
OUTSIDE = edition == "ebook" ? 54.0 : 45.0
BODY_H = BOTTOM - TOP
TOL = 0.6
HANG = %w[. , ; : - – — ) ( " “ ” ’ ‘ « » ! ?].push("\u00AD").freeze
HANG_TOL = 4.0

def run(*cmd)
  out, err, st = Open3.capture3(*cmd)
  abort "#{cmd.first(3).join(' ')} failed:\n#{err}" unless st.success?
  out
end

# --- structure records from the Typst source
# Same per-chapter tightening the PDFs were compiled with (see `rake fit`).
tighten_file = File.join(ROOT, "build", lang, ".tighten")
tighten = File.exist?(tighten_file) ? File.read(tighten_file).strip : ""
meta = JSON.parse(run(TYPST, "query", "--root", ROOT, "--font-path", File.join(ROOT, "assets", "fonts"),
                      "--input", "edition=#{edition}", "--input", "tighten=#{tighten}",
                      typ, "metadata", "--field", "value"))
meta.select! { _1.is_a?(Hash) && _1["ak"] }
h1s = meta.select { _1["ak"] == "h1" }

# --- text lines and images per page
Line = Struct.new(:x0, :y0, :x1, :y1, :text)
pages = []
cur = nil
run("pdftotext", "-bbox-layout", pdf, "-").each_line do |l|
  if l.include?("<page ")
    cur = []
    pages << cur
  elsif (m = l.match(/<line xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)"/))
    cur << Line.new(*m.captures.map(&:to_f), +"")
  elsif (m = l.match(/<word [^>]*>(.*)<\/word>/)) && cur&.last
    cur.last.text << " " unless cur.last.text.empty?
    cur.last.text << m[1].gsub("&amp;", "&").gsub("&lt;", "<").gsub("&gt;", ">").gsub("&quot;", '"')
  end
end
images = Hash.new { |h, k| h[k] = [] }
run("pdfimages", "-list", pdf).lines.drop(2).each do |l|
  f = l.split
  images[f[0].to_i] << { w: f[3].to_i, h: f[4].to_i, xppi: f[12].to_f, yppi: f[13].to_f }
end
npages = pages.size

body = ->(p) { (pages[p - 1] || []).select { _1.y0 >= TOP - 4 && _1.y1 <= BOTTOM + 4 } }
text_lines = ->(p) { body.(p).reject { _1.text.strip.empty? } }

# --- book structure
main_start = h1s.find { _1["title"] != "Sumário" && _1["title"] != "Contents" && !_1["part"] }&.fetch("page") || 1
folio = ->(p) { p >= main_start ? p - main_start + 1 : nil }
units = h1s.reject { _1["page"] < main_start }.each_with_index.map do |h, i|
  nxt = h1s.find { _1["page"] > h["page"] }
  last = (nxt ? nxt["page"] - 1 : npages)
  last -= 1 while last > h["page"] && text_lines.(last).empty? && images[last].empty?
  h.merge("first" => h["page"], "last" => last, "idx" => i)
end
chapters = units.reject { _1["part"] }
id_for = ->(label) { label.to_s.sub(/\Asec-/, "") }
file_for = lambda do |u|
  id = id_for.(u && u["label"])
  return "?" if id.empty?
  id == "prefacio" ? "book/#{lang}/index.md" : "book/#{lang}/#{id}.md"
end
unit_at = ->(p) { chapters.select { _1["first"] <= p }.max_by { _1["first"] } }
where = ->(p) { "#{file_for.(unit_at.(p))}:#{p}#{folio.(p) ? " (fl. #{folio.(p)})" : ''}" }

findings = []
add = ->(kind, p, msg) { findings << [p, kind, "#{where.(p)}  #{kind}  #{msg}"] }

# HEADING-AT-FOOT
meta.select { _1["ak"] == "h" }.each do |h|
  p = h["page"]
  next unless p.between?(1, npages)

  after = text_lines.(p).select { _1.y0 > h["y"] + 8 }
  add.("HEADING-AT-FOOT", p, "\"#{h['title']}\" (h#{h['level']}) has no text after it on the page") if after.empty?
end

# SPLIT (blocks recorded with start/end markers)
starts = meta.select { _1["ak"] == "blk" && _1["edge"] == "start" }.to_h { [_1["id"], _1] }
meta.select { _1["ak"] == "blk" && _1["edge"] == "end" }.each do |e|
  s = starts[e["id"]] or next
  next if s["page"] == e["page"]
  next if s["allowed"] && !verbose # too tall to keep whole: breaking is right

  add.("SPLIT", s["page"], "#{s['kind']} split across pages #{s['page']}-#{e['page']}#{s['allowed'] ? ' (taller than allowed to keep whole)' : ''}")
end

# FIG-OUTSIDE: caption lines are set smaller than body text (line box < 12pt)
cap_re = /\A(Figura|Tabela|Figure|Table) ([A-Z]|\d+)\.(\d+)\b/
chapter_by_num = chapters.select { _1["numbered"] }.to_h { [_1["num"].to_s.sub(/\.\z/, ""), _1] }
(1..npages).each do |p|
  body.(p).each do |l|
    m = l.text.match(cap_re) or next
    next unless (l.y1 - l.y0) < 12.5

    ch = chapter_by_num[m[2]] or next
    next if p.between?(ch["first"], ch["last"])

    add.("FIG-OUTSIDE", p, "#{m[1]} #{m[2]}.#{m[3]} belongs to #{file_for.(ch)} (pages #{ch['first']}-#{ch['last']})")
  end
end

# RUNT-END
runt_ids = []
chapters.each do |c|
  next if c["last"] <= c["first"]

  n = text_lines.(c["last"]).size
  next if n > 3 || !images[c["last"]].empty?

  runt_ids << id_for.(c["label"])
  add.("RUNT-END", c["last"], "last page of \"#{c['title']}\" has #{n} line#{n == 1 ? '' : 's'}")
end

# GAP
openings = units.map { _1["first"] }
finals = chapters.map { _1["last"] }
(main_start..npages).each do |p|
  next if openings.include?(p) || finals.include?(p) || !images[p].empty?

  ls = text_lines.(p)
  next if ls.empty? # intentional blank (verso before a recto opening)

  cover = ls.sum { _1.y1 - _1.y0 } / BODY_H
  add.("GAP", p, format("page only %d%% text (%d lines), no figure", (cover * 100).round, ls.size)) if cover < 0.25
end

# OVERFULL
cover_pages = edition == "ebook" ? 1 : 0
(1..npages).each do |p|
  next if p <= cover_pages

  recto = edition == "ebook" || (p - cover_pages).odd?
  left = recto ? INSIDE : OUTSIDE
  right = PAGE_W - (recto ? OUTSIDE : INSIDE)
  (pages[p - 1] || []).each do |l|
    # Typst hangs punctuation and hyphens into the margin (optical margin
    # alignment); that overhang is intended, so allow it at line ends.
    t = l.text.strip
    rtol = HANG.include?(t[-1]) ? HANG_TOL : TOL
    ltol = HANG.include?(t[0]) ? HANG_TOL : TOL
    next unless l.x0 < left - ltol || l.x1 > right + rtol

    over = [left - l.x0, l.x1 - right].max
    add.("OVERFULL", p, format("line %.1fpt past the margin: \"%s\"", over, l.text[0, 70]))
  end
end

# OVERSIZED: rendered image size from pixel size / effective ppi
images.each do |p, list|
  list.each do |im|
    next if p <= cover_pages || im[:xppi].zero?

    w = im[:w] / im[:xppi] * 72
    h = im[:h] / im[:yppi] * 72
    text_w = PAGE_W - INSIDE - OUTSIDE
    add.("OVERSIZED", p, format("image %.0fx%.0fpt (text block %.0fx%.0fpt)", w, h, text_w, BODY_H)) if h > BODY_H * 0.62 || w > text_w + 1
  end
end

if runts_only
  puts runt_ids.join(",")
  exit 0
end

findings.sort_by! { [_1[0], _1[1]] }
puts "page audit: #{File.basename(pdf)} (#{edition}, #{npages} pages, #{chapters.size} units)"
counts = findings.group_by { _1[1] }.transform_values(&:size)
findings.each { puts "  #{_1[2]}" }
puts(findings.empty? ? "  clean" : "  totals: #{counts.map { |k, v| "#{k} #{v}" }.join(', ')}")
exit(strict && !findings.empty? ? 1 : 0)
