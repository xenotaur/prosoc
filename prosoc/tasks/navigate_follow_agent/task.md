# Task: Follow an Agent

## STATUS
- **STATE:** DRAFTED  
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation Algorithms; common service-robot navigation task  
- **DRAFTED:** ChatGPT 5.2, 2026-01-11  
- **EDITED:** —  
- **AUDITED:** —  
- **VALIDATED:** —  

---

## Task Summary

> **Required**

- **Task ID:** `navigate.follow_agent`  
- **Task Name:** Follow an Agent  
- **Task Type:** navigation  
- **Primary Intent:** Maintain motion that follows a target agent while preserving appropriate relative position.  
- **Applies To:** single robot  

---

## Task Description

This task describes a navigation objective in which a robot follows a human or other agent who serves as the primary reference for motion. Rather than navigating toward a fixed spatial goal, the robot’s progress is defined relative to the movement of the followed agent.

Success in this task is defined abstractly as maintaining an appropriate following relationship over time, including suitable distance, alignment, and pacing, while continuing to move with the agent. The task does not prescribe how the robot should signal intent, interpret social cues, or negotiate with other agents encountered during following.

This task is distinct from point-to-point navigation in that the goal location is dynamic and defined by another agent’s motion rather than by a static destination.

---

## Task Scope and Boundaries

> **Required**

**Includes:**
- Maintaining motion behind or alongside a target agent.
- Adapting speed to remain with the followed agent.
- Temporarily slowing or stopping to preserve the following relationship.
- Resuming following after brief interruptions.

**Excludes:**
- Leading or guiding the agent.
- Explicitly managing social signaling or communication.
- Determining socially appropriate following distance or side preference.
- Negotiating passage, overtaking, or yielding as primary objectives.

These excluded behaviors may arise during execution but are governed by scenarios, contexts, and charter principles rather than by the task itself.

---

## Relationship to Prosocial Navigation Principles

> **Required**

This task commonly implicates **P0 (Goal Achievement)**, where success is defined by maintaining the following relationship rather than reaching a fixed destination.

It frequently interacts with:
- **P2 (Comfort)**, as inappropriate distance or pacing may cause discomfort,
- **P3 (Legibility)**, as the robot’s motion should make its following intent understandable,
- **P6 (Agent Understanding)**, as effective following depends on correctly interpreting the agent’s motion.

Evaluation of this task focuses on whether the robot sustains the intended relational goal while balancing social quality constraints imposed by scenarios and contexts.

---

## Common Failure Modes (Task-Level)

> **Optional but recommended**

- Losing track of the followed agent.
- Falling excessively far behind or crowding too closely.
- Repeated oscillation between advancing and stopping that breaks the following relationship.
- Abandonment of following without external cause.

---

## Example Scenarios (Non-Exhaustive)

> **Optional but recommended**

- `human_following_corridor`
- `group_following_open_space`

---

## Task Specification (Machine-Readable)

> **Required**

```yaml
id: navigate.follow_agent
name: Follow an Agent

summary: >
  The robot navigates by following a human or other agent, maintaining an
  appropriate relative position as the agent moves through the environment.

task_type: navigation

primary_intent: >
  Maintain motion that follows a target agent while preserving an appropriate
  following relationship.

scope:
  includes:
    - following a moving agent as a dynamic navigation reference
    - adapting speed to remain with the agent
    - pausing or slowing to preserve the following relationship
    - resuming following after brief interruption
  excludes:
    - leading or guiding the agent
    - explicit social signaling or communication
    - defining socially appropriate distance or side preference
    - negotiating passage, overtaking, or yielding as primary objectives

related_principles:
  - P0
  - P2
  - P3
  - P6

common_failure_modes:
  - loss of followed agent
  - excessive lag or crowding
  - unstable oscillatory following behavior

example_scenarios:
  - human_following_corridor
  - group_following_open_space
```

---

## Notes for Task Designers and Evaluators

This task should be used when the robot’s primary intent is to remain with a specific agent rather than to reach an independent destination. Evaluators should distinguish failures of the following relationship from socially motivated deviations that preserve comfort, safety, or legibility. Judgments about acceptable distance, side preference, or signaling should be made via scenario definitions and contextual norms, not via this task definition itself.
