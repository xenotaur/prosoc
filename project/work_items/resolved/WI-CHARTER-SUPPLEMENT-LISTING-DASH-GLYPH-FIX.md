---
resolution: "Implemented and merged in PR #127 (commit 5883fbacd09fda4f451ed4c1c8700782c36c26ec) -- the literatecard lstlisting style's en/em dash glyphs now render at correct visual width via \\dashstretch, verified by a real pdflatex+pdftoppm round trip and a new image-based regression test (TestListingDashGlyphVisualWidth); pdftotext's ToUnicode mapping from WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX is unaffected."
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX
title: "Fix visually-incorrect en/em dash glyphs inside charter supplement lstlisting blocks (ToUnicode mapping is correct, the drawn glyph isn't)"
type: deliverable
status: resolved
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PROOFREADING
depends_on: []
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_lifecycle_state_change]
acceptance:
  - "Rendering the P0 principle's embedded YAML lstlisting block (page 3 equivalent) to a PNG image shows a visibly full-length en dash in 'P1–P9', not a short hyphen-like glyph"
  - "Rendering the movable-obstruction scenario's lstlisting block (page 25 equivalent) to a PNG image shows visibly full-length em dashes in 'itself—by' and 'obstruction—thereby'"
  - "A new automated check renders representative pages to PNG/image and inspects glyph width (or an equivalent image-based signal), not pdftotext text extraction alone"
  - "pdftotext-based extraction continues to report the correct Unicode codepoints (no regression on WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX's prior fix)"
required_evidence: [manual_review, test_output]
artifacts_expected:
  - papers/01_charter/template.tex
---

## Summary
A second-pass proofread of the charter supplement PDF found that
`WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX`'s fix only corrected the PDF's
`ToUnicode`/text-extraction mapping for en/em dashes inside `lstlisting`
blocks -- the actual glyph drawn on the page in the monospace listing font
is still visually a short hyphen, not a true en/em dash.

## Problem / Context
`WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX` added
`\usepackage[T1]{fontenc}` to `papers/01_charter/template.tex` and verified
the fix via a `pdflatex` + `pdftotext -layout` round trip: en/em dash
character counts increased by exactly the previously-corrupted occurrence
count, and the extracted text read `P1–P9` / `itself—by` correctly. That
verification was accepted as sufficient at the time.

A fresh external review of the resulting PDF found otherwise. Verified
directly in this session by rendering the actual pages to PNG at 600 DPI
(`pdftoppm -png -r 600`) and visually comparing glyphs, not re-trusting
`pdftotext`:

- In body prose (e.g. "the social principles P1–P9." on page 3), the en
  dash renders correctly -- long, clearly distinct from a hyphen.
- In the *same sentence* rendered inside the P0 principle's embedded YAML
  `lstlisting` block (the `literatecard` style, monospace `\ttfamily`),
  the glyph between P1 and P9 is visibly short -- a hyphen, not an en
  dash -- even though `pdftotext` extracts `P1–P9` correctly for both.
- Same pattern confirmed for the em dash on page 25 ("itself-by",
  "obstruction-thereby" visually, vs. correct `pdftotext` extraction).

This means `pdftotext`'s `ToUnicode` CMap is correct (so copy-pasted or
extracted text reads right), but the font actually used to draw the
`\textendash`/`\textemdash` glyph inside the monospace listing context
renders a visually different, shorter mark. `pdftotext`-only validation
cannot detect this class of defect -- it never inspects the rendered
glyph, only the text-layer mapping.

### Duplication search
- In-repo: no existing image-based/visual rendering check exists anywhere
  in the papers pipeline; `WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION`
  and `WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX` both validated via
  `pdftotext` extraction only.
- Recommendation: Proceed.

### Demand search
- Directly requested by a second-pass external proofread of the generated
  PDF (this session, 2026-11-04), which this work item's Problem/Context
  section quotes and independently re-verifies.
