---
id: FOCUS-NORMATIVE-PACKET-ASSEMBLY
title: Promote the normative card corpus to APPROVED
status: active
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/adopted/normative-packet-assembly/00_proposal.md
---

# Current Focus

The **manifest-driven normative packet assembler** is built: `scripts/assemble`
resolves a manifest's member cards, schema-validates and hashes each one,
applies a fail-closed lifecycle gate, and composes them into a single
machine-readable guidance packet, with a CI drift check
(`.github/workflows/packet.yml`) keeping checked-in golden packets honest.
The design is settled in
[`PROP-NORMATIVE-PACKET-ASSEMBLY`](../design/proposals/adopted/normative-packet-assembly/00_proposal.md)
(adopted), the work is governed by
[`WS-NORMATIVE-PACKET-ASSEMBLY`](../workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md),
and prosoc's human-facing docs (top-level `README.md`, all six family
`README.md`s) were brought up to date with this architecture in PR #67.
Phases 0a through 3 of the workstream are all complete; only Phase 4
(signing, `related_contexts`/`example_scenarios` auto-resolution) remains
deferred.

The active front is now **corpus promotion**: getting every card in the
corpus to `APPROVED`, not just the field/mechanism supporting each
principle. The user confirmed this scope directly on 2026-08-01 — note that
`WS-NORMATIVE-PACKET-ASSEMBLY`'s own Exit Criteria section does not yet
state this explicitly (its bullets cover schema/tooling support for the
`APPROVED` state, not full-corpus completion), so don't cite a specific
numbered criterion for it; treat this paragraph, not the WS file, as the
source for that requirement until the WS file is updated to match. As of
this writing (live count, not a cached snapshot — re-run before trusting
this number):

| Family | APPROVED | AUDITED | DRAFTED | Total |
|---|---|---|---|---|
| Scenarios | 5 | 3 | 12 | 20 |
| Tasks | 3 | 1 | 0 | 4 |
| Contexts | 1 | 3 | 0 | 4 |
| Constitutions | 1 | 1 | 0 | 2 |
| Charter | 1 | 0 | 0 | 1 |
| **Total** | **11** | **8** | **12** | **31** |

`AUDITED` cards are ready for a human `APPROVED` pass; `DRAFTED` cards still
need an audit first. Several sessions (PRs #68–#71) have been promoting
cards in batches of ~5 using `prosoc-card-review-all` /
`prosoc-card-audit-all`; continue that pattern — the ranked review queue is
`scripts/validate/review-queue`.

Next concrete step: keep running `prosoc-card-review-all` (or
`prosoc-card-audit` for one card at a time) against the remaining 20
non-`APPROVED` cards, prioritizing the 8 already `AUDITED` since those are
closest to done.

## Scenario-corpus maintenance note

Any edit to a scenario's prose or YAML invalidates its prior audit — re-run
`prosoc-card-audit` (single) or `prosoc-card-audit-all` (family/corpus)
rather than assuming a stale audit still holds. `prosoc/scenarios/AUDIT_SUMMARY.md`
is a point-in-time index only; it does not self-update.

## Scope note

This file documents *prosoc's own engineering focus* (the LRH control plane's
"focus" concept). It is unrelated to any individual scenario's content
lifecycle state (SOURCE/DRAFTED/EDITED/AUDITED/VALIDATED, per
`prosoc/scenarios/workflow.md`) and to the P1–P8 social navigation charter
principles (`.claude/skills/_shared/principles.md`) — those are separate,
scenario-content concepts that this file does not track.
