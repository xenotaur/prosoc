# Scenario Audit Summary

- **Run date:** 2026-07-21
- **Branch:** claude/prosoc-audit-refresh-20260721
- **Scenarios audited:** 20 (0 skipped)

This is a point-in-time index, not a live report — each scenario's own
`audit.md` is the source of truth for full findings detail. Re-running the
audit against a scenario does not automatically update this file; regenerate
it (this file was produced by `/prosoc-scenario-audit-all`, see
`.claude/skills/prosoc-scenario-audit-all/`) after any re-audit.

No scenario's `scenario.md`, `scenario.yml`, or STATUS/STATE block was
modified in producing these audits, and no scenario STATE was promoted —
that remains a human decision per [workflow.md](workflow.md).

This run follows [PR #28](https://github.com/xenotaur/prosoc/pull/28), which
resolved both follow-ups the 2026-07-20 snapshot had flagged: P0 (Goal
Achievement) was restored to `relevant_principles` in the four scenarios
whose own prose explicitly discusses a goal-vs-social tradeoff
(`intersection_gesture_proceed`, `intersection_gesture_wait`,
`pedestrian_overtaking`, `movable_obstruction`), and `related_scenarios`/
`cited_in` were backfilled across the 13 scenarios that had the schema
fields but no values. Along the way, a propagated citation error
("Robots@Games (R@G)") was corrected to "Robotics at Google (R@G)" in
`entering_room`, `exiting_room`, and the shared `pg_scenarios.md` reference.
The 2026-07-20 snapshot is superseded by this one.

## Results

| Scenario | Verdict | Blocking | Should-fix | Suggestion |
|---|---|---|---|---|
| blind_corner | ready | 0 | 0 | 0 |
| crash_cart | ready | 0 | 0 | 2 |
| crowd_navigation | ready | 0 | 0 | 1 |
| entering_room | ready | 0 | 0 | 2 |
| exiting_room | ready | 0 | 0 | 1 |
| following | ready | 0 | 0 | 0 |
| frontal_approach | ready_with_fixes | 0 | 1 | 2 |
| intersection_gesture_proceed | ready_with_fixes | 0 | 1 | 2 |
| intersection_gesture_wait | not_ready | 1 | 0 | 2 |
| intersection_no_gesture | not_ready | 1 | 0 | 3 |
| join_a_group | ready | 0 | 0 | 2 |
| leading | ready | 0 | 0 | 1 |
| movable_obstruction | ready_with_fixes | 0 | 1 | 0 |
| narrow_doorway | ready | 0 | 0 | 1 |
| object_handover | ready | 0 | 0 | 1 |
| parallel_traffic | ready | 0 | 0 | 1 |
| pedestrian_overtaking | ready | 0 | 0 | 1 |
| perpendicular_traffic | ready | 0 | 0 | 0 |
| robot_overtaking | ready_with_fixes | 0 | 1 | 2 |
| single_file_hallway | ready_with_fixes | 0 | 1 | 1 |

**Totals:** 20 scenarios, 13 `ready`, 5 `ready_with_fixes`, 2 `not_ready`.
2 blocking, 5 should-fix, 25 suggestion findings.

Compared to the 2026-07-20 snapshot: `ready` scenarios rose from 3 to 13,
should-fix findings dropped from 19 to 5, and blocking findings held at 2
(the same root cause as before — `scenario_usage_guide` is still entirely
absent from `intersection_gesture_wait` and `intersection_no_gesture`'s
YAML, which remains out of scope for this pass).

## Recurring Patterns

Extracted the same way as the 2026-07-20 snapshot: exact-matching each
finding's normalized title across scenarios, then a manual reading since
parallel-dispatched subagents word the same underlying issue differently.

**Mechanical (exact-title match, threshold 3): none found.** Closest
matches were pairs:
- "`scenario_usage_guide` block still entirely missing from YAML" —
  `intersection_gesture_wait`, `intersection_no_gesture`
- "Normative Expectations prose doesn't mirror the must/should/should_not
  split" — `object_handover`, `parallel_traffic`
- "STATUS block's EDITED date does not reflect the latest edit" —
  `crowd_navigation`, `entering_room`

**Manual reading — one pattern worth a single decision:**

1. **`related_scenarios` sometimes names a different scenario than what
   P&G Table 3 itself lists**, because the table's named scenario isn't
   implemented in this corpus. Flagged (with varying wording) as a
   `suggestion` — informational, no action required until the table's
   scenario gets its own directory — in `crash_cart` (table says "Food
   Delivery", card says `object_handover`), `join_a_group` (table says
   "Leave Group", card says `crowd_navigation`), `leading` (table says
   "Tour Guide", card says `following`), and noted as informational
   context (not a numbered finding) in `narrow_doorway`, `object_handover`,
   `parallel_traffic`, and the `intersection_gesture_*` trio. This is
   expected, not a defect — this session's backfill deliberately links
   only to scenarios that exist as corpus directories, per `schema.json`'s
   own definition of the field (clarified in PR #27's review-response
   round). All three numbered instances (`crash_cart`, `join_a_group`,
   `leading`) are now treated consistently as `suggestion`-severity,
   no-action-needed findings (`crash_cart`'s audit briefly diverged to
   `should-fix` on the first pass and was corrected in PR #29's
   review-response round) — still worth a single documented convention
   (e.g. an `evaluation_notes` note pattern for "table names an
   unimplemented scenario") so future audits don't need to re-derive this
   reasoning from scratch each time.

No other pattern from the 2026-07-20 snapshot recurred: the P0 under-trim
and the `related_scenarios`/`cited_in` backfill are both resolved.
