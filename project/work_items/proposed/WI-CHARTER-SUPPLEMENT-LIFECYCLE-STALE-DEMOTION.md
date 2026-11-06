---
resolution: null
blocked_reason: null
blocked: false
id: WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION
title: 'Demote 9 charter-supplement cards from APPROVED to EDITED pending re-audit'
type: operation
status: proposed
related_workstreams:
  - WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY
related_design:
  - 'project/design/proposals/adopted/normative-card-approval/00_proposal.md'
depends_on: []
blocked_by: []
expected_actions: [edit_file, run_tests, create_pr]
forbidden_actions: [force_push, delete_branch, merge_pr, implement_promotion, run_prosoc_card_audit_all, run_prosoc_card_review]
acceptance:
  - 'All 9 cards'' embedded fenced-YAML state: reads EDITED, with the charter''s separate free-text Status: header updated to match'
  - 'Each demoted card gains exactly one new EDITED history bullet citing this audit-currency finding, with no other prose/content change'
  - 'Distilled YAML is regenerated for every affected card via its family distiller, with no other diff'
  - 'scripts/validate/status --fix projects the STATE bullet correctly and scripts/validate/status reports 0 errors'
  - 'No audit.md is created, modified, or deleted by this work item -- that is WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH''s job'
required_evidence: [manual_review, lrh_validate, test_output]
artifacts_expected:
  - src/prosoc/prnc/charter/charter.md
  - src/prosoc/prnc/charter/charter.yml
  - src/prosoc/prnc/scenarios/frontal_approach/scenario.md
  - src/prosoc/prnc/scenarios/single_file_hallway/scenario.md
  - src/prosoc/prnc/scenarios/movable_obstruction/scenario.md
  - src/prosoc/prnc/tasks/navigate_point_to_point/task.md
  - src/prosoc/prnc/tasks/deliver_object/task.md
  - src/prosoc/prnc/tasks/navigate_follow_agent/task.md
  - src/prosoc/prnc/tasks/navigate_lead_agent/task.md
  - src/prosoc/prnc/contexts/high_urgency/context.md
---

## Summary

Demote 9 normative cards' lifecycle `state:` from `APPROVED` to `EDITED`:
each one carries a real content edit committed after its most recent
`audit.md`, so its current `APPROVED` state is stale per this project's own
documented policy.

## Problem / Context

