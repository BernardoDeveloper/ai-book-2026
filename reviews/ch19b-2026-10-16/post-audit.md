# preview.9 pre-release audit

Base: v1.0.0-preview.8, 3e1bd1e865e63a727593ac9aad0ca21a3e8ce110.
Starting HEAD: e5593f825100c5851ca3003e2e63ac10f6ade26a.
Three accumulated commits before this editorial release candidate. Full
post-audit required, not skipped. Candidate adds the approved bilingual
chapter, photos, provenance, surrounding corrections and current blog sync.

## Provenance and composition

PR #4 is merged at e5593f8; its contributor commit b6a364c and maintainer
date correction d7251e1 are preserved. Repeated copyedit commit subjects
describe the contribution and its merge, not duplicate edits. No open PRs;
open issue #3 (audiobook/podcast suggestion) is outside this release scope.

The only build-code change since preview.8 is gen_back_matter.rb's explicit
English photo-credit override (plus an English source-introduction copyedit).
The regression test covers that override and unchanged PT output. This
composes correctly with the new photos' separately written bilingual credits.
No dependency, lockfile, workflow, permissions, download-source, executable-mode,
symlink or submodule change is introduced. New binary assets are inspected
JPEG/PNG photographs, not executables. No bidirectional controls in the diff.

Trusted CI builds both languages separately, runs tests/check/build, uploads
only EPUB/PDF outputs, and publishes tags only after both builds pass. Its
existing retention policy keeps two releases and preserves old tags.
Local editions must build sequentially because index.typ is shared.

## Evidence and boundaries

- Regression suite: 178 tests, 971 assertions, no failures/errors/skips.
- Both source checks pass; focused new/changed chapter lint is clean.
- Both language source-drift checks clean after reviewing blog 557350127df1.
- Source markers, citations, bilingual figures and translation hashes checked.
- Fresh five-persona scoped reread recorded in personas-round2.
- Existing Kindle cleanup and accessibility gates remain in every build.
- No open secret-scanning alerts returned. Dependabot alerts disabled (403);
  code scanning has no analysis (404). These are coverage limitations, not
  evidence that dependency/security analysis passed.
- This is a source/build-pipeline audit, not a penetration test or legal review.

No blocking code/security finding. The author-selected photos have unverified
reuse permissions, explicitly disclosed before the instruction to include
them; credits, README, license notes and afterword no longer imply all photos
have cleared/free licences. No downstream reuse permission is asserted.

## Release handoff

User explicitly selected v1.0.0-preview.9: additive chapter in the existing
1.0.0 prerelease series. Single mainline plus annotated tag. Local PDF/EPUB
build, page audit and visual checks must pass before publication. Push the
candidate, require both hosted language jobs green at its exact SHA, then tag
that SHA and verify the tag-driven release and all six assets. Keep the final
local deliverables requested by the author; do not regenerate old spine covers.
Final page counts and hosted run outcomes are reported with the release.
