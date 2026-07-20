# Scenario: Pedestrian Overtaking a Robot from Behind

## Status

- **STATE:** DRAFT
- **SOURCE:** Prompt to ChatGPT 5.2
- **DRAFTED:** ChatGPT 5.2, 2026-01-02
- **EDITED:** render_sections.py, 2026-07-19

## Scenario Card Summary

- **Scenario Name:** Pedestrian Overtaking a Robot from Behind
- **Scenario Description:** A human pedestrian approaches and overtakes a slower-moving robot from behind in a shared pathway. The robot must behave predictably and cooperatively, allowing safe and comfortable passing without impeding the pedestrian.
- **Physical Environment:** indoor
- **Robot Role:** navigating_agent

**Remaining gaps:**

- **Scientific Purpose** — should-fill-in-now
- **Geometric Layout** — should-fill-in-now
- **Robot Task** — should-fill-in-now
- **Human Behavior** — should-fill-in-now
- **Success Metrics** — should-fill-in-now
- **Quality Metrics** — should-fill-in-now
- **Ideal Outcome** — should-fill-in-now
- **Related Scenarios** — should-fill-in-now
- **Cited In** — should-fill-in-now

---

## Scenario Overview

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
id: pedestrian_overtaking_01
name: Pedestrian Overtaking a Robot from Behind

summary: >
  A human pedestrian approaches and overtakes a slower-moving robot from
  behind in a shared pathway. The robot must behave predictably and
  cooperatively, allowing safe and comfortable passing without impeding
  the pedestrian.

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
        awareness: attentive

initial_conditions:
  robot_position: ahead_of_pedestrian
  relative_speed: pedestrian_faster
  visibility: pedestrian_clear_view

expected_behaviors:
  must:
    - avoid impeding the pedestrian’s overtaking maneuver
    - maintain a predictable trajectory during passing
  should:
    - yield lateral space when feasible
    - avoid sudden speed or direction changes
    - maintain steady motion to reduce uncertainty
  should_not:
    - accelerate to block overtaking
    - drift unpredictably during passing
    - force the pedestrian to slow or change path

relevant_principles:
  - P0  # Goal Achievement
  - P1  # Safety
  - P2  # Comfort
  - P3  # Legibility
  - P4  # Politeness
  - P9  # Prosocial Behavior

evaluation_notes: >
  This scenario evaluates the robot’s ability to act as a cooperative and
  predictable participant when being overtaken by a human. Successful
  behavior minimizes the cognitive and physical burden on the pedestrian
  and allows passing to occur smoothly.

  Failure modes include blocking behavior, sudden motion changes, or
  trajectories that require the pedestrian to hesitate or reroute.
```

---

## Scenario Usage Guide

**Remaining gaps:**

- **Success Metrics** — should-fill-in-now
- **Quality Metrics** — should-fill-in-now
- **Ideal Outcome** — should-fill-in-now
- **Failure Modes** — should-fill-in-now
- **Labeling Criteria** — should-fill-in-now

---

## Notes for Scenario Designers and Evaluators

- This scenario emphasizes **reactive social compliance** rather than
  assertive navigation.
- The robot is not expected to signal overtaking intent; instead, it should
  avoid behaviors that interfere with the human’s maneuver.
- Variants may include narrow passages, distracted pedestrians, or multiple
  humans overtaking simultaneously.

