---
resolution: 'Implemented and merged in PR #135 (commit e70e4f353c59000bc1b666dbbfc469ad5120268a) -- wrote fresh, findings-only audit.md reports for all 9 demoted cards, plus a run-scoped project/audits/CARD_AUDIT_SUMMARY.md. Two review rounds found and fixed real content-accuracy errors in the audit text itself (P8/P9 principle-identity and branch-assignment mistakes, a genuine prose/YAML drift in single_file_hallway, and two reversed "no citations exist" vs. "none recorded" claims), independently re-verified against the actual charter/card source rather than accepted from review prose. CI''s check-packet-drift/test failures are the same already-disclosed sample_packet consequence inherited from WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION, not new.'
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH
title: 'Re-audit the 9 demoted charter-supplement cards against their current content'
type: evaluation
status: resolved
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY
related_design: []
depends_on:
  - WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION
blocked_by: []
expected_actions: [run_tests, create_pr, create_report]
forbidden_actions: [force_push, delete_branch, merge_pr, edit_card_content, implement_promotion]
acceptance:
  - 'Every one of the 9 cards has a fresh audit.md dated on or after this work item''s run, assessing its current (post-demotion) content'
  - 'No audit.md carries a verdict below ready_with_fixes without a corresponding should_fix/blocking item recorded'
  - 'No card''s state:, Markdown prose, or distilled YAML is modified by this work item'
required_evidence: [manual_review, validation_output]
artifacts_expected:
  - src/prosoc/prnc/charter/audit.md
  - src/prosoc/prnc/scenarios/frontal_approach/audit.md
  - src/prosoc/prnc/scenarios/single_file_hallway/audit.md
  - src/prosoc/prnc/scenarios/movable_obstruction/audit.md
  - src/prosoc/prnc/tasks/navigate_point_to_point/audit.md
  - src/prosoc/prnc/tasks/deliver_object/audit.md
  - src/prosoc/prnc/tasks/navigate_follow_agent/audit.md
  - src/prosoc/prnc/tasks/navigate_lead_agent/audit.md
  - src/prosoc/prnc/contexts/high_urgency/audit.md
---

## Summary

Refresh `audit.md` evidence for the 9 cards demoted by
`WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION`, using the exact
family-scoped `/prosoc-card-audit-all` invocations the originating
review specified.

## Problem / Context

Once the 9 cards are demoted to `EDITED`, their existing `audit.md` files
still describe pre-November content (dated 2026-07-29 through 2026-08-19)
and cannot be used as evidence for a future `AUDITED`/`APPROVED`
promotion. `prosoc-card-audit-all`
(`.claude/skills/prosoc-card-audit-all/SKILL.md:16-17`) is confirmed
read-only with respect to card state -- "it never edits any card's
Markdown, YAML, or STATUS/STATE block, and it never promotes a card's
lifecycle stage" -- so running it here cannot itself advance any card,
only produce the evidence the next work item's promotions require.

### Duplication search
- In-repo: `prosoc-card-audit-all` already exists and does exactly this;
  no duplicate work item or skill needed.
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed -- this item is an invocation of existing
  tooling, not new capability.

### Demand search
- Work items: None found requesting this specific re-audit batch.
- Proposals: None found.
- Backlog: No matching entries.
- Recommendation: No action.

## Scope

Run `/prosoc-card-audit-all` once per family grouping, scoped to exactly
the demoted cards in that family, per the originating review's own
prescribed commands (extended to cover `navigate_follow_agent` and
`navigate_lead_agent`, which the review did not know about).

## Required Changes

1. `/prosoc-card-audit-all charter`
2. `/prosoc-card-audit-all scenarios frontal_approach single_file_hallway movable_obstruction`
3. `/prosoc-card-audit-all tasks navigate_point_to_point deliver_object navigate_follow_agent navigate_lead_agent`
4. `/prosoc-card-audit-all contexts high_urgency`
5. Review each resulting `audit.md` for `blocking`/`should_fix` findings;
   if any blocking finding appears, route it back to a human decision
   before the promotion work item proceeds on that card.
6. If the skill opens a separate audit PR (per its own git-action
   pattern), land or rebase it before `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`
   begins, per the skill's own noted dependency.

## Non-Goals

- Does not audit any card outside the 9 named here.
- Does not change any card's `state:`, promote it, or edit its
  Markdown/YAML content.
- Does not resolve any `blocking`/`should_fix` audit finding -- surfaced
  to the human, not fixed here.

## Acceptance Criteria

(see frontmatter `acceptance`)

## Validation

- `lrh validate`
- Manual review of each new `audit.md`'s `verdict`, `blocking`, and
  `should_fix` fields

## Risk Notes

- A `blocking` finding on `high_urgency` is the most likely outcome here,
  since its post-audit edit was the one substantive normative change in
  this batch (P9 reclassified from `emphasized` to `deprioritized`) -- if
  the audit surfaces concerns about that reclassification itself, that is
  a real finding to route to the human, not a tooling problem.
