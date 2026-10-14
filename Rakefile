# frozen_string_literal: true

# Book build. Everything runs from pinned tools in tools/ (see tools/SHA256SUMS).
#   rake tools          fetch + verify + unpack pinned toolchain
#   rake inventory      re-scan the blog (hashes, links)
#   rake drift          what in the book is stale vs the blog (DIFF=1 for diffs)
#   rake check          outline coverage + chapter lint
#   rake diagrams       render assets/diagrams/*.d2 for each language
#   rake build          render PT edition (EPUB, print + ebook PDF, HTML, DOCX) + epubcheck + page audit
#   rake audit          page-level layout audit of the PDFs (scripts/page_audit.rb)
#   rake build BOOK_LANG=en  same for the EN edition
#   rake review DIR=reviews/<version>/<lang>  validate + summarise copyedit findings (scripts/review.rb)
#   rake balance        words per unit and per source post, overlap between units (build/<lang>/balance.md)
#   rake test           regression tests of the tools (test/, isolated fixture book)

require "digest"
require "fileutils"
require "open3"
require "rake/testtask"

ROOT = __dir__
LANG = ENV.fetch("BOOK_LANG", "pt")
TOOLS = File.join(ROOT, "tools")
QUARTO = File.join(TOOLS, "quarto-1.10.19", "bin", "quarto")
EPUBCHECK_JAR = File.join(TOOLS, "epubcheck-5.4.0", "epubcheck.jar")
D2 = File.join(TOOLS, "d2-v0.9.0", "bin", "d2")
DOWNLOADS = {
  "quarto-1.10.19-linux-amd64.tar.gz" => "https://github.com/quarto-dev/quarto-cli/releases/download/v1.10.19/quarto-1.10.19-linux-amd64.tar.gz",
  "epubcheck-5.4.0.zip" => "https://github.com/w3c/epubcheck/releases/download/v5.4.0/epubcheck-5.4.0.zip",
  "d2-v0.9.0-linux-amd64.tar.gz" => "https://github.com/terrastruct/d2/releases/download/v0.9.0/d2-v0.9.0-linux-amd64.tar.gz",
}.freeze

desc "Fetch, verify and unpack the pinned toolchain"
task :tools do
  cache = File.join(TOOLS, "cache")
  FileUtils.mkdir_p(cache)
  sums = File.readlines(File.join(TOOLS, "SHA256SUMS")).to_h { |l| l.split.reverse }
  DOWNLOADS.each do |name, url|
    path = File.join(cache, name)
    sh "curl -sSfL -o #{path} #{url}" unless File.exist?(path)
    actual = Digest::SHA256.file(path).hexdigest
    raise "checksum mismatch for #{name}: #{actual}" unless actual == sums.fetch(name)
  end
  Dir.chdir(TOOLS) do
    sh "tar xzf cache/quarto-1.10.19-linux-amd64.tar.gz" unless File.exist?(QUARTO)
    sh "unzip -qo cache/epubcheck-5.4.0.zip" unless File.exist?(EPUBCHECK_JAR)
    sh "tar xzf cache/d2-v0.9.0-linux-amd64.tar.gz" unless File.exist?(D2)
  end
end

desc "Re-scan the blog: hashes, links"
task :inventory do
  ruby "scripts/inventory.rb"
  ruby "scripts/links.rb"
end

desc "Report chapters/analyses out of sync with the blog"
task drift: :inventory do
  args = ["--lang", LANG]
  args << "--diff" if ENV["DIFF"]
  ruby "scripts/drift.rb", *args
end

desc "Validate outline coverage and lint chapter sources"
task :check do
  ruby "scripts/outline_check.rb"
  generated = %w[glossario.md bibliografia.md fontes.md creditos.md]
  files = Dir[File.join(ROOT, "book", LANG, "*.md")].reject { generated.include?(File.basename(_1)) }
  ruby "scripts/lint_chapter.rb", *files unless files.empty?
  ruby "scripts/en_quote_punct.rb", "--check" if LANG == "en" # EN house style: punctuation inside quotes
  ruby "scripts/doctor.rb", "--lang", LANG
