---
name: prosoc-card-audit
description: >
  Audit an existing prosoc normative card — a scenario, task, context,
  constitution, the charter, or a packet manifest — for prose/YAML
  consistency, schema and charter compliance, and completeness. Use this
  skill whenever the user asks to audit, review, check, or validate a card in
  any of these six families — especially referencing the AUDITED lifecycle
  stage in workflow.md, or asking to "prep a card for review". Produces a
  findings-only audit.md next to the card (or src/prosoc/prnc/charter/audit.md
  for the charter) without modifying the card or promoting its STATE.
  Family-dispatched successor to prosoc-scenario-audit.
---

# prosoc-card-audit Skill

This skill produces an audit report for an existing prosoc normative card —
scenario, task, context, constitution, the charter, or a packet manifest —
corresponding to the
**AUDITED** lifecycle stage described in `src/prosoc/prnc/scenarios/workflow.md`. It
performs machine-assisted work that a human must review and act on: it writes
**findings for a human editor**, not fixes, and it never promotes a card's
STATE. Promotion to EDITED or AUDITED remains a human decision — this skill's
job ends at the report.

Scope is a single card per invocation. Cross-card consistency within a family,
and any dispatch across a family or the whole corpus, is
`prosoc-card-audit-all`'s job, not this skill's.

This skill supersedes the retired `prosoc-scenario-audit` (its exact logic for
the scenarios family is preserved here, family-dispatched rather than
scenario-only, per `PROP-NORMATIVE-PACKET-ASSEMBLY` Decision 7).

---

## Inputs

The user names a card — by id, directory name, or path — under one of the six
families. Optional inputs:

- **An explicit family name** (`scenarios`, `tasks`, `contexts`,
  `constitutions`, `charter`, `manifests`), if the card id alone is ambiguous
  or the user states it directly (e.g. "audit the `navigate_lead_agent` task").
- **`--paper <path>`** (scenarios only) — path to a PDF to check source
  fidelity against, if the scenario's SOURCE field points somewhere other than
  the P&G paper Table 3.
- **"the charter"** — the charter has no per-card id; naming it directly is
  sufficient.

If the family isn't stated, resolve it by checking which family directory the
named id resolves under — `src/prosoc/prnc/scenarios/<id>/`,
`src/prosoc/prnc/tasks/<id>/`, `src/prosoc/prnc/contexts/<id>/`,
`src/prosoc/constitutions/<id>/`, `src/prosoc/manifests/<id>/`,
in that order. If the id resolves under more than one family (unlikely, since
each family's ids follow different conventions — see each checklist's
Required Fields), or under none, ask the user to state the family explicitly
rather than guessing.

---

## Reference Knowledge

Load these before auditing:

1. **`../_shared/audit_checklists/<family>.md`** — the family-specific
   verification rubric. Load only the one matching the resolved family.

