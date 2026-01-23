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
id: pedestrian_overtaking_01
name: Pedestrian Overtaking a Robot from Behind
summary: 'A human pedestrian approaches and overtakes a slower-moving robot from behind
  in a shared pathway. The robot must behave predictably and cooperatively, allowing
  safe and comfortable passing without impeding the pedestrian.

  '
context:
  environment:
    type: indoor
    setting: corridor or sidewalk-like passage
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
    - lateral_adjustment
    - stopping
  humans:
  - role: pedestrian
    count: 1
    attributes:
      mobility: typical
      awareness: attentive
initial_conditions:
  robot_position: ahead_of_pedestrian
  relative_speed: pedestrian_faster
  visibility: pedestrian_clear_view
expected_behaviors:
  must:
  - "avoid impeding the pedestrian\u2019s overtaking maneuver"
  - maintain a predictable trajectory during passing
  should:
  - yield lateral space when feasible
  - avoid sudden speed or direction changes
  - maintain steady motion to reduce uncertainty
  should_not:
  - accelerate to block overtaking
  - drift unpredictably during passing
  - force the pedestrian to slow or change path
relevant_principles:
- P0
- P1
- P2
- P3
- P4
- P9
evaluation_notes: "This scenario evaluates the robot\u2019s ability to act as a cooperative\
  \ and predictable participant when being overtaken by a human. Successful behavior\
  \ minimizes the cognitive and physical burden on the pedestrian and allows passing\
  \ to occur smoothly.\nFailure modes include blocking behavior, sudden motion changes,\
  \ or trajectories that require the pedestrian to hesitate or reroute."
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

