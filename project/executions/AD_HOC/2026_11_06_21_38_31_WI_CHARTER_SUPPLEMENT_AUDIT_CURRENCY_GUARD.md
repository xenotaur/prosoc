---
execution_id: 2026_11_06_21_38_31_WI_CHARTER_SUPPLEMENT_AUDIT_CURRENCY_GUARD
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_AUDIT_CURRENCY_GUARD)[2026-11-06T21:35:58+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-11-06T21:38:31+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Files `WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD`: add a git-history (or
equivalent durable-signal) audit-currency check to
`scripts/validate/status`, so an `APPROVED`/`AUDITED` card whose source
postdates its audit evidence is caught automatically going forward.

# Result

Created `project/work_items/proposed/WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD.md`
with `type: deliverable`, `status: proposed`, no `depends_on` (runs
independently of the other 3 items). Confirmed `check_audit_evidence`
(`src/prosoc/nca/utils/cards/status.py:201-237`) has no staleness check
today, and explicitly called out that a naive commit-timestamp
comparison would false-positive on the 3 cards this workstream confirmed
are backfill-only, not stale (`routine_delivery`, `guidance_docent`,
`public_navigation`) -- any implementation must distinguish the two
cases. Filed separately rather than bundled into the repair, per the
originating review's own instruction not to broaden the fix unilaterally.
This record covers only the work item's creation; design and
implementation of the check are future work.

# Validation

- `lrh validate` -- 0 errors (checked after all 4 work items and the
  workstream backfill were written together).

# Follow-up

The hard part -- distinguishing a genuine post-audit content edit from a
provenance-only backfill reliably -- needs its own design pass before
implementation; the work item's Risk Notes flag this explicitly and ask
that any approach beyond a straightforward timestamp comparison be
confirmed with the user first.
