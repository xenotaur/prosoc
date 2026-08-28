---
execution_id: 2026_08_28_07_24_21_WI_DECLARE_OPENAI_DOTENV_DEPS_IMPL
prompt_id: PROMPT(WI-DECLARE-OPENAI-DOTENV-DEPS:WI_DECLARE_OPENAI_DOTENV_DEPS_IMPL)[2026-08-28T07:19:12+00:00]
work_item: WI-DECLARE-OPENAI-DOTENV-DEPS
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/105
commit: 
created_at: 2026-08-28T07:24:21+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-DECLARE-OPENAI-DOTENV-DEPS.md
session_transcript: pending
---

# Summary

Implements `WI-DECLARE-OPENAI-DOTENV-DEPS`: declares `openai` and
`python-dotenv` as core `pyproject.toml` dependencies, since both are
unconditional module-level runtime imports that a plain `pip install
-e .` previously failed to satisfy.

# Result

Added `openai` and `python-dotenv` to `pyproject.toml`'s `dependencies`
list (core, not an optional extra — the WI's own acceptance criteria
require a plain `pip install -e .` with no extra to reach 259/259,
which only a core dependency satisfies). Removed the now-redundant
explicit `python -m pip install openai python-dotenv` line from
`.github/workflows/tests.yml`.

Verified via diff-mode `/lrh-self-review`: both imports are genuinely
unconditional (no lazy/conditional import), no other file in `src/`
needs the same treatment, and no other install-assumption site
(README, other CI workflows) needed touching — `environment.yml`
already lists both but is an unrelated full conda/pip-freeze snapshot,
not part of the `pip install -e .` path.

# Validation

- Fresh venv: `pip install -e .` (no separate install), then
  `scripts/test` — 259/259 passing.
- `scripts/format --check --diff` — clean for the 2 changed files
  (pre-existing, unrelated black-version drift noted in 22 other files,
  not touched by this change).
- `scripts/lint` — all checks passed.
- `lrh validate` — 0 errors, 20 pre-existing warnings in unrelated
  files.

# Follow-up

- `/lrh-land` chain (review-response, confirm-fixes, merge, closeout)
  to follow via `/lrh-execute`'s own Step 4.
- `session_transcript: pending` should be updated to the durable
  Claude.app session pointer when available.
