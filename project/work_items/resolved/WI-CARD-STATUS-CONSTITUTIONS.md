---
resolution: Implemented and merged in PR #47 (commit 1680ea4); constitutions family now carries a machine-readable state field enforced by scripts/validate/status.
blocked_reason: null
blocked: false
id: WI-CARD-STATUS-CONSTITUTIONS
title: Extend the card lifecycle-state contract to the constitutions family (Phase 0a)
type: deliverable
status: resolved
assigned_agents: []
related_focus:
  - FOCUS-NORMATIVE-PACKET-ASSEMBLY
related_roadmap: []
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/proposed/normative-packet-assembly/00_proposal.md
depends_on:
  - WI-CARD-STATUS-CONTEXTS
blocked_by: []
expected_actions:
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - edit_constitution_normative_content
  - apply_to_charter
  - implement_assembler_engine
acceptance:
  - The shared read_yaml_state/check_source accept a root_key, and the constitutions family is registered with yaml_root_key "constitution"; scripts/validate/status validates scenarios + tasks + contexts + constitutions (30 cards) all consistent
  - Each constitution's Markdown STATUS block uses the canonical "- **STATE:**" bullet, and prosoc/constitutions/schema.json requires a state enum inside the constitution object; both constitution.yml carry a schema-valid state (EDITED), with no other payload change
  - lrh validate, scripts/lint, scripts/test, and scripts/validate/status all report 0 errors, and no constitution normative content changed
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/utils/cards/status.py
  - prosoc/utils/cards/validate_status.py
  - prosoc/constitutions/schema.json
  - prosoc/constitutions/*/constitution.md
  - prosoc/constitutions/*/constitution.yml
  - prosoc/constitutions/template.md
  - tests/utils/cards/status_test.py
  - tests/utils/cards/validate_status_test.py
---

# WI-CARD-STATUS-CONSTITUTIONS

## Summary

Extend the machine-readable lifecycle-`state` contract to the constitutions
family, which requires two small extensions to the shared tooling to handle
constitutions' root-wrapped YAML and heading-style STATUS block.

## Problem / Context

Constitutions are the fourth of five families (only the charter remains).
Unlike tasks and contexts, they diverge structurally in two ways verified in
the corpus:

1. **Root-wrapped fenced YAML** — the machine payload starts with a
   `constitution:` top key, with `id`/`name`/etc. nested under it, and
   `constitution.yml` is root-wrapped the same way. So a machine-readable
   `state` nests at `constitution.state`, not top-level — but the shared
   `read_yaml_state` reads top-level `data["state"]`.
2. **Heading-embedded state** — the STATUS block is `## STATUS: EDITED <date>`
   with no `- **STATE:**` bullet, so the shared `parse_markdown_state` (which
   matches the bullet) would fail. Both constitution cards are at `EDITED`, not
   `DRAFTED`.

This item normalizes the constitution STATUS blocks to the canonical
`- **STATE:**` bullet form (as prescribed by
`prosoc/scenarios/workflow.md`'s Status Section Template) and adds a `root_key`
parameter to the shared state helpers so the validator can read a nested
`state`. The lifecycle enum is reused unchanged.

### Duplication search
- In-repo: No constitution status handling yet; the generic tooling in
  `prosoc/utils/cards/` is being extended (root_key + a family registration),
  not duplicated.
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed.

### Demand search
- Work items: None found. `WI-CARD-STATUS-CONTEXTS` (resolved) is the
  predecessor this builds on.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` governs this work item.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

- Extend `read_yaml_state`/`check_source` with an optional `root_key`; add a
  `yaml_root_key` to the validator's `Family`.
- Normalize the 2 constitution STATUS blocks to the `- **STATE:**` bullet form.
- Apply the `state` schema field + fenced-YAML authoring (nested under
  `constitution:`) to the constitutions family.

## Required Changes

1. `prosoc/utils/cards/status.py`: give `read_yaml_state(yml_path,
   root_key=None)` and `check_source(md_path, yml_path, root_key=None)` an
   optional `root_key`; when set, read `data[root_key]["state"]` instead of
   top-level `data["state"]`. Default `None` preserves current behaviour.
2. `prosoc/utils/cards/validate_status.py`: add `yaml_root_key: str | None =
   None` to `Family`; have `_check_family` pass it to `check_source`; register
   the `constitutions` family (`discover_constitutions` — wrap in `list()` if
   it is a generator; `yaml_root_key="constitution"`, `supports_flat=False`,
   default root the constitutions package dir).
3. `prosoc/constitutions/*/constitution.md`: normalize the STATUS block from
   `## STATUS: <STATE> <date>` to `## STATUS` + a `- **STATE:** <STATE>` first
   bullet (keep the existing provenance bullets; the heading date is already in
   the `EDITED` provenance bullet). Add `state: <STATE>` under `constitution:`
   in the fenced YAML, sourced from the card's actual state. Regenerate each
   `constitution.yml` (state field only).
4. `prosoc/constitutions/schema.json`: add a required `state` enum inside the
   `constitution` object (mirror the enum used by the other families).
5. `prosoc/constitutions/template.md`: normalize its STATUS block to the bullet
   form and add `state` under `constitution:` in the fenced YAML.
6. Tests: add a `read_yaml_state` `root_key` case to
   `tests/utils/cards/status_test.py`; add a constitutions-family class to
   `tests/utils/cards/validate_status_test.py` (consistent + inconsistent,
   exercising `yaml_root_key`).
7. Add `WI-CARD-STATUS-CONSTITUTIONS` to the `work_items:` list (and the Work
   Items prose) of
   `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`.

## Non-Goals

- Do not extend to the charter — it is the last and structurally most
  different family (a single multi-principle document, not a card-per-directory
  family); it gets its own work item.
- Do not re-resolve the lifecycle enum — it is canonical in
  `prosoc/scenarios/workflow.md`; reuse it.
- Do not change any constitution's `STATE` value (both stay `EDITED`) or its
  normative rules/payload.
- Do not build the assembler engine, gate, or manifest.

## Acceptance Criteria

- The shared `read_yaml_state`/`check_source` accept a `root_key`, and the
  constitutions family is registered with `yaml_root_key="constitution"`;
  `scripts/validate/status` validates scenarios + tasks + contexts +
  constitutions (30 cards) all consistent.
- Each constitution's Markdown STATUS block uses the canonical `- **STATE:**`
  bullet, and `prosoc/constitutions/schema.json` requires a `state` enum inside
  the `constitution` object; both `constitution.yml` carry a schema-valid
  `state` (`EDITED`), with no other payload change.
- `lrh validate`, `scripts/lint`, `scripts/test`, and `scripts/validate/status`
  all report 0 errors, and no constitution normative content changed.

## Validation

- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/validate/status`
- `scripts/validate/status --family constitutions`
- `python -m prosoc.constitutions.distill --dry-run --show-diffs`

## Risk Notes

- The `root_key` change touches shared helpers used by every family; the
  existing scenario/task/context tests are the guard that top-level
  (`root_key=None`) behaviour is unchanged.
- Normalizing the STATUS heading is a STATUS-block reformat only — the
  constitution rules/payload must not change; verify each `constitution.md`
  diff is limited to the STATUS block plus the fenced-YAML `state` line.
- Constitutions are `EDITED`, not `DRAFTED` — the migration must source the
  actual state from each card, not hardcode `DRAFTED`.
- Verify whether `discover_constitutions` is a generator (like
  `discover_contexts`) and wrap it in `list()` if so.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
- Design: `project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`
