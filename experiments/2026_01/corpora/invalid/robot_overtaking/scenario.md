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
"id: intersection_gesture_proceed_01\nname: Intersection \u2013 Gesture Proceed\n\n\
  summary: >\n  A robot and a human pedestrian approach an indoor intersection. The\
  \ human\n  explicitly gestures for the robot to proceed. The robot must recognize\
  \ the\n  gesture and cross the intersection safely, legibly, and without undue delay.\n\
  \ncontext:\n  environment:\n    type: indoor\n    setting: hallway intersection\n\
  \    width: moderate\n  social_setting:\n    formality: informal\n    crowd_level:\
  \ low\n\nagents:\n  robot:\n    role: navigating_agent\n    capabilities:\n    \
  \  - forward_motion\n      - speed_adjustment\n      - stopping\n      - gesture_recognition\n\
  \      - path_commitment\n  humans:\n    - role: pedestrian\n      count: 1\n  \
  \    attributes:\n        mobility: typical\n        gesturing: proceed\n\ninitial_conditions:\n\
  \  approach_pattern: orthogonal\n  arrival_timing: near_simultaneous\n  visibility:\
  \ mutual\n\nexpected_behaviors:\n  must:\n    - recognize the human\u2019s gesture\
  \ granting permission to proceed\n    - enter and traverse the intersection safely\n\
  \    - avoid collision with the human\n  should:\n    - commit promptly to motion\
  \ after the gesture\n    - maintain a smooth and legible trajectory\n  should_not:\n\
  \    - hesitate excessively after permission is given\n    - proceed aggressively\
  \ or at unsafe speed\n    - undermine the clarity of the human\u2019s signal\n\n\
  relevant_principles:\n  - P0  # Goal Achievement\n  - P1  # Safety\n  - P2  # Comfort\n\
  \  - P3  # Legibility\n  - P4  # Politeness\n  - P9  # Prosocial Behavior\n\n\n\
  evaluation_notes: >\n  This scenario evaluates the robot\u2019s ability to act appropriately\
  \ on explicit\n  human permission. Successful behavior demonstrates timely commitment,\n\
  \  predictable motion, and respect for the human\u2019s safety and comfort.\n\n\
  \  Failure modes include ignoring the gesture, delayed or ambiguous motion,\n  or\
  \ overly aggressive crossing behavior."
```

## Notes for Scenario Designers and Evaluators

- This scenario is intentionally **underspecified** with respect to exact distances and speeds, allowing evaluators to adapt it across platforms and cultures.
- The robot is not required to overtake; choosing to follow temporarily can be socially preferable.
- This scenario pairs naturally with frontal approach scenarios, group overtaking variants, narrow-passage constraints, and distracted pedestrian variants.

