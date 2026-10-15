#!/usr/bin/env ruby
# frozen_string_literal: true

# Strips the inline <style> blocks Quarto injects into every EPUB chapter:
# callout CSS with base64 PNG icons as data: URIs and flexbox layout-panel
# rules. The book uses neither callouts nor layout panels, and Kindle's
# converter (KDP) rejected the EPUB with "We couldn't convert your HTML file";
# data: URIs and flex layouts are what Kindle handles worst. The book's own
# stylesheet (styles/stylesheet1.css) is linked, not inline, and stays.
#
# Usage: scripts/epub_clean.rb BOOK.epub   (rewrites it in place)

require "tmpdir"
require "fileutils"

epub = File.expand_path(ARGV.fetch(0) { abort "usage: epub_clean.rb BOOK.epub" })
UNUSED = /class="[^"]*\b(callout|quarto-layout|panel-)/

Dir.mktmpdir("epub-clean") do |dir|
  system("unzip", "-q", epub, "-d", dir, exception: true)
  pages = Dir[File.join(dir, "**", "*.xhtml")]
  if (used = pages.find { File.read(_1).match?(UNUSED) })
    abort "#{File.basename(used)} uses callout/layout classes; their inline CSS can't be stripped"
  end

  stripped = 0
  pages.each do |page|
    html = File.read(page)
    clean = html.gsub(%r{[ \t]*<style(?:\s[^>]*)?>.*?</style>\n?}m) { stripped += 1; "" }
    File.write(page, clean) unless clean == html
  end

  # mimetype first and uncompressed, as the EPUB container requires.
  FileUtils.rm_f(epub)
  Dir.chdir(dir) do
    system("zip", "-X0q", epub, "mimetype", exception: true)
    system("zip", "-Xr9Dq", epub, ".", "-x", "mimetype", exception: true)
  end
  warn "epub_clean: removed #{stripped} inline <style> blocks from #{File.basename(epub)}"
end
