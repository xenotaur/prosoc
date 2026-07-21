---
scenario: crash_cart
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-07-20
---

# Audit: Crash Cart

- **Scenario:** `prosoc/scenarios/crash_cart/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Related Scenarios / Cited In not carried into Card Summary — should-fix
- **Section/field:** Scenario Card Summary — Related Scenarios / Cited In fields
- **Issue:** The rendered `## Scenario Card Summary` section (scenario.md lines 12-34) self-flags this under "Remaining gaps" as "should-fill-in-now" for both fields. Unlike a genuinely-unknown gap, the content already exists elsewhere in the card: the Notes section names Food Delivery (Table 3's listed Related Scenario) and Object Handover, and the Status block states "cited in this article." Because the values are already written and readily copyable, this stays should-fix rather than dropping to a suggestion.
- **Recommended fix:** Add `**Related Scenarios:** Food Delivery` and `**Cited In:** this article` lines to the Scenario Card Summary block, matching the template's field list.

### 2. Bystander count is an unstated elaboration — suggestion
- **Section/field:** Scenario Overview / Social Navigation Context prose vs. `agents.humans[0].count: 3`
- **Issue:** Prose still refers to "bystanders" and "pedestrians" generically throughout the Overview, Social Navigation Context, and Normative Expectations sections; no sentence grounds the specific `count: 3` chosen in the YAML. This is drift rather than contradiction — a reasonable concretization for simulation setup — but there's still no prose basis to confirm 3 specifically (vs. 1, 2, or more). Unresolved from the prior audit.
- **Recommended fix:** Either state an approximate bystander count in prose (e.g., "a small number of bystanders (2-3)") to ground the YAML's `count: 3`, or note in `evaluation_notes` that the count is a reasonable default subject to variation.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Crash Cart" entry, cited in "this article." Compared against `../../.claude/skills/_shared/pg_scenarios.md`:

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
| Related Scenarios | Food Delivery | Notes section: "related to Object Handover... and to Food Delivery" | Yes |
| Cited In | this article | Status block: "cited in this article" | Yes |

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

Re-checked against `template.md`'s "Required for AUDITED scenarios" fields, following the substantial rendering pass this session (Scenario Card Summary and Scenario Usage Guide are now both present as dedicated prose sections, resolving the prior audit's Findings 1 and 2; the bystander-awareness clarification in `initial_conditions.human_positions` — "initially unaware of the specific urgency but expected to update upon perceiving the robot's signaling" — resolves the prior audit's Finding 3):

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome) — present and populated (scenario.md lines 12-29).
- **Related Scenarios / Cited In** (Card Summary fields) — should-fill-in-now; values are already known and written elsewhere (Notes section, Status block) but not yet copied into the summary table. See Finding 1.
- **Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria** — all present as a dedicated `## Scenario Usage Guide` prose section (scenario.md lines 198-216), consistent with the embedded YAML's `scenario_usage_guide` block.

## Prose/YAML Consistency (Step 2)

No contradictions found. The bystander-awareness relationship between `initial_conditions.human_positions`, `intended_human_behavior`, and the Normative Expectations/`expected_behaviors` sections — flagged as ambiguous in the 2026-07-05 audit — is now internally consistent: bystanders start "unaware of the specific urgency" and are "expected to update upon perceiving the robot's signaling," which matches the prose's expectation that bystanders yield once the robot signals urgency and matches `expected_behaviors.should` ("signal urgent status clearly to bystanders... so they can accommodate it"). Scenario Overview, Social Navigation Context, and Normative Expectations otherwise align cleanly with `intended_robot_task`, `agents`, `expected_behaviors`, and `ideal_outcome`.

## Schema and Charter Compliance (Step 3)

- `scripts/distill/scenarios --scenario crash_cart --dry-run --show-diffs` produced no diff and no schema validation error — `scenario.yml` is in sync with `scenario.md` and validates against `schema.json`.
- `relevant_principles`: P1, P3, P7, P8 — four principles, all valid P0-P9 IDs, within the recommended 3-5 range.
- `scenario_usage_guide.quality_metrics`: P3, P8 — valid P0-P9 IDs.
- `expected_behaviors` entries describe kinds of behavior ("move at an elevated pace," "signal urgent status," "take reasonable priority") rather than exact motions or numeric thresholds — no over-specification (P&G Guideline N6) found.
