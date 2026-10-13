#!/usr/bin/env ruby
# frozen_string_literal: true

# Fetches one Wikimedia Commons file plus its licence metadata and writes
#   assets/figures/<fig>.jpg        (original, re-encoded only if not JPEG/PNG)
#   assets/credits/<fig>.yml        provenance + attribution (docs/research/IMAGES.md §6)
#
# Usage: scripts/commons_fetch.rb <fig-id> "File:Some name.jpg" [--crop] [--placement interior|cover]
#        scripts/commons_fetch.rb --search "Linus Torvalds"     (list candidate files)
#
# Refuses non-free licences and files carrying a personality restriction when
# --placement cover is requested. Credits the Artist field, never the uploader.

require "json"
require "net/http"
require "uri"
require "yaml"
require "digest"
require "fileutils"
require "date"
require "cgi"

ROOT = File.expand_path("..", __dir__)
UA = "ai-book-2026/1.0 (https://www.akitaonrails.com/)" # Wikimedia UA policy: tool name + contact URL; a vague UA gets HTTP 429
API = URI("https://commons.wikimedia.org/w/api.php")
FREE = /\A(CC BY(-SA)? [1-4]\.0( [A-Z]{2,})?|CC0( 1\.0)?|Public domain|PD.*)\z/i

# Wikimedia rate-limits bursts (429) and parallel agents share one IP:
# back off, honouring Retry-After, before giving up.
def get(uri, attempts: 6)
  attempts.times do |i|
    res = Net::HTTP.start(uri.host, uri.port, use_ssl: true) do |h|
      h.request(Net::HTTP::Get.new(uri, "User-Agent" => UA))
    end
    return res.body if res.is_a?(Net::HTTPSuccess)
    raise "HTTP #{res.code} for #{uri}" unless %w[429 503].include?(res.code) && i < attempts - 1

    wait = [res["Retry-After"].to_i, 5 * 2**i].max
    warn "HTTP #{res.code}, retrying in #{wait}s"
    sleep wait
  end
end

def api(params)
  uri = API.dup
  uri.query = URI.encode_www_form(params.merge(format: "json", formatversion: 2))
  JSON.parse(get(uri))
end

def strip_html(s) = CGI.unescapeHTML(s.to_s.gsub(/<[^>]+>/, "")).strip

if ARGV[0] == "--search"
  r = api(action: "query", generator: "search", gsrsearch: ARGV[1], gsrnamespace: 6, gsrlimit: 12,
          prop: "imageinfo", iiprop: "size|extmetadata", iiextmetadatafilter: "LicenseShortName|Artist|Restrictions")
  Array(r.dig("query", "pages")).each do |p|
    ii = p["imageinfo"][0]
    em = ii["extmetadata"]
    puts format("%-70s %5dx%-5d %-14s %s %s", p["title"][0, 70], ii["width"], ii["height"],
                em.dig("LicenseShortName", "value"), strip_html(em.dig("Artist", "value"))[0, 30],
                em.dig("Restrictions", "value").to_s.empty? ? "" : "[#{em.dig('Restrictions', 'value')}]")
  end
  exit
end

fig, title = ARGV[0], ARGV[1]
abort "usage: commons_fetch.rb FIG-ID 'File:...'" unless fig && title&.start_with?("File:")
placement = ARGV[ARGV.index("--placement") + 1] if ARGV.include?("--placement")
placement ||= "interior"

r = api(action: "query", titles: title, prop: "imageinfo",
        iiprop: "url|size|mime|sha1|extmetadata|user|timestamp",
        iiextmetadatafilter: "Artist|Credit|LicenseShortName|LicenseUrl|AttributionRequired|Restrictions|DateTimeOriginal|ImageDescription|ObjectName")
