---
name: prosoc-scenario-audit
description: >
  Audit an existing prosoc social navigation scenario for prose/YAML consistency,
  schema and charter compliance, source fidelity, and completeness. Use this skill
  whenever the user asks to audit, review, check, or validate a scenario card —
  especially referencing the AUDITED lifecycle stage in workflow.md, or asking to
  "prep a scenario for review" or "check a scenario against the P&G paper". Produces
  an audit.md findings report in prosoc/scenarios/<name>/ without modifying the
  scenario or promoting its STATE.
---

# prosoc-scenario-audit Skill

This skill produces an audit report for an existing prosoc social navigation scenario
card, corresponding to the **AUDITED** lifecycle stage described in
`prosoc/scenarios/workflow.md`. Like `prosoc-scenario-new`, it performs machine-assisted
work that a human must review and act on: it writes **findings for a human editor**,
not fixes, and it never promotes a scenario's STATE. Promotion to EDITED or AUDITED
remains a human decision — this skill's job ends at the report.

Scope is a single scenario per invocation. Cross-scenario consistency (duplicate
principle-selection patterns, naming drift across the corpus) is a separate, larger
problem and out of scope here.

---

## Inputs

The user will provide at minimum a scenario name or path under `prosoc/scenarios/`.
Optional inputs:

- **`--paper <path>`** — path to a PDF to check source fidelity against, if the
  scenario's SOURCE field points somewhere other than the P&G paper Table 3, or if
  the user wants to check against a specific paper/section directly.

---

## Reference Knowledge

Load these before auditing:

1. **`../_shared/pg_scenarios.md`** — Table 3 data for all 18 P&G scenarios. Shared
   with `prosoc-scenario-new`; do not fork a local copy. Use this to check source
   fidelity whenever SOURCE cites the P&G paper.

2. **`../_shared/principles.md`** — The P1–P8 principle definitions and selection
   guidance. Shared with `prosoc-scenario-new`; do not fork a local copy. Use this to
   validate `relevant_principles` usage.

3. **`references/audit_checklist.md`** — Field-by-field verification rubric derived
   from schema.json and template.md, organized for checking rather than authoring.

4. **`prosoc/scenarios/schema.json`** — The JSON schema the distilled `scenario.yml`
   must conform to.

