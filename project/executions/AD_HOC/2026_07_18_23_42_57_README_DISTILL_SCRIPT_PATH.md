---
execution_id: 2026_07_18_23_42_57_README_DISTILL_SCRIPT_PATH
prompt_id: PROMPT(AD_HOC:README_DISTILL_SCRIPT_PATH)[2026-07-18T23:41:22-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/20
commit: 
created_at: 2026-07-18T23:42:57-04:00
agent: claude_app
instruction_source: ad hoc — README.md stale scripts/distill references, deferred from WI-SCENARIO-DISTILL-INVOCATION's design discussion as a separate doc-drift bug
session_transcript: pending
---

# Summary

Fix README.md's four stale `scripts/distill` references, which predate the
later split into per-content-type wrappers
(`scripts/distill/{charter,constitutions,contexts,scenarios,tasks}`) and no
longer work as documented.

# Result

Replaced all four `scripts/distill` occurrences with `scripts/distill/charter`
(the correct, working invocation for charter distillation specifically):
the charter-regeneration instructions, the dry-run preview command, the
scripts index entry, and the CI-failure resolution snippet. Added a one-line
note in the scripts index that sibling wrappers exist for the other content
types, since the new directory-scoped path would otherwise read as an
unexplained rename.

# Validation

- `scripts/distill/charter --dry-run --show-diffs` — runs clean, confirms
  the corrected command actually works.
- `scripts/lint` — "All checks passed!"
- `scripts/test` — 65 tests, 0 failures (no regression).
- `lrh validate` — only the known pre-existing, unrelated
  `focus/current_focus.md` error.

# Follow-up

- None — this closes the doc-drift bug flagged (and explicitly deferred) in
  WI-SCENARIO-DISTILL-INVOCATION's design discussion.
