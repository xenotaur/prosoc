---
family: scenarios
card: perpendicular_traffic
verdict: ready
blocking: 0
should_fix: 0
suggestion: 3
audited: 2026-08-08
---

# Audit: Perpendicular Traffic

- **Card:** `prosoc/scenarios/perpendicular_traffic/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-08 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — this pass adds three new
  findings on a card that previously had zero)
- **Verdict:** Ready for `AUDITED`, no blocking or should-fix issues found

## Findings

### 1. "Normative Expectations" prose omits a `must`-level item — suggestion
- **Section/field:** `expected_behaviors.must` ("avoid collision with any
  pedestrian in the flow", "not stop or reverse within the middle of the
  flow once crossing has begun") vs. the prose "Unacceptable behavior"
  list
- **Issue:** The second `must` item is covered ("Stopping or reversing
  in the middle of the crossing, creating an obstruction within the
  flow"), but the first ("avoid collision") is never stated as its own
  bullet. Matches the recurring must-level-prose-gap pattern already
  tracked in `project/design/backlog.md`.
- **Recommended fix:** Add an explicit "Colliding with a pedestrian
  while crossing the flow" bullet to Unacceptable behavior. Not required
  for `AUDITED`; deferred to the dedicated backlog-burndown pass.

### 2. One-way `related_scenarios` cross-reference with `crowd_navigation` — suggestion
- **Section/field:** `related_scenarios: [parallel_traffic,
  intersection_no_gesture]` vs. `crowd_navigation`'s own
  `related_scenarios: [parallel_traffic, perpendicular_traffic]`
- **Issue:** `crowd_navigation` lists `perpendicular_traffic` as related,
  but this card doesn't list `crowd_navigation` back — a one-way
  reference. Already logged in `project/design/backlog.md`'s "Open
  suggestions on promoted cards" table (found via independent subagent
  review on PR #71, attributed to `perpendicular_traffic`'s side); this
  is that same pre-existing gap, now confirmed directly while auditing
  this card itself rather than only from `crowd_navigation`'s side.
- **Recommended fix:** Consider adding `crowd_navigation` to this card's
  `related_scenarios` for symmetry. Not required for `AUDITED`.

### 3. One-way `related_scenarios` cross-reference with `intersection_no_gesture` — suggestion (new)
- **Section/field:** `related_scenarios: [parallel_traffic,
  intersection_no_gesture]` vs. `intersection_no_gesture`'s own
  `related_scenarios: [intersection_gesture_proceed,
  intersection_gesture_wait]`
- **Issue:** This card lists `intersection_no_gesture` as related (its
  own Notes section frames it as "a single-human crossing negotiation,
  rather than a continuous multi-pedestrian stream" analog), but
  `intersection_no_gesture` doesn't reciprocate — a second, previously
  unnoticed one-way reference distinct from Finding 2.
- **Recommended fix:** Consider adding `perpendicular_traffic` to
  `intersection_no_gesture`'s `related_scenarios`. Not required for
  `AUDITED`; logging to the backlog for the burndown pass.

No must-level or should-fix issues. `parallel_traffic`'s own
`related_scenarios` does reciprocate this card's link (no gap there).

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Perpendicular Traffic" (cited in
[167]). Compared against `.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | Crowd moves perpendicular to the robot | Overview: "robot crosses an intersection or plaza while a crowd of pedestrians flows perpendicular to its path" | Match |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Intersection | `geometric_layout: intersection` | Match |
| Scientific Purpose | Crowd navigation | `scientific_purpose: crowd navigation` | Match |
| Robot Task | Cross navigate | `intended_robot_task: cross navigate through the perpendicular flow` | Match |
| Human Behavior | Mill from A to B | `intended_human_behavior: mill from A to B, forming a continuous perpendicular stream` | Match |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot crosses the perpendicular flow without collision or obstruction` | Match |
| Related Scenarios | Plaza Crossing | `related_scenarios: [parallel_traffic, intersection_no_gesture]` — Plaza Crossing has no implemented scenario directory; card's own `evaluation_notes` documents the substitution | Consistent — expected divergence per convention, not a fidelity gap |
| Cited In | [167] | `cited_in: ["167"]` | Match |

No mismatches found. "Plaza Crossing" is not yet tracked in
`project/design/backlog.md`'s "Missing forward-referenced cards" table —
adding it as part of this review.

## Completeness

Scenario Card Summary: all fields present and rendered — Scenario Name,
Description, Scientific Purpose, Physical Environment, Geometric Layout,
Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics,
Ideal Outcome, Related Scenarios, Cited In (`167`).

Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome,
Failure Modes, and Labeling Criteria all present and non-trivial.
`quality_metrics` (P3, P7) is a sensible subset of `relevant_principles`
(P1, P3, P6, P7).

No required fields are blank. `scripts/distill/scenarios --scenario
perpendicular_traffic --dry-run --show-diffs` reported no diff,
confirming `scenario.md` and `scenario.yml` are in sync.
