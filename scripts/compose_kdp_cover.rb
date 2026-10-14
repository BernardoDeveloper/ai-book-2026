#!/usr/bin/env ruby
# frozen_string_literal: true

# Composes the printed hardcover's wraparound cover (back | spine | front) on
# KDP's cover template and writes the flattened CMYK PDF KDP asks for.
#
# Usage: scripts/compose_kdp_cover.rb TEMPLATE.png OUT.pdf [--lang en] [--art PATH]
#
# TEMPLATE.png is the PNG from KDP's cover calculator (assets/cover/kdp/...),
# drawn at 600 dpi for one trim size, page count and paper. Every measure is
# read from its guide lines, so a new page count only needs a new template:
#   blue lines (bottom wrap)  hinge | spine fold | spine fold | hinge
#   black line                trim (the board edge; outside it is wrap)
#   white areas               live areas of back, spine and front
#   yellow box                barcode, which KDP prints: kept as plain background
# Front: the ebook layout (cover_layout.rb) over the art, fitted to the front
# live area. Spine: title and author. Back: book/<lang>/_back_cover.yml.
# Next to OUT it writes OUT-preview.jpg (RGB) and OUT-guides.jpg (template
# lines over the art) for checking; neither is uploaded.

require_relative "cover_layout"
require "tmpdir"

ROOT = CoverLayout::ROOT
args = ARGV.dup
opt = ->(name, default) { (i = args.index(name)) ? args.slice!(i, 2).last : default }
lang = opt.("--lang", "en")
art = opt.("--art", File.join(ROOT, "assets", "cover", "cover-d.png"))
template, out = args
abort "usage: compose_kdp_cover.rb TEMPLATE.png OUT.pdf [--lang en] [--art PATH]" unless template && out

DPI = 600
NAVY = "#0B1A26"
BRASS = "#D7B062"
CREAM = CoverLayout::CREAM
FONTS = CoverLayout::FONTS
ICC = "/usr/share/ghostscript/iccprofiles"

def magick(*cmd) = system("magick", *cmd.map(&:to_s), exception: true)
def capture(*cmd) = IO.popen(["magick", *cmd.map(&:to_s)], &:read).strip

# Runs of a colour along one row or column of the template, as [start, end]
# pairs. `band` rows are merged first, so dashed lines are not missed in a gap.
# The colour is first swapped for a magenta marker, so pixels that were already
# black or white in the template don't count as hits.
def runs(template, color, row: nil, col: nil, band: 1)
  tw, th = capture(template, "-format", "%w %h", "info:").split.map(&:to_i)
  crop = row ? "#{tw}x#{band}+0+#{row}" : "1x#{th}+#{col}+0"
  txt = capture(template, "-crop", crop, "+repage", "-alpha", "off", "-fuzz", "10%", "-fill", "#FF00FF", "-opaque", color,
                "-fill", "white", "+opaque", "#FF00FF", "-fill", "black", "-opaque", "#FF00FF", "-scale", row ? "#{tw}x1!" : "1x#{th}!",
                "-threshold", "99%", "-depth", "8", "txt:-")
  hits = txt.lines.drop(1).filter_map do |l|
    l =~ /\A(\d+),(\d+):.*black/ && (row ? Regexp.last_match(1) : Regexp.last_match(2)).to_i
  end
  hits.slice_when { _2 != _1 + 1 }.map { [_1.first, _1.last] }
end

# --- template geometry ---------------------------------------------------------
pink = "#FFAFAF" # the wrap colour reaches every edge of the template; KDP pads it with white
w = runs(template, pink, row: 100).last.last + 1
h = runs(template, pink, col: 100).last.last + 1
blue = runs(template, "#0000FF", row: h - 300, band: 250).map { (_1 + _2) / 2 }
abort "expected 4 blue guide lines, found #{blue.size}" unless blue.size == 4
hinge_l, fold_l, fold_r, hinge_r = blue
probe = (fold_l + fold_r) / 2 + 150 # inside the spine's live area, clear of its label
trim = runs(template, "#000000", col: probe).first.then { (_1 + _2) / 2 }
live_y0 = runs(template, "#FFFFFF", col: probe).first.first
live_y1 = h - live_y0
white = runs(template, "#FFFFFF", row: live_y0 + 4).reject { |x0, _| x0 >= w }
abort "expected 3 live areas, found #{white.size}" unless white.size == 3
(back_x0, back_x1), (spine_x0, spine_x1), (front_x0, front_x1) = white
bc = capture(template, "-fuzz", "10%", "-fill", "black", "+opaque", "#FFFF00", "-format", "%@", "info:")
bc_w, bc_h, bc_x, bc_y = bc.scan(/\d+/).map(&:to_i)
geom = { canvas: [w, h], folds: [fold_l, fold_r], hinges: [hinge_l, hinge_r], trim:, live_y: [live_y0, live_y1],
         back: [back_x0, back_x1], spine: [spine_x0, spine_x1], front: [front_x0, front_x1], barcode: [bc_x, bc_y, bc_w, bc_h] }
