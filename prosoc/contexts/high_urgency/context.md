# Context: Emergency High-Urgency Operation

## STATUS
- **STATE:** DRAFTED
- **CONTEXT TYPE:** CORE
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation Algorithms; emergency robotics and medical transport literature
- **CREATED:** 2026-01-11
- **MODIFIED:** —
- **AUDITED:** —
- **VALIDATED:** —

---

## Context Summary

> **Required**

- **Context ID:** emergency.high_urgency
- **Context Name:** Emergency High-Urgency Operation
- **Context Class:** core
- **Primary Role of Robot:** emergency responder
- **Applies To Tasks:** "*"

---

## Context Description

Emergency High-Urgency Operation describes situations in which a robot is engaged in time-critical activity where delays may result in significant harm. Typical examples include transporting emergency equipment, supporting medical response, or assisting during evacuation scenarios.

In this context, the robot is perceived as having a legitimate and urgent operational purpose. Humans are expected to recognize the exceptional nature of the robot’s activity and tolerate behaviors that would be inappropriate under normal circumstances, provided safety is maintained.

This context is normatively distinct because urgency fundamentally alters how trade-offs between efficiency, politeness, and comfort are interpreted.

---

## Normative Significance

> **Required**

This context introduces urgency as a dominant normative factor that can override everyday social navigation expectations.

Key normative expectations include:
- rapid and decisive motion toward task completion,
- reduced emphasis on comfort and deference,
- strong prioritization of task success when safety can be maintained.

Failures in this context are especially salient when excessive caution undermines urgent response, or when unsafe behavior causes additional harm.

---

## Context Axes Instantiated

> **Required**

### Cultural Context
- Many cultures share an expectation that emergency operations justify exceptional behavior.
- The degree of tolerated assertiveness may vary, but urgency is broadly recognized.

### Diversity Context
- Humans may be stressed, distracted, or impaired.
- The robot must not assume cooperation or predictable responses from others.

### Environmental Context

**Geometric Factors**
- Often crowded, constrained, or chaotic spaces.
- Reduced predictability due to human motion and obstacles.

**Operational Factors**
- Environment is temporarily repurposed for emergency response.
- Emergency activity implicitly grants priority, though not formal right-of-way in all settings.

### Task Context
- Task goals are time-critical and justify assertive navigation.
- Delays are treated as significant failures.

### Interpersonal Context
- Humans are treated as collaborators in a shared emergency rather than neutral pedestrians.
- Compliance may be implicit but cannot be assumed.

---

## Relationship to Prosocial Navigation Principles

> **Required**

In this context:

- **P0 (Goal Achievement)** is strongly emphasized due to urgency.
- **P1 (Safety)** remains critical and cannot be abandoned.
- **P2 (Comfort)** and **P3 (Legibility)** may be deprioritized when they conflict with urgent response.
- **P9 (Prosocial Behavior)** is interpreted as prioritizing harm prevention over everyday politeness.

Common tensions include:
- speed versus safety,
- assertiveness versus predictability,
- urgency versus perceived rudeness.

---

## Applicability and Limits

> **Required**

**Includes:**
- Emergency equipment transport (e.g., crash carts).
- Time-critical medical or safety-related navigation.
- Situations where delay materially increases risk.

**Excludes:**
- Routine service delivery without urgency.
- Situations lacking clear time-critical stakes.
- Contexts where authority or priority is not socially recognized.

---

## Derived and Related Contexts

> **Optional but recommended**

- `service.routine_delivery` — non-urgent service baseline.
- `baseline.public_navigation` — default normative reference.
- `emergency.coordinated_response` — adds structured human-robot coordination.

---

## Example Scenario Classes (Non-Exhaustive)

> **Optional**

- Crash cart transport in a hospital
- Emergency supply delivery during evacuation
- Rapid response navigation in disaster scenarios

---

## Context Specification (Machine-Readable)

> **Required**

```yaml
id: emergency.high_urgency
name: Emergency High-Urgency Operation
context_class: core

primary_robot_role: emergency responder

applies_to_tasks:
  - "*"

axes:
  cultural: >
    Broad cultural recognition that emergency situations justify exceptional
    navigation behavior, with some regional variation.
  diversity: >
    Humans may be stressed, impaired, or unpredictable; cooperation cannot be
    assumed.
  environmental:
    geometric: >
      Crowded, constrained, or dynamically changing spaces with limited
      predictability.
    operational: >
      Environment is temporarily repurposed for emergency response, implicitly
      granting priority without guaranteed formal right-of-way.
  task: >
    Task goals are time-critical and justify assertive navigation when safety
    constraints are respected.
  interpersonal: >
    Humans are treated as collaborators in a shared emergency rather than neutral
    bystanders.

principle_emphasis:
  emphasized:
    - P0
    - P1
    - P9
  deprioritized:
    - P2
    - P3
  common_tensions:
    - speed versus safety
    - assertiveness versus predictability
    - urgency versus politeness

limits:
  includes:
    - time-critical emergency operations
    - navigation where delay increases harm
  excludes:
    - routine, non-urgent service tasks
    - contexts lacking recognized urgency

related_contexts:
  - service.routine_delivery
  - baseline.public_navigation
```

---

## Notes for Context Designers and Evaluators

Evaluators should select this context only when urgency is genuine and socially recognizable. Deviations from comfort or politeness norms should be explicitly justified by time-critical goals, and unsafe behavior should remain unacceptable even under urgent conditions.
