---
family: scenarios
card: frontal_approach
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-11-07
---

# Audit: Frontal Approach

- **Card:** `src/prosoc/prnc/scenarios/frontal_approach/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED with a minor fix — reconcile the SOURCE
  field's non-derivation disclaimer against the card's otherwise exact
  fidelity to P&G Table 3; no blocking issues.

## Findings

### 1. SOURCE field disclaims external-citation derivation that the card's own content contradicts — should-fix
- **Section/field:** `## Status` `**SOURCE:**` line vs. `cited_in`, `evaluation_notes`, and the Scenario Card Summary's content
- **Issue:** The SOURCE line reads "Original scenario concept, LLM-assisted
  drafting (ChatGPT 5.2); a common pedestrian-interaction benchmark pattern,
  **not derived from a specific external citation**." But the card's own
  content matches the P&G paper's Table 3 "Frontal Approach" entry closely
  and specifically: `cited_in: ["50", "126", "167"]` is exactly Table 3's
  "Cited In: [50, 126, 167]"; `scientific_purpose`, `geometric_layout`,
  `intended_robot_task`, `intended_human_behavior`, and `ideal_outcome` all
  match Table 3's Scientific Purpose / Geometric Layout / Robot Task / Human
  Behavior / Ideal Outcome fields (specialized to an indoor office hallway,
  but not contradicting them); and `evaluation_notes` explicitly discusses
  what "P&G Table 3 lists ... as this scenario's related entry." A card this
  closely aligned to a specific, identifiable Table 3 row is hard to square
  with a SOURCE line asserting it is "not derived from a specific external
  citation." This may be an artifact of the project's ongoing
  internal-development-vs-external-reader provenance wording effort
  (WI-CHARTER-SUPPLEMENT-SOURCE-FIXES, 2026-10-27; and
  WI-CHARTER-SUPPLEMENT-PUBLICATION-VIEW-FILTER, 2026-11-06, both editing
  this same SOURCE line's phrasing), in which case the current wording may be
  an intentional simplification rather than an oversight — but as written it
  reads as a factual claim that the card's own `cited_in`/`evaluation_notes`
  content contradicts.
- **Recommended fix:** A human editor should decide whether SOURCE should
  instead acknowledge the P&G Table 3 row as (at least) the originating
  template this scenario specializes — e.g. "Specializes the P&G Table 3
  'Frontal Approach' entry (Francis et al., 2025); drafted with LLM
  assistance (ChatGPT 5.2)" — or, if the "not derived from a specific
  external citation" framing is intentional per the project's provenance
  policy, confirm that reading explicitly rather than leaving the tension
  implicit.

### 2. Optional "Social Navigation Context" and "Normative Expectations" prose sections are entirely absent — suggestion
- **Section/field:** `template.md`'s optional `## Social Navigation Context` / `## Normative Expectations` sections
- **Issue:** `template.md` marks these sections "Optional but recommended."
  `scenario.md` has neither heading at all (not merely blank) — the
  `## Scenario Overview` paragraph briefly names the social-navigation
  principles in play but does not separately discuss social expectations,
  ambiguity/asymmetry sources, or natural-language normative guidance beyond
  what the YAML `expected_behaviors` block already states. Since the card
  already has the underlying content (`context.social_setting`,
  `expected_behaviors.{must,should,should_not}`), a short prose section could
  be drafted mostly by restating what is already authored.
- **Recommended fix:** Reasonably blank — these sections are optional, not
  required for AUDITED. Optionally, a human editor could add brief
  "Social Navigation Context" and "Normative Expectations" prose sections
  drawing on the existing YAML content for readability, but this is not
  required to proceed.

## Source Fidelity

SOURCE cites no specific external reference (see Finding 1 on the tension
this creates), so the comparison below is made against `../pg_scenarios.md`'s
"Frontal Approach" entry (P&G Table 3) on its own merits, since the scenario
name and content make that the only plausible checkable source:

| Field | P&G Table 3 | Card | Match |
|---|---|---|---|
| Description | Pedestrian and robot approach head-on in a passable space | Robot and human approach in opposite directions in a narrow (office) hallway, passing safely/comfortably/without prolonged hesitation | Consistent — specialized, not contradicted |
| Physical Env | Generic | Indoor (office hallway) | Consistent specialization |
| Geometric Layout | Passable space | passable space | Exact match |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Exact match |
| Robot Task | Navigate A to B | navigate from A to B | Exact match |
| Human Behavior | Navigate B to A | navigate from B to A | Exact match |
| Ideal Outcome | Robot/humans pass | robot and human pass each other safely, comfortably, and without prolonged hesitation | Consistent, elaborated |
| Related Scenarios | Ped. Obstruct (no implemented directory) | blind_corner, movable_obstruction, single_file_hallway | Expected divergence — Table 3's named scenario has no implemented directory, and the card substitutes implemented scenarios it discusses in `evaluation_notes`; this is one of the checklist's explicitly-not-a-defect cases, and the card's own notes already explain the substitution |
| Cited In | [50, 126, 167] | "50", "126", "167" | Exact match |

All verified `related_scenarios` directory references (`blind_corner`,
`movable_obstruction`, `single_file_hallway`) exist under
`src/prosoc/prnc/scenarios/`. Overall: the card is faithful to Table 3
wherever Table 3 specifies a value, with only the expected and
self-documented Related-Scenarios substitution — the only real issue is the
SOURCE line's framing versus this fidelity (Finding 1), not the content
itself.

## Completeness

- Scenario Card Summary: all required fields present (Scenario Name,
  Description, Scientific Purpose, Physical Environment, Geometric Layout,
  Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics,
  Ideal Outcome, Related Scenarios, Cited In).
- Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome,
  Failure Modes, and Labeling Criteria are all present and match the embedded
  YAML `scenario_usage_guide` block.
- `## Social Navigation Context` and `## Normative Expectations` are
  reasonably blank (optional per `template.md`; see Finding 2) — not required
  for AUDITED and not blocking.
