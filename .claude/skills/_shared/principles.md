# Prosoc Social Navigation Principles and Metrics

## The Ten Principles (P0–P9)

This project's charter (`prosoc/charter/charter.md`, distilled to `prosoc/charter/charter.yml`)
defines **ten** principles, P0–P9. P1–P8 are the eight principles from the P&G paper (Francis et
al., 2025, "Principles and Guidelines for Evaluating Social Robot Navigation Algorithms", THRI
Vol. 14 No. 2); P0 and P9 are this project's own explicit extensions beyond the P&G paper.
`prosoc/charter/charter.md` is the sole source of truth for this list — verify against it (or its
generated `charter.yml`) if this table and the charter ever appear to disagree.

| ID | Name | Description |
|----|------|-------------|
| P0 | Goal Achievement | Attempt to achieve assigned navigation/task objectives, balanced against P1–P9 |
| P1 | Safety | Protect humans, other robots, and their environments from harm |
| P2 | Comfort | Do not create annoyance or stress in humans |
| P3 | Legibility | Behave so robot goals can be understood by others |
| P4 | Politeness | Be respectful and considerate of other agents |
| P5 | Social Competency | Comply with social norms for navigating in shared space |
| P6 | Agent Understanding | Predict and accommodate the behavior of other agents |
| P7 | Proactivity | Take the initiative to resolve potential deadlocks |
| P8 | Contextual Appropriateness | Behave properly in the current context |
| P9 | Prosocial Behavior | Improve the experience or success of other agents, even when not explicitly required |

**Important:** The schema enforces `^P[0-9]+$`, which permits P0–P9 (and, syntactically, higher
numbers). Only emit P0–P9 — do not invent principle IDs outside this set (e.g. P10+). If a
scenario involves a concept not captured by P0–P9, note it in `evaluation_notes` rather than
inventing a new ID.

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

- **P0 (Goal Achievement)** — include when task completion/efficiency is in explicit tension with the social principles
- **P1 (Safety)** — include whenever collision risk is plausible
- **P2 (Comfort)** — include whenever the robot's proximity or speed could cause stress
- **P3 (Legibility)** — include whenever the robot's intent might be unclear to a human
- **P4 (Politeness)** — include whenever turn-taking, yielding, or consideration is required
- **P5 (Social Competency)** — include whenever a cultural or contextual convention governs behavior
- **P6 (Agent Understanding)** — include whenever the robot must predict or model human intent
- **P7 (Proactivity)** — include specifically when deadlock or hesitation is the core challenge
- **P8 (Contextual Appropriateness)** — include when the appropriate behavior depends heavily on environment/task context
- **P9 (Prosocial Behavior)** — include when the scenario turns on discretionary, beyond-the-task helpfulness rather than mere compliance

Limit `relevant_principles` to the 3–5 most directly relevant. Including all ten dilutes meaning.

This is a soft guideline, not a hard cap: if a scenario's own prose (Overview,
Discussion, or `evaluation_notes`) explicitly names and discusses a principle
— e.g. analyzing a specific trade-off involving it, the way `movable_obstruction`'s
Discussion names "Trade-offs between Goal Achievement (P0) and prosocial
action" — include that principle even if the list grows past 5. A principle
the card's own text explicitly discusses is definitionally relevant; dropping
it solely to satisfy the count guideline would make `relevant_principles`
contradict the rest of the card.
