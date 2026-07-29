---
resolution: null
blocked_reason: null
blocked: false
id: WI-CARD-STATUS-CHARTER
title: Extend the card lifecycle-state contract to the charter family (Phase 0a — final family)
type: deliverable
status: proposed
assigned_agents: []
related_focus:
  - FOCUS-NORMATIVE-PACKET-ASSEMBLY
related_roadmap: []
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/proposed/normative-packet-assembly/00_proposal.md
depends_on:
  - WI-CARD-STATUS-CONSTITUTIONS
blocked_by: []
expected_actions:
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - edit_charter_normative_content
  - implement_assembler_engine
acceptance:
  - A single-source charter family is registered in the validator (yaml_root_key null, single charter.md->charter.yml source); scripts/validate/status validates scenarios + tasks + contexts + constitutions + charter all consistent
  - charter.md carries a canonical "- **STATE:**" bullet in a Status block, prosoc/charter/schema.json requires a top-level state enum alongside principles, and charter.yml carries a schema-valid top-level state (DRAFTED) with no change to any principle payload
  - lrh validate, scripts/lint, scripts/test, and scripts/validate/status all report 0 errors, and no charter principle (P0-P9) normative content changed
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/utils/cards/validate_status.py
  - prosoc/charter/distill.py
  - prosoc/charter/schema.json
  - prosoc/charter/charter.md
  - prosoc/charter/charter.yml
  - tests/utils/cards/validate_status_test.py
---

# WI-CARD-STATUS-CHARTER

## Summary

Extend the machine-readable lifecycle-`state` contract to the charter, the
fifth and final Phase 0a family. Unlike every prior family, the charter is a
single multi-principle document (`charter.md` -> `charter.yml`), so this
requires a single-source family adapter in the validator and a change to the
charter distiller to emit a document-level `state`. Completing it means all
five card families carry the contract.

## Problem / Context

Charter is the last of five families, and structurally the most different.
Three divergences are verified in the corpus:

1. **Single document, not a card family** — there is one `charter.md` compiled
   to one `charter.yml`, not a directory-of-cards (scenarios/tasks/contexts) or
   root-wrapped card-per-directory (constitutions). Discovery must yield a
   single source, not iterate a root.
2. **Principle-aggregating distiller** — `prosoc/charter/distill.py` compiles
   with `ROOT_KEY = "principles"`, so `compiler.compile_file` gathers every
   fenced per-principle block (P0-P9) into a list under `principles:`. The
   schema (`prosoc/charter/schema.json`) is `additionalProperties: false` with
   `required: ["principles"]` — there is no top-level field to hang `state` on,
   and no authored top-level mapping the compiler preserves.
3. **No STATUS block** — `charter.md` has no `## Status`/`## STATUS` section and
   no `- **STATE:**` bullet. The only status metadata is an inline top-matter
   line, `**Status:** Draft (Normative)` (charter.md:4), whose value is not a
   canonical lifecycle enum. It maps to `DRAFTED`.

Because the `state` is document-level, it belongs at the **top level** of
`charter.yml` (a sibling of `principles:`), so `yaml_root_key` is `None` — the
YAML dimension is like scenarios, not root-wrapped like constitutions. The real
work is the single-source discovery and teaching the charter distiller to emit
a top-level `state`.

### Duplication search
- In-repo: No charter status handling yet. The generic tooling in
  `prosoc/utils/cards/` is extended (a single-source family registration), not
  duplicated; the charter distiller is extended, not replaced.
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed.

### Demand search
- Work items: None found. `WI-CARD-STATUS-CONSTITUTIONS` (resolved) is the
  predecessor this builds on; this is the final family in the same slice.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` governs this work item.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

- Register a single-source `charter` family in
  `prosoc/utils/cards/validate_status.py` (`yaml_root_key=None`,
  `supports_flat=False`, single `charter.md`->`charter.yml` source).
- Extend `prosoc/charter/distill.py` to emit a top-level `state` sibling of
  `principles` in `charter.yml`, sourced from the authoritative Markdown state.
- Introduce a `## Status` block with a `- **STATE:** DRAFTED` bullet in
  `charter.md` and require a top-level `state` enum in
  `prosoc/charter/schema.json`.

## Required Changes

