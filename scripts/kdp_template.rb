# frozen_string_literal: true

# Binding and page-count checks shared by the cover task and compositor.
module KdpTemplate
  BINDINGS = { "CASE_LAMINATE" => "hardcover", "PAPERBACK" => "paperback" }.freeze
  module_function

  def metadata(path)
    m = File.basename(path).match(/\A(CASE_LAMINATE|PAPERBACK)_(\d+\.\d+)x(\d+\.\d+)_(\d+)_BW_WHITE_[a-z]{2}_[A-Z]{2}\.png\z/)
    raise ArgumentError, "unsupported KDP template: #{path} (expected BW/WHITE PNG)" unless m

    { binding: BINDINGS.fetch(m[1]), trim: [m[2].to_f, m[3].to_f], pages: m[4].to_i }
  end

  def validate!(path, binding:, pages:, trim: [6.0, 9.0])
    actual = metadata(path)
    expected = { binding:, trim:, pages: }
    raise ArgumentError, "template mismatch: #{actual.inspect}; expected #{expected.inspect}" unless actual == expected

    path
  end

  def select(paths, binding:, pages:, explicit: nil)
    raise ArgumentError, "BINDING must be hardcover or paperback" unless BINDINGS.value?(binding)
    return validate!(explicit, binding:, pages:) if explicit

    found = paths.sort.find do |path|
      metadata(path) == { binding:, trim: [6.0, 9.0], pages: }
    rescue ArgumentError
      false
    end
    found || raise(ArgumentError, "no KDP #{binding} template for #{pages} pages (6x9, BW/WHITE)")
  end

  # Paperback has folds but no hardcover hinge. Keep the compositor's common
  # geometry tuple, with zero hinge width for paperback.
  def guides(binding, blue)
    expected = { "hardcover" => 4, "paperback" => 2 }.fetch(binding)
    raise ArgumentError, "expected #{expected} blue guide lines, found #{blue.size}" unless blue.size == expected
    raise ArgumentError, "unordered or duplicate fold guides" unless blue.each_cons(2).all? { |a, b| a < b }

    binding == "hardcover" ? blue : [blue[0], blue[0], blue[1], blue[1]]
  end
end
