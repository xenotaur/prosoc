# Hallway Passing 01

A robot and a human pass each other in a narrow hallway.

**Version:** 0.1  
**Status:** Draft (Normative)  
**Scope:** Mobile robot navigation in human-populated environments  
**Derived from:**  
- *Principles and Guidelines for Evaluating Social Robot Navigation Algorithms* (Francis et al.)  


```yaml
id: hallway_passing_01
name: Passing a Human in a Narrow Hallway

summary: >
  A robot and a human approach each other from opposite ends of a narrow hallway,
  requiring coordination to pass safely and comfortably.

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
      - stopping
      - lateral_adjustment
  humans:
    - role: pedestrian
      count: 1
      attributes:
        mobility: typical
        awareness: attentive

initial_conditions:
  robot_position: end_of_hallway
  human_position: opposite_end
  visibility: clear

expected_behaviors:
  must:
    - maintain safe distance
    - avoid sudden movements
  should:
    - signal intent clearly
    - yield if appropriate
  should_not:
    - force the human to stop abruptly
    - invade personal space

relevant_principles:
  - P1   # Safety
  - P2   # Comfort
  - P3   # Legibility
  - P4   # Politeness

evaluation_notes: >
  Successful behavior involves clear intent signaling and smooth coordination.
  Failure modes include hesitation deadlock or aggressive approach.
```