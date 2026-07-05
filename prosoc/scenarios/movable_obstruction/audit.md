# Audit: Movable Obstruction

- **Scenario:** `prosoc/scenarios/movable_obstruction/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready — 3 blocking issues

## Findings

### 1. `relevant_principles` and `quality_metrics` invent a non-canonical principle ID (P9) — blocking
- **Section/field:** `relevant_principles`; `scenario_usage_guide.quality_metrics`
- **Issue:** Both lists include `P9` ("Prosocial Behavior"), which is not one of the eight canonical principles defined in `../_shared/principles.md` (P1–P8). The schema's `^P[0-9]+$` pattern permits it syntactically, but `_shared/principles.md` is explicit: "Only emit P1–P8... If a scenario involves a principle not well-captured by P1–P8, note it in `evaluation_notes` rather than inventing a new ID." The scenario's own prose (Overview, Discussion) leans heavily on this invented P9 concept and also references an undefined "P0 (Goal Achievement)" in the Discussion section.
- **Recommended fix:** Remove `P9` from both `relevant_principles` and `quality_metrics`. If the "environmental stewardship beyond immediate interaction" concept is important to preserve, move it into `evaluation_notes` as prose rather than a principle ID, and remove the "P0 (Goal Achievement)" reference in the Discussion section for the same reason (P0 is not a defined principle anywhere in the corpus).

### 2. `relevant_principles` count (7, after excluding P9) exceeds the 3–5 guidance — blocking
- **Section/field:** `relevant_principles`
- **Issue:** The list currently has 7 entries (P1, P2, P3, P5, P6, P7, P9). Even discounting the invalid P9, that leaves 6 (P1, P2, P3, P5, P6, P7) — still above the "3–5 most directly relevant" guidance in `../_shared/principles.md`, which warns that including too many "dilutes meaning."
- **Recommended fix:** Narrow to the 3–5 principles most central to the scenario's core conflict (obstruction handling/intervention vs. yielding). P1 (Safety), P7 (Proactivity), and P5 (Social Competency) look most load-bearing given the prose; P2, P3, and P6 are plausible but should be reconsidered for necessity.

### 3. `scenario.md` does not follow `template.md`'s structure — no Scenario Card Summary, Social Navigation Context, Normative Expectations, or Scenario Usage Guide sections — blocking
- **Section/field:** Whole-document structure vs. `template.md`
- **Issue:** The card consists only of a `## STATUS` block, an `## Overview` section, the embedded YAML, and a `## Discussion` section. It is missing the `## Scenario Card Summary` block (required for AUDITED scenarios — Scenario Name, Description, Scientific Purpose, Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome, etc.), the `## Social Navigation Context` section, a dedicated `## Normative Expectations` section, and the `## Scenario Usage Guide` section (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria as prose). Some of this content exists only inside the YAML block or is absent entirely — see Completeness below.
- **Recommended fix:** Restructure `scenario.md` to follow `template.md`'s section headings, adding the missing prose sections (Scenario Card Summary, Social Navigation Context, Normative Expectations, Scenario Usage Guide) before this scenario can be considered for AUDITED status.

### 4. Prose refers to concepts absent from the YAML schema (P9, P0, task names) — should-fix
- **Section/field:** Overview / Discussion vs. `scenario.yml`
- **Issue:** The Overview and Discussion sections reference "Prosocial Behavior (P9)" and "Goal Achievement (P0)" as if these were established principles in this project, and name specific tasks/contexts (`NAVIGATE_POINT_TO_POINT`, `DELIVER_OBJECT`, `ROUTINE_DELIVERY`, `GUIDANCE_DOCENT`, `HIGH_URGENCY`) that appear to reference `prosoc/tasks/` and `prosoc/contexts/` IDs but are not connected to this scenario's YAML in any structured field (no `initial_conditions` or other field ties the scenario to a specific task/context pairing).
- **Recommended fix:** Once P9/P0 are resolved (Finding 1), align the prose's principle references with the corrected `relevant_principles` list. If the task/context cross-references are intentional, consider whether they belong in `evaluation_notes` or a "Related Scenarios"/cross-reference field rather than embedded narrative prose only.

