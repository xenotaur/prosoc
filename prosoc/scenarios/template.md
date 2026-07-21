# Scenario: Social Navigation Scenario Template

## STATUS: DRAFT 2026-01-06
- SOURCE: Prompt to ChatGPT 5.2
- DRAFTED: ChatGPT 5.2, 2026-01-02
- EDITED: Anthony Francis centaur@logicalrobotics.com, 2026-01-09

This template defines the recommended structure for authoring **social navigation scenarios** in the Prosoc project. A social navigation scenario describes a situation in which a navigating robot operates in a shared human environment, and is designed to capture the context, agents, roles, tasks, evaluation criteria, and normative expectations relevant to evaluating robot navigation behavior in sufficient detail to recognize scenarios in data or to set up scenarios for evaluation.

Scenarios authored using this template are intended to be:
- human-readable and reviewable as a coherent Markdown document,
- machine-readable via embedded YAML within that document,
- machine-validatable against the scenario JSON schema,
- auditable against the Prosocial Navigation Charter,
- and compatible with the scenario definitions in the *Principles and Guidelines for Social Robot Navigation* paper.

Use this template as a starting point when authoring new scenario cards. Authors are encouraged to treat this template as a scaffold. Replace all placeholder text (`<...>`) with scenario-specific content, and remove sections that are not applicable. Avoid over-specifying details unless they are essential to the scenario’s intent. Not all sections are required at early stages, but **AUDITED** scenarios should include all sections marked as such.

## Status

> **Required for all scenarios**

- **STATE:** DRAFTED  
- **SOURCE:** <paper, URL, dataset, or prior scenario>  
- **DRAFTED:** <author or system, date>  
- **EDITED:** <optional>  
- **AUDITED:** <optional>  
- **VALIDATED:** <optional>

See [`workflow.md`](workflow.md) for definitions of lifecycle states.

## Scenario Card Summary

> **Required for AUDITED scenarios**  
> Drawn from Tables 2 and 3 of the P&G paper.

- **Scenario Name:** <concise, canonical name>
- **Scenario Description:** <1–2 sentence physical description of the interaction>
- **Scientific Purpose:** <e.g., pedestrian interaction, legibility, safety>
- **Physical Environment:** <Indoor / Outdoor>
- **Geometric Layout:** <Intersection / Corridor / Sidewalk / …>
- **Robot Role:** <Any / Leader / Follower / …>
- **Robot Task:** <e.g., Navigate from A to B>
- **Human Behavior:** <e.g., Cross navigate, gesture wait, gesture proceed>
- **Success Metrics:** <list, if any>
- **Quality Metrics:** <list, if any>
- **Ideal Outcome:** <concise outcome statement>
- **Related Scenarios:** <list, if any>
- **Cited In:** <references, if applicable>

## Scenario Overview

> **Required**

Provide a clear, human-readable description of the scenario. This section should explain:
- what the robot and human(s) are doing,
- where the interaction occurs,
- and why coordination or social judgment is required.

Avoid technical jargon where possible; this section should be understandable without the YAML specification.

## Social Navigation Context

> **Optional but recommended**

Describe the broader social or behavioral context of the scenario, including:
- common human expectations,
- sources of ambiguity or asymmetry,
- and why this scenario is socially or scientifically interesting.

---

## Normative Expectations

> **Optional but recommended**

Describe acceptable and unacceptable robot behaviors in natural language. This section provides interpretive guidance beyond the formal specification.

## Scenario Specification (Machine-Readable)

> **Required**

This section contains the machine-readable YAML specification for the scenario. It must conform to `schema.json`.

```yaml
id: <unique_scenario_id>
name: <Human-Readable Scenario Name>

summary: >
  <Concise physical description of the interaction>

scientific_purpose: >
  <What this scenario is intended to study or evaluate>

context:
  environment:
    type: <Environment Type, e.g., indoor | outdoor | mixed | other>
    setting: <Physical Layout, e.g., hallway, lobby, sidewalk, plaza>
    width: <Qualitative Description, e.g., narrow, wide>
  social_setting:
    formality: <Social Formality, e.g., informal | formal | mixed>
    crowd_level: <Crowd Level, e.g., low | medium | high>

agents:
  robot:
    role: <Robot Role, e.g., navigating_agent | leader | follower | any>
    capabilities:
      - <Capability>
  humans:
    - role: <Human Role, e.g., pedestrian | group>
      count: <integer>
      attributes:
        <Attribute>: <Value>

initial_conditions:
  <Key>: <Value>

intended_robot_task: <Robot Task, e.g., navigate from A to B>
intended_human_behavior: <Human Behavior, e.g., cross navigate, gesture wait>

expected_behaviors:
  must:
    - <Behavior that is required for acceptable performance>
  should:
    - <Behavior that is encouraged or preferred>
  should_not:
    - <Behavior that is discouraged or unacceptable>

relevant_principles:
  - <Principle>

ideal_outcome: <concise outcome statement>

related_scenarios:
  - <scenario-directory-name>  # e.g. frontal_approach -- the directory/key used in audit.md and AUDIT_SUMMARY.md, not scenario.yml's suffixed id

cited_in:
  - <reference>             # external works or citation indices referencing this scenario

scenario_usage_guide:
  success_metrics:
    - <metric-id>            # e.g., SR, NoCollisions
  quality_metrics:
    - <principle-id>         # e.g., P2, P3
  failure_modes:
    - <failure-description>  # e.g., collision with human
  labeling_criteria:
    - <criterion-description>

evaluation_notes: >
  <Guidance for evaluators on how to interpret behavior in this scenario.
  Note acceptable trade-offs, common failure modes, and assumptions
  about human behavior or context. Optionally, describe why it is
  socially or evaluatively interesting. Focus on the coordination
  challenge rather than implementation details unless they are
  relevant to the evaluation.>
```

## Scenario Usage Guide

> **Required for AUDITED scenarios**

### Success Metrics

List objective criteria indicating successful execution of the scenario.

### Quality Metrics

List secondary or graded measures (e.g., smoothness, timing, legibility).

### Ideal Outcome

Describe the ideal unfolding of the interaction in concrete terms.

### Failure Modes

Enumerate common or critical ways the scenario can fail.

### Labeling Criteria

Provide guidance for annotators or evaluators on how to label outcomes.

## Notes for Scenario Designers and Evaluators

> **Optional**

Include any additional guidance, variants, or cautions relevant to interpretation or reuse of the scenario.

