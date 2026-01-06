# Social Navigation Scenario Template

This template defines the recommended structure for authoring **social navigation scenarios** in the Prosoc project.

Scenarios authored using this template are intended to be:
- human-readable and reviewable,
- machine-readable via embedded YAML,
- auditable against the Prosocial Navigation Charter,
- and compatible with the scenario definitions in the *Principles and Guidelines for Social Robot Navigation* paper.

Authors are encouraged to treat this template as a scaffold. Not all sections are required at early stages, but **AUDITED** scenarios should include all sections marked as such.

---

## Status

> **Required for all scenarios**

- **STATE:** DRAFTED  
- **SOURCE:** <paper, URL, dataset, or prior scenario>  
- **DRAFTED:** <author or system, date>  
- **EDITED:** <optional>  
- **AUDITED:** <optional>  
- **VALIDATED:** <optional>

See `workflow.md` for definitions of lifecycle states.

---

## Scenario Card Summary

> **Required for AUDITED scenarios**  
> Mirrors Table 3 of the P&G paper.

- **Scenario Name:** <concise, canonical name>
- **Scenario Description:** <1–2 sentence physical description of the interaction>
- **Physical Environment:** <Indoor / Outdoor>
- **Geometric Layout:** <Intersection / Corridor / Sidewalk / …>
- **Scientific Purpose:** <e.g., pedestrian interaction, legibility, safety>
- **Robot Role:** <Any / Leader / Follower / …>
- **Robot Task:** <e.g., Navigate from A to B>
- **Human Behavior:** <e.g., Cross navigate, gesture wait, gesture proceed>
- **Ideal Outcome:** <concise outcome statement>
- **Related Scenarios:** <list, if any>
- **Cited In:** <references, if applicable>

---

## Scenario Overview

> **Required**

Provide a clear, human-readable description of the scenario. This section should explain:
- what the robot and human(s) are doing,
- where the interaction occurs,
- and why coordination or social judgment is required.

Avoid technical jargon where possible; this section should be understandable without the YAML specification.

---

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

---

## Scenario Specification (Machine-Readable)

> **Required**

This section contains the machine-readable YAML specification for the scenario. It must conform to `schema.json`.

```yaml
id: <unique_scenario_id>
name: <scenario_name>

summary: >
  <Concise physical description of the interaction>

scientific_purpose: >
  <What this scenario is intended to study or evaluate>

context:
  environment:
    type: <indoor|outdoor>
    setting: <text description>
  social_setting:
    formality: <informal|formal|mixed>
    crowd_level: <low|medium|high>

agents:
  robot:
    role: <navigating_agent|leader|follower|any>
    capabilities:
      - <capability>
  humans:
    - role: <pedestrian|group>
      count: <integer>
      attributes:
        <key>: <value>

initial_conditions:
  <key>: <value>

intended_robot_task: <e.g., navigate from A to B>
intended_human_behavior: <e.g., cross navigate, gesture wait>

expected_behaviors:
  must:
    - <required behavior>
  should:
    - <preferred behavior>
  should_not:
    - <prohibited behavior>

relevant_principles:
  - P0
  - P1


evaluation_notes: >
  <High-level guidance for evaluators>
```

---

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

---

## Notes for Scenario Designers and Evaluators

> **Optional**

Include any additional guidance, variants, or cautions relevant to interpretation or reuse of the scenario.

