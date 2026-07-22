---
scenario: intersection_gesture_wait
verdict: not_ready
blocking: 1
should_fix: 0
suggestion: 2
audited: 2026-07-21
---

# Audit: Intersection – Gesture Wait

- **Scenario:** `prosoc/scenarios/intersection_gesture_wait/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Not ready — 1 blocking issue (`scenario_usage_guide` still entirely
  absent from the machine-readable spec). The prior should-fix (P0 dropped from
  `relevant_principles`) has been resolved by this session's restoration of P0.

This is a fresh point-in-time re-audit reflecting the current state of the scenario
(no changes to `scenario.md`/`scenario.yml` since the 2026-07-20 audit other than the
`relevant_principles` restoration of P0). It fully supersedes and replaces the
2026-07-20 audit below rather than patching it incrementally.

## Findings

### 1. `scenario_usage_guide` block still entirely missing from YAML — blocking
- **Section/field:** Scenario Usage Guide (prose) vs. `scenario_usage_guide` (YAML) — required for AUDITED per `template.md`
- **Issue:** The rendered "Scenario Usage Guide" section restates Ideal Outcome and explicitly lists Success Metrics, Quality Metrics, Failure Modes, and Labeling Criteria as "Remaining gaps." The embedded/distilled YAML still has no `scenario_usage_guide` key at all — not even empty placeholders. Unchanged from the prior audit (still blocking).
- **Recommended fix:** Author `scenario_usage_guide.success_metrics` (e.g. `SR`, `NoCollisions` are directly applicable), `quality_metrics` (candidates: `P0`–`P4`, mirroring the now-restored `relevant_principles`), `failure_modes` (readily draftable from the existing `evaluation_notes` text — "ignoring the gesture," "partial compliance that introduces ambiguity," "delayed responses"), and `labeling_criteria` (needs fresh authoring, less directly inferable).

## Resolved Since Prior Audit

**P0 restored to `relevant_principles` (previously should-fix, now resolved).**
`relevant_principles` is now `P0, P1, P2, P3, P4` (5 entries, still within the 3–5
soft-guidance band). The prior audit flagged P0's absence as likely a mistake, since
the Scenario Overview explicitly states the robot must prioritize "safety, comfort,
and social compliance over immediate goal progress" and `evaluation_notes` says
success "prioritizes deference and safety over efficiency" — a textbook P0-inclusion
case per `_shared/principles.md`'s guidance ("include when task completion/efficiency
is in explicit tension with the social principles"). P0 has been restored, and per
this session's update to `_shared/principles.md`, the 3–5 count is explicitly a soft
guideline that yields when a scenario's own prose names and discusses a principle —
which applies here regardless of count. No further action needed on this point.

## Findings carried forward as suggestions (unchanged)

### 2. Related Scenarios lists one more entry than P&G Table 3 — suggestion
- **Section/field:** Scenario Card Summary "Related Scenarios" / `related_scenarios` vs. `_shared/pg_scenarios.md`
- **Issue:** Table 3 lists only "Gesture Proceed" as the related scenario for Intersection Gesture Wait. This card lists both `intersection_gesture_proceed` and `intersection_no_gesture`. Likely a reasonable corpus-level enrichment (all three intersection variants are natural comparators, and the scenario's own Notes section already discusses comparison with both) rather than an error, but it goes beyond what the cited source specifies.
- **Recommended fix:** No action required if the addition is intentional; consider noting "per P&G Table 3" vs. "additional corpus cross-reference" if precision matters for future source-fidelity checks. (Note: this is also tracked corpus-wide as part of the deferred `related_scenarios`/`cited_in` backfill follow-up.)

### 3. Consider whether P6 (Agent Understanding) applies — suggestion
- **Section/field:** `relevant_principles`
- **Issue:** The scenario's core mechanic is the robot recognizing and correctly interpreting an explicit human gesture — arguably a case of predicting/accommodating another agent's communicated intent, which is P6's definition ("Predict and accommodate the behavior of other agents"). Currently P0–P4 are listed; P6 is not.
- **Recommended fix:** Optional — if the editor judges gesture *recognition* (a perception/interpretation task) as materially different from behavior *prediction*, P6 can reasonably stay excluded. Flagging for a second opinion, not a required change. Adding P6 would bring the count to 6, which is acceptable under the soft-guidance rule only if the card's prose is updated to explicitly discuss the prediction/accommodation angle — currently it isn't, so this stays a suggestion rather than a should-fix.

## Source Fidelity

Checked against `_shared/pg_scenarios.md`'s "Intersection Gesture Wait" entry (P&G Table 3):

| Field | Table 3 | This card | Match |
|---|---|---|---|
| Physical Env | Indoor | indoor | Yes |
| Geometric Layout | Intersection | intersection | Yes |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Yes |
| Robot Role | Servant | servant | Yes |
| Robot Task | Navigate A to B | navigate from A to B | Yes |
| Human Behavior | Cross navigate (gesture wait) | cross navigate (gesture wait) | Yes |
| Ideal Outcome | Human goes, then robot | human gestures the robot to wait; human crosses first, then robot proceeds without collision | Yes — consistent, elaborated |
| Related Scenarios | Gesture Proceed | intersection_gesture_proceed, intersection_no_gesture | Partial — see Finding 2 |
| Cited In | [126] | "126" | Yes |

No contradictions found.

## Completeness

`scripts/distill/scenarios --scenario intersection_gesture_wait --dry-run --show-diffs`
reports no diff and no schema errors — `scenario.md`'s embedded YAML and
`scenario.yml` are in sync and schema-valid, and `relevant_principles: [P0, P1, P2,
P3, P4]` is consistent between both files.

**Scenario Card Summary** (required for AUDITED): Scenario Name, Description,
Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task,
Human Behavior, Ideal Outcome, Related Scenarios, Cited In — all present. Success
Metrics and Quality Metrics — still blank, should-fill-in-now (the card itself
already self-flags these as "Remaining gaps").

**Scenario Usage Guide** (required for AUDITED): Ideal Outcome present (restated
from Card Summary). Success Metrics, Quality Metrics, Failure Modes, Labeling
Criteria — all blank, both in prose and absent from the YAML entirely (Finding 1).
Failure Modes and Quality Metrics are should-fill-in-now (directly inferable from
`evaluation_notes` and `relevant_principles` respectively). Labeling Criteria leans
should-fill-in-now but requires genuine new authoring rather than transcription.

Prose vs. YAML consistency (Scenario Overview, Social Navigation Context, Normative
Expectations against `intended_robot_task`, `intended_human_behavior`, `agents`,
`expected_behaviors`, `ideal_outcome`): no contradictions or drift found.
`expected_behaviors` entries describe kinds of behavior, not exact motions or
numeric thresholds — no over-specification (N6) issues.

## Change Summary vs. 2026-07-20 Audit

The 2026-07-20 audit recorded blocking:1, should_fix:1, suggestion:2. The single
should-fix (P0 dropped from `relevant_principles` despite prose satisfying its
inclusion criterion) is now resolved — P0 has been restored, per the project owner's
explicit direction to include a principle when the scenario's own prose specifically
discusses it, even past the 3–5 count guidance. The blocking `scenario_usage_guide`
gap is unchanged and remains blocking. The two suggestions (extra `related_scenarios`
entry; possible P6 applicability) are unchanged. Net: blocking:1, should_fix:0,
suggestion:2 — down from should_fix:1.
