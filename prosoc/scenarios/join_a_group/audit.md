---
scenario: join_a_group
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-22
---

# Audit: Join a Group

- **Scenario:** `prosoc/scenarios/join_a_group/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready, no blocking or should-fix issues found

## Findings

### 1. Redundant duplicate field — suggestion
- **Section/field:** `agents.humans[0].count` vs `agents.humans[0].attributes.group_size`
- **Issue:** Both fields independently state the group size is 3 (`count: 3` and `attributes.group_size: 3`). Harmless today since both values agree, but a future edit to one without the other would silently desynchronize them.
- **Recommended fix:** Consider dropping `attributes.group_size` and relying solely on `count`, or explicitly document why both are kept (e.g., if `group_size` is meant to describe the F-formation size distinctly from the modeled agent count).

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Join a Group" (cited in [50, 161]), which matches the entry in `.claude/skills/_shared/pg_scenarios.md`:

| Table 3 field | Reference value | Scenario card |
|---|---|---|
| Description | Robot joins a group of robots or people | Matches — Overview: "robot navigating toward and joining a standing group of robots or people" |
| Physical Env | Generic | Matches — `context.environment.type: generic` |
| Geometric Layout | Open space | Matches — `geometric_layout: open space` |
| Scientific Purpose | Group interaction | Matches — `scientific_purpose: group interaction` |
| Robot Task | Navigate to group | Matches — `intended_robot_task: navigate to and join the group` |
| Human Behavior | Continue conversing | Matches — `intended_human_behavior: continue conversing, accommodating the robot's arrival` (elaboration, not contradiction) |
| Ideal Outcome | Robot joins group | Matches — `ideal_outcome: robot joins the group, settling into the formation without disrupting the conversation` |
| Related Scenarios | Leaving a Group | `related_scenarios` lists `crowd_navigation` rather than Leaving a Group, because Leaving a Group has no implemented scenario directory under `prosoc/scenarios/`. This is the expected, documented `related_scenarios`/Table 3 divergence pattern (see `audit_checklist.md`), not a source-fidelity defect — the card's own `evaluation_notes` "Related Scenarios note" paragraph (added in PR #30) explicitly explains the substitution. |
| Cited In | [50, 161] | Matches — `cited_in: ["50", "161"]` |

No mismatches found. Source fidelity: confirmed against Table 3.

## Completeness

`scripts/distill/scenarios --scenario join_a_group --dry-run --show-diffs` produced no diff and no schema errors — `scenario.yml` is in sync with the embedded YAML block and validates against `schema.json` (confirmed independently with `jsonschema.validate`).

Walking the fields `template.md` marks "Required for AUDITED scenarios":

- **Scenario Card Summary block** — present and complete (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In).
- **Scenario Usage Guide — Success Metrics** — present (`SR`, `NoCollisions`), matches YAML.
- **Scenario Usage Guide — Quality Metrics** — present (`P2`, `P4`, `P5`), matches YAML and is a sensible subset of `relevant_principles` (`P1`, `P2`, `P4`, `P5`, `P8`).
- **Scenario Usage Guide — Ideal Outcome** — present, matches YAML `ideal_outcome`.
- **Scenario Usage Guide — Failure Modes** — present, four modes, matches YAML.
- **Scenario Usage Guide — Labeling Criteria** — present, three criteria, matches YAML.

No blank required fields remain. Prose (Scenario Overview, Social Navigation Context, Normative Expectations) is internally consistent with the YAML's `intended_robot_task`, `intended_human_behavior`, `agents`, `expected_behaviors`, and `ideal_outcome` — no contradictions or drift found. `relevant_principles` (5 entries, all P0–P9) and `quality_metrics` are within the recommended 3–5 range. `expected_behaviors` entries describe kinds of behavior ("approach along a peripheral or curved path," "slow down when nearing the group's formation boundary") rather than exact motions or numeric thresholds — no over-specification per P&G Guideline N6.
