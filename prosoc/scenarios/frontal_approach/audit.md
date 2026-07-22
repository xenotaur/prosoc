---
scenario: frontal_approach
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 2
audited: 2026-07-21
---

# Audit: Frontal Approach

- **Scenario:** `prosoc/scenarios/frontal_approach/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready for AUDITED with minor fixes — no contradictions, no schema issues, `related_scenarios` is now populated with three reciprocally-linked scenarios (`blind_corner`, `movable_obstruction`, `single_file_hallway`), all of which exist in the corpus and cite `frontal_approach` back. One should-fix item remains.

## Findings

### 1. Robot capabilities omit sensing/prediction implied by the Overview — should-fix
- **Section/field:** Scenario Overview vs. `agents.robot.capabilities`
- **Issue:** The Scenario Overview states "successful social navigation may require trajectory prediction, interpreting intent, resolving hesitation, and resolving conflicts," and `relevant_principles` includes P6 (Agent Understanding) accordingly. But `agents.robot.capabilities` lists only motion primitives (`forward_motion`, `steering`, `stopping`) — no sensing, prediction, or intent-recognition capability is declared, even though the prose and the P6 selection both depend on the robot having some perceptual/predictive capacity.
- **Recommended fix:** Either add a capability (e.g. `trajectory_prediction` or `intent_estimation`) to `agents.robot.capabilities`, or soften the Overview's claim so it doesn't imply a capability the YAML doesn't grant.

### 2. No "Social Navigation Context" section — suggestion
- **Section/field:** Template's optional-but-recommended "Social Navigation Context" section (absent from `scenario.md`)
- **Issue:** The template recommends a section describing common human expectations, sources of ambiguity/asymmetry, and why the scenario is socially interesting, distinct from the Overview. This scenario folds a little of that into the Overview and Discussion sections but has no dedicated section, and `context.social_setting` (formality: informal, crowd_level: low) is never narrated in prose.
- **Recommended fix:** Optional — add a short "Social Navigation Context" section, or accept the current Overview/Discussion coverage as sufficient since the section is not required for AUDITED.

### 3. No "Normative Expectations" prose section — suggestion
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
| Related Scenarios | Ped. Obstruct | blind_corner, movable_obstruction, single_file_hallway | Elaboration, not a strict transcription of "Ped. Obstruct" — see note below |
| Cited In | [50, 126, 167] | 50, 126, 167 | Exact match |

No contradictions found. On Related Scenarios: P&G Table 3 names a single related concept, "Ped. Obstruct," which has no scenario of that exact name in the corpus. The card now instead links three scenarios (`blind_corner`, `movable_obstruction`, `single_file_hallway`) that are thematically related hallway/passing scenarios, and all three reciprocally list `frontal_approach` back in their own `related_scenarios`. This is a reasonable editorial judgment call rather than a direct transcription of the P&G source field, and is internally consistent across the corpus — not flagged as an issue.

## Completeness

Walked against `template.md`'s "Required for AUDITED scenarios" sections:

- **Scenario Card Summary** — all fields populated (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, Cited In). Related Scenarios, previously blank, is now filled in with three reciprocally-consistent entries.
- **Scenario Usage Guide** — Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, and Labeling Criteria are all populated, consistent between the embedded YAML and the standalone "Scenario Usage Guide" section at the end of the document.

Reasonably blank: none. No fields remain that need filling for AUDITED completeness.
