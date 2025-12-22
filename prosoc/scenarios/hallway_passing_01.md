# Scenario: Passing a Human in a Narrow Hallway

This scenario describes a canonical **social navigation coordination problem** in which a robot and a human approach each other from opposite ends of a narrow hallway. The scenario tests **mutual coordination under ambiguity**, where neither agent has an explicit right-of-way and successful navigation depends on interpreting intent, resolving hesitation, and avoiding discomfort or deadlock.

---

```yaml
id: hallway_passing_01
name: Passing a Human in a Narrow Hallway

summary: >
  A robot and a human approach each other from opposite ends of a narrow hallway,
  requiring mutual coordination to pass safely, comfortably, and without
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
  - P4  # Politeness


 evaluation_notes: >
  This scenario evaluates how well the robot coordinates with a human under
  mutual uncertainty. Brief hesitation may be acceptable if it increases
  legibility or clarifies intent, but prolonged deadlock, abrupt reversals,
  or aggressive advancement are indicative of poor performance.

  The scenario assumes an attentive human pedestrian. Different behaviors may
  be appropriate if the human is distracted, impaired, or encumbered, which
  are addressed in separate scenario variants.
```

---

## Discussion

This scenario is intended as a **baseline social navigation test case** and may be extended through variants that modify hallway width, human attentiveness, group size, or cultural expectations around yielding. The goal is not to prescribe a single correct behavior, but to evaluate whether the robot behaves as a cooperative, legible participant in shared space, consistent with the Prosocial Navigation Charter.

