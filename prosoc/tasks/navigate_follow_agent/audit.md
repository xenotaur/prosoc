---
family: tasks
card: navigate_follow_agent
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 0
audited: 2026-08-02
---

# Audit: Follow an Agent

- **Card:** `prosoc/tasks/navigate_follow_agent/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (re-audit;
  supersedes the 2026-07-29 pass)
- **Verdict:** Ready for AUDITED with one minor finding remaining

## Findings

### 1. Common failure mode missing from YAML — RESOLVED
- **Section/field:** Common Failure Modes (Task-Level) vs. `common_failure_modes`
- **Issue (as originally found):** Prose listed four failure modes, but the
  fourth — "Abandonment of following without external cause" — had no
  corresponding entry in the YAML `common_failure_modes` list (which had
  only three).
- **Fix applied:** Added `unjustified abandonment of following` to
  `common_failure_modes`. `task.yml` regenerated and confirmed in sync
  (`scripts/distill/tasks --dry-run --show-diffs`, no diff).

### 2. Dangling `example_scenarios` entries — PARTIALLY RESOLVED, one remains open
- **Section/field:** Example Scenarios (Non-Exhaustive) / `example_scenarios`
- **Issue (as originally found):** Both listed scenarios,
  `human_following_corridor` and `group_following_open_space`, had no
  matching directory under `prosoc/scenarios/`.
- **Fix applied:** `human_following_corridor` replaced with `following` —
  a real, existing scenario directory (`prosoc/scenarios/following/`,
  internal `scenario.yml` id `following_01`) whose description ("A robot
  in a servant role follows a human who leads their own navigation...
  maintain an appropriate following distance") is a strong topical match
  for this task. Uses the directory name, not the versioned `scenario.yml`
  id, per the convention `tasks/navigate_point_to_point/audit.md` Finding 2
  establishes (`example_scenarios` resolves against scenario directory
  names). Two self-caught slips corrected before finalizing this audit:
  the fenced YAML was initially updated but not the matching prose bullet
  list, and the entry was initially written as the id form
  (`following_01`) before being corrected to the directory form
  (`following`).
- **Still open:** `group_following_open_space` remains dangling — no
  existing scenario covers a multi-agent/group-following variant. Logged
  to `project/design/backlog.md` (2026-08-02) as a missing forward
  reference rather than fixed inline.

## Prose/YAML Consistency

Task Summary, Task Description, and Task Scope and Boundaries align cleanly
with `task_type`, `primary_intent`, `summary`, and
`scope.{includes,excludes}` — the Scope section's bullets match the YAML
list-for-list. Relationship to Prosocial Navigation Principles names P0, P2,
P3, P6 in prose, matching `related_principles` exactly. Common Failure Modes
now matches prose exactly (Finding 1, resolved above).

## Schema and Charter Compliance

- `scripts/distill/tasks --dry-run --show-diffs` produced no diff and no
  schema validation error (whole-family dry-run) after the fixes.
- `related_principles`: P0, P2, P3, P6 — four valid P0–P9 IDs.
- `task_type: navigation` — exact enum match.
- The task stays abstract throughout — no environment/agent-count/social
  content leaks into `scope`, `primary_intent`, or the description.
- `common_failure_modes` entries are task-level.
- `example_scenarios[0]` (`following`) resolves to a real scenario card;
  `example_scenarios[1]` (`group_following_open_space`) does not (see
  Finding 2, tracked not blocking).

## Completeness

All Required sections present. Both optional-but-recommended sections
(Common Failure Modes, Example Scenarios) are populated — see Finding 2 for
its one still-open content issue (tracked, not blocking `AUDITED`).
