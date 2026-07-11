---
execution_id: 2026_07_09_16_38_11_WI_SCENARIO_DISTILL_INVOCATION
prompt_id: PROMPT(WI-SCENARIO-DISTILL-INVOCATION:WI_SCENARIO_DISTILL_INVOCATION)[2026-07-09T16:30:02-04:00]
work_item: WI-SCENARIO-DISTILL-INVOCATION
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/15
commit: e65bb575448248b6d4b8d75e659d1eae0b33f3f0
created_at: 2026-07-09T16:38:11-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-SCENARIO-DISTILL-INVOCATION.md
session_transcript: claude-app:cce2dec4-70fb-48fa-b215-e794254850a0
---

# Summary

Implement WI-SCENARIO-DISTILL-INVOCATION: add `--scenario <id>` scoping to
`prosoc.scenarios.distill`'s discovery layer, and fix both scenario-authoring
skills' distiller invocations to use the canonical `scripts/distill/scenarios`
wrapper instead of broken/hand-rolled alternatives.

# Result

- Added `scenario: str | None = None` filtering to `discover_directory_layout`,
  `discover_flat_layout`, `discover_scenarios`, and `distill_all` in
  `prosoc/scenarios/distill.py`; added `--scenario ID` to the CLI.
- Added `LiterateDiscoveryError` to `prosoc/literate/errors.py` — discovered
  during implementation that this class was imported and raised by all five
  `distill.py` modules (charter, constitutions, contexts, scenarios, tasks)
  but never defined, so the empty-corpus/no-match path silently raised
  `ImportError` instead. Never previously exercised because the corpus is
  never actually empty in practice. This was a blocking dependency for the
  work item's own acceptance criteria, not unrelated scope creep.
- Created `tests/scenarios/distill_test.py` (7 tests): directory- and
  flat-layout `--scenario` filtering (match, no-match, unfiltered), and
  `distill_all`'s two distinct `LiterateDiscoveryError` messages (scoped
  no-match names the scenario and root; unscoped empty-corpus does not).
- Fixed `.claude/skills/prosoc-scenario-new/SKILL.md` Step 6: replaced two
  invocations that both raised `ModuleNotFoundError` with `scripts/distill/scenarios`.
- Fixed `.claude/skills/prosoc-scenario-audit/SKILL.md` Step 1: replaced the
  inline `python -c` heredoc with `scripts/distill/scenarios --scenario <name>
  --dry-run --show-diffs`, trimmed the surrounding justification prose.

# Validation

- `scripts/lint` — "All checks passed!"
- `scripts/test` — 64 tests, 0 failures (57 pre-existing + 7 new)
- `lrh validate` — only the known pre-existing, unrelated
  `focus/current_focus.md` error
- `scripts/format --check --diff` — the only hunk in `prosoc/scenarios/distill.py`
  is pre-existing, unrelated blank-line drift (confirmed via `git diff` — not
  touched by this change); `tests/scenarios/distill_test.py` formatted clean
  after a scoped `black` pass (new file, no baseline to preserve)
- `scripts/distill/scenarios --scenario blind_corner --dry-run --show-diffs` —
  exit 0, no diff
- `scripts/distill/scenarios --scenario nonexistent-id --dry-run` — exit 1,
  `LiterateDiscoveryError: No scenario 'nonexistent-id' found under .../prosoc/scenarios`

# Follow-up

- `README.md`'s stale `scripts/distill` (singular) references and the
  repo-wide `scripts/format --check --diff` drift across ~14 unrelated files
  remain untracked — out of scope here, noted in the prior PR's execution
  record as well.
