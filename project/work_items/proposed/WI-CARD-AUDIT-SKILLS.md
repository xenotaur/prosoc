---
resolution: null
blocked_reason: null
blocked: false
id: WI-CARD-AUDIT-SKILLS
title: Family-dispatched card audit skills — prosoc-card-audit and prosoc-card-audit-all (Phase 0b)
type: deliverable
status: proposed
assigned_agents: []
related_focus:
  - FOCUS-NORMATIVE-PACKET-ASSEMBLY
related_roadmap: []
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/proposed/normative-packet-assembly/00_proposal.md
depends_on: []
blocked_by: []
expected_actions:
  - create_file
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - promote_card_state
  - edit_card_normative_content
  - implement_manifest_card_family
  - implement_ci_drift_check
acceptance:
  - prosoc-card-audit and prosoc-card-audit-all exist and dispatch correctly across all five card families (scenarios, tasks, contexts, constitutions, charter) via per-family checklists under .claude/skills/_shared/audit_checklists/
  - The charter gets a bespoke audit shape (single multi-principle document, not card-per-directory) and constitutions get a genuinely new checklist (no prior audit.md precedent)
  - Running the audit against a real card in each family produces a findings-only audit.md, with the card and its STATE left untouched
  - prosoc-scenario-audit and prosoc-scenario-audit-all are retired with no duplicate skill surface for scenarios
required_evidence:
  - manual_review
artifacts_expected:
  - .claude/skills/_shared/audit_checklists/scenarios.md
  - .claude/skills/_shared/audit_checklists/tasks.md
  - .claude/skills/_shared/audit_checklists/contexts.md
  - .claude/skills/_shared/audit_checklists/constitutions.md
  - .claude/skills/_shared/audit_checklists/charter.md
  - .claude/skills/prosoc-card-audit/SKILL.md
  - .claude/skills/prosoc-card-audit-all/SKILL.md
---

# WI-CARD-AUDIT-SKILLS

## Summary

Build the family-dispatched audit skills settled in `PROP-NORMATIVE-PACKET-ASSEMBLY`
Decision 7: one `prosoc-card-audit` skill (single card, any family) and one
`prosoc-card-audit-all` skill (fan-out across a family or the whole corpus),
backed by per-family checklists under `.claude/skills/_shared/audit_checklists/`.
This is Phase 0b — the corpus's path from `DRAFTED` toward `AUDITED`/`APPROVED`,
which is what lets the Phase 1 assembler emit production packets without
`--allow-unapproved`.

## Problem / Context

Today only the scenarios family has audit tooling
(`prosoc-scenario-audit` / `prosoc-scenario-audit-all`), corresponding to the
`AUDITED` lifecycle stage in `prosoc/scenarios/workflow.md` §4: "an automated
audit... has examined the [card] and recorded its findings" — a
machine-assisted readiness *check* that never promotes STATE and does not by
itself constitute human approval (that is `APPROVED`, a separate, later,
human-only stage). Tasks, contexts, constitutions, and the charter have no
audit skill at all.

Decision 7 in the governing proposal considered two shapes: (a) four separate
per-family audit skills, or (b) one family-dispatched `prosoc-card-audit` (+
`-audit-all`), with per-family checklists in `_shared/` and the shared audit
protocol living in the skill body. **(b) was chosen** specifically to avoid
duplicating "the same thing" five times over — which means this WI's scope
includes retiring the scenario-specific skills into the new dispatch, not
just adding four more.

Two wrinkles the proposal calls out explicitly:

- **The charter is not a card-per-directory family** — it is ten principles in
  one document (`prosoc/charter/charter.md`), so its audit shape and output
  location (`prosoc/charter/audit.md`, not per-principle files) are genuinely
  different from the other four families.
- **Constitutions have no audit precedent** — unlike scenarios (which has a
  working `audit_checklist.md` to generalize from), the constitutions checklist
  is new work, not a migration.

### Duplication search
- In-repo: `prosoc-scenario-audit` and `prosoc-scenario-audit-all` exist and
  work well for scenarios; their checklist format
  (`.claude/skills/prosoc-scenario-audit/references/audit_checklist.md` — a
  schema/template-derived verification rubric) and non-modifying,
  non-promoting contract are the patterns to generalize, not duplicate. No
  audit tooling exists for the other four families.
