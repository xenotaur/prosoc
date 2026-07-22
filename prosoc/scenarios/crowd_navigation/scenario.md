# Scenario: Crowd Navigation

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in various
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** render_sections.py, 2026-07-20

---

## Scenario Card Summary

- **Scenario Name:** Crowd Navigation
- **Scenario Description:** A robot navigates through a crowd of people who are milling about with no single dominant trajectory. The robot must continuously replan around many loosely coordinated human movements while making steady progress through the space.
- **Scientific Purpose:** crowd navigation
- **Physical Environment:** generic
- **Geometric Layout:** passable space
- **Robot Role:** navigating_agent
- **Robot Task:** navigate through the crowd to a destination on the far side
- **Human Behavior:** mill about, moving independently without regard to the robot's specific path
- **Success Metrics:**
  - SR
  - NoCollisions
  - TTG
  - PathLength
- **Quality Metrics:**
  - P2
  - P7
- **Ideal Outcome:** robot crosses the crowd without collision or obstruction, making steady progress
- **Related Scenarios:** parallel_traffic, perpendicular_traffic
- **Cited In:** various

---

## Scenario Overview

This scenario describes a robot navigating **through a crowd of people who are milling about** rather than moving with any single, predictable trajectory. Unlike the dyadic pedestrian-interaction scenarios (Frontal Approach, Overtaking, Intersection), Crowd Navigation involves many simultaneous, loosely coordinated human trajectories, and the robot must continuously replan around a dynamic, multi-agent field of motion.

The defining challenge is **many-agent, low-predictability navigation**: individual humans in a milling crowd may pause, change direction, form small clusters, or drift unpredictably, and the robot cannot rely on any single dominant interaction pattern. The robot's task is simply to cross the space, but doing so safely and comfortably requires continuously balancing progress against the shifting positions of many nearby humans.

Successful navigation requires the robot to maintain safe clearance from multiple humans simultaneously, avoid abrupt or erratic path changes that could startle bystanders, and make steady progress toward its goal without becoming stuck or excessively conservative.

---

## Social Navigation Context

Crowds are common in transit hubs, plazas, lobbies, and events. Humans navigating crowds rely on years of implicit practice reading the aggregate flow and micro-adjusting continuously; they rarely stop entirely, instead threading through gaps as they open. A robot that stops entirely at the first close approach, or that takes an overly wide detour around every individual, will appear conspicuously non-human and may itself become an obstacle.

Key challenges:

- **Multi-agent prediction**: several nearby humans may move independently in different directions at once, unlike the single dominant interaction of dyadic scenarios.
- **Local density variation**: crowd density can vary within the same episode (temporary clusters vs. open gaps).
- **Balancing caution and progress**: excessive conservatism (frequent stopping, wide detours) can itself be a failure mode, distinct from collision risk.
- **Comfort at scale**: even without any single collision risk, cumulative close passes with many individuals can create a diffuse sense of crowding or unease.

This scenario is scientifically interesting because it evaluates aggregate, multi-agent social navigation competence, complementing the single-agent focus of most other Table 3 scenarios.

---

## Normative Expectations

Acceptable robot behavior includes:

- Continuously adjusting trajectory in response to the positions and apparent motion of multiple nearby humans
- Threading through gaps in the crowd as they become available, rather than stopping at every close approach
- Maintaining reasonable clearance from individuals without requiring excessive personal space that blocks its own progress
- Making steady, legible progress toward its goal across the crowd

Unacceptable behavior includes:

- Colliding with or forcing evasive action from any individual in the crowd
- Freezing indefinitely or taking excessively wide detours around minor crowd density
- Moving erratically or reversing direction frequently in response to shifting crowd positions
- Ignoring local density changes and proceeding at a fixed pace regardless of how crowded the immediate space becomes

---

## Scenario Specification (Machine-Readable)

