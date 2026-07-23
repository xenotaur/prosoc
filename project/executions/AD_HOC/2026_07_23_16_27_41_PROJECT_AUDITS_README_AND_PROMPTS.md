---
execution_id: 2026_07_23_16_27_41_PROJECT_AUDITS_README_AND_PROMPTS
prompt_id: PROMPT(AD_HOC:PROJECT_AUDITS_README_AND_PROMPTS)[2026-07-23T16:27:41-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/34
commit: 3185cd84c2628f5cdb003572f120caee6e84510f
created_at: 2026-07-23T16:27:41-04:00
agent: claude_app
instruction_source: ad hoc — Tier 2 follow-up from the same lrh project init bootstrap investigation that produced PR #33 (PROJECT_SCAFFOLD_FOCUS_EXECUTIONS_README), deferred at the time as lower-priority
session_transcript: claude-app:18a43d9f-32c1-4b82-8883-e2cb590cf592
---

# Summary

Second of two follow-ups from the `lrh project init` bootstrap
investigation. Landed `PROMPTS.md` (closing the last `doctor`-required-but-
missing scaffold path) and `project/audits/README.md` (disambiguating
LRH's cross-repo engineering-audit convention from prosoc's unrelated
scenario-content-audit concept), both documenting conventions already in
real, de facto use rather than authoring speculative content.

`/lrh-review-response` was run against PR #34 and reported "Nothing to
resolve" (no open review comments) — no fix round was needed, so no
`_REVIEW` execution record exists for this PR.

# Result

**`PROMPTS.md`:** documents the `PROMPT(<WORK_ITEM_OR_AD_HOC>:<SLUG>)[<timestamp>]`
ID format, prosoc's `_REVIEW`/`_CONFIRM` slug-suffix convention, and the
`lrh prompt label` / `record-execution` / `check-execution` /
`update-execution` CLI commands.

**`project/audits/README.md`:** documents `project/audits/` as an
LRH-wide convention (`lrh request audit-docs`'s default output path,
confirmed precedented in LRH's own repo and in `xenotaur/LCATS`) distinct
from `prosoc/scenarios/<name>/audit.md`/`AUDIT_SUMMARY.md`, which is the
unrelated scenario-content-lifecycle audit.

This is a retroactive execution record — the session was ad hoc
investigation-then-implementation, not started via `/lrh-implement`, so no
`in_progress` record existed prior to `/lrh-closeout`.

# Validation

- `lrh validate`: 0 errors, 0 warnings (unchanged — already clean before
  this PR)
- `lrh project doctor`: `PROMPTS.md` now reports `present`;
  `recommended_next_step` dropped from `--profile full` to `--profile
  minimal`
