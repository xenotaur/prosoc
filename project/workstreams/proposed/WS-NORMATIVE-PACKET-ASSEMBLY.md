---
id: WS-NORMATIVE-PACKET-ASSEMBLY
kind: planning_node
title: Normative Packet Assembly — Implementation
status: proposed
stage: designed
origin: follow_up
summary: Implement the manifest-driven normative packet assembler defined in PROP-NORMATIVE-PACKET-ASSEMBLY, from lifecycle/status normalization through the assembler engine, manifest card family, and CI drift checks.
related_focus: []
related_roadmap: []
related_design:
  - project/design/proposals/proposed/normative-packet-assembly/00_proposal.md
work_items: []
exit_criteria:
  - PROP-NORMATIVE-PACKET-ASSEMBLY is adopted (status adopted)
  - All five card families carry a machine-readable status field with the APPROVED lifecycle state, projected into the Markdown STATUS block and enforced by scripts/validate/status
  - prosoc-card-audit and prosoc-card-audit-all skills exist with per-family checklists, including charter-specific handling
  - The assembler produces a deterministic, namespaced provenance-envelope packet from a manifest, with a fail-closed lifecycle gate and an in-payload --allow-unapproved escape hatch
  - Manifests are an auditable card family and packet drift is checked in CI against checked-in golden packets
---

# Normative Packet Assembly — Implementation

## Purpose

Coordinates the phased implementation of `PROP-NORMATIVE-PACKET-ASSEMBLY`:
assembling normative cards (charter principles, constitutions, tasks,
contexts, scenarios) into a single machine-readable guidance packet for a
downstream agent, via a human-authored auditable manifest and a deterministic
assembler engine. The design is settled and merged (PR #36); this workstream
tracks the build through to closeout.

It exists now because the packet is the pivot between two halves of the
project: everything below it — authoring, distillation, schema validation,
agent auditing — is built and tested, and everything above it — agent
consumption, navigation — is blocked on there being a packet to consume.

## Scope

- **Phase 0a** — lifecycle enum (insert `APPROVED`) and status-block
  normalization across all five card families, with `status` projected from
  the fenced YAML into the Markdown STATUS block and a `scripts/validate/status`
  backstop. Landed family-by-family (schema + distiller + regenerated `.yml`
  per commit), `lrh validate` green throughout.
- **Phase 0b** — `prosoc-card-audit` / `prosoc-card-audit-all` skills with
  per-family checklists under `.claude/skills/_shared/audit_checklists/`, plus
  charter-specific audit handling. Parallel to 0a.
- **Phase 1** — the assembler engine: `resolve`, `gate` (fail-closed), a
  generic `CardLoader`, `assemble`, `packet.schema.json`, and the in-toto /
  DSSE-shaped provenance envelope. Ships behind `--allow-unapproved`.
- **Phase 2** — the manifest as an auditable card family (`manifest.md` +
  template + distiller + schema).
- **Phase 3** — CI drift check (`scripts/assemble --check`) against
  checked-in golden packets.

## Prior Art Check

### Duplication search
- In-repo: No existing implementation. Only `PROP-NORMATIVE-PACKET-ASSEMBLY`
  (the governing proposal) matches; no assembler code and no prior workstream.
- Sibling repos: None identified. LogicalRoboticsHarness is prosoc's control
  plane, not a normative-artifact consumer.
- External libraries: None adoptable wholesale — in-toto/DSSE and SLSA inform
  the envelope shape only (schemas borrowed, not tooling).
- Recommendation: Proceed.

### Demand search
- Work items: None found — there is no `project/work_items/proposed/` bucket.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` — this workstream governs its
  implementation; not a duplicate.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Work Items

None created yet. Work items will be created via `/lrh-work-item` as each
phase is planned, and added to `work_items:` as they land. The expected
breakdown follows the phases in Scope — Phase 0a in particular is planned as
family-by-family commits, which may be one work item or several.

## Exit Criteria

- `PROP-NORMATIVE-PACKET-ASSEMBLY` is adopted (`status: adopted`).
- All five card families carry a machine-readable `status` field including the
  `APPROVED` lifecycle state, projected into the Markdown STATUS block and
  enforced by `scripts/validate/status`.
- `prosoc-card-audit` and `prosoc-card-audit-all` skills exist with per-family
  checklists, including charter-specific handling.
- The assembler produces a deterministic, namespaced provenance-envelope
  packet from a manifest, with a fail-closed lifecycle gate and an in-payload
  `--allow-unapproved` escape hatch.
- Manifests are an auditable card family and packet drift is checked in CI
  against checked-in golden packets.

## Non-Goals

- Does not include Phase 4 (cryptographic signing; scenario→task/context
  auto-resolution) — explicitly deferred by the proposal; a future workstream
  owns it.
- Does not repair the dangling `example_scenarios` task references — a
  validator surfaces them; they are tracked as corpus work.
- Does not author scenario→task or scenario→context reference fields.

## Relationship to Design

- Governing proposal:
  [`project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`](../../design/proposals/proposed/normative-packet-assembly/00_proposal.md)
  (`PROP-NORMATIVE-PACKET-ASSEMBLY`).

## Open Questions

- `project/focus/current_focus.md` currently scopes the active focus to
  scenario-corpus maintenance; this workstream opens a new front and the focus
  file likely wants updating (out of scope for this skill).
- The `VALIDATED` (empirical, per `scenarios/workflow.md`) vs `VERIFIED`
  (production, per `constitutions/template.md` and the paper) stage-5 naming
  split must be resolved in Phase 0a, per the proposal's open question.