end

desc "Copyedit step 2: validate and summarise findings (DIR=reviews/<version>/<lang>, GREP=regex optional)"
task :review do
  dir = ENV["DIR"] or abort "usage: rake review DIR=reviews/<version>/<lang> [GREP=regex]"
  ruby "scripts/review.rb", "validate", dir
  summary = ["summary", dir]
  summary += ["--grep", ENV["GREP"]] if ENV["GREP"]
  ruby "scripts/review.rb", *summary
end

desc "Integrity check of the sources (scripts/doctor.rb): refs, citations, glossary, figures, provenance, callbacks, parity"
task :doctor do
  ruby "scripts/doctor.rb", "--lang", LANG
end

desc "Copyedit step 1: mechanical style report (repetition, tics, variants) in build/<lang>/style-report.md"
task :style do
  ruby "scripts/style_report.rb", "--lang", LANG
end

desc "Structural balance: words per unit and per source post, overlap, in build/<lang>/balance.md"
task :balance do
  ruby "scripts/balance_report.rb", "--lang", LANG
end

desc "Strict pre-release check: doctor in release mode (placeholders and stale translations are errors)"
task :release_check do
  ruby "scripts/doctor.rb", "--lang", LANG, "--release", "--output"
end

# Each test runs the scripts inside a throwaway fixture repository (see
# test/test_helper.rb); the real book is never touched. No Quarto render.
Rake::TestTask.new(:test) do |t|
  t.description = "Regression tests of the tools (scripts/, filters/) against a fixture book"
  t.libs << "test"
  t.test_files = FileList["test/test_*.rb"].exclude("test/test_helper.rb")
  t.warning = false
end

desc "Render D2 diagrams for the current language"
task diagrams: :tools do
  Dir[File.join(ROOT, "assets", "diagrams", "*.d2")].each do |src|
    ruby "scripts/render_diagram.rb", src, LANG, D2
  end
end

desc "Render matplotlib charts/diagrams (assets/charts/*.py) for the current language"
task :charts do
  Dir[File.join(ROOT, "assets", "charts", "*.py")].sort.each do |py|
    # chart_check.py runs the script and refuses to save if a label spills out
    # of its box or off the canvas (labels change length between languages).
    sh "uv", "run", "--quiet", "--with", "matplotlib", "--with", "numpy", "python", "-I", "scripts/chart_check.py", py, LANG
  end
  # Label overlays on AI art (ImageMagick), same language convention.
  Dir[File.join(ROOT, "assets", "charts", "*.rb")].sort.each { |rb| ruby rb, LANG }
end

desc "Generate the Quarto profile from book/outline.yml"
task :config do
  ruby "scripts/gen_quarto.rb", LANG
end

desc "Merge per-chapter bibliography and glossary proposals"
task :merge do
  ruby "scripts/merge_refs.rb", LANG
  ruby "scripts/merge_glossary.rb", LANG
end

desc "Generate glossary/bibliography/sources pages and figure placeholders"
task :backmatter do
  ruby "scripts/gen_back_matter.rb", LANG
  ruby "scripts/figures.rb", LANG, "--placeholders"
end

desc "Build all formats for LANG (default pt), fit and audit the PDF, validate the EPUB"
task build: %i[tools merge backmatter config] do
  profile = File.join(ROOT, "_quarto-#{LANG}.yml")
  raise "missing profile #{profile}" unless File.exist?(profile) # quarto ignores unknown profiles silently
  # Keep Quarto's output in build/logs/render-<lang>.log (outside the output
  # dir, which Quarto wipes at the start of a render): the doctor's output
  # checks read it for unresolved cross-references, unknown glossary keys and
  # missing citations (Quarto only warns about those).
  log = File.join(ROOT, "build", "logs", "render-#{LANG}.log")
  FileUtils.mkdir_p(File.dirname(log))
  status = Open3.popen2e(QUARTO, "render", "--profile", LANG) do |_in, out, wait|
    File.open(log, "w") { |f| out.each_line { |l| print l; f.write(l) } }
    wait.value
  end
  raise "quarto render failed (see #{log})" unless status.success?
  Rake::Task[:fit].invoke
  Rake::Task[:ebook_pdf].invoke
  Rake::Task[:epubcheck].invoke
  Rake::Task[:audit].invoke
  ruby "scripts/doctor.rb", "--lang", LANG, "--output"
