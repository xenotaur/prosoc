# prosoc.packet — normative packet assembler (Phase 1–3)

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
scripts/assemble prosoc/manifests/sample_packet/manifest.yml

# Development packet: lowers the floor and stamps a non-production marker
# (predicate.policy.escape_hatch + guidance.notice) into the payload.
scripts/assemble prosoc/manifests/sample_packet/manifest.yml \
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

## Scope

The manifest a packet is assembled from is itself an auditable **card
family**, `prosoc/manifests/` (its own `manifest.md` + template + distiller +
schema, Phase 2) — this engine's `manifest.py` reads any manifest YAML with a
`members`/`builder` shape, whether from `prosoc/manifests/` or an ad-hoc file.
Cryptographic signing is Phase 4. See the governing proposal for the full
plan.

## CI packet-drift check (Phase 3)

`--check` assembles as usual (respecting `--allow-unapproved`), then
byte-compares the rendered packet against a checked-in golden file at
`<manifest_dir>/packet.golden.yml` instead of printing it. Goldens are
always YAML, so `--check` rejects `--format json` (exit 2) rather than
comparing incompatible serializations:

```bash
scripts/assemble prosoc/manifests/sample_packet/manifest.yml --check
```

- Exact match: exit 0, silent.
- Drift: exit 1, unified diff on stderr.
- No golden file yet: exit 1, an error explaining how to create one.

**Generate a golden in the same mode you intend to ship.** There is no CLI
flag to write or regenerate one — redirect a normal run:

```bash
scripts/assemble prosoc/manifests/sample_packet/manifest.yml \
  > prosoc/manifests/sample_packet/packet.golden.yml
```

`sample_packet`'s golden is production-mode (`--allow-unapproved` omitted):
all five of its members reached `APPROVED` in `WI-CARD-APPROVAL-PILOT`, the
corpus's first production-mode packet. A manifest whose members are **not**
all `APPROVED` yet can only produce a dev-mode golden — regenerate with
`--allow-unapproved "<justification>"` instead, and keep the same
justification string between golden generation and whatever CI step checks
it, or the check spuriously fails on the notice text alone. Once every
member of such a manifest reaches `APPROVED`, regenerate its golden in
production mode too, the same way this one was.

`.github/workflows/packet.yml` enumerates every `prosoc/manifests/*/packet.golden.yml`
and runs `--check` against each — not a CLI `--check-all` mode. Editing *any*
member card pulled into a manifest (not just the manifest file itself)
changes the assembled packet and trips the corresponding golden's check; this
is intentional (it is the drift the check exists to catch) — regenerate the
golden as part of that change.
