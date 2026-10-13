#!/usr/bin/env ruby
# frozen_string_literal: true

# Builds inventory/posts.yml: one entry per blog post of the target year,
# with content hashes for both language siblings. The hashes are the
# provenance anchor: book chapters record the hash they were written from,
# and scripts/drift.rb compares them against this file.
#
# Usage: scripts/inventory.rb [--blog PATH] [--year 2026]

require "yaml"
require "digest"
require "date"
require "optparse"

opts = { blog: File.expand_path("~/Projects/akitaonrails-hugo"), year: "2026" }
OptionParser.new do |o|
  o.on("--blog PATH") { |v| opts[:blog] = File.expand_path(v) }
  o.on("--year YEAR") { |v| opts[:year] = v }
end.parse!

ROOT = File.expand_path("..", __dir__)
LINK_RE = /(?<!!)\[([^\]]*)\]\((https?:\/\/[^)\s]+|\/[^)\s]*)\)/
IMG_RE = /!\[([^\]]*)\]\(([^)\s]+)\)/

def split_front_matter(text)
  return [{}, text] unless text.start_with?("---")

  _, fm, body = text.split(/^---[ \t]*$/, 3)
  [YAML.safe_load(fm, permitted_classes: [Date, Time]) || {}, body.to_s]
end

def read_post(path)
  return nil unless File.exist?(path)

  raw = File.read(path)
  fm, body = split_front_matter(raw)
  {
    "sha256" => Digest::SHA256.hexdigest(raw),
    "title" => fm["title"],
    "description" => fm["description"],
    "slug" => fm["slug"],
    "tags" => Array(fm["tags"]),
    "words" => body.split.size,
    "links" => body.scan(LINK_RE).map { |text, url| { "text" => text, "url" => url } },
    "images" => body.scan(IMG_RE).map { |alt, url| { "alt" => alt, "url" => url } },
    "youtube" => body.scan(/youtube\s+id="([^"]+)"/).flatten,
  }
end

posts = Dir.glob(File.join(opts[:blog], "content", opts[:year], "*/*/*/index.md")).sort.map do |pt_path|
  dir = File.dirname(pt_path)
  id = dir.delete_prefix(File.join(opts[:blog], "content") + "/")
  pt = read_post(pt_path)
  en = read_post(File.join(dir, "index.en.md"))
  fm, = split_front_matter(File.read(pt_path))
  {
    "id" => id,
    "date" => fm["date"].to_s,
    "url_pt" => "https://www.akitaonrails.com/#{id}/",
    "url_en" => en && "https://www.akitaonrails.com/en/#{File.dirname(id)}/#{en['slug'] || File.basename(id)}/",
    "pt" => pt,
    "en" => en,
  }
end

out = File.join(ROOT, "inventory", "posts.yml")
commit = `git -C #{opts[:blog]} rev-parse HEAD`.strip
dirty = `git -C #{opts[:blog]} status --porcelain -- content/#{opts[:year]}`.lines.map { _1[3..].strip }
File.write(out, { "generated_from" => opts[:blog], "blog_commit" => commit, "dirty_files" => dirty,
                  "year" => opts[:year], "posts" => posts }.to_yaml)
warn "wrote #{posts.size} posts to #{out.delete_prefix(ROOT + '/')}"
