---
execution_id: 2026_07_29_03_55_40_WI_CARD_STATUS_CHARTER
prompt_id: PROMPT(WI-CARD-STATUS-CHARTER:WI_CARD_STATUS_CHARTER)[2026-07-29T03:40:52-04:00]
work_item: WI-CARD-STATUS-CHARTER
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/49
commit: 592204f478a9b7d7f52dbb14ef71660a258a167d
created_at: 2026-07-29T03:55:40-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-STATUS-CHARTER.md
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Implemented WI-CARD-STATUS-CHARTER — extending the machine-readable
lifecycle-`state` contract to the charter, the fifth and final Phase 0a family.
The charter is a single multi-principle document (`charter.md` -> `charter.yml`,
top-level `principles:` list), so this adds a single-source family adapter and
teaches the charter distiller to emit a document-level `state`.

# Result

Settled the flagged design decision in favour of **fenced-YAML-authoritative**
(uniform with the other four families), rather than making the charter the one
family where Markdown is authoritative.

- `prosoc/charter/charter.md`: added a `## Status` block with a canonical
  `- **STATE:** DRAFTED` bullet and an authoritative fenced `state: DRAFTED`
  block. No principle (P0-P9) content changed (+20 lines, Status section only).
- `prosoc/charter/schema.json`: top-level `state` enum now required alongside
  `principles` (kept `additionalProperties: false`).
- `prosoc/charter/distill.py`: reworked `distill_charter` to compose the
  compiler's lower-level helpers, split the state block (has `state`, no `id`)
  from principle blocks, assemble `{state, principles}`, then validate — the
  generic `compile_file` validates mid-compile and would sweep the state block
  into `principles`. Added `CharterSource` + `discover_charter` (single-source)
  for the status validator.
- `prosoc/charter/charter.yml`: regenerated — single `+state: DRAFTED` line,
  principles untouched; distiller is idempotent.
- `prosoc/charter/runtime.py`: added an optional `state` field to the `Charter`
  pydantic model so `loader.load_charter()` exposes it (pydantic 2 would
  otherwise silently drop the extra top-level key).
- `prosoc/utils/cards/validate_status.py`: registered the single-source
  `charter` family (`yaml_root_key=None`, `supports_flat=False`).
- Tests: `distill_test.py` state-lifting + `discover_charter` cases;
  `validate_status_test.py` `CharterFamilyTest`; routed the `charter_test.py`
  md<->yml consistency guardrail through `distill_charter` (it previously used
  the generic `compile_file`, which now fails the state-requiring schema).

Prior-art check present in the WI (`## Problem / Context`); no duplication or
demand issues. This completes Phase 0a — all five families carry the contract.

# Validation

- `scripts/test`: 147 passed (+8).
- `scripts/lint`: All checks passed.
- `scripts/format --check` (black 25.12.0): clean (53 files unchanged).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 31 cards (5 families) consistent;
  `--family charter`: consistent.
- `python -m prosoc.charter.distill --dry-run --show-diffs`: no differences.

# Follow-up

- At closeout, resolve WI-CARD-STATUS-CHARTER and mark the workstream's charter
  bullet resolved. The workstream stays open (audit skills, assembler,
  manifests, CI drift gate remain).
- `scripts/version` (from the skill's canonical sequence) does not exist in this
  repo; used the `scripts/` commands that do.
