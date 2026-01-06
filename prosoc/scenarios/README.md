# Prosoc Social Navigation Scenarios

This directory contains **social navigation scenario documents** used by the Prosoc framework to illustrate, evaluate, and reason about prosocial robot navigation behavior.

Scenarios serve as *concrete, situated cases* that complement the abstract principles defined in the Prosocial Navigation Charter.

They are designed to be:

- **Human-readable** (for discussion, review, and pedagogy)
- **Machine-readable** (for evaluation, simulation, and analysis)
- **Normatively explicit** (clearly stating expectations and constraints)
- **Provenance-aware** (transparent about authorship and review status)

---

## What Is a Social Navigation Scenario?

A social navigation scenario describes:

- a physical and social context (e.g., hallway, sidewalk, shared space),
- the agents involved (robot, pedestrians, groups),
- the asymmetries of awareness, capability, or responsibility,
- the **expected behaviors** of a robot operating in that context,
- and the **charter principles** implicated by those behaviors.

Scenarios are not algorithms, policies, or reward functions. They are **normative reference cases** that help bridge theory, implementation, and evaluation.

---

## File Structure

Each scenario is authored as a Markdown file using a *literate specification* style:

```text
scenario_name.md   # Human-readable narrative + embedded YAML blocks
```

From each Markdown source, a machine-readable YAML representation can be generated using the Prosoc tooling.

This ensures that:
- humans edit and review the narrative form,
- machines consume the structured form,
- and the two remain consistent by construction.

---

## Key Files in This Directory

```text
scenarios/
├── README.md                  # This file
├── workflow.md                # Scenario lifecycle and review process
├── schema.json                # JSON Schema for scenario validation
├── scenario_template.md       # Recommended authoring template
├── frontal_approach_01.md     # Example scenario
├── pedestrian_overtaking_01.md
└── ...                         # Additional scenarios
```

---

## Authoring a New Scenario

To create a new scenario:

1. Copy `scenario_template.md` and rename it appropriately.
2. Write a clear, human-readable scenario narrative.
3. Populate the embedded YAML block with structured fields.
4. Reference relevant charter principles (e.g., `P1`, `P5`, `P9`).
5. Add a **Status** section describing the scenario’s lifecycle stage.
6. Validate and distill the scenario using the provided tooling.

See `workflow.md` for guidance on drafting, editing, auditing, and validation stages.

---

## Lifecycle and Status

Each scenario should include a **Status** section indicating its current state, such as:

- DRAFTED
- EDITED
- AUDITED
- VALIDATED
- DEPRECATED

Only scenarios that have been **AUDITED** should be treated as ready for use in evaluation or experiments.

See `workflow.md` for the full lifecycle definition.

---

## Relationship to the Charter

Scenarios are explicitly linked to the **Prosocial Navigation Charter**:

- Each scenario lists the charter principles it implicates.
- Scenarios provide concrete interpretations of abstract principles.
- Conflicts or ambiguities revealed by scenarios can motivate charter refinement.

The charter defines *what matters*; scenarios show *what that means in practice*.

---

## Intended Uses

Scenarios in this directory may be used for:

- designing simulation or experimental tasks
- evaluating navigation algorithms or learned policies
- annotating video or log data
- training or prompting language-model-based planners
- teaching social and ethical aspects of robot navigation

They are **research artifacts**, not deployment specifications.

---

## Contribution Philosophy

Contributions are welcome and encouraged.

You do not need to be “finished” or “perfect” to contribute a scenario. Drafts are valuable.

However:
- provenance must be clear,
- human audit is required before evaluation use,
- and empirical claims should be supported when asserted.

---

## Disclaimer

These scenarios are provided for **research and discussion purposes only**.

They do not constitute safety certification, regulatory approval, or ethical endorsement of any deployed robotic system.

