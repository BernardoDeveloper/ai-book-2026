# frozen_string_literal: true

require "digest"

# Measurements transcribed from the author's portal-generated JPG, not its
# schematic drawing (which is not to scale). Refresh after page/paper changes.
module UiclapTemplate
  SHA256 = "bd9dc0d506f2388d5b76e111ce9d2fed3671c004138e8d0dbc054f6684077781"
  PAGES = 547
  DPI = 600

  def self.validate!(template, pages)
    raise "UICLAP template is for #{PAGES} pages; obtain a new template" unless pages == PAGES
    raise "UICLAP template changed; review its measurements" unless Digest::SHA256.file(template).hexdigest == SHA256
  end

  def self.geometry
    # Panels: 3874 px each INCLUDING 5 mm outer bleed; spine: 661 px.
    # 10 mm live-area inset from trim, and 3 mm from each spine fold.
    { canvas: [8409, 5646], folds: [3874, 4535], hinges: [3874, 4535],
      trim: 118, live_y: [354, 5292], back: [354, 3638],
      spine: [3945, 4464], front: [4771, 8055],
      barcode: [1984, 4111, 1654, 1181] }
  end
end
