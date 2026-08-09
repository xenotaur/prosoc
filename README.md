# `prosoc`: A Prosocial Robot Navigation Framework

**`prosoc`** is a research-oriented Python framework for developing, evaluating, and reasoning about **prosocial robot navigation** systems: robotic systems that take responsibility for improving the physical and social environments within which they operate, consistent with achieving their own goals. In particular, `prosoc` is designed to support experimentation with *constitutional AI–style approaches* to robotics, where navigation behavior is guided by an explicit, inspectable **charter of principles** rather than solely relying on opaque black box models or hard-to-reason about algorithms and reward functions.

The `prosoc` project emphasizes and is developing tooling support for:

* Human-readable, source-controlled norms
* Machine-checkable policy artifacts
* Reproducibility and auditability
* Compatibility with learning-based and planning-based systems

`prosoc` is currently in **active research development** and should be considered *pre-alpha software*.

---

## Motivation

Autonomous robots increasingly operate in **human-centered environments**: homes, hospitals, workplaces, and public spaces. In these contexts, navigating humans do not merely care about reaching their goal efficiently, nor even simply respecting human safety, comfort, social norms, and ethical expectations; they actually do work to improve their navigation environments by providing signage, clearing obstructions, and providing directions to passersby. Robots operating in these environments should aspire to do the same.

Traditional navigation systems typically encode these concerns indirectly, via cost functions or heuristics, or by providing large numbers of rated examples to train learning systems. `prosoc` is designed to explore a different approach:

> **Make the robot’s navigation principles explicit, inspectable, and enforceable.**

