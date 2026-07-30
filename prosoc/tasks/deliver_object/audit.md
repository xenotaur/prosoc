---
family: tasks
card: deliver_object
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 0
audited: 2026-07-29
---

# Audit: Deliver an Object

- **Card:** `prosoc/tasks/deliver_object/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-07-29
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Common failure mode omitted or softened in YAML — should-fix
- **Section/field:** Common Failure Modes (Task-Level) vs. `common_failure_modes`
- **Issue:** Prose's third bullet, "Abandonment of delivery **without external
  cause**," is present in `common_failure_modes` only as "abandonment of
  delivery task" — the qualifier "without external cause" is dropped, which
  changes the meaning (any abandonment vs. specifically unjustified
  abandonment).
- **Recommended fix:** Restore the qualifier in the YAML entry, e.g.
  "unjustified abandonment of delivery task."

### 2. Dangling `example_scenarios` entries — should-fix
- **Section/field:** Example Scenarios (Non-Exhaustive) / `example_scenarios`
- **Issue:** All three listed scenarios — `package_delivery_office`,
  `handoff_to_human_corridor`, `pickup_and_deliver_shelf_to_desk` — have no
  matching directory under `prosoc/scenarios/`.
- **Recommended fix:** Author these scenarios, or replace the entries with
  existing scenario directories that exercise this task (known, tracked
  corpus-wide work per `PROP-NORMATIVE-PACKET-ASSEMBLY`'s Non-Goals — not
  unique to this card).

## Prose/YAML Consistency

Task Summary, Task Description, and Task Scope and Boundaries align with
`task_type`, `primary_intent`, `summary`, and `scope.{includes,excludes}`
(the excludes list's five prose items consolidate cleanly into four YAML
bullets — "requesting/accepting/refusing" and "appropriate or authorized"
merge into one "social authorization or consent" bullet, a reasonable
consolidation, not an omission). Relationship to Prosocial Navigation
Principles names P0, P1, P2, P3, P9 in prose, matching `related_principles`
exactly. See Finding 1 for the one Common Failure Modes discrepancy.

## Schema and Charter Compliance

- `scripts/distill/tasks --dry-run --show-diffs` produced no diff and no
  schema validation error (whole-family dry-run).
- `related_principles`: P0, P1, P2, P3, P9 — five valid P0–P9 IDs, at the
  upper end of the recommended range but each is discussed in the card's own
  prose.
- `task_type: navigation` — exact enum match.
- The task stays abstract: no geometric layout, agent count, or
  social-setting content leaks into `scope`, `primary_intent`, or the
  description.
- `common_failure_modes` entries are task-level, independent of social
  context.

## Completeness

All Required sections present. Both optional-but-recommended sections
(Common Failure Modes, Example Scenarios) are populated — see Findings 1–2
for their content issues.
