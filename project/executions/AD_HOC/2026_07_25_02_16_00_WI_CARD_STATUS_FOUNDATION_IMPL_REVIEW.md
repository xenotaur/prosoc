---
execution_id: 2026_07_25_02_16_00_WI_CARD_STATUS_FOUNDATION_IMPL_REVIEW
prompt_id: PROMPT(AD_HOC:WI_CARD_STATUS_FOUNDATION_IMPL_REVIEW)[2026-07-25T02:14:01-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 2026_07_25_02_09_07_WI_CARD_STATUS_FOUNDATION
pr: https://github.com/xenotaur/prosoc/pull/40
commit: 
created_at: 2026-07-25T02:16:00-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/40
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Addressed three Copilot review comments on PR #40 (implementation of
WI-CARD-STATUS-FOUNDATION), all valid correctness/coverage findings.

`rerun_of` points at the **implementation** primary record
(`2026_07_25_02_09_07_...`, PR #40), not the earlier work-item-*creation*
primary (`2026_07_25_00_21_46_...`, PR #39): both share the slug
`WI_CARD_STATUS_FOUNDATION`, so the primary-record search matched both and was
disambiguated by `pr:` / bucket (cf. the known slug-collision gotcha).

# Result

**Thread 1** (`validate_status`, two issues) —
[r3649619395](https://github.com/xenotaur/prosoc/pull/40#discussion_r3649619395).
(a) In `--layout flat`, the per-scenario label used `md_path.parent.name`,
which is the `--root` directory in flat layout; changed to label by the
Markdown file stem for flat layout. (b) The `--fix` path could raise an
uncaught `ValueError` when the YAML `state` is unrecognised (it tried to
project an invalid state); it now reports a failure and continues, so the CLI
reliably returns non-zero.

**Thread 2** (`workflow.md` template) —
[r3649619404](https://github.com/xenotaur/prosoc/pull/40#discussion_r3649619404).
The Status Section Template called the Markdown `STATE` bullet "authoritative",
contradicting the fenced-YAML-is-authoritative contract stated below it and
enforced by `scripts/validate/status`. Reworded so the bullet is described as a
projection of the authoritative YAML `state`.

**Thread 3** (test coverage) —
[r3649619409](https://github.com/xenotaur/prosoc/pull/40#discussion_r3649619409).
Added regression tests for `--layout flat` (consistent + inconsistent) and for
`--fix` with an invalid YAML `state` (asserts non-zero exit and that the
Markdown STATE line is left untouched).

All three comments passed presence/validity/feasibility triage; nothing was
skipped.

# Validation

- `scripts/format --check`: clean.
- `scripts/lint`: All checks passed.
- `scripts/test`: 100 passed (+3 new regression tests).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 20 scenarios consistent.

# Follow-up

- Suggest `/lrh-confirm-fixes` on PR #40 before merge to resolve the three
  review threads.
