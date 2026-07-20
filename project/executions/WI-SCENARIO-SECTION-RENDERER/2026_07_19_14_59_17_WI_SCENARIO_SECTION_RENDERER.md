---
execution_id: 2026_07_19_14_59_17_WI_SCENARIO_SECTION_RENDERER
prompt_id: PROMPT(WI-SCENARIO-SECTION-RENDERER:WI_SCENARIO_SECTION_RENDERER)[2026-07-19T14:35:46-04:00]
work_item: WI-SCENARIO-SECTION-RENDERER
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/21
commit: 3e454a04fd6724f3f4437ab8712c96d8827751bd
agent: claude_app
instruction_source: project/work_items/proposed/WI-SCENARIO-SECTION-RENDERER.md
session_transcript: claude-app:e2216c34-0687-42db-a1fa-2245f8a00059
created_at: 2026-07-19T14:59:17-04:00
---

# Summary

Implement `prosoc/scenarios/render_sections.py`, a script that mechanically
renders `template.md`'s required "Scenario Card Summary" and "Scenario Usage
Guide" sections into a scenario's `scenario.md` from its already-distilled
`scenario.yml`, flagging (never fabricating) any absent field, and refusing
rather than overwriting when either section already exists or `scenario.yml`
is stale relative to `scenario.md`'s embedded YAML.

# Result

- Added `prosoc/scenarios/render_sections.py`, sibling to `distill.py`,
  reusing its `ScenarioSource`/`discover_scenarios`/`SCHEMA_PATH` and the
  `compiler.compile_file` + `utils.dump_yaml` freshness-check pipeline.
- Renders both sections with raw pass-through of `scenario.yml` fields per
  the field/schema-path mapping in the work item; absent fields (and the two
  schema-unsupported fields `Related Scenarios`/`Cited In`) are listed in a
  trailing "Remaining gaps" section using the same bullet format as
  `prosoc-scenario-audit`'s `audit.md` Completeness section.
- Refuses and reports (never overwrites) when either target section is
  already present, or when `scenario.yml` is stale/missing relative to
  `scenario.md`'s embedded YAML.
- Inserts Card Summary before `## Scenario Overview` and Usage Guide before
  `## Notes for Scenario Designers and Evaluators` (falling back to
  appending at end of file if that optional heading is absent); raises a
  clear structural error, rather than guessing, if the required
  `## Scenario Overview` anchor is missing.
- Stamps the scenario's `EDITED:` Status-block field on successful render,
  per `workflow.md`'s Status Section Template.
- CLI: `python3 -m prosoc.scenarios.render_sections <scenario_id>` or
  `--all`, mirroring `distill.py`'s `--dry-run`/`--show-diffs` flags.
- Fixed a bug found during manual verification: YAML folded scalars (e.g.
  `summary: >`) retain a trailing newline that was leaking into rendered
  bullets as a stray blank line; field values are now stripped before
  rendering.
- Added `tests/scenarios/render_sections_test.py` (14 tests) covering full
  rendering, gaps-checklist rendering, refuse-on-existing-section,
  refuse-on-stale-yaml (including missing yml), missing-anchor-heading
  behavior, and `--all` batch scoping/skip behavior.

# Validation

- `scripts/format --check --diff` — clean (43 files unchanged after
  `scripts/format` was run once to fix 2 files)
- `scripts/lint` — all checks passed
- `scripts/test` — 79 tests OK (incl. 14 new)
- `lrh validate` — 1 error, 0 warnings; the error is the known pre-existing
  `focus/current_focus.md` `FILE_NOT_FOUND`, unrelated to this change
- `python3 -m prosoc.scenarios.render_sections join_a_group --dry-run --show-diffs`
  — renders both sections with zero schema-backed gaps (only the two
  permanent `Related Scenarios`/`Cited In` gaps)
- `python3 -m prosoc.scenarios.render_sections leading --dry-run --show-diffs`
  — same
- `python3 -m prosoc.scenarios.render_sections object_handover --dry-run --show-diffs`
  — same
- `python3 -m prosoc.scenarios.render_sections intersection_gesture_proceed --dry-run`
  — refuses cleanly, reporting both sections already present
- `python3 -m prosoc.scenarios.render_sections movable_obstruction --dry-run`
  — refuses cleanly; this scenario predates `template.md`'s heading
  structure (`## Overview` instead of `## Scenario Overview`, no
  `## Scenario Specification (Machine-Readable)` heading), so the tool
  correctly reports rather than guessing an insertion point
- Confirmed via `git status --short` that none of the above dry-runs
  modified any real corpus file — only the two new files are untracked

`scripts/version tools` from the skill's canonical validation sequence does
not exist in this repo (no `scripts/version` script); skipped as
inapplicable.

# Follow-up

- Fixing the underlying missing-YAML-field gaps for the 8 partial-data
  scenarios identified in `prosoc/scenarios/AUDIT_SUMMARY.md` (e.g.
  `movable_obstruction`) is separate, scenario-by-scenario editorial work,
  out of scope here per the work item's Non-Goals.
- `movable_obstruction`'s `scenario.md` structure predates `template.md`'s
  current heading conventions; bringing it into structural conformance
  (`## Overview` → `## Scenario Overview`, adding a
  `## Scenario Specification (Machine-Readable)` heading) is a prerequisite
  before this tool can render sections into it — also out of scope here.
- `session_transcript` is `pending`; update to `claude-app:<session-id>`
  before or when this PR lands.
