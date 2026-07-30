---
execution_id: 2026_07_30_02_44_48_FIX_ATOMIC_WRITE_SHOW_DIFFS_MISSING_FILE
prompt_id: PROMPT(AD_HOC:FIX_ATOMIC_WRITE_SHOW_DIFFS_MISSING_FILE)[2026-07-30T02:28:41-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/57
commit: 
created_at: 2026-07-30T02:44:48-04:00
agent: claude_app
instruction_source: user request following WI-PACKET-MANIFEST-FAMILY (PR #56) closeout
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Fixed a pre-existing bug in `prosoc.literate.utils.atomic_write`: with
`show_diffs=True` it unconditionally read the target path for the diff,
raising `FileNotFoundError` on any card's very first distill (before its
`.yml` exists). Found while implementing WI-PACKET-MANIFEST-FAMILY (PR #56)
and deferred there as out of that WI's scope; addressed here as its own
small standalone ad-hoc chore, not a tracked work item.

# Result

- `prosoc/literate/utils.py`: `atomic_write`'s `show_diffs` branch now treats
  a missing target path as an empty diff baseline (`old_text = ""`) rather
  than crashing — the whole of the new content shows as additions, mirroring
  the pattern `prosoc/charter/distill.py` already implements manually
  (its own `if DEFAULT_CHARTER_YML.exists(): ... else: old_yaml = ""` before
  calling `utils.unified_diff` directly). Updated the docstring to document
  this behavior. No other `atomic_write` behavior changed.
- Confirmed this bug was repo-wide, not manifests-specific: all five family
  distillers (`scenarios`, `tasks`, `contexts`, `constitutions`,
  `manifests`) pipe their CLI `--show-diffs` flag straight into
  `atomic_write`, so any of them would hit it on a brand-new card's first
  `--show-diffs` run. It never surfaced before because every checked-in card
  had already been distilled once (a plain run, no `--show-diffs`) prior to
  anyone trying `--show-diffs` on it.
- `tests/literate/utils_test.py`: added three regression tests —
  `show_diffs` on a new file no longer raises and diffs against an empty
  baseline; the existing-file diff path is separately guarded to confirm the
  real-content-baseline case is unaffected.

Reproduced the crash directly against `main` before fixing, and confirmed it
is gone afterward (same repro, no exception).

# Validation

- `scripts/test`: 199 passed (+3, no regressions elsewhere).
- `scripts/lint`: All checks passed.
- `scripts/format --check` (black 25.12.0): clean (71 files unchanged — same
  file count as before; this PR only modifies two existing files).
- `lrh validate`: 0 errors, 0 warnings.
- Manual repro: `utils.atomic_write(<new-path>, ..., show_diffs=True,
  dry_run=True)` against a path that does not exist — raised
  `FileNotFoundError` before the fix, does not raise after.

# Follow-up

- None — this was itself the deferred follow-up noted in
  WI-PACKET-MANIFEST-FAMILY's execution record.
