---
execution_id: 2026_10_26_08_18_10_WI_CHARTER_LIFECYCLE_DISPLAY_FIX
prompt_id: PROMPT(AD_HOC:WI_CHARTER_LIFECYCLE_DISPLAY_FIX)[2026-10-26T08:17:36+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-10-26T08:18:10+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-LIFECYCLE-DISPLAY-FIX.md
session_transcript: pending
---

# Summary

Create `WI-CHARTER-LIFECYCLE-DISPLAY-FIX`, planning a display-only fix to
the charter's stale `Status:` header and missing re-approval history
bullets — explicitly not a `state:` change.

# Result

Wrote `project/work_items/proposed/WI-CHARTER-LIFECYCLE-DISPLAY-FIX.md`
(`status: proposed`), grounded in the audit's finding that the charter's
`APPROVED` state is legitimately earned (PR #79, PR #97) and that only its
free-text header/history are stale. No source files were edited by this
item — it is planning only.

# Validation

- `lrh prompt check-execution --slug wi-charter-lifecycle-display-fix` —
  no prior record.
- `lrh validate` — 0 errors.

# Follow-up

Implementation is deferred to a later PR against this work item. This
item stays `proposed` at this PR's closeout.
