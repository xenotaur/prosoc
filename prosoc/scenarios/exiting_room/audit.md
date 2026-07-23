---
scenario: exiting_room
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-22
---

# Audit: Exiting Room

- **Scenario:** `prosoc/scenarios/exiting_room/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready for AUDITED, no blocking or should-fix issues found

## Findings

### 1. `relevant_principles` omits P7 despite an explicit deadlock/hesitation theme — suggestion
- **Section/field:** `relevant_principles` (currently P1, P3, P5, P6) vs. `expected_behaviors.should_not` ("hesitate indefinitely at the threshold") and `scenario_usage_guide.failure_modes` ("prolonged stand-off with neither agent moving through the doorway")
- **Issue:** Per `.claude/skills/_shared/principles.md`, P7 (Proactivity) is specifically for scenarios where "deadlock or hesitation is the core challenge." This scenario names indefinite hesitation and stand-off as an explicit failure mode and unacceptable behavior, which is a reasonable match for P7, but P7 isn't listed.
- **Recommended fix:** Consider adding P7 to `relevant_principles` (and possibly `scenario_usage_guide.quality_metrics`) if a human editor agrees the deadlock-avoidance angle is principal enough to call out explicitly; not required since P3/P5/P6 already partially cover the same ground via legibility and priority-timing.

## Source Fidelity

SOURCE cites P&G Paper Table 3 plus Robotics at Google (R@G), internal scenario reference. Compared against `.claude/skills/_shared/pg_scenarios.md`'s "Exiting Room" entry (Doorway Scenarios section):

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | Robot exits a room while a human enters | Robot exits while human enters through same doorway | Match |
| Physical Env | Indoor | `context.environment.type: indoor` | Match |
| Geometric Layout | Room and door | `geometric_layout: room and door` | Match |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Match |
| Robot Task | Navigate in to out | `intended_robot_task: navigate from inside to outside the room` | Match |
| Human Behavior | Navigate in to out (as literally transcribed in Table 3) | `intended_human_behavior: navigate from outside to inside the room` | Discrepancy — already flagged and resolved by the card's own `evaluation_notes` |
| Ideal Outcome | Robot exits first | `ideal_outcome: robot exits the room first, then the human enters...` | Match |
| Related Scenarios | Exiting Elevator (R@G) | `related_scenarios: [entering_room, narrow_doorway]` in YAML; Exiting Elevator discussed in prose ("Notes for Scenario Designers and Evaluators") but not machine-readable, since it has no Table 3 entry/scenario directory of its own | Consistent — the two YAML entries are corpus-internal siblings (both directories exist under `prosoc/scenarios/`), Exiting Elevator remains prose-only because it isn't an implemented scenario |
| Cited In | R@G — Robotics at Google, an internal scenario reference (not a public citation index) | `cited_in: ["Robotics at Google (R@G), internal scenario reference"]` | Match |

The Human Behavior field discrepancy is unchanged from prior audits: Table 3 as transcribed in the reference data literally reads "Navigate in to out" for Human Behavior, identical to the Robot Task field, which is inconsistent with the Description ("human enters") and the Ideal Outcome ("robot exits first"). The card's `evaluation_notes` continues to identify this exact inconsistency, attribute it to a probable transcription error in the source, and state that the card follows the Description/Ideal Outcome reading (human enters, i.e., "outside to inside") rather than the literal Human Behavior field text — asking a human editor to verify against the original paper PDF if available. This remains a reasonable, transparently-documented interpretive call, not a fabricated fidelity claim.

All other fields, including `related_scenarios` and `cited_in`, match cleanly.

## Completeness

Scenario Card Summary: all fields present and rendered — Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios (`entering_room`, `narrow_doorway`), and Cited In (`Robotics at Google (R@G), internal scenario reference`).

Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all present and non-trivial.

No required fields are blank. The dry-run distiller check (`scripts/distill/scenarios --scenario exiting_room --dry-run --show-diffs`) reported no diff and no schema validation errors, confirming `scenario.md` and `scenario.yml` are in sync.
