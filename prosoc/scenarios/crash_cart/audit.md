---
scenario: crash_cart
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-21
---

# Audit: Crash Cart

- **Scenario:** `prosoc/scenarios/crash_cart/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready for AUDITED, no fixes required

## Findings

### 1. `related_scenarios` diverges from Table 3's stated related scenario — suggestion
- **Section/field:** `related_scenarios` (YAML) vs. P&G Table 3 "Related Scenarios" and
  the card's own "Notes for Scenario Designers and Evaluators" section
- **Issue:** `related_scenarios` now lists only `object_handover`. Table 3 lists
  "Food Delivery" as Crash Cart's related scenario, and the card's Notes section
  already discusses both in prose — Object Handover as "the general delivery and
  handoff task without time pressure" and Food Delivery as "a related delivery
  context implied by the paper's 'Related Scenarios' note ... not separately defined
  in Table 3." `object_handover` is a reasonable and schema-correct choice —
  `related_scenarios` must reference an implemented scenario directory per
  `schema.json`'s description, and `food_delivery` does not exist as a directory
  under `prosoc/scenarios/` (confirmed by directory listing) — but this is worth
  noting since Table 3's own related-scenario pointer isn't yet represented. Not a
  silent substitution: the card's own Notes section already documents both names.
- **Recommended fix:** No action required now. If/when a `food_delivery` scenario is
  drafted, add it to `related_scenarios` alongside or instead of `object_handover`.

### 2. Bystander count is an unstated elaboration — suggestion
- **Section/field:** Scenario Overview / Social Navigation Context prose vs.
  `agents.humans[0].count: 3`
- **Issue:** Prose still refers to "bystanders" and "pedestrians" generically
  throughout the Overview, Social Navigation Context, and Normative Expectations
  sections; no sentence grounds the specific `count: 3` chosen in the YAML. This is
  drift rather than contradiction — a reasonable concretization for simulation setup
  — but there's still no prose basis to confirm 3 specifically (vs. 1, 2, or more).
  Unresolved from both the 2026-07-05 and 2026-07-20 audits.
- **Recommended fix:** Either state an approximate bystander count in prose (e.g., "a
  small number of bystanders (2-3)") to ground the YAML's `count: 3`, or note in
  `evaluation_notes` that the count is a reasonable default subject to variation.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Crash Cart" entry, cited in "this article." Compared
against `.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | scenario.yml / scenario.md | Match? |
|---|---|---|---|
| Description | Robot delivering a medical product indoors | Overview: robot delivers urgent medical product indoors | Yes |
| Physical Env | Indoor | `context.environment.type: indoor` | Yes |
| Geometric Layout | Passable space | `geometric_layout: passable space` | Yes |
| Scientific Purpose | Interactive navigation | `scientific_purpose: interactive navigation` | Yes |
| Robot Role | Leader | `agents.robot.role: leader` | Yes |
| Robot Task | Deliver object | `intended_robot_task: deliver the medical product urgently` | Yes (elaborated with urgency, consistent with description) |
| Human Behavior | Receive object | `intended_human_behavior: ...recipient receives the medical product upon arrival` | Yes |
| Ideal Outcome | Delivery of medicine | `ideal_outcome: delivery of medicine to the recipient promptly and without collision or unsafe maneuvers` | Yes (elaborated, consistent) |
| Related Scenarios | Food Delivery | `related_scenarios: [object_handover]` | Not a mismatch — Table 3's "Food Delivery" has no implemented scenario directory; the card's own Notes section already documents both names (see Finding 1). |
| Cited In | this article | `cited_in: ["this article"]` | Yes |

No mismatches found. All fields confirmed against P&G Table 3.

## Completeness

Re-checked against `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose, Physical
  Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success
  Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) — present and
  populated (scenario.md lines 12-31). Related Scenarios and Cited In are now filled
  in, resolving the prior audit's should-fix finding about those fields being
  tracked only in the Status block/Notes rather than the summary table (see Finding 1
  for a non-blocking note on the value chosen for Related Scenarios).
- **Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome, Failure
  Modes, Labeling Criteria** — all present as a dedicated `## Scenario Usage Guide`
  prose section (scenario.md lines 201-219), consistent with the embedded YAML's
  `scenario_usage_guide` block.

No blank required fields remain.

## Prose/YAML Consistency (Step 2)

No contradictions found. The bystander-awareness relationship between
`initial_conditions.human_positions`, `intended_human_behavior`, and the Normative
Expectations/`expected_behaviors` sections remains internally consistent: bystanders
start "unaware of the specific urgency" and are "expected to update upon perceiving
the robot's signaling," matching the prose's expectation that bystanders yield once
the robot signals urgency and matching `expected_behaviors.should`. Scenario Overview,
Social Navigation Context, and Normative Expectations otherwise align cleanly with
`intended_robot_task`, `agents`, `expected_behaviors`, and `ideal_outcome`.

The new Card Summary "Related Scenarios: object_handover" line is internally
consistent with the embedded YAML's `related_scenarios: [object_handover]` and with
the Notes section's mention of Object Handover — the divergence from Table 3's own
"Food Delivery" citation (see Finding 1) is expected, not an internal prose/YAML
drift.

## Schema and Charter Compliance (Step 3)

- `scripts/distill/scenarios --scenario crash_cart --dry-run --show-diffs` produced no
  diff and no schema validation error — `scenario.yml` is in sync with `scenario.md`
  and validates against `schema.json`.
- `relevant_principles`: P1, P3, P7, P8 — four principles, all valid P0-P9 IDs, within
  the recommended 3-5 range.
- `scenario_usage_guide.quality_metrics`: P3, P8 — valid P0-P9 IDs.
- `expected_behaviors` entries describe kinds of behavior ("move at an elevated pace,"
  "signal urgent status," "take reasonable priority") rather than exact motions or
  numeric thresholds — no over-specification (P&G Guideline N6) found.
- `related_scenarios: [object_handover]` references a scenario directory that exists
  under `prosoc/scenarios/` (well-formed; see Finding 1 for the non-blocking note on
  Table 3 divergence).
