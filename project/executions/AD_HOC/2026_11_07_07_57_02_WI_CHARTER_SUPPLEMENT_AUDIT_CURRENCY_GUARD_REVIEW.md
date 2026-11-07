---
execution_id: 2026_11_07_07_57_02_WI_CHARTER_SUPPLEMENT_AUDIT_CURRENCY_GUARD_REVIEW
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_AUDIT_CURRENCY_GUARD_REVIEW)[2026-11-07T07:56:57+00:00]
work_item: AD_HOC
status: landed
rerun_of: 2026_11_07_07_05_00_WI_CHARTER_SUPPLEMENT_AUDIT_CURRENCY_GUARD
pr: https://github.com/xenotaur/prosoc/pull/137
commit: 70c51fba846ca319731bcde2d48f461018814564
created_at: 2026-11-07T07:57:02+00:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/137
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Review-response pass for PR #137: 6 Copilot findings, all substantive
and all confirmed real by independent reproduction before fixing (one
very severe -- a shallow-clone boundary misattribution that would have
silently defeated the guard entirely wherever it runs in a shallow
checkout).

# Result

All 6 findings triaged present/valid/feasible and fixed; none skipped.
Each independently reproduced against real data before fixing (not
accepted from the review comments alone):

1. **Shallow-clone boundary misattribution.** Reproduced with a real
   `git clone --depth 1` of a disposable 3-commit repo: `git log -1 --
   audit.md` incorrectly returned the shallow boundary commit (which
   never touched `audit.md`) as its last-touching commit, which would
   compare the card's current content against itself. Fixed by reading
   `<git-dir>/shallow` and treating a match as "no reliable reference."
2. **Block-boundary masking could swallow real content.** Reproduced:
   `_mask_lifecycle_surface` dropped a Markdown heading that immediately
   followed the last history bullet with no blank line in between.
   Replaced the pattern-based continuation heuristic with an
   indentation-based one -- also subsumes and improves on my own prior
   self-review fix for a narrower version of this same bug class.
3. **YAML `state:` masking matched prose inside unrelated block
   scalars.** Reproduced: a line reading `state: blocked` inside a
   different field's block scalar got masked right along with the real
   lifecycle field. Fixed by making the match family-aware (exact
   column 0 for flat families, exact 2-space indent for root-wrapped),
   mirroring `read_yaml_state`'s existing `root_key` parameter.
4. **The guard never checked the distilled YAML, only the Markdown** --
   against the work item's own acceptance criteria, which name
   "Markdown or distilled YAML" explicitly. Added a second, independent
   comparison (state field removed) reusing the same git-history helper
   for the `*.yml` path.
5. **`FileNotFoundError` if `git` isn't on `PATH`** would have aborted
   the whole validator run. Wrapped in `try/except OSError`.
6. **An inline YAML comment on the state line defeated masking
   entirely** -- reproduced: `state: AUDITED # reviewed` didn't match at
   all, leaving the whole line unmasked. Fixed to mask only the value
   token, preserving the comment.

Also fixed in the same pass, newly relevant now that the check runs
twice per card: `_check_extras` now skips the git lookups entirely for
cards below `AUDITED`.

# Validation

- Each finding reproduced directly against real inputs (a real `git
  clone --depth 1`, real crafted Markdown/YAML) before fixing, and
  re-verified after.
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
  -- 390 tests, 0 failures, 1 pre-existing skip.
- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- `scripts/lint` and `black --check` (pinned `25.12.0`) -- clean.
- Full corpus `scripts/validate/status` (no `--family`) -- 32/32 cards
  consistent.
- **Publication outcome: Pushed directly** -- to
  `xenotaur/feat/wi-charter-supplement-audit-currency-guard` on
  `xenotaur/prosoc#137`.

# Follow-up

None blocking. Thread resolution is `/lrh-confirm-fixes`'s job, not
this record's.