2. **`../_shared/principles.md`** — the P0–P9 principle definitions and
   selection guidance. Relevant to every family's principle-reference fields
   (`relevant_principles`, `related_principles`, `principle_emphasis`, or the
   charter's own principle list).

3. **`../_shared/pg_scenarios.md`** — Table 3 data for all 18 P&G scenarios.
   **Scenarios only.** Used for source-fidelity checks.

4. **`src/prosoc/prnc/<family>/schema.json`** (or `src/prosoc/<family>/schema.json`
   for constitutions/manifests) — the JSON schema the card's distilled
   YAML must conform to (see the Card YAML column in Step 1's table for the
   exact per-family filename — `scenario.yml`, `task.yml`, `context.yml`,
   `constitution.yml`, `charter.yml`, or `manifest.yml`).

5. **`src/prosoc/prnc/scenarios/workflow.md`** — defines the AUDITED stage. The audit
   report's verdict and vocabulary should speak in these terms regardless of
   family (an audit "asserts... internally coherent, aligns with the...
   Charter, reasonably captures a social navigation situation, is suitable
   for use" — it does not imply empirical validation).

6. **`src/prosoc/prnc/<family>/template.md`** (or `src/prosoc/<family>/template.md`
   for constitutions/manifests) — marks which sections/fields are
   "Required" (or, for the charter, defines its structural sections). Use
   this as the completeness checklist, alongside the family checklist's own
   Completeness section.

---

## Execution Steps

Work through these steps in order.

### 1. Locate and read the card

| Family | Card path | Card YAML |
|---|---|---|
| scenarios | `src/prosoc/prnc/scenarios/<id>/scenario.md` | `scenario.yml` |
| tasks | `src/prosoc/prnc/tasks/<id>/task.md` | `task.yml` |
| contexts | `src/prosoc/prnc/contexts/<id>/context.md` | `context.yml` |
| constitutions | `src/prosoc/constitutions/<id>/constitution.md` | `constitution.yml` |
| charter | `src/prosoc/prnc/charter/charter.md` | `charter.yml` (no id) |
| manifests | `src/prosoc/manifests/<id>/manifest.md` | `manifest.yml` |

If either file is missing, stop and report — do not proceed with a partial
audit.

Read the Markdown in full (prose sections plus the embedded fenced YAML) and
the card's distilled YAML (per Step 1's table). Confirm the two are in sync
by re-running that family's distiller in dry-run mode, from the repository
root:

```bash
scripts/distill/scenarios --scenario <id> --dry-run --show-diffs   # scenarios: scoped to this card
scripts/distill/tasks --dry-run --show-diffs                       # tasks: whole-family, no per-card scoping
scripts/distill/contexts --dry-run --show-diffs                    # contexts: whole-family, no per-card scoping
scripts/distill/constitutions --dry-run --show-diffs               # constitutions: whole-family, no per-card scoping
scripts/distill/charter --dry-run --show-diffs                     # charter: single source, inherently "scoped"
scripts/distill/manifests --dry-run --show-diffs                   # manifests: whole-family, no per-card scoping
```

**Only scenarios supports per-card scoping** (`--scenario <id>`). For tasks,
contexts, constitutions, and manifests, dry-run necessarily re-validates and
diffs the **whole family**, since their distillers have no per-card flag. Treat only the
diff lines belonging to the card under audit as part of this audit's verdict;
if the dry-run surfaces drift in a *different* card in the same family, note
it briefly as an aside for a separate audit of that card — it is out of scope
here, not something to fold into this one's findings or verdict.

**Do not** run any distiller without `--dry-run`: unscoped or not, a real run
writes the card's distilled YAML — silently violating this skill's promise
not to modify cards. Do not diff the embedded YAML block against the
distilled YAML as raw text — the distiller re-serializes YAML (strips comments, rewraps long
strings, changes flow style) even when perfectly in sync, so a literal text
diff always shows noise regardless of whether anything is actually stale. If
the dry-run reports a diff or a schema validation error for the card under
audit, flag it as **blocking** — a tooling-freshness issue, not prose/YAML
drift, so report it separately from Step 2's findings.

### 2. Prose vs. YAML consistency

Follow the resolved family checklist's **Prose/YAML Cross-Checks** table.
Flag:

- **Contradictions** — prose and YAML assert incompatible facts.
- **Drift** — merely inconsistent in emphasis or detail rather than outright
  contradictory — still worth a should-fix.
- **One-sided claims** — behavior/content described in prose but absent from
  the corresponding YAML field, or vice versa.

### 3. Schema and charter compliance

Follow the resolved family checklist's **Schema Compliance** section (each
checklist's own structural/normative-coherence checks — e.g. principle-id
validity, rule contradiction checks for constitutions, collective coherence
for the charter). If there's any doubt the YAML reflects the current
Markdown, re-run Step 1's dry-run check — do not re-derive schema validity by
hand.

### 4. Fidelity to source (scenarios only)

Scenarios' checklist has a **Source Fidelity** section; the other four
families do not (tasks/contexts/constitutions/charter have no equivalent
per-card external-source citation field). For scenarios:

- If SOURCE cites the P&G paper Table 3: compare against
  `../_shared/pg_scenarios.md`'s entry for this scenario.
- If `--paper <path>` was given, or SOURCE points elsewhere: read that source
  directly and compare against it.
- If there is no checkable source: **say so explicitly** — "Source fidelity:
  not checkable — <reason>." Never fabricate a comparison.

