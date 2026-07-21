---
scenario: blind_corner
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-20
---

# Audit: Blind Corner

- **Scenario:** `prosoc/scenarios/blind_corner/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready, no blocking or should-fix issues found

## Findings

### 1. Related Scenarios / Cited In not carried into Card Summary — suggestion
- **Section/field:** Scenario Card Summary — Related Scenarios / Cited In fields
- **Issue:** The rendered `## Scenario Card Summary` section (scenario.md lines 12-34) self-flags this under "Remaining gaps" as "should-fill-in-now" for both Related Scenarios and Cited In. Table 3 lists no related scenario for Blind Corner, and the citation `[126, 171]` is already present in the Status block's SOURCE line, so the information is not lost — it's just not duplicated into the summary table the template structures for this purpose.
- **Recommended fix:** Add `**Related Scenarios:** (none listed)` and `**Cited In:** [126, 171]` lines to the Scenario Card Summary block to match the template's field list and resolve the doc's own self-flagged gap.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Blind Corner" entry, cited in [126, 171]. Compared against `../../.claude/skills/_shared/pg_scenarios.md`:

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

Re-checked against `template.md`'s "Required for AUDITED scenarios" fields, following the substantial rendering pass this session (Scenario Card Summary and Scenario Usage Guide are now both present as dedicated prose sections, resolving the two should-fix findings from the 2026-07-05 audit):

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome) — present and populated (scenario.md lines 12-29).
- **Related Scenarios / Cited In** (Card Summary fields) — reasonably blank as distinct summary fields; both are genuinely known (Table 3 lists no related scenario, citation is [126, 171]) but tracked in the Status block and the doc's own "Remaining gaps" note rather than duplicated in the summary table. See Finding 1.
- **Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria** — all present as a dedicated `## Scenario Usage Guide` prose section (scenario.md lines 195-213), consistent with the embedded YAML's `scenario_usage_guide` block.

## Prose/YAML Consistency (Step 2)

No contradictions or drift found. Scenario Overview, Social Navigation Context, and Normative Expectations align with `intended_robot_task`, `intended_human_behavior`, `agents`, `expected_behaviors`, and `ideal_outcome`. The prose's normative "acceptable"/"unacceptable" behavior lists map cleanly onto `expected_behaviors.{must,should,should_not}` with no one-sided claims.

## Schema and Charter Compliance (Step 3)

- `scripts/distill/scenarios --scenario blind_corner --dry-run --show-diffs` produced no diff and no schema validation error — `scenario.yml` is in sync with `scenario.md` and validates against `schema.json`.
- `relevant_principles`: P1, P2, P3, P7 — four principles, all valid P0-P9 IDs, within the recommended 3-5 range.
- `scenario_usage_guide.quality_metrics`: P2, P3 — valid P0-P9 IDs.
- `expected_behaviors` entries describe kinds of behavior ("reduce speed," "stop promptly," "yield") rather than exact motions or numeric thresholds — no over-specification (P&G Guideline N6) found.
