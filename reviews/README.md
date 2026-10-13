# Copyedit reviews

One folder per release and language, from the reader pass in
`docs/COPYEDIT.md` (step 2). Each `<part>.yml` is a read-only reader's
findings for one part of the book; `triage.md` records which items were
applied, rejected (and why) or left for the author.

Item format (YAML list):

```yaml
- unit: ch05            # unit id (preface: prefacio)
  line: 42              # line in book/<lang>/<unit>.md at review time
  quote: "exact words"  # verbatim, short, so the item survives line shifts
  category: error | consistency | repetition | clarity | pacing
  severity: high | medium | low
  problem: "what is wrong, in one or two sentences"
  suggestion: "replacement text, or what to do"
```
