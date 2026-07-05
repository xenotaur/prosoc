# Scenario: Following

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [50]
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** —

---

## Scenario Overview

This scenario describes a robot in a **servant role** whose task is to follow a human as the human leads their own navigation. The human moves freely through a walking space — choosing pace, direction, and path — while the robot's job is to maintain an appropriate following distance and trajectory, staying with the human through turns, stops, and pace changes.

The defining challenge is **joint navigation under asymmetric control**: the robot does not choose the destination or path; it must continuously infer the human's intended trajectory and adapt in real time, without either lagging so far behind that it loses track of the human or crowding so close that it feels intrusive.

Successful navigation requires the robot to maintain a socially comfortable following distance, handle the human's turns and pace changes smoothly, and avoid cutting corners or overtaking when the human merely slows down temporarily.

---

## Social Navigation Context

Following behavior appears in real-world use cases such as luggage-carrying robots, robotic shopping carts, and assistive robots accompanying a person from behind. Humans expect a following robot to behave somewhat like a well-trained companion or pet: present and responsive, but not intrusive or unpredictable.

Key challenges:

- **Distance calibration**: too close feels crowding or threatening; too far risks losing the human in a crowd or at a turn.
- **Turn anticipation**: the robot must predict the human's turning intent early enough to avoid cutting corners or swinging wide.
- **Pace variability**: humans slow down, speed up, and pause; the robot must distinguish a brief pause from a full stop or destination change.
- **Occlusion and crowd robustness**: in populated walking spaces, the robot may temporarily lose direct line of sight to the human and must re-acquire the correct trajectory.

This scenario is scientifically interesting because it tests sustained, real-time responsiveness to another agent's freely chosen path, rather than negotiation of a shared conflict point as in most pedestrian-interaction scenarios.

---

## Normative Expectations

Acceptable robot behavior includes:

- Maintaining a following distance appropriate to the walking space and crowd density
- Smoothly adjusting trajectory through the human's turns without cutting corners or lagging into obstacles
- Slowing and stopping promptly when the human stops
- Recovering gracefully if momentarily blocked or if the human is briefly out of view

Unacceptable behavior includes:

- Following at a distance so close that the human feels pursued or physically crowded
- Following at a distance so far that the robot loses the human at a turn or in a crowd
- Cutting through obstacles or other pedestrians to preserve following distance
- Overtaking or attempting to lead when the human merely pauses briefly

---

## Scenario Specification (Machine-Readable)

```yaml
id: following_01
name: Following

summary: >
  A robot in a servant role follows a human who leads their own navigation
  through a walking space, freely choosing pace, direction, and path. The
  robot must maintain an appropriate following distance and trajectory
  through turns, stops, and pace changes.

scientific_purpose: joint navigation

geometric_layout: walking space

context:
  environment:
    type: generic
    setting: indoor or outdoor pedestrian walking space
    width: moderate
  social_setting:
    formality: informal
    crowd_level: low

agents:
  robot:
    role: servant
    capabilities:
      - forward_motion
      - steering
      - stopping
      - speed_adjustment
      - human_tracking
  humans:
    - role: leader
      count: 1
      attributes:
        mobility: typical
        awareness: typical

initial_conditions:
  robot_position: behind the human at a comfortable following distance
  human_position: leading, free to choose path and pace
  robot_task: maintain following relationship

intended_robot_task: follow the lead human

intended_human_behavior: lead, navigating freely through the space at self-chosen pace and path

expected_behaviors:
  must:
    - avoid collision with the human, other pedestrians, and obstacles
    - not lose track of the human during turns or brief occlusions
  should:
    - maintain a socially comfortable following distance
    - smoothly track the human's turns without cutting corners
    - stop promptly when the human stops
    - recover gracefully after temporary loss of line of sight
  should_not:
    - follow so closely that the human feels physically crowded
    - follow so far behind that the human is lost at a turn or in a crowd
    - cut through obstacles or other pedestrians to preserve distance
    - overtake or lead when the human only pauses briefly

relevant_principles:
  - P1  # Safety — collision risk with the human, bystanders, and obstacles
  - P2  # Comfort — following distance directly affects the human's comfort
  - P6  # Agent Understanding — predicting the human's turning and pacing intent
  - P8  # Contextual Appropriateness — following distance should adapt to crowd density and space width

ideal_outcome: robot follows the person continuously, maintaining an appropriate distance without losing track of them

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
    - PathLength
  quality_metrics:
    - P2  # Comfort
    - P6  # Agent Understanding
  failure_modes:
    - robot loses track of the human at a turn or in a crowd
    - robot follows too closely, crowding the human
    - robot lags so far behind that following relationship breaks down
    - robot cuts corners or clips obstacles while tracking a turn
  labeling_criteria:
    - robot is in a servant/follower role relative to a single leading human
    - the human's path is not predetermined and may change direction or pace freely
    - the robot's trajectory is derived from tracking the human rather than an independent goal

evaluation_notes: >
  This scenario should be evaluated over a sustained trajectory rather than
  a single conflict point, unlike most other Table 3 scenarios. Evaluators
  should sample multiple turns, pace changes, and (if applicable) brief
  occlusions within a single episode to assess consistency of following
  behavior, not just a single snapshot of distance-keeping.

  Following distance norms are context-dependent (P8): a narrow hallway may
  require closer following than a wide plaza to avoid losing the human at a
  turn, while a crowded space may require a different balance between
  proximity and collision avoidance with third parties.

  This scenario is related to Accompany Peer (Figure 7, not in Table 3),
  which involves side-by-side co-navigation rather than following from
  behind, and to Leading, its role-reversed counterpart where the robot
  leads and the human follows.
```

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Leading*: the role-reversed counterpart, where the robot leads and the human follows.
- *Accompany Peer* (Figure 7 variant): side-by-side co-navigation with a peer, rather than trailing from behind.

**Suggested variants:**
- Following through a crowded space, testing robustness to occlusion and third-party avoidance
- Following at a running or brisk pace vs. a leisurely stroll
- Human deliberately testing the robot (sudden stops, sharp turns, doubling back)

**Key measurement question:** Does the robot maintain a stable, comfortable following distance across turns and pace changes, or does its behavior degrade (crowding, lagging, corner-cutting) under those conditions even if it performs acceptably on straight, steady-pace segments?
