# Scenario: Parallel Traffic

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [167]
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** render_sections.py, 2026-07-20

---

## Scenario Card Summary

- **Scenario Name:** Parallel Traffic
- **Scenario Description:** A robot navigates from A to B while a crowd of pedestrians moves broadly in the same direction, forming an emergent pedestrian stream. The robot must merge into and hold a stable position within the flow, matching pace and minimizing lateral weaving.
- **Scientific Purpose:** crowd navigation
- **Physical Environment:** generic
- **Geometric Layout:** passable space
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from A to B
- **Human Behavior:** mill from A to B, forming a parallel pedestrian stream
- **Success Metrics:**
  - SR
  - NoCollisions
  - TTG
- **Quality Metrics:**
  - P2
  - P5
- **Ideal Outcome:** robot merges into and travels with the pedestrian stream without collision or obstruction

**Remaining gaps:**

- **Related Scenarios** — should-fill-in-now
- **Cited In** — should-fill-in-now

---

## Scenario Overview

This scenario describes a robot navigating from point A to point B while a **crowd of pedestrians moves in the same general direction**, roughly parallel to the robot's own path — as in a busy sidewalk, corridor, or plaza where foot traffic flows predominantly one way (or bidirectionally along a shared axis). Unlike Crowd Navigation, where the crowd mills about without a shared direction, Parallel Traffic isolates the case where crowd motion is broadly aligned with the robot's direction of travel.

The defining challenge is **merging into and maintaining position within directional flow**: the robot must match the general pace and lane discipline of the surrounding pedestrian stream, finding and holding a consistent position within the flow rather than weaving unpredictably or forcing its way through parallel-moving pedestrians.

Successful navigation requires the robot to merge into the flow smoothly, maintain a consistent relative pace and lane position, and adjust incrementally to local speed variation without significant weaving, overtaking abruptly, or repeatedly crossing other pedestrians' lanes.

---

## Social Navigation Context

Sidewalks, corridors, and transit concourses often exhibit emergent "lane" behavior, where pedestrians moving in the same direction implicitly organize into loosely parallel streams (a phenomenon well documented in pedestrian dynamics research). Humans entering such a flow typically merge at the edge and settle into a stable position, adjusting pace to the local stream rather than cutting across multiple lanes.

Key challenges:

- **Flow matching**: the robot should adopt a pace broadly consistent with the surrounding pedestrian stream rather than moving substantially faster or slower.
- **Lane discipline**: minimizing lateral weaving preserves the flow's emergent organization and reduces the chance of unexpected close passes.
- **Local speed variation**: pedestrian streams naturally speed up and slow down; the robot should track these variations smoothly rather than reacting abruptly to each fluctuation.
- **Distinguishing from Circular Crossing**: this scenario assumes a broadly straight, shared-direction flow rather than pedestrians crossing the robot's path at an angle.

This scenario is scientifically interesting because it tests a robot's ability to conform to emergent group dynamics (stream behavior) rather than treating each nearby pedestrian as an independent obstacle.

---

## Normative Expectations

Acceptable robot behavior includes:

- Merging into the pedestrian stream at a natural point rather than cutting across multiple lanes
- Matching pace broadly to the surrounding flow, adjusting incrementally as the flow speeds up or slows down
- Maintaining a consistent lateral position (lane) rather than weaving between pedestrians
- Overtaking only when a clear, socially unobtrusive gap is available

Unacceptable behavior includes:

- Cutting perpendicular to the flow to reach a position, disrupting multiple pedestrians' paths
- Moving substantially faster or slower than the surrounding stream without cause
- Weaving laterally between pedestrians repeatedly rather than holding a stable position
- Forcing an overtake through a gap too narrow for comfortable clearance

---

## Scenario Specification (Machine-Readable)

