---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX
title: "Fix PDF-text corruption of en/em dash inside charter supplement lstlisting blocks (missing T1 font encoding)"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
depends_on: []
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_lifecycle_state_change]
acceptance:
  - "A real pdflatex + pdftotext -layout round trip shows en dash and em dash surviving correctly inside lstlisting blocks (not corrupted to '{' or '|')"
  - "papers/01_charter/template.tex loads a font encoding under which \\textendash/\\textemdash (used by the literatecard literate= mapping) produce PDF text with correct ToUnicode mappings"
  - "papers/01_charter/golden/rendered.tex is regenerated with human review of the resulting diff (expected: the new preamble line only, no card-content changes)"
  - "scripts/test and lrh validate pass"
required_evidence: [manual_review, test_output]
artifacts_expected:
  - papers/01_charter/template.tex
---

## Summary
Fix a confirmed PDF-text corruption: the `literatecard` lstlisting
style's `literate=` mapping for en dash and em dash
(`papers/01_charter/template.tex:65-66`) does not survive a real
`pdflatex` + `pdftotext -layout` round trip -- both characters are
corrupted in the extracted text, even though the previous fix
(`WI-CHARTER-SUPPLEMENT-RENDERER-FIXES`) was verified at the
pandoc/`.tex`-source level only.

## Problem / Context
`WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION`'s real-compile
verification (2026-11-01) found: inside the P0 principle's embedded
YAML `lstlisting` block, `P1–P9` (en dash) extracts as `P1{P9` --
confirmed byte-for-byte via hexdump, not a display artifact. The two
em dashes in the movable-obstruction scenario's listing block extract
as `|` in place of `—`. The one curly-apostrophe occurrence in the
corpus's listing blocks extracts correctly.

Root cause (diagnostic, not yet fixed): neither `template.tex` nor the
Frontiers `frontiers_suppmat.cls` class file loads
`\usepackage[T1]{fontenc}` or `\usepackage{textcomp}` (confirmed via
grep -- zero matches in either file). Without T1 encoding,
`\textendash`/`\textemdash` fall back to OT1-encoded Computer Modern
glyphs whose PDF `ToUnicode` mapping is wrong -- a well-documented
LaTeX pitfall. `\textquoteright` (curly apostrophe) happens to degrade
to a glyph with a sane mapping even under OT1, which is why only the
apostrophe case survived.

### Duplication search
- In-repo: no existing `fontenc`/`textcomp` usage anywhere in
  `papers/01_charter/template.tex` or the Frontiers class file
  (confirmed via `grep`).
- Recommendation: Proceed.

### Demand search
- `WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION`'s own Acceptance
  Criteria require filing a new work item for exactly this kind of
  residual gap; no other open work item covers it.
- Recommendation: Proceed.

## Scope
- Add `\usepackage[T1]{fontenc}` (and `\usepackage{textcomp}` if T1
  alone doesn't fix it) to `papers/01_charter/template.tex`, near the
  existing `\usepackage{lmodern}` line (`template.tex:9-13`), which was
  added for the analogous "outline fonts, not bitmap" reason.
- Re-run the real `pdflatex` + `pdftotext -layout` round trip and
  confirm both previously-corrupted characters now extract correctly.
- Expect `papers/01_charter/golden/rendered.tex` to require
  regeneration: `render_paper()` copies `template.tex`'s preamble
  verbatim into the assembled `.tex` and only substitutes card
  placeholders (`src/prosoc/nca/utils/papers/render.py:248-276`), so
  adding a `\usepackage` line to `template.tex` changes the generated
  preamble even though no card fragment content is affected.
  Regenerate the golden file with human review of the diff, confirming
  only the expected preamble-line addition appears and no card content
  changed.

## Non-Goals
- Does not change the `literate=` character mappings themselves --
  the mapping logic is correct; only the font encoding needed to
  render its output correctly is missing.
- Does not re-verify the non-breaking hyphen or curly double-quote
  mappings -- those remain unverifiable because the current corpus
  content has zero occurrences inside `lstlisting` blocks (a separate,
  pre-existing content-coverage gap, not this WI's concern).

## Acceptance Criteria
- Real round-trip shows en dash and em dash surviving correctly inside
  `lstlisting` blocks.
- `papers/01_charter/template.tex` loads the font encoding needed for
  `\textendash`/`\textemdash` to produce correct PDF text.
- Golden file regenerated, with human review confirming the diff is
  only the expected new preamble line.
- `scripts/test` / `lrh validate` pass.

## Validation
- `scripts/test`
- `lrh validate`
- Manual `pdflatex` + `pdftotext -layout` round trip, with before/after
  character-level comparison, reported in the execution record.

## Risk Notes
- Needs the same `pdflatex`/`kpsewhich`/Frontiers-class-file
  environment as `WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION` --
  not available in default CI or a stock sandbox.

## Dependencies / Order
None. Can be worked independently once an environment with the TeX
toolchain is available.
