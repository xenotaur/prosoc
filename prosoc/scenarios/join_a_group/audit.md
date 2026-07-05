# Audit: Join a Group

- **Scenario:** `prosoc/scenarios/join_a_group/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready — 2 blocking issues

## Findings

### 1. Scenario Card Summary section is missing — blocking
- **Section/field:** Scenario Card Summary (template.md: "Required for AUDITED scenarios")
- **Issue:** `scenario.md` has no `## Scenario Card Summary` section at all. `template.md` requires this block (Scenario Name, Scenario Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) for any scenario reaching AUDITED. The card currently jumps from `## Status` straight to `## Scenario Overview`.
- **Recommended fix:** Add a `## Scenario Card Summary` section populated from the existing YAML/prose content (much of the raw material — scientific purpose, geometric layout, robot role/task, human behavior, ideal outcome — is already present in the YAML block and could be transcribed rather than re-derived) before this scenario is promoted past DRAFTED toward AUDITED.

### 2. Scenario Usage Guide prose section is missing — blocking
- **Section/field:** Scenario Usage Guide — Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria (template.md: "Required for AUDITED scenarios")
- **Issue:** `scenario.md` has no `## Scenario Usage Guide` section with the five required subsections. The equivalent content exists only inside the embedded YAML (`scenario_usage_guide.success_metrics`, `.quality_metrics`, `.failure_modes`, `.labeling_criteria`, and top-level `ideal_outcome`), not as human-readable prose alongside it, contrary to template.md's structure (the YAML is meant to be the machine-readable mirror of prose sections that also exist independently).
- **Recommended fix:** Add a `## Scenario Usage Guide` section with the five subsections, largely restating the YAML's `scenario_usage_guide` fields and `ideal_outcome` in prose form.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Join a Group" (cited in [50, 161]), which matches the entry in `../../.claude/skills/_shared/pg_scenarios.md`:

| Table 3 field | Reference value | Scenario card |
|---|---|---|
| Description | Robot joins a group of robots or people | Matches — Overview: "robot navigating toward and joining a standing group of robots or people" |
| Physical Env | Generic | Matches — `context.environment.type: generic` |
| Geometric Layout | Open space | Matches — `geometric_layout: open space` |
| Scientific Purpose | Group interaction | Matches — `scientific_purpose: group interaction` |
| Robot Task | Navigate to group | Matches — `intended_robot_task: navigate to and join the group` |
| Human Behavior | Continue conversing | Matches — `intended_human_behavior: continue conversing, accommodating the robot's arrival` (accommodating clause is an elaboration, not a contradiction) |
| Ideal Outcome | Robot joins group | Matches — `ideal_outcome: robot joins the group, settling into the formation without disrupting the conversation` |
| Related Scenarios | Leaving a Group | Matches — noted in Notes section and evaluation_notes |
| Cited In | [50, 161] | Matches — Status block |

No mismatches found. Source fidelity: confirmed against Table 3.

## Completeness

Walking the fields `template.md` marks "Required for AUDITED scenarios":

- **Scenario Card Summary block** — should-fill-in-now (see Finding 1). All constituent facts (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome, Related Scenarios, Cited In) are already available elsewhere in the card (YAML fields, Status block, Notes section) and only need to be assembled into the required section.
- **Scenario Usage Guide — Success Metrics** — should-fill-in-now (see Finding 2). Values (`SR`, `NoCollisions`) already exist in YAML.
- **Scenario Usage Guide — Quality Metrics** — should-fill-in-now. Values (`P2`, `P4`, `P5`) already exist in YAML.
- **Scenario Usage Guide — Ideal Outcome** — should-fill-in-now. Already stated concisely in YAML `ideal_outcome` and could be restated in one sentence of prose.
- **Scenario Usage Guide — Failure Modes** — should-fill-in-now. Four failure modes already enumerated in YAML; not yet mirrored in prose.
- **Scenario Usage Guide — Labeling Criteria** — should-fill-in-now. Three criteria already enumerated in YAML; not yet mirrored in prose.
- **Related Scenarios / Cited In** (optional sub-fields) — reasonably present already, just not inside a formal Summary block (see Finding 1) — content itself is not blank.