An external paper-review pass over the regenerated charter supplement
flagged 7 cards displaying `STATE: APPROVED` despite status-history entries
showing edits after their last audit. An independent, corpus-wide
git-history sweep in this session (comparing each card's and its
distilled YAML's last-touching commit against its `audit.md`'s, then
inspecting the actual diff of every flagged card to rule out
metadata-only backfills) confirmed all 7 and surfaced 2 more
(`navigate_follow_agent`, `navigate_lead_agent` -- the same
`WI-CHARTER-SUPPLEMENT-PUBLICATION-POLISH` whitespace fix that touched
`navigate_point_to_point`/`deliver_object` was applied to all 4 task
cards "for corpus-wide consistency," per that WI's own execution record,
even though only 2 are in this paper's `sources.txt`).

The 9 confirmed-stale cards, with audit date vs. last real edit:

| Card | `audit.md` date | Last edit after audit |
|---|---|---|
| `charter/charter.md` | 2026-08-19 | 2026-11-05, 2026-11-06 (2 content edits) |
| `scenarios/frontal_approach/scenario.md` | 2026-08-02 | 2026-11-06 (SOURCE/EDITED reword + `evaluation_notes` rewrite) |
| `scenarios/single_file_hallway/scenario.md` | 2026-08-06 | 2026-11-05, 2026-11-06 |
| `scenarios/movable_obstruction/scenario.md` | 2026-08-06 | 2026-11-05 |
| `tasks/navigate_point_to_point/task.md` | 2026-08-02 | 2026-11-06 |
| `tasks/deliver_object/task.md` | 2026-08-01 | 2026-11-05, 2026-11-06 |
| `tasks/navigate_follow_agent/task.md` | 2026-08-02 | 2026-11-06 |
| `tasks/navigate_lead_agent/task.md` | 2026-07-29 | 2026-11-06 |
| `contexts/high_urgency/context.md` | 2026-07-29 | 2026-11-06 (substantive: reclassifies P9 from `emphasized` to `deprioritized` in both prose and `principle_emphasis` YAML) |

Three cards that the naive git-log-date check also flags
(`contexts/routine_delivery`, `contexts/guidance_docent`,
`contexts/public_navigation`) are confirmed **not** stale on inspection:
their only post-audit touch backfilled a previously-blank `AUDITED:`
bullet with a date copied from their own pre-existing `audit.md` (PR
#128) -- no new content, no post-audit edit. They are explicitly excluded
from this work item's scope.

`project/focus/current_focus.md:45-50` states the governing policy
without a trivial-edit exception: "Any edit to a scenario's prose or
YAML invalidates its prior audit... This applies even though every card
currently carries `APPROVED` -- a later content edit to an `APPROVED`
card still invalidates its audit the same way." No existing skill
performs this demotion: `prosoc-card-approve`
(`.claude/skills/prosoc-card-approve/SKILL.md:39-41`) explicitly "never
demotes," so this is a direct, confirm-gated hand-edit.

### Duplication search
- In-repo: No existing work item or skill performs a demotion. Related:
  `project/design/proposals/adopted/normative-card-approval/00_proposal.md:213`
  names this exact gap as an unsolved, deferred Open Question.
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed.

### Demand search
- Work items: None found.
- Proposals: None found.
- Backlog: No matching entries.
- Recommendation: No action.

## Scope

For each of the 9 confirmed-stale cards, flip the embedded YAML `state:`
from `APPROVED` to `EDITED`, project that into the Markdown STATE
bullet(s), regenerate distilled YAML, and record the demotion itself as a
new `EDITED` history bullet. Does not touch `routine_delivery`,
`guidance_docent`, or `public_navigation`.

## Required Changes

1. For each of the 9 cards: change the fenced-YAML `state: APPROVED` to
   `state: EDITED`. For the charter specifically, also update the
   free-text `**Status:**` header line (checked by
   `check_charter_status_line`) to match.
2. Run `scripts/validate/status --fix` to project the corrected `STATE`
   bullet into each card's Markdown.
3. Add one new `**EDITED:**` history bullet per card, dated today, citing
   this work item and summarizing that the card's `APPROVED` state was
   found stale against its existing `audit.md` -- preserve all existing
   history bullets verbatim.
4. Regenerate each affected family's distilled YAML
   (`scripts/distill/scenarios`, `scripts/distill/tasks`,
   `scripts/distill/contexts`, and the charter's own `distill.py`) and
   hand-review the diff maps only to the `state:` field change.
5. Check whether any affected card is a packet-manifest member (per this
   session's own `feedback_packet_manifest_golden_cascade` lesson) and
   regenerate `packet.golden.yml` if so.
6. Run the full test suite and `scripts/validate/status` to confirm 0
   errors.

## Non-Goals

- Does not run `/prosoc-card-audit-all` or `/prosoc-card-review` -- those
  are `WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH` and
  `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`.
- Does not touch `routine_delivery`, `guidance_docent`, or
  `public_navigation` -- confirmed not stale.
- Does not regenerate the charter-supplement PDF -- deferred to the
  promotion work item, after cards are back to `APPROVED`.
- Does not change any card's normative prose or YAML content beyond the
  `state:` field and the new history bullet.

## Acceptance Criteria

(see frontmatter `acceptance`)

## Validation

- `scripts/validate/status`
- `lrh validate`
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
- `scripts/lint`

## Risk Notes

- Demoting the charter itself is the most visible change in this batch --
  it is the corpus's top-level governing document, and its free-text
  `**Status:**` header must be kept in sync with the fenced YAML or
  `check_charter_status_line` will fail.
- Regenerating distilled YAML for a card whose only change is `state:`
  should produce a single-field diff; a larger diff signals an
  unintended content change and should block before committing.
