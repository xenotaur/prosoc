# Scenario: Single File Hallway

## STATUS: DRAFT 2026-01-16
- SOURCE: Principles and Guidelines for Evaluating Social Robot Navigation (P&G paper)
- DRAFTED: ChatGPT 5.2, 2026-01-16
- EDITED: Anthony Francis centaur@logicalrobotics.com (pending)

## Overview

This scenario describes a social navigation conflict in which a robot and a human approach each other in a hallway that is **too narrow for safe and comfortable passing**. Unlike *Frontal Approach* and *Movable Obstruction*, the environment itself cannot be improved by intervention: the hallway geometry enforces **single‑file passage**.

The purpose of this scenario is to isolate and evaluate **Proactivity (P7)** without introducing opportunities for **Prosocial Behavior (P9)**. The robot must anticipate the conflict and take initiative—through signaling, yielding, or negotiation—to prevent deadlock or discomfort.

---

```yaml
"id: pedestrian_overtaking_01\nname: Pedestrian Overtaking a Robot from Behind\n\n\
  summary: >\n  A human pedestrian approaches and overtakes a slower-moving robot\
  \ from\n  behind in a shared pathway. The robot must behave predictably and\n  cooperatively,\
  \ allowing safe and comfortable passing without impeding\n  the pedestrian.\n\n\
  context:\n  environment:\n    type: indoor\n    setting: corridor or sidewalk-like\
  \ passage\n    width: moderate\n  social_setting:\n    formality: informal\n   \
  \ crowd_level: low\n\nagents:\n  robot:\n    role: navigating_agent\n    capabilities:\n\
  \      - forward_motion\n      - speed_adjustment\n      - lateral_adjustment\n\
  \      - stopping\n  humans:\n    - role: pedestrian\n      count: 1\n      attributes:\n\
  \        mobility: typical\n        awareness: attentive\n\ninitial_conditions:\n\
  \  robot_position: ahead_of_pedestrian\n  relative_speed: pedestrian_faster\n  visibility:\
  \ pedestrian_clear_view\n\nexpected_behaviors:\n  must:\n    - avoid impeding the\
  \ pedestrian\u2019s overtaking maneuver\n    - maintain a predictable trajectory\
  \ during passing\n  should:\n    - yield lateral space when feasible\n    - avoid\
  \ sudden speed or direction changes\n    - maintain steady motion to reduce uncertainty\n\
  \  should_not:\n    - accelerate to block overtaking\n    - drift unpredictably\
  \ during passing\n    - force the pedestrian to slow or change path\n\nrelevant_principles:\n\
  \  - P0  # Goal Achievement\n  - P1  # Safety\n  - P2  # Comfort\n  - P3  # Legibility\n\
  \  - P4  # Politeness\n  - P9  # Prosocial Behavior\n\nevaluation_notes: >\n  This\
  \ scenario evaluates the robot\u2019s ability to act as a cooperative and\n  predictable\
  \ participant when being overtaken by a human. Successful\n  behavior minimizes\
  \ the cognitive and physical burden on the pedestrian\n  and allows passing to occur\
  \ smoothly.\n\n  Failure modes include blocking behavior, sudden motion changes,\
  \ or\n  trajectories that require the pedestrian to hesitate or reroute."
```

---

## Discussion

The **SINGLE_FILE_HALLWAY** scenario serves as a **clean control case** for proactivity in social
navigation. In contrast to *Movable Obstruction*, there is no opportunity for environmental
stewardship or third‑party benefit—only the opportunity to **prevent conflict before it occurs**.

Together, *Frontal Approach*, *Single File Hallway*, and *Movable Obstruction* form a minimal
scenario set that:

- Progressively constrains the environment
- Cleanly separates P7 (Proactivity) from P9 (Prosocial Behavior)
- Supports comparative evaluation across identical agent configurations

This scenario is especially useful for benchmarking hesitation handling, signaling clarity, and
right‑of‑way negotiation under unavoidable spatial constraints.

