# Scenario: Frontal Approach

## STATUS: DRAFT 2026-01-05
- SOURCE: Prompt to ChatGPT 5.2
- DRAFTED: ChatGPT 5.2, 2026-01-02
- EDITED: Anthony Francis centaur@logicalrobotics.com, 2026-01-05

## Overview

This scenario describes a canonical social navigation conflict in which a robot and a human approach each other in opposite directions in a narrow hallway where neither agent has an explicit right-of-way. Successful navigation depends on sensing and agile navigation, and successful social navigation may require trajectory prediction, interpreting intent, resolving hesitation, and resolving conflicts. The scenario tests social navigation principles including safety, comfort, legibility, following social norms, and agent understanding.

---

```yaml
"id: intersection_no_gesture_01\nname: Intersection \u2013 No Gesture\n\nsummary:\
  \ >\n  A robot and a human pedestrian approach and cross an indoor intersection\n\
  \  without any explicit gestural communication. The robot must coordinate\n  passage\
  \ safely and legibly using motion cues and social norms alone.\n\ncontext:\n  environment:\n\
  \    type: indoor\n    setting: hallway intersection\n    width: moderate\n  social_setting:\n\
  \    formality: informal\n    crowd_level: low\n\nagents:\n  robot:\n    role: navigating_agent\n\
  \    capabilities:\n      - forward_motion\n      - speed_adjustment\n      - stopping\n\
  \      - path_commitment\n  humans:\n    - role: pedestrian\n      count: 1\n  \
  \    attributes:\n        mobility: typical\n        gesturing: none\n\ninitial_conditions:\n\
  \  approach_pattern: orthogonal\n  arrival_timing: near_simultaneous\n  visibility:\
  \ mutual\n\nexpected_behaviors:\n  must:\n    - avoid collision with the human at\
  \ the intersection\n    - behave conservatively when right-of-way is ambiguous\n\
  \  should:\n    - slow slightly when approaching the intersection\n    - yield if\
  \ the human\u2019s intent appears dominant\n    - commit clearly once a crossing\
  \ decision is made\n  should_not:\n    - aggressively assert right-of-way\n    -\
  \ oscillate indecisively at the intersection\n    - force the human to stop abruptly\n\
  \nrelevant_principles:\n  - P0  # Goal Achievement\n  - P1  # Safety\n  - P2  #\
  \ Comfort\n  - P3  # Legibility\n  - P4  # Politeness\n\n\nevaluation_notes: >\n\
  \  This scenario evaluates the robot\u2019s ability to navigate an intersection\n\
  \  using implicit coordination cues only. Successful behavior allows both\n  agents\
  \ to pass smoothly without collision or hesitation.\n\n  Common failure modes include\
  \ overly aggressive entry, excessive hesitation,\n  or late yielding that disrupts\
  \ the human\u2019s motion."
```

---

## Discussion

This scenario is intended as a **baseline social navigation test case** and may be extended through variants that modify hallway width, human attentiveness, group size, or cultural expectations around yielding. The goal is not to prescribe a single correct behavior, but to evaluate whether the robot behaves as a cooperative, legible participant in shared space, consistent with the Prosocial Navigation Charter.

