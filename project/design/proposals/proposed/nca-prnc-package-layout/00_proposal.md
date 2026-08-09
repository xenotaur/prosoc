---
id: PROP-NCA-PRNC-PACKAGE-LAYOUT
type: design_proposal
title: Separate NCA Engine from PRNC Data in prosoc's Package Layout
status: proposed
created_on: 2026-08-09
updated_on: 2026-08-09
implementation_status: not_started
implemented_by: []
supersedes: []
superseded_by: null
related_design:
  - project/design/proposals/adopted/normative-packet-assembly/00_proposal.md
  - project/design/backlog.md
---

# Separate NCA Engine from PRNC Data in prosoc's Package Layout

## Summary

Restructures `prosoc`'s Python package from a flat layout that mixes engine code and normative-card data throughout `prosoc/{packet,literate,auditor,utils,charter,scenarios,tasks,contexts,constitutions,manifests}/` into a `src/`-layout single top-level package with an internal boundary: `prosoc.nca` for verified domain-agnostic engine code, `prosoc.prnc`/`prosoc.constitutions`/`prosoc.manifests` for data (each retaining its still-PRNC-specific glue code), bundled as one wheel.

## Background / Motivation

`prosoc/packet/loader.py`'s own module docstring already calls itself a "generic card loader," and `PROP-NORMATIVE-PACKET-ASSEMBLY` (adopted) built the packet engine on the premise that composition logic is separable from the five card families it composes (`prosoc/packet/loader.py:69-79`'s `FAMILIES` registry; the corpus has six families total, but `manifests` isn't a packet member — it's the packet definition itself, excluded by design). That separation currently exists only in the code's *behavior*, not in the repo's *layout* — `prosoc/packet/`, `prosoc/literate/`, and `prosoc/auditor/` (the genuinely reusable parts) sit as siblings to `prosoc/scenarios/`, `prosoc/tasks/`, `prosoc/charter/`, etc. (the PRNC-specific parts) with no structural marker distinguishing them, and `pyproject.toml`'s `[tool.setuptools] packages = ["prosoc"]` doesn't even declare the subpackages correctly — the last built wheel (`dist/prosoc-0.1.0-py3-none-any.whl`, Dec 2025) contains only `prosoc/__init__.py`, nothing else.

This needs addressing now, deliberately in a narrow way: not because prosoc is ready to be reused by a second domain (a separate, earlier design conversation this same session concluded that extraction is premature — no second consumer exists to pressure-test a plugin API), but because the *layout* question is independent of that one and much cheaper to resolve. It's fully reversible, requires no external consumer to justify it, and makes the actual, already-established generic/domain boundary (documented in the earlier session's file-by-file audit) visible in the repo's own structure instead of just in prose.

## Prior Art Check

### Duplication search
- In-repo: No existing implementation found (`grep -rli "src layout\|src-layout\|src/nca\|package restructur\|separate.*code.*data" prosoc/ project/design/proposals/ .claude/skills/` — zero hits).
- Sibling repos: Not a duplicate, but directly reusable precedent — `LogicalRoboticsHarness` already runs this exact pattern: `src/lrh/`, single top-level package, `pyproject.toml:52-61` (`package-dir = {"" = "src"}`, `packages.find.where = ["src"]`, `include-package-data = true`, per-subpackage `package-data` globs). This proposal's `pyproject.toml` design mirrors that shape.
- External libraries: None identified — this is a layout convention, not a capability a library provides.
- **Recommendation: Proceed.**

### Demand search
- Work items: None found (`project/work_items/proposed/`).
- Proposals: None found (`project/design/proposals/proposed/`).
- Backlog: No matching entries (`project/design/backlog.md`).
- **Recommendation: No action.**

## Design Decisions

### Decision 1: Single top-level package vs. multiple top-level packages under `src/`

Options considered:
- Four independent top-level packages (`prosoc`, `prnc`, `constitutions`, `manifests`) as siblings under `src/`.
- One top-level package (`prosoc`) with `nca`/`prnc`/`constitutions`/`manifests`/`experiments` as subpackages.

