# Audit: Following

- **Scenario:** `prosoc/scenarios/following/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Missing "Scenario Card Summary" section — should-fix
- **Section/field:** `scenario.md` structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Card Summary block
- **Issue:** `scenario.md` goes directly from the `## Status` block to `## Scenario Overview`. There is no standalone "Scenario Card Summary" section presenting Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, and Cited In as a scannable table, as `template.md` specifies for AUDITED scenarios. The equivalent information already exists inside the embedded YAML (`scientific_purpose`, `geometric_layout`, `agents.robot.role`, `intended_robot_task`, etc.) but not as the dedicated prose summary section.
- **Recommended fix:** A human editor should add a "Scenario Card Summary" section populated from the existing YAML fields (a mechanical transcription, not new content) before promoting to AUDITED.

### 2. Missing standalone "Scenario Usage Guide" prose section — should-fix
- **Section/field:** `scenario.md` structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Usage Guide (Success Metrics / Quality Metrics / Ideal Outcome / Failure Modes / Labeling Criteria)
- **Issue:** These fields exist and are populated inside the embedded YAML's `scenario_usage_guide` block (`success_metrics`, `quality_metrics`, `failure_modes`, `labeling_criteria`) and `ideal_outcome`, but `scenario.md` has no dedicated human-readable "Scenario Usage Guide" section with those subheadings, as distinct prose, per the template.
- **Recommended fix:** A human editor should add the prose "Scenario Usage Guide" section, transcribing the already-authored YAML content into readable form.

### 3. Reference-table "Robot Task" wording is internally inconsistent, unremarked by the card — suggestion
- **Section/field:** Source Fidelity — P&G Table 3 "Robot Task" field vs. `intended_robot_task`
- **Issue:** The reference data (`.claude/skills/_shared/pg_scenarios.md`) lists Table 3's Robot Task for this scenario as "Follow lead robot," which is very likely itself a transcription artifact in the source table (the scenario Description reads "A robot follows a person," not another robot). The card sensibly renders this as `intended_robot_task: follow the lead human`, which is more internally coherent than the literal table text, but the card does not call out this discrepancy the way `exiting_room`'s card explicitly notes its own Table 3 ambiguity.
- **Recommended fix:** Optional — a human editor with access to the original P&G paper could add a short `evaluation_notes` remark (as `exiting_room` does) noting that the card's "follow the lead human" reading resolves an apparent wording slip in the reference table's "Follow lead robot" text, for consistency with how the sibling scenario documents its own source ambiguity.

## Source Fidelity

SOURCE cites P&G Paper Table 3, cited in [50]. Compared against `.claude/skills/_shared/pg_scenarios.md`'s "Following" entry:

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | A robot follows a person | Robot in servant role follows a leading human | Match |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Walking space | `geometric_layout: walking space` | Match |
| Scientific Purpose | Joint navigation | `scientific_purpose: joint navigation` | Match |
| Robot Role | Servant | `agents.robot.role: servant` | Match |
| Robot Task | Follow lead robot (likely a transcription slip in the source table) | `intended_robot_task: follow the lead human` | Coherent reading, see Finding 3 |
| Human Behavior | Lead human | `intended_human_behavior: lead, navigating freely through the space...` | Match |
| Ideal Outcome | Robot follows person | `ideal_outcome: robot follows the person continuously...` | Match |
| Related Scenarios | Accompany Peer | Covered in "Notes for Scenario Designers and Evaluators" and `evaluation_notes` (also correctly notes "Leading" as the role-reversed counterpart) | Match |
| Cited In | [50] | STATUS block cites "[50]" | Match |

All fields match the reference data, aside from the minor Robot Task wording note above (Finding 3), which does not rise to a contradiction given the Description field's clear framing.

## Completeness

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In): **should probably be filled in now** — all underlying data already exists in the YAML block; this is a transcription task, not new authoring. See Finding 1.
- **Scenario Usage Guide** (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria as prose subsections): **should probably be filled in now** — same reasoning; content already exists in `scenario_usage_guide.*` YAML fields. See Finding 2.
- **Related Scenarios / Cited In** (if presented as part of Scenario Card Summary): **reasonably blank as a standalone field for now**, since the equivalent content (Leading, Accompany Peer) is already covered in the "Notes for Scenario Designers and Evaluators" section and `evaluation_notes`; filling in the Scenario Card Summary (Finding 1) would naturally surface this too.
