---
family: scenarios
card: blind_corner
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-07-29
---

# Audit: Blind Corner

- **Card:** `prosoc/scenarios/blind_corner/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-07-29
- **Verdict:** Ready, no issues found

## Findings

No findings. Fresh point-in-time re-audit under `prosoc-card-audit` (the
family-dispatched successor to `prosoc-scenario-audit`); independently
reconfirms the same clean result as the prior audit.

## Prose/YAML Consistency

No contradictions or drift found. Scenario Overview, Social Navigation Context,
and Normative Expectations align with `intended_robot_task`,
`intended_human_behavior`, `agents`, and `ideal_outcome`. The prose's
"acceptable"/"unacceptable" behavior lists map cleanly onto
`expected_behaviors.{must,should,should_not}` with no one-sided claims.

## Schema and Charter Compliance

- `scripts/distill/scenarios --scenario blind_corner --dry-run --show-diffs`
  produced no diff and no schema validation error — `scenario.yml` is in sync
  with `scenario.md`'s embedded YAML and validates against `schema.json`.
- `expected_behaviors` uses only `must`/`should`/`should_not`.
- `relevant_principles`: P1, P2, P3, P7 — four valid P0–P9 IDs, within the
  recommended 3–5 range, each discussed in the card's own prose.
- `scenario_usage_guide.quality_metrics`: P2, P3 — valid P0–P9 IDs.
- `expected_behaviors` entries describe kinds of behavior, not exact motions
  or numeric thresholds — no over-specification per P&G Guideline N6.
- `related_scenarios` (`frontal_approach`, `narrow_doorway`) both reference
  existing directories. Table 3 lists no related scenario for Blind Corner,
  so this addition is the documented, expected divergence case — not a
  defect.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Blind Corner" entry, cited in [126, 171].
Compared against `.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | Card | Match |
|---|---|---|---|
| Description | Robot and human meet at a blind corner | Robot and human pedestrian meet at an indoor blind corner | Yes |
| Physical Env | Indoor | Indoor | Yes |
| Geometric Layout | Corner | Corner | Yes |
| Scientific Purpose | Pedestrian interaction | Pedestrian interaction | Yes |
| Robot Task | Navigate A to B | Navigate from A to B through the corner | Yes |
| Human Behavior | Navigate B to A | Navigate from B to A through the corner | Yes |
| Ideal Outcome | No collision / obstruction | Robot and human pass each other at the corner without collision or obstruction | Yes |
| Related Scenarios | (none listed) | frontal_approach, narrow_doorway (documented expected divergence) | Consistent |
| Cited In | [126, 171] | 126, 171 | Yes |

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

All fields `template.md` marks "Required for AUDITED scenarios" are filled —
Scenario Card Summary and Scenario Usage Guide are both fully populated. No
blank required fields.
