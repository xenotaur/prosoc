---
scenario: parallel_traffic
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-21
---

# Audit: Parallel Traffic

- **Scenario:** `prosoc/scenarios/parallel_traffic/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready, no blocking or should-fix issues found — Card Summary, YAML, and Usage Guide are complete and internally consistent; both previously-flagged completeness gaps (Related Scenarios, Cited In) are now filled in.

## Findings

### 1. Normative Expectations prose doesn't mirror the must/should/should_not split — suggestion
- **Section/field:** Normative Expectations vs. `expected_behaviors.{must,should,should_not}`
- **Issue:** The prose "Normative Expectations" section presents two flat lists ("Acceptable robot behavior includes" / "Unacceptable behavior includes") without distinguishing `must` (strictly required) from `should`/`should_not` (preferred). For example, "Cutting perpendicular to the flow to reach a position, disrupting multiple pedestrians' paths" reads as strictly forbidden and correctly maps to `must` ("not cut across multiple pedestrians' lanes to force a position"), while "Merging into the pedestrian stream at a natural point" maps to `should` — but a reader relying only on the prose can't tell the two apart. Content matches the YAML; this is drift in emphasis, not a contradiction. (Carried forward unchanged from the 2026-07-20 audit — not addressed by the related_scenarios/cited_in backfill, which was orthogonal.)
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
| Related Scenarios | Circular Crossing | Card lists `perpendicular_traffic`, `crowd_navigation` (not `circular_crossing`) | Partial — see note below |
| Cited In | [167] | `cited_in: ["167"]`, and Card Summary "Cited In: 167" | Match |

**Note on Related Scenarios divergence:** P&G Table 3 names "Circular Crossing" as Parallel Traffic's related scenario, but the card's `related_scenarios` field (and Card Summary) list `perpendicular_traffic` and `crowd_navigation` instead. This is not an error: `circular_crossing` does not exist as an implemented scenario directory in this repo (confirmed — no such directory under `prosoc/scenarios/`; `pg_scenarios.md` itself notes Circular Crossing is a Figure 7 variant not in Table 3 with no full metadata), so it cannot be used as a `related_scenarios` reference to a real scenario id. The card's own `evaluation_notes` and "Notes for Scenario Designers and Evaluators" section discuss all three (Perpendicular Traffic, Circular Crossing, Crowd Navigation) as related; choosing the two that actually exist in the corpus for the machine-readable field is a reasonable, deliberate choice. No mismatch flagged; this is provenance context for a human reviewer, not a finding.

## Schema and Charter Compliance

- Single-scenario dry-run distill (`scripts/distill/scenarios --scenario parallel_traffic --dry-run --show-diffs`) reported no diff and no schema validation error (exit 0) — `scenario.yml` is in sync with the embedded YAML in `scenario.md` and validates against `schema.json`.
- `relevant_principles: [P1, P2, P5, P6]` — 4 entries, all valid P0–P9, within the recommended 3–5 range.
- `scenario_usage_guide.quality_metrics: [P2, P5]` — valid P0–P9.
- `expected_behaviors` entries describe kinds of behavior (e.g., "match pace broadly to the surrounding flow," "maintain a consistent lateral position within the flow") rather than exact motions or numeric thresholds — no P&G Guideline N6 over-specification found.
- `related_scenarios: [perpendicular_traffic, crowd_navigation]` and `cited_in: ["167"]` are both present in `scenario.yml` and schema-valid (arrays of strings).

## Completeness

**Scenario Card Summary** (template.md: required for AUDITED):
- Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome — all present and consistent with the YAML and P&G source.
- Related Scenarios — now filled in (`perpendicular_traffic`, `crowd_navigation`) — previously should-fix, now resolved.
- Cited In — now filled in (`167`) — previously should-fix, now resolved.

**Scenario Usage Guide** (template.md: required for AUDITED):
- Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria — all present and consistent with the YAML's `scenario_usage_guide` block.

No required fields are blank.
