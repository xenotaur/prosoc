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
id: movable_obstruction_01
name: Movable Obstruction
summary: 'A robot and a human approach each other in a hallway that is partially blocked
  by a movable obstruction. The robot must decide whether to yield, wait, remove the
  obstruction, or report it, balancing task goals with prosocial responsibility.

  '
context:
  environment:
    type: indoor
    setting: office hallway
    width: nominal
    obstruction:
      present: true
      movable: true
      blocks_full_passing: true
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
    - manipulation
    - object_movement
  humans:
  - role: pedestrian
    count: 1
    attributes:
      mobility: typical
      awareness: typical
initial_conditions:
  robot_position: end_of_hallway
  human_position: opposite_end
  obstruction_position: center_of_hallway
  visibility: clear
expected_behaviors:
  must:
  - maintain a safe physical distance from the human
  - avoid causing the human to take evasive or unsafe actions
  should:
  - recognize that the obstruction limits comfortable passing
  - communicate intent clearly through motion or signaling
  - select a behavior that resolves or mitigates the obstruction-induced conflict
  - remove the obstruction if physically capable and task-appropriate
  - report the obstruction to facility management when appropriate
  - yield or wait if intervention is inappropriate
  should_not:
  - ignore the obstruction if it predictably causes repeated conflicts
  - force the human into single-file passage without acknowledgment
  - manipulate the obstruction in a way that creates new hazards
relevant_principles:
- P1
- P2
- P3
- P5
- P6
- P7
- P9
scenario_usage_guide:
  success_metrics:
  - SR
  - NoCollisions
  - ConflictResolved
  quality_metrics:
  - P2
  - P7
  - P9
  failure_modes:
  - robot repeatedly yields without addressing obstruction
  - robot causes discomfort by forcing single-file passage
  - robot manipulates obstruction unsafely
  labeling_criteria:
  - obstruction is movable and blocks comfortable passing
  - robot and human approach from opposite directions
  - robot is physically capable of intervention
evaluation_notes: "This scenario evaluates whether a robot treats navigation as a\
  \ shared, community-level problem rather than a purely local motion-planning task.\
  \ Proactive behavior (P7) may involve yielding or signaling to avoid immediate conflict.\
  \ Prosocial behavior (P9) is demonstrated when the robot improves the environment\
  \ itself\u2014by removing or reporting the obstruction\u2014thereby benefiting not\
  \ only the current interaction but future navigators as well.\nAppropriate behavior\
  \ depends on task and context. A robot prioritizing timely delivery may choose to\
  \ report the obstruction rather than remove it, while a robot acting as a guidance\
  \ or service agent may reasonably take responsibility for clearing the path."
```

---

## Notes for Scenario Designers and Evaluators

- This scenario intentionally excludes explicit gestures or signals.
- Variants may include different arrival timings, reduced visibility, or
  multiple humans approaching from different directions.
- Comparison with gesture-based intersection scenarios can help isolate the
  effects of explicit communication versus motion-based coordination.

