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
id: robot_overtaking_01
name: Overtaking a Pedestrian from Behind
summary: 'A robot approaches a human pedestrian from behind in a shared pathway where
  both are moving in the same direction. The robot must decide whether to follow or
  overtake in a manner that is safe, legible, and socially comfortable.

  '
context:
  environment:
    type: indoor
    setting: corridor or sidewalk-like passage
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
    - lateral_adjustment
    - stopping
  humans:
  - role: pedestrian
    count: 1
    attributes:
      mobility: typical
      awareness: variable
initial_conditions:
  robot_position: behind_pedestrian
  relative_speed: robot_faster
  visibility: clear_forward_view
expected_behaviors:
  must:
  - avoid colliding with or startling the pedestrian
  - maintain a safe and respectful distance during approach and passing
  should:
  - signal overtaking intent through smooth, predictable motion
  - choose a passing side consistent with local social norms
  - adjust speed to minimize perceived pressure on the pedestrian
  should_not:
  - follow too closely from behind
  - pass abruptly or at excessive speed
  - force the pedestrian to change path or pace
relevant_principles:
- P0
- P1
- P2
- P3
- P4
evaluation_notes: "This scenario evaluates how the robot handles an interaction in\
  \ which it has greater situational control than the human. Acceptable behavior may\
  \ include delaying overtaking when space is limited.\nSuccessful overtaking is characterized\
  \ by early intent signaling, sufficient lateral clearance, and minimal disruption\
  \ to the pedestrian\u2019s motion. Failure modes include tailgating, sudden lateral\
  \ movements, or passing in a way that causes surprise or discomfort.\nHuman awareness\
  \ is assumed to be variable; overly assertive behavior is inappropriate even if\
  \ the pedestrian appears unaware of the robot\u2019s presence."
```

---

## Notes for Scenario Designers and Evaluators

- This scenario emphasizes **reactive social compliance** rather than
  assertive navigation.
- The robot is not expected to signal overtaking intent; instead, it should
  avoid behaviors that interfere with the human’s maneuver.
- Variants may include narrow passages, distracted pedestrians, or multiple
  humans overtaking simultaneously.

