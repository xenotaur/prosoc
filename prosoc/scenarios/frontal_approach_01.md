# Scenario: Frontal Approach

## STATUS: DRAFT 2026-01-02
- SOURCE: Prompt to ChatGPT 5.2
- DRAFTED: ChatGPT 5.2, 2026-01-02
- EDITED: Anthony Francis centaur@logicalrobotics.com, 2026-01-05

## Overview

This scenario describes a canonical social navigation conflict in which a robot and a human approach each other in opposite directions in a narrow hallway where neither agent has an explicit right-of-way. Successful navigation depends on sensing and agile navigation, and successful social navigation may require trajectory prediction, interpreting intent, resolving hesitation, and resolving conflicts. The scenario tests social navigation principles including safety, comfort, legibility, following social norms, and agent understanding.

---

```yaml
id: frontal_approach_01
name:  Frontal Approach

summary: >
  A robot and a human approach each other in opposite directions in a narrow hallway and pass each other safely, comfortably, and without
  prolonged hesitation.

context:
  environment:
    type: indoor
    setting: office hallway
    width: narrow
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
    - maintain a safe physical distance
    - avoid physical contact or forcing evasive action
  should:
    - signal intent clearly through motion or positioning
    - resolve hesitation without prolonged deadlock
    - yield if appropriate given the spatial configuration
  should_not:
    - force the human to stop abruptly
    - invade personal space
    - advance aggressively in a way that causes discomfort

relevant_principles:
  - P1  # Safety
  - P2  # Comfort
  - P3  # Legibility
  - P5  # Social Competency
  - P6  # Agent Understanding


 evaluation_notes: >
  This scenario evaluates how well the robot navigates through shared space with a human in the conditions for a mild and typiocal conflict.
  Changing direction, slowing down, braking or hesitation may be acceptable if they increase safety, comfort, or legibility, but  prolonged deadlock, abrupt reversals,
  or aggressive advancement are indicative of poor performance.

  The scenario assumes a pedestrian with a typical level of awareness,
  neither oblivious to the presence of the robot nor overly attettentive too it.

```

---

## Discussion

This scenario is intended as a **baseline social navigation test case** and may be extended through variants that modify hallway width, human attentiveness, group size, or cultural expectations around yielding. The goal is not to prescribe a single correct behavior, but to evaluate whether the robot behaves as a cooperative, legible participant in shared space, consistent with the Prosocial Navigation Charter.

