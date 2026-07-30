---
id: FOCUS-NORMATIVE-PACKET-ASSEMBLY
title: Implement the manifest-driven normative packet assembler
status: active
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/proposed/normative-packet-assembly/00_proposal.md
---

# Current Focus

The active focus is implementing the **manifest-driven normative packet
assembler**: the tooling that composes prosoc's normative cards (charter
principles, constitutions, tasks, contexts, scenarios) into a single
machine-readable guidance packet for a downstream agent. The design is settled
in [`PROP-NORMATIVE-PACKET-ASSEMBLY`](../design/proposals/proposed/normative-packet-assembly/00_proposal.md)
and the work is governed by
[`WS-NORMATIVE-PACKET-ASSEMBLY`](../workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md).

This is the pivot between two halves of the project: everything below the
packet — authoring, distillation, schema validation, agent auditing — is built
and tested, while everything above it — agent consumption, navigation — is
blocked on there being a packet to consume.

The workstream is phased. The immediate front is **Phase 0a**: insert the
`APPROVED` lifecycle state, normalize the STATUS blocks across all five card
families, and project a machine-readable `status` field from the fenced YAML
into the Markdown, enforced by `scripts/validate/status`. Phase 0a is the
unblocker for the rest and also settles the `VALIDATED` (empirical, per
`prosoc/scenarios/workflow.md`) vs `VERIFIED` (production, per
`prosoc/constitutions/template.md` and the paper) stage-5 naming question. Later
phases add the family-dispatched audit skills (0b), the assembler engine (1),
the manifest card family (2), and CI drift checks (3). Phase 4 (signing,
auto-resolution) is deferred.

Next concrete step: create the first Phase 0a work item via `/lrh-work-item`
under `WS-NORMATIVE-PACKET-ASSEMBLY`.

## Background: scenario-corpus maintenance (ongoing)

The prior focus — keeping the 20-scenario social navigation corpus under
`prosoc/scenarios/` audit-clean — remains an ongoing background
responsibility, not the active deliverable. The corpus reached a fully
audit-clean state in the 2026-07-22 corpus-wide audit
(`prosoc/scenarios/AUDIT_SUMMARY.md`: 20/20 audited, 0 blocking findings).
Keep it there as edits land:

- Run `/prosoc-card-audit` (single) or `/prosoc-card-audit-all` (full family
  or corpus) after any change to a scenario's prose or YAML, rather than
  assuming a prior audit still holds.
- Treat `prosoc/scenarios/AUDIT_SUMMARY.md` as a point-in-time index only — it
  does not self-update and must be regenerated after any re-audit.

Note that Phase 0a of the packet work will itself touch every scenario card's
STATUS block, so the two efforts intersect: STATUS normalization is packet
work, but it should leave each scenario's audit-clean content intact.

## Scope note

This file documents *prosoc's own engineering focus* (the LRH control plane's
"focus" concept). It is unrelated to any individual scenario's content
lifecycle state (SOURCE/DRAFTED/EDITED/AUDITED/VALIDATED, per
`prosoc/scenarios/workflow.md`) and to the P1–P8 social navigation charter
principles (`.claude/skills/_shared/principles.md`) — those are separate,
scenario-content concepts that this file does not track.
