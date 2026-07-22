# Prosoc Scenario Audit Checklist

This is a verification rubric, companion to `prosoc/scenarios/schema.json` and
`prosoc/scenarios/template.md`. Where `prosoc-scenario-new`'s `schema_guide.md`
explains what to put in each field when authoring, this file explains what to check
when auditing an already-drafted card. Read `../../_shared/principles.md` for the
P0–P9 definitions referenced below.

## Required Fields (schema.json)

| Field | Check |
|-------|-------|
| `id` | Matches `<snake_case>_01` convention, matches the directory name |
| `name` | Matches the scenario's title heading in `scenario.md` |
| `summary` | Stands alone without the surrounding prose; not a restatement of the title |

## Prose/YAML Cross-Checks

| Prose section | Cross-check against YAML field(s) |
|---|---|
| Scenario Overview | `intended_robot_task`, `intended_human_behavior`, `context` |
| Social Navigation Context | `agents`, `context.social_setting` |
| Normative Expectations | `expected_behaviors.{must,should,should_not}` |
| (implicit throughout) | `ideal_outcome` — does the prose's described "good ending" match? |

Flag a **contradiction** when prose and YAML assert incompatible facts (e.g. different
robot role, different human count). Flag **drift** when they're merely inconsistent in
emphasis or detail rather than outright contradictory — still worth a should-fix.

## Schema / Charter Compliance

- [ ] `scenario.yml` validates against `schema.json` (no `additionalProperties`
      violations; `expected_behaviors` only has `must`/`should`/`should_not`)
- [ ] `relevant_principles` — every entry matches `^P[0-9]+$` and is P0–P9
- [ ] `relevant_principles` count is roughly 3–5 (0 is likely under-specified; 10 dilutes
      meaning per `../../_shared/principles.md`) — but a count above 5 is not itself a
      finding if the card's own prose explicitly discusses each included principle; check
      before flagging as a suggestion
- [ ] `scenario_usage_guide.quality_metrics` — same P0–P9 constraint
- [ ] `expected_behaviors` entries describe a *kind* of behavior, not an exact motion,
      numeric threshold, or implementation detail (P&G Guideline N6 — over-specification)
- [ ] `related_scenarios` — must reference scenario **directory names** (the key used
      by `audit.md` frontmatter and `AUDIT_SUMMARY.md` rows), not the versioned
      `scenario.yml` `id` field and not a P&G Table 3 citation string. It commonly
      diverges from what P&G Table 3 itself lists as the scenario's "Related
      Scenarios" entry — that divergence is **expected, not a defect**, in three
      recognized cases (see `../../_shared/pg_scenarios.md` for Table 3 values):
      - Table 3 names a scenario with no implemented directory yet (the most common
        case — most of Table 3's own "Related Scenarios" values point at a Figure-7
        or sibling scenario this corpus hasn't drafted), and the card substitutes an
        implemented scenario it actually discusses in its own prose instead.
      - Table 3's named scenario *is* implemented and *is* included, but the card
        adds further scenarios beyond it — Table 3's field is a single citation, not
        an exhaustive list, so extra editorially-relevant cross-references are fine.
      - Table 3 lists no related scenario at all, but the card adds one anyway based
        on its own prose/Notes analysis — again fine, since Table 3's silence isn't a
        claim that no relationship exists.
      Do not flag any of these as a should-fix "source-fidelity mismatch." Only flag
      `related_scenarios` if it references a directory that doesn't exist under
      `prosoc/scenarios/`, or if it clearly contradicts the card's own prose.

## Source Fidelity (only if a checkable source exists)

- If SOURCE cites P&G Table 3: compare against `../../_shared/pg_scenarios.md`'s entry
  for this scenario — physical description, scientific purpose, geometric layout,
  robot/human roles, task, ideal outcome.
- If SOURCE cites something else (a paper section, dataset, prior scenario) or
  `--paper` was given: read that source directly.
- If SOURCE is blank or unverifiable (e.g. an informal prompt with no retrievable
  content): state plainly that fidelity is not checkable. Never infer a verdict from
  an unavailable source.

## Completeness (required for AUDITED per template.md)

- [ ] Scenario Card Summary fields (Scenario Name, Description, Scientific Purpose,
      Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior,
      Ideal Outcome; Success/Quality Metrics and Related Scenarios/Cited In if applicable)
- [ ] Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome,
      Failure Modes, Labeling Criteria

For each blank, decide: reasonably blank (genuinely unknown/not yet applicable) vs.
should probably be filled in now (inferable from prose already present elsewhere in
the card).
