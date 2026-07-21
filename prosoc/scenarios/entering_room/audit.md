---
scenario: entering_room
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-07-20
---

# Audit: Entering Room

- **Scenario:** `prosoc/scenarios/entering_room/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with one minor fix — no blocking issues, one should-fix completeness gap, one optional suggestion

## Findings

### 1. "Related Scenarios" and "Cited In" left blank in Scenario Card Summary — should-fix
- **Section/field:** Scenario Card Summary vs. `template.md`'s "Required for AUDITED scenarios" block
- **Issue:** The now-rendered `## Scenario Card Summary` section explicitly lists "Related Scenarios" and "Cited In" under its own "Remaining gaps" note as should-fill-in-now, and leaves them out of the bulleted summary entirely. Both are readily determinable: the STATUS block's SOURCE field already says "Robots@Games (R@G)," the "Notes for Scenario Designers and Evaluators" section already names Entering Elevator, Exiting Room, and Narrow Doorway as related, and `../../../.claude/skills/_shared/pg_scenarios.md`'s Entering Room entry lists "Related Scenarios: Entering Elevator (R@G)" / "Cited In: R@G" directly.
- **Recommended fix:** Add `- **Related Scenarios:** Entering Elevator (R@G); see also Exiting Room, Narrow Doorway` and `- **Cited In:** R@G` to the Scenario Card Summary bullet list, and drop the "Remaining gaps" note once filled. Optionally also add `related_scenarios`/`cited_in` arrays to the YAML block (schema supports both fields; currently neither is populated in `scenario.yml`).

### 2. P3 (Legibility) not included in relevant_principles — suggestion
- **Section/field:** `relevant_principles` vs. `../../../.claude/skills/_shared/principles.md` selection guidance
- **Issue:** The scenario's normative core is about the robot recognizing and communicating deference at a threshold ("proceed to enter promptly once the threshold is clear," avoiding "waiting so far back... entry is delayed"). P3 (Legibility — behave so robot goals can be understood by others) arguably applies here, since a human benefits from being able to tell that the robot is intentionally waiting rather than malfunctioning or blocked. Current selection (P1, P4, P5, P6) is reasonable and within the 3-5 guidance, so this is not a defect, just worth a human's consideration. Unchanged since the prior audit.
- **Recommended fix:** Optionally add P3 if the editor agrees legibility of the robot's "waiting" intent is a distinct concern from politeness/social-norm compliance; otherwise no change needed.

## Source Fidelity

SOURCE cites P&G Paper Table 3 and Robots@Games (R@G). Compared against `../../../.claude/skills/_shared/pg_scenarios.md`'s "Entering Room" entry (Doorway Scenarios section):

- Description ("Robot enters a room occupied by a human") — matches.
- Physical Environment: Indoor — matches (`context.environment.type: indoor`).
- Geometric Layout: Room and door — matches (`geometric_layout: room and door`).
- Scientific Purpose: Pedestrian interaction — matches (`scientific_purpose: pedestrian interaction`).
- Robot Task: Navigate out to in — matches (`intended_robot_task: navigate from outside to inside the room`).
- Human Behavior: Navigate in to out — matches (`intended_human_behavior: navigate from inside to outside the room`).
- Ideal Outcome: Robot lets human exit — matches almost verbatim (`ideal_outcome: robot lets the human exit fully, then enters the room without obstruction`).
- Related Scenarios: Entering Elevator (R@G) — matches the reference source, but as noted in Finding 1 this is not yet surfaced in the card's own Scenario Card Summary bullet list.
- Cited In: R@G — matches STATUS field, likewise not yet surfaced in the summary bullet list.

No mismatches found. Source fidelity: confirmed against P&G Table 3 / R@G.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" checklist:

- **Scenario Card Summary block** — present (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome all filled in from the embedded YAML). Previously missing entirely (prior audit, 2026-07-05); now rendered in, resolving that finding.
- **Related Scenarios / Cited In** (sub-fields of the summary block) — should-fill-in-now. Explicitly flagged blank by the card's own "Remaining gaps" note. See Finding 1.
- **Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)** — present as prose, mirroring the YAML `scenario_usage_guide` block. Previously missing entirely (prior audit, 2026-07-05); now rendered in, resolving that finding.

## Change vs. prior audit (2026-07-05)

The prior audit (should_fix: 2, suggestion: 1, verdict ready_with_fixes) flagged: (1) missing Scenario Card Summary section, (2) missing Scenario Usage Guide prose subsections, and (3) a suggestion to consider adding P3 (Legibility). Findings 1 and 2 are resolved in this pass — both sections are now rendered in. The P3 suggestion is unchanged (still open, still non-blocking). One new, narrower should-fix remains: Related Scenarios/Cited In are still blank within the newly rendered summary block.
