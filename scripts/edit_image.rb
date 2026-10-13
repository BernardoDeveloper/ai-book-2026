#!/usr/bin/env ruby
# frozen_string_literal: true

# Edits an existing image with the pinned OpenAI image model (POST
# /v1/images/edits), optionally guided by reference images, and records the
# edit on top of the source image's provenance.
#   build/genimg/<id>-<n>.png       every draft
#   <out>                           draft 1, flattened (pick another with --select)
#   assets/credits/<id>.yml         source record + this edit (prompt, refs, request id)
#
# Usage: scripts/edit_image.rb <id> SOURCE.png "<instruction>" --out PATH
#          [--ref REF.png]... [--size 1024x1536] [--quality high] [--n 2]
#        scripts/edit_image.rb <id> --select N
# The key is read from OPENAI_API_KEY or ~/.config/zsh/secrets; never printed.

require "json"
require "net/http"
require "uri"
require "yaml"
require "base64"
require "digest"
require "fileutils"
require "securerandom"
require "time"

ROOT = File.expand_path("..", __dir__)
MODEL = "gpt-image-2.5-flare-2026-09-08"

def finalize(src, out)
  FileUtils.mkdir_p(File.dirname(out))
  system("magick", src, "-background", "#FBF9F4", "-alpha", "remove", "-alpha", "off", "-colorspace", "sRGB", out, exception: true)
end

id = ARGV[0]
abort "usage: see header" unless id
credits = File.join(ROOT, "assets", "credits", "#{id}.yml")

if ARGV[1] == "--select"
  rec = YAML.load_file(credits)
  edit = rec["edits"].last
  src = File.join(ROOT, edit["drafts"].fetch(ARGV[2].to_i - 1))
  finalize(src, File.join(ROOT, rec["file"]))
  edit["selected"] = ARGV[2].to_i
  rec["sha256"] = Digest::SHA256.file(File.join(ROOT, rec["file"])).hexdigest
  File.write(credits, rec.to_yaml)
  warn "#{id}: selected edit draft #{ARGV[2]}"
  exit
end

source, instruction = ARGV[1], ARGV[2]
abort "usage: see header" unless source && instruction
opt = ->(name, default) { (i = ARGV.index("--#{name}")) ? ARGV[i + 1] : default }
refs = ARGV.each_index.select { ARGV[_1] == "--ref" }.map { ARGV[_1 + 1] }
out = File.expand_path(opt.("out", nil) || abort("--out required"), ROOT)
size = opt.("size", "1024x1536")
quality = opt.("quality", "high")
n = opt.("n", "2")

key = ENV["OPENAI_API_KEY"] || File.read(File.expand_path("~/.config/zsh/secrets"))[/^export OPENAI_API_KEY=["']?([^"'\s]+)/, 1]
abort "OPENAI_API_KEY not found" unless key

# multipart/form-data by hand (Net::HTTP has no builder that handles repeated image[] parts)
boundary = "----akita#{SecureRandom.hex(12)}"
field = ->(name, value) { "--#{boundary}\r\nContent-Disposition: form-data; name=\"#{name}\"\r\n\r\n#{value}\r\n" }
file = lambda do |path|
  "--#{boundary}\r\nContent-Disposition: form-data; name=\"image[]\"; filename=\"#{File.basename(path)}\"\r\n" \
    "Content-Type: image/png\r\n\r\n#{File.binread(path)}\r\n"
end
pngs = [source, *refs].map do |p|
  next p if p.end_with?(".png")

  conv = File.join(ROOT, "build", "genimg", "#{File.basename(p, '.*')}-ref.png")
  FileUtils.mkdir_p(File.dirname(conv))
  system("magick", p, conv, exception: true)
  conv
end
body = +""
body << field.("model", MODEL) << field.("prompt", instruction) << field.("size", size)
body << field.("quality", quality) << field.("n", n) << field.("output_format", "png")
pngs.each { body << file.(_1) }
body << "--#{boundary}--\r\n"

uri = URI("https://api.openai.com/v1/images/edits")
req = Net::HTTP::Post.new(uri, "Authorization" => "Bearer #{key}", "Content-Type" => "multipart/form-data; boundary=#{boundary}")
req.body = body.b
res = Net::HTTP.start(uri.host, uri.port, use_ssl: true, read_timeout: 600) { _1.request(req) }
data = JSON.parse(res.body)
abort "OpenAI error #{res.code}: #{data.dig('error', 'message')}" unless res.is_a?(Net::HTTPSuccess)

FileUtils.mkdir_p(File.join(ROOT, "build", "genimg"))
paths = data["data"].each_with_index.map do |d, i|
  path = File.join(ROOT, "build", "genimg", "#{id}-edit-#{i + 1}.png")
  File.binwrite(path, Base64.decode64(d["b64_json"]))
  path
end
finalize(paths.first, out)

rec = File.exist?(credits) ? YAML.load_file(credits) : { "id" => id, "kind" => "ai_illustration", "kdp_disclosure" => "ai_generated_image" }
rec["file"] = out.delete_prefix(ROOT + "/")
rec["sha256"] = Digest::SHA256.file(out).hexdigest
(rec["edits"] ||= []) << {
  "endpoint" => "POST /v1/images/edits", "model" => MODEL, "date" => Time.now.iso8601,
  "source" => source.delete_prefix(ROOT + "/"), "references" => refs, "instruction" => instruction,
  "params" => { "size" => size, "quality" => quality, "n" => n.to_i },
  "request_id" => data["data"][0]["generation_id"] || res["x-request-id"], "usage" => data["usage"],
  "drafts" => paths.map { _1.delete_prefix(ROOT + "/") }, "selected" => 1
}
File.write(credits, rec.to_yaml)
warn "#{id}: #{paths.size} edit draft(s), usage #{data['usage'].to_json}"
