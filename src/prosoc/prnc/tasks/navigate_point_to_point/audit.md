---
family: tasks
card: navigate_point_to_point
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 0
audited: 2026-11-07
---

# Audit: Navigate from Start to Goal

- **Card:** `src/prosoc/prnc/tasks/navigate_point_to_point/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED with one minor wording fix

## Findings

### 1. Scope prose mentions "rerouting" and "politeness" that the YAML scope omits — should-fix
- **Section/field:** Task Scope and Boundaries vs. `scope.includes` / `scope.excludes`
- **Issue:** The prose Includes list names "slowing, stopping, **or rerouting**
  in service of reaching the goal," but `scope.includes` only has "progressing
  toward a destination," "pausing or stopping temporarily while pursuing the
  goal," and "resuming motion toward the goal after interruption" — rerouting
  has no explicit counterpart. Symmetrically, the prose Excludes list names
  "Optimizing for comfort, legibility, **or politeness** beyond what is
  required to reach the destination," but the matching `scope.excludes` entry
  reads "optimization for social comfort or legibility beyond goal
  completion" — "politeness" is dropped. Neither is a contradiction (the
  surrounding YAML entries are broad enough to arguably cover both), but both
  are one-sided claims per the audit checklist's Prose/YAML Cross-Checks
  guidance.
- **Recommended fix:** Add "rerouting toward the destination" to
  `scope.includes`, and restore "politeness" (or an equivalent "comfort,
  legibility, or politeness" phrasing) to `scope.excludes`, so the YAML
  enumerates the same behaviors the prose calls out by name.

## Completeness

All Required sections (per `template.md`) are present: Task Summary, Task
Description, Task Scope and Boundaries, Relationship to Prosocial Navigation
Principles. Both optional-but-recommended sections are populated:
`common_failure_modes` has four task-level entries that map 1:1 to the prose
Common Failure Modes list (including the "without external cause" /
"unjustified" qualifier), and `example_scenarios` lists three entries
(`frontal_approach`, `intersection_no_gesture`, `pedestrian_overtaking`), all
three of which resolve to real scenario directories under
`src/prosoc/prnc/scenarios/` — no dangling references.

`related_principles` (P0, P1, P2, P3) matches the principles the
"Relationship to Prosocial Navigation Principles" section names by number
(P0 directly, P1–P3 as the principles P0 is in tension with); all four are
valid P0–P9 IDs and within the 3–5 recommended count. `task_type: navigation`
is an exact enum match. The card stays abstract throughout — no specific
environment, agent count, or social setting leaks into `scope`,
`primary_intent`, or the Task Description; this is itself stated as a design
goal in the card's own closing "Notes for Task Designers and Evaluators."
`scope` has only `includes`/`excludes`, matching `schema.json`'s
`additionalProperties: false` constraint.

`scripts/distill/tasks --dry-run --show-diffs` (whole-family dry-run, no
per-card scoping available) produced **no diff and no schema validation
error** — nothing to report for this card, nor was any drift observed
affecting a different task card in the same run.

`VALIDATED: —` in the STATUS block is reasonably blank — this task has not
yet been supported by empirical evidence, and VALIDATED is an optional,
later lifecycle stage per `workflow.md`.
