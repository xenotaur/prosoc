# Scenario: Perpendicular Traffic

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [167]
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** —

---

## Scenario Overview

This scenario describes a robot **crossing an intersection while a crowd of pedestrians flows perpendicular to its path** — for example, a robot crossing a busy corridor junction or plaza crossing where a stream of foot traffic moves from A to B across the robot's intended route. Unlike Parallel Traffic, where crowd motion aligns with the robot's direction, Perpendicular Traffic requires the robot to cut across an orthogonal, continuous flow of pedestrians.

The defining challenge is **gap selection in a continuous cross-flow**: the robot cannot simply merge and match pace as in Parallel Traffic; it must identify safe openings in the perpendicular stream and time its crossing to avoid inserting itself into the flow at an unsafe moment, much like a pedestrian crossing a busy street without a signal.

Successful navigation requires the robot to assess the flow's density and pace, select an appropriate gap or moment to cross, commit to the crossing decisively once selected, and avoid lingering at the boundary of the flow in a way that creates ambiguity for oncoming pedestrians.

---

## Social Navigation Context

Crossing perpendicular pedestrian traffic is analogous to jaywalking through a busy pedestrian corridor or crossing a plaza's main foot-traffic axis. Humans performing this crossing typically watch the flow, identify a gap or a slowing point, and commit to crossing briskly and predictably; hesitating partway across a flow is more disruptive and riskier than either waiting or committing.

Key challenges:

- **Gap assessment**: the robot must judge flow density and speed to identify a safe crossing opportunity, rather than proceeding at a fixed schedule.
- **Commitment**: once crossing begins, hesitating or reversing mid-flow is more disruptive to pedestrians already adjusting to the robot's presence than either waiting or continuing.
- **Legible crossing behavior**: pedestrians in the flow need to be able to predict whether the robot is crossing or waiting, especially since the robot is moving across their path rather than alongside it.
- **Avoiding indefinite waiting**: in a continuously dense flow, the robot must still find or create an acceptable moment to cross rather than waiting indefinitely.

This scenario is scientifically interesting because it isolates decisive, well-timed crossing behavior against continuous multi-agent traffic, distinct from the single-pedestrian negotiation in Intersection scenarios.

---

## Normative Expectations

Acceptable robot behavior includes:

- Pausing at the flow boundary to assess density and timing before committing to cross
- Selecting a gap or lull in the flow and crossing briskly and predictably
- Committing to the crossing once begun, rather than hesitating or reversing partway
- Adjusting crossing speed modestly if the flow shifts, without abandoning the crossing unnecessarily

Unacceptable behavior includes:

- Entering the flow without adequate assessment, forcing pedestrians to stop or swerve
- Stopping or reversing in the middle of the crossing, creating an obstruction within the flow
- Waiting indefinitely at the boundary without ever finding an acceptable moment to cross
- Crossing so slowly that it remains within the flow's path for an extended period

---

## Scenario Specification (Machine-Readable)

```yaml
id: perpendicular_traffic_01
name: Perpendicular Traffic

summary: >
  A robot crosses an intersection or plaza while a crowd of pedestrians
  flows perpendicular to its path. The robot must assess the density and
  pace of the cross-flow, select a safe gap or moment, and cross decisively
  without lingering within the flow.

scientific_purpose: crowd navigation

geometric_layout: intersection

context:
  environment:
    type: generic
    setting: busy corridor junction or plaza crossing
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
        movement_pattern: perpendicular_stream

initial_conditions:
  robot_position: at the boundary of the perpendicular pedestrian flow
  human_positions: a continuous stream moving from A to B, orthogonal to the robot's intended path
  flow_direction: perpendicular to robot's cross-navigate path

intended_robot_task: cross navigate through the perpendicular flow

intended_human_behavior: mill from A to B, forming a continuous perpendicular stream

expected_behaviors:
  must:
    - avoid collision with any pedestrian in the flow
    - not stop or reverse within the middle of the flow once crossing has begun
  should:
    - assess flow density and timing before committing to cross
    - select a gap or lull and cross briskly and predictably
    - commit decisively once crossing begins
  should_not:
    - enter the flow without adequate assessment, forcing pedestrians to stop or swerve
    - wait indefinitely at the boundary without completing the crossing
    - cross so slowly that it remains within the flow's path for an extended period

relevant_principles:
  - P1  # Safety — collision risk while crossing a continuous cross-flow
  - P3  # Legibility — crossing intent must be clear to flow pedestrians
  - P6  # Agent Understanding — assessing flow density and timing to select a safe gap
  - P7  # Proactivity — avoiding indefinite waiting at the flow boundary

ideal_outcome: robot crosses the perpendicular flow without collision or obstruction

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
    - TTG
  quality_metrics:
    - P3  # Legibility
    - P7  # Proactivity
  failure_modes:
    - robot collides with a pedestrian while crossing the flow
    - robot stops or reverses mid-crossing, obstructing the flow
    - robot waits indefinitely at the boundary without crossing
    - robot forces multiple pedestrians to stop or swerve to avoid it
  labeling_criteria:
    - a crowd of pedestrians is present with a shared direction of travel
    - the robot's intended path crosses that shared direction at an angle (typically perpendicular)
    - the robot's task requires traversing the flow rather than merging into it

evaluation_notes: >
  This scenario isolates decisive gap-selection and crossing behavior
  against a continuous cross-flow, distinct from Intersection No Gesture,
  which involves a single human rather than a continuous stream. Evaluators
  should measure both the wait time before crossing (excessive waiting is
  a failure mode) and the smoothness/commitment of the crossing itself.

  This scenario is related to Plaza Crossing (a descriptive variant implied
  by [167], not separately defined in Table 3) and to Parallel Traffic,
  which involves flow aligned with rather than orthogonal to the robot's
  path.
```

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Parallel Traffic*: crowd flow aligned with the robot's path, requiring flow-matching rather than gap-crossing.
- *Intersection No Gesture*: a single-human crossing negotiation, rather than a continuous multi-pedestrian stream.
- *Plaza Crossing*: a descriptive variant of this scenario set in an open plaza rather than a corridor junction.

**Suggested variants:**
- Varying flow density (light foot traffic vs. rush-hour density)
- Flow with intermittent gaps vs. a continuously dense stream requiring the robot to create space
- Multiple perpendicular flows crossing at the same junction

**Key measurement question:** Does the robot select a well-timed gap and commit decisively, or does it enter the flow reactively (forcing pedestrians to accommodate it) or wait indefinitely without ever crossing?
