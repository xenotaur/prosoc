---
scenario: movable_obstruction
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-07-22
---

# Audit: Movable Obstruction

- **Scenario:** `prosoc/scenarios/movable_obstruction/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready, no issues found.

## Findings

No findings this pass. The should-fix carried across the 2026-07-05, 2026-07-20, and
2026-07-21 audits — the Discussion section's task/context cross-reference using
invented uppercase IDs (`NAVIGATE_POINT_TO_POINT`, `DELIVER_OBJECT`,
`ROUTINE_DELIVERY`, `GUIDANCE_DOCENT`, `HIGH_URGENCY`) not connected to any real
taxonomy — is resolved. The Discussion prose now cites the actual dot-delimited
lowercase task/context IDs (`navigate.point_to_point`, `deliver.object`,
`service.routine_delivery`, `guidance.docent`, `emergency.high_urgency`), verified
against `prosoc/tasks/*/task.yml` and `prosoc/contexts/*/context.yml`:

| Cited ID | Verified against |
|---|---|
| `navigate.point_to_point` | `prosoc/tasks/navigate_point_to_point/task.yml` |
| `deliver.object` | `prosoc/tasks/deliver_object/task.yml` |
| `service.routine_delivery` | `prosoc/contexts/routine_delivery/context.yml` |
| `guidance.docent` | `prosoc/contexts/guidance_docent/context.yml` |
| `emergency.high_urgency` | `prosoc/contexts/high_urgency/context.yml` |

All five resolve to real files with matching `id:` values. The cross-reference is
also now echoed verbatim in `evaluation_notes` ("Task/context cross-reference: ..."),
making it machine-visible rather than narrative-only in the Discussion section alone
— satisfying the prior audit's recommended fix ("move the cross-reference into
`evaluation_notes` so it is machine-visible").

### Distiller check

`scripts/distill/scenarios --scenario movable_obstruction --dry-run --show-diffs`
reports no diff and no schema validation error. `scenario.md`'s embedded YAML and
`scenario.yml` are in sync.

### Prose/YAML consistency

- Scenario Overview vs. `intended_robot_task`/`intended_human_behavior`/`context`:
  consistent — robot as `navigating_agent` deciding to yield/remove/report the
  obstruction; human as a single pedestrian approaching from the opposite end.
- Social Navigation Context vs. `agents`: consistent — one human, `role: pedestrian`,
  `count: 1`; office hallway, informal/low-crowd social setting.
- Normative Expectations (Discussion + Scenario Usage Guide prose) vs.
  `expected_behaviors.{must,should,should_not}`: consistent — no one-sided claims
  found.
- `ideal_outcome` prose matches the YAML field verbatim in both Scenario Card Summary
  and Scenario Usage Guide sections.

### Schema and charter compliance

- `scenario.yml` validates (confirmed via the dry-run distill above; no
  `additionalProperties` violations, `expected_behaviors` limited to
  `must`/`should`/`should_not`).
- `relevant_principles`: `P0, P1, P3, P5, P7, P9` — all valid P0–P9 IDs. Count is 6,
  above the 3–5 soft guideline, but the Discussion section explicitly names and
  discusses "Trade-offs between Goal Achievement (P0) and prosocial action," which is
  the documented exception in `.claude/skills/_shared/principles.md` for prose that
  explicitly discusses an included principle. Not flagged as a finding.
- `scenario_usage_guide.quality_metrics`: `P3, P7, P9` — valid P0–P9 IDs, consistent
  with the subset of `relevant_principles` the Discussion foregrounds.
- `expected_behaviors` entries describe kinds of behavior ("communicate intent
  clearly," "remove the obstruction if physically capable," "yield or wait if
  intervention is inappropriate") rather than exact motions or numeric thresholds —
  no over-specification (P&G Guideline N6) found.
- `related_scenarios: [frontal_approach, single_file_hallway]` — both are real
  directories under `prosoc/scenarios/`, and both are referenced in the card's own
  prose (Scenario Overview explicitly contrasts this scenario with *Frontal
  Approach*; Discussion frames it as an extension of *Frontal Approach*). No
  contradiction with the card's own text.

## Source Fidelity

The SOURCE field cites "Principles and Guidelines for Evaluating Social Robot
Navigation (P&G paper)" generically, without a specific table or section reference.
Per `.claude/skills/_shared/pg_scenarios.md` (line 266): "The `movable_obstruction`
scenario has no direct P&G Table 3 counterpart."

**Source fidelity: not checkable against Table 3** — the shared reference data
explicitly states this scenario has no direct P&G Table 3 counterpart, and the SOURCE
field does not cite a specific section, page, or figure of the paper that could be
checked directly instead. This is unchanged from all prior audits and is not a
defect — the scenario is explicitly framed in its own prose as an original extension
of *Frontal Approach* motivated by the paper's P7/P9 principle distinction, not a
direct restatement of a Table 3 entry.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric
  Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome** — present, consistent
  between prose and YAML.
- **Success Metrics, Quality Metrics** — present as both YAML fields and prose
  (Scenario Card Summary and Scenario Usage Guide sections agree: `SR, NoCollisions,
  ConflictResolved` / `P3, P7, P9`).
- **Related Scenarios** — present (`frontal_approach`, `single_file_hallway`).
- **Failure Modes, Labeling Criteria** — present as both YAML and prose, matching.
- **Cited In** — blank. Self-flagged in the scenario's own "Remaining gaps" note as
  should-fill-in-now; concur with that self-assessment. Not blocking for AUDITED (no
  evidence yet of external citation from another scenario's `related_scenarios`
  or `Cited In` field), but should be revisited if this scenario later gets
  referenced elsewhere in the corpus.

## Verdict Rationale

All prior should-fix findings are resolved: the task/context cross-reference now uses
real, verified IDs and is machine-visible in `evaluation_notes`. No contradictions,
drift, schema violations, or over-specification found. The one remaining gap
(`Cited In` blank) is reasonably blank per the card's own self-assessment and does not
block AUDITED. This scenario is ready for AUDITED.
