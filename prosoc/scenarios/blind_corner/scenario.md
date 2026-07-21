# Scenario: Blind Corner

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [126, 171]
- **DRAFTED:** Claude (new-scenario skill), 2026-06-19
- **EDITED:** render_sections.py, 2026-07-20

---

## Scenario Card Summary

- **Scenario Name:** Blind Corner
- **Scenario Description:** A robot and a human pedestrian approach each other from opposite directions and meet at an indoor blind corner, where neither can see the other until they are in close proximity. The robot must detect the human at short range and resolve the encounter safely without collision or prolonged obstruction.
- **Scientific Purpose:** pedestrian interaction
- **Physical Environment:** indoor
- **Geometric Layout:** corner
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from A to B through the corner
- **Human Behavior:** navigate from B to A through the corner
- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P2
  - P3
- **Ideal Outcome:** robot and human pass each other at the corner without collision or obstruction

**Remaining gaps:**

- **Related Scenarios** — should-fill-in-now
- **Cited In** — should-fill-in-now

---

## Scenario Overview

This scenario describes a navigation encounter in which a robot and a human pedestrian approach each other from opposite directions and meet at a **blind corner** — a turn or bend in an indoor environment where neither agent has advance visibility of the other. Unlike a hallway approach or intersection, neither party can see the other until they are in close proximity, leaving minimal time and space to negotiate passage.

The defining challenge is the **sudden mutual discovery**: both agents must rapidly assess the situation, communicate intent, and resolve right-of-way with little preparation and limited maneuvering space. The robot cannot rely on trajectory prediction from a distance; it must detect and respond to the human at short range.

Successful navigation requires the robot to avoid collision, avoid startling the human, and resolve the encounter without forcing either party to reverse or become stuck. The scenario is particularly relevant to indoor environments such as office buildings, hospitals, and warehouses where corridor layouts create frequent blind turns.

---

## Social Navigation Context

Blind corners are a common site of social friction in indoor pedestrian environments. Human pedestrians typically slow near corners, listen for approaching footsteps, or audibly signal their presence (e.g., calling "corner" in restaurant kitchens). Robots lack these informal human signals and may approach corners at full navigation speed without awareness of an impending encounter.

This asymmetry creates several challenges:

- **Startling**: A robot appearing suddenly at close range may alarm a human, even if no collision occurs.
- **Reduced reaction time**: Short detection range means both parties have less time to yield or replan.
- **Constrained space**: The geometry of a corner limits passing options; one party may need to reverse.
- **Legibility under pressure**: The robot must communicate its intent quickly and clearly under spatial constraints.

The scenario is studied in the social navigation literature because it tests the robot's ability to handle **unexpected close encounters** — a failure mode that can undermine human trust even when collisions are avoided.

---

## Normative Expectations

Acceptable robot behavior in this scenario includes:

- Slowing on approach to corners, particularly when the turn is sharp or visibility is limited
- Stopping promptly upon detecting the human at short range
- Yielding right-of-way to the human when maneuvering space is constrained
- Signaling presence audibly or through motion legibility when approaching high-risk corners
- Resolving the encounter efficiently without requiring the human to reverse

Unacceptable behavior includes:

- Approaching a blind corner at full speed without any speed modulation
- Continuing to advance after the human is detected, forcing a collision or evasive action
- Stopping abruptly and waiting indefinitely without a resolution strategy
- Reversing in a sudden or unpredictable manner that further startles the human

---

## Scenario Specification (Machine-Readable)