For every other family, omit this section from the report entirely (not "not
applicable" boilerplate — just don't include the heading).

### 5. Completeness

Follow the resolved family checklist's **Completeness** section. For each
blank required field/section, judge and state which of these it is:

- **Reasonably blank** — genuinely unknown or not yet applicable.
- **Should probably be filled in now** — inferable from prose already written
  elsewhere in the card.

### 6. Write the audit report

Output path is family-dependent: `src/prosoc/prnc/<family>/<id>/audit.md`
for scenarios/tasks/contexts, `src/prosoc/<family>/<id>/audit.md` for
constitutions/manifests, or `src/prosoc/prnc/charter/audit.md` for the
charter (no id, one document).

Start with a small structured frontmatter block — this is what lets tooling
(`prosoc-card-audit-all`) parse verdicts and counts reliably instead of
scraping prose — followed by a provenance header in the same spirit as the
card's own STATUS block, followed by the findings:

```markdown
---
family: <scenarios|tasks|contexts|constitutions|charter>
card: <id, or the literal "charter" for the charter family>
verdict: <one of: ready, ready_with_fixes, not_ready>
blocking: <count>
should_fix: <count>
suggestion: <count>
audited: <today's date, YYYY-MM-DD>
---

# Audit: <Card Name>

- **Card:** `src/prosoc/prnc/<family>/<id>/` for scenarios/tasks/contexts,
  `src/prosoc/<family>/<id>/` for constitutions/manifests (or
  `src/prosoc/prnc/charter/` for the charter)
- **Audited:** Claude (prosoc-card-audit skill), <today's date>
- **Verdict:** <one line, e.g. "Ready for AUDITED with minor fixes" |
  "Not ready — N blocking issues" | "Ready, no issues found">

## Findings

### 1. <short title> — <severity: blocking | should-fix | suggestion>
- **Section/field:** <e.g. Normative Statement vs. description>
- **Issue:** <what's wrong>
- **Recommended fix:** <what a human editor should do — not applied automatically>

<repeat per finding, most severe first>

## Source Fidelity
<Scenarios only: Step 4's result, or the explicit "not checkable — <reason>"
statement. Omit this section entirely for every other family.>

## Completeness
<Step 5's findings, each labeled reasonably-blank or should-fill-in-now.>
```

Pick the frontmatter `verdict` by holistic judgment — it is not purely derived
from the counts (e.g. a card with zero blocking findings can still warrant
`not_ready` if the should-fix findings are substantial enough that AUDITED
promotion would be premature). `blocking`, `should_fix`, and `suggestion` must
equal the number of findings actually listed at each severity below.

This file is a report for the EDITED/AUDITED review pass, not something
applied automatically. **Do not edit the card's Markdown, YAML, or the
STATUS/STATE block.** A human takes responsibility for acting on it.

### 7. Report to the user

Tell the user:

- The one-line verdict
- Counts of findings by severity
- Path to `audit.md`
- An explicit reminder that the card was not modified and promotion to
  AUDITED is a human decision

---

## Quality Checklist

Before reporting completion, verify:

- [ ] The card's Markdown, YAML, `schema.json`, `template.md`, and `distill.py`
      were not modified
- [ ] The card's STATUS/STATE block was not changed
- [ ] Every finding has a severity, a section/field, and a recommended fix
- [ ] The frontmatter's `blocking`/`should_fix`/`suggestion` counts match the
      findings actually listed
- [ ] Principle-reference fields were checked against P0–P9 only
- [ ] For scenarios: source fidelity was either checked against a real source
      or explicitly marked not checkable — never fabricated. For every other
      family: the Source Fidelity section is omitted entirely.
- [ ] Completeness covers every field the family checklist marks Required

---

## What This Skill Does Not Do

- Does not promote a card's STATE to AUDITED (human responsibility)
- Does not edit any card's Markdown, YAML, `schema.json`, `template.md`, or
  distiller
- Does not perform cross-card consistency checks within a family, or dispatch
  across multiple cards — that is `prosoc-card-audit-all`'s job
- Does not fabricate a source comparison when no checkable source exists
  (scenarios) or claim source fidelity for families that have no such field
- Does not guarantee scientific or normative correctness beyond what is
  checkable against the schema, the charter, and (for scenarios) the cited
  source
