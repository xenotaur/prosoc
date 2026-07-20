---
execution_id: 2026_07_20_00_33_14_AUDIT_FRONTMATTER_BACKFILL
prompt_id: PROMPT(AD_HOC:AUDIT_FRONTMATTER_BACKFILL)[2026-07-20T00:32:22-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/23
commit: 
agent: claude_app
instruction_source: ad_hoc conversation — user asked whether the missing frontmatter block across all 20 scenario audit.md files (discovered while analyzing options for a post-render human-work summary) could be backfilled automatically, then asked for it as its own small PR
session_transcript: pending
created_at: 2026-07-20T00:33:14-04:00
---

# Summary

Backfill the `scenario`/`verdict`/`blocking`/`should_fix`/`suggestion`/
`audited` frontmatter block that `prosoc-scenario-audit`'s `SKILL.md`
documents and `prosoc-scenario-audit-all`'s aggregation step parses, into
all 20 existing `audit.md` files, none of which had it (the original
full-corpus audit run in PR #4 predates the convention).

# Result

- Parsed each `audit.md`'s existing `### N. <title> — <severity>` finding
  headings (excluding `RETRACTED` ones) to derive `blocking`/`should_fix`/
  `suggestion` counts, and its `**Verdict:**` line (three unambiguous
  prefixes: `"Ready for AUDITED with minor fixes..."` →
  `ready_with_fixes`, `"Ready, no blocking issues found"` → `ready`,
  `"Not ready..."` → `not_ready`) and `**Audited:**` line for the date.
- Wrote a one-off Python script (not committed — a throwaway backfill, not
  reusable tooling) that prepends the derived frontmatter block to each
  file, leaving every other line untouched.
- Verified via `git diff` that each of the 20 files changed by exactly 9
  lines (frontmatter + trailing blank line) — no prose, findings, or
  Correction Notice content touched anywhere.
- Cross-validated every derived count and verdict against
  `prosoc/scenarios/AUDIT_SUMMARY.md`'s already-published table before
  committing: all 20 rows matched exactly, zero discrepancies — strong
  independent confirmation the parse is correct, not just self-consistent.

# Validation

- `scripts/lint` — all checks passed
- `scripts/format --check --diff` — clean, 43 files unchanged
- `scripts/test` — 80 tests OK (unchanged; no Python source touched)
- `lrh validate` — 1 pre-existing error (`focus/current_focus.md` not
  found), unrelated; 0 errors attributable to this change
- Manual cross-check of all 20 derived frontmatter blocks against
  `AUDIT_SUMMARY.md`'s table — 100% match

# Follow-up

- This unblocks a future `/prosoc-scenario-audit-all` run (full or
  scoped to a subset) from correctly aggregating existing `audit.md`
  files instead of falling back to `"unparseable — needs re-audit"` for
  all of them.
- `session_transcript: pending` should be updated to
  `claude-app:<session-id>` after this session ends.
