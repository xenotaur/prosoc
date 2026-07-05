# Scenario Audit Summary

Aggregate results from the first full-corpus run of `/prosoc-scenario-audit`
against all 20 scenario directories under `prosoc/scenarios/`, one invocation
per scenario. See [xenotaur/prosoc#4](https://github.com/xenotaur/prosoc/pull/4)
for the run that produced this snapshot.

This file is a point-in-time index, not a live report — each scenario's own
`audit.md` is the source of truth for full findings detail. Re-running the
audit against a scenario does not automatically update this file; regenerate
it by hand (or via a future batch-audit skill) after any re-audit.

No scenario's `scenario.md`, `scenario.yml`, or STATUS/STATE block was
modified in producing these audits, and no scenario STATE was promoted —
that remains a human decision per [workflow.md](workflow.md).

## Results (as of 2026-07-05)

| Scenario | Verdict | Blocking | Should-fix | Suggestion |
|---|---|---|---|---|
| blind_corner | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| crash_cart | Ready for AUDITED with minor fixes | 0 | 3 | 1 |
| crowd_navigation | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| entering_room | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| exiting_room | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| following | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| frontal_approach | Not ready | 1 | 2 | 2 |
| intersection_gesture_proceed | Not ready | 2 | 2 | 1 |
| intersection_gesture_wait | Not ready | 3 | 2 | 1 |
| intersection_no_gesture | Not ready | 2 | 1 | 2 |
| join_a_group | Not ready | 2 | 0 | 0 |
| leading | Not ready | 2 | 0 | 1 |
| movable_obstruction | Not ready | 3 | 2 | 0 |
| narrow_doorway | Ready | 0 | 0 | 2 |
| object_handover | Not ready | 0 | 3 | 1 |
| parallel_traffic | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| pedestrian_overtaking | Not ready | 2 | 1 | 1 |
| perpendicular_traffic | Ready for AUDITED with minor fixes | 0 | 2 | 0 |
| robot_overtaking | Not ready | 3 | 1 | 1 |
| single_file_hallway | Not ready | 3 | 1 | 2 |

**Totals:** 20 scenarios, 8 "ready" (no blocking), 12 "not ready" (blocking
issues present). 25 blocking, 28 should-fix, 20 suggestion findings.

## Recurring patterns

These are cross-cutting observations noticed while aggregating results —
not part of any single scenario's audit scope, which stays limited to one
scenario per invocation. Each still requires a human decision to act on.

1. **Missing "Scenario Card Summary" section** — flagged in the large
   majority of scenarios (should-fix or blocking depending on how far along
   the card is). The underlying data already exists in each card's
   YAML/prose; this is consistently a transcription gap, not a
   missing-information gap. Worth a repo-wide template/checklist fix rather
   than fixing card-by-card.
2. **Missing "Scenario Usage Guide" prose section / `scenario_usage_guide`
   YAML block** — similarly widespread across most scenarios, same
   transcription-gap character as #1.
3. **Invalid principle IDs `P0`/`P9` used in `relevant_principles`/
   `quality_metrics`** — found in 7 of 20 scenarios
   (intersection_gesture_proceed, intersection_gesture_wait,
   intersection_no_gesture, movable_obstruction, pedestrian_overtaking,
   robot_overtaking, single_file_hallway), all outside the canonical
   `P1`–`P8` set defined in
   [`../../.claude/skills/_shared/principles.md`](../../.claude/skills/_shared/principles.md).
   Concentrated in scenarios that look like they were drafted together —
   suggests a shared drafting-time error rather than 7 independent mistakes.
