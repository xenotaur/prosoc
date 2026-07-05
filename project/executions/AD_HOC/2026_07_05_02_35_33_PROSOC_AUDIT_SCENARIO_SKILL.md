---
execution_id: 2026_07_05_02_35_33_PROSOC_AUDIT_SCENARIO_SKILL
prompt_id: PROMPT(AD_HOC:PROSOC_AUDIT_SCENARIO_SKILL)[2026-07-05T02:24:03-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/3
commit: 6ddf9a0ce37de8580c84f2adb083a8b8bc8c1e64
created_at: 2026-07-05T02:35:33-04:00
agent: claude_app
instruction_source: ad_hoc conversation - design session for a prosoc-scenario-audit skill (AUDITED lifecycle stage support)
session_transcript: claude-app:bd6f49d9-4298-4251-8c35-c13b8b341339
---

# Summary

Add a project-local `prosoc-scenario-audit` skill that produces an `audit.md`
findings report for a prosoc scenario directory, covering prose/YAML
consistency, schema and charter compliance, source fidelity against the P&G
paper, and completeness against the AUDITED-required sections in
`prosoc/scenarios/template.md`. Also move `pg_scenarios.md`/`principles.md`
to `.claude/skills/_shared/` and rename `new-scenario` to
`prosoc-scenario-new` for tab-completion clustering. Design decisions
(shared-reference location, single-scenario scope, naming) were reached
through discussion before implementation began.

# Result

- Created `.claude/skills/prosoc-scenario-audit/SKILL.md` and
  `references/audit_checklist.md`.
- Moved `.claude/skills/new-scenario/references/{pg_scenarios,principles}.md`
  to `.claude/skills/_shared/`; both scenario skills now read that location
  directly instead of maintaining copies.
- Renamed `.claude/skills/new-scenario` to `.claude/skills/prosoc-scenario-new`,
  updated its `name:` frontmatter and internal reference paths. Left the
  historical `DRAFTED: Claude (new-scenario skill), <date>` citations already
  committed in existing scenario cards untouched (provenance, not a live
  pointer).
- Fixed a bug found during dry-run: the skill's Step 1 originally proposed a
  literal text diff between the embedded YAML block and `scenario.yml` to
  check freshness; this always shows noise because the distiller
  re-serializes YAML. Changed to re-run the distiller and check for a real
  diff/error instead.
- Opened PR #3.

# Validation

- `scripts/format`, `scripts/lint`, `scripts/test` all pass (57 tests). An
  initial `scripts/format --check --diff` run reformatted 14 unrelated
  pre-existing files (the script ignores its arguments and always reformats
  in place); those changes were reverted as out of scope.
- Manually dry-ran the audit checklist against
  `prosoc/scenarios/blind_corner/`: confirmed correct source-fidelity match
  against `pg_scenarios.md`, confirmed prose/YAML consistency, and confirmed
  the completeness check correctly flags the missing AUDITED-required
  sections (Scenario Card Summary, prose Scenario Usage Guide) that none of
  the 18 existing DRAFTED scenarios currently have.
- `lrh validate` does **not** pass cleanly: `project/focus/current_focus.md`
  is missing. This is pre-existing and out of scope for this change — prosoc
  has never had the full LRH project control-plane scaffold (`lrh project
  doctor` reports `project/principles`, `project/goal`, `project/roadmap`,
  `project/focus`, `project/work_items`, `project/evidence`,
  `project/status`, `project/executions/README.md`, and `PROMPTS.md` all
  missing; only `project/executions/` exists, created by this task). Running
  `lrh project init --profile full` would fix this but is a separate,
  larger decision (it would create real content like `project/goal` and
  `project/principles`, which risks name-colliding with prosoc's own
  charter/P1-P8 principles concept) — flagged for the user rather than done
  unilaterally.

# Follow-up

- No scenario has been audited yet with the new skill; running it against a
  real scenario and reviewing the resulting `audit.md` is a natural next step
  once this PR lands.
- Decide whether/how to bootstrap the rest of the LRH project control-plane
  scaffold (`lrh project init --profile full`) as a separate, deliberate
  initiative — not done as part of this task.
- `session_transcript` should be updated from `pending` to
  `claude-app:<session-id>` once the session ID is known.
- Once PR #3 merges, update this record to `status: landed` with the merge
  commit SHA (`lrh prompt update-execution`).
