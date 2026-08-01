---
family: contexts
card: routine_delivery
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-08-01
---

# Audit: Routine Service Delivery

- **Card:** `prosoc/contexts/routine_delivery/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-01
- **Verdict:** Ready, no issues found

## Findings

No findings. `context.yml` is in sync with `context.md` (confirmed via
`scripts/distill/contexts --dry-run --show-diffs`, no diff for this card).
All required schema fields are present and valid:

- `id: service.routine_delivery` matches the dotted-id pattern.
- `context_class: core` matches the STATUS block's `CONTEXT TYPE: CORE`.
- `primary_robot_role: service provider` is a social role, not a task
  description.
- `applies_to_tasks: [deliver.object]` resolves to a real task
  (`prosoc/tasks/deliver_object/task.yml`).
- All five `axes` subsections are present, non-empty, and stay
  qualitative/descriptive rather than numeric weightings.
- `principle_emphasis` has all three required keys; every entry
  (`P0`, `P1`, `P2`, `P3`, `P9` emphasized; nothing deprioritized) matches
  `^P[0-9]+$`, no principle appears in both lists, and an empty
  `deprioritized` list is schema-valid.
- `P0` moving from baseline's `deprioritized` list into this context's
  `emphasized` list is a coherent, legible differentiation — the prose
  explicitly names it ("P0 (Goal Achievement) gains importance relative to
  baseline navigation"), consistent with a routine-delivery robot being
  "on duty" rather than an undifferentiated pedestrian.
- `limits.includes`/`limits.excludes` both present and consistent with the
  prose's "Includes"/"Excludes" lists.
- `related_contexts` (`baseline.public_navigation`, `emergency.high_urgency`,
  `workplace.formalized_service`) — the first two resolve to real context
  cards; `workplace.formalized_service` is a forward reference to a context
  not yet drafted. Logged to `project/design/backlog.md` rather than
  flagged here, consistent with how `guidance_docent` and
  `public_navigation`'s own forward references were handled.

Prose/YAML cross-checks (Context Summary, Context Axes Instantiated,
Relationship to Prosocial Navigation Principles, Applicability and Limits)
all agree with their corresponding YAML fields — no contradictions or drift.

## Completeness

All required sections (per `template.md`) are present and filled in:
Context Summary, Context Description, Normative Significance, Context Axes
Instantiated (all five subsections), Relationship to Prosocial Navigation
Principles, Applicability and Limits.

Optional-but-recommended sections are also filled in: Derived and Related
Contexts, Example Scenario Classes.
