#!/usr/bin/env ruby
# frozen_string_literal: true

# Renames a chapter's front-matter `title:` key to `chapter:`. Quarto prints a
# `title:` as an extra heading on top of the H1, duplicating chapter titles in
# the PDF and TOC. Idempotent; touches only the front-matter block.
#
# Usage: scripts/fix_front_matter.rb FILE...

ARGV.each do |path|
  text = File.read(path)
  next unless text.start_with?("---\n")

  fm_end = text.index(/^---[ \t]*$/, 4) or next
  fm = text[0...fm_end]
  next unless fm.match?(/^title: /)

  File.write(path, fm.sub(/^title: /, "chapter: ") + text[fm_end..])
  warn "renamed title -> chapter in #{path}"
end
