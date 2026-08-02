---
family: tasks
card: navigate_point_to_point
verdict: ready_with_fixes
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-08-02
---

# Audit: Navigate from Start to Goal

- **Card:** `prosoc/tasks/navigate_point_to_point/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (re-audit;
  supersedes the 2026-07-29 pass)
- **Verdict:** Ready for AUDITED — both findings resolved

## Findings

### 1. Common failure mode omitted or softened in YAML — RESOLVED
- **Section/field:** Common Failure Modes (Task-Level) vs. `common_failure_modes`
- **Issue (as originally found):** Prose listed four failure modes; the
  fourth — "Oscillatory or indecisive motion that prevents sustained
  progress" — had no corresponding entry in `common_failure_modes` (which
  had only three). Separately, the third prose bullet, "Abandonment of the
  goal **without external cause**," was present in YAML only as
  "abandonment of navigation goal" — the qualifier was dropped.
- **Fix applied:** Added `oscillatory or indecisive motion preventing
  sustained progress` to `common_failure_modes`, and reworded
  `abandonment of navigation goal` to `unjustified abandonment of
  navigation goal` to restore the qualifier's intent. `task.yml`
  regenerated and confirmed in sync (`scripts/distill/tasks --dry-run
  --show-diffs`, no diff).

### 2. `example_scenarios` used a versioned id instead of the directory name — RESOLVED
- **Section/field:** Example Scenarios (Non-Exhaustive) / `example_scenarios`
- **Issue (as originally found):** `frontal_approach_01` did not resolve
  to any directory under `prosoc/scenarios/` — the actual directory is
  `frontal_approach` (no `_01` suffix). `intersection_no_gesture` and
  `pedestrian_overtaking` already resolved correctly.
- **Fix applied:** Changed `frontal_approach_01` to `frontal_approach` in
  both the fenced YAML and the matching prose bullet list (checked both
  this time, per the prose/YAML mismatch caught while fixing
  `navigate_follow_agent` earlier this session). Confirmed
  `prosoc/scenarios/frontal_approach/` exists.

## Prose/YAML Consistency

Task Summary, Task Description, and Task Scope and Boundaries align with
`task_type`, `primary_intent`, `summary`, and `scope.{includes,excludes}`.
Relationship to Prosocial Navigation Principles names P0, P1, P2, P3 in
prose, matching `related_principles` exactly. Common Failure Modes and
Example Scenarios now both match prose exactly (Findings 1–2, resolved
above).

## Schema and Charter Compliance

- `scripts/distill/tasks --dry-run --show-diffs` produced no diff and no
  schema validation error (whole-family dry-run) after the fixes.
- `related_principles`: P0, P1, P2, P3 — four valid P0–P9 IDs.
- `task_type: navigation` — exact enum match.
- The task stays abstract throughout — no environment/agent-count/social
  content leaks into `scope`, `primary_intent`, or the description.
- `common_failure_modes` entries are task-level.
- All three `example_scenarios` entries now resolve to real scenario
  directories (`frontal_approach`, `intersection_no_gesture`,
  `pedestrian_overtaking`).

## Completeness

All Required sections present. Both optional-but-recommended sections
(Common Failure Modes, Example Scenarios) are populated with no remaining
content issues.
