# Task: Lead an Agent

## STATUS
- **STATE:** DRAFTED  
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation Algorithms; common service-robot guidance task  
- **DRAFTED:** ChatGPT 5.2, 2026-01-11  
- **EDITED:** —  
- **AUDITED:** —  
- **VALIDATED:** —  

---

## Task Summary

> **Required**

- **Task ID:** `navigate.lead_agent`  
- **Task Name:** Lead an Agent  
- **Task Type:** navigation  
- **Primary Intent:** Guide a target agent by moving ahead and providing a navigational reference.  
- **Applies To:** single robot  

---

## Task Description

This task describes a navigation objective in which a robot leads a human or other agent toward a destination by moving ahead and serving as a navigational reference. Unlike point-to-point navigation, the robot’s motion is intended to be followed by another agent, and unlike following tasks, the robot establishes the trajectory and pace rather than reacting to them.

Success in this task is defined abstractly as maintaining a coherent leading relationship over time, such that the guided agent can reasonably infer the robot’s intent to be followed and is able to keep up with the robot’s motion. The task does not prescribe how the robot communicates intent, confirms compliance, or negotiates social interactions encountered during guidance.

---

## Task Scope and Boundaries

> **Required**

**Includes:**
- Moving ahead of a target agent to provide a navigational lead.
- Selecting a trajectory that can be reasonably followed by another agent.
- Adapting speed to maintain a leading relationship.
- Temporarily slowing or pausing to preserve guidance coherence.
- Resuming leading after brief interruptions.

**Excludes:**
- Explicit verbal or gestural communication with the agent.
- Determining whether the agent is successfully following.
- Social signaling beyond what is inherent in motion.
- Yielding, overtaking, or negotiating passage as primary objectives.

These excluded behaviors may arise during execution but are governed by scenarios, contexts, and charter principles rather than by the task itself.

---

## Relationship to Prosocial Navigation Principles

> **Required**

This task implicates **P0 (Goal Achievement)**, where success depends on sustaining progress toward a destination while maintaining a guidance relationship.

It commonly interacts with:
- **P3 (Legibility)**, as the robot’s motion must make its intent to lead clear,
- **P2 (Comfort)**, as inappropriate speed or path choice may cause stress or confusion,
- **P6 (Agent Understanding)**, as effective leading depends on anticipating the follower’s capabilities and responses.

Evaluation of this task focuses on whether the robot provides a clear, followable navigational reference while balancing social quality constraints imposed by scenarios and contexts.

---

## Common Failure Modes (Task-Level)

> **Optional but recommended**

- Moving too quickly for the agent to follow.
- Selecting paths that are difficult or unsafe for the agent.
- Abrupt changes in direction or speed that obscure intent.
- Abandonment of the leading relationship without external cause.

---

## Example Scenarios (Non-Exhaustive)

> **Optional but recommended**

- `guided_navigation_corridor`
- `escort_to_destination`

---

## Task Specification (Machine-Readable)

> **Required**

```yaml
id: navigate.lead_agent
name: Lead an Agent

summary: >
  The robot navigates ahead of a human or other agent, providing a moving
  reference that the agent is expected to follow toward a destination.

task_type: navigation

primary_intent: >
  Guide a target agent by moving ahead and establishing a trajectory to be
  followed.

scope:
  includes:
    - leading a target agent as a navigation reference
    - selecting paths that can be reasonably followed
    - adapting speed to maintain a leading relationship
    - pausing or slowing to preserve guidance coherence
    - resuming leading after brief interruption
  excludes:
    - explicit verbal or gestural communication
    - confirming whether the agent is following
    - social signaling beyond motion itself
    - yielding, overtaking, or negotiating passage as primary objectives

related_principles:
  - P0
  - P2
  - P3
  - P6

common_failure_modes:
  - excessive speed preventing following
  - unclear or erratic leading motion
  - selection of unsafe or impractical paths

example_scenarios:
  - guided_navigation_corridor
  - escort_to_destination
```

---

## Notes for Task Designers and Evaluators

This task should be used when the robot’s primary intent is to act as a guide or escort rather than to independently reach a destination. Evaluators should distinguish failures of guidance coherence from socially motivated deviations that preserve safety, comfort, or legibility. Judgments about communication style or confirmation of compliance should be made via scenario definitions and contextual norms, not via this task definition itself.
