---
family: scenarios
card: narrow_doorway
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-02
---

# Audit: Narrow Doorway

- **Card:** `prosoc/scenarios/narrow_doorway/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — finding carries forward
  unchanged since no content changed)
- **Verdict:** Ready for `AUDITED`, no blocking or should-fix issues found

## Findings

### 1. `expected_behaviors.should` mixes a graded/comparative claim — suggestion (carried forward from 2026-07-22)
- **Section/field:** `expected_behaviors.should` ("proceed decisively and
  without hesitation") vs. P&G Guideline N6 (over-specification)
- **Issue:** Phrased as a kind of behavior rather than an exact motion or
  numeric threshold, so not a blocking over-specification violation, but
  it edges toward prescribing manner/style rather than outcome.
- **Recommended fix:** No change required; optionally rephrase as
  "proceed without ambiguity about intent" to keep focus on legibility
  (P3) rather than motion style.

No other findings. This card is unusually clean: both `must`-level
behaviors ("avoid collision," "not stop in a position that blocks the
doorway") are explicitly bulleted in the prose "Unacceptable behavior"
list (no instance of the recurring must-level-prose-gap pattern seen on
other cards), and all three `related_scenarios` entries (`blind_corner`,
`entering_room`, `exiting_room`) reciprocate the link back to
`narrow_doorway` in their own `related_scenarios` — no one-way
cross-reference gap.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Narrow Doorway" (cited in [126]).
Compared against `.claude/skills/_shared/pg_scenarios.md`'s "Narrow
Doorway" entry:

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | Robot and human at a narrow doorway (room and door) | Overview: "robot and a human pedestrian approach a narrow doorway from opposite directions" | Match |
| Physical Env | Indoor | `context.environment.type: indoor` | Match |
| Geometric Layout | Room and door | `geometric_layout: room and door` | Match |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Match |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B through the doorway` | Match |
| Human Behavior | Navigate B to A | `intended_human_behavior: navigate from B to A through the doorway` | Match |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot and human sequence through the doorway one at a time without collision or obstruction` | Match |
| Related Scenarios | Narrow Arch | `related_scenarios: [blind_corner, entering_room, exiting_room]` — Narrow Arch has no implemented scenario directory; card's own `evaluation_notes` documents the substitution | Consistent — expected divergence per convention, not a fidelity gap |
| Cited In | [126] | `cited_in: ["126"]` | Match |

No mismatches found. "Narrow Arch" is not yet tracked in
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
`quality_metrics` (P3, P4) is a sensible subset of `relevant_principles`
(P1, P3, P4, P7).

No required fields are blank. `scripts/distill/scenarios --scenario
narrow_doorway --dry-run --show-diffs` reported no diff, confirming
`scenario.md` and `scenario.yml` are in sync.
