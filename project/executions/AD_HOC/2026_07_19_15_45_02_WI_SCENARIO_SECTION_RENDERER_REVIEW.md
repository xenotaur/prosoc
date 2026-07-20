---
execution_id: 2026_07_19_15_45_02_WI_SCENARIO_SECTION_RENDERER_REVIEW
prompt_id: PROMPT(AD_HOC:WI_SCENARIO_SECTION_RENDERER_REVIEW)[2026-07-19T15:43:24-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 2026_07_19_14_59_17_WI_SCENARIO_SECTION_RENDERER
pr: https://github.com/xenotaur/prosoc/pull/21
commit: 
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/21
session_transcript: pending
created_at: 2026-07-19T15:45:02-04:00
---

# Summary

Address 1 open `copilot-pull-request-reviewer` comment on PR #21 ("Add
scenario section renderer (WI-SCENARIO-SECTION-RENDERER)").

# Result

The comment passed presence/validity/feasibility checks and was fixed:

1. `render_scenario_sections` ran the compile-and-compare freshness check
   (`_load_and_check_freshness`) before checking whether the target
   sections already exist. A scenario that already has hand-authored
   sections (e.g. `intersection_gesture_proceed`) could therefore raise
   `StaleScenarioYamlError` first, even though the renderer would have
   refused on `SectionAlreadyPresentError` anyway — confusing, and noisier
   than necessary in `--all` batch runs. Reordered
   `render_scenario_sections` in
   `prosoc/scenarios/render_sections.py` to read `scenario.md` and check
   for existing sections first, only running the freshness check
   afterward. Added
   `TestRefuseOnExistingSection.test_existing_section_check_short_circuits_before_freshness_check`
   to `tests/scenarios/render_sections_test.py`, asserting that a scenario
   with both an already-present section and a deliberately stale
   `scenario.yml` raises `SectionAlreadyPresentError`, not
   `StaleScenarioYamlError`.

# Validation

- `git rev-parse HEAD` — f8faced68beec1b3f3316ed1e65ffd11665a2947 (before
  this fix's commit)
- `git status --short` — only the two files touched by this fix
- `scripts/version tools` — not present in this repo (confirmed absent);
  no equivalent found
- `scripts/format --check --diff` — clean, 43 files unchanged
- `scripts/lint` — all checks passed
- `scripts/test` — 80 tests OK (79 prior + 1 new regression test)
- `lrh validate` — 1 pre-existing error (`focus/current_focus.md` not
  found), unrelated to this change; 0 errors attributable to this fix
- `python3 -m prosoc.scenarios.render_sections intersection_gesture_proceed --dry-run`
  — re-verified the exact scenario the review comment used as its
  motivating example still refuses cleanly

# Follow-up

- `session_transcript: pending` should be updated to
  `claude-app:<session-id>` after this session ends.
