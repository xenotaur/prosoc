# Task: Deliver an Object

## STATUS
- **STATE:** DRAFTED  
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation Algorithms; common service-robot delivery task  
- **DRAFTED:** ChatGPT 5.2, 2026-01-11  
- **EDITED:** —  
- **AUDITED:** —  
- **VALIDATED:** —  

---

## Task Summary

> **Required**

- **Task ID:** `deliver.object`  
- **Task Name:** Deliver an Object  
- **Task Type:** navigation  
- **Primary Intent:** Transfer a specified object from a source to a destination.  
- **Applies To:** single robot  

---

## Task Description

This task describes a navigation-centered objective in which a robot delivers an object from a source to a destination. The defining characteristic of the task is successful transfer of the object, not the specific method by which the object is acquired, transported, or handed off.

The source and destination may be locations or agents, and the object may already be in the robot’s possession or may need to be collected as part of the delivery process. These variations affect task realization but do not alter the underlying intent of delivery.

Success in this task is defined abstractly as the object reaching its intended destination under reasonable constraints, independent of specific environmental geometry, social norms, or interaction protocols.

---

## Task Scope and Boundaries

> **Required**

**Includes:**
- Navigating in service of transporting an object toward a destination.
- Temporarily pausing, stopping, or rerouting to preserve delivery success.
- Coordinating navigation across multiple phases of delivery (e.g., approach, transit, arrival).

**Excludes:**
- Object manipulation details such as grasping or release mechanics.
- Social protocols for requesting, accepting, or refusing delivery.
- Determining whether delivery is appropriate or authorized.
- Normative judgments about urgency, politeness, or priority.
- Negotiation of hand-off beyond physical co-location.

These excluded aspects are governed by scenarios, contexts, and charter principles rather than by the task itself.

---

## Relationship to Prosocial Navigation Principles

> **Required**

This task directly implicates **P0 (Goal Achievement)**, as success depends on the object reaching its intended destination.

It frequently interacts with:
- **P1 (Safety)**, when transporting objects near humans or obstacles,
- **P2 (Comfort)**, when delivery motion intrudes on personal space,
- **P3 (Legibility)**, when the robot’s intent to deliver must be inferred,
- **P9 (Prosocial Behavior)**, as delivery tasks often serve human needs.

Evaluation of this task therefore focuses on whether delivery is achieved while appropriately balancing these principles under scenario- and context-specific constraints.

---

## Common Failure Modes (Task-Level)

> **Optional but recommended**

- Failure to deliver the object to the intended destination.
- Delivery to the wrong location or agent.
- Abandonment of delivery without external cause.
- Excessive delay that renders the delivery ineffective.

---

## Example Scenarios (Non-Exhaustive)

> **Optional but recommended**

- `package_delivery_office`
- `handoff_to_human_corridor`
- `pickup_and_deliver_shelf_to_desk`

---

## Task Specification (Machine-Readable)

> **Required**

```yaml
id: deliver.object
name: Deliver an Object

summary: >
  The robot transfers a specified object from a source to a destination,
  navigating in service of successful delivery rather than independent travel.

task_type: navigation

primary_intent: >
  Transport an object from its source to an intended destination.

scope:
  includes:
    - navigating while carrying or transporting an object
    - pausing or rerouting to preserve delivery success
    - coordinating navigation across delivery phases
  excludes:
    - object manipulation mechanics
    - social authorization or consent for delivery
    - urgency, politeness, or priority judgments
    - detailed hand-off negotiation beyond co-location

related_principles:
  - P0
  - P1
  - P2
  - P3
  - P9

common_failure_modes:
  - failure to deliver object
  - delivery to incorrect destination
  - abandonment of delivery task
  - excessive delay rendering delivery ineffective

example_scenarios:
  - package_delivery_office
  - handoff_to_human_corridor
  - pickup_and_deliver_shelf_to_desk
```

---

## Notes for Task Designers and Evaluators

This task should be used whenever the robot’s primary intent is to transfer an object, regardless of whether the object is already in the robot’s possession or must be acquired during execution. Evaluators should distinguish failures of delivery from socially motivated deviations intended to preserve safety, comfort, or prosocial behavior. Social protocols for hand-off, consent, or prioritization should be evaluated via scenario definitions and context cards, not via this task definition itself.
