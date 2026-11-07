---
family: tasks
card: navigate_follow_agent
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-11-07
---

# Audit: Follow an Agent

- **Card:** `src/prosoc/prnc/tasks/navigate_follow_agent/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED, no blocking, should-fix, or suggestion
  findings.

This is a fresh audit written after confirming the prior audit's should-fix
finding (dangling `example_scenarios` entry) is already tracked as a
known, open gap in `project/design/backlog.md`, consistent with that
file's own stated policy for this exact class of finding (the same basis
already applied to `tasks/deliver_object`'s audit this session).

## Findings

### Resolved: Dangling `example_scenarios` entry, but already tracked

**Verified:** `group_following_open_space` still has no matching directory
under `src/prosoc/prnc/scenarios/` — re-confirmed fresh for this audit,
unchanged from the prior pass. It is already listed in
`project/design/backlog.md`'s "Missing forward-referenced cards" table
(entry dated 2026-08-02, status `open`, referenced by
`tasks/navigate_follow_agent`'s `example_scenarios`) — not a new finding
this audit is surfacing. `following` (the other `example_scenarios` entry)
continues to resolve to a real, strong-match scenario directory.

Per `project/design/backlog.md`'s own stated policy, a dangling
`example_scenarios` entry that is already tracked in the backlog does not
warrant a should-fix on this card specifically — the gap is the missing
sibling scenario's absence, not an error in `navigate_follow_agent` itself.
No new backlog entry was needed — the entry already existed.

## Prose/YAML Consistency

Task Summary, Task Description, and Task Scope and Boundaries all align
cleanly with `task_type`, `primary_intent`, `summary`, and
`scope.{includes,excludes}` — the Scope section's includes/excludes bullets
map list-for-list onto the YAML arrays. Relationship to Prosocial Navigation
Principles names P0, P2, P3, P6 in prose, matching
`related_principles: [P0, P2, P3, P6]` exactly. Common Failure Modes
(Task-Level) lists four bullets that map 1:1 onto the four
`common_failure_modes` YAML entries — no omissions or contradictions found.

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
  Description, consistent with the schema's "abstract robot intents" framing
  and `template.md`'s "avoid geometric layouts, agent counts, or social
  norms" instruction.
- `common_failure_modes` entries are task-level (independent of social
  context) — none are really scenario- or context-specific.

## Completeness

All Required sections present and filled: Task Summary, Task Description,
Task Scope and Boundaries, Relationship to Prosocial Navigation Principles.
Both optional-but-recommended sections (Common Failure Modes, Example
Scenarios) are populated — see the resolved finding above for the one
already-tracked content issue (not blocking `AUDITED`).
