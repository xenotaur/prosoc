# Scenario: Narrow Doorway

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [126]
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** render_sections.py, 2026-07-20

---

## Scenario Card Summary

- **Scenario Name:** Narrow Doorway
- **Scenario Description:** A robot and a human pedestrian approach a narrow doorway from opposite directions. The doorway permits only single-file passage, so the two agents must sequence their passage through the threshold without collision or mutual blocking.
- **Scientific Purpose:** pedestrian interaction
- **Physical Environment:** indoor
- **Geometric Layout:** room and door
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from A to B through the doorway
- **Human Behavior:** navigate from B to A through the doorway
- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P3
  - P4
- **Ideal Outcome:** robot and human sequence through the doorway one at a time without collision or obstruction
- **Related Scenarios:** blind_corner, entering_room, exiting_room
- **Cited In:** 126

---

## Scenario Overview

This scenario describes an encounter in which a robot and a human pedestrian must pass through a **narrow doorway** from opposite directions. Unlike an open hallway, a doorway is a single-file bottleneck: the room and door geometry means that only one agent can pass through the threshold at a time, and simultaneous passage risks a collision or mutual blocking at the frame.

The defining challenge is **sequencing through a bottleneck**: the robot and human must negotiate who goes first, since the doorway's width does not allow side-by-side passage. This differs from a frontal hallway approach, where lateral space typically allows both parties to adjust trajectory and pass side by side.

Successful navigation requires the robot to recognize the bottleneck early, choose or yield the right of way clearly, and pass through without forcing the human to stop awkwardly at the threshold or squeeze past at close quarters.

---

## Social Navigation Context

Doorways are classic sites of everyday social negotiation — holding a door, waiting for someone to pass, or the mutual "after you" hesitation. Humans use subtle cues (eye contact, slight pauses, body orientation) to resolve who goes first. A robot lacks some of these cues and may not read the human's approach speed or intent correctly.

Key challenges:

- **Bottleneck geometry**: the doorway permits only one agent through at a time, unlike open passable space.
- **Timing sensitivity**: arriving at the threshold simultaneously creates ambiguity about right-of-way.
- **Legibility of yielding**: the robot must clearly signal whether it is yielding or proceeding, since a doorway offers little room for the human to reinterpret an ambiguous robot trajectory.

This scenario is scientifically interesting because it isolates sequencing behavior at a hard bottleneck, distinct from the trajectory-negotiation behavior tested in open hallway scenarios.

---

## Normative Expectations

Acceptable robot behavior includes:

- Recognizing the doorway bottleneck from a distance and adjusting speed accordingly
- Yielding clearly (stopping short of the threshold) when the human is closer to or already at the door
- Proceeding decisively when the robot has clear priority, rather than hesitating at the threshold
- Passing through without requiring the human to flatten against the doorframe

Unacceptable behavior includes:

- Arriving at the threshold at the same time as the human and forcing a stand-off or collision
- Committing to passage after the human has already begun entering the doorway
- Stopping directly in the doorway, blocking it for both parties
- Oscillating between yielding and proceeding in a way that confuses the human

---

## Scenario Specification (Machine-Readable)

```yaml
id: narrow_doorway_01
name: Narrow Doorway

summary: >
  A robot and a human pedestrian approach a narrow doorway from opposite
  directions. The doorway permits only single-file passage, so the two
  agents must sequence their passage through the threshold without
  collision or mutual blocking.

scientific_purpose: pedestrian interaction

geometric_layout: room and door

context:
  environment:
    type: indoor
    setting: office or residential room with a single doorway
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
      - speed_adjustment
  humans:
    - role: pedestrian
      count: 1
      attributes:
        mobility: typical
        awareness: typical

initial_conditions:
  robot_position: one side of the doorway
  human_position: opposite side of the doorway
  doorway_width: single-file only
  mutual_visibility: full, from moderate distance

intended_robot_task: navigate from A to B through the doorway

intended_human_behavior: navigate from B to A through the doorway

expected_behaviors:
  must:
    - avoid collision with the human at or in the doorway
    - not stop in a position that blocks the doorway for both agents
  should:
    - recognize the single-file bottleneck and adjust approach speed
    - yield clearly when the human is closer to the threshold
    - proceed decisively and without hesitation when the robot has priority
  should_not:
    - arrive at the threshold simultaneously with the human without resolving priority
    - commit to passage after the human has already entered the doorway
    - oscillate between yielding and proceeding

relevant_principles:
  - P1  # Safety — collision risk at the constrained threshold
  - P3  # Legibility — robot must clearly signal yield/proceed intent
  - P4  # Politeness — courteous sequencing through a shared bottleneck
  - P7  # Proactivity — resolving the sequencing decision without deadlock

ideal_outcome: robot and human sequence through the doorway one at a time without collision or obstruction

related_scenarios:
  - blind_corner
  - entering_room
  - exiting_room

cited_in:
  - "126"

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
  quality_metrics:
    - P3  # Legibility
    - P4  # Politeness
  failure_modes:
    - robot collides with human at the doorway threshold
    - robot and human reach a stand-off, neither proceeding
    - robot stops inside the doorway, blocking passage
    - human is forced to squeeze past the robot at close quarters
  labeling_criteria:
    - robot and human approach a single doorway from opposite sides
    - the doorway geometry does not permit side-by-side passage
    - agents are on a collision course toward the same threshold

evaluation_notes: >
  This scenario isolates sequencing behavior at a hard single-file bottleneck,
  as distinct from the lateral trajectory negotiation tested in Frontal
  Approach. Evaluators should focus on whether the robot resolves right-of-way
  early and legibly, rather than on the specific trajectory taken.

  The scenario is related to Blind Corner in that both involve constrained
  geometry, but Narrow Doorway typically affords full mutual visibility from
  a distance, so failures here reflect poor sequencing decisions rather than
  limited detection range.

  Variants may include different approach speeds, a partially open vs. fully
  open door, or a human carrying an object that further narrows the usable
  width.
```

---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P3
  - P4
- **Ideal Outcome:** robot and human sequence through the doorway one at a time without collision or obstruction
- **Failure Modes:**
  - robot collides with human at the doorway threshold
  - robot and human reach a stand-off, neither proceeding
  - robot stops inside the doorway, blocking passage
  - human is forced to squeeze past the robot at close quarters
- **Labeling Criteria:**
  - robot and human approach a single doorway from opposite sides
  - the doorway geometry does not permit side-by-side passage
  - agents are on a collision course toward the same threshold

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Narrow Arch*: a related geometric variant using an archway rather than a hinged door; expected to share the same sequencing dynamics.
- *Blind Corner*: shares constrained geometry but removes advance visibility; Narrow Doorway typically preserves full visibility, so the challenge is sequencing rather than detection.
- *Entering Room* / *Exiting Room*: variants of the room-and-door layout where the human's task is a fixed room transit rather than a two-way corridor crossing.

**Suggested variants:**
- Partially obstructed doorway (e.g., propped open at an angle)
- Human carrying a bulky object that further reduces effective doorway width
- Simultaneous arrival timed precisely to test deadlock-resolution behavior

**Key measurement question:** Does the robot commit to a yield/proceed decision early enough that the human can read it, or does it leave the decision ambiguous until the last moment?
