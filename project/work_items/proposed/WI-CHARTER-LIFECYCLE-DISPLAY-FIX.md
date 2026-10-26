---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-LIFECYCLE-DISPLAY-FIX
title: "Fix the charter's stale Status: header and missing re-approval history"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
related_design:
  - project/design/proposals/adopted/charter-frontiers-sync/00_proposal.md
depends_on: []
blocked_by: []
expected_actions: [edit_file, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_lifecycle_state_change]
acceptance:
  - "charter.md's free-text Status: line matches its STATE bullet / embedded YAML"
  - "Edit history includes closing re-approval entries for both reverts"
  - "charter.yml's state: field is unchanged"
required_evidence: [manual_review, lrh_validate]
artifacts_expected:
  - src/prosoc/prnc/charter/charter.md
---

## Summary
Fix `charter.md:4`'s stale `**Status:** Draft (Normative)` header line and
add the missing closing "re-approved" history bullet(s) — a display and
provenance-bookkeeping fix only.

## Problem / Context
`charter.md:4` contradicts its own `## Status` block and embedded YAML
(both `APPROVED`). The edit history records "reverted from APPROVED
pending re-audit" twice (2026-08-05, 2026-08-19) but never records the
matching re-approval, even though PR #79 and PR #97 both show a formal
re-audit/re-approval via `prosoc-card-approve` (see
`project/audits/2026-10-26_charter_supplement_pipeline_audit.md`). **This
item must not change `state:` in `charter.yml` or the embedded YAML.**

### Duplication search
- In-repo: no existing fix; confirmed by direct inspection.
- Recommendation: Proceed.

### Demand search
- None found.
- Recommendation: No action.

## Scope
- Update `charter.md:4`'s `Status:` line to match the current `STATE`.
- Add history bullets documenting the 2026-08-07 (PR #79) and 2026-08-19
  (PR #97) re-approvals.

## Required Changes
1. `src/prosoc/prnc/charter/charter.md:4` — change `Status:` to reflect
   `APPROVED` (or remove the redundant free-text field in favor of pointing
   at the `## Status` block, implementor's call).
2. `src/prosoc/prnc/charter/charter.md` edit-history bullets — add entries
   recording each re-approval that closes out a "reverted...pending
   re-audit" entry.

## Non-Goals
- Does not change `state:` in `charter.yml` or the embedded YAML.
- Does not alter any principle's normative content.

## Acceptance Criteria
- `charter.md:4`'s `Status:` line matches the `STATE` bullet / embedded YAML.
- Edit history includes closing entries for both reverts.
- `scripts/validate/status --family charter --card charter` reports consistent.

## Validation
- `lrh validate`
- `scripts/validate/status --family charter --card charter`
