---
scenario: join_a_group
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-21
---

# Audit: Join a Group

- **Scenario:** `prosoc/scenarios/join_a_group/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready, no blocking or should-fix issues found

## Findings

### 1. `related_scenarios` diverges from Table 3's stated related scenario — suggestion
- **Section/field:** `related_scenarios` (YAML) vs. P&G Table 3 "Related Scenarios" and the card's own "Notes for Scenario Designers and Evaluators" section
- **Issue:** `related_scenarios` now lists only `crowd_navigation`. Table 3 lists "Leaving a Group" as Join a Group's related scenario, and the card's Notes/`evaluation_notes` discuss *Leave Group* (its "natural inverse") and *Accompany Peer* at least as prominently as *Crowd Navigation*. `crowd_navigation` is a reasonable and schema-correct choice — `related_scenarios` must reference an implemented scenario directory per `schema.json`'s description, and neither `leave_group` nor `accompany_peer` exists yet under `prosoc/scenarios/` (confirmed by directory listing) — but a reader comparing this field against the prose or the paper may expect the paper's stated relation to appear.
- **Recommended fix:** No action required now. When/if `leave_group` (and/or `accompany_peer`) is drafted as its own scenario, add it to `related_scenarios` alongside or instead of `crowd_navigation`, since it is the more central relationship per both the paper and this card's own Notes section.

### 2. Redundant duplicate field — suggestion
- **Section/field:** `agents.humans[0].count` vs `agents.humans[0].attributes.group_size`
- **Issue:** Both fields independently state the group size is 3 (`count: 3` and `attributes.group_size: 3`). Harmless today since both values agree, but a future edit to one without the other would silently desynchronize them. (Same pattern flagged and since resolved in the `leading` scenario's `initial_conditions.robot_task`/`intended_robot_task` duplication.)
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
| Related Scenarios | Leaving a Group | Partial — formal `related_scenarios` field now populated but lists `crowd_navigation` rather than Leaving a Group, since the latter is not yet an implemented scenario directory (see Finding 1) |
| Cited In | [50, 161] | Matches — formal `cited_in: ["50", "161"]` now present, matching the Status block's SOURCE line and Table 3 |

No mismatches found beyond the related_scenarios note above. Source fidelity: confirmed against Table 3.

## Completeness

`scripts/distill/scenarios --scenario join_a_group --dry-run --show-diffs` produced no diff and no schema errors — `scenario.yml` is in sync with the embedded YAML and validates against `schema.json`.

Walking the fields `template.md` marks "Required for AUDITED scenarios":

- **Scenario Card Summary block** — present and complete (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In). Related Scenarios / Cited In — previously flagged as the sole gap — are now filled in (`crowd_navigation`; `50, 161`).
- **Scenario Usage Guide — Success Metrics** — present (`SR`, `NoCollisions`), matches YAML.
- **Scenario Usage Guide — Quality Metrics** — present (`P2`, `P4`, `P5`), matches YAML and is a sensible subset of `relevant_principles` (`P1`, `P2`, `P4`, `P5`, `P8`).
- **Scenario Usage Guide — Ideal Outcome** — present, matches YAML `ideal_outcome`.
- **Scenario Usage Guide — Failure Modes** — present, four modes, matches YAML.
- **Scenario Usage Guide — Labeling Criteria** — present, three criteria, matches YAML.

No blank required fields remain. Prose (Scenario Overview, Social Navigation Context, Normative Expectations) is internally consistent with the YAML's `intended_robot_task`, `intended_human_behavior`, `agents`, `expected_behaviors`, and `ideal_outcome` — no contradictions or drift found. `relevant_principles` (5 entries, all P0–P9) and `quality_metrics` are within the recommended 3–5 range. `expected_behaviors` entries describe kinds of behavior ("approach along a peripheral or curved path," "slow down when nearing the group's formation boundary") rather than exact motions or numeric thresholds — no over-specification per P&G Guideline N6.
