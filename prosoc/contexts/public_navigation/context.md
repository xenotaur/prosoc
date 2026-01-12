# Context: Baseline Public Navigation

## STATUS
- **STATE:** DRAFTED
- **CONTEXT TYPE:** CORE
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation Algorithms; general public-space navigation literature
- **CREATED:** 2026-01-11
- **MODIFIED:** —
- **AUDITED:** —
- **VALIDATED:** —

---

## Context Summary

> **Required**

- **Context ID:** baseline.public_navigation
- **Context Name:** Baseline Public Navigation
- **Context Class:** core
- **Primary Role of Robot:** neutral navigator
- **Applies To Tasks:** "*"

---

## Context Description

Baseline Public Navigation describes situations in which a robot navigates shared public space without a specialized social role, service obligation, or operational priority. The robot is perceived as a generic moving agent whose primary responsibility is to move safely and predictably while minimizing disruption to others.

Humans in this context typically do not expect the robot to assert authority, provide guidance, or perform a specific service. Instead, they assume the robot will follow broadly accepted social norms for shared space, similar to those applied to other pedestrians or non-threatening mobile devices.

This context serves as the normative reference point against which other contexts—such as service delivery, emergency operation, or guidance—are contrasted.

---

## Normative Significance

> **Required**

This context establishes the default interpretation of prosocial navigation principles in the absence of task- or role-specific modifiers.

Key normative expectations include:
- conservative motion in proximity to humans,
- clear and predictable trajectories,
- willingness to yield or pause to avoid conflict.

Failures in this context are particularly salient when they violate everyday expectations of safety, comfort, or social predictability, even if task efficiency is preserved.

---

## Context Axes Instantiated

> **Required**

### Cultural Context
- Social norms for personal space, passing behavior, and yielding are assumed to follow local cultural conventions.
- Norms are generally shared but may vary by region.

### Diversity Context
- The population is assumed to be heterogeneous, with varying levels of mobility, attention, and familiarity with robots.
- No specific accommodations are assumed by default, but conservative behavior is expected.

### Environmental Context

**Geometric Factors**
- Public spaces with variable width, visibility, and crowd density.
- Mixed static and dynamic obstacles.

**Operational Factors**
- Space is intended for general public use, not specialized operations.
- No agent is assumed to have inherent right-of-way.

### Task Context
- Tasks are incidental to navigation and do not justify assertive or disruptive behavior.
- Efficiency is secondary to safety and social acceptability.

### Interpersonal Context
- Humans are treated as independent pedestrians.
- Minimal engagement or explicit interaction is expected.

---

## Relationship to Prosocial Navigation Principles

> **Required**

In this context:

- **P1 (Safety)** and **P2 (Comfort)** are strongly emphasized, as violations are immediately noticeable and socially unacceptable.
- **P3 (Legibility)** is important to ensure humans can easily predict the robot’s motion.
- **P0 (Goal Achievement)** is constrained by the above principles and rarely justifies aggressive behavior.

Common tensions include:
- efficiency versus comfort,
- direct paths versus legible motion,
- task completion versus willingness to yield.

---

## Applicability and Limits

> **Required**

**Includes:**
- Navigation in sidewalks, hallways, plazas, and similar public areas.
- Situations where the robot has no explicit service or authority role.

**Excludes:**
- Emergency or high-urgency operations.
- Service roles such as delivery, escort, or guidance.
- Environments with formalized right-of-way rules favoring the robot.

---

## Derived and Related Contexts

> **Optional but recommended**

- `service.routine_delivery` — adds a service obligation to this baseline.
- `environment.child_centric` — adds heightened safety and accommodation expectations.
- `environment.dense_crowd` — adds geometric density and group-level interaction.

---

## Example Scenario Classes (Non-Exhaustive)

> **Optional**

- Point-to-point navigation in public hallways
- Passing pedestrians in corridors
- Navigating shared open spaces

---

## Context Specification (Machine-Readable)

> **Required**

```yaml
id: baseline.public_navigation
name: Baseline Public Navigation
context_class: core

primary_robot_role: neutral navigator

applies_to_tasks:
  - "*"

axes:
  cultural: >
    Local cultural norms for shared public space, including personal space,
    yielding behavior, and passing conventions.
  diversity: >
    Heterogeneous population with varying mobility, attention, and familiarity
    with robots; conservative assumptions apply.
  environmental:
    geometric: >
      Variable-width public spaces with mixed static and dynamic obstacles and
      fluctuating crowd density.
    operational: >
      General public use with no specialized operational priority or assigned
      right-of-way.
  task: >
    Task goals do not justify assertive or disruptive navigation behavior.
  interpersonal: >
    Humans are treated as independent pedestrians with minimal expected engagement.

principle_emphasis:
  emphasized:
    - P1
    - P2
    - P3
  deprioritized:
    - P0
  common_tensions:
    - efficiency versus comfort
    - direct paths versus legibility
    - goal completion versus yielding

limits:
  includes:
    - general public navigation without specialized role
    - shared spaces with mixed pedestrian traffic
  excludes:
    - emergency response contexts
    - service delivery or guidance roles

related_contexts:
  - service.routine_delivery
  - environment.child_centric
  - environment.dense_crowd
```

---

## Notes for Context Designers and Evaluators

This context should be selected whenever no more specific service, urgency, or guidance context applies. Evaluators should treat it as the default normative baseline and explicitly justify any deviations from its expectations when other contexts are chosen.
