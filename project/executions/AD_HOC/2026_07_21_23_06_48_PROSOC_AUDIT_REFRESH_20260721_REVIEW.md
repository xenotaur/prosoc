---
execution_id: 2026_07_21_23_06_48_PROSOC_AUDIT_REFRESH_20260721_REVIEW
prompt_id: PROMPT(AD_HOC:PROSOC_AUDIT_REFRESH_20260721_REVIEW)[2026-07-21T22:53:30-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/29
commit: 91ba2a5
created_at: 2026-07-21T23:06:48-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/29
session_transcript: pending
---

# Summary

Address 5 open `copilot-pull-request-reviewer` comments on
[xenotaur/prosoc#29](https://github.com/xenotaur/prosoc/pull/29) (the
corpus-wide audit refresh after PR #28), via `/lrh-review-response`.

# Result

Triaged the 5 comments into one root cause plus a drive-by fix, all valid
and feasible:

1. **Relative path typo in `crash_cart/audit.md`** (2 comments) —
   `../../.claude/skills/_shared/pg_scenarios.md` would resolve under
   `prosoc/scenarios/.claude/`, which doesn't exist. Fixed both occurrences
   to the repo-root path `.claude/skills/_shared/pg_scenarios.md`, matching
   the convention already used by several sibling `audit.md` files. Also
   fixed the identical, unflagged typo in `blind_corner/audit.md` (same PR,
   same bug class, in scope).
2. **`crash_cart`'s Finding 1 mischaracterized the `related_scenarios`
   divergence as a should-fix "source-fidelity mismatch"/"silent
   substitution"** (1 comment) — but the field is schema-defined as
   corpus-directory names, not a Table 3 transcription, and the card's own
   Notes section already documents both `object_handover` and the
   unimplemented "Food Delivery" by name, so nothing is silent. Rewrote
   Finding 1 to match the established `suggestion`/"no action required now"
   framing already used for the identical pattern in `join_a_group` and
   `leading`; updated frontmatter (`should_fix: 1->0`, `suggestion: 1->2`,
   `verdict: ready_with_fixes->ready`) and the Source Fidelity table row
   and every downstream cross-reference to Finding 1 accordingly.
3. **`crash_cart`'s "Verdict Rationale" said "ready for AUDITED" while
   frontmatter said `ready_with_fixes`** (1 comment) — resolved as a
   side-effect of (2): verdict is now `ready` with a matching rationale
   line, no more contradiction.
4. **`AUDIT_SUMMARY.md` was internally inconsistent** — it called the
   related-scenarios-vs-Table-3 divergence "expected, not a defect" while
   `crash_cart` counted it as should-fix (1 comment) — updated the
   `crash_cart` row (`ready_with_fixes,0,1,1` -> `ready,0,0,2`), the totals
   (`ready` 12->13, `ready_with_fixes` 6->5, should-fix 6->5, suggestion
   24->25), and strengthened the "Manual reading" section to note all
   three numbered instances (`crash_cart`, `join_a_group`, `leading`) are
   now consistently treated as suggestion-severity, no-action-needed
   findings.

No comments were skipped.

# Validation

- `git rev-parse HEAD` (pre-fix): `c9774c538ba13b4f91e3a00a5cb0b95122400b12`
- `scripts/version tools`: unavailable (no such script in this repo)
- `scripts/format --check --diff`: pass, 43 files unchanged
- `scripts/lint`: pass, all checks passed
- `scripts/test`: pass, 80 tests OK
- `lrh validate`: 1 pre-existing error (`focus/current_focus.md` missing --
  known repo-wide gap, unrelated to this change)

# Follow-up

The "table names an unimplemented scenario" pattern (now `crash_cart`,
`join_a_group`, `leading`, plus informational mentions elsewhere) is still
only resolved case-by-case with matching prose; `AUDIT_SUMMARY.md` itself
notes it's worth a single documented convention (e.g. an `evaluation_notes`
note pattern) rather than re-deriving the reasoning per scenario as more
scenarios get implemented. Not actioned in this pass.
