#!/usr/bin/env ruby
# frozen_string_literal: true

# Validates book/outline.yml against the inventory and analyses:
# every referenced post exists, every core/substantial post is placed or
# excluded with a reason, and no post is both. Prints usage counts.

require "yaml"

ROOT = File.expand_path("..", __dir__)
outline = YAML.load_file(File.join(ROOT, "book", "outline.yml"))
inventory = YAML.load_file(File.join(ROOT, "inventory", "posts.yml"))["posts"]
ids = inventory.reject { _1["background"] }.map { _1["id"] }
background = Array(outline["background_sources"]).map { _1["post"] }
analyses = Dir[File.join(ROOT, "inventory", "analysis", "*.yml")].map { YAML.load_file(_1) }
full = ->(id) { id.start_with?("2026/") ? id : "2026/#{id}" }

used = Hash.new { |h, k| h[k] = [] }
walk = lambda do |node, where|
  case node
  when Hash
    here = node["id"] || where
    Array(node["sources"]).each { |s| used[full.(s)] << here } if node["sources"].is_a?(Array)
    if node["sources"].is_a?(Hash)
      %w[primary supporting].each { |k| Array(node["sources"][k]).each { |s| used[full.(s)] << "#{here}(#{k[0]})" } }
    end
    node.each { |k, v| walk.(v, here) unless k == "sources" || k == "excluded" || k == "background_sources" }
  when Array then node.each { walk.(_1, where) }
  end
end
walk.(outline.reject { |k, _| %w[excluded background_sources].include?(k) }, nil)
excluded = outline["excluded"].to_h { [full.(_1["post"]), _1["reason"]] }

errors = 0
(used.keys + excluded.keys).uniq.each do |id|
  next if ids.include?(id)
  puts "UNKNOWN #{id}"; errors += 1
end
background.each do |id|
  unless id.match?(%r{\A\d{4}/\d\d/\d\d/}) && inventory.any? { _1["id"] == id && _1["background"] }
    puts "UNKNOWN background source #{id} (full yyyy/mm/dd/slug, present in the blog)"; errors += 1
  end
  next unless id.start_with?("2026/")

  puts "BACKGROUND #{id} is a 2026 post; use sources/excluded"; errors += 1
end
analyses.each do |a|
  next unless %w[core substantial].include?(a["ai_relevance"])
  next if used.key?(a["id"]) || excluded.key?(a["id"])
  puts "UNPLACED #{a['id']} (#{a['ai_relevance']})"; errors += 1
end
(used.keys & excluded.keys).each { puts "BOTH used+excluded #{_1}: #{used[_1].join(',')}" }
multi = used.select { |_, v| v.size > 2 }
puts "posts used in 3+ places: #{multi.map { |k, v| "#{k.split('/').last[0, 30]}=#{v.join(',')}" }.join('; ')}" unless multi.empty?
puts "#{used.size} posts used, #{excluded.size} excluded, #{background.size} background sources, #{errors} error(s)"
exit(errors.zero? ? 0 : 1)
