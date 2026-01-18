# Scenario:Pedestrian Overtaking

## STATUS: DRAFT 2026-01-02
- SOURCE: Prompt to ChatGPT 5.2
- DRAFTED: ChatGPT 5.2, 2026-01-02
- EDITED: Anthony Francis centaur@logicalrobotics.com, 2026-01-02

## Overview

In this scenario, **a human pedestrian overtakes a slower-moving robot from behind** while both are traveling in the same direction along a shared pathway.

Unlike robot-overtaking scenarios, this interaction places the **initiative primarily with the human**, while the robot is expected to behave as a predictable, socially compliant participant. The robot must recognize that it is being overtaken and avoid behaviors that increase uncertainty, discomfort, or risk for the human.

The scenario evaluates whether the robot can maintain **prosocial navigation norms**—including predictability, deference, and respect for personal space—while continuing to make progress toward its goal.

---

## Social Navigation Context

In human environments, pedestrians routinely overtake slower agents such as other people, cyclists, or robots. When being overtaken, socially appropriate behavior typically involves:

- maintaining a steady and predictable trajectory,
- avoiding sudden lateral movements,
- refraining from accelerating or blocking,
- yielding sufficient space for safe passing.

Humans generally expect slower agents to be cooperative and non-obstructive during overtaking. Any ambiguity in motion can cause hesitation or discomfort, even if the physical space is sufficient.

This scenario corresponds to **pedestrian-overtaking cases** discussed in the *Principles and Guidelines for Social Robot Navigation* paper, where the robot’s role is primarily reactive rather than assertive.

---

## Normative Expectations

Acceptable robot behavior in this scenario may include:

- maintaining a consistent speed and heading while being overtaken,
- subtly yielding lateral space when feasible,
- avoiding sudden changes in velocity or direction.

Unacceptable behavior includes accelerating to prevent passing, drifting unpredictably, or positioning itself in a way that forces the pedestrian to take evasive action.

---

## Scenario Specification (Machine-Readable)

```yaml
"id: robot_overtaking_01\nname: Overtaking a Pedestrian from Behind\n\nsummary: >\n\
  \  A robot approaches a human pedestrian from behind in a shared pathway\n  where\
  \ both are moving in the same direction. The robot must decide whether\n  to follow\
  \ or overtake in a manner that is safe, legible, and socially\n  comfortable.\n\n\
  context:\n  environment:\n    type: indoor\n    setting: corridor or sidewalk-like\
  \ passage\n    width: moderate\n  social_setting:\n    formality: informal\n   \
  \ crowd_level: low\n\nagents:\n  robot:\n    role: navigating_agent\n    capabilities:\n\
  \      - forward_motion\n      - speed_adjustment\n      - lateral_adjustment\n\
  \      - stopping\n  humans:\n    - role: pedestrian\n      count: 1\n      attributes:\n\
  \        mobility: typical\n        awareness: variable\n\ninitial_conditions:\n\
  \  robot_position: behind_pedestrian\n  relative_speed: robot_faster\n  visibility:\
  \ clear_forward_view\n\nexpected_behaviors:\n  must:\n    - avoid colliding with\
  \ or startling the pedestrian\n    - maintain a safe and respectful distance during\
  \ approach and passing\n  should:\n    - signal overtaking intent through smooth,\
  \ predictable motion\n    - choose a passing side consistent with local social norms\n\
  \    - adjust speed to minimize perceived pressure on the pedestrian\n  should_not:\n\
  \    - follow too closely from behind\n    - pass abruptly or at excessive speed\n\
  \    - force the pedestrian to change path or pace\n\nrelevant_principles:\n  -\
  \ P0  # Goal Achievement\n  - P1  # Safety\n  - P2  # Comfort\n  - P3  # Legibility\n\
  \  - P4  # Politeness\n  \nevaluation_notes: >\n  This scenario evaluates how the\
  \ robot handles an interaction in which it\n  has greater situational control than\
  \ the human. Acceptable behavior may\n  include delaying overtaking when space is\
  \ limited.\n\n  Successful overtaking is characterized by early intent signaling,\n\
  \  sufficient lateral clearance, and minimal disruption to the pedestrian\u2019\
  s\n  motion. Failure modes include tailgating, sudden lateral movements, or\n  passing\
  \ in a way that causes surprise or discomfort.\n\n  Human awareness is assumed to\
  \ be variable; overly assertive behavior is\n  inappropriate even if the pedestrian\
  \ appears unaware of the robot\u2019s presence."
```

---

## Notes for Scenario Designers and Evaluators

- This scenario emphasizes **reactive social compliance** rather than
  assertive navigation.
- The robot is not expected to signal overtaking intent; instead, it should
  avoid behaviors that interfere with the human’s maneuver.
- Variants may include narrow passages, distracted pedestrians, or multiple
  humans overtaking simultaneously.

