---
scenario: crowd_navigation
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-22
---

# Audit: Crowd Navigation

- **Scenario:** `prosoc/scenarios/crowd_navigation/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready — no blocking or should-fix issues found; one minor suggestion

## Findings

### 1. STATUS block's EDITED date does not reflect the latest edit — suggestion
- **Section/field:** Status block (`EDITED: render_sections.py, 2026-07-20`)
- **Issue:** `git log` shows the most recent edit to `scenario.md`/`scenario.yml` is commit `8b6ee81` ("Document and self-document the related_scenarios/Table 3 divergence convention", 2026-07-22), which added a "Related Scenarios note" paragraph to `evaluation_notes`. The STATUS block still shows only the prior `render_sections.py, 2026-07-20` entry and has not been updated to record this most recent pass.
- **Recommended fix:** Add an additional `EDITED` line (or update the existing one) noting the `evaluation_notes` self-documentation pass and its date/author, consistent with how the STATUS block tracks provenance elsewhere in the corpus.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "cited in various." Compared against `../../.claude/skills/_shared/pg_scenarios.md`'s "Crowd Navigation" entry (Crowd Scenarios section):

- **Description** ("A robot navigates through a crowd") — matches.
- **Physical Environment** (Generic) — matches (`context.environment.type: generic`).
- **Geometric Layout** (Passable space) — matches (`geometric_layout: passable space`).
- **Scientific Purpose** (Crowd navigation) — matches (`scientific_purpose: crowd navigation`).
- **Robot Task** (Navigate thru) — matches (`intended_robot_task: navigate through the crowd to a destination on the far side`).
- **Human Behavior** (Mill about) — matches (`intended_human_behavior: mill about, moving independently...`).
- **Ideal Outcome** (No collision/obstruction) — matches, with an added "steady progress" clause that is an elaboration rather than a contradiction.
- **Cited In** (Various) — matches (`cited_in: [various]`).
- **Related Scenarios**: Table 3 lists "Robot Crowding," which is a Figure 7 scenario with no implemented directory under `prosoc/scenarios/` (confirmed: no `robot_crowding` directory exists). The card's `related_scenarios` field instead references `parallel_traffic` and `perpendicular_traffic`, both implemented sibling scenarios that the card's own "Notes for Scenario Designers and Evaluators" section already discusses, and `evaluation_notes` now explicitly documents this substitution as expected per the `related_scenarios` convention in `audit_checklist.md`. Not a mismatch.

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" checklist:

- **Scenario Card Summary block** — fully present: Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, and Cited In are all filled in.
- **Scenario Usage Guide** (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria) — present as prose, mirroring the YAML `scenario_usage_guide` block.
- **`relevant_principles`** (P1, P2, P6, P7) — 4 entries, within the 3–5 guidance, all valid P0–P9.
- **`expected_behaviors`** — qualitative kind-of-behavior descriptions throughout (e.g. "thread through gaps," "maintain reasonable clearance"); no numeric-threshold or exact-motion over-specification found (P&G Guideline N6 satisfied).
- Prose vs. YAML cross-check (Scenario Overview / Social Navigation Context / Normative Expectations against `intended_robot_task`, `intended_human_behavior`, `agents`, `expected_behaviors`, `ideal_outcome`) found no contradictions or drift — both describe the same many-agent, low-predictability crossing task with 10 milling pedestrians and matching must/should/should_not lists.
- Single-scenario dry-run distill (`scripts/distill/scenarios --scenario crowd_navigation --dry-run --show-diffs`) reported no diff and no schema errors — `scenario.yml` is in sync with `scenario.md`.

No blank required fields.
