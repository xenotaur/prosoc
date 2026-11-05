---
execution_id: 2026_11_05_21_28_45_WI_CHARTER_SUPPLEMENT_COPYEDIT_FIXES_REVIEW
prompt_id: PROMPT(AD_HOC:WI_CHARTER_SUPPLEMENT_COPYEDIT_FIXES_REVIEW)[2026-11-05T21:28:38+00:00]
work_item: AD_HOC
status: in_progress
rerun_of: 2026_11_05_21_19_43_WI_CHARTER_SUPPLEMENT_COPYEDIT_FIXES
pr: https://github.com/xenotaur/prosoc/pull/129
commit:
created_at: 2026-11-05T21:28:45+00:00
agent: claude-code
instruction_source: https://github.com/xenotaur/prosoc/pull/129
session_transcript: pending
---

# Summary

`/lrh-review-response` pass for PR #129: one open Copilot review comment
(Medium severity, "Changes recommended") on commit `79d334b`.

# Result

- **Comment**: `extract_pdf_text()` uses `pdftotext -layout`, which
  preserves line breaks and layout spacing. A multi-word stale-wording
  substring (e.g. "no external literature yet exists that could cite
  it") can straddle a line wrap, silently evading
  `check_stale_supplement_wording()`'s plain substring search and
  letting `build_pdf()` succeed despite a reverted copyedit. Requested:
  normalize whitespace before matching, and cover a wrapped phrase in
  the regression tests (the existing tests only exercise contiguous
  strings).
- **Triage**: Presence -- confirmed present (the function had no
  whitespace normalization). Validity -- confirmed valid: this is a
  genuine false-negative in a check I added this same PR, specifically
  undermining its own stated purpose. Feasibility -- feasible: a
  one-line whitespace-collapse fix plus one new test.
- **Fix**: added a `_WHITESPACE_RUN_RE = re.compile(r"\s+")` and applied
  `.sub(" ", pdf_text)` before the substring search in
  `check_stale_supplement_wording()`. Added
  `test_detects_phrase_wrapped_across_a_pdftotext_line_break`, using the
  reviewer's own example phrase split across a line break with
  continuation-line indentation, to `TestStaleSupplementWording`.
- Identity confirmed before editing: local `HEAD` (`794cc96`) matched
  the PR's reported `headRefOid` exactly.

# Validation

- `PYTHONPATH="$(pwd)/src" python -m unittest tests.nca.utils.papers.render_test -v`
  -- all pass, including the new wrapped-phrase test.
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
  -- 344 tests, `OK (skipped=1)`.
- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- `scripts/lint` -- all checks passed. `scripts/format --check` on the
  2 touched files -- clean (the pre-existing 22-file repo-wide drift is
  unaffected, neither touched file is in that list).
- A real `PYTHONPATH="$(pwd)/src" papers/01_charter/render.py --pdf`
  build re-run after the fix -- succeeds cleanly, no regression-check
  `RuntimeError`.
- **Publication outcome: Pushed directly** -- `git push` succeeded as
  commit `2da4591` on `xenotaur/feat/wi-charter-supplement-copyedit-fixes`.

# Follow-up

None blocking. Thread resolution (if any GitHub review thread exists
for this comment) is `/lrh-confirm-fixes`'s job, not this skill's.
