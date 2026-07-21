# Scenario: Leading

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [50]
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** render_sections.py, 2026-07-19

---

## Scenario Card Summary

- **Scenario Name:** Leading
- **Scenario Description:** A robot in a leader role guides a human through a walking space, choosing the path and pace, while the human's task is to follow. The robot must move legibly, match its pace to the human's ability, and monitor whether the human remains present and following.
- **Scientific Purpose:** joint navigation
- **Physical Environment:** generic
- **Geometric Layout:** walking space
- **Robot Role:** leader
- **Robot Task:** lead the human to a destination
- **Human Behavior:** follow the robot, tracking its path and pace
- **Success Metrics:**
  - SR
  - NoCollisions
  - TTG
- **Quality Metrics:**
  - P3
  - P6
- **Ideal Outcome:** person follows the robot to the destination, with the robot adapting pace and signaling turns so the human stays with it
- **Related Scenarios:** following
- **Cited In:** 50

---

## Scenario Overview

This scenario describes a robot in a **leader role** whose task is to guide a human through a walking space, with the human's behavior being to follow the robot. This is the role-reversed counterpart of Following: here the robot chooses the path and pace, and the human's task is to keep up and stay oriented toward the robot's guidance.

The defining challenge is **legible leadership**: since the robot is now the one determining the route, it must move in a way the human can easily track and anticipate, checking that the human is still following rather than assuming compliance, and adjusting pace to the human's demonstrated capability.

Successful navigation requires the robot to choose a reasonable pace, provide enough separation for the human to see and track its motion, slow or pause when the human falls behind or hesitates at a junction, and communicate upcoming turns early enough for a smooth followership.

---

## Social Navigation Context

Leading a human is common in guide-robot and tour-robot use cases (e.g., museum tour guides, airport wayfinding robots, or guide robots for the visually impaired). Unlike Following, where the robot infers the human's intent, in Leading the robot must proactively communicate its own intent so the human can predict and follow it.

Key challenges:

- **Pace matching**: the robot must choose a pace the human can sustain, and adapt if the human falls behind.
- **Turn signaling**: the robot should indicate upcoming turns (via trajectory curvature, deceleration, or explicit signaling) early enough for a human to follow smoothly.
- **Monitoring the human**: unlike a robot navigating alone, a leading robot must periodically confirm the human is still present and following, especially at turns or in crowds.
- **Recovering from separation**: if the human falls behind or is blocked, the robot should pause or backtrack rather than proceeding obliviously.

This scenario is scientifically interesting because it tests proactive, other-aware navigation: the robot must accept responsibility for maintaining the joint navigation relationship rather than simply reaching its own goal.

---

## Normative Expectations

Acceptable robot behavior includes:

- Choosing a pace appropriate to the human's demonstrated walking speed
- Signaling upcoming turns clearly and with enough lead time for the human to follow
- Periodically checking (implicitly or explicitly) that the human is still following
- Slowing or pausing if the human falls behind, is blocked, or hesitates

Unacceptable behavior includes:

- Proceeding at a fixed pace regardless of whether the human is keeping up
- Turning sharply or suddenly without providing the human time to react
- Continuing to a destination while unaware the human has been separated (e.g., by a crowd or obstacle)
- Moving so slowly or hesitantly that the human is uncertain whether the robot is actually leading

---

## Scenario Specification (Machine-Readable)

