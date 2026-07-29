---
execution_id: 2026_07_29_04_01_39_WI_CARD_STATUS_CHARTER_IMPL_REVIEW
prompt_id: PROMPT(AD_HOC:WI_CARD_STATUS_CHARTER_IMPL_REVIEW)[2026-07-29T04:01:39-04:00]
work_item: AD_HOC
status: landed
rerun_of: 2026_07_29_03_55_40_WI_CARD_STATUS_CHARTER
pr: https://github.com/xenotaur/prosoc/pull/49
commit: 592204f478a9b7d7f52dbb14ef71660a258a167d
created_at: 2026-07-29T04:01:39-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/49
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Addressed two Copilot review comments on PR #49 (implementation of
WI-CARD-STATUS-CHARTER). `rerun_of` points at the implementation primary
(`2026_07_29_03_55_40_WI_CARD_STATUS_CHARTER`).

# Result

Both comments passed presence/validity/feasibility triage; both applied.

1. [comment on `validate_status.py`] — the single-source charter family was
   labelled by `source.md_path.parent.name`, so under a `--root` whose directory
   is not named `charter` the reported card id (and `--card` filtering) tracked
   the root dir name instead of a stable id. Added a `label_by_stem` flag to
   `Family` (set for charter) and taught `_label` to use the Markdown file stem
   for single-source families. `--card charter` now matches under any root.
2. [comment on `distill_test.py`] — `schema_with_state()`'s enum omitted
   `DEPRECATED`/`RETIRED`. Aligned it with the canonical lifecycle states
   (`prosoc/charter/schema.json` / `prosoc.utils.cards.status.STATES`).

Added a regression test (`test_card_id_is_stem_not_root_dir_name`) covering the
label fix.

# Validation

- `scripts/test` / pytest: 148 passed (+1 regression test).
- `scripts/lint`: All checks passed.
- `scripts/format --check` (black 25.12.0): clean.
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 31 cards consistent; `--family charter --card
  charter`: consistent.

# Follow-up

- `/lrh-confirm-fixes` on PR #49 to verify against the live diff and resolve the
  two review threads before merge.
