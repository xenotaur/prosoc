---
id: FOCUS-NORMATIVE-PACKET-ASSEMBLY
title: Promote the normative card corpus to APPROVED
status: completed
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/adopted/normative-packet-assembly/00_proposal.md
---

# Current Focus

**This focus is complete.** The **manifest-driven normative packet
assembler** is built: `scripts/assemble` resolves a manifest's member
cards, schema-validates and hashes each one, applies a fail-closed
lifecycle gate, and composes them into a single machine-readable
guidance packet, with a CI drift check (`.github/workflows/packet.yml`)
keeping checked-in golden packets honest. The design is settled in
[`PROP-NORMATIVE-PACKET-ASSEMBLY`](../design/proposals/adopted/normative-packet-assembly/00_proposal.md)
(adopted), the work was governed by
[`WS-NORMATIVE-PACKET-ASSEMBLY`](../workstreams/resolved/WS-NORMATIVE-PACKET-ASSEMBLY.md)
(closed 2026-08-09), and prosoc's human-facing docs (top-level `README.md`,
all six family `README.md`s) were brought up to date with this
architecture in PR #67.

The workstream's final exit criterion — every card in the corpus
reaching `APPROVED`, not just the field/mechanism supporting it — was
met in PR #84 (2026-08-09): all 32 cards across all six families
(`scenarios`, `tasks`, `contexts`, `constitutions`, `charter`,
`manifests`) are now `APPROVED`. `scripts/assemble` no longer needs
`--allow-unapproved` to produce a production packet from any current
manifest; the escape hatch remains available for any future
not-yet-`APPROVED` card.

**No new focus has been chosen yet.** Per `WS-NORMATIVE-PACKET-ASSEMBLY`'s
own Purpose section, the packet was "the pivot between two halves of the
project: everything below it — authoring, distillation, schema
validation, agent auditing — is built and tested, and everything above
it — agent consumption, navigation — is blocked on there being a packet
to consume." That's now unblocked, but which front to open next is an
open decision, not made here.

## Scenario-corpus maintenance note

Any edit to a scenario's prose or YAML invalidates its prior audit — re-run
`prosoc-card-audit` (single) or `prosoc-card-audit-all` (family/corpus)
rather than assuming a stale audit still holds. `prosoc/scenarios/AUDIT_SUMMARY.md`
is a point-in-time index only; it does not self-update. This applies even
though every card currently carries `APPROVED` — a later content edit to
an `APPROVED` card still invalidates its audit the same way.

## Scope note

This file documents *prosoc's own engineering focus* (the LRH control plane's
"focus" concept). It is unrelated to any individual scenario's content
lifecycle state (SOURCE/DRAFTED/EDITED/AUDITED/VALIDATED, per
`prosoc/scenarios/workflow.md`) and to the P1–P8 social navigation charter
principles (`.claude/skills/_shared/principles.md`) — those are separate,
scenario-content concepts that this file does not track.