end

# Quarto renders the print PDF (6x9 in, mirrored margins, no cover) and keeps
# the Typst source (keep-typ) as index.typ. The tasks below recompile that
# source with Quarto's bundled typst; build/<lang>/.tighten holds the
# per-chapter tightening (`--input tighten=...`) shared by every compile and
# by the audit, so they all see the same layout.
# Resolved lazily: in a fresh checkout Quarto (which bundles Typst) is only
# unpacked by the tools task, after this file is loaded.
def typst_bin
  Dir[File.join(TOOLS, "quarto-1.10.19", "bin", "tools", "*", "typst")].first or raise "typst not found; run rake tools"
end
TIGHTEN = File.join(ROOT, "build", LANG, ".tighten")

def typst_sources
  typ = File.join(ROOT, "index.typ")
  print_pdf = Dir[File.join(ROOT, "build", LANG, "*.pdf")].reject { _1.end_with?("-ebook.pdf") }.first
  raise "run `rake build` first (missing #{typ} or the print PDF)" unless File.exist?(typ) && print_pdf

  [typ, print_pdf]
end

def typst_compile(typ, pdf, edition)
  tighten = File.exist?(TIGHTEN) ? File.read(TIGHTEN).strip : ""
  sh typst_bin, "compile", "--root", ROOT, "--font-path", File.join(ROOT, "assets", "fonts"), "--pdf-standard", "ua-1",
     "--input", "edition=#{edition}", "--input", "tighten=#{tighten}", typ, pdf
end

# A chapter whose last page holds 1-3 lines (RUNT-END in the audit) is set a
# hair tighter (level 1, then 2: see ak-unit in the template) and the print PDF is
# recompiled, until no runt is left or every runt chapter is at level 3.
desc "Recompile the print PDF, tightening chapters that end in a runt page"
task :fit do
  typ, print_pdf = typst_sources
  levels = {}
  File.write(TIGHTEN, "")
  4.times do
    runts = `#{RbConfig.ruby} #{File.join(ROOT, 'scripts', 'page_audit.rb')} --lang #{LANG} --runts`.strip.split(",")
    grow = runts.reject { levels.fetch(_1, 0) >= 3 }
    break if grow.empty?

    grow.each { levels[_1] = levels.fetch(_1, 0) + 1 }
    File.write(TIGHTEN, levels.map { "#{_1}:#{_2}" }.join(","))
    puts "fit: tightening #{File.read(TIGHTEN)}"
    typst_compile(typ, print_pdf, "print")
  end
end

# The ebook PDF is the same source compiled with `--input edition=ebook`
# (cover page, symmetric margins, no blank pages). See
# _extensions/akita-book/typst-template.typ.
desc "Compile the ebook PDF from the Typst source kept by the last render"
task :ebook_pdf do
  typ, print_pdf = typst_sources
  typst_compile(typ, print_pdf.sub(/\.pdf\z/, "-ebook.pdf"), "ebook")
end

desc "Page-level layout audit of the print and ebook PDFs (STRICT=1 fails on findings)"
task :audit do
  args = ["--lang", LANG]
  args << "--strict" if ENV["STRICT"]
  ruby "scripts/page_audit.rb", *args, "--edition", "print"
  ruby "scripts/page_audit.rb", *args, "--edition", "ebook"
end

desc "Validate built EPUBs with epubcheck"
task :epubcheck do
  Dir[File.join(ROOT, "build", LANG, "*.epub")].each do |epub|
    sh "java", "-jar", EPUBCHECK_JAR, "--failonwarnings", epub
  end
end

task default: %i[check build]
