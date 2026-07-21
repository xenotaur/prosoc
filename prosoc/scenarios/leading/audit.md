---
scenario: leading
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 0
audited: 2026-07-20
---

# Audit: Leading

- **Scenario:** `prosoc/scenarios/leading/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Related Scenarios / Cited In omitted from Card Summary and YAML — should-fix
- **Section/field:** Scenario Card Summary (`Related Scenarios`, `Cited In`) and the machine-readable `related_scenarios` / `cited_in` YAML fields (present in `schema.json`, absent from `scenario.yml`)
- **Issue:** The Card Summary's own "Remaining gaps" note flags these two fields as `should-fill-in-now`, and the content is already present elsewhere in the card: the Status block's SOURCE line cites `[50]`, and the "Notes for Scenario Designers and Evaluators" section already names *Following* (role-reversed counterpart) and *Tour Guide* (extended variant) as related scenarios. Neither value has been transcribed into the Card Summary bullets or the YAML block.
- **Recommended fix:** Add `- **Related Scenarios:** Following, Tour Guide` and `- **Cited In:** [50]` to the Card Summary block, and add corresponding `related_scenarios:` / `cited_in:` keys to the embedded YAML (re-run the distiller afterward to sync `scenario.yml`).

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Leading" (cited in [50]), which matches the entry in `.claude/skills/_shared/pg_scenarios.md`:

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
| Related Scenarios | Tour Guide | Consistent — noted in Notes section and evaluation_notes, not yet in a formal `related_scenarios` field (see Finding 1) |
| Cited In | [50] | Consistent — present in Status block, not yet in a formal `cited_in` field (see Finding 1) |

No mismatches found. Source fidelity: confirmed against Table 3.

## Completeness

`scripts/distill/scenarios --scenario leading --dry-run --show-diffs` produced no diff and no schema errors — `scenario.yml` is in sync with the embedded YAML and validates against `schema.json`.

Walking the fields `template.md` marks "Required for AUDITED scenarios":

- **Scenario Card Summary block** — present (`## Scenario Card Summary`, populated with Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome). Related Scenarios / Cited In are the only gaps — should-fill-in-now (Finding 1).
- **Scenario Usage Guide — Success Metrics** — present (`SR`, `NoCollisions`, `TTG`), matches YAML.
- **Scenario Usage Guide — Quality Metrics** — present (`P3`, `P6`), matches YAML and is a sensible subset of `relevant_principles` (`P1`, `P3`, `P6`, `P8`).
- **Scenario Usage Guide — Ideal Outcome** — present, matches YAML `ideal_outcome`.
- **Scenario Usage Guide — Failure Modes** — present, four modes, matches YAML.
- **Scenario Usage Guide — Labeling Criteria** — present, three criteria, matches YAML.

No blank required fields remain. Prose (Scenario Overview, Social Navigation Context, Normative Expectations) is internally consistent with the YAML's `intended_robot_task`, `intended_human_behavior`, `agents` (leader/follower roles, count 1), `expected_behaviors`, and `ideal_outcome` — no contradictions or drift found. `relevant_principles` (4 entries, all P0–P9) and `quality_metrics` are within the recommended 3–5 range. `expected_behaviors` entries describe kinds of behavior ("choose a pace appropriate to the human's demonstrated walking speed," "signal upcoming turns with enough lead time") rather than exact motions or numeric thresholds — no over-specification per P&G Guideline N6.

`initial_conditions` now contains only `robot_position` and `human_position` (situational starting conditions), with no `robot_task` key restating `intended_robot_task` — the duplicate field noted in the prior audit has been removed and is no longer a finding.
