---
execution_id: 2026_10_27_15_06_37_WI_CHARTER_SUPPLEMENT_SOURCE_FIXES_CONFIRM
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-SOURCE-FIXES:WI_CHARTER_SUPPLEMENT_SOURCE_FIXES_CONFIRM)[2026-10-27T06:43:16+00:00]
work_item: WI-CHARTER-SUPPLEMENT-SOURCE-FIXES
status: landed
rerun_of: 2026_10_27_06_40_09_WI_CHARTER_SUPPLEMENT_SOURCE_FIXES
pr: https://github.com/xenotaur/prosoc/pull/112
commit: 906890aa1be2626ae2e886047e63ff09f21802b1
created_at: 2026-10-27T15:06:37+00:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/112 (confirm-fixes pass)
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Pre-merge confirm-fixes pass for PR #112. An initial read found 0
threads (nothing had landed yet); a Copilot review landed moments later
with 2 real inline findings, which this record's commit was updated to
reflect and resolve — amended in place rather than spawning a parallel
`_CONFIRM` record for the same round, per this repo's established
practice.

# Result

Initial authoritative check (`lrh github threads --mode raw --state
all`) found 0 threads — read before any review had landed (a real race:
the review posted ~25s after the implementation push). Branch-rules
check confirmed no `required_status_checks` rule on `main` (count 0), so
CI was read via the unfiltered `gh pr checks` form: `check-charter`,
`lint`, `check-packet-drift`, and `test` all `SUCCESS`.

A re-check surfaced a Copilot review with 2 new inline threads:
`frontal_approach/scenario.yml:91` and
`movable_obstruction/scenario.yml:101–102` both still contained stale
`prosoc/<family>/` paths — the Markdown-level path fixes in
`WI-CHARTER-SUPPLEMENT-SOURCE-FIXES`'s primary commit edited the
*embedded* YAML inside the `.md` source, but the *distilled* `.yml`
siblings (which the packet loader actually reads) were never
regenerated. Both **Clear-satisfied** on inspection — directly confirmed
via `grep` that the stale paths were still present in the `.yml` files.

Regenerating required discovering and working around a real environment
hazard: this machine's global `prosoc` pip editable install points at an
unrelated, stale clone
(`.../CharterReconciliation/prosoc`, pinned at commit `e029fe4`, predating
even PR #111) rather than this worktree — confirmed via `python3 -c
"import prosoc; print(prosoc.__file__)"`. Plain `scripts/distill/scenarios`
silently distills *that* checkout's already-consistent files and reports
no diff. Worked around locally with `PYTHONPATH="$(pwd)/src"` prefixed
on every `prosoc`-importing command for the rest of this round (distill,
`lrh validate`, `scripts/test`, `scripts/lint`, `render.py`) — all
re-verified clean against the correctly-scoped package. Regenerated both
`.yml` files via `PYTHONPATH="$(pwd)/src" python3 -m
prosoc.prnc.scenarios.distill`, confirmed the resulting diff was exactly
the two path corrections (no unrelated content drift), committed
(`36599e2`), and resolved both threads via `resolveReviewThread`.

Thread-resolution verdict: **Green** — both threads resolved, no
exceptions remain open.

# Validation

- `lrh github threads --mode raw --state all` — 2 threads found after
  the review landed, both resolved (`isResolved: true` confirmed via the
  `resolveReviewThread` mutation response).
- `gh api repos/xenotaur/prosoc/rules/branches/main` — confirmed no
  `required_status_checks` rule (count 0).
- `gh pr checks 112 --json name,state,bucket` — 4/4 `SUCCESS` (provisional read).
- Re-ran with `PYTHONPATH` correctly scoped: `lrh validate` (0 errors),
  `scripts/test` (259 tests, OK), `scripts/lint` (all checks passed),
  `papers/01_charter/render.py` (exit 0) — all against the real worktree
  content this time, not the stale global package.

# Follow-up

Step 8 (readiness report) still needs to re-fetch CI against the
post-push `HEAD` (commit `36599e2`) and check for an automatic reviewer
response (or dispatch a substitute `/lrh-self-review --pr` pass) before
the final merge-readiness verdict — this amended commit is new content
that hasn't itself been reviewed yet.

Worth a standing memory: any `prosoc`-importing command on this machine
needs `PYTHONPATH="$(pwd)/src")` (or equivalent) to target the active
worktree rather than the globally-registered stale editable install.
