---
scenario: intersection_gesture_wait
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-22
---

# Audit: Intersection – Gesture Wait

- **Scenario:** `prosoc/scenarios/intersection_gesture_wait/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready, no blocking or should-fix issues found

This is a fresh point-in-time re-audit reflecting PR #31's addition of a full
`scenario_usage_guide` YAML block (success_metrics, quality_metrics, failure_modes,
labeling_criteria), which resolves the sole blocking finding from the prior
(2026-07-21) audit. It fully supersedes and replaces that audit below rather than
patching it incrementally.

## Findings

### 1. `related_scenarios` lists one more entry than P&G Table 3's single citation — suggestion
- **Section/field:** Scenario Card Summary "Related Scenarios" / `related_scenarios` vs. `.claude/skills/_shared/pg_scenarios.md`
- **Issue:** Not a defect — flagged for visibility only. Table 3 lists only "Gesture Proceed" as the related scenario for Intersection Gesture Wait; this card's `related_scenarios` also adds `intersection_no_gesture`. Per `audit_checklist.md`'s documented convention, this is an expected divergence (Table 3's Related Scenarios field is a single citation, not exhaustive), and the card's own `evaluation_notes` already self-documents the rationale explicitly citing this convention.
- **Recommended fix:** None required.

### 2. Consider whether P6 (Agent Understanding) applies — suggestion
- **Section/field:** `relevant_principles`
- **Issue:** The scenario's core mechanic is the robot recognizing and correctly interpreting an explicit human gesture — arguably touches P6's definition ("Predict and accommodate the behavior of other agents"). Currently `relevant_principles` is P0–P4; P6 is not included.
- **Recommended fix:** Optional — if the editor judges gesture *recognition* (a perception/interpretation task) as materially different from behavior *prediction*, P6 can reasonably stay excluded. Adding P6 would push the count to 6, acceptable under the soft-guidance rule only if the card's prose explicitly discusses the prediction/accommodation angle — it currently doesn't, so this remains a suggestion, not a should-fix.

## Source Fidelity

Checked against `.claude/skills/_shared/pg_scenarios.md`'s "Intersection Gesture Wait" entry (P&G Table 3):

| Field | Table 3 | This card | Match |
|---|---|---|---|
| Physical Env | Indoor | indoor | Yes |
| Geometric Layout | Intersection | intersection | Yes |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Yes |
| Robot Role | Servant | servant | Yes |
| Robot Task | Navigate A to B | navigate from A to B | Yes |
| Human Behavior | Cross navigate (gesture wait) | cross navigate (gesture wait) | Yes |
| Ideal Outcome | Human goes, then robot | human gestures the robot to wait; human crosses first, then robot proceeds without collision | Yes — consistent, elaborated |
| Related Scenarios | Gesture Proceed | intersection_gesture_proceed, intersection_no_gesture | Partial — see Finding 1 (expected divergence) |
| Cited In | [126] | "126" | Yes |

No contradictions found.

## Completeness

`scripts/distill/scenarios --scenario intersection_gesture_wait --dry-run --show-diffs`
reports no diff and no schema errors — `scenario.md`'s embedded YAML and
`scenario.yml` are in sync and schema-valid.

**Scenario Card Summary** (required for AUDITED): Scenario Name, Description,
Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task,
Human Behavior, Ideal Outcome, Related Scenarios, Cited In, Success Metrics, Quality
Metrics — all present.

**Scenario Usage Guide** (required for AUDITED): Success Metrics (SR, NoCollisions),
Quality Metrics (P2, P3, P4), Ideal Outcome, Failure Modes (3 entries), Labeling
Criteria (3 entries) — all now present in both the embedded YAML `scenario_usage_guide`
block and the standalone prose section. This closes the gap that was the sole
blocking finding in the prior audit; no blank required fields remain.

Prose vs. YAML consistency (Scenario Overview, Social Navigation Context, Normative
Expectations against `intended_robot_task`, `intended_human_behavior`, `agents`,
`expected_behaviors`, `ideal_outcome`): no contradictions or drift found.
`expected_behaviors` entries describe kinds of behavior, not exact motions or numeric
thresholds — no over-specification (N6) issues. `relevant_principles` (P0–P4, 5
entries) and `scenario_usage_guide.quality_metrics` (P2–P4) are both valid P0–P9
subsets within the guideline range.

## Change Summary vs. Prior (2026-07-21) Audit

The prior audit recorded `not_ready`, blocking:1, should_fix:0, suggestion:2, with
the single blocking finding being the total absence of `scenario_usage_guide` from
the machine-readable spec (PR #31's target). That gap is now fully resolved: the
YAML `scenario_usage_guide` block (success_metrics, quality_metrics, failure_modes,
labeling_criteria) is present, schema-valid, and consistent with the parallel prose
"Scenario Usage Guide" section. No new should-fix issues were introduced by the
change. The two suggestions (extra `related_scenarios` entry; possible P6
applicability) carry forward unchanged. Net: `ready`, blocking:0, should_fix:0,
suggestion:2 — down from `not_ready`, blocking:1.
