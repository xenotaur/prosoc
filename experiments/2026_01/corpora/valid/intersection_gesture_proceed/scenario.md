# Intersection – Gesture Proceed

## Status

- **STATE:** DRAFTED
- **SOURCE:** Principles and Guidelines for Social Robot Navigation (Table 3)
- **DRAFTED:** ChatGPT, 2026-01-06
- **EDITED:** —

---

## Scenario Card Summary

- **Scenario Name:** Intersection – Gesture Proceed
- **Scenario Description:** Physical robot and human cross at an indoor intersection; the human explicitly gestures for the robot to proceed.
- **Physical Environment:** Indoor
- **Geometric Layout:** Intersection
- **Scientific Purpose:** Pedestrian interaction
- **Robot Role:** Any (navigating agent)
- **Robot Task:** Navigate from A to B
- **Human Behavior:** Cross navigation with explicit proceed gesture
- **Ideal Outcome:** Human gestures, robot proceeds, human proceeds, no collision
- **Related Scenarios:** Intersection – No Gesture; Intersection – Gesture Wait
- **Cited In:** Principles and Guidelines for Social Robot Navigation (Table 3)

---

## Scenario Overview

This scenario describes an **intersection crossing interaction** in which a robot and a human pedestrian approach an indoor intersection, and the **human explicitly gestures for the robot to proceed**.

In this case, the human resolves ambiguity about right-of-way by granting the robot permission to enter the intersection. The robot is expected to recognize the gesture, commit to motion promptly, and traverse the intersection in a way that is safe, legible, and socially appropriate.

The scenario evaluates whether the robot can **confidently but responsibly act on explicit human permission**, balancing goal achievement with safety and comfort.

---

## Social Navigation Context

In human–human interactions, gestures such as a forward wave or pointing motion are commonly used to invite another agent to proceed first. When such a signal is given, hesitation or failure to act can create confusion or inefficiency, while overly aggressive motion can undermine trust.

For robots, responding to a “proceed” gesture requires not only recognizing the signal but also committing to a clear trajectory and timing that confirms the robot has accepted the invitation.

This scenario corresponds to **“Intersection – Gesture Proceed”** cases discussed in the *Principles and Guidelines for Social Robot Navigation* paper, emphasizing legibility, responsiveness, and appropriate assertiveness.

---

## Normative Expectations

Acceptable robot behavior in this scenario may include:

- recognizing the human’s gesture as permission to proceed,
- entering the intersection without undue delay,
- maintaining a smooth and predictable trajectory while crossing.

Unacceptable behavior includes ignoring the gesture, hesitating excessively after the signal, or proceeding in a way that startles or endangers the human.

---

## Scenario Specification (Machine-Readable)

```yaml
id: intersection_gesture_proceed_01
name: Intersection – Gesture Proceed

summary: >
  A robot and a human pedestrian approach an indoor intersection. The human
  explicitly gestures for the robot to proceed. The robot must recognize the
  gesture and cross the intersection safely, legibly, and without undue delay.

context:
  environment:
    type: indoor
    setting: hallway intersection
    width: moderate
  social_setting:
    formality: informal
    crowd_level: low

agents:
  robot:
    role: navigating_agent
    capabilities:
      - forward_motion
      - speed_adjustment
      - stopping
      - gesture_recognition
      - path_commitment
  humans:
    - role: pedestrian
      count: 1
      attributes:
        mobility: typical
        gesturing: proceed

initial_conditions:
  approach_pattern: orthogonal
  arrival_timing: near_simultaneous
  visibility: mutual

expected_behaviors:
  must:
    - recognize the human’s gesture granting permission to proceed
    - enter and traverse the intersection safely
    - avoid collision with the human
  should:
    - commit promptly to motion after the gesture
    - maintain a smooth and legible trajectory
  should_not:
    - hesitate excessively after permission is given
    - proceed aggressively or at unsafe speed
    - undermine the clarity of the human’s signal

relevant_principles:
  - P0  # Goal Achievement
  - P1  # Safety
  - P2  # Comfort
  - P3  # Legibility
  - P4  # Politeness
  - P9  # Prosocial Behavior


evaluation_notes: >
  This scenario evaluates the robot’s ability to act appropriately on explicit
  human permission. Successful behavior demonstrates timely commitment,
  predictable motion, and respect for the human’s safety and comfort.

  Failure modes include ignoring the gesture, delayed or ambiguous motion,
  or overly aggressive crossing behavior.
```

---

## Scenario Usage Guide

### Success Metrics
- No collision occurs
- Robot commits to crossing promptly after gesture
- Human proceeds without hesitation or retreat

### Quality Metrics
- Time between gesture and robot motion
- Smoothness and predictability of robot trajectory
- Absence of oscillation or hesitation

### Ideal Outcome
- Robot accepts the gesture and crosses smoothly
- Human follows and crosses without disruption

### Failure Modes
- Ignoring the gesture
- Excessive hesitation after permission
- Aggressive or unsafe crossing

### Labeling Criteria
- Outcome: Success / Partial Success / Failure
- Gesture recognized: Yes / No
- Human disrupted: Yes / No

---

## Notes for Scenario Designers and Evaluators

- This scenario assumes the human’s gesture is clear and unambiguous.
- Variants may explore delayed execution, partial gestures, or conflicting
  signals from multiple humans.
- Comparison with the no-gesture and gesture-wait scenarios helps isolate
  the effects of explicit permission versus implicit coordination.

