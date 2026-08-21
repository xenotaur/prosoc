---
execution_id: 2026_08_20_00_13_37_WI_SKILL_DOCS_SRC_LAYOUT_REFRESH
prompt_id: PROMPT(AD_HOC:WI_SKILL_DOCS_SRC_LAYOUT_REFRESH)[2026-08-20T00:12:15+00:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/99
commit: df41656572510124117694477434c9d7cc8c7f12
created_at: 2026-08-20T00:13:37+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-SKILL-DOCS-SRC-LAYOUT-REFRESH.md
session_transcript: claude-app:9686211b-8ac8-4bcd-bd8f-8b198c484df2
---

# Summary

Created work item `WI-SKILL-DOCS-SRC-LAYOUT-REFRESH`: a planning artifact
requesting stale pre-move `prosoc/...` path references be refreshed
across 9 actively-used `.claude/skills/*.md` files, left out of scope by
`WI-NCA-PRNC-PACKAGE-LAYOUT`'s deliberately narrow Required Changes.

# Result

Wrote `project/work_items/proposed/WI-SKILL-DOCS-SRC-LAYOUT-REFRESH.md`,
opened PR #99 (`xenotaur/chore/wi-skill-docs-src-layout-refresh`). The 9
affected files and their exact stale-reference counts were enumerated by
a cold-context `/lrh-self-review` subagent dispatched independently
against `WI-NCA-PRNC-PACKAGE-LAYOUT`'s PR #95, and re-verified fresh via
grep while drafting this work item (counts: `prosoc-card-audit/SKILL.md`
13, `prosoc-card-approve/SKILL.md` 11, `prosoc-card-review/SKILL.md` 2,
`prosoc-card-review-all/SKILL.md` 2, `prosoc-card-audit-all/SKILL.md` 5,
`prosoc-scenario-new/SKILL.md` 7, its `references/schema_guide.md` 1,
`_shared/principles.md` 2, `_shared/pg_scenarios.md` 2). No
implementation performed in this session — this record documents the
work item's creation only.

# Validation

- `lrh validate` — 0 errors, 0 warnings, after writing the work item file.

# Follow-up

- `/lrh-implement WI-SKILL-DOCS-SRC-LAYOUT-REFRESH` to actually apply the
  path-reference fixes.
- `session_transcript: pending` should be updated to the durable
  Claude.app session pointer when available.
