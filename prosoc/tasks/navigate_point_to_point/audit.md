---
family: tasks
card: navigate_point_to_point
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 0
audited: 2026-07-29
---

# Audit: Navigate from Start to Goal

- **Card:** `prosoc/tasks/navigate_point_to_point/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-07-29
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Common failure mode omitted or softened in YAML — should-fix
- **Section/field:** Common Failure Modes (Task-Level) vs. `common_failure_modes`
- **Issue:** Prose lists four failure modes; the fourth — "Oscillatory or
  indecisive motion that prevents sustained progress" — has no corresponding
  entry in `common_failure_modes` (which has only three). Separately, the
  third prose bullet, "Abandonment of the goal **without external cause**,"
  is present in YAML only as "abandonment of navigation goal" — the
  qualifier is dropped.
- **Recommended fix:** Add an entry for the oscillation/indecision failure
  mode, and restore the "without external cause" qualifier on the
  abandonment entry.

### 2. `example_scenarios` uses a versioned id instead of the directory name — should-fix
- **Section/field:** Example Scenarios (Non-Exhaustive) / `example_scenarios`
- **Issue:** `frontal_approach_01` does not resolve to any directory under
  `prosoc/scenarios/` — the actual directory is `frontal_approach` (no
  `_01` suffix). `intersection_no_gesture` and `pedestrian_overtaking`
  resolve correctly. This is the versioned `scenario.yml` `id`-field pattern
  rather than the directory name, the same distinction the scenarios
  checklist's `related_scenarios` convention calls out.
- **Recommended fix:** Change `frontal_approach_01` to `frontal_approach`.

## Prose/YAML Consistency

Task Summary, Task Description, and Task Scope and Boundaries align with
`task_type`, `primary_intent`, `summary`, and `scope.{includes,excludes}`.
Relationship to Prosocial Navigation Principles names P0, P1, P2, P3 in
prose, matching `related_principles` exactly. See Finding 1 for the Common
Failure Modes discrepancies.

## Schema and Charter Compliance

- `scripts/distill/tasks --dry-run --show-diffs` produced no diff and no
  schema validation error (whole-family dry-run).
- `related_principles`: P0, P1, P2, P3 — four valid P0–P9 IDs.
- `task_type: navigation` — exact enum match.
- The task stays abstract throughout.
- `common_failure_modes` entries are task-level.

## Completeness

All Required sections present. Both optional-but-recommended sections
(Common Failure Modes, Example Scenarios) are populated — see Findings 1–2
for their content issues.
