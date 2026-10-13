# frozen_string_literal: true

require_relative "test_helper"

# scripts/en_quote_punct.rb: the EN house style puts periods and commas inside
# closing quotes, in prose only.
class TestEnQuotePunct < ToolTest
  SAMPLE = <<~MD
    ---
    chapter: "Test"
    ---

    # Test {#sec-ch09}

    <!-- src: original -->
    The runs "completed". He said "done", then left. She asked "is this right?".

    ![A "label".](assets/figures/x.png){#fig-x fig-alt="a value"}

    ```
    "deny": ["Bash(sudo *)"],
    ```
  MD

  # Guards the rewrite: prose fixed; front matter, figure lines, attributes
  # and code untouched.
  def test_rewrites_prose_only
    fx.write("book/en/ch09.md", SAMPLE)
    assert_exit 0, fx.run("en_quote_punct", fx.path("book/en/ch09.md"))
    text = fx.read("book/en/ch09.md")
    assert_includes text, %(The runs "completed." He said "done," then left. She asked "is this right?")
    assert_includes text, %(chapter: "Test"\n)
    assert_includes text, %(![A "label".](assets/figures/x.png){#fig-x fig-alt="a value"})
    assert_includes text, %("deny": ["Bash(sudo *)"],)
  end

  # Guards --check: reports and fails without writing; passes once clean.
  def test_check_mode
    fx.write("book/en/ch09.md", SAMPLE)
    res = fx.run("en_quote_punct", "--check", fx.path("book/en/ch09.md"))
    assert_exit 1, res
    assert_equal SAMPLE, fx.read("book/en/ch09.md")
    fx.run("en_quote_punct", fx.path("book/en/ch09.md"))
    assert_exit 0, fx.run("en_quote_punct", "--check", fx.path("book/en/ch09.md"))
  end
end
