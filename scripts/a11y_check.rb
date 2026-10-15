#!/usr/bin/env ruby
# frozen_string_literal: true

# Lightweight assertions around the generated HTML and EPUB. DAISY Ace and
# EPUBCheck remain the standards-aware validators; these checks protect the
# book-specific contract and make regressions easier to diagnose.

require "open3"

ROOT = File.expand_path("..", __dir__)
lang = "pt"
ARGV.each_with_index { |arg, i| lang = ARGV[i + 1] if arg == "--lang" }
build = File.join(ROOT, "build", lang)
errors = []

html_files = Dir[File.join(build, "**", "*.html")]
errors << "no generated HTML found under build/#{lang}" if html_files.empty?
html_files.each do |path|
  text = File.read(path)
  rel = path.delete_prefix(ROOT + "/")
  errors << "#{rel}: html element lacks language" unless text.match?(/<html\b[^>]*\blang="[^"]+"/i)
  text.scan(/<img\b[^>]*>/i).each do |tag|
    next if tag.match?(/\b(?:role="presentation"|aria-hidden="true")/i)
    errors << "#{rel}: image lacks nonempty alt: #{tag[0, 120]}" unless tag.match?(/\balt="[^"]+"/i)
  end
  text.scan(/<table\b.*?<\/table>/mi).each do |table|
    errors << "#{rel}: data table lacks caption" unless table.match?(/<caption\b/i)
  end
end

source_figures = Dir[File.join(ROOT, "book", lang, "*.md")].sum do |path|
  File.foreach(path).count { _1.start_with?("![") }
end
generated_descriptions = html_files.sum { |path| File.read(path).scan(/class="[^"]*\bfigure-description\b/).size }
unless generated_descriptions == source_figures
  errors << "HTML has #{generated_descriptions} detailed figure descriptions; expected #{source_figures}"
end

epubs = Dir[File.join(build, "*.epub")]
errors << "no EPUB found under build/#{lang}" if epubs.empty?
epubs.each do |epub|
  list, status = Open3.capture2("unzip", "-Z1", epub)
  unless status.success?
    errors << "cannot list #{epub}"
    next
  end
  nav_name = list.lines.map(&:strip).find { _1.end_with?("/nav.xhtml") }
  opf_name = list.lines.map(&:strip).find { _1.end_with?(".opf") }
  nav, = Open3.capture2("unzip", "-p", epub, nav_name.to_s)
  opf, = Open3.capture2("unzip", "-p", epub, opf_name.to_s)
  list.lines.map(&:strip).grep(/\.xhtml\z/).each do |name|
    page, = Open3.capture2("unzip", "-p", epub, name)
    errors << "#{File.basename(epub)}: Kindle-unsafe inline style remains in #{name}" if page.match?(/<style\b/i)
    errors << "#{File.basename(epub)}: Kindle-unsafe data URI remains in #{name}" if page.match?(/data:image/i)
    errors << "#{File.basename(epub)}: Kindle-unsafe callout/layout class remains in #{name}" if page.match?(/class="[^"]*\b(callout|quarto-layout|panel-)/i)
  end
  %w[bodymatter glossary bibliography credits].each do |type|
    errors << "#{File.basename(epub)}: landmark #{type} missing" unless nav.include?(%(epub:type="#{type}"))
  end
  errors << "#{File.basename(epub)}: accessibilitySummary missing" unless opf.include?("schema:accessibilitySummary")
end

if errors.empty?
  puts "accessibility: HTML and EPUB contract OK (#{lang}, #{source_figures} figures)"
else
  errors.each { warn "accessibility: #{_1}" }
  exit 1
end
