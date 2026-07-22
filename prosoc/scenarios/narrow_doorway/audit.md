---
scenario: narrow_doorway
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-21
---

# Audit: Narrow Doorway

- **Scenario:** `prosoc/scenarios/narrow_doorway/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready, no blocking issues found — the prior audit's Related
  Scenarios/Cited In transcription gap is now resolved.

## Findings

### 1. `expected_behaviors.should` mixes a graded/comparative claim ("proceed decisively and without hesitation") — suggestion
- **Section/field:** `expected_behaviors.should` vs. P&G Guideline N6 (over-specification)
- **Issue:** Unchanged from prior audits. The entries are phrased as kinds of behavior
  ("recognize... adjust approach speed," "yield clearly," "proceed decisively...
  without hesitation") rather than exact motions or numeric thresholds, so this is not
  a blocking over-specification violation. However, "proceed decisively and without
  hesitation" edges toward prescribing manner/style rather than outcome; it is
  defensible as legibility guidance but worth a second look.
- **Recommended fix:** No change required; flagging only as a minor style note. If
  tightened, could be rephrased as "proceed without ambiguity about intent" to keep
  focus on legibility (the underlying principle, P3) rather than motion style.

## Source Fidelity

SOURCE cites "P&G Paper, Table 3 (Francis et al., 2025, ACM THRI Vol. 14, No. 2,
Article 34); cited in [126]." This matches the Table 3 entry in
`.claude/skills/_shared/pg_scenarios.md` under Doorway Scenarios → **Narrow Doorway**.
Comparison:

| Field | P&G Table 3 (`pg_scenarios.md`) | This scenario | Match? |
|---|---|---|---|
| Description | Robot and human at a narrow doorway (room and door) | Robot and human pedestrian approach a narrow doorway from opposite directions, single-file passage | Yes |
| Physical Env | Indoor | `context.environment.type: indoor` | Yes |
| Geometric Layout | Room and door | `geometric_layout: room and door` | Yes |
| Scientific Purpose | Pedestrian interaction | `scientific_purpose: pedestrian interaction` | Yes |
| Robot Task | Navigate A to B | `intended_robot_task: navigate from A to B through the doorway` | Yes |
| Human Behavior | Navigate B to A | `intended_human_behavior: navigate from B to A through the doorway` | Yes |
| Ideal Outcome | No collision / obstruction | `ideal_outcome: robot and human sequence through the doorway one at a time without collision or obstruction` | Yes |
| Related Scenarios | Narrow Arch | `related_scenarios: [blind_corner, entering_room, exiting_room]` — see note below | Yes, informally |
| Cited In | [126] | `cited_in: ["126"]` | Yes |

**Source fidelity: checked against P&G Table 3 — full match, no mismatches found.**
All physical description, purpose, layout, roles, task, and ideal-outcome fields are
consistent with the canonical Table 3 entry. Table 3 names "Narrow Arch" as the
related scenario, but no `narrow_arch` scenario card exists yet in
`prosoc/scenarios/` (confirmed: no matching directory), so `related_scenarios`
correctly points instead to the implemented, related-by-geometry scenarios
(`blind_corner`, `entering_room`, `exiting_room`) rather than a not-yet-existing
directory — consistent with `template.md`'s note that this field should reference
"the directory/key used in audit.md and AUDIT_SUMMARY.md." This is not a fidelity
mismatch.

## Completeness

Walking `template.md`'s "Required for AUDITED scenarios" fields:

**Scenario Card Summary:**
- Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric
  Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome — all present,
  consistent between prose and YAML.
- Success Metrics / Quality Metrics — present (SR, NoCollisions / P3, P4), consistent
  across Card Summary, YAML, and the Scenario Usage Guide prose section.
- **Related Scenarios** — now present (`blind_corner, entering_room, exiting_room`)
  in both the Card Summary bullet and the YAML `related_scenarios` key. Resolves the
  prior audit's Finding 1 (was should-fill-in-now).
- **Cited In** — now present (`126`) in both the Card Summary bullet and the YAML
  `cited_in` key. Resolves the prior audit's Finding 1.

**Scenario Usage Guide:**
- Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria —
  all present and consistent between the prose section and `scenario_usage_guide` in
  the YAML. No gaps.

This card remains in good shape: schema-valid (dry-run distiller check produced no
diff), principle count within guidance (4, within 3–5), no invented-principle issues,
and full Table 3 fidelity including the now-transcribed Related Scenarios/Cited In
fields. The only remaining item is the single low-severity phrasing suggestion above,
which is not a blocker to AUDITED promotion.
