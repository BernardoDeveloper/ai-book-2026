#!/usr/bin/env ruby
# frozen_string_literal: true

# EN house style: periods and commas go inside closing quotation marks
# (American style), and a quoted question or exclamation takes no extra
# period ('?".' -> '?"'). Touches prose lines only: front matter, code blocks,
# figure/table lines, attribute values (fig-alt="...") and the generated
# back-matter pages are left alone.
#
# Usage: scripts/en_quote_punct.rb [--check] [files...]   (default: book/en/*.md)

check = ARGV.delete("--check")
GENERATED = %w[glossario bibliografia fontes creditos].freeze # rebuilt by scripts/gen_back_matter.rb
files = ARGV.empty? ? Dir[File.expand_path("../book/en/*.md", __dir__)] : ARGV
files = files.reject { GENERATED.include?(File.basename(_1, ".md")) }
bad = 0
files.sort.each do |f|
  text = File.read(f)
  fm = text[/\A---.*?^---[ \t]*$\n?/m].to_s
  body = text[fm.size..]
  in_code = false
  out = body.lines.map do |line|
    in_code = !in_code if line.start_with?("```")
    next line if in_code || line.lstrip.start_with?("!", "|", ":::", "<!--")

    line.gsub(/([?!])"\./) { %(#{$1}") }
        .gsub(/(?<![=\w])"([^"\n]+?)"([.,])/) { %("#{$1}#{$2}") }
        .gsub(/([?!])\."/) { %(#{$1}") }
  end.join
  next if out == body

  bad += 1
  check ? warn("quote punctuation: #{f}") : File.write(f, fm + out)
end
exit(check && bad.positive? ? 1 : 0)
