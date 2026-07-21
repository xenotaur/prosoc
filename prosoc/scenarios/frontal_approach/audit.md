---
scenario: frontal_approach_01
verdict: ready_with_fixes
blocking: 0
should_fix: 2
suggestion: 2
audited: 2026-07-20
---

# Audit: Frontal Approach

- **Scenario:** `prosoc/scenarios/frontal_approach/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes — no contradictions, no schema issues, and every previously-blocking gap (missing `ideal_outcome`, `scientific_purpose`, `geometric_layout`, `intended_robot_task`, `intended_human_behavior`) has been filled in. Two should-fix items remain.

## Findings

### 1. Related Scenarios self-flagged as "should-fill-in-now" but no matching scenario exists in the corpus — should-fix
- **Section/field:** Scenario Card Summary → Related Scenarios / YAML `related_scenarios` (absent)
- **Issue:** The card's own "Remaining gaps" note labels Related Scenarios as "should-fill-in-now," implying the value is readily inferable and just needs transcribing. However, the P&G Table 3 entry for Frontal Approach lists "Ped. Obstruct" as the related scenario, and no scenario with that concept currently exists in `prosoc/scenarios/` (the closest name, `movable_obstruction`, is explicitly noted elsewhere as having no P&G Table 3 counterpart, so it should not be assumed to be the same thing without verification).
- **Recommended fix:** A human editor should either (a) verify whether `movable_obstruction` is actually the intended referent and link it, (b) leave `related_scenarios` blank with a note that the P&G-listed relative ("Pedestrian Obstruction") is not yet implemented, or (c) correct the self-assessment from "should-fill-in-now" to "reasonably blank — referent not yet implemented."

### 2. Robot capabilities omit sensing/prediction implied by the Overview — should-fix
- **Section/field:** Scenario Overview vs. `agents.robot.capabilities`
- **Issue:** The Scenario Overview states "successful social navigation may require trajectory prediction, interpreting intent, resolving hesitation, and resolving conflicts," and `relevant_principles` includes P6 (Agent Understanding) accordingly. But `agents.robot.capabilities` lists only motion primitives (`forward_motion`, `steering`, `stopping`) — no sensing, prediction, or intent-recognition capability is declared, even though the prose and the P6 selection both depend on the robot having some perceptual/predictive capacity.
- **Recommended fix:** Either add a capability (e.g. `trajectory_prediction` or `intent_estimation`) to `agents.robot.capabilities`, or soften the Overview's claim so it doesn't imply a capability the YAML doesn't grant.

### 3. No "Social Navigation Context" section — suggestion
- **Section/field:** Template's optional-but-recommended "Social Navigation Context" section (absent from `scenario.md`)
- **Issue:** The template recommends a section describing common human expectations, sources of ambiguity/asymmetry, and why the scenario is socially interesting, distinct from the Overview. This scenario folds a little of that into the Overview and Discussion sections but has no dedicated section, and `context.social_setting` (formality: informal, crowd_level: low) is never narrated in prose.
- **Recommended fix:** Optional — add a short "Social Navigation Context" section, or accept the current Overview/Discussion coverage as sufficient since the section is not required for AUDITED.

### 4. No "Normative Expectations" prose section — suggestion
- **Section/field:** Template's optional-but-recommended "Normative Expectations" section (absent) vs. `expected_behaviors.{must,should,should_not}`
- **Issue:** `expected_behaviors` in the YAML is fairly rich (2 must, 3 should, 3 should_not), but none of it is narrated in prose outside the YAML block — a reader skimming only the Markdown prose (Overview + Discussion) would miss the specific behavioral expectations entirely.
- **Recommended fix:** Optional — add a short "Normative Expectations" section restating the must/should/should_not list in natural language, per the template's guidance. Not required for AUDITED, but improves human readability.

## Source Fidelity

Checked against `_shared/pg_scenarios.md`'s P&G Table 3 entry for **Frontal Approach**:

| Field | P&G Table 3 | This scenario | Match |
|---|---|---|---|
| Description | Pedestrian and robot approach head-on in a passable space | Robot and human approach each other in opposite directions, pass safely/comfortably/without prolonged hesitation | Match |
| Physical Env | Generic | Indoor (office hallway, narrow) | Deliberate elaboration, not a contradiction — P&G leaves this generic/unspecified |
| Geometric Layout | Passable space | passable space | Exact match |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Exact match |
| Robot Task | Navigate A to B | navigate from A to B | Match |
| Human Behavior | Navigate B to A | navigate from B to A | Exact match |
| Ideal Outcome | Robot/humans pass | robot and human pass each other safely, comfortably, and without prolonged hesitation | Match (elaborated) |
| Related Scenarios | Ped. Obstruct | (blank) | Gap — see Finding 1 |
| Cited In | [50, 126, 167] | 50, 126, 167 | Exact match |

No contradictions found. The scenario elaborates on the generic P&G entry (concrete hallway setting, explicit must/should/should_not behaviors) without deviating from its substance. Compared to the prior audit pass, `ideal_outcome`, `scientific_purpose`, `geometric_layout`, `intended_robot_task`, and `intended_human_behavior` are now all present and all match the source.

## Completeness

Walked against `template.md`'s "Required for AUDITED scenarios" sections:

- **Scenario Card Summary** — all fields populated (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Cited In) except **Related Scenarios**, which is blank — see Finding 1 (should-fill-in-now per the card's own note, but the referent scenario doesn't yet exist in the corpus, so treat as reasonably-blank-pending-clarification rather than a simple transcription task).
- **Scenario Usage Guide** — Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all populated, consistent between the embedded YAML and the standalone "Scenario Usage Guide" section at the end of the document.

Reasonably blank: none beyond Related Scenarios (which is a should-fix, not reasonably-blank, given the card itself flags it as should-fill-in-now).
