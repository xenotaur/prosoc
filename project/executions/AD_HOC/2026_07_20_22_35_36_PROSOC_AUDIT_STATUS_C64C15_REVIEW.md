---
execution_id: 2026_07_20_22_35_36_PROSOC_AUDIT_STATUS_C64C15_REVIEW
prompt_id: PROMPT(AD_HOC:PROSOC_AUDIT_STATUS_C64C15_REVIEW)[2026-07-20T22:25:59-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/27
commit: a6eb6ee881d5221bdb9ce3205db80028f716f98a
created_at: 2026-07-20T22:35:36-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/27
session_transcript: claude-app:556d2127-e3d4-49e0-a746-95ad3c7a8f6e
---

# Summary

Address 17 open `copilot-pull-request-reviewer` comments on
[xenotaur/prosoc#27](https://github.com/xenotaur/prosoc/pull/27) (the
full-corpus manual editing pass + audit refresh), via `/lrh-review-response`.

# Result

Triaged the 17 comments into 3 groups, all valid and feasible:

1. **`related_scenarios` values don't match scenario `id`** (7 comments) —
   the new `related_scenarios` field used directory-style scenario names
   (e.g. `frontal_approach`) while `scenario.yml`'s own `id:` field carries a
   versioned suffix (`frontal_approach_01`). Rather than rewrite the data to
   the suffixed form (which would break consistency with the corpus's
   already-established directory-name convention used by `audit.md`
   frontmatter and `AUDIT_SUMMARY.md`), reworded `schema.json`'s
   `related_scenarios` description and `template.md`'s YAML sample comment
   to clarify the field references directory names/scenario keys, not the
   internal `id`.
2. **`audit.md` frontmatter `scenario:` inconsistency** (8 comments) — 8 of
   20 `audit.md` files (produced by parallel audit subagents in the prior
   session) used the suffixed `_01` scenario.yml `id` as their frontmatter
   `scenario:` value instead of the directory name used by the other 12.
   Normalized all 8 (`frontal_approach`, `intersection_gesture_proceed`,
   `intersection_gesture_wait`, `intersection_no_gesture`,
   `pedestrian_overtaking`, `perpendicular_traffic`, `following`,
   `exiting_room`) to the directory-name convention.
3. **Stale "future batch-audit skill" wording** (1 comment) —
   `AUDIT_SUMMARY.md` referenced a hypothetical future mechanism even though
   `/prosoc-scenario-audit-all` already exists and produced the file.
   Reworded to reference it directly.

No comments were skipped.

# Validation

- `git rev-parse HEAD` (pre-fix): `b6a66ec7c734ee7cf0acd3da5957aadc0a3a32ee`
- `scripts/version tools`: unavailable (no such script in this repo)
- `scripts/format --check --diff`: pass, 43 files unchanged
- `scripts/lint`: pass, all checks passed
- `scripts/test`: pass, 80 tests OK
- `lrh validate`: 1 pre-existing error (`focus/current_focus.md` missing —
  known repo-wide gap, unrelated to this change; see project memory
  `project_lrh_scaffolding_status`)
- `python3 -c "import json; json.load(open('prosoc/scenarios/schema.json'))"`:
  valid JSON after edit

# Follow-up

None new. The two follow-ups already deferred from the parent PR
(`related_scenarios`/`cited_in` backfill, possible P0 principles
under-trim) remain open, tracked separately.
