---
scenario: crash_cart
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-22
---

# Audit: Crash Cart

- **Scenario:** `prosoc/scenarios/crash_cart/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready for AUDITED, no fixes required

## Findings

### 1. Bystander count is an unstated elaboration — suggestion
- **Section/field:** Scenario Overview / Social Navigation Context prose vs.
  `agents.humans[0].count: 3`
- **Issue:** Prose refers to "bystanders" and "pedestrians" generically throughout
  the Overview, Social Navigation Context, and Normative Expectations sections; no
  sentence grounds the specific `count: 3` chosen in the YAML. This is drift rather
  than contradiction — a reasonable concretization for simulation setup — but there
  is still no prose basis to confirm 3 specifically (vs. 1, 2, or more). Unresolved
  across the 2026-07-05, 2026-07-20, and 2026-07-21 audits; still present in this
  point-in-time re-check.
- **Recommended fix:** Either state an approximate bystander count in prose (e.g., "a
  small number of bystanders (2-3)") to ground the YAML's `count: 3`, or note in
  `evaluation_notes` that the count is a reasonable default subject to variation.

Note: `related_scenarios: [object_handover]` diverges from P&G Table 3's "Food
Delivery" citation, but this is the documented, expected divergence case (Table 3
names an unimplemented scenario; the card substitutes an implemented one it
discusses in its own prose) per the audit checklist's `related_scenarios` guidance —
not flagged as a finding here. See Source Fidelity below.

## Prose/YAML Consistency

No contradictions found. The bystander-awareness relationship between
`initial_conditions.human_positions`, `intended_human_behavior`, and the Normative
Expectations/`expected_behaviors` sections is internally consistent: bystanders
start "unaware of the specific urgency" and are "expected to update upon perceiving
the robot's signaling," matching the prose's expectation that bystanders yield once
the robot signals urgency, and matching `expected_behaviors.should`. Scenario
Overview, Social Navigation Context, and Normative Expectations otherwise align
cleanly with `intended_robot_task`, `agents`, `expected_behaviors`, and
`ideal_outcome`. (See Finding 1 for the one unresolved drift point — bystander
count.)

## Schema and Charter Compliance

- `scripts/distill/scenarios --scenario crash_cart --dry-run --show-diffs` produced
  no diff and no schema validation error — `scenario.yml` is in sync with
  `scenario.md`'s embedded YAML and validates against `schema.json`.
- `expected_behaviors` uses only `must`/`should`/`should_not`, matching the schema's
  `additionalProperties: false` constraint.
- `relevant_principles`: P1, P3, P7, P8 — four valid P0–P9 IDs, within the
  recommended 3–5 range, each discussed in the card's own prose.
- `scenario_usage_guide.quality_metrics`: P3, P8 — valid P0–P9 IDs.
- `expected_behaviors` entries describe kinds of behavior ("move at an elevated
  pace," "signal urgent status," "take reasonable priority") rather than exact
  motions or numeric thresholds — no over-specification per P&G Guideline N6.
- `related_scenarios: [object_handover]` references a scenario directory that exists
  under `prosoc/scenarios/`.

## Source Fidelity

SOURCE cites P&G Paper Table 3 (Francis et al., 2025), "Crash Cart" entry, cited in
"this article." Compared against `.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | Card | Match |
|---|---|---|---|
| Description | Robot delivering a medical product indoors | Robot in leader role delivers an urgent medical product indoors | Yes |
| Physical Env | Indoor | Indoor | Yes |
| Geometric Layout | Passable space | Passable space | Yes |
| Scientific Purpose | Interactive navigation | Interactive navigation | Yes |
| Robot Role | Leader | Leader | Yes |
| Robot Task | Deliver object | Deliver the medical product urgently | Yes (elaborated with urgency, consistent) |
| Human Behavior | Receive object | Bystanders yield to the passing robot; recipient receives the medical product upon arrival | Yes (elaborated, consistent) |
| Ideal Outcome | Delivery of medicine | Delivery of medicine to the recipient promptly and without collision or unsafe maneuvers | Yes (elaborated, consistent) |
| Related Scenarios | Food Delivery | object_handover | Expected divergence — Food Delivery has no implemented scenario directory under `prosoc/scenarios/`; the card's own Notes section discusses both Object Handover and Food Delivery, and substitutes the implemented one per the documented convention. Not a defect. |
| Cited In | this article | this article | Yes |

No mismatches found. All checkable fields confirmed against P&G Table 3.

## Completeness

All fields `template.md` marks "Required for AUDITED scenarios" are filled:

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose,
  Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior,
  Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) —
  all present and populated.
- **Scenario Usage Guide** (Success Metrics, Quality Metrics, Ideal Outcome, Failure
  Modes, Labeling Criteria) — all present as a dedicated section, consistent with
  the embedded YAML's `scenario_usage_guide` block.

No blank required fields; nothing to categorize as reasonably-blank or
should-fill-in-now.
