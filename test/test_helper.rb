# frozen_string_literal: true

# Shared fixture for the tool regression tests (`rake test`).
#
# Every script computes ROOT from its own location, so each test runs the
# scripts from a throwaway copy of a tiny, self-consistent book:
#
#   <tmp>/repo   scripts/ + filters/ copied from this checkout, book/outline.yml,
#                book/{pt,en}/*.md, book/back/*, assets/, inventory/
#   <tmp>/blog   a fake akitaonrails-hugo git repository (content/2026/...)
#
# The fixture is built once per process (Fixture.template) and copied for each
# test, so tests can mutate it freely. The real book is never touched.
#
# The base fixture is "clean": lint, outline_check, doctor (pt and en) and
# drift pass on it. Each test makes one change and checks the tool notices.

require "minitest/autorun"
require "fileutils"
require "tmpdir"
require "open3"
require "digest"
require "yaml"
require "rbconfig"

module FixtureData
  REPO_ROOT = File.expand_path("..", __dir__)

  # 1x1 transparent PNG; the tools only check that image files exist.
  PNG = ["89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d4944415478da63f8cfc0f01f0005000201d3a0b5e40000000049454e44ae426082"].pack("H*")

  # Blog posts: id => { pt: [title, body], en: [title, slug, body] }.
  POSTS = {
    "2026/01/15/post-janeiro" => {
      pt: ["Post de janeiro", "Um post de antes do corte.\n"],
    },
    "2026/02/10/primeiro-post" => {
      pt: ["Primeiro post", "O Perceptron prometia demais em 1958.\n\nVeja [o artigo](https://example.com/ai).\n"],
      en: ["First post", "first-post", "The Perceptron promised too much in 1958.\n"],
    },
    "2026/03/05/segundo-post" => {
      pt: ["Segundo post", "O agente esquece tudo entre sessões.\n\nCada conversa começa do zero.\n"],
      en: ["Second post", "second-post", "The agent forgets everything between sessions.\n"],
    },
    "2026/04/01/terceiro-post" => {
      pt: ["Terceiro post", "Traduzi vinte anos de blog.\n"],
      en: ["Third post", "third-post", "I translated twenty years of blog posts.\n"],
    },
    "2019/10/09/episodio-antigo" => {
      pt: ["Episódio antigo", "Anos atrás eu terceirizava decisões demais.\n"],
      en: ["Old episode", "old-episode", "Years ago I outsourced too many decisions.\n"],
    },
    "2026/04/20/post-excluido" => {
      pt: ["Post excluído", "Memória de vídeo limita o modelo.\n"],
      en: ["Excluded post", "excluded-post", "Video memory limits the model.\n"],
    },
  }.freeze

  ANALYSES = %w[2026/01/15/post-janeiro 2026/02/10/primeiro-post 2026/03/05/segundo-post
                2026/04/01/terceiro-post 2026/04/20/post-excluido].freeze

  OUTLINE = <<~YAML
    meta:
      working_title: "Livro de Teste"
      subtitle: "Um subtítulo"
      working_title_en: "Test Book"
      subtitle_en: "A subtitle"
      author: "Autor Teste"
      accessibility_summary: "Texto refluível com descrições de imagens."
      accessibility_summary_en: "Reflowable text with image descriptions."
      owned_names: ["akitaonrails", "Frank"]
      open_source_licenses: {ai-jail: "GPL-3.0"}
      cutoff: "2026-10-13"
      source_from: "2026-02-01"

    front:
      - id: prefacio
        title: "Prefácio"
        kind: original
        sources: [02/10/primeiro-post]

    parts:
      - id: p1
        title: "Parte I: Começo"
        title_en: "Part I: Beginning"
        chapters:
          - id: ch01
            title: "Um gerador de texto"
            sources:
              primary: [02/10/primeiro-post]
          - id: ch02
            title: "A memória de um peixe"
            sources:
              primary: [03/05/segundo-post]
              supporting: [02/10/primeiro-post]
      - id: interlude1
        title: "Interlúdio: Pausa"
        kind: interlude
        sources: [04/01/terceiro-post]
      - id: p2
        title: "Parte II: Meio"
        title_en: "Part II: Middle"
        chapters:
          - id: ch03
            title: "Números e propaganda"
            sources:
              primary: [04/01/terceiro-post]

    back:
      - id: epilogo
        title: "Epílogo"
        kind: original
      - id: apA
        title: "Linha do tempo"
        kind: appendix
      - id: fontes
        title: "Fontes: os artigos originais"
        kind: generated
      - id: creditos
        title: "Créditos das imagens"
        kind: generated
      - id: glossario
        title: "Glossário"
        kind: generated
      - id: bibliografia
        title: "Referências"
        kind: generated

    background_sources:
      - {post: 2019/10/09/episodio-antigo, why: "colors the narrator's history"}

    excluded:
      - {post: 01/15/post-janeiro, reason: "before the cut-off"}
      - {post: 04/20/post-excluido, reason: "superseded; ch03 borrows one explainer", borrowed_by: [ch03]}
  YAML

  # Unit bodies, per language. Front matter is generated (sources/sha256 from
  # the blog, translated_from from the PT file).
  UNITS = {
    "prefacio" => {
      file: "index.md", sources: %w[2026/02/10/primeiro-post],
      pt: ["Prefácio", <<~MD],
        # Prefácio {#sec-prefacio .unnumbered}

        <!-- src: 2026/02/10/primeiro-post -->
        Este livro começou num blog. Cada capítulo conta um pedaço do ano.

        <!-- src: original -->
        A ordem dos capítulos segue o calendário.
      MD
      en: ["Preface", <<~MD],
        # Preface {#sec-prefacio .unnumbered}

        <!-- src: 2026/02/10/primeiro-post -->
        This book started on a blog. Each chapter tells a piece of the year.

        <!-- src: original -->
        The chapters follow the calendar.
      MD
    },
    "ch01" => {
      file: "ch01.md", sources: %w[2026/02/10/primeiro-post],
      pt: ["Um gerador de texto", <<~MD],
        # Um gerador de texto {#sec-ch01}

        <!-- src: 2026/02/10/primeiro-post -->
        Um [LLM]{.gls} calcula a próxima palavra. Os [modelos grandes]{.gls key=llm} fazem isso em escala [@smith2026ai].

        <!-- src: 2026/02/10/primeiro-post -->
        O Perceptron de 1958 já prometia demais, como mostra a @fig-ch01-arte.

        ![Uma máquina antiga.](assets/figures/ch01-arte.png){#fig-ch01-arte fig-alt="Máquina antiga." fig-desc="Uma máquina antiga ocupando uma sala."}

        <!-- src: original -->
        A memória fica para @sec-ch02.
      MD
      en: ["A Text Generator", <<~MD],
        # A Text Generator {#sec-ch01}

        <!-- src: 2026/02/10/primeiro-post -->
        An [LLM]{.gls} computes the next word. The [large models]{.gls key=llm} do it at scale [@smith2026ai].

        <!-- src: 2026/02/10/primeiro-post -->
        The 1958 Perceptron already promised too much, as @fig-ch01-arte shows.

        ![An old machine.](assets/figures/en/ch01-arte.png){#fig-ch01-arte fig-alt="Old machine." fig-desc="An old machine occupying a room."}

        <!-- src: original -->
        Memory is for @sec-ch02.
      MD
    },
    "ch02" => {
      file: "ch02.md", sources: %w[2026/03/05/segundo-post 2026/02/10/primeiro-post],
      pt: ["A memória de um peixe", <<~MD],
        # A memória de um peixe {#sec-ch02}

        <!-- src: 2026/03/05/segundo-post -->
        O agente esquece tudo entre uma sessão e outra. Cada conversa começa do zero, com [tokens]{.gls key=token} novos [@doe2026].

        <!-- src: 2026/02/10/primeiro-post -->
        Como contei em @sec-ch01, o Perceptron já prometia demais.

        ![Diagrama da memória.](assets/figures/ch02-diagrama.png){#fig-ch02-diagrama fig-alt="Diagrama da memória." fig-desc="Blocos mostram a memória entrando e saindo do contexto."}
      MD
      en: ["A Goldfish Memory", <<~MD],
        # A Goldfish Memory {#sec-ch02}

        <!-- src: 2026/03/05/segundo-post -->
        The agent forgets everything between sessions. Each conversation starts from scratch, with new [tokens]{.gls key=token} [@doe2026].

        <!-- src: 2026/02/10/primeiro-post -->
        As I told in @sec-ch01, the Perceptron already promised too much.

        ![Memory diagram.](assets/figures/ch02-diagrama.png){#fig-ch02-diagrama fig-alt="Memory diagram." fig-desc="Blocks show memory entering and leaving the context."}
      MD
    },
    "interlude1" => {
      file: "interlude1.md", sources: %w[2026/04/01/terceiro-post],
      pt: ["Interlúdio: Pausa", <<~MD],
        # Interlúdio: Pausa {#sec-interlude1 .unnumbered}

        <!-- src: 2026/04/01/terceiro-post -->
        Traduzi vinte anos de blog num fim de semana.
      MD
      en: ["Interlude: A Pause", <<~MD],
        # Interlude: A Pause {#sec-interlude1 .unnumbered}

        <!-- src: 2026/04/01/terceiro-post -->
        I translated twenty years of blog posts in a weekend.
      MD
    },
    "ch03" => {
      file: "ch03.md", sources: %w[2026/04/01/terceiro-post 2026/04/20/post-excluido],
      pt: ["Números e propaganda", <<~MD],
        # Números e propaganda {#sec-ch03}

        <!-- src: 2026/04/01/terceiro-post -->
        Um teste de modelos leva dias. A @fig-ch03-foto mostra uma sala de máquinas.

        ![Uma sala de máquinas.](assets/figures/ch03-foto.jpg){#fig-ch03-foto fig-alt="Sala de máquinas." fig-desc="Fileiras de computadores ocupam uma sala de máquinas."}

        <!-- src: 2026/04/20/post-excluido -->
        A memória de vídeo limita o tamanho do modelo [@doe2026].
      MD
      en: ["Numbers and Hype", <<~MD],
        # Numbers and Hype {#sec-ch03}

        <!-- src: 2026/04/01/terceiro-post -->
        A model test takes days. @fig-ch03-foto shows a machine room.

        ![A machine room.](assets/figures/ch03-foto.jpg){#fig-ch03-foto fig-alt="Machine room." fig-desc="Rows of computers occupy a machine room."}

        <!-- src: 2026/04/20/post-excluido -->
        Video memory limits the size of the model [@doe2026].
      MD
    },
    "epilogo" => {
      file: "epilogo.md", sources: [],
      pt: ["Epílogo", <<~MD],
        # Epílogo {#sec-epilogo .unnumbered}

        <!-- src: original -->
        Teste as ferramentas você mesmo, como em @sec-ch03.
      MD
      en: ["Epilogue", <<~MD],
        # Epilogue {#sec-epilogo .unnumbered}

        <!-- src: original -->
        Test the tools yourself, as in @sec-ch03.
      MD
    },
    "apA" => {
      file: "apA.md", sources: [],
      pt: ["Linha do tempo", <<~MD],
        # Linha do tempo {#sec-apA}

        <!-- src: original -->
        - 2017: o transformer.
        - 2026: este livro.
      MD
      en: ["Timeline", <<~MD],
        # Timeline {#sec-apA}

        <!-- src: original -->
        - 2017: the transformer.
        - 2026: this book.
      MD
    },
  }.freeze

  REFERENCES = [
    { "id" => "doe2026", "type" => "webpage", "title" => "Doe on agents", "URL" => "https://example.org/doe",
      "note" => "cited-by: 2026/03/05/segundo-post, Arquivado em: https://web.archive.org/web/2026/example.org/doe" },
    { "id" => "smith2026ai", "type" => "webpage", "title" => "Smith on AI", "URL" => "https://example.com/ai",
      "note" => "cited-by: 2026/02/10/primeiro-post" },
  ].freeze

  GLOSSARY_PT = <<~YAML
    # Glossário de teste. Cabeçalho preservado pelo merge.
    agente:
      term: Agente
      def: Um modelo com ferramentas.
    llm:
      term: LLM
      long: Large Language Model
      def: Modelo de linguagem de grande porte.
    token:
      term: Token
      def: Pedaço de texto.
  YAML

  GLOSSARY_EN = <<~YAML
    # Test glossary.
    agente:
      term: Agent
      def: A model with tools.
    llm:
      term: LLM
      long: Large Language Model
      def: A large language model.
    token:
      term: Token
      def: A piece of text.
  YAML

  CREDITS = {
    "ch01-arte" => { "id" => "ch01-arte", "kind" => "ai_illustration", "file" => "assets/figures/ch01-arte.png",
                     "notes" => "idea from 2026/02/10/primeiro-post",
                     "generation" => { "model" => "gpt-image-test", "date" => "2026-10-01T10:00:00-03:00" } },
    "ch02-diagrama" => { "id" => "ch02-diagrama", "kind" => "chart_code", "file" => "assets/figures/ch02-diagrama.png" },
    "ch03-foto" => { "id" => "ch03-foto", "kind" => "photo", "file" => "assets/figures/ch03-foto.jpg",
                     "source" => { "title" => "Sala de máquinas", "page_url" => "https://commons.wikimedia.org/wiki/File:Sala.jpg" },
                     "author" => "Fulano de Tal",
                     "license" => { "short" => "CC BY-SA 4.0", "url" => "https://creativecommons.org/licenses/by-sa/4.0" },
                     "modifications" => ["redimensionada", "em tons de cinza"],
                     "credit" => { "backmatter" => "\"Sala de máquinas\", Fulano de Tal. CC BY-SA 4.0. Modificações: redimensionada." } },
    "cover-d" => { "id" => "cover-d", "kind" => "ai_illustration", "file" => "assets/cover/cover-d.png",
                   "generation" => { "model" => "gpt-image-cover", "date" => "2026-10-02T10:00:00-03:00" } },
  }.freeze

  FIGS = {
    "ch01" => [{ "fig" => "ch01-arte", "kind" => "concept-art", "idea" => "uma máquina antiga" }],
    "ch02" => [{ "fig" => "ch02-diagrama", "kind" => "diagram", "idea" => "memória" },
               { "fig" => "ch02-sobra", "kind" => "diagram", "idea" => "nunca usada" }],
    "ch03" => [{ "fig" => "ch03-foto", "kind" => "photo", "idea" => "sala de máquinas" }],
  }.freeze

  LINEAGE = <<~YAML
    series:
      test:
        members:
          - {post: 02/10/primeiro-post, era: v1, status: current-lesson}
  YAML
end

# Builds and copies fixture repositories, runs scripts inside them.
class Fixture
  include FixtureData

  GIT_ID = %w[-c user.name=Fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false
              -c init.defaultBranch=main -c core.hooksPath=/dev/null].freeze

  Result = Struct.new(:out, :err, :status) do
    def code = status.exitstatus
    def ok? = status.success?
    def all = out + err
  end

  class << self
    # Built once per process and removed at exit.
    def template
      @template ||= begin
        dir = Dir.mktmpdir("book-fixture-template")
        Minitest.after_run { FileUtils.rm_rf(dir) }
        new(dir, build: true)
      end
    end

    def copy
      dir = Dir.mktmpdir("book-fixture")
      FileUtils.cp_r(File.join(template.base, "."), dir)
      fx = new(dir)
      posts = fx.path("inventory/posts.yml")
      File.write(posts, File.read(posts).gsub(template.base, dir))
      fx
    end

    def git(dir, *args)
      out, status = Open3.capture2e("git", *GIT_ID, "-C", dir, *args)
      raise "git #{args.join(' ')} failed in #{dir}:\n#{out}" unless status.success?

      out
    end

    def sha(path) = Digest::SHA256.file(path).hexdigest
  end

  attr_reader :base, :root, :blog

  def initialize(base, build: false)
    @base = base
    @root = File.join(base, "repo")
    @blog = File.join(base, "blog")
    build! if build
  end

  def cleanup = FileUtils.rm_rf(base)

  def path(rel) = File.join(root, rel)
  def read(rel) = File.read(path(rel))
  def exist?(rel) = File.exist?(path(rel))

  def write(rel, content)
    FileUtils.mkdir_p(File.dirname(path(rel)))
    File.write(path(rel), content)
  end

  def edit(rel)
    write(rel, yield(read(rel)))
  end

  def sha(rel) = self.class.sha(path(rel))
  def yaml(rel) = YAML.load_file(path(rel), permitted_classes: [Date, Time])

  # Runs scripts/<name>.rb (or any path relative to the fixture) with the
  # fixture's ruby, from the fixture root, without inheriting BOOK_LANG/PARTIAL.
  def run(script, *args, env: {})
    file = script.include?("/") ? path(script) : path("scripts/#{script}.rb")
    full_env = { "BOOK_LANG" => nil, "PARTIAL" => nil }.merge(env)
    out, err, status = Open3.capture3(full_env, RbConfig.ruby, file, *args.map(&:to_s), chdir: root)
    Result.new(out, err, status)
  end

  # ---- blog ------------------------------------------------------------------

  def blog_git(*args) = self.class.git(blog, *args)
  def blog_head = blog_git("rev-parse", "HEAD").strip

  def post_path(id, lang = "pt")
    File.join(blog, "content", id, lang == "en" ? "index.en.md" : "index.md")
  end

  def write_post(id, lang, title, body, slug: nil)
    file = post_path(id, lang)
    FileUtils.mkdir_p(File.dirname(file))
    date = id[0, 10].tr("/", "-")
    File.write(file, <<~MD)
      ---
      title: "#{title}"
      date: '#{date}T10:00:00-03:00'
      slug: #{slug || File.basename(id)}
      description: "#{title}."
      tags: [ia]
      ---

      #{body}
    MD
  end

  # Changes a post and commits it in the fake blog.
  def edit_post(id, lang = "pt", message: "edit #{id}")
    file = post_path(id, lang)
    File.write(file, yield(File.read(file)))
    blog_git("add", "-A")
    blog_git("commit", "-q", "-m", message)
  end

  def inventory!
    res = run("inventory", "--blog", blog)
    raise "inventory failed: #{res.all}" unless res.ok?

    res
  end

  # ---- the book as its own git repository (drift --diff for translations,
  # public_guard) --------------------------------------------------------------

  def book_git(*args) = self.class.git(root, *args)

  def init_book_git!
    write(".gitignore", "/private/\n/build/\n")
    book_git("init", "-q")
    book_git("add", "-A")
    book_git("commit", "-q", "-m", "fixture book")
  end

  # ---- unit helpers -------------------------------------------------------------

  def unit_rel(id, lang = "pt") = "book/#{lang}/#{id == 'prefacio' ? 'index.md' : "#{id}.md"}"

  # Front matter + body of a unit, as the drafters write it.
  def unit_text(id, lang, sources:, chapter:, body:, commit:, translated_from: nil)
    src_lines = sources.map do |post|
      %(  - {post: #{post}, sha256: "#{self.class.sha(post_path(post, lang))}"})
    end
    fm = ["---", "id: #{id}", %(chapter: "#{chapter}")]
    fm << (src_lines.empty? ? "sources: []" : "sources:")
    fm.concat(src_lines)
    fm << "refs_projects: []" << %(blog_commit: "#{commit}")
    fm << %(translated_from: {file: #{translated_from}, sha256: "#{sha(translated_from)}"}) if translated_from
    fm << "---"
    "#{fm.join("\n")}\n\n#{body}"
  end

  private

  def build!
    build_blog!
    FileUtils.mkdir_p(root)
    FileUtils.cp_r(File.join(REPO_ROOT, "scripts"), root)
    FileUtils.cp_r(File.join(REPO_ROOT, "filters"), root)
    write("book/outline.yml", OUTLINE)
    write("inventory/lineage.yml", LINEAGE)
    inventory!
    ANALYSES.each do |id|
      write("inventory/analysis/#{id.gsub('/', '__')}.yml", <<~YAML)
        id: "#{id}"
        source_sha256: "#{self.class.sha(post_path(id))}"
        ai_relevance: core
        summary: "Fixture analysis."
      YAML
    end
    write("book/back/references.yaml", { "references" => REFERENCES.map(&:dup) }.to_yaml)
    write("book/back/glossary-pt.yml", GLOSSARY_PT)
    write("book/back/glossary-en.yml", GLOSSARY_EN)
    CREDITS.each { |name, rec| write("assets/credits/#{name}.yml", rec.to_yaml) }
    %w[assets/figures/ch01-arte.png assets/figures/en/ch01-arte.png assets/figures/ch02-diagrama.png
       assets/figures/ch03-foto.jpg assets/cover/cover-d.png].each { write(_1, PNG) }
    FIGS.each { |ch, reqs| write("book/pt/_figs/#{ch}.yml", reqs.to_yaml) }
    commit = blog_head
    %w[pt en].each do |lang|
      UNITS.each do |id, u|
        chapter, body = u.fetch(lang.to_sym)
        write(unit_rel(id, lang), unit_text(id, lang, sources: u[:sources], chapter: chapter, body: body, commit: commit,
                                                      translated_from: lang == "en" ? unit_rel(id, "pt") : nil))
      end
    end
  end

  def build_blog!
    FileUtils.mkdir_p(blog)
    POSTS.each do |id, langs|
      write_post(id, "pt", *langs[:pt])
      next unless langs[:en]

      title, slug, body = langs[:en]
      write_post(id, "en", title, body, slug: slug)
    end
    blog_git("init", "-q")
    blog_git("add", "-A")
    blog_git("commit", "-q", "-m", "posts")
  end
end

# Base class: a fresh fixture copy per test.
class ToolTest < Minitest::Test
  def setup
    @fx = Fixture.copy
  end

  def teardown
    @fx&.cleanup
  end

  attr_reader :fx

  def assert_exit(code, res, msg = nil)
    assert_equal code, res.code, msg || "expected exit #{code}, got #{res.code}\n--- stdout\n#{res.out}\n--- stderr\n#{res.err}"
  end
end
