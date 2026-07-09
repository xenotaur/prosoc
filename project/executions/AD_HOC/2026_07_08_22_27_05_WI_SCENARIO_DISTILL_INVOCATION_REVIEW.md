---
execution_id: 2026_07_08_22_27_05_WI_SCENARIO_DISTILL_INVOCATION_REVIEW
prompt_id: PROMPT(AD_HOC:WI_SCENARIO_DISTILL_INVOCATION_REVIEW)[2026-07-08T22:22:17-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/14
commit: c9d9f712e91b1cfd075c83c9e299034efce53150
created_at: 2026-07-08T22:27:05-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/14
session_transcript: claude-app:cce2dec4-70fb-48fa-b215-e794254850a0
---

# Summary

Address two copilot-pull-request-reviewer comments on PR #14
(WI-SCENARIO-DISTILL-INVOCATION): angle-bracket placeholders in the
`acceptance:` YAML list would be parsed as HTML tags by GitHub's markdown
renderer, and the acceptance criteria's not-found error message was
inconsistent with the message shape specified in Required Changes.

# Result

Both comments passed triage (present, valid, feasible) and were fixed:

1. Quoted/backtick-wrapped the `<id>` / `<bogus-id>` placeholders in three
   `acceptance:` YAML list items (previously bare angle brackets).
2. Reconciled the not-found error message wording in both the YAML
   `acceptance:` list and the body `## Acceptance Criteria` section to state
   the message names the searched root, matching Required Changes' actual
   `LiterateDiscoveryError(f"No scenario '{scenario}' found under {root}")`
   shape, instead of the narrower literal string quoted before.

Both fixes applied to `project/work_items/proposed/WI-SCENARIO-DISTILL-INVOCATION.md`
only; no other files touched.

# Validation

- `git rev-parse HEAD` / `git status --short` — confirmed only the work item
  file was modified before and after the fix.
- `python -c "yaml.safe_load(...)"` — confirmed the edited `acceptance:`
  YAML list still parses correctly after quoting.
- `scripts/version tools` — not present in this repo; skipped.
- `scripts/format --check --diff` — reported 14 files needing reformatting;
  none are files this change touched (only the `.md` work item file was
  modified). Confirmed pre-existing, unrelated drift (likely a `black`
  version mismatch — local `black 26.3.1` vs. whatever produced the
  committed formatting; `pyproject.toml` does not pin a `black` version).
  Not fixed here — out of scope for this review response.
- `scripts/lint` — passed, "All checks passed!"
- `scripts/test` — passed, 57 tests, 0 failures.
- `lrh validate` — 1 pre-existing error (`focus/current_focus.md` missing),
  unrelated to this change; 0 errors attributable to this file.

# Follow-up

- The pre-existing `scripts/format --check --diff` drift across 14 files
  (unrelated to this PR) is not tracked by any work item yet; worth a
  separate item if it starts blocking CI.
