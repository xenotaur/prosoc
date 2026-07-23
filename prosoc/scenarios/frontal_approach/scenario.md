# Scenario: Frontal Approach

## Status

- **STATE:** DRAFTED
- **SOURCE:** Prompt to ChatGPT 5.2
- **DRAFTED:** ChatGPT 5.2, 2026-01-02
- **EDITED:** render_sections.py, 2026-07-19

## Scenario Card Summary

- **Scenario Name:** Frontal Approach
- **Scenario Description:** A robot and a human approach each other in opposite directions in a narrow hallway and pass each other safely, comfortably, and without prolonged hesitation.
- **Scientific Purpose:** pedestrian interaction
- **Physical Environment:** indoor
- **Geometric Layout:** passable space
- **Robot Role:** navigating_agent
- **Robot Task:** navigate from A to B
- **Human Behavior:** navigate from B to A
- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P2
  - P3
  - P5
- **Ideal Outcome:** robot and human pass each other safely, comfortably, and without prolonged hesitation
- **Related Scenarios:** blind_corner, movable_obstruction, single_file_hallway
- **Cited In:** 50, 126, 167

---

## Scenario Overview

This scenario describes a canonical social navigation conflict in which a robot and a human approach each other in opposite directions in a narrow hallway where neither agent has an explicit right-of-way. Successful navigation depends on sensing and agile navigation, and successful social navigation may require trajectory prediction, interpreting intent, resolving hesitation, and resolving conflicts. The scenario tests social navigation principles including safety, comfort, legibility, following social norms, and agent understanding.

---

## Scenario Specification (Machine-Readable)

```yaml
id: frontal_approach_01
name: Frontal Approach

summary: >
  A robot and a human approach each other in opposite directions in a narrow hallway and pass each other safely, comfortably, and without
  prolonged hesitation.

scientific_purpose: pedestrian interaction

geometric_layout: passable space

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
      - trajectory_prediction
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

intended_robot_task: navigate from A to B

intended_human_behavior: navigate from B to A

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

ideal_outcome: robot and human pass each other safely, comfortably, and without prolonged hesitation

related_scenarios:
  - blind_corner
  - movable_obstruction
  - single_file_hallway

cited_in:
  - "50"
  - "126"
  - "167"

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
  quality_metrics:
    - P2   # Comfort
    - P3   # Legibility
    - P5   # Social Competency
  failure_modes:
    - robot collides with human
    - robot fails to make progress toward passing
  labeling_criteria:
    - robot and human face each other at the start of the episode
    - robot and human move toward each other
    - sufficient clearance exists for passing

evaluation_notes: >
  This scenario evaluates how well the robot navigates through shared space with a human in the conditions for a mild and typical conflict.
  Changing direction, slowing down, braking or hesitation may be acceptable if they increase safety, comfort, or legibility, but  prolonged deadlock, abrupt reversals,
  or aggressive advancement are indicative of poor performance.

  The scenario assumes a pedestrian with a typical level of awareness,
  neither oblivious to the presence of the robot nor overly attentive to it.

  Related Scenarios note: P&G Table 3 lists "Ped. Obstruct" as this
  scenario's related entry, which has no implemented scenario directory
  under prosoc/scenarios/. `related_scenarios` instead references
  blind_corner, movable_obstruction, and single_file_hallway, which this
  corpus's own scenario set explicitly treats as a progressively
  constrained variant series of this scenario. This is expected per the
  related_scenarios convention (prosoc-scenario-audit's
  audit_checklist.md), not a source-fidelity gap.

```

---

## Discussion

This scenario is intended as a **baseline social navigation test case** and may be extended through variants that modify hallway width, human attentiveness, group size, or cultural expectations around yielding. The goal is not to prescribe a single correct behavior, but to evaluate whether the robot behaves as a cooperative, legible participant in shared space, consistent with the Prosocial Navigation Charter.


---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
- **Quality Metrics:**
  - P2
  - P3
  - P5
- **Failure Modes:**
  - robot collides with human
  - robot fails to make progress toward passing
- **Labeling Criteria:**
  - robot and human face each other at the start of the episode
  - robot and human move toward each other
  - sufficient clearance exists for passing
- **Ideal Outcome:** robot and human pass each other safely, comfortably, and without prolonged hesitation
