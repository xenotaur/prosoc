---
execution_id: 2026_11_07_07_05_00_WI_CHARTER_SUPPLEMENT_AUDIT_CURRENCY_GUARD
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD:WI_CHARTER_SUPPLEMENT_AUDIT_CURRENCY_GUARD)[2026-11-07T06:43:14+00:00]
work_item: WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/137
commit:
created_at: 2026-11-07T07:05:00+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implements `WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD`: a git-history
audit-currency check in `scripts/validate/status`, closing the gap
`PROP-NORMATIVE-CARD-APPROVAL` Decision 5 deferred.

# Result

- Designed and confirmed the approach with the human before implementing
  (per the work item's own risk notes): mask the lifecycle-tracking
  surface from both the card's current Markdown and its content as of
  the commit that last touched its `audit.md`, then compare for exact
  equality -- not a timestamp comparison, which was confirmed to fail
  for both the provenance-backfill case and every ordinary promotion
  commit.
- Implemented `status._mask_lifecycle_surface` /
  `status.check_audit_currency` (pure) and a new
  `prosoc.nca.utils.cards.git_history` module (the one git subprocess
  call this needs, isolated so `status.py` stays pure). Wired into
  `validate_status._check_extras` alongside the existing audit-evidence
  check. Refactored `audit_path_for` out of `check_audit_evidence` so
  both checks agree on which file is "the" audit.
- Validated the design against two real historical cases before writing
  any code: PR #128's `routine_delivery` backfill, and this session's
  own `deliver_object` promotion diff (`24e5aad..4c7ab6c`) -- both
  mask-equal, confirmed correctly not stale.
- Running the new check against the full corpus surfaced two genuine,
  previously-undetected stale cards outside this workstream's original
  9: `routine_delivery` and `guidance_docent`, both drifted by a
  2026-10-27 formatting commit (`WI-CHARTER-SUPPLEMENT-SOURCE-FIXES`,
  PR #112) with no `EDITED:` bullet or re-audit at the time. Confirmed
  with the human this was a real finding, not a bug; fixed both through
  the same demote -> audit -> promote cycle (4 live human-confirmation
  gates) used throughout this workstream, including two small
  should-fix findings caught during re-audit (a common-tensions wording
  drift; a `primary_robot_role` prose/YAML mismatch).

# Validation

- Pure masking/comparison unit tests (no git) in `status_test.py`.
- Git-history helper unit tests in new `git_history_test.py`, using
  disposable temp git repos created fresh per test (never the real
  prosoc repo).
- Full end-to-end integration tests in `validate_status_test.py`
  covering all three of the work item's required cases (genuinely
  stale, provenance-backfill-only, ordinary-promotion-only) plus the
  no-git-repo skip path.
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
  -- 370 tests, 0 failures, 1 pre-existing skip.
- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- `scripts/lint` (ruff) and `black --check` (pinned `25.12.0`, installed
  in an isolated venv since this machine's global `black` is a newer,
  incompatible version) -- clean.
- Full corpus `scripts/validate/status` (no `--family`) -- 32/32 cards
  consistent.
- Directly verified the check actively engages (not silently skipping)
  against the already-merged `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`
  cards' real committed git history (e.g. `frontal_approach`'s audit.md
  at commit `4c7ab6c`), not just the two newly-fixed cards.

# Follow-up

None blocking. Once this PR merges, resolve
`WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD` and close
`WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY` -- this is the workstream's
last work item.
