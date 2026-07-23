---
execution_id: 2026_07_22_21_39_06_SCENARIO_USAGE_GUIDE_GAP_20260722_REVIEW
prompt_id: PROMPT(AD_HOC:SCENARIO_USAGE_GUIDE_GAP_20260722_REVIEW)[2026-07-22T21:32:47-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/31
commit: 600a6a3
created_at: 2026-07-22T21:39:06-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/31
session_transcript: pending
---

# Summary

Address 2 open `copilot-pull-request-reviewer` comments on
[xenotaur/prosoc#31](https://github.com/xenotaur/prosoc/pull/31) (the
scenario_usage_guide gap closure + should-fix cleanup), via
`/lrh-review-response`.

# Result

Both comments flagged the same issue: the task/context cross-reference
added to `movable_obstruction/scenario.md`'s `evaluation_notes` used
uppercase snake-case IDs (`NAVIGATE_POINT_TO_POINT`, `DELIVER_OBJECT`,
`ROUTINE_DELIVERY`, `GUIDANCE_DOCENT`, `HIGH_URGENCY`) that don't match
prosoc's actual task/context ID format. Confirmed via
`prosoc/tasks/*/task.yml` and `prosoc/contexts/*/context.yml` that real
IDs are dot-delimited lowercase: `navigate.point_to_point`,
`deliver.object`, `service.routine_delivery`, `guidance.docent`,
`emergency.high_urgency`. Fixed both the new `evaluation_notes` addition
and the pre-existing Discussion section prose (the original, uncorrected
source of the same wrong IDs, copied forward into my new note) to use the
correct IDs.

No comments were skipped.

# Validation

- `git rev-parse HEAD` (pre-fix): `56350cfa4b3210adf3ef11a3a51db975ca0451a8`
- `scripts/version tools`: unavailable (no such script in this repo)
- `scripts/format --check --diff`: pass, 43 files unchanged
- `scripts/lint`: pass, all checks passed
- `scripts/test`: pass, 80 tests OK
- `lrh validate`: 1 pre-existing error (`focus/current_focus.md` missing --
  known repo-wide gap, unrelated to this change)

# Follow-up

None new.
