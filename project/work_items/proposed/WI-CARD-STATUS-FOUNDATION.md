---
resolution: null
blocked_reason: null
blocked: false
id: WI-CARD-STATUS-FOUNDATION
title: Establish the card lifecycle-state field and STATUS-block projection (Phase 0a foundation)
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
depends_on: []
blocked_by: []
expected_actions:
  - edit_file
  - create_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - edit_scenario_normative_content
  - apply_to_other_card_families
  - implement_assembler_engine
acceptance:
  - prosoc/scenarios/workflow.md documents the active lifecycle chain with APPROVED inserted after AUDITED, and records the VALIDATED-vs-VERIFIED stage-5 decision
  - Each scenario.yml carries a machine-readable lifecycle-state field validated by prosoc/scenarios/schema.json
  - The Markdown STATUS block STATE is projected from / kept consistent with the YAML state, and scripts/validate/status reports agreement for all 20 scenarios
  - lrh validate, scripts/lint, and scripts/test all report 0 errors, and all 20 scenarios remain audit-clean (no normative-content change)
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/scenarios/workflow.md
  - prosoc/scenarios/schema.json
  - prosoc/scenarios/*/scenario.yml
  - prosoc/scenarios/*/scenario.md
  - scripts/validate/status
  - prosoc/scenarios/render_sections.py
---

# WI-CARD-STATUS-FOUNDATION

## Summary

Establish the shared contract for the normative-card lifecycle — the canonical
STATUS-block format, the `APPROVED` state, and a machine-readable
lifecycle-state field projected from the fenced YAML into the Markdown — and
prove it end-to-end on the scenarios family, so the remaining four card
families can follow the same pattern in later Phase 0a work items.

## Problem / Context

The packet assembler defined in `PROP-NORMATIVE-PACKET-ASSEMBLY` must gate on
human approval before a card's guidance can reach a downstream agent, but a
card's lifecycle state lives only in its Markdown STATUS block today — in four
mutually incompatible encodings across the five families — and never reaches
the distilled YAML a machine gate would read. Phase 0a fixes that. This work
item does Phase 0a's shared, decision-bearing work once: resolve the lifecycle
enum (insert `APPROVED` for human approval; settle the `VALIDATED` vs
`VERIFIED` stage-5 naming), define the normalized STATUS-block format, and add
a machine-readable lifecycle-state field with a projection mechanism and a
validator — applied to the scenarios family as the reference implementation.
It must land first because every per-family rollout item depends on the
contract it establishes. Scenarios are chosen as the reference family because
they are the largest (20 cards), the best-understood, and already have a
projection precedent in `prosoc/scenarios/render_sections.py`, which renders
prose sections from `scenario.yml` and already stamps the STATUS block's
`EDITED` line.

### Duplication search
- In-repo: No existing status-normalization tooling. `render_sections.py` is
  the projection precedent to extend, not a duplicate.
- Sibling repos: None identified.
- External libraries: None identified.
- Recommendation: Proceed.

### Demand search
- Work items: None found. `WI-SCENARIO-SECTION-RENDERER` (resolved) is the
  projection precedent, not a request for this work.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` governs this work item.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

- Resolve the repo-side lifecycle enum in `prosoc/scenarios/workflow.md`
  (insert `APPROVED`; settle `VALIDATED`/`VERIFIED`).
- Define the canonical STATUS-block format and a machine-readable
  lifecycle-state field (proposed field name: `state`).
- Implement the contract end-to-end for the **scenarios** family only: schema,
  YAML, Markdown projection, and a validator.

## Required Changes

1. `prosoc/scenarios/workflow.md`: document the active lifecycle chain
   `DRAFTED → EDITED → AUDITED → APPROVED → …`, inserting `APPROVED` (human
   approval, the meaning `AUDITED` previously carried) and reconciling the
   stage-5 `VALIDATED` (empirical, per this file) vs `VERIFIED` (production,
   per `prosoc/constitutions/template.md` and the paper) split — recommend
   keeping `VALIDATED` and retiring or aliasing `VERIFIED`.
2. `prosoc/scenarios/schema.json`: add the machine-readable lifecycle-state
   field to the scenario payload.
3. `prosoc/scenarios/*/scenario.yml`: add the state field to all 20 scenarios,
   sourced from each card's current STATUS-block `STATE`.
4. Projection: extend `prosoc/scenarios/render_sections.py` (or the distiller)
   so the Markdown STATUS block `STATE` is rendered from / kept consistent with
   the YAML state, and normalize the scenario STATUS-block format.
5. `scripts/validate/status`: new validator asserting YAML state ↔ Markdown
   STATUS-block agreement for the scenario family, structured so the other
   families can be added later.
6. Add `WI-CARD-STATUS-FOUNDATION` to the `work_items:` list of
   `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`.

## Non-Goals

- Do not apply status normalization to tasks, contexts, constitutions, or the
  charter — each is a follow-on Phase 0a work item reusing this contract.
- Do not build the assembler engine, gate, manifest, or provenance envelope
  (Phases 1–2).
- Do not change any scenario's normative content or audit verdict — only the
  STATUS-block encoding.
- Do not adopt `PROP-NORMATIVE-PACKET-ASSEMBLY` or close
  `WS-NORMATIVE-PACKET-ASSEMBLY`.
- Do not edit the Frontiers paper; the Figure 3 / §3.3.5 edits are tracked
  separately by the proposal.

## Acceptance Criteria

- `prosoc/scenarios/workflow.md` documents the active lifecycle chain with
  `APPROVED` inserted after `AUDITED`, and records the `VALIDATED`-vs-`VERIFIED`
  stage-5 decision.
- Each `scenario.yml` carries a machine-readable lifecycle-state field
  validated by `prosoc/scenarios/schema.json`.
- The Markdown STATUS block `STATE` is projected from / kept consistent with
  the YAML state, and `scripts/validate/status` reports agreement for all 20
  scenarios.
- `lrh validate`, `scripts/lint`, and `scripts/test` all report 0 errors, and
  all 20 scenarios remain audit-clean (no normative-content change).

## Validation

- `scripts/version tools`
- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/validate/status` (new — run over `prosoc/scenarios/`)
- `scripts/distill/scenarios --dry-run --show-diffs`

## Risk Notes

- Regenerating 20 `scenario.yml` risks reflowing unrelated content — keep the
  diff to the added state field and verify with
  `scripts/distill/scenarios --dry-run --show-diffs` before committing.
- The corpus is audit-clean (see `FOCUS-NORMATIVE-PACKET-ASSEMBLY` background
  and PRs #30–32); a STATUS-block reformat must not alter normative content —
  re-run `/prosoc-scenario-audit-all` if any scenario prose shifts.
- The lifecycle-state field name (`state`) must not collide with existing keys
  such as the top-level `context:` in `scenario.yml` — confirm before
  finalizing.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
- Design: `project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`