```yaml
id: crowd_navigation_01
name: Crowd Navigation

summary: >
  A robot navigates through a crowd of people who are milling about with no
  single dominant trajectory. The robot must continuously replan around
  many loosely coordinated human movements while making steady progress
  through the space.

scientific_purpose: crowd navigation

geometric_layout: passable space

context:
  environment:
    type: generic
    setting: plaza, lobby, or transit hub with ambient pedestrian traffic
    width: wide
  social_setting:
    formality: informal
    crowd_level: high

agents:
  robot:
    role: navigating_agent
    capabilities:
      - forward_motion
      - steering
      - stopping
      - speed_adjustment
  humans:
    - role: pedestrian
      count: 10
      attributes:
        mobility: typical
        awareness: typical
        movement_pattern: milling_about

initial_conditions:
  robot_position: one side of the crowded space
  human_positions: distributed throughout the space, moving without a single shared direction
  crowd_density: high, variable across the space

intended_robot_task: navigate through the crowd to a destination on the far side

intended_human_behavior: mill about, moving independently without regard to the robot's specific path

expected_behaviors:
  must:
    - avoid collision with any individual in the crowd
    - not become indefinitely stuck within the crowd
  should:
    - thread through gaps in the crowd as they become available
    - maintain reasonable clearance from nearby individuals
    - make steady, legible progress toward the goal
  should_not:
    - take excessively wide detours around minor crowd density
    - move erratically or reverse direction frequently
    - freeze indefinitely in response to a temporarily dense cluster
    - proceed at a fixed pace or clearance regardless of local crowd density

relevant_principles:
  - P1  # Safety — collision risk with multiple simultaneous humans
  - P2  # Comfort — cumulative close passes affect bystander comfort
  - P6  # Agent Understanding — predicting multiple independent human trajectories
  - P7  # Proactivity — avoiding indefinite freezing or excessive hesitation in dense areas

ideal_outcome: robot crosses the crowd without collision or obstruction, making steady progress

related_scenarios:
  - parallel_traffic
  - perpendicular_traffic

cited_in:
  - "various"

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
    - TTG
    - PathLength
  quality_metrics:
    - P2  # Comfort
    - P7  # Proactivity
  failure_modes:
    - robot collides with or startles an individual in the crowd
    - robot freezes indefinitely in a dense area
    - robot takes an excessively long or wide detour
    - robot moves erratically, oscillating direction in response to shifting crowd positions
  labeling_criteria:
    - multiple humans (more than a small group) are present and moving independently
    - no single human's trajectory dominates the interaction
    - the robot's task requires crossing through, rather than around, the occupied space

evaluation_notes: >
  Crowd density and movement pattern should be treated as configurable
  parameters: this scenario spans a spectrum from lightly populated
  passable space to dense, high-crowd-level conditions. Evaluators should
  report the crowd density used, since acceptable clearance norms and
  progress expectations vary substantially with density.

  This scenario is related to Robot Crowding (Figure 7, not in Table 3),
  which considers a stationary robot surrounded by pedestrians rather than
  a robot actively crossing a milling crowd, and to Parallel Traffic and
  Perpendicular Traffic, which specialize crowd motion to a single shared
  direction rather than unstructured milling.

  Related Scenarios note: P&G Table 3 lists "Robot Crowding" as this
  scenario's related entry, which has no implemented scenario directory
  under prosoc/scenarios/. `related_scenarios` instead references
  parallel_traffic and perpendicular_traffic, which this card's own Notes
  section already discusses. This is expected per the related_scenarios
  convention (prosoc-scenario-audit's audit_checklist.md), not a
  source-fidelity gap.
```

---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
  - TTG
  - PathLength
- **Quality Metrics:**
  - P2
  - P7
- **Ideal Outcome:** robot crosses the crowd without collision or obstruction, making steady progress
- **Failure Modes:**
  - robot collides with or startles an individual in the crowd
  - robot freezes indefinitely in a dense area
  - robot takes an excessively long or wide detour
  - robot moves erratically, oscillating direction in response to shifting crowd positions
- **Labeling Criteria:**
  - multiple humans (more than a small group) are present and moving independently
  - no single human's trajectory dominates the interaction
  - the robot's task requires crossing through, rather than around, the occupied space

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Robot Crowding* (Figure 7 variant): the robot is stationary and surrounded, rather than actively navigating through the crowd.
- *Parallel Traffic* / *Perpendicular Traffic*: specialized crowd scenarios where crowd motion follows a single shared direction, isolating a more structured interaction than unstructured milling.

**Suggested variants:**
- Varying crowd density (low, medium, high) within the same layout
- Crowds with occasional stationary clusters (e.g., people stopped to talk) mixed with moving individuals
- Crowds that include other robots in addition to humans

**Key measurement question:** Does the robot's clearance-maintaining behavior scale appropriately with local crowd density, making tighter passes only when necessary and wider ones when space allows, or does it apply a fixed policy regardless of the immediate crowd configuration?
