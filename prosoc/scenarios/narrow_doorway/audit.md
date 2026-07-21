---
scenario: narrow_doorway
verdict: ready
blocking: 0
should_fix: 0
suggestion: 2
audited: 2026-07-20
---

# Audit: Narrow Doorway

- **Scenario:** `prosoc/scenarios/narrow_doorway/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-20
- **Verdict:** Ready, no blocking issues found

## Findings

### 1. "Related Scenarios" and "Cited In" are self-flagged as blank in the Scenario Card Summary — suggestion
- **Section/field:** Scenario Card Summary ("Remaining gaps" note) vs. `related_scenarios` / `cited_in` (both optional per `schema.json`, currently absent from `scenario.yml`)
- **Issue:** The card now includes a full `## Scenario Card Summary` section (this addresses the prior 2026-07-05 audit's Finding 1, which noted the section was entirely missing). However, its own "Remaining gaps" note flags **Related Scenarios** and **Cited In** as `should-fill-in-now`, and both are readily available elsewhere in the card: "Notes for Scenario Designers and Evaluators" already names *Narrow Arch*, *Blind Corner*, *Entering Room*, and *Exiting Room* as related scenarios, and the Status block's SOURCE line already reads "cited in [126]". Neither has been transcribed into the Card Summary bullets or into the `related_scenarios` / `cited_in` YAML keys.
- **Recommended fix:** Add `- **Related Scenarios:** Narrow Arch, Blind Corner, Entering Room, Exiting Room` and `- **Cited In:** 126` to the Card Summary block, and add corresponding `related_scenarios:` / `cited_in:` keys to the embedded YAML (re-run the distiller afterward to sync `scenario.yml`). Low severity — all underlying content already exists in the card, this is a transcription gap rather than missing information.

### 2. `expected_behaviors.should` mixes a graded/comparative claim ("proceed decisively and without hesitation") — suggestion
- **Section/field:** `expected_behaviors.should` vs. P&G Guideline N6 (over-specification)
- **Issue:** Unchanged from the prior audit. The entries are phrased as kinds of behavior ("recognize... adjust approach speed," "yield clearly," "proceed decisively... without hesitation") rather than exact motions or numeric thresholds, so this is not a blocking over-specification violation. However, "proceed decisively and without hesitation" edges toward prescribing manner/style rather than outcome; it is defensible as legibility guidance but worth a second look.
- **Recommended fix:** No change required; flagging only as a minor style note. If tightened, could be rephrased as "proceed without ambiguity about intent" to keep focus on legibility (the underlying principle, P3) rather than motion style.

## Source Fidelity

SOURCE cites "P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2, Article 34); cited in [126]." This matches the Table 3 entry in `.claude/skills/_shared/pg_scenarios.md` under Doorway Scenarios → **Narrow Doorway**. Comparison:

| Field | P&G Table 3 (`pg_scenarios.md`) | This scenario | Match? |
|---|---|---|---|
| Description | Robot and human at a narrow doorway (room and door) | Robot and human pedestrian approach a narrow doorway from opposite directions, single-file passage | Yes |
| Physical Env | Indoor | `context.environment.type: indoor` | Yes |
| Geometric Layout | Room and door | `geometric_layout: room and door` | Yes |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Yes |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B through the doorway` | Yes |
| Human Behavior | Navigate B to A | `intended_human_behavior: navigate from B to A through the doorway` | Yes |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot and human sequence through the doorway one at a time without collision or obstruction` | Yes |
| Related Scenarios | Narrow Arch | Noted in "Notes for Scenario Designers and Evaluators," not yet in Card Summary or YAML (see Finding 1) | Yes, informally |
| Cited In | [126] | SOURCE field cites [126], not yet transcribed to Card Summary or YAML (see Finding 1) | Yes, informally |

**Source fidelity: checked against P&G Table 3 — full match, no mismatches found.** All physical description, purpose, layout, roles, task, and ideal-outcome fields are consistent with the canonical Table 3 entry, and the "Related Scenarios" cross-reference (Narrow Arch) is preserved in prose even though not yet formalized in the Card Summary/YAML.

## Completeness

Walking `template.md`'s "Required for AUDITED scenarios" fields:

**Scenario Card Summary** (now present as a standalone section — resolves the prior audit's Finding 1):
- Scenario Name — present ("Narrow Doorway")
- Scenario Description — present
- Scientific Purpose — present (`pedestrian interaction`)
- Physical Environment — present (`indoor`)
- Geometric Layout — present (`room and door`)
- Robot Role — present (`navigating_agent`)
- Robot Task / Human Behavior — present
- Success Metrics / Quality Metrics — present (SR, NoCollisions / P3, P4), consistent between Card Summary, YAML, and the Scenario Usage Guide prose section
- Ideal Outcome — present
- Related Scenarios — should-fill-in-now (see Finding 1); content already exists informally in the Notes section
- Cited In — should-fill-in-now (see Finding 1); content already exists in the SOURCE line

**Scenario Usage Guide** (now present as a standalone prose section, in addition to the YAML):
- Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria — all present and consistent between the prose section (lines under `## Scenario Usage Guide`) and `scenario_usage_guide` in the YAML. No gaps.

This card remains in good shape: schema-valid (dry-run distiller check produced no diff), principle count within guidance (4, within 3–5), no invented-principle issues, and full Table 3 fidelity. The only remaining gaps are the two suggestion-level items above (Related Scenarios / Cited In transcription, and a minor phrasing note), both low severity and both a human editorial choice rather than a blocker to AUDITED promotion.
