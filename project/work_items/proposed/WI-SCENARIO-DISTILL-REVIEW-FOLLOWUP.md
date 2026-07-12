---
resolution: null
blocked_reason: null
blocked: false
id: WI-SCENARIO-DISTILL-REVIEW-FOLLOWUP
title: Address deferred PR #15 review comments on scenario distiller scoping
type: deliverable
status: proposed
assigned_agents: []
related_focus: []
related_roadmap: []
related_workstreams: []
related_design: []
depends_on: []
blocked_by: []
expected_actions:
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - edit_scenario_content
  - promote_scenario_state
  - modify_schema_json
  - force_push
  - delete_branch
acceptance:
  - tests/scenarios/distill_test.py includes a test exercising `distill_all(root=..., layout="flat", scenario=<nonexistent>)` and asserting a `LiterateDiscoveryError` naming both the scenario and the root
  - "`.claude/skills/prosoc-scenario-new/SKILL.md` Step 6 runs `scripts/distill/scenarios --scenario <scenario-id>` (scoped to the scenario just drafted) instead of the unscoped whole-corpus invocation"
  - scripts/lint, scripts/test, and lrh validate report 0 errors attributable to this change
required_evidence:
  - manual_review
  - lrh_validate
  - test_output
artifacts_expected:
  - tests/scenarios/distill_test.py
  - .claude/skills/prosoc-scenario-new/SKILL.md
---

## Summary

Address two `copilot-pull-request-reviewer` comments on PR #15 (WI-SCENARIO-DISTILL-INVOCATION) that were left unresolved when that PR merged: add a `distill_all(layout="flat")` no-match test, and scope `prosoc-scenario-new/SKILL.md` Step 6 to `--scenario <id>`.

## Problem / Context

PR #15 added `--scenario <id>` filtering to `prosoc.scenarios.distill`, but two reviewer comments on it were never acted on before merge (recorded in `WI-SCENARIO-DISTILL-INVOCATION`'s `resolution:` note, `project/work_items/resolved/WI-SCENARIO-DISTILL-INVOCATION.md`):
1. `tests/scenarios/distill_test.py`'s flat-layout coverage only exercises `discover_flat_layout` directly (lines 59-81); the CLI actually routes through `distill_all`, and that entry point's flat-layout no-match path (the one users hit) is untested.
2. `prosoc-scenario-new/SKILL.md` Step 6 (lines 137-143) still runs `scripts/distill/scenarios` unscoped after drafting a single new scenario — even though `--scenario` now exists — which rewrites every `scenario.yml` in the corpus and can fail on unrelated corpus issues that have nothing to do with the scenario just drafted.

## Scope

- Add one test to `tests/scenarios/distill_test.py` covering `distill_all(layout="flat")`'s no-match path.
- Scope `prosoc-scenario-new/SKILL.md` Step 6 to `--scenario <scenario-id>`, using the scenario id already derived in that skill's Step 4.

## Required Changes

1. In `tests/scenarios/distill_test.py`, add a test to `TestDistillAllScenarioScoping` (or a new case) that creates a flat-layout scenario file, calls `distill.distill_all(root=root, layout="flat", scenario="nonexistent")`, and asserts it raises `errors.LiterateDiscoveryError` with a message containing both the scenario id and the root — mirroring the existing directory-layout test at lines 86-96.
2. In `.claude/skills/prosoc-scenario-new/SKILL.md` Step 6, change the invocation from `scripts/distill/scenarios` to `scripts/distill/scenarios --scenario <scenario-id>`, referencing the `<scenario-id>` already established in Step 4 ("Derive the scenario directory name").

## Non-Goals

- Do not re-litigate or expand `WI-SCENARIO-DISTILL-INVOCATION`'s scope — this item only closes the two specific deferred comments.
- Do not touch `prosoc-scenario-audit/SKILL.md` — its distiller invocation was already fixed and scoped in the prior work item.
- Do not modify `prosoc/scenarios/distill.py`'s behavior — `--scenario` and the flat-layout code path already exist and work; this item only adds test coverage and a doc fix.

## Acceptance Criteria

- `tests/scenarios/distill_test.py` has a passing test for `distill_all(layout="flat")`'s no-match `LiterateDiscoveryError`, naming both scenario and root.
- `prosoc-scenario-new/SKILL.md` Step 6 no longer runs an unscoped distill after drafting a single scenario.
- `scripts/lint`, `scripts/test`, and `lrh validate` report 0 errors attributable to this change (pre-existing `focus/current_focus.md` error expected and unrelated).

## Validation

- `scripts/lint`
- `scripts/test`
- `lrh validate`

## Risk Notes

- Low risk: this is additive test coverage plus a one-line doc/invocation change in an already-existing, already-tested code path (`--scenario` shipped and was validated end-to-end in WI-SCENARIO-DISTILL-INVOCATION).