**Chosen: one top-level package.** Matches the overwhelming majority of real Python packages and the sibling-repo precedent (`src/lrh/`). Avoids name-collision risk for generic words like `constitutions`/`manifests` (documented failure mode: ZeroCM/zcm#186, carpedm20/emoji#49). Positions correctly for a possible future split into separately-installable distributions via PEP 420 namespace packages (the `google-cloud-storage`/`google-cloud-bigquery` pattern under `google.cloud`), which requires the shared-prefix structure this decision establishes.

### Decision 2: Scope of `nca/`

Options considered:
- Move everything currently called "code" into `nca/`.
- Move only verified domain-agnostic modules; leave PRNC-specific glue code (`distill.py` per family) with its data; flag the two still-coupled engine files inline rather than silently relabeling them.

**Chosen: the narrower scope.** Freshly re-verified this session: `prosoc/constitutions/schema.json` has zero navigation/robot/social references (`grep` confirmed), but `prosoc/packet/loader.py:23-27` hardcodes imports of all five families' `distill` modules, and `prosoc/packet/assemble.py:53,64-107,110-126` hardcodes PRNC's principle-union composition. Calling these files `nca` unchanged would misrepresent their actual state. `packet/` stays one directory under `nca/` (splitting `loader.py`'s generic `CardLoader` class from its coupled `FAMILIES` registry is the refactor `PROP-NORMATIVE-PACKET-ASSEMBLY`'s own follow-on work already anticipates, not a layout question) but its two coupled files are documented as such, not hidden.

### Decision 3: Constitutions — split schema from content, or keep together

Options considered:
- Split: `constitutions/schema.json` (verified domain-agnostic) under `nca/`; authored content (`asimov_three_laws/`, `asimov_four_laws/`) as data.
- Keep together as one package.

**Chosen: keep together.** User's explicit rationale: the small size of these components is itself an argument for not splitting — nothing today registers a second constitution-shaped family through `nca`, so the split buys ambiguity now for a payoff not yet claimed. Revisitable later at negligible cost (small, self-contained directory).

### Decision 4: Manifests — fold into `prnc/` or keep separate

**Chosen: keep separate.** A manifest is packet-assembly configuration (a named `{family, id}` member list), not normative content in the sense charter/scenarios/tasks/contexts are.

### Decision 5: Packaging mechanism — single wheel vs. extras vs. multi-package

Options considered:
- `optional-dependencies` (`prosoc[bare]`/`prosoc[all]`) controlling which files ship.
- Separate PyPI distributions per data package, glued by extras.
- Single wheel, everything bundled, `include-package-data = true`.

**Chosen: single wheel.** Verified this session: `optional-dependencies`/`extras_require` never change wheel contents — they only gate additional dependency installs; genuinely different shipped content requires separate distributions (the `spaCy` language-model pattern), which real precedent uses only at a data scale (10s–100s of MB) far beyond this repo's actual data footprint (`du -ck` verified: ~800KB of `.md`+`.yml` content, ~204KB of `.py`). Bundling everything in one wheel is right-sized for the current scale, not premature optimization.

### Decision 6: Implementation staging — single PR vs. multi-stage

Options considered:
- Multiple smaller PRs (e.g., move `nca/` first, then data, then wiring).
- One PR.

**Chosen: one PR.** `packet/loader.py`'s imports only resolve once *both* the engine code and the referenced family have moved — a genuine multi-PR staging would leave `main` in a broken intermediate state between stages unless done on a long-lived branch, which erases the main benefit of staging (small reviewable diffs landing independently). See Implementation Plan.

## Non-Goals

- Does not extract NCA into a separate library or repository — that's a materially different, larger decision this same design session's earlier conversation already concluded is premature (no second consumer exists to pressure-test a plugin API). This proposal is a same-repo layout change only.
- Does not fix `packet/loader.py`'s hardcoded `FAMILIES` registry or `packet/assemble.py`'s PRNC-specific principle-union logic (`_guidance_body`/`_principle_union`/`_tensions`). Both move under `nca/packet/` as-is, documented as still domain-coupled. Fixing them is separate follow-on work.
- Does not introduce PyPI extras, optional-dependencies, or a multi-package split. Single wheel only.
- Does not split `constitutions/`'s schema from its content (Decision 3).
- Does not change any card content, schema, or normative meaning — this is a pure file-location and import-path change.
- Does not attempt to actually publish a `prosoc` wheel to PyPI — `scripts/publish` already states this is deliberately deferred ("not yet supported until prosoc is more heavily tested / fleshed out"); this proposal makes a future publish *possible*, it doesn't schedule one.

## Implementation Plan

Single PR (Decision 6). Within it, sequenced so each intermediate step stays internally consistent even though only the final state is testable end-to-end:

1. `git mv` engine code into `src/prosoc/nca/{literate,auditor,packet,utils}/`.
2. `git mv` each family's data + glue code into its new home: `src/prosoc/prnc/{charter,scenarios,tasks,contexts}/`, `src/prosoc/constitutions/`, `src/prosoc/manifests/`; `git mv` `utils/experiments/` to `src/prosoc/experiments/`.
3. Fix the enumerated breakage: `packet/loader.py:23-27` import paths (4 of 5 change; `constitutions` doesn't move under `prnc`), `packet/loader.py:33` `REPO_ROOT` (`parents[2]` → `parents[4]`), `utils/cards/validate_status.py:22-28` (same import fix, its own separate `FAMILIES` dict).
4. Rewrite `pyproject.toml`: `package-dir`, `packages.find.where`, `include-package-data`, per-subpackage `package-data` globs — mirroring `LogicalRoboticsHarness`'s `pyproject.toml:52-61`.
5. Update `tests/` (mirrors `prosoc/` 1:1) — directory structure and import paths.
6. Update `.github/workflows/packet.yml:10-16`, `charter.yml:6` path triggers; `scripts/distill/*`, `scripts/validate/*` module paths; `.claude/skills/_shared/audit_checklists/*.md` (6 files) path references.
7. `lrh validate` + full test suite green before opening the PR.

No workstream or separate work item — this proposal's implementation is the one bounded PR above; a companion `/lrh-work-item` is offered at the end of this run, not a workstream.

## Cross-References

- `project/design/proposals/adopted/normative-packet-assembly/00_proposal.md` — establishes the packet engine this proposal relocates without modifying its behavior.
- `LogicalRoboticsHarness`'s `pyproject.toml` (sibling repo) — the packaging-config precedent this proposal's `pyproject.toml` rewrite follows.
