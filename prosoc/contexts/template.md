# Core Context Card Template

## STATUS
- **STATE:** DRAFTED | STABLE | DEPRECATED
- **CONTEXT TYPE:** CORE
- **SOURCE:** <P&G paper, literature, real-world domain>
- **CREATED:** <date>
- **MODIFIED:** <date>
- **AUDITED:** <optional>
- **VALIDATED:** <optional>

---

## Context Summary

> **Required**

- **Context ID:** <canonical_context_id>
- **Context Name:** <short descriptive name>
- **Context Class:** core
- **Primary Role of Robot:** <e.g., neutral navigator | service provider | guide | emergency responder>
- **Applies To Tasks:** <list of compatible task IDs or “multiple”>

---

## Context Description

> **Required**

Provide a concise, human-readable description of this context.

This section should explain:
- what kind of situation this context represents,
- why it is normatively distinct from other contexts,
- and what assumptions humans are likely to make about the robot’s role.

This description should:
- be understandable without reference to any specific scenario,
- avoid encoding task logic,
- avoid prescribing specific behaviors.

---

## Normative Significance

> **Required**

Explain *why this context matters* for social robot navigation.

Specifically:
- what kinds of trade-offs are foregrounded,
- how expectations differ from baseline public navigation,
- and what failures are particularly salient in this context.

This section motivates *why* principle weightings shift, without defining the shifts numerically.

---

## Context Axes Instantiated

> **Required**

Describe how this context instantiates or anchors the major context axes identified in the P&G paper.

### Cultural Context
- Describe relevant cultural expectations or variability.
- Note whether norms are assumed to be broadly shared or highly variable.

### Diversity Context
- Describe assumptions (or lack thereof) about human abilities, familiarity, or vulnerability.
- State whether accommodation is expected by default.

### Environmental Context

**Geometric Factors**
- Typical spatial characteristics (e.g., density, visibility, confinement).

**Operational Factors**
- Intended use of the space (e.g., public thoroughfare, workplace, emergency zone).

### Task Context
- Describe how the *type of task* affects what behaviors are considered appropriate.
- Do not enumerate tasks here; describe the relationship abstractly.

### Interpersonal Context
- Describe how humans are typically regarded:
  - independent pedestrians,
  - collaborators,
  - recipients of service,
  - guided participants, etc.

---

## Relationship to Prosocial Navigation Principles

> **Required**

Describe how this context systematically affects the interpretation or prioritization of principles in the Prosocial Navigation Charter.

- Identify principles that are **especially emphasized** in this context.
- Identify principles that are **commonly relaxed or deprioritized**.
- Describe typical tensions (e.g., speed vs. politeness, legibility vs. efficiency).

This section must remain descriptive and qualitative.

---

## Applicability and Limits

> **Required**

Clearly state:
- what situations *do* fall under this context,
- what situations *do not*.

This prevents overgeneralization and misuse.

---

## Derived and Related Contexts

> **Optional but recommended**

List known contexts that are:
- derived from this one,
- parameterized variants of this one,
- or commonly confused with this one.

Briefly describe how they differ (e.g., “adds urgency,” “adds accessibility constraints”).

---

## Example Scenario Classes (Non-Exhaustive)

> **Optional**

List scenario *types* (not specific IDs) that commonly occur in this context.

This aids discoverability without binding to concrete datasets.

---

## Context Specification (Machine-Readable)

> **Required**

```yaml
id: <canonical_context_id>
name: <Human-Readable Context Name>
context_class: core

primary_robot_role: <string>

applies_to_tasks:
  - <task_id or "*">

axes:
  cultural: <description>
  diversity: <description>
  environmental:
    geometric: <description>
    operational: <description>
  task: <description>
  interpersonal: <description>

principle_emphasis:
  emphasized:
    - <P#>
  deprioritized:
    - <P#>
  common_tensions:
    - <free text>

limits:
  includes:
    - <what is included>
  excludes:
    - <what is excluded>

related_contexts:
  - <context_id>
```

---

## Notes for Context Designers and Evaluators

> **Optional**

Provide guidance on:
- how this context should be selected or inferred,
- common mistakes in applying it,
- how it interacts with scenarios and tasks during evaluation.
