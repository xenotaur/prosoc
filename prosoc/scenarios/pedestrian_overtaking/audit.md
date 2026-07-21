---
scenario: pedestrian_overtaking_01
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-20
---

# Audit: Pedestrian Overtaking a Robot from Behind

- **Scenario:** `prosoc/scenarios/pedestrian_overtaking/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready — no blocking or should-fix issues found; two minor suggestions for human consideration.

## Findings

### 1. Physical Environment more specific than source table — suggestion
- **Section/field:** Scenario Card Summary `Physical Environment` / YAML `context.environment.type` vs. P&G Table 3
- **Issue:** `../_shared/pg_scenarios.md`'s Pedestrian Overtaking row lists Physical Env as "Generic," while this scenario commits to `indoor` (corridor or sidewalk-like passage). This isn't a contradiction — "Generic" in the source table means unspecified, and `indoor` is a reasonable concretization — but it is an editorial choice beyond the source, not something drawn directly from Table 3.
- **Recommended fix:** No action required. Optionally note in `evaluation_notes` that the indoor setting is an authorial concretization of the source's generic physical environment, if precise source fidelity matters for downstream use.

### 2. P0 (Goal Achievement) dropped despite prose hinting at goal/social tension — suggestion
- **Section/field:** `relevant_principles` vs. Scenario Overview prose
- **Issue:** The Scenario Overview states the robot must maintain prosocial norms "while continuing to make progress toward its goal," which echoes the P0 selection criterion in `../_shared/principles.md` ("include when task completion/efficiency is in explicit tension with the social principles"). `relevant_principles` currently lists P1–P4 only (4 principles, within the recommended 3–5 range), with P0 and P9 trimmed this session (previously 6: P0, P1–P4, P9).
- **Recommended fix:** No action required — 4 principles is well within guidance, and the trim to P1–P4 (Safety, Comfort, Legibility, Politeness) is defensible since the goal/progress tension here is mild (the robot need only hold speed and heading, not actively trade off goal progress against yielding). Flagging only so a human reviewer can confirm the trim was a deliberate scoping decision rather than an oversight.

## Source Fidelity

The prose explicitly states this scenario "corresponds to pedestrian-overtaking cases discussed in the *Principles and Guidelines for Social Robot Navigation* paper," and `cited_in: ["26"]` points to the same source, so fidelity is checked against `../_shared/pg_scenarios.md`'s "Pedestrian Overtaking" entry (P&G Table 3) even though the Status block's `SOURCE:` line itself still reads "Prompt to ChatGPT 5.2" (informal, not directly checkable, but superseded here by the prose's explicit paper reference):

| Field | P&G Table 3 | This scenario | Match? |
|---|---|---|---|
| Description | Pedestrian overtakes moving robot | Human pedestrian approaches and overtakes a slower-moving robot from behind | Yes |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Yes |
| Geometric Layout | Passable space | passable space | Yes |
| Robot Task | Navigate A to B | navigate from A to B | Yes |
| Human Behavior | Navigate A to B (faster) | navigate from A to B, faster than the robot | Yes |
| Ideal Outcome | Human passes robot | human passes the robot safely, comfortably, and without disruption | Yes (elaborated, not contradicted) |
| Physical Env | Generic | indoor | Concretized, not contradicted (see Finding 1) |
| Related Scenarios | Down Path | robot_overtaking | Not a mismatch — "Down Path" is the P&G paper's own informal related-scenario label and has no corresponding entry anywhere in this project's implemented corpus (checked: no scenario named/aliased "down_path" exists, and no other row in `pg_scenarios.md` maps to it either). Pointing instead to the implemented `robot_overtaking` scenario is a reasonable, more useful editorial substitution. |
| Cited In | [26] | 26 | Yes |

No fidelity mismatches requiring a fix. All previously-missing fields this table depends on (`scientific_purpose`, `geometric_layout`, `intended_robot_task`, `intended_human_behavior`, `ideal_outcome`) are now present in the YAML, resolving what was the prior audit's blocking finding.

## Completeness

All fields marked "Required for AUDITED scenarios" in `template.md` are now filled:

- **Scenario Card Summary:** Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, and Cited In are all present.
- **Scenario Usage Guide:** Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all present and substantive (this entire section was authored from scratch this session — previously entirely absent — and is now complete).

No blank required fields remain.

## Schema / Tooling Check

`scripts/distill/scenarios --scenario pedestrian_overtaking --dry-run --show-diffs` produced no diff and exited 0 — `scenario.yml` is in sync with the embedded YAML in `scenario.md` and validates against `schema.json`. `expected_behaviors` uses only `must`/`should`/`should_not`. `relevant_principles` (P1, P2, P3, P4) and `scenario_usage_guide.quality_metrics` (P2, P3, P4) contain only valid P0–P9 identifiers, count 4 (within the 3–5 guidance, down from 6 previously). No over-specified (exact-motion or numeric-threshold) entries found in `expected_behaviors`. The `STATE` field reads `DRAFTED` (previously the invalid value `DRAFT`), a valid enumerated lifecycle state per `workflow.md`; this audit did not modify it.
