---
resolution: Implemented and merged in PR #97 (commit 5c1a22f)
blocked_reason: null
blocked: false
id: WI-CHARTER-FRONTIERS-SYNC
title: Reconcile prosoc Charter principle wording with the Frontiers paper
type: operation
status: resolved
assigned_agents: []
related_focus: []
related_roadmap: []
related_workstreams: []
related_design:
  - project/design/proposals/proposed/charter-frontiers-sync/00_proposal.md
depends_on: []
blocked_by: []
expected_actions:
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - modify_severity_field
  - expand_scope_beyond_proposal
acceptance:
  - P1's normative statement and YAML description are broadened to include other robots and self-damage protection, per PROP-CHARTER-FRONTIERS-SYNC's P1 decision
  - P2, P3, P4, P7 normative statements and YAML descriptions are updated to the merged wording recorded in PROP-CHARTER-FRONTIERS-SYNC
  - P5's "where feasible" hedge is restored
  - P6's wording is unchanged; its modal changes from MUST to SHOULD
  - P8's normative statement inlines the six-context taxonomy (cultural, diversity, environmental [geometric/operational], task, interpersonal)
  - P9's normative statement trims the task/context/goals qualifier; Section 2's definition retains it, unchanged
  - Modal verbs across all ten principles read MUST for P0 and P1 only, SHOULD for P2-P9, in both normative statements and YAML `description` fields
  - severity fields are unchanged for all ten principles
  - charter.yml is regenerated via `scripts/distill/charter` and matches charter.md
  - charter's Status section records this edit with a dated entry, and STATE reverts APPROVED -> EDITED
  - lrh validate and scripts/validate/status report 0 errors
  - the charter is re-audited (audit.md updated) and carried back through AUDITED -> APPROVED
required_evidence:
  - manual_review
  - lrh_validate
  - validation_output
artifacts_expected:
  - prosoc/charter/charter.md
  - prosoc/charter/charter.yml
  - prosoc/charter/audit.md
---

# WI-CHARTER-FRONTIERS-SYNC

## Summary

Implement the charter content edits decided in `PROP-CHARTER-FRONTIERS-SYNC`:
broaden P1's Safety scope, restore P5's feasibility hedge, adopt merged
P2/P3/P4/P7 wording, apply the MUST-for-P0-and-P1/SHOULD-elsewhere modal
convention across all ten principles, inline P8's context taxonomy, and
trim P9's qualifier — reconciling `prosoc/charter/charter.md` with the
submitted Frontiers paper.

## Problem / Context

