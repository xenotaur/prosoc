---
execution_id: 2026_07_05_12_35_29_FORMAT_SCRIPT_ARGS_FIX
prompt_id: PROMPT(AD_HOC:FORMAT_SCRIPT_ARGS_FIX)[2026-07-05T12:35:29-04:00]
work_item: AD_HOC
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/5
commit: 77b9d0f8038abea1a688f7f889c7d9a3cf180138
created_at: 2026-07-05T12:35:29-04:00
agent: claude_app
instruction_source: ad_hoc conversation - user asked to fix scripts/format so --check/--diff behave as a real dry-run, per the bug flagged in the PR #3 execution record
session_transcript: claude-app:028f5db7-057b-4fbb-b4b5-38d9d9675bdc
---

# Summary

`scripts/format` was a one-line wrapper (`black prosoc tests`) that ignored
all CLI arguments, so `scripts/format --check --diff` — the canonical
validation invocation documented in `.claude/skills/*/SKILL.md` — silently
reformatted files in place instead of doing a non-destructive dry-run. This
was previously flagged as a known issue in the PR #3 execution record
(`2026_07_05_02_35_33_PROSOC_AUDIT_SCENARIO_SKILL.md`), where it had bitten a
prior session twice, reformatting 14 unrelated pre-existing files that then
had to be reverted with `git checkout --`.

# Result

- Changed `scripts/format` to forward `"$@"` to black
  (`black prosoc tests "$@"`), so `--check`/`--diff` are actually passed
  through instead of being silently dropped.
- Opened and merged PR #5.

# Validation

- `scripts/format --check --diff` now correctly reports the 14 pre-existing
  files that would reformat, without writing to any of them (`git status`
  stays clean after running it).
- Plain `scripts/format` (no args) is unaffected, since an empty `"$@"` is a
  no-op passthrough — it still reformats in place as before.

# Follow-up

- None. The 14 pre-existing files that `black` still flags as needing
  reformatting remain out of scope for this change.
