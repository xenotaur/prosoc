# Scenario: <Short Descriptive Title>

This scenario describes a **social navigation situation** in which a robot operates in a shared human environment. It is intended to capture the *context*, *agents*, and *normative expectations* relevant to evaluating robot navigation behavior under the Prosocial Navigation Charter.

Use this template as a starting point when authoring new scenario cards. Replace all placeholder text (`<...>`) with scenario-specific content, and remove sections that are not applicable. Avoid over-specifying details unless they are essential to the scenario’s intent.

---

```yaml
id: <unique_scenario_id>
name: <Human-readable scenario name>

summary: >
  <Brief natural-language description of the scenario and why it is
  socially or evaluatively interesting. Focus on the coordination
  challenge rather than implementation details.>

context:
  environment:
    type: <indoor | outdoor | mixed | other>
    setting: <e.g., hallway, lobby, sidewalk, plaza>
    width: <qualitative description, e.g., narrow, wide>
  social_setting:
    formality: <formal | informal | mixed>
    crowd_level: <low | medium | high>

agents:
  robot:
    role: navigating_agent
    capabilities:
      - <capability_1>
      - <capability_2>
  humans:
    - role: <pedestrian | group_member | bystander | other>
      count: <integer >= 1>
      attributes:
        <attribute_key>: <attribute_value>

initial_conditions:
  <key>: <value>

expected_behaviors:
  must:
    - <Behavior that is required for acceptable performance>
  should:
    - <Behavior that is preferred or encouraged>
  should_not:
    - <Behavior that is discouraged or unacceptable>

relevant_principles:
  - <Px>  # e.g., P1 Safety, P3 Legibility

 evaluation_notes: >
  <Guidance for evaluators on how to interpret behavior in this scenario.
  Note acceptable trade-offs, common failure modes, and assumptions
  about human behavior or context.>
```

---

## Discussion

This section may be used to elaborate on the intent of the scenario, discuss known variants, or explain how this scenario relates to others in the library. It should remain **descriptive rather than prescriptive** and is intended primarily for human readers.

Possible discussion topics include:
- Why this scenario is challenging or representative
- Known edge cases or ambiguities
- Suggested scenario variants (e.g., different crowd levels, attentiveness)
- Cultural or contextual factors that may affect interpretation

---

## Authoring Notes

- Treat this scenario as a *contextual test case*, not a policy specification.
- Do not redefine charter principles here; instead, reference them via `relevant_principles`.
- Keep normative expectations confined to `expected_behaviors`.
- Prefer qualitative descriptions over precise numeric thresholds unless essential.
- Assume that evaluation may involve human judgment, automated analysis, or both.

All machine-readable content must appear inside the fenced YAML block above. Do not edit generated `.yml` files directly; they should be produced via the designated distillation tools.

