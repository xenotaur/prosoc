---
execution_id: 2026_10_27_06_40_09_WI_CHARTER_SUPPLEMENT_SOURCE_FIXES
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-SOURCE-FIXES:WI_CHARTER_SUPPLEMENT_SOURCE_FIXES)[2026-10-27T05:19:33+00:00]
work_item: WI-CHARTER-SUPPLEMENT-SOURCE-FIXES
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/112
commit: 906890aa1be2626ae2e886047e63ff09f21802b1
created_at: 2026-10-27T06:40:09+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-SOURCE-FIXES.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implement `WI-CHARTER-SUPPLEMENT-SOURCE-FIXES`: text-level fixes across
the 9 source cards included in the Frontiers charter supplement, plus
`papers/01_charter/README.md`'s stale import-path claim.

# Result

Applied all fixes from the work item's Required Changes: blank-line
fixes before Markdown lists following a label (across `navigate_point_to_point`,
`deliver_object`, `routine_delivery`, `guidance_docent`, `high_urgency`),
stale pre-restructure path corrections (`charter.md`,
`frontal_approach/scenario.md` — two locations, `movable_obstruction/scenario.md`),
a publication reword of `frontal_approach`'s `SOURCE:` field, removal of a
leaked `.claude/skills/...` path from two scenario cards' edit history
(historical fact preserved), `Context ID:`/`Applies To Tasks:` code-span
normalization in the 3 context cards, and the README import-path fix.

Deliberately left as-is: `frontal_approach/scenario.md`'s `blind_corner`
Related-Scenario reference — it's a real scenario elsewhere in the repo,
just not one of the 9 excerpted cards; removing it would corrupt real
corpus data to fix a presentation-only limitation.

A pre-push diff-mode `/lrh-self-review` pass caught one missed instance
of the stale-path fix (`frontal_approach/scenario.md`'s evaluation_notes
prose, "under prosoc/scenarios/."), which was fixed and re-verified before
this push. Opened PR #112.

# Validation

- `lrh validate`: 0 errors, 20 pre-existing unrelated warnings.
- `scripts/lint`: all checks passed.
- `scripts/test`: 259 tests, OK.
- `papers/01_charter/render.py`: exit 0; all 9 fragments + `rendered.tex`
  render cleanly; confirmed via grep on the fresh output that no
  collapsed-list pattern remains.

# Follow-up

None outstanding for this item. `blind_corner` dangling-reference
resolution (if ever wanted) belongs to a renderer/template-level fix, not
a source-text change — not scoped to any existing work item.
