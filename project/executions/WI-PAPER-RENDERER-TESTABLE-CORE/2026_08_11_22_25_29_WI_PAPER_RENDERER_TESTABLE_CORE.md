---
execution_id: 2026_08_11_22_25_29_WI_PAPER_RENDERER_TESTABLE_CORE
prompt_id: PROMPT(WI-PAPER-RENDERER-TESTABLE-CORE:WI_PAPER_RENDERER_TESTABLE_CORE)[2026-08-11T22:13:20+00:00]
work_item: WI-PAPER-RENDERER-TESTABLE-CORE
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/89
commit: 65f034026213de65d2f14fdd33cb157c32e4f645
created_at: 2026-08-11T22:25:29+00:00
agent: codex_app
instruction_source: project/work_items/proposed/WI-PAPER-RENDERER-TESTABLE-CORE.md
session_transcript: pending
---

# Summary

Extract the Frontiers supplement renderer's reusable mechanics into an
importable `prosoc` module with focused unit tests while keeping the
paper-specific renderer path intact.

# Result

Implemented `prosoc.utils.papers.render` with source-manifest parsing, Pandoc
argument construction, deterministic LaTeX fragment fixups, placeholder
substitution, and path-parameterized paper rendering. Replaced
`papers/01_charter/render.py` with a thin shim that remains directly runnable
from the repository root and still writes
`build/papers/01_charter/rendered.tex`. Added unit tests under
`tests/utils/papers/` and updated setuptools package discovery so new
subpackages are included.

Prior-art check was already present in the work item. No additional demand
match was actioned during implementation. A fresh independent self-review
subagent reviewed the working-tree diff and reported no issues.

# Validation

- `scripts/version tools` was unavailable in this repo (`scripts/version` does
  not exist).
- `black --check --diff prosoc/utils/papers/render.py tests/utils/papers/render_test.py papers/01_charter/render.py`
  passed after formatting touched files.
- `scripts/format --check --diff` was run and remains blocked by pre-existing
  unrelated Black formatting debt outside this change set.
- `scripts/lint` passed.
- `python -m unittest tests.utils.papers.render_test` ran 15 tests and passed.
- `scripts/test` ran 254 tests and passed.
- `lrh validate` reported 0 errors and 0 warnings.
- `papers/01_charter/render.py` rendered
  `build/papers/01_charter/rendered.tex`.

# Follow-up

Land PR #89 via the LRH land chain. Keep the run's explicit constraint not to
manually trigger GitHub review agents; use local/fresh self-review instead if
another independent look is needed.
