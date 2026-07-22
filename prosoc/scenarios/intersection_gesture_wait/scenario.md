# Intersection – Gesture Wait

## Status

- **STATE:** DRAFTED
- **SOURCE:** Principles and Guidelines for Social Robot Navigation (Table 3)
- **DRAFTED:** ChatGPT, 2026-01-06
- **EDITED:** render_sections.py, 2026-07-20

---

## Scenario Card Summary

- **Scenario Name:** Intersection – Gesture Wait
- **Scenario Description:** A robot and a human pedestrian approach an indoor intersection. The human explicitly gestures for the robot to wait. The robot must recognize and comply with the gesture, yielding the intersection safely and legibly.
- **Scientific Purpose:** pedestrian interaction
- **Physical Environment:** indoor
- **Geometric Layout:** intersection
- **Robot Role:** servant
- **Robot Task:** navigate from A to B
- **Human Behavior:** cross navigate (gesture wait)
- **Ideal Outcome:** human gestures the robot to wait; human crosses first, then robot proceeds without collision
- **Related Scenarios:** intersection_gesture_proceed, intersection_no_gesture
- **Cited In:** 126

**Remaining gaps:**

- **Success Metrics** — should-fill-in-now
- **Quality Metrics** — should-fill-in-now

---

## Scenario Overview

This scenario describes an **intersection crossing interaction** in which a robot and a human pedestrian approach an indoor intersection, and the **human explicitly gestures for the robot to wait**.

In this case, the human resolves the ambiguity of right-of-way through a clear social signal. The robot is expected to recognize, interpret, and comply with the gesture in a manner that is safe, legible, and socially appropriate.

The scenario evaluates whether the robot can **defer appropriately to explicit human intent**, prioritizing safety, comfort, and social compliance over immediate goal progress.

---

## Social Navigation Context

In human–human navigation, gestures such as a raised hand, a stopping motion, or a brief wave are commonly used to coordinate passage at intersections. When such a gesture is given, the recipient is expected to acknowledge and comply, unless doing so would create safety risks.

For robots operating in shared human environments, explicit gestures provide valuable disambiguation. Failure to respond appropriately can erode trust, cause confusion, or lead to unsafe interactions.

This scenario corresponds to **“Intersection – Gesture Wait”** cases discussed in the *Principles and Guidelines for Social Robot Navigation* paper, highlighting the importance of responsiveness to clear human social signals.

---

## Normative Expectations

Acceptable robot behavior in this scenario may include:

- recognizing the human’s gesture as a request to wait,
- slowing or stopping before entering the intersection,
- maintaining a stationary and predictable posture while yielding.

Unacceptable behavior includes ignoring the gesture, proceeding into the intersection, or exhibiting ambiguous motion that undermines the clarity of the human’s signal.

---

## Scenario Specification (Machine-Readable)

```yaml
id: intersection_gesture_wait_01
name: Intersection – Gesture Wait

summary: >
  A robot and a human pedestrian approach an indoor intersection. The human
  explicitly gestures for the robot to wait. The robot must recognize and
  comply with the gesture, yielding the intersection safely and legibly.

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
    role: servant
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

intended_robot_task: navigate from A to B

intended_human_behavior: cross navigate (gesture wait)

expected_behaviors:
  must:
    - recognize the human’s gesture requesting the robot to wait
    - stop or slow before entering the intersection
    - avoid entering the intersection until it is clear
  should:
    - acknowledge the gesture through compliant motion
    - remain stationary and predictable while yielding
  should_not:
    - ignore or override the human’s gesture
    - proceed into the intersection prematurely
    - display ambiguous motion while waiting

relevant_principles:
  - P0  # Goal Achievement
  - P1  # Safety
  - P2  # Comfort
  - P3  # Legibility
  - P4  # Politeness

ideal_outcome: human gestures the robot to wait; human crosses first, then robot proceeds without collision

related_scenarios:
  - intersection_gesture_proceed
  - intersection_no_gesture

cited_in:
  - "126"

evaluation_notes: >
  This scenario evaluates the robot’s ability to comply with explicit human
  social signals. Successful behavior prioritizes deference and safety over
  efficiency, reinforcing trust and predictability.

  Failure modes include ignoring the gesture, partial compliance that
  introduces ambiguity, or delayed responses that undermine the signal.

  Related Scenarios note: `related_scenarios` includes P&G Table 3's own
  citation for this scenario (intersection_gesture_proceed, listed as
  "Gesture Proceed") plus intersection_no_gesture, since Table 3's Related
  Scenarios field is a single citation, not an exhaustive list. This is
  expected per the related_scenarios convention (prosoc-scenario-audit's
  audit_checklist.md).
```

---

## Scenario Usage Guide

- **Ideal Outcome:** human gestures the robot to wait; human crosses first, then robot proceeds without collision

**Remaining gaps:**

- **Success Metrics** — should-fill-in-now
- **Quality Metrics** — should-fill-in-now
- **Failure Modes** — should-fill-in-now
- **Labeling Criteria** — should-fill-in-now

---

## Notes for Scenario Designers and Evaluators

- This scenario assumes the gesture is clear and unambiguous.
- Variants may explore delayed recognition, ambiguous gestures, or conflicting
  signals from multiple humans.
- Comparison with the no-gesture and gesture-proceed scenarios helps isolate
  the role of explicit social communication in intersection navigation.

