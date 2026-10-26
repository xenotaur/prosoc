---
execution_id: 2026_10_26_08_18_10_WI_CARD_LIFECYCLE_VALIDATOR_AUDIT_CHECK
prompt_id: PROMPT(AD_HOC:WI_CARD_LIFECYCLE_VALIDATOR_AUDIT_CHECK)[2026-10-26T08:17:36+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-10-26T08:18:10+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK.md
session_transcript: pending
---

# Summary

Create `WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK`, planning an extension to
`scripts/validate/status` so it checks each card's `audit.md`
existence/verdict instead of the optional `AUDITED:` provenance bullet,
plus a charter-specific `Status:`-vs-`STATE` check.

# Result

Wrote `project/work_items/proposed/WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK.md`
(`status: proposed`), grounded in the audit's finding that `AUDITED: —`
is not itself evidence of a missing audit (the provenance bullet is
optional per `workflow.md:143`) while a sibling `audit.md` is the real
signal. No source files were edited by this item — it is planning only.

# Validation

- `lrh prompt check-execution --slug wi-card-lifecycle-validator-audit-check`
  — no prior record.
- `lrh validate` — 0 errors.

# Follow-up

Implementation is deferred to a later PR against this work item. This
item stays `proposed` at this PR's closeout.
