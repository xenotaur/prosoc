---
scenario: leading
verdict: not_ready
blocking: 2
should_fix: 0
suggestion: 1
audited: 2026-07-05
---

# Audit: Leading

- **Scenario:** `prosoc/scenarios/leading/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready — 2 blocking issues

## Findings

### 1. Scenario Card Summary section is missing — blocking
- **Section/field:** Scenario Card Summary (template.md: "Required for AUDITED scenarios")
- **Issue:** `scenario.md` has no `## Scenario Card Summary` section. `template.md` requires this block (Scenario Name, Scenario Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) for any scenario reaching AUDITED. The card currently jumps from `## Status` straight to `## Scenario Overview`.
- **Recommended fix:** Add a `## Scenario Card Summary` section. Nearly all constituent facts (scientific purpose, geometric layout, robot role `leader`, robot task, human behavior, ideal outcome) are already present in the YAML block or Notes section and could be transcribed rather than re-derived, before this scenario is promoted past DRAFTED toward AUDITED.

### 2. Scenario Usage Guide prose section is missing — blocking
- **Section/field:** Scenario Usage Guide — Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria (template.md: "Required for AUDITED scenarios")
- **Issue:** `scenario.md` has no `## Scenario Usage Guide` section with the five required subsections. The equivalent content exists only inside the embedded YAML (`scenario_usage_guide.success_metrics`, `.quality_metrics`, `.failure_modes`, `.labeling_criteria`, and top-level `ideal_outcome`), not as human-readable prose alongside it.
- **Recommended fix:** Add a `## Scenario Usage Guide` section with the five subsections, largely restating the YAML's `scenario_usage_guide` fields and `ideal_outcome` in prose form.

### 3. `initial_conditions` duplicates `intended_robot_task` — suggestion
- **Section/field:** Scenario Specification (Machine-Readable) — `initial_conditions.robot_task`
- **Issue:** `initial_conditions.robot_task: guide the human to a destination` restates the same fact as the top-level `intended_robot_task: lead the human to a destination` field, in slightly different wording ("guide" vs. "lead"). `initial_conditions` is meant to describe spatial/temporal/situational starting conditions (per schema.json's description and the other two sibling keys `robot_position`/`human_position`), not to restate the task. The wording difference ("guide" vs. "lead") is harmless but redundant.
- **Recommended fix:** Either remove `initial_conditions.robot_task` (the task is already fully captured by `intended_robot_task`) or, if keeping it for situational framing, align its wording with `intended_robot_task` to avoid two slightly different phrasings of the same fact.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Leading" (cited in [50]), which matches the entry in `../../../.claude/skills/_shared/pg_scenarios.md`:

| Table 3 field | Reference value | Scenario card |
|---|---|---|
| Description | A robot leads a person | Matches — Overview: "a robot in a leader role whose task is to guide a human through a walking space" |
| Physical Env | Generic | Matches — `context.environment.type: generic` |
| Geometric Layout | Walking space | Matches — `geometric_layout: walking space` |
| Scientific Purpose | Joint navigation | Matches — `scientific_purpose: joint navigation` |
| Robot Role | Leader | Matches — `agents.robot.role: leader` |
| Robot Task | Lead human | Matches — `intended_robot_task: lead the human to a destination` |
| Human Behavior | Follow robot | Matches — `intended_human_behavior: follow the robot, tracking its path and pace` |
| Ideal Outcome | Person follows robot | Matches — `ideal_outcome: person follows the robot to the destination, with the robot adapting pace and signaling turns so the human stays with it` |
| Related Scenarios | Tour Guide | Matches — noted in Notes section and evaluation_notes |
| Cited In | [50] | Matches — Status block |

No mismatches found. Source fidelity: confirmed against Table 3.

## Completeness

Walking the fields `template.md` marks "Required for AUDITED scenarios":

- **Scenario Card Summary block** — should-fill-in-now (see Finding 1). All constituent facts (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome, Related Scenarios, Cited In) are already available elsewhere in the card (YAML fields, Status block, Notes section) and only need to be assembled into the required section.
- **Scenario Usage Guide — Success Metrics** — should-fill-in-now (see Finding 2). Values (`SR`, `NoCollisions`, `TTG`) already exist in YAML.
- **Scenario Usage Guide — Quality Metrics** — should-fill-in-now. Values (`P3`, `P6`) already exist in YAML.
- **Scenario Usage Guide — Ideal Outcome** — should-fill-in-now. Already stated concisely in YAML `ideal_outcome` and could be restated in one sentence of prose.
- **Scenario Usage Guide — Failure Modes** — should-fill-in-now. Four failure modes already enumerated in YAML; not yet mirrored in prose.
- **Scenario Usage Guide — Labeling Criteria** — should-fill-in-now. Three criteria already enumerated in YAML; not yet mirrored in prose.
- **Related Scenarios / Cited In** (optional sub-fields) — reasonably present already, just not inside a formal Summary block (see Finding 1) — content itself is not blank.
