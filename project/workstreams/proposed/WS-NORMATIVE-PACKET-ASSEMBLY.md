---
id: WS-NORMATIVE-PACKET-ASSEMBLY
kind: planning_node
title: Normative Packet Assembly — Implementation
status: proposed
stage: designed
origin: follow_up
summary: Implement the manifest-driven normative packet assembler defined in PROP-NORMATIVE-PACKET-ASSEMBLY, from lifecycle/status normalization through the assembler engine, manifest card family, and CI drift checks.
related_focus:
  - FOCUS-NORMATIVE-PACKET-ASSEMBLY
related_roadmap: []
related_design:
  - project/design/proposals/adopted/normative-packet-assembly/00_proposal.md
  - project/design/proposals/adopted/normative-card-approval/00_proposal.md
work_items:
  - WI-CARD-STATUS-FOUNDATION
  - WI-CARD-STATUS-TASKS
  - WI-CARD-STATUS-CONTEXTS
  - WI-CARD-STATUS-CONSTITUTIONS
  - WI-CARD-STATUS-CHARTER
  - WI-PACKET-ASSEMBLER-ENGINE
  - WI-CARD-AUDIT-SKILLS
  - WI-PACKET-MANIFEST-FAMILY
  - WI-PACKET-CI-DRIFT-CHECK
  - WI-CARD-APPROVE-SKILLS
  - WI-CARD-APPROVAL-PILOT
