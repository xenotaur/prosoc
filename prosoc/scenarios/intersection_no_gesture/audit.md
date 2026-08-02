---
family: scenarios
card: intersection_no_gesture
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-08-02
---

# Audit: Intersection – No Gesture

- **Card:** `prosoc/scenarios/intersection_no_gesture/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's
  2026-07-25 edit, and is superseded by this pass)
- **Verdict:** Ready, one minor suggestion

## Findings

### 1. "Normative Expectations" prose omits the two `must`-level behaviors — suggestion
- **Section/field:** Normative Expectations (prose) vs. `expected_behaviors.must`
- **Issue:** The prose section explicitly lists the three `should` behaviors
  ("approaching... at a moderated speed," "yielding when right-of-way is
  ambiguous," "clearly committing to a trajectory") and the three
  `should_not` behaviors, but never explicitly states the two `must`
  behaviors ("avoid collision with the human," "behave conservatively when
  right-of-way is ambiguous") as their own bullets. Both ideas are present
  elsewhere in the card (collision-avoidance via `ideal_outcome` and the
  Scenario Overview's "without collision"; conservative behavior via the
  Social Navigation Context's "Humans generally expect... to behave
  conservatively and predictably"), so this is drift in presentation, not
  a contradiction or omission of substance.
- **Recommended fix:** Optionally add the two `must` behaviors as their own
  bullets under Normative Expectations for symmetry with `should`/`should_not`
  — not required for `AUDITED`.

## Source Fidelity

SOURCE cites P&G Table 3. Compared against `../_shared/pg_scenarios.md`'s
"Intersection No Gesture" entry: Physical Environment (Indoor), Geometric
Layout (Intersection), Scientific Purpose (Pedestrian interaction), Robot
Task ("Navigate A to B" / "navigate from A to B"), Human Behavior ("Cross
navigate"), Ideal Outcome ("Both pass, no collision" / "robot and human
both cross the intersection without collision, absent any explicit
gesture"), and Cited In (`[27, 50, 167]`) all match exactly. Table 3 lists
no "Related Scenarios" entry for this card, consistent with the card's own
`evaluation_notes` explicitly noting this and explaining why
`related_scenarios` adds `intersection_gesture_proceed` and
`intersection_gesture_wait` anyway (its own gesture-based counterparts —
an expected case per the checklist's `related_scenarios` convention, not a
defect). Both referenced directories exist under `prosoc/scenarios/`.

## Completeness

All required Scenario Card Summary fields present (Scenario Name,
Description, Scientific Purpose, Physical Environment, Geometric Layout,
Robot Role, Robot Task, Human Behavior, Ideal Outcome, Success/Quality
Metrics, Related Scenarios, Cited In). Scenario Usage Guide fully populated
(Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling
Criteria). No blank required fields.

`relevant_principles` (P0, P1, P2, P3, P4) — five valid P0–P9 IDs, at the
upper end of the recommended 3–5 range but each is discussed in the card's
own prose (P0 via goal-achievement/prosocial-norms balance in the
Overview; P1 via collision avoidance; P2/P3/P4 via the Quality Metrics and
Normative Expectations sections). `scenario_usage_guide.quality_metrics`
(P2, P3, P4) is a consistent subset. `expected_behaviors` entries describe
kinds of behavior ("moderated speed," "yielding," "committing") rather
than exact motions or numeric thresholds — no over-specification.
`scenario.yml` confirmed in sync with `scenario.md`
(`scripts/distill/scenarios --scenario intersection_no_gesture --dry-run
--show-diffs`, no diff).
