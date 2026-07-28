---
resolution: null
blocked_reason: null
blocked: false
id: WI-CARD-STATUS-CONTEXTS
title: Extend the card lifecycle-state contract to the contexts family (Phase 0a)
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
depends_on:
  - WI-CARD-STATUS-TASKS
blocked_by: []
expected_actions:
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - edit_context_normative_content
  - apply_to_remaining_card_families
  - implement_assembler_engine
acceptance:
  - The contexts family is registered in prosoc/utils/cards/validate_status.py and scripts/validate/status validates scenarios + tasks + contexts (28 cards) all consistent
  - prosoc/contexts/schema.json requires a state enum, and all 4 context.yml carry a schema-valid state (DRAFTED), with no other payload change
  - lrh validate, scripts/lint, scripts/test, and scripts/validate/status all report 0 errors, and no context normative content changed
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/utils/cards/validate_status.py
  - prosoc/contexts/schema.json
  - prosoc/contexts/*/context.md
  - prosoc/contexts/*/context.yml
  - prosoc/contexts/template.md
  - tests/utils/cards/validate_status_test.py
---

# WI-CARD-STATUS-CONTEXTS

## Summary

Extend the machine-readable lifecycle-`state` contract to the contexts family
by registering it with the now-generic status tooling and applying the `state`
field to the four context cards.

## Problem / Context

`WI-CARD-STATUS-TASKS` (PR #42) generalized the status tooling into
`prosoc/utils/cards/` with a family registry. Contexts are the third of five
families (constitutions and the charter remain). With the tooling generic, this
item is now mechanical — register the contexts family and migrate its cards.
The lifecycle enum is canonical in `prosoc/scenarios/workflow.md` and reused
unchanged.

### Duplication search
- In-repo: No context status handling yet; the generic tooling in
  `prosoc/utils/cards/` is the thing being reused, not duplicated.
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed.

### Demand search
- Work items: None found. `WI-CARD-STATUS-TASKS` (resolved) is the predecessor
  this builds on.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` governs this work item.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

- Register the `contexts` family in the shared validator.
- Apply the `state` schema field + fenced-YAML authoring to the **contexts**
  family only.

## Required Changes

1. `prosoc/utils/cards/validate_status.py`: add a `contexts` entry to
   `FAMILIES`. Because `prosoc.contexts.distill.discover_contexts` is a
   generator (it `yield`s, unlike the list-returning `discover_tasks` /
   `discover_scenarios`), wrap it: `discover=lambda root, layout:
   list(contexts_distill.discover_contexts(root))`. Set `supports_flat=False`
   and the default root to the contexts package directory.
2. `prosoc/contexts/schema.json`: add a required `state` enum mirroring the
   scenario/task schemas.
3. `prosoc/contexts/*/context.md`: add `state: DRAFTED` to each fenced YAML
   (all 4), sourced from the current STATUS-block `STATE`; regenerate each
   `context.yml` via the contexts distiller (state line only).
4. `prosoc/contexts/template.md`: add `state: DRAFTED` to the fenced-YAML
   template so new context cards satisfy the now-required field.
5. Tests: extend `tests/utils/cards/validate_status_test.py` with a
   contexts-family class (consistent + inconsistent), which also guards the
   generator-wrapping (an unwrapped generator would break the validator's
   `len()` / `not sources` logic).
6. Add `WI-CARD-STATUS-CONTEXTS` to the `work_items:` list (and the Work Items
   prose) of `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`.

## Non-Goals

- Do not extend to constitutions or the charter — separate follow-on items.
  The charter in particular is a single multi-principle document, not a
  card-per-directory family, and needs a different family adapter.
- Do not re-resolve the lifecycle enum — it is canonical in
  `prosoc/scenarios/workflow.md`; reuse it.
- Do not change any context's `STATE` (all stay `DRAFTED`) or normative
  content.
- Do not build the assembler engine, gate, or manifest.

## Acceptance Criteria

- The contexts family is registered in `prosoc/utils/cards/validate_status.py`,
  and `scripts/validate/status` validates scenarios + tasks + contexts (28
  cards) all consistent.
- `prosoc/contexts/schema.json` requires a `state` enum; all 4 `context.yml`
  carry a schema-valid `state` (`DRAFTED`), with no other payload change.
- `lrh validate`, `scripts/lint`, `scripts/test`, and `scripts/validate/status`
  all report 0 errors, and no context normative content changed.

## Validation

- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/validate/status`
- `scripts/validate/status --family contexts`
- `python -m prosoc.contexts.distill --dry-run --show-diffs`

## Risk Notes

- `discover_contexts` is a generator; registering it without `list()` breaks
  the validator's `len()` / `not sources` logic — the contexts-family test is
  the guard.
- The context STATUS block carries an extra `- **CONTEXT TYPE:**` bullet; the
  `STATE` regex is anchored to the STATE bullet only, so it is unaffected — but
  verify parsing on all 4 context cards.
- Keep each `context.yml` regeneration to the `state` line only — verify with
  `python -m prosoc.contexts.distill --dry-run --show-diffs` before committing.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
- Design: `project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`
