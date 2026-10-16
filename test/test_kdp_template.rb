# frozen_string_literal: true

require "minitest/autorun"
require_relative "../scripts/kdp_template"

class TestKdpTemplate < Minitest::Test
  HC = "CASE_LAMINATE_6.000x9.000_531_BW_WHITE_en_US.png"
  PB = "PAPERBACK_6.000x9.000_531_BW_WHITE_en_US.png"
  EN = "CASE_LAMINATE_6.000x9.000_517_BW_WHITE_en_US.png"

  # Same page count must never select the other binding's different spine.
  def test_selects_binding_and_pages
    paths = [PB, EN, HC]
    assert_equal HC, KdpTemplate.select(paths, binding: "hardcover", pages: 531)
    assert_equal PB, KdpTemplate.select(paths, binding: "paperback", pages: 531)
    assert_equal EN, KdpTemplate.select(paths, binding: "hardcover", pages: 517)
    assert_raises(ArgumentError) { KdpTemplate.select(paths, binding: "paperback", pages: 517) }
    assert_raises(ArgumentError) { KdpTemplate.select(paths, binding: "unknown", pages: 531) }
  end

  def test_explicit_template_cannot_bypass_checks
    assert_equal PB, KdpTemplate.select([], binding: "paperback", pages: 531, explicit: PB)
    [HC, EN, PB.sub("6.000", "5.000"), PB.sub("WHITE", "CREAM")].each do |wrong|
      assert_raises(ArgumentError) { KdpTemplate.select([], binding: "paperback", pages: 531, explicit: wrong) }
    end
  end

  def test_missing_or_unsupported_templates_fail
    assert_raises(ArgumentError) { KdpTemplate.select(["unknown.png"], binding: "hardcover", pages: 531) }
    assert_raises(ArgumentError) { KdpTemplate.metadata("unknown.png") }
  end

  def test_template_ui_locale_is_not_the_book_language
    assert_equal KdpTemplate.metadata(HC), KdpTemplate.metadata(HC.sub("en_US", "pt_BR"))
  end

  def test_paperback_has_no_hinges
    assert_equal [100, 100, 800, 800], KdpTemplate.guides("paperback", [100, 800])
    assert_equal [50, 100, 800, 850], KdpTemplate.guides("hardcover", [50, 100, 800, 850])
    assert_raises(ArgumentError) { KdpTemplate.guides("paperback", [50, 100, 800, 850]) }
    assert_raises(ArgumentError) { KdpTemplate.guides("hardcover", [100, 800]) }
    assert_raises(ArgumentError) { KdpTemplate.guides("paperback", [800, 100]) }
  end
end
