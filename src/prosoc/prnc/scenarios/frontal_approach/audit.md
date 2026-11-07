---
family: scenarios
card: frontal_approach
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-11-07
---

# Audit: Frontal Approach

- **Card:** `src/prosoc/prnc/scenarios/frontal_approach/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED, no blocking or should-fix issues — one
  low-priority suggestion only.

This is a fresh audit written after `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`
resolved the prior audit's should-fix Finding 1 (SOURCE line vs. Table 3
fidelity). It does not carry forward that finding's text, since the SOURCE
line it described no longer exists.

## Findings

### Resolved: SOURCE field disclaimed external-citation derivation that the card's own content contradicted

The prior audit's should-fix Finding 1 is resolved. SOURCE now reads:
`P&G Paper, Table 3 "Frontal Approach" entry (Francis et al., 2025, ACM
THRI Vol. 14, No. 2, Article 34); cited in [50, 126, 167]` — matching the
convention used by other Table-3-sourced cards in this family (e.g.
`blind_corner/scenario.md`'s SOURCE line) and no longer contradicting the
card's own `cited_in`/`evaluation_notes` content. This is a Markdown-only
metadata edit — `scenario.yml` has no `source` field, confirmed by
`scripts/distill/scenarios --scenario frontal_approach --dry-run
--show-diffs` reporting no differences (re-run fresh for this audit, with
the correct `PYTHONPATH` for this checkout).

### 1. Optional "Social Navigation Context" and "Normative Expectations" prose sections are entirely absent — suggestion
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

SOURCE now explicitly cites the P&G Table 3 "Frontal Approach" entry.
Re-verified directly against `../pg_scenarios.md`:

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
self-documented Related-Scenarios substitution; SOURCE now accurately
reflects that fidelity instead of contradicting it.

## Completeness

- Scenario Card Summary: all required fields present (Scenario Name,
  Description, Scientific Purpose, Physical Environment, Geometric Layout,
  Robot Role, Robot Task, Human Behavior, Success Metrics, Quality Metrics,
  Ideal Outcome, Related Scenarios, Cited In).
- Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome,
  Failure Modes, and Labeling Criteria are all present and match the embedded
  YAML `scenario_usage_guide` block.
- `## Social Navigation Context` and `## Normative Expectations` are
  reasonably blank (optional per `template.md`; see Finding 1) — not required
  for AUDITED and not blocking.
