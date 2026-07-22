---
scenario: entering_room
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-21
---

# Audit: Entering Room

- **Scenario:** `prosoc/scenarios/entering_room/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready — no blocking or should-fix issues found; two minor suggestions

## Findings

### 1. P3 (Legibility) not included in relevant_principles — suggestion
- **Section/field:** `relevant_principles` vs. `.claude/skills/_shared/principles.md` selection guidance
- **Issue:** The scenario's normative core is about the robot recognizing and communicating deference at a threshold ("proceed to enter promptly once the threshold is clear," avoiding "waiting so far back... entry is delayed"). P3 (Legibility — behave so robot goals can be understood by others) arguably applies here, since a human benefits from being able to tell that the robot is intentionally waiting rather than malfunctioning or blocked. Current selection (P1, P4, P5, P6) is reasonable and within the 3-5 guidance, so this is not a defect, just worth a human's consideration. Unchanged since the prior two audits.
- **Recommended fix:** Optionally add P3 if the editor agrees legibility of the robot's "waiting" intent is a distinct concern from politeness/social-norm compliance; otherwise no change needed.

### 2. STATUS block's EDITED date does not reflect the latest edit — suggestion
- **Section/field:** Status block (`EDITED: render_sections.py, 2026-07-20`)
- **Issue:** `git log` shows the most recent edit to `scenario.md`/`scenario.yml` is commit `93d55c3` ("Resolve the two deferred follow-ups from PR #27"), which backfilled `related_scenarios`/`cited_in` and corrected the R@G citation text from "Robots@Games (R@G)" to "Robotics at Google (R@G), internal scenario reference." The STATUS block still shows only the prior `render_sections.py, 2026-07-20` entry and does not record this most recent pass.
- **Recommended fix:** Add an additional `EDITED` line (or update the existing one) noting the `related_scenarios`/`cited_in` backfill and R@G correction, with date/author, consistent with how the STATUS block tracks provenance elsewhere in the corpus.

## Source Fidelity

SOURCE cites P&G Paper Table 3 and "Robotics at Google (R@G), internal scenario reference." Compared against `.claude/skills/_shared/pg_scenarios.md`'s "Entering Room" entry (Doorway Scenarios section):

- Description ("Robot enters a room occupied by a human") — matches.
- Physical Environment: Indoor — matches (`context.environment.type: indoor`).
- Geometric Layout: Room and door — matches (`geometric_layout: room and door`).
- Scientific Purpose: Pedestrian interaction — matches (`scientific_purpose: pedestrian interaction`).
- Robot Task: Navigate out to in — matches (`intended_robot_task: navigate from outside to inside the room`).
- Human Behavior: Navigate in to out — matches (`intended_human_behavior: navigate from inside to outside the room`).
- Ideal Outcome: Robot lets human exit — matches almost verbatim (`ideal_outcome: robot lets the human exit fully, then enters the room without obstruction`).
- Cited In: the reference table now reads "R@G — Robotics at Google, an internal scenario reference (not a public citation index)." The scenario's `cited_in` field reads "Robotics at Google (R@G), internal scenario reference" — consistent with the corrected text, confirming the citation-error fix (previously "Robots@Games (R@G)") landed correctly in both `scenario.md`/`scenario.yml` and the shared reference file.
- Related Scenarios: the reference table lists "Entering Elevator (R@G)," but Entering Elevator is a Figure 7 scenario with no implemented directory in this repo (confirmed: no `entering_elevator` directory exists under `prosoc/scenarios/`). The card's own `related_scenarios` field instead links to `exiting_room` and `narrow_doorway`, both implemented sibling scenarios discussed in the "Notes for Scenario Designers and Evaluators" section, consistent with `template.md`'s definition of `related_scenarios` as pointing to actual corpus directories. This is not a mismatch — the prose still names Entering Elevator as a conceptual relative in `evaluation_notes` and the Notes section.

No mismatches found. Source fidelity: confirmed against P&G Table 3 / R@G, including the corrected citation text.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" checklist:

- **Scenario Card Summary block** — fully present, including `Related Scenarios: exiting_room, narrow_doorway` and `Cited In: Robotics at Google (R@G), internal scenario reference`, resolving the should-fix from the prior audit (2026-07-20).
- **Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)** — present as prose, mirroring the YAML `scenario_usage_guide` block.
- **`relevant_principles`** (P1, P4, P5, P6) — 4 entries, within the 3-5 guidance, all valid P0-P9. See Finding 1 for the optional P3 consideration.
- **`expected_behaviors`** — qualitative kind-of-behavior descriptions throughout; no numeric-threshold or exact-motion over-specification found.
- Single-scenario dry-run distill (`scripts/distill/scenarios --scenario entering_room --dry-run --show-diffs`) reported no diff and no schema errors — `scenario.yml` is in sync with `scenario.md`.

No blank fields remain from the prior audit's completeness pass.

## Change vs. prior audit (2026-07-20)

The prior audit (`verdict: ready_with_fixes`, `should_fix: 1`, `suggestion: 1`) flagged one should-fix (`Related Scenarios`/`Cited In` left blank) and one suggestion (consider adding P3). Since then, both `scenario.md` and `scenario.yml` were backfilled with `related_scenarios: [exiting_room, narrow_doorway]` and `cited_in: ["Robotics at Google (R@G), internal scenario reference"]`, and the R@G citation text was corrected from the earlier unverified "Robots@Games (R@G)" to the confirmed "Robotics at Google (R@G)" (commit `93d55c3`), fully resolving the should-fix. The P3 suggestion remains open and unchanged (non-blocking, editor's call). One new suggestion-level observation was added: the STATUS block's `EDITED` provenance line has not been updated to record this backfill-and-correction pass.
