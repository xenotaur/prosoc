---
execution_id: 2026_10_28_06_26_28_WI_CARD_LIFECYCLE_VALIDATOR_AUDIT_CHECK
prompt_id: PROMPT(WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK:WI_CARD_LIFECYCLE_VALIDATOR_AUDIT_CHECK)[2026-10-28T00:20:20+00:00]
work_item: WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/114
commit:
created_at: 2026-10-28T06:26:28+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implement `WI-CARD-LIFECYCLE-VALIDATOR-AUDIT-CHECK`: extend
`scripts/validate/status` with two new checks (audit-evidence,
charter-only `Status:` line) on top of the unchanged STATE-vs-YAML
consistency check.

# Result

Added `check_audit_evidence` and `check_charter_status_line` to
`src/prosoc/nca/utils/cards/status.py`, wired into
`validate_status.py`'s per-card loop via a new `_check_extras` helper,
evaluated against the Markdown's current on-disk STATE (not addressed
by `--fix`). Added unit tests (`status_test.py`) and integration tests
through `validate_status.main` (`validate_status_test.py`), including a
fixture card missing `audit.md` at `APPROVED`. Updated one existing
sibling test (`tests/prnc/scenarios/validate_status_test.py`) whose
`--fix`-then-recheck assertion now legitimately needs an `audit.md`
fixture once its card reaches `APPROVED` on the recheck.

Caught and fixed two real bugs of my own via testing before pushing: (1)
the `check_charter_status_line` substring match failed for `DRAFTED`
("Draft" vs. "DRAFTED" token mismatch) — added a label-mapping table;
(2) my own test's premise conflicted with the deliberate
pre-fix-evaluation design — corrected the test rather than the
implementation, since the design matches the pre-existing
`test_fix_projects_then_passes` contract.

A pre-push self-review independently traced the branching logic, ran
empirical edge-case tests (missing STATE line, malformed/null-verdict
`audit.md`, `--fix` suppression) in a scratch directory, and verified
the full test/lint/validate suite itself. I independently re-verified
its two key claims myself — and in doing so caught my own mistake: I'd
used `python3 -I`, which ignores `PYTHONPATH` and silently fell back to
the stale global `prosoc` install, making my first re-check look like a
contradiction. Redone correctly (no `-I`), both claims held up: a null
verdict correctly fails (cosmetic `'None'`-string nitpick aside), and
`--fix` never suppresses the new checks.

Opened PR #114.

# Validation

- `scripts/test`: 281 tests, OK.
- `scripts/lint`: all checks passed.
- `lrh validate`: 0 errors, 20 pre-existing unrelated warnings.
- `scripts/validate/status` (full corpus): all 32 cards consistent.

# Follow-up

None outstanding for this item. The cosmetic null-verdict string
quirk (`'None'` vs. `None` in the failure message) is not worth a
corrective change — it doesn't affect pass/fail correctness.
