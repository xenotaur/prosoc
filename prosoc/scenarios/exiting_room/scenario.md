# Scenario: Exiting Room

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); Robotics at Google (R@G), internal scenario reference
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** render_sections.py, 2026-07-20

---

## Scenario Card Summary

- **Scenario Name:** Exiting Room
- **Scenario Description:** A robot exits a room through a doorway while a human is simultaneously entering the same room through the same doorway. The robot is expected to exit first, but must avoid colliding with or blocking the entering human.
- **Scientific Purpose:** pedestrian interaction
- **Physical Environment:** indoor
- **Geometric Layout:** room and door
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from inside to outside the room
- **Human Behavior:** navigate from outside to inside the room
- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P3
  - P5
- **Ideal Outcome:** robot exits the room first, then the human enters, without collision or obstruction
- **Related Scenarios:** entering_room, narrow_doorway
- **Cited In:** Robotics at Google (R@G), internal scenario reference

---

## Scenario Overview

This scenario describes a robot **exiting a room while a human is simultaneously entering** the same room through the same doorway. It is the inverse of Entering Room: here the robot's task is to transition from inside to outside, while the human's task is to transition from outside to inside.

The defining challenge is again **directional right-of-way at a threshold with asymmetric roles**, but with the ideal outcome reversed from Entering Room: per the P&G paper, the ideal outcome here is that the **robot exits first**. This reflects a task-oriented norm rather than a strict "occupant always has priority" rule — the robot, having already completed its business in the room, should not be delayed indefinitely by an entering human, but should also not force its way out if the human is already committed to the doorway.

Successful navigation requires the robot to time its exit so that it clears the doorway promptly, without colliding with or blocking the entering human, and without hesitating so long that the scenario's intended outcome (robot exits first) fails to occur.

---

## Social Navigation Context

This scenario probes a subtler social convention than the generic "let people out first" norm: here the robot is the one leaving, and the paper's stated ideal outcome is that the robot should exit before the human enters, rather than deferring to the entering human. This is consistent with the "let people out first" convention viewed from the exiting party's perspective — the robot, as the one already inside and moving toward the door, occupies the socially favored position.

Key challenges:

- **Role asymmetry**: the robot's task (exit) and the human's task (enter) are directly opposed at the same threshold.
- **Priority calibration**: unlike Entering Room, where the robot defers, here the robot is expected to proceed with reasonable confidence, while still avoiding collision if the human is already crossing the threshold.
- **Avoiding false confidence**: the robot must not use "I have priority" as a license to push through a doorway the human has already entered.

This scenario is scientifically interesting because, when paired with Entering Room, it tests whether the robot's priority-taking behavior correctly flips depending on which side of the doorway transition it is performing.

---

## Normative Expectations

Acceptable robot behavior includes:

- Proceeding toward the doorway and exiting promptly when it is the first to reach the threshold
- Slowing or briefly pausing if the human is already committed to entering through the doorway
- Communicating an exiting intent early enough that the human can wait
- Resolving the encounter without a prolonged stand-off

Unacceptable behavior includes:

- Deferring to the entering human by default, contrary to the scenario's intended outcome
- Pushing through the doorway after the human has already begun entering
- Colliding with the human at or near the threshold
- Hesitating indefinitely, resulting in neither party exiting or entering

---

## Scenario Specification (Machine-Readable)

```yaml
id: exiting_room_01
name: Exiting Room

summary: >
  A robot exits a room through a doorway while a human is simultaneously
  entering the same room through the same doorway. The robot is expected to
  exit first, but must avoid colliding with or blocking the entering human.

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
  robot_position: inside the room, moving toward the doorway
  human_position: outside the room, moving toward the doorway
  robot_task_direction: inside to outside
  human_task_direction: outside to inside

intended_robot_task: navigate from inside to outside the room

intended_human_behavior: navigate from outside to inside the room

expected_behaviors:
  must:
    - avoid collision with the human at the doorway
    - not force the human to reverse or stop abruptly if the human has already committed to the doorway
  should:
    - proceed to exit promptly when the robot reaches the threshold first
    - signal exiting intent clearly and early
    - yield briefly if the human is already committed to entering
  should_not:
    - default to deferring to the human without cause, contrary to the expected robot-exits-first outcome
    - push through the doorway after the human has already begun entering
    - hesitate indefinitely at the threshold

relevant_principles:
  - P1  # Safety — collision risk at the shared threshold
  - P3  # Legibility — robot must clearly signal its exiting intent
  - P5  # Social Competency — applying the task-appropriate exit-priority norm
  - P6  # Agent Understanding — recognizing whether the human has already committed to entering

ideal_outcome: robot exits the room first, then the human enters, without collision or obstruction

related_scenarios:
  - entering_room
  - narrow_doorway

cited_in:
  - "Robotics at Google (R@G), internal scenario reference"

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
  quality_metrics:
    - P3  # Legibility
    - P5  # Social Competency
  failure_modes:
    - robot collides with human at the doorway
    - robot defers to the human by default and fails to exit first as intended
    - robot pushes through after the human has already begun entering
    - prolonged stand-off with neither agent moving through the doorway
  labeling_criteria:
    - robot is positioned inside a room with the task of exiting
    - a human is outside the room and moving toward the same doorway to enter
    - the robot's and human's paths intersect at the doorway

evaluation_notes: >
  Ambiguity note: the P&G Table 3 entry for this scenario lists the Human
  Behavior field as "Navigate in to out," which appears to be a transcription
  inconsistency given the scenario Description ("Robot exits a room while a
  human enters") and the stated Ideal Outcome ("Robot exits first"). This
  card follows the Description and Ideal Outcome fields, treating the human
  as navigating from outside to inside (entering) while the robot exits.
  A human editor should verify this interpretation against the source paper
  text if available.

  This scenario is the inverse of Entering Room. When both scenarios are
  used together, evaluators can check whether the robot's priority-taking
  correctly flips based on its own task direction (entering defers,
  exiting proceeds) rather than applying a single fixed rule regardless
  of role.

  This scenario is related to Exiting Elevator (Figure 7, not in Table 3),
  which applies a similar norm in a higher-density, time-constrained
  elevator context.
```

---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P3
  - P5
- **Ideal Outcome:** robot exits the room first, then the human enters, without collision or obstruction
- **Failure Modes:**
  - robot collides with human at the doorway
  - robot defers to the human by default and fails to exit first as intended
  - robot pushes through after the human has already begun entering
  - prolonged stand-off with neither agent moving through the doorway
- **Labeling Criteria:**
  - robot is positioned inside a room with the task of exiting
  - a human is outside the room and moving toward the same doorway to enter
  - the robot's and human's paths intersect at the doorway

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Entering Room*: the inverse role assignment, where the robot defers to an exiting human. Pairing the two scenarios tests whether robot priority behavior is correctly role-sensitive.
- *Exiting Elevator* (Figure 7 variant): the same norm applied within an elevator car, typically at higher crowd density and under time pressure from closing doors.
- *Narrow Doorway*: a symmetric two-way crossing without a fixed enter/exit priority expectation.

**Suggested variants:**
- Human already partway through the doorway when the robot begins to exit, testing collision avoidance under a violated priority assumption
- Multiple humans queued to enter, testing whether the robot still exits cleanly amid a small queue
- Time-pressured variant where the robot has an urgent reason to exit quickly

**Key measurement question:** Does the robot correctly take priority when exiting (rather than reflexively yielding, as in Entering Room), while still avoiding collision if the human has already committed to the doorway?
