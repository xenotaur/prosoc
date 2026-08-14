# Tasks

This directory contains **task cards**: a Prosoc normative card family
representing the *abstract navigation goals* a robot pursues — delivering an
object, following an agent, leading an agent, navigating point to point —
independent of any specific scenario or environmental context.

Tasks complement [scenarios](../scenarios/README.md) and
[contexts](../contexts/README.md): a task is what the robot is trying to
accomplish in the abstract, a scenario is a concrete situated encounter that
may involve that task, and a context is the situational backdrop the task is
carried out in.

---

## What Is a Task Card?

A task card describes a goal, not a situation. It states:

- what goal the robot is pursuing and what success means in abstract terms,
- what the task explicitly includes and excludes (e.g., whether yielding or
  rerouting are part of the task itself or a subordinate behavior),
- which charter principles typically come into tension with the task, and
- task-level failure modes that indicate poor execution independent of
  social context (e.g., failing to reach a destination) — as distinct from
  scenario- or context-specific failures, which do not belong here.

Task descriptions are deliberately independent of specific environments,
agent counts, or social norms; those belong to scenarios and contexts.

---

## Directory Structure

```text
prosoc/tasks/
├── README.md                     # This file
├── template.md                    # Recommended authoring template
├── schema.json                     # JSON Schema for task validation
├── distill.py                       # Task distiller
├── AUDIT_SUMMARY.md                  # Point-in-time index of audit results
├── deliver_object/
│   └── task.md                        # Example task card
├── navigate_follow_agent/
│   └── task.md
├── navigate_lead_agent/
│   └── task.md
├── navigate_point_to_point/
│   └── task.md
└── ...                                  # Additional tasks
```

Each task is authored as a Markdown file with an embedded YAML block. From
each `task.md`, `scripts/distill/tasks` generates a machine-readable
`task.yml`.

---

## Authoring a New Task

1. Copy `template.md` into a new subdirectory and rename it appropriately.
2. Write the task description and scope/boundaries in prose, keeping it
   independent of any specific environment or scenario.
3. Populate the embedded YAML block, including `related_principles`,
   `common_failure_modes`, and (optionally) `example_scenarios` for
   traceability.
4. Add a `## STATUS` section recording the task's lifecycle stage.
5. Run `scripts/distill/tasks` and validate.

Note that `example_scenarios` is for discoverability only — it is not a
structural cross-reference the packet assembler resolves, and some existing
entries currently point to scenario IDs that don't (yet) exist; that is
tracked as corpus cleanup, not a packet-assembly defect.

---

## Lifecycle and Status

Each task includes a **STATUS** section indicating its lifecycle state,
authored machine-readably as a `state:` field in the embedded YAML (the
authoritative source) and projected onto the Markdown `## STATUS` block's
`STATE` line; `scripts/validate/status` checks the two agree. The lifecycle
is the same seven-state chain used across all six card families — `DRAFTED`,
`EDITED`, `AUDITED`, `APPROVED`, `VALIDATED`, `DEPRECATED`, `RETIRED` — see
[`prosoc/scenarios/workflow.md`](../scenarios/workflow.md) for the full
definition. `AUDITED` denotes a passing automated audit via
`prosoc-card-audit` (see `AUDIT_SUMMARY.md` for the family's current
audit status); only `APPROVED` tasks should be treated as ready for
production use, including inclusion in an assembled packet.

---

## Relationship to the Charter and Other Families

- Tasks reference charter principles via `related_principles`, the same
  cross-reference mechanism scenarios (`relevant_principles`) and contexts
  (`principle_emphasis`) use.
- Tasks are a permitted member family for a packet
  [manifest](../manifests/README.md); the
  [packet assembler](../packet/README.md) unions a task's
  `related_principles` with those of any scenario or context also in the
  manifest.
- A scenario's `intended_robot_task` field is currently free text, not a
  structural reference to a task card — inferring packet membership by
  traversal from a scenario is deferred (see
  [`PROP-NORMATIVE-PACKET-ASSEMBLY`](../../project/design/proposals/adopted/normative-packet-assembly/00_proposal.md)'s
  Non-Goals); manifest membership is stated explicitly today.

---

## Intended Uses

Task cards are research artifacts, used to:

- name the abstract goal a scenario or evaluation exercises,
- ground the `task:` member of an assembled
  [packet](../manifests/README.md) manifest,
- and support evaluation setups that vary the task independently of the
  specific scenario or context.
