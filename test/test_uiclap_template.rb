# frozen_string_literal: true

require "minitest/autorun"
require "tempfile"
require_relative "../scripts/uiclap_template"

class TestUiclapTemplate < Minitest::Test
  def test_geometry_matches_printed_values_not_schematic_pixels
    g = UiclapTemplate.geometry
    assert_equal [8409, 5646], g[:canvas]
    assert_equal 3874, g[:folds].first
    assert_equal 661, g[:folds].last - g[:folds].first
    assert_equal 3874, g[:canvas].first - g[:folds].last
    assert_equal 600, UiclapTemplate::DPI
    x, y, width, height = g[:barcode]
    assert_equal 1654, width # 70 mm at 600 dpi
    assert_equal 1181, height # 50 mm at 600 dpi
    assert_equal 236, g[:folds].first - x - width # 10 mm from spine fold
    assert_equal 354, g[:canvas].last - y - height # 10 mm + 5 mm bleed
    %i[back spine front].each do |part|
      left, right = g.fetch(part)
      assert_operator left, :<, right
      assert_operator left, :>, 0
      assert_operator right, :<, g[:canvas].first
    end
  end

  def test_stale_template_and_page_count_are_rejected
    template = File.expand_path("../assets/cover/uiclap-medidas-capa.jpg", __dir__)
    UiclapTemplate.validate!(template, 547)
    assert_raises(RuntimeError) { UiclapTemplate.validate!(template, 531) }
    Tempfile.create do |f|
      f.write("different template")
      f.flush
      assert_raises(RuntimeError) { UiclapTemplate.validate!(f.path, 547) }
    end
  end
end
