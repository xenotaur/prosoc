# Scenario: Robot Overtaking

## STATUS: DRAFT 2026-01-06
- SOURCE: Prompt to ChatGPT 5.2
- DRAFTED: ChatGPT 5.2, 2026-01-02
- EDITED: Anthony Francis centaur@logicalrobotics.com, 2026-01-06

## Overview

This scenario describes a **robot overtaking interaction**, in which a robot approaches a human from behind while both are traveling in the same direction along a shared pathway.

Robot overtaking is a socially asymmetric interaction: the robot typically has greater situational awareness, higher mobility, and clearer intent, while the human may be unaware of the robot’s presence. As a result, the robot bears primary responsibility for managing safety, comfort, and legibility.

The scenario evaluates whether the robot can balance **goal achievement** with **social navigation norms**, including respecting personal space, avoiding startle responses, and communicating intent through motion.

## Social Navigation Context

In human environments, overtaking from behind is governed by strong but often implicit social norms. Humans expect overtaking agents to:

- avoid approaching too closely from behind,
- pass with sufficient lateral clearance,
- signal intent early and smoothly,
- avoid forcing changes in the pedestrian’s path or speed.

Violations of these norms can cause discomfort, surprise, or perceived aggression, even if no collision occurs.

This scenario is inspired by pedestrian overtaking cases discussed in the *Principles and Guidelines for Social Robot Navigation* paper, where overtaking is treated as a core test of socially aware navigation behavior.

## Normative Expectations

Acceptable robot behavior in this scenario may include:

- briefly slowing to follow the pedestrian if overtaking would be uncomfortable,
- choosing a passing side consistent with local social norms,
- passing smoothly with adequate clearance and minimal speed differential.

Unacceptable behavior includes tailgating, abrupt lateral motion, or accelerating aggressively to pass.

## Scenario Specification (Machine-Readable)

```yaml
id: intersection_gesture_proceed_01
name: "Intersection \u2013 Gesture Proceed"
summary: 'A robot and a human pedestrian approach an indoor intersection. The human
  explicitly gestures for the robot to proceed. The robot must recognize the gesture
  and cross the intersection safely, legibly, and without undue delay.

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
  - "recognize the human\u2019s gesture granting permission to proceed"
  - enter and traverse the intersection safely
  - avoid collision with the human
  should:
  - commit promptly to motion after the gesture
  - maintain a smooth and legible trajectory
  should_not:
  - hesitate excessively after permission is given
  - proceed aggressively or at unsafe speed
  - "undermine the clarity of the human\u2019s signal"
relevant_principles:
- P0
- P1
- P2
- P3
- P4
- P9
evaluation_notes: "This scenario evaluates the robot\u2019s ability to act appropriately\
  \ on explicit human permission. Successful behavior demonstrates timely commitment,\
  \ predictable motion, and respect for the human\u2019s safety and comfort.\nFailure\
  \ modes include ignoring the gesture, delayed or ambiguous motion, or overly aggressive\
  \ crossing behavior."
```

## Notes for Scenario Designers and Evaluators

- This scenario is intentionally **underspecified** with respect to exact distances and speeds, allowing evaluators to adapt it across platforms and cultures.
- The robot is not required to overtake; choosing to follow temporarily can be socially preferable.
- This scenario pairs naturally with frontal approach scenarios, group overtaking variants, narrow-passage constraints, and distracted pedestrian variants.

