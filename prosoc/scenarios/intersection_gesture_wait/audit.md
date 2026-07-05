# Audit: Intersection – Gesture Wait

- **Scenario:** `prosoc/scenarios/intersection_gesture_wait/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready — 3 blocking issues

## Findings

### 1. Invalid principle IDs `P0` and `P9` in `relevant_principles` — blocking
- **Section/field:** Scenario Specification (YAML) → `relevant_principles`
- **Issue:** The YAML lists `P0  # Goal Achievement` and `P9  # Prosocial Behavior` alongside P1–P4. `../../../.claude/skills/_shared/principles.md` defines only P1–P8; there is no P0 or P9, and no principle named "Goal Achievement" or "Prosocial Behavior" exists in the charter. `schema.json`'s `pattern: "^P[0-9]+$"` has no upper bound, so this passes schema/dry-run validation silently — it is a charter-compliance defect, not a schema error.
- **Recommended fix:** Remove `P0` and `P9`. If "goal achievement" and "prosocial behavior generally" are concepts the author wants to flag, note them in `evaluation_notes` instead of inventing new principle IDs, per `../../../.claude/skills/_shared/principles.md`'s explicit guidance.

### 2. Same invalid IDs would need to be checked in `quality_metrics` — blocking (moot, but related)
- **Section/field:** `scenario_usage_guide.quality_metrics`
- **Issue:** This field doesn't exist in the card at all (see Finding 4), so the P1–P8-only constraint can't yet be violated there — but whoever fills it in should not reuse P0/P9 from `relevant_principles`.
- **Recommended fix:** When authoring `quality_metrics`, draw only from the corrected P1–P8 list, not from the current (invalid) `relevant_principles` set.

### 3. Missing `scenario_usage_guide` block entirely — blocking
- **Section/field:** Scenario Specification (YAML) — `scenario_usage_guide` (success_metrics, quality_metrics, failure_modes, labeling_criteria)
- **Issue:** The embedded YAML has no `scenario_usage_guide` key at all. `template.md` marks the Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria) as "Required for AUDITED scenarios."
- **Recommended fix:** Add a `scenario_usage_guide` block. Much of the content is inferable from prose already on the card (see Completeness below) — a human editor should draft it before promoting to AUDITED.

### 4. Missing "Scenario Card Summary" section — should-fix
- **Section/field:** Prose — no "Scenario Card Summary" heading present (template.md requires it for AUDITED)
- **Issue:** The card jumps from Status straight to Scenario Overview; the structured summary block (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) is entirely absent.
- **Recommended fix:** Add the section, drawing on prose already present (Overview, Normative Expectations) and the `../../../.claude/skills/_shared/pg_scenarios.md` Table 3 entry for "Intersection Gesture Wait."

### 5. Robot Role drift vs. P&G source — should-fix
- **Section/field:** Fidelity to source vs. `agents.robot.role`
- **Issue:** `../../../.claude/skills/_shared/pg_scenarios.md`'s Table 3 entry for "Intersection Gesture Wait" lists **Robot Role: Servant**. The scenario's YAML instead sets `agents.robot.role: navigating_agent` (a generic/default value used elsewhere across scenarios, not specific to this one). This isn't a hard contradiction — "navigating_agent" isn't false — but it drops information the source specifies.
- **Recommended fix:** Consider setting `role: servant` (or otherwise noting the Servant role in prose/YAML) to align with Table 3, or explicitly explain in `evaluation_notes` why a more generic role was chosen instead.

### 6. `relevant_principles` count of 4 (once P0/P9 removed) is within guidance but omits some plausible candidates — suggestion
- **Section/field:** `relevant_principles` (P1, P2, P3, P4 remain after removing invalid IDs)
- **Issue:** Once P0 and P9 are dropped, 4 principles remain — within the 3–5 guidance band, so not a problem on its own. However, P6 (Agent Understanding — predicting/accommodating the human's gesture) and P7 (Proactivity — resolving the wait/proceed ambiguity) both seem plausibly relevant to a gesture-compliance scenario and are not listed.
- **Recommended fix:** Human editor should consider whether P6 or P7 belong, without exceeding 5 total.

## Source Fidelity

SOURCE cites "Principles and Guidelines for Social Robot Navigation (Table 3)," matching `../../../.claude/skills/_shared/pg_scenarios.md`'s "Intersection Gesture Wait" entry. Comparison:

| Field | Table 3 (pg_scenarios.md) | This scenario | Match? |
|---|---|---|---|
| Description | Robot told to wait at intersection | Human gestures for robot to wait; robot complies | Match |
| Physical Env | Indoor | indoor | Match |
| Geometric Layout | Intersection | hallway intersection | Match |
| Robot Task | Navigate A to B | intended_robot_task not explicitly stated as a separate field, but consistent with prose ("approach an indoor intersection") | Match (loosely — see completeness note) |
| Human Behavior | Cross navigate (gesture wait) | human pedestrian, `gesturing: wait` | Match |
| Robot Role | **Servant** | `navigating_agent` | **Mismatch** — see Finding 5 |
| Ideal Outcome | Human goes, then robot | `expected_behaviors` implies this (robot yields, waits) but no explicit `ideal_outcome` field is present in the YAML at all | Partial — `ideal_outcome` field is missing (see Completeness) |
| Related Scenarios | Gesture Proceed | Notes section mentions comparison with "no-gesture and gesture-proceed scenarios" | Match |

Overall: broadly faithful to Table 3, with one flagged Robot Role drift (Finding 5) and a missing `ideal_outcome` field (see Completeness).

## Completeness

Fields required for AUDITED per `template.md`:

- **Scenario Card Summary section** — **should probably be filled in now.** Entirely absent; content is readily inferable from Overview/Normative Expectations prose and the Table 3 entry.
- **`ideal_outcome` (YAML field)** — **should probably be filled in now.** Not present in the embedded YAML at all, even though `schema.json` defines it and prose clearly implies one ("human goes, then robot"; robot yields safely and legibly).
- **`scenario_usage_guide.success_metrics`** — **should probably be filled in now.** Plausible candidates (e.g., NoCollisions, a gesture-compliance/legibility metric) are inferable from Normative Expectations.
- **`scenario_usage_guide.quality_metrics`** — **should probably be filled in now.** Should mirror a corrected `relevant_principles` list.
- **`scenario_usage_guide.failure_modes`** — **should probably be filled in now.** Already implied in prose ("ignoring the gesture," "partial compliance," "delayed responses") and in `evaluation_notes` — just needs to be lifted into the structured field.
- **`scenario_usage_guide.labeling_criteria`** — **reasonably blank**, but only in the sense that it requires new authoring judgment (how would an annotator recognize this scenario in a trace, independent of behavior quality) rather than being a straightforward lift from existing prose.
- **Related Scenarios / Cited In (Scenario Card Summary sub-fields)** — **reasonably blank** for now if the Scenario Card Summary section is being added fresh, though the Notes section already names the related "gesture proceed" and "no-gesture" scenarios and "Cited In: [126]" is available from `pg_scenarios.md`.
