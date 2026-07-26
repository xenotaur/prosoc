---
execution_id: 2026_07_25_22_35_49_WI_CARD_STATUS_TASKS
prompt_id: PROMPT(WI-CARD-STATUS-TASKS:WI_CARD_STATUS_TASKS)[2026-07-25T22:08:39-04:00]
work_item: WI-CARD-STATUS-TASKS
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/42
commit: 3fd3f997618f14856455da22ca278a6d567b5553
created_at: 2026-07-25T22:35:49-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-STATUS-TASKS.md
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Implemented the second Phase 0a family of the normative packet assembler:
generalized the lifecycle-`state` tooling into `prosoc/utils/cards/`
(family-aware) and applied the `state` contract to the tasks family, reusing
the foundation from `WI-CARD-STATUS-FOUNDATION`. Opened as PR #42.

# Result

**Generalization (decision A, confirmed at the plan gate)** — moved the
family-agnostic helpers to `prosoc/utils/cards/status.py`; added a family-aware
CLI `prosoc/utils/cards/validate_status.py` with a family registry (scenarios:
layout + flat; tasks: directory-only). `prosoc/scenarios/status.py` and
`prosoc/scenarios/validate_status.py` are thin re-export/force-`--family`
shims, so the just-landed scenario code and its tests are unchanged.
`scripts/validate/status` now runs `python -m prosoc.utils.cards.validate_status`
and validates all families by default.

**Tasks family** — added a required `state` enum to `prosoc/tasks/schema.json`;
authored `state: DRAFTED` in each of the 4 task cards' fenced YAML (from the
STATUS-block STATE); regenerated `task.yml` (state line only, no normative
change). Added `state: DRAFTED` to `prosoc/tasks/template.md` so new task cards
satisfy the now-required field.

**Tests** — `tests/utils/cards/status_test.py` (shared helpers, uppercase-`##
STATUS` parsing, shim re-export) and `tests/utils/cards/validate_status_test.py`
(generalized CLI over scenarios + tasks, `--fix`, flat, invalid-state, guards,
real-repo smoke). Existing `tests/scenarios/*` untouched and green.

CHAIN-NOTE: cycles=1; stops=0; gates=[implement-plan, merge]; friction=validator-polish-review; note="one review round, 4 valid Copilot findings on the generalized validator (trailing-whitespace preservation in --fix, failures->stderr, --card no-match message, test fixture); fixed."

# Validation

- `scripts/format --check`: clean.
- `scripts/lint`: All checks passed.
- `scripts/test`: 127 passed (was 100; +27).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 24 cards consistent (20 scenarios + 4 tasks);
  `--family tasks` reports 4/4.
- Task `.md`/`.yml` diffs confirmed to be the `state` line only.

# Follow-up

- Remaining Phase 0a families: contexts, constitutions, charter — now
  near-trivial (register the family + add the schema `state` + migrate cards).
- The scenarios template (`prosoc/scenarios/template.md`) has the same latent
  gap this PR fixes for tasks (lacks `state` despite the required schema field,
  pre-existing from PR #40) — worth a small follow-up.
