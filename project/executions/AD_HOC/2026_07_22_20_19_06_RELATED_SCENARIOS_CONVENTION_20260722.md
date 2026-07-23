---
execution_id: 2026_07_22_20_19_06_RELATED_SCENARIOS_CONVENTION_20260722
prompt_id: PROMPT(AD_HOC:RELATED_SCENARIOS_CONVENTION_20260722)[2026-07-22T20:14:51-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/30
commit: 2dc660fe0a3b319893dde54cbdb01c2178b2db42
created_at: 2026-07-22T20:19:06-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/30
session_transcript: claude-app:556d2127-e3d4-49e0-a746-95ad3c7a8f6e
---

# Summary

Retroactive execution record for [xenotaur/prosoc#30](https://github.com/xenotaur/prosoc/pull/30),
a follow-up to PR #29's review-response round: document the
`related_scenarios`/P&G Table 3 divergence convention that PR #29 had to
work out ad hoc for `crash_cart`/`join_a_group`/`leading`, and make every
affected scenario card self-contained.

# Result

Re-derived the full picture across all 20 scenarios (rather than trust
`AUDIT_SUMMARY.md`'s partial 9-scenario list) and found three distinct
sub-patterns affecting 18 of 20 scenarios:

- **Pattern A (13 scenarios)** — Table 3 names an unimplemented sibling
  scenario (the most common case), and the card substitutes an implemented
  one it actually discusses instead: `frontal_approach`,
  `pedestrian_overtaking`, `narrow_doorway`, `entering_room`,
  `exiting_room`, `join_a_group`, `following`, `leading`,
  `crowd_navigation`, `parallel_traffic`, `perpendicular_traffic`,
  `object_handover`, `crash_cart`.
- **Pattern B (2 scenarios)** — Table 3's named scenario is implemented and
  included, but the card adds further cross-references beyond it:
  `intersection_gesture_proceed`, `intersection_gesture_wait`.
- **Pattern C (3 scenarios)** — Table 3 lists no related scenario at all,
  but the card adds one anyway: `blind_corner`, `robot_overtaking`,
  `intersection_no_gesture`.

Added a checklist entry to `prosoc-scenario-audit`'s `audit_checklist.md`
documenting all three patterns as expected, not a source-fidelity defect.
Added a "Related Scenarios note" to `evaluation_notes` in all 18 affected
scenarios, naming the specific Table 3 citation and why the card's
`related_scenarios` value diverges, so each card is self-contained.

`/lrh-review-response` was run against PR #30 and reported "Nothing to
resolve" (no open review comments) — no fix round was needed, so no
`_REVIEW` execution record exists for this PR, matching the pattern from
PR #28.

# Validation

- `python3 -m pytest tests/`: 80/80 passing
- `python3 -m prosoc.scenarios.distill` (dry-run and applied): no
  unexpected diffs, all `scenario.yml` files in sync
- `scripts/format --check --diff` / `scripts/lint`: clean
- `lrh validate`: 1 pre-existing error (`focus/current_focus.md` missing —
  known repo-wide gap, unrelated to this change)

# Follow-up

None. This closes out the `related_scenarios`/Table 3 convention
follow-up flagged during PR #29's review-response round.
