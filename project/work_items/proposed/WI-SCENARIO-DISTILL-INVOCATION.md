---
resolution: null
blocked_reason: null
blocked: false
id: WI-SCENARIO-DISTILL-INVOCATION
title: Fix scenario-authoring skills' distiller invocations; add --scenario scoping
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
  - create_file
  - edit_file
  - run_tests
  - add_cli_command
  - create_pr
forbidden_actions:
  - edit_scenario_content
  - promote_scenario_state
  - modify_schema_json
  - force_push
  - delete_branch
acceptance:
  - python -m prosoc.scenarios.distill --scenario <id> --dry-run restricts discovery to exactly one scenario, for both directory and flat layouts
  - python -m prosoc.scenarios.distill --scenario <bogus-id> raises a distinct "No scenario '<id>' found" error, not the existing corpus-empty message
  - tests/scenarios/distill_test.py exists and passes, covering scoping and no-match cases
  - .claude/skills/prosoc-scenario-new/SKILL.md Step 6 references only scripts/distill/scenarios (no cd prosoc && python -m ... or python prosoc/scenarios/distill.py invocations remain)
  - .claude/skills/prosoc-scenario-audit/SKILL.md Step 1 invokes scripts/distill/scenarios --scenario <id> --dry-run --show-diffs in place of the inline python -c heredoc
  - scripts/lint, scripts/test, and lrh validate all report 0 errors attributable to this change
required_evidence:
  - manual_review
  - lrh_validate
  - test_output
artifacts_expected:
  - prosoc/scenarios/distill.py
  - tests/scenarios/distill_test.py
  - .claude/skills/prosoc-scenario-new/SKILL.md
  - .claude/skills/prosoc-scenario-audit/SKILL.md
---

## Summary

Add a `--scenario <id>` scoping flag to `prosoc/scenarios/distill.py`, and fix two scenario-authoring skills' distiller invocations: `prosoc-scenario-new`'s SKILL.md currently documents two invocations that both raise `ModuleNotFoundError`, and `prosoc-scenario-audit`'s SKILL.md hand-rolls an inline `python -c` snippet to work around the CLI's lack of single-scenario scoping.

## Problem / Context

`prosoc-scenario-new/SKILL.md` Step 6 documents `cd prosoc && python -m prosoc.scenarios.distill` and `python prosoc/scenarios/distill.py` as equivalent invocations; both fail with `ModuleNotFoundError: No module named 'prosoc'` because `prosoc` is installed editable and only resolves via `-m` from the repo root. The one invocation that works, `scripts/distill/scenarios` (a pre-existing wrapper mirroring `scripts/distill/{charter,constitutions,contexts,tasks}`), is never referenced. Separately, `prosoc-scenario-audit/SKILL.md` Step 1 needs to dry-run *one* scenario without touching the rest of the corpus — a capability `distill.py`'s CLI doesn't expose — so it embeds a `python -c` heredoc calling `distill.distill_scenario()` directly. Both skills independently hand-rolled distiller internals; this item fixes the doc bug and closes the CLI gap that caused the second skill to work around it. Full design discussion preceding this item is in-conversation only (no design doc file exists).

## Scope

- Add `--scenario <id>` filtering to `prosoc/scenarios/distill.py`'s discovery layer (both directory and flat layouts).
- Point `prosoc-scenario-new/SKILL.md` Step 6 at the existing `scripts/distill/scenarios` wrapper.
- Point `prosoc-scenario-audit/SKILL.md` Step 1 at `scripts/distill/scenarios --scenario <id> --dry-run --show-diffs`, replacing its inline Python snippet.

## Required Changes

1. In `prosoc/scenarios/distill.py`:
   - Add optional `scenario: str | None = None` param to `discover_directory_layout` (filter `child.name == scenario`) and `discover_flat_layout` (filter `md_path.stem == scenario`).
   - Thread `scenario` through `discover_scenarios()` and `distill_all()`.
   - Add `parser.add_argument("--scenario", metavar="ID", help="Restrict to a single scenario by directory/id name")` in `main()`.
   - When `--scenario` is given and no source matches, raise `LiterateDiscoveryError(f"No scenario '{scenario}' found under {root}")` — distinct message from the existing empty-corpus error.
2. Create `tests/scenarios/distill_test.py` (mirroring `tests/charter/distill_test.py`'s tempfile-fixture style), covering:
   - `--scenario` matches exactly one of several directory-layout scenarios.
   - `--scenario` with no match raises `LiterateDiscoveryError` with the new message.
   - Flat-layout stem matching.
3. In `.claude/skills/prosoc-scenario-new/SKILL.md` Step 6: replace both broken invocations with `scripts/distill/scenarios`.
4. In `.claude/skills/prosoc-scenario-audit/SKILL.md` Step 1: replace the inline `python -c` heredoc with `scripts/distill/scenarios --scenario <name> --dry-run --show-diffs`, and trim the surrounding justification prose (lines ~93–99) to reflect that scoping is now a documented flag rather than inferred from source-reading.

## Non-Goals

- Do not fix `README.md`'s stale `scripts/distill` (singular) references — separate doc-drift bug, unrelated root file, tracked as its own future item.
- Do not add a new standalone script for single-scenario distillation — extend the existing CLI instead (see design discussion for why this was rejected).
- Do not touch `prosoc/scenarios/render_sections.py` (WI-SCENARIO-SECTION-RENDERER) even though it has a similar single-scenario-selection need — that tool's CLI surface is out of scope here.
- Do not modify `schema.json`, `template.md`, or any scenario content.

## Acceptance Criteria

- `python -m prosoc.scenarios.distill --scenario <id> --dry-run` distills only that scenario (directory and flat layouts).
- `python -m prosoc.scenarios.distill --scenario <bogus-id>` fails with a message naming the missing scenario, distinct from the empty-corpus message.
- `tests/scenarios/distill_test.py` exists and passes.
- `prosoc-scenario-new/SKILL.md` Step 6 contains no invocation that raises `ModuleNotFoundError` when run from the repo root.
- `prosoc-scenario-audit/SKILL.md` Step 1 no longer contains an inline `python -c` heredoc.
- `scripts/lint`, `scripts/test`, and `lrh validate` report 0 errors attributable to this change (pre-existing `focus/current_focus.md` `lrh validate` error is expected and unrelated).

## Validation

- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/distill/scenarios --scenario <existing-id> --dry-run --show-diffs`
- `scripts/distill/scenarios --scenario nonexistent-id --dry-run`

## Risk Notes

- `discover_flat_layout`'s stem-matching path is currently untested and possibly unused in the live corpus (all scenarios appear to use directory layout) — the new test exercises it directly since it wasn't previously covered at all.
- The `--scenario` no-match error message change is additive (new message, not a change to the existing empty-corpus message), so no existing callers should observe a behavior change.
