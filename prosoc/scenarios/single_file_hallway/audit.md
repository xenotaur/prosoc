---
scenario: single_file_hallway
verdict: ready_with_fixes
blocking: 0
should_fix: 1
suggestion: 1
audited: 2026-07-20
---

# Audit: Single File Hallway

- **Scenario:** `prosoc/scenarios/single_file_hallway/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready for AUDITED with minor fixes — all three prior blocking issues
  (duplicated `should_not` entries, missing Scenario Card Summary, missing Scenario
  Usage Guide prose) are resolved in the current card; only minor prose-completeness
  gaps remain.

## Findings

### 1. `expected_behaviors.must` items not echoed anywhere in prose — should-fix
- **Section/field:** Scenario Overview (prose) vs. `expected_behaviors.must`
- **Issue:** `scenario.md` has no "Normative Expectations" or "Social Navigation
  Context" section (both optional per `template.md`, but recommended). The Scenario
  Overview does summarize the `should` list in natural language ("The robot must
  anticipate the conflict and take initiative—through signaling, yielding, or
  negotiation—to prevent deadlock or discomfort"), but the two safety-critical `must`
  items — "maintain a safe physical distance from the human" and "avoid entering the
  hallway simultaneously with the human" — are not stated anywhere in prose; they
  exist only inside the embedded YAML/`scenario.yml`. This is a one-sided claim per
  the audit checklist (behavior specified in YAML but absent from prose).
- **Recommended fix:** Add a short "Normative Expectations" section (as
  `robot_overtaking`'s card has) that states the required minimum behaviors —
  maintaining safe distance and not entering the hallway simultaneously with the
  human — in natural language, alongside the already-covered `should` guidance.

### 2. "Cited In" gap note is stale/misleading given source limitations — suggestion
- **Section/field:** Scenario Card Summary "Remaining gaps" note vs. Source Fidelity
- **Issue:** The Card Summary block still carries a self-flagged note: "**Remaining
  gaps:** Cited In — should-fill-in-now." However, per
  `../../../.claude/skills/_shared/pg_scenarios.md`, `single_file_hallway` corresponds
  to the Figure 7 "Narrow Hallway" sketch, which — unlike full Table 3 entries — has no
  citation-index data available at all ("they do not have full Table 3 metadata").
  There is no retrievable citation to fill in, so labeling this "should-fill-in-now"
  overstates what's actually actionable; it reads more like "reasonably blank pending
  a source that has this data."
- **Recommended fix:** Either reword the gap note to reflect that Cited In is
  currently unfillable from available sources (not a pending to-do), or remove the
  note entirely if the omission is considered acceptable for a Figure-7-derived
  scenario.

## Source Fidelity

SOURCE is explicitly cited as "Principles and Guidelines for Evaluating Social Robot
Navigation (P&G paper)" — a checkable source in principle. However, per
`../../../.claude/skills/_shared/pg_scenarios.md`, "Single File Hallway" is **not**
one of the 18 named entries in P&G Table 3. The reference file's "Additional Scenarios
(Figure 7, not in Table 3)" section states:

> The `single_file_hallway` scenario in the repo corresponds to the **Narrow Hallway**
> figure [in Figure 7]... If implementing these, note that they do not have full Table
> 3 metadata and should be extrapolated carefully from the paper's descriptions and
> Figure 7.

Comparing the card against what's available:
- **Correspondence to Narrow Hallway (Figure 7):** The card's description — "a hallway
  that is too narrow for safe and comfortable passing... single-file passage" — is
  consistent with `pg_scenarios.md`'s one-line gloss: "single-file passage in a narrow
  corridor." No contradiction found.
- **No Table 3 metadata to compare against:** Because Narrow Hallway has no full Table
  3 entry (no Scientific Purpose, Robot Task, Human Behavior, Ideal Outcome, or Cited
  In fields listed in `pg_scenarios.md` beyond the one-line description), a
  field-by-field fidelity check like the one possible for Table 3 scenarios cannot be
  performed for `scientific_purpose`, `intended_robot_task`, `intended_human_behavior`,
  `ideal_outcome`, or `cited_in` — all of these were authored this session without a
  ground-truth Table 3 entry to check against.

**Source fidelity: partially checkable.** The high-level correspondence to the Figure
7 "Narrow Hallway" concept holds, and the newly-authored fields (scientific_purpose,
geometric_layout, intended_robot_task, intended_human_behavior, ideal_outcome) are all
internally plausible and consistent with the Figure 7 gloss and the card's own
Overview/Discussion prose, but they cannot be verified against Table-3-style
ground truth because none exists for this scenario. Verifying deeper fidelity would
require reading the P&G paper's Figure 7 discussion directly (not provided as
`--paper` input for this audit) — this audit does not fabricate that comparison.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary:** Complete except **Cited In**, which is blank and
  self-flagged in a "Remaining gaps" note (see Finding 2) — reasonably blank given no
  citation data exists for this Figure-7-derived scenario in the available reference
  material, though the note's phrasing overstates it as actionable.
- **Scenario Usage Guide — Success Metrics:** Complete (SR, NoCollisions,
  DeadlockFree).
- **Scenario Usage Guide — Quality Metrics:** Complete (P3, P5, P7 — consistent with
  `relevant_principles` [P1, P3, P5, P7]).
- **Scenario Usage Guide — Ideal Outcome:** Complete, present both in the YAML
  `ideal_outcome` field and the Card Summary/Usage Guide prose.
- **Scenario Usage Guide — Failure Modes:** Complete (three concrete failure modes).
- **Scenario Usage Guide — Labeling Criteria:** Complete (three concrete,
  data-recognizable criteria).

No required fields are blank aside from the optional Cited In noted above. The
optional "Normative Expectations" prose section remains absent (see Finding 1).
