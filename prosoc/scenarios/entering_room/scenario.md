# Scenario: Entering Room

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); Robotics at Google (R@G), internal scenario reference
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** render_sections.py, 2026-07-20

---

## Scenario Card Summary

- **Scenario Name:** Entering Room
- **Scenario Description:** A robot approaches a room from outside with the task of entering, while a human occupant inside the room is simultaneously heading toward the same doorway to exit. The robot must defer to the exiting human before entering.
- **Scientific Purpose:** pedestrian interaction
- **Physical Environment:** indoor
- **Geometric Layout:** room and door
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from outside to inside the room
- **Human Behavior:** navigate from inside to outside the room
- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P4
  - P5
- **Ideal Outcome:** robot lets the human exit fully, then enters the room without obstruction
- **Related Scenarios:** exiting_room, narrow_doorway
- **Cited In:** Robotics at Google (R@G), internal scenario reference

---

## Scenario Overview

This scenario describes a robot **entering a room that is currently occupied by a human**, while that human is simultaneously heading toward the same doorway to exit. Unlike Narrow Doorway, where both agents cross a threshold in a generic two-way corridor sense, Entering Room is asymmetric: the robot's task is specifically to transition from outside the room to inside it, while the human's task is to transition from inside to outside.

The defining challenge is **directional right-of-way at a threshold with asymmetric roles**: conventional etiquette in many cultures favors letting the occupant/exiting party leave before someone enters. The robot must recognize that the human is already inside and moving toward the exit, and defer accordingly, rather than treating the doorway as a symmetric passing situation.

Successful navigation requires the robot to pause or hold position outside the doorway, allow the human to exit fully, and then proceed to enter — without blocking the door or hovering in a way that pressures the human to hurry.

---

## Social Navigation Context

In many social contexts, the norm is "let people out before you go in" — familiar from elevators, subway cars, and meeting rooms. This norm is not universal but is common enough in shared indoor spaces (offices, homes) that robots operating in such environments should generally default to it unless explicit context indicates otherwise.

Key challenges:

- **Role asymmetry**: the robot's task (enter) and the human's task (exit) are directly opposed at the same threshold, unlike a generic two-way doorway crossing.
- **Norm awareness**: the robot must apply the "exiting party goes first" convention rather than a naive first-come-first-served or shortest-path heuristic.
- **Avoiding the appearance of hovering**: waiting too conspicuously close to the doorway can make the human feel rushed or watched.

This scenario is scientifically interesting because it tests whether the robot's yielding behavior is sensitive to *task role* (entering vs. exiting) rather than purely to geometry or timing.

---

## Normative Expectations

Acceptable robot behavior includes:

- Detecting that the room is occupied and that the human is moving toward the doorway to exit
- Holding position at a comfortable distance from the doorway rather than crowding it
- Allowing the human to exit completely before entering
- Proceeding into the room promptly once the threshold is clear

Unacceptable behavior includes:

- Attempting to enter the room while the human is still in the doorway or actively exiting
- Blocking the human's exit path by positioning too close to the door
- Waiting so far back or so passively that entry is delayed long after the human has cleared
- Hovering directly in the doorway in a way that makes the human feel crowded while exiting

---

## Scenario Specification (Machine-Readable)

```yaml
id: entering_room_01
name: Entering Room

summary: >
  A robot approaches a room from outside with the task of entering, while a
  human occupant inside the room is simultaneously heading toward the same
  doorway to exit. The robot must defer to the exiting human before entering.

scientific_purpose: pedestrian interaction

geometric_layout: room and door

context:
  environment:
    type: indoor
    setting: office or home room with a single doorway
    width: narrow
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
      - speed_adjustment
  humans:
    - role: pedestrian
      count: 1
      attributes:
        mobility: typical
        awareness: typical

initial_conditions:
  robot_position: outside the room, near the doorway
  human_position: inside the room, moving toward the doorway
  robot_task_direction: outside to inside
  human_task_direction: inside to outside

intended_robot_task: navigate from outside to inside the room

intended_human_behavior: navigate from inside to outside the room

expected_behaviors:
  must:
    - avoid blocking the human's exit path
    - avoid collision with the human at the doorway
  should:
    - hold position outside the doorway until the human has exited
    - proceed to enter promptly once the threshold is clear
  should_not:
    - attempt to enter while the human is still in the doorway
    - crowd the doorway in a way that pressures the human while exiting
    - wait indefinitely after the doorway is clear

relevant_principles:
  - P1  # Safety — collision risk at the shared threshold
  - P4  # Politeness — deferring to the exiting occupant
  - P5  # Social Competency — applying the "let people out first" norm
  - P6  # Agent Understanding — recognizing the human's exit intent and role

ideal_outcome: robot lets the human exit fully, then enters the room without obstruction

related_scenarios:
  - exiting_room
  - narrow_doorway

cited_in:
  - "Robotics at Google (R@G), internal scenario reference"

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
  quality_metrics:
    - P4  # Politeness
    - P5  # Social Competency
  failure_modes:
    - robot attempts to enter while human is still exiting, causing collision or blocking
    - robot crowds the doorway, forcing the human to squeeze past
    - robot waits far longer than necessary after the human has cleared the doorway
  labeling_criteria:
    - robot is positioned outside a room with the task of entering
    - a human occupant is inside the room and moving toward the same doorway to exit
    - the robot's and human's paths intersect at the doorway

evaluation_notes: >
  This scenario specifically tests role-sensitive yielding: the robot's
  yielding should be driven by the recognition that the human is exiting a
  room it is trying to enter, not simply by generic doorway right-of-way
  rules. Evaluators should distinguish a robot that defers because it
  recognizes the exit norm from one that happens to yield due to
  proximity-based reactive stopping.

  This scenario is closely related to Entering Elevator (Figure 7, not in
  Table 3), which shares the same "let people out first" norm but in an
  elevator car context with typically higher crowd density and a hard
  time constraint (door closing).

  The inverse of this scenario is Exiting Room, where the robot is the
  one leaving while a human enters.
```

---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P4
  - P5
- **Ideal Outcome:** robot lets the human exit fully, then enters the room without obstruction
- **Failure Modes:**
  - robot attempts to enter while human is still exiting, causing collision or blocking
  - robot crowds the doorway, forcing the human to squeeze past
  - robot waits far longer than necessary after the human has cleared the doorway
- **Labeling Criteria:**
  - robot is positioned outside a room with the task of entering
  - a human occupant is inside the room and moving toward the same doorway to exit
  - the robot's and human's paths intersect at the doorway

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Exiting Room*: the inverse role assignment — robot exits while human enters. Comparing behavior across both variants can reveal whether the robot's yielding logic is symmetric or specific to its own task direction.
- *Entering Elevator* (Figure 7 variant): same underlying norm, applied in a more crowded and time-constrained context.
- *Narrow Doorway*: a more symmetric two-way crossing without the enter/exit role distinction.

**Suggested variants:**
- Room occupied by multiple humans, only one of whom is exiting
- Human pauses in the doorway (e.g., to hold the door), testing whether the robot over-yields
- Time pressure variant where the robot has an urgent task, testing the acceptable limits of politeness delay

**Key measurement question:** Does the robot's yielding behavior generalize correctly to the "exiting party has priority" norm, or does it only react to immediate collision geometry regardless of task roles?
