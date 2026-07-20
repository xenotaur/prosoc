---
scenario: intersection_no_gesture
verdict: not_ready
blocking: 1
should_fix: 1
suggestion: 2
audited: 2026-07-05
---

# Audit: Intersection – No Gesture

- **Scenario:** `prosoc/scenarios/intersection_no_gesture/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready — 1 blocking issue (corrected 2026-07-05 — see Correction Notice)

## Correction Notice (2026-07-05)

This audit originally flagged `P0` in `relevant_principles` as an invalid,
non-canonical principle ID (Finding 1 below). That was incorrect:
`prosoc/charter/charter.md` (the sole source of truth) defines **ten** principles,
P0–P9 — P0 (Goal Achievement) is this project's own explicit, intentional
extension beyond the P&G paper's eight, not an invented ID. `charter.yml` (the
generated artifact) confirms this (distiller dry-run reports no diff). The error
originated in a stale `.claude/skills/_shared/principles.md`, which claimed only
P1–P8 were valid and has since been corrected. Finding 1 is retracted; Finding 4
is corrected to reflect the real principle count of 5, not 4.

### 1. ~~Invalid principle ID `P0` in `relevant_principles`~~ — RETRACTED
- **Status:** Retracted 2026-07-05. See Correction Notice above — P0 is a valid
  canonical principle per `prosoc/charter/charter.md`, not an invented ID.

### 2. Missing `scenario_usage_guide` block entirely — blocking
- **Section/field:** Scenario Specification (YAML) — `scenario_usage_guide` (success_metrics, quality_metrics, failure_modes, labeling_criteria)
- **Issue:** The embedded YAML has no `scenario_usage_guide` key at all. `template.md` marks the Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria) as "Required for AUDITED scenarios."
- **Recommended fix:** Add a `scenario_usage_guide` block. Much of the content is inferable from prose already on the card (see Completeness below) — a human editor should draft it before promoting to AUDITED.

### 3. Missing "Scenario Card Summary" section — should-fix
- **Section/field:** Prose — no "Scenario Card Summary" heading present (template.md requires it for AUDITED)
- **Issue:** The card jumps from Status straight to Scenario Overview; the structured summary block (Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success/Quality Metrics, Ideal Outcome, Related Scenarios, Cited In) is entirely absent.
- **Recommended fix:** Add the section, drawing on prose already present (Overview, Normative Expectations) and the `../../../.claude/skills/_shared/pg_scenarios.md` Table 3 entry for "Intersection No Gesture."

### 4. `relevant_principles` count of 5 (P0, P1–P4) sits at the upper edge of guidance and omits some plausible candidates — suggestion
- **Section/field:** `relevant_principles` (P0, P1, P2, P3, P4 — corrected 2026-07-05, see Correction Notice)
- **Issue:** With P0 correctly counted as valid, 5 principles are listed — at the top of the 3–5 guidance band, not over it. However, the prose repeatedly emphasizes "implicit coordination," "mutual anticipation of trajectories," and avoiding "oscillate indecisively" — which sound like P6 (Agent Understanding — predicting the human's trajectory/intent) and P7 (Proactivity — resolving the ambiguity/deadlock without hesitation). Neither is listed.
- **Recommended fix:** Human editor should consider whether P6 or P7 would be more central than one of the currently-listed entries, without exceeding 5 total.

### 5. Possible over-specification in `should_not` — suggestion
- **Section/field:** `expected_behaviors.should_not` vs. P&G Guideline N6 (over-specification)
- **Issue:** Entries like "oscillate indecisively at the intersection" and "force the human to stop abruptly" describe kinds of behavior (fine), but "aggressively assert right-of-way" borders on prescribing a specific strategy rather than a behavior category. This is a mild case, not a clear violation — flagged as suggestion-level only.
- **Recommended fix:** Optional — human editor may leave as-is, since it still describes a behavior class rather than an exact motion/threshold.

## Source Fidelity

SOURCE cites "Principles and Guidelines for Social Robot Navigation (Table 3)," matching `../../../.claude/skills/_shared/pg_scenarios.md`'s "Intersection No Gesture" entry. Comparison:

| Field | Table 3 (pg_scenarios.md) | This scenario | Match? |
|---|---|---|---|
| Description | Robot and human cross at an indoor intersection without gesture | Robot and human pedestrian approach/cross indoor intersection, no explicit gestural communication | Match |
| Physical Env | Indoor | indoor | Match |
| Geometric Layout | Intersection | hallway intersection | Match |
| Robot Task | Navigate A to B | Consistent with prose ("approach and cross an indoor intersection"); no explicit `intended_robot_task` YAML field present (see Completeness) | Match (loosely) |
| Human Behavior | Cross navigate | human pedestrian, `gesturing: none` | Match |
| Robot Role | (not specified in Table 3 for this entry) | `navigating_agent` | No conflict — Table 3 has no Robot Role for this entry, so nothing to mismatch |
| Ideal Outcome | Both pass, no collision | `expected_behaviors.must` includes "avoid collision with the human at the intersection," consistent — but no explicit `ideal_outcome` YAML field present at all | Partial — `ideal_outcome` field is missing (see Completeness) |
| Cited In | [27, 50, 167] | Not reproduced in this card (no Cited In field present) | N/A — Scenario Card Summary section (which would carry this) is absent |

Overall: broadly faithful to Table 3, no contradictions found. The one gap is the missing `ideal_outcome` field (see Completeness), which otherwise aligns with the source's "both pass, no collision" outcome per the prose and `expected_behaviors.must`.

## Completeness

Fields required for AUDITED per `template.md`:

- **Scenario Card Summary section** — **should probably be filled in now.** Entirely absent; content is readily inferable from Overview/Normative Expectations prose and the Table 3 entry.
- **`ideal_outcome` (YAML field)** — **should probably be filled in now.** Not present in the embedded YAML at all, even though `schema.json` defines it and prose clearly implies one ("both agents pass smoothly without collision or hesitation").
- **`scenario_usage_guide.success_metrics`** — **should probably be filled in now.** Plausible candidates (e.g., NoCollisions, SR) are directly inferable from `expected_behaviors.must` ("avoid collision").
- **`scenario_usage_guide.quality_metrics`** — **should probably be filled in now.** Should mirror a corrected `relevant_principles` list.
- **`scenario_usage_guide.failure_modes`** — **should probably be filled in now.** Already implied in prose ("overly aggressive entry, excessive hesitation, or late yielding that disrupts the human's motion") and in `evaluation_notes` — just needs to be lifted into the structured field.
- **`scenario_usage_guide.labeling_criteria`** — **reasonably blank**, in the sense that it requires new authoring judgment (how an annotator would recognize this scenario in a trace, independent of behavior quality) rather than being a straightforward lift from existing prose.
- **Related Scenarios / Cited In (Scenario Card Summary sub-fields)** — **reasonably blank** for now if the Scenario Card Summary section is being added fresh, though the Notes section already gestures at "gesture-based intersection scenarios" as related, and "Cited In: [27, 50, 167]" is available from `pg_scenarios.md`.
