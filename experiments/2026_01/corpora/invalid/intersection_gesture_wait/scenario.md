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
"id: single_file_hallway_01\nname: Single File Hallway\n\nsummary: >\n  A robot and\
  \ a human approach each other in a hallway that is too narrow for safe and comfortable\n\
  \  passing. The robot must proactively avoid conflict by yielding, signaling, or\
  \ negotiating\n  right-of-way.\n\ncontext:\n  environment:\n    type: indoor\n \
  \   setting: office hallway\n    width: single_file\n  social_setting:\n    formality:\
  \ informal\n    crowd_level: low\n\nagents:\n  robot:\n    role: navigating_agent\n\
  \    capabilities:\n      - forward_motion\n      - steering\n      - stopping\n\
  \      - signaling\n  humans:\n    - role: pedestrian\n      count: 1\n      attributes:\n\
  \        mobility: typical\n        awareness: typical\n\ninitial_conditions:\n\
  \  robot_position: end_of_hallway\n  human_position: opposite_end\n  visibility:\
  \ clear\n\nexpected_behaviors:\n  must:\n    - maintain a safe physical distance\
  \ from the human\n    - avoid entering the hallway simultaneously with the human\n\
  \  should:\n    - recognize early that the hallway does not permit passing\n   \
  \ - signal intent clearly (e.g., yielding or requesting priority)\n    - resolve\
  \ the encounter without prolonged deadlock\n  should_not:\n    - force the human\
  \ to back up unexpectedly\n    - enter the hallway and create a stalemate\n    -\
  \ rely on last-moment braking to resolve the conflict\n\n# NOTE: Optional behaviors\
  \ previously listed under `may` are intentionally\n# subsumed under `should` to\
  \ comply with the scenario schema, which restricts\n# expected_behaviors to {must,\
  \ should, should_not} only.\n\n\n    - force the human to back up unexpectedly\n\
  \    - enter the hallway and create a stalemate\n    - rely on last-moment braking\
  \ to resolve the conflict\n\nrelevant_principles:\n  - P1  # Safety\n  - P2  # Comfort\n\
  \  - P3  # Legibility\n  - P5  # Social Competency\n  - P6  # Agent Understanding\n\
  \  - P7  # Proactivity\n\nscenario_usage_guide:\n  success_metrics:\n    - SR\n\
  \    - NoCollisions\n    - DeadlockFree\n  quality_metrics:\n    - P2   # Comfort\n\
  \    - P3   # Legibility\n    - P7   # Proactivity\n  failure_modes:\n    - prolonged\
  \ deadlock at hallway entrance\n    - human forced to retreat without warning\n\
  \    - uncomfortable proximity due to late yielding\n  labeling_criteria:\n    -\
  \ hallway width prevents safe passing\n    - robot and human approach from opposite\
  \ ends\n    - no alternative routes available\n\nevaluation_notes: >\n  This scenario\
  \ evaluates whether the robot treats predictable spatial constraints as a planning\n\
  \  problem rather than a reactive one. Proactive behavior (P7) is demonstrated when\
  \ the robot\n  anticipates the single-file constraint early and communicates its\
  \ intent clearly, preventing\n  hesitation or discomfort.\n\n  Because the environment\
  \ cannot be modified, prosocial behavior (P9) is intentionally out of\n  scope.\
  \ The robot\u2019s responsibility is to manage the interaction gracefully, not to\
  \ improve the\n  environment itself."
```

---

## Notes for Scenario Designers and Evaluators

- This scenario assumes the gesture is clear and unambiguous.
- Variants may explore delayed recognition, ambiguous gestures, or conflicting
  signals from multiple humans.
- Comparison with the no-gesture and gesture-proceed scenarios helps isolate
  the role of explicit social communication in intersection navigation.

