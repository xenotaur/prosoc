---
execution_id: 2026_07_25_22_43_16_WI_CARD_STATUS_TASKS_IMPL_REVIEW
prompt_id: PROMPT(AD_HOC:WI_CARD_STATUS_TASKS_IMPL_REVIEW)[2026-07-25T22:40:55-04:00]
work_item: AD_HOC
status: landed
rerun_of: 2026_07_25_22_35_49_WI_CARD_STATUS_TASKS
pr: https://github.com/xenotaur/prosoc/pull/42
commit: 3fd3f997618f14856455da22ca278a6d567b5553
created_at: 2026-07-25T22:43:16-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/42
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Addressed four Copilot review comments on PR #42 (implementation of
WI-CARD-STATUS-TASKS), all valid correctness/quality/coverage findings.

`rerun_of` points at the **implementation** primary
(`2026_07_25_22_35_49_...`, PR #42, work-item bucket), disambiguated from the
same-slug work-item-*creation* primary (`2026_07_25_22_02_30_...`, PR #41,
AD_HOC) by `pr:` / bucket.

# Result

- [r3651588315](https://github.com/xenotaur/prosoc/pull/42#discussion_r3651588315)
  — `project_state_into_markdown` rewrote the whole STATE line, stripping the
  two trailing spaces task cards use for Markdown line breaks (so `--fix` would
  churn formatting). Fixed: the STATE regex now captures `prefix`/`suffix`
  groups and projection swaps only the state token, preserving trailing
  whitespace (verified on a real task card: `DRAFTED␠␠` → `APPROVED␠␠`).
- [r3651588323](https://github.com/xenotaur/prosoc/pull/42#discussion_r3651588323)
  — the flat-layout failure printed to stdout while other failures used stderr.
  Fixed: all failure messages now go to stderr; only `ok`/`fix` progress lines
  stay on stdout.
- [r3651588324](https://github.com/xenotaur/prosoc/pull/42#discussion_r3651588324)
  — with `--card` and no match, the CLI said "no cards found under {root}",
  misleading when the root has other cards. Fixed: a distinct
  "no card '<id>' found" error (noting other cards exist).
- [r3651588329](https://github.com/xenotaur/prosoc/pull/42#discussion_r3651588329)
  — the uppercase-heading fixture claimed to cover trailing whitespace but had
  none. Fixed: the fixture now carries real trailing spaces (via explicit
  escapes, so the source line has none), plus a
  projection-preserves-trailing-whitespace test and a `--card` no-match test.

All four passed presence/validity/feasibility triage; nothing was skipped.

# Validation

- `scripts/format --check`: clean.
- `scripts/lint`: All checks passed.
- `scripts/test`: 129 passed (+2 new regression tests).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 24 cards consistent.

# Follow-up

- Suggest `/lrh-confirm-fixes` on PR #42 before merge to resolve the four
  review threads.