5. **`prosoc/scenarios/workflow.md`** — Defines the AUDITED stage. The audit report's
   verdict and vocabulary should speak in these terms (an audit "asserts... internally
   coherent, aligns with the... Charter, reasonably captures a social navigation
   situation, is suitable for use" — it does not imply empirical validation).

6. **`prosoc/scenarios/template.md`** — Marks which sections/fields are
   "Required for AUDITED scenarios." Use this as the completeness checklist.

---

## Execution Steps

Work through these steps in order.

### 1. Locate and read the scenario

Find `prosoc/scenarios/<name>/scenario.md` and `scenario.yml`. If either is missing,
stop and report — do not proceed with a partial audit.

Read `scenario.md` in full (prose sections plus the embedded YAML block) and the
distilled `scenario.yml`. Confirm the two are in sync by **re-running the distiller**
(`python prosoc/scenarios/distill.py`) and checking it exits cleanly with no diff to
the committed `scenario.yml` — do not diff the embedded YAML block against
`scenario.yml` textually, since the distiller re-serializes YAML (strips comments,
rewraps long strings, changes flow style) even when perfectly in sync, which makes a
literal text diff always show noise. If re-running the distiller produces a real
(post-re-run) diff or a validation error, flag it as **blocking** — it is a
tooling-freshness issue, not prose/YAML drift, so report it separately from Step 2's
findings.

### 2. Prose vs. YAML consistency

Compare the **Scenario Overview**, **Social Navigation Context**, and **Normative
Expectations** prose sections against the embedded YAML's `intended_robot_task`,
`intended_human_behavior`, `agents` (roles, counts), `expected_behaviors`, and
`ideal_outcome`. Flag:

- **Contradictions** — e.g. prose describes the robot as a follower while YAML says
  `role: leader`.
- **Drift** — e.g. prose describes a small group of pedestrians while YAML has
  `humans: [{count: 1}]`.
- **One-sided claims** — behavior described in prose but absent from
  `expected_behaviors`, or vice versa.

### 3. Schema and charter compliance

- Validate `scenario.yml` against `prosoc/scenarios/schema.json` (re-run
  `python prosoc/scenarios/distill.py` if there's any doubt it reflects the current
  `scenario.md`).
- Check `relevant_principles` (and `scenario_usage_guide.quality_metrics`) contain
  only `P1`–`P8` per `../_shared/principles.md`. Flag 0 principles (probably
  under-specified) or all 8 (dilutes meaning per `../_shared/principles.md`'s
  guidance to limit to 3–5 most relevant).
- Check `expected_behaviors` for **over-specification** (P&G Guideline N6): flag
  entries that prescribe exact motions or numeric thresholds rather than describing
  a *kind* of behavior.

### 4. Fidelity to source

- If the scenario's **SOURCE** field cites the P&G paper Table 3: look up the matching
  entry in `../_shared/pg_scenarios.md` and compare physical description, scientific
  purpose, geometric layout, robot/human roles, task, and ideal outcome. Flag mismatches.
- If `--paper <path>` was given, or SOURCE points elsewhere (a different paper, a
  dataset, a prior scenario): read the relevant section of that source directly and
  compare against it instead.
- If there is no checkable source (SOURCE is blank, unverifiable, or informal, e.g.
  "Prompt to ChatGPT 5.2" with no retrievable content): **say so explicitly** in the
  report — "Source fidelity: not checkable — <reason>." Do not fabricate a comparison.

### 5. Completeness

Walk the fields `template.md` marks "Required for AUDITED scenarios" (the Scenario
Card Summary block; the Scenario Usage Guide's Success Metrics, Quality Metrics, Ideal
Outcome, Failure Modes, and Labeling Criteria). For each blank field, judge and state
which of these it is:

- **Reasonably blank** — the information is genuinely unknown or not yet applicable
  (e.g. "Related Scenarios" when none exist yet).
- **Should probably be filled in now** — the content is readily inferable from prose
  already written elsewhere in the card (e.g. Failure Modes left blank when several
  are already implied by the Normative Expectations section).

### 6. Write the audit report

Create `prosoc/scenarios/<name>/audit.md`. Give it a short provenance header in the
same spirit as the scenario's own STATUS block, followed by the findings:

```markdown
# Audit: <Scenario Name>

- **Scenario:** `prosoc/scenarios/<id>/`
- **Audited:** Claude (prosoc-scenario-audit skill), <today's date>
- **Verdict:** <one line, e.g. "Ready for AUDITED with minor fixes" |
  "Not ready — N blocking issues" | "Ready, no issues found">

## Findings

### 1. <short title> — <severity: blocking | should-fix | suggestion>
- **Section/field:** <e.g. Normative Expectations vs. expected_behaviors.must>
- **Issue:** <what's wrong>
- **Recommended fix:** <what a human editor should do — not applied automatically>

<repeat per finding, most severe first>

## Source Fidelity
<Result of Step 4, or the explicit "not checkable — <reason>" statement.>

## Completeness
<Blank fields from Step 5, each labeled reasonably-blank or should-fill-in-now.>
```

This file is a report for the EDITED/AUDITED review pass, not something applied
automatically. **Do not edit `scenario.md`, `scenario.yml`, or the STATUS/STATE
block.** A human takes responsibility for acting on it.

### 7. Report to the user

Tell the user:

- The one-line verdict
- Counts of findings by severity
- Path to `audit.md`
- An explicit reminder that scenario files were not modified and promotion to
  AUDITED is a human decision

---

## Quality Checklist

Before reporting completion, verify:

- [ ] `scenario.md`, `scenario.yml`, `schema.json`, `template.md`, and `distill.py`
      were not modified
- [ ] The scenario's STATUS/STATE block was not changed
- [ ] Every finding has a severity, a section/field, and a recommended fix
- [ ] `relevant_principles` was checked against P1–P8 only
- [ ] Source fidelity was either checked against a real source or explicitly marked
      not checkable — never fabricated
- [ ] Completeness covers every field `template.md` marks "Required for AUDITED
      scenarios"

---

## What This Skill Does Not Do

- Does not promote a scenario's STATE to AUDITED (human responsibility)
- Does not edit `scenario.md`, `scenario.yml`, `schema.json`, `template.md`, or
  the distiller
- Does not perform cross-scenario consistency checks across `prosoc/scenarios/`
  (a separate, corpus-level problem)
- Does not fabricate a source comparison when no checkable source exists
- Does not guarantee scientific or normative correctness beyond what is checkable
  against the schema, the charter, and the cited source
