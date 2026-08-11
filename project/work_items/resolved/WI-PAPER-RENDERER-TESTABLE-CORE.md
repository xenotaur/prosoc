---
resolution: "Implemented and merged in PR #89 (commit ad0acda284c2652d26d1fb8e7d41080bdb1fcf60)"
blocked_reason: null
blocked: false
id: WI-PAPER-RENDERER-TESTABLE-CORE
title: Extract testable paper renderer core
type: deliverable
status: resolved
assigned_agents: []
related_focus: []
related_roadmap: []
related_workstreams: []
related_design: []
depends_on: []
blocked_by: []
expected_actions:
  - create_file
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - merge_pr
  - publish_package
  - run_lrh_agentic
  - implement_publication_framework
acceptance:
  - The paper renderer's reusable logic is importable from prosoc.
  - papers/01_charter/render.py remains runnable from the repository root and delegates to the importable renderer core.
  - Unit tests cover source parsing, Pandoc argument construction, fragment fixups, placeholder substitution, and representative error cases without requiring Pandoc for ordinary unit tests.
  - Existing papers/01_charter/render.py behavior and output paths are preserved.
  - scripts/lint, scripts/test, and lrh validate pass.
required_evidence:
  - manual_review
  - lrh_validate
  - test_output
artifacts_expected:
  - prosoc/utils/papers/render.py
  - prosoc/utils/papers/__init__.py
  - tests/utils/papers/render_test.py
  - tests/utils/papers/__init__.py
  - papers/01_charter/render.py
  - pyproject.toml
---

# WI-PAPER-RENDERER-TESTABLE-CORE

## Summary

Extract the Frontiers supplement renderer's reusable mechanics into an
importable `prosoc` module with focused unit tests, while keeping
`papers/01_charter/render.py` as the paper-specific entry point.

## Problem / Context

The current Frontiers supplementary-material renderer is useful, but all
rendering logic lives inside `papers/01_charter/render.py`, outside the
repository's normal `prosoc`/`tests` lint and format paths. The repo already
has precedent for importable renderer modules with unit tests, including
`prosoc/scenarios/render_sections.py` and `tests/scenarios/render_sections_test.py`,
and script wrappers that delegate to `python -m` modules. This work item
captures the small refactor needed to preserve the just-landed paper workflow
while making the renderer's parsing, Pandoc argument construction, LaTeX
fixups, and template substitution testable.

### Duplication search
- In-repo: Related implementation exists in `papers/01_charter/render.py`;
  related renderer/test precedent exists in `prosoc/scenarios/render_sections.py`
  and `tests/scenarios/render_sections_test.py`. No existing importable
  paper-renderer core or tests were found.
- Sibling repos: None identified.
- External libraries: Pandoc remains the external renderer dependency, but no
  external library should replace the repository-specific Frontiers glue and
  deterministic post-processing.
- Recommendation: Proceed by extracting the current script's testable core
  rather than creating a generalized publication framework.

### Demand search
- Work items: None found in `project/work_items/proposed/`.
- Proposals: None found in `project/design/proposals/proposed/`.
- Backlog: No matching entry found in `project/design/backlog.md`.
- Recommendation: No action.

## Scope

- Move the reusable paper-rendering mechanics into `prosoc/utils/papers/render.py`.
- Keep `papers/01_charter/render.py` as a thin paper-specific shim that
  preserves the current command path and output locations.
- Add focused unit tests for the renderer core without making ordinary unit
  tests depend on Pandoc being installed.
- Preserve the existing Frontiers paper behavior; this is a refactor and
  testability item, not a publication-system redesign.

## Required Changes

1. Create `prosoc/utils/papers/render.py` with the importable renderer core:
   - source-manifest parsing;
   - Pandoc command construction, including charter versus non-charter
     heading-shift behavior;
   - fragment fixups for `lstlisting`, Pandoc horizontal rules, and inline-code
     passthroughs;
   - template placeholder substitution and unresolved-placeholder validation;
   - a callable render entry point parameterized by paths and injectable
     subprocess runner where useful for tests.
2. Add `prosoc/utils/papers/__init__.py` so the new renderer package imports
   cleanly.
3. Replace `papers/01_charter/render.py` with a thin shim that computes the
   paper-specific paths and calls the importable renderer core, while preserving
   the existing repository-root invocation:
   - `papers/01_charter/render.py`
   - output `build/papers/01_charter/rendered.tex`
   - fragments under `build/papers/01_charter/fragments/`.
4. Add `tests/utils/papers/render_test.py` covering:
   - valid and invalid `sources.txt` parsing;
   - exact Pandoc argument construction for `CHARTER` and a non-charter card;
   - fragment fixups for listings, horizontal rules, and inline code;
   - successful placeholder substitution;
   - duplicate, missing, and unresolved placeholder failures;
   - subprocess invocation behavior using a fake or mocked runner rather than
     real Pandoc.
5. Add `tests/utils/papers/__init__.py` if needed by the existing unittest
   discovery/import pattern.
6. Update packaging metadata only if needed so any newly added package path is
   included consistently with the repository's intended packaging behavior.

## Non-Goals

- Do not redesign the paper-rendering system into a generic publication
  framework.
- Do not introduce Lua filters, a Pandoc plugin architecture, or a new rendering
  DSL.
- Do not change normative card content.
- Do not change the current Frontiers supplement template or source list except
  as required to keep the shim path working.
- Do not require Pandoc for ordinary unit tests; reserve real Pandoc execution
  for the existing renderer command or a clearly optional integration check.
- Do not merge the PR as part of implementation.

## Acceptance Criteria

- The paper renderer's reusable logic is importable from `prosoc`.
- `papers/01_charter/render.py` remains runnable from the repository root and
  delegates to the importable renderer core.
- Unit tests cover source parsing, Pandoc argument construction, fragment fixups,
  placeholder substitution, and representative error cases without requiring
  Pandoc for ordinary unit tests.
- Existing `papers/01_charter/render.py` behavior and output paths are
  preserved.
- `scripts/lint`, `scripts/test`, and `lrh validate` pass.

## Validation

- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `papers/01_charter/render.py`

## Risk Notes

- Moving logic out of the paper directory could accidentally make paper-specific
  behavior look like a general publication API; keep names and interfaces narrow.
- The current package metadata lists only `prosoc`, so implementation should
  verify whether new subpackages need a packaging adjustment.
- Tests should avoid overfitting to full Pandoc output, which may drift by
  Pandoc version; focus unit tests on deterministic repo-owned behavior and
  command construction.
