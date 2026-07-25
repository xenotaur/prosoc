---
execution_id: 2026_07_25_02_09_07_WI_CARD_STATUS_FOUNDATION
prompt_id: PROMPT(WI-CARD-STATUS-FOUNDATION:WI_CARD_STATUS_FOUNDATION)[2026-07-25T01:29:53-04:00]
work_item: WI-CARD-STATUS-FOUNDATION
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/40
commit: 
created_at: 2026-07-25T02:09:07-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-STATUS-FOUNDATION.md
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Implemented the Phase 0a foundation of the normative packet assembler on the
scenarios family: the shared card-lifecycle contract and a machine-readable
`state` field, projected into the Markdown STATUS block and enforced by a new
`scripts/validate/status`. First implementation work item under
`WS-NORMATIVE-PACKET-ASSEMBLY`; the other four card families follow as separate
items reusing this contract.

# Result

**Lifecycle enum (`prosoc/scenarios/workflow.md`)** — inserted `APPROVED`
between `AUDITED` and `VALIDATED` (decision B): `AUDITED` now denotes an
automated audit; `APPROVED` is the human-approval gate that `AUDITED`
previously carried. Retired `VERIFIED` in favor of `VALIDATED` (decision A);
paper Figure 3 reconciliation stays tracked in the proposal. Documented the
canonical chain and the machine-readable `state` field.

**Machine-readable state** — added a required `state` enum to
`prosoc/scenarios/schema.json`; authored `state` in each scenario's fenced YAML
(authoritative), sourced from its current STATUS-block `STATE`; regenerated all
20 `scenario.yml`. The only payload change is `+state: DRAFTED`; no normative
content changed, so the corpus stays audit-clean (verified the `scenario.md`
and `.yml` diffs are the `state` line only).

**Projection + validation** — `prosoc/scenarios/status.py` (pure helpers),
`prosoc/scenarios/validate_status.py` + `scripts/validate/status` (CLI: checks
Markdown `STATE` == YAML `state`; `--fix` reprojects). Used the
bash-wrapper + `python -m` pattern (matches `scripts/distill/*`) rather than
the direct-import pattern of `scripts/validate/card`, which only works with the
repo root on `PYTHONPATH`. Added unit + CLI tests and updated the
`render_sections_test` fixtures for the now-required `state`. Updated the
scenarios README and the `workflow.md` Status template.

Decisions A (keep `VALIDATED`, retire `VERIFIED`) and B (insert `APPROVED`,
`AUDITED`→automated) were confirmed by the user at the implement plan gate.

# Validation

- `scripts/format --check`: clean.
- `scripts/lint`: All checks passed.
- `scripts/test`: 97 passed (was 80; +17 new).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 20 scenarios consistent.
- `scripts/version tools`: not present in this repo (WI listed it generically);
  skipped.

# Follow-up

- Roll out the same contract to the other four card families (tasks, contexts,
  constitutions, charter) as follow-on Phase 0a work items.
- Optionally wire `prosoc-scenario-audit` to advance a card's STATE to
  `AUDITED` on a passing audit (currently STATE is edited manually).
- Consider adding `scripts/validate/status` to CI.
