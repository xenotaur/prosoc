---
family: tasks
card: navigate_point_to_point
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-11-07
---

# Audit: Navigate from Start to Goal

- **Card:** `src/prosoc/prnc/tasks/navigate_point_to_point/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED, no blocking, should-fix, or suggestion
  findings.

This is a fresh audit written after `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`
resolved the prior audit's should-fix finding (Scope prose/YAML one-sided
claims for "rerouting" and "politeness"). It does not carry forward that
finding's text, since the YAML content it described no longer exists.

## Findings

### Resolved: Scope prose mentioned "rerouting" and "politeness" that the YAML scope omitted

The prior audit's should-fix finding is resolved. `scope.includes` now adds
"rerouting toward the destination," and `scope.excludes` now reads
"optimization for social comfort, legibility, or politeness beyond goal
completion" — both now enumerate the exact behaviors the prose Scope and
Boundaries section already named. Re-distilled
(`scripts/distill/tasks --dry-run --show-diffs`, whole-family, reports no
differences — re-run fresh for this audit with the correct `PYTHONPATH`
for this checkout) and schema-validated clean.

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
