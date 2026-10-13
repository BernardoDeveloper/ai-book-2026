#!/usr/bin/env ruby
# frozen_string_literal: true

# Answers "what in the book is out of date with the blog?".
#
# Compares the current blog against what the book recorded:
#   1. chapters: front matter `sources: [{post, sha256}]` + `blog_commit`
#   2. analyses: inventory/analysis/*.yml `source_sha256`
#   3. coverage: 2026 posts with no analysis, and analyzed AI posts no chapter uses
#
# For each stale chapter source it prints the blog diff since the recorded
# commit, so the update can touch only the paragraphs marked
# `<!-- src: <post> -->` that the change affects.
#
# Usage: scripts/drift.rb [--diff] [--lang pt]
#   Run scripts/inventory.rb first so hashes are fresh (the Rakefile does).

require "yaml"
require "digest"
require "date"
require "optparse"

opts = { diff: false, lang: "pt" }
OptionParser.new do |o|
  o.on("--diff", "print the blog diff for every stale source") { opts[:diff] = true }
  o.on("--lang LANG") { |v| opts[:lang] = v }
end.parse!

ROOT = File.expand_path("..", __dir__)
inv = YAML.load_file(File.join(ROOT, "inventory", "posts.yml"))
blog = inv["generated_from"]
by_id = inv["posts"].to_h { [_1["id"], _1] }
lang_key = opts[:lang] == "en" ? "en" : "pt"
file_name = lang_key == "en" ? "index.en.md" : "index.md"

def front_matter(path)
  text = File.read(path)
  return {} unless text.start_with?("---")

  YAML.safe_load(text.split(/^---[ \t]*$/, 3)[1], permitted_classes: [Date, Time]) || {}
end

problems = 0
used = Hash.new { |h, k| h[k] = [] }

puts "== Chapters (#{opts[:lang]})"
Dir.glob(File.join(ROOT, "book", opts[:lang], "**", "*.md")).sort.each do |path|
  fm = front_matter(path)
  rel = path.delete_prefix(ROOT + "/")
  Array(fm["sources"]).each do |src|
    used[src["post"]] << rel
    post = by_id[src["post"]]
    if post.nil?
      puts "  MISSING  #{rel}: #{src['post']} no longer exists in the blog"
      problems += 1
    elsif post.dig(lang_key, "sha256") != src["sha256"]
      puts "  STALE    #{rel}: #{src['post']}"
      problems += 1
      next unless opts[:diff]

      from = src["commit"] || fm["blog_commit"] || inv["blog_commit"]
      puts `git -C #{blog} diff --stat --patch #{from} -- content/#{src['post']}/#{file_name}`.gsub(/^/, "      ")
    end
  end
end

unless opts[:lang] == "pt"
  # Translations follow the canonical PT chapter: front matter
  # `translated_from: {file: book/pt/<id>.md, sha256: ...}`.
  puts "== Translations (#{opts[:lang]} vs pt)"
  Dir.glob(File.join(ROOT, "book", opts[:lang], "*.md")).sort.each do |path|
    tf = front_matter(path)["translated_from"] or next
    pt = File.join(ROOT, tf["file"])
    next if File.exist?(pt) && Digest::SHA256.file(pt).hexdigest == tf["sha256"]

    puts "  STALE    #{path.delete_prefix(ROOT + '/')}: #{tf['file']} changed since translation"
    problems += 1
    next unless opts[:diff]

    # Find the commit whose version of the PT file has the recorded hash, then
    # show exactly what changed since: that's what the translation must follow.
    base = `git -C #{ROOT} log --format=%H -- #{tf['file']}`.split.find do |rev|
      Digest::SHA256.hexdigest(`git -C #{ROOT} show #{rev}:#{tf['file']} 2>/dev/null`) == tf["sha256"]
    end
    if base
      puts "      PT changes since the translated version (#{base[0, 8]}):"
      puts `git -C #{ROOT} diff --word-diff=plain #{base} -- #{tf['file']}`.gsub(/^/, "      ")
    else
      puts "      translated version not found in git history; compare against the whole PT unit"
    end
  end
end

puts "== Analyses"
Dir.glob(File.join(ROOT, "inventory", "analysis", "*.yml")).sort.each do |path|
  a = YAML.load_file(path)
  post = by_id[a["id"]]
  next if post && post.dig("pt", "sha256") == a["source_sha256"]

  puts "  STALE    #{File.basename(path)} (re-run analysis for #{a['id']})"
  problems += 1
end

analyzed = Dir.glob(File.join(ROOT, "inventory", "analysis", "*.yml")).to_h { |p| a = YAML.load_file(p); [a["id"], a] }
puts "== Coverage"
(by_id.keys - analyzed.keys).each do |id|
  puts "  NEW      #{id} has no analysis yet"
  problems += 1
end
unless used.empty?
  # Posts deliberately left out (with a reason) in book/outline.yml aren't news.
  excluded = Array(YAML.load_file(File.join(ROOT, "book", "outline.yml"))["excluded"]).map { "2026/#{_1['post']}" }
  analyzed.each do |id, a|
    next unless %w[core substantial].include?(a["ai_relevance"]) && !used.key?(id) && !excluded.include?(id)

    puts "  UNUSED   #{id} (#{a['ai_relevance']}) is not a source of any chapter; check book/outline.yml exclusions"
  end
end

puts problems.zero? ? "OK: book is in sync with blog commit #{inv['blog_commit'][0, 12]}" : "#{problems} item(s) need attention"
exit(problems.zero? ? 0 : 1)
