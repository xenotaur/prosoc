---
id: WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY
kind: planning_node
title: 'Repair stale APPROVED lifecycle state across the charter supplement corpus'
status: resolved
stage: closed
origin: follow_up
summary: 'Demote and re-promote the 9 normative cards whose APPROVED state postdates their last real audit, add a regression guard against recurrence, and confirm the resulting charter-supplement PDF is internally consistent.'
related_focus: []
related_roadmap: []
related_design:
  - 'project/design/proposals/adopted/normative-card-approval/00_proposal.md'
work_items:
  - WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION
  - WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH
  - WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION
  - WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD
exit_criteria:
  - 'All 9 identified cards (charter, frontal_approach, single_file_hallway, movable_obstruction, navigate_point_to_point, deliver_object, navigate_follow_agent, navigate_lead_agent, high_urgency) have a current audit.md and are back to APPROVED via an explicit human-confirmed promotion, or are left below APPROVED with recorded rationale'
  - 'scripts/validate/status and the full test suite pass with 0 errors'
  - 'papers/01_charter is rebuilt from canonical sources only, with no new clipping, spacing, or pagination regressions'
  - 'A regression-guard work item exists (filed or landed) to catch future APPROVED-but-stale drift automatically'
---

## Purpose

An external review of the regenerated charter supplement found that 7
cards (independent corpus-wide verification in this session found 2 more:
`navigate_follow_agent` and `navigate_lead_agent`) display `STATE:
APPROVED` even though their status history shows real content edits
committed after their most recent `audit.md`. This workstream repairs those
9 cards through the proper `EDITED → AUDITED → APPROVED` cycle, closes the
"an `APPROVED` card can be silently re-edited without dropping its state"
gap that `PROP-NORMATIVE-CARD-APPROVAL` Decision 5 explicitly deferred
rather than solved, and adds a lasting check so it doesn't recur silently.

## Scope

- Demote the 9 stale cards' embedded YAML `state:` from `APPROVED` to
  `EDITED` (direct hand-edit -- no existing skill performs a demotion)
- Refresh `audit.md` evidence for those 9 cards via
  `/prosoc-card-audit-all`, scoped by family
- Re-promote each card through `EDITED → AUDITED → APPROVED` via
  `/prosoc-card-review`, with an explicit human confirmation at every
  single promotion
- Regenerate the charter-supplement PDF from canonical sources afterward
  and re-verify consistency (STATE/AUDITED/APPROVED dates, no rendering
  regressions)
- Propose (not silently implement) a git-history-based audit-currency
  regression guard

## Prior Art Check

### Duplication search
- In-repo: No existing implementation found. One related hit:
  `project/design/proposals/adopted/normative-card-approval/00_proposal.md:213`
  names this exact failure mode ("State-staleness/auto-regression on later
  content edits... is an acknowledged gap, deferred as an Open Question,
  not solved here") -- this workstream is the deferred follow-up, not a
  duplicate.
- Sibling repos: None identified.
- External libraries: None identified -- this is a repo-specific
  lifecycle/provenance check, not a generic capability.
- Recommendation: Proceed.

### Demand search
- Work items: None found in `project/work_items/proposed/`.
- Proposals: None found in `project/design/proposals/proposed/`.
- Backlog: No matching entries in `project/design/backlog.md`.
- Recommendation: No action -- this is new, intentionally-scoped work, not
  something already requested elsewhere.

## Work Items

- **WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION** -- demote the 9 cards
  (charter, `frontal_approach`, `single_file_hallway`,
  `movable_obstruction`, `navigate_point_to_point`, `deliver_object`,
  `navigate_follow_agent`, `navigate_lead_agent`, `high_urgency`) from
  `APPROVED` to `EDITED`, one PR, with an explanatory `EDITED` bullet per
  card.
- **WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH** -- the 4 family-scoped
  `/prosoc-card-audit-all` runs against the demoted cards (`charter`;
  `scenarios frontal_approach single_file_hallway movable_obstruction`;
  `tasks navigate_point_to_point deliver_object navigate_follow_agent
  navigate_lead_agent`; `contexts high_urgency`).
- **WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION** -- the two human-gated
  `/prosoc-card-review` rounds (`EDITED → AUDITED`, then `AUDITED →
  APPROVED`) back to `APPROVED` for all 9 cards, plus the final
  regenerate/validate/visual-check of the PDF.
- **WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD** -- extend
  `check_audit_evidence` (`src/prosoc/nca/utils/cards/status.py:201`) /
  `scripts/validate/status` with a git-timestamp staleness check, filed
  separately per the originating review's own instruction not to broaden
  the repair unilaterally.

## Exit Criteria

(see frontmatter `exit_criteria`)

## Non-Goals

- Does not revisit the provenance-retention decision -- already resolved
  in `WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER` /
  `docs/paper-supplements.md:372-373`.
- Does not pursue tagged-PDF/accessibility support -- already an explicit,
  publisher-controlled non-goal of the prior workstream.
- Does not redesign the `audit.md` evidence format (e.g. content hashes
  instead of timestamps) unless a separate design process authorizes it.
- Does not implement the audit-currency guard's validator code as part of
  the demotion/promotion work items -- it is its own work item, confirmed
  on its own.
