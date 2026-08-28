---
resolution: null
blocked_reason: null
blocked: false
id: WI-DECLARE-OPENAI-DOTENV-DEPS
title: Declare openai and python-dotenv as pyproject.toml dependencies
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
acceptance:
  - "`pip install -e .` in a fresh venv, with no separate `openai`/`python-dotenv` install, followed by `scripts/test`, reports 259/259 tests passing with 0 errors"
  - "`.github/workflows/tests.yml`'s separate `python -m pip install openai python-dotenv` line is removed as redundant, and CI still reports 259/259"
  - lrh validate passes with 0 errors
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - pyproject.toml
  - .github/workflows/tests.yml
---

# Declare openai and python-dotenv as pyproject.toml dependencies

## Summary

`src/prosoc/nca/auditor/openai_client.py` and `src/prosoc/nca/utils/secrets.py` have unconditional, module-level runtime imports of `openai` and `dotenv` respectively, but neither package is declared in `pyproject.toml`'s `dependencies` list (only `pyyaml`, `jsonschema`, `pydantic` are). Declare them so a plain `pip install -e .` — the repo's own documented dev-setup command — actually works.

## Problem / Context

Confirmed during `WI-TESTS-YML-DISCOVERY-FIX`'s implementation (PR #101) and independently re-verified by a cold-context `/lrh-self-review` subagent dispatched against that same PR: `pip install -e .` alone leaves `import openai` (in `openai_client.py:18`) and `import dotenv` (in `secrets.py:7`) unsatisfied, producing two `ModuleNotFoundError`s when the test suite runs (`tests/nca/auditor/openai_client_test.py`, `tests/nca/utils/secrets_test.py`). This gap predates `WI-TESTS-YML-DISCOVERY-FIX` — it was first documented during `WI-NCA-PRNC-PACKAGE-LAYOUT`'s landing (PR #95) as a known, pre-existing environment gap, and was worked around rather than fixed in both of those PRs (by installing the two packages ad hoc in CI's own workflow, and by manually installing them in local verification venvs) because it was out of scope for either of those work items.

The workaround means the workflow's own CI environment now diverges from what `pyproject.toml` itself declares as the package's dependencies — anyone following the repo's own README (`pip install -e .`) or installing `prosoc` as a real package outside CI still hits the same import failures. This work item closes that gap at the source.

Notably, Copilot's automated review on PR #101 independently flagged this same issue — but as a "suppressed" (collapsed, non-threaded) comment in its review body rather than an open review thread, so it was never surfaced to that PR's own review-response workflow. It was only caught because a self-review subagent read the review's full body text directly.

### Duplication search
- In-repo: No existing implementation found.
- Sibling repos: None identified.
- External libraries: None identified — this is a packaging-metadata fix, not a library capability.
- Recommendation: Proceed.

### Demand search
- Work items: None found.
- Proposals: None found.
- Backlog: No matching entries.
- Recommendation: No action beyond implementing this fix.

## Scope

- Declare `openai` and `python-dotenv` in `pyproject.toml` so `pip install -e .` alone satisfies every module-level import in `src/`.
- Simplify `.github/workflows/tests.yml`'s install step accordingly, removing the now-redundant explicit install.

## Required Changes

1. Add `openai` and `python-dotenv` to `pyproject.toml`'s `dependencies` list — or to a dedicated optional extra, if these two are judged to be optional/auditor-and-secrets-specific rather than core runtime needs (a call to make during implementation, based on whether every consumer of this package needs them or only the auditor/secrets-handling paths).
2. Remove `.github/workflows/tests.yml`'s separate `python -m pip install openai python-dotenv` line once `pip install -e .` alone covers it (or update it to install the chosen extra, e.g. `pip install -e ".[test]"`, if Required Change 1 uses an extra rather than core dependencies).
3. Verify in a fresh venv: `pip install -e .` (or `pip install -e ".[<extra>]"`) alone, then `scripts/test`, reports 259/259 with 0 errors.

## Non-Goals

- Does not change any test's logic or assertions.
- Does not add new tests.
- Does not touch `.github/workflows/lint.yml`, `charter.yml`, or `packet.yml`.

## Acceptance Criteria

- `pip install -e .` (or the chosen extra) in a fresh venv, with no separate `openai`/`python-dotenv` install step, followed by `scripts/test`, reports 259/259 tests passing with 0 errors.
- `.github/workflows/tests.yml`'s CI run reports the same 259/259 result using only the simplified install step.
- `lrh validate` reports 0 errors.

## Validation

- `lrh validate`
- `scripts/test` (in a fresh venv using only the new install command)
- Inspect the PR's own `test` CI check run for a 259/259 result

## Risk Notes

- Low risk: a `pyproject.toml` dependency-list addition plus a CI workflow simplification. The main judgment call is core-dependency vs. extra — get this right by checking whether every `prosoc` entry point needs `openai`/`dotenv` available, or only the auditor/secrets-handling code paths specifically.

## Related Workstream and Designs

- None — surfaced during `WI-TESTS-YML-DISCOVERY-FIX`'s implementation (PR #101) and independently by a `/lrh-self-review` substitute pass on that same PR.
