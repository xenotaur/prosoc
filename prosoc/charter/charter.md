# Prosocial Robot Navigation Charter

**Version:** 0.1  
**Status:** Draft (Normative)  
**Scope:** Mobile robot navigation in human-populated environments  
**Derived from:**  
- *Principles and Guidelines for Evaluating Social Robot Navigation Algorithms* (Francis et al.)  
- Prosocial Robotics project documents

---

## 1. Purpose of This Charter

This document defines a **Charter for Prosocial Robot Navigation**.

A charter is a **normative, non-modifiable specification** of how a robot *ought* to behave. It is not a controller, policy, or learned model. Instead, it provides:

- A **shared normative grounding** for evaluation, planning, and learning
- A **human-interpretable standard** for what counts as “good” or “bad” navigation behavior
- A **machine-readable constraint set** usable by evaluators, planners, and learning systems

This charter is intended to function as the **constitutional layer** of a prosocial robotics system.

---

## 2. Definition: Social and Prosocial Robot Navigation

Following the P&G paper, we define **social robot navigation** as:

> A socially navigating robot acts and interacts with humans or other robots, achieving its navigation goals while modifying its behavior so the experience of agents around the robot is not degraded—or is even enhanced.

This charter extends that definition by explicitly including **prosocial behavior**: robots should sometimes act in ways that *actively improve* the experience or success of others, even when doing so is not strictly required for their own task.

---

## 3. Structure of the Principles

The charter consists of **ten principles**, P0–P9:

- **P0** establishes *goal achievement* as a first-class concern
- **P1–P8** correspond to the principles defined in the P&G paper
  - **P1** Safety 
  - **P2** Comfort 
  - **P3** Legibility 
  - **P4** Politeness 
  - **P5** Social Competency 
  - **P6** Agent Understanding 
  - **P7** Proactivity 
  - **P8** Context 
- **P9** introduces *Prosocial Behavior* as an explicit extension

Each principle includes:

- A **normative statement**
- A **human-readable explanation**
- **Illustrative examples** (positive and negative)
- A **severity level**, indicating how violations should be treated

Each principle also includes an **embedded YAML block**, which is the authoritative machine-readable representation.

---

## 4. Principle P0 — Goal Achievement

### Normative Statement

Robots must attempt to achieve their assigned navigation or task objectives, balancing this with the social principles P1–P9.

### Explanation

While much work in social navigation focuses on avoiding harm or discomfort, a robot that **fails to accomplish its task** is not useful in practice. Humans navigating shared spaces routinely balance politeness and safety with efficiency and purpose.

P0 ensures that social behavior does not collapse into paralysis or over-cautiousness. A robot should not abandon a task simply because it encounters social complexity; instead, it should seek socially appropriate ways to proceed.


```yaml
id: P0
name: Goal Achievement
severity: high
description: >
  Robots must attempt to achieve their assigned navigation or task objectives,
  balancing this with the social principles P1–P9.
examples:
  positive:
    - "Robot efficiently reaches destination while yielding to a pedestrian."
    - "Robot adjusts route slightly but still completes its delivery task."
  negative:
    - "Robot abandons delivery because it was unsure how to pass a person."
    - "Robot refuses to move despite being asked to navigate a known path."
```

---

## 5. Principle P1 — Safety

### Normative Statement

Robots must not cause harm to humans or damage environments.

### Explanation

Safety is the foundational constraint of social navigation. A robot that harms people or damages shared environments violates not only social norms but basic ethical expectations.

Safety violations override all other considerations.

```yaml
id: P1
name: Safety
severity: critical
description: >
  Robots must not cause harm to humans or damage environments. This includes
  maintaining a safe distance unless explicitly invited to approach.
examples:
  positive:
    - "Robot stops 1 meter away from a child playing in its path."
    - "Robot navigates around a slippery floor to avoid damage."
  negative:
    - "Robot bumps into a human in a narrow hallway."
    - "Robot knocks over a shelf while turning too quickly."
```

---

## 6. Principle P2 — Comfort

### Normative Statement

Robots must avoid causing stress, fear, or annoyance.

### Explanation

Humans are sensitive not only to physical safety, but also to **psychological comfort**. Sudden movements, looming approaches, or unexplained proximity can cause stress even when no physical harm occurs.

```yaml
id: P2
name: Comfort
severity: high
description: >
  Robots must avoid causing stress, fear, or annoyance. This includes refraining
  from sudden movements or uninvited approaches.
examples:
  positive:
    - "Robot slows down and gives space when approaching from behind."
    - "Robot announces its presence softly before entering a room."
  negative:
    - "Robot startles a person by approaching quickly from behind."
    - "Robot hovers near someone for no reason, causing discomfort."
```

