# Scenario: Movable Obstruction

## STATUS: DRAFT 2026-01-16
- SOURCE: Principles and Guidelines for Evaluating Social Robot Navigation (P&G paper)
- DRAFTED: ChatGPT 5.2, 2026-01-16
- EDITED: Anthony Francis centaur@logicalrobotics.com (pending)

## Overview

This scenario describes a social navigation conflict in which a robot and a human approach each other in a hallway that is nominally wide enough for passing, but partially blocked by a **movable obstruction** (e.g., a cart, box, or misplaced furniture). The scenario is designed to distinguish **Proactivity (P7)** from **Prosocial Behavior (P9)** by introducing opportunities for the robot to improve the navigability of the environment, rather than merely adapting to it.

Unlike *Frontal Approach*, successful navigation in this scenario may involve **environmental intervention** (physically moving the obstruction or reporting it), not just motion planning or yielding behavior.

---

```yaml
id: intersection_gesture_wait_01
name: "Intersection \u2013 Gesture Wait"
summary: 'A robot and a human pedestrian approach an indoor intersection. The human
  explicitly gestures for the robot to wait. The robot must recognize and comply with
  the gesture, yielding the intersection safely and legibly.

  '
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
  humans:
  - role: pedestrian
    count: 1
    attributes:
      mobility: typical
      gesturing: wait
initial_conditions:
  approach_pattern: orthogonal
  arrival_timing: near_simultaneous
  visibility: mutual
expected_behaviors:
  must:
  - "recognize the human\u2019s gesture requesting the robot to wait"
  - stop or slow before entering the intersection
  - avoid entering the intersection until it is clear
  should:
  - acknowledge the gesture through compliant motion
  - remain stationary and predictable while yielding
  should_not:
  - "ignore or override the human\u2019s gesture"
  - proceed into the intersection prematurely
  - display ambiguous motion while waiting
relevant_principles:
- P0
- P1
- P2
- P3
- P4
- P9
evaluation_notes: "This scenario evaluates the robot\u2019s ability to comply with\
  \ explicit human social signals. Successful behavior prioritizes deference and safety\
  \ over efficiency, reinforcing trust and predictability.\nFailure modes include\
  \ ignoring the gesture, partial compliance that introduces ambiguity, or delayed\
  \ responses that undermine the signal."
```

---

## Discussion

The **MOVABLE_OBSTRUCTION** scenario explicitly extends *Frontal Approach* by introducing a decision point where **environmental improvement** is possible. This enables systematic evaluation of:

- The boundary between **conflict avoidance** (P7) and **environmental stewardship** (P9)
- Trade-offs between **Goal Achievement (P0)** and prosocial action
- The influence of **task** (e.g., NAVIGATE_POINT_TO_POINT vs DELIVER_OBJECT) and **context**
  (ROUTINE_DELIVERY, GUIDANCE_DOCENT, HIGH_URGENCY)

This scenario is intentionally underdetermined: multiple behaviors may be acceptable depending on task weighting and context, but **persistent failure to address a known, movable obstruction** is indicative of poor prosocial performance.

