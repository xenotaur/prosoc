---
resolution: null
blocked_reason: null
blocked: false
id: WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK
title: "Validate lifecycle state against audit.md evidence, not the AUDITED: bullet"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PIPELINE
depends_on: []
blocked_by: []
expected_actions: [create_file, edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_lifecycle_state_change]
acceptance:
  - "scripts/validate/status checks audit.md existence/verdict for AUDITED/APPROVED cards"
  - "scripts/validate/status checks the charter's free-text Status: line against STATE"
  - "Full corpus passes once WI-CHARTER-LIFECYCLE-DISPLAY-FIX lands"
required_evidence: [manual_review, lrh_validate, test_output]
artifacts_expected:
  - src/prosoc/nca/utils/cards/validate_status.py
  - tests/nca/utils/cards/validate_status_test.py
---

## Summary
Extend `scripts/validate/status` so lifecycle validation checks a card's
actual audit evidence (sibling `audit.md` existence/verdict) rather than
the optional `AUDITED:` provenance bullet, and additionally checks the
charter's free-text `Status:` line against its authoritative `STATE`.

## Problem / Context
The audit found 5+ cards showing `STATE: APPROVED` next to `AUDITED: —`,
which looked like a lifecycle violation but isn't: `workflow.md:143` makes
that provenance bullet optional, and all 8 non-charter cards actually have
a `ready`/`ready_with_fixes` `audit.md`. The validator should check the
real signal. Separately, nothing currently catches the charter's
`Status:`-vs-`STATE` drift that motivated WI-CHARTER-LIFECYCLE-DISPLAY-FIX.

### Duplication search
- In-repo: `scripts/validate/status` / `prosoc.nca.utils.cards.validate_status`
  exists and does the STATE-vs-YAML check already; this extends it rather
  than duplicating.
- Recommendation: Proceed (extend existing module).

### Demand search
- None found.
- Recommendation: No action.

## Scope
- For any card whose `STATE` is `AUDITED` or `APPROVED`, require a sibling
  `audit.md` with verdict `ready` or `ready_with_fixes` (not `blocking`).
- For the charter specifically, check its free-text `Status:` header line
  against the authoritative `STATE`.
- Keep the existing STATE-vs-distilled-YAML check unchanged.

## Required Changes
1. `src/prosoc/nca/utils/cards/validate_status.py` — add the `audit.md`
   existence/verdict check and the charter `Status:`-line check.
2. `tests/nca/utils/cards/validate_status_test.py` — unit tests for both
   new checks, including a fixture card missing `audit.md` at `APPROVED`.

## Non-Goals
- Does not change any card's `STATE`.
- Does not require the optional `AUDITED:` provenance bullet to be populated.

## Acceptance Criteria
- New checks implemented with unit tests.
- `scripts/validate/status` over the full corpus reports 0 failures once
  WI-CHARTER-LIFECYCLE-DISPLAY-FIX lands.
- `lrh validate` / `scripts/test` pass.

## Validation
- `scripts/test`
- `lrh validate`
- `scripts/validate/status`

## Dependencies / Order
No hard `depends_on`, but land at or after WI-CHARTER-LIFECYCLE-DISPLAY-FIX
so the new charter check doesn't immediately flag the very drift that item
fixes.
