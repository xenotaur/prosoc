# Prosoc Social Navigation Principles and Metrics

## The Eight Principles (P1–P8)

These are the canonical social navigation principles from the P&G paper (Francis et al., 2025,
"Principles and Guidelines for Evaluating Social Robot Navigation Algorithms", THRI Vol. 14 No. 2).
Use ONLY these identifiers in `relevant_principles` and `quality_metrics` fields.

| ID | Name | Description |
|----|------|-------------|
| P1 | Safety | Protect humans, other robots, and their environments from harm |
| P2 | Comfort | Do not create annoyance or stress in humans |
| P3 | Legibility | Behave so robot goals can be understood by others |
| P4 | Politeness | Be respectful and considerate of other agents |
| P5 | Social Competency | Comply with social norms for navigating in shared space |
| P6 | Agent Understanding | Predict and accommodate the behavior of other agents |
| P7 | Proactivity | Take the initiative to resolve potential deadlocks |
| P8 | Contextual Appropriateness | Behave properly in the current context |

**Important:** The schema enforces `^P[0-9]+$`. Only emit P1–P8. Do not use P0 or invent other
principle IDs. If a scenario involves a principle not well-captured by P1–P8, note it in
`evaluation_notes` rather than inventing a new ID.

## Common Success Metrics

These are task-level metrics used in `scenario_usage_guide.success_metrics`:

| ID | Name | Description |
|----|------|-------------|
| SR | Success Rate | Fraction of episodes in which the robot reaches its goal |
| NoCollisions | No Collisions | Episodes completed without physical contact |
| PSC | Personal Space Comfort | Metric for maintaining appropriate proxemic distance |
| TTG | Time to Goal | Time taken to complete the navigation task |
| PathLength | Path Length | Total distance traveled by the robot |

Other metrics may be appropriate for specific scenarios; use plain English strings if a
standard abbreviation doesn't exist.

## Principle Selection Guidance

- **P1 (Safety)** — include whenever collision risk is plausible
- **P2 (Comfort)** — include whenever the robot's proximity or speed could cause stress
- **P3 (Legibility)** — include whenever the robot's intent might be unclear to a human
- **P4 (Politeness)** — include whenever turn-taking, yielding, or consideration is required
- **P5 (Social Norms)** — include whenever a cultural or contextual convention governs behavior
- **P6 (Agent Understanding)** — include whenever the robot must predict or model human intent
- **P7 (Proactivity)** — include specifically when deadlock or hesitation is the core challenge
- **P8 (Context)** — include when the appropriate behavior depends heavily on environment/task context

Limit `relevant_principles` to the 3–5 most directly relevant. Including all eight dilutes meaning.
