---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-PDF-BUILD
title: "Add a reproducible PDF build entry point for the charter supplement"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
depends_on: []
blocked_by: []
expected_actions: [create_file, edit_file, run_tests, create_pr, write_docs]
forbidden_actions: [force_push, delete_branch, merge_pr, modify_ci_pipeline]
acceptance:
  - "A scripted command produces a compiled PDF when required tools/assets are present"
  - "The command fails clearly, not silently, when tools/assets are missing or versions mismatch"
required_evidence: [manual_review, lrh_validate, test_output]
artifacts_expected:
  - papers/01_charter/render.py
  - scripts/build-paper-supplement
  - docs/paper-supplements.md
---

## Summary
Add a reproducible PDF build entry point for the charter supplement: a
fail-fast `pdflatex` compile with outline fonts, `pdftotext` checks, and a
pinned/checked Pandoc version.

## Problem / Context
No PDF build path exists today — `render.py`'s `main()` explicitly rejects
any arguments. The pipeline's reproducibility depends on an unpinned Pandoc
version; the audit observed 3.10.1 and 2.9.2 across two sandboxes, straddling
a documented `--listings`-spelling deprecation.

### Duplication search
- In-repo: `render.py` exists but has no PDF stage; extend rather than
  duplicate.
- Recommendation: Proceed.

### Demand search
- None found.
- Recommendation: No action.

## Scope
- Add `render.py --pdf`/`--check` (or a new `scripts/build-paper-supplement`
  entrypoint) that validates sources, renders fragments/`rendered.tex`,
  runs the semantic/LaTeX checks from WI-CHARTER-SUPPLEMENT-TEST-COVERAGE,
  compiles the PDF with fail-fast `pdflatex` flags and outline fonts
  (`lmodern`/`cm-super`), runs `pdftotext -layout`, and runs PDF-text
  regression checks.
- Pin or explicitly check the Pandoc version and TeX engine/version; fail
  with a clear message if unmet.
- Document whether Frontiers class/publisher assets are committed or must
  be supplied locally, and their licensing status.

## Required Changes
1. `papers/01_charter/render.py` (or new `scripts/build-paper-supplement`).
2. `docs/paper-supplements.md` — document the new build/check command.

## Non-Goals
- Does not commit third-party Frontiers publisher files without confirming
  licensing.
- Does not regenerate the golden file itself (see WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN).

## Acceptance Criteria
- A documented, scripted command produces a compiled PDF from current
  sources when required tools/assets are present, reporting Pandoc
  version, TeX engine/version, PDF path, and page count.
- The command fails clearly when required tools/assets are missing or
  versions are mismatched.
- `lrh validate` / `scripts/test` pass.

## Validation
- `scripts/test`
- `lrh validate`
- the new build/check command itself, run and its output reported in the PR

## Risk Notes
- Publisher (Frontiers) class files may not be redistributable — this item
  may land with a documented "supply your own" setup rather than a
  committed asset, pending a licensing answer.