- Sibling repos: None identified.
- External libraries: Not applicable — this is Claude Code skill authoring.
- Recommendation: Proceed, generalizing rather than duplicating the existing
  scenario skills (per Decision 7's rationale).

### Demand search
- Work items: None found. `WI-CARD-STATUS-CHARTER` (resolved) completed Phase
  0a; `WI-PACKET-ASSEMBLER-ENGINE` (resolved) completed Phase 1. This is the
  first Phase 0b work item.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` (Decision 7) governs this item.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

New/changed skill files under `.claude/skills/`, per Decision 7's chosen
shape. No changes to `prosoc/` Python code, schemas, or distillers — this is
skill authoring against the corpus and contract that already exist.

## Required Changes

1. **`.claude/skills/_shared/audit_checklists/scenarios.md`** — migrate the
   existing `prosoc-scenario-audit/references/audit_checklist.md` here
   unchanged in substance (same schema/template-derived rubric), so it is
   shared the same way `_shared/pg_scenarios.md` and `_shared/principles.md`
   already are.
2. **`.claude/skills/_shared/audit_checklists/tasks.md`** and
   **`contexts.md`** — new rubrics derived from each family's `schema.json`
   and `template.md`, following the scenarios checklist's structure (required
   fields, prose/YAML cross-checks, schema/charter compliance).
3. **`.claude/skills/_shared/audit_checklists/constitutions.md`** — new; no
   prior `audit.md` precedent to migrate from. Must account for the
   root-wrapped `constitution:` YAML shape and the rules/`conflict_resolution`
   structure.
4. **`.claude/skills/_shared/audit_checklists/charter.md`** — new and
   structurally distinct: audits the single document's ten principles
   collectively (coverage, internal consistency, schema compliance against
   `prosoc/charter/schema.json`), not a per-card rubric.
5. **`.claude/skills/prosoc-card-audit/SKILL.md`** — family-dispatched single-
   card audit. Given a family (and a card id, except for the single-source
   charter), loads the matching checklist plus any family-specific shared
   reference data, and writes a findings-only `audit.md` into the card's
   directory (or `prosoc/charter/audit.md` for the charter). Preserves the
   existing contract exactly: never edits the card, never promotes `STATE`.
6. **`.claude/skills/prosoc-card-audit-all/SKILL.md`** — fans out
   `prosoc-card-audit` across one family, several families, or the whole
   corpus; aggregates into a corpus-level `AUDIT_SUMMARY.md`; takes the git
   actions (branch, commit, PR) itself, mirroring the existing
   `prosoc-scenario-audit-all`'s responsibility split.
7. **Retire `.claude/skills/prosoc-scenario-audit/`  and
   `prosoc-scenario-audit-all/`** — remove them once their logic and
   references are folded into the new dispatch skills; update any doc
   references (e.g. `prosoc/scenarios/workflow.md`'s mention of
   `/prosoc-scenario-audit`) to point at `/prosoc-card-audit`.

## Non-Goals

- Does not advance any card's `state` to `AUDITED` or `APPROVED` — the audit
  skills remain findings-only; promotion stays a separate human/tooling
  decision made by editing the card directly.
- Does not build per-family *authoring* skills (a `prosoc-scenario-new`
  equivalent for tasks, contexts, constitutions, or the charter).
- Does not touch the Phase 1 assembler engine, `prosoc/packet/`, or any
  family's `schema.json` / `distill.py`.
- Does not implement the manifest card family (Phase 2) or the CI drift check
  (Phase 3).
- Does not change any card's normative content.

## Acceptance Criteria

- `prosoc-card-audit` and `prosoc-card-audit-all` exist and dispatch correctly
  across all five card families via per-family checklists under
  `.claude/skills/_shared/audit_checklists/`.
- The charter gets a bespoke audit shape (single multi-principle document, not
  card-per-directory) and constitutions get a genuinely new checklist (no
  prior `audit.md` precedent).
- Running the audit against a real card in each family produces a
  findings-only `audit.md`, with the card and its `STATE` left untouched.
- `prosoc-scenario-audit` and `prosoc-scenario-audit-all` are retired with no
  duplicate skill surface for scenarios.

## Validation

- Manually invoke `prosoc-card-audit` against one real card per family
  (scenarios, tasks, contexts, constitutions, charter) and confirm each
  produces a findings-only `audit.md` with no card/STATE mutation.
- Manually invoke `prosoc-card-audit-all` scoped to a single family and
  confirm it aggregates correctly and takes git actions (branch/commit/PR)
  without touching card content.
- Confirm no leftover references to `/prosoc-scenario-audit` or
  `/prosoc-scenario-audit-all` remain in repo docs.
- `lrh validate`

## Risk Notes

- Retiring the scenario-specific skills is a deletion, not just an addition —
  verify nothing else in the repo (docs, other skills) still names them before
  removing.
- The charter's single-document audit shape is the one place this WI departs
  from the "per-card `audit.md`" pattern; keep that departure explicit in the
  new skill rather than forcing a card-per-directory shape onto it.
- Constitutions' checklist is new work with no existing rubric to check
  against; ground it directly in `prosoc/constitutions/schema.json` and
  `template.md` rather than assuming scenario conventions transfer.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
  (Phase 0b).
- Design: `project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`
  (Decision 7).
