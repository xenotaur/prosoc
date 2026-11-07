---
family: tasks
card: deliver_object
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 0
audited: 2026-11-07
---

# Audit: Deliver an Object

- **Card:** `src/prosoc/prnc/tasks/deliver_object/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED with one open should-fix (dangling example
  scenarios)

## Findings

### 1. All three `example_scenarios` entries are dangling — should-fix
- **Section/field:** Example Scenarios (Non-Exhaustive) / `example_scenarios`
- **Issue:** Both the prose list and `example_scenarios` name
  `package_delivery_office`, `handoff_to_human_corridor`, and
  `pickup_and_deliver_shelf_to_desk` — consistent with each other, but none
  of the three resolves to a directory under `src/prosoc/prnc/scenarios/`
  (confirmed by listing that directory: it contains `object_handover` and
  `crash_cart`, among others, but no scenario with any of these three names).
  Per the audit checklist's Cross-Reference Sanity section, a dangling
  `example_scenarios` entry is a should-fix, not a reason for `not_ready` on
  its own — this corpus is known to have several, tracked separately per
  `PROP-NORMATIVE-PACKET-ASSEMBLY`'s Non-Goals.
- **Recommended fix:** Either author scenario cards under these three names
  (or similar), or replace the entries with existing scenario directories
  that actually exercise an object-delivery intent (e.g. `object_handover`
  or `crash_cart` look like plausible candidates worth checking against this
  task, though neither was verified here as a drop-in substitute).

## Completeness

All Required sections (per `template.md`) are present: Task Summary, Task
Description, Task Scope and Boundaries, Relationship to Prosocial Navigation
Principles. Both optional-but-recommended sections are populated.
`common_failure_modes` has four task-level entries that map 1:1 to the prose
Common Failure Modes list, including the "without external cause" /
"unjustified" qualifier on the abandonment entry. `example_scenarios` is
populated but all three entries are dangling — see Finding 1 (not a
completeness gap in the "blank field" sense, since the field itself is
filled in; tracked there instead).

The prose Excludes list's five bullets consolidate cleanly into the YAML's
four `scope.excludes` entries — "requesting/accepting/refusing" delivery and
"determining whether delivery is appropriate or authorized" merge into one
"social authorization or consent for delivery" bullet, a reasonable
paraphrase rather than an omission; the other three excludes entries, and
all three `scope.includes` entries (including "rerouting," which this card
does carry through to YAML, unlike its sibling `navigate_point_to_point`),
match the prose 1:1. `related_principles` (P0, P1, P2, P3, P9) matches the
five principles the "Relationship to Prosocial Navigation Principles"
section names explicitly; all five are valid P0–P9 IDs, at the upper end of
the 3–5 recommended count but each is explicitly discussed in the card's own
prose, which the principles-selection guidance treats as sufficient
justification to keep all five. `task_type: navigation` is an exact enum
match, and the card stays abstract throughout — no specific environment,
agent count, or social-setting content leaks into `scope`, `primary_intent`,
or the Task Description. `scope` has only `includes`/`excludes`, matching
`schema.json`'s `additionalProperties: false` constraint.

`scripts/distill/tasks --dry-run --show-diffs` (whole-family dry-run, no
per-card scoping available) produced **no diff and no schema validation
error** — nothing to report for this card, nor was any drift observed
affecting a different task card in the same run.

`VALIDATED: —` in the STATUS block is reasonably blank — this task has not
yet been supported by empirical evidence, and VALIDATED is an optional,
later lifecycle stage per `workflow.md`.