```yaml
id: parallel_traffic_01
name: Parallel Traffic

summary: >
  A robot navigates from A to B while a crowd of pedestrians moves broadly
  in the same direction, forming an emergent pedestrian stream. The robot
  must merge into and hold a stable position within the flow, matching
  pace and minimizing lateral weaving.

scientific_purpose: crowd navigation

geometric_layout: passable space

context:
  environment:
    type: generic
    setting: busy sidewalk, corridor, or transit concourse
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
      count: 15
      attributes:
        mobility: typical
        awareness: typical
        movement_pattern: parallel_stream

initial_conditions:
  robot_position: entering the pedestrian stream from one side
  human_positions: distributed along a shared direction of travel roughly parallel to the robot's path
  flow_direction: broadly aligned with robot's A-to-B path

intended_robot_task: navigate from A to B

intended_human_behavior: mill from A to B, forming a parallel pedestrian stream

expected_behaviors:
  must:
    - avoid collision with any pedestrian in the stream
    - not cut across multiple pedestrians' lanes to force a position
  should:
    - merge into the stream smoothly at a natural entry point
    - match pace broadly to the surrounding flow
    - maintain a consistent lateral position within the flow
  should_not:
    - move substantially faster or slower than the surrounding stream without cause
    - weave laterally between pedestrians repeatedly
    - force an overtake through an insufficiently clear gap

relevant_principles:
  - P1  # Safety — collision risk within a dense parallel stream
  - P2  # Comfort — erratic weaving or pace mismatch affects bystander comfort
  - P5  # Social Competency — conforming to emergent lane/stream norms
  - P6  # Agent Understanding — predicting the stream's aggregate pace and flow

ideal_outcome: robot merges into and travels with the pedestrian stream without collision or obstruction

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
    - TTG
  quality_metrics:
    - P2  # Comfort
    - P5  # Social Competency
  failure_modes:
    - robot collides with a pedestrian while merging or traveling within the stream
    - robot cuts across the flow, disrupting multiple pedestrians
    - robot's pace diverges substantially from the surrounding stream
    - robot weaves laterally rather than holding a stable lane position
  labeling_criteria:
    - a crowd of pedestrians is present with a broadly shared direction of travel
    - the robot's intended path is roughly aligned with that shared direction
    - the robot's task requires sustained travel through the stream rather than a single crossing

evaluation_notes: >
  This scenario isolates directional-flow conformance from the more general
  Crowd Navigation scenario, where crowd motion has no shared direction.
  Evaluators should measure lateral weaving (e.g., variance in lane
  position) and pace-matching (relative speed to the local stream) as
  quality indicators distinct from simple collision avoidance.

  This scenario is related to Circular Crossing (Figure 7, not in Table 3),
  which involves pedestrians crossing at an angle rather than moving
  parallel to the robot, and to Perpendicular Traffic, which specializes
  crowd motion to a direction orthogonal to the robot's path.
```

---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
  - TTG
- **Quality Metrics:**
  - P2
  - P5
- **Ideal Outcome:** robot merges into and travels with the pedestrian stream without collision or obstruction
- **Failure Modes:**
  - robot collides with a pedestrian while merging or traveling within the stream
  - robot cuts across the flow, disrupting multiple pedestrians
  - robot's pace diverges substantially from the surrounding stream
  - robot weaves laterally rather than holding a stable lane position
- **Labeling Criteria:**
  - a crowd of pedestrians is present with a broadly shared direction of travel
  - the robot's intended path is roughly aligned with that shared direction
  - the robot's task requires sustained travel through the stream rather than a single crossing

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Perpendicular Traffic*: crowd motion is orthogonal to the robot's path rather than parallel, requiring crossing behavior instead of flow-matching.
- *Circular Crossing* (Figure 7 variant): pedestrians cross in a circular or angled pattern rather than a straight parallel stream.
- *Crowd Navigation*: crowd motion has no shared direction; Parallel Traffic specializes this to an aligned, structured stream.

**Suggested variants:**
- Bidirectional parallel streams (two opposing lanes) vs. unidirectional flow
- Variable stream density and pace (e.g., rush-hour vs. sparse pedestrian traffic)
- Robot needing to exit the stream at a specific point (e.g., a storefront), requiring lateral movement out of the flow

**Key measurement question:** Does the robot conform to the emergent lane/stream structure of the crowd (stable position, matched pace), or does it treat each pedestrian as an independent obstacle to be individually avoided, producing erratic weaving?
