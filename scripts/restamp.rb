#!/usr/bin/env ruby
# frozen_string_literal: true

# After a blog post changed and the affected book text was reviewed (and
# updated, or found unaffected), record that the book now matches the post's
# current version: re-stamps the post's sha256, plus the blog commit it was
# reviewed at, in every chapter source entry citing it, and updates the post
# analysis' source_sha256.
#
# Usage: scripts/restamp.rb [--lang en] 2026/MM/DD/slug [...]   (run scripts/inventory.rb first)
# Each edition tracks its own language of the post (index.md / index.en.md).
# Only touches the front-matter block; prose is never modified. The
# chapter-level blog_commit stays as the baseline for the chapter's other
# sources, so scripts/drift.rb --diff stays correct for them.

require "yaml"

ROOT = File.expand_path("..", __dir__)
inv = YAML.load_file(File.join(ROOT, "inventory", "posts.yml"))
posts = inv["posts"].to_h { [_1["id"], _1] }
head = inv["blog_commit"]
lang = "pt"
if (i = ARGV.index("--lang"))
  lang = ARGV[i + 1]
  ARGV.slice!(i, 2)
end
abort "usage: restamp.rb [--lang en] POST_ID..." if ARGV.empty?

ARGV.each do |id|
  sha = posts.fetch(id) { abort "unknown post #{id}" }.dig(lang, "sha256")
  entry = /\{post: #{Regexp.escape(id)}, sha256: "[0-9a-f]{64}"(, commit: "[0-9a-f]+")?\}/
  Dir[File.join(ROOT, "book", lang, "*.md")].sort.each do |path|
    text = File.read(path)
    next unless text.start_with?("---\n")

    fm_end = text.index(/^---[ \t]*$/, 4) or next
    fm = text[0...fm_end]
    next unless fm.match?(entry)

    fm = fm.sub(entry, %({post: #{id}, sha256: "#{sha}", commit: "#{head}"}))
    File.write(path, fm + text[fm_end..])
    warn "restamped #{File.basename(path)} for #{id}"
  end
  analysis = File.join(ROOT, "inventory", "analysis", "#{id.gsub('/', '__')}.yml")
  next unless lang == "pt" && File.exist?(analysis) # analyses are of the canonical PT post

  File.write(analysis, File.read(analysis).sub(/^source_sha256: .*$/, %(source_sha256: "#{sha}")))
  warn "restamped analysis #{File.basename(analysis)}"
end
