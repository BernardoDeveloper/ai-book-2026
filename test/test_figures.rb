# frozen_string_literal: true

require_relative "test_helper"

# scripts/figures.rb: figure requests (book/<lang>/_figs) vs images referenced
# in the chapters; placeholders so the book builds before the art exists.
class TestFigures < ToolTest
  PENDING = "assets/figures/ch02-pendente.png"

  def add_pending
    fx.edit("book/pt/_figs/ch02.yml") { _1 + "- fig: ch02-pendente\n  kind: diagram\n  idea: um diagrama que falta\n" }
    fx.edit("book/pt/ch02.md") { _1 + "\n![Falta.](#{PENDING}){#fig-ch02-pendente}\n" }
  end

  def magick? = system("magick", "-version", out: File::NULL, err: File::NULL)

  # Guards orphan detection being extension-agnostic: requests carry only the
  # figure id, so ch03-foto requested and referenced as .jpg is not an orphan.
  def test_orphans_extension_agnostic
    res = fx.run("figures")
    assert_exit 0, res
    assert_includes res.out, "3 figures referenced, 0 pending, 1 requested but unused"
    assert_includes res.out, "ORPHAN  ch02-sobra"
    refute_includes res.out, "ORPHAN  ch03-foto"
  end

  # Guards pending detection: a referenced image that doesn't exist is listed
  # with its request's kind; without --placeholders nothing is written.
  def test_pending_listed
    add_pending
    res = fx.run("figures")
    assert_includes res.out, "PENDING #{PENDING} (diagram)"
    refute fx.exist?(PENDING)
    refute fx.exist?("assets/figures/.placeholders")
  end

  # Guards --placeholders: the PNG is created, its name recorded in
  # .placeholders, and it stays pending (the doctor then warns about it).
  def test_placeholders_created_and_listed
    skip "ImageMagick `magick` not available" unless magick?
    add_pending
    res = fx.run("figures", "pt", "--placeholders")
    assert_exit 0, res
    assert fx.exist?(PENDING)
    assert_equal "ch02-pendente.png\n", fx.read("assets/figures/.placeholders")
    again = fx.run("figures")
    assert_includes again.out, "PENDING #{PENDING} (diagram)", "a placeholder is still pending"
    fx.write("assets/credits/ch02-pendente.yml", { "file" => PENDING }.to_yaml)
    assert_includes fx.run("doctor").out, "warn  ch02: image #{PENDING} is still a placeholder"
  end

  # Guards the credits check for final images.
  def test_no_credit_record_warning
    fx.write("assets/figures/ch01-extra.png", Fixture::PNG)
    fx.edit("book/pt/ch01.md") { _1 + "\n![Extra.](assets/figures/ch01-extra.png){#fig-ch01-extra}\n" }
    res = fx.run("figures")
    assert_includes res.err, "NO CREDIT RECORD: assets/figures/ch01-extra.png"
  end
end
