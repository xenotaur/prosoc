---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-TEST-COVERAGE
title: "Add regression tests for the charter supplement's known defect classes"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
depends_on: []
blocked_by: []
expected_actions: [create_file, edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr]
acceptance:
  - "New tests exist for list-collapse, heading-number, YAML round-trip, and identifier survival"
  - "Tests fail against current unfixed output and pass once source/renderer fixes land"
required_evidence: [manual_review, lrh_validate, test_output]
artifacts_expected:
  - tests/nca/utils/papers/render_test.py
  - tests/nca/utils/papers/paper_semantics_test.py
---

## Summary
Add regression tests for the collapsed-list, heading-numbering, Unicode,
identifier-survival, and YAML-semantic-round-trip defects found in
`project/audits/2026-10-26_charter_supplement_pipeline_audit.md`.

## Problem / Context
Current tests only confirm Pandoc ran and a listing style was substituted;
none of the above defect classes are regression-tested, so they could
silently recur. One required test (`test_rejects_unresolved_placeholders`)
already exists — don't duplicate it.

### Duplication search
- In-repo: `tests/nca/utils/papers/render_test.py` exists but doesn't cover
  these cases; extend rather than duplicate.
- Recommendation: Proceed.

### Demand search
- None found beyond the audit doc itself.
- Recommendation: No action.

## Scope
- List-collapse regression test keyed on "a bold or plain label
  (colon-terminated or not) immediately followed by a hyphen-prefixed
  run-on", not a literal bolded string and not requiring a colon, so it
  also catches the unbolded `include:`/`tensions include:` cases and the
  colonless `Geometric Factors`/`Operational Factors` cases.
- Heading-number test asserting generated LaTeX contains *no* authored
  heading-number prefix (the Lua filter strips it before LaTeX emission,
  so the `.tex` source itself never carries a number — only the Frontiers
  class's automatic counter does, applied at compile time) and that the
  compiled PDF text shows each heading's number exactly once.
- YAML semantic round-trip test: extract fenced YAML from source, extract
  and normalize the corresponding rendered listing, parse both, compare
  structures.
- Identifier-survival test: collect key identifiers from source cards,
  confirm recoverable from generated LaTeX and (once a PDF build exists)
  extracted PDF text, normalizing for line wrapping.

## Required Changes
1. `tests/nca/utils/papers/render_test.py` — add the list-collapse and
   heading-number tests.
2. New `tests/nca/utils/papers/paper_semantics_test.py` (or similar) — YAML
   round-trip and identifier-survival tests.

## Non-Goals
- Does not implement the fixes these tests check for.
- Does not duplicate `test_rejects_unresolved_placeholders`.

## Acceptance Criteria
- New tests exist and are collected by `scripts/test`.
- Tests fail against the current (unfixed) output and pass once
  WI-CHARTER-SUPPLEMENT-SOURCE-FIXES / RENDERER-FIXES land.

## Validation
- `scripts/test`
- `lrh validate`

## Dependencies / Order
Can be written test-first (red) ahead of WI-CHARTER-SUPPLEMENT-SOURCE-FIXES
/ RENDERER-FIXES (green), or alongside them — implementor's call.
