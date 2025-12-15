# Prosoc: A Prosocial Robot Navigation Framework

**Prosoc** is a research-oriented Python framework for developing, evaluating, and reasoning about **prosocial robot navigation** systems. It is designed to support *constitutional AI–style approaches* to robotics, where navigation behavior is guided by an explicit, inspectable **charter of principles** rather than opaque reward functions alone.

The project emphasizes:

* Human-readable, source-controlled norms
* Machine-checkable policy artifacts
* Reproducibility and auditability
* Compatibility with learning-based and planning-based systems

Prosoc is currently in **active research development** and should be considered *alpha software*.

---

## Motivation

Autonomous robots increasingly operate in **human-centered environments**: homes, hospitals, workplaces, and public spaces. In these contexts, navigation is not merely about reaching a goal efficiently—it must also respect human safety, comfort, social norms, and ethical expectations.

Traditional navigation systems typically encode these concerns indirectly, via cost functions or heuristics. Prosoc takes a different approach:

> **Make the robot’s navigation principles explicit, inspectable, and enforceable.**

Inspired by work on **prosocial robotics**, **social navigation**, and **constitutional AI**, Prosoc treats navigation norms as a first-class artifact: a *charter* that can be read by humans, validated by machines, and referenced by downstream decision-making systems.

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
scripts/distill
```

This operation is:

* Schema-validated
* Atomic (no partial writes)
* Safe against malformed edits

### Previewing Changes

To preview changes without writing files:

```bash
scripts/distill --dry-run --show-diffs
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
