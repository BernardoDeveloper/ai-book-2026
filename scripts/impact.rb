#!/usr/bin/env ruby
# frozen_string_literal: true

# Change-impact map: before changing something, list everything in the book
# that depends on it, so the edit can be planned and split between agents
# without overlapping files. Written after the February cut-off change, where
# this map was assembled by hand with grep.
#
#   scripts/impact.rb post 2026/01/28/slug      paragraphs marked with that post, units
#                                               listing it, figures/credits/refs citing it
#   scripts/impact.rb posts-before 2026-02-01   the same for every post before a date
#   scripts/impact.rb unit ch05                 units that cross-reference ch05, and the
#                                               sentences that do (callbacks to re-check),
#                                               the hooks in and out, its figures
#   scripts/impact.rb term "TV Clipboard"       every unit/line mentioning a term
#
# Options: --lang pt|en (default pt).

require "yaml"
require "date"

ROOT = File.expand_path("..", __dir__)
lang = ARGV.include?("--lang") ? ARGV[ARGV.index("--lang") + 1] : "pt"
args = ARGV.reject.with_index { |a, i| a == "--lang" || ARGV[i - 1] == "--lang" }
mode, target = args
abort File.read(__FILE__)[/^#   scripts.*?(?=\n#\n# Options)/m] unless mode && target

files = Dir[File.join(ROOT, "book", lang, "*.md")].sort
         .reject { %w[glossario bibliografia fontes creditos].include?(File.basename(_1, ".md")) }
uid = ->(f) { (b = File.basename(f, ".md")) == "index" ? "prefacio" : b }
read = ->(f) { File.read(f) }

# Paragraph blocks grouped under each src marker: marker => [[unit, first line, text]].
def blocks(path)
  out = []
  current = nil
  File.readlines(path).each_with_index do |line, i|
    if (m = line.match(/<!-- src: (\S+) -->/))
      current = { src: m[1], line: i + 1, text: +"" }
      out << current
    elsif current
      current[:text] << line
    end
  end
  out
end

report_posts = lambda do |posts|
  posts.each do |post|
    puts "== #{post}"
    files.each do |f|
      text = read.(f)
      listed = text[/\A---.*?^---/m].to_s.include?("post: #{post}")
      bl = blocks(f).select { _1[:src] == post }
      next unless listed || bl.any?

      words = bl.sum { _1[:text].split.size }
      puts "  #{uid.(f)}: #{bl.size} marked block(s), ~#{words} words#{listed ? '' : ' (NOT in front-matter sources)'}" \
           "#{bl.any? ? ", lines #{bl.map { _1[:line] }.join(', ')}" : ''}"
    end
    Dir[File.join(ROOT, "assets", "credits", "*.yml")].each do |c|
      puts "  figure #{File.basename(c, '.yml')} mentions it" if File.read(c).include?(post)
    end
    Dir[File.join(ROOT, "assets", "charts", "*")].each do |c|
      puts "  chart script #{File.basename(c)} cites it" if File.read(c).include?(post[5..])
    end
    refs = File.read(File.join(ROOT, "book", "back", "references.yaml")).scan(/^- id: (\S+)\n(?:  .*\n)*?  note: .*#{Regexp.escape(post)}/).flatten
    puts "  references noted as cited-by it: #{refs.join(', ')}" unless refs.empty?
    lin = File.read(File.join(ROOT, "inventory", "lineage.yml"))
    puts "  appears in inventory/lineage.yml (check supersession)" if lin.include?(post[5..])
  end
end

case mode
when "post"
  report_posts.([target])
when "posts-before"
  limit = Date.parse(target)
  posts = files.flat_map { read.(_1).scan(/(?:post: |src: )(\d{4}\/\d\d\/\d\d\/[^\s,"}]+)/).flatten }.uniq
               .select { Date.parse(_1[0, 10].tr("/", "-")) < limit }.sort
  puts "#{posts.size} post(s) before #{limit} are used"
  report_posts.(posts)
when "unit"
  ref = "@sec-#{target}"
  file = File.join(ROOT, "book", lang, target == "prefacio" ? "index.md" : "#{target}.md")
  puts "== callbacks into #{target} (re-check these when #{target} changes)"
  files.each do |f|
    next if f == file

    read.(f).gsub(/<!--.*?-->/m, "").split(/(?<=[.!?])\s+/).each do |s|
      puts "  #{uid.(f)}: #{s.strip[0, 160]}" if s.include?(ref)
    end
  end
  outline = YAML.load_file(File.join(ROOT, "book", "outline.yml"))
  order = outline["front"].map { _1["id"] } + outline["parts"].flat_map { |p| p["chapters"] ? p["chapters"].map { _1["id"] } : [p["id"]] } +
          outline["back"].reject { _1["kind"] == "generated" }.map { _1["id"] }
  i = order.index(target)
  puts "== hand-offs: #{i.zero? ? '(start)' : order[i - 1]} → #{target} → #{order[i + 1] || '(end)'} (closing/opening paragraphs must still match)" if i
  if File.exist?(file)
    figs = read.(file).scan(%r{assets/figures/[^)\s]+}).uniq
    puts "== figures: #{figs.join(', ')}" unless figs.empty?
    en = File.join(ROOT, "book", "en", File.basename(file))
    puts "== translation: #{en.delete_prefix(ROOT + '/')} will go stale" if lang == "pt" && File.exist?(en)
  end
when "term"
  re = Regexp.new(Regexp.escape(target), Regexp::IGNORECASE)
  files.each do |f|
    read.(f).each_line.with_index(1) do |line, n|
      puts "  #{uid.(f)}:#{n}: #{line.strip[0, 160]}" if line.match?(re) && !line.start_with?("<!--")
    end
  end
else
  abort "unknown mode #{mode}"
end
