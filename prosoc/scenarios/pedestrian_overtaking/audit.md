# Audit: Pedestrian Overtaking

- **Scenario:** `prosoc/scenarios/pedestrian_overtaking/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready — 2 blocking issues

## Findings

### 1. Invalid principle identifiers `P0` and `P9` — blocking
- **Section/field:** `relevant_principles` (scenario.md embedded YAML and scenario.yml)
- **Issue:** The list is `[P0, P9, P1, P2, P3, P4]` (ordered `P0, P1, P2, P3, P4, P9` in the file). `P0` ("Goal Achievement") and `P9` ("Prosocial Behavior") are not among the eight canonical charter principles (P1–Safety through P8–Contextual Appropriateness) defined in `../../../.claude/skills/_shared/principles.md`. Both values happen to satisfy the schema's `^P[0-9]+$` regex, so `schema.json` validation and the distiller's dry-run do not catch this — it is a charter-compliance issue, not a schema error.
- **Recommended fix:** Remove `P0` and `P9`. If the drafter intended to flag a concept not captured by P1–P8 (e.g., "goal achievement" or "general prosocial behavior"), move that idea into `evaluation_notes` as guidance rather than inventing new principle IDs, per `../../../.claude/skills/_shared/principles.md`'s explicit instruction. After removing the two invalid entries, the remaining set (P1 Safety, P2 Comfort, P3 Legibility, P4 Politeness) is a reasonable 4-principle selection for this scenario and does not need further reduction.

### 2. Missing Scenario Card Summary and Scenario Usage Guide sections — blocking
- **Section/field:** `scenario.md` structure; YAML fields `scientific_purpose`, `geometric_layout`, `ideal_outcome`, `intended_robot_task`, `intended_human_behavior`, and the entire `scenario_usage_guide` block (`success_metrics`, `quality_metrics`, `failure_modes`, `labeling_criteria`)
- **Issue:** `template.md` marks the "Scenario Card Summary" section and the "Scenario Usage Guide" section (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria) as **Required for AUDITED scenarios**. Neither section exists anywhere in `scenario.md` — the document jumps from `## STATUS` directly to `## Overview`, and after the YAML block goes straight to `## Notes for Scenario Designers and Evaluators`. Correspondingly, the YAML has no `scientific_purpose`, `geometric_layout`, `ideal_outcome`, `intended_robot_task`, `intended_human_behavior`, or `scenario_usage_guide` keys at all (confirmed: `scenario.yml` top-level keys are only `id, name, summary, context, agents, initial_conditions, expected_behaviors, relevant_principles, evaluation_notes`). This scenario cannot reach AUDITED status until these are added.
- **Recommended fix:** Add a "Scenario Card Summary" section drawn from the P&G Table 3 entry for Pedestrian Overtaking (see Source Fidelity below), and a "Scenario Usage Guide" section with Success Metrics (e.g., `SR`, `NoCollisions`, `PSC`), Quality Metrics (a P1–P8 subset), Failure Modes, and Labeling Criteria. Add the corresponding `scientific_purpose: pedestrian interaction`, `geometric_layout: passable space` (or corridor/sidewalk), `ideal_outcome`, `intended_robot_task`, and `intended_human_behavior` fields to the YAML — this scenario predates the more complete field set used in newer cards (e.g. `perpendicular_traffic`) and should be brought up to that standard.

