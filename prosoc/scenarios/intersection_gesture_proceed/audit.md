# Audit: Intersection – Gesture Proceed

- **Scenario:** `prosoc/scenarios/intersection_gesture_proceed/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready for AUDITED — 2 blocking issues, several should-fix gaps

## Findings

### 1. Invalid principle identifiers P0 and P9 used in `relevant_principles` — blocking
- **Section/field:** `scenario.yml` / embedded YAML `relevant_principles` (both list `P0  # Goal Achievement` and `P9  # Prosocial Behavior`)
- **Issue:** Per `../_shared/principles.md`, only P1–P8 are valid principle identifiers, and the schema's regex (`^P[0-9]+$`) does not by itself enforce this — it will accept `P0`/`P9` syntactically without error (confirmed: the dry-run distiller check reported no schema violation). "Goal Achievement" and "Prosocial Behavior" are not among the eight canonical principles (Safety, Comfort, Legibility, Politeness, Social Competency, Agent Understanding, Proactivity, Contextual Appropriateness) and appear to be invented identifiers. This also means `relevant_principles` effectively has only 4 valid P1–P8 entries (P1–P4), which is below the recommended 3–5 range in spirit once the invalid ones are discounted, though nominally 6 entries are listed.
- **Recommended fix:** Remove `P0` and `P9`. If "Goal Achievement" or "Prosocial Behavior" concepts are important to this scenario, note them in `evaluation_notes` instead (per `_shared/principles.md`'s explicit guidance: "If a scenario involves a principle not well-captured by P1–P8, note it in `evaluation_notes` rather than inventing a new ID"). Consider whether P6 (Agent Understanding) or P7 (Proactivity) should be added instead, since the scenario involves predicting/responding to a human's explicit gesture — currently neither is included despite being plausibly relevant.

### 2. `scenario_usage_guide` block entirely absent from machine-readable YAML — blocking
- **Section/field:** `scenario.yml` (missing `scenario_usage_guide`); prose "Scenario Usage Guide" section (present, with Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria all populated)
- **Issue:** The prose section fully specifies Success Metrics ("No collision occurs," "Robot commits to crossing promptly after gesture," "Human proceeds without hesitation or retreat"), Quality Metrics, Failure Modes, and Labeling Criteria — but none of this is reflected in the embedded YAML or `scenario.yml`. This is a one-sided claim (present in prose, absent from YAML) affecting the entire `scenario_usage_guide` object, not just one field. It also means `quality_metrics` was never checked against the P1–P8 constraint in machine-readable form, since the field doesn't exist there (the prose Quality Metrics list — "Time between gesture and robot motion," "Smoothness and predictability of robot trajectory," "Absence of oscillation or hesitation" — doesn't even use P1–P8 identifiers, it uses free-text descriptions, which is itself inconsistent with how `scenario_usage_guide.quality_metrics` is used elsewhere in the corpus, e.g. `frontal_approach`, where it holds principle IDs).
- **Recommended fix:** Add a `scenario_usage_guide` block to the YAML with `success_metrics`, `quality_metrics` (using P1–P8 IDs, not free text), `failure_modes`, and `labeling_criteria`, transcribing the content already drafted in the prose section.

### 3. `ideal_outcome`, `scientific_purpose`, `geometric_layout`, `intended_robot_task`, `intended_human_behavior` all absent from YAML despite being specified in prose — should-fix
- **Section/field:** `scenario.yml` (missing all five fields); Scenario Card Summary (has Scientific Purpose: "Pedestrian interaction", Geometric Layout: "Intersection", Robot Task: "Navigate from A to B", Human Behavior: "Cross navigation with explicit proceed gesture", Ideal Outcome: "Human gestures, robot proceeds, human proceeds, no collision" — all populated in prose)
- **Issue:** This scenario's prose Card Summary is fully filled out, but none of that content made it into the machine-readable spec. This is the same one-sided-claim pattern as Finding 2, extended to the Card Summary fields. Since the audit checklist's prose/YAML cross-check explicitly relies on `ideal_outcome` to verify the prose's "good ending" claim, its absence from YAML weakens that check (though in this case the prose's own Card Summary and Overview are mutually consistent, so no contradiction was found — just a machine-readability gap).
- **Recommended fix:** Populate these five fields in `scenario.yml`/embedded YAML directly from the already-written Card Summary prose (this is a low-effort transcription, not new content creation).

