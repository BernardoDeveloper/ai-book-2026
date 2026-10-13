#!/usr/bin/env ruby
# frozen_string_literal: true

# Figure inventory. Reads every figure request in book/<lang>/_figs/*.yml and
# every image reference in the chapters, then:
#   - lists figures still missing their final asset and credits record,
#   - with --placeholders, writes a clearly marked placeholder PNG for each
#     missing one so the book builds before the art exists. Placeholder names
#     are tracked in assets/figures/.placeholders; the image pipeline removes
#     a name from that list when it writes the real asset.
#
# Usage: scripts/figures.rb [lang] [--placeholders]

require "yaml"
require "set"

ROOT = File.expand_path("..", __dir__)
lang = ARGV.find { !_1.start_with?("--") } || "pt"
make = ARGV.include?("--placeholders")
fig_dir = File.join(ROOT, "assets", "figures")
credits = Dir[File.join(ROOT, "assets", "credits", "*.yml")].map { YAML.load_file(_1)["file"] }.to_set
placeholder_list = File.join(fig_dir, ".placeholders")
placeholders = File.exist?(placeholder_list) ? File.readlines(placeholder_list, chomp: true).to_set : Set.new

requests = Dir[File.join(ROOT, "book", lang, "_figs", "*.yml")].sort.flat_map { Array(YAML.load_file(_1)) }
referenced = Dir[File.join(ROOT, "book", lang, "*.md")].flat_map { File.read(_1).scan(%r{\]\((assets/figures/[^)\s]+)\)}).flatten }.uniq

missing = []
referenced.each do |rel|
  path = File.join(ROOT, rel)
  name = File.basename(rel)
  if !File.exist?(path) || placeholders.include?(name)
    req = requests.find { _1["fig"] == File.basename(name, ".*") } || {}
    missing << [rel, req]
    next unless make && !File.exist?(path)

    Dir.mkdir(fig_dir) unless Dir.exist?(fig_dir)
    label = "FIGURA PENDENTE\n#{name}\n#{req['kind']}: #{req['idea'].to_s[0, 90]}"
    system("magick", "-size", "1600x900", "xc:#f2efe8", "-fill", "#5a5a5a", "-gravity", "center",
           "-pointsize", "40", "-annotate", "+0+0", label, path, exception: true)
    placeholders << name
  elsif !credits.include?(rel)
    warn "NO CREDIT RECORD: #{rel}"
  end
end
File.write(placeholder_list, placeholders.sort.join("\n") + "\n") if make && !placeholders.empty?

# Requests carry only the figure id; the asset may be .png or .jpg.
referenced_ids = referenced.map { File.basename(_1, ".*") }
orphans = requests.map { _1["fig"] }.reject { referenced_ids.include?(_1) }
puts "#{referenced.size} figures referenced, #{missing.size} pending, #{orphans.size} requested but unused"
missing.each { |rel, req| puts "  PENDING #{rel} (#{req['kind'] || '?'})" }
orphans.each { puts "  ORPHAN  #{_1} (requested, not referenced in any chapter)" }
