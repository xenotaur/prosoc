# Task: Navigate from Start to Goal

## STATUS
- **STATE:** DRAFTED  
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation Algorithms; common mobile robot navigation task  
- **DRAFTED:** ChatGPT 5.2, 2026-01-11  
- **EDITED:** —  
- **AUDITED:** —  
- **VALIDATED:** —  

---

## Task Summary

> **Required**

- **Task ID:** `navigate.point_to_point`  
- **Task Name:** Navigate from Start to Goal  
- **Task Type:** navigation  
- **Primary Intent:** Reach a specified destination from an initial location.  
- **Applies To:** single robot  

---

## Task Description

This task describes the fundamental navigation objective in which a robot attempts to move from a given start location to a specified goal location.

Success in this task is defined abstractly as reaching the intended destination within reasonable time and resource constraints, without regard to the specific environment, geometry, or presence of other agents. The task itself does not assume static or dynamic surroundings, nor does it prescribe how the robot should respond to social interactions encountered along the way.

This task serves as the baseline intent underlying most social navigation scenarios. Social behaviors, interaction strategies, and normative trade-offs are evaluated relative to this core objective, but are not part of the task definition itself.

---

## Task Scope and Boundaries

> **Required**

**Includes:**
- Selecting and executing motion to progress toward a destination.
- Temporarily slowing, stopping, or rerouting in service of reaching the goal.
- Resuming motion toward the goal after interruptions or delays.

**Excludes:**
- Passing, overtaking, following, or leading specific agents.
- Yielding right-of-way as a primary objective.
- Interpreting gestures, social signals, or cultural norms.
- Optimizing for comfort, legibility, or politeness beyond what is required to reach the destination.

These excluded behaviors may arise during execution but are governed by scenarios, contexts, and charter principles rather than by the task itself.

---

## Relationship to Prosocial Navigation Principles

> **Required**

This task directly implicates **P0 (Goal Achievement)**, as successful completion depends on reaching the intended destination.

Tension commonly arises between P0 and social or ethical principles such as:
- **P1 (Safety)**, when progress toward the goal conflicts with collision avoidance,
- **P2 (Comfort)**, when efficient motion creates discomfort for nearby humans,
- **P3 (Legibility)**, when direct trajectories are socially ambiguous.

Evaluation of this task therefore requires assessing how goal achievement is balanced against other principles under scenario- and context-specific constraints, rather than whether the goal is achieved at all costs.

---

## Common Failure Modes (Task-Level)

> **Optional but recommended**

- Failure to reach the destination.
- Excessive delay or stagnation without clear justification.
- Abandonment of the goal without external cause.
- Oscillatory or indecisive motion that prevents sustained progress.

---

## Example Scenarios (Non-Exhaustive)

> **Optional but recommended**

- `frontal_approach_01`
- `intersection_no_gesture`
- `pedestrian_overtaking`

---

## Task Specification (Machine-Readable)

> **Required**

```yaml
id: navigate.point_to_point
name: Navigate from Start to Goal

summary: >
  The robot attempts to move from an initial location to a specified destination,
  serving as the baseline navigation intent underlying most social navigation scenarios.

task_type: navigation

primary_intent: >
  Reach a designated goal location from a starting position.

scope:
  includes:
    - progressing toward a destination
    - pausing or stopping temporarily while pursuing the goal
    - resuming motion toward the goal after interruption
  excludes:
    - explicit interaction with specific agents
    - yielding or asserting right-of-way as a primary objective
    - interpretation of social signals or gestures
    - optimization for social comfort or legibility beyond goal completion

related_principles:
  - P0
  - P1
  - P2
  - P3

common_failure_modes:
  - failure to reach destination
  - excessive delay without justification
  - abandonment of navigation goal

example_scenarios:
  - frontal_approach_01
  - intersection_no_gesture
  - pedestrian_overtaking
```

---

## Notes for Task Designers and Evaluators

This task should be treated as the **default intent** when no more specific navigation task applies. Evaluators should avoid penalizing deviations from direct or optimal paths unless such deviations materially undermine goal achievement. Social appropriateness, signaling, and interaction quality should be assessed via scenario expectations and charter principles, not via this task definition itself.
