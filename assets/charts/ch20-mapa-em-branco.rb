#!/usr/bin/env ruby
# frozen_string_literal: true

# ch20-mapa-em-branco: AI-generated map art (assets/art/ch20-mapa-em-branco-base.png,
# label-free, see assets/credits/ch20-mapa-em-branco.yml) with labels set as
# real type, per language. Reproduces the recorded post-processing:
# upscale, paint out three generated banners, overlay labels.
# Usage: ruby assets/charts/ch20-mapa-em-branco.rb [pt|en]

ROOT = File.expand_path("../..", __dir__)
lang = ARGV[0] || "pt"
fonts = File.join(ROOT, "assets", "fonts")
L = {
  "pt" => { public: "público", private: "privado", code: "código das empresas", games: "jogos comerciais",
            banks: "sistemas de bancos", forms: "formulários", records: "cadastros", sites: "sites" },
  "en" => { public: "public", private: "private", code: "company code", games: "commercial games",
            banks: "banking systems", forms: "forms", records: "records", sites: "websites" },
}.fetch(lang)
out = File.join(ROOT, "assets", "figures", *(lang == "pt" ? [] : [lang]), "ch20-mapa-em-branco.png")
Dir.mkdir(File.dirname(out)) unless Dir.exist?(File.dirname(out))

label = ->(font, size, color, off, text, under: nil) {
  ["-font", "#{fonts}/#{font}", "-pointsize", size.to_s, "-fill", color,
   *(under ? ["-undercolor", under] : ["-undercolor", "none"]), "-annotate", off, text]
}
system("magick", File.join(ROOT, "assets", "art", "ch20-mapa-em-branco-base.png"),
       "-background", "#FBF9F4", "-alpha", "remove", "-alpha", "off", "-colorspace", "sRGB",
       "-filter", "Lanczos", "-resize", "2400x1600!",
       "-fill", "#E8DABC", "-draw", "rectangle 315,190 712,318", "-draw", "rectangle 1680,208 2085,345",
       "-draw", "rectangle 1745,1135 2128,1268",
       "-gravity", "center",
       *label.("NotoSans-SemiBold.ttf", 54, "#1B2238", "-694+208", L[:public]),
       *label.("NotoSans-SemiBold.ttf", 96, "#2B3A67", "-50-330", L[:private]),
       *label.("NotoSans-Italic.ttf", 52, "#565C68", "-680-546", L[:code]),
       *label.("NotoSans-Italic.ttf", 52, "#565C68", "+680-524", L[:games]),
       *label.("NotoSans-Italic.ttf", 52, "#565C68", "+735+400", L[:banks]),
       *label.("NotoSans-Regular.ttf", 44, "#1B2238", "-840-160", L[:forms], under: "#FBF9F4"),
       *label.("NotoSans-Regular.ttf", 44, "#1B2238", "-440+105", L[:records], under: "#FBF9F4"),
       *label.("NotoSans-Regular.ttf", 44, "#1B2238", "-95+260", L[:sites], under: "#FBF9F4"),
       out, exception: true)
warn "wrote #{out}"
