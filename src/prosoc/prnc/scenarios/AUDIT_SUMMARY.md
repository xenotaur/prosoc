# Scenario Audit Summary

- **Run date:** 2026-07-22
- **Branch:** claude/audit-all-scenarios-2026-07-22
- **Scenarios audited:** 20 (0 skipped)

This is a point-in-time index, not a live report — each scenario's own
`audit.md` is the source of truth for full findings detail. Re-running the
audit against a scenario does not automatically update this file; regenerate
it (this file was produced by `/prosoc-scenario-audit-all`, see
`.claude/skills/prosoc-scenario-audit-all/`) after any re-audit.

No scenario's `scenario.md`, `scenario.yml`, or STATUS/STATE block was
modified in producing these audits, and no scenario STATE was promoted —
that remains a human decision per [workflow.md](workflow.md).

This run follows [PR #30](https://github.com/xenotaur/prosoc/pull/30) (the
`related_scenarios`/Table 3 divergence convention) and
[PR #31](https://github.com/xenotaur/prosoc/pull/31), which closed the
corpus's last remaining blocking gap — `intersection_gesture_wait` and
`intersection_no_gesture` had an entirely empty `scenario_usage_guide`
since the very first audit (2026-07-05) — and resolved the 4 remaining
should-fix findings from the 2026-07-21 snapshot (`frontal_approach`,
`movable_obstruction`, `robot_overtaking`, `single_file_hallway`). The
2026-07-21 snapshot is superseded by this one.

## Results

| Scenario | Verdict | Blocking | Should-fix | Suggestion |
|---|---|---|---|---|
| blind_corner | ready | 0 | 0 | 0 |
| crash_cart | ready | 0 | 0 | 1 |
| crowd_navigation | ready | 0 | 0 | 1 |
| entering_room | ready | 0 | 0 | 2 |
| exiting_room | ready | 0 | 0 | 1 |
| following | ready | 0 | 0 | 0 |
| frontal_approach | ready | 0 | 0 | 2 |
| intersection_gesture_proceed | ready | 0 | 0 | 2 |
| intersection_gesture_wait | ready | 0 | 0 | 2 |
| intersection_no_gesture | ready | 0 | 0 | 3 |
| join_a_group | ready | 0 | 0 | 1 |
| leading | ready | 0 | 0 | 0 |
| movable_obstruction | ready | 0 | 0 | 0 |
| narrow_doorway | ready | 0 | 0 | 1 |
| object_handover | ready | 0 | 0 | 1 |
| parallel_traffic | ready | 0 | 0 | 1 |
| pedestrian_overtaking | ready | 0 | 0 | 1 |
| perpendicular_traffic | ready | 0 | 0 | 0 |
| robot_overtaking | ready | 0 | 0 | 2 |
| single_file_hallway | ready | 0 | 0 | 1 |

**Totals:** 20 scenarios, 20 `ready`, 0 `ready_with_fixes`, 0 `not_ready`.
0 blocking, 0 should-fix, 22 suggestion findings.

Compared to the 2026-07-21 snapshot: every scenario is now `ready` (up from
13), with 0 blocking and 0 should-fix findings corpus-wide (down from 2 and
5 respectively). All remaining findings are suggestion-level — optional
polish, not defects.

## Recurring Patterns

Extracted the same way as prior snapshots: exact-matching each finding's
normalized title across scenarios, then a manual reading since
parallel-dispatched subagents word the same underlying issue differently.

**Mechanical (exact-title match, threshold 3): none found.** Closest
matches were pairs:
- "STATUS block's EDITED date does not reflect the latest edit" —
  `crowd_navigation`, `entering_room`
- "Normative Expectations prose doesn't mirror the must/should/should_not
  split" — `object_handover`, `parallel_traffic`
- "Physical Environment [more specific than / specialization vs.] P&G
  Table 3 'Generic'" (worded differently in each) — `pedestrian_overtaking`,
  `robot_overtaking`

**Manual reading:**

1. **STATUS block `EDITED` dates are stale in at least 2 scenarios**
   (`crowd_navigation`, `entering_room`) — both were edited by PR #30
   (the "Related Scenarios note" backfill) but their `EDITED:` line still
   reads `render_sections.py, 2026-07-20`. This is likely present in more
   scenarios than these two flag explicitly (most of the 18 scenarios PR
   #30 touched went through the same edit without a STATUS bump) — worth a
   corpus-wide pass to bump `EDITED` dates consistently, or a decision that
   this field isn't worth maintaining precisely.
2. **The `related_scenarios`/P&G Table 3 divergence pattern from prior
   snapshots is now fully resolved as a non-issue.** No scenario this run
   flagged it as a should-fix; every remaining mention (`intersection_gesture_proceed`,
   `intersection_gesture_wait`, `intersection_no_gesture`, `robot_overtaking`)
   is a suggestion-level, no-action-needed note, consistent with the
   convention documented in PR #30 and `prosoc-scenario-audit`'s
   `audit_checklist.md`.

No blocking or should-fix pattern recurred. The corpus is clean.
