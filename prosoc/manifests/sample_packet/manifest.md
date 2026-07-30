# Manifest: Sample Packet

## STATUS
- **STATE:** DRAFTED
- **SOURCE:** WI-PACKET-MANIFEST-FAMILY, migrated from prosoc/packet/examples/sample_manifest.yml (Phase 1)
- **DRAFTED:** Claude (WI-PACKET-MANIFEST-FAMILY), 2026-07-30
- **EDITED:** —
- **AUDITED:** —
- **VALIDATED:** —

---

## Manifest Summary

> **Required**

- **Manifest ID:** `sample_packet`
- **Manifest Name:** Sample Packet
- **Builder:** prosoc packet assembler (sample)
- **Member Count:** 5

---

## Manifest Description

A demonstration manifest exercising the assembler engine end to end: one
member from each of the five content card families. The whole corpus is
currently `DRAFTED`, so `scripts/assemble` on this manifest is fail-closed by
default and emits nothing; pass `--allow-unapproved "<why>"` to produce a
non-production packet stamped with the escape-hatch marker.

---

## Members

> **Required**

- `charter/charter` — the ten prosocial navigation principles, always
  included as the packet's normative grounding.
- `constitutions/asimov_three_laws` — a canonical historical constitution,
  demonstrating a root-wrapped card family in an assembled packet.
- `scenarios/intersection_gesture_wait` — a representative scenario
  exercising a gesture-based social navigation encounter.
- `tasks/navigate_lead_agent` — a representative abstract navigation task.
- `contexts/high_urgency` — a representative context, demonstrating
  principle emphasis/deprioritization in an assembled packet.

---

## Manifest Specification (Machine-Readable)

> **Required**

```yaml
id: sample_packet
name: Sample Packet
state: DRAFTED

builder: "prosoc packet assembler (sample)"

members:
  - {family: charter, id: charter}
  - {family: constitutions, id: asimov_three_laws}
  - {family: scenarios, id: intersection_gesture_wait}
  - {family: tasks, id: navigate_lead_agent}
  - {family: contexts, id: high_urgency}
```
