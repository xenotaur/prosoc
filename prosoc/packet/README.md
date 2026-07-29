# prosoc.packet — normative packet assembler (Phase 1)

Turns a human-authored **manifest** naming member cards into a single
machine-readable **guidance packet** for a downstream agent, per
`PROP-NORMATIVE-PACKET-ASSEMBLY` (Decisions 2, 4, 5, 6).

## Pipeline

```
manifest.yml
  → manifest.load_manifest   (parse family+id members)
  → resolve.resolve          (locate cards)
  → loader.load_card         (schema-validate + hash + read state)  ← single validation gate
  → gate.gate                (fail-closed lifecycle gate)
  → assemble.assemble        (namespaced in-toto envelope, schema-validated)
```

## Usage

```bash
# Fail-closed by default: emits nothing unless every member is APPROVED.
scripts/assemble prosoc/packet/examples/sample_manifest.yml

# Development packet: lowers the floor and stamps a non-production marker
# (predicate.policy.escape_hatch + guidance.notice) into the payload.
scripts/assemble prosoc/packet/examples/sample_manifest.yml \
  --allow-unapproved "local eval; corpus not yet human-approved"
```

## Envelope shape

An in-toto-style statement with a reserved, DSSE-shaped `signatures: []` slot,
split into two audiences:

- **`guidance`** — what the agent consumes: each card namespaced by family/id
  (never deep-merged, so `scenario.context` never collides with a context
  card), `state` stripped, family root keys normalized, and a Decision-6
  **principle union** (`emphasis: emphasized | deprioritized | neutral`, none
  dropped). `subject.digest` covers the serialized `guidance` only, so a
  detached copy stays verifiable.
- **`predicate`** — what the auditor consumes: builder identity, gate policy
  (and any escape hatch), and each resolved card's `id`, `family`, `path`,
  `sha256`, and lifecycle `state`.

## Lifecycle gate

Production order `DRAFTED < EDITED < AUDITED < APPROVED < VALIDATED`; default
floor is `APPROVED`. `DEPRECATED`/`RETIRED` never ship. `--allow-unapproved`
lowers the floor to any live pre-approval state and records the bypass in the
payload — a development packet is never byte-indistinguishable from a
production one.

## Scope (Phase 1)

The manifest input here is minimal. Making manifests an auditable **card
family** (their own `manifest.md` + template + distiller + schema) is Phase 2;
cryptographic signing and CI packet-drift checks are Phases 3–4. See the
governing proposal for the full plan.