### 4. Robot Role mismatch with P&G Table 3 source — should-fix
- **Section/field:** Scenario Card Summary "Robot Role" / `agents.robot.role` vs. P&G Table 3
- **Issue:** P&G Table 3 specifies **Robot Role: Servant** for "Intersection Gesture Proceed" (consistent with the scenario's framing — a human directs the robot). This card instead states "Robot Role: Any (navigating agent)" in the Card Summary and `role: navigating_agent` in YAML, which is a genericization that loses the "servant" framing the source paper assigns. This changes the interpretive stakes of the scenario: under a "servant" framing, the human's gesture is closer to a command the robot is obligated to follow; under "any/navigating_agent" framing, it's simply one input the robot may weigh.
- **Recommended fix:** Either align `agents.robot.role` (and the Card Summary) to `servant`/"Servant" to match the P&G source, or, if the deviation is intentional (e.g. broadening the scenario beyond servant robots), add a note in `evaluation_notes` explaining the deliberate departure from Table 3's role assignment.

### 5. `expected_behaviors` phrasing borders on prescribing exact response timing — suggestion
- **Section/field:** `expected_behaviors.should` — "commit promptly to motion after the gesture"; Quality Metrics prose — "Time between gesture and robot motion"
- **Issue:** These are still qualitative ("promptly," not a numeric threshold), so this does not clearly violate P&G Guideline N6 over-specification as written. However, "Time between gesture and robot motion" as a *quality metric* edges toward a measurable latency criterion without stating what counts as acceptable, which could invite inconsistent labeling.
- **Recommended fix:** No changes strictly required; optionally clarify in `evaluation_notes` what a "prompt" response window looks like qualitatively (e.g. "within a natural conversational turn-taking pause") without introducing a hard numeric threshold.

## Source Fidelity

SOURCE is explicitly stated as "Principles and Guidelines for Social Robot Navigation (Table 3)," so it is checked directly against `../_shared/pg_scenarios.md`'s "Intersection Gesture Proceed" entry:

| Field | P&G Table 3 | This scenario | Match? |
|---|---|---|---|
| Description | Robot told to proceed at intersection | Human explicitly gestures for robot to proceed; robot recognizes and crosses | Consistent — same interaction, elaborated |
| Physical Env | Indoor | Indoor | Match |
| Geometric Layout | Intersection | Intersection (Card Summary); absent from YAML | Match in prose; missing field in YAML (Finding 3) |
| Scientific Purpose | Pedestrian interaction | Pedestrian interaction (Card Summary); absent from YAML | Match in prose; missing field in YAML (Finding 3) |
| Robot Role | Servant | Any (navigating agent) | **Mismatch** (Finding 4) |
| Robot Task | Navigate A to B | Navigate from A to B (Card Summary); absent from YAML | Match in prose; missing field in YAML (Finding 3) |
| Human Behavior | Cross navigate (gesture proceed) | Cross navigation with explicit proceed gesture | Match |
| Ideal Outcome | Robot goes first | Human gestures, robot proceeds, human proceeds, no collision | Consistent — "robot goes first" is implied by "robot proceeds, human proceeds" (robot acts first after receiving the gesture) |
| Related Scenarios | Gesture Wait | Intersection – No Gesture; Intersection – Gesture Wait | Consistent, and appropriately broader |
| Cited In | [126] | Principles and Guidelines for Social Robot Navigation (Table 3) | Consistent |

**Overall:** Strong fidelity apart from the Robot Role discrepancy (Finding 4), which is the one clear mismatch against the source.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields, assessed against the prose sections (all present in `scenario.md`) and the YAML (several fields missing):

**Scenario Card Summary** — all fields present in prose:
- Scenario Name, Scenario Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome, Related Scenarios, Cited In: all filled in prose — complete at the prose level.
- Success Metrics / Quality Metrics: not present as discrete Card Summary lines (they appear later under the separate "Scenario Usage Guide" section instead) — reasonably blank here, since the template allows flexibility in where these appear and they are populated elsewhere.
- **However**, none of the above are mirrored in `scenario.yml` (Finding 3) — should probably be filled in now given the prose content already exists.

**Scenario Usage Guide** — all subsections present in prose (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria are each filled with concrete content) — complete at the prose level, but **should probably be filled in now** in the machine-readable YAML, since the content already exists and just needs transcription (Finding 2).

No fields were found to be reasonably-blank-and-acceptable in this scenario — every gap identified is prose-complete content that simply hasn't been carried into the YAML, making all of them "should probably be filled in now" rather than "genuinely unknown."
