---
scenario: intersection_no_gesture_01
verdict: not_ready
blocking: 1
should_fix: 0
suggestion: 3
audited: 2026-07-20
---

# Audit: Intersection – No Gesture

- **Scenario:** `prosoc/scenarios/intersection_no_gesture/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Not ready — 1 blocking issue (required Scenario Usage Guide content entirely unpopulated in the machine-readable spec); remaining findings are minor.

This is a full re-audit reflecting this session's edits (Card Summary/Usage Guide
prose rendered in; `scientific_purpose`, `geometric_layout`, `intended_robot_task`,
`intended_human_behavior`, `ideal_outcome`, `related_scenarios`, `cited_in` authored
from P&G Table 3). It supersedes and fully replaces the 2026-07-05 audit below.

## Findings

### 1. `scenario_usage_guide` block still entirely missing from YAML — blocking
- **Section/field:** Scenario Specification (YAML) — `scenario_usage_guide` (success_metrics, quality_metrics, failure_modes, labeling_criteria)
- **Issue:** The rendered "Scenario Usage Guide" section now restates Ideal Outcome and explicitly lists Success Metrics, Quality Metrics, Failure Modes, and Labeling Criteria as "Remaining gaps." The embedded/distilled YAML still has no `scenario_usage_guide` key at all — not even empty placeholders. `template.md` marks this section as "Required for AUDITED scenarios." Unchanged from the prior audit's Finding 2.
- **Recommended fix:** Add a `scenario_usage_guide` block. `success_metrics` (e.g. `NoCollisions`, `SR`) is directly inferable from `expected_behaviors.must` ("avoid collision with the human"); `quality_metrics` can mirror `relevant_principles`; `failure_modes` is already implied in prose ("overly aggressive entry, excessive hesitation, or late yielding") and in `evaluation_notes`; `labeling_criteria` needs fresh authoring.

### 2. `relevant_principles` omits P6/P7 despite prose language that fits them — suggestion
- **Section/field:** `relevant_principles` (`P0, P1, P2, P3, P4` — unchanged this session)
- **Issue:** At 5 entries this sits at the top of the 3–5 guidance band, not over it, so this stays suggestion-level. The prose repeatedly emphasizes "implicit coordination," "mutual anticipation of trajectories," and avoiding "oscillate indecisively" — language that maps closely to P6 (Agent Understanding — predicting the human's trajectory/intent) and P7 (Proactivity — resolving ambiguity/deadlock without hesitation). Neither is listed. Unchanged from the prior audit's Finding 4.
- **Recommended fix:** Optional — human editor may consider swapping in P6 or P7 for one of the current five, without exceeding the guidance band.

### 3. Possible mild over-specification in `expected_behaviors.should_not` — suggestion
- **Section/field:** `expected_behaviors.should_not` vs. P&G Guideline N6 (over-specification)
- **Issue:** "oscillate indecisively at the intersection" and "force the human to stop abruptly" describe behavior kinds (fine); "aggressively assert right-of-way" borders on prescribing a specific strategy rather than a behavior category, though still mild. Unchanged from the prior audit's Finding 5.
- **Recommended fix:** Optional — may be left as-is; it still names a behavior class rather than an exact motion or numeric threshold.

### 4. Related Scenarios lists two entries where P&G Table 3 lists none — suggestion
- **Section/field:** Scenario Card Summary "Related Scenarios" / `related_scenarios` vs. `_shared/pg_scenarios.md`
- **Issue:** The Table 3 entry for "Intersection No Gesture" has no "Related Scenarios" field at all. This session's newly-authored Card Summary and YAML list `intersection_gesture_proceed` and `intersection_gesture_wait`. Reasonable corpus-level enrichment given the Notes section already discusses comparison with gesture-based intersection scenarios, but it is content added beyond the cited source, not drawn from it.
- **Recommended fix:** No action required if intentional; optionally note it as a corpus cross-reference distinct from a Table 3-sourced field.

## Source Fidelity

Checked against `_shared/pg_scenarios.md`'s "Intersection No Gesture" entry (P&G Table 3):

| Field | Table 3 | This card | Match |
|---|---|---|---|
| Physical Env | Indoor | indoor | Yes |
| Geometric Layout | Intersection | intersection | Yes |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Yes |
| Robot Role | (not specified in Table 3) | navigating_agent | No conflict — source doesn't specify a role for this entry |
| Robot Task | Navigate A to B | navigate from A to B | Yes |
| Human Behavior | Cross navigate | cross navigate | Yes |
| Ideal Outcome | Both pass, no collision | robot and human both cross the intersection without collision, absent any explicit gesture | Yes — consistent, elaborated. Resolves the prior audit's finding that `ideal_outcome` was missing from the YAML entirely |
| Related Scenarios | (not specified in Table 3) | intersection_gesture_proceed, intersection_gesture_wait | See Finding 4 |
| Cited In | [27, 50, 167] | "27", "50", "167" | Yes — resolves the prior audit's note that Cited In wasn't reproduced anywhere on the card |

No contradictions found. Compared with the 2026-07-05 audit, the newly-authored
Card Summary and `ideal_outcome`/`cited_in` fields resolve what were previously
should-fix/completeness findings.

## Completeness

`scripts/distill/scenarios --scenario intersection_no_gesture --dry-run --show-diffs`
reports no diff and no schema errors — `scenario.md`'s embedded YAML and
`scenario.yml` are in sync and schema-valid.

**Scenario Card Summary** (required for AUDITED): Scenario Name, Description,
Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task,
Human Behavior, Ideal Outcome, Related Scenarios, Cited In — all now present (this
resolves the prior audit's Finding 3, "missing Scenario Card Summary section
entirely"). Success Metrics and Quality Metrics — still blank, should-fill-in-now
(the card itself already self-flags these as "Remaining gaps").

**Scenario Usage Guide** (required for AUDITED): Ideal Outcome present (restated
from Card Summary). Success Metrics, Quality Metrics, Failure Modes, Labeling
Criteria — all blank, both in prose and absent from the YAML entirely (Finding 1).
Failure Modes and Success/Quality Metrics are should-fill-in-now (directly
inferable from `evaluation_notes`/`expected_behaviors.must` and
`relevant_principles` respectively). Labeling Criteria leans should-fill-in-now but
requires genuine new authoring rather than transcription.

Prose vs. YAML consistency (Scenario Overview, Social Navigation Context, Normative
Expectations against `intended_robot_task`, `intended_human_behavior`, `agents`,
`expected_behaviors`, `ideal_outcome`): no contradictions or drift found.

## Change Summary vs. 2026-07-05 Audit

The prior audit (after its 2026-07-05 correction notice) recorded blocking:1,
should_fix:1, suggestion:2. The blocking finding was the missing
`scenario_usage_guide` block; the should-fix finding was the missing Scenario Card
Summary section; the two suggestions were about `relevant_principles` candidate
coverage (P6/P7) and mild over-specification in `should_not`. This session's edits
resolved the Scenario Card Summary should-fix finding entirely, and authored
previously-missing `ideal_outcome` and `cited_in` fields. The `scenario_usage_guide`
gap persists unchanged and remains blocking. The two carried-forward suggestions
are unchanged, and one new suggestion was added (Related Scenarios enrichment
beyond what Table 3 specifies for this entry) — net should_fix drops from 1 to 0,
suggestion rises from 2 to 3, blocking stays at 1.
