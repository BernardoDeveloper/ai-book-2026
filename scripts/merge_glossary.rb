#!/usr/bin/env ruby
# frozen_string_literal: true

# Merges per-chapter glossary proposals (book/<lang>/_gls/*.yml) into
# book/back/glossary-<lang>.yml. New keys are added; existing keys are never
# overwritten (definitions are curated in the main file), but conflicting
# proposals are reported so an editor can choose. Also reports seed terms no
# chapter uses, so dead entries don't ship.
#
# Usage: scripts/merge_glossary.rb [lang]

require "yaml"

ROOT = File.expand_path("..", __dir__)
lang = ARGV[0] || "pt"
main_path = File.join(ROOT, "book", "back", "glossary-#{lang}.yml")
main = YAML.load_file(main_path) || {}
header = File.read(main_path)[/\A(#.*\n)+/].to_s

added = []
Dir[File.join(ROOT, "book", lang, "_gls", "*.yml")].sort.each do |path|
  (YAML.load_file(path) || {}).each do |key, entry|
    if main.key?(key)
      warn "conflict #{key} (#{File.basename(path)}): keeping curated definition" if main[key]["def"] != entry["def"]
    else
      main[key] = entry
      added << key
    end
  end
end

used = Dir[File.join(ROOT, "book", lang, "*.md")].flat_map do |f|
  File.read(f).scan(/\[([^\]]+)\]\{\.gls(?:\s+key=([\w-]+))?\}/).map { |t, k| k || t.downcase }
end.uniq
unused = main.keys - used
unknown = used - main.keys

File.write(main_path, header + main.sort.to_h.to_yaml.sub(/\A---\n/, ""))
warn "#{added.size} added (#{added.join(', ')}); #{main.size} total"
warn "unused glossary keys: #{unused.join(', ')}" unless unused.empty?
warn "UNKNOWN keys used in chapters: #{unknown.join(', ')}" unless unknown.empty?
exit(unknown.empty? ? 0 : 1)
