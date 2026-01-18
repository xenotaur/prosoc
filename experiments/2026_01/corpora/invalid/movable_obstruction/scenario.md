# Scenario: Movable Obstruction

## STATUS: DRAFT 2026-01-16
- SOURCE: Principles and Guidelines for Evaluating Social Robot Navigation (P&G paper)
- DRAFTED: ChatGPT 5.2, 2026-01-16
- EDITED: Anthony Francis centaur@logicalrobotics.com (pending)

## Overview

This scenario describes a social navigation conflict in which a robot and a human approach each other in a hallway that is nominally wide enough for passing, but partially blocked by a **movable obstruction** (e.g., a cart, box, or misplaced furniture). The scenario is designed to distinguish **Proactivity (P7)** from **Prosocial Behavior (P9)** by introducing opportunities for the robot to improve the navigability of the environment, rather than merely adapting to it.

Unlike *Frontal Approach*, successful navigation in this scenario may involve **environmental intervention** (physically moving the obstruction or reporting it), not just motion planning or yielding behavior.

---

```yaml
"id: intersection_gesture_wait_01\nname: Intersection \u2013 Gesture Wait\n\nsummary:\
  \ >\n  A robot and a human pedestrian approach an indoor intersection. The human\n\
  \  explicitly gestures for the robot to wait. The robot must recognize and\n  comply\
  \ with the gesture, yielding the intersection safely and legibly.\n\ncontext:\n\
  \  environment:\n    type: indoor\n    setting: hallway intersection\n    width:\
  \ moderate\n  social_setting:\n    formality: informal\n    crowd_level: low\n\n\
  agents:\n  robot:\n    role: navigating_agent\n    capabilities:\n      - forward_motion\n\
  \      - speed_adjustment\n      - stopping\n      - gesture_recognition\n  humans:\n\
  \    - role: pedestrian\n      count: 1\n      attributes:\n        mobility: typical\n\
  \        gesturing: wait\n\ninitial_conditions:\n  approach_pattern: orthogonal\n\
  \  arrival_timing: near_simultaneous\n  visibility: mutual\n\nexpected_behaviors:\n\
  \  must:\n    - recognize the human\u2019s gesture requesting the robot to wait\n\
  \    - stop or slow before entering the intersection\n    - avoid entering the intersection\
  \ until it is clear\n  should:\n    - acknowledge the gesture through compliant\
  \ motion\n    - remain stationary and predictable while yielding\n  should_not:\n\
  \    - ignore or override the human\u2019s gesture\n    - proceed into the intersection\
  \ prematurely\n    - display ambiguous motion while waiting\n\nrelevant_principles:\n\
  \  - P0  # Goal Achievement\n  - P1  # Safety\n  - P2  # Comfort\n  - P3  # Legibility\n\
  \  - P4  # Politeness\n  - P9  # Prosocial Behavior\n\n\nevaluation_notes: >\n \
  \ This scenario evaluates the robot\u2019s ability to comply with explicit human\n\
  \  social signals. Successful behavior prioritizes deference and safety over\n \
  \ efficiency, reinforcing trust and predictability.\n\n  Failure modes include ignoring\
  \ the gesture, partial compliance that\n  introduces ambiguity, or delayed responses\
  \ that undermine the signal."
```

---

## Discussion

The **MOVABLE_OBSTRUCTION** scenario explicitly extends *Frontal Approach* by introducing a decision point where **environmental improvement** is possible. This enables systematic evaluation of:

- The boundary between **conflict avoidance** (P7) and **environmental stewardship** (P9)
- Trade-offs between **Goal Achievement (P0)** and prosocial action
- The influence of **task** (e.g., NAVIGATE_POINT_TO_POINT vs DELIVER_OBJECT) and **context**
  (ROUTINE_DELIVERY, GUIDANCE_DOCENT, HIGH_URGENCY)

This scenario is intentionally underdetermined: multiple behaviors may be acceptable depending on task weighting and context, but **persistent failure to address a known, movable obstruction** is indicative of poor prosocial performance.