```yaml
id: blind_corner_01
name: Blind Corner

summary: >
  A robot and a human pedestrian approach each other from opposite directions and
  meet at an indoor blind corner, where neither can see the other until they are
  in close proximity. The robot must detect the human at short range and resolve
  the encounter safely without collision or prolonged obstruction.

scientific_purpose: pedestrian interaction

geometric_layout: corner

context:
  environment:
    type: indoor
    setting: office or hospital corridor with a blind turn
    width: narrow to moderate
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
        visibility_of_robot: none_until_close

initial_conditions:
  robot_position: one side of the corner
  human_position: other side of the corner
  mutual_visibility: none
  detection_range: short

intended_robot_task: navigate from A to B through the corner

intended_human_behavior: navigate from B to A through the corner

expected_behaviors:
  must:
    - avoid collision with the human at the corner
    - not force the human to take abrupt evasive action
  should:
    - reduce speed when approaching blind corners
    - stop promptly upon detecting the human at close range
    - yield to the human when space is insufficient for simultaneous passage
    - resolve the encounter without requiring either party to reverse unnecessarily
  should_not:
    - approach blind corners at full speed without any modulation
    - continue advancing after human detection in a way that causes alarm
    - remain stopped indefinitely without attempting to resolve the encounter

relevant_principles:
  - P1  # Safety — collision risk is high due to limited detection range
  - P2  # Comfort — sudden appearance at close range can startle or stress the human
  - P3  # Legibility — robot intent must be communicated quickly under spatial constraint
  - P7  # Proactivity — robot may need to take initiative to resolve a spatial deadlock

ideal_outcome: robot and human pass each other at the corner without collision or obstruction

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
  quality_metrics:
    - P2  # Comfort
    - P3  # Legibility
  failure_modes:
    - robot collides with human at or around the corner
    - robot startles human by appearing suddenly at full speed
    - encounter results in prolonged standoff requiring one party to reverse
    - robot stops and fails to resolve the encounter within time limit
  labeling_criteria:
    - robot and human approach the same corner from opposite sides
    - neither agent has line-of-sight to the other at the start of the episode
    - agents come into detection range within a short distance of the corner apex

evaluation_notes: >
  This scenario evaluates the robot's ability to handle unexpected close encounters
  caused by limited visibility. The key challenge is not just avoiding collision but
  doing so in a way that does not alarm or inconvenience the human.

  Speed modulation on approach — slowing before the corner even without detecting the
  human — is a proactive safety behavior that distinguishes socially competent navigation
  from purely reactive collision avoidance. Evaluators should distinguish between:
  (a) a robot that stops safely because it detected the human in time, and
  (b) a robot that narrowly avoids collision because it happened to be moving slowly.

  The scenario is related to the Frontal Approach scenario but differs in that the
  critical constraint is reduced detection range rather than hallway width. Variants
  may include different corner angles (sharp 90° vs. gentle curves), different corridor
  widths, and different robot speeds on approach.

  Human behavior playbook: the human confederate should approach the corner at a
  natural walking pace without anticipating the robot's presence. The confederate
  should not slow down preemptively — the encounter should simulate a natural blind
  corner meeting.
```

---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P2
  - P3
- **Ideal Outcome:** robot and human pass each other at the corner without collision or obstruction
- **Failure Modes:**
  - robot collides with human at or around the corner
  - robot startles human by appearing suddenly at full speed
  - encounter results in prolonged standoff requiring one party to reverse
  - robot stops and fails to resolve the encounter within time limit
- **Labeling Criteria:**
  - robot and human approach the same corner from opposite sides
  - neither agent has line-of-sight to the other at the start of the episode
  - agents come into detection range within a short distance of the corner apex

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Frontal Approach*: both agents have advance visibility; the challenge is hallway width and trajectory negotiation. Blind Corner removes advance visibility entirely, compressing the response window.
- *Narrow Doorway*: similarly constrained geometry but typically with a static doorframe, not a moving pedestrian approaching simultaneously.

**Suggested variants:**
- **Sharp corner** (90°) vs. **gentle curve** — affects detection range and time available to respond
- **Different robot speeds on approach** — isolates the effect of speed modulation as a proactive safety strategy
- **Audible signal** — robot announces its presence before the corner (tests communicative legibility)
- **High-traffic corridor** — corner is frequently used, raising the prior probability of an encounter

**Key measurement question:** Does the robot slow proactively on corner approach, or only react after detection? Proactive slowing is a signature of socially competent behavior (P7, Proactivity) and distinguishes this scenario from pure collision avoidance benchmarks.