Inspired by work on **prosocial psychology**, **social navigation**, and **constitutional AI**, `prosoc` treats navigation norms as a first-class artifact: a *charter* that can be read by humans, validated by machines, and referenced by downstream decision-making systems. This charter is based on the Social Navigation Principles and Scenarios from the [Principles and Guidelines for Evaluating Social Robot Navigation Algorithms](https://dl.acm.org/doi/10.1145/3700599) paper.

---

## Core Concepts

### 1. The Prosocial Navigation Charter

At the heart of Prosoc is a **navigation charter**, a structured set of principles (P0–P9) that define acceptable and unacceptable robot behavior.

* The charter is authored in **Markdown** (`charter.md`) for human readability
* Machine-readable policy is generated automatically as **YAML** (`charter.yml`)
* A **JSON Schema** (`schema.json`) defines the formal structure
* A distillation tool enforces consistency between representations

This ensures that the *human* and *machine* views of the robot’s norms never silently diverge.

### 2. Constitutional-Style Enforcement

Rather than embedding norms implicitly in code, Prosoc supports workflows where:

1. Principles are declared explicitly
2. Examples illustrate compliant and non-compliant behavior
3. Downstream systems (evaluators, planners, learning agents) reference the charter
4. CI and tests enforce consistency and validity

This mirrors emerging **constitutional AI** practices, adapted to embodied robotics.

### 3. Research-Friendly Architecture

Prosoc is intentionally modular and lightweight:

* No simulator or robot platform is assumed
* No specific planner or learning algorithm is required
* Components are designed to be reused across projects

The framework is meant to *support experimentation*, not constrain it.

---

## Repository Structure

Prosoc's normative content lives in six **card families**, each a directory
of literate (Markdown + embedded YAML) cards that share a common lifecycle,
plus a **packet assembler** that composes cards from any family into a
single machine-readable artifact for a downstream agent. See
[Normative Cards, Lifecycle, and Packet Assembly](#normative-cards-lifecycle-and-packet-assembly)
below for how these pieces fit together.

```text
prosoc/
├── prosoc/
│   ├── charter/               # The charter: P0–P9 principles (single document)
│   │   ├── charter.md         #   Human-readable charter (source of truth)
│   │   ├── charter.yml        #   Machine-readable charter (generated)
│   │   ├── schema.json        #   JSON Schema for validation
│   │   ├── distill.py         #   Markdown → YAML compiler
│   │   ├── loader.py          #   Runtime loader and validation (single gate)
│   │   └── runtime.py         #   Pydantic runtime models
│   │
│   ├── scenarios/              # Card family: concrete social navigation situations
│   ├── tasks/                  # Card family: abstract robot navigation goals
│   ├── contexts/                # Card family: situational/environmental settings
│   ├── constitutions/           # Card family: rule sets sent to a downstream agent
│   ├── manifests/                # Card family: named member lists for packets
│   │   └── sample_packet/         #   Example manifest + golden packet
│   │
│   ├── packet/                 # Manifest-driven packet assembler (resolve → load →
│   │                            # gate → assemble); see prosoc/packet/README.md
│   ├── auditor/                # Agentic card-audit tooling shared by prosoc-card-audit
│   └── literate/               # Shared Markdown+YAML literate-card infrastructure
│
├── scripts/
│   ├── distill/                # Per-family Markdown → YAML compilers
│   │   └── charter, scenarios, tasks, contexts, constitutions, manifests
│   ├── validate/               # Per-card and lifecycle-status validators
│   │   ├── card                #   Schema/prose validation for any card
│   │   └── status               #   Checks Markdown STATE line vs YAML state field
│   ├── assemble                # Manifest → guidance packet (the packet assembler CLI)
│   ├── develop                 # Install in editable mode
│   ├── build                   # Build distribution artifacts
│   ├── lint                    # Ruff static analysis
│   └── publish                 # (Future) publish to PyPI
│
├── tests/                      # Unit and integration tests, mirroring prosoc/
├── notebooks/                  # Research and prototyping notebooks
├── .github/workflows/          # CI workflows (tests, lint, charter check, packet-drift check)
├── pyproject.toml              # Packaging and tool configuration
└── README.md                   # This file
```

---

## Normative Cards, Lifecycle, and Packet Assembly

Prosoc represents robot-relevant norms as **normative cards**: literate
documents (Markdown narrative + an embedded, schema-validated YAML block)
that are human-reviewable and machine-consumable at once. There are six card
families:

| Family | Directory | Represents |
|---|---|---|
| Charter | [`prosoc/charter/`](prosoc/charter/README.md) | The ten prosocial navigation principles (P0–P9); a single document, not a card-per-directory family |
| Scenarios | [`prosoc/scenarios/`](prosoc/scenarios/README.md) | Concrete, situated social navigation cases |
| Tasks | [`prosoc/tasks/`](prosoc/tasks/README.md) | Abstract robot navigation goals, independent of scenario or context |
| Contexts | [`prosoc/contexts/`](prosoc/contexts/README.md) | Situational/environmental settings that shift how principles apply |
| Constitutions | [`prosoc/constitutions/`](prosoc/constitutions/README.md) | Rule sets (must/must not/should) intended to be sent to or enforced by a downstream agent |
| Manifests | [`prosoc/manifests/`](prosoc/manifests/README.md) | Human-authored, auditable lists naming which cards a packet should assemble |

Every family (other than the single-document charter) follows the same
pattern: author a card as `<name>/<family-singular>.md` (e.g.
`scenarios/frontal_approach/scenario.md`,
`constitutions/asimov_three_laws/constitution.md`) with a narrative and an
embedded YAML block, run `scripts/distill/<family>` to regenerate the
machine-readable `.yml`, and validate against that family's `schema.json`.
The Markdown is always the source of truth; generated files are never
hand-edited.

### Lifecycle

Every card carries a lifecycle state, one of `DRAFTED`, `EDITED`, `AUDITED`,
`APPROVED`, `VALIDATED`, `DEPRECATED`, or `RETIRED` (an optional `SOURCE`
stage precedes `DRAFTED`):

```
SOURCE (optional) → DRAFTED → EDITED → AUDITED → APPROVED → VALIDATED (optional) → DEPRECATED / RETIRED
```

`AUDITED` and `APPROVED` are deliberately distinct: `AUDITED` means an
**automated** audit — the `prosoc-card-audit` (single card) or
`prosoc-card-audit-all` (whole family/corpus) skill — has examined the card
and recorded findings in a sibling `audit.md`; `APPROVED` means a **human**
has reviewed the card (and its audit findings) and taken accountability for
its readiness. Downstream production use requires `APPROVED`, not merely
`AUDITED`. The state is authored once, in the card's embedded YAML (the
authoritative source), and projected into the Markdown status block's
`STATE` line — spelled `## Status` in scenarios and the charter, `## STATUS`
elsewhere; `scripts/validate/status` accepts either heading. See
[`prosoc/scenarios/workflow.md`](prosoc/scenarios/workflow.md) for the full
lifecycle definition, which applies uniformly across all six families.

### The Packet Assembler

A **manifest** (a card in the `manifests` family) names a set of member
cards drawn from any of the other five families. `scripts/assemble` resolves
those members, schema-validates and hashes each one, applies a **fail-closed
lifecycle gate** (by default every member must be `APPROVED` or better), and
composes them into a single machine-readable **guidance packet**: an
in-toto-style envelope with a `guidance` section for the downstream agent
and a `predicate` section recording provenance (builder identity, and each
member's id, family, path, hash, and lifecycle state) for an auditor.
Principles referenced across a packet's scenario/task/context members are
unioned and annotated (`emphasized` / `deprioritized` / `neutral`), never
silently dropped.

The entire card corpus reached `APPROVED` in PR #84 (2026-08-09), so
every current manifest assembles a production packet by default.
`scripts/assemble` still supports a `--allow-unapproved "<justification>"`
escape hatch for development packets built against any future
not-yet-`APPROVED` card; it lowers the gate floor and stamps a
non-production notice directly into the packet payload, so a development
packet is never byte-indistinguishable from a production one. A CI check
(`.github/workflows/packet.yml`) byte-compares every manifest's assembled
packet against a checked-in golden file and fails the build on drift.

See [`prosoc/packet/README.md`](prosoc/packet/README.md) for the full
pipeline, envelope shape, and CLI usage, and
[`PROP-NORMATIVE-PACKET-ASSEMBLY`](project/design/proposals/adopted/normative-packet-assembly/00_proposal.md)
for the design rationale behind these choices.

---

## Installation

Prosoc is designed to be installed in a standard Python environment.

### Development installation

```bash
pip install -e .
```

This installs Prosoc in *editable mode*, suitable for research and development.

### Dependencies

Runtime dependencies are intentionally minimal and include:

* `pyyaml`
* `jsonschema`
* `pydantic`

Development tools such as `ruff` and `black` are optional and can be installed via:

```bash
pip install .[dev]
```

---

## Using the Charter Tooling

### Distilling the Charter

After modifying `prosoc/charter/charter.md`, regenerate the machine-readable charter with:

```bash
scripts/distill/charter
```

This operation is:

* Schema-validated
* Atomic (no partial writes)
* Safe against malformed edits

### Previewing Changes

To preview changes without writing files:

```bash
scripts/distill/charter --dry-run --show-diffs
```

This is the recommended workflow before committing charter changes.

---

## Testing and Continuous Integration

Prosoc uses CI to enforce **code correctness**, **card consistency**, and
**packet reproducibility**, via four workflows under `.github/workflows/`:

* `tests.yml` — unit tests validate charter parsing, validation, and runtime loading
* `lint.yml` — Ruff and Black run in check-only mode (never auto-applied)
* `charter.yml` — guardrail check that `charter.md` and `charter.yml` remain in sync; fails if the charter is modified without regeneration
* `packet.yml` — guardrail check that every manifest's assembled packet matches its checked-in golden file (`prosoc/manifests/*/packet.golden.yml`); fails on drift in any member card across all six families

To run tests locally:

```bash
python -m unittest discover -v
```

---

## Intended Audience

Prosoc is intended for:

* Robotics researchers studying social or prosocial navigation
* Embodied AI researchers exploring norm-aware planning
* Developers interested in constitutional or policy-based AI systems
* Educators teaching ethical or human-centered robotics

It is **not** intended to be a drop-in navigation stack or end-user robot product.

---

## Project Status

Prosoc is currently:

* In active research development
* Evolving alongside ongoing academic work
* Subject to breaking changes

APIs, schemas, and charter contents may change as the research matures.


---

## Development Philosophy and Workflow

Prosoc follows a deliberately **conservative, explicit, and research-friendly software development philosophy**. The goal is not rapid feature accretion, but *clarity, auditability, and reproducibility*—especially for artifacts that encode normative or ethical assumptions.

### Guiding Principles

The development approach emphasizes:

* **Explicit over implicit behavior**  
  Important assumptions (e.g., navigation norms) are represented as data and documents, not hidden in code paths or learned weights.

* **Single sources of truth**  
  Human-authored artifacts (such as `charter.md`) are treated as authoritative and compiled into machine-readable forms. Generated files should never be edited by hand.

* **Human review before automation**  
  Tools validate, diff, and check consistency, but do not silently “fix” or rewrite important artifacts in CI.

* **Boundaries over cleverness**  
  Clear module boundaries, schemas, and runtime models are preferred over tightly coupled or overly abstract designs.

* **Tooling as guardrails, not gatekeepers**  
  Linters, formatters, and CI exist to catch mistakes and drift—not to enforce stylistic uniformity for its own sake.

---

### Scripts and Command-Line Workflow

The `scripts/` directory contains small, explicit wrappers around common development tasks. These scripts are intentionally simple and transparent, and can be read or modified easily.

Key scripts include:

* `scripts/distill/charter`  
  Regenerates the machine-readable charter (`charter.yml`) from the human-readable source (`charter.md`).  
  Supports `--dry-run` and `--show-diffs` to preview changes safely.
  Sibling wrappers (`scripts/distill/constitutions`, `scripts/distill/contexts`,
  `scripts/distill/scenarios`, `scripts/distill/tasks`) distill the other
  literate-programming content types the same way.

* `scripts/develop`  
  Installs Prosoc in editable mode (`pip install -e .`) for local development.

* `scripts/build`  
  Builds distribution artifacts using Python’s standard build system.

* `scripts/lint`  
  Runs static analysis using Ruff. Additional flags (such as `--fix`) may be passed through.

These scripts are intended to be the **canonical interface** for common tasks, both locally and in CI.

---

### Linting, Formatting, and Code Style

Prosoc uses a minimal, modern tooling stack:

* **Ruff** for linting and static analysis
* **Black** for code formatting

The responsibilities are intentionally separated:

* Black handles formatting deterministically.
* Ruff focuses on correctness, hygiene, and likely errors.

Formatting and linting are:
* Encouraged locally (and supported in VS Code)
* Enforced in CI in *check-only* mode
* Never auto-applied by CI

This ensures that all changes remain intentional and reviewable.

---

### VS Code Recommendations

Prosoc works well with VS Code, though no editor is required.

Recommended (optional) setup:
* Install the **Ruff** extension for inline lint feedback
* Use **Black** as the Python formatter
* Enable format-on-save if desired

These settings provide fast feedback during development while preserving full control over when changes are committed.

---

### Continuous Integration Philosophy

CI is used to enforce **invariants**, not to make decisions on behalf of developers.

In particular:
* CI verifies that each card family's Markdown source and generated YAML are consistent
* CI verifies that every manifest's assembled packet matches its checked-in golden file
* CI fails if generated artifacts are out of sync
* CI does not modify files or commit changes automatically

If CI fails due to charter inconsistency, the expected resolution is:

```bash
scripts/distill/charter
git commit
```

If CI fails due to packet drift (a manifest or a member card changed without
regenerating its golden packet), the expected resolution is:

```bash
scripts/assemble prosoc/manifests/<name>/manifest.yml \
  --allow-unapproved "CI packet-drift check (dev-mode golden; member card not yet APPROVED)" \
  > prosoc/manifests/<name>/packet.golden.yml
git commit
```

See [`prosoc/packet/README.md`](prosoc/packet/README.md) for more on the
`--allow-unapproved` escape hatch.

---


## License

This project is released under the **MIT License** (see `LICENSE`).

---

## Acknowledgments

This project builds on ideas from the social navigation and prosocial robotics literature, including work on:

* Social robot navigation principles
* Human-aware motion planning
* Constitutional AI

See the project documents and charter for detailed references and context.

---


## Disclaimer

This software is provided for research purposes only.

Robotic systems operating in real-world environments should undergo extensive safety testing, validation, and regulatory review before deployment.


