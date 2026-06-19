---
name: new-scenario
description: >
  Draft a new prosoc social navigation scenario card from a paper or description.
  Use this skill whenever the user asks to implement, add, create, author, or draft
  a social navigation scenario — especially when they name a scenario (e.g. "blind
  corner", "entering room", "following", "crowd navigation"), reference the P&G paper,
  or provide a new paper and ask for a scenario from it. Produces a DRAFTED scenario.md
  and scenario.yml under prosoc/scenarios/<name>/. Also use when the user asks to
  "fill in" missing scenarios or "implement scenarios from the paper".
---

# new-scenario Skill

This skill drafts a new social navigation scenario card for the prosoc project, following
the project's literate-programming workflow: a human-readable `scenario.md` (with embedded
YAML) is the source of truth, from which `scenario.yml` is distilled and validated.

All output is marked **DRAFTED** — machine-generated content that requires human review
before promotion to EDITED or AUDITED. This is by design; the workflow explicitly
anticipates machine-assisted drafts.

---

## Inputs

The user will provide at minimum a scenario name. Optional inputs:

- **`--paper <path>`** — path to a PDF containing the scenario description
  (e.g. `/path/to/paper.pdf`). If omitted, assume the P&G paper (Table 3).
- **`--description "<text>"`** — a free-text description to use instead of reading a paper.

If the scenario name matches one in Table 3 of the P&G paper, the reference data in
`references/pg_scenarios.md` provides all the metadata you need and you do not need to
read a PDF.

---

## Reference Knowledge

Load these before generating the scenario card:

1. **`references/pg_scenarios.md`** — Table 3 data for all 18 P&G scenarios, plus notes
   on which are already implemented. Always read this first to check if the scenario is
   already implemented and to get canonical metadata.

2. **`references/principles.md`** — The P1–P8 principle definitions and common metric IDs.
   Read this to correctly populate `relevant_principles` and `scenario_usage_guide`.

3. **`references/schema_guide.md`** — Field-by-field guidance for the scenario schema.
   Read this to understand what goes in each YAML field and what to leave blank.

4. **`prosoc/scenarios/scenario_template.md`** — The canonical output template. Read this
   to understand the required Markdown structure and section ordering.

5. **`prosoc/scenarios/schema.json`** — The JSON schema enforced by the distiller. Refer
   to this if you are uncertain whether a field or value is valid.

---

## Execution Steps

Work through these steps in order.

### 1. Check for existing implementation

List `prosoc/scenarios/` and check whether a directory for this scenario already exists.
If it does, report this to the user and ask whether to overwrite or extend. Do not
silently overwrite existing work.

### 2. Identify the source

- If the scenario name matches a P&G Table 3 entry (see `references/pg_scenarios.md`):
  use the reference data directly. No PDF reading needed.
- If `--paper` was given: read the relevant sections of the PDF. Focus on scenario
  descriptions, tables, and figures — not the full paper. Extract the metadata fields
  listed in `references/schema_guide.md` as a structured extraction target.
- If `--description` was given: use it directly as the basis for the summary and overview.
- If none of the above: ask the user for a source before proceeding.

### 3. Extract scenario metadata

Map the source material to these fields (refer to `references/schema_guide.md`):

- scenario name, id (snake_case_01), summary
- scientific_purpose, geometric_layout
- environment type/setting/width, social setting
- robot role and capabilities, human role and count
- intended_robot_task, intended_human_behavior
- ideal_outcome
- relevant_principles (P1–P8 only — see `references/principles.md`)
- expected_behaviors (must / should / should_not)
- scenario_usage_guide (success_metrics, quality_metrics, failure_modes, labeling_criteria)
- evaluation_notes

**Leave fields blank rather than guessing.** A sparse but accurate card is better than
a complete but fabricated one.

**Avoid over-specification** (P&G Guideline N6): expected_behaviors should describe
what *kind* of behavior is expected, not prescribe exact motions. The scenario should
be broad enough to capture naturally occurring variants.

### 4. Derive the scenario directory name

Convert the scenario name to snake_case: e.g. "Blind Corner" → `blind_corner`.
The scenario id should be `<snake_case>_01`.

### 5. Write the scenario card

Create `prosoc/scenarios/<scenario-id>/scenario.md` following the structure in
`prosoc/scenarios/scenario_template.md`. The file must include:

**STATUS section** (at the top, after the title):
```markdown
## Status

- **STATE:** DRAFTED
- **SOURCE:** <paper citation or "P&G Paper, Table 3"> 
- **DRAFTED:** Claude (new-scenario skill), <today's date>
- **EDITED:** —
```

**Required sections** (in this order):
1. `# Scenario: <Name>` — title
2. `## Status` — lifecycle block (as above)
3. `## Scenario Overview` — human-readable prose description (2–4 paragraphs)
4. `## Social Navigation Context` — why this scenario is socially interesting
5. `## Normative Expectations` — prose description of acceptable/unacceptable behavior
6. `## Scenario Specification (Machine-Readable)` — the fenced YAML block
7. `## Notes for Scenario Designers and Evaluators` — variants, caveats, comparison notes

The fenced YAML block must start with ` ```yaml ` and end with ` ``` ` and contain
the complete scenario specification conforming to `prosoc/scenarios/schema.json`.

### 6. Run the distiller

After writing the file, run:

```bash
cd prosoc && python -m prosoc.scenarios.distill
```

Or equivalently from the repo root:

```bash
python prosoc/scenarios/distill.py
```

If the distiller reports a schema validation error, fix the YAML before reporting
completion. Common errors:
- `relevant_principles` contains an invalid ID (must match `^P[0-9]+$`)
- `expected_behaviors` has an unknown sub-key (only `must`, `should`, `should_not`)
- A field not in `schema.json` was added at the root level (`additionalProperties: false`)

### 7. Report to the user

Tell the user:
- What was created and where
- What STATUS it has (DRAFTED)
- Which fields were left blank and why
- What a human editor should review next (EDITED stage)
- Whether any aspects of the scenario were ambiguous or required judgment calls

---

## Quality Checklist

Before reporting completion, verify:

- [ ] The scenario directory exists and contains both `scenario.md` and `scenario.yml`
- [ ] The STATUS block is present and says DRAFTED
- [ ] The fenced YAML block is valid and passes the distiller
- [ ] `relevant_principles` contains only P1–P8 identifiers
- [ ] `expected_behaviors` is flexible, not over-specified
- [ ] The Scenario Overview is readable without the YAML
- [ ] The source is cited in the STATUS block

---

## What This Skill Does Not Do

- Does not promote scenarios to EDITED or AUDITED (human responsibility)
- Does not modify `schema.json`, the template, or the distiller
- Does not decide whether a scenario is redundant — flags it and asks
- Does not invent scenarios without a source
- Does not guarantee correctness of scientific or normative claims — that is what
  the AUDITED stage is for
