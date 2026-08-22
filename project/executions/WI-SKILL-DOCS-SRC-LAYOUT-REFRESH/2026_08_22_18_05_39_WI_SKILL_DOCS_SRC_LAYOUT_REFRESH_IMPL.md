---
execution_id: 2026_08_22_18_05_39_WI_SKILL_DOCS_SRC_LAYOUT_REFRESH_IMPL
prompt_id: PROMPT(WI-SKILL-DOCS-SRC-LAYOUT-REFRESH:WI_SKILL_DOCS_SRC_LAYOUT_REFRESH_IMPL)[2026-08-22T17:52:22+00:00]
work_item: WI-SKILL-DOCS-SRC-LAYOUT-REFRESH
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/103
commit: 
created_at: 2026-08-22T18:05:39+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-SKILL-DOCS-SRC-LAYOUT-REFRESH.md
session_transcript: pending
---

# Summary

Implements `WI-SKILL-DOCS-SRC-LAYOUT-REFRESH`: updates all 9 named
`.claude/skills/*.md` files whose `prosoc/<family>/...`/`prosoc.<family>`
references still pointed at the pre-migration flat package layout, after
`WI-NCA-PRNC-PACKAGE-LAYOUT` moved the package under `src/`.

# Result

Fixed all 13/11/2/2/5/7/1/2/2 stale references across the WI's 9 listed
files, per the mapping the WI documents: charter/scenarios/tasks/contexts
→ `src/prosoc/prnc/<family>/...`; constitutions/manifests →
`src/prosoc/<family>/...` (stay top-level, not under `prnc/`);
literate/auditor/packet/utils (including `utils/cards`) →
`src/prosoc/nca/<family>/...`.

A diff-mode `/lrh-self-review` pass (Step 7.5, before first push) surfaced
one real, independently-verified issue beyond the WI's literal scope: two
lines in `prosoc-scenario-new/SKILL.md` referenced
`scenario_template.md`, a filename that was renamed to `template.md`
before the `src/`-layout migration even happened (verified via `git log
--diff-filter=R` and `find` — `bcb5350`). The mechanical flat→`src/`
prefix translation preserved this already-broken filename, so the
"corrected" path still didn't resolve on disk. Fixed both references to
`template.md` directly, since this was the same two lines already being
edited and left the deliverable's own paths still broken otherwise.

# Validation

- `grep -rEn 'prosoc\.(literate|auditor|packet|utils|charter|scenarios|tasks|contexts)\b' .claude/skills/` — 0 matches
- `grep -rEn '\bprosoc/(charter|scenarios|tasks|contexts|constitutions|manifests|packet|literate|auditor|utils)\b' .claude/skills/ | grep -v 'src/prosoc/'` — 0 matches
- `lrh validate` — 0 errors, 0 warnings
- `scripts/format --check --diff` — clean
- `scripts/lint` — all checks passed
- `scripts/test` — 259/259 passing
- Diff-mode `/lrh-self-review` dispatched; its top finding
  (`scenario_template.md` mismatch) independently re-verified directly
  via `find`/`ls` before being fixed

# Follow-up

- `/lrh-land` chain (review-response, confirm-fixes, merge, closeout) to
  follow via `/lrh-execute`'s own Step 4.
- `session_transcript: pending` should be updated to the durable
  Claude.app session pointer when available.
