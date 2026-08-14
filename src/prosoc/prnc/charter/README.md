# Charter

This directory holds the **Prosocial Robot Navigation Charter**: the single
document that defines the ten prosocial navigation principles, P0–P9. Unlike
the other five card families, the charter is not a directory of many cards —
it is one document that serves as the normative grounding every other family
references.

---

## Directory Structure

```text
prosoc/charter/
├── charter.md      # Human-readable charter (source of truth)
├── charter.yml      # Machine-readable charter (generated)
├── schema.json       # JSON Schema for validation
├── distill.py         # Markdown → YAML compiler
├── loader.py            # Runtime loader and validation (single validation gate)
├── runtime.py             # Pydantic runtime models
└── audit.md                # Findings from the most recent prosoc-card-audit run
```

---

## What Is the Charter?

The charter defines **what matters**: a normative, non-modifiable
specification of how a robot *ought* to behave, expressed as ten principles
(P0–P9). It is not a controller, policy, or learned model — it is the shared
normative grounding that scenarios, tasks, contexts, and constitutions all
reference or implicate.

Each principle in `charter.md` includes a normative statement, a
human-readable explanation, illustrative examples, and a severity level,
followed by an embedded YAML block capturing the same content
machine-readably. `distill.py` extracts and validates all ten principle YAML
blocks plus the document-level `state:` field into `charter.yml`.

See the top-level [README's "Core Concepts"](../../README.md#core-concepts)
section for the charter's role in prosoc's constitutional-AI-style approach,
and [`prosoc/charter/charter.md`](charter.md) itself for the principles.

---

## Lifecycle and Status

The charter carries a single, document-level lifecycle state — it applies to
the charter as a whole, not to individual principles — one of `DRAFTED`,
`EDITED`, `AUDITED`, `APPROVED`, `VALIDATED`, `DEPRECATED`, or `RETIRED`. The
state is authored in the embedded `state:` field near the top of
`charter.md` (the authoritative source) and projected onto the Markdown
`## Status` block's `STATE` bullet; `scripts/validate/status` checks the two
agree.

`AUDITED` means the `prosoc-card-audit` skill has examined the charter and
recorded findings in `audit.md` — using a bespoke audit shape, since the
charter is a single multi-principle document rather than a card-per-directory
family. `APPROVED` means a human has reviewed the charter and its audit
findings and taken accountability for its readiness; downstream production
use (including inclusion in an assembled packet) should require `APPROVED`,
not merely `AUDITED`. See
[`prosoc/scenarios/workflow.md`](../scenarios/workflow.md) for the full
lifecycle definition, which applies uniformly across all six card families.

---

## Distilling the Charter

After modifying `charter.md`, regenerate the machine-readable
`charter.yml`:

```bash
scripts/distill/charter
```

Preview changes without writing files:

```bash
scripts/distill/charter --dry-run --show-diffs
```

Distillation is schema-validated and atomic; `loader.py` is the *only*
runtime validation gate for the charter — `runtime.py` assumes all data
passed through it already.

---

## Relationship to the Packet Assembler

The charter is a permitted member family for a packet
[manifest](../manifests/README.md); a manifest typically includes
`{family: charter, id: charter}` so every assembled packet carries the
principles as normative grounding. See
[`prosoc/packet/README.md`](../packet/README.md) for how the assembler
resolves, gates, and embeds charter content alongside other families.

---

## Relationship to Other Families

Scenarios reference principles via `relevant_principles`, tasks via
`related_principles`, and contexts via `principle_emphasis`. The packet
assembler unions these references (Decision 6 of
[`PROP-NORMATIVE-PACKET-ASSEMBLY`](../../project/design/proposals/adopted/normative-packet-assembly/00_proposal.md))
so a packet's `guidance` always carries the full set of principles
implicated by its other members, annotated by emphasis rather than filtered.
