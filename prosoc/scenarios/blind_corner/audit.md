---
scenario: blind_corner
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-07-22
---

# Audit: Blind Corner

- **Scenario:** `prosoc/scenarios/blind_corner/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready, no issues found

## Findings

No findings. This is a fresh point-in-time re-audit of the current corpus state; the
scenario has not been edited since the prior audit (2026-07-21), and this pass
independently reconfirms the same clean result rather than relying on it.

## Prose/YAML Consistency

No contradictions or drift found. Scenario Overview, Social Navigation Context, and
Normative Expectations align with `intended_robot_task` ("navigate from A to B
through the corner"), `intended_human_behavior` ("navigate from B to A through the
corner"), `agents` (robot: `navigating_agent`; humans: one `pedestrian`), and
`ideal_outcome`. The prose's "acceptable"/"unacceptable" behavior lists map cleanly
onto `expected_behaviors.{must,should,should_not}` with no one-sided claims (e.g.
"slowing on approach" ↔ `should: reduce speed when approaching blind corners`;
"approaching at full speed without modulation" ↔ `should_not: approach blind
corners at full speed without any modulation`).

## Schema and Charter Compliance

- `scripts/distill/scenarios --scenario blind_corner --dry-run --show-diffs` produced
  no diff and no schema validation error — `scenario.yml` is in sync with
  `scenario.md`'s embedded YAML and validates against `schema.json`.
- `expected_behaviors` uses only `must`/`should`/`should_not`, matching the schema's
  `additionalProperties: false` constraint.
- `relevant_principles`: P1, P2, P3, P7 — four valid P0–P9 IDs, within the
  recommended 3–5 range, each discussed in the card's own prose (safety/detection
  range, comfort/startling, legibility under spatial constraint, proactivity/
  deadlock resolution).
- `scenario_usage_guide.quality_metrics`: P2, P3 — valid P0–P9 IDs.
- `expected_behaviors` entries describe kinds of behavior ("reduce speed," "stop
  promptly," "yield") rather than exact motions or numeric thresholds — no
  over-specification per P&G Guideline N6.
- `related_scenarios` (`frontal_approach`, `narrow_doorway`) both reference existing
  directories under `prosoc/scenarios/`. Table 3 lists no related scenario for Blind
  Corner, so this addition is the documented, expected divergence case (per the
  audit checklist and the card's own "Related Scenarios note" in
  `evaluation_notes`) — not a defect.

## Source Fidelity

SOURCE cites P&G Paper Table 3 (Francis et al., 2025), "Blind Corner" entry, cited
in [126, 171]. Compared against `.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | Card | Match |
|---|---|---|---|
| Description | Robot and human meet at a blind corner | Robot and human pedestrian meet at an indoor blind corner | Yes |
| Physical Env | Indoor | Indoor | Yes |
| Geometric Layout | Corner | Corner | Yes |
| Scientific Purpose | Pedestrian interaction | Pedestrian interaction | Yes |
| Robot Task | Navigate A to B | Navigate from A to B through the corner | Yes |
| Human Behavior | Navigate B to A | Navigate from B to A through the corner | Yes |
| Ideal Outcome | No collision / obstruction | Robot and human pass each other at the corner without collision or obstruction | Yes |
| Related Scenarios | (none listed) | frontal_approach, narrow_doorway (card's own addition, documented as expected divergence) | Consistent |
| Cited In | [126, 171] | 126, 171 | Yes |

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

All fields `template.md` marks "Required for AUDITED scenarios" are filled:

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose,
  Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior,
  Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) —
  all present and populated.
- **Scenario Usage Guide** (Success Metrics, Quality Metrics, Ideal Outcome, Failure
  Modes, Labeling Criteria) — all present as a dedicated section, consistent with
  the embedded YAML's `scenario_usage_guide` block.

No blank required fields; nothing to categorize as reasonably-blank or
should-fill-in-now.