exit_criteria:
  - PROP-NORMATIVE-PACKET-ASSEMBLY is adopted (status adopted)
  - All five card families carry a machine-readable status field with the APPROVED lifecycle state, projected into the Markdown STATUS block and enforced by scripts/validate/status
  - prosoc-card-audit and prosoc-card-audit-all skills exist with per-family checklists, including charter-specific handling
  - The assembler produces a deterministic, namespaced provenance-envelope packet from a manifest, with a fail-closed lifecycle gate and an in-payload --allow-unapproved escape hatch
  - Manifests are an auditable card family and packet drift is checked in CI against checked-in golden packets
  - Every card in the corpus reaches APPROVED (per PROP-NORMATIVE-CARD-APPROVAL's framing of this as the workstream's second exit criterion; confirmed with the user 2026-08-01)
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
- Work items: None found at authoring time — the
  `project/work_items/proposed/` bucket did not yet exist. This workstream's
  own first item, `WI-CARD-STATUS-FOUNDATION`, was created under it afterward.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` — this workstream governs its
  implementation; not a duplicate.
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Work Items

- **WI-CARD-STATUS-FOUNDATION** — Phase 0a foundation (resolved): resolve the
  lifecycle enum (insert `APPROVED`; settle `VALIDATED`/`VERIFIED`), define the
  canonical STATUS-block format and a machine-readable lifecycle-state field,
  and prove the contract end-to-end on the scenarios family.
- **WI-CARD-STATUS-TASKS** — Phase 0a, tasks family (resolved): generalize the
  status tooling into `prosoc/utils/cards/` (family-aware) and apply the state
  contract to the four task cards, reusing the foundation contract.
- **WI-CARD-STATUS-CONTEXTS** — Phase 0a, contexts family (resolved): register
  the contexts family with the now-generic tooling and apply the state contract
  to the four context cards.
- **WI-CARD-STATUS-CONSTITUTIONS** — Phase 0a, constitutions family (resolved):
  add a `root_key` parameter to the shared state helpers and normalize the
  constitution STATUS blocks (root-wrapped YAML, heading-style STATUS), then
  apply the state contract to the two constitution cards.
- **WI-CARD-STATUS-CHARTER** — Phase 0a, charter family (resolved): register a
  single-source charter family and teach the charter distiller to emit a
  document-level `state`, applying the contract to the single multi-principle
  charter document. Merged in PR #49, closing out Phase 0a — all five families
  now carry the machine-readable lifecycle-state contract.
- **WI-PACKET-ASSEMBLER-ENGINE** — Phase 1, the assembler engine (resolved): a
  generic `CardLoader`, manifest `resolve`, a fail-closed lifecycle `gate`, and
  `assemble` into a namespaced in-toto / DSSE-shaped provenance envelope
  (`prosoc/packet/schema.json`), shipped behind `--allow-unapproved`. Merged in
  PR #51 — the core engine the workstream is built toward now exists
  (`prosoc/packet/` + `scripts/assemble`).
- **WI-CARD-AUDIT-SKILLS** — Phase 0b, family-dispatched audit skills
  (resolved): `prosoc-card-audit` and `prosoc-card-audit-all` with per-family
  checklists under `.claude/skills/_shared/audit_checklists/`, including a
  bespoke charter shape and a new constitutions checklist; retires
  `prosoc-scenario-audit(-all)` into the generic dispatch. Merged in PR #54.
- **WI-PACKET-MANIFEST-FAMILY** — Phase 2, the manifest as an auditable card
  family (resolved): a sixth card family (`prosoc/manifests/`) mirroring the
  existing five, registered with `scripts/validate/status` and
  `prosoc-card-audit`; migrates the Phase 1 sample manifest into a real card.
  Merged in PR #56.
- **WI-PACKET-CI-DRIFT-CHECK** — Phase 3, CI packet-drift check (resolved):
  a `--check` flag on the packet CLI comparing an assembled packet against a
  checked-in golden file, plus a new CI workflow enumerating golden-having
  manifests. Merged in PR #59, closing out Phase 3.
- **WI-CARD-APPROVE-SKILLS** — corpus review-queue engine and the
  `prosoc-card-approve` / `prosoc-card-review` / `prosoc-card-review-all`
  skill stack (resolved; merged in PR #64, commit `6fe3152`): tooling to
  rank the corpus by what most needs review and to promote a card's
  lifecycle state from `AUDITED` to `APPROVED`, settled in
  `PROP-NORMATIVE-CARD-APPROVAL`. Works toward the corpus-approval exit
  criterion below — no card is promoted by this item itself, only the
  mechanism to do so; the pilot item below is the first to use it.
- **WI-CARD-APPROVAL-PILOT** — promote the 5 `sample_packet` cards to
  `APPROVED` (resolved; merged in PR #65, commit `0049f6c`): promoted
  charter, `asimov_three_laws`, `intersection_gesture_wait`,
  `navigate_lead_agent`, and `high_urgency` through `AUDITED` to
  `APPROVED`, then regenerated `sample_packet`'s golden packet without
  `--allow-unapproved` — the corpus's first production-mode packet.

Further work items are created via `/lrh-work-item` as each phase is planned
and added to `work_items:` as they land. Phases 0a, 0b, 1, 2, and 3 are
done, and the corpus-approval tooling (`WI-CARD-APPROVE-SKILLS`,
`WI-CARD-APPROVAL-PILOT`) is built and piloted; the exit criterion itself —
every card in the corpus reaching `APPROVED` — remains open. 11 of 32 cards
carried `APPROVED` as of 2026-08-06 — a point-in-time snapshot, not a
dynamically updated figure; see
[`FOCUS-NORMATIVE-PACKET-ASSEMBLY`](../../focus/current_focus.md) for the
latest count. Promotion continues via `prosoc-card-review-all`.

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
- Every card in the corpus reaches `APPROVED` (per `PROP-NORMATIVE-CARD-APPROVAL`'s
  framing of this as the workstream's second exit criterion; confirmed with
  the user 2026-08-01). Tooling for this (the review-queue engine and
  `prosoc-card-approve`/`prosoc-card-review`/`prosoc-card-review-all`
  skills) is built and piloted; the criterion itself is not yet met.

## Non-Goals

- Does not include Phase 4 (cryptographic signing; scenario→task/context
  auto-resolution) — explicitly deferred by the proposal; a future workstream
  owns it.
- Does not repair the dangling `example_scenarios` task references — a
  validator surfaces them; they are tracked as corpus work.
- Does not author scenario→task or scenario→context reference fields.

## Relationship to Design

- Governing proposal:
  [`project/design/proposals/adopted/normative-packet-assembly/00_proposal.md`](../../design/proposals/adopted/normative-packet-assembly/00_proposal.md)
  (`PROP-NORMATIVE-PACKET-ASSEMBLY`, adopted 2026-07-30).
- Governing proposal for the corpus-approval review pass:
  [`project/design/proposals/proposed/normative-card-approval/00_proposal.md`](../../design/proposals/proposed/normative-card-approval/00_proposal.md)
  (`PROP-NORMATIVE-CARD-APPROVAL`, proposed 2026-07-30).

## Open Questions

- `project/focus/current_focus.md` currently scopes the active focus to
  scenario-corpus maintenance; this workstream opens a new front and the focus
  file likely wants updating (out of scope for this skill).
- The `VALIDATED` (empirical, per `scenarios/workflow.md`) vs `VERIFIED`
  (production, per `constitutions/template.md` and the paper) stage-5 naming
  split must be resolved in Phase 0a, per the proposal's open question.
