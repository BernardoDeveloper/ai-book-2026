#!/usr/bin/env ruby
# frozen_string_literal: true

# Tooling for copyedit findings files (docs/COPYEDIT.md step 2; format in
# reviews/README.md): reviews/<version>/<lang>/part*.yml, each a list of items
# (or a hash with `findings:` / `items:`). <dir> is that folder; the language
# is its basename.
#
#   review.rb validate <dir>   schema check, quotes found in the unit (the actual
#                              line is reported when it moved), stable ids
#                              `<part>.<n>` added to items that lack one (the
#                              file is rewritten only then). Exit 1 on schema
#                              errors or quotes not found.
#   review.rb summary <dir> [--grep REGEX]
#                              one line per item + counts per category/severity;
#                              REGEX filters over problem + suggestion
#   review.rb status <dir>     after applying: items whose quote is still verbatim
#                              in the unit ("unchanged"); ids listed in triage.md
#                              under a heading containing "Rejected" or "No change"
#                              are shown as "rejected" instead
#
# Units: "prefacio" and "index" are book/<lang>/index.md; "glossary" is
# book/back/glossary-<lang>.yml, where the quote is the entry key
# (and `line` is optional).

require "yaml"
require "optparse"

ROOT = File.expand_path("..", __dir__)
REQUIRED = %w[unit line quote category severity problem suggestion].freeze
CATEGORIES = %w[error consistency repetition clarity pacing].freeze
SEVERITIES = %w[high medium low].freeze

Item = Struct.new(:id, :data, :file, :index)

def items_of(doc)
  return doc if doc.is_a?(Array)
  return doc["findings"] || doc["items"] || [] if doc.is_a?(Hash)

  []
end

# Loads every part file of the folder. Returns [items, rewrites, errors]; rewrites maps
# a path to its new content when ids had to be added.
def load_dir(dir)
  items = []
  rewrites = {}
  errors = []
  files = Dir[File.join(dir, "part*.yml")].sort_by { [File.basename(_1)[/part(\d+)/, 1].to_i, _1] }
  errors << "#{dir}: no part*.yml files" if files.empty?
  files.each do |path|
    name = File.basename(path)
    part = name[/part(\d+)/, 1] or (errors << "#{name}: file name needs a part number (part<N>-...)"; next)
    doc = YAML.safe_load_file(path, permitted_classes: [Date, Time])
    list = items_of(doc)
    errors << "#{name}: no findings (expected a list or findings:/items:)" if list.empty?
    added = false
    list.each_with_index do |raw, i|
      unless raw.is_a?(Hash)
        errors << "#{name}[#{i + 1}]: item is not a mapping"
        next
      end
      id = "#{part}.#{i + 1}"
      if raw["id"].nil?
        added = true
        fixed = { "id" => id }.merge(raw)
        raw.replace(fixed)
      end
      items << Item.new(raw["id"].to_s, raw, name, i + 1)
    end
    rewrites[path] = YAML.dump(doc) if added
  end
  [items, rewrites, errors]
end

def lang_of(dir) = File.basename(File.expand_path(dir))

# Text to search for the unit, and the line lookup. Glossary: the quote is a key.
def unit_source(unit, lang)
  case unit.to_s
  when "prefacio", "index" then File.join(ROOT, "book", lang, "index.md")
  when "glossary" then File.join(ROOT, "book", "back", "glossary-#{lang}.yml")
  else File.join(ROOT, "book", lang, "#{unit}.md")
  end
end

def occurrences(text, quote)
  lines = []
  from = 0
  while (idx = text.index(quote, from))
    lines << text[0...idx].count("\n") + 1
    from = idx + 1
  end
  lines
end

def trunc(str, len)
  s = str.to_s.gsub(/\s+/, " ").strip
  s.size > len ? "#{s[0, len - 1]}…" : s
end

def validate_item(item, lang, cache)
  d = item.data
  where = "#{item.file}##{item.id}"
  errs = []
  notes = []
  required = d["unit"].to_s == "glossary" ? REQUIRED - ["line"] : REQUIRED # glossary entries have no line
  missing = required.reject { d.key?(_1) && !d[_1].to_s.strip.empty? }
  errs << "#{where}: missing #{missing.join(', ')}" unless missing.empty?
  errs << "#{where}: category '#{d['category']}' not one of #{CATEGORIES.join('|')}" if d["category"] && !CATEGORIES.include?(d["category"].to_s)
  errs << "#{where}: severity '#{d['severity']}' not one of #{SEVERITIES.join('|')}" if d["severity"] && !SEVERITIES.include?(d["severity"].to_s)
  errs << "#{where}: line must be an integer" if d["line"] && !d["line"].is_a?(Integer)
  return [errs, notes] unless missing.empty?

  src = unit_source(d["unit"], lang)
  rel = src.delete_prefix(ROOT + "/")
  unless File.exist?(src)
    return [errs << "#{where}: unit #{d['unit']} has no #{rel}", notes]
  end

  quote = d["quote"].to_s
  if d["unit"].to_s == "glossary"
    keys = (cache[src] ||= YAML.load_file(src, permitted_classes: [Date, Time]).keys)
    errs << "#{where}: glossary key '#{quote}' not in #{rel}" unless keys.include?(quote)
  else
    text = (cache[src] ||= File.read(src))
    lines = occurrences(text, quote)
    if lines.empty?
      errs << "#{where}: quote not found in #{rel}: #{trunc(quote, 70)}"
    elsif d["line"] && !lines.include?(d["line"])
      actual = lines.min_by { (_1 - d["line"]).abs }
      notes << "#{where}: moved, line #{d['line']} -> #{actual} (#{rel})"
    end
  end
  [errs, notes]
