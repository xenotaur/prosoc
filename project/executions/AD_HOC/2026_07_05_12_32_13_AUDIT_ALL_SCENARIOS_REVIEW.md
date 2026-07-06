---
execution_id: 2026_07_05_12_32_13_AUDIT_ALL_SCENARIOS_REVIEW
prompt_id: PROMPT(AD_HOC:AUDIT_ALL_SCENARIOS_REVIEW)[2026-07-05T12:27:32-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/4
commit: 1db2b8a34d9f204ea77ca27e9fc9deeea58b2d74
created_at: 2026-07-05T12:32:13-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/4
session_transcript: claude-app:53383085-c1b0-4aa4-a2ae-3ad99f9716b5
---

# Summary

Address the 5 open `copilot-pull-request-reviewer` comments on PR #4
("Audit all 20 scenarios with prosoc-scenario-audit"). All 5 comments
flagged the same underlying issue: `audit.md` reports written by the
batch-audit subagents cited the shared reference files
(`_shared/pg_scenarios.md`, `_shared/principles.md`) using relative paths
that don't actually resolve from each scenario directory.

Note: PR #4 was created directly in a working session rather than via
`/lrh-implement`, so no prior primary execution record exists to link.
`rerun_of` is left empty per the documented edge case.

# Result

Grepped every `prosoc/scenarios/*/audit.md` for citations of `_shared/`
and found the broken forms varied across files: bare `_shared/pg_scenarios.md`,
`../_shared/pg_scenarios.md`, `../_shared/principles.md`, and
`../../.claude/skills/_shared/pg_scenarios.md` — none of which resolve
from `prosoc/scenarios/<name>/audit.md`. Even the forms some subagents
believed were already correct (bare `.claude/skills/_shared/pg_scenarios.md`,
used in `exiting_room` and `following`) were also broken relative paths.

Verified the correct file-relative path from any `prosoc/scenarios/<name>/`
directory to the shared files is `../../../.claude/skills/_shared/pg_scenarios.md`
and `../../../.claude/skills/_shared/principles.md` (three levels up to repo
root, then into `.claude/skills/_shared/`). Applied a single normalization
pass (regex matching any path-like prefix immediately before
`_shared/pg_scenarios.md` / `_shared/principles.md` and replacing the whole
match with the canonical path) across all 20 `audit.md` files, then verified
every scenario directory resolves both shared files via the new path.

Triage: all 5 reported comments passed presence/validity/feasibility checks
and were fixed via this single normalization pass (which also fixed the
same defect in files the 5 comments didn't individually call out, since the
error was systemic across all 20 reports, not isolated to 5 lines).

# Validation

- `scripts/format --check --diff` — discovered this script does not actually
  honor `--check`/`--diff` flags (it unconditionally runs `black prosoc tests`
  regardless of args), so invoking it reformatted 14 unrelated Python files.
  Reverted those via `git checkout --` since they were out of scope for this
  markdown-only fix; no Python files are part of this change.
- `scripts/lint` — all checks passed
- `scripts/test` — 57 tests OK
- `lrh validate` — 1 pre-existing error (`focus/current_focus.md` not found),
  unrelated to this change; see project memory
  `project-lrh-scaffolding-status` (prosoc has never run `lrh project init`).
  0 errors attributable to this change.
- `scripts/version` — not present in this repo; no equivalent tool-version
  script found, so tool versions were not separately recorded.

# Follow-up

- `scripts/format` should be fixed to actually pass `--check`/`--diff`
  through to `black` (currently silently ignores all arguments) — flagged
  as a separate, out-of-scope repo issue, not addressed here.
- `session_transcript: pending` should be updated to `claude-app:<session-id>`
  after this session ends.
