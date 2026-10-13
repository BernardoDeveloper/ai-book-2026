#!/usr/bin/env ruby
# frozen_string_literal: true

# Seeds the bibliography work: collects every link in the inventoried posts
# (PT side, canonical), dedupes by normalized URL, classifies it, and records
# which posts cite it. Output: inventory/links.yml. Curated entries live in
# book/back/references.yaml; this file is only the raw material.

require "yaml"
require "uri"

ROOT = File.expand_path("..", __dir__)
posts = YAML.load_file(File.join(ROOT, "inventory", "posts.yml"))["posts"]

def normalize(url)
  u = URI.parse(url)
  u.fragment = nil
  if u.query
    q = URI.decode_www_form(u.query).reject { |k, _| k.start_with?("utm_") || %w[pp si feature].include?(k) }
    u.query = q.empty? ? nil : URI.encode_www_form(q)
  end
  u.to_s.sub(%r{/\z}, "")
rescue URI::InvalidURIError
  url
end

def kind(url)
  case url
  when %r{\A/}, %r{akitaonrails\.com} then "internal"
  when /youtube\.com|youtu\.be/ then "video"
  when /arxiv\.org|doi\.org|acm\.org|ieee\.org|nature\.com|science\.org/ then "paper"
  when /github\.com|gitlab\.com|codeberg\.org/ then "repo"
  when %r{x\.com|twitter\.com|reddit\.com|news\.ycombinator|bsky|mastodon} then "social"
  when /wikipedia\.org/ then "encyclopedia"
  else "web"
  end
end

links = Hash.new { |h, k| h[k] = { "url" => k, "kind" => kind(k), "texts" => [], "cited_by" => [] } }
posts.each do |p|
  p["pt"]["links"].each do |l|
    e = links[normalize(l["url"])]
    e["texts"] |= [l["text"]]
    e["cited_by"] |= [p["id"]]
  end
end

entries = links.values.sort_by { |e| [-e["cited_by"].size, e["url"]] }
File.write(File.join(ROOT, "inventory", "links.yml"), entries.to_yaml)
warn entries.group_by { _1["kind"] }.transform_values(&:size).inspect
warn "#{entries.size} unique links"