- Recommendation: Proceed.

## Scope
Make the `literatecard` lstlisting style's en/em dash glyphs visually
correct inside the compiled PDF -- not merely correct in extracted text --
and add a regression check that can actually catch this defect class.

## Required Changes
1. Investigate why `\textendash`/`\textemdash` render short inside this
   `\ttfamily`/monospace listing context specifically, when the same
   commands render correctly in body prose using the same `lmodern`
   family. Candidate root causes to check: whether Latin Modern Mono
   (`lmtt`)'s T1-encoded en/em dash glyph slots are genuinely drawn at
   reduced width (a known limitation of some monospace/typewriter faces,
   which historically use a single dash-minus for all dash purposes
   since true dash-width differentiation conflicts with fixed-pitch
   spacing), vs. a `literate=` mapping or font-selection issue specific
   to this style.
2. Based on the root cause, pick and apply a fix -- for example (not
   prescriptive; the investigation in step 1 should decide): switching to
   a monospace face with genuine en/em dash glyphs, or adopting an
   explicit visual substitution for dash context (e.g. `--`/`---`-style
   doubled/tripled hyphens, a conventional typewriter-era approximation
   for en/em dash in fixed-pitch contexts) if no monospace font in this
   pipeline draws them correctly.
3. Add an image-based regression check: render representative pages (or a
   minimal reproduction) to PNG/raster and verify the dash glyph's drawn
   width or shape, not just `pdftotext`'s extracted text. Keep the
   existing `pdftotext`-based `KNOWN_PDF_TEXT_CORRUPTIONS` check in place
   as a complementary, faster check -- this item adds coverage, it
   doesn't replace that check.
4. Re-verify the fix with a real `pdflatex` compile and a visual
   (image-rendered) inspection of the P0 YAML block and the
   movable-obstruction scenario's listing block.
5. Regenerate `papers/01_charter/golden/rendered.tex` with human review of
   the diff, per this pipeline's established golden-file rule.

## Non-Goals
- Does not change the `literate=` character-mapping logic's scope
  (which characters get special-cased) -- only how the already-mapped
  en/em dash characters are visually drawn.
- Does not re-verify the non-breaking hyphen or curly-quote mappings --
  still zero occurrences in current listing-block content, per
  `WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION`'s Non-Goals.
- Does not replace `pdftotext`-based validation -- adds an image-based
  check alongside it.

## Acceptance Criteria
- A 600+ DPI render of the P0 YAML block and the movable-obstruction
  scenario's listing block visually shows correct, full-length en/em
  dashes, confirmed by direct image inspection (not inferred from text
  extraction).
- `pdftotext`-based extraction still reports the correct Unicode
  characters (no regression).
- A new automated check exists that can catch a reintroduction of this
  specific defect class (visually-wrong glyph, correctly-mapped
  `ToUnicode`) -- not solely `pdftotext`-based.
- Golden file regenerated with human-reviewed diff.
- `scripts/test` / `lrh validate` pass.

## Validation
- `scripts/test`
- `lrh validate`
- Real `pdflatex` + `pdftoppm` round trip with direct visual/image
  inspection of the affected pages, reported in the execution record
  with the rendered crops or a clear description of what was checked.

## Risk Notes
- Needs the same `pdflatex`/`kpsewhich`/Frontiers-class-file/Ghostscript
  environment as prior renderer-verification work items -- see
  `docs/paper-supplements.md`'s Environment Setup section.
- If the root cause is a genuine font limitation (monospace faces lacking
  true en/em dash glyphs), the "ideal" fix of a visually long true dash
  inside a fixed-pitch font may not exist -- the investigation step should
  surface this plainly rather than forcing a cosmetically awkward
  workaround, and may need the user's input on an acceptable visual
  convention.

## Dependencies / Order
None. Can be worked independently; recommended first among this
workstream's items since it is a regression in previously-closed work and
the most technically novel finding from the proofread.
