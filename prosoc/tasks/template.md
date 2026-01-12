# Task: <Human-Readable Task Name>

## STATUS
- **STATE:** DRAFTED
- **SOURCE:** <paper, prior framework, common navigation task>
- **DRAFTED:** <author or system, date>
- **EDITED:** <optional>
- **AUDITED:** <optional>
- **VALIDATED:** <optional>

---

## Task Summary

> **Required**

- **Task ID:** <canonical_task_id>
- **Task Name:** <concise human-readable name>
- **Task Type:** <navigation | interaction | coordination>
- **Primary Intent:** <one-line statement of what the robot is trying to accomplish>
- **Applies To:** <single robot | multi-robot | human-robot>

---

## Task Description

> **Required**

Provide a clear, human-readable description of the task, including:
- what goal the robot is pursuing,
- what success means in abstract terms,
- and what makes this task distinct from other navigation tasks.

This description should be:
- independent of specific environments,
- independent of specific human behaviors,
- and understandable without reference to any particular scenario.

Avoid geometric layouts, agent counts, or social norms here; those belong to scenarios and contexts.

---

## Task Scope and Boundaries

> **Required**

Explicitly state:
- what this task **includes**,
- what it **does not include**.

Clarify common confusions, such as:
- how this task differs from related tasks,
- whether yielding, stopping, or rerouting are part of the task or subordinate behaviors.

---

## Relationship to Prosocial Navigation Principles

> **Required**

Describe how this task interacts with the Prosocial Navigation Charter:
- which principles are typically in tension with this task,
- which principles commonly constrain task execution,
- and how task success may trade off with social quality.

This section should remain descriptive, not prescriptive.

---

## Common Failure Modes (Task-Level)

> **Optional but recommended**

List failures that indicate poor task execution *independent of social context*, such as:
- failure to reach a destination,
- excessive delay without justification,
- abandonment of the task.

Do **not** list scenario-specific or context-specific failures here.

---

## Example Scenarios (Non-Exhaustive)

> **Optional but recommended**

List representative Scenario IDs that commonly involve this task.

This section is for traceability and discoverability only.

---

## Task Specification (Machine-Readable)

> **Required**

```yaml
id: <canonical_task_id>
name: <Human-Readable Task Name>

summary: >
  <One–two sentence abstract description of the task’s intent>

task_type: <navigation | interaction | coordination>

primary_intent: >
  <Concise description of the robot’s goal>

scope:
  includes:
    - <What is explicitly part of this task>
  excludes:
    - <What is explicitly not part of this task>

related_principles:
  - <P0–P9 identifiers typically implicated by this task>

common_failure_modes:
  - <abstract task-level failure>

example_scenarios:
  - <scenario_id>
