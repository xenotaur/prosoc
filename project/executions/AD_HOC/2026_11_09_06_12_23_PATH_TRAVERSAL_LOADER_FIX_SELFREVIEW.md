---
execution_id: 2026_11_09_06_12_23_PATH_TRAVERSAL_LOADER_FIX_SELFREVIEW
prompt_id: PROMPT(AD_HOC:PATH_TRAVERSAL_LOADER_FIX_SELFREVIEW)[2026-11-09T06:12:17+00:00]
work_item: AD_HOC
status: landed
rerun_of: 2026_11_09_06_14_12_PATH_TRAVERSAL_LOADER_FIX
pr: https://github.com/xenotaur/prosoc/pull/140
commit: 14119c38c25562b17b551b91dc6c13a07f311e43
created_at: 2026-11-09T06:12:23+00:00
agent: claude_app
instruction_source: "ad_hoc conversation — re-doing PR #73's path-traversal fix at its current post-layout-migration location"
session_transcript: claude-app:0a4099db-6380-4f7b-86e5-f652e0c70455
---

# Summary

`/lrh-self-review` diff-mode pass (Step 7.5) on the two-file diff fixing
the HIGH-severity path-traversal vulnerability in
`src/prosoc/nca/packet/loader.py`'s `PacketFamily.yml_path()`, before this
change's first PR push.

# Result

Dispatched a cold-context `general-purpose` subagent against `git diff
main`. Its report: no real defect found; the fix mirrors the existing
containment-check style in `src/prosoc/nca/utils/papers/render.py`,
`ResolveError` is correctly imported, and the real corpus has no
multi-segment card ids that could false-positive. It also reasoned
(without adding a test) that absolute-path and symlink-based traversal
variants would be caught by the same `resolve()`+`relative_to()` check.

Independently re-verifying that reasoning (mandatory Step 4) surfaced two
real problems the subagent's non-empirical reasoning missed:

1. **The subagent's own empirical checks ran against a stale global
   `prosoc` editable install**, not this worktree — the same silent
   failure mode already in agent memory
   (`prosoc_pythonpath_stale_editable_install`). `python3 -c "import
   prosoc; print(prosoc.__file__)"` resolved to an unrelated checkout
   (`.../CharterReconciliation/prosoc`) pinned at an old commit. Every
   bare `python3 -c` sanity check — mine and, going by its report's
   phrasing, likely the subagent's "verified empirically" claims too —
   needs `PYTHONPATH="$(pwd)/src"` to actually exercise this worktree's
   code.
2. **The originally committed regression test
   (`test_card_id_path_traversal_is_rejected`) was not a true regression
   test.** It called `load_card("scenarios", "../../etc")` and asserted
   `ResolveError`, but `load_card`'s own *separate* "no card" check also
   raises `ResolveError` whenever the resolved path doesn't exist on disk
   — which `../../etc/scenario.yml` never does, fix or no fix. Confirmed
   by temporarily reverting only `loader.py` (via a tagged `git stash`,
   restored via `apply`+`drop`, never bare `pop`) and re-running the test
   under the correct `PYTHONPATH`: it still passed `ok` against the
   *unfixed* code, meaning it was testing the symptom (an exception
   raised) rather than the actual containment mechanism.

Fixed both: rewrote the test to call `FAMILIES["scenarios"].yml_path(...)`
directly (bypassing `load_card`'s confounding existence check), and added
a second test for the absolute-path case the subagent only reasoned
about (`Path.__truediv__` discards the left operand when the right is
absolute, so `self.root / "/etc"` collapses to `/etc` — a second, distinct
way to escape `self.root` that needs the same guard). Re-verified both
new tests independently: they **fail** against unfixed `loader.py` and
**pass** against the fix, under `PYTHONPATH="$(pwd)/src"` — genuine
regression tests, not restatements of the diff's own claims.

# Validation

- `PYTHONPATH="$(pwd)/src" scripts/test` — 392 tests, `OK (skipped=1)`,
  with the fix in place.
- Same command with only `loader.py` temporarily reverted (test file
  unchanged) — `FAILED (failures=2, skipped=1)`, exactly the two new
  traversal tests, confirming they are real regression tests and nothing
  else regressed.
- `scripts/lint` — all checks passed (static; unaffected by the
  `PYTHONPATH` issue).
- `lrh validate` — 0 errors, 20 pre-existing warnings (unaffected; matches
  the pre-change baseline — `lrh validate` does not import `prosoc` per
  agent memory).

# Follow-up

None for this fix. The underlying stale-editable-install environment issue
is pre-existing and already tracked in agent memory
(`prosoc_pythonpath_stale_editable_install`); this record reconfirms it
and additionally notes that it can silently invalidate a self-review
subagent's own "verified empirically" claims, not just `scripts/distill`
and `scripts/test` run bare.
