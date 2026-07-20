---
scenario: parallel_traffic
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 1
audited: 2026-07-05
---

# Audit: Parallel Traffic

- **Scenario:** `prosoc/scenarios/parallel_traffic/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Ready for AUDITED with minor fixes — content is sound and source-faithful, but two required structural sections are missing from scenario.md.

## Findings

### 1. Scenario Card Summary section missing — should-fix
- **Section/field:** scenario.md structure — "Scenario Card Summary" (template.md: "Required for AUDITED scenarios")
- **Issue:** scenario.md has no `## Scenario Card Summary` section at all. template.md requires this block (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) for any scenario reaching AUDITED. Every one of these values is already present elsewhere in the card (Scenario Overview prose, STATUS block, and the embedded YAML), so this is not missing information — it's a missing section.
- **Recommended fix:** Add a `## Scenario Card Summary` section directly after `## Status`, populated from existing content: Scenario Name "Parallel Traffic"; Description drawn from the Scenario Overview's first sentence; Scientific Purpose "crowd navigation"; Physical Environment "Generic"; Geometric Layout "Passable space"; Robot Role "navigating_agent"; Robot Task "Navigate from A to B"; Human Behavior "Mill from A to B (parallel pedestrian stream)"; Success Metrics SR / NoCollisions / TTG; Quality Metrics P2, P5; Ideal Outcome per `ideal_outcome`; Related Scenarios Circular Crossing, Perpendicular Traffic, Crowd Navigation; Cited In [167].

### 2. Scenario Usage Guide prose section missing — should-fix
- **Section/field:** scenario.md structure — "Scenario Usage Guide" (template.md: "Required for AUDITED scenarios")
- **Issue:** template.md requires a prose `## Scenario Usage Guide` section with `### Success Metrics`, `### Quality Metrics`, `### Ideal Outcome`, `### Failure Modes`, and `### Labeling Criteria` subsections, distinct from the machine-readable `scenario_usage_guide` YAML block. scenario.md only has the YAML version (embedded in the Scenario Specification section); no human-readable prose rendering of it exists in the document.
- **Recommended fix:** Add a `## Scenario Usage Guide` section (e.g., after "Normative Expectations" or after the YAML spec) that restates the YAML's `scenario_usage_guide.success_metrics`, `.quality_metrics`, `.failure_modes`, and `.labeling_criteria` as short human-readable prose under the matching subheadings, plus an `### Ideal Outcome` subsection restating `ideal_outcome` in prose. All content already exists in the YAML — this is a transcription task, not new authoring.

### 3. STATE is still DRAFTED, not yet EDITED — suggestion
- **Section/field:** Status block — STATE
- **Issue:** Per workflow.md, AUDITED review normally follows an EDITED pass. This scenario's STATUS block shows `STATE: DRAFTED` with `EDITED: —`. This isn't a defect in the scenario content, but the two missing required sections above (Findings 1 and 2) are exactly the kind of structural gaps an EDITED pass is meant to close before an AUDITED judgment is made final.
- **Recommended fix:** No content change required from this audit; noting for the human editor that closing Findings 1 and 2 effectively constitutes the EDITED pass, after which STATE can be updated to EDITED (and, following separate human review, AUDITED). This audit does not change STATE itself.

## Source Fidelity

SOURCE cites "P&G Paper, Table 3 ... cited in [167]." Compared against the canonical Table 3 "Parallel Traffic" entry in `../../../.claude/skills/_shared/pg_scenarios.md`:

| Field | P&G Table 3 | scenario.md / scenario.yml | Result |
|---|---|---|---|
| Description | Crowd moves parallel to the robot | Crowd of pedestrians moves broadly in the same direction, forming an emergent pedestrian stream | Consistent (elaborated, not contradicted) |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Passable space | `geometric_layout: passable space` | Match |
| Scientific Purpose | Crowd navigation | `scientific_purpose: crowd navigation` | Match |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B` | Match |
| Human Behavior | Mill from A to B | `intended_human_behavior: mill from A to B, forming a parallel pedestrian stream` | Match (elaborated) |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: ...without collision or obstruction` | Match |
| Related Scenarios | Circular Crossing | Notes/evaluation_notes cite Circular Crossing and also add Perpendicular Traffic, Crowd Navigation | Consistent; additional related scenarios do not contradict the source |
| Cited In | [167] | STATUS: "cited in [167]" | Match |

No mismatches found. The card is a faithful and appropriately elaborated rendering of the Table 3 entry — no fabrication or drift from the cited source.

## Completeness

**Blocking (Step 1 dry-run):** None. The single-scenario dry-run (`distill.distill_scenario(..., dry_run=True, show_diffs=True)`) produced no diff output and no schema validation error — scenario.md and scenario.yml are in sync and schema-valid.

**Scenario Card Summary fields** (template.md, required for AUDITED) — *should probably be filled in now* (see Finding 1): the whole section is absent, but every field's value is already inferable from existing prose/YAML:
- Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In — all **should-fill-in-now**.

**Scenario Usage Guide fields** (template.md, required for AUDITED) — *should probably be filled in now* (see Finding 2): the section is absent in prose form, but fully populated in the YAML:
- Success Metrics — should-fill-in-now (YAML has SR, NoCollisions, TTG).
- Quality Metrics — should-fill-in-now (YAML has P2, P5).
- Ideal Outcome — should-fill-in-now (YAML has a one-line `ideal_outcome`; needs a short prose restatement).
- Failure Modes — should-fill-in-now (YAML lists four failure modes already).
- Labeling Criteria — should-fill-in-now (YAML lists three labeling criteria already).

No fields were judged **reasonably blank** — this scenario has no gaps due to genuinely unknown or not-yet-applicable information; the only gaps are missing prose sections whose content already exists elsewhere in the document.
