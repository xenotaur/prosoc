---
scenario: intersection_gesture_wait
verdict: not_ready
blocking: 1
should_fix: 1
suggestion: 2
audited: 2026-07-20
---

# Audit: Intersection – Gesture Wait

- **Scenario:** `prosoc/scenarios/intersection_gesture_wait/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Not ready — 1 blocking issue (required Scenario Usage Guide content entirely unpopulated in the machine-readable spec) plus one principle-selection should-fix.

This is a full re-audit reflecting this session's edits (Card Summary/Usage Guide
prose rendered in; `scientific_purpose`, `geometric_layout`, `intended_robot_task`,
`intended_human_behavior`, `ideal_outcome`, `related_scenarios`, `cited_in` authored
from P&G Table 3; Robot Role corrected from `navigating_agent` to `servant`;
`relevant_principles` trimmed from 6 to 4). It supersedes and fully replaces the
2026-07-05 audit below.

## Findings

### 1. `scenario_usage_guide` block still entirely missing from YAML — blocking
- **Section/field:** Scenario Usage Guide (prose) vs. `scenario_usage_guide` (YAML) — required for AUDITED per `template.md`
- **Issue:** The rendered "Scenario Usage Guide" section now restates Ideal Outcome and explicitly lists Success Metrics, Quality Metrics, Failure Modes, and Labeling Criteria as "Remaining gaps." The embedded/distilled YAML still has no `scenario_usage_guide` key at all — not even empty placeholders. This is unchanged from the prior audit (previously Finding 3, blocking) and remains a required-for-AUDITED gap.
- **Recommended fix:** Author `scenario_usage_guide.success_metrics` (e.g. `SR`, `NoCollisions` are directly applicable), `quality_metrics` (candidates: `P1`–`P4`, mirroring `relevant_principles`, once Finding 2 below is resolved), `failure_modes` (readily draftable from the existing `evaluation_notes` text — "ignoring the gesture," "partial compliance that introduces ambiguity," "delayed responses"), and `labeling_criteria` (needs fresh authoring, less directly inferable).

### 2. `relevant_principles` drops P0 despite prose explicitly describing a goal-vs-social tension — should-fix
- **Section/field:** `relevant_principles` (now `P1, P2, P3, P4`, trimmed this session from `P0, P1, P2, P3, P4, P9`)
- **Issue:** Per `_shared/principles.md`, P0 (Goal Achievement) should be included "when task completion/efficiency is in explicit tension with the social principles." The Scenario Overview explicitly states the robot must prioritize "safety, comfort, and social compliance over immediate goal progress," and `evaluation_notes` says success "prioritizes deference and safety over efficiency, reinforcing trust and predictability." Both are textbook P0 inclusion cases per the shared guidance, yet P0 was removed in this session's trim from 6 to 4 principles.
- **Recommended fix:** Re-add `P0` to `relevant_principles` (5 principles, still within the 3–5 guidance band), or, if the omission is intentional, add a sentence to `evaluation_notes` clarifying why the explicit goal-tension language doesn't warrant P0. P9's removal, by contrast, looks correct — this scenario is externally-triggered compliance, not discretionary beyond-task helpfulness — no fix needed there. The prior 6-principle set's over-count (suggestion-level, previously Finding 6) is now resolved by the trim; only the specific choice of *which* principles to drop is in question.

### 3. Related Scenarios lists one more entry than P&G Table 3 — suggestion
- **Section/field:** Scenario Card Summary "Related Scenarios" / `related_scenarios` vs. `_shared/pg_scenarios.md`
- **Issue:** Table 3 lists only "Gesture Proceed" as the related scenario for Intersection Gesture Wait. This card lists both `intersection_gesture_proceed` and `intersection_no_gesture`. Likely a reasonable corpus-level enrichment (all three intersection variants are natural comparators, and the scenario's own Notes section already discusses comparison with both) rather than an error, but it goes beyond what the cited source specifies.
- **Recommended fix:** No action required if the addition is intentional; consider noting "per P&G Table 3" vs. "additional corpus cross-reference" if precision matters for future source-fidelity checks.

### 4. Consider whether P6 (Agent Understanding) applies — suggestion
- **Section/field:** `relevant_principles`
- **Issue:** The scenario's core mechanic is the robot recognizing and correctly interpreting an explicit human gesture — arguably a case of predicting/accommodating another agent's communicated intent, which is P6's definition ("Predict and accommodate the behavior of other agents"). Currently only P1–P4 are listed.
- **Recommended fix:** Optional — if the editor judges gesture *recognition* (a perception/interpretation task) as materially different from behavior *prediction*, P6 can reasonably stay excluded. Flagging for a second opinion, not a required change.

## Source Fidelity

Checked against `_shared/pg_scenarios.md`'s "Intersection Gesture Wait" entry (P&G Table 3):

| Field | Table 3 | This card | Match |
|---|---|---|---|
| Physical Env | Indoor | indoor | Yes |
| Geometric Layout | Intersection | intersection | Yes |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Yes |
| Robot Role | Servant | servant | Yes — this session's role correction (`navigating_agent` → `servant`) resolves the prior audit's blocking Robot Role finding |
| Robot Task | Navigate A to B | navigate from A to B | Yes |
| Human Behavior | Cross navigate (gesture wait) | cross navigate (gesture wait) | Yes |
| Ideal Outcome | Human goes, then robot | human gestures the robot to wait; human crosses first, then robot proceeds without collision | Yes — consistent, elaborated. Also resolves the prior audit's finding that `ideal_outcome` was missing from the YAML entirely |
| Related Scenarios | Gesture Proceed | intersection_gesture_proceed, intersection_no_gesture | Partial — see Finding 3 |
| Cited In | [126] | "126" | Yes |

No contradictions found. Compared with the 2026-07-05 audit, the Robot Role
correction and the newly-authored `ideal_outcome`/Card Summary fields resolve what
were previously the audit's blocking and should-fix source-fidelity findings.

## Completeness

`scripts/distill/scenarios --scenario intersection_gesture_wait --dry-run --show-diffs`
reports no diff and no schema errors — `scenario.md`'s embedded YAML and
`scenario.yml` are in sync and schema-valid.

**Scenario Card Summary** (required for AUDITED): Scenario Name, Description,
Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task,
Human Behavior, Ideal Outcome, Related Scenarios, Cited In — all now present (this
resolves the prior audit's Finding 4, "missing Scenario Card Summary section
entirely"). Success Metrics and Quality Metrics — still blank, should-fill-in-now
(the card itself already self-flags these as "Remaining gaps").

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

## Change Summary vs. 2026-07-05 Audit

The prior audit (after its 2026-07-05 correction notice) recorded blocking:1,
should_fix:2, suggestion:1 — the blocking finding was the missing
`scenario_usage_guide` block, and the should-fix findings were the missing Scenario
Card Summary section and the Robot Role drift (`navigating_agent` vs. source's
`servant`). This session's edits resolved the Scenario Card Summary and Robot Role
findings entirely, and authored a previously-missing `ideal_outcome` field. The
`scenario_usage_guide` gap remains unresolved and stays blocking here — it is still
completely absent from the YAML, unchanged from the prior audit. The principle trim
from 6 to 4 introduced a new should-fix finding (dropping P0 despite prose that
satisfies its inclusion criterion) not present in the prior audit; the prior
suggestion about the 6-principle set being one over the 3–5 guidance band is now
moot since the count dropped to 4.