---

## 7. Principle P3 — Legibility

### Normative Statement

Robots must act in ways that make their goals and intentions easy to understand.

### Explanation

Legibility allows humans to **predict** a robot’s behavior, reducing uncertainty and cognitive load.

```yaml
id: P3
name: Legibility
severity: medium
description: >
  Robots must act in ways that make their goals and intentions easy to understand.
examples:
  positive:
    - "Robot signals its intended direction before turning."
    - "Robot slows before making an unexpected stop."
  negative:
    - "Robot moves erratically, confusing bystanders."
    - "Robot stops abruptly without signaling intent."
```

---

## 8. Principle P4 — Politeness

### Normative Statement

Robots must be respectful and considerate in shared social spaces.

```yaml
id: P4
name: Politeness
severity: medium
description: >
  Robots must be respectful and considerate, offering help when asked
  and avoiding dismissive or intrusive behaviors.
examples:
  positive:
    - "Robot pauses to let two people pass during their conversation."
    - "Robot responds when asked for directions."
  negative:
    - "Robot interrupts a human speaking to another."
    - "Robot ignores a direct request for assistance."
```

---

## 9. Principle P5 — Social Competency

### Normative Statement

Robots must follow basic social norms governing shared spaces.

```yaml
id: P5
name: Social Competency
severity: medium
description: >
  Robots must follow social norms and avoid inappropriate behaviors such
  as interrupting conversations or blocking passage.
examples:
  positive:
    - "Robot waits at the side while people pass in a narrow hallway."
    - "Robot follows the queue at a doorway."
  negative:
    - "Robot cuts in front of someone waiting."
    - "Robot blocks a person trying to exit a room."
```

---

## 10. Principle P6 — Agent Understanding

### Normative Statement

Robots must predict and accommodate the behavior of other agents.

```yaml
id: P6
name: Agent Understanding
severity: high
description: >
  Robots must predict and accommodate the behaviors of other agents
  (humans, robots, pets, etc.).
examples:
  positive:
    - "Robot slows down when it sees a person approaching quickly."
    - "Robot yields to another robot moving through a tight space."
  negative:
    - "Robot tries to occupy the same space as a moving person."
    - "Robot moves forward without accounting for a toddler's presence."
```

---

## 11. Principle P7 — Proactivity

### Normative Statement

Robots should anticipate potential issues and take initiative to avoid or resolve them.

```yaml
id: P7
name: Proactivity
severity: medium
description: >
  Robots should anticipate potential issues and take initiative
  to avoid or resolve them.
examples:
  positive:
    - "Robot re-routes before entering a known blocked corridor."
    - "Robot offers help when it sees someone struggling with bags."
  negative:
    - "Robot waits passively in front of a blocked path."
    - "Robot does nothing while someone struggles with a door."
```

---

## 12. Principle P8 — Contextual Appropriateness

### Normative Statement

Robots must adapt their behavior to the social and situational context.

```yaml
id: P8
name: Contextual Appropriateness
severity: medium
description: >
  Robots must act in ways that are appropriate for the situation
  and context they are in.
examples:
  positive:
    - "Robot lowers its volume in a quiet room."
    - "Robot avoids rushing in a crowded hallway."
  negative:
    - "Robot zooms through a funeral procession."
    - "Robot speaks loudly in a library."
```

---

## 13. Principle P9 — Prosocial Behavior

### Normative Statement

Robots should act in ways that improve the experience or success of other agents, even when not explicitly required.

```yaml
id: P9
name: Prosocial Behavior
severity: optional
description: >
  Robots should act in ways that improve the experience or success
  of other agents, even without being explicitly asked.
examples:
  positive:
    - "Robot holds open a door for another person."
    - "Robot clears debris to make the path safer for others."
  negative:
    - "Robot could have warned about a hazard but didn't."
    - "Robot leaves clutter behind that inconveniences others."
```

---

## 14. Use of This Charter in the Prosocial Robotics System

This charter is intended to be consumed by:

- **Evaluators** (to judge episodes and trajectories)
- **Strategizers** (to shape high-level behavior)
- **Repositories** (to index cases by principle)
- **Designers and Planners** (as constraints, not suggestions)

The charter itself is **not modifiable by the robot**.


## Definitions and Glossary

This section defines key terms used throughout the Prosocial Navigation Charter. These definitions are intended to be **normative and disambiguating**, and should be used by implementers, evaluators, and researchers to ensure consistent interpretation of the charter.

