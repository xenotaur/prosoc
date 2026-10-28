---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION
title: "Verify charter renderer heading-numbering and Unicode fixes via a real pdflatex+pdftotext round trip"
type: evaluation
status: proposed
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
