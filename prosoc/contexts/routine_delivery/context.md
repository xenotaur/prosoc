# Context: Routine Service Delivery

## STATUS
- **STATE:** DRAFTED
- **CONTEXT TYPE:** CORE
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation Algorithms; service robot literature
- **CREATED:** 2026-01-11
- **MODIFIED:** —
- **AUDITED:** —
- **VALIDATED:** —

---

## Context Summary

> **Required**

- **Context ID:** service.routine_delivery
- **Context Name:** Routine Service Delivery
- **Context Class:** core
- **Primary Role of Robot:** service provider
- **Applies To Tasks:** deliver.object

---

## Context Description

Routine Service Delivery describes situations in which a robot performs a non-urgent service function involving the transport or delivery of objects in human-shared environments. The robot is perceived as having a legitimate service role, but not one that overrides everyday social expectations.

Humans in this context generally expect the robot to complete its delivery efficiently while still adhering to common norms of safety, comfort, and politeness. The robot’s service role provides some justification for purposeful motion but does not grant priority over humans.

This context is normatively distinct from baseline public navigation because the robot is assumed to be “on duty,” yet remains constrained by everyday social expectations.

---

## Normative Significance

> **Required**

This context introduces a task-driven reweighting of prosocial navigation principles without invoking urgency or authority.

Key normative expectations include:
- purposeful, goal-directed motion in service of delivery,
- continued deference to human comfort and safety,
- tolerance for minor social disruption when clearly attributable to service execution.

Failures in this context are salient when the robot either behaves as if it has undue priority or, conversely, behaves so conservatively that the service becomes ineffective.

---

## Context Axes Instantiated

> **Required**

### Cultural Context
- Cultural expectations influence tolerance for service robots occupying space or interrupting flow.
- Norms regarding politeness versus efficiency vary by setting.

### Diversity Context
- Delivery recipients and bystanders may have varying needs or expectations.
- Accommodation may be expected but is not assumed to override delivery entirely.

### Environmental Context

**Geometric Factors**
- Often includes constrained spaces such as hallways, storage areas, or offices.
- Moderate pedestrian density is typical.

**Operational Factors**
- Environment supports routine service operations but is not dedicated exclusively to them.
- The robot is not granted formal right-of-way.

### Task Context
- The delivery task justifies purposeful motion and limited assertiveness.
- Delays are acceptable but undermine task success if excessive.

### Interpersonal Context
- Humans are treated primarily as bystanders or recipients of service.
- Interactions are typically brief and transactional.

---

## Relationship to Prosocial Navigation Principles

> **Required**

In this context:

- **P0 (Goal Achievement)** gains importance relative to baseline navigation.
- **P1 (Safety)** and **P2 (Comfort)** remain strongly emphasized.
- **P3 (Legibility)** is important to ensure humans understand the robot’s delivery intent.
- **P9 (Prosocial Behavior)** is relevant insofar as delivery serves human needs.

Common tensions include:
- efficiency versus politeness,
- direct delivery routes versus human comfort,
- service effectiveness versus willingness to yield.

---

## Applicability and Limits

> **Required**

**Includes:**
- Non-urgent delivery of packages, mail, tools, or supplies.
- Service robots operating in offices, hospitals, or campuses under routine conditions.

**Excludes:**
- Emergency or high-urgency delivery scenarios.
- Guidance or escort roles.
- Situations where the robot is granted explicit priority over humans.

---

## Derived and Related Contexts

> **Optional but recommended**

- `emergency.high_urgency` — adds urgency and priority override.
- `workplace.formalized_service` — adds structured workflows and trained humans.
- `baseline.public_navigation` — baseline normative reference.

---

## Example Scenario Classes (Non-Exhaustive)

> **Optional**

- Package delivery through office corridors
- Supply transport within hospitals (non-emergency)
- Mail delivery on campus

---

## Context Specification (Machine-Readable)

> **Required**

```yaml
id: service.routine_delivery
name: Routine Service Delivery
context_class: core

primary_robot_role: service provider

applies_to_tasks:
  - deliver.object

axes:
  cultural: >
    Cultural expectations shape tolerance for service robots occupying shared
    space and prioritizing task completion.
  diversity: >
    Mixed population with varying expectations and abilities; accommodation may
    be expected but does not eliminate delivery obligations.
  environmental:
    geometric: >
      Constrained indoor spaces such as corridors, offices, and storage areas
      with moderate pedestrian density.
    operational: >
      Environment supports routine service activities without granting formal
      priority or exclusive access.
  task: >
    The delivery task justifies purposeful motion and limited assertiveness but
    does not override everyday social norms.
  interpersonal: >
    Humans are primarily bystanders or recipients of service, with brief and
    transactional interactions.

principle_emphasis:
  emphasized:
    - P0
    - P1
    - P2
    - P3
    - P9
  deprioritized: []
  common_tensions:
    - efficiency versus politeness
    - delivery speed versus human comfort
    - task completion versus yielding

limits:
  includes:
    - routine, non-urgent delivery services
    - shared environments supporting service robots
  excludes:
    - emergency or time-critical delivery
    - roles involving guidance or authority

related_contexts:
  - baseline.public_navigation
  - emergency.high_urgency
  - workplace.formalized_service
```

---

## Notes for Context Designers and Evaluators

This context should be selected when a robot is performing routine delivery without urgency or authority. Evaluators should ensure that delivery effectiveness is considered alongside continued adherence to safety, comfort, and legibility expectations, and that neither excessive assertiveness nor excessive deference dominates behavior.