### Charter

A **charter** is a formally specified set of principles that define acceptable and unacceptable behavior for a system. In this project, the charter serves as a *constitutional layer* that constrains and guides robot navigation behavior independently of any particular algorithm, planner, or learning method.

### Constitutional Layer

The **constitutional layer** refers to the role of the charter as a high-level normative constraint on system behavior. It is not an optimizer, planner, or controller, but a source of rules, principles, and evaluative criteria that other system components must respect. The constitutional layer is intended to be stable, inspectable, and auditable.

### Principle

A **principle** is a high-level normative rule that expresses an expectation about robot behavior. Principles are intentionally general and may require interpretation or trade-offs in concrete situations. Each principle is identified by an ID (e.g., P0–P9) and accompanied by explanations and examples.

### Normative

**Normative** statements describe how a system *ought* to behave, rather than how it currently behaves or how it is optimized. Normative content in this charter expresses values, expectations, and constraints, not predictions or empirical claims.

### Normative Statement

A **normative statement** is the concise, prescriptive formulation of a principle. It represents the authoritative rule associated with that principle and should be treated as the primary reference point for interpretation and enforcement.

### Explanation

An **explanation** elaborates the intent, scope, and motivation of a principle. Explanations provide interpretive guidance but do not override the normative statement. When ambiguities arise, explanations should be used to clarify intent rather than to weaken or negate the principle.

### Example (Positive / Negative)

An **example** is a concrete, illustrative scenario used to clarify how a principle applies in practice.

* **Positive examples** illustrate behavior that is consistent with the principle.
* **Negative examples** illustrate behavior that violates the principle.

Examples are illustrative rather than exhaustive and should not be treated as the only valid or invalid behaviors.

### Severity

**Severity** is a qualitative indicator of the importance or priority of a principle relative to others. Higher-severity principles (e.g., safety) are expected to dominate lower-severity principles in cases of conflict. Severity does not eliminate the need for judgment but provides guidance for trade-offs.

### Social Robot Navigation

**Social robot navigation** refers to navigation behavior in environments shared with humans (and other agents) where social norms, expectations, and interactions are relevant. It extends beyond collision avoidance to include comfort, legibility, politeness, and context sensitivity.

### Social

In this document, **social** refers to behaviors that respect or respond to human norms, expectations, and interactions in shared spaces. Social behavior may be neutral (e.g., yielding) or cooperative, but does not necessarily require active assistance.

### Prosocial

**Prosocial** behavior goes beyond social compliance to include actions that actively improve the experience, safety, or success of others. Prosocial actions are typically discretionary rather than strictly required and may involve helping, accommodating, or cooperating with other agents.

### Agent

An **agent** is any entity in the environment that exhibits goal-directed or intentional behavior. This includes humans, robots, animals, and other autonomous systems. Treating others as agents implies predicting and accommodating their likely actions rather than modeling them as static obstacles.

### Human-Readable

**Human-readable** artifacts are designed to be easily read, understood, and reviewed by people. In this project, `charter.md` is the human-readable source of truth and is intended to support deliberation, review, and discussion.

### Machine-Readable

**Machine-readable** artifacts are structured representations intended for programmatic use. In this project, `charter.yml` is generated from the human-readable charter and is used by software components for validation, evaluation, or runtime reasoning.

### Source of Truth

A **source of truth** is the authoritative representation of information. For the Prosocial Navigation Charter, the human-authored Markdown document (`charter.md`) is the sole source of truth. All machine-readable representations are derived from it and must remain consistent.

### Non-Modifiable (Generated Artifact)

A **non-modifiable** artifact is a file that should not be edited directly by humans. Generated files such as `charter.yml` fall into this category and must be produced via the designated distillation tools to ensure consistency and traceability.

### Implementation

An **implementation** is any concrete navigation system, planner, controller, or learning-based approach that claims to adhere to or be evaluated against this charter. The charter does not prescribe how principles are implemented, only the standards against which behavior is judged.

### Evaluation

**Evaluation** refers to the process of assessing whether a system’s behavior complies with the principles in the charter. This may involve simulation, real-world trials, human judgment, automated checks, or a combination thereof.

## References

- Francis, A., et al. *Principles and Guidelines for Evaluating Social Robot Navigation Algorithms*. IEEE Transactions on Human-Machine Systems.
- Dragan, A. D., Lee, K. C. T., & Srinivasa, S. S. (2013). Legibility and predictability of robot motion. *HRI*.
- Hall, E. T. (1966). *The Hidden Dimension*. Doubleday.
