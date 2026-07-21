# Scenario: Movable Obstruction

## Status

- **STATE:** DRAFTED
- **SOURCE:** Principles and Guidelines for Evaluating Social Robot Navigation (P&G paper)
- **DRAFTED:** ChatGPT 5.2, 2026-01-16
- **EDITED:** render_sections.py, 2026-07-19

## Scenario Card Summary

- **Scenario Name:** Movable Obstruction
- **Scenario Description:** A robot and a human approach each other in a hallway that is partially blocked by a movable obstruction. The robot must decide whether to yield, wait, remove the obstruction, or report it, balancing task goals with prosocial responsibility.
- **Scientific Purpose:** interactive navigation
- **Physical Environment:** indoor
- **Geometric Layout:** passable space, partially obstructed
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from one end of the hallway to the other, resolving or mitigating the obstruction as appropriate
- **Human Behavior:** navigate from the opposite end toward the robot
- **Success Metrics:**
  - SR
  - NoCollisions
  - ConflictResolved
- **Quality Metrics:**
  - P3
  - P7
  - P9
- **Ideal Outcome:** robot and human pass safely; the robot resolves or mitigates the obstruction-induced conflict (yielding, removing, or reporting it) rather than ignoring it
- **Related Scenarios:** frontal_approach, single_file_hallway

**Remaining gaps:**

- **Cited In** — should-fill-in-now

---

## Scenario Overview

This scenario describes a social navigation conflict in which a robot and a human approach each other in a hallway that is nominally wide enough for passing, but partially blocked by a **movable obstruction** (e.g., a cart, box, or misplaced furniture). The scenario is designed to distinguish **Proactivity (P7)** from **Prosocial Behavior (P9)** by introducing opportunities for the robot to improve the navigability of the environment, rather than merely adapting to it.

Unlike *Frontal Approach*, successful navigation in this scenario may involve **environmental intervention** (physically moving the obstruction or reporting it), not just motion planning or yielding behavior.

---

## Scenario Specification (Machine-Readable)

```yaml
id: movable_obstruction_01
name: Movable Obstruction

summary: >
  A robot and a human approach each other in a hallway that is partially blocked by a movable obstruction.
  The robot must decide whether to yield, wait, remove the obstruction, or report it, balancing task goals
  with prosocial responsibility.

scientific_purpose: interactive navigation

geometric_layout: passable space, partially obstructed

context:
  environment:
    type: indoor
    setting: office hallway
    width: nominal
    obstruction:
      present: true
      movable: true
      blocks_full_passing: true
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
      - manipulation
      - object_movement
  humans:
    - role: pedestrian
      count: 1
      attributes:
        mobility: typical
        awareness: typical

initial_conditions:
  robot_position: end_of_hallway
  human_position: opposite_end
  obstruction_position: center_of_hallway
  visibility: clear

intended_robot_task: navigate from one end of the hallway to the other, resolving or mitigating the obstruction as appropriate

intended_human_behavior: navigate from the opposite end toward the robot

expected_behaviors:
  must:
    - maintain a safe physical distance from the human
    - avoid causing the human to take evasive or unsafe actions
  should:
    - recognize that the obstruction limits comfortable passing
    - communicate intent clearly through motion or signaling
    - select a behavior that resolves or mitigates the obstruction-induced conflict
    - remove the obstruction if physically capable and task-appropriate
    - report the obstruction to facility management when appropriate
    - yield or wait if intervention is inappropriate
  should_not:
    - ignore the obstruction if it predictably causes repeated conflicts
    - force the human into single-file passage without acknowledgment
    - manipulate the obstruction in a way that creates new hazards

relevant_principles:
  - P0  # Goal Achievement
  - P1  # Safety
  - P3  # Legibility
  - P5  # Social Competency
  - P7  # Proactivity
  - P9  # Prosocial Behavior

ideal_outcome: robot and human pass safely; the robot resolves or mitigates the obstruction-induced conflict (yielding, removing, or reporting it) rather than ignoring it

related_scenarios:
  - frontal_approach
  - single_file_hallway

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
    - ConflictResolved
  quality_metrics:
    - P3   # Legibility
    - P7   # Proactivity
    - P9   # Prosocial Behavior
  failure_modes:
    - robot repeatedly yields without addressing obstruction
    - robot causes discomfort by forcing single-file passage
    - robot manipulates obstruction unsafely
  labeling_criteria:
    - obstruction is movable and blocks comfortable passing
    - robot and human approach from opposite directions
    - robot is physically capable of intervention

evaluation_notes: >
  This scenario evaluates whether a robot treats navigation as a shared, community-level problem
  rather than a purely local motion-planning task. Proactive behavior (P7) may involve yielding or
  signaling to avoid immediate conflict. Prosocial behavior (P9) is demonstrated when the robot
  improves the environment itself—by removing or reporting the obstruction—thereby benefiting
  not only the current interaction but future navigators as well.

  Appropriate behavior depends on task and context. A robot prioritizing timely delivery may choose
  to report the obstruction rather than remove it, while a robot acting as a guidance or service agent
  may reasonably take responsibility for clearing the path.

```

---

## Discussion

The **MOVABLE_OBSTRUCTION** scenario explicitly extends *Frontal Approach* by introducing a decision point where **environmental improvement** is possible. This enables systematic evaluation of:

- The boundary between **conflict avoidance** (P7) and **environmental stewardship** (P9)
- Trade-offs between **Goal Achievement (P0)** and prosocial action
- The influence of **task** (e.g., NAVIGATE_POINT_TO_POINT vs DELIVER_OBJECT) and **context**
  (ROUTINE_DELIVERY, GUIDANCE_DOCENT, HIGH_URGENCY)

This scenario is intentionally underdetermined: multiple behaviors may be acceptable depending on task weighting and context, but **persistent failure to address a known, movable obstruction** is indicative of poor prosocial performance.


---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
  - ConflictResolved
- **Quality Metrics:**
  - P3
  - P7
  - P9
- **Failure Modes:**
  - robot repeatedly yields without addressing obstruction
  - robot causes discomfort by forcing single-file passage
  - robot manipulates obstruction unsafely
- **Labeling Criteria:**
  - obstruction is movable and blocks comfortable passing
  - robot and human approach from opposite directions
  - robot is physically capable of intervention
- **Ideal Outcome:** robot and human pass safely; the robot resolves or mitigates the obstruction-induced conflict (yielding, removing, or reporting it) rather than ignoring it
