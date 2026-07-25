---
resolution: null
blocked_reason: null
blocked: false
id: WI-CARD-STATUS-TASKS
title: Extend the card lifecycle-state contract to the tasks family (Phase 0a)
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
  - WI-CARD-STATUS-FOUNDATION
blocked_by: []
expected_actions:
  - edit_file
  - create_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - edit_task_normative_content
  - apply_to_remaining_card_families
  - implement_assembler_engine
acceptance:
  - The family-agnostic lifecycle-state helpers live in a shared module (prosoc/utils/cards/status.py) used by both the scenarios and tasks validators, with no duplication
  - scripts/validate/status validates both the scenarios and tasks families and reports all cards consistent
  - prosoc/tasks/schema.json requires a state enum, and all 4 task.yml carry a schema-valid state (DRAFTED), with no other payload change
  - lrh validate, scripts/lint, scripts/test, and scripts/validate/status all report 0 errors, and no task normative content changed
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/utils/cards/status.py
  - prosoc/scenarios/status.py
  - prosoc/scenarios/validate_status.py
  - prosoc/tasks/schema.json
  - prosoc/tasks/*/task.md
  - prosoc/tasks/*/task.yml
  - scripts/validate/status
  - tests/utils/cards/status_test.py
---

# WI-CARD-STATUS-TASKS

## Summary

Extend the machine-readable lifecycle-`state` contract established by
`WI-CARD-STATUS-FOUNDATION` to the tasks family, and generalize the shared
status tooling so a single validator covers all card families.

## Problem / Context

`WI-CARD-STATUS-FOUNDATION` (PR #40) proved the state contract on scenarios and
deliberately located its helpers in `prosoc/scenarios/`, noting they were
"structured to extend to other families." Tasks are the second of five families
(tasks, contexts, constitutions, charter remain). Rather than duplicate
scenario-specific tooling four more times, this item lifts the family-agnostic
helpers into the shared card-tooling home (`prosoc/utils/cards/`, alongside
`validator.py`) and makes the status validator family-aware, then applies the
contract to the four task cards. The lifecycle enum itself is already canonical
in `prosoc/scenarios/workflow.md` (states `DRAFTED`, `EDITED`, `AUDITED`,
`APPROVED`, `VALIDATED`, `DEPRECATED`, `RETIRED`) and is reused unchanged.

### Duplication search
- In-repo: The scenario status tooling exists and is the thing being
  generalized, not duplicated; `prosoc/utils/cards/` is the established shared
  home (it already holds `validator.py`).
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed.

### Demand search
- Work items: None found. `WI-CARD-STATUS-FOUNDATION` (resolved) is the
  predecessor this builds on, not a duplicate request.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` governs this work item.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

- Generalize the family-agnostic state helpers into
  `prosoc/utils/cards/status.py`; update the scenarios modules to consume the
  shared module (no behaviour change).
- Make the status validator family-aware (scenarios + tasks) behind
  `scripts/validate/status`.
- Apply the `state` schema field + fenced-YAML authoring to the **tasks**
  family only.

## Required Changes

1. Move the family-agnostic helpers — `STATES`, `parse_markdown_state`,
   `project_state_into_markdown`, `check_consistency`, `read_yaml_state`,
   `check_source` — from `prosoc/scenarios/status.py` to
   `prosoc/utils/cards/status.py`; keep `prosoc/scenarios/status.py` working by
   re-exporting from the shared module so existing imports and tests are
   unaffected.
2. Generalize `validate_status` to dispatch over a small family registry
   (scenarios → `discover_scenarios`/`scenario.{md,yml}`; tasks →
   `discover_tasks`/`task.{md,yml}`). `scripts/validate/status` checks all
   registered families, with an optional `--family` filter. Keep the
   bash-wrapper + `python -m` invocation pattern.
3. `prosoc/tasks/schema.json`: add a required `state` enum mirroring the
   scenario schema.
4. `prosoc/tasks/*/task.md`: add `state: DRAFTED` to each fenced YAML (all 4),
   sourced from the current STATUS-block `STATE`; regenerate each `task.yml`
   via the tasks distiller (state line only).
5. Tests: add `tests/utils/cards/status_test.py` for the shared module; extend
   the validator tests to cover the tasks family. Keep the scenario tests
   green (they are the guard that the refactor changed no behaviour).
6. Add `WI-CARD-STATUS-TASKS` to the `work_items:` list of
   `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`.

## Non-Goals

- Do not extend to contexts, constitutions, or the charter — separate
  follow-on items (near-trivial once the tooling is generic).
- Do not re-resolve the lifecycle enum — it is canonical in
  `prosoc/scenarios/workflow.md`; reuse it.
- Do not change any task's `STATE` (all stay `DRAFTED`) or normative content.
- Do not build the assembler engine, gate, or manifest.

## Acceptance Criteria

- The family-agnostic helpers live in `prosoc/utils/cards/status.py` and are
  used by both the scenarios and tasks validators, with no duplication.
- `scripts/validate/status` validates both the scenarios and tasks families and
  reports all cards consistent.
- `prosoc/tasks/schema.json` requires a `state` enum; all 4 `task.yml` carry a
  schema-valid `state` (`DRAFTED`), with no other payload change.
- `lrh validate`, `scripts/lint`, `scripts/test`, and `scripts/validate/status`
  all report 0 errors, and no task normative content changed.

## Validation

- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/validate/status`
- `scripts/distill/tasks --dry-run --show-diffs`

## Risk Notes

- The refactor touches just-landed scenarios code; the scenario validator
  behaviour must not change — the existing scenario tests are the guard, and
  `scripts/validate/status` must still report 20/20 scenarios consistent.
- Tasks use a `## STATUS` heading with trailing-whitespace line breaks; the
  `STATE` regex already tolerates both, but verify parsing on all 4 task cards.
- Keep each `task.yml` regeneration to the `state` line only — verify with
  `scripts/distill/tasks --dry-run --show-diffs` before committing.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
- Design: `project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`
