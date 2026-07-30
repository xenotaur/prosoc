---
execution_id: 2026_07_30_02_48_01_FIX_ATOMIC_WRITE_SHOW_DIFFS_MISSING_FILE_REVIEW
prompt_id: PROMPT(AD_HOC:FIX_ATOMIC_WRITE_SHOW_DIFFS_MISSING_FILE_REVIEW)[2026-07-30T02:48:01-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 2026_07_30_02_44_48_FIX_ATOMIC_WRITE_SHOW_DIFFS_MISSING_FILE
pr: https://github.com/xenotaur/prosoc/pull/57
commit: 
created_at: 2026-07-30T02:48:01-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/57
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Addressed one Copilot review comment on PR #57 (fix for the
`atomic_write`/`show_diffs` crash). `rerun_of` points at the implementation
primary (`2026_07_30_02_44_48_FIX_ATOMIC_WRITE_SHOW_DIFFS_MISSING_FILE`).

# Result

Passed presence/validity/feasibility triage; applied.

1. [`prosoc/literate/utils.py`] — the initial fix used `path.exists()` to
   decide whether to treat the target as missing, which would silently
   swallow a genuine `PermissionError` (or other stat-time `OSError`) on an
   *existing but unreadable* file as if it were simply new, producing a
   misleading empty-baseline diff instead of surfacing the real I/O problem.
   Replaced with a `try: path.read_text() except FileNotFoundError:
   old_text = ""` — only the specific "does not exist" case falls back to
   empty; every other read failure (permissions, etc.) still propagates as
   before. Updated the docstring to state this explicitly. Added a
   regression test (`test_show_diffs_permission_error_on_existing_file_
   propagates`) that mocks `Path.read_text` to raise `PermissionError` and
   asserts it still propagates through `atomic_write`.

# Validation

- pytest (`tests/literate/utils_test.py`): 11 passed (+1 for the new
  permission-error regression test).
- `scripts/test`: 200 passed overall.
- `scripts/lint`, `scripts/format --check`, `lrh validate`: all clean.

# Follow-up

- `/lrh-confirm-fixes` on PR #57 to verify against the live diff and resolve
  the review thread before merge.
