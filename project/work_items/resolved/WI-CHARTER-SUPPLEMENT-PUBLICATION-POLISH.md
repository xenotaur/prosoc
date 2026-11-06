---
resolution: "Implemented and merged in PR #132 (commit 71009327ca63460813aa0c58f3dfcbc29845aec7) -- stripped the trailing Markdown hard-line-break whitespace causing the mismatched status-block spacing from the 4 affected task cards (navigate_point_to_point, deliver_object, navigate_follow_agent, navigate_lead_agent), covering both their STATUS blocks and, after a substitute PR-mode self-review caught the gap, their Task Summary blocks too; and added author-controlled PDF Title/Author/Subject/Keywords/Language metadata to the Frontiers template via hyperref. Final page left untouched (no distortion to fill it), per the acceptance criteria."
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-PUBLICATION-POLISH
title: "Normalize status-block spacing and set author-controlled PDF metadata for the charter supplement"
type: deliverable
status: resolved
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PROOFREADING
depends_on: []
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_lifecycle_state_change]
acceptance:
  - "Task and context card status blocks render with spacing consistent with the scenario status blocks (no large blank gaps between bullets), without reintroducing the earlier collapsed-list bug"
  - "The compiled PDF has non-blank, author-controlled Title, Author, Subject, Keywords, and document-language metadata, if supported by the Frontiers template"
  - "The final page's layout is left as-is (not distorted to eliminate the roughly-half-empty last page) unless other fixes in this workstream naturally make the content fit more tightly"
required_evidence: [manual_review, test_output]
artifacts_expected:
  - papers/01_charter/template.tex
  - src/prosoc/nca/utils/papers/render.py
---

## Summary
Three smaller, independent polish items from the second-pass proofread:
inconsistent blank-line spacing in task/context status blocks (vs. the
tighter scenario status blocks), missing author-controlled PDF metadata
(Title/Author/Subject/Keywords/language), and the mostly-empty final
page (explicitly flagged by the reviewer as acceptable, not a defect to
chase).

## Problem / Context
Not independently re-verified in this planning pass; the executing
session should confirm the spacing difference between task/context and
scenario status blocks (reported at pp. 26, 29, 32, 36, 40 vs. the
tighter scenario blocks) and the current PDF metadata state (`pdfinfo` on
the regenerated PDF) before editing.

The reviewer is explicit that the final-page layout is **not** something
to force-fix: "It is acceptable and no heading is orphaned, so do not
distort typography merely to eliminate it." This item should treat that
as a non-goal by default, only revisiting it if the other workstream
items happen to naturally tighten the content enough to remove it without
typographic distortion.

### Duplication search
- In-repo: no existing work item covers status-block spacing consistency
  or PDF metadata; `WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN` and
  `WI-CHARTER-SUPPLEMENT-PDF-BUILD` (both resolved) cover the build
  pipeline itself, not these cosmetic properties.
- Recommendation: Proceed.

### Demand search
- Directly requested by the second-pass proofread (this session,
  2026-11-04).
- Recommendation: Proceed.

## Scope
Source Markdown/template spacing fix for status blocks, plus a
`template.tex`/`render.py` change to set PDF metadata if the Frontiers
class/template supports author-controlled metadata fields. No final-page
layout changes except as an incidental side effect of other workstream
items.

## Required Changes
1. Compare the Markdown source structure of a task/context status block
   against a scenario status block to find the actual source of the
   spacing difference (e.g. extra blank lines between bullets, or a
   different list-rendering path in `render.py`/Pandoc for one family vs.
   the other).
2. Normalize the spacing -- in source Markdown or the publication
   filter, whichever is the actual cause -- so task/context status blocks
   render as tightly as scenario ones. Explicitly verify this does not
   reintroduce the collapsed-list bug `WI-CHARTER-SUPPLEMENT-SOURCE-FIXES`
   already fixed (same family of defect, opposite direction).
3. Check whether `frontiers_suppmat.cls` (or the standard `hyperref`
   metadata hooks already loaded via `template.tex`) exposes
   author-controlled PDF Title/Author/Subject/Keywords/Lang metadata
   (e.g. via `\hypersetup{...}` or `pdftitle`/`pdfauthor`-style macros).
   If supported without a risky template rewrite, set meaningful values
   for each. If the publisher's own production step controls this (as
   may be the case for a Frontiers-submitted supplement), document that
   limitation instead of forcing it.
4. Do not attempt full tagged-PDF/accessibility support if that is a
   publisher-controlled production step -- document the limitation
   rather than undertaking a risky template rewrite, per the reviewer's
   own explicit guidance.

## Non-Goals
- Does not alter the final page's layout to eliminate empty space --
  explicitly out of scope per the reviewer's own instruction, unless
  other workstream items incidentally make it fit without distortion.
- Does not undertake tagged-PDF/accessibility support if it's a
  publisher-controlled step.

## Acceptance Criteria
- Task/context status blocks visually match scenario status blocks'
  spacing in the regenerated PDF.
- `pdfinfo` on the regenerated PDF shows non-blank Title/Author/Subject/
  Keywords/language, or a documented reason why any of these couldn't be
  set.
- Final page left alone unless naturally resolved elsewhere.
- Golden file regenerated with human-reviewed diff.
- `scripts/test` / `lrh validate` pass.

## Validation
- `scripts/test`
- `lrh validate`
- `pdfinfo` on the regenerated PDF.
- Visual comparison of task/context vs. scenario status-block spacing.

## Risk Notes
- Spacing fixes in list-rendering logic have previously caused a
  collapsed-list regression in this pipeline (the original 2026-10-26
  audit's finding, fixed by `WI-CHARTER-SUPPLEMENT-SOURCE-FIXES`) -- test
  explicitly against that regression, not just the new spacing goal.

## Dependencies / Order
None. Independent of the other items in this workstream; low risk,
suitable to run last.
