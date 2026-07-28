---
execution_id: 2026_07_28_03_06_27_WI_CARD_STATUS_CONTEXTS
prompt_id: PROMPT(WI-CARD-STATUS-CONTEXTS:WI_CARD_STATUS_CONTEXTS)[2026-07-28T02:39:26-04:00]
work_item: WI-CARD-STATUS-CONTEXTS
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/45
commit: 
created_at: 2026-07-28T03:06:27-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-STATUS-CONTEXTS.md
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Implemented the third Phase 0a family: registered the contexts family with the
generic status tooling (from WI-CARD-STATUS-TASKS) and applied the `state`
contract to the four context cards. Opened as PR #45.

# Result

- `prosoc/utils/cards/validate_status.py`: added a `contexts` entry to
  `FAMILIES`. `discover_contexts` is a generator, so it is wrapped in `list()`
  (unlike the list-returning tasks/scenarios discoverers) to keep the caller's
  `len()`/`not sources` logic working.
- `prosoc/contexts/schema.json`: added a required `state` enum.
- `prosoc/contexts/*/context.md`: added `state: DRAFTED` to each fenced YAML
  (all 4), from the STATUS-block `STATE`; regenerated `context.yml` via
  `scripts/distill/contexts` (state line only, no normative change — verified
  the `.md`/`.yml` diffs are the `state` line only).
- `prosoc/contexts/template.md`: added `state: DRAFTED`.
- `tests/utils/cards/validate_status_test.py`: added a contexts-family class
  (consistent / inconsistent / flat-unsupported), which also guards the
  generator-wrapping.

Toolchain note: the CI `Black formatting check` pins `black==25.12.0`, while the
local environment had `black 26.3.1`, whose different formatting made
`scripts/format --check` report ~20 pre-existing files as "would reformat" — a
version-skew false alarm. Installed `black==25.12.0` (the CI pin) and confirmed
`black --check prosoc tests` is clean; the local 26.3.1 drift is not real.

# Validation

- `scripts/format --check` (black 25.12.0, the CI pin): clean (53 files
  unchanged).
- `scripts/lint`: All checks passed.
- `scripts/test`: 132 passed (+3 contexts-family tests).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 28 cards consistent (20 scenarios + 4 tasks +
  4 contexts); `--family contexts` reports 4/4.

# Follow-up

- Remaining Phase 0a families: constitutions, then the charter. Constitutions
  follow the same pattern (register family + schema `state` + migrate cards).
  The charter is a single multi-principle document, not a card-per-directory
  family, so it needs a different family adapter.
