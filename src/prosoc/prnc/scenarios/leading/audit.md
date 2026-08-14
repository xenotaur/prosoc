---
family: scenarios
card: leading
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-07
---

# Audit: Leading

- **Card:** `prosoc/scenarios/leading/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-07 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — this pass adds one new
  finding)
- **Verdict:** Ready for `AUDITED`, no blocking or should-fix issues found

## Findings

### 1. "Normative Expectations" prose omits a `must`-level item — suggestion
- **Section/field:** `expected_behaviors.must` ("avoid collision with the
  human, other pedestrians, and obstacles", "not proceed to the
  destination while unaware the human has been separated") vs. the prose
  "Unacceptable behavior" list
- **Issue:** The second `must` item is covered verbatim ("Continuing to a
  destination while unaware the human has been separated"), but the
  first ("avoid collision") is never stated as its own bullet. Matches
  the recurring must-level-prose-gap pattern already tracked in
  `project/design/backlog.md`.
- **Recommended fix:** Add an explicit "Colliding with the human, other
  pedestrians, or obstacles while leading" bullet to Unacceptable
  behavior. Not required for `AUDITED`; deferred to the dedicated
  backlog-burndown pass.

No other findings. `related_scenarios: [following]` reciprocates —
`following`'s own `related_scenarios` lists `leading` back. No one-way
cross-reference gap.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Leading" (cited in [50]). Compared
against `.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | A robot leads a person | Overview: "robot in a leader role whose task is to guide a human through a walking space" | Match |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Walking space | `geometric_layout: walking space` | Match |
| Scientific Purpose | Joint navigation | `scientific_purpose: joint navigation` | Match |
| Robot Role | Leader | `agents.robot.role: leader` | Match |
| Robot Task | Lead human | `intended_robot_task: lead the human to a destination` | Match |
| Human Behavior | Follow robot | `intended_human_behavior: follow the robot, tracking its path and pace` | Match |
| Ideal Outcome | Person follows robot | `ideal_outcome: person follows the robot to the destination...` | Match |
| Related Scenarios | Tour Guide | `related_scenarios: [following]` — Tour Guide has no implemented scenario directory; card's own `evaluation_notes` documents the substitution | Consistent — expected divergence per convention, not a fidelity gap |
| Cited In | [50] | `cited_in: ["50"]` | Match |

No mismatches found. Unlike `following`, no erratum or ambiguity here —
every field matches cleanly with no interpretive call needed. "Tour
Guide" is not yet tracked in `project/design/backlog.md`'s "Missing
forward-referenced cards" table — adding it as part of this review.

## Completeness

Scenario Card Summary: all fields present and rendered — Scenario Name,
Description, Scientific Purpose, Physical Environment, Geometric Layout,
Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics,
Ideal Outcome, Related Scenarios (`following`), Cited In (`50`).

Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome,
Failure Modes, and Labeling Criteria all present and non-trivial.
`quality_metrics` (P3, P6) is a sensible subset of `relevant_principles`
(P1, P3, P6, P8).

No required fields are blank. `scripts/distill/scenarios --scenario
leading --dry-run --show-diffs` reported no diff, confirming
`scenario.md` and `scenario.yml` are in sync.
