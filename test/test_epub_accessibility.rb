# frozen_string_literal: true

require_relative "test_helper"

class TestEpubAccessibility < ToolTest
  def test_adds_localized_landmarks_and_preserves_epub_container
    dir = fx.path("epub-src")
    FileUtils.mkdir_p(File.join(dir, "EPUB"))
    fx.write("epub-src/mimetype", "application/epub+zip")
    fx.write("epub-src/EPUB/nav.xhtml", <<~XHTML)
      <html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="pt-BR">
      <body><nav epub:type="toc"><ol>
      <li><a href="text/ch001.xhtml#sec-ch01">Capítulo 1</a></li>
      <li><a href="text/ch002.xhtml#sec-creditos">Créditos</a></li>
      <li><a href="text/ch003.xhtml#sec-glossario">Glossário</a></li>
      <li><a href="text/ch004.xhtml#sec-bibliografia">Referências</a></li>
      </ol></nav><nav epub:type="landmarks" hidden="hidden"><ol>
      <li><a href="title.xhtml" epub:type="titlepage">Título</a></li>
      </ol></nav></body></html>
    XHTML
    epub = fx.path("test.epub")
    Dir.chdir(dir) do
      system("zip", "-X0q", epub, "mimetype", exception: true)
      system("zip", "-Xr9Dq", epub, ".", "-x", "mimetype", exception: true)
    end

    res = fx.run("epub_accessibility", epub)
    assert_exit 0, res
    nav, status = Open3.capture2("unzip", "-p", epub, "EPUB/nav.xhtml")
    assert status.success?
    %w[bodymatter glossary bibliography credits].each { assert_includes nav, %(epub:type="#{_1}") }
    assert_includes nav, "Início do texto"
    first, = Open3.capture2("unzip", "-Z1", epub)
    assert_equal "mimetype", first.lines.first.strip
  end
end
