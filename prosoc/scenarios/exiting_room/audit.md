---
scenario: exiting_room
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-07-20
---

# Audit: Exiting Room

- **Scenario:** `prosoc/scenarios/exiting_room/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. `related_scenarios` and `cited_in` fields absent from YAML — should-fix
- **Section/field:** Scenario Card Summary ("Related Scenarios," "Cited In" — currently listed under "Remaining gaps") and the machine-readable `related_scenarios` / `cited_in` YAML keys (present in `schema.json` and `template.md` but omitted from `scenario.yml`)
- **Issue:** The rendered Card Summary itself flags both as gaps ("should-fill-in-now"), and the prose already supplies the content needed to fill them: the "Notes for Scenario Designers and Evaluators" section names Entering Room, Exiting Elevator, and Narrow Doorway as related scenarios, and `../_shared/pg_scenarios.md`'s Exiting Room entry lists "Cited In: R@G." Neither is captured in the machine-readable spec, so tooling that reads `related_scenarios`/`cited_in` (e.g. cross-scenario consistency checks) can't see this information even though a human reading the prose would know it.
- **Recommended fix:** Add `related_scenarios: [entering_room_01, narrow_doorway_01]` (or whichever precise IDs the corpus uses) and `cited_in: ["R@G"]` to the YAML block, then re-render the Card Summary's Related Scenarios / Cited In lines to match.

### 2. `relevant_principles` omits P7 despite an explicit deadlock/hesitation theme — suggestion
- **Section/field:** `relevant_principles` (currently P1, P3, P5, P6) vs. `expected_behaviors.should_not` ("hesitate indefinitely at the threshold") and `scenario_usage_guide.failure_modes` ("prolonged stand-off with neither agent moving through the doorway")
- **Issue:** Per `../_shared/principles.md`, P7 (Proactivity) is specifically for scenarios where "deadlock or hesitation is the core challenge." This scenario names indefinite hesitation and stand-off as an explicit failure mode and unacceptable behavior, which is a reasonable match for P7, but P7 isn't listed.
- **Recommended fix:** Consider adding P7 to `relevant_principles` (and possibly `scenario_usage_guide.quality_metrics`) if a human editor agrees the deadlock-avoidance angle is principal enough to call out explicitly; not required since P3/P5/P6 already partially cover the same ground via legibility and priority-timing.

## Source Fidelity

SOURCE cites P&G Paper Table 3 plus Robots@Games (R@G). Compared against `../_shared/pg_scenarios.md`'s "Exiting Room" entry (Doorway Scenarios section):

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | Robot exits a room while a human enters | Robot exits while human enters through same doorway | Match |
| Physical Env | Indoor | `context.environment.type: indoor` | Match |
| Geometric Layout | Room and door | `geometric_layout: room and door` | Match |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Match |
| Robot Task | Navigate in to out | `intended_robot_task: navigate from inside to outside the room` | Match |
| Human Behavior | Navigate in to out (as literally transcribed in Table 3) | `intended_human_behavior: navigate from outside to inside the room` | Discrepancy — already flagged and resolved by the card's own `evaluation_notes` |
| Ideal Outcome | Robot exits first | `ideal_outcome: robot exits the room first, then the human enters...` | Match |
| Related Scenarios | Exiting Elevator (R@G) | Not in YAML (see Finding 1); mentioned only in prose | Present in prose, not machine-readable |
| Cited In | R@G | Not in YAML (see Finding 1) | Present in Status block's SOURCE line, not `cited_in` |

The Human Behavior field discrepancy is unchanged from before this session's edits: Table 3 as transcribed in the reference data literally reads "Navigate in to out" for Human Behavior, identical to the Robot Task field, which is inconsistent with the Description ("human enters") and the Ideal Outcome ("robot exits first"). The card's `evaluation_notes` continues to identify this exact inconsistency, attribute it to a probable transcription error in the source, and state that the card follows the Description/Ideal Outcome reading (human enters, i.e., "outside to inside") rather than the literal Human Behavior field text — asking a human editor to verify against the original paper PDF if available. This remains a reasonable, transparently-documented interpretive call, not a fabricated fidelity claim.

All other fields match cleanly.

## Completeness

Scenario Card Summary: Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, and Ideal Outcome are all now present and rendered (this is new since the prior audit — the section did not previously exist as standalone prose). Related Scenarios and Cited In remain blank, and the rendered summary itself now explicitly labels them "should-fill-in-now" — see Finding 1.

Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all present as a standalone rendered section (also new since the prior audit) and are non-trivial.

No other required fields are blank. The dry-run distiller check (`scripts/distill/scenarios --scenario exiting_room --dry-run --show-diffs`) reported no diff and no schema validation errors, confirming `scenario.md` and `scenario.yml` are in sync.
