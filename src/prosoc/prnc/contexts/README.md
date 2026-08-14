# Contexts

This directory contains **context cards**: a Prosoc normative card family
representing the *situational and environmental settings* in which social
robot navigation occurs — public sidewalks, hospital corridors, high-urgency
emergencies, and so on.

Contexts complement [scenarios](../scenarios/README.md) and
[tasks](../tasks/README.md): a scenario is a concrete situated case and a
task is an abstract goal, while a context is the situational backdrop that
systematically shifts how the [charter's](../charter/README.md) principles
apply, independent of any one scenario or task.

---

## What Is a Context Card?

A context card describes a class of situation — not a specific encounter —
and explains:

- what kind of situation the context represents, and why it's normatively
  distinct from other contexts,
- how the context instantiates the P&G paper's context axes (cultural,
  diversity, environmental, task, interpersonal),
- which charter principles are typically **emphasized** or
  **deprioritized** in this context, and what tensions commonly arise,
- and the applicability limits of the context — what does and does not fall
  under it.

Context cards are deliberately qualitative and descriptive: they motivate
*why* principle weighting shifts in a given setting, without prescribing
specific robot behaviors or numeric weightings.

---

## Directory Structure

```text
prosoc/contexts/
├── README.md                # This file
├── template.md               # Recommended authoring template
├── schema.json                 # JSON Schema for context validation
├── distill.py                    # Context distiller
├── high_urgency/
│   └── context.md                 # Example context card
├── public_navigation/
│   └── context.md
├── routine_delivery/
│   └── context.md
├── guidance_docent/
│   └── context.md
└── ...                              # Additional contexts
```

Each context is authored as a Markdown file with an embedded YAML block,
following the same literate-card pattern as every other family. From each
`context.md`, `scripts/distill/contexts` generates a machine-readable
`context.yml`.

---

## Authoring a New Context

1. Copy `template.md` into a new subdirectory and rename it appropriately.
2. Write the context description, normative significance, and context-axes
   sections in prose.
3. Populate the embedded YAML block, including `principle_emphasis`
   (`emphasized` / `deprioritized` / `common_tensions`) and applicability
   `limits`.
4. Add a `## STATUS` section recording the context's lifecycle stage.
5. Run `scripts/distill/contexts` and validate.

---

## Lifecycle and Status

Each context includes a **STATUS** section indicating its lifecycle state,
authored machine-readably as a `state:` field in the embedded YAML (the
authoritative source) and projected onto the Markdown `## STATUS` block's
`STATE` line; `scripts/validate/status` checks the two agree. The lifecycle
is the same seven-state chain used across all six card families — `DRAFTED`,
`EDITED`, `AUDITED`, `APPROVED`, `VALIDATED`, `DEPRECATED`, `RETIRED` — see
[`prosoc/scenarios/workflow.md`](../scenarios/workflow.md) for the full
definition. `AUDITED` denotes a passing automated audit via
`prosoc-card-audit`; only `APPROVED` contexts should be treated as ready for
production use, including inclusion in an assembled packet.

---

## Relationship to the Charter and Other Families

- Contexts reference charter principles via `principle_emphasis`, the same
  cross-reference mechanism scenarios (`relevant_principles`) and tasks
  (`related_principles`) use.
- A context's `principle_emphasis.deprioritized` principles are never
  dropped from a packet that includes the context — the
  [packet assembler](../packet/README.md) annotates them as
  `deprioritized` rather than silently filtering them out, since removing a
  principle from an agent's view is itself a normative act.
- A context's `applies_to_tasks` and a task's own scope describe how the two
  families relate without either encoding the other's content.

---

## Intended Uses

Context cards are research artifacts, used to:

- explain why the same task or scenario calls for different behavior in
  different settings,
- ground the `context:` member of an assembled
  [packet](../manifests/README.md) manifest,
- and support evaluation setups that vary the situational backdrop
  independently of the specific encounter.
