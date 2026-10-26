---
execution_id: 2026_10_26_08_18_11_WI_CHARTER_SUPPLEMENT_GOLDEN_REGEN
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_GOLDEN_REGEN)[2026-10-26T08:17:37+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-10-26T08:18:11+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN.md
session_transcript: pending
---

# Summary

Create `WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN`, planning the regeneration of
`papers/01_charter/golden/rendered.tex` with a mandatory human
content-diff review, gated on three other work items landing first.

# Result

Wrote `project/work_items/proposed/WI-CHARTER-SUPPLEMENT-GOLDEN-REGEN.md`
(`status: proposed`, `depends_on: [WI-CHARTER-SUPPLEMENT-RENDERER-FIXES,
WI-CHARTER-SUPPLEMENT-TEST-COVERAGE, WI-CHARTER-SUPPLEMENT-PDF-BUILD]`),
grounded in the audit's concrete finding that the current golden file
predates PR #97's charter content (confirmed via stale P1 explanation
prose), so a naive regeneration would conflate defect fixes with unrelated
content drift. No golden files were changed by this item — it is planning
only.

# Validation

- `lrh prompt check-execution --slug wi-charter-supplement-golden-regen`
  — no prior record.
- `lrh validate` — 0 errors.

# Follow-up

Implementation is deferred to a later PR against this work item, and must
not start before its three dependencies land. This item stays `proposed`
at this PR's closeout.
