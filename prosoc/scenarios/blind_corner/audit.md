# Audit: Blind Corner

- **Scenario:** `prosoc/scenarios/blind_corner/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. Missing "Scenario Card Summary" section — should-fix
- **Section/field:** `scenario.md` structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Card Summary block
- **Issue:** `scenario.md` has no `## Scenario Card Summary` section (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In). The equivalent content exists only inside the embedded YAML block, not as a human-readable summary table as the template structures it for AUDITED scenarios.
- **Recommended fix:** Add a `## Scenario Card Summary` section populated from the YAML/prose fields already present (values are all available — this is a presentation gap, not a missing-information gap).

### 2. Missing standalone "Scenario Usage Guide" prose section — should-fix
- **Section/field:** `scenario.md` structure vs. `template.md`'s "Required for AUDITED scenarios" Scenario Usage Guide section (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria as prose subsections)
- **Issue:** This content currently exists only inside `scenario_usage_guide` in the YAML block, not as the dedicated prose section template.md requires for AUDITED readiness.
- **Recommended fix:** Add a `## Scenario Usage Guide` section with `### Success Metrics`, `### Quality Metrics`, `### Ideal Outcome`, `### Failure Modes`, `### Labeling Criteria` subsections, restating the YAML content in prose form.

### 3. No "Related Scenarios" / "Cited In" callout outside Notes — suggestion
- **Section/field:** Scenario Card Summary (once added) — Related Scenarios / Cited In fields
- **Issue:** Table 3 lists no "Related Scenarios" for Blind Corner but does list `Cited In: [126, 171]`, which is captured in the Status block's SOURCE line but not surfaced as a distinct summary field. Minor, since the Status block already carries this.
- **Recommended fix:** When adding the Scenario Card Summary section (Finding 1), carry `Cited In: [126, 171]` and `Related Scenarios: (none listed)` into it explicitly.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Blind Corner" entry, cited in [126, 171]. Compared against `../../../.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | scenario.yml / scenario.md | Match? |
|---|---|---|---|
| Physical Env | Indoor | `context.environment.type: indoor` | Yes |
| Geometric Layout | Corner | `geometric_layout: corner` | Yes |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Yes |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B through the corner` | Yes |
| Human Behavior | Navigate B to A | `intended_human_behavior: navigate from B to A through the corner` | Yes |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot and human pass each other at the corner without collision or obstruction` | Yes |
| Related Scenarios | (none listed) | Not stated as a summary field, but Notes section correctly compares to Frontal Approach and Narrow Doorway without claiming a formal Table 3 relation | Consistent |
| Cited In | [126, 171] | Status block: "cited in [126, 171]" | Yes |
| Robot Role | (blank in Table 3) | `agents.robot.role: navigating_agent` | No conflict — an elaboration of an unspecified field, not a contradiction |

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

- **Scenario Card Summary fields** — should-fill-in-now. No dedicated section exists in `scenario.md`, but every underlying value (name, description, scientific purpose, physical environment, geometric layout, robot role, robot task, human behavior, ideal outcome, cited-in) is already present in prose or YAML. See Finding 1.
- **Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)** — should-fill-in-now as a prose section. All content already exists in the YAML's `scenario_usage_guide` block (SR, NoCollisions; P2, P3; failure modes list; labeling criteria list). See Finding 2.
- **Related Scenarios / Cited In** — reasonably blank as a distinct summary field for now, since Table 3 lists no related scenario and the citation is already tracked in the Status block; would be folded in when Finding 1 is addressed.
