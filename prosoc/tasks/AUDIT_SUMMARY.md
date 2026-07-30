# Card Audit Summary

- **Run date:** 2026-07-29
- **Branch:** xenotaur/feat/wi-card-audit-skills-impl
- **Scope:** tasks
- **Cards audited:** 4 (0 skipped)

## Results

| Family | Card | Verdict | Blocking | Should-fix | Suggestion |
|---|---|---|---|---|---|
| tasks | deliver_object | ready_with_fixes | 0 | 2 | 0 |
| tasks | navigate_follow_agent | ready_with_fixes | 0 | 2 | 0 |
| tasks | navigate_lead_agent | ready_with_fixes | 0 | 2 | 0 |
| tasks | navigate_point_to_point | ready_with_fixes | 0 | 2 | 0 |

**Totals:** 4 cards, 0 `ready`, 4 `ready_with_fixes`, 0 `not_ready`. 0 blocking,
8 should-fix, 0 suggestion findings.

## Recurring Patterns

- **Common failure mode omitted or softened in YAML** (should-fix) — recurs
  in all 4 cards (`deliver_object`, `navigate_follow_agent`,
  `navigate_lead_agent`, `navigate_point_to_point`). In every case, the
  prose Common Failure Modes list has an item — usually "abandonment...
  without external cause," once an oscillation/indecision mode — that is
  either fully absent from the YAML `common_failure_modes` list or present
  with a qualifier silently dropped. This looks like a shared drafting-time
  pattern (the "abandonment without external cause" nuance systematically
  gets lost going from prose to YAML across this family) rather than four
  independent errors — worth a corpus-wide pass on `common_failure_modes`
  fidelity, and possibly worth calling out explicitly in
  `prosoc/tasks/template.md`'s guidance for this field.
- **Dangling `example_scenarios` entries** (should-fix) — recurs in 3 of 4
  cards (`deliver_object`, `navigate_follow_agent`, `navigate_lead_agent`;
  the fourth, `navigate_point_to_point`, has a related but distinct
  directory-name/id-field issue instead). This matches the corpus-wide gap
  already tracked in `PROP-NORMATIVE-PACKET-ASSEMBLY`'s Non-Goals (dangling
  `example_scenarios` references, ~7 of 10 task cards at proposal time) — not
  a new finding, but this run independently reconfirms its scope within the
  tasks family specifically.
