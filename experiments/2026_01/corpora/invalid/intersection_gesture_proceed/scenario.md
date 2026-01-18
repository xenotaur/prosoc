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
"id: frontal_approach_01\nname: Frontal Approach\n\nsummary: >\n  A robot and a human\
  \ approach each other in opposite directions in a narrow hallway and pass each other\
  \ safely, comfortably, and without\n  prolonged hesitation.\n\ncontext:\n  environment:\n\
  \    type: indoor\n    setting: office hallway\n    width: narrow\n  social_setting:\n\
  \    formality: informal\n    crowd_level: low\n\nagents:\n  robot:\n    role: navigating_agent\n\
  \    capabilities:\n      - forward_motion\n      - steering\n      - stopping\n\
  \  humans:\n    - role: pedestrian\n      count: 1\n      attributes:\n        mobility:\
  \ typical\n        awareness: typical\n\ninitial_conditions:\n  robot_position:\
  \ end_of_hallway\n  human_position: opposite_end\n  visibility: clear\n\nexpected_behaviors:\n\
  \  must:\n    - maintain a safe physical distance\n    - avoid physical contact\
  \ or forcing evasive action\n  should:\n    - signal intent clearly through motion\
  \ or positioning\n    - resolve hesitation without prolonged deadlock\n    - yield\
  \ if appropriate given the spatial configuration\n  should_not:\n    - force the\
  \ human to stop abruptly\n    - invade personal space\n    - advance aggressively\
  \ in a way that causes discomfort\n\nrelevant_principles:\n  - P1  # Safety\n  -\
  \ P2  # Comfort\n  - P3  # Legibility\n  - P5  # Social Competency\n  - P6  # Agent\
  \ Understanding\n\nscenario_usage_guide:\n  success_metrics:\n    - SR\n    - NoCollisions\n\
  \  quality_metrics:\n    - P2   # Comfort\n    - P3   # Legibility\n    - P5   #\
  \ Social Competency\n  failure_modes:\n    - robot collides with human\n    - robot\
  \ fails to pass within time limit\n  labeling_criteria:\n    - robot and human face\
  \ each other at the start of the episode\n    - robot and human move toward each\
  \ other\n    - sufficient clearance exists for passing\n\nevaluation_notes: >\n\
  \  This scenario evaluates how well the robot navigates through shared space with\
  \ a human in the conditions for a mild and typiocal conflict.\n  Changing direction,\
  \ slowing down, braking or hesitation may be acceptable if they increase safety,\
  \ comfort, or legibility, but  prolonged deadlock, abrupt reversals,\n  or aggressive\
  \ advancement are indicative of poor performance.\n\n  The scenario assumes a pedestrian\
  \ with a typical level of awareness,\n  neither oblivious to the presence of the\
  \ robot nor overly attettentive too it."
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

