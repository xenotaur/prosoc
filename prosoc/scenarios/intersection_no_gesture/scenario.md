# Intersection – No Gesture

## Status

- **STATE:** DRAFTED
- **SOURCE:** Principles and Guidelines for Social Robot Navigation (Table 3)
- **DRAFTED:** ChatGPT, 2026-01-06
- **EDITED:** render_sections.py, 2026-07-20

---

## Scenario Card Summary

- **Scenario Name:** Intersection – No Gesture
- **Scenario Description:** A robot and a human pedestrian approach and cross an indoor intersection without any explicit gestural communication. The robot must coordinate passage safely and legibly using motion cues and social norms alone.
- **Scientific Purpose:** pedestrian interaction
- **Physical Environment:** indoor
- **Geometric Layout:** intersection
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from A to B
- **Human Behavior:** cross navigate
- **Ideal Outcome:** robot and human both cross the intersection without collision, absent any explicit gesture
- **Related Scenarios:** intersection_gesture_proceed, intersection_gesture_wait
- **Cited In:** 27, 50, 167

**Remaining gaps:**

- **Success Metrics** — should-fill-in-now
- **Quality Metrics** — should-fill-in-now

---

## Scenario Overview

This scenario describes an **intersection crossing interaction** in which a robot and a human pedestrian arrive at and traverse an indoor intersection **without any explicit gestural communication** from the human.

Unlike gesture-based intersection scenarios, the human does **not** signal for the robot to proceed or wait. As a result, the robot must rely solely on motion cues, spatial context, and social norms to coordinate safe passage.

The scenario evaluates whether the robot can navigate the intersection in a way that balances **goal achievement** with **prosocial navigation norms**, including safety, legibility, and non-intrusive behavior, under conditions of **implicit coordination**.

---

## Social Navigation Context

Intersections are common sites of social ambiguity in indoor human environments such as office buildings, hospitals, and academic facilities. When two agents approach an intersection without explicit communication, coordination typically emerges through:

- speed modulation,
- subtle yielding or assertive motion,
- mutual anticipation of trajectories.

Humans generally expect other agents—whether people or robots—to behave conservatively and predictably in these situations. Failure to do so can result in hesitation, discomfort, or collision risk.

This scenario corresponds to **“Intersection – No Gesture”** cases discussed in the *Principles and Guidelines for Social Robot Navigation* paper, which emphasize the importance of legibility and safety when explicit social signals are absent.

---

## Normative Expectations

Acceptable robot behavior in this scenario may include:

- approaching the intersection at a moderated speed,
- yielding when right-of-way is ambiguous,
- clearly committing to a trajectory once a decision is made.

Unacceptable behavior includes aggressively asserting right-of-way, oscillating indecisively, or entering the intersection in a way that forces the human to stop abruptly.

---

## Scenario Specification (Machine-Readable)

```yaml
id: intersection_no_gesture_01
name: Intersection – No Gesture

summary: >
  A robot and a human pedestrian approach and cross an indoor intersection
  without any explicit gestural communication. The robot must coordinate
  passage safely and legibly using motion cues and social norms alone.

scientific_purpose: pedestrian interaction

geometric_layout: intersection

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
      - path_commitment
  humans:
    - role: pedestrian
      count: 1
      attributes:
        mobility: typical
        gesturing: none

initial_conditions:
  approach_pattern: orthogonal
  arrival_timing: near_simultaneous
  visibility: mutual

intended_robot_task: navigate from A to B

intended_human_behavior: cross navigate

expected_behaviors:
  must:
    - avoid collision with the human at the intersection
    - behave conservatively when right-of-way is ambiguous
  should:
    - slow slightly when approaching the intersection
    - yield if the human’s intent appears dominant
    - commit clearly once a crossing decision is made
  should_not:
    - aggressively assert right-of-way
    - oscillate indecisively at the intersection
    - force the human to stop abruptly

relevant_principles:
  - P0  # Goal Achievement
  - P1  # Safety
  - P2  # Comfort
  - P3  # Legibility
  - P4  # Politeness

ideal_outcome: robot and human both cross the intersection without collision, absent any explicit gesture

related_scenarios:
  - intersection_gesture_proceed
  - intersection_gesture_wait

cited_in:
  - "27"
  - "50"
  - "167"

evaluation_notes: >
  This scenario evaluates the robot’s ability to navigate an intersection
  using implicit coordination cues only. Successful behavior allows both
  agents to pass smoothly without collision or hesitation.

  Common failure modes include overly aggressive entry, excessive hesitation,
  or late yielding that disrupts the human’s motion.

  Related Scenarios note: P&G Table 3 lists no related scenario for this
  entry. `related_scenarios` adds intersection_gesture_proceed and
  intersection_gesture_wait, this scenario's gesture-based counterparts,
  which is expected — Table 3's silence isn't a claim that no relationship
  exists (see the related_scenarios convention in prosoc-scenario-audit's
  audit_checklist.md).
```

---

## Scenario Usage Guide

- **Ideal Outcome:** robot and human both cross the intersection without collision, absent any explicit gesture

**Remaining gaps:**

- **Success Metrics** — should-fill-in-now
- **Quality Metrics** — should-fill-in-now
- **Failure Modes** — should-fill-in-now
- **Labeling Criteria** — should-fill-in-now

---

## Notes for Scenario Designers and Evaluators

- This scenario intentionally excludes explicit gestures or signals.
- Variants may include different arrival timings, reduced visibility, or
  multiple humans approaching from different directions.
- Comparison with gesture-based intersection scenarios can help isolate the
  effects of explicit communication versus motion-based coordination.

