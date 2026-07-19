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

```text
prosoc/
├── prosoc/
│   └── charter/
│       ├── charter.md        # Human-readable charter (source of truth)
│       ├── charter.yml       # Machine-readable charter (generated)
│       ├── schema.json       # JSON Schema for validation
│       ├── distill.py        # Markdown → YAML compiler
│       ├── loader.py         # Runtime loader and validation
│       └── runtime.py        # Pydantic runtime models
│
├── scripts/
│   ├── distill               # Safely regenerate charter.yml
│   ├── develop               # Install in editable mode
│   ├── build                 # Build distribution artifacts
│   └── publish               # (Future) publish to PyPI
│
├── tests/
│   └── charter/              # Unit and integration tests for charter tooling
│
├── notebooks/                # Research and prototyping notebooks
├── .github/workflows/        # CI workflows (tests, charter checks, lint)
├── pyproject.toml            # Packaging and tool configuration
└── README.md                 # This file
```

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

Prosoc uses CI to enforce both **code correctness** and **constitutional consistency**.

In particular:

* Unit tests validate charter parsing, validation, and runtime loading
* Guardrail tests ensure `charter.md` and `charter.yml` remain in sync
* CI fails if the charter is modified without regeneration

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
* CI verifies that `charter.md` and `charter.yml` are consistent
* CI fails if generated artifacts are out of sync
* CI does not modify files or commit changes automatically

If CI fails due to charter inconsistency, the expected resolution is:

```bash
scripts/distill/charter
git commit
```

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


