---
scenario: intersection_gesture_proceed
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-22
---

# Audit: Intersection – Gesture Proceed

- **Scenario:** `prosoc/scenarios/intersection_gesture_proceed/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready — no contradictions, no schema issues. The previously-flagged should-fix (missing `scenario_usage_guide` YAML block, with free-text quality-measures instead of P0–P9 IDs) is resolved: `scenario.yml` now carries a complete `scenario_usage_guide` (success_metrics, quality_metrics using proper P0–P9 IDs, failure_modes, labeling_criteria), and the standalone prose "Scenario Usage Guide" section now mirrors it in the corpus's standard structured bullet format rather than free-text prose. Two low-severity suggestions remain, unchanged from the prior audit.

## Findings

### 1. `expected_behaviors.should` / Quality Metrics edge toward a measurable-latency criterion — suggestion
- **Section/field:** `expected_behaviors.should` — "commit promptly to motion after the gesture"; the underlying "prompt response" concept implicit in the scenario's framing
- **Issue:** This remains qualitative ("promptly," not a numeric threshold), so it does not clearly violate P&G Guideline N6 over-specification as written. But timing/promptness is a recurring theme across the Overview, Normative Expectations, and failure modes ("hesitates excessively after permission is given"), and no qualitative anchor is given for what counts as acceptable, which could invite inconsistent labeling across evaluators.
- **Recommended fix:** No change strictly required; optionally clarify in `evaluation_notes` what a "prompt" response window looks like qualitatively (e.g. "within a natural conversational turn-taking pause") without introducing a hard numeric threshold.

### 2. Related Scenarios lists one more entry than the P&G source — suggestion
- **Section/field:** Scenario Card Summary / YAML `related_scenarios` vs. P&G Table 3
- **Issue:** P&G Table 3 lists only "Gesture Wait" as the related scenario for Intersection Gesture Proceed. This card additionally lists `intersection_no_gesture`. Both referenced IDs exist in the corpus (`intersection_gesture_wait/`, `intersection_no_gesture/` both present under `prosoc/scenarios/`), and both reciprocally list `intersection_gesture_proceed` back in their own `related_scenarios`, so this isn't a broken reference — just a reasonable, intentional broadening beyond what the source paper states.
- **Recommended fix:** No change required; noted for the human editor's awareness that this is an addition beyond the source, not an error.

## Prose/YAML Consistency and Schema Check

- `scripts/distill/scenarios --scenario intersection_gesture_proceed --dry-run --show-diffs` produced no diff and no schema errors — `scenario.yml` is in sync with the embedded YAML block in `scenario.md`.
- The prose "## Scenario Usage Guide" section (previously ad-hoc free text with measures like "Time between gesture and robot motion" and "Absence of oscillation or hesitation") has been replaced with the corpus's standard structured bullet format — Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria — and now matches the embedded YAML's `scenario_usage_guide` block exactly (SR/NoCollisions success metrics; P2/P3/P4 quality metrics; matching failure modes and labeling criteria).
- `scenario.yml`'s `scenario_usage_guide.quality_metrics` (`P2, P3, P4`) now uses proper P0–P9 principle IDs consistent with `relevant_principles` and with how `_shared/principles.md` describes the field ("Charter principles used specifically as quality metrics") — closing the content-model gap flagged as should-fix in the prior audit (2026-07-21).
- No contradictions found between prose (Overview, Social Navigation Context, Normative Expectations) and YAML (`agents`, `expected_behaviors`, `ideal_outcome`, `intended_robot_task`/`intended_human_behavior`).
- `relevant_principles` (P0, P1, P2, P3, P4) validate against P0–P9; count of 5 is within the 3–5 guideline, and P0's inclusion is well-founded by the Overview's explicit "balancing goal achievement with safety and comfort" language (per `_shared/principles.md`'s P0 selection guidance).
- `expected_behaviors` entries describe kinds of behavior ("commit promptly to motion after the gesture," "maintain a smooth and legible trajectory") rather than exact motions or numeric thresholds — no over-specification (P&G Guideline N6) flagged.
- `related_scenarios` (`intersection_gesture_wait`, `intersection_no_gesture`) — both directories exist under `prosoc/scenarios/` and reciprocally reference `intersection_gesture_proceed`; the broadening beyond P&G Table 3's single "Gesture Wait" citation is expected per the audit_checklist.md convention and self-documented in the card's own `evaluation_notes` (see Finding 2 / Source Fidelity).

## Source Fidelity

SOURCE is explicitly stated as "Principles and Guidelines for Social Robot Navigation (Table 3)," so it is checked directly against `_shared/pg_scenarios.md`'s "Intersection Gesture Proceed" entry:

| Field | P&G Table 3 | This scenario | Match? |
|---|---|---|---|
| Description | Robot told to proceed at intersection | Human explicitly gestures for robot to proceed; robot recognizes and crosses | Consistent — same interaction, elaborated |
| Physical Env | Indoor | Indoor | Match |
| Geometric Layout | Intersection | intersection | Match |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Match |
| Robot Role | Servant | servant | Match |
| Robot Task | Navigate A to B | navigate from A to B | Match |
| Human Behavior | Cross navigate (gesture proceed) | cross navigate (gesture proceed) | Exact match |
| Ideal Outcome | Robot goes first | human gestures the robot to proceed; robot goes first and both cross without collision | Match (elaborated) |
| Related Scenarios | Gesture Wait | intersection_gesture_wait, intersection_no_gesture | Consistent, appropriately broader (Finding 2) |
| Cited In | [126] | "126" | Match |

**Overall:** Full fidelity to the P&G source — no mismatches found. The new `scenario_usage_guide` block is an addition beyond Table 3's fields (which does not enumerate usage-guide metrics) and does not conflict with any Table 3 field.

## Completeness

Walked against `template.md`'s "Required for AUDITED scenarios" sections, checking both prose and the machine-readable YAML:

- **Scenario Card Summary** — all fields present and mirrored in `scenario.yml`: `id`, `name`, `summary`, `scientific_purpose`, `geometric_layout`, `agents.robot.role`, `intended_robot_task`, `intended_human_behavior`, `ideal_outcome`, `related_scenarios`, `cited_in` are all populated in both prose and YAML — complete.
- **Scenario Usage Guide** — all subsections (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria) are now complete and consistent in both prose and the machine-readable `scenario_usage_guide` YAML block. This closes the completeness gap flagged in the prior audit.

No fields were found to be reasonably blank in this scenario.
