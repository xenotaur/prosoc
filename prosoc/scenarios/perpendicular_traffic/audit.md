---
scenario: perpendicular_traffic_01
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-07-20
---

# Audit: Perpendicular Traffic

- **Scenario:** `prosoc/scenarios/perpendicular_traffic/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with one minor fix.

## Findings

### 1. Related Scenarios / Cited In left incomplete despite content already existing elsewhere in the card — should-fix
- **Section/field:** Scenario Card Summary (`Related Scenarios`, `Cited In` bullets are absent entirely, replaced by a "Remaining gaps" callout); YAML `related_scenarios` and `cited_in` keys are also absent from `scenario.yml`/the embedded YAML.
- **Issue:** The Status block already states `cited in [167]`, and `evaluation_notes` already says this scenario "is related to Plaza Crossing... and to Parallel Traffic." `parallel_traffic` is an implemented scenario in this corpus (`prosoc/scenarios/parallel_traffic/`), so at least that relation is a real, referenceable `related_scenarios` entry — this data isn't missing, it just hasn't been promoted from prose into the structured Card Summary/YAML fields the template expects.
- **Recommended fix:** Add `- **Related Scenarios:** parallel_traffic (Plaza Crossing — descriptive variant per [167], not separately defined in Table 3, not implemented in this corpus)` and `- **Cited In:** [167]` to the Scenario Card Summary, and add corresponding `related_scenarios: [parallel_traffic]` and `cited_in: ["167"]` keys to the YAML block (and `scenario.yml` via the distiller).

## Suggestions

### 2. Stray "Remaining gaps" audit-artifact note left inside the Scenario Card Summary — suggestion
- **Section/field:** `scenario.md`, Scenario Card Summary section, lines "**Remaining gaps:** / - **Related Scenarios** — should-fill-in-now / - **Cited In** — should-fill-in-now"
- **Issue:** This looks like a note carried over from an earlier audit/edit pass rather than content defined by `template.md` (which has no "Remaining gaps" subsection). Leaving it in the published card is harmless but non-standard, and it duplicates what Finding 1 above already covers more precisely.
- **Recommended fix:** Remove the "Remaining gaps" callout once Finding 1 is addressed (or now, since it's redundant with this audit report).

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
| Related Scenarios | Plaza Crossing | Discussed in `evaluation_notes` but not in a structured field (see Finding 1) | Content present, not yet structured |
| Cited In | [167] | In STATUS block, not in a structured Card Summary/YAML field (see Finding 1) | Content present, not yet structured |

No content mismatches found. The card remains faithful to the Table 3 entry across every checkable dimension.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary:** Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, and Ideal Outcome are all present as a standalone Markdown section (resolving both should-fix findings from the prior audit, which flagged the entire Card Summary and Scenario Usage Guide sections as missing from `scenario.md`). Related Scenarios and Cited In are the only gaps — should-fill-in-now (Finding 1).
- **Scenario Usage Guide:** Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all present as a standalone Markdown section, matching the embedded YAML's `scenario_usage_guide`.

## Schema / Tooling Check

`scripts/distill/scenarios --scenario perpendicular_traffic --dry-run --show-diffs` produced no diff and exited 0 — `scenario.yml` is in sync with `scenario.md`'s embedded YAML and validates against `schema.json`. `expected_behaviors` uses only `must`/`should`/`should_not`, with no over-specified (exact-motion/numeric-threshold) entries. `relevant_principles` (P1, P3, P6, P7) and `scenario_usage_guide.quality_metrics` (P3, P7) contain only valid P0–P9 identifiers, count 4 (within the 3–5 guidance). `STATE` reads `DRAFTED`, a valid enumerated lifecycle state; this audit did not modify it.