```yaml
id: leading_01
name: Leading

summary: >
  A robot in a leader role guides a human through a walking space, choosing
  the path and pace, while the human's task is to follow. The robot must
  move legibly, match its pace to the human's ability, and monitor whether
  the human remains present and following.

scientific_purpose: joint navigation

geometric_layout: walking space

context:
  environment:
    type: generic
    setting: indoor or outdoor pedestrian walking space
    width: moderate
  social_setting:
    formality: informal
    crowd_level: low

agents:
  robot:
    role: leader
    capabilities:
      - forward_motion
      - steering
      - stopping
      - speed_adjustment
      - human_tracking
      - gesture_or_signal_output
  humans:
    - role: follower
      count: 1
      attributes:
        mobility: typical
        awareness: typical

initial_conditions:
  robot_position: ahead of the human, at the start of the route
  human_position: behind the robot, ready to follow

intended_robot_task: lead the human to a destination

intended_human_behavior: follow the robot, tracking its path and pace

expected_behaviors:
  must:
    - avoid collision with the human, other pedestrians, and obstacles
    - not proceed to the destination while unaware the human has been separated
  should:
    - choose a pace appropriate to the human's demonstrated walking speed
    - signal upcoming turns with enough lead time for the human to follow
    - pause or slow when the human falls behind, hesitates, or is blocked
    - periodically confirm the human is still following
  should_not:
    - move at a fixed pace regardless of whether the human keeps up
    - turn sharply or suddenly without warning
    - continue navigating obliviously after losing track of the human

relevant_principles:
  - P1  # Safety — collision risk with the human, bystanders, and obstacles
  - P3  # Legibility — robot must clearly signal its route and turns
  - P6  # Agent Understanding — monitoring whether the human is keeping up
  - P8  # Contextual Appropriateness — pace and turn timing should adapt to the human's demonstrated capability

ideal_outcome: person follows the robot to the destination, with the robot adapting pace and signaling turns so the human stays with it

related_scenarios:
  - following

cited_in:
  - "50"

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
    - TTG
  quality_metrics:
    - P3  # Legibility
    - P6  # Agent Understanding
  failure_modes:
    - robot loses the human without noticing and continues to the destination alone
    - robot's pace is mismatched to the human's ability, causing separation
    - robot turns without adequate warning, confusing the human
    - human is uncertain whether the robot is actually leading (ambiguous role signaling)
  labeling_criteria:
    - robot is in a leader role relative to a single following human
    - the robot's path determines the intended route, and the human's task is to track it
    - the robot has some means of monitoring the human's continued presence

evaluation_notes: >
  This scenario should be evaluated over a sustained trajectory, sampling
  multiple turns and at least one pace-mismatch or hesitation event within
  a single episode, rather than a single conflict point.

  Evaluators should distinguish a robot that proactively monitors and adapts
  to the human (checking for separation, adjusting pace) from one that
  merely executes a fixed route irrespective of the human's state — the
  latter should be scored as a failure even if the human happens to keep up.

  This scenario is related to Tour Guide (a specialized, extended variant
  not separately defined in Table 3) and is the role-reversed counterpart
  of Following, where the human leads and the robot tracks them instead.
```

---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
  - TTG
- **Quality Metrics:**
  - P3
  - P6
- **Ideal Outcome:** person follows the robot to the destination, with the robot adapting pace and signaling turns so the human stays with it
- **Failure Modes:**
  - robot loses the human without noticing and continues to the destination alone
  - robot's pace is mismatched to the human's ability, causing separation
  - robot turns without adequate warning, confusing the human
  - human is uncertain whether the robot is actually leading (ambiguous role signaling)
- **Labeling Criteria:**
  - robot is in a leader role relative to a single following human
  - the robot's path determines the intended route, and the human's task is to track it
  - the robot has some means of monitoring the human's continued presence

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Following*: the role-reversed counterpart, where the human leads and the robot follows.
- *Tour Guide*: an extended, task-specific variant of Leading (e.g., museum or facility tours) with additional narration or stopping-point requirements, not separately specified in Table 3.

**Suggested variants:**
- Leading through a crowded space, testing the robot's ability to detect separation from the human
- Human intentionally lagging or stopping, testing the robot's monitoring and pause behavior
- Multi-turn route requiring several legible turn signals in sequence

**Key measurement question:** Does the robot actively monitor whether the human is still following and adapt accordingly, or does it execute a fixed route without regard to the human's actual state?
