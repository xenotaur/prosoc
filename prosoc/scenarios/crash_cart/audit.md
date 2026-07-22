---
scenario: crash_cart
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-07-21
---

# Audit: Crash Cart

- **Scenario:** `prosoc/scenarios/crash_cart/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready for AUDITED with one fix to reconcile against source

## Findings

### 1. `related_scenarios` names a different scenario than Table 3's own entry — should-fix
- **Section/field:** `related_scenarios` (scenario.yml / embedded YAML) and Scenario
  Card Summary "Related Scenarios" (scenario.md line 30) vs. P&G Table 3
- **Issue:** The newly backfilled `related_scenarios: [object_handover]` (and matching
  Card Summary line `**Related Scenarios:** object_handover`) does not match what
  Table 3 itself lists as Crash Cart's related scenario. `../../.claude/skills/_shared/pg_scenarios.md`
  line 246 gives Crash Cart's Table-3 "Related Scenarios" value as **Food Delivery**,
  not Object Handover. The card's own Notes section (scenario.md lines 225-227)
  already draws this distinction correctly in prose — it names Object Handover as an
  analytically related scenario in its own right ("the general delivery and handoff
  task without time pressure") *and separately* names Food Delivery as the Table-3
  cross-reference ("a related delivery context implied by the paper's 'Related
  Scenarios' note ... not separately defined in Table 3"). The backfill appears to
  have picked up the Notes' first/more prominent comparison (Object Handover, which
  has an implemented scenario directory) rather than the value Table 3 itself records
  (Food Delivery, which has no implemented directory under `prosoc/scenarios/`).
  This is a genuine source-fidelity mismatch, not present in the 2026-07-20 audit
  because `related_scenarios` did not yet exist as a populated field at that time.
- **Recommended fix:** A human editor should decide the intent: (a) if
  `related_scenarios` is meant to mirror Table 3's citation, correct it to reference
  Food Delivery (adding a note that no scenario directory exists for it yet, since
  it's unimplemented), or (b) if it's meant to be a practical cross-reference to
  scenarios that actually exist in this repo, keep `object_handover` but add a short
  note (e.g. in `evaluation_notes` or the Notes section) explicitly flagging that this
  diverges from Table 3's own "Food Delivery" citation and explaining why. Either is
  defensible, but the current state — silently substituting one for the other with no
  note of the divergence — risks looking like an unnoticed error on a future source
  fidelity check.

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
against `../../.claude/skills/_shared/pg_scenarios.md`:

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
| Related Scenarios | Food Delivery | `related_scenarios: [object_handover]` | **No — mismatch.** See Finding 1. |
| Cited In | this article | `cited_in: ["this article"]` | Yes |

One mismatch found (Related Scenarios — see Finding 1). All other fields confirmed
against P&G Table 3.

## Completeness

Re-checked against `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose, Physical
  Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success
  Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) — present and
  populated (scenario.md lines 12-31). Related Scenarios and Cited In are now filled
  in, resolving the prior audit's should-fix finding about those fields being
  tracked only in the Status block/Notes rather than the summary table — but see
  Finding 1 for a correctness issue in the value chosen for Related Scenarios.
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
the Notes section's mention of Object Handover — the inconsistency is external, against
Table 3 (see Finding 1), not an internal prose/YAML drift.

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
- `related_scenarios: [object_handover]` references a scenario ID that exists as a
  directory under `prosoc/scenarios/` (well-formed, but see Finding 1 for the
  source-fidelity concern independent of well-formedness).