### 3. STATUS block uses outdated template format — should-fix
- **Section/field:** `## STATUS: DRAFT 2026-01-02` header
- **Issue:** `template.md` and `workflow.md` specify the Status section should use a `**STATE:** DRAFTED` field within a `## Status` heading (see `perpendicular_traffic/scenario.md` for the current convention). This scenario instead folds the state and date into the heading text (`## STATUS: DRAFT 2026-01-02`) with no explicit `STATE:` line, and the state value `DRAFT` doesn't match the enumerated lifecycle states in `workflow.md` (`DRAFTED`, `EDITED`, `AUDITED`, `VALIDATED`, `DEPRECATED`/`RETIRED`) — closest is `DRAFTED`, but the file's `EDITED:` line is already filled in, so the actual current stage is ambiguous from the STATE value alone.
- **Recommended fix:** Not a change this audit should make (STATUS block is off-limits per this skill's rules), but flagging for the human editor to normalize to the current Status template when next editing this file: `- **STATE:** EDITED` (since an EDITED line with a named editor and date is already present), plus the existing SOURCE/DRAFTED/EDITED lines.

### 4. Title heading missing a space — suggestion
- **Section/field:** `scenario.md` line 1, `# Scenario:Pedestrian Overtaking`
- **Issue:** Missing space after the colon (compare `perpendicular_traffic`'s `# Scenario: Perpendicular Traffic`). Cosmetic only.
- **Recommended fix:** Change to `# Scenario: Pedestrian Overtaking`.

## Source Fidelity

SOURCE is listed as "Prompt to ChatGPT 5.2" (informal, no retrievable content of the prompt itself). However, the prose explicitly states "This scenario corresponds to pedestrian-overtaking cases discussed in the *Principles and Guidelines for Social Robot Navigation* paper," which points to a checkable source: `../../../.claude/skills/_shared/pg_scenarios.md`'s "Pedestrian Overtaking" entry (P&G Table 3, cited in [26]).

Comparison against that entry:
- **Description** ("Pedestrian overtakes moving robot"): matches — scenario has the human pedestrian overtaking a slower-moving robot.
- **Physical Env / Geometric Layout** (Generic / Passable space): the scenario's `context.environment.setting` ("corridor or sidewalk-like passage") is a reasonable specialization of "Generic / Passable space," not a contradiction.
- **Scientific Purpose** (Pedestrian interaction): consistent with the prose, though the field is absent from the YAML (see Finding 2).
- **Robot Task** (Navigate A to B) / **Human Behavior** (Navigate A to B, faster): consistent with `initial_conditions.relative_speed: pedestrian_faster` and the prose, though `intended_robot_task`/`intended_human_behavior` fields are absent from the YAML (see Finding 2).
- **Ideal Outcome** (Human passes robot): consistent with the prose's description of successful passing, though no `ideal_outcome` field exists in the YAML (see Finding 2).
- **Related Scenarios** (Down Path): not mentioned in this card; reasonably blank at this stage (see Completeness).

No contradictions found. The card is faithful to the Table 3 entry in substance, but the SOURCE field itself should probably be updated to cite the P&G paper directly given the prose's explicit reference to it, rather than only "Prompt to ChatGPT 5.2." That's a should-fix-adjacent observation but is bundled into Finding 2's broader recommendation rather than listed separately, since it's about the SOURCE line rather than content correctness.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary block** — entirely absent (see Finding 2). Should-fill-in-now: all sub-fields (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome) are readily inferable from the existing Overview/Social Navigation Context/Normative Expectations prose and the P&G Table 3 entry above.
- **Success Metrics** — absent. Should-fill-in-now: plausible candidates (`SR`, `NoCollisions`, `PSC`) are implied by the Normative Expectations prose (safe passing, no forced hesitation/reroute).
- **Quality Metrics** — absent. Should-fill-in-now: a P1–P8 subset (e.g., P2 Comfort, P3 Legibility) mirroring `relevant_principles` once Finding 1 is corrected.
- **Ideal Outcome** — absent as a discrete field, though implied by prose ("safe and comfortable passing without impeding the pedestrian"). Should-fill-in-now.
- **Failure Modes** — not present as a `scenario_usage_guide.failure_modes` list, though `evaluation_notes` already states failure modes in prose ("blocking behavior, sudden motion changes, or trajectories that require the pedestrian to hesitate or reroute"). Should-fill-in-now: this content already exists and just needs to move into the structured field.
- **Labeling Criteria** — absent. Should-fill-in-now: criteria are implicit in `initial_conditions` (robot ahead, pedestrian faster, clear visibility) and could be directly adapted into a labeling-criteria list.
- **Related Scenarios / Cited In** — absent. Reasonably blank: while `../../../.claude/skills/_shared/pg_scenarios.md` lists "Down Path" as a related scenario and `[26]` as a citation, whether to carry these into the card is a minor editorial choice, not a required inference from existing prose in this card.
