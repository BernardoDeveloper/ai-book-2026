#!/usr/bin/env ruby
# frozen_string_literal: true

# Compares two persona review rounds (docs/PERSONA-REVIEW.md): per-unit
# engagement scores for each persona, the average per unit and the change,
# the book average, and annotation counts by type. Changes nothing.
#
#   scripts/persona_compare.rb reviews/<v>/personas reviews/<v>/personas-round2
#   scripts/persona_compare.rb OLD NEW --grep 'ch20|linha reta'   (round-2
#       annotations whose unit, quote or note match, to see what recurs)
#
# Scores are noisy (unchanged chapters move by up to ~0.6 between rounds);
# read the recurring annotations, not the averages alone.

require "yaml"
require "optparse"

opts = {}
OptionParser.new { |o| o.on("--grep REGEX") { opts[:grep] = Regexp.new(_1, Regexp::IGNORECASE) } }.parse!
abort "usage: persona_compare.rb OLD_DIR NEW_DIR [--grep REGEX]" unless ARGV.size == 2

load_round = lambda do |dir|
  Dir[File.join(dir, "*.yml")].sort.to_h { |f| [File.basename(f, ".yml"), YAML.load_file(f)] }
                              .select { |_, d| d.is_a?(Hash) && d["units"] }
end
old, new = ARGV.map { load_round.(_1) }
personas = (old.keys | new.keys).sort
units = (old.values + new.values).flat_map { |d| d["units"].map { _1["unit"] } }.uniq
score = ->(round, p, u) { (round[p]&.dig("units")&.find { _1["unit"] == u } || {})["score"] }
mean = ->(xs) { xs = xs.compact; xs.empty? ? nil : xs.sum.to_f / xs.size }

puts "unit".ljust(12) + personas.map { _1[0, 5].ljust(8) }.join + "old  new  delta"
sums = [[], []]
units.each do |u|
  a = personas.map { score.(old, _1, u) }
  b = personas.map { score.(new, _1, u) }
  next if a.compact.size < 2 && b.compact.size < 2 # an appendix only one reader scored

  m1, m2 = mean.(a), mean.(b)
  sums[0] << m1 if m1
  sums[1] << m2 if m2
  delta = m1 && m2 ? format("%+.1f", m2 - m1) : ""
  puts u.ljust(12) + a.zip(b).map { |x, y| "#{x}->#{y}".ljust(8) }.join +
       "#{m1 ? format('%.1f', m1) : ' -  '}  #{m2 ? format('%.1f', m2) : ' -  '}  #{delta}"
end
puts format("book average: %.2f -> %.2f", mean.(sums[0]), mean.(sums[1]))
count = ->(round) { round.values.flat_map { Array(_1["annotations"]) }.group_by { _1["type"] }.transform_values(&:size).sort.to_h }
puts "annotations old: #{count.(old)}"
puts "annotations new: #{count.(new)}"

if opts[:grep]
  puts "", "round-2 annotations matching #{opts[:grep].source}:"
  new.each do |p, d|
    Array(d["annotations"]).each do |a|
      text = "#{a['unit']} #{a['quote']} #{a['why']}"
      puts "  #{p[0, 5]} #{a['unit']} #{a['type']}: #{a['why'].to_s.gsub("\n", ' ')[0, 160]}" if text.match?(opts[:grep])
    end
  end
end
