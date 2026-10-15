# frozen_string_literal: true

require_relative "test_helper"

class TestEpubClean < ToolTest
  def epub_with(body)
    dir = fx.path("kindle-src")
    FileUtils.mkdir_p(File.join(dir, "EPUB"))
    fx.write("kindle-src/mimetype", "application/epub+zip")
    fx.write("kindle-src/EPUB/page.xhtml", body)
    epub = fx.path("kindle.epub")
    Dir.chdir(dir) do
      system("zip", "-X0q", epub, "mimetype", exception: true)
      system("zip", "-Xr9Dq", epub, ".", "-x", "mimetype", exception: true)
    end
    epub
  end

  def test_removes_inline_styles_and_data_uri_icons_for_kindle
    epub = epub_with('<html><head><style>.x{background:url(data:image/png;base64,AAAA);display:flex}</style></head><body><p>Text</p></body></html>')
    res = fx.run("epub_clean", epub)
    assert_exit 0, res
    page, = Open3.capture2("unzip", "-p", epub, "EPUB/page.xhtml")
    refute_includes page, "<style"
    refute_includes page, "data:image"
    assert_includes page, "<p>Text</p>"
  end

  def test_refuses_to_strip_css_if_a_callout_or_layout_uses_it
    epub = epub_with('<html><head><style>.callout{display:flex}</style></head><body><div class="callout">Warning</div></body></html>')
    res = fx.run("epub_clean", epub)
    assert_exit 1, res
    assert_includes res.err, "uses callout/layout classes"
  end
end
