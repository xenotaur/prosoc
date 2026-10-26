---
execution_id: 2026_10_26_08_18_10_WI_CHARTER_SUPPLEMENT_TEST_COVERAGE
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_TEST_COVERAGE)[2026-10-26T08:17:37+00:00]
work_item: AD_HOC
status: in_progress
rerun_of:
pr:
commit:
created_at: 2026-10-26T08:18:10+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-TEST-COVERAGE.md
session_transcript: pending
---

# Summary

Create `WI-CHARTER-SUPPLEMENT-TEST-COVERAGE`, planning regression tests
for the list-collapse, heading-number, YAML-round-trip, and
identifier-survival defect classes found in the pipeline audit.

# Result

Wrote `project/work_items/proposed/WI-CHARTER-SUPPLEMENT-TEST-COVERAGE.md`
(`status: proposed`), explicitly keying the list-collapse test on a
pattern (not a literal bolded string) per the audit's finding that the
originally-proposed test would miss unbolded cases, and noting that
`test_rejects_unresolved_placeholders` already exists and shouldn't be
duplicated. No test files were written by this item — it is planning only.

# Validation

- `lrh prompt check-execution --slug wi-charter-supplement-test-coverage`
  — no prior record.
- `lrh validate` — 0 errors.

# Follow-up

Implementation is deferred to a later PR against this work item. This
item stays `proposed` at this PR's closeout.
