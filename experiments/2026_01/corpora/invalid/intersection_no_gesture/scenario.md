# Intersection – No Gesture

## Status

- **STATE:** DRAFTED
- **SOURCE:** Principles and Guidelines for Social Robot Navigation (Table 3)
- **DRAFTED:** ChatGPT, 2026-01-06
- **EDITED:** —

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
"id: movable_obstruction_01\nname: Movable Obstruction\n\nsummary: >\n  A robot and\
  \ a human approach each other in a hallway that is partially blocked by a movable\
  \ obstruction.\n  The robot must decide whether to yield, wait, remove the obstruction,\
  \ or report it, balancing task goals\n  with prosocial responsibility.\n\ncontext:\n\
  \  environment:\n    type: indoor\n    setting: office hallway\n    width: nominal\n\
  \    obstruction:\n      present: true\n      movable: true\n      blocks_full_passing:\
  \ true\n  social_setting:\n    formality: informal\n    crowd_level: low\n\nagents:\n\
  \  robot:\n    role: navigating_agent\n    capabilities:\n      - forward_motion\n\
  \      - steering\n      - stopping\n      - manipulation\n      - object_movement\n\
  \  humans:\n    - role: pedestrian\n      count: 1\n      attributes:\n        mobility:\
  \ typical\n        awareness: typical\n\ninitial_conditions:\n  robot_position:\
  \ end_of_hallway\n  human_position: opposite_end\n  obstruction_position: center_of_hallway\n\
  \  visibility: clear\n\nexpected_behaviors:\n  must:\n    - maintain a safe physical\
  \ distance from the human\n    - avoid causing the human to take evasive or unsafe\
  \ actions\n  should:\n    - recognize that the obstruction limits comfortable passing\n\
  \    - communicate intent clearly through motion or signaling\n    - select a behavior\
  \ that resolves or mitigates the obstruction-induced conflict\n    - remove the\
  \ obstruction if physically capable and task-appropriate\n    - report the obstruction\
  \ to facility management when appropriate\n    - yield or wait if intervention is\
  \ inappropriate\n  should_not:\n    - ignore the obstruction if it predictably causes\
  \ repeated conflicts\n    - force the human into single-file passage without acknowledgment\n\
  \    - manipulate the obstruction in a way that creates new hazards\n\nrelevant_principles:\n\
  \  - P1  # Safety\n  - P2  # Comfort\n  - P3  # Legibility\n  - P5  # Social Competency\n\
  \  - P6  # Agent Understanding\n  - P7  # Proactivity\n  - P9  # Prosocial Behavior\n\
  \nscenario_usage_guide:\n  success_metrics:\n    - SR\n    - NoCollisions\n    -\
  \ ConflictResolved\n  quality_metrics:\n    - P2   # Comfort\n    - P7   # Proactivity\n\
  \    - P9   # Prosocial Behavior\n  failure_modes:\n    - robot repeatedly yields\
  \ without addressing obstruction\n    - robot causes discomfort by forcing single-file\
  \ passage\n    - robot manipulates obstruction unsafely\n  labeling_criteria:\n\
  \    - obstruction is movable and blocks comfortable passing\n    - robot and human\
  \ approach from opposite directions\n    - robot is physically capable of intervention\n\
  \nevaluation_notes: >\n  This scenario evaluates whether a robot treats navigation\
  \ as a shared, community-level problem\n  rather than a purely local motion-planning\
  \ task. Proactive behavior (P7) may involve yielding or\n  signaling to avoid immediate\
  \ conflict. Prosocial behavior (P9) is demonstrated when the robot\n  improves the\
  \ environment itself\u2014by removing or reporting the obstruction\u2014thereby\
  \ benefiting\n  not only the current interaction but future navigators as well.\n\
  \n  Appropriate behavior depends on task and context. A robot prioritizing timely\
  \ delivery may choose\n  to report the obstruction rather than remove it, while\
  \ a robot acting as a guidance or service agent\n  may reasonably take responsibility\
  \ for clearing the path."
```

---

## Notes for Scenario Designers and Evaluators

- This scenario intentionally excludes explicit gestures or signals.
- Variants may include different arrival timings, reduced visibility, or
  multiple humans approaching from different directions.
- Comparison with gesture-based intersection scenarios can help isolate the
  effects of explicit communication versus motion-based coordination.