### 5. `scenario.yml`'s top-level `evaluation_notes` matches `scenario.md`'s content but was reflowed by the distiller — suggestion
- **Section/field:** `evaluation_notes`
- **Issue:** Not a defect — this is expected distiller re-serialization behavior (folded scalar → double-quoted string with escaped unicode em dash). Noted here only for completeness since the dry-run check produced no diff, confirming `scenario.yml` is in sync with the embedded YAML in `scenario.md`.
- **Recommended fix:** None needed.

## Source Fidelity

The SOURCE field cites "Principles and Guidelines for Evaluating Social Robot Navigation (P&G paper)" generically, without a specific table or section reference. Per `../_shared/pg_scenarios.md`: **"The `movable_obstruction` scenario has no direct P&G Table 3 counterpart."** This is stated explicitly in the shared reference data, meaning there is no Table 3 entry to compare physical description, scientific purpose, geometric layout, roles, task, or ideal outcome against.

**Source fidelity: not checkable against Table 3 — the shared reference data explicitly states this scenario has no direct P&G Table 3 counterpart, and the SOURCE field does not cite a specific section, page, or figure of the paper that could be checked directly.** The SOURCE field should be more precise (e.g., citing the general P7/proactivity guideline discussion, or marking this as an original extension of *Frontal Approach* rather than a direct paper citation) so that future audits know what, if anything, is checkable.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

**Scenario Card Summary (entirely absent as a prose section):**
- **Scenario Name** — should-fill-in-now (trivially available: "Movable Obstruction")
- **Scenario Description** — should-fill-in-now (derivable from the YAML `summary` field, which is already populated)
- **Scientific Purpose** — should-fill-in-now; the YAML has no `scientific_purpose` field at all (unlike `narrow_doorway`, which populates it as `pedestrian interaction`), though the Overview prose implies something like "proactivity vs. prosocial/environmental-stewardship distinction." This should be captured explicitly once Finding 1 is resolved.
- **Physical Environment** — should-fill-in-now (readily available from `context.environment.type: indoor`)
- **Geometric Layout** — should-fill-in-now; no `geometric_layout` field exists in the YAML (schema supports it, `narrow_doorway` uses it as `room and door`). Here it would be something like "hallway."
- **Robot Role** — should-fill-in-now (available as `agents.robot.role: navigating_agent`)
- **Robot Task** — should-fill-in-now; no `intended_robot_task` field exists in the YAML at all. This is a required-for-schema-completeness gap even though the schema doesn't mandate it structurally — `template.md` lists "Robot Task" as required for AUDITED, and the field exists in schema.json but is unused here.
- **Human Behavior** — should-fill-in-now; likewise, no `intended_human_behavior` field is populated.
- **Success Metrics / Quality Metrics** — present in YAML (`scenario_usage_guide.success_metrics`, `quality_metrics`) but not surfaced as prose in a Scenario Card Summary or Scenario Usage Guide section.
- **Ideal Outcome** — should-fill-in-now; no top-level `ideal_outcome` field exists in the YAML, even though `evaluation_notes` and the Discussion prose gesture at what a good outcome looks like. This is a notable gap since `ideal_outcome` is schema-supported and used by `narrow_doorway`.
- **Related Scenarios** — reasonably blank, though the Discussion section already names *Frontal Approach* as the extended baseline; this could be promoted to a formal "Related Scenarios" entry.
- **Cited In** — reasonably blank (no evidence of other papers/datasets citing this scenario).

**Scenario Usage Guide (as a prose section — currently only exists inside the YAML block, not as human-readable prose):**
- **Success Metrics** — should-fill-in-now as prose (YAML values exist: SR, NoCollisions, ConflictResolved)
- **Quality Metrics** — should-fill-in-now as prose, pending the P9 fix (Finding 1)
- **Ideal Outcome** — should-fill-in-now; blocked on adding the `ideal_outcome` YAML field first
- **Failure Modes** — should-fill-in-now as prose (YAML values exist and are reasonably detailed)
- **Labeling Criteria** — should-fill-in-now as prose (YAML values exist)

Overall, this scenario is more DRAFTED than EDITED in its current state — its STATUS block itself says "STATE: DRAFT" with EDITED listed as "(pending)" — and has substantial structural and content gaps relative to `template.md` before it should be considered for AUDITED promotion.
