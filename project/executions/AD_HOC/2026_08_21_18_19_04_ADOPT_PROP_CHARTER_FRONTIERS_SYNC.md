---
execution_id: 2026_08_21_18_19_04_ADOPT_PROP_CHARTER_FRONTIERS_SYNC
prompt_id: PROMPT(AD_HOC:ADOPT_PROP_CHARTER_FRONTIERS_SYNC)[2026-08-21T18:16:18+00:00]
work_item: AD_HOC
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/100
commit: 
created_at: 2026-08-21T18:19:04+00:00
agent: claude_app
instruction_source: project/design/proposals/proposed/charter-frontiers-sync/00_proposal.md
session_transcript: claude-app:6efe0e72-8a38-4514-9b6b-98d6424e6149
---

# Summary

Adopted `PROP-CHARTER-FRONTIERS-SYNC` — the final loose end of the
charter/Frontiers-paper reconciliation effort, now that its
implementation (`WI-CHARTER-FRONTIERS-SYNC`, PR #97) is confirmed
merged and complete.

# Result

Edited the proposal's frontmatter: `status: proposed` → `adopted`,
`implementation_status: not_started` → `implemented`,
`implemented_by: [WI-CHARTER-FRONTIERS-SYNC]`, and updated
`related_design` from the pre-restructure `prosoc/charter/...` paths to
the current `src/prosoc/prnc/charter/...` paths. Moved the proposal
directory from `proposed/` to `adopted/`. No content changes — pure
control-plane bookkeeping.

# Validation

- `lrh validate` — 0 errors, 0 warnings.

# Follow-up

- None — this closes out the charter/Frontiers-paper reconciliation
  effort in full (PROP #92 → WI #94 → implementation #97 → this
  adoption).
