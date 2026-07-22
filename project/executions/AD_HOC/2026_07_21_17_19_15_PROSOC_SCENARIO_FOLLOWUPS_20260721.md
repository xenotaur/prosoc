---
execution_id: 2026_07_21_17_19_15_PROSOC_SCENARIO_FOLLOWUPS_20260721
prompt_id: PROMPT(AD_HOC:PROSOC_SCENARIO_FOLLOWUPS_20260721)[2026-07-21T17:19:04-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/28
commit: c2421b5f5890dbf00e07428acf10c733294956e5
created_at: 2026-07-21T17:19:15-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/28
session_transcript: claude-app:556d2127-e3d4-49e0-a746-95ad3c7a8f6e
---

# Summary

Retroactive execution record for [xenotaur/prosoc#28](https://github.com/xenotaur/prosoc/pull/28),
resolving the two follow-ups deferred from PR #27 (tracked in project
memory `project_scenario_corpus_followups`, not a formal work item): a
possible P0 (Goal Achievement) principles under-trim, and the
`related_scenarios`/`cited_in` schema-field backfill.

# Result

**P0 restoration (4 scenarios):** `intersection_gesture_proceed`,
`intersection_gesture_wait`, `pedestrian_overtaking`, and
`movable_obstruction` all had prose explicitly framing a goal-vs-social
tradeoff (e.g. `movable_obstruction`'s Discussion literally names
"Trade-offs between Goal Achievement (P0) and prosocial action"), so P0
was restored to `relevant_principles` in all four per the user's explicit
direction, even where it pushes a scenario's count past the 3-5 guidance.
Updated `.claude/skills/_shared/principles.md` and
`prosoc-scenario-audit`'s `audit_checklist.md` to make explicit that the
3-5 count is a soft guideline that yields to a principle the card's own
prose explicitly discusses.

**`related_scenarios`/`cited_in` backfill (13 scenarios):** transcribed
from each card's own STATUS `SOURCE` line and "Comparison with related
scenarios" Notes prose, linking only to scenarios that exist as corpus
directories (per the field's definition clarified in PR #27's
review-response round).

**Citation correction:** while backfilling `entering_room`/`exiting_room`,
traced "Robots@Games (R@G)" via `git log -S` to a single LLM-authored
scenario card with no verifiable citation, silently inherited afterward by
the shared `pg_scenarios.md` reference doc. Confirmed directly with the
project owner: R@G is "Robotics at Google," an internal scenario
reference. Corrected in both scenario cards and `pg_scenarios.md`.

`/lrh-review-response` was run against PR #28 and reported "Nothing to
resolve" (no open review comments) — no fix round was needed, so no
`_REVIEW` execution record exists for this PR.

# Validation

- `python3 -m pytest tests/`: 80/80 passing
- `python3 -m prosoc.scenarios.distill` (dry-run and applied): no
  unexpected diffs, all `scenario.yml` files in sync with their
  `scenario.md` embedded YAML
- `lrh validate`: 1 pre-existing error (`focus/current_focus.md` missing —
  known repo-wide gap, unrelated to this change; see project memory
  `project_lrh_scaffolding_status`)

# Follow-up

None. Both follow-ups tracked in `project_scenario_corpus_followups` are
now resolved.
