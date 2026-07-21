---
scenario: following_01
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 0
audited: 2026-07-20
---

# Audit: Following

- **Scenario:** `prosoc/scenarios/following/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes

## Findings

### 1. `related_scenarios` and `cited_in` fields absent from YAML — should-fix
- **Section/field:** Scenario Card Summary ("Related Scenarios," "Cited In" — currently listed under "Remaining gaps") and the machine-readable `related_scenarios` / `cited_in` YAML keys (present in `schema.json` and `template.md` but omitted from `scenario.yml`)
- **Issue:** The rendered Card Summary itself flags both as gaps ("should-fill-in-now"), and the prose already supplies the content needed to fill them: the "Notes for Scenario Designers and Evaluators" section names Leading (role-reversed counterpart) and Accompany Peer as related scenarios, and `../_shared/pg_scenarios.md`'s Following entry lists "Related Scenarios: Accompany Peer" and "Cited In: [50]" (also present in the card's own STATUS/SOURCE line). Neither is captured in the machine-readable spec.
- **Recommended fix:** Add `related_scenarios: [leading_01, accompany_peer_01]` (whichever precise IDs the corpus uses — `accompany_peer` may not yet exist as an implemented scenario, in which case omit or note it as a Figure-7 concept) and `cited_in: ["50"]` to the YAML block, then re-render the Card Summary's Related Scenarios / Cited In lines to match.

## Source Fidelity

SOURCE cites P&G Paper Table 3, cited in [50]. Compared against `../_shared/pg_scenarios.md`'s "Following" entry (Interpersonal Scenarios section):

| Field | Table 3 | This card | Match? |
|---|---|---|---|
| Description | A robot follows a person | Robot in servant role follows a leading human | Match |
| Physical Env | Generic | `context.environment.type: generic` | Match |
| Geometric Layout | Walking space | `geometric_layout: walking space` | Match |
| Scientific Purpose | Joint navigation | `scientific_purpose: joint navigation` | Match |
| Robot Role | Servant | `agents.robot.role: servant` | Match |
| Robot Task | Follow lead robot | `intended_robot_task: follow the lead human` | Divergence, explicitly addressed — see below |
| Human Behavior | Lead human | `intended_human_behavior: lead, navigating freely through the space...` | Match |
| Ideal Outcome | Robot follows person | `ideal_outcome: robot follows the person continuously...` | Match |
| Related Scenarios | Accompany Peer | Covered in prose only, not YAML (Finding 1) | Present in prose, not machine-readable |
| Cited In | [50] | STATUS block cites "[50]"; not in YAML `cited_in` (Finding 1) | Present in STATUS, not machine-readable |

This is a change from the prior audit (2026-07-05), which flagged the "Follow lead robot" reference-table wording as an unremarked discrepancy (suggestion-level finding) and recommended the card add an `evaluation_notes` entry documenting it, similar to how `exiting_room` handles its own Table 3 ambiguity. That gap has since been closed: the card's `evaluation_notes` now includes an explicit "Ambiguity note" stating that "Follow lead robot" appears to be a transcription slip given the Description field ("A robot follows a person"), and that the card follows the Description's reading. This is a reasonable, transparently-documented interpretive call, not a fabricated fidelity claim, and it directly matches the reference data available in this repo. No further action needed on this point.

All other fields match cleanly.

## Completeness

Scenario Card Summary: Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, and Ideal Outcome are all now present and rendered (new since the prior audit, which found the whole section missing as standalone prose). Related Scenarios and Cited In remain blank, and the rendered summary itself now explicitly labels them "should-fill-in-now" — see Finding 1.

Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all present as a standalone rendered section (also new since the prior audit) and are non-trivial.

No other required fields are blank. `relevant_principles` (P1, P2, P6, P8) and `scenario_usage_guide.quality_metrics` (P2, P6) remain valid P0–P9 entries, 4 and 2 respectively — within the recommended 3–5 range for `relevant_principles`, no under- or over-specification. The dry-run distiller check (`scripts/distill/scenarios --scenario following --dry-run --show-diffs`) reported no diff and no schema validation errors, confirming `scenario.md` and `scenario.yml` are in sync.
