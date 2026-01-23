# Scenario: Frontal Approach

## STATUS: DRAFT 2026-01-05
- SOURCE: Prompt to ChatGPT 5.2
- DRAFTED: ChatGPT 5.2, 2026-01-02
- EDITED: Anthony Francis centaur@logicalrobotics.com, 2026-01-05

## Overview

This scenario describes a canonical social navigation conflict in which a robot and a human approach each other in opposite directions in a narrow hallway where neither agent has an explicit right-of-way. Successful navigation depends on sensing and agile navigation, and successful social navigation may require trajectory prediction, interpreting intent, resolving hesitation, and resolving conflicts. The scenario tests social navigation principles including safety, comfort, legibility, following social norms, and agent understanding.

---

```yaml
id: intersection_no_gesture_01
name: "Intersection \u2013 No Gesture"
summary: 'A robot and a human pedestrian approach and cross an indoor intersection
  without any explicit gestural communication. The robot must coordinate passage safely
  and legibly using motion cues and social norms alone.

  '
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
expected_behaviors:
  must:
  - avoid collision with the human at the intersection
  - behave conservatively when right-of-way is ambiguous
  should:
  - slow slightly when approaching the intersection
  - "yield if the human\u2019s intent appears dominant"
  - commit clearly once a crossing decision is made
  should_not:
  - aggressively assert right-of-way
  - oscillate indecisively at the intersection
  - force the human to stop abruptly
relevant_principles:
- P0
- P1
- P2
- P3
- P4
evaluation_notes: "This scenario evaluates the robot\u2019s ability to navigate an\
  \ intersection using implicit coordination cues only. Successful behavior allows\
  \ both agents to pass smoothly without collision or hesitation.\nCommon failure\
  \ modes include overly aggressive entry, excessive hesitation, or late yielding\
  \ that disrupts the human\u2019s motion."
```

---

## Discussion

This scenario is intended as a **baseline social navigation test case** and may be extended through variants that modify hallway width, human attentiveness, group size, or cultural expectations around yielding. The goal is not to prescribe a single correct behavior, but to evaluate whether the robot behaves as a cooperative, legible participant in shared space, consistent with the Prosocial Navigation Charter.

