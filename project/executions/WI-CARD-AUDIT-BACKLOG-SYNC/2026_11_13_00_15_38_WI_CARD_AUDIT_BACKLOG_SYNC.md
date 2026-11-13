---
execution_id: 2026_11_13_00_15_38_WI_CARD_AUDIT_BACKLOG_SYNC
prompt_id: PROMPT(WI-CARD-AUDIT-BACKLOG-SYNC:WI_CARD_AUDIT_BACKLOG_SYNC)[2026-11-13T00:00:20+00:00]
work_item: WI-CARD-AUDIT-BACKLOG-SYNC
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/148
commit:
created_at: 2026-11-13T00:15:38+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-AUDIT-BACKLOG-SYNC.md
session_transcript: claude-app:0a4099db-6380-4f7b-86e5-f652e0c70455
---

# Summary

Implement `WI-CARD-AUDIT-BACKLOG-SYNC`'s six Required Changes: teach
`prosoc-card-audit`, `prosoc-card-review`, and `prosoc-card-review-all`
to append a row to the matching table in `project/design/backlog.md`
when they encounter a missing forward-referenced card, an APPROVED card
promoted with an unresolved finding, or a promotion with an open
suggestion — in addition to (never instead of) each card's own
self-contained `audit.md`.

# Result

Added `.claude/skills/prosoc-card-audit/SKILL.md` Step 6.5 (missing
forward-referenced card sync, with a `(missing id, referencing card)`
dedupe key); `.claude/skills/prosoc-card-review/SKILL.md` Step 6 promote
branch (APPROVED-unresolved and open-suggestion syncs, each with its own
dedupe key); and updated `.claude/skills/prosoc-card-audit-all/SKILL.md`
Step 8 and `.claude/skills/prosoc-card-review-all/SKILL.md` Step 7 commit
steps + Quality Checklists so a wrapped skill's backlog append is no
longer flagged as an unrelated sweep-in. `project/design/backlog.md`
itself was deliberately left unmodified — the WI's own Scope section
lists "any other backlog.md section" as out of scope, and no table row
changes until a skill actually runs against a real card; an earlier
draft's edit to the "Tooling" section was reverted after the self-review
pass below flagged it as a scope excursion.

A diff-mode `/lrh-self-review` pass (cold-context subagent, dispatched
before this PR's first push) found 3 should-fix findings: (1) Step 6.5's
trigger condition was mis-described for tasks' `example_scenarios` check
(lives in the checklist's separate "Cross-Reference Sanity" section,
never reached by Step 3's "Schema Compliance" wording, and checks the
`scenarios/` directory, not the task's own family directory) and never
fires for contexts' `related_contexts` (no such check exists in that
checklist today); (2) the backlog.md Tooling-section edit itself (scope
excursion, reverted); (3) inconsistent dedupe wording-tolerance between
the three tables. All three were independently re-verified directly
against the real checklist files and fixed before this push. Two
suggestion-level findings (malformed nested-backtick row-format
examples; a one-day-off date in the now-reverted Tooling note) were also
fixed/mooted.

# Validation

- `lrh validate`: 0 errors, 20 pre-existing warnings (none attributable
  to this PR's files).
- Confirmed via `git diff origin/main` that `project/design/backlog.md`
  has zero changes in this PR — every hand-authored row in all three
  tables is untouched, and no `audit.md` was touched.
- Scratch fixture walkthrough (two cases) of the promotion-table dedupe
  keys: (a) a repeat finding on the same card correctly produces no
  duplicate row; (b) a genuinely new finding on a different card
  correctly appends exactly one new row without disturbing existing
  ones.
- Cold-context self-review subagent pass (see `_SELFREVIEW` record,
  `rerun_of` set once this record's `execution_id` is known) — findings
  independently re-verified and fixed prior to push.

# Follow-up

None required by this WI's acceptance criteria. Noted in Non-Goals: the
skills append to backlog.md but still do not consult it before acting
(e.g. to skip re-flagging an already-tracked gap) — that remains
possible future work, not scoped here. Contexts' `related_contexts`
dangling-reference detection does not exist in the shared checklist
today, so the backlog sync added here cannot yet fire for that field;
adding that detection is out of this WI's stated `artifacts_expected`
scope.
