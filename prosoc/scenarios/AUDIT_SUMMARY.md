# Scenario Audit Summary

- **Run date:** 2026-07-20
- **Branch:** claude/prosoc-audit-status-c64c15
- **Scenarios audited:** 20 (0 skipped)

This is a point-in-time index, not a live report — each scenario's own
`audit.md` is the source of truth for full findings detail. Re-running the
audit against a scenario does not automatically update this file; regenerate
it by hand (or via a future batch-audit skill) after any re-audit.

No scenario's `scenario.md`, `scenario.yml`, or STATUS/STATE block was
modified in producing these audits, and no scenario STATE was promoted —
that remains a human decision per [workflow.md](workflow.md).

This run follows a manual editing pass (this same session) that rendered
missing Card Summary/Usage Guide sections, trimmed over-long
`relevant_principles` lists, authored previously-missing fields
(`scientific_purpose`, `geometric_layout`, `intended_robot_task`,
`intended_human_behavior`, `ideal_outcome`, and for two scenarios the entire
`scenario_usage_guide`) grounded in the P&G Table 3 reference where
available, and fixed a handful of small prose/YAML issues across all 20
scenarios. The prior snapshot (2026-07-05) is superseded by this one.

## Results

| Scenario | Verdict | Blocking | Should-fix | Suggestion |
|---|---|---|---|---|
| blind_corner | ready | 0 | 0 | 1 |
| crash_cart | ready_with_fixes | 0 | 1 | 1 |
| crowd_navigation | ready_with_fixes | 0 | 1 | 0 |
| entering_room | ready_with_fixes | 0 | 1 | 1 |
| exiting_room | ready_with_fixes | 0 | 1 | 1 |
| following | ready_with_fixes | 0 | 1 | 0 |
| frontal_approach | ready_with_fixes | 0 | 2 | 2 |
| intersection_gesture_proceed | ready_with_fixes | 0 | 1 | 2 |
| intersection_gesture_wait | not_ready | 1 | 1 | 2 |
| intersection_no_gesture | not_ready | 1 | 0 | 3 |
| join_a_group | ready_with_fixes | 0 | 1 | 1 |
| leading | ready_with_fixes | 0 | 1 | 0 |
| movable_obstruction | ready_with_fixes | 0 | 1 | 1 |
| narrow_doorway | ready | 0 | 0 | 2 |
| object_handover | ready_with_fixes | 0 | 2 | 1 |
| parallel_traffic | ready_with_fixes | 0 | 2 | 1 |
| pedestrian_overtaking | ready | 0 | 0 | 2 |
| perpendicular_traffic | ready_with_fixes | 0 | 1 | 1 |
| robot_overtaking | ready_with_fixes | 0 | 1 | 2 |
| single_file_hallway | ready_with_fixes | 0 | 1 | 1 |

**Totals:** 20 scenarios, 3 `ready`, 15 `ready_with_fixes`, 2 `not_ready`.
2 blocking, 19 should-fix, 25 suggestion findings.

Compared to the 2026-07-05 snapshot: 16 blocking findings resolved down to 2
(both are the same root cause — `scenario_usage_guide` still entirely absent
from `intersection_gesture_wait` and `intersection_no_gesture`'s
machine-readable YAML, which was out of scope for this session's editing
pass), and the not-ready count dropped from 12 to 2.

## Recurring Patterns

These findings were extracted mechanically by exact-matching each finding's
normalized title (per this skill's Step 6 rule) across scenarios. Because
this run dispatched one subagent per scenario pair in parallel, semantically
identical findings were frequently worded differently by different
subagents — so the strict exact-match rule under-counts here. Both the
mechanical result and a manual reading are given below.

**Mechanical (exact-title match, threshold 3): none found.** The closest
mechanical matches were pairs, not triples:
- "`scenario_usage_guide` block still entirely missing from YAML" —
  `intersection_gesture_wait`, `intersection_no_gesture` (2 scenarios)
- Several near-identical "Related Scenarios / Cited In" titles, each shared
  by exactly 2 scenarios (see manual reading below for why this fragmented).

**Manual reading — two patterns worth a single decision rather than
per-scenario fixes:**

1. **`related_scenarios` / `cited_in` left blank despite the schema fields
   now existing.** This is by far the most common finding in this run,
   appearing under many different exact wordings in at least 13 of 20
   scenarios (blind_corner, crash_cart, crowd_navigation, entering_room,
   exiting_room, following, frontal_approach, join_a_group, leading,
   narrow_doorway, object_handover, parallel_traffic, perpendicular_traffic).
   The schema fields were added this session (see `schema.json`), but
   backfilling actual values — cross-referencing which scenarios are
   genuinely related, and transcribing citation indices already sitting in
   `evaluation_notes`/STATUS/Notes prose — is exactly the kind of
   research-judgment task flagged as future work in this session's editing
   pass. Worth a dedicated pass across the whole corpus rather than
   scenario-by-scenario, since the source material (prose already
   mentioning related scenarios, STATUS block citations) is usually already
   sitting in each card.
2. **P0 (Goal Achievement) may have been under-trimmed out of
   `relevant_principles`.** Three independent audits — `movable_obstruction`
   (suggestion: prose names P0 as a core tension but it was never included),
   `intersection_gesture_wait` (should-fix: this session's trim dropped P0
   despite prose explicitly describing a goal-vs-social tension), and
   `pedestrian_overtaking` (suggestion: same pattern) — all flagged the same
   underlying concern independently. This session's principles-trim step
   (see git history) treated P0 as a low-signal, near-universal principle
   and defaulted to dropping it in `intersection_gesture_proceed`,
   `intersection_gesture_wait`, and `pedestrian_overtaking`. In hindsight,
   for scenarios whose prose explicitly frames a goal-achievement-vs-social
   tension as the point of the scenario (the way `movable_obstruction`'s
   prose does for P9), P0 may be as load-bearing as P9 was in
   `movable_obstruction` — where P9 was deliberately restored for exactly
   this reason. Worth revisiting whether P0 should be restored in
   `intersection_gesture_wait` and `pedestrian_overtaking` specifically (and
   possibly added to `movable_obstruction`), as a single human decision
   rather than three separate ones.