`PROP-CHARTER-FRONTIERS-SYNC` (proposed, PR #92) records finalized
decisions comparing the APPROVED charter against the frozen Frontiers
paper "The Prosocial Robot Navigation Charter." The paper cannot be
edited further (submitted); the charter is the only artifact that can
still change. This work item implements those decisions as actual edits
to `prosoc/charter/charter.md`, following the precedent set by the
2026-08-05 edit that reverted the charter from APPROVED to EDITED for a
content update and carried it back through the lifecycle.

### Duplication search
- In-repo: No existing implementation. `WI-CARD-STATUS-CHARTER` (resolved)
  touched the charter but only added lifecycle-state machinery, explicitly
  forbidding any principle content edit (`forbidden_actions:
  edit_charter_normative_content`) — this item is the complementary
  content-editing work that item deliberately excluded.
- Sibling repos: None identified — the Frontiers paper lives in Overleaf,
  outside any repo.
- External libraries: Not applicable.
- Recommendation: Proceed.

### Demand search
- Work items: None found under `project/work_items/proposed/`.
- Proposals: `PROP-CHARTER-FRONTIERS-SYNC` (proposed) — this work item
  directly implements it.
- Backlog: No matching entries.
- Recommendation: No action beyond the `related_design` link above.

## Scope

- Edit `prosoc/charter/charter.md`'s principle normative statements and
  YAML `description` fields for P1–P9 (P0 unchanged), per
  `PROP-CHARTER-FRONTIERS-SYNC`'s Design Decisions.
- Regenerate `prosoc/charter/charter.yml` via `scripts/distill/charter`.
- Carry the charter back through its lifecycle: APPROVED → EDITED
  (content update) → AUDITED → APPROVED, updating `prosoc/charter/audit.md`
  and the charter's Status section accordingly.

## Required Changes

Target text below reflects the decisions in `PROP-CHARTER-FRONTIERS-SYNC`;
refine minor phrasing during implementation if needed, but do not change
the decided scope or modal verb.

1. **P0 — Goal Achievement:** no change. Confirm wording and modal ("must")
   already match the paper; do not edit.
2. **P1 — Safety:** broaden scope, modal unchanged (MUST).
   Target: *"Robots must not cause harm to humans, or damage to other
   robots, environments, or themselves."*
3. **P2 — Comfort:** modal MUST → SHOULD, merged wording.
   Target: *"Robots should avoid causing stress, fear, or annoyance in
   nearby humans."*
4. **P3 — Legibility:** modal MUST → SHOULD, merged wording.
   Target: *"Robots should act in ways that make their goals and
   intentions clear from their behavior."*
5. **P4 — Politeness:** modal MUST → SHOULD, merged wording. Keep the
   existing YAML description's "offering help when asked and avoiding
   dismissive or intrusive behaviors" clause.
   Target: *"Robots should be respectful and considerate toward other
   agents in shared social spaces."*
6. **P5 — Social Competency:** modal MUST → SHOULD, restore the "where
   feasible" hedge.
   Target: *"Robots should follow basic social norms governing shared
   spaces where feasible."*
7. **P6 — Agent Understanding:** modal MUST → SHOULD only; wording
   unchanged.
   Target: *"Robots should predict and accommodate the behavior of other
   agents."*
8. **P7 — Proactivity:** modal unchanged (SHOULD), merged wording.
   Target: *"Robots should proactively anticipate potential issues or
   conflicts and take initiative to avoid or resolve them."*
9. **P8 — Contextual Appropriateness:** modal MUST → SHOULD, inline the
   six-context taxonomy.
   Target: *"Robots should act appropriately given their task,
   environmental (geometric and operational), cultural, diversity, and
   interpersonal context."*
10. **P9 — Prosocial Behavior:** modal unchanged (SHOULD), trim the
    trailing qualifier.
    Target: *"Robots should act, during or in support of navigation, to
    improve the navigation experiences of other agents or to preserve or
    improve the navigability of their shared environment."*
11. Update each edited principle's YAML `description` field to match its
    normative statement change (modal + wording), leaving `severity`
    untouched.
12. Regenerate `prosoc/charter/charter.yml`: `scripts/distill/charter`.
13. Add a dated `## Status` entry documenting this edit; set
    `state: EDITED` in the embedded YAML (reverting from `APPROVED`).
14. Re-audit the charter (`prosoc-card-audit` or manual equivalent),
    update `prosoc/charter/audit.md`, and carry the charter back through
    `AUDITED` → `APPROVED`.

## Non-Goals

- Does not edit the Frontiers paper — it is submitted and frozen, and not
  tracked in this repo.
- Does not touch Section 2's prosocial-navigation definition or P0's
  wording — both already match the paper.
- Does not change any principle's `severity` field — the proposal's audit
  confirmed the existing ladder.
- Does not re-litigate decisions already finalized in
  `PROP-CHARTER-FRONTIERS-SYNC` — any further wording disagreement
  discovered during implementation should go back through a proposal
  update, not be freelanced here.
- Does not modify `prosoc/charter/schema.json` or the distiller's code —
  only `charter.md` content and the regenerated `charter.yml`.

## Acceptance Criteria

- `lrh validate` reports 0 errors after all files are written.
- `scripts/validate/status` reports the charter's lifecycle state and
  Status block are consistent.
- `prosoc/charter/charter.yml` matches a fresh `scripts/distill/charter`
  run with no diff.
- Every acceptance item in the frontmatter `acceptance:` list is
  independently verifiable against the resulting `charter.md`.
- `prosoc/charter/audit.md` reflects a clean pass on the re-audit and the
  charter's `STATE` reads `APPROVED` again at the end of this item's work.

## Validation

- `scripts/version tools`
- `lrh validate`
- `scripts/validate/status`
- `scripts/distill/charter --dry-run --show-diffs`
- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`

## Risk Notes

- The modal-verb correction (P0 MUST vs. SHOULD) was caught and fixed in
  `PROP-CHARTER-FRONTIERS-SYNC` mid-session (2026-08-13) — implementers
  should read the proposal's current version, not rely on a cached or
  earlier summary of its decisions.
- P1, P5, P6, P8, and P9's "Target" text above are freshly drafted for
  this work item (not literally quoted in the proposal's prose) — worth a
  careful re-read against the proposal's Design Decisions section before
  landing, since a transcription slip here would ship as a charter content
  error, not just a planning artifact error.
- Re-running the charter through APPROVED → EDITED → AUDITED → APPROVED
  touches a card that gates `sample_packet`'s manifest assembly (fails
  closed below APPROVED) — coordinate if any other in-flight work depends
  on the charter staying at APPROVED during this window.
