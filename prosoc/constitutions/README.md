# Constitutions

This directory defines **Constitution Cards**: a Prosoc normative card type for representing
**robot or agent constitutions** as structured, auditable, machine-consumable artifacts.

A constitution, in this sense, is a **high-level normative rule set** intended to be
*sent to or enforced by an AI or robotic system*, for example as:
- system instructions,
- prompt prefixes,
- runtime policy constraints,
- or evaluation-time violation criteria.

This directory parallels other Prosoc card families (e.g., `scenarios/`) and follows the
same **literate + schema-validated** design philosophy.

---

## Directory Structure

```text
prosoc/constitutions/
├── asimov_three_laws/
│   └── constitution.md      # Example constitution card (historical baseline)
├── distill.py               # Constitution distiller
├── schema.json              # JSON Schema for constitution YAML blocks
└── template.md              # Template for new constitution cards
```

---

## What Is a Constitution Card?

A **constitution card** is a Markdown document with:

1. **Human-auditable context** (Markdown)
   - purpose and scope
   - provenance and assumptions
   - known ambiguities and failure modes
   - amendment history and review status

2. **Machine-readable normative content** (embedded YAML)
   - a structured set of rules (must / must not / should)
   - explicit priorities and conflict resolution
   - runtime and evaluation metadata

This design allows constitutions to be:
- reviewed and debated by humans,
- validated and consumed by tools,
- versioned and amended over time.

---

## Relationship to Prior Work

This directory is inspired by:
- *Generating Robot Constitutions* and the Asimov benchmark,
- Constitutional AI–style approaches,
- and earlier work on normative rule systems in robotics.

Unlike most prior approaches, Prosoc treats constitutions as
**first-class governed artifacts**, not just prompt text or benchmark inputs.

---

## The Distillation Process

Constitution cards are **not used directly at runtime**.

Instead, they are processed by the **constitution distiller** (`distill.py`), which:

1. Extracts the embedded YAML block from each `constitution.md`
2. Validates it against `schema.json`
3. Emits a distilled, machine-consumable representation
4. Attaches provenance metadata (source file, hash, etc.)

This mirrors the distillation process used for scenarios and other Prosoc cards.

> Distillation is intentionally conservative:
> - exactly one YAML block is allowed per card
> - schema violations fail fast
> - rendering decisions are *out of scope*

---

## Rendering and Use at Runtime

The distiller **does not** decide how a constitution is rendered into text.

Rendering (e.g., turning a constitution into a system prompt or instruction block)
is handled by separate tooling and may vary by:
- model,
- deployment context,
- runtime constraints (token limits),
- or evaluation setup.

This separation keeps:
- **normative content** stable and auditable,
- **rendering policy** explicit and testable.

---

## Example: Asimov’s Three Laws

The `asimov_three_laws/` example encodes the classic Three Laws of Robotics
as a constitution card.

It is included as:
- a historical reference,
- a baseline for benchmarks,
- and a demonstration of how high-impact normative rules
  can be represented in a structured, auditable form.

It is **not** intended as a sufficient modern safety system.

---

## Creating a New Constitution

1. Copy `template.md` into a new subdirectory
2. Fill in the Markdown sections for context and auditability
3. Define the normative rules in the embedded YAML block
4. Run the constitution distiller
5. Use a renderer to generate runtime instructions as needed

---

## Design Principles

Constitution cards are designed to be:

- **Auditable** – humans can understand and critique them
- **Machine-checkable** – schemas enforce structure and consistency
- **Composable** – can be generated from or linked to other Prosoc cards
- **Amendable** – changes are explicit and reviewable
- **Research-friendly** – suitable for benchmarking and reproducibility

---

## Status

Constitution support is under active development.

The current focus is on:
- establishing a stable representation format,
- enabling distillation and validation,
- and supporting constitution generation and amendment workflows.

Rendering, auto-amendment, and evaluation integrations are expected to evolve
as part of ongoing research.