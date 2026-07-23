# Scenario: Overtaking a Pedestrian from Behind

## Status

- **STATE:** DRAFTED
- **SOURCE:** Prompt to ChatGPT 5.2
- **DRAFTED:** ChatGPT 5.2, 2026-01-02
- **EDITED:** render_sections.py, 2026-07-19

## Scenario Card Summary

- **Scenario Name:** Overtaking a Pedestrian from Behind
- **Scenario Description:** A robot approaches a human pedestrian from behind in a shared pathway where both are moving in the same direction. The robot must decide whether to follow or overtake in a manner that is safe, legible, and socially comfortable.
- **Scientific Purpose:** pedestrian interaction
- **Physical Environment:** indoor
- **Geometric Layout:** passable space
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from A to B
- **Human Behavior:** navigate from A to B, slower than the robot
- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P2
  - P3
  - P4
- **Ideal Outcome:** robot passes the human safely, comfortably, and without disruption
- **Related Scenarios:** pedestrian_overtaking
- **Cited In:** 50, 157

---

## Scenario Overview

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

Unacceptable behavior includes tailgating, abrupt lateral motion, accelerating aggressively to pass, or forcing the pedestrian to change path or pace to accommodate the robot.

## Scenario Specification (Machine-Readable)

```yaml
id: robot_overtaking_01
name: Overtaking a Pedestrian from Behind

summary: >
  A robot approaches a human pedestrian from behind in a shared pathway
  where both are moving in the same direction. The robot must decide whether
  to follow or overtake in a manner that is safe, legible, and socially
  comfortable.

scientific_purpose: pedestrian interaction

geometric_layout: passable space

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

intended_robot_task: navigate from A to B

intended_human_behavior: navigate from A to B, slower than the robot

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
    - pass abruptly / with sudden lateral motion
    - accelerate excessively when passing
    - force the pedestrian to change path or pace

relevant_principles:
  - P0  # Goal Achievement
  - P1  # Safety
  - P2  # Comfort
  - P3  # Legibility
  - P4  # Politeness

ideal_outcome: robot passes the human safely, comfortably, and without disruption

related_scenarios:
  - pedestrian_overtaking

cited_in:
  - "50"
  - "157"

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
  quality_metrics:
    - P2   # Comfort
    - P3   # Legibility
    - P4   # Politeness
  failure_modes:
    - robot tailgates the pedestrian for a prolonged period before passing
    - robot makes sudden lateral movements while passing
    - robot passes in a way that startles or discomforts the pedestrian
  labeling_criteria:
    - robot approaches a human pedestrian from behind in a shared pathway
    - robot and human are moving in the same direction
    - robot's speed exceeds the pedestrian's speed

evaluation_notes: >
  This scenario evaluates how the robot handles an interaction in which it
  has greater situational control than the human. Acceptable behavior may
  include delaying overtaking when space is limited.

  Successful overtaking is characterized by early intent signaling,
  sufficient lateral clearance, and minimal disruption to the pedestrian’s
  motion. Failure modes include tailgating, sudden lateral movements, or
  passing in a way that causes surprise or discomfort.

  Human awareness is assumed to be variable; overly assertive behavior is
  inappropriate even if the pedestrian appears unaware of the robot’s presence.

  Related Scenarios note: P&G Table 3 lists no related scenario for this
  entry. `related_scenarios` adds pedestrian_overtaking, this scenario's
  role-reversed counterpart, which is expected — Table 3's silence isn't a
  claim that no relationship exists (see the related_scenarios convention
  in prosoc-scenario-audit's audit_checklist.md).
```

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P2
  - P3
  - P4
- **Ideal Outcome:** robot passes the human safely, comfortably, and without disruption
- **Failure Modes:**
  - robot tailgates the pedestrian for a prolonged period before passing
  - robot makes sudden lateral movements while passing
  - robot passes in a way that startles or discomforts the pedestrian
- **Labeling Criteria:**
  - robot approaches a human pedestrian from behind in a shared pathway
  - robot and human are moving in the same direction
  - robot's speed exceeds the pedestrian's speed

---

## Notes for Scenario Designers and Evaluators

- This scenario is intentionally **underspecified** with respect to exact distances and speeds, allowing evaluators to adapt it across platforms and cultures.
- The robot is not required to overtake; choosing to follow temporarily can be socially preferable.
- This scenario pairs naturally with frontal approach scenarios, group overtaking variants, narrow-passage constraints, and distracted pedestrian variants.

