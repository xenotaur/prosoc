---
resolution: "Verified via a real pdflatex+pdftotext round trip: heading numbering is correct (152/152 headings, each numbered once); Unicode survival inside lstlisting blocks fails for en dash and em dash (passes for curly apostrophe; 3 characters unverifiable due to zero occurrences in current content). Filed WI-CHARTER-SUPPLEMENT-RENDERER-DASH-FIX for the confirmed gap (merged PR #121, commit f4e3e7927840b57b01027477f7494e66a5facd82)."
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION
title: "Verify charter renderer heading-numbering and Unicode fixes via a real pdflatex+pdftotext round trip"
type: evaluation
status: resolved
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
depends_on:
  - WI-CHARTER-SUPPLEMENT-RENDERER-FIXES
blocked_by: []
expected_actions: [run_tests]
forbidden_actions: [force_push, delete_branch, merge_pr, modify_ci_pipeline, implement_lifecycle_state_change]
acceptance:
  - "Compiled PDF text shows each heading's number exactly once (the Frontiers class's automatic number, not a doubled authored-plus-automatic count)"
  - "Unicode dash/quote characters inside lstlisting blocks survive a real pdflatex compile + pdftotext -layout extraction"
  - "Any residual gap found is filed as a new work item, not silently left unresolved"
required_evidence: [manual_review, test_output]
artifacts_expected: []
---

## Summary
Run the real `pdflatex` compile + `pdftotext -layout` round trip that
`WI-CHARTER-SUPPLEMENT-RENDERER-FIXES`'s acceptance criteria originally
called for, but which that work item's landing session could not
perform (no `pdflatex` in that sandbox). Confirms the heading-numbering
and Unicode `literate=` fixes actually hold under a real compile, not
just at the `.tex`-source level.

## Problem / Context
`WI-CHARTER-SUPPLEMENT-RENDERER-FIXES` fixes the double-numbering (via a
Pandoc Lua filter) and Unicode dash/quote loss (via `literate=` mappings
in the `literatecard` `lstlisting` style) in the charter supplement
renderer. Its two PDF-level acceptance criteria — the compiled PDF
showing each heading's number exactly once, and Unicode characters
surviving a real `pdflatex`+`pdftotext` round trip — could not be
verified in that landing session because `pdflatex` was not installed
in the sandbox (a `brew install --cask basictex` attempt failed: the
cask's installer requires interactive `sudo`, which is not available in
this environment). That session verified only at the pandoc/`.tex`-source
level (Lua filter output inspected directly, `literate=` syntax checked
against pandoc's own handling) and deferred the real round trip here,
per explicit user decision, to unblock the rest of the workstream.

### Duplication search
- In-repo: no existing automated PDF-compile check; confirmed by
  inspecting `scripts/test` and `scripts/validate` — neither invokes
  `pdflatex`.
- Recommendation: Proceed.

### Demand search
- None found beyond the parent WI's own deferred acceptance criteria.
- Recommendation: No action.

## Scope
- In an environment with a working `pdflatex` (with outline fonts) and
  `pdftotext`, render the charter supplement, compile it, and extract
  text from the resulting PDF.
- Confirm each heading's number appears exactly once.
- Confirm the Unicode dash/quote characters in `lstlisting` blocks
  (en dash, em dash, non-breaking hyphen, curly double quotes, curly
  apostrophe `'`) survive the round trip intact.
- If either check fails, file a new work item for the gap rather than
  silently reporting a pass.

## Required Changes
1. In an environment with `pdflatex`, `pdftotext`, `kpsewhich`, and the
   Frontiers `frontiers_suppmat.cls` class file all available, run
   `PYTHONPATH="$(pwd)/src" papers/01_charter/render.py --pdf` to drive
   the full `build_pdf()` pipeline in
   `src/prosoc/nca/utils/papers/render.py` (pandoc-version check,
   tool/class-file prerequisite checks, semantic checks, render,
   `pdflatex` compile, internal `pdftotext -layout` text extraction, and
   `check_pdf_text_regressions`).
2. `build_pdf()` consumes its own extracted text internally and does not
   save it -- the CLI reports only tool versions, the PDF path, and a
   page count, leaving no text artifact for steps 3-4 below. Separately
   run `pdftotext -layout build/papers/01_charter/rendered.pdf
   build/papers/01_charter/rendered.txt` to produce a saved, inspectable
   text file; do not rely on step 1's internal extraction for manual
   inspection.
3. Inspect `build/papers/01_charter/rendered.txt` and the compiled
   `build/papers/01_charter/rendered.pdf` (per
   `docs/paper-supplements.md`'s "PDF Build" section) and confirm each
   heading's number appears exactly once -- not doubled by the Frontiers
   class's own automatic numbering on top of the Lua-filter output from
   `WI-CHARTER-SUPPLEMENT-RENDERER-FIXES`.
4. For each of the Unicode characters this WI's Acceptance Criteria names
   (en dash, em dash, non-breaking hyphen, curly double open quote, curly
   double close quote, curly apostrophe), run an explicit per-character
   coverage check against every `lstlisting` block in
   `build/papers/01_charter/rendered.txt` -- not just the corruptions
   `KNOWN_PDF_TEXT_CORRUPTIONS` in `render.py` already enumerates, since
   `check_pdf_text_regressions` only catches those. As of this WI's own
   drafting, `papers/01_charter/golden/rendered.tex`'s 19 `lstlisting`
   blocks contain 0 occurrences of the non-breaking hyphen (U+2011) or
   either curly double quote (U+201C/U+201D), so this round trip cannot
   verify those three characters as the source stands today -- record any
   character with no occurrence to check as an unverified gap in step 6
   below, never as a passing check.
5. Record the environment used (OS, `pdflatex`/`pdftotext` versions, and
   the Frontiers class file's source/licensing status) in the execution
   record -- `WI-CHARTER-SUPPLEMENT-CI`'s own CI workflow confirmed this
   tooling is still unavailable on its `ubuntu-latest` runner as of
   2026-11-01, so this WI cannot be run on that CI runner and needs a
   different environment.
6. File a new `WI-*` work item describing any failing check, or any
   unverified-gap character from step 4, rather than silently reporting a
   complete pass; do not attempt a renderer/template fix within this
   WI's own scope (see Non-Goals).

## Non-Goals
- Does not re-implement or modify the renderer, template, or Lua filter
  — this is verification only, of work already landed.
- Does not install a TeX toolchain as part of this WI's own scope (the
  environment running this WI is expected to already have one, or to
  set one up as a precondition, not as a deliverable of the WI itself).

## Acceptance Criteria
- Compiled PDF text shows each heading's number exactly once.
- Unicode dash/quote characters in `lstlisting` blocks survive the real
  round trip.
- Any residual gap found is filed as a new work item, not silently left
  unresolved.

## Validation
- Manual `pdflatex` + `pdftotext -layout` spot check, documented in the
  execution record (no code change expected, so no PR is required
  unless a gap is found).

## Risk Notes
- Needs an environment with `pdflatex` and outline fonts available —
  the same constraint that motivated deferring this from
  `WI-CHARTER-SUPPLEMENT-RENDERER-FIXES` in the first place.

## Dependencies / Order
`depends_on: [WI-CHARTER-SUPPLEMENT-RENDERER-FIXES]` — the fixes must
land first.
