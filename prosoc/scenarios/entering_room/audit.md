---
scenario: entering_room
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-22
---

# Audit: Entering Room

- **Scenario:** `prosoc/scenarios/entering_room/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready — no blocking or should-fix issues found; two minor suggestions

## Findings

### 1. P3 (Legibility) not included in relevant_principles — suggestion
- **Section/field:** `relevant_principles` vs. `.claude/skills/_shared/principles.md` selection guidance
- **Issue:** The scenario's normative core is about the robot recognizing and communicating deference at a threshold ("proceed to enter promptly once the threshold is clear," avoiding "waiting so far back... entry is delayed"). P3 (Legibility — behave so robot goals can be understood by others) arguably applies here, since a human benefits from being able to tell the robot is intentionally waiting rather than malfunctioning or blocked. The current selection (P1, P4, P5, P6) is reasonable and within the 3-5 guidance, so this is not a defect, just worth a human's consideration.
- **Recommended fix:** Optionally add P3 if the editor agrees legibility of the robot's "waiting" intent is a distinct concern from politeness/social-norm compliance; otherwise no change needed.

### 2. STATUS block's EDITED date does not reflect the latest edit — suggestion
- **Section/field:** Status block (`EDITED: render_sections.py, 2026-07-20`)
- **Issue:** `git log` shows the most recent edit to `scenario.md`/`scenario.yml` is commit `8b6ee81` ("Document and self-document the related_scenarios/Table 3 divergence convention", 2026-07-22), which added a "Related Scenarios note" paragraph to `evaluation_notes`. The STATUS block still shows only the prior `render_sections.py, 2026-07-20` entry and has not been updated to record this most recent pass.
- **Recommended fix:** Add an additional `EDITED` line (or update the existing one) noting the `evaluation_notes` self-documentation pass and its date/author, consistent with how the STATUS block tracks provenance elsewhere in the corpus.

## Source Fidelity

SOURCE cites P&G Paper Table 3 and "Robotics at Google (R@G), internal scenario reference." Compared against `../../.claude/skills/_shared/pg_scenarios.md`'s "Entering Room" entry (Doorway Scenarios section):

- **Description** ("Robot enters a room occupied by a human") — matches.
- **Physical Environment** (Indoor) — matches (`context.environment.type: indoor`).
- **Geometric Layout** (Room and door) — matches (`geometric_layout: room and door`).
- **Scientific Purpose** (Pedestrian interaction) — matches (`scientific_purpose: pedestrian interaction`).
- **Robot Task** (Navigate out to in) — matches (`intended_robot_task: navigate from outside to inside the room`).
- **Human Behavior** (Navigate in to out) — matches (`intended_human_behavior: navigate from inside to outside the room`).
- **Ideal Outcome** (Robot lets human exit) — matches almost verbatim (`ideal_outcome: robot lets the human exit fully, then enters the room without obstruction`).
- **Cited In**: the reference table reads "R@G — Robotics at Google, an internal scenario reference (not a public citation index)." The scenario's `cited_in` field reads "Robotics at Google (R@G), internal scenario reference" — consistent.
- **Related Scenarios**: Table 3 lists "Entering Elevator (R@G)," which is a Figure 7 scenario with no implemented directory under `prosoc/scenarios/` (confirmed: no `entering_elevator` directory exists). The card's `related_scenarios` field instead references `exiting_room` and `narrow_doorway`, both implemented sibling scenarios the card's own "Notes for Scenario Designers and Evaluators" section already discusses, and `evaluation_notes` now explicitly documents this substitution as expected per the `related_scenarios` convention in `audit_checklist.md`. Not a mismatch.

No mismatches found. Source fidelity: confirmed against P&G Table 3 / R@G.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" checklist:

- **Scenario Card Summary block** — fully present: Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, and Cited In are all filled in.
- **Scenario Usage Guide** (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria) — present as prose, mirroring the YAML `scenario_usage_guide` block.
- **`relevant_principles`** (P1, P4, P5, P6) — 4 entries, within the 3–5 guidance, all valid P0–P9. See Finding 1 for the optional P3 consideration.
- **`expected_behaviors`** — qualitative kind-of-behavior descriptions throughout (e.g. "hold position outside the doorway," "crowd the doorway"); no numeric-threshold or exact-motion over-specification found (P&G Guideline N6 satisfied).
- Prose vs. YAML cross-check (Scenario Overview / Social Navigation Context / Normative Expectations against `intended_robot_task`, `intended_human_behavior`, `agents`, `expected_behaviors`, `ideal_outcome`) found no contradictions or drift — both describe the same asymmetric enter/exit threshold with a single human occupant and matching must/should/should_not lists.
- Single-scenario dry-run distill (`scripts/distill/scenarios --scenario entering_room --dry-run --show-diffs`) reported no diff and no schema errors — `scenario.yml` is in sync with `scenario.md`.

No blank required fields.
