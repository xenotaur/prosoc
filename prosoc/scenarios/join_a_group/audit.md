---
scenario: join_a_group
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-07-20
---

# Audit: Join a Group

- **Scenario:** `prosoc/scenarios/join_a_group/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Related Scenarios / Cited In omitted from Card Summary and YAML — should-fix
- **Section/field:** Scenario Card Summary (`Related Scenarios`, `Cited In`) and the machine-readable `related_scenarios` / `cited_in` YAML fields (present in `schema.json`, absent from `scenario.yml`)
- **Issue:** The Card Summary's own "Remaining gaps" note flags these two fields as `should-fill-in-now`, and the content needed to fill them is already sitting elsewhere in the card: the Status block's SOURCE line cites `[50, 161]`, and the "Notes for Scenario Designers and Evaluators" section already names *Leave Group* and *Accompany Peer* as related scenarios. Neither value has been transcribed into the Card Summary bullets or the YAML block, so the machine-readable spec is missing information the prose already establishes.
- **Recommended fix:** Add `- **Related Scenarios:** Leave Group, Accompany Peer` and `- **Cited In:** [50, 161]` to the Card Summary block, and add corresponding `related_scenarios:` / `cited_in:` keys to the embedded YAML (and re-run the distiller to sync `scenario.yml`).

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
| Related Scenarios | Leaving a Group | Consistent — noted in Notes section and evaluation_notes, though not yet in a formal `related_scenarios` field (see Finding 1) |
| Cited In | [50, 161] | Consistent — present in Status block, not yet in a formal `cited_in` field (see Finding 1) |

No mismatches found. Source fidelity: confirmed against Table 3.

## Completeness

`scripts/distill/scenarios --scenario join_a_group --dry-run --show-diffs` produced no diff and no schema errors — `scenario.yml` is in sync with the embedded YAML and validates against `schema.json`.

Walking the fields `template.md` marks "Required for AUDITED scenarios":

- **Scenario Card Summary block** — present (`## Scenario Card Summary`, populated with Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome). Related Scenarios / Cited In are the only gaps — should-fill-in-now (Finding 1).
- **Scenario Usage Guide — Success Metrics** — present (`SR`, `NoCollisions`), matches YAML.
- **Scenario Usage Guide — Quality Metrics** — present (`P2`, `P4`, `P5`), matches YAML and is a sensible subset of `relevant_principles` (`P1`, `P2`, `P4`, `P5`, `P8`).
- **Scenario Usage Guide — Ideal Outcome** — present, matches YAML `ideal_outcome`.
- **Scenario Usage Guide — Failure Modes** — present, four modes, matches YAML.
- **Scenario Usage Guide — Labeling Criteria** — present, three criteria, matches YAML.

No blank required fields remain. Prose (Scenario Overview, Social Navigation Context, Normative Expectations) is internally consistent with the YAML's `intended_robot_task`, `intended_human_behavior`, `agents`, `expected_behaviors`, and `ideal_outcome` — no contradictions or drift found. `relevant_principles` (5 entries, all P0–P9) and `quality_metrics` are within the recommended 3–5 range. `expected_behaviors` entries describe kinds of behavior ("approach along a peripheral or curved path," "slow down when nearing the group's formation boundary") rather than exact motions or numeric thresholds — no over-specification per P&G Guideline N6.

### 2. Redundant duplicate field — suggestion
- **Section/field:** `agents.humans[0].count` vs `agents.humans[0].attributes.group_size`
- **Issue:** Both fields independently state the group size is 3 (`count: 3` and `attributes.group_size: 3`). This mirrors the duplication pattern recently cleaned up in the `leading` scenario (`initial_conditions.robot_task` restating `intended_robot_task`) — harmless today since both values agree, but a future edit to one without the other would silently desynchronize them.
- **Recommended fix:** Consider dropping `attributes.group_size` and relying solely on `count`, or explicitly document why both are kept (e.g., if `group_size` is meant to describe the F-formation size distinctly from the modeled agent count).
