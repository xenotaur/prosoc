---
family: manifests
card: sample_packet
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-07-30
---

# Audit: Sample Packet

- **Card:** `prosoc/manifests/sample_packet/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-07-30
- **Verdict:** Ready, no issues found

## Findings

No findings.

## Prose/YAML Consistency

Manifest Summary (`Manifest ID: sample_packet`, `Manifest Name: Sample
Packet`, `Builder: prosoc packet assembler (sample)`, `Member Count: 5`)
matches `id`, `name`, `builder`, and `len(members)` exactly. The Members
section lists 5 bullets, one per `members[]` entry, with no prose bullet
lacking a YAML counterpart or vice versa.

## Schema Compliance

- `scripts/distill/manifests --dry-run --show-diffs` produced no diff and no
  schema validation error (whole-family dry-run; the corpus's only other
  manifest — none — is not applicable, this is the sole card in the family).
- `members[]` has only `family`/`id` per entry; no `additionalProperties`
  violations.
- No `members[].family` is `manifests` — all five are valid content families.
- No duplicate `{family, id}` pairs.

## Member Resolvability

All five members resolve and load via `prosoc.packet.loader.load_card`:

| Member | Resolves | State |
|---|---|---|
| `charter/charter` | Yes | DRAFTED |
| `constitutions/asimov_three_laws` | Yes | EDITED |
| `scenarios/intersection_gesture_wait` | Yes | DRAFTED |
| `tasks/navigate_lead_agent` | Yes | DRAFTED |
| `contexts/high_urgency` | Yes | DRAFTED |

No dangling members. All member states are pre-`APPROVED` (informational
only, per this checklist — the packet assembler's own fail-closed gate is
the enforcement point, not this audit): `scripts/assemble` on this manifest
is fail-closed by default with the default `APPROVED` threshold, and only
emits a packet with `--allow-unapproved`, as documented in the manifest's
own Manifest Description.

## Completeness

Manifest Summary, Manifest Description, and Members are all present and
populated. No blank required fields.
