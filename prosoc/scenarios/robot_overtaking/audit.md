---
scenario: robot_overtaking
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-22
---

# Audit: Robot Overtaking

- **Scenario:** `prosoc/scenarios/robot_overtaking/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready — no blocking or should-fix issues found; the Normative
  Expectations gap flagged in the prior audit (2026-07-21) has been resolved.

## Findings

### 1. Physical Environment specialization vs. P&G Table 3 "Generic" — suggestion
- **Section/field:** Scenario Card Summary "Physical Environment" / YAML
  `context.environment.type` vs. P&G Table 3's Robot Overtaking entry
- **Issue:** The card specifies `indoor` / "corridor or sidewalk-like passage," while
  P&G Table 3 categorizes Robot Overtaking's Physical Env as "Generic" (Geometric
  Layout: "Passable space," which the card does match). This is a reasonable
  specialization, not a contradiction, but the card doesn't note that it's a
  deliberate narrowing of the paper's more general categorization.
- **Recommended fix:** Optionally add a brief note (in `evaluation_notes` or the
  Social Navigation Context section) that "indoor" is a deliberate specialization of
  the paper's "generic" passable-space categorization, so a reader comparing against
  Table 3 doesn't mistake it for drift.

### 2. `related_scenarios` could include additional corpus matches named in prose — suggestion
- **Section/field:** `related_scenarios` (YAML) / "Related Scenarios" (Card Summary)
  vs. "Notes for Scenario Designers and Evaluators"
- **Issue:** `related_scenarios` lists only `pedestrian_overtaking`, but the Notes
  section says this scenario "pairs naturally with frontal approach scenarios, group
  overtaking variants, narrow-passage constraints, and distracted pedestrian
  variants." Two of these correspond to scenarios that already exist in the corpus —
  `frontal_approach` and `single_file_hallway` (the corpus's narrow-passage scenario,
  per `../../../.claude/skills/_shared/pg_scenarios.md`) — but neither is added to
  `related_scenarios`.
- **Recommended fix:** Consider adding `frontal_approach` and `single_file_hallway` to
  `related_scenarios` if the pairing is intended to be a formal cross-reference; leave
  as-is if the Notes mention is meant only as a loose, non-binding aside.

## Source Fidelity

SOURCE is cited informally as "Prompt to ChatGPT 5.2" with no retrievable content, but
the Social Navigation Context section explicitly ties this scenario to the *Principles
and Guidelines for Social Robot Navigation* paper, and it clearly corresponds to the
**Robot Overtaking** entry in P&G Table 3 (per `../../../.claude/skills/_shared/pg_scenarios.md`):

- **P&G Table 3 "Robot Overtaking":** Description: "Robot overtakes a moving
  pedestrian"; Physical Env: Generic; Geometric Layout: Passable space; Scientific
  Purpose: Pedestrian interaction; Robot Task: Navigate A to B; Human Behavior:
  Navigate A to B (slower); Ideal Outcome: Robot passes human; Cited In: [50, 157].

Comparing against the card:
- **Robot/human roles and relative speed:** Match — `relative_speed: robot_faster`,
  human is the slower pedestrian being overtaken, consistent with "Human Behavior:
  Navigate A to B (slower)."
- **Task:** Match — `intended_robot_task: navigate from A to B`.
- **Geometric layout:** Match — `geometric_layout: passable space`.
- **Scientific purpose:** Match — `scientific_purpose: pedestrian interaction`.
- **Ideal outcome:** Match in substance — `ideal_outcome: robot passes the human
  safely, comfortably, and without disruption` is a reasonable elaboration of Table
  3's "Robot passes human."
- **Cited In:** Match — `cited_in: ["50", "157"]` matches Table 3 exactly.
- **Physical environment:** Drift, not contradiction — card specifies `indoor` where
  Table 3 says "Generic" (see Finding 1 above).

Overall: strong fidelity to the P&G Table 3 entry, with one minor, non-contradictory
specialization (physical environment) noted above.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields, all are present:

- **Scenario Card Summary:** Complete — Scenario Name, Description, Scientific
  Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human
  Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, and
  Cited In are all populated and consistent with the YAML.
- **Scenario Usage Guide — Success Metrics:** Complete (SR, NoCollisions).
- **Scenario Usage Guide — Quality Metrics:** Complete (P2, P3, P4 — a sensible
  subset of `relevant_principles`).
- **Scenario Usage Guide — Ideal Outcome:** Complete.
- **Scenario Usage Guide — Failure Modes:** Complete (three concrete failure modes,
  consistent with `evaluation_notes`).
- **Scenario Usage Guide — Labeling Criteria:** Complete (three concrete,
  data-recognizable criteria).

No required fields are blank. `related_scenarios` is populated but could arguably be
expanded (see Finding 2, a suggestion rather than a completeness gap, since a single
related scenario is a valid non-empty answer).

## Re-audit Note

This is a fresh point-in-time re-audit (2026-07-22), reflecting PR #31's edit to the
Normative Expectations prose. That edit added the previously-missing clause covering
`expected_behaviors.should_not`'s fourth entry ("force the pedestrian to change path
or pace"): the paragraph now reads "...or forcing the pedestrian to change path or
pace to accommodate the robot." This closes the prior audit's (2026-07-21) sole
should-fix finding — prose and YAML `should_not` are now fully aligned, all four
entries covered. `scripts/distill/scenarios --scenario robot_overtaking --dry-run
--show-diffs` reports no diff and no schema errors. The two suggestions from the prior
audit (physical-environment specialization vs. Table 3's "Generic"; possible
expansion of `related_scenarios`) remain open and are carried forward unchanged, as
neither was addressed by this edit. Verdict is upgraded from `ready_with_fixes` to
`ready` since no should-fix or blocking findings remain.
