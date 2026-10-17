# Release 1.0.0 audit

Date: 2026-10-17. Base: v1.0.0-preview.9 (`a71f35c`). Mainline at
audit start: `a7ad8b9`; one direct commit since the last tag, plus the
author-requested local UICLAP work. No open PRs. Issue #3 (audiobook/podcast
suggestion) is unrelated to this print/ebook release and remains open.

## Scope and conclusions

- First stable release, explicitly requested by the author after publication.
  Single mainline plus annotated tag; no new book prose or translations.
- Reviewed the combined paperback ISBN/profile selection, per-language Typst
  sources, PDF selection, KDP binding checks, and isolated UICLAP profile,
  geometry, barcode reserve, render commands, tests, and documentation.
- UICLAP remains a local opt-in target, not a GitHub release artifact.
  Its supplied template is hash-pinned, checked against 547 pages, and its
  70x50 mm barcode reserve is covered by regression tests and visual inspection.
- No dependency, lockfile, workflow, permission, release destination, or
  toolchain checksum changes. Subprocess additions use argument arrays;
  source/config inputs are trusted local author files, not remote requests.
  No new network-facing or authentication surface.
- No substantiated security findings in this scope. The security surface
  scan found no bidi controls; book discussions of prompts/credentials are
  prose, not executable behavior. Public-guard checks remain mandatory.
- GitHub secret-scanning reports zero open alerts. Dependabot alerts are
  disabled (403); code-scanning has no analysis (404). These are coverage
  limitations, not successful scans. No live-site penetration testing.

## Evidence and release gates

- Final material tree: 194 tests / 1,072 assertions, all passing.
- PT and EN source/release checks and public guard must pass before push.
- UICLAP: strict audit clean, 547 pages at 160x230 mm; renamed interior's
  SHA-256 remains `fa6c66f5250ed7317e930e670e51299486a631bcc7d79a90e757987df9db80e3`.
- UICLAP cover: visually inspected final CMYK proof and guide overlay;
  8409x5646 pixels, 600 dpi, upload JPG below 50 MB, PDF structural check clean.
  Reused from the byte-identical material inputs verified in this session.
- Full PT/EN build matrix must pass on the exact committed release candidate
  before tagging. The trusted tag workflow then rebuilds and publishes both
  languages, preserving its existing two-release retention policy.
- Latest blog drift was reported during format work. The author requested
  format-only changes and now release of the published books; the additional
  blog edits are not silently incorporated or stamped as reviewed here.

## Cleanup policy

Preserve final Amazon/UICLAP upload files, original artwork/templates,
provenance and editorial reviews, and pinned reusable toolchains. After
release verification, move obsolete Clube output and session scratch to
the desktop trash so cleanup is recoverable. Do not remove shared caches.
