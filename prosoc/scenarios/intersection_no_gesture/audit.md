---
scenario: intersection_no_gesture
verdict: ready
blocking: 0
should_fix: 0
suggestion: 3
audited: 2026-07-22
---

# Audit: Intersection – No Gesture

- **Scenario:** `prosoc/scenarios/intersection_no_gesture/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-22
- **Verdict:** Ready, no blocking or should-fix issues found

This is a fresh point-in-time re-audit reflecting PR #31's addition of a full
`scenario_usage_guide` YAML block (success_metrics, quality_metrics, failure_modes,
labeling_criteria), which resolves the sole blocking finding from the prior
(2026-07-21) audit. It fully supersedes and replaces that audit below rather than
patching it incrementally.

## Findings

### 1. `relevant_principles` omits P6/P7 despite prose language that fits them — suggestion
- **Section/field:** `relevant_principles` (`P0, P1, P2, P3, P4`)
- **Issue:** At 5 entries this sits at the top of the 3–5 guidance band, not over it, so this stays suggestion-level. The prose repeatedly emphasizes "implicit coordination," "mutual anticipation of trajectories," and avoiding "oscillate indecisively" — language that maps closely to P6 (Agent Understanding — predicting the human's trajectory/intent) and P7 (Proactivity — resolving ambiguity/deadlock without hesitation). Neither is listed.
- **Recommended fix:** Optional — human editor may consider swapping in P6 or P7 for one of the current five, without exceeding the guidance band.

### 2. Possible mild over-specification in `expected_behaviors.should_not` — suggestion
- **Section/field:** `expected_behaviors.should_not` vs. P&G Guideline N6 (over-specification)
- **Issue:** "oscillate indecisively at the intersection" and "force the human to stop abruptly" describe behavior kinds (fine); "aggressively assert right-of-way" borders on prescribing a specific strategy rather than a behavior category, though still mild.
- **Recommended fix:** Optional — may be left as-is; it still names a behavior class rather than an exact motion or numeric threshold.

### 3. Related Scenarios lists two entries where P&G Table 3 lists none — suggestion
- **Section/field:** Scenario Card Summary "Related Scenarios" / `related_scenarios` vs. `.claude/skills/_shared/pg_scenarios.md`
- **Issue:** Not a defect — flagged for visibility only. The Table 3 entry for "Intersection No Gesture" has no "Related Scenarios" field at all. This card's Card Summary and YAML list `intersection_gesture_proceed` and `intersection_gesture_wait`. Per `audit_checklist.md`'s documented convention, this is an expected divergence (Table 3's silence is not a claim that no relationship exists), and the card's own `evaluation_notes` already self-documents the rationale explicitly citing this convention.
- **Recommended fix:** None required.

## Source Fidelity

Checked against `.claude/skills/_shared/pg_scenarios.md`'s "Intersection No Gesture" entry (P&G Table 3):

| Field | Table 3 | This card | Match |
|---|---|---|---|
| Physical Env | Indoor | indoor | Yes |
| Geometric Layout | Intersection | intersection | Yes |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Yes |
| Robot Role | (not specified in Table 3) | navigating_agent | No conflict — source doesn't specify a role for this entry |
| Robot Task | Navigate A to B | navigate from A to B | Yes |
| Human Behavior | Cross navigate | cross navigate | Yes |
| Ideal Outcome | Both pass, no collision | robot and human both cross the intersection without collision, absent any explicit gesture | Yes — consistent, elaborated |
| Related Scenarios | (not specified in Table 3) | intersection_gesture_proceed, intersection_gesture_wait | See Finding 3 (expected divergence) |
| Cited In | [27, 50, 167] | "27", "50", "167" | Yes |

No contradictions found.

## Completeness

`scripts/distill/scenarios --scenario intersection_no_gesture --dry-run --show-diffs`
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

## Change Summary vs. Prior (2026-07-21) Audit

The prior audit recorded `not_ready`, blocking:1, should_fix:0, suggestion:3, with
the single blocking finding being the total absence of `scenario_usage_guide` from
the machine-readable spec (PR #31's target). That gap is now fully resolved: the
YAML `scenario_usage_guide` block (success_metrics, quality_metrics, failure_modes,
labeling_criteria) is present, schema-valid, and consistent with the parallel prose
"Scenario Usage Guide" section. No new should-fix issues were introduced by the
change. The three suggestions (possible P6/P7 principle additions; mild
over-specification in `should_not`; extra `related_scenarios` entries) carry forward
unchanged. Net: `ready`, blocking:0, should_fix:0, suggestion:3 — down from
`not_ready`, blocking:1.
