#!/usr/bin/env ruby
# frozen_string_literal: true

# Generates one label-free concept illustration with the pinned OpenAI image
# model and the house style prefix (docs/research/IMAGES.md §4), then writes
#   assets/figures/<fig>.png         flattened on paper colour, sRGB, no alpha
#   assets/credits/<fig>.yml         full generation record (model, prompt,
#                                    params, request id, cost, KDP disclosure)
#   build/genimg/<fig>-<n>.png       every draft, for selection
#
# Usage: scripts/gen_image.rb <fig-id> "<scene description>" [--size 1536x1024] [--quality high] [--n 2]
#        scripts/gen_image.rb <fig-id> --select N     (use draft N instead; no API call)
#        --style-file PATH  use the style prefix in PATH instead of the interior house style
#                           (the cover uses assets/cover/STYLE-cover.txt)
#        --out PATH         write the final image elsewhere than assets/figures/<fig>.png
# The key is read from OPENAI_API_KEY or ~/.config/zsh/secrets; it is never printed.
# Never use this for likenesses of real people (house rule).

require "json"
require "net/http"
require "uri"
require "yaml"
require "base64"
require "digest"
require "fileutils"
require "time"

ROOT = File.expand_path("..", __dir__)
MODEL = "gpt-image-2.5-flare-2026-09-08"
STYLE = <<~S.tr("\n", " ").strip
  STYLE v1: flat editorial vector illustration, thick uniform ink outlines (#1B2238),
  limited palette navy #2B3A67, teal #2F7F86, amber #E3A23B accent, sand #E9DFC9 panels,
  off-white #FBF9F4 background, generous whitespace, no gradients, no textures,
  no text, no letters, no numbers, no logos, no real people, high contrast,
  reads clearly in grayscale.
S

def finalize(src, out)
  FileUtils.mkdir_p(File.dirname(out))
  system("magick", src, "-background", "#FBF9F4", "-alpha", "remove", "-alpha", "off", "-colorspace", "sRGB", out, exception: true)
end

fig, scene = ARGV[0], ARGV[1]
if scene == "--select"
  n = ARGV[2].to_i
  credits = File.join(ROOT, "assets", "credits", "#{fig}.yml")
  rec = YAML.load_file(credits)
  src = File.join(ROOT, rec["generation"]["drafts"].fetch(n - 1))
  out = File.join(ROOT, rec["file"])
  finalize(src, out)
  rec["generation"]["selected"] = n
  rec["sha256"] = Digest::SHA256.file(out).hexdigest
  File.write(credits, rec.to_yaml)
  warn "#{fig}: selected draft #{n}"
  exit
end
abort "usage: gen_image.rb FIG-ID 'scene description' [--size WxH] [--quality q] [--n N]" unless fig && scene
opt = ->(name, default) { (i = ARGV.index("--#{name}")) ? ARGV[i + 1] : default }
size = opt.("size", "1536x1024")
quality = opt.("quality", "high")
n = opt.("n", "2").to_i

key = ENV["OPENAI_API_KEY"] || File.read(File.expand_path("~/.config/zsh/secrets"))[/^export OPENAI_API_KEY=["']?([^"'\s]+)/, 1]
abort "OPENAI_API_KEY not found" unless key

style_file = opt.("style-file", nil)
style = style_file ? File.read(style_file).tr("\n", " ").strip : STYLE
style_version = style_file ? File.basename(style_file, ".txt") : "STYLE v1"
prompt = "#{style} Scene: #{scene}"
uri = URI("https://api.openai.com/v1/images/generations")
req = Net::HTTP::Post.new(uri, "Authorization" => "Bearer #{key}", "Content-Type" => "application/json")
req.body = { model: MODEL, prompt: prompt, size: size, quality: quality, n: n, output_format: "png", background: "opaque" }.to_json
res = Net::HTTP.start(uri.host, uri.port, use_ssl: true, read_timeout: 300) { _1.request(req) }
body = JSON.parse(res.body)
abort "OpenAI error #{res.code}: #{body.dig('error', 'message')}" unless res.is_a?(Net::HTTPSuccess)

drafts = File.join(ROOT, "build", "genimg")
FileUtils.mkdir_p(drafts)
paths = body["data"].each_with_index.map do |d, i|
  path = File.join(drafts, "#{fig}-#{i + 1}.png")
  File.binwrite(path, Base64.decode64(d["b64_json"]))
  path
end

# Draft 1 becomes the figure; pick another later with --select N.
out = File.expand_path(opt.("out", File.join(ROOT, "assets", "figures", "#{fig}.png")), ROOT)
finalize(paths.first, out)

FileUtils.mkdir_p(File.join(ROOT, "assets", "credits"))
record = {
  "id" => fig,
  "kind" => "ai_illustration",
  "file" => out.delete_prefix(ROOT + "/"),
  "sha256" => Digest::SHA256.file(out).hexdigest,
  "generation" => {
    "provider" => "openai",
    "endpoint" => "POST /v1/images/generations",
    "model" => MODEL,
    "date" => Time.now.iso8601,
    "style_version" => style_version,
    "scene" => scene,
    "prompt" => prompt,
    "params" => { "size" => size, "quality" => quality, "background" => "opaque", "output_format" => "png", "n" => n },
    "seed" => nil,
    "request_id" => body["data"][0]["generation_id"] || res["x-request-id"],
    "usage" => body["usage"],
    "drafts" => paths.map { _1.delete_prefix(ROOT + "/") },
    "selected" => 1,
  },
  "post_processing" => ["flattened onto #FBF9F4, sRGB, alpha removed"],
  "human_contribution" => "art direction (scene brief), selection, placement and caption",
  "terms" => { "provider_terms" => "https://openai.com/policies/services-agreement/",
               "copyright_status" => "AI-generated; likely not protectable (US Copyright Office Part 2; Lei 9.610 art. 11)" },
  "kdp_disclosure" => "ai_generated_image",
  "credit" => { "caption_pt" => "Ilustração gerada por IA (GPT Image 2.5, OpenAI) sob direção do autor",
                "caption_en" => "AI-generated illustration (GPT Image 2.5, OpenAI) under the author's direction" },
}
File.write(File.join(ROOT, "assets", "credits", "#{fig}.yml"), record.to_yaml)
ph = File.join(ROOT, "assets", "figures", ".placeholders")
File.write(ph, File.readlines(ph, chomp: true).reject { _1 == "#{fig}.png" }.map { "#{_1}\n" }.join) if File.exist?(ph)
warn "#{fig}: #{paths.size} draft(s) in build/genimg/, figure written, usage #{body['usage'].to_json}"
