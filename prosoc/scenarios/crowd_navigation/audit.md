---
scenario: crowd_navigation
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 0
audited: 2026-07-20
---

# Audit: Crowd Navigation

- **Scenario:** `prosoc/scenarios/crowd_navigation/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with one minor fix — no blocking issues, one should-fix completeness gap

## Findings

### 1. "Related Scenarios" and "Cited In" left blank in Scenario Card Summary — should-fix
- **Section/field:** Scenario Card Summary vs. `template.md`'s "Required for AUDITED scenarios" block
- **Issue:** The now-rendered `## Scenario Card Summary` section explicitly lists "Related Scenarios" and "Cited In" under its own "Remaining gaps" note as should-fill-in-now, and leaves them out of the bulleted summary entirely. Both are readily determinable: the STATUS block's SOURCE field already says "cited in various," the "Notes for Scenario Designers and Evaluators" section already names Robot Crowding, Parallel Traffic, and Perpendicular Traffic as related, and `../../../.claude/skills/_shared/pg_scenarios.md`'s Crowd Navigation entry lists "Related Scenarios: Robot Crowding" / "Cited In: Various" directly.
- **Recommended fix:** Add `- **Related Scenarios:** Robot Crowding (Figure 7 variant); see also Parallel Traffic, Perpendicular Traffic` and `- **Cited In:** Various` to the Scenario Card Summary bullet list, and drop the "Remaining gaps" note once filled. Optionally also add `related_scenarios`/`cited_in` arrays to the YAML block (schema supports both fields; currently neither is populated in `scenario.yml`).

## Source Fidelity

SOURCE cites P&G Paper Table 3, "cited in various." Compared against `../../../.claude/skills/_shared/pg_scenarios.md`'s "Crowd Navigation" entry (Crowd Scenarios section):

- Description ("A robot navigates through a crowd") — matches.
- Physical Environment: Generic — matches (`context.environment.type: generic`).
- Geometric Layout: Passable space — matches (`geometric_layout: passable space`).
- Scientific Purpose: Crowd navigation — matches (`scientific_purpose: crowd navigation`).
- Robot Task: Navigate thru — matches (`intended_robot_task: navigate through the crowd to a destination on the far side`).
- Human Behavior: Mill about — matches (`intended_human_behavior: mill about, moving independently...`).
- Ideal Outcome: No collision/obstruction — matches, with an added "steady progress" clause that is an elaboration rather than a contradiction.
- Related Scenarios: Robot Crowding — matches the reference source, but as noted in Finding 1 this is not yet surfaced in the card's own Scenario Card Summary bullet list.
- Cited In: Various — matches STATUS field, likewise not yet surfaced in the summary bullet list.

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" checklist:

- **Scenario Card Summary block** — present (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome all filled in from the embedded YAML). Previously missing entirely (prior audit, 2026-07-05); now rendered in, resolving that finding.
- **Related Scenarios / Cited In** (sub-fields of the summary block) — should-fill-in-now. Explicitly flagged blank by the card's own "Remaining gaps" note. See Finding 1.
- **Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)** — present as prose, mirroring the YAML `scenario_usage_guide` block. Previously missing entirely (prior audit, 2026-07-05); now rendered in, resolving that finding.
- **`expected_behaviors.should_not` vs. Normative Expectations prose** — now fully aligned: the YAML `should_not` list includes "proceed at a fixed pace or clearance regardless of local crowd density," which was flagged as a gap (suggestion) in the prior audit and has since been added. No remaining prose/YAML drift found in this area.

## Change vs. prior audit (2026-07-05)

The prior audit (should_fix: 2, suggestion: 1, verdict ready_with_fixes) flagged: (1) missing Scenario Card Summary section, (2) missing Scenario Usage Guide prose subsections, and (3) a should_not gap for "fixed pace regardless of density." All three are resolved in this pass — the sections are now rendered in and the should_not entry was added. One new, narrower should-fix remains: Related Scenarios/Cited In are still blank within the newly rendered summary block.
