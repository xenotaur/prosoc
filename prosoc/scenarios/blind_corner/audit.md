---
scenario: blind_corner
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-07-21
---

# Audit: Blind Corner

- **Scenario:** `prosoc/scenarios/blind_corner/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready, no issues found

## Findings

No findings. This is a fresh re-audit following the `related_scenarios`/`cited_in`
backfill: the prior audit (2026-07-20) raised one suggestion — that Related Scenarios
and Cited In were tracked only in the Status block and the doc's own "Remaining gaps"
note rather than duplicated into the Scenario Card Summary and machine-readable YAML.
That gap is now closed: `scenario.md`'s Scenario Card Summary (lines 29-30) lists
`**Related Scenarios:** frontal_approach, narrow_doorway` and `**Cited In:** 126, 171`,
and the embedded/distilled YAML carries matching `related_scenarios: [frontal_approach,
narrow_doorway]` and `cited_in: ["126", "171"]` fields. Both referenced scenarios
(`frontal_approach`, `narrow_doorway`) exist as directories under `prosoc/scenarios/`.
No new issues were introduced by the backfill.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "Blind Corner" entry, cited in [126, 171]. Compared
against `../../.claude/skills/_shared/pg_scenarios.md`:

| Field | Table 3 | scenario.yml / scenario.md | Match? |
|---|---|---|---|
| Physical Env | Indoor | `context.environment.type: indoor` | Yes |
| Geometric Layout | Corner | `geometric_layout: corner` | Yes |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Yes |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B through the corner` | Yes |
| Human Behavior | Navigate B to A | `intended_human_behavior: navigate from B to A through the corner` | Yes |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot and human pass each other at the corner without collision or obstruction` | Yes |
| Related Scenarios | (none listed) | `related_scenarios: [frontal_approach, narrow_doorway]` | Not a mismatch — Table 3 lists no related scenario for this entry, but the card's own Notes section (scenario.md lines 223-225) independently and explicitly analyzes the relationship to both Frontal Approach and Narrow Doorway; the new `related_scenarios` field formalizes an editorial cross-reference already present in the card's prose, not a claim about Table 3 content. |
| Cited In | [126, 171] | `cited_in: ["126", "171"]` | Yes |
| Robot Role | (blank in Table 3) | `agents.robot.role: navigating_agent` | No conflict — an elaboration of an unspecified field, not a contradiction |

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

Re-checked against `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose, Physical
  Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success
  Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) — present and
  populated (scenario.md lines 12-30). Related Scenarios and Cited In are now filled
  in (`frontal_approach, narrow_doorway` / `126, 171`), resolving the prior audit's
  should-fill-in-now / suggestion finding.
- **Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome, Failure
  Modes, Labeling Criteria** — all present as a dedicated `## Scenario Usage Guide`
  prose section (scenario.md lines 200-217), consistent with the embedded YAML's
  `scenario_usage_guide` block.

No blank required fields remain.

## Prose/YAML Consistency (Step 2)

No contradictions or drift found. Scenario Overview, Social Navigation Context, and
Normative Expectations align with `intended_robot_task`, `intended_human_behavior`,
`agents`, `expected_behaviors`, and `ideal_outcome`. The prose's normative
"acceptable"/"unacceptable" behavior lists map cleanly onto
`expected_behaviors.{must,should,should_not}` with no one-sided claims. The newly
added Related Scenarios / Cited In summary fields match the corresponding YAML fields
and the Status block's SOURCE line and Notes prose exactly.

## Schema and Charter Compliance (Step 3)

- `scripts/distill/scenarios --scenario blind_corner --dry-run --show-diffs` produced
  no diff and no schema validation error — `scenario.yml` is in sync with
  `scenario.md` and validates against `schema.json`.
- `relevant_principles`: P1, P2, P3, P7 — four principles, all valid P0-P9 IDs, within
  the recommended 3-5 range.
- `scenario_usage_guide.quality_metrics`: P2, P3 — valid P0-P9 IDs.
- `expected_behaviors` entries describe kinds of behavior ("reduce speed," "stop
  promptly," "yield") rather than exact motions or numeric thresholds — no
  over-specification (P&G Guideline N6) found.
- `related_scenarios` and `cited_in` entries are well-formed (scenario IDs matching
  existing directories; citation numbers as strings matching schema expectations).
