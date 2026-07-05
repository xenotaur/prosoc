# Audit: Entering Room

- **Scenario:** `prosoc/scenarios/entering_room/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Ready for AUDITED with minor fixes — no blocking issues, some should-fix completeness gaps

## Findings

### 1. Missing "Scenario Card Summary" section — should-fix
- **Section/field:** Markdown structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Card Summary block
- **Issue:** `scenario.md` has no `## Scenario Card Summary` section. `template.md` marks this block (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) as required for AUDITED scenarios, drawn from Tables 2/3 of the P&G paper. The document goes straight from `## Status` to `## Scenario Overview`.
- **Recommended fix:** Add a `## Scenario Card Summary` section populated from data already present in the embedded YAML and STATUS block (e.g., Scientific Purpose: pedestrian interaction; Physical Environment: indoor; Geometric Layout: room and door; Robot Role: navigating_agent; Robot Task: navigate from outside to inside the room; Human Behavior: navigate from inside to outside; Ideal Outcome: robot lets the human exit fully, then enters without obstruction; Related Scenarios: Entering Elevator, Exiting Room, Narrow Doorway; Cited In: R@G).

### 2. Missing "Scenario Usage Guide" prose subsections — should-fix
- **Section/field:** Markdown structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)
- **Issue:** The document has no `## Scenario Usage Guide` section with these five subsections as prose. The content exists in the YAML's `scenario_usage_guide` block (`success_metrics`, `quality_metrics`, `failure_modes`, `labeling_criteria`) and top-level `ideal_outcome`, but is not surfaced as human-readable prose per the template.
- **Recommended fix:** Add a `## Scenario Usage Guide` section with the five subheadings, restating the YAML list content in prose/bulleted form for human readability, as the template specifies.

### 3. P3 (Legibility) not included in relevant_principles — suggestion
- **Section/field:** `relevant_principles` vs. `_shared/principles.md` selection guidance
- **Issue:** The scenario's normative core is about the robot recognizing and communicating deference at a threshold ("proceed to enter promptly once the threshold is clear," avoiding "waiting so far back... entry is delayed"). P3 (Legibility — behave so robot goals can be understood by others) arguably applies here, since a human benefits from being able to tell that the robot is intentionally waiting rather than malfunctioning or blocked. Current selection (P1, P4, P5, P6) is reasonable and within the 3-5 guidance, so this is not a defect, just worth a human's consideration.
- **Recommended fix:** Optionally add P3 if the editor agrees legibility of the robot's "waiting" intent is a distinct concern from politeness/social-norm compliance; otherwise no change needed.

## Source Fidelity

SOURCE cites P&G Paper Table 3 and Robots@Games (R@G). Compared against `_shared/pg_scenarios.md`'s "Entering Room" entry (Doorway Scenarios section):

- Description ("Robot enters a room occupied by a human") — matches.
- Physical Environment: Indoor — matches (`context.environment.type: indoor`).
- Geometric Layout: Room and door — matches (`geometric_layout: room and door`).
- Scientific Purpose: Pedestrian interaction — matches (`scientific_purpose: pedestrian interaction`).
- Robot Task: Navigate out to in — matches (`intended_robot_task: navigate from outside to inside the room`).
- Human Behavior: Navigate in to out — matches (`intended_human_behavior: navigate from inside to outside the room`).
- Ideal Outcome: Robot lets human exit — matches almost verbatim (`ideal_outcome: robot lets the human exit fully, then enters the room without obstruction`).
- Related Scenarios: Entering Elevator (R@G) — matches (cross-referenced in `evaluation_notes` and the Notes section; card also adds Exiting Room and Narrow Doorway as related, which is a reasonable extension consistent with `pg_scenarios.md`'s note that Exiting Room and Narrow Doorway are themselves Table 3 doorway-family entries).
- Cited In: R@G — matches STATUS field ("Robots@Games (R@G)").

No mismatches found. Source fidelity: confirmed against P&G Table 3 / R@G.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" checklist:

- **Scenario Card Summary block** — should-fill-in-now. Section is entirely absent from the Markdown prose, though its constituent data (scientific purpose, geometric layout, robot role/task, human behavior, ideal outcome, related scenarios, cited-in) is already present in the YAML and STATUS block and is directly inferable. See Finding 1.
- **Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)** — should-fill-in-now. Section is absent as prose; equivalent YAML lists (`scenario_usage_guide.success_metrics/quality_metrics/failure_modes/labeling_criteria`, top-level `ideal_outcome`) already exist and just need to be restated in prose form. See Finding 2.
- **Related Scenarios / Cited In** (sub-fields of the summary block) — reasonably present in spirit: covered in the `evaluation_notes` YAML field and the "Notes for Scenario Designers and Evaluators" prose section, just not in the dedicated summary-block fields called for by the template.
