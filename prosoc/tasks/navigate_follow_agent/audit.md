---
family: tasks
card: navigate_follow_agent
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 0
audited: 2026-07-29
---

# Audit: Follow an Agent

- **Card:** `prosoc/tasks/navigate_follow_agent/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-07-29
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Common failure mode omitted or softened in YAML — should-fix
- **Section/field:** Common Failure Modes (Task-Level) vs. `common_failure_modes`
- **Issue:** Prose lists four failure modes, but the fourth — "Abandonment of
  following without external cause" — has no corresponding entry in the YAML
  `common_failure_modes` list (which has only three).
- **Recommended fix:** Add an entry such as `unjustified abandonment of
  following` to `common_failure_modes`, or remove the prose bullet if
  intentionally dropped.

### 2. Dangling `example_scenarios` entries — should-fix
- **Section/field:** Example Scenarios (Non-Exhaustive) / `example_scenarios`
- **Issue:** Both listed scenarios, `human_following_corridor` and
  `group_following_open_space`, have no matching directory under
  `prosoc/scenarios/`.
- **Recommended fix:** Author these scenarios, or replace the entries with
  existing scenario directories that exercise this task (known, tracked
  corpus-wide work).

## Prose/YAML Consistency

Task Summary, Task Description, and Task Scope and Boundaries align cleanly
with `task_type`, `primary_intent`, `summary`, and
`scope.{includes,excludes}` — the Scope section's bullets match the YAML
list-for-list. Relationship to Prosocial Navigation Principles names P0, P2,
P3, P6 in prose, matching `related_principles` exactly. See Finding 1 for the
Common Failure Modes discrepancy.

## Schema and Charter Compliance

- `scripts/distill/tasks --dry-run --show-diffs` produced no diff and no
  schema validation error (whole-family dry-run).
- `related_principles`: P0, P2, P3, P6 — four valid P0–P9 IDs.
- `task_type: navigation` — exact enum match.
- The task stays abstract throughout — no environment/agent-count/social
  content leaks into `scope`, `primary_intent`, or the description.
- `common_failure_modes` entries are task-level.

## Completeness

All Required sections present. Both optional-but-recommended sections
(Common Failure Modes, Example Scenarios) are populated — see Findings 1–2
for their content issues.
