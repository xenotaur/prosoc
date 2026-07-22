# Scenario: Crash Cart

## Status

- **STATE:** DRAFTED
- **SOURCE:** P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in this article
- **DRAFTED:** Claude (new-scenario skill), 2026-07-05
- **EDITED:** render_sections.py, 2026-07-20

---

## Scenario Card Summary

- **Scenario Name:** Crash Cart
- **Scenario Description:** A robot in a leader role delivers an urgent medical product through an indoor environment (e.g., a hospital), moving with elevated pace and priority while signaling its urgent status to bystanders, and still avoiding collisions despite the time pressure.
- **Scientific Purpose:** interactive navigation
- **Physical Environment:** indoor
- **Geometric Layout:** passable space
- **Robot Role:** leader
- **Robot Task:** deliver the medical product urgently
- **Human Behavior:** bystanders yield to the passing robot; recipient receives the medical product upon arrival
- **Success Metrics:**
  - SR
  - NoCollisions
  - TTG
- **Quality Metrics:**
  - P3
  - P8
- **Ideal Outcome:** delivery of medicine to the recipient promptly and without collision or unsafe maneuvers
- **Related Scenarios:** object_handover
- **Cited In:** this article

---

## Scenario Overview

This scenario describes a robot in a **leader role** delivering an urgent medical product (analogous to a hospital "crash cart," used to rush critical supplies to a patient) through an indoor environment, with the goal of reaching a human recipient as quickly as safety allows. Unlike Object Handover, which emphasizes a calm, comfortable close-range interaction, Crash Cart introduces genuine time pressure: the delivery is urgent, and the robot's navigation priorities must shift accordingly, while still avoiding harm to bystanders.

The defining challenge is **balancing urgency against social navigation norms**: the robot should move with more assertiveness and speed than in a routine delivery scenario, signal its urgent status clearly to bystanders so they can accommodate it, and still avoid collisions or unsafe maneuvers even under time pressure.

Successful navigation requires the robot to move briskly through the indoor environment, communicate urgency to pedestrians and bystanders in its path (so they yield proactively), and deliver the medical product to the recipient promptly and safely.

---

## Social Navigation Context

Hospitals and similar settings have existing norms for urgent situations — humans generally understand and yield to visibly urgent movement (e.g., a nurse or attendant moving quickly with a crash cart), even though the same pace or assertiveness would be considered impolite in a routine context. A robot performing this task must be legible about its urgent status, since bystanders unfamiliar with robots may not otherwise infer that unusually fast or assertive movement is socially licensed.

Key challenges:

- **Context-dependent norm shift**: behavior that would be discourteous in a routine delivery (moving quickly, closely passing bystanders, taking priority at intersections) becomes appropriate, even expected, in this urgent context.
- **Communicating urgency**: since the robot cannot rely on bystanders recognizing "medical urgency" the way they would a running human in scrubs, it may need explicit signaling (visual, audible) to convey its priority status.
- **Safety under time pressure**: even with elevated priority, the robot must not increase actual collision risk — urgency justifies faster, more assertive navigation, not reduced caution.
- **Graceful degradation**: if bystanders do not yield despite signaling, the robot must still avoid collision, since safety is not suspended by urgency.

This scenario is scientifically interesting because it tests whether a robot's social navigation policy can be context-modulated by task priority (P8, Contextual Appropriateness) without abandoning baseline safety guarantees.

---

## Normative Expectations

Acceptable robot behavior includes:

- Moving at an elevated pace appropriate to the urgency of the delivery, faster than a routine task
- Clearly signaling urgent status (e.g., visual or audible cues) so bystanders can proactively yield
- Taking reasonable priority at intersections or shared spaces when signaling is acknowledged
- Maintaining collision avoidance and safe stopping distances despite the elevated pace

Unacceptable behavior includes:

- Moving at increased speed without any corresponding increase in legibility or signaling of urgency
- Forcing passage through bystanders who have not had a chance to yield
- Treating urgency as license to reduce safety margins or ignore collision risk
- Failing to revert to normal-priority behavior once the urgent delivery is complete

---

## Scenario Specification (Machine-Readable)

