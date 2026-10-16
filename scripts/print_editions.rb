# frozen_string_literal: true

# The existing unsuffixed PDF remains the hardcover for download compatibility.
# Never let a glob's order select the paperback as the canonical print master.
module PrintEditions
  module_function

  def typ(root, lang)
    raise ArgumentError, "unsupported language: #{lang}" unless %w[pt en].include?(lang)

    File.join(root, "index-#{lang}.typ")
  end

  def pdf(dir, edition = "print")
    suffix = { "print" => "", "hardcover" => "", "paperback" => "-paperback", "ebook" => "-ebook" }.fetch(edition)
    master = Dir[File.join(dir, "*.pdf")].sort.find { !_1.match?(/-(?:ebook|paperback)\.pdf\z/) }
    return unless master

    candidate = master.sub(/\.pdf\z/, "#{suffix}.pdf")
    candidate if File.file?(candidate)
  end
end
