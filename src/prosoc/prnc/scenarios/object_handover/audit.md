---
family: scenarios
card: object_handover
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-02
---

# Audit: Object Handover

- **Card:** `prosoc/scenarios/object_handover/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — finding carries forward,
  refined below)
- **Verdict:** Ready for `AUDITED`, no blocking or should-fix issues found

## Findings

### 1. "Normative Expectations" prose omits a `must`-level item — suggestion (refines prior finding from 2026-07-22)
- **Section/field:** `expected_behaviors.must` ("avoid collision with the
  human during approach", "not release the object before the human has a
  secure grip") vs. the prose "Unacceptable behavior includes" list
- **Issue:** The second `must` item is explicitly covered ("Releasing the
  object before the human has a secure hold..."), but the first
  ("avoid collision... during approach") is never stated as its own
  bullet — the nearest prose item ("Approaching at a pace or trajectory
  that startles the human or resembles an unrelated close pass") implies
  but doesn't name collision risk. Matches the recurring
  must-level-prose-gap pattern already tracked in
  `project/design/backlog.md`; the prior audit's broader framing ("prose
  doesn't mirror the must/should/should_not split") is refined here to
  the specific missing item.
- **Recommended fix:** Add an explicit "Approaching in a way that risks
  collision with the human" bullet to Unacceptable behavior, or
  optionally annotate the prose list to distinguish required vs.
  preferred items. Not required for `AUDITED`; deferred to the dedicated
  backlog-burndown pass.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Object Handover" (cited in [161]).
Compared against `.claude/skills/_shared/pg_scenarios.md`'s "Object
Handover" entry (Specialized Scenarios section):

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | A robot hands an object to a human | Overview: "servant robot navigates to a human and hands over an object..." | Match (elaborated) |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Passable space | `geometric_layout: passable space` | Match |
| Scientific Purpose | Interactive navigation | `scientific_purpose: interactive navigation` | Match |
| Robot Role | Servant | `agents.robot.role: servant` | Match |
| Robot Task | Deliver object | `intended_robot_task: deliver the object to the human` | Match |
| Human Behavior | Receive object | `intended_human_behavior: receive the object` | Match |
| Ideal Outcome | Human takes object | `ideal_outcome: human takes the object from the robot without awkwardness, collision, or dropped object` | Match (elaborated) |
| Related Scenarios | Robot Courier | `related_scenarios: [crash_cart]` — Robot Courier has no implemented scenario directory; card's own `evaluation_notes` documents the substitution, and `crash_cart` reciprocates the link | Consistent — expected divergence per convention, not a fidelity gap |
| Cited In | [161] | `cited_in: ["161"]` | Match |

No mismatches found. "Robot Courier" is not yet tracked in
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
`quality_metrics` (P2, P4) is a sensible subset of `relevant_principles`
(P1, P2, P4, P6).

No required fields are blank. `scripts/distill/scenarios --scenario
object_handover --dry-run --show-diffs` reported no diff, confirming
`scenario.md` and `scenario.yml` are in sync.
