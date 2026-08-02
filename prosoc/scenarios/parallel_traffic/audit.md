---
family: scenarios
card: parallel_traffic
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-02
---

# Audit: Parallel Traffic

- **Card:** `prosoc/scenarios/parallel_traffic/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — finding carries forward,
  refined below)
- **Verdict:** Ready for `AUDITED`, no blocking or should-fix issues found

## Findings

### 1. "Normative Expectations" prose omits a `must`-level item — suggestion (refines prior finding from 2026-07-22)
- **Section/field:** `expected_behaviors.must` ("avoid collision with any
  pedestrian in the stream", "not cut across multiple pedestrians' lanes
  to force a position") vs. the prose "Unacceptable behavior includes"
  list
- **Issue:** The second `must` item is explicitly covered ("Cutting
  perpendicular to the flow to reach a position, disrupting multiple
  pedestrians' paths"), but the first ("avoid collision with any
  pedestrian in the stream") is never stated as its own bullet — the
  closest prose items address pace/weaving/overtake, not collision
  directly. Matches the recurring must-level-prose-gap pattern already
  tracked in `project/design/backlog.md`; the prior audit's broader
  framing ("prose doesn't mirror must/should/should_not split") is
  refined here to the specific missing item.
- **Recommended fix:** Add an explicit "Colliding with a pedestrian while
  merging into or traveling within the stream" bullet to Unacceptable
  behavior. Not required for `AUDITED`; deferred to the dedicated
  backlog-burndown pass.

No other findings. `related_scenarios` (`perpendicular_traffic`,
`crowd_navigation`) both reciprocate the link back to `parallel_traffic`
in their own `related_scenarios` — no one-way cross-reference gap.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Parallel Traffic" (cited in [167]).
Compared against `.claude/skills/_shared/pg_scenarios.md`'s "Parallel
Traffic" entry:

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | Crowd moves parallel to the robot | Overview: "crowd of pedestrians moves broadly in the same direction, forming an emergent pedestrian stream" | Match (elaborated) |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Passable space | `geometric_layout: passable space` | Match |
| Scientific Purpose | Crowd navigation | `scientific_purpose: crowd navigation` | Match |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B` | Match |
| Human Behavior | Mill from A to B | `intended_human_behavior: mill from A to B, forming a parallel pedestrian stream` | Match (elaborated) |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot merges into and travels with the pedestrian stream without collision or obstruction` | Match |
| Related Scenarios | Circular Crossing | `related_scenarios: [perpendicular_traffic, crowd_navigation]` — Circular Crossing is a Figure 7 variant with no implemented scenario directory; card's own `evaluation_notes` documents the substitution | Consistent — expected divergence per convention, not a fidelity gap |
| Cited In | [167] | `cited_in: ["167"]` | Match |

No mismatches found. "Circular Crossing" is not yet tracked in
`project/design/backlog.md`'s "Missing forward-referenced cards" table —
added to `project/design/backlog.md`'s "Missing forward-referenced cards"
table as part of this review.

## Completeness

Scenario Card Summary: all fields present and rendered — Scenario Name,
Description, Scientific Purpose, Physical Environment, Geometric Layout,
Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics,
Ideal Outcome, Related Scenarios, Cited In.

Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome,
Failure Modes, and Labeling Criteria all present and non-trivial.
`quality_metrics` (P2, P5) is a sensible subset of `relevant_principles`
(P1, P2, P5, P6).

No required fields are blank. `scripts/distill/scenarios --scenario
parallel_traffic --dry-run --show-diffs` reported no diff, confirming
`scenario.md` and `scenario.yml` are in sync.
