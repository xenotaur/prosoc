# Prosoc Scenario Schema Field Guide

This is a human-readable companion to `prosoc/scenarios/schema.json`. Use it when mapping
source paper content to scenario card fields.

## Required Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Unique stable identifier. Use `snake_case_01` convention, e.g. `blind_corner_01` |
| `name` | string | Human-readable name matching Table 3, e.g. `Blind Corner` |
| `summary` | string | 1–2 sentence physical description. Should stand alone without the prose. |

## Strongly Recommended Fields

| Field | Type | Notes |
|-------|------|-------|
| `scientific_purpose` | string | e.g. "pedestrian interaction", "crowd navigation", "group interaction" |
| `geometric_layout` | string | e.g. "corridor", "intersection", "room and door", "open space" |
| `context.environment.type` | string | `indoor`, `outdoor`, or `generic` |
| `context.environment.setting` | string | e.g. "office hallway", "hospital corridor", "plaza" |
| `context.environment.width` | string | e.g. "narrow", "moderate", "wide" |
| `context.social_setting.formality` | string | `informal`, `formal`, `mixed` |
| `context.social_setting.crowd_level` | string | `low`, `medium`, `high` |
| `intended_robot_task` | string | e.g. "navigate from A to B", "deliver object to human" |
| `intended_human_behavior` | string | e.g. "cross navigate", "gesture wait", "lead robot to destination" |
| `ideal_outcome` | string | Concise: e.g. "robot and human pass without collision" |
| `relevant_principles` | array of P1–P8 | See principles.md. Limit to 3–5 most relevant. |

## agents Block

```yaml
agents:
  robot:
    role: navigating_agent   # or: leader, follower, servant, any
    capabilities:
      - forward_motion
      - steering
      - stopping
      # add others as appropriate: speed_adjustment, path_commitment, gesture_recognition
  humans:
    - role: pedestrian        # or: group, leader, confederate
      count: 1
      attributes:
        mobility: typical
        awareness: typical
        # add others: gesturing, speed, group_size
```

## expected_behaviors Block

Three sub-arrays: `must`, `should`, `should_not`. Follow P&G Guideline N6 — keep these
**broad and flexible**, not prescriptive. Describe *what kind* of behavior is expected,
not exact motion commands.

```yaml
expected_behaviors:
  must:
    - avoid collision with human
    - not block the human's path indefinitely
  should:
    - yield when right-of-way is ambiguous
    - signal intent through consistent motion
  should_not:
    - force the human to stop abruptly
    - oscillate or hesitate excessively
```

## scenario_usage_guide Block

```yaml
scenario_usage_guide:
  success_metrics:
    - SR          # Success Rate (reached goal)
    - NoCollisions
  quality_metrics:
    - P2          # Comfort
    - P3          # Legibility
  failure_modes:
    - robot collides with human
    - robot fails to pass within time limit
    - robot blocks human path
  labeling_criteria:
    - observable geometric conditions that identify this scenario in data
    - e.g. "robot and human approach from opposite directions in corridor"
```

## evaluation_notes

Use this free-text field to:
- Explain acceptable trade-offs (e.g. slowing down is OK if it increases safety)
- Describe common failure modes in detail
- Note context-dependence (e.g. speed norms differ in hospital vs. office)
- Flag any ambiguities not resolvable from the source paper

## What to Leave Blank

It is better to leave a field blank than to guess. The workflow lifecycle (DRAFTED status)
signals that the card is incomplete. A human editor (EDITED stage) can fill gaps with
domain knowledge. Do not fabricate values to make the card look complete.

## additionalProperties

The root schema has `"additionalProperties": false`. Do not add fields not defined in
schema.json. The `context`, `agents`, `initial_conditions`, and `agents.humans[].attributes`
blocks allow additional properties and can be extended freely.
