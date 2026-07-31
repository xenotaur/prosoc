---
execution_id: 2026_07_31_18_54_54_WI_CARD_APPROVE_SKILLS_IMPL_REVIEW
prompt_id: PROMPT(AD_HOC:WI_CARD_APPROVE_SKILLS_IMPL_REVIEW)[2026-07-31T16:44:52+00:00]
work_item: AD_HOC
status: in_progress
rerun_of: 2026_07_31_09_20_16_WI_CARD_APPROVE_SKILLS
pr: https://github.com/xenotaur/prosoc/pull/64
commit: 13ecd9a
created_at: 2026-07-31T18:54:54+00:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/64
session_transcript: pending
---

# Summary

Review-response pass for PR #64 (WI-CARD-APPROVE-SKILLS implementation).
Copilot posted a full review with 5 inline findings on the PR's first
commit (`ec751c4`) at 09:24:06Z -- discovered late, after an initial
polling pass incorrectly scoped its `since` filter to only the *second*
commit's push time (09:33:25Z), missing the review that had already landed
on the first. Caught only when the user asked me to double-check; flagged
to the user as my own process error before proceeding.

# Result

All 5 findings from `copilot-pull-request-reviewer`, all valid, present,
and fixed:

1. `review_queue.py:115` (`_read_audit`) -- `int(...)` casts on
   `blocking`/`should_fix`/`suggestion` could raise `ValueError`/`TypeError`
   on non-numeric frontmatter scalars, crashing queue generation instead of
   failing closed like the rest of the function. **Fixed**: wrapped the
   three casts in a `try`/`except (TypeError, ValueError)` that returns the
   same "no audit" tuple as every other malformed-frontmatter case.
2. `review_queue.py:246` (`main`) -- `--order` longer than `--sort` made
   `sort_queue()`'s `orders` list longer than `keys`, which could crash via
   `zip(..., strict=True)` and would let a user-supplied direction leak
   into the supposedly-always-ascending `(family, id)` tiebreak. **Fixed**:
   added an explicit `parser.error(...)` check in `main()` rejecting
   `len(order_dirs) > len(sort_fields)`, plus a docstring note on
   `sort_queue()` stating this is a caller precondition, not something the
   function itself guesses at.
3. `review_queue_test.py` (two integration tests) -- hardcoded the corpus
   size (`32`), which would break as the corpus grows/shrinks even with
   correct logic. **Fixed**: added `_expected_corpus_size()`, an
   independent oracle that sums each family's raw `discover()` results
   directly (not reusing `build_queue()`'s own count), and used it in place
   of the literal `32` in both tests.
4. No test covered the malformed-scalar case from finding #1. **Fixed**:
   added `test_non_numeric_scalar_reports_no_audit_instead_of_raising`.
5. No test covered the `--order`-longer-than-`--sort` case from finding
   #2. **Fixed**: added `test_main_rejects_order_longer_than_sort`.

Thread resolution is `/lrh-confirm-fixes`'s job per this skill's own
"What This Skill Does Not Do" -- the 5 threads remain open, to be resolved
during the confirm-fixes pass against this commit's diff.

# Validation

- `python -m unittest tests.utils.cards.review_queue_test` -- 31 tests
  (29 prior + 2 new), OK.
- `scripts/test` -- full suite, 236 tests, OK.
- `scripts/lint` -- all checks passed.
- `black --check` scoped to the two touched files -- clean (repo-wide
  `scripts/format --check` still reports pre-existing, unrelated drift from
  the local-vs-CI `black` version mismatch already on record).
- `lrh validate` -- 0 errors, 0 warnings.

# Follow-up

- Next: `/lrh-confirm-fixes` to verify these fixes against the current
  diff and resolve the 5 review threads before merge.
- Process note: the `since`-timestamp scoping bug that caused the missed
  review is worth a session memory once this PR lands -- a review-response
  poll should check activity since the *PR's original push*, not just the
  most recent commit, unless it has already confirmed no earlier review
  exists.
