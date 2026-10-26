---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-CI
title: "Add CI coverage for the charter supplement pipeline"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
depends_on:
  - WI-CHARTER-SUPPLEMENT-PDF-BUILD
blocked_by: []
expected_actions: [create_file, edit_file, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr]
acceptance:
  - "CI runs on changes to papers/01_charter/**, its 9 sources, and the renderer"
  - "CI fails on a golden diff and on pandoc-version or PDF-stage failures, not silently"
  - "Workflow artifacts include the generated PDF and diagnostics when the PDF stage runs"
required_evidence: [manual_review, lrh_validate]
artifacts_expected:
  - .github/workflows/charter-supplement.yml
---

## Summary
Add or extend a GitHub Actions workflow that exercises the full
charter-supplement pipeline — render, golden diff, and PDF compile — on
relevant changes.

## Problem / Context
`.github/workflows/charter.yml` only runs charter distillation and a YAML
diff check; its `paths:` trigger doesn't include `papers/**`, and nothing
renders or compiles the supplement. This item depends on
WI-CHARTER-SUPPLEMENT-PDF-BUILD existing, since there's nothing to invoke
in CI otherwise.

### Duplication search
- In-repo: `.github/workflows/charter.yml` exists but doesn't cover this;
  extend or add a sibling workflow rather than duplicate its distillation
  checks.
- Recommendation: Proceed.

### Demand search
- None found.
- Recommendation: No action.

## Scope
- Trigger on `papers/01_charter/**`, the 9 listed sources,
  `src/prosoc/nca/utils/papers/render.py`, its tests, and relevant
  validation/build-environment files.
- Install/check the pinned Pandoc version; run source validation; run
  renderer tests; render the supplement; fail on a golden diff; compile
  and inspect the PDF when licensed assets are available; upload the
  generated PDF and diagnostics as workflow artifacts.
- Report clearly (not silently skip) when the PDF stage cannot run due to
  missing assets.

## Required Changes
1. New `.github/workflows/charter-supplement.yml` (or an extended
   `charter.yml`, implementor's call).

## Non-Goals
- Does not modify `.github/workflows/charter.yml`'s existing
  charter-distillation checks beyond adding a trigger path, if that's the
  chosen approach instead of a new file.

## Acceptance Criteria
- New/extended CI workflow runs on PRs touching the declared paths.
- CI fails on a golden diff and on Pandoc-version or PDF-stage failures,
  not silently.
- Workflow artifacts include the generated PDF and diagnostics when the
  PDF stage runs.

## Validation
- A test PR run of the new workflow (reported in this item's PR description)
- `lrh validate`

## Dependencies / Order
Do not start before WI-CHARTER-SUPPLEMENT-PDF-BUILD lands — there's no PDF
stage to invoke otherwise.
