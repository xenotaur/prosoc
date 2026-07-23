---
scenario: perpendicular_traffic
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-07-22
---

# Audit: Perpendicular Traffic

- **Scenario:** `prosoc/scenarios/perpendicular_traffic/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready — no blocking, should-fix, or suggestion findings.

## Findings

No findings. `scenario.md` and `scenario.yml` are unchanged since the 2026-07-21 audit, which itself found no outstanding issues (the should-fix and suggestion flagged in the 2026-07-20 audit — missing `related_scenarios`/`cited_in` in the Card Summary, and a stray "Remaining gaps" callout — were resolved before that pass and remain resolved here).

## Source Fidelity

SOURCE cites "P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [167]" — checked against `../_shared/pg_scenarios.md`'s "Perpendicular Traffic" entry:

| Field | P&G Table 3 | Scenario card | Match? |
|---|---|---|---|
| Description | Crowd moves perpendicular to the robot | Robot crosses while a crowd flows perpendicular to its path | Yes |
| Physical Env | Generic | `context.environment.type: generic` | Yes |
| Geometric Layout | Intersection | `geometric_layout: intersection` | Yes |
| Scientific Purpose | Crowd navigation | `scientific_purpose: crowd navigation` | Yes |
| Robot Task | Cross navigate | `intended_robot_task: cross navigate through the perpendicular flow` | Yes |
| Human Behavior | Mill from A to B | `intended_human_behavior: mill from A to B, forming a continuous perpendicular stream` | Yes |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot crosses the perpendicular flow without collision or obstruction` | Yes |
| Related Scenarios | Plaza Crossing | `related_scenarios: [parallel_traffic, intersection_no_gesture]`; `evaluation_notes` separately notes Plaza Crossing is "a descriptive variant implied by [167], not separately defined in Table 3" and thus not implemented in this corpus | Yes — Table 3's "Plaza Crossing" has no implemented counterpart to link to; the card correctly substitutes the two implemented, conceptually related scenarios (`parallel_traffic`, `intersection_no_gesture`) and explains the Plaza Crossing gap in prose |
| Cited In | [167] | `cited_in: ["167"]` | Yes |

No content mismatches found. The card remains faithful to the Table 3 entry across every checkable dimension.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary:** Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, and Cited In are all present.
- **Scenario Usage Guide:** Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all present and match the embedded YAML's `scenario_usage_guide`.

No blank required fields remain.

## Schema / Tooling Check

`scripts/distill/scenarios --scenario perpendicular_traffic --dry-run --show-diffs` produced no diff and exited 0 — `scenario.yml` is in sync with `scenario.md`'s embedded YAML and validates against `schema.json`. `expected_behaviors` uses only `must`/`should`/`should_not`, with no over-specified (exact-motion/numeric-threshold) entries. `relevant_principles` (P1, P3, P6, P7) and `scenario_usage_guide.quality_metrics` (P3, P7) contain only valid P0–P9 identifiers, count 4 (within the 3–5 guidance). `STATE` reads `DRAFTED`, a valid enumerated lifecycle state; this audit did not modify it.

## Change Since Last Audit (2026-07-21)

No changes to `scenario.md` or `scenario.yml` since the 2026-07-21 audit. This re-audit reproduces the same verdict and counts (ready; 0 blocking; 0 should-fix; 0 suggestion) — no substantive change.
