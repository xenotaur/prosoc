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

## Correction (2026-07-05)

The initial run of this audit incorrectly flagged `P0` and `P9` in
`relevant_principles` as invalid, invented principle IDs, in 7 scenarios. This
was wrong: `prosoc/charter/charter.md` (the sole source of truth, confirmed
consistent with the generated `prosoc/charter/charter.yml`) defines **ten**
principles, P0–P9 — P0 (Goal Achievement) and P9 (Prosocial Behavior) are this
project's own explicit extensions beyond the P&G paper's eight, not invented
IDs. The error originated in a stale `.claude/skills/_shared/principles.md`,
which claimed only P1–P8 were valid; that file (and the corresponding checks
in both `prosoc-scenario-audit` and `prosoc-scenario-new`'s skill files) has
since been corrected. The table below reflects the corrected counts; each
affected scenario's `audit.md` has its own "Correction Notice" section
documenting exactly what changed.

## Results (as of 2026-07-05, corrected)

| Scenario | Verdict | Blocking | Should-fix | Suggestion |
|---|---|---|---|---|
| blind_corner | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| crash_cart | Ready for AUDITED with minor fixes | 0 | 3 | 1 |
| crowd_navigation | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| entering_room | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| exiting_room | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| following | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| frontal_approach | Not ready | 1 | 2 | 2 |
| intersection_gesture_proceed | Not ready | 1 | 2 | 2 |
| intersection_gesture_wait | Not ready | 1 | 2 | 1 |
| intersection_no_gesture | Not ready | 1 | 1 | 2 |
| join_a_group | Not ready | 2 | 0 | 0 |
| leading | Not ready | 2 | 0 | 1 |
| movable_obstruction | Not ready | 2 | 1 | 1 |
| narrow_doorway | Ready | 0 | 0 | 2 |
| object_handover | Not ready | 0 | 3 | 1 |
| parallel_traffic | Ready for AUDITED with minor fixes | 0 | 2 | 1 |
| pedestrian_overtaking | Not ready | 1 | 1 | 2 |
| perpendicular_traffic | Ready for AUDITED with minor fixes | 0 | 2 | 0 |
| robot_overtaking | Not ready | 2 | 1 | 1 |
| single_file_hallway | Not ready | 3 | 1 | 1 |

**Totals:** 20 scenarios, 8 "ready" (no blocking), 12 "not ready" (blocking
issues present — the ready/not-ready split is unchanged by the correction,
since no scenario's blocking count dropped to zero solely from retracting the
P0/P9 findings). 16 blocking, 31 should-fix, 23 suggestion findings.

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
3. **A stale shared skill reference caused 7 false-positive "invalid
   principle ID" findings** — `.claude/skills/_shared/principles.md` claimed
   only P1–P8 were valid principles, but this project's charter
   (`prosoc/charter/charter.md`) defines ten (P0–P9), with P0 and P9 as
   deliberate extensions beyond the P&G paper. Every scenario using P0 or P9
   (intersection_gesture_proceed, intersection_gesture_wait,
   intersection_no_gesture, movable_obstruction, pedestrian_overtaking,
   robot_overtaking, single_file_hallway) was incorrectly dinged for it,
   several at blocking severity. This was caught via user review, not by the
   audit or its checklist — worth remembering that shared skill reference
   data can itself drift out of sync with a project's actual source of
   truth, and that "the checklist says so" isn't sufficient evidence when a
   normative document (here, the charter) is directly checkable.
