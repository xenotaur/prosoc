# Context: Guidance and Docent Operation

## STATUS
- **STATE:** DRAFTED
- **CONTEXT TYPE:** CORE
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation Algorithms; museum guide and escort robot literature
- **CREATED:** 2026-01-11
- **MODIFIED:** —
- **AUDITED:** —
- **VALIDATED:** —

---

## Context Summary

> **Required**

- **Context ID:** guidance.docent
- **Context Name:** Guidance and Docent Operation
- **Context Class:** core
- **Primary Role of Robot:** guide / escort
- **Applies To Tasks:** navigate.lead_agent

---

## Context Description

Guidance and Docent Operation describes situations in which a robot leads, escorts, or guides one or more humans through an environment. Typical examples include museum docents, campus guides, hospital escorts, or wayfinding assistants.

In this context, the robot’s navigation behavior is explicitly communicative: motion is not only a means of reaching a destination but also a signal of intent, pacing, and attention. Humans expect the robot to be aware of followers and to adapt its behavior to maintain group coherence.

This context is normatively distinct because success depends on sustained interpersonal coupling rather than individual navigation efficiency.

---

## Normative Significance

> **Required**

This context foregrounds legibility, predictability, and interpersonal awareness as primary normative concerns.

Key normative expectations include:
- maintaining a pace suitable for followers,
- ensuring the robot remains observable and understandable,
- prioritizing group cohesion over shortest paths.

Failures in this context are salient when humans become confused, left behind, or feel ignored, even if the robot technically reaches the destination.

---

## Context Axes Instantiated

> **Required**

### Cultural Context
- Cultural norms influence preferred interpersonal distance, pacing, and formality during guided movement.
- Expectations of docent behavior vary across institutions and cultures.

### Diversity Context
- Followers may include children, elderly individuals, or people with mobility or sensory impairments.
- Accommodation and adaptability are often expected by default.

### Environmental Context

**Geometric Factors**
- Semi-structured spaces with points of interest, intersections, and stopping areas.
- Variable visibility and occasional congestion.

**Operational Factors**
- Environment supports lingering, stopping, and rerouting for explanation or coordination.
- Navigation efficiency is secondary to clarity and cohesion.

### Task Context
- The guidance task justifies slower speeds and indirect routes when they improve comprehension or group cohesion.
- Reaching the destination is necessary but not sufficient for success.

### Interpersonal Context
- Humans are treated as guided participants rather than independent pedestrians.
- Sustained attention and responsiveness are expected.

---

## Relationship to Prosocial Navigation Principles

> **Required**

In this context:

- **P3 (Legibility)** is strongly emphasized, as motion serves a communicative role.
- **P2 (Comfort)** is important to ensure followers feel at ease and included.
- **P0 (Goal Achievement)** is reframed as successful guidance rather than mere arrival.
- **P9 (Prosocial Behavior)** is expressed through attentiveness and accommodation.

Common tensions include:
- pace versus group cohesion,
- efficiency versus clarity,
- autonomy versus responsiveness.

---

## Applicability and Limits

> **Required**

**Includes:**
- Guided tours and escorting individuals or groups.
- Wayfinding assistance with sustained following.

**Excludes:**
- Routine navigation without followers.
- Emergency or high-urgency response.
- Pure delivery tasks without guidance intent.

---

## Derived and Related Contexts

> **Optional but recommended**

- `baseline.public_navigation` — when no guidance role is present.
- `service.routine_delivery` — when service replaces guidance.
- `guidance.accessibility_sensitive` — adds heightened accommodation needs.

---

## Example Scenario Classes (Non-Exhaustive)

> **Optional**

- Museum tours led by a robot
- Campus or hospital escort scenarios
- Group wayfinding through complex environments

---

## Context Specification (Machine-Readable)

> **Required**

```yaml
id: guidance.docent
name: Guidance and Docent Operation
context_class: core

primary_robot_role: guide

applies_to_tasks:
  - navigate.lead_agent

axes:
  cultural: >
    Cultural norms shape expectations for pacing, interpersonal distance,
    and formality during guided movement.
  diversity: >
    Followers may have varied abilities or needs; accommodation and adaptability
    are often expected by default.
  environmental:
    geometric: >
      Semi-structured spaces with landmarks, intersections, and variable
      visibility.
    operational: >
      Environment supports stopping, slowing, and rerouting to maintain group
      cohesion and understanding.
  task: >
    Guidance tasks prioritize clarity, cohesion, and successful escort over
    shortest-path efficiency.
  interpersonal: >
    Humans are treated as guided participants requiring sustained attention
    and responsiveness.

principle_emphasis:
  emphasized:
    - P2
    - P3
    - P9
  deprioritized:
    - P0
  common_tensions:
    - pace versus group cohesion
    - efficiency versus clarity
    - autonomy versus responsiveness

limits:
  includes:
    - sustained guidance or escort roles
    - navigation where motion is communicative
  excludes:
    - navigation without followers
    - emergency or delivery-focused contexts

related_contexts:
  - baseline.public_navigation
  - service.routine_delivery
```

---

## Notes for Context Designers and Evaluators

Evaluators should assess success in this context based on follower experience and understanding, not solely on navigation efficiency or arrival time. Deviations from direct paths or higher speeds may be appropriate when they improve legibility or group cohesion.
