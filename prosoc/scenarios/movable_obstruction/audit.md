---
scenario: movable_obstruction
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 0
audited: 2026-07-21
---

# Audit: Movable Obstruction

- **Scenario:** `prosoc/scenarios/movable_obstruction/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready for AUDITED with a minor fix — the P0 principle-omission finding
  from the prior audit is resolved (P0 has been restored to `relevant_principles`,
  consistent with the Discussion section's explicit naming of "Trade-offs between
  Goal Achievement (P0) and prosocial action"). One should-fix carried forward from
  the prior audit remains open.

## Findings

### 1. Discussion still references task/context names not connected to the YAML — should-fix
- **Section/field:** Discussion vs. `scenario.yml`
- **Issue:** The Discussion section names specific tasks/contexts
  (`NAVIGATE_POINT_TO_POINT`, `DELIVER_OBJECT`, `ROUTINE_DELIVERY`, `GUIDANCE_DOCENT`,
  `HIGH_URGENCY`) that appear to reference `prosoc/tasks/` and `prosoc/contexts/` IDs,
  but no structured field in `scenario.yml` (`initial_conditions`, `evaluation_notes`,
  or otherwise) ties this scenario to a specific task/context pairing. This is a
  carry-over from the 2026-07-05 and 2026-07-20 audits and has not yet been addressed.
- **Recommended fix:** If the task/context cross-references are intentional, either add
  a structured field tying the scenario to specific task/context IDs, or move the
  cross-reference into `evaluation_notes` so it is machine-visible rather than
  narrative-only.

## Source Fidelity

The SOURCE field cites "Principles and Guidelines for Evaluating Social Robot
Navigation (P&G paper)" generically, without a specific table or section reference.
Per `.claude/skills/_shared/pg_scenarios.md`: **"The `movable_obstruction` scenario
has no direct P&G Table 3 counterpart."** This is unchanged from prior audits.

**Source fidelity: not checkable against Table 3** — the shared reference data
explicitly states this scenario has no direct P&G Table 3 counterpart, and the SOURCE
field does not cite a specific section, page, or figure of the paper that could be
checked directly. Carried forward as a standing observation rather than a numbered
finding: the SOURCE field would ideally be more precise (e.g., marking this as an
original extension of *Frontal Approach* motivated by the P7/P9 distinction in the
paper's principle framework, rather than a direct paper citation).

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric
  Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome** — present, consistent
  between prose and YAML.
- **Success Metrics, Quality Metrics** — present as both YAML fields and prose
  (Scenario Card Summary and Scenario Usage Guide sections agree: `SR, NoCollisions,
  ConflictResolved` / `P3, P7, P9`).
- **Related Scenarios** — present (`frontal_approach`, `single_file_hallway`).
- **Failure Modes, Labeling Criteria** — present as both YAML and prose, matching.
- **Cited In** — still blank. This is already self-flagged in the scenario's own
  "Remaining gaps" note as should-fill-in-now; concur with that self-assessment. Not
  blocking for AUDITED (no evidence yet of external citation), but should be revisited
  if this scenario is referenced elsewhere.

## Principle Count Note (relevant_principles = 6)

`relevant_principles` now lists six principles (`P0, P1, P3, P5, P7, P9`), above the
3–5 count in `.claude/skills/_shared/principles.md`'s soft guideline. Per that same
file (updated this session): *"if a scenario's own prose (Overview, Discussion, or
`evaluation_notes`) explicitly names and discusses a principle... include that
principle even if the list grows past 5."* The Discussion section explicitly names
"Trade-offs between **Goal Achievement (P0)** and prosocial action" as one of the
scenario's three analytical axes, so P0's inclusion is directly justified by the
card's own prose. This is not raised as a finding — the count-over-guidance pattern
here is exactly the documented exception, not a defect.

## Verdict Rationale

With the P0/`relevant_principles` inconsistency resolved and no other correctness
issues found, this scenario is ready for AUDITED. The remaining should-fix
(unconnected task/context taxonomy in Discussion prose) is a completeness/traceability
nit rather than a blocker — the task/context names are illustrative examples within a
paragraph explaining how appropriate behavior varies by task and context, not a
formal claim requiring a structured cross-reference.
