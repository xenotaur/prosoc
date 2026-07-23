---
scenario: parallel_traffic
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-22
---

# Audit: Parallel Traffic

- **Scenario:** `prosoc/scenarios/parallel_traffic/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready, no blocking or should-fix issues found — Card Summary, YAML, and Usage Guide are complete and internally consistent. This re-audit reflects the PR #30 addition of an explicit "Related Scenarios note" to `evaluation_notes` documenting the `related_scenarios`/Table 3 divergence; that note is itself the expected self-documentation the audit checklist calls for, not a defect.

## Findings

### 1. Normative Expectations prose doesn't mirror the must/should/should_not split — suggestion
- **Section/field:** Normative Expectations vs. `expected_behaviors.{must,should,should_not}`
- **Issue:** The prose "Normative Expectations" section presents two flat lists ("Acceptable robot behavior includes" / "Unacceptable behavior includes") without distinguishing `must` (strictly required) from `should`/`should_not` (preferred). For example, "Cutting perpendicular to the flow to reach a position, disrupting multiple pedestrians' paths" reads as strictly forbidden and correctly maps to `must` ("not cut across multiple pedestrians' lanes to force a position"), while "Merging into the pedestrian stream at a natural point" maps to `should` — but a reader relying only on the prose can't tell the two apart. Content matches the YAML; this is drift in emphasis, not a contradiction. (Carried forward unchanged across prior audits — not addressed by the related_scenarios/cited_in backfill or the new PR #30 evaluation_notes addition, both of which are orthogonal to this section.)
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
| Related Scenarios | Circular Crossing | Card lists `perpendicular_traffic`, `crowd_navigation` (not `circular_crossing`) | Expected divergence — see note below |
| Cited In | [167] | `cited_in: ["167"]`, and Card Summary "Cited In: 167" | Match |

**Note on Related Scenarios divergence:** P&G Table 3 names "Circular Crossing" as Parallel Traffic's related scenario, but the card's `related_scenarios` field (and Card Summary) list `perpendicular_traffic` and `crowd_navigation` instead. `circular_crossing` does not exist as an implemented scenario directory in this repo (confirmed — no such directory under `prosoc/scenarios/`; `pg_scenarios.md` itself notes Circular Crossing is a Figure 7 variant not in Table 3 with no full metadata), which is the first of the three expected-divergence cases in `prosoc-scenario-audit`'s `audit_checklist.md`: Table 3 names an unimplemented sibling and the card substitutes implemented scenarios it actually discusses in its own prose. As of PR #30, `evaluation_notes` now includes an explicit "Related Scenarios note" paragraph stating exactly this rationale, so the card self-documents the divergence rather than leaving it implicit. Per the checklist, this is expected and not a source-fidelity defect — no mismatch flagged.

## Schema and Charter Compliance

- Single-scenario dry-run distill (`scripts/distill/scenarios --scenario parallel_traffic --dry-run --show-diffs`) reported no diff and no schema validation error (exit 0) — `scenario.yml` is in sync with the embedded YAML in `scenario.md` and validates against `schema.json`.
- `relevant_principles: [P1, P2, P5, P6]` — 4 entries, all valid P0–P9, within the recommended 3–5 range.
- `scenario_usage_guide.quality_metrics: [P2, P5]` — valid P0–P9.
- `expected_behaviors` entries describe kinds of behavior (e.g., "match pace broadly to the surrounding flow," "maintain a consistent lateral position within the flow") rather than exact motions or numeric thresholds — no P&G Guideline N6 over-specification found.
- `related_scenarios: [perpendicular_traffic, crowd_navigation]` and `cited_in: ["167"]` are both present in `scenario.yml`, reference existing scenario directories, and are schema-valid (arrays of strings).

## Completeness

**Scenario Card Summary** (template.md: required for AUDITED):
- Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In — all present and consistent with the YAML and P&G source.

**Scenario Usage Guide** (template.md: required for AUDITED):
- Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria — all present and consistent with the YAML's `scenario_usage_guide` block.

No required fields are blank.