warn "template: #{geom}"

Dir.mktmpdir("kdp-cover") do |tmp|
  # Pango finds the book's fonts through a private fontconfig. Sizes go to it
  # in pixels (pt at DPI): with -density it stops wrapping at the given width.
  px = ->(pt) { format("%.1fpx", pt * DPI / 72.0) }
  File.write(File.join(tmp, "fonts.conf"), <<~XML)
    <?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">
    <fontconfig><include ignore_missing="yes">/etc/fonts/fonts.conf</include>
    <dir>#{FONTS}</dir><cachedir>#{tmp}/fc</cachedir></fontconfig>
  XML
  ENV["FONTCONFIG_FILE"] = File.join(tmp, "fonts.conf")
  pango = lambda do |name, markup, width:, align: "left"|
    path = File.join(tmp, "#{name}.png")
    magick("-background", "none", "-size", "#{width}x", "-define", "pango:align=#{align}",
           "-define", "pango:wrap=word", "pango:#{markup}", "-trim", "+repage", path)
    [path, *capture(path, "-format", "%w %h", "info:").split.map(&:to_i)]
  end

  # --- background: navy with a faint paper grain, across the whole wrap ---------
  bg = File.join(tmp, "bg.png")
  magick("-size", "#{w}x#{h}", "gradient:#10283A-#091520",
         "(", "-size", "#{w}x#{h}", "xc:gray50", "+noise", "Gaussian", "-colorspace", "gray", "-blur", "0x0.8", ")",
         "-compose", "softlight", "-define", "compose:args=12", "-composite", bg)

  # --- front ----------------------------------------------------------------------
  # Art covers everything right of the spine fold, bleed included. The ebook
  # layout (a 1600x2560 virtual cover) is scaled to fit the front live area.
  fw = w - fold_r
  lx0, lx1 = front_x0 - fold_r, front_x1 - fold_r
  s = [(lx1 - lx0) / 1600.0, (live_y1 - live_y0) / 2560.0].min
  vw, vh = 1600 * s, 2560 * s
  vx0, vy0 = lx0 + (lx1 - lx0 - vw) / 2, live_y0 + (live_y1 - live_y0 - vh) / 2
  front = File.join(tmp, "front.png")
  feather = ((hinge_r - fold_r) * 1.6).round # fades the art into the navy spine across the hinge
  magick(art, "-filter", "Lanczos", "-resize", "#{fw}x#{h}^", "-gravity", "center", "-extent", "#{fw}x#{h}",
         "-unsharp", "0x1.2+0.6+0.02",
         *CoverLayout.front_layers(lang:, w: fw, h:, s:, dx: vx0 + vw / 2 - fw / 2.0, top: vy0, bottom: h - (vy0 + vh),
                                   right: fw - (vx0 + vw), with_sticker: false, author_size: 96),
         "(", "-size", "#{h}x#{feather}", "gradient:#{NAVY}FF-#{NAVY}00", "-rotate", "-90", ")",
         "-gravity", "west", "-compose", "over", "-composite", front)

  # --- spine: reads top to bottom, title at the head, author at the foot --------
  # A long title (the PT one) shrinks until at least half an inch separates it
  # from the author.
  t = CoverLayout.texts(lang)
  sw = spine_x1 - spine_x0
  spine = File.join(tmp, "spine.png")
  title_font, author_font = "#{FONTS}/Limelight-Regular.ttf", "#{FONTS}/SourceSans3-Bold.otf"
  text_w = ->(font, pt, kern, text) { capture("-font", font, "-pointsize", pt, "-kerning", kern, "label:#{text}", "-format", "%w", "info:").to_i }
  author_pt = (sw * 0.2).round
  author_kern = (author_pt * 0.22).round
  head = (sw * 0.45).round
  room = live_y1 - live_y0 - 2 * head - (0.5 * DPI).round - text_w.(author_font, author_pt, author_kern, t[:author])
  title_pt = (sw * 0.36).round
  until text_w.(title_font, title_pt, (title_pt * 0.04).round, t[:title_line]) <= room
    title_pt -= 4
    abort "spine too narrow for the title" if title_pt < sw * 0.15
  end
  magick("-size", "#{h}x#{fold_r - fold_l}", "xc:none", "-gravity", "west",
         "-font", title_font, "-pointsize", title_pt, "-kerning", (title_pt * 0.04).round,
         "-fill", CREAM, "-annotate", "+#{live_y0 + head}+0", t[:title_line],
         "-gravity", "east", "-font", author_font, "-pointsize", author_pt,
         "-kerning", author_kern, "-fill", BRASS, "-annotate", "+#{live_y0 + head}+0", t[:author],
         "-rotate", "90", spine)

  # --- back -------------------------------------------------------------------------
  # The body starts at 11 pt and steps down until the copy ends at least a
  # quarter inch above the barcode box.
  copy = YAML.load_file(File.join(ROOT, "book", lang, "_back_cover.yml"))
  pad = (0.42 * DPI).round
  cx0, cx1 = back_x0 + pad, back_x1 - pad
  cw = cx1 - cx0
  st_d = (1.15 * DPI).round
  sticker = CoverLayout.sticker(File.join(tmp, "sticker.png"), k: st_d / 400.0)
  magick(sticker, "-resize", "#{st_d}x#{st_d}", sticker)
  bio_x = cx0 + st_d + (0.25 * DPI).round
  limit = (cx1 > bc_x ? bc_y : live_y1) - (0.25 * DPI).round
  # The author's sayings: a pull-quote block behind a brass bar, each quote's
  # last two words tied so no line holds a lone word.
  qx = cx0 + (0.22 * DPI).round
  sayings = copy["quotes"].map { _1.sub(/ (\S+)\z/, "\u00A0\\1") }
  back_layout = lambda do |body_pt|
    layers = []
    y = live_y0 + (0.3 * DPI).round
    path, _, ph = pango.("headline", %(<span font="Source Sans 3 Bold #{px.(17)}" foreground="#{BRASS}">#{copy['headline']}</span>), width: cw)
    layers << [path, cx0, y]
    y += ph + (0.22 * DPI).round
    copy["paragraphs"].each_with_index do |para, i|
      path, _, ph = pango.("p#{i}", %(<span font="Source Serif 4 #{px.(body_pt)}" foreground="#{CREAM}" line_height="1.3">#{para}</span>), width: cw)
      layers << [path, cx0, y]
      y += ph + (0.2 * DPI).round
    end
    y += (0.1 * DPI).round
    q_top = y
    sayings.each_with_index do |q, i|
      path, _, qh = pango.("q#{i}", %(<span font="Source Serif 4 Italic #{px.(body_pt + 0.5)}" foreground="#{CREAM}" line_height="1.2">#{q}</span>), width: cx1 - qx)
      layers << [path, qx, y]
      y += qh + (0.2 * DPI).round
    end
    q_span = [q_top, y - (0.2 * DPI).round]
    y += (0.3 * DPI).round
    path, _, bh = pango.("bio", %(<span font="Source Sans 3 #{px.(body_pt - 1.5)}" foreground="#{CREAM}" line_height="1.25">#{copy['bio']}</span>), width: cx1 - bio_x)
    layers << [sticker, cx0 - (0.06 * DPI).round, y - (0.08 * DPI).round]
    layers << [path, bio_x, y]
    [layers, q_span, [y + bh, y + st_d].max]
  end
  body_pt = 11.0
  layers, q_span, bottom = back_layout.(body_pt)
  while bottom > limit
    warn "back: #{body_pt} pt ends at #{bottom}, limit #{limit}" if ENV["DEBUG"]
    abort "back copy does not fit above the barcode even at #{body_pt} pt: shorten book/#{lang}/_back_cover.yml" if body_pt <= 9.5
    body_pt -= 0.25
    layers, q_span, bottom = back_layout.(body_pt)
  end
  warn "spine title #{title_pt} px, back body #{body_pt} pt"

  # --- flatten ----------------------------------------------------------------------
  rgb = File.join(tmp, "cover.png")
  magick(bg, front, "-geometry", "+#{fold_r}+0", "-compose", "over", "-composite",
         spine, "-geometry", "+#{fold_l}+0", "-composite",
         "-fill", BRASS, "-draw", "rectangle #{cx0},#{q_span[0]} #{cx0 + 9},#{q_span[1]}",
         *layers.flat_map { |p, x, yy| [p, "-geometry", "+#{x}+#{yy}", "-composite"] },
         "-alpha", "remove", "-alpha", "off", "-units", "PixelsPerInch", "-density", DPI, rgb)
  magick(rgb, "(", template, "-crop", "#{w}x#{h}+0+0", "+repage", "-fuzz", "8%", "-transparent", "#FFFFFF",
         "-channel", "A", "-evaluate", "multiply", "0.55", "+channel", ")", "-composite", "-resize", "25%",
         "-depth", "8", "-quality", "88", out.sub(/\.pdf\z/, "-guides.jpg"))
  magick(rgb, "-depth", "8", "-quality", "92", out.sub(/\.pdf\z/, "-preview.jpg"))
  # Press PDF: CMYK through Ghostscript's default profiles, one flattened image.
  magick(rgb, "-profile", "#{ICC}/default_rgb.icc", "-profile", "#{ICC}/default_cmyk.icc",
         "-units", "PixelsPerInch", "-density", DPI, "-compress", "jpeg", "-quality", "94", out)
end
warn "wrote #{out} (#{format('%.3f x %.3f in', w.to_f / DPI, h.to_f / DPI)})"
