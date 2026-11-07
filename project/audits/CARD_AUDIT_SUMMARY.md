# Card Audit Summary

- **Run date:** 2026-11-07
- **Branch:** xenotaur/audit/wi-charter-supplement-lifecycle-audit-refresh
- **Scope:** `WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH` -- the 9 cards
  `WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION` demoted from `APPROVED`
  to `EDITED`, across 4 families (not a full-family or whole-corpus run)
- **Cards audited:** 9 (0 skipped)

This is a point-in-time index, not a live report -- each card's own
`audit.md` is the source of truth for full findings detail. No card's
Markdown, YAML, or STATUS/STATE block was modified in producing these
audits, and no card's STATE was promoted -- that remains a human decision
per [workflow.md](../../src/prosoc/prnc/scenarios/workflow.md).

**Deliberately does not touch `src/prosoc/prnc/scenarios/AUDIT_SUMMARY.md`
or `src/prosoc/prnc/tasks/AUDIT_SUMMARY.md`.** Both are full-family indexes
(20 scenarios, 4 tasks) from earlier whole-family runs; this run only
re-audited a subset of each (3 of 20 scenarios, 4 of 4 tasks but not as a
dedicated whole-family run), and `charter`/`contexts` have never had a
per-family summary file. Overwriting either existing file with only this
run's subset would misrepresent the other, untouched cards' documented
state. This run-scoped file is the honest alternative -- a snapshot of
exactly what this run covered, per `prosoc-card-audit-all`'s own
multi-family convention.

## Results

| Family | Card | Verdict | Blocking | Should-fix | Suggestion |
|---|---|---|---|---|---|
| charter | charter | ready_with_fixes | 0 | 1 | 1 |
| scenarios | frontal_approach | ready_with_fixes | 0 | 1 | 1 |
| scenarios | single_file_hallway | ready_with_fixes | 0 | 1 | 1 |
| scenarios | movable_obstruction | ready_with_fixes | 0 | 1 | 2 |
| tasks | navigate_point_to_point | ready_with_fixes | 0 | 1 | 0 |
| tasks | deliver_object | ready_with_fixes | 0 | 1 | 0 |
| tasks | navigate_follow_agent | ready_with_fixes | 0 | 1 | 0 |
| tasks | navigate_lead_agent | ready_with_fixes | 0 | 2 | 0 |
| contexts | high_urgency | ready_with_fixes | 0 | 2 | 2 |

**Totals:** 9 cards, 0 `ready`, 9 `ready_with_fixes`, 0 `not_ready`.
0 blocking, 11 should-fix, 7 suggestion findings.

*(Revised after review-response: `charter`'s should-fix count dropped from
2 to 1, and `single_file_hallway`'s rose from 0/`ready` to 1/`ready_with_fixes`
-- see each card's own `audit.md` for what changed and why. Totals are
unchanged, since the two corrections offset exactly.)*

No card's content was found wrong enough to block promotion -- every
one of the 9 cards is eligible for `EDITED -> AUDITED` under this
workstream's next work item
(`WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`), subject to the human
reviewing each should-fix/suggestion finding in its own `audit.md` first.

Notably, `high_urgency`'s audit specifically scrutinized the one
substantive (non-mechanical) content change among these 9 cards -- the
reclassification of P9 from `emphasized` to `deprioritized` in this
context -- and concluded it holds up against the charter's own P9
(Principle 13) Explanation, which directly ties increased task urgency to
a reduced expectation of P9's discretionary acts.

## Recurring Patterns

Extracted the same way as prior snapshots: exact-matching each finding's
normalized title across cards first, then a manual reading, since
parallel-dispatched subagents word the same underlying issue differently.

**Mechanical (exact-title match, threshold 3): none found** -- no two
findings in this run happened to share an identical normalized title.

**Manual reading, two recurring themes (each at or above threshold 3):**

1. **Dangling `example_scenarios` entries, recurring across 3 of the 4
   audited task cards** (`deliver_object`, `navigate_follow_agent`,
   `navigate_lead_agent` -- only `navigate_point_to_point`'s entries all
   resolve). Each lists one or more scenario ids that don't match any
   directory under `src/prosoc/prnc/scenarios/`. Independently
   re-verified: `deliver_object`'s three entries
   (`package_delivery_office`, `handoff_to_human_corridor`,
   `pickup_and_deliver_shelf_to_desk`) are all dangling; so is
   `navigate_follow_agent`'s `group_following_open_space`; so are both of
   `navigate_lead_agent`'s (`guided_navigation_corridor`,
   `escort_to_destination`) -- and `navigate_lead_agent`'s own audit
   flagged that `src/prosoc/prnc/scenarios/leading/` (an `APPROVED`
   scenario whose `intended_robot_task` is literally "lead the human to a
   destination") is a close topical match never referenced at all. This
   looks like a shared drafting-time gap in the `tasks` family's
   `example_scenarios` field, worth a dedicated pass across the whole
   family (not just these 4 cards) rather than fixing card-by-card.
2. **Missing optional prose sections, recurring across all 3 audited
   scenario cards.** `frontal_approach` and `single_file_hallway` lack an
   optional "Social Navigation Context" section (suggestion-level, not
   required); `movable_obstruction` additionally lacks a "Normative
   Expectations" section its own should-fix finding says is directly
   inferable from its existing `expected_behaviors` YAML (its sibling
   `single_file_hallway` already has one). This suggests the `scenarios`
   template's optional sections are inconsistently populated across the
   family generally, not just these 3 -- worth a corpus-wide pass or a
   template-level decision on whether to make "Normative Expectations"
   effectively required.

No blocking pattern recurred at any threshold. All findings across all 9
cards are should-fix or suggestion level.
