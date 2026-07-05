# Audit: Crowd Navigation

- **Scenario:** `prosoc/scenarios/crowd_navigation/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Ready for AUDITED with minor fixes — no blocking issues, several should-fix completeness gaps

## Findings

### 1. Missing "Scenario Card Summary" section — should-fix
- **Section/field:** Markdown structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Card Summary block
- **Issue:** `scenario.md` has no `## Scenario Card Summary` section. `template.md` marks this block (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) as required for AUDITED scenarios, drawn from Tables 2/3 of the P&G paper. The document goes straight from `## Status` to `## Scenario Overview`.
- **Recommended fix:** Add a `## Scenario Card Summary` section populated from data already present in the embedded YAML and STATUS block (e.g., Scientific Purpose: crowd navigation; Physical Environment: generic/indoor-outdoor unspecified; Geometric Layout: passable space; Robot Role: navigating_agent; Robot Task: navigate through the crowd to a destination on the far side; Human Behavior: mill about; Ideal Outcome: robot crosses the crowd without collision or obstruction; Related Scenarios: Robot Crowding, Parallel Traffic, Perpendicular Traffic; Cited In: various).

### 2. Missing "Scenario Usage Guide" prose subsections — should-fix
- **Section/field:** Markdown structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)
- **Issue:** The document has no `## Scenario Usage Guide` section with these five subsections as prose. The content exists in the YAML's `scenario_usage_guide` block (`success_metrics`, `quality_metrics`, `failure_modes`, `labeling_criteria`) and top-level `ideal_outcome`, but is not surfaced as human-readable prose per the template.
- **Recommended fix:** Add a `## Scenario Usage Guide` section with the five subheadings, restating the YAML list content in prose/bulleted form for human readability, as the template specifies.

### 3. Some unacceptable behaviors in prose lack a direct YAML counterpart — suggestion
- **Section/field:** Normative Expectations vs. `expected_behaviors.should_not`
- **Issue:** The prose lists "Colliding with or forcing evasive action from any individual" and "Ignoring local density changes and proceeding at a fixed pace regardless of how crowded the immediate space becomes" as unacceptable behaviors. The YAML `must` captures collision avoidance but not "forcing evasive action" specifically, and `should_not` has no entry for ignoring density changes / fixed-pace navigation (only "excessively wide detours," "erratic/reversing," and "freeze indefinitely" are present, which are related but not the same failure as "proceeds at a fixed pace regardless of density").
- **Recommended fix:** Consider adding a `should_not` entry along the lines of "proceed at a fixed pace or clearance regardless of local crowd density" to close this gap, or confirm it's intentionally left as an implicit consequence of the existing entries.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "cited in various." Compared against `../../../.claude/skills/_shared/pg_scenarios.md`'s "Crowd Navigation" entry (Crowd Scenarios section):

- Description ("A robot navigates through a crowd") — matches.
- Physical Environment: Generic — matches (`context.environment.type: generic`).
- Geometric Layout: Passable space — matches (`geometric_layout: passable space`).
- Scientific Purpose: Crowd navigation — matches (`scientific_purpose: crowd navigation`).
- Robot Task: Navigate thru — matches (`intended_robot_task: navigate through the crowd to a destination on the far side`).
- Human Behavior: Mill about — matches (`intended_human_behavior: mill about, moving independently...`).
- Ideal Outcome: No collision/obstruction — matches, with an added "steady progress" clause that is an elaboration rather than a contradiction.
- Related Scenarios: Robot Crowding — matches; card also correctly cross-references Parallel Traffic and Perpendicular Traffic (documented in `pg_scenarios.md`'s "Additional Scenarios" note as related structured-crowd variants).
- Cited In: Various — matches STATUS field.

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" checklist:

- **Scenario Card Summary block** — should-fill-in-now. Section is entirely absent from the Markdown prose, though its constituent data (scientific purpose, geometric layout, robot role/task, human behavior, ideal outcome, related scenarios, cited-in) is already present in the YAML and STATUS block and is directly inferable. See Finding 1.
- **Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)** — should-fill-in-now. Section is absent as prose; equivalent YAML lists (`scenario_usage_guide.success_metrics/quality_metrics/failure_modes/labeling_criteria`, top-level `ideal_outcome`) already exist and just need to be restated in prose form. See Finding 2.
- **Related Scenarios / Cited In** (sub-fields of the summary block) — reasonably present in spirit: covered in the `evaluation_notes` YAML field and the "Notes for Scenario Designers and Evaluators" prose section, just not in the dedicated summary-block fields called for by the template.
