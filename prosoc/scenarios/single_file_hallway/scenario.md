# Scenario: Single File Hallway

## Status

- **STATE:** DRAFTED
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation (P&G paper)
- **DRAFTED:** ChatGPT 5.2, 2026-01-16
- **EDITED:** render_sections.py, 2026-07-19

## Scenario Card Summary

- **Scenario Name:** Single File Hallway
- **Scenario Description:** A robot and a human approach each other in a hallway that is too narrow for safe and comfortable passing. The robot must proactively avoid conflict by yielding, signaling, or negotiating right-of-way.
- **Scientific Purpose:** pedestrian interaction
- **Physical Environment:** indoor
- **Geometric Layout:** narrow hallway
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from one end of the hallway to the other
- **Human Behavior:** navigate from the opposite end toward the robot
- **Success Metrics:**
  - SR
  - NoCollisions
  - DeadlockFree
- **Quality Metrics:**
  - P3
  - P5
  - P7
- **Ideal Outcome:** robot and human sequence through the hallway one at a time, without collision, deadlock, or the human being forced to retreat
- **Related Scenarios:** frontal_approach, movable_obstruction

**Remaining gaps:**

- **Cited In** — should-fill-in-now

---

## Scenario Overview

This scenario describes a social navigation conflict in which a robot and a human approach each other in a hallway that is **too narrow for safe and comfortable passing**. Unlike *Frontal Approach* and *Movable Obstruction*, the environment itself cannot be improved by intervention: the hallway geometry enforces **single‑file passage**.

The purpose of this scenario is to isolate and evaluate **Proactivity (P7)** without introducing opportunities for **Prosocial Behavior (P9)**. The robot must anticipate the conflict and take initiative—through signaling, yielding, or negotiation—to prevent deadlock or discomfort.

---

## Normative Expectations

At minimum, the robot must maintain a safe physical distance from the human at all times and must not enter the hallway simultaneously with the human once a conflict is recognized. Beyond these required behaviors, acceptable robot behavior may include recognizing early that the hallway does not permit passing, signaling intent clearly, and resolving the encounter without prolonged deadlock.

Unacceptable behavior includes forcing the human to back up unexpectedly, entering the hallway and creating a stalemate, or relying on last-moment braking to resolve the conflict.

---

## Scenario Specification (Machine-Readable)

```yaml
id: single_file_hallway_01
name: Single File Hallway

summary: >
  A robot and a human approach each other in a hallway that is too narrow for safe and comfortable
  passing. The robot must proactively avoid conflict by yielding, signaling, or negotiating
  right-of-way.

scientific_purpose: pedestrian interaction

geometric_layout: narrow hallway

context:
  environment:
    type: indoor
    setting: office hallway
    width: single_file
  social_setting:
    formality: informal
    crowd_level: low

agents:
  robot:
    role: navigating_agent
    capabilities:
      - forward_motion
      - steering
      - stopping
      - signaling
  humans:
    - role: pedestrian
      count: 1
      attributes:
        mobility: typical
        awareness: typical

initial_conditions:
  robot_position: end_of_hallway
  human_position: opposite_end
  visibility: clear

intended_robot_task: navigate from one end of the hallway to the other

intended_human_behavior: navigate from the opposite end toward the robot

expected_behaviors:
  must:
    - maintain a safe physical distance from the human
    - avoid entering the hallway simultaneously with the human
  should:
    - recognize early that the hallway does not permit passing
    - signal intent clearly (e.g., yielding, requesting priority, or other clear signaling)
    - resolve the encounter without prolonged deadlock
  should_not:
    - force the human to back up unexpectedly
    - enter the hallway and create a stalemate
    - rely on last-moment braking to resolve the conflict

relevant_principles:
  - P1  # Safety
  - P3  # Legibility
  - P5  # Social Competency
  - P7  # Proactivity

ideal_outcome: robot and human sequence through the hallway one at a time, without collision, deadlock, or the human being forced to retreat

related_scenarios:
  - frontal_approach
  - movable_obstruction

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
    - DeadlockFree
  quality_metrics:
    - P3   # Legibility
    - P5   # Social Competency
    - P7   # Proactivity
  failure_modes:
    - prolonged deadlock at hallway entrance
    - human forced to retreat without warning
    - uncomfortable proximity due to late yielding
  labeling_criteria:
    - hallway width prevents safe passing
    - robot and human approach from opposite ends
    - no alternative routes available

evaluation_notes: >
  This scenario evaluates whether the robot treats predictable spatial constraints as a planning
  problem rather than a reactive one. Proactive behavior (P7) is demonstrated when the robot
  anticipates the single-file constraint early and communicates its intent clearly, preventing
  hesitation or discomfort.

  Because the environment cannot be modified, prosocial behavior (P9) is intentionally out of
  scope. The robot’s responsibility is to manage the interaction gracefully, not to improve the
  environment itself.

```

---

## Discussion

The **SINGLE_FILE_HALLWAY** scenario serves as a **clean control case** for proactivity in social
navigation. In contrast to *Movable Obstruction*, there is no opportunity for environmental
stewardship or third‑party benefit—only the opportunity to **prevent conflict before it occurs**.

Together, *Frontal Approach*, *Single File Hallway*, and *Movable Obstruction* form a minimal
scenario set that:

- Progressively constrains the environment
- Cleanly separates P7 (Proactivity) from P9 (Prosocial Behavior)
- Supports comparative evaluation across identical agent configurations

This scenario is especially useful for benchmarking hesitation handling, signaling clarity, and
right‑of‑way negotiation under unavoidable spatial constraints.


---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
  - DeadlockFree
- **Quality Metrics:**
  - P3
  - P5
  - P7
- **Failure Modes:**
  - prolonged deadlock at hallway entrance
  - human forced to retreat without warning
  - uncomfortable proximity due to late yielding
- **Labeling Criteria:**
  - hallway width prevents safe passing
  - robot and human approach from opposite ends
  - no alternative routes available
- **Ideal Outcome:** robot and human sequence through the hallway one at a time, without collision, deadlock, or the human being forced to retreat
