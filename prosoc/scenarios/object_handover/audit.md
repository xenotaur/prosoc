# Audit: Object Handover

- **Scenario:** `prosoc/scenarios/object_handover/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready for AUDITED — required prose sections missing; STATE is still DRAFTED, not EDITED

## Findings

### 1. Scenario Card Summary section missing from scenario.md — should-fix
- **Section/field:** Scenario Card Summary (template.md: "Required for AUDITED scenarios")
- **Issue:** `scenario.md` has no `## Scenario Card Summary` heading at all. template.md requires this human-readable block (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) as prose, distinct from the embedded YAML. All of the underlying data exists in the YAML block and is fully consistent with the P&G Table 3 source, so this is a presentation/completeness gap rather than a content gap.
- **Recommended fix:** Add a `## Scenario Card Summary` section between `## Status` and `## Scenario Overview`, populated from the existing YAML fields (name, summary, scientific_purpose, geometric_layout, agents.robot.role, intended_robot_task, intended_human_behavior, ideal_outcome) plus the STATUS block's SOURCE citation ("[161]") for Cited In, and evaluation_notes' mentions of Crash Cart / Robot Courier for Related Scenarios.

### 2. Scenario Usage Guide prose section missing from scenario.md — should-fix
- **Section/field:** Scenario Usage Guide (template.md: "Required for AUDITED scenarios" — Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)
- **Issue:** `scenario.md` has no `## Scenario Usage Guide` heading with the five required subsections. The equivalent data exists only inside the embedded YAML's `scenario_usage_guide` block (success_metrics, quality_metrics, failure_modes, labeling_criteria) — there is no human-readable prose rendering of it, which template.md requires as a distinct section for AUDITED scenarios.
- **Recommended fix:** Add a `## Scenario Usage Guide` section (after `## Scenario Specification (Machine-Readable)`, before or merged with `## Notes for Scenario Designers and Evaluators`) with `### Success Metrics`, `### Quality Metrics`, `### Ideal Outcome`, `### Failure Modes`, `### Labeling Criteria` subsections, restating the YAML's `scenario_usage_guide` and `ideal_outcome` content in prose form.

### 3. STATE is DRAFTED, not EDITED — should-fix
- **Section/field:** Status block (`## Status`)
- **Issue:** The Status block shows `STATE: DRAFTED` with `EDITED: —`. Per `workflow.md`, AUDITED normally follows an EDITED stage where the scenario has been "revised for clarity, consistency, and alignment with the conventions of the `prosoc` project" and judged "structurally sound." This scenario has not yet passed through an EDITED stage, and the missing prose sections (Findings 1-2) are exactly the kind of structural gap an EDITED pass would be expected to close.
- **Recommended fix:** Before promoting to AUDITED, a human editor should move the scenario through EDITED (filling in the missing prose sections above, updating the Status block accordingly) rather than promoting directly from DRAFTED.

### 4. Normative Expectations prose doesn't mirror the must/should/should_not split — suggestion
- **Section/field:** Normative Expectations vs. `expected_behaviors.{must,should,should_not}`
- **Issue:** The prose "Normative Expectations" section presents two flat lists ("Acceptable robot behavior includes" / "Unacceptable behavior includes") without distinguishing `must` (strictly required) from `should` (preferred). For example, "Waiting for a clear indication of grip before releasing the object" reads like a strict requirement but its YAML counterpart ("not release the object before the human has a secure grip") is correctly in `must`, while "Approaching the human at a moderate, predictable pace" is in `should` — the prose doesn't signal this required/preferred distinction to a human reader relying only on prose. Not a contradiction (content matches), just drift in emphasis.
- **Recommended fix:** Optionally annotate the prose list (e.g., "(required)" / "(preferred)" tags) or reorder to visually group must-items first, so a prose-only reader gets the same must/should signal as the YAML.

## Source Fidelity

SOURCE cites "P&G Paper, Table 3 ... cited in [161]." Compared against `_shared/pg_scenarios.md`'s Object Handover entry (Specialized Scenarios section):

| Field | P&G Table 3 | Scenario card | Result |
|---|---|---|---|
| Description | "A robot hands an object to a human" | Servant robot navigates to human and hands over object | Match |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Passable space | `geometric_layout: passable space` | Match |
| Scientific Purpose | Interactive navigation | `scientific_purpose: interactive navigation` | Match |
| Robot Role | Servant | `agents.robot.role: servant` | Match |
| Robot Task | Deliver object | `intended_robot_task: deliver the object to the human` | Match |
| Human Behavior | Receive object | `intended_human_behavior: receive the object` | Match |
| Ideal Outcome | Human takes object | `ideal_outcome: human takes the object ... without awkwardness, collision, or dropped object` | Match (elaborated, not contradicted) |
| Related Scenarios | Robot Courier | `evaluation_notes` cites Robot Courier and Crash Cart | Match (superset) |
| Cited In | [161] | STATUS block cites "[161]" | Match |

No mismatches found. Note: `robot_courier` does not yet exist as an implemented scenario directory in this repo (only `crash_cart` does) — this doesn't affect fidelity to the P&G source, but the "Related Scenarios" reference in the card points to a scenario not yet drafted.

## Completeness

Per template.md's "Required for AUDITED scenarios" checklist:

**Scenario Card Summary block — entire section blank/missing (should probably be filled in now):**
- Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome, Related Scenarios, Cited In — all readily inferable from the existing YAML block and STATUS field; nothing here is genuinely unknown. See Finding 1.
- Success/Quality Metrics — same: directly available from `scenario_usage_guide.success_metrics` / `quality_metrics` in the YAML.

**Scenario Usage Guide (prose) — entire section blank/missing (should probably be filled in now):**
- Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria — all already populated in the YAML's `scenario_usage_guide` block and just need prose restatement. See Finding 2.

**Fields that are reasonably blank / not applicable:**
- None identified as problematic beyond the two sections above — the YAML content itself (agents, context, expected_behaviors, evaluation_notes) is fully populated and consistent, so there is no missing *information*, only missing *prose presentation* of information that already exists.
