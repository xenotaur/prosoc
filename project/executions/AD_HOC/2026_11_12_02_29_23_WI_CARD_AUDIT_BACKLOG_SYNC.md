---
execution_id: 2026_11_12_02_29_23_WI_CARD_AUDIT_BACKLOG_SYNC
prompt_id: PROMPT(AD_HOC:WI_CARD_AUDIT_BACKLOG_SYNC)[2026-11-11T17:22:15+00:00]
work_item: AD_HOC
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/146
commit: 51cba60928edc665b54486b2d00dba09374c9ff2
created_at: 2026-11-12T02:29:23+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-AUDIT-BACKLOG-SYNC.md
session_transcript: claude-app:0a4099db-6380-4f7b-86e5-f652e0c70455
---

# Summary

`/lrh-work-item` session scoping backlog.md item #7: teach
`prosoc-card-audit`, `prosoc-card-review`, and `prosoc-card-review-all` to
append findings into backlog.md's three existing tracked tables, in
addition to each card's own self-contained `audit.md` — never replacing
it. This record covers the work item's *creation* only (planning, not
implementation), hence the `AD_HOC` bucket per the standing convention
that keeps a freshly created, not-yet-implemented item from being treated
as resolved when this planning PR merges.

# Result

Created `project/work_items/proposed/WI-CARD-AUDIT-BACKLOG-SYNC.md` with
full frontmatter and body (Summary, Problem/Context with a prior-art
duplication/demand search, Scope, Required Changes, Non-Goals, Acceptance
Criteria, Validation, Risk Notes). An earlier draft's wording ("instead of
(or in addition to)" noting a finding in the card's own `audit.md`) was
corrected, at the user's direction, to read unambiguously "in addition
to" throughout — Required Changes item 1, the Summary, the Acceptance
Criteria, and a new Non-Goal all make explicit that each card's `audit.md`
must stay self-contained and the backlog.md row is additive only.

Opened PR https://github.com/xenotaur/prosoc/pull/146. No related
workstream exists in this repo (all four existing workstreams are
`resolved/`), so Step 11's workstream-update offer does not apply.

# Validation

- `lrh validate` — 0 errors, 21 warnings (20 pre-existing across other
  files; the one new warning, `OWNER_NOT_IN_CONTRIBUTORS`, is expected
  and non-blocking, matching the pattern on other existing work items).

# Follow-up

None. Next step is `/lrh-land` (or manual review) on PR #146, followed by
`/lrh-implement WI-CARD-AUDIT-BACKLOG-SYNC` once the planning PR merges.
`session_transcript: pending` should be updated to the durable session
pointer when available.
