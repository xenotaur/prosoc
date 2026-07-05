# Audit: Perpendicular Traffic

- **Scenario:** `prosoc/scenarios/perpendicular_traffic/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. No "Scenario Card Summary" section in scenario.md — should-fix
- **Section/field:** `scenario.md` structure (between `## Status` and `## Scenario Overview`)
- **Issue:** `template.md` marks the "Scenario Card Summary" block (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) as **Required for AUDITED scenarios**, as a distinct human-readable markdown section. This scenario's YAML has all the corresponding data (`scientific_purpose`, `geometric_layout`, `intended_robot_task`, `intended_human_behavior`, `ideal_outcome`, `scenario_usage_guide.success_metrics`/`quality_metrics`), but no equivalent standalone prose summary section exists in `scenario.md` itself — a human reviewer skimming the Markdown (without reading the embedded YAML) would not see this at-a-glance summary.
- **Recommended fix:** Add a "## Scenario Card Summary" section after "## Status" and before "## Scenario Overview", populated from the already-present YAML values and the P&G Table 3 entry (see Source Fidelity below): Scenario Name "Perpendicular Traffic"; Description per `summary`; Scientific Purpose "Crowd navigation"; Physical Environment "Generic"; Geometric Layout "Intersection"; Robot Role "navigating_agent" / Any; Robot Task "Cross navigate"; Human Behavior "Mill from A to B"; Success Metrics SR/NoCollisions/TTG; Quality Metrics P3/P7; Ideal Outcome per `ideal_outcome`; Related Scenarios "Plaza Crossing, Parallel Traffic"; Cited In "[167]".

### 2. No discrete "Scenario Usage Guide" prose section in scenario.md — should-fix
- **Section/field:** `scenario.md` structure (after the YAML block, before "## Notes for Scenario Designers and Evaluators")
- **Issue:** `template.md` requires, for AUDITED scenarios, a "## Scenario Usage Guide" section with Success Metrics / Quality Metrics / Ideal Outcome / Failure Modes / Labeling Criteria as human-readable prose subsections — distinct from the same data living inside the embedded YAML's `scenario_usage_guide` key. Currently this content exists only inside the fenced YAML block; there is no corresponding Markdown section restating it for human readers.
- **Recommended fix:** Add a "## Scenario Usage Guide" section (with "### Success Metrics", "### Quality Metrics", "### Ideal Outcome", "### Failure Modes", "### Labeling Criteria" subsections) directly transcribing the already-authored `scenario_usage_guide` YAML content into prose form. This is a low-risk, mechanical addition since the underlying content is already fully specified and requires no new authoring judgment.

## Source Fidelity

SOURCE cites "P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [167]" — checked against `../../../.claude/skills/_shared/pg_scenarios.md`'s "Perpendicular Traffic" entry (under Crowd Scenarios):

| Field | P&G Table 3 | Scenario card | Match? |
|---|---|---|---|
| Description | Crowd moves perpendicular to the robot | Robot crosses while a crowd flows perpendicular to its path | Yes |
| Physical Env | Generic | `context.environment.type: generic` | Yes |
| Geometric Layout | Intersection | `geometric_layout: intersection` | Yes |
| Scientific Purpose | Crowd navigation | `scientific_purpose: crowd navigation` | Yes |
| Robot Task | Cross navigate | `intended_robot_task: cross navigate through the perpendicular flow` | Yes |
| Human Behavior | Mill from A to B | `intended_human_behavior: mill from A to B, forming a continuous perpendicular stream` | Yes |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot crosses the perpendicular flow without collision or obstruction` | Yes |
| Related Scenarios | Plaza Crossing | Discussed in `evaluation_notes` ("related to Plaza Crossing... and to Parallel Traffic") | Yes |
| Cited In | [167] | STATUS block cites "[167]" | Yes |

No mismatches found. The card is faithful to the Table 3 entry across every checkable dimension, and correctly notes in its own evaluation_notes that "Plaza Crossing" is a descriptive variant implied by [167] rather than a separately defined Table 3 entry — consistent with `pg_scenarios.md`'s own framing of Figure-7-only scenarios.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields — checked at the YAML level (all present) and the Markdown-section level (two missing, per Findings 1 and 2 above):

- **Scenario Card Summary (YAML-equivalent data)** — all present: `scientific_purpose`, `geometric_layout`, `intended_robot_task`, `intended_human_behavior`, `ideal_outcome` are populated. As a standalone Markdown section, absent (Finding 1).
- **Success Metrics** — present: `SR`, `NoCollisions`, `TTG` (all standard metric IDs per `../../../.claude/skills/_shared/principles.md`).
- **Quality Metrics** — present: `P3`, `P7`, both valid P0–P9 identifiers and a subset of `relevant_principles`.
- **Ideal Outcome** — present, both in `ideal_outcome` and restated in `scenario_usage_guide` context via `evaluation_notes`.
- **Failure Modes** — present: four concrete failure modes listed (collision, mid-crossing stop/reversal, indefinite waiting, forcing pedestrians to stop/swerve).
- **Labeling Criteria** — present: three criteria distinguishing this scenario from others (crowd with shared direction, robot's path crosses at an angle, task requires traversing rather than merging).
- **Related Scenarios / Cited In** — present in prose (`evaluation_notes` and STATUS block) though not yet in a discrete Scenario Card Summary field (Finding 1).

No fields are reasonably-blank-and-left-blank; the only gaps are the two structural/presentational ones above, both should-fill-in-now since the underlying content is already fully authored elsewhere in the card.
