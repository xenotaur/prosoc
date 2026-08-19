---
resolution: "Implemented and merged in PR #95 (commit a9ea0c3), squashed."
blocked_reason: null
blocked: false
id: WI-NCA-PRNC-PACKAGE-LAYOUT
title: Restructure prosoc into src/prosoc/{nca,prnc,constitutions,manifests}
type: deliverable
status: resolved
owner: anthony
contributors:
  - anthony
assigned_agents: []
related_focus: []
related_roadmap: []
related_workstreams: []
related_design:
  - project/design/proposals/proposed/nca-prnc-package-layout/00_proposal.md
depends_on: []
blocked_by: []
expected_actions:
  - create_file
  - edit_file
  - delete_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - implement_nca_extraction
  - refactor_family_registry
  - publish_package
  - edit_card_normative_content
  - add_package_extras
acceptance:
  - src/prosoc/{nca,prnc,constitutions,manifests}/ exists matching PROP-NCA-PRNC-PACKAGE-LAYOUT's design, with nca/ containing exactly the verified-generic modules (literate/, auditor/, packet/, utils/ — utils/ moved wholesale, including utils/experiments/, not carved out separately) and the three still-coupled packet/ artifacts (loader.py, assemble.py, schema.json) present but unmodified in behavior
  - packet/loader.py's 5 family imports and REPO_ROOT (parents[2] to parents[4]) are fixed; utils/cards/validate_status.py's matching imports are fixed
  - pyproject.toml rewritten (package-dir, packages.find.where, include-package-data, per-subpackage package-data globs) mirroring LogicalRoboticsHarness's pyproject.toml:52-61
  - tests/ mirrors the new layout with all import paths updated
  - .github/workflows/packet.yml and charter.yml path triggers, scripts/distill/* and scripts/validate/* module paths, and .claude/skills/_shared/audit_checklists/*.md (6 files) are all updated to the new paths
  - Root-level <root>/experiments/ (dated research-run archives, not part of the prosoc package) is untouched by this work item
  - No normative card content, schema, or normative meaning changed — verified by content-hash comparison before/after the move, not just file presence
  - papers/01_charter/sources.txt's 9 paths and render.py's sys.path assumption are updated; re-running the renderer against the new paths produces output byte-identical to papers/01_charter/golden/rendered.tex
  - lrh validate reports 0 errors; full test suite (scripts/test) passes
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - src/prosoc/nca/{literate,auditor,packet,utils}/
  - src/prosoc/prnc/{charter,scenarios,tasks,contexts}/
  - src/prosoc/constitutions/
  - src/prosoc/manifests/
  - pyproject.toml
  - tests/ (restructured)
  - .github/workflows/packet.yml
  - .github/workflows/charter.yml
  - scripts/distill/*
  - scripts/validate/*
  - .claude/skills/_shared/audit_checklists/*.md
  - papers/01_charter/sources.txt
  - papers/01_charter/render.py
---

# Restructure prosoc into src/prosoc/{nca,prnc,constitutions,manifests}

## Summary

Implements `PROP-NCA-PRNC-PACKAGE-LAYOUT`: moves prosoc's flat `prosoc/{packet,literate,auditor,utils,charter,scenarios,tasks,contexts,constitutions,manifests}/` layout into a `src/`-layout single top-level package, separating verified domain-agnostic engine code (`prosoc.nca`) from PRNC-specific data (`prosoc.prnc`/`prosoc.constitutions`/`prosoc.manifests`), with `pyproject.toml` rewired to actually build a complete single-wheel distribution.

## Problem / Context

The proposal (`project/design/proposals/proposed/nca-prnc-package-layout/00_proposal.md`, merged via prosoc PR #85) established the design and rationale — engine and data currently sit as flat siblings with no structural marker. Packaging is half-fixed as of this writing: `pyproject.toml`'s code-discovery declaration was corrected independently (`[tool.setuptools.packages.find] include = ["prosoc*"]`) — verified by a fresh local build, which now correctly packages all 40 `.py` files — but `package-data` still only declares `prosoc.charter`'s three files; the other five families' `schema.json`/`template.md`/content, and `packet/schema.json`/`auditor/schema.json`, ship in no wheel build today. This item is the implementation the proposal's own Implementation Plan describes.

Three corrections were made to the proposal after it merged, before or during this work item's drafting, all carried through here: (1) `prosoc/utils/experiments/` moves as part of `utils/` wholesale into `nca/utils/`, not carved out into its own top-level `prosoc.experiments` package — the original reasoning for splitting it out didn't hold up under the same scrutiny applied to the other splits, and the split would have collided in name with the pre-existing, unrelated top-level `<root>/experiments/` (a non-package directory of dated research-run archives). (2) `packet/schema.json`'s `guidance` object is a third domain-coupled artifact alongside `loader.py`/`assemble.py` (its `principles[].id`/`emphasis` fields are the wire-format consequence of the same PRNC-specific coupling) — the proposal originally undercounted this as "two coupled files." (3) Implementation was deliberately deferred while `papers/01_charter/` — the Frontiers in Robotics paper's supplementary-material renderer, with a golden-file regression test — landed on a real submission deadline (`WI-PAPER-RENDERER-TESTABLE-CORE`, PRs #89–90, resolved). That work added `prosoc/utils/papers/render.py` (generic, no PRNC-specific imports, covered by the existing wholesale `utils/` move) and, at the repo root, `papers/01_charter/sources.txt` + `render.py`, which hardcode the flat `prosoc/...` paths this work item relocates — addressed in Required Changes step 7.

### Duplication search
- In-repo: No existing implementation found.
- Sibling repos: `LogicalRoboticsHarness`'s `src/lrh/` is the packaging-config precedent this item's `pyproject.toml` rewrite follows (`pyproject.toml:52-61`).
- External libraries: None identified — layout convention, not a library capability.
- Recommendation: Proceed.

### Demand search
- Work items: None found.
- Proposals: Found — `PROP-NCA-PRNC-PACKAGE-LAYOUT` (status `proposed`). This work item directly implements it; not a duplicate.
- Backlog: No matching entries.
- Recommendation: No action beyond implementing the proposal.

## Scope

- Relocate engine code and PRNC data per the proposal's Decisions 1–4 (as corrected).
- Fix the two files whose import paths break because of the move (`packet/loader.py`, `utils/cards/validate_status.py`) — path updates only, not the deeper `FAMILIES`-registry refactor.
- Rewrite `pyproject.toml` for a working single-wheel build.
- Update every downstream path reference: tests, CI workflows, `scripts/`, skill audit-checklist docs.

## Required Changes

1. `git mv` engine code into `src/prosoc/nca/{literate,auditor,packet,utils}/` — `utils/` moves wholesale, including `utils/experiments/mutator.py`; no separate `src/prosoc/experiments/` package.
2. `git mv` each family's data + glue code into `src/prosoc/prnc/{charter,scenarios,tasks,contexts}/`, `src/prosoc/constitutions/`, `src/prosoc/manifests/`.
3. Fix `packet/loader.py:23-27` (4 of 5 imports change; `constitutions` doesn't move under `prnc`) and `packet/loader.py:33` (`REPO_ROOT` `parents[2]` → `parents[4]`); fix `utils/cards/validate_status.py:22-28`'s matching imports.
4. Rewrite `pyproject.toml`: `package-dir`, `packages.find.where`, `include-package-data`, per-subpackage `package-data` globs.
5. Update `tests/` — directory structure and import paths (mirrors `prosoc/` 1:1 today).
6. Update `.github/workflows/packet.yml:10-16`, `charter.yml:6`; `scripts/distill/*`, `scripts/validate/*` module paths; `.claude/skills/_shared/audit_checklists/*.md` (6 files).
7. Update `papers/01_charter/sources.txt`'s 9 hardcoded `prosoc/...` paths to their new `src/prosoc/prnc/...` locations; verify `papers/01_charter/render.py`'s `sys.path.insert(0, str(REPO_ROOT))` still resolves an importable `prosoc` under the new layout (prefer relying on `pip install -e .` per the rewritten `pyproject.toml` over the raw path hack, if cleaner); re-run the renderer and diff against `papers/01_charter/golden/rendered.tex` for byte-identical output.
8. `lrh validate` + full test suite green before opening the PR.

## Non-Goals

- Does not extract NCA into a separate library/repo (proposal's Non-Goals, carried over).
- Does not fix `packet/loader.py`'s `FAMILIES` registry, `packet/assemble.py`'s principle-union coupling, or `packet/schema.json`'s `guidance.principles`/`guidance.tensions` required fields — all three move as-is, still documented as domain-coupled.
- Does not introduce PyPI extras or a multi-package split.
- Does not split `constitutions/`'s schema from its content.
- Does not change any card content, schema, or normative meaning.
- Does not publish a `prosoc` wheel to PyPI.
- Does not touch root-level `<root>/experiments/` — it isn't part of the `prosoc` package.

## Acceptance Criteria

- `src/prosoc/{nca,prnc,constitutions,manifests}/` matches the (corrected) proposal's design — no `src/prosoc/experiments/`.
- `packet/loader.py` and `utils/cards/validate_status.py` import paths and `REPO_ROOT` depth are correct — verified by running the packet assembler end-to-end (`scripts/assemble` against `prosoc/manifests/sample_packet/manifest.yml` or its new path) and confirming it still produces the same golden output.
- `pyproject.toml` builds a wheel (`scripts/build`) that actually contains all six families' data (not just `prosoc.charter`'s three files, the current state) alongside the already-correctly-discovered code.
- `lrh validate` reports 0 errors; `scripts/test`, `scripts/lint`, `scripts/format --check --diff` all pass.
- Content-hash comparison of every `.md`/`.yml` card file before and after the move shows zero content changes — only paths moved.
- `papers/01_charter/render.py` runs successfully against the new layout and produces output byte-identical to `papers/01_charter/golden/rendered.tex`.

## Validation

- `scripts/version tools`
- `lrh validate`
- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `scripts/build` (confirm the built wheel contains data for all six families, not just `prosoc.charter`'s three files)
- `papers/01_charter/render.py` (diff its output against `papers/01_charter/golden/rendered.tex`)

## Risk Notes

- Mechanical size (~150+ files via `git mv`) makes this a large diff even though individually each change is simple — real review risk is missing one of the ~10 files needing content fixes (not just moves), enumerated precisely in Required Changes.
- `scripts/assemble` end-to-end against the golden packet fixture is the strongest signal that `packet/loader.py`'s import-path fix is actually correct, not just that it imports without error.
- `papers/01_charter/`'s golden-file test is externally significant (a real paper submission's supplementary material) — a silent break here has consequences beyond this repo. Verify the renderer explicitly rather than assuming the `git mv` alone preserved it.

## Related Workstream and Designs

- Design: `project/design/proposals/proposed/nca-prnc-package-layout/00_proposal.md`
- Related, independently landed: `project/work_items/resolved/WI-PAPER-RENDERER-TESTABLE-CORE.md` — the source of the `papers/01_charter/` dependency this item accounts for.