```yaml
id: crash_cart_01
name: Crash Cart

summary: >
  A robot in a leader role delivers an urgent medical product through an
  indoor environment (e.g., a hospital), moving with elevated pace and
  priority while signaling its urgent status to bystanders, and still
  avoiding collisions despite the time pressure.

scientific_purpose: interactive navigation

geometric_layout: passable space

context:
  environment:
    type: indoor
    setting: hospital or medical facility corridor
    width: moderate
  social_setting:
    formality: formal
    crowd_level: medium

agents:
  robot:
    role: leader
    capabilities:
      - forward_motion
      - steering
      - stopping
      - speed_adjustment
      - gesture_or_signal_output
  humans:
    - role: pedestrian
      count: 3
      attributes:
        mobility: typical
        awareness: typical
    - role: recipient
      count: 1
      attributes:
        mobility: stationary
        awareness: aware_of_incoming_delivery

initial_conditions:
  robot_position: starting point of an urgent delivery route
  human_positions: bystanders along the corridor, initially unaware of the specific urgency but expected to update upon perceiving the robot's signaling
  recipient_position: destination of the delivery route
  delivery_urgency: high
  destination: patient or recipient location

intended_robot_task: deliver the medical product urgently

intended_human_behavior: bystanders yield to the passing robot; recipient receives the medical product upon arrival

expected_behaviors:
  must:
    - avoid collision with bystanders despite elevated pace
    - deliver the medical product to the intended recipient
  should:
    - move at an elevated pace appropriate to the delivery's urgency
    - signal urgent status clearly to bystanders in its path
    - take reasonable priority at intersections when signaling is acknowledged
    - revert to normal-priority behavior once the delivery is complete
  should_not:
    - increase speed without corresponding urgency signaling
    - force passage through bystanders who have not yielded
    - reduce safety margins or collision-avoidance behavior due to time pressure

relevant_principles:
  - P1  # Safety — collision risk must not increase despite time pressure
  - P3  # Legibility — urgency must be clearly signaled to bystanders
  - P7  # Proactivity — taking priority appropriately to complete an urgent task
  - P8  # Contextual Appropriateness — navigation norms shift with task urgency

ideal_outcome: delivery of medicine to the recipient promptly and without collision or unsafe maneuvers

related_scenarios:
  - object_handover

cited_in:
  - "this article"

scenario_usage_guide:
  success_metrics:
    - SR
    - NoCollisions
    - TTG
  quality_metrics:
    - P3  # Legibility
    - P8  # Contextual Appropriateness
  failure_modes:
    - robot collides with or startles a bystander while moving urgently
    - robot moves quickly without signaling urgency, appearing reckless to bystanders
    - robot fails to complete the delivery within an acceptable time
    - robot continues urgent-priority behavior after the delivery is complete
  labeling_criteria:
    - the robot's task is a time-critical object delivery in an indoor setting
    - the robot's navigation priority is elevated relative to a routine delivery
    - bystanders are present who must be aware of and accommodate the robot's urgency

evaluation_notes: >
  This scenario is explicitly about context-dependent norm shifting: the
  same behaviors (fast pace, taking priority) that would be a failure mode
  in Object Handover or Frontal Approach are expected and appropriate here,
  provided they are matched with clear urgency signaling. Evaluators should
  calibrate expectations to the stated urgency level rather than applying
  routine-delivery norms.

  Because urgency does not suspend safety, evaluators should treat any
  collision or near-miss as a serious failure regardless of the time
  pressure — this scenario tests assertive-but-safe navigation, not
  reckless navigation.

  This scenario is related to Object Handover (the general delivery/handoff
  task without urgency) and to Food Delivery (a related but lower-urgency
  delivery context, not separately defined in Table 3).

  Related Scenarios note: P&G Table 3 lists "Food Delivery" as this
  scenario's related entry, which has no implemented scenario directory
  under prosoc/scenarios/. `related_scenarios` instead references
  object_handover, which this card's own Notes section already discusses.
  This is expected per the related_scenarios convention
  (prosoc-scenario-audit's audit_checklist.md), not a source-fidelity gap.
```

---

## Scenario Usage Guide

- **Success Metrics:**
  - SR
  - NoCollisions
  - TTG
- **Quality Metrics:**
  - P3
  - P8
- **Ideal Outcome:** delivery of medicine to the recipient promptly and without collision or unsafe maneuvers
- **Failure Modes:**
  - robot collides with or startles a bystander while moving urgently
  - robot moves quickly without signaling urgency, appearing reckless to bystanders
  - robot fails to complete the delivery within an acceptable time
  - robot continues urgent-priority behavior after the delivery is complete
- **Labeling Criteria:**
  - the robot's task is a time-critical object delivery in an indoor setting
  - the robot's navigation priority is elevated relative to a routine delivery
  - bystanders are present who must be aware of and accommodate the robot's urgency

---

## Notes for Scenario Designers and Evaluators

**Comparison with related scenarios:**
- *Object Handover*: the general delivery and handoff task without time pressure; Crash Cart specializes this to an urgent context with elevated navigation priority.
- *Food Delivery*: a related delivery context implied by the paper's "Related Scenarios" note, presumably with lower urgency and less pronounced priority-taking.

**Suggested variants:**
- Varying levels of urgency signaling (visual only, audible only, combined)
- Bystanders who are slow to notice or yield to the urgency signal
- Multiple simultaneous urgent deliveries competing for priority in the same corridor

**Key measurement question:** Does the robot's elevated pace and priority-taking come paired with clear, legible urgency signaling that lets bystanders accommodate it proactively, or does the robot simply move faster without giving bystanders a way to understand why?
