---
family: tasks
card: navigate_lead_agent
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-11-07
---

# Audit: Lead an Agent

- **Card:** `src/prosoc/prnc/tasks/navigate_lead_agent/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED, no blocking, should-fix, or suggestion
  findings.

This is a fresh audit written after `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`
resolved both should-fix findings tracked for this card since 2026-08-02 in
`project/design/backlog.md`'s "APPROVED cards with unresolved findings"
table (now removed from that table, since both are fixed) — the same
backlog-driven cleanup pattern used for `charter` in 2026-08-06. It does
not carry forward either finding's text, since the content it described no
longer exists.

## Findings

### Resolved: Common failure mode omitted from YAML

`common_failure_modes` now includes "unexplained abandonment of the leading
relationship," matching the prose's fourth bullet. Re-distilled
(`PYTHONPATH="$(pwd)/src" python -m prosoc.prnc.tasks.distill --dry-run
--show-diffs` reports no diff for the whole tasks family) and
schema-validated clean.

### Resolved: Dangling `example_scenarios` entries; existing match now used

`example_scenarios` (and the matching prose list) now reads `leading`,
`escort_to_destination` — replacing the dangling `guided_navigation_corridor`
with the existing, `APPROVED` `leading` scenario directory (role `leader`,
task "lead the human to a destination" — a direct match, re-verified
directly against `scenarios/leading/scenario.md`). `escort_to_destination`
remains dangling; rather than leave it untracked, it is now logged in
`project/design/backlog.md`'s "Missing forward-referenced cards" table
(added 2026-11-07), consistent with that table's existing entries for this
same corpus-wide, not-yet-blocking gap pattern.

## Prose/YAML Consistency

Task Summary, Task Description, and Task Scope and Boundaries all align
cleanly with `task_type`, `primary_intent`, `summary`, and
`scope.{includes,excludes}` — the Scope section's includes/excludes bullets
map list-for-list onto the YAML arrays (5 includes, 4 excludes, matched in
both). Relationship to Prosocial Navigation Principles names P0, P3, P2, P6
in prose (order differs from the YAML list, not a defect), matching
`related_principles: [P0, P2, P3, P6]` exactly. Common Failure Modes and
Example Scenarios are now both consistent — see the resolved findings
above.

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
  context) and now complete (see the resolved finding above); no scenario-
  or context-specific failure leaked in among the four.

## Completeness

All Required sections present and filled: Task Summary, Task Description,
Task Scope and Boundaries, Relationship to Prosocial Navigation Principles.
Both optional-but-recommended sections (Common Failure Modes, Example
Scenarios) are populated and now consistent with the YAML — see the
resolved findings above (one entry, `escort_to_destination`, remains a
tracked backlog item, not blocking `AUDITED`).
