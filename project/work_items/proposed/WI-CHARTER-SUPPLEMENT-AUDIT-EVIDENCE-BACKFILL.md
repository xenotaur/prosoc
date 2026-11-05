---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-AUDIT-EVIDENCE-BACKFILL
title: "Project real audit.md evidence into blank AUDITED: bullets for APPROVED task/context cards, and strengthen the status validator"
type: deliverable
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-PROOFREADING
depends_on: []
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_lifecycle_state_change]
acceptance:
  - "Every APPROVED task/context card's AUDITED: bullet reflects its real audit.md evidence (date and, where meaningful, verdict/auditor) instead of the placeholder '—'"
  - "No card's underlying lifecycle STATE changes as part of this fix -- this is a provenance-display fix, not a re-audit"
  - "scripts/validate/status fails (not just warns) when a card is APPROVED but has no audit.md, or has an audit.md with a non-acceptable verdict"
required_evidence: [manual_review, test_output]
artifacts_expected:
  - src/prosoc/prnc/tasks/
  - src/prosoc/prnc/contexts/
---

## Summary
A second-pass proofread of the charter supplement PDF found 5 cards
displaying `STATE: APPROVED` alongside a blank `AUDITED: —` bullet.
Verified directly in this session: all 5 (and, on a full corpus scan, all
8 APPROVED task/context cards, including 3 not in the supplement's
`sources.txt`) genuinely have a real `audit.md` on disk with an acceptable
verdict (`ready` or `ready_with_fixes`) -- the audit evidence exists, it
just was never projected into the card's own `AUDITED:` bullet.

## Problem / Context
The 5 cards the reviewer flagged (PDF page numbers as rendered then):
Navigate from Start to Goal (p. 26), Deliver an Object (p. 29), Routine
Service Delivery (p. 32), Guidance and Docent Operation (p. 36), Emergency
High-Urgency Operation (p. 40).

Direct verification this session (`src/prosoc/prnc/tasks/*/audit.md`,
`src/prosoc/prnc/contexts/*/audit.md`):

- `navigate_point_to_point`: `audit.md` exists, `verdict: ready_with_fixes`,
  `audited: 2026-08-02`, auditor "Claude (prosoc-card-audit skill)".
- `deliver_object`: `audit.md` exists, `verdict: ready_with_fixes`.
- `routine_delivery`: `audit.md` exists, `verdict: ready`.
- `guidance_docent`: `audit.md` exists, `verdict: ready`.
- `high_urgency`: `audit.md` exists, `verdict: ready_with_fixes`.

All 5 `task.md`/`context.md` files' `## STATUS` blocks show
`**AUDITED:** —` regardless. A full corpus scan found this is systemic,
not limited to these 5: `navigate_lead_agent`, `navigate_follow_agent`,
and `public_navigation` (not part of the charter supplement, so not seen
in the reviewed PDF) show the identical pattern -- real, passing
`audit.md`, blank `AUDITED:` bullet.

`WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK` (resolved, PR #114) deliberately
made `scripts/validate/status` check the real `audit.md` file's
existence/verdict rather than this bullet, specifically because the
bullet is optional, human-authored provenance that can be stale. That
design choice is correct for *validation* but is exactly what allows this
*display* gap to exist undetected -- a reader of the Markdown or the
rendered PDF has no way to see that real audit evidence exists, since the
only thing they can see says "—".

### Duplication search
- In-repo: `WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK` covers the validator
  side of audit evidence; no existing work item covers backfilling the
  bullet text itself.
- Recommendation: Proceed.

### Demand search
- Directly requested by the second-pass proofread (this session,
  2026-11-04), which also asks for the validator to go further: "extend
  validation so that APPROVED combined with absent required audit/
  approval evidence fails automatically." Needs checking against
  `WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK`'s actual current enforcement
  to determine what, if anything, is still missing there (this item
  should include that re-check as its first step rather than assume a
  gap).
- Recommendation: Proceed.

## Scope
For every APPROVED task/context card with a real, passing `audit.md` but
a blank `AUDITED:` bullet, project that evidence into the bullet. Confirm
(or close any remaining gap in) `scripts/validate/status`'s hard-fail
behavior for the APPROVED-without-evidence case.

## Required Changes
1. Re-check `scripts/validate/status`'s current behavior for an APPROVED
   card with a missing or non-acceptable-verdict `audit.md` -- confirm
   whether it already hard-fails (per `WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-
   CHECK`) or only warns, and close any remaining gap.
2. For each of the 8 affected cards (the 5 in the supplement plus
   `navigate_lead_agent`, `navigate_follow_agent`, `public_navigation`),
   replace the `AUDITED: —` bullet with the real evidence from its
   `audit.md` (at minimum the audit date; include auditor/verdict if that
   matches this card family's existing bullet-content convention
   elsewhere in the corpus -- check how other APPROVED cards with a
   filled-in `AUDITED:` bullet format it, e.g. the charter's own
   `APPROVED: Claude, 2026-08-07 (PR #79)` bullet, and match that style).
3. Re-run `scripts/validate/status --fix` where applicable to keep the
   distilled YAML/Markdown STATUS block in sync.
4. Regenerate the charter supplement's golden file if any of the 5
   in-supplement cards' rendered content changes, with human review of
   the diff.

## Non-Goals
- Does not change any card's lifecycle `STATE:` -- every affected card
  has genuine passing audit evidence; this is a display-completeness fix,
  not a re-audit or a demotion.
- Does not touch cards outside the task/context families unless the same
  corpus-wide scan (step 1 of Required Changes, extended if needed) finds
  the same pattern elsewhere.

## Acceptance Criteria
- All 8 identified cards' `AUDITED:` bullets reflect their real
  `audit.md` evidence.
- `scripts/validate/status` demonstrably fails (not warns) on a
  synthetic APPROVED-without-audit-evidence fixture.
- Golden file regenerated with human-reviewed diff if supplement content
  changed.
- `scripts/test` / `lrh validate` / `scripts/validate/status` pass.

## Validation
- `scripts/validate/status`
- `scripts/test`
- `lrh validate`
- Manual diff review of each changed card's STATUS block.

## Risk Notes
- Low risk -- content-only change (a bullet's text), no lifecycle-state
  or code-logic change to the cards themselves.

## Dependencies / Order
None. Independent of `WI-CHARTER-SUPPLEMENT-LISTING-DASH-GLYPH-FIX`;
recommended early since it's already fully scoped by this investigation.
