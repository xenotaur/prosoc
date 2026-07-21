# Scenario: Object Handover

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [161]
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** render_sections.py, 2026-07-19

---

## Scenario Card Summary

- **Scenario Name:** Object Handover
- **Scenario Description:** A robot in a servant role navigates to a human and hands over an object. The robot must transition from open navigation to a close-range, comfortable final approach, present the object for an easy reach, and recognize when the human has received it.
- **Scientific Purpose:** interactive navigation
- **Physical Environment:** generic
- **Geometric Layout:** passable space
- **Robot Role:** servant
- **Robot Task:** deliver the object to the human
- **Human Behavior:** receive the object
- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P2
  - P4
- **Ideal Outcome:** human takes the object from the robot without awkwardness, collision, or dropped object
- **Related Scenarios:** crash_cart
- **Cited In:** 161

---

## Scenario Overview

This scenario describes a robot in a **servant role** whose task is to navigate to a human and deliver an object, with the human's role being to receive it. Unlike pure transit scenarios, Object Handover has a terminal interactive phase: after navigating to within reach of the human, the robot must position itself so the handover can occur comfortably and safely, and the episode concludes only once the human has taken the object.

The defining challenge is **combining navigation with a close-range interactive handoff**: the robot must transition from open-space navigation to a final approach that accounts for arm reach, orientation toward the human, and the appropriate final distance for a handover — closer than typical passing distance, but not so close as to invade personal space or create a hazard while extending the object.

Successful navigation requires the robot to approach the human at a comfortable angle and speed, stop at a distance and orientation suitable for a handover, present the object such that the human can take it without awkward reaching, and recognize when the object has been received to conclude the interaction.

---

## Social Navigation Context

Object handover is a canonical human-robot interaction task in delivery robots, assistive robots, and service robots — it appears in warehouse-to-person delivery, home assistance, and hospital contexts. Unlike ordinary personal-space norms that keep pedestrians at arm's length or beyond, a successful handover explicitly requires closing that distance, but doing so must be signaled clearly and executed at a controlled, non-startling pace.

Key challenges:

- **Final approach distance**: personal-space norms must be deliberately relaxed for the handover, but the transition must feel intentional and controlled, not like an unexpected approach.
- **Orientation and presentation**: the robot must orient the object and itself so the human's reach is natural, given the human's likely dominant hand and standing position.
- **Timing the release**: releasing an object too early (before the human has a secure grip) or too late (holding on after the human has taken hold) can create an awkward or unsafe moment.
- **Recognizing completion**: the robot must correctly detect that the object has changed hands to conclude the interaction and disengage.

This scenario is scientifically interesting because it bridges navigation research and human-robot physical interaction, evaluating the transition from approach navigation to a cooperative manipulation-adjacent event.

---

## Normative Expectations

Acceptable robot behavior includes:

- Approaching the human at a moderate, predictable pace along a legible path
- Slowing and stopping at a distance appropriate for a comfortable handover (closer than typical passing distance)
- Orienting itself and the object to allow a natural, unstrained reach
- Waiting for a clear indication of grip before releasing the object

Unacceptable behavior includes:

- Approaching at a pace or trajectory that startles the human or resembles an unrelated close pass
- Stopping too far away, requiring the human to step forward or lean uncomfortably
- Presenting the object at an angle or height that is awkward to reach
- Releasing the object before the human has a secure hold, or continuing to hold it after the human has grasped it

---

## Scenario Specification (Machine-Readable)

