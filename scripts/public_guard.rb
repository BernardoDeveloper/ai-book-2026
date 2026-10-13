#!/usr/bin/env ruby
# frozen_string_literal: true

# Blocks pushing anything that names private infrastructure. The repository is
# public; the author's private repos, hosts and addresses must never appear in
# tracked files or commit messages. The patterns themselves are private, so
# they live in private/forbidden.txt (gitignored, one literal per line); this
# script is a no-op where that file doesn't exist (e.g. CI).
#
# Usage: scripts/public_guard.rb [<rev-range>]   (installed as .git/hooks/pre-push)
# inventory/ is exempt: it mirrors what the public blog already published.

ROOT = File.expand_path("..", __dir__)
list = File.join(ROOT, "private", "forbidden.txt")
exit 0 unless File.exist?(list)

patterns = File.readlines(list, chomp: true).reject { _1.strip.empty? || _1.start_with?("#") }
regex = Regexp.union(patterns.map { Regexp.new(Regexp.escape(_1), Regexp::IGNORECASE) })
hits = []

Dir.chdir(ROOT) do
  `git ls-files -z`.split("\0").each do |f|
    next if f.start_with?("inventory/") || !File.file?(f)

    File.foreach(f).with_index(1) do |line, n|
      hits << "#{f}:#{n}" if line.valid_encoding? && line.match?(regex)
    end
  rescue ArgumentError
    next # binary file
  end
  range = ARGV[0] || "HEAD"
  `git log --format=%H%x09%B #{range} 2>/dev/null`.each_line do |line|
    hits << "commit message: #{line.strip[0, 80]}" if line.match?(regex)
  end
end

if hits.empty?
  puts "public guard: clean"
else
  warn "public guard: private references found, push blocked:"
  hits.uniq.first(30).each { warn "  #{_1}" }
  exit 1
end
