#!/usr/bin/env ruby
# frozen_string_literal: true

# Adds useful EPUB landmarks that Pandoc does not generate for this book.
# The TOC remains the source of truth for file names, so numbered XHTML names
# may change without making these links stale.
#
# Usage: scripts/epub_accessibility.rb BOOK.epub   (rewrites it in place)

require "cgi"
require "fileutils"
require "tmpdir"

epub = File.expand_path(ARGV.fetch(0) { abort "usage: epub_accessibility.rb BOOK.epub" })

Dir.mktmpdir("epub-accessibility") do |dir|
  system("unzip", "-q", epub, "-d", dir, exception: true)
  nav_path = Dir[File.join(dir, "**", "nav.xhtml")].first or abort "nav.xhtml not found in #{epub}"
  nav = File.read(nav_path)
  lang = nav[/\b(?:xml:)?lang="([^"]+)"/, 1].to_s.start_with?("en") ? "en" : "pt"
  labels = {
    "pt" => { "bodymatter" => "Início do texto", "glossary" => "Glossário", "bibliography" => "Referências", "credits" => "Créditos das imagens" },
    "en" => { "bodymatter" => "Start of text", "glossary" => "Glossary", "bibliography" => "References", "credits" => "Image credits" },
  }.fetch(lang)
  sections = {
    "bodymatter" => "sec-ch01",
    "glossary" => "sec-glossario",
    "bibliography" => "sec-bibliografia",
    "credits" => "sec-creditos",
  }

  landmarks = sections.filter_map do |type, section|
    next if nav.match?(%r{epub:type="#{Regexp.escape(type)}"})
    href = nav[%r{<a\s+href="([^"]*##{Regexp.escape(section)})"}, 1]
    abort "TOC target ##{section} not found in #{File.basename(epub)}" unless href

    %(    <li><a href="#{CGI.escapeHTML(href)}" epub:type="#{type}">#{CGI.escapeHTML(labels.fetch(type))}</a></li>)
  end

  unless landmarks.empty?
    pattern = %r{(<nav\s+epub:type="landmarks".*?<ol>)(.*?)(</ol>.*?</nav>)}m
    abort "landmarks navigation not found in #{File.basename(epub)}" unless nav.match?(pattern)
    nav.sub!(pattern) { "#{$1}#{$2.rstrip}\n#{landmarks.join("\n")}\n  #{$3}" }
    File.write(nav_path, nav)
  end

  # EPUB requires mimetype to be the first, uncompressed entry.
  FileUtils.rm_f(epub)
  Dir.chdir(dir) do
    system("zip", "-X0q", epub, "mimetype", exception: true)
    system("zip", "-Xr9Dq", epub, ".", "-x", "mimetype", exception: true)
  end
  warn "epub_accessibility: added #{landmarks.size} landmarks to #{File.basename(epub)}"
end