1. **`prosoc/charter/distill.py`** — emit a document-level `state` alongside
   `principles` in the compiled dict written to `charter.yml`. Because the
   `ROOT_KEY="principles"` compilation sweeps every fenced block into the
   principles list, the distiller must obtain `state` outside that collection
   (see the design decision below) and inject it as a top-level sibling.
2. **`prosoc/charter/schema.json`** — add a required top-level `state` enum
   (mirror the enum used by the other families) beside `principles`, keeping
   `additionalProperties: false`.
3. **`prosoc/charter/charter.md`** — add a `## Status` section whose first
   bullet is `- **STATE:** DRAFTED` (uniform with the other four families).
   Reconcile the inline `**Status:** Draft (Normative)` top-matter line so the
   document has a single, canonical state source. No principle (P0-P9) content
   changes.
4. **`prosoc/charter/charter.yml`** — regenerate so it carries the top-level
   `state: DRAFTED` (state field only; principle payloads unchanged).
5. **`prosoc/utils/cards/validate_status.py`** — register the `charter` family
   with a single-source discoverer exposing `md_path`/`yml_path` (so the
   existing `_label`/`check_source` path works), `yaml_root_key=None`,
   `supports_flat=False`.
6. **`tests/utils/cards/validate_status_test.py`** — add a charter-family test
   class (consistent + inconsistent) exercising the single-source discovery and
   top-level `state`.

### Design decision to settle at implementation

Where the authoritative document-level `state` is authored so the distiller can
emit it as a top-level sibling of `principles`:

- **Leading approach** — author `state` in a small document-level fenced block
  under the new `## Status` section, and special-case it in the charter
  distiller so it is lifted to a top-level `state` sibling rather than swept
  into the `principles` list; project the `- **STATE:**` bullet for the
  validator. Keeps the "fenced-YAML-authoritative, projected into Markdown"
  model uniform with the other families.
- **Alternative** — treat the Markdown `## Status` `- **STATE:**` bullet as
  authoritative and derive `charter.yml`'s `state` from it. Simpler, but
  inverts the family model and makes `scripts/validate/status`'s md<->yml
  agreement check trivial (and reverses the `--fix` direction).

Resolve this at `/lrh-implement`; the acceptance criteria hold either way.

## Non-Goals

- Do not build the assembler engine, lifecycle gate, or manifest — later
  workstream phases.
- Do not re-resolve the lifecycle enum — it is canonical in
  `prosoc/scenarios/workflow.md`; reuse it.
- Do not change any charter principle (P0-P9) normative statement, example, or
  severity, or any glossary/definition prose. Charter stays `DRAFTED`.
- Do not close `WS-NORMATIVE-PACKET-ASSEMBLY` — its exit criteria (audit skills,
  assembler, manifests, CI drift gate) remain beyond this Phase-0a slice.

## Acceptance Criteria

- A single-source charter family is registered in the validator
  (`yaml_root_key=None`, single `charter.md`->`charter.yml` source);
  `scripts/validate/status` validates scenarios + tasks + contexts +
  constitutions + charter all consistent.
- `charter.md` carries a canonical `- **STATE:**` bullet in a Status block,
  `prosoc/charter/schema.json` requires a top-level `state` enum alongside
  `principles`, and `charter.yml` carries a schema-valid top-level `state`
  (`DRAFTED`) with no change to any principle payload.
- `lrh validate`, `scripts/lint`, `scripts/test`, and `scripts/validate/status`
  all report 0 errors, and no charter principle (P0-P9) normative content
  changed.

## Validation

- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/validate/status`
- `scripts/validate/status --family charter`
- `python -m prosoc.charter.distill --dry-run --show-diffs`

## Risk Notes

- The charter distiller change is the crux: the `ROOT_KEY="principles"`
  compiler aggregates all fenced blocks, so `state` must be injected without
  being mistaken for a principle. Verify a distilled `charter.yml` has `state`
  at the top level and `principles` unchanged (P0-P9 intact, count and order).
- Adding a required top-level `state` to the charter schema will break
  distillation until `charter.yml`/`charter.md` are migrated together; land the
  schema, distiller, and regenerated `charter.yml` in one change.
- Single-source discovery differs from every prior family (which iterate a
  root). Ensure the `--card`/empty-root guards in `_check_family` behave
  sensibly for a one-source family.
- Reconciling the inline `**Status:** Draft (Normative)` line with the new
  `## Status` block is a metadata reformat only — confirm the charter.md diff
  touches no principle or glossary content.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
- Design: `project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`
