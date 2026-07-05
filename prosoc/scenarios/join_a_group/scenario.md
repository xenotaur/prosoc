# Scenario: Join a Group

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [50, 161]
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** —

---

## Scenario Overview

This scenario describes a robot navigating toward and **joining a standing group of robots or people** who are already engaged in conversation or a shared activity in an open space. Unlike passing or crossing scenarios, the robot's task here is not to travel *through* the space but to *terminate* its navigation within the group's social formation — becoming, in effect, a new member of an existing F-formation (the spatial arrangement humans naturally adopt when conversing in a group).

The defining challenge is **socially appropriate approach and formation entry**: the robot must approach the group from a reasonable angle, at a reasonable speed, and stop at a position and orientation that a human would recognize as "joining the conversation" rather than "passing by," "interrupting," or "looming."

Successful navigation requires the robot to select an approach vector that doesn't cut through the group's shared conversational space, slow appropriately on approach, and settle into a position that expands the group's formation naturally rather than crowding any individual member.

---

## Social Navigation Context

Humans use well-studied spatial conventions for group conversation, described in the literature as F-formations: an O-space (the shared interaction area), a P-space (where members stand), and an R-space (the audience/periphery). Joining a group means smoothly transitioning from being an outsider to becoming a P-space member, which existing members typically accommodate by shifting slightly to open the formation.

Key challenges:

- **Formation geometry**: the robot must recognize the group's O-space and approach without crossing directly through the center of the conversation.
- **Approach legibility**: humans signal intent to join well before arriving (gaze, trajectory curvature, deceleration); a robot approaching group members directly and at a constant speed may read as intrusive or threatening.
- **Timing**: joining while the group is mid-conversation requires different judgment than joining a group that is dispersing or forming.
- **Under-specification risk**: because "join" allows many valid final positions and orientations, this scenario should avoid being interpreted as requiring a single fixed stopping point.

This scenario is scientifically interesting because it evaluates group-level, rather than dyadic, social navigation — a qualitatively different problem than the pedestrian-interaction scenarios elsewhere in Table 3.

---

## Normative Expectations

Acceptable robot behavior includes:

- Approaching the group along a curved or peripheral path rather than a straight line through the conversational center
- Slowing down as it nears the group's O-space boundary
- Coming to rest at a position and orientation that faces into the group's shared space, at a distance consistent with the group's existing spacing norms
- Pausing briefly before fully integrating, allowing existing members to acknowledge or accommodate the new arrival

Unacceptable behavior includes:

- Approaching at full speed and stopping abruptly at close range to a group member
- Cutting directly through the group's O-space to reach a position on the far side
- Positioning itself so close to one member that it appears to address only that individual rather than the group
- Stopping short in a way that leaves it neither clearly inside nor clearly outside the formation (ambiguous membership)

---

## Scenario Specification (Machine-Readable)

```yaml
id: join_a_group_01
name: Join a Group

summary: >
  A robot navigates across open space toward a standing group of robots or
  people already engaged in conversation, and must approach and settle into
  the group's spatial formation as a new member, without disrupting the
  ongoing interaction.

scientific_purpose: group interaction

geometric_layout: open space

context:
  environment:
    type: generic
    setting: open indoor or outdoor gathering space
    width: wide
  social_setting:
    formality: informal
    crowd_level: medium

agents:
  robot:
    role: navigating_agent
    capabilities:
      - forward_motion
      - steering
      - stopping
      - speed_adjustment
      - orientation_control
  humans:
    - role: group
      count: 3
      attributes:
        mobility: stationary
        awareness: typical
        group_size: 3
        formation: conversing_circle

initial_conditions:
  robot_position: outside the group's O-space, approaching
  human_position: standing group already in conversational formation
  group_activity: ongoing conversation

intended_robot_task: navigate to and join the group

intended_human_behavior: continue conversing, accommodating the robot's arrival

expected_behaviors:
  must:
    - avoid collision with any group member
    - avoid cutting directly through the group's shared conversational space
  should:
    - approach along a peripheral or curved path
    - slow down when nearing the group's formation boundary
    - settle at a position and orientation consistent with joining the formation
  should_not:
    - stop abruptly at close range to a single group member
    - position itself so close to one member that it appears to exclude the others
    - leave its final position and orientation ambiguous as to whether it has joined

relevant_principles:
  - P1  # Safety — collision risk when approaching close-standing humans
  - P2  # Comfort — approach speed and proximity affect group members' comfort
  - P4  # Politeness — respecting the group's shared conversational space
  - P5  # Social Competency — recognizing and conforming to F-formation norms
  - P8  # Contextual Appropriateness — behavior must fit the specific group and setting

ideal_outcome: robot joins the group, settling into the formation without disrupting the conversation

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
  quality_metrics:
    - P2  # Comfort
    - P4  # Politeness
    - P5  # Social Competency
  failure_modes:
    - robot collides with or comes uncomfortably close to a group member
    - robot cuts through the group's conversational space
    - robot's final position is ambiguous, unclear whether it has joined or is passing by
    - group members are startled or forced to step back to accommodate the robot
  labeling_criteria:
    - a stationary group of two or more agents is present in a recognizable conversational formation
    - the robot's trajectory terminates at or near the group rather than passing through it
    - the robot's final position and orientation face into the group's shared space

evaluation_notes: >
  This scenario deliberately avoids over-specifying the robot's final
  stopping position, per P&G Guideline N6 — many final positions can
  correctly constitute "joining," and evaluators should judge whether the
  approach and settling behavior is socially legible rather than checking
  against one fixed pose.

  Evaluators should pay particular attention to the *approach trajectory*,
  not just the final position: a robot that ends in a good position after
  cutting through the group's O-space at speed has still failed the social
  competency requirement even if no collision occurred.

  This scenario is closely related to Leaving a Group (Figure 7, not in
  Table 3), its natural inverse, and to Accompany Peer (Figure 7), which
  involves ongoing co-location with a single human rather than a discrete
  join event with a multi-person group.
```

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Leave Group* (Figure 7 variant): the inverse scenario — a robot or agent smoothly disengages from an existing group formation.
- *Accompany Peer* (Figure 7 variant): sustained side-by-side co-navigation with one human, rather than a one-time approach-and-join event with a multi-person group.
- *Crowd Navigation*: distinguished from Join a Group in that crowd members are not in a stable conversational formation and the robot's task is to pass through rather than join.

**Suggested variants:**
- Group size (dyad vs. larger group) — affects available approach angles and formation geometry
- Group already partially open/oriented toward the approaching robot vs. fully closed formation
- Mixed robot/human group membership
- Group actively signaling invitation (e.g., gesturing) vs. neutral/unaware of the approach

**Key measurement question:** Does the robot's approach trajectory respect the group's O-space boundary throughout, or only arrive at an acceptable final position while violating social space during the approach itself?