page = r.dig("query", "pages", 0)
ii = page&.dig("imageinfo", 0) or abort "not found: #{title}"
em = ii["extmetadata"].transform_values { _1["value"] }
license = em["LicenseShortName"].to_s
abort "refusing non-free licence: #{license.inspect}" unless license.match?(FREE)
restrictions = em["Restrictions"].to_s.split("|").reject(&:empty?)
abort "personality restriction: not allowed on the cover" if placement == "cover" && restrictions.include?("personality")

svg = ii["mime"] == "image/svg+xml"
ext = ii["mime"] == "image/png" || svg ? "png" : "jpg"
FileUtils.mkdir_p(File.join(ROOT, "assets", "figures"))
FileUtils.mkdir_p(File.join(ROOT, "assets", "credits"))
file = "assets/figures/#{fig}.#{ext}"
original = ii["url"].sub(/\?.*/, "")
body = get(URI(original))
actual_sha1 = Digest::SHA1.hexdigest(body)
abort "sha1 mismatch for #{original}" unless actual_sha1 == ii["sha1"]
tmp = File.join(ROOT, "build", "photo-#{fig}.orig#{svg ? '.svg' : ''}")
FileUtils.mkdir_p(File.dirname(tmp))
File.binwrite(tmp, body)
# Kindle wants sRGB without alpha; cap the long side at 3000 px (enough for 300 DPI at 10 in).
# Vector originals are rasterized at print density instead of their nominal size.
density = svg ? ["-density", "600", "-background", "#FBF9F4"] : []
system("magick", *density, tmp, "-auto-orient", "-colorspace", "sRGB", "-alpha", "remove", "-resize", "3000x3000>",
       File.join(ROOT, file), exception: true)
File.delete(tmp)

author = strip_html(em["Artist"])
short = license.sub(/\APublic domain\z/i, "domínio público")
pd = license.match?(/public domain|\APD|CC0/i)
mods = [svg ? "convertida de SVG para PNG" : "redimensionada"]
kind_pt = svg ? "Imagem" : "Foto"
record = {
  "id" => fig,
  "kind" => "photo",
  "file" => file,
  "sha256" => Digest::SHA256.file(File.join(ROOT, file)).hexdigest,
  "pixels" => { "width" => ii["width"], "height" => ii["height"] },
  "source" => {
    "repository" => "wikimedia_commons",
    "page_url" => ii["descriptionurl"],
    "original_url" => original,
    "original_sha1" => ii["sha1"],
    "retrieved" => Date.today.iso8601,
    "title" => page["title"].delete_prefix("File:").sub(/\.\w+\z/, ""),
    "date_taken" => strip_html(em["DateTimeOriginal"]),
    "description" => strip_html(em["ImageDescription"])[0, 300],
  },
  "author" => author,
  "uploader" => ii["user"],
  "license" => { "short" => license, "url" => em["LicenseUrl"], "attribution_required" => em["AttributionRequired"] == "true",
                 "share_alike" => license.include?("SA"), "restrictions" => restrictions },
  "modifications" => mods,
  "adaptation" => false,
  "placement" => placement,
  "personality_rights_check" => "public figure, editorial context, #{placement} only",
  "kdp_disclosure" => "none",
  "credit" => {
    "caption_pt" => pd ? "#{kind_pt}: #{author} / domínio público" : "#{kind_pt}: #{author} / Wikimedia Commons, #{short}",
    "backmatter" => %("#{page['title'].delete_prefix('File:')}", #{author}. #{ii['descriptionurl']}. #{pd ? 'Domínio público.' : "Licença #{license}, #{em['LicenseUrl']}."} Modificações: #{mods.join(', ')}.),
  },
}
File.write(File.join(ROOT, "assets", "credits", "#{fig}.yml"), record.to_yaml)
ph = File.join(ROOT, "assets", "figures", ".placeholders")
File.write(ph, File.readlines(ph, chomp: true).reject { _1.start_with?("#{fig}.") }.map { "#{_1}\n" }.join) if File.exist?(ph)
warn "#{file}: #{author}, #{license}#{restrictions.empty? ? '' : " [#{restrictions.join(',')}]"}"
puts record["credit"]["caption_pt"]