end

def cmd_validate(dir)
  lang = lang_of(dir)
  items, rewrites, errors = load_dir(dir)
  cache = {}
  notes = []
  items.each do |item|
    e, n = validate_item(item, lang, cache)
    errors.concat(e)
    notes.concat(n)
  end
  dup = items.group_by(&:id).select { |_, v| v.size > 1 }.keys
  dup.each { errors << "duplicate id #{_1}" }
  rewrites.each do |path, content|
    File.write(path, content)
    puts "ids added: #{File.basename(path)}"
  end
  notes.each { puts "  moved  #{_1}" }
  errors.each { puts "  ERROR  #{_1}" }
  puts "review (#{lang}): #{items.size} item(s), #{errors.size} error(s), #{notes.size} moved"
  errors.empty?
end

def cmd_summary(dir, grep)
  items, _, errors = load_dir(dir)
  abort errors.join("\n") if items.empty? && errors.any?
  re = grep && Regexp.new(grep, Regexp::IGNORECASE)
  shown = items.select { !re || "#{_1.data['problem']} #{_1.data['suggestion']}".match?(re) }
  shown.each do |it|
    d = it.data
    puts "#{it.id.ljust(5)} #{d['category']}/#{d['severity']}  #{d['unit']}:#{d['line']}  " \
         "\"#{trunc(d['quote'], 40)}\"  #{trunc(d['problem'], 90)}"
  end
  puts
  puts "#{shown.size} of #{items.size} item(s)"
  puts "  by category: " + shown.group_by { _1.data["category"] }.sort.map { |k, v| "#{k} #{v.size}" }.join(", ")
  puts "  by severity: " + shown.group_by { _1.data["severity"] }.sort_by { |k, _| SEVERITIES.index(k.to_s) || 9 }
                              .map { |k, v| "#{k} #{v.size}" }.join(", ")
  true
end

# ids mentioned in the Rejected / No change sections of triage.md (ranges "6.15-6.17" expand).
def rejected_ids(dir)
  path = File.join(dir, "triage.md")
  return [] unless File.exist?(path)

  ids = []
  inside = false
  File.readlines(path, chomp: true).each do |line|
    if (h = line.match(/\A#+\s+(.*)/))
      inside = h[1].match?(/rejected|no change/i)
      next
    end
    next unless inside

    line.scan(/(?<![\d.])(\d+)\.(\d+)(?:\s*[-–]\s*(?:\d+\.)?(\d+))?(?![\d]|\.\d)/) do |part, from, to|
      (from.to_i..(to || from).to_i).each { ids << "#{part}.#{_1}" }
    end
  end
  ids.uniq
end

def cmd_status(dir)
  lang = lang_of(dir)
  items, _, errors = load_dir(dir)
  abort errors.join("\n") if items.empty? && errors.any?
  rejected = rejected_ids(dir)
  cache = {}
  unchanged = []
  items.each do |it|
    d = it.data
    src = unit_source(d["unit"], lang)
    next unless File.exist?(src)

    quote = d["quote"].to_s
    present = if d["unit"].to_s == "glossary"
                (cache[src] ||= YAML.load_file(src, permitted_classes: [Date, Time]).keys).include?(quote)
              else
                (cache[src] ||= File.read(src)).include?(quote)
              end
    next unless present

    # A glossary item's quote is the entry key, which stays: only a person can tell.
    state = if rejected.include?(it.id) then "rejected"
            elsif d["unit"].to_s == "glossary" then "by hand"
            else "unchanged"
            end
    unchanged << [state, it]
  end
  unchanged.each do |state, it|
    d = it.data
    puts "#{state.ljust(9)} #{it.id.ljust(5)} #{d['unit']}:#{d['line']}  \"#{trunc(d['quote'], 50)}\"  #{trunc(d['problem'], 70)}"
  end
  count = ->(state) { unchanged.count { _1[0] == state } }
  puts "status (#{lang}): #{items.size} item(s); #{count.('unchanged')} unchanged (quote still present), " \
       "#{count.('by hand')} glossary to check by hand, #{count.('rejected')} rejected, " \
       "#{items.size - unchanged.size} edited away"
  true
end

cmd = ARGV.shift
dir = ARGV.shift
usage = "usage: review.rb validate|summary|status <reviews/version/lang> [--grep REGEX]"
abort usage unless %w[validate summary status].include?(cmd) && dir && File.directory?(dir)

ok = case cmd
     when "validate" then cmd_validate(dir)
     when "summary"
       grep = nil
       OptionParser.new { |o| o.on("--grep RE") { grep = _1 } }.parse!(ARGV)
       cmd_summary(dir, grep)
     else cmd_status(dir)
     end
exit(ok ? 0 : 1)
