#!/usr/bin/env ruby
# frozen_string_literal: true

# Merges per-chapter bibliography proposals (book/<lang>/_refs/*.yaml) into
# book/back/references.yaml. Entries are deduplicated by normalized URL (or by
# id when there is no URL). When two chapters used different keys for the same
# source, the key already in the bibliography (or the first seen) wins and the
# losing key is rewritten in the chapter files. `note` fields are unioned so
# every entry keeps its "cited-by" provenance.
#
# Usage: scripts/merge_refs.rb [lang]

require "yaml"
require "date"

ROOT = File.expand_path("..", __dir__)
lang = ARGV[0] || "pt"
main_path = File.join(ROOT, "book", "back", "references.yaml")

def norm_url(u)
  u.to_s.strip.sub(%r{\Ahttps?://(www\.)?}, "").sub(%r{/\z}, "").downcase
end

def load_refs(path)
  Array((YAML.load_file(path, permitted_classes: [Date]) || {})["references"])
end

merged = File.exist?(main_path) ? load_refs(main_path) : []
by_id = merged.to_h { [_1["id"], _1] }
by_url = merged.select { _1["URL"] }.to_h { [norm_url(_1["URL"]), _1] }
renames = {} # chapter => { old_key => new_key }: key clashes, local to the proposing chapter
aliases = {} # old_key => canonical key: same work under another key, rewritten book-wide

Dir[File.join(ROOT, "book", lang, "_refs", "*.yaml")].sort.each do |path|
  chapter = File.basename(path, ".yaml")
  load_refs(path).each do |ref|
    existing = (ref["URL"] && by_url[norm_url(ref["URL"])]) || by_id[ref["id"]]
    if existing.nil?
      merged << ref
      by_id[ref["id"]] = ref
      by_url[norm_url(ref["URL"])] = ref if ref["URL"]
      next
    end
    if existing["URL"] && ref["URL"] && norm_url(existing["URL"]) != norm_url(ref["URL"])
      # Found by key only: same key, different source. Rename the newcomer.
      new_id = "#{ref['id']}#{('b'..'z').find { |s| !by_id.key?("#{ref['id']}#{s}") }}"
      warn "key clash #{ref['id']} (#{chapter}) -> #{new_id}"
      (renames[chapter] ||= {})[ref["id"]] = new_id
      ref = ref.merge("id" => new_id)
      merged << ref
      by_id[new_id] = ref
      by_url[norm_url(ref["URL"])] = ref
      next
    end
    if existing["id"] != ref["id"]
      # Same source under another key. If that key names another work in the
      # bibliography (a clash renamed on an earlier run), the rewrite stays in
      # the proposing chapter; otherwise it is an alias, rewritten book-wide.
      if by_id.key?(ref["id"])
        (renames[chapter] ||= {})[ref["id"]] = existing["id"]
      else
        aliases[ref["id"]] = existing["id"]
      end
    end
    notes = [existing["note"], ref["note"]].compact.flat_map { _1.sub(/\Acited-by:\s*/, "").split(/,\s*/) }.uniq
    existing["note"] = "cited-by: #{notes.join(', ')}" unless notes.empty?
  end
end

rewrite = lambda do |file, map|
  text = File.read(file)
  changed = map.reduce(text) { |t, (old, new)| t.gsub(/@#{Regexp.escape(old)}(?![\w:.-]*\w)/, "@#{new}") }
  return if changed == text

  File.write(file, changed)
  warn "rewrote keys in #{File.basename(file)}: #{map.map { |o, n| "#{o}->#{n}" }.join(", ")}"
end

# Aliases apply to every chapter: a chapter may cite a key it never proposed.
Dir[File.join(ROOT, "book", lang, "*.md")].each { rewrite.(_1, aliases) } unless aliases.empty?

renames.each do |chapter, map|
  file = File.join(ROOT, "book", lang, chapter == "prefacio" ? "index.md" : "#{chapter}.md")
  next unless File.exist?(file)

  rewrite.(file, map)
end

merged.sort_by! { _1["id"] }
File.write(main_path, { "references" => merged }.to_yaml)
warn "#{merged.size} references in #{main_path.delete_prefix(ROOT + '/')}"
