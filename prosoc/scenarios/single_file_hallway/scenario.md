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
id: single_file_hallway_01
name: Single File Hallway

summary: >
  A robot and a human approach each other in a hallway that is too narrow for safe and comfortable
  passing. The robot must proactively avoid conflict by yielding, signaling, or negotiating
  right-of-way.

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

# NOTE: Optional behaviors previously listed under `may` are intentionally
# subsumed under `should` to comply with the scenario schema, which restricts
# expected_behaviors to {must, should, should_not} only.


    - force the human to back up unexpectedly
    - enter the hallway and create a stalemate
    - rely on last-moment braking to resolve the conflict

relevant_principles:
  - P1  # Safety
  - P2  # Comfort
  - P3  # Legibility
  - P5  # Social Competency
  - P6  # Agent Understanding
  - P7  # Proactivity

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
    - DeadlockFree
  quality_metrics:
    - P2   # Comfort
    - P3   # Legibility
    - P7   # Proactivity
  failure_modes:
    - prolonged deadlock at hallway entrance
    - human forced to retreat without warning
    - uncomfortable proximity due to late yielding
  labeling_criteria:
    - hallway width prevents safe passing
    - robot and human approach from opposite ends
    - no alternative routes available

evaluation_notes: >
  This scenario evaluates whether the robot treats predictable spatial constraints as a planning
  problem rather than a reactive one. Proactive behavior (P7) is demonstrated when the robot
  anticipates the single-file constraint early and communicates its intent clearly, preventing
  hesitation or discomfort.

  Because the environment cannot be modified, prosocial behavior (P9) is intentionally out of
  scope. The robot’s responsibility is to manage the interaction gracefully, not to improve the
  environment itself.

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

