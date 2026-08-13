---
execution_id: 2026_08_13_03_41_47_WI_NCA_PRNC_PACKAGE_LAYOUT
prompt_id: PROMPT(AD_HOC:WI_NCA_PRNC_PACKAGE_LAYOUT)[2026-08-13T03:40:44+00:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/91
commit: cfb1420
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/91
session_transcript: claude-app:f087f2be-5992-4711-b12b-40cebb7e8305
created_at: 2026-08-13T03:41:47+00:00
---

# Summary

Adds `project/contributors/` (anthony + claude/codex/antigravity agent
entries), fixes four issues found in review of
`PROP-NCA-PRNC-PACKAGE-LAYOUT` (merged via PR #85), and adds its
implementation work item, `WI-NCA-PRNC-PACKAGE-LAYOUT`. Not a `rerun_of`
of that proposal's own primary record
(`2026_08_09_05_05_56_NCA_PRNC_PACKAGE_LAYOUT.md`) — this is new work
(a work item didn't exist before), not a repeat attempt at the same slug.

# Result

Four corrections made to the merged proposal, all carried into the new
work item:

1. `prosoc/utils/experiments/` moves wholesale with `utils/` into
   `nca/utils/`, not carved into its own top-level `prosoc.experiments`
   package — the original split reasoning didn't hold up under scrutiny,
   and collided in name with the unrelated, pre-existing top-level
   `<root>/experiments/`.
2. `packet/schema.json`'s `guidance` object is a third domain-coupled
   artifact alongside `loader.py`/`assemble.py` — previously undercounted
   as "two coupled files."
3. The packaging claim was stale: rebasing onto current `main` (20
   commits ahead of where this worktree was cut) showed `pyproject.toml`'s
   code-discovery declaration (`packages.find.include = ["prosoc*"]`) was
   already fixed independently. Verified with a real `python -m build
   --wheel` — all 40 `.py` files package correctly now. `package-data`
   remains exactly as incomplete as originally described (only
   `prosoc.charter`'s 3 files ship).
4. `papers/01_charter/` (`WI-PAPER-RENDERER-TESTABLE-CORE`, resolved via
   PRs #89-90) landed on `main` while this proposal's implementation was
   deliberately deferred for a real paper submission deadline. It
   hardcodes the flat `prosoc/...` paths this proposal relocates
   (`papers/01_charter/sources.txt`'s 9 source paths,
   `render.py`'s `sys.path` assumption) and ships a golden-file
   regression fixture — both now accounted for in the work item's
   Required Changes, Acceptance Criteria, and Risk Notes.

# Validation

- `lrh validate` — 0 errors, 0 warnings on every commit (contributors,
  proposal fix, work item).
- `python -m build --wheel` from this branch — confirmed 40/40 `.py`
  files package correctly (code-discovery fix already on `main`); data
  files confirmed still limited to `prosoc/charter/{charter.md,
  charter.yml,schema.json}` only, matching the corrected claim.
- Fast-forward merge from the original branch point to current `main`
  (`c252a47..a352335`) — clean, no conflicts with the proposal file.

# Follow-up

- The work item itself (`WI-NCA-PRNC-PACKAGE-LAYOUT`) is the next unit of
  work — the actual `src/` restructuring hasn't started.
- `session_transcript: pending` — update to
  `claude-app:f087f2be-5992-4711-b12b-40cebb7e8305` after the session
  ends.
