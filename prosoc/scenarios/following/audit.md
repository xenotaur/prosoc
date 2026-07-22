---
scenario: following
verdict: ready
blocking: 0
should_fix: 0
suggestion: 0
audited: 2026-07-21
---

# Audit: Following

- **Scenario:** `prosoc/scenarios/following/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready for AUDITED, no issues found

## Findings

No findings. The should-fix item from the 2026-07-20 audit (missing `related_scenarios`/`cited_in` in the machine-readable YAML) has been resolved: `scenario.yml` now carries `related_scenarios: [leading]` and `cited_in: ["50"]`, and the Scenario Card Summary renders both accordingly.

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
| Related Scenarios | Accompany Peer | `related_scenarios: [leading]` in YAML; Accompany Peer discussed in prose ("Notes for Scenario Designers and Evaluators") but not machine-readable, since it is a Figure-7 concept with no implemented scenario directory of its own | Consistent — `leading` is the corpus-internal, implemented sibling; Accompany Peer remains prose-only because it isn't an implemented scenario |
| Cited In | [50] | `cited_in: ["50"]` | Match |

The "Follow lead robot" vs. "follow the lead human" divergence is unchanged from prior audits: the card's `evaluation_notes` includes an explicit "Ambiguity note" stating that "Follow lead robot" appears to be a transcription slip in Table 3 given the Description field ("A robot follows a person"), and that the card follows the Description's reading. This remains a reasonable, transparently-documented interpretive call, not a fabricated fidelity claim.

All other fields, including the newly backfilled `related_scenarios` and `cited_in`, match cleanly.

## Completeness

Scenario Card Summary: all fields present and rendered — Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios (`leading`), and Cited In (`50`). This resolves the should-fix finding from the 2026-07-20 audit.

Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all present and non-trivial.

No required fields are blank. `relevant_principles` (P1, P2, P6, P8) and `scenario_usage_guide.quality_metrics` (P2, P6) remain valid P0–P9 entries, 4 and 2 respectively — within the recommended 3–5 range, no under- or over-specification. The dry-run distiller check (`scripts/distill/scenarios --scenario following --dry-run --show-diffs`) reported no diff and no schema validation errors, confirming `scenario.md` and `scenario.yml` are in sync.
