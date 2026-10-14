#!/usr/bin/env ruby
# frozen_string_literal: true

# After a blog post changed and the affected book text was reviewed (and
# updated, or found unaffected), record that the book now matches the post's
# current version: re-stamps the post's sha256, plus the blog commit it was
# reviewed at, in every chapter source entry citing it, and updates the post
# analysis' source_sha256.
#
# Usage: scripts/restamp.rb [--lang en] 2026/MM/DD/slug [...]   (run scripts/inventory.rb first)
#        scripts/restamp.rb --translation ch03[,ch04...] | --all-translations
# The second form is for EN units re-synced to their PT unit: it sets
# translated_from.sha256 in book/en/<unit>.md to the PT file's current hash
# (and nothing else). Never edit that hash by hand.
# scripts/restamp.rb --parked <topic>   (pt) records, in
# book/parked/<topic>/sources.yml, the current hash and blog commit of every post
# the parked material cites (drift.rb "== Parked" compares against it).
# Each edition tracks its own language of the post (index.md / index.en.md).
# Only touches the front-matter block; prose is never modified. The
# chapter-level blog_commit stays as the baseline for the chapter's other
# sources, so scripts/drift.rb --diff stays correct for them.

require "yaml"
require "digest"

ROOT = File.expand_path("..", __dir__)
inv = YAML.load_file(File.join(ROOT, "inventory", "posts.yml"))
posts = inv["posts"].to_h { [_1["id"], _1] }
head = inv["blog_commit"]
lang = "pt"
if (i = ARGV.index("--lang"))
  lang = ARGV[i + 1]
  ARGV.slice!(i, 2)
end
translations = nil
if (i = ARGV.index("--translation"))
  translations = ARGV[i + 1].to_s.split(",").map(&:strip).reject(&:empty?)
  ARGV.slice!(i, 2)
end
all_translations = !ARGV.delete("--all-translations").nil?

if translations || all_translations
  abort "--translation needs unit ids" if translations&.empty?
  dir = File.join(ROOT, "book", "en")
  files = if all_translations
            Dir[File.join(dir, "*.md")].sort
          else
            translations.map do |u|
              path = File.join(dir, u == "prefacio" ? "index.md" : "#{u}.md")
              File.exist?(path) ? path : abort("unknown unit #{u}: no #{path.delete_prefix(ROOT + '/')}")
            end
          end
  files.each do |path|
    text = File.read(path)
    fm_end = text.start_with?("---\n") && text.index(/^---[ \t]*$/, 4)
    tf = fm_end && text[0...fm_end].match(/^translated_from: \{file: (\S+?), sha256: "?[0-9a-f]{64}"?\}$/)
    unless tf
      next if all_translations

      abort "#{File.basename(path)} has no translated_from line"
    end
    pt = File.join(ROOT, tf[1])
    abort "#{tf[1]} (translated_from of #{File.basename(path)}) does not exist" unless File.exist?(pt)

    sha = Digest::SHA256.file(pt).hexdigest
    line = %(translated_from: {file: #{tf[1]}, sha256: "#{sha}"})
    File.write(path, text[0...fm_end].sub(tf[0]) { line } + text[fm_end..])
    warn "restamped #{File.basename(path)} translated_from"
  end
  exit
end

if (i = ARGV.index("--parked"))
  topic = ARGV[i + 1] or abort "--parked needs a topic"
  dir = File.join(ROOT, "book", "parked", topic)
  abort "no book/parked/#{topic}" unless File.directory?(dir)
  ids = Dir[File.join(dir, "**", "*.md")].sort.flat_map { File.read(_1).scan(%r{<!-- src: (\d{4}/\d\d/\d\d/[^ ]+) -->}).flatten }.uniq
  entries = ids.map do |id|
    sha = posts.fetch(id) { abort "unknown post #{id}" }.dig("pt", "sha256")
    { "post" => id, "sha256" => sha, "commit" => head }
  end
  File.write(File.join(dir, "sources.yml"), { "posts" => entries }.to_yaml)
  warn "restamped book/parked/#{topic}/sources.yml (#{entries.size} posts)"
  exit
end

abort "usage: restamp.rb [--lang en] POST_ID... | --translation UNIT[,UNIT] | --all-translations | --parked TOPIC" if ARGV.empty?

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
