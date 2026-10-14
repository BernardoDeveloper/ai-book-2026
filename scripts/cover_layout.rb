# frozen_string_literal: true

# Front-cover layout shared by the ebook cover (compose_cover.rb) and the
# printed wraparound (compose_kdp_cover.rb). The layout is drawn on a virtual
# 1600x2560 cover scaled by `s` and placed inside a larger canvas: `top`,
# `bottom` and `right` are the canvas margins around that virtual cover and
# `dx` shifts it horizontally from the canvas centre. The ebook passes
# s=1 and zero margins.
#   title:    Limelight (OFL), art deco display face
#   subtitle/author: Source Sans 3 (OFL), the book's heading face

require "yaml"
require "fileutils"

module CoverLayout
  ROOT = File.expand_path("..", __dir__)
  FONTS = File.join(ROOT, "assets", "fonts")
  CREAM = "#F4E9D0"
  SHADOW = "#0B1A26"
  STICKER_SRC = File.join(ROOT, "assets", "cover", "akita-portrait.png")

  module_function

  def meta = YAML.load_file(File.join(ROOT, "book", "outline.yml"))["meta"]

  # Title, subtitle and author for an edition, broken where the words land well
  # on a poster: "COMPETENTE / O SUFICIENTE".
  def texts(lang)
    m = meta
    suffix = lang == "pt" ? "" : "_#{lang}"
    words = (m["working_title#{suffix}"] || m["working_title"]).upcase.split
    { title: words.size > 2 ? "#{words.first}\n#{words[1..].join(' ')}" : words.join("\n"),
      title_line: words.join(" "),
      subtitle: (m["subtitle#{suffix}"] || m["subtitle"]).to_s.sub(/,\s*/, ",\n"),
      author: m["author"].to_s.upcase }
  end

  def text_layer(w:, h:, font:, size:, text:, gravity:, offset:, s: 1, kerning: 0, interline: 0)
    geo = ->(x, y) { format("%+d%+d", x.round, y.round) }
    ["(", "-size", "#{w}x#{h}", "xc:none", "-font", font, "-pointsize", (size * s).round.to_s,
     "-kerning", (kerning * s).to_s, "-interline-spacing", (interline * s).to_s, "-gravity", gravity,
     "-fill", SHADOW, "-annotate", geo.(offset[0] + 6 * s, offset[1] + 8 * s), text, "-blur", "0x#{10 * s}",
     "-fill", CREAM, "-annotate", geo.(*offset), text, ")", "-composite"]
  end

  # Author sticker: the official portrait (from the AI-Lair site) as a round
  # die-cut sticker, tilted. `k` scales the whole sticker (k=1: 452 px before
  # rotation), so print gets a sharper one instead of an upscaled ebook sticker.
  def sticker(out, k: 1)
    return nil unless File.exist?(STICKER_SRC)

    d = (400 * k).round
    c = (452 * k).round
    FileUtils.mkdir_p(File.dirname(out))
    system("magick", STICKER_SRC, "-background", CREAM, "-alpha", "remove", "-alpha", "off",
           "-crop", "1180x1180+230+40", "+repage", "-resize", "#{d}x#{d}",
           "(", "-size", "#{d}x#{d}", "xc:black", "-fill", "white", "-draw", "circle #{d / 2},#{d / 2} #{d / 2},#{(2 * k).round}", ")",
           "-alpha", "off", "-compose", "CopyOpacity", "-composite", out, exception: true)
    system("magick", "-size", "#{c}x#{c}", "xc:none", "-fill", "#FBF9F4", "-stroke", "#1B2238", "-strokewidth", (5 * k).round.to_s,
           "-draw", "circle #{c / 2},#{c / 2} #{c / 2},#{(6 * k).round}", out, "-geometry", "+#{(26 * k).round}+#{(26 * k).round}",
           "-compose", "over", "-composite",
           "(", "+clone", "-background", SHADOW, "-shadow", "70x#{10 * k}+#{(8 * k).round}+#{(12 * k).round}", ")", "+swap",
           "-background", "none", "-layers", "merge", "+repage", "-rotate", "-7", out, exception: true)
    out
  end

  # ImageMagick arguments that draw the front-cover type (and the sticker) over
  # a w x h canvas already holding the art.
  def front_layers(lang:, w:, h:, s: 1, dx: 0, top: 0, bottom: 0, right: 0, sticker_k: 1)
    t = texts(lang)
    st = sticker(File.join(ROOT, "build", sticker_k == 1 ? "cover-sticker.png" : "cover-sticker@#{sticker_k}.png"), k: sticker_k)
    [
      # a gentle darkening behind the title keeps it legible on bright skies
      "(", "-size", "#{w}x#{(top + 900 * s).round}", "gradient:#0B1A26B0-#0B1A2600", ")", "-gravity", "north", "-composite",
      *text_layer(w:, h:, s:, font: "#{FONTS}/Limelight-Regular.ttf", size: 190, text: t[:title], gravity: "north",
                  offset: [dx, top + 150 * s], kerning: 4, interline: -10),
      # Footer block: subtitle above the author, both on a dark gradient, so the
      # title area at the top stays clear of the art's focal point (the robot head).
      "(", "-size", "#{w}x#{(bottom + 820 * s).round}", "gradient:#0B1A2600-#0B1A26E0", ")", "-gravity", "south", "-composite",
      *text_layer(w:, h:, s:, font: "#{FONTS}/SourceSans3-Semibold.otf", size: 54, text: t[:subtitle], gravity: "south",
                  offset: [dx, bottom + 430 * s], kerning: 2),
      *text_layer(w:, h:, s:, font: "#{FONTS}/SourceSans3-Bold.otf", size: 78, text: t[:author], gravity: "south",
                  offset: [dx - 190 * s, bottom + 150 * s], kerning: 18),
      # Bottom-right corner, beside the author name, like a signature badge.
      *(st ? ["(", st, "-resize", "#{(360 * s).round}x#{(360 * s).round}", ")", "-gravity", "southeast",
              "-geometry", format("+%d+%d", (right + 70 * s).round, (bottom + 40 * s).round), "-compose", "over", "-composite"] : [])
    ]
  end
end
