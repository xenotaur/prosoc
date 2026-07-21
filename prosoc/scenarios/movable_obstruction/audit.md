---
scenario: movable_obstruction
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-07-20
---

# Audit: Movable Obstruction

- **Scenario:** `prosoc/scenarios/movable_obstruction/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes — the structural gaps and principle-count
  issue from the prior (2026-07-05) audit have been resolved; one should-fix and one
  suggestion remain.

## Findings

### 1. Discussion still references task/context names not connected to the YAML — should-fix
- **Section/field:** Discussion vs. `scenario.yml`
- **Issue:** The Discussion section names specific tasks/contexts (`NAVIGATE_POINT_TO_POINT`,
  `DELIVER_OBJECT`, `ROUTINE_DELIVERY`, `GUIDANCE_DOCENT`, `HIGH_URGENCY`) that appear to
  reference `prosoc/tasks/` and `prosoc/contexts/` IDs, but no structured field in
  `scenario.yml` (`initial_conditions`, `evaluation_notes`, or otherwise) ties this
  scenario to a specific task/context pairing. This is a carry-over from the prior audit
  (Finding 4, 2026-07-05) and was not addressed by this session's edits.
- **Recommended fix:** If the task/context cross-references are intentional, either add a
  structured field tying the scenario to specific task/context IDs, or move the
  cross-reference into `evaluation_notes` so it is machine-visible rather than narrative-only.

### 2. Discussion names Goal Achievement (P0) as a core tension, but `relevant_principles` omits it — suggestion
- **Section/field:** Discussion vs. `relevant_principles`
- **Issue:** The Discussion section explicitly calls out "Trade-offs between **Goal
  Achievement (P0)** and prosocial action" as one of the scenario's evaluative dimensions,
  but `relevant_principles` (`P1, P3, P5, P7, P9`) does not include P0. This isn't a
  contradiction — P0 is discussed as context for the P7/P9 tension rather than asserted as
  a directly-evaluated principle — but it's a one-sided claim worth a human's judgment call.
- **Recommended fix:** Either add P0 to `relevant_principles` (would bring the count to 6,
  above the 3–5 guidance) or soften/remove the explicit "(P0)" tag in the Discussion prose
  if it's meant as background framing rather than a claim that P0 is being evaluated here.

## Source Fidelity

The SOURCE field cites "Principles and Guidelines for Evaluating Social Robot Navigation
(P&G paper)" generically, without a specific table or section reference. Per
`.claude/skills/_shared/pg_scenarios.md`: **"The `movable_obstruction` scenario has no
direct P&G Table 3 counterpart."** This is unchanged from the prior audit and is stated
explicitly in the shared reference data, meaning there is no Table 3 entry to compare
physical description, scientific purpose, geometric layout, roles, task, or ideal outcome
against.

**Source fidelity: not checkable against Table 3** — the shared reference data explicitly
states this scenario has no direct P&G Table 3 counterpart, and the SOURCE field does not
cite a specific section, page, or figure of the paper that could be checked directly. This
is carried forward as a standing observation rather than a numbered finding (consistent
with the prior audit's treatment): the SOURCE field would ideally be more precise (e.g.,
marking this as an original extension of *Frontal Approach* motivated by the P7/P9
distinction in the paper's principle framework, rather than a direct paper citation).

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields — this session's edits
(scientific_purpose, geometric_layout, intended_robot_task, intended_human_behavior,
ideal_outcome, related_scenarios, and the full Scenario Card Summary / Scenario Usage
Guide prose sections) resolved essentially all of the completeness gaps flagged in the
prior (2026-07-05) audit:

- **Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric
  Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome** — present, consistent
  between prose and YAML.
- **Success Metrics, Quality Metrics** — present as both YAML fields and prose (Scenario
  Card Summary and Scenario Usage Guide sections agree: `SR, NoCollisions,
  ConflictResolved` / `P3, P7, P9`).
- **Related Scenarios** — now filled in (`frontal_approach`, `single_file_hallway`);
  resolves the prior audit's "reasonably blank, could be promoted" note.
- **Failure Modes, Labeling Criteria** — present as both YAML and prose, matching.
- **Cited In** — still blank. This is already self-flagged in the scenario's own
  "Remaining gaps" note as should-fill-in-now; concur with that self-assessment. Not
  blocking for AUDITED (no evidence yet of external citation), but should be revisited
  if this scenario is referenced elsewhere.

Overall this scenario has moved substantially closer to AUDITED-readiness since the prior
audit: the structural gap (missing template sections) and the principle-count overage are
both resolved, leaving one should-fix (unconnected task/context taxonomy in prose) and one
suggestion (P0 mentioned in Discussion but not in `relevant_principles`).
