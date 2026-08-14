---
family: scenarios
card: frontal_approach
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-08-02
---

# Audit: Frontal Approach

- **Card:** `prosoc/scenarios/frontal_approach/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — and is superseded by this
  pass; findings carry forward unchanged since no content changed)
- **Verdict:** Ready — no contradictions, no schema issues; two low-severity
  suggestions

## Findings

### 1. No "Social Navigation Context" section — suggestion
- **Section/field:** Template's optional-but-recommended "Social Navigation
  Context" section (absent from `scenario.md`)
- **Issue:** The template recommends a section describing common human
  expectations, sources of ambiguity/asymmetry, and why the scenario is
  socially interesting, distinct from the Overview. This scenario folds a
  little of that into the Overview and Discussion sections but has no
  dedicated section, and `context.social_setting` (formality: informal,
  crowd_level: low) is never narrated in prose.
- **Recommended fix:** Optional — add a short "Social Navigation Context"
  section, or accept the current Overview/Discussion coverage as
  sufficient since the section is not required for `AUDITED`.

### 2. No "Normative Expectations" prose section — suggestion
- **Section/field:** Template's optional-but-recommended "Normative
  Expectations" section (absent) vs. `expected_behaviors.{must,should,should_not}`
- **Issue:** `expected_behaviors` in the YAML is fairly rich (2 must, 3
  should, 3 should_not), but none of it is narrated in prose outside the
  YAML block — a reader skimming only the Markdown prose (Overview +
  Discussion) would miss the specific behavioral expectations entirely.
- **Recommended fix:** Optional — add a short "Normative Expectations"
  section restating the must/should/should_not list in natural language,
  per the template's guidance. Not required for `AUDITED`, but improves
  human readability.

## Prose/YAML Consistency and Schema Check

- `scripts/distill/scenarios --scenario frontal_approach --dry-run
  --show-diffs` produced no diff and no schema errors — `scenario.yml` is
  in sync with the embedded YAML block in `scenario.md`.
- Scenario Overview explicitly states "[s]uccessful navigation depends on
  sensing and agile navigation, and successful social navigation may
  require trajectory prediction, interpreting intent, resolving
  hesitation, and resolving conflicts." `agents.robot.capabilities`
  includes `forward_motion`, `steering`, `stopping`, and
  `trajectory_prediction` — this backs the prose's trajectory-prediction
  claim and the `relevant_principles` inclusion of P6 (Agent
  Understanding).
- No contradictions found between prose (Overview, Discussion) and YAML
  (`agents`, `expected_behaviors`, `ideal_outcome`,
  `intended_robot_task`/`intended_human_behavior`).
- `relevant_principles` (P1, P2, P3, P5, P6) and
  `scenario_usage_guide.quality_metrics` (P2, P3, P5) all validate against
  P0–P9; count of 5 relevant principles is within the 3–5 guideline.
- `expected_behaviors` entries describe kinds of behavior ("maintain a
  safe physical distance," "signal intent clearly through motion or
  positioning") rather than exact motions or numeric thresholds — no
  over-specification (P&G Guideline N6) flagged.
- `related_scenarios` (`blind_corner`, `movable_obstruction`,
  `single_file_hallway`) — all three directories exist under
  `prosoc/scenarios/` and reciprocally reference `frontal_approach`; per
  the checklist's `related_scenarios` convention this substitution for
  P&G's unimplemented "Ped. Obstruct" citation is expected, not a defect,
  and is self-documented in the card's own `evaluation_notes`.

## Source Fidelity

Checked against `.claude/skills/_shared/pg_scenarios.md`'s P&G Table 3
entry for **Frontal Approach**:

| Field | P&G Table 3 | This card | Match |
|---|---|---|---|
| Description | Pedestrian and robot approach head-on in a passable space | Robot and human approach each other in opposite directions, pass safely/comfortably/without prolonged hesitation | Match |
| Physical Env | Generic | Indoor (office hallway, narrow) | Deliberate elaboration, not a contradiction — P&G leaves this generic/unspecified |
| Geometric Layout | Passable space | passable space | Exact match |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Exact match |
| Robot Task | Navigate A to B | navigate from A to B | Match |
| Human Behavior | Navigate B to A | navigate from B to A | Exact match |
| Ideal Outcome | Robot/humans pass | robot and human pass each other safely, comfortably, and without prolonged hesitation | Match (elaborated) |
| Related Scenarios | Ped. Obstruct | blind_corner, movable_obstruction, single_file_hallway | Elaboration, not a strict transcription — see note below |
| Cited In | [50, 126, 167] | 50, 126, 167 | Exact match |

No contradictions found. On Related Scenarios: P&G Table 3 names a single
related concept, "Ped. Obstruct," which has no scenario of that exact name
in the corpus. The card instead links three thematically related
hallway/passing scenarios, all of which reciprocally list
`frontal_approach` back — a reasonable editorial judgment call, internally
consistent across the corpus, and self-documented in the card's
`evaluation_notes`. Not flagged as an issue.

`SOURCE: Prompt to ChatGPT 5.2` (not an explicit P&G Table 3 citation) —
noted but not flagged: the same generic SOURCE line appears on other
early-batch scenarios drafted 2026-01-02 whose content is nonetheless
verifiably Table-3-derived (e.g. `pedestrian_overtaking`); a corpus-wide
legacy-attribution pattern from the earliest drafting batch, out of scope
for a single-card audit.

## Completeness

Walked against `template.md`'s "Required for AUDITED scenarios" sections:

- **Scenario Card Summary** — all fields populated (Scenario Name,
  Description, Scientific Purpose, Physical Environment, Geometric Layout,
  Robot Role, Robot Task, Human Behavior, Success Metrics, Quality
  Metrics, Ideal Outcome, Related Scenarios, Cited In).
- **Scenario Usage Guide** — Success Metrics, Quality Metrics, Ideal
  Outcome, Failure Modes, and Labeling Criteria are all populated,
  consistent between the embedded YAML and the standalone "Scenario Usage
  Guide" section at the end of the document.

Reasonably blank: none. No fields remain that need filling for `AUDITED`
completeness.