```yaml
id: object_handover_01
name: Object Handover

summary: >
  A robot in a servant role navigates to a human and hands over an object.
  The robot must transition from open navigation to a close-range,
  comfortable final approach, present the object for an easy reach, and
  recognize when the human has received it.

scientific_purpose: interactive navigation

geometric_layout: passable space

context:
  environment:
    type: generic
    setting: home, office, or service environment
    width: moderate
  social_setting:
    formality: informal
    crowd_level: low

agents:
  robot:
    role: servant
    capabilities:
      - forward_motion
      - steering
      - stopping
      - speed_adjustment
      - orientation_control
      - object_manipulation
  humans:
    - role: pedestrian
      count: 1
      attributes:
        mobility: typical
        awareness: typical

initial_conditions:
  robot_position: some distance from the human, carrying an object to deliver
  human_position: stationary, aware of the robot's approach
  object_state: held by the robot, to be transferred to the human

intended_robot_task: deliver the object to the human

intended_human_behavior: receive the object

expected_behaviors:
  must:
    - avoid collision with the human during approach
    - not release the object before the human has a secure grip
  should:
    - approach at a moderate, predictable pace
    - stop at a distance and orientation suitable for a comfortable handover
    - present the object so the human can reach it naturally
    - recognize when the object has been received and disengage
  should_not:
    - approach in a way that startles the human
    - stop too far away, requiring the human to step forward or overreach
    - continue holding the object after the human has taken hold

relevant_principles:
  - P1  # Safety — collision and object-drop risk during close-range handover
  - P2  # Comfort — final approach distance and pace affect the human's comfort
  - P4  # Politeness — courteous presentation and timing of the handover
  - P6  # Agent Understanding — recognizing grip and release timing

ideal_outcome: human takes the object from the robot without awkwardness, collision, or dropped object

related_scenarios:
  - crash_cart

cited_in:
  - "161"

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
  quality_metrics:
    - P2  # Comfort
    - P4  # Politeness
  failure_modes:
    - robot collides with or startles the human during final approach
    - robot stops too far away, forcing an awkward reach
    - object is dropped due to premature release or unclear grip timing
    - robot lingers after handover, prolonging the interaction unnecessarily
  labeling_criteria:
    - the robot is carrying or holding an object intended for a specific human
    - the robot's task terminates in a close-range handover rather than a pass-through
    - the episode includes a final approach phase distinct from open-space navigation

evaluation_notes: >
  This scenario spans both navigation and manipulation-adjacent behavior;
  evaluators focused purely on trajectory metrics should still assess the
  final approach distance and orientation, since these are the primary
  social navigation contribution to an otherwise manipulation-heavy task.

  The appropriate handover distance is context-dependent (e.g., closer for
  a small light object, more cautious for a hot beverage or sharp object)
  and should be noted when instantiating this scenario for a specific
  object type.

  This scenario is related to Crash Cart, a specialized variant involving
  urgent medical delivery in an indoor setting, and to Robot Courier
  (a general delivery task without the close-range interactive handoff
  emphasized here).
```

---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P2
  - P4
- **Ideal Outcome:** human takes the object from the robot without awkwardness, collision, or dropped object
- **Failure Modes:**
  - robot collides with or startles the human during final approach
  - robot stops too far away, forcing an awkward reach
  - object is dropped due to premature release or unclear grip timing
  - robot lingers after handover, prolonging the interaction unnecessarily
- **Labeling Criteria:**
  - the robot is carrying or holding an object intended for a specific human
  - the robot's task terminates in a close-range handover rather than a pass-through
  - the episode includes a final approach phase distinct from open-space navigation

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Crash Cart*: a specialized, urgency-driven variant of object delivery in a medical/indoor context, with a different risk and pacing profile.
- *Robot Courier*: a related but more general delivery task that may not require the same close-range interactive handoff detail.

**Suggested variants:**
- Object type variation (light/small vs. bulky/fragile), affecting appropriate approach distance and orientation
- Human distracted or not immediately aware of the robot's approach, requiring an attention-getting signal before the handover
- Handover interrupted (human steps away mid-approach), testing the robot's ability to pause or replan

**Key measurement question:** Does the robot's final approach and presentation of the object feel natural and unhurried to the human, or does the transition from open navigation to close-range interaction feel abrupt or awkward?
