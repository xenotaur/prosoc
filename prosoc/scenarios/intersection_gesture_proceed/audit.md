---
scenario: intersection_gesture_proceed_01
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 2
audited: 2026-07-20
---

# Audit: Intersection – Gesture Proceed

- **Scenario:** `prosoc/scenarios/intersection_gesture_proceed/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes — the prior blocking gap (Card Summary content absent from the machine-readable YAML) and the prior Robot Role mismatch against the P&G source are both resolved. One should-fix remains: `scenario_usage_guide` is still missing from the YAML, and the prose Quality Metrics list still doesn't use the P0–P9 convention the schema field expects.

## Findings

### 1. `scenario_usage_guide` still absent from the machine-readable YAML; prose Quality Metrics uses free-text measures instead of P0–P9 principle IDs — should-fix
- **Section/field:** `scenario.yml` (no `scenario_usage_guide` key); prose "## Scenario Usage Guide" section (present, fully populated)
- **Issue:** The prose section fully specifies Success Metrics ("No collision occurs," "Robot commits to crossing promptly after gesture," "Human proceeds without hesitation or retreat"), Quality Metrics ("Time between gesture and robot motion," "Smoothness and predictability of robot trajectory," "Absence of oscillation or hesitation"), Failure Modes, and Labeling Criteria — but none of it is mirrored in the embedded YAML or `scenario.yml`. This is a one-sided claim (present in prose, absent from YAML) covering the entire `scenario_usage_guide` object. It also means `quality_metrics` was never checked against the P0–P9 pattern the schema expects for that field, since the field doesn't exist in machine-readable form here — and the prose content itself doesn't use principle IDs at all (it lists measurable behavioral quantities like response latency and trajectory smoothness), which is a different content model from `frontal_approach`'s `scenario_usage_guide.quality_metrics: [P2, P3, P5]` and from how `_shared/principles.md` describes the field ("Charter principles used specifically as quality metrics").
- **Recommended fix:** Add a `scenario_usage_guide` block to the YAML with `success_metrics`, `quality_metrics` (using P0–P9 IDs — e.g. P1/P2/P3/P4, mirroring `relevant_principles` — rather than free-text latency/smoothness descriptions), `failure_modes`, and `labeling_criteria`, transcribing the content already drafted in the prose section. If the free-text latency/smoothness measures are meant to be kept as evaluator guidance rather than principle references, consider moving them into `evaluation_notes` instead, and let `quality_metrics` hold only P0–P9 IDs.

### 2. `expected_behaviors.should` / prose Quality Metrics edge toward a measurable-latency criterion — suggestion
- **Section/field:** `expected_behaviors.should` — "commit promptly to motion after the gesture"; prose Quality Metrics — "Time between gesture and robot motion"
- **Issue:** Both are still qualitative ("promptly," not a numeric threshold), so this does not clearly violate P&G Guideline N6 over-specification as written. However, "Time between gesture and robot motion" as a quality metric edges toward a measurable latency criterion without stating what counts as acceptable, which could invite inconsistent labeling across evaluators.
- **Recommended fix:** No change strictly required; optionally clarify in `evaluation_notes` what a "prompt" response window looks like qualitatively (e.g. "within a natural conversational turn-taking pause") without introducing a hard numeric threshold.

### 3. Related Scenarios lists one more entry than the P&G source — suggestion
- **Section/field:** Scenario Card Summary / YAML `related_scenarios` vs. P&G Table 3
- **Issue:** P&G Table 3 lists only "Gesture Wait" as the related scenario for Intersection Gesture Proceed. This card additionally lists `intersection_no_gesture`. Both referenced IDs exist in the corpus (`intersection_gesture_wait/`, `intersection_no_gesture/` both present under `prosoc/scenarios/`), so this isn't a broken reference — just a reasonable, intentional broadening beyond what the source paper states.
- **Recommended fix:** No change required; noted for the human editor's awareness that this is an addition beyond the source, not an error.

## Source Fidelity

SOURCE is explicitly stated as "Principles and Guidelines for Social Robot Navigation (Table 3)," so it is checked directly against `_shared/pg_scenarios.md`'s "Intersection Gesture Proceed" entry:

| Field | P&G Table 3 | This scenario | Match? |
|---|---|---|---|
| Description | Robot told to proceed at intersection | Human explicitly gestures for robot to proceed; robot recognizes and crosses | Consistent — same interaction, elaborated |
| Physical Env | Indoor | Indoor | Match |
| Geometric Layout | Intersection | intersection | Match |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Match |
| Robot Role | Servant | servant | **Match — fixed since prior audit** (was `navigating_agent`) |
| Robot Task | Navigate A to B | navigate from A to B | Match |
| Human Behavior | Cross navigate (gesture proceed) | cross navigate (gesture proceed) | Exact match |
| Ideal Outcome | Robot goes first | human gestures the robot to proceed; robot goes first and both cross without collision | Match (elaborated) |
| Related Scenarios | Gesture Wait | intersection_gesture_wait, intersection_no_gesture | Consistent, appropriately broader (Finding 3) |
| Cited In | [126] | "126" | Match |

**Overall:** Full fidelity to the P&G source — no mismatches found. The Robot Role discrepancy flagged in the prior audit is resolved: the scenario now correctly uses `servant`, matching Table 3.

## Completeness

Walked against `template.md`'s "Required for AUDITED scenarios" sections, this time checking both prose and the machine-readable YAML (which, unlike the prior audit, now carries the Card Summary content):

- **Scenario Card Summary** — all fields present and now mirrored in `scenario.yml`: `id`, `name`, `summary`, `scientific_purpose`, `geometric_layout`, `agents.robot.role`, `intended_robot_task`, `intended_human_behavior`, `ideal_outcome`, `related_scenarios`, `cited_in` are all populated in both prose and YAML — complete. (Previously, all five of `ideal_outcome`, `scientific_purpose`, `geometric_layout`, `intended_robot_task`, `intended_human_behavior` were absent from YAML; that gap is now closed.)
- **Scenario Usage Guide** — all subsections (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria) are complete in prose, but still **should probably be filled in now** in the machine-readable YAML — see Finding 1. This is the one remaining completeness gap from the prior audit.

No fields were found to be reasonably blank in this scenario.
