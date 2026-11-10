---
execution_id: 2026_11_10_21_58_19_OPENAI_CLIENT_TIMEOUT
prompt_id: PROMPT(AD_HOC:OPENAI_CLIENT_TIMEOUT)[2026-11-10T21:58:19+00:00]
work_item: AD_HOC
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/142
commit: fdab8e88e38db14b0952dab6575c2d74b0905478
created_at: 2026-11-10T21:58:19+00:00
agent: claude_app
instruction_source: "ad_hoc conversation — /lrh-pr-triage recommended closing PR #25 (obsolete: targeted a pre-layout-migration path) and re-opening a fresh fix against the still-live issue at its current location; user approved proceeding"
session_transcript: claude-app:0a4099db-6380-4f7b-86e5-f652e0c70455
---

# Summary

Add a timeout to the OpenAI client construction in
`src/prosoc/nca/auditor/openai_client.py`'s `OpenAIClient.__init__`: a
hung network call could previously block indefinitely, since
`openai.OpenAI(...)` was constructed with no `timeout`. Re-does the fix
originally proposed in PR #25 (`xenotaur/prosoc`), which targeted the
pre-layout-migration path `prosoc/auditor/openai_client.py` and is now
closed as obsolete — ported here to the module's current location.

Prior-art check: duplication search found no existing timeout handling
anywhere in `src/prosoc/nca/auditor/`; demand search found no open
WI/proposal requesting this — tracked only in the now-closed PR #25.
Verdict: proceed.

# Result

- `src/prosoc/nca/auditor/openai_client.py`: `OpenAIClient.__init__` now
  accepts `timeout: float = 60.0` and passes it through to
  `openai.OpenAI(...)`, with a one-line comment explaining the rationale
  (matching PR #25's original diff shape).
- `tests/nca/auditor/openai_client_test.py`: added
  `test_default_timeout_is_passed_to_openai_constructor` and
  `test_explicit_timeout_overrides_default`, both asserting against the
  already-mocked `OpenAI` constructor's `call_args` — confirmed (by both
  this session and the self-review subagent, independently) to fail
  against the unfixed code.
- Closed PR #25 with an explanatory comment (obsolete target path, but
  the issue it described is still live).
- PR: https://github.com/xenotaur/prosoc/pull/142

# Validation

- `PYTHONPATH="$(pwd)/src" scripts/test` — 394 tests, `OK (skipped=1)`,
  with the fix. Confirmed the two new tests are genuine regression tests
  via a tagged-stash revert-and-restore cycle of `openai_client.py` alone:
  both failed (`KeyError`/`TypeError`) against the unfixed code, all other
  tests unaffected.
- `scripts/lint` — all checks passed.
- `lrh validate` — 0 errors, 20 pre-existing warnings (unchanged from
  baseline).
- See `2026_11_10_22_05_06_OPENAI_CLIENT_TIMEOUT_SELFREVIEW.md` for the
  Step 7.5 cold-context review and its independent re-verification
  findings (confirmed `timeout` is a valid `OpenAI.__init__` keyword in
  the installed `openai` 1.66.3).

# Follow-up

None scoped by this fix.
