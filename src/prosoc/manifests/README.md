# Manifests

This directory contains **manifest cards**: a Prosoc normative card family
that names the member cards a
[packet assembler](../packet/README.md) run should compose into a single
machine-readable **guidance packet** for a downstream agent. A manifest is
the newest of the six card families (Phase 2 of
[`PROP-NORMATIVE-PACKET-ASSEMBLY`](../../project/design/proposals/adopted/normative-packet-assembly/00_proposal.md)),
and the only family whose cards reference cards from every other family
rather than describing navigation content directly.

---

## What Is a Manifest Card?

A manifest card is a small, human-authored, auditable list. It states:

- **who** is building packets from it (`builder`),
- **which cards** belong in the packet, each named by `family` + the
  member's locator `id` (e.g. `{family: scenarios, id: frontal_approach_01}`),
  and
- **why** those particular members were chosen together — what downstream
  agent or purpose the assembled packet serves.

A manifest names members; it does not embed or duplicate their content. The
[packet assembler](../packet/README.md) resolves each named member at
assembly time, so a packet always reflects the current state of its member
cards. A manifest must never name another manifest as a member.

This is deliberately a human-in-the-loop design (Decision 3 of the governing
proposal): the alternative — inferring a packet's membership automatically by
graph traversal from a scenario — is disqualified today because the
scenario→task and scenario→context reference edges the traversal would need
don't exist in the corpus yet. A manifest is the auditable, human-approved
intermediary that stands between the corpus and the downstream agent.

---

## Directory Structure

```text
prosoc/manifests/
├── README.md                  # This file
├── template.md                  # Recommended authoring template
├── schema.json                    # JSON Schema for manifest validation
├── distill.py                       # Manifest distiller
└── sample_packet/
    ├── manifest.md                    # Example manifest card
    ├── manifest.yml                     # Generated machine-readable manifest
    ├── audit.md                           # Audit findings
    └── packet.golden.yml                   # Checked-in golden packet (CI drift check)
```

Each manifest is authored as a Markdown file with an embedded YAML block,
following the same literate-card pattern as every other family. From each
`manifest.md`, `scripts/distill/manifests` generates a machine-readable
`manifest.yml`.

---

## Authoring a New Manifest

1. Copy `template.md` into a new subdirectory and rename it appropriately.
2. Write the manifest description: what downstream agent or purpose the
   assembled packet serves, and why these members belong together.
3. List each member under `## Members` with a one-line rationale, and
   populate the embedded YAML's `members:` list with matching
   `{family, id}` pairs.
4. Add a `## STATUS` section recording the manifest's lifecycle stage.
5. Run `scripts/distill/manifests` and validate.
6. Generate the packet and its golden file (see
   [`prosoc/packet/README.md`](../packet/README.md#ci-packet-drift-check-phase-3)):
   ```bash
   scripts/assemble prosoc/manifests/<name>/manifest.yml \
     --allow-unapproved "<justification>" \
     > prosoc/manifests/<name>/packet.golden.yml
   ```
   so `.github/workflows/packet.yml` can catch future drift.

---

## Lifecycle and Status

Each manifest includes a **STATUS** section indicating its lifecycle state,
authored machine-readably as a `state:` field in the embedded YAML (the
authoritative source) and projected onto the Markdown `## STATUS` block's
`STATE` line; `scripts/validate/status` checks the two agree. The lifecycle
is the same seven-state chain used across all six card families — `DRAFTED`,
`EDITED`, `AUDITED`, `APPROVED`, `VALIDATED`, `DEPRECATED`, `RETIRED` — see
[`prosoc/scenarios/workflow.md`](../scenarios/workflow.md) for the full
definition.

A manifest's own lifecycle state governs *the manifest card itself* (has a
human approved this particular grouping of members?) and is independent of
each member card's lifecycle state, which the
[packet assembler's fail-closed gate](../packet/README.md#lifecycle-gate)
checks separately at assembly time. A `DRAFTED` manifest naming five
`APPROVED` members is a perfectly valid manifest — assembling from it just
means a human hasn't yet signed off on *this particular grouping*.

---

## Relationship to the Packet Assembler

`prosoc/packet/manifest.py` reads any manifest YAML with a `members`/
`builder` shape — whether from this directory or an ad-hoc file — so this
family's schema and the assembler's expectations are the same contract. See
[`prosoc/packet/README.md`](../packet/README.md) for the full resolve →
load → gate → assemble pipeline, the envelope shape, and CLI usage.
