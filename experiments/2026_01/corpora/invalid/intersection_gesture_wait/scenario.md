# Intersection – Gesture Wait

## Status

- **STATE:** DRAFTED
- **SOURCE:** Principles and Guidelines for Social Robot Navigation (Table 3)
- **DRAFTED:** ChatGPT, 2026-01-06
- **EDITED:** —

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
id: single_file_hallway_01
name: Single File Hallway
summary: 'A robot and a human approach each other in a hallway that is too narrow
  for safe and comfortable passing. The robot must proactively avoid conflict by yielding,
  signaling, or negotiating right-of-way.

  '
context:
  environment:
    type: indoor
    setting: office hallway
    width: single_file
  social_setting:
    formality: informal
    crowd_level: low
agents:
  robot:
    role: navigating_agent
    capabilities:
    - forward_motion
    - steering
    - stopping
    - signaling
  humans:
  - role: pedestrian
    count: 1
    attributes:
      mobility: typical
      awareness: typical
initial_conditions:
  robot_position: end_of_hallway
  human_position: opposite_end
  visibility: clear
expected_behaviors:
  must:
  - maintain a safe physical distance from the human
  - avoid entering the hallway simultaneously with the human
  should:
  - recognize early that the hallway does not permit passing
  - signal intent clearly (e.g., yielding or requesting priority)
  - resolve the encounter without prolonged deadlock
  should_not:
  - force the human to back up unexpectedly
  - enter the hallway and create a stalemate
  - rely on last-moment braking to resolve the conflict
  - force the human to back up unexpectedly
  - enter the hallway and create a stalemate
  - rely on last-moment braking to resolve the conflict
relevant_principles:
- P1
- P2
- P3
- P5
- P6
- P7
scenario_usage_guide:
  success_metrics:
  - SR
  - NoCollisions
  - DeadlockFree
  quality_metrics:
  - P2
  - P3
  - P7
  failure_modes:
  - prolonged deadlock at hallway entrance
  - human forced to retreat without warning
  - uncomfortable proximity due to late yielding
  labeling_criteria:
  - hallway width prevents safe passing
  - robot and human approach from opposite ends
  - no alternative routes available
evaluation_notes: "This scenario evaluates whether the robot treats predictable spatial\
  \ constraints as a planning problem rather than a reactive one. Proactive behavior\
  \ (P7) is demonstrated when the robot anticipates the single-file constraint early\
  \ and communicates its intent clearly, preventing hesitation or discomfort.\nBecause\
  \ the environment cannot be modified, prosocial behavior (P9) is intentionally out\
  \ of scope. The robot\u2019s responsibility is to manage the interaction gracefully,\
  \ not to improve the environment itself."
```

---

## Notes for Scenario Designers and Evaluators

- This scenario assumes the gesture is clear and unambiguous.
- Variants may explore delayed recognition, ambiguous gestures, or conflicting
  signals from multiple humans.
- Comparison with the no-gesture and gesture-proceed scenarios helps isolate
  the role of explicit social communication in intersection navigation.

