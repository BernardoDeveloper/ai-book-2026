#!/usr/bin/env ruby
# frozen_string_literal: true

# Renders one diagram-as-code figure for one language.
#   assets/diagrams/<fig>.d2           D2 source with {{label-key}} placeholders
#   assets/diagrams/<fig>.labels.yml   { pt: {key: text}, en: {key: text} }
# Output: assets/figures/<fig>.png (2x, flattened on the paper colour, sRGB)
# and assets/figures/<fig>.svg. House style: docs/research/IMAGES.md §4.
#
# Usage: scripts/render_diagram.rb assets/diagrams/<fig>.d2 <lang> <d2-binary>

require "yaml"
require "fileutils"

src, lang, d2 = ARGV
abort "usage: render_diagram.rb SRC LANG D2" unless src && lang && d2
ROOT = File.expand_path("..", __dir__)
fig = File.basename(src, ".d2")
labels_path = src.sub(/\.d2\z/, ".labels.yml")
labels = File.exist?(labels_path) ? YAML.load_file(labels_path).fetch(lang) : {}
text = File.read(src).gsub(/\{\{([\w-]+)\}\}/) do
  labels.fetch(Regexp.last_match(1)) { abort "#{fig}: label '#{Regexp.last_match(1)}' missing for #{lang}" }.to_s.gsub('"', '\"')
end

out_dir = File.join(ROOT, "assets", "figures")
FileUtils.mkdir_p(out_dir)
tmp = File.join(ROOT, "build", "diagrams", lang)
FileUtils.mkdir_p(tmp)
resolved = File.join(tmp, "#{fig}.d2")
File.write(resolved, text)
# D2 resolves imports next to the file it compiles; bring the house style along.
Dir[File.join(File.dirname(src), "_*.d2")].each { FileUtils.cp(_1, tmp) }
fonts = File.join(ROOT, "assets", "fonts")
svg = File.join(out_dir, "#{fig}.svg")
png = File.join(out_dir, "#{fig}.png")
system(d2, "--pad=40", "--font-regular=#{fonts}/NotoSans-Regular.ttf", "--font-bold=#{fonts}/NotoSans-SemiBold.ttf",
       "--font-italic=#{fonts}/NotoSans-Italic.ttf", resolved, svg, exception: true)
# D2 embeds the fonts as WOFF under generated family names, which Inkscape
# (magick's SVG delegate) doesn't honour, so it falls back to a default sans.
# Rasterize a copy whose families point at the installed Noto Sans instead.
raster_src = File.join(tmp, "#{fig}.raster.svg")
File.write(raster_src, File.read(svg).gsub(/d2-\d+-font-(regular|bold|semibold|italic)/) do
  { "bold" => "Noto Sans SemiBold", "semibold" => "Noto Sans SemiBold", "italic" => "Noto Sans Italic" }.fetch(Regexp.last_match(1), "Noto Sans")
end)
# Inkscape prints the embedded fonts on stderr; keep it quiet.
system("magick", "-density", "300", "-background", "#FBF9F4", raster_src, "-flatten", "-alpha", "remove", "-alpha", "off",
       "-colorspace", "sRGB", "-resize", "2400x2400>", png, err: File::NULL, exception: true)

ph = File.join(out_dir, ".placeholders")
if File.exist?(ph)
  File.write(ph, File.readlines(ph, chomp: true).reject { _1 == "#{fig}.png" }.map { "#{_1}\n" }.join)
end
warn "rendered #{fig} (#{lang})"
