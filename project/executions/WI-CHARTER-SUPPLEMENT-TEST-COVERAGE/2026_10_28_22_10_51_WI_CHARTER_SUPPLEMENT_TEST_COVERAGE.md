---
execution_id: 2026_10_28_22_10_51_WI_CHARTER_SUPPLEMENT_TEST_COVERAGE
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-TEST-COVERAGE:WI_CHARTER_SUPPLEMENT_TEST_COVERAGE)[2026-10-28T20:44:22+00:00]
work_item: WI-CHARTER-SUPPLEMENT-TEST-COVERAGE
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/116
commit: e170c7d649037899657cde30384bd3022f8184a8
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
created_at: 2026-10-28T22:10:51+00:00
---

# Summary

Implements WI-CHARTER-SUPPLEMENT-TEST-COVERAGE: regression tests for the
charter supplement's known defect classes from
`project/audits/2026-10-26_charter_supplement_pipeline_audit.md` —
collapsed-list formatting, heading double-numbering, YAML semantic
round-trip, and context-identifier survival.

# Result

Added two new test classes to `tests/nca/utils/papers/render_test.py`
(`TestListCollapseRegression`, `TestHeadingNumberRegression`) and created
`tests/nca/utils/papers/paper_semantics_test.py` with
`TestYamlSemanticRoundTrip` and `TestIdentifierSurvival`. All four run
real pandoc against the real in-paper source cards (not fakes).

PDF-level checks described in the WI's Scope section (compiled-PDF
heading-number count, PDF-text identifier survival) are deferred —
consistent with WI-CHARTER-SUPPLEMENT-RENDERER-FIXES's prior narrowing,
since this sandbox has no `pdflatex` and installing one needs interactive
`sudo` that isn't available here. LaTeX-fragment-level equivalents were
substituted; the real PDF round-trip remains tracked under
WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION.

`/lrh-self-review` diff-mode ran before this PR's first push (correcting
the ordering slip from the prior round) — see
`project/executions/AD_HOC/2026_10_28_22_09_34_WI_CHARTER_SUPPLEMENT_TEST_COVERAGE_SELFREVIEW.md`.
0 findings; the subagent's top claim (list-collapse test is genuinely
non-vacuous) was independently re-verified by directly re-rendering the
pre-fix source.

PR: https://github.com/xenotaur/prosoc/pull/116

# Validation

- `PYTHONPATH="$(pwd)/src" scripts/test` — 308 tests, OK
- `lrh validate` — 0 errors
- `black --check` on both changed files — clean
- `/lrh-self-review` diff-mode — 0 findings, top finding independently re-verified

# Follow-up

None for this WI. The deferred PDF-level verification is tracked separately
under WI-CHARTER-SUPPLEMENT-RENDERER-PDF-VERIFICATION (currently blocked on
its own readiness gap — missing Required Changes section).
