# Audit: Exiting Room

- **Scenario:** `prosoc/scenarios/exiting_room/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Missing "Scenario Card Summary" section — should-fix
- **Section/field:** `scenario.md` structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Card Summary block
- **Issue:** `scenario.md` goes directly from the `## Status` block to `## Scenario Overview`. There is no standalone "Scenario Card Summary" section presenting Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, and Cited In as a scannable table, as `template.md` specifies for AUDITED scenarios. The equivalent information exists scattered inside the embedded YAML (`scientific_purpose`, `geometric_layout`, `intended_robot_task`, etc.) but not as the dedicated prose summary section.
- **Recommended fix:** A human editor should add a "Scenario Card Summary" section populated from the existing YAML fields (this is a mechanical transcription, not new content) before promoting to AUDITED. Note this same gap appears in other scenario cards in the corpus (e.g. `entering_room`, `blind_corner`), so it may reflect a project-wide template drift rather than an issue unique to this card — worth flagging to the project maintainer if a corpus-wide fix is warranted (out of scope for this single-scenario audit).

### 2. Missing standalone "Scenario Usage Guide" prose section — should-fix
- **Section/field:** `scenario.md` structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Usage Guide (Success Metrics / Quality Metrics / Ideal Outcome / Failure Modes / Labeling Criteria)
- **Issue:** These fields exist and are populated inside the embedded YAML's `scenario_usage_guide` block (`success_metrics`, `quality_metrics`, `failure_modes`, `labeling_criteria`) and `ideal_outcome`, but `scenario.md` has no dedicated human-readable "Scenario Usage Guide" section with those subheadings, as distinct prose, per the template.
- **Recommended fix:** A human editor should add the prose "Scenario Usage Guide" section (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria subheadings) transcribing the already-authored YAML content into readable form.

### 3. Robot Role left implicit — suggestion
- **Section/field:** Scenario Card Summary (would-be) "Robot Role" field vs. YAML `agents.robot.role: navigating_agent`
- **Issue:** `navigating_agent` is a generic role label; it doesn't convey the "exits first" priority-holder framing that the prose spends two sections establishing. This isn't a contradiction (P&G Table 3 also leaves Robot Role blank for this entry), but a more specific role label could make the card's intent clearer at a glance.
- **Recommended fix:** Optional — a human editor could consider whether a more descriptive role tag (still schema-valid as a free-form string) would aid legibility of the card itself, though this is not required by schema or template.

## Source Fidelity

SOURCE cites P&G Paper Table 3. Compared against `.claude/skills/_shared/pg_scenarios.md`'s "Exiting Room" entry:

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | Robot exits a room while a human enters | Robot exits while human enters through same doorway | Match |
| Physical Env | Indoor | `context.environment.type: indoor` | Match |
| Geometric Layout | Room and door | `geometric_layout: room and door` | Match |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Match |
| Robot Task | Navigate in to out | `intended_robot_task: navigate from inside to outside the room` | Match |
| Human Behavior | **Navigate in to out** (as literally transcribed in Table 3) | `intended_human_behavior: navigate from outside to inside the room` | **Discrepancy, already flagged by the card itself** |
| Ideal Outcome | Robot exits first | `ideal_outcome: robot exits the room first, then the human enters...` | Match |

The one discrepancy is the Human Behavior field: Table 3 as transcribed in the reference data literally reads "Navigate in to out" for Human Behavior, identical to the Robot Task field, which is inconsistent with the Description ("human enters") and the Ideal Outcome ("robot exits first"). This card's own `evaluation_notes` already identifies this exact inconsistency, attributes it to a probable transcription error in the source, and states the card follows the Description/Ideal Outcome reading (human enters, i.e., "outside to inside") rather than the literal Human Behavior field text. This is a reasonable, transparently-documented interpretive call — not a fabricated fidelity claim — and matches the reference data available in this repo. A human editor with access to the original P&G paper PDF could still verify which reading is correct, as the card itself recommends.

All other fields match cleanly.

## Completeness

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In): **should probably be filled in now** — all underlying data already exists in the YAML block; this is a transcription task, not new authoring. See Finding 1.
- **Scenario Usage Guide** (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria as prose subsections): **should probably be filled in now** — same reasoning; content already exists in `scenario_usage_guide.*` YAML fields. See Finding 2.
- **Related Scenarios / Cited In** (if presented as part of Scenario Card Summary): **reasonably blank as a standalone field for now**, since the equivalent content (Entering Room, Exiting Elevator) is already covered in the "Notes for Scenario Designers and Evaluators" section and in `evaluation_notes`; filling in the Scenario Card Summary (Finding 1) would naturally surface this too.
