# Scenario: Frontal Approach

## Status

- **STATE:** APPROVED
- **SOURCE:** P&G Paper, Table 3 "Frontal Approach" entry (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [50, 126, 167]
- **DRAFTED:** ChatGPT 5.2, 2026-01-02
- **EDITED:** render_sections.py, 2026-07-19
- **EDITED:** Claude (WI-CHARTER-SUPPLEMENT-SOURCE-FIXES), 2026-10-27 — reword the SOURCE entry for publication clarity
- **EDITED:** Claude (WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES), 2026-11-05 — label the bare "Cited In" citation-index list, reduce a repeated "navigation" in the Scenario Overview, reword an awkward evaluation-notes phrase, and fix a malformed quote-mark pair around an identifier
- **EDITED:** Claude (WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER), 2026-11-06 — reword two phrases that referenced internal development context meaninglessly to an external reader, independent of the project's retain-vs-filter decision for provenance generally
- **EDITED:** Claude (WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION), 2026-11-06 — demoted from APPROVED to EDITED: the 2026-11-06 edits above postdate this card's existing audit.md (2026-08-02), making the prior APPROVED state stale per project/focus/current_focus.md's audit-currency policy; pending re-audit and re-approval
- **EDITED:** Claude (WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION), 2026-11-07 — reworded SOURCE to cite the P&G Table 3 "Frontal Approach" entry explicitly, resolving the should-fix finding that the prior "not derived from a specific external citation" wording contradicted the card's own close fidelity to that table entry
- **AUDITED:** Claude (WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION), 2026-11-07 — fresh audit after the SOURCE fix above: verdict ready, 0 blocking, 0 should-fix, 1 suggestion; promoted EDITED → AUDITED
- **APPROVED:** Claude (WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION), 2026-11-07 (PR #136) — human-confirmed re-approval closing out the 2026-11-06 demotion; promoted AUDITED → APPROVED

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
- **Cited In:** P&G references 50, 126, and 167

---

## Scenario Overview

This scenario describes a canonical social navigation conflict in which a robot and a human approach each other in opposite directions in a narrow hallway where neither agent has an explicit right-of-way. Successful navigation depends on sensing and agile movement, while successful social navigation may additionally require trajectory prediction, interpreting intent, resolving hesitation, and resolving conflicts. The scenario tests social navigation principles including safety, comfort, legibility, following social norms, and agent understanding.

---

## Scenario Specification (Machine-Readable)

```yaml
id: frontal_approach_01
name: Frontal Approach
state: APPROVED

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
  This scenario evaluates how well the robot navigates through shared space with a human under the conditions of a mild, typical conflict.
  Changing direction, slowing down, braking or hesitation may be acceptable if they increase safety, comfort, or legibility, but  prolonged deadlock, abrupt reversals,
  or aggressive advancement are indicative of poor performance.

  The scenario assumes a pedestrian with a typical level of awareness,
  neither oblivious to the presence of the robot nor overly attentive to it.

  Related Scenarios note: P&G Table 3 lists "Ped. Obstruct" as this
  scenario's related entry, which has no implemented scenario directory
  under src/prosoc/prnc/scenarios/. "related_scenarios" instead references
  blind_corner, movable_obstruction, and single_file_hallway, which this
  corpus's own scenario set explicitly treats as a progressively
  constrained variant series of this scenario. This reflects a deliberate
  divergence from P&G Table 3's single-citation convention, consistent
  with how this corpus treats closely related scenario variants, not an
  inconsistency.

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
