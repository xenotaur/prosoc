---
scenario: pedestrian_overtaking
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-22
---

# Audit: Pedestrian Overtaking a Robot from Behind

- **Scenario:** `prosoc/scenarios/pedestrian_overtaking/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready — no blocking or should-fix issues found; one minor suggestion for human consideration.

## Findings

### 1. Physical Environment more specific than source table — suggestion
- **Section/field:** Scenario Card Summary `Physical Environment` / YAML `context.environment.type` vs. P&G Table 3
- **Issue:** `.claude/skills/_shared/pg_scenarios.md`'s Pedestrian Overtaking row lists Physical Env as "Generic," while this scenario commits to `indoor` (corridor or sidewalk-like passage). This isn't a contradiction — "Generic" in the source table means unspecified, and `indoor` is a reasonable concretization — but it is an editorial choice beyond the source, not something drawn directly from Table 3.
- **Recommended fix:** No action required. Optionally note in `evaluation_notes` that the indoor setting is an authorial concretization of the source's generic physical environment, if precise source fidelity matters for downstream use.

## Source Fidelity

The prose explicitly states this scenario "corresponds to pedestrian-overtaking cases discussed in the *Principles and Guidelines for Social Robot Navigation* paper," and `cited_in: ["26"]` points to the same source, so fidelity is checked against `.claude/skills/_shared/pg_scenarios.md`'s "Pedestrian Overtaking" entry (P&G Table 3) even though the Status block's `SOURCE:` line itself still reads "Prompt to ChatGPT 5.2" (informal, not directly checkable, but superseded here by the prose's explicit paper reference):

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

No fidelity mismatches requiring a fix.

## Completeness

All fields marked "Required for AUDITED scenarios" in `template.md` are filled:

- **Scenario Card Summary:** Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, and Cited In are all present.
- **Scenario Usage Guide:** Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all present and substantive.

No blank required fields remain.

## Schema / Tooling Check

`scripts/distill/scenarios --scenario pedestrian_overtaking --dry-run --show-diffs` produced no diff and exited 0 — `scenario.yml` is in sync with the embedded YAML in `scenario.md` and validates against `schema.json`. `expected_behaviors` uses only `must`/`should`/`should_not`. `relevant_principles` (P0, P1, P2, P3, P4) and `scenario_usage_guide.quality_metrics` (P2, P3, P4) contain only valid P0–P9 identifiers. Five principles (P0–P4) is one over the nominal 3–5 range's midpoint but is covered by the explicit prose-discussion exception in `.claude/skills/_shared/principles.md` (the Scenario Overview explicitly discusses P0 — "while continuing to make progress toward its goal"), so it is not flagged.

## Change Since Last Audit (2026-07-21)

No changes to `scenario.md` or `scenario.yml` since the 2026-07-21 audit. This re-audit reproduces the same verdict, finding, and counts (ready; 0 blocking; 0 should-fix; 1 suggestion) — no substantive change.
