---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN
title: "Regenerate the charter supplement's golden rendering, with reviewed content diff"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
depends_on:
  - WI-CHARTER-SUPPLEMENT-SOURCE-FIXES
  - WI-CHARTER-LIFECYCLE-DISPLAY-FIX
  - WI-CHARTER-SUPPLEMENT-RENDERER-FIXES
  - WI-CHARTER-SUPPLEMENT-TEST-COVERAGE
  - WI-CHARTER-SUPPLEMENT-PDF-BUILD
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr]
acceptance:
  - "New golden/rendered.tex passes all checks from WI-CHARTER-SUPPLEMENT-TEST-COVERAGE"
  - "PR description separates defect-fix hunks from unrelated content-drift hunks"
  - "golden/original.tex is unchanged"
required_evidence: [manual_review, lrh_validate, test_output]
artifacts_expected:
  - papers/01_charter/golden/rendered.tex
---

## Summary
Regenerate `papers/01_charter/golden/rendered.tex` after the renderer
fixes, new tests, and PDF build entry point land, with a mandatory human
review of the resulting content diff.

## Problem / Context
`golden/rendered.tex` (PR #90, 2026-08-12) predates PR #97's charter
content (2026-08-19) — confirmed via P1's stale "harms people or damages
shared environments" explanation text, which is missing the broadened
other-robots/self-damage language `audit.md` records as added on the
19th. A fresh render will differ from golden for two unrelated reasons at
once: genuine defect fixes and ordinary already-landed content drift. This
item must not start until its dependencies land, and must include a
human-reviewed diff, not a mechanical regeneration.

### Duplication search
- Not applicable — this is a regeneration of an existing checked-in file.
- Recommendation: Proceed, once dependencies land.

### Demand search
- None found.
- Recommendation: No action.

## Scope
- Run the full render + new checks against current sources.
- Diff the result against the existing `golden/rendered.tex`; separate
  "defect fix" hunks from "unrelated content drift" hunks in the PR
  description.
- Get explicit human sign-off on the diff before replacing
  `golden/rendered.tex`.
- Leave `golden/original.tex` untouched.

## Required Changes
1. `papers/01_charter/golden/rendered.tex` — regenerated.

## Non-Goals
- Does not modify `golden/original.tex`.
- Does not re-open any editorial/content-review question from the audit's
  "Not independently re-verified" section.

## Acceptance Criteria
- New `golden/rendered.tex` passes all checks from
  WI-CHARTER-SUPPLEMENT-TEST-COVERAGE and the semantic LaTeX checks.
- PR description documents, hunk by hunk, which changes are defect fixes
  vs. content drift, and records the human reviewer's sign-off.
- `golden/original.tex` unchanged.

## Validation
- `papers/01_charter/render.py`
- `diff -u papers/01_charter/golden/rendered.tex build/papers/01_charter/rendered.tex`
- `scripts/test`
- `lrh validate`

## Dependencies / Order
Do not start before WI-CHARTER-SUPPLEMENT-SOURCE-FIXES,
WI-CHARTER-LIFECYCLE-DISPLAY-FIX, WI-CHARTER-SUPPLEMENT-RENDERER-FIXES,
WI-CHARTER-SUPPLEMENT-TEST-COVERAGE, and WI-CHARTER-SUPPLEMENT-PDF-BUILD
all land — regenerating against unfixed output would re-bake the defects
into golden. SOURCE-FIXES and LIFECYCLE-DISPLAY-FIX both edit Markdown
that's embedded directly in the golden output (the collapsed lists are
fixed only by SOURCE-FIXES), so without them as explicit prerequisites
the remaining three dependencies alone cannot guarantee the new
list-collapse checks pass or prevent baking those defects back into
golden.
