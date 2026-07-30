# Prosoc Task Audit Checklist

This is a verification rubric, companion to `prosoc/tasks/schema.json` and
`prosoc/tasks/template.md`. It explains what to check when auditing an
already-drafted task card. Read `../principles.md` for the P0–P9 definitions
referenced below.

## Required Fields (schema.json)

| Field | Check |
|-------|-------|
| `id` | Matches `^[a-z]+(\.[a-z0-9_]+)+$` (dotted, e.g. `navigate.lead_agent`) |
| `name` | Matches the task's title heading in `task.md` |
| `summary` | Stands alone; not a restatement of `primary_intent` |
| `task_type` | One of `navigation`, `interaction`, `coordination` |
| `primary_intent` | A concise robot-goal statement, not a scenario description |
| `scope.includes` / `scope.excludes` | Both present; together they should make the task's
  boundary unambiguous — no gap or overlap left implicit |

## Prose/YAML Cross-Checks

| Prose section | Cross-check against YAML field(s) |
|---|---|
| Task Summary | `task_type`, `primary_intent` |
| Task Description | `primary_intent`, `summary` |
| Task Scope and Boundaries | `scope.includes`, `scope.excludes` |
| Relationship to Prosocial Navigation Principles | `related_principles` |
| Common Failure Modes (Task-Level) | `common_failure_modes` |
| Example Scenarios | `example_scenarios` |

Flag a **contradiction** when prose and YAML assert incompatible facts (e.g. prose
describes the task as multi-robot coordination but `task_type: navigation` with no
coordination framing). Flag **drift** when merely inconsistent in emphasis or detail.

## Schema Compliance

- [ ] `task.yml` validates against `schema.json` (no `additionalProperties`
      violations; `scope` has only `includes`/`excludes`)
- [ ] `related_principles` — every entry matches `^P[0-9]+$` and is P0–P9 (see
      `../principles.md`)
- [ ] `task_type` is exactly one of the three enum values, not a free-text variant
- [ ] The task stays **abstract** — per the schema's own description ("abstract robot
      intents... composed with scenarios, contexts, and charter principles"), flag any
      field that encodes a specific environment, agent count, or social setting; that
      content belongs to a scenario or context card, not here (mirrors the Task
      Description section's own "Avoid geometric layouts, agent counts, or social
      norms" instruction in `template.md`)
- [ ] `common_failure_modes` entries are task-level (independent of social context) —
      flag any entry that is really a scenario-specific or context-specific failure

## Completeness (template.md "Required" sections)

- [ ] Task Summary (Task ID, Task Name, Task Type, Primary Intent, Applies To)
- [ ] Task Description
- [ ] Task Scope and Boundaries
- [ ] Relationship to Prosocial Navigation Principles

Optional-but-recommended sections (`common_failure_modes`, `example_scenarios`): if
blank, decide reasonably blank (genuinely not yet known) vs. should probably be
filled in now (inferable from the Task Description already written).

## Cross-Reference Sanity (traceability only, not blocking)

`example_scenarios` entries are scenario **directory names** for discoverability —
check they aren't obviously malformed (e.g. not a full path, not the scenario's
`scenario.yml` `id`). A dangling `example_scenarios` entry (no matching directory
under `prosoc/scenarios/`) is a **should-fix**, not blocking: task cards predate full
scenario coverage, and this corpus is known to have several dangling entries tracked
as separate corpus work (see `PROP-NORMATIVE-PACKET-ASSEMBLY`'s Non-Goals) — do not
treat a dangling entry alone as reason for a `not_ready` verdict.
