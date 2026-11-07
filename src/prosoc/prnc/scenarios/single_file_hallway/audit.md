---
family: scenarios
card: single_file_hallway
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-11-07
---

# Audit: Single File Hallway

- **Card:** `src/prosoc/prnc/scenarios/single_file_hallway/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-11-07
- **Verdict:** Ready for AUDITED with a minor fix — one should-fix prose/YAML
  drift, caught and corrected in review, plus one low-priority structural
  suggestion.

This is a fresh audit of the card's current content, written from scratch
after the card was demoted from `APPROVED` back to `EDITED`
(`WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION`) because two prose-only
edits (2026-11-05, 2026-11-06) postdated the prior `audit.md` (2026-08-06).
It does not carry forward or assume any findings from that prior audit.

## Findings

### 1. `expected_behaviors.must` drops the prose's conflict-recognition qualifier — should-fix
- **Section/field:** "Normative Expectations" prose vs.
  `expected_behaviors.must`
- **Issue:** **Caught in review.** An earlier draft of this audit declared
  the prose and YAML `must` items an exact match. They are not: the prose
  says the robot "must not enter the hallway simultaneously with the human
  **once a conflict is recognized**," but the YAML `must` item reads only
  "avoid entering the hallway simultaneously with the human," with no
  recognition condition. A robot that enters simultaneously before a
  conflict is recognized would satisfy the prose's conditional requirement
  but violate the YAML's unconditional one -- a genuine one-sided drift
  (YAML is stricter than prose), not a cosmetic wording difference.
- **Recommended fix:** A human editor should reconcile the two: either add
  the recognition condition to the YAML `must` item, or confirm the
  unconditional YAML reading is actually intended (i.e. the robot must
  never enter simultaneously, recognition or not) and loosen the prose's
  qualifier to match. This audit does not edit the card.

### 2. No dedicated "Social Navigation Context" prose section — suggestion
- **Section/field:** Markdown structure vs. `template.md`'s "Social Navigation
  Context" section (marked "Optional but recommended").
- **Issue:** The card includes "Scenario Overview" and "Normative
  Expectations" but has no separate "Social Navigation Context" section
  describing common human expectations, sources of ambiguity/asymmetry, and
  why the scenario is socially/scientifically interesting.
- **Recommended fix:** Optional, not required for `AUDITED`. The "Discussion"
  section (below the machine-readable YAML block) already substantively
  covers the "why this is interesting" angle ("a clean control case for
  proactivity... cleanly separates P7 from P9"), so nothing is actually
  missing from the card's content — a human editor could, at their
  discretion, lift a sentence or two into a dedicated Social Navigation
  Context section purely for closer conformance to `template.md`'s section
  layout.

One should-fix prose/YAML drift was found (Finding 1); no contradictions,
schema violations, or blocking issues were found.

## Prose/YAML Consistency

- **Scenario Overview vs. `intended_robot_task` / `intended_human_behavior` /
  `context`:** Consistent. The hallway-too-narrow-to-pass framing, the
  single-file geometry (`context.environment.width: single_file`,
  `geometric_layout: narrow hallway`), and the two agents' tasks all match.
- **Normative Expectations prose vs. `expected_behaviors.{must,should,should_not}`:**
  Mostly consistent, but see Finding 1: the prose's first `must` item
  carries a "once a conflict is recognized" qualifier the YAML `must` item
  drops -- a genuine one-sided drift, not an exact match. The `should`
  paragraph matches all three `should` items; the `should_not` paragraph
  matches all three `should_not` items.
- **`ideal_outcome`:** Identical string used in the Scenario Card Summary, the
  fenced YAML, and the standalone Scenario Usage Guide section — no drift.
- **Scenario Card Summary vs. fenced YAML:** Success Metrics, Quality
  Metrics, Robot Role, Physical Environment, and Geometric Layout all match
  the YAML fields exactly.

### Distiller check

`scripts/distill/scenarios --scenario single_file_hallway --dry-run
--show-diffs` reports **no diff and no schema validation error** — run fresh
for this audit. `scenario.md`'s embedded YAML and `scenario.yml` are in
sync; no drift to report as blocking.

## Schema and Charter Compliance

- `scenario.yml` validates against `schema.json`; `expected_behaviors` has
  only `must`/`should`/`should_not`.
- `relevant_principles` (`P1, P3, P5, P7`) are all valid P0–P9 IDs; count of 4
  is within the 3–5 guideline, so no explicit-discussion check is required.
- `scenario_usage_guide.quality_metrics` (`P3, P5, P7`) — valid IDs, and a
  subset of `relevant_principles` as expected.
- `related_scenarios` (`frontal_approach`, `movable_obstruction`) reference
  real directories under `src/prosoc/prnc/scenarios/` (both confirmed to
  exist) and match the card's own Discussion section, which explicitly frames
  all three as "a minimal scenario set."
- Charter alignment: cited principles (Safety, Legibility, Social
  Competency, Proactivity) match `principles.md`'s P0–P9 definitions and are
  used consistently with their defined meanings.

## Source Fidelity

The card's `SOURCE` line states this scenario is **not** derived from the
P&G paper's Table 3 or Figure 7, despite a superficial thematic resemblance
to Figure 7's "Narrow Hallway" sketch — it was "developed specifically for"
*The Prosocial Robot Navigation Charter* (Francis, in press at Frontiers),
§4.2.1. This is consistent with `../_shared/pg_scenarios.md`'s own
2026-08-06 correction note, which explicitly supersedes an earlier,
incorrect guess that this scenario was extrapolated from Figure 7, and
states it is "original to that paper, not derived from or extrapolated from
any P&G Table 3 entry or Figure 7 sketch." No contradiction between the
card's `SOURCE` line and `pg_scenarios.md`'s reference data.

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

A prior, now-superseded audit (dated 2026-08-06, since invalidated by edits
made after it) reports having had the actual paper PDF attached via
`--paper` and performed a paragraph-level textual comparison, including a
near-verbatim match against the paper's own published `expected_behaviors`
listing. If that PDF becomes available again for a future audit, repeating
that direct comparison would be more conclusive than this pass's
reference-only check.

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
- **`Cited In`** — reasonably blank. **Caught in review:** the card's own
  "Remaining gaps" note makes the narrower claim that no external citations
  are currently *recorded* for this scenario -- not that none exist. The
  2026-11-05 copyedit (`WI-CHARTER-SUPPLEMENT-COPYEDIT-FIXES`) deliberately
  narrowed this from an earlier, broader claim; being in press doesn't
  establish that no citations exist, only that none are currently known/
  recorded. This phrasing (and label) is itself correct and current as
  written -- an earlier draft of this audit reversed the distinction.
- **"Social Navigation Context" section** — reasonably blank (optional,
  see Finding 2); its substance is already covered by the Discussion
  section elsewhere in the card.
