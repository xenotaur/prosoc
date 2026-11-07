---
family: tasks
card: navigate_lead_agent
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 0
audited: 2026-11-07
---

# Audit: Lead an Agent

- **Card:** `src/prosoc/prnc/tasks/navigate_lead_agent/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Common failure mode omitted from YAML — should-fix
- **Section/field:** Common Failure Modes (Task-Level) vs. `common_failure_modes`
- **Issue:** The prose section lists four failure modes, but the fourth —
  "Abandonment of the leading relationship without external cause" — has no
  corresponding entry in the embedded YAML `common_failure_modes` list,
  which has only three entries (each matching one of the other three prose
  bullets: excessive speed, unclear/erratic motion, unsafe path selection).
- **Recommended fix:** Add an entry such as `unexplained abandonment of the
  leading relationship` to `common_failure_modes` (and, once a human
  confirms the fix, re-run `scripts/distill/tasks` for real to regenerate
  `task.yml`), or remove the prose bullet if it was intentionally dropped.

### 2. Dangling `example_scenarios` entries; existing match omitted — should-fix
- **Section/field:** Example Scenarios (Non-Exhaustive) / `example_scenarios`
- **Issue:** Both listed scenarios, `guided_navigation_corridor` and
  `escort_to_destination`, have no matching directory under
  `src/prosoc/prnc/scenarios/`. Meanwhile, `src/prosoc/prnc/scenarios/leading/`
  exists in the corpus and is a close topical match for this task — its
  scenario is titled "Leading," its `Robot Role` is `leader`, and its
  `Robot Task` is "lead the human to a destination" — yet it is not
  referenced here.
- **Recommended fix:** Replace one or both dangling entries with `leading`
  (an existing, `APPROVED` scenario directory), and either author the
  remaining missing scenario(s) or log them as tracked backlog work, per
  `PROP-NORMATIVE-PACKET-ASSEMBLY`'s Non-Goals (dangling `example_scenarios`
  entries are known, corpus-wide, not-yet-blocking work).

## Prose/YAML Consistency

Task Summary, Task Description, and Task Scope and Boundaries all align
cleanly with `task_type`, `primary_intent`, `summary`, and
`scope.{includes,excludes}` — the Scope section's includes/excludes bullets
map list-for-list onto the YAML arrays (5 includes, 4 excludes, matched in
both). Relationship to Prosocial Navigation Principles names P0, P3, P2, P6
in prose (order differs from the YAML list, not a defect), matching
`related_principles: [P0, P2, P3, P6]` exactly. See Finding 1 for the one
Common Failure Modes discrepancy.

## Schema and Charter Compliance

- `PYTHONPATH="$(pwd)/src" python3 -m prosoc.prnc.tasks.distill --dry-run
  --show-diffs` (run with an explicit `PYTHONPATH` to target this worktree's
  own `src/`, since this machine's global `prosoc` editable install
  otherwise resolves to an unrelated, stale checkout) produced no diff and no
  schema-validation error for the whole tasks family (4 cards, including
  this one) — `task.yml` is in sync with `task.md`'s embedded YAML, and no
  other task card in the family showed drift either.
- `related_principles`: P0, P2, P3, P6 — four valid P0–P9 identifiers.
- `task_type: navigation` — exact enum match.
- The task stays abstract throughout: no geometric layout, agent count, or
  specific social setting leaks into `scope`, `primary_intent`, or the Task
  Description.
- `common_failure_modes` entries are task-level (independent of social
  context) — see Finding 1 for the one missing entry; no scenario- or
  context-specific failure leaked in among the three that are present.

## Completeness

All Required sections present and filled: Task Summary, Task Description,
Task Scope and Boundaries, Relationship to Prosocial Navigation Principles.
Both optional-but-recommended sections (Common Failure Modes, Example
Scenarios) are populated — see Findings 1–2 for their content issues
(tracked, not blocking `AUDITED`).
