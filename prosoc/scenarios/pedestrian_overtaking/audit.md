---
family: scenarios
card: pedestrian_overtaking
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-08-02
---

# Audit: Pedestrian Overtaking a Robot from Behind

- **Card:** `prosoc/scenarios/pedestrian_overtaking/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — finding 1 carries forward
  unchanged, finding 2 is new)
- **Verdict:** Ready for `AUDITED`, no blocking or should-fix issues found

## Findings

### 1. Physical Environment more specific than source table — suggestion (carried forward from 2026-07-22)
- **Section/field:** `context.environment.type` (`indoor`) vs. P&G Table 3's
  "Generic" Physical Env for this row
- **Issue:** Not a contradiction — "Generic" means unspecified, and
  `indoor` is a reasonable concretization — but it's an editorial choice
  beyond the source. Same pattern already flagged and logged for the
  sibling scenario `robot_overtaking`.
- **Recommended fix:** No action required. Optionally note in
  `evaluation_notes` that the indoor setting is an authorial
  concretization.

### 2. "Normative Expectations" prose loosely paraphrases a `must`-level item — suggestion
- **Section/field:** `expected_behaviors.must` ("avoid impeding the
  pedestrian's overtaking maneuver") vs. the prose "Unacceptable behavior"
  sentence
- **Issue:** The prose covers this via "positioning itself in a way that
  forces the pedestrian to take evasive action" — a paraphrase, not an
  explicit restatement of "impeding." Same loose-paraphrase pattern
  already logged for `robot_overtaking`'s recurring must-level-prose-gap
  entry.
- **Recommended fix:** No action required for `AUDITED`; deferred to the
  dedicated backlog-burndown pass.

## Source Fidelity

The prose explicitly states this scenario "corresponds to
pedestrian-overtaking cases discussed in the *Principles and Guidelines
for Social Robot Navigation* paper," and `cited_in: ["26"]` matches, so
fidelity is checked against `.claude/skills/_shared/pg_scenarios.md`'s
"Pedestrian Overtaking" entry — even though the Status block's `SOURCE:`
line reads "Prompt to ChatGPT 5.2" (an informal drafting-provenance note,
not a source-fidelity claim; superseded here by the prose's explicit
paper reference, consistent with the prior audit's treatment):

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | Pedestrian overtakes moving robot | Overview: "human pedestrian approaches and overtakes a slower-moving robot from behind" | Match |
| Physical Env | Generic | `context.environment.type: indoor` | Concretized, not contradicted (Finding 1) |
| Geometric Layout | Passable space | `geometric_layout: passable space` | Match |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Match |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B` | Match |
| Human Behavior | Navigate A to B (faster) | `intended_human_behavior: navigate from A to B, faster than the robot` | Match |
| Ideal Outcome | Human passes robot | `ideal_outcome: human passes the robot safely, comfortably, and without disruption` | Match (elaborated) |
| Related Scenarios | Down Path | `related_scenarios: [robot_overtaking]` — Down Path has no implemented scenario directory; card's own `evaluation_notes` documents the substitution | Consistent — expected divergence per convention, not a fidelity gap |
| Cited In | [26] | `cited_in: ["26"]` | Match |

No mismatches found. "Down Path" is not yet tracked in
`project/design/backlog.md`'s "Missing forward-referenced cards" table —
adding it as part of this review.

## Completeness

Scenario Card Summary: all fields present and rendered — Scenario Name,
Description, Scientific Purpose, Physical Environment, Geometric Layout,
Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics,
Ideal Outcome, Related Scenarios, Cited In.

Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome,
Failure Modes, and Labeling Criteria all present and non-trivial.
`quality_metrics` (P2, P3, P4) is a sensible subset of
`relevant_principles` (P0, P1, P2, P3, P4) — five principles is one over
the nominal 3-5 midpoint but covered by the explicit prose-discussion
exception (Overview explicitly discusses P0 goal achievement).

No required fields are blank. `scripts/distill/scenarios --scenario
pedestrian_overtaking --dry-run --show-diffs` reported no diff,
confirming `scenario.md` and `scenario.yml` are in sync.
