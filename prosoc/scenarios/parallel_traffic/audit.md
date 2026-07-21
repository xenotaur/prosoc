---
scenario: parallel_traffic
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 1
audited: 2026-07-20
---

# Audit: Parallel Traffic

- **Scenario:** `prosoc/scenarios/parallel_traffic/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes — Card Summary and Usage Guide prose are now present and are a faithful, consistent rendering of the YAML; two required completeness fields remain blank but are readily fillable.

## Findings

### 1. Related Scenarios blank in Scenario Card Summary — should-fix
- **Section/field:** Scenario Card Summary — Related Scenarios (template.md: "Required for AUDITED scenarios")
- **Issue:** The Card Summary's own "Remaining gaps" note already flags this field as blank. It is readily inferable: the "Notes for Scenario Designers and Evaluators" section and the YAML's `evaluation_notes` both already name *Perpendicular Traffic*, *Circular Crossing*, and *Crowd Navigation* as related scenarios, and `.claude/skills/_shared/pg_scenarios.md`'s P&G Table 3 entry for Parallel Traffic lists "Circular Crossing" as the canonical related scenario.
- **Recommended fix:** Populate "Related Scenarios" in the Card Summary (and optionally a `related_scenarios` list in the YAML block, which schema.json supports but the file currently omits) with `circular_crossing`, `perpendicular_traffic`, and `crowd_navigation`.

### 2. Cited In blank in Scenario Card Summary — should-fix
- **Section/field:** Scenario Card Summary — Cited In (template.md: "Required for AUDITED scenarios")
- **Issue:** Also self-flagged in the "Remaining gaps" note. The Status block's SOURCE line already states "cited in [167]," and pg_scenarios.md's Table 3 entry confirms `[167]` as the citation for Parallel Traffic, so the value is already known and just needs to be copied into the Card Summary (and optionally the YAML's `cited_in` field, which schema.json supports but the file omits).
- **Recommended fix:** Populate "Cited In" with `[167]` in the Card Summary; consider adding `cited_in: ["167"]` to the YAML block for machine-readability.

### 3. Normative Expectations prose doesn't mirror the must/should/should_not split — suggestion
- **Section/field:** Normative Expectations vs. `expected_behaviors.{must,should,should_not}`
- **Issue:** The prose "Normative Expectations" section presents two flat lists ("Acceptable robot behavior includes" / "Unacceptable behavior includes") without distinguishing `must` (strictly required) from `should` (preferred). For example, "Cutting perpendicular to the flow to reach a position, disrupting multiple pedestrians' paths" reads as strictly forbidden and correctly maps to `must` ("not cut across multiple pedestrians' lanes to force a position"), while "Merging into the pedestrian stream at a natural point" maps to `should` — but a reader relying only on the prose can't tell the two apart. Content matches the YAML; this is drift in emphasis, not a contradiction.
- **Recommended fix:** Optionally annotate the prose list (e.g., "(required)" / "(preferred)" tags) or group must-items first, so a prose-only reader gets the same required/preferred signal as the YAML.

## Source Fidelity

SOURCE cites "P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [167]." Compared against `.claude/skills/_shared/pg_scenarios.md`'s Parallel Traffic entry (Crowd Scenarios section):

| Field | P&G Table 3 | Scenario card | Result |
|---|---|---|---|
| Description | "Crowd moves parallel to the robot" | Crowd moves broadly in the same direction, forming an emergent pedestrian stream the robot must merge into and hold position within | Match (elaborated) |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Passable space | `geometric_layout: passable space` | Match |
| Scientific Purpose | Crowd navigation | `scientific_purpose: crowd navigation` | Match |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B` | Match |
| Human Behavior | Mill from A to B | `intended_human_behavior: mill from A to B, forming a parallel pedestrian stream` | Match (elaborated) |
| Ideal Outcome | No collision / obstruction | "robot merges into and travels with the pedestrian stream without collision or obstruction" | Match |
| Related Scenarios | Circular Crossing | Named in Notes/evaluation_notes (plus Perpendicular Traffic, Crowd Navigation), but blank in the required Card Summary field | See Finding 1 |
| Cited In | [167] | Named in Status/SOURCE, but blank in the required Card Summary field | See Finding 2 |

No mismatches. All checkable Table 3 fields agree with the scenario card.

## Schema and Charter Compliance

- Single-scenario dry-run distill (`scripts/distill/scenarios --scenario parallel_traffic --dry-run --show-diffs`) reported no diff and no schema validation error — `scenario.yml` is in sync with the embedded YAML in `scenario.md` and validates against `schema.json`.
- `relevant_principles: [P1, P2, P5, P6]` — 4 entries, all valid P0–P9, within the recommended 3–5 range.
- `scenario_usage_guide.quality_metrics: [P2, P5]` — valid P0–P9.
- `expected_behaviors` entries describe kinds of behavior (e.g., "match pace broadly to the surrounding flow," "maintain a consistent lateral position within the flow") rather than exact motions or numeric thresholds — no P&G Guideline N6 over-specification found.

## Completeness

**Scenario Card Summary** (template.md: required for AUDITED):
- Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome — all present and consistent with the YAML and P&G source.
- Related Scenarios — blank — **should-fill-in-now** (Finding 1).
- Cited In — blank — **should-fill-in-now** (Finding 2).

**Scenario Usage Guide** (template.md: required for AUDITED):
- Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria — all present and consistent with the YAML's `scenario_usage_guide` block.

No other required fields are blank.
