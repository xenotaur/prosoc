---
execution_id: 2026_11_06_21_38_30_WI_CHARTER_SUPPLEMENT_LIFECYCLE_STALE_DEMOTION
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_LIFECYCLE_STALE_DEMOTION)[2026-11-06T21:35:57+00:00]
work_item: AD_HOC
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/133
commit: 3f430773f974061a713b46f5043f8d5691a6301d
created_at: 2026-11-06T21:38:30+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Files `WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION`: demote the 9
charter-supplement cards found to carry `state: APPROVED` despite a real
content edit postdating their `audit.md`, down to `EDITED`.

# Result

Created `project/work_items/proposed/WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION.md`
with `type: operation`, `status: proposed`, no `depends_on` (first item
in the chain). The body cites the exact audit-date-vs-last-edit evidence
for each of the 9 cards, gathered via `git log` against `origin/main` in
this session, and explicitly excludes the 3 cards confirmed not stale.
This record covers only the work item's creation; the demotion itself is
future work.

# Validation

- `lrh validate` -- 0 errors (checked after all 4 work items and the
  workstream backfill were written together).

# Follow-up

Implementation of the actual demotion (editing the 9 cards' `state:`
fields, adding `EDITED` bullets, regenerating distilled YAML) is deferred
to whoever executes this work item next -- not performed as part of
filing it.
