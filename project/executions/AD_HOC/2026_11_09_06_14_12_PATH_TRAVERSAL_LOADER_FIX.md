---
execution_id: 2026_11_09_06_14_12_PATH_TRAVERSAL_LOADER_FIX
prompt_id: PROMPT(AD_HOC:PATH_TRAVERSAL_LOADER_FIX)[2026-11-09T05:42:28+00:00]
work_item: AD_HOC
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/140
commit: 14119c38c25562b17b551b91dc6c13a07f311e43
created_at: 2026-11-09T06:14:12+00:00
agent: claude_app
instruction_source: "ad_hoc conversation — /lrh-pr-triage recommended closing PR #73 (obsolete: targeted a pre-layout-migration path) and re-opening a fresh fix against the still-live vulnerability at its current location; user approved proceeding"
session_transcript: claude-app:0a4099db-6380-4f7b-86e5-f652e0c70455
---

# Summary

Fix the HIGH-severity path-traversal vulnerability in
`src/prosoc/nca/packet/loader.py`'s `PacketFamily.yml_path()`: a
malicious `card_id` could join outside `self.root` via a `../../`-style
relative traversal or an absolute path. Re-does the fix originally
proposed in PR #73 (`xenotaur/prosoc`), which targeted the
pre-layout-migration path `prosoc/packet/loader.py` and is now closed as
obsolete/conflicting — ported here to the module's current location, plus
the regression test its review asked for but never got.

Prior-art check: duplication search found only unrelated `yml_path`
callers (no existing fix); demand search found no open WI/proposal
requesting this — tracked only in the now-closed PR #73. Verdict:
proceed.

# Result

- `src/prosoc/nca/packet/loader.py`: `PacketFamily.yml_path()` now
  resolves the joined `root/card_id/filename` path and checks it is
  still under `self.root.resolve()` (via `.relative_to()` inside a
  try/except `ValueError`, matching the existing containment-check style
  in `src/prosoc/nca/utils/papers/render.py`'s `load_sources`), raising
  the module's existing `ResolveError` otherwise. The `single=True`
  branch (charter) is unaffected since it ignores `card_id`.
- `tests/nca/packet/loader_test.py`: added
  `test_card_id_path_traversal_is_rejected` and
  `test_card_id_absolute_path_is_rejected`, both calling
  `FAMILIES["scenarios"].yml_path(...)` directly (not `load_card`) so the
  assertion isolates the containment check from `load_card`'s separate
  "no card" `ResolveError` on a nonexistent path — see the `_SELFREVIEW`
  record for why that distinction mattered (the first draft of this test
  passed even against the unfixed code).
- Closed PR #73 with an explanatory comment (obsolete target path, but
  the vulnerability it described is still live).
- PR: https://github.com/xenotaur/prosoc/pull/140

# Validation

- `PYTHONPATH="$(pwd)/src" scripts/test` — 392 tests, `OK (skipped=1)`,
  with the fix. Confirmed the two new tests are genuine regression tests
  by temporarily reverting only `loader.py`: `FAILED (failures=2,
  skipped=1)`, exactly those two tests, nothing else.
- `scripts/lint` — all checks passed.
- `lrh validate` — 0 errors, 20 pre-existing warnings (unchanged from
  baseline).
- See `2026_11_09_06_12_23_PATH_TRAVERSAL_LOADER_FIX_SELFREVIEW.md` for
  the Step 7.5 cold-context review and its independent re-verification
  findings.

# Follow-up

None scoped by this fix. The agent-memory note
`prosoc_pythonpath_stale_editable_install` (this machine's global
`prosoc` editable install points at an unrelated stale checkout) remains
open and is reconfirmed by this session — see the `_SELFREVIEW` record.
