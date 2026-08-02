---
family: scenarios
card: join_a_group
verdict: ready
blocking: 0
should_fix: 0
suggestion: 3
audited: 2026-08-02
---

# Audit: Join a Group

- **Card:** `prosoc/scenarios/join_a_group/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — content unchanged since
  then, so the 2026-07-22 finding is carried forward and two new
  observations are added)
- **Verdict:** Ready for `AUDITED`, no blocking or should-fix issues found

## Findings

### 1. Redundant duplicate field — suggestion (carried forward from 2026-07-22)
- **Section/field:** `agents.humans[0].count` vs `agents.humans[0].attributes.group_size`
- **Issue:** Both fields independently state the group size is 3 (`count: 3`
  and `attributes.group_size: 3`). Harmless today since both values agree,
  but a future edit to one without the other would silently desynchronize
  them.
- **Recommended fix:** Consider dropping `attributes.group_size` and
  relying solely on `count`, or explicitly document why both are kept.

### 2. "Normative Expectations" prose omits a `must`-level item — suggestion
- **Section/field:** `expected_behaviors.must` (`avoid collision with any
  group member`, `avoid cutting directly through the group's shared
  conversational space`) vs. the prose "Unacceptable behavior includes"
  list
- **Issue:** The prose list explicitly covers the second `must` item
  ("Cutting directly through the group's O-space...") but never states
  the first ("avoid collision with any group member") as its own bullet —
  collision only appears implicitly via the Success Metrics
  (`NoCollisions`) and failure modes. Matches the recurring
  must-level-prose-gap pattern already tracked in `project/design/backlog.md`.
- **Recommended fix:** Add an explicit "Approaching or stopping in a way
  that risks collision with any group member" bullet to Unacceptable
  behavior. Not required for `AUDITED`; deferred to the dedicated
  backlog-burndown pass.

### 3. One-way `related_scenarios` cross-reference — suggestion
- **Section/field:** `related_scenarios: [crowd_navigation]`
- **Issue:** `join_a_group` lists `crowd_navigation` as related, but
  `crowd_navigation`'s own `related_scenarios` (`parallel_traffic`,
  `perpendicular_traffic`) does not reciprocate. Same one-way-reference
  pattern already flagged on `crowd_navigation`/`perpendicular_traffic`
  during PR #71's review.
- **Recommended fix:** Consider adding `join_a_group` to
  `crowd_navigation`'s `related_scenarios` for symmetry. Not required for
  `AUDITED` since the corpus doesn't currently enforce reciprocal linking;
  logged to the backlog for the future burndown pass.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Join a Group" (cited in [50, 161]).
Compared against `.claude/skills/_shared/pg_scenarios.md`'s "Join a Group"
entry:

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | Robot joins a group of robots or people | Overview: "robot navigating toward and joining a standing group..." | Match |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Open space | `geometric_layout: open space` | Match |
| Scientific Purpose | Group interaction | `scientific_purpose: group interaction` | Match |
| Robot Task | Navigate to group | `intended_robot_task: navigate to and join the group` | Match |
| Human Behavior | Continue conversing | `intended_human_behavior: continue conversing, accommodating the robot's arrival` (elaboration, not contradiction) | Match |
| Ideal Outcome | Robot joins group | `ideal_outcome: robot joins the group, settling into the formation without disrupting the conversation` | Match |
| Related Scenarios | Leaving a Group | `related_scenarios: [crowd_navigation]` — Leaving a Group has no implemented scenario directory; card's own `evaluation_notes` "Related Scenarios note" documents the substitution | Consistent — expected divergence per convention, not a fidelity gap |
| Cited In | [50, 161] | `cited_in: ["50", "161"]` | Match |

No mismatches found. "Leaving a Group" is not yet tracked in
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
`quality_metrics` (P2, P4, P5) is a sensible subset of
`relevant_principles` (P1, P2, P4, P5, P8).

No required fields are blank. `scripts/distill/scenarios --scenario
join_a_group --dry-run --show-diffs` reported no diff, confirming
`scenario.md` and `scenario.yml` are in sync.
