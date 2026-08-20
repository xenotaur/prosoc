---
resolution: null
blocked_reason: null
blocked: false
id: WI-TESTS-YML-DISCOVERY-FIX
title: Fix tests.yml CI workflow to actually discover and run the test suite
type: operation
status: proposed
owner: anthony
contributors:
  - anthony
assigned_agents: []
related_focus: []
related_roadmap: []
related_workstreams: []
related_design: []
depends_on: []
blocked_by: []
expected_actions:
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - modify_ci_pipeline
acceptance:
  - .github/workflows/tests.yml's `run:` step invokes `python -m unittest discover tests "*_test.py" -v` (or equivalent), matching scripts/test's own working invocation
  - The workflow's next CI run reports the true test count (259+ as of this writing), not "Ran 0 tests in 0.000s"
  - lrh validate passes with 0 errors
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - .github/workflows/tests.yml
---

# Fix tests.yml CI workflow to actually discover and run the test suite

## Summary

`.github/workflows/tests.yml` runs `python -m unittest discover -v` with no `--pattern` flag, so it uses the default `test*.py` glob — which never matches this repo's actual `*_test.py`-suffixed test files. CI has been silently discovering and running zero tests on every push, always reporting "pass," regardless of whether the test suite itself is actually green.

## Problem / Context

The `tests` CI check has read as green on every PR in this repo's history, but it has never actually exercised the test suite: `python -m unittest discover` defaults to the `test*.py` glob (prefix match), while every test file in this repo is named `<name>_test.py` (suffix match) — a pattern mismatch that means zero test modules are ever discovered. The gap was found and independently confirmed twice during `WI-NCA-PRNC-PACKAGE-LAYOUT`'s landing (PR #95): once directly in this session (`gh run view` on the workflow's own run showing `Ran 0 tests in 0.000s`, reproduced identically on `main`'s tip from before that PR even started), and once by a cold-context `/lrh-self-review` subagent dispatched independently against the same PR, which flagged it as a "dead/no-op CI job" unrelated to that migration. The local `scripts/test` wrapper already invokes the discovery correctly (`python -m unittest discover tests "*_test.py"`) — the workflow just never matched it.

This needs fixing now because CI's `tests` check is currently pure theater: it cannot catch a real test regression, and every PR merged through this repo's history has relied on `scripts/test` being run locally (if at all) rather than on CI actually verifying it.

### Duplication search
- In-repo: No existing implementation found.
- Sibling repos: None identified.
- External libraries: None identified — this is a one-line CI invocation fix, not a library capability.
- Recommendation: Proceed.

### Demand search
- Work items: None found.
- Proposals: None found.
- Backlog: No matching entries.
- Recommendation: No action beyond implementing this fix.

## Scope

- Fix `.github/workflows/tests.yml`'s test-discovery invocation so it actually runs the suite.
- Verify the fix by observing a real test count on the next CI run.

## Required Changes

1. Update `.github/workflows/tests.yml`'s `Run unit tests` step from `python -m unittest discover -v` to `python -m unittest discover tests "*_test.py" -v` (or the equivalent explicit `--pattern`/`--start-directory` flags), matching `scripts/test`'s own working invocation.
2. Push and observe the workflow's next run reports a real test count, not `Ran 0 tests in 0.000s`.

## Non-Goals

- Does not add new tests or change test coverage — this fixes CI's ability to run the existing suite, not the suite itself.
- Does not change `scripts/test` (already correct) or any other CI workflow.
- Does not add required-status-check branch protection — this repo currently has none; that's a separate decision.

## Acceptance Criteria

- `.github/workflows/tests.yml`'s test-discovery command matches `scripts/test`'s working pattern.
- The workflow's next CI run on this PR reports the true test count (259+ as of this writing) and passes/fails based on real results.
- `lrh validate` reports 0 errors.

## Validation

- `lrh validate`
- `scripts/test` (confirm the same invocation works locally before pushing the workflow change)
- Inspect the PR's own `tests` CI check run and confirm it reports a non-zero test count

## Risk Notes

- Low risk: a one-line CI config change. The main risk is that fixing discovery surfaces a real, previously-masked test failure — if so, that failure should be triaged and either fixed or explicitly tracked, not papered over by reverting this fix.

## Related Workstream and Designs

- None — this is a standalone CI-hygiene fix surfaced during `WI-NCA-PRNC-PACKAGE-LAYOUT`'s landing (PR #95), not part of any existing workstream.
