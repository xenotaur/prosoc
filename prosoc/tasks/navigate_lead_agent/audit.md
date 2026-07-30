---
family: tasks
card: navigate_lead_agent
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 0
audited: 2026-07-29
---

# Audit: Lead an Agent

- **Card:** `prosoc/tasks/navigate_lead_agent/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-07-29
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Common failure mode omitted or softened in YAML — should-fix
- **Section/field:** Common Failure Modes (Task-Level) vs. `common_failure_modes`
- **Issue:** Prose lists four failure modes, but the fourth — "Abandonment of the
  leading relationship without external cause" — has no corresponding entry in
  the YAML `common_failure_modes` list (which has only three, each matching one
  of the other three prose bullets).
- **Recommended fix:** Add an entry such as `unexplained abandonment of the
  leading relationship` to `common_failure_modes`, or remove the prose bullet if
  it was intentionally dropped.

### 2. Dangling `example_scenarios` entries — should-fix
- **Section/field:** Example Scenarios (Non-Exhaustive) / `example_scenarios`
- **Issue:** Both listed scenarios, `guided_navigation_corridor` and
  `escort_to_destination`, have no matching directory under
  `prosoc/scenarios/`.
- **Recommended fix:** Either author these scenarios, or replace the entries
  with existing scenario directories that exercise this task (this is known,
  tracked corpus-wide work per `PROP-NORMATIVE-PACKET-ASSEMBLY`'s Non-Goals —
  not unique to this card, and not itself a reason to withhold AUDITED).

## Prose/YAML Consistency

Task Summary, Task Description, and Task Scope and Boundaries all align
cleanly with `task_type`, `primary_intent`, `summary`, and
`scope.{includes,excludes}` — the Scope section's bullets match the YAML
list-for-list. Relationship to Prosocial Navigation Principles names P0, P3,
P2, P6 in prose, matching `related_principles: [P0, P2, P3, P6]` exactly
(order differs, not a defect). See Finding 1 for the one Common Failure Modes
discrepancy.

## Schema and Charter Compliance

- `scripts/distill/tasks --dry-run --show-diffs` produced no diff and no
  schema validation error (whole-family dry-run; no other task in the corpus
  showed drift either).
- `related_principles`: P0, P2, P3, P6 — four valid P0–P9 IDs.
- `task_type: navigation` — exact enum match.
- The task stays abstract throughout: no geometric layout, agent count, or
  social-setting content leaks into `scope`, `primary_intent`, or the
  description, consistent with the schema's "abstract robot intents" framing
  and the template's own "avoid geometric layouts... those belong to
  scenarios and contexts" instruction.
- `common_failure_modes` entries are task-level (independent of social
  context) — no scenario/context-specific failure leaked in.

## Completeness

All Required sections present: Task Summary, Task Description, Task Scope and
Boundaries, Relationship to Prosocial Navigation Principles. Both
optional-but-recommended sections (Common Failure Modes, Example Scenarios)
are populated (not blank) — see Findings 1–2 for their content issues.
