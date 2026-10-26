---
execution_id: 2026_10_26_08_18_09_WI_CHARTER_SUPPLEMENT_SOURCE_FIXES
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_SOURCE_FIXES)[2026-10-26T08:17:36+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-10-26T08:18:09+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-SOURCE-FIXES.md
session_transcript: pending
---

# Summary

Create `WI-CHARTER-SUPPLEMENT-SOURCE-FIXES`, planning the text-level fixes
to the charter supplement's 9 source cards (collapsed lists, stale paths,
leaked internal references, identifier formatting, stale README path).

# Result

Wrote `project/work_items/proposed/WI-CHARTER-SUPPLEMENT-SOURCE-FIXES.md`
(`status: proposed`), scoped and cited to specific files/lines found in
`project/audits/2026-10-26_charter_supplement_pipeline_audit.md`, and
linked under `WS-CHARTER-SUPPLEMENT-PIPELINE`. No source files were edited
by this item — it is planning only.

# Validation

- `lrh prompt check-execution --slug wi-charter-supplement-source-fixes` —
  no prior record.
- `lrh validate` — 0 errors.

# Follow-up

Implementation (the actual edits) is deferred to a later PR against this
work item. Per this repo's planning-only-PR convention, this item stays
`proposed` at this PR's closeout.
