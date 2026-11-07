---
family: scenarios
card: movable_obstruction
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 2
audited: 2026-11-07
---

# Audit: Movable Obstruction

- **Card:** `src/prosoc/prnc/scenarios/movable_obstruction/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready with one should-fix — the card is internally coherent
  and schema/charter-compliant, but is missing a prose section that its
  sibling card (`single_file_hallway`) already has, and that a prior audit
  of this exact card once required closing before full readiness.

This is a fresh audit of the card's current content, written from scratch
after the card was demoted from `APPROVED` back to `EDITED`
(`WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION`) because a prose-only edit
(2026-11-05) postdated the prior `audit.md` (2026-08-06). It does not carry
forward or assume any findings from that prior audit.

## Findings

### 1. Missing "Normative Expectations" prose section — should-fix
- **Section/field:** Markdown structure — the card has "Scenario Overview"
  followed directly by "Scenario Specification (Machine-Readable)", with no
  "Normative Expectations" section in between.
- **Issue:** `template.md` marks "Normative Expectations" as "Optional but
  recommended," intended to describe acceptable/unacceptable robot behavior
  in natural language, as interpretive guidance beyond the formal YAML spec.
  The sibling scenario `single_file_hallway` has this section, restating its
  `must`/`should`/`should_not` items as readable prose. `movable_obstruction`
  does not: a human reader gets the YAML's `expected_behaviors` list and a
  high-level "Discussion," but no plain-language walk-through of what the
  robot must/should/should-not do. This is also the audit checklist's
  Prose/YAML Cross-Check target for this section — with no prose to check,
  there is nothing to cross-reference `expected_behaviors` against beyond
  the YAML's own comments and the brief bullet list in the Scenario Usage
  Guide, which essentially repeats the YAML rather than restating it in
  natural language.
  Notably, a prior audit of `single_file_hallway` (referenced in that card's
  own edit history) once treated this exact gap as a should-fix that had to
  be closed before promotion; this card has never had that gap closed.
- **Recommended fix:** Add a "Normative Expectations" section between
  "Scenario Overview" and "Scenario Specification (Machine-Readable)",
  restating the `must`/`should`/`should_not` items in prose — directly
  inferable from the content already present in the card's own
  `expected_behaviors` YAML, so this requires no new content decisions, only
  transcription into prose (mirroring `single_file_hallway`'s existing
  section as a model).

### 2. `relevant_principles` count (6) exceeds the 3–5 guideline, and P5 lacks explicit grounding — suggestion
- **Section/field:** `relevant_principles` (`P0, P1, P3, P5, P7, P9`) vs.
  the card's prose (Scenario Overview, Discussion) and
  `scenario_usage_guide.quality_metrics` (`P3, P7, P9`).
- **Issue:** Per `../_shared/principles.md`, a count above 5 is acceptable
  only when the card's own prose explicitly discusses each included
  principle. P0 ("Trade-offs between Goal Achievement (P0) and prosocial
  action"), P7, and P9 are all explicitly named and discussed in the
  Scenario Overview and Discussion sections. P1 and P3 are not named by ID
  in prose, but are clearly grounded in specific `expected_behaviors` items
  (safety distance / evasive-action avoidance for P1; "communicate intent
  clearly" plus `quality_metrics` inclusion for P3). **P5 (Social
  Competency)**, however, has no clear grounding anywhere: it is not named
  in prose, not included in `quality_metrics`, and no `expected_behaviors`
  item maps obviously to a social-convention concern distinct from safety,
  legibility, or proactivity.
- **Recommended fix:** Either drop `P5` from `relevant_principles` (it
  currently reads as padding against the 3–5 guideline), or — if a human
  editor believes it belongs (e.g., tying it to "force the human into
  single-file passage without acknowledgment" as a social-norms concern) —
  add a sentence to the (currently-missing, see Finding 1) Normative
  Expectations section naming and justifying it explicitly, and consider
  adding it to `quality_metrics` for consistency.

### 3. No dedicated "Social Navigation Context" prose section — suggestion
- **Section/field:** Markdown structure vs. `template.md`'s "Social
  Navigation Context" section (marked "Optional but recommended").
- **Issue:** Same gap as noted in `single_file_hallway`'s audit: no section
  describing common human expectations, sources of ambiguity, or why the
  scenario is socially/scientifically interesting, separate from the
  Overview/Discussion.
- **Recommended fix:** Optional, not required for `AUDITED`. The
  "Discussion" section (below the YAML block) already substantively covers
  this ground ("explicitly extends Frontal Approach by introducing a
  decision point where environmental improvement is possible..."), so
  nothing is actually missing from the card's content — only its section
  layout diverges from the template.

## Prose/YAML Consistency

- **Scenario Overview vs. `intended_robot_task` / `intended_human_behavior` /
  `context`:** Consistent. The "nominally wide enough... partially blocked
  by a movable obstruction" framing matches `geometric_layout: passable
  space, partially obstructed` and `context.environment.obstruction`.
- **`expected_behaviors` vs. prose:** No contradictions found, but (per
  Finding 1) there is no dedicated prose section to cross-check against —
  the Discussion section's high-level framing ("boundary between conflict
  avoidance (P7) and environmental stewardship (P9)") is consistent with,
  but does not restate, the specific `must`/`should`/`should_not` items.
- **`ideal_outcome`:** Identical string used in the Scenario Card Summary,
  the fenced YAML, and the standalone Scenario Usage Guide section — no
  drift.
- **Evaluation notes' task/context cross-reference:** Independently
  verified against the actual corpus — `navigate.point_to_point`,
  `deliver.object` (in `src/prosoc/prnc/tasks/`), and
  `service.routine_delivery`, `guidance.docent`, `emergency.high_urgency`
  (in `src/prosoc/prnc/contexts/`) all exist with exactly these IDs. No
  one-sided or stale references.

### Distiller check

`scripts/distill/scenarios --scenario movable_obstruction --dry-run
--show-diffs` reports **no diff and no schema validation error** — run
fresh for this audit. `scenario.md`'s embedded YAML and `scenario.yml` are
in sync; no drift to report as blocking.

## Schema and Charter Compliance

- `scenario.yml` validates against `schema.json`; `expected_behaviors` has
  only `must`/`should`/`should_not`.
- `relevant_principles` entries are all valid P0–P9 IDs (see Finding 2 for
  the count/grounding concern — a suggestion, not a schema violation).
- `scenario_usage_guide.quality_metrics` (`P3, P7, P9`) — valid IDs, a
  subset of `relevant_principles` as expected.
- `related_scenarios` (`frontal_approach`, `single_file_hallway`) reference
  real directories under `src/prosoc/prnc/scenarios/` (both confirmed to
  exist) and match the card's own Discussion section, which frames this
  scenario as extending `frontal_approach` and pairs it with
  `single_file_hallway`.
- Charter alignment: cited principles (Goal Achievement, Safety, Legibility,
  Social Competency, Proactivity, Prosocial Behavior) match
  `principles.md`'s P0–P9 definitions; the P0/P9 trade-off this scenario is
  built around is used consistently with the charter's own framing of P0 and
  P9.

## Source Fidelity

The card's `SOURCE` line states this scenario is **not** derived from the
P&G paper, which "has no Table 3 or Figure 7 counterpart for this
scenario" — it was "developed specifically for" *The Prosocial Robot
Navigation Charter* (Francis, in press at Frontiers), §4.2.1. This is
consistent with `../_shared/pg_scenarios.md`'s own 2026-08-06 correction
note, which explicitly states this scenario (alongside `single_file_hallway`)
is "original to that paper, not derived from or extrapolated from any P&G
Table 3 entry or Figure 7 sketch." No contradiction between the card's
`SOURCE` line and `pg_scenarios.md`'s reference data.

Beyond that internal cross-reference check, **direct fidelity against the
primary source — the in-press Frontiers paper itself — is not checkable in
this audit pass.** No `--paper` input was supplied for this invocation, and
the only PDF present in the working tree
(`build/papers/01_charter/rendered.pdf`) was checked and found to be this
project's own generated rendering of its scenario/task/context cards (it
reproduces this very card's prose, including its "Discussion" section,
nearly verbatim as a numbered subsection) — a self-referential build
artifact, not an independent copy of the cited paper. Comparing the card
against it would not be a meaningful fidelity check.

A prior, now-superseded audit (dated 2026-08-06, since invalidated by an
edit made after it) reports having had the actual paper PDF attached via
`--paper` and performed a paragraph-level textual comparison, including
confirming the task/context worked example and the High-Urgency nuance
against the paper's §4.2.2 discussion. If that PDF becomes available again
for a future audit, repeating that direct comparison would be more
conclusive than this pass's reference-only check.

**Source fidelity: not checkable against the primary source this pass;
no contradiction found against the project's own corrective reference
data (`pg_scenarios.md`).**

## Completeness

All fields required by `schema.json` and marked "Required" or "Required for
AUDITED" in `template.md` are present and non-contradictory:

- Scenario Card Summary: Scenario Name, Description, Scientific Purpose,
  Physical Environment, Geometric Layout, Robot Role, Robot Task, Human
  Behavior, Success Metrics, Quality Metrics, Ideal Outcome, Related
  Scenarios — all present.
- Scenario Usage Guide: Success Metrics, Quality Metrics, Ideal Outcome,
  Failure Modes, Labeling Criteria — all present, both in the Summary and in
  the standalone "Scenario Usage Guide" section.
- **`Cited In`** — reasonably blank. The card's own "Remaining gaps" note
  explains this scenario originates in a source paper that is itself still
  in press and not yet widely available, so no external citations currently
  exist to record. This phrasing (and label) is itself correct and current.
- **"Normative Expectations" section — should probably be filled in now**
  (see Finding 1): directly inferable from the already-present
  `expected_behaviors` YAML, not genuinely unknown or inapplicable.
- **"Social Navigation Context" section** — reasonably blank (optional,
  see Finding 3); its substance is already covered by the Discussion
  section elsewhere in the card.
