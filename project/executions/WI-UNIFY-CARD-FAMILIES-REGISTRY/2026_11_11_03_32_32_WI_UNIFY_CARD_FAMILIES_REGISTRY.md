---
execution_id: 2026_11_11_03_32_32_WI_UNIFY_CARD_FAMILIES_REGISTRY
prompt_id: PROMPT(WI-UNIFY-CARD-FAMILIES-REGISTRY:WI_UNIFY_CARD_FAMILIES_REGISTRY)[2026-11-11T03:22:58+00:00]
work_item: WI-UNIFY-CARD-FAMILIES-REGISTRY
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/144
commit:
created_at: 2026-11-11T03:32:32+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-UNIFY-CARD-FAMILIES-REGISTRY.md
session_transcript: claude-app:0a4099db-6380-4f7b-86e5-f652e0c70455
---

# Summary

Implement `WI-UNIFY-CARD-FAMILIES-REGISTRY`: extract the shared
card-family identity (name, root directory, `yaml_root_key`,
single-document flag) that `src/prosoc/nca/packet/loader.py` and
`src/prosoc/nca/utils/cards/validate_status.py` each independently
hardcoded, into one shared module.

# Result

- Created `src/prosoc/nca/utils/cards/family_registry.py`: a
  `CardFamilyIdentity` frozen dataclass (`name`, `root`, `yaml_root_key`,
  `single`) and a `CARD_FAMILIES` dict for the five shared families.
- `src/prosoc/nca/packet/loader.py`: `_family()`/`FAMILIES` now build
  `PacketFamily` from `CARD_FAMILIES` plus the loader-specific
  `card_filename`; removed the now-redundant direct `*_distill` imports
  (confirmed unused elsewhere in the file).
- `src/prosoc/nca/utils/cards/validate_status.py`: a new `_family()`
  helper builds each `Family`'s shared fields
  (`name`/`default_root`/`yaml_root_key`/`label_by_stem`) from
  `CARD_FAMILIES`, keeping `supports_flat`/`discover` consumer-specific.
  The `manifests` entry (validate_status-only) is untouched, per the
  work item's Non-Goals.
- `PacketFamily` and `Family`'s dataclass shapes are unchanged — both
  have existing tests calling `dataclasses.replace(...)` on their
  current fields, and `review_queue.py` imports `FAMILIES, Family`
  directly from `validate_status`; neither was touched.
- PR: https://github.com/xenotaur/prosoc/pull/144

# Validation

- `scripts/validate/status` and `scripts/assemble
  src/prosoc/manifests/sample_packet/manifest.yml` — captured before and
  after the refactor; `diff` confirmed byte-identical output both times.
- `PYTHONPATH="$(pwd)/src" scripts/test` — 394 tests, `OK (skipped=1)`,
  no new failures (including the `dataclasses.replace(...)` tests in
  `tests/nca/packet/cli_test.py` and
  `tests/nca/utils/cards/review_queue_test.py`).
- `scripts/lint` — all checks passed; `scripts/format --check --diff` —
  neither touched file flagged (this repo has pre-existing, unrelated
  formatting drift elsewhere, confirmed not introduced by this change).
- `lrh validate` — 0 errors, 20 pre-existing warnings (baseline).
- See `2026_11_11_03_30_49_WI_UNIFY_CARD_FAMILIES_REGISTRY_SELFREVIEW.md`
  for the Step 7.5 cold-context review and its independent
  re-verification of the two highest-risk special cases (`charter`'s
  single-document flag, `constitutions`'s `yaml_root_key`).

# Follow-up

None scoped by this fix.
