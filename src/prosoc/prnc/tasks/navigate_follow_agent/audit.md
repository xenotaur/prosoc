---
family: tasks
card: navigate_follow_agent
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 0
audited: 2026-11-07
---

# Audit: Follow an Agent

- **Card:** `src/prosoc/prnc/tasks/navigate_follow_agent/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED with one minor finding

## Findings

### 1. Dangling `example_scenarios` entry — should-fix
- **Section/field:** Example Scenarios (Non-Exhaustive) / `example_scenarios`
- **Issue:** `example_scenarios` lists `following` and `group_following_open_space`.
  `following` resolves to a real scenario directory
  (`src/prosoc/prnc/scenarios/following/`) and is a strong topical match.
  `group_following_open_space` has no matching directory under
  `src/prosoc/prnc/scenarios/` — no multi-agent/group-following scenario
  currently exists in the corpus.
- **Recommended fix:** Author a scenario covering group/multi-agent
  following, or replace the entry with an existing scenario directory that
  exercises this task, or explicitly log it as tracked backlog work (per
  `PROP-NORMATIVE-PACKET-ASSEMBLY`'s Non-Goals, this corpus is known to have
  dangling `example_scenarios` entries — not unique to this card, and not
  itself a blocker for `AUDITED`).

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
Scenarios) are populated — see Finding 1 for the one still-open content
issue (tracked, not blocking `AUDITED`).
