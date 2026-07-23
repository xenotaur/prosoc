---
id: FOCUS-SCENARIO-CORPUS-MAINTENANCE
title: Keep the social navigation scenario corpus audit-clean as PRs land
status: active
---

# Current Focus

The scenario corpus (20 scenarios under `prosoc/scenarios/`) reached a
fully audit-clean state as of the 2026-07-22 corpus-wide audit
(`prosoc/scenarios/AUDIT_SUMMARY.md`): 20/20 scenarios audited, 0 blocking
or should-fix findings outstanding. [PR #30](https://github.com/xenotaur/prosoc/pull/30)
and [PR #31](https://github.com/xenotaur/prosoc/pull/31) closed the last
remaining gaps (the `related_scenarios`/Table 3 divergence convention and
the `intersection_gesture_wait`/`intersection_no_gesture` empty
`scenario_usage_guide` sections); [PR #32](https://github.com/xenotaur/prosoc/pull/32)
re-ran `/prosoc-scenario-audit-all` against the full corpus to confirm the
clean state and landed it.

The active focus now is **maintenance, not a single deliverable**: keep the
corpus in this audit-clean state as further edits land, by:

- Running `/prosoc-scenario-audit` (single scenario) or
  `/prosoc-scenario-audit-all` (full corpus) after any change to a
  scenario's prose or YAML, rather than assuming a prior audit still holds.
- Treating `prosoc/scenarios/AUDIT_SUMMARY.md` as a point-in-time index
  only — it does not self-update, and must be regenerated after any
  re-audit (see its own header note).
- Using `/lrh-review-response` and `/lrh-confirm-fixes` to close out PR
  feedback on scenario changes, consistent with the execution-record
  history under `project/executions/`.

There is no currently open work item under `project/work_items/proposed/`
driving this; new scenario or tooling work should get its own work item
(see `project/work_items/resolved/` for the shape recent ones have taken:
`WI-SCENARIO-SECTION-RENDERER`, `WI-SCENARIO-DISTILL-INVOCATION`,
`WI-SCENARIO-DISTILL-REVIEW-FOLLOWUP`) rather than being folded into this
focus note.

Note: this file documents *prosoc's own engineering focus* (the LRH control
plane's "focus" concept). It is unrelated to any individual scenario's
content lifecycle state (SOURCE/DRAFTED/EDITED/AUDITED/VALIDATED, per
`prosoc/scenarios/workflow.md`) and to the P1–P8 social navigation charter
principles (`.claude/skills/_shared/principles.md`) — those are separate,
scenario-content concepts that this file does not track.
