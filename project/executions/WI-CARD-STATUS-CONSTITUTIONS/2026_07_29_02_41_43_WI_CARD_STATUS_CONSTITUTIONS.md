---
execution_id: 2026_07_29_02_41_43_WI_CARD_STATUS_CONSTITUTIONS
prompt_id: PROMPT(WI-CARD-STATUS-CONSTITUTIONS:WI_CARD_STATUS_CONSTITUTIONS)[2026-07-29T00:20:01-04:00]
work_item: WI-CARD-STATUS-CONSTITUTIONS
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/47
commit: 1680ea4f84497ee0342a98df46b2ae026b8f4556
created_at: 2026-07-29T02:41:43-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-STATUS-CONSTITUTIONS.md
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Implemented the fourth Phase 0a family. Constitutions diverge structurally
(root-wrapped YAML, heading-style STATUS block), so this added two small
shared-tooling extensions and normalized the constitution STATUS blocks, then
applied the `state` contract to the two constitution cards. Opened as PR #47.

# Result

**Shared tooling (backward-compatible)** — `read_yaml_state`/`check_source` in
`prosoc/utils/cards/status.py` gained an optional `root_key`; when set, state is
read from `data[root_key]["state"]` (default `None` keeps top-level behaviour
unchanged for the other families). `validate_status.py`'s `Family` gained
`yaml_root_key`, forwarded by `_check_family`; the constitutions family is
registered with `yaml_root_key="constitution"`. Note `discover_constitutions`
takes `(root, layout)` (like scenarios), not `(root)`, and returns a list — no
`list()` wrap needed.

**Constitutions family** — added a required `state` enum inside the
`constitution` object in `schema.json`; normalized each `constitution.md` STATUS
block from `## STATUS: EDITED <date>` to `## STATUS` + a bold `- **STATE:**
EDITED` first bullet (provenance bullets bolded); added `state: EDITED` under
`constitution:` in the fenced YAML; regenerated `constitution.yml`. Verified the
`.md`/`.yml` diffs are limited to the STATUS block and the `state` line — no
rule/payload change.

**Template** — normalized `constitution/template.md` to the canonical STATUS
form; retired `VERIFIED` for `VALIDATED` and added `APPROVED`, resolving the
reconciliation `prosoc/scenarios/workflow.md` explicitly flagged for this file;
added nested `state`.

**Tests** — `root_key` cases for `read_yaml_state`/`check_source` in
`status_test.py`; a constitutions-family class in `validate_status_test.py`
(consistent / inconsistent / missing-root-wrapper).

# Validation

- `scripts/format --check` (black 25.12.0, the CI pin): clean (53 files
  unchanged).
- `scripts/lint`: All checks passed.
- `scripts/test`: 138 passed (+6: root_key + constitutions-family tests).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 30 cards consistent (20 scenarios + 4 tasks +
  4 contexts + 2 constitutions); `--family constitutions` reports 2/2.

# Follow-up

- The **charter** is the last Phase 0a family and the structural outlier: a
  single multi-principle document rooted under `principles:`, not a
  card-per-directory family — its family adapter and STATUS/state placement
  differ from the per-card families. Its WI closes out Phase 0a and the
  workstream.
