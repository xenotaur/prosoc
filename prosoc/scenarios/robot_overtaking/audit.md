# Audit: Robot Overtaking

- **Scenario:** `prosoc/scenarios/robot_overtaking/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready — 2 blocking issues (corrected 2026-07-05 — see Correction Notice)

## Correction Notice (2026-07-05)

This audit originally flagged `P0` in `relevant_principles` as an invalid,
non-canonical principle ID (Finding 1 below). That was incorrect:
`prosoc/charter/charter.md` (the sole source of truth) defines **ten** principles,
P0–P9 — P0 (Goal Achievement) is this project's own explicit, intentional
extension beyond the P&G paper's eight, not an invented ID. `charter.yml` (the
generated artifact) confirms this (distiller dry-run reports no diff). The error
originated in a stale `.claude/skills/_shared/principles.md`, which claimed only
P1–P8 were valid and has since been corrected. Finding 1 is retracted; the
`relevant_principles` list totals 5 (P0, P1–P4) once P0 is correctly counted,
which is within the 3–5 guidance, so no replacement finding is needed.

### 1. ~~Invalid principle identifier `P0` in `relevant_principles`~~ — RETRACTED
- **Status:** Retracted 2026-07-05. See Correction Notice above — P0 is a valid
  canonical principle per `prosoc/charter/charter.md`, not an invented ID.

### 2. Missing "Scenario Card Summary" section — blocking
- **Section/field:** Scenario Card Summary (per `template.md`, "Required for AUDITED
  scenarios")
- **Issue:** `scenario.md` has no Scenario Card Summary section at all — it goes directly
  from the STATUS block to Overview. Fields such as Scenario Name, Scientific Purpose,
  Physical Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Success
  Metrics, Quality Metrics, Ideal Outcome, Related Scenarios, and Cited In are entirely
  absent from the prose, even though several are inferable from the YAML and prose
  elsewhere in the card.
- **Recommended fix:** Add a Scenario Card Summary section per `template.md`, populated
  from the existing YAML/prose content (e.g. Scientific Purpose: pedestrian interaction;
  Physical Environment: indoor; Robot Task: navigate A to B / overtake pedestrian; Human
  Behavior: navigate same direction, slower; Ideal Outcome: robot passes human safely and
  comfortably) and from the P&G Table 3 "Robot Overtaking" entry (see Source Fidelity
  below).

### 3. Missing `scenario_usage_guide` YAML block and prose section — blocking
- **Section/field:** `scenario_usage_guide` (YAML) / "Scenario Usage Guide" prose section
  (template.md, "Required for AUDITED scenarios")
- **Issue:** Neither the embedded YAML nor `scenario.yml` contains a
  `scenario_usage_guide` object (success_metrics, quality_metrics, failure_modes,
  labeling_criteria all absent), and `scenario.md` has no corresponding "Scenario Usage
  Guide" prose section. `evaluation_notes` gestures at failure modes in prose
  ("tailgating, sudden lateral movements, or passing in a way that causes surprise or
  discomfort") but this content has not been structured into `failure_modes` or the
  other required subfields.
- **Recommended fix:** Add a `scenario_usage_guide` block with `success_metrics` (e.g.
  SR, NoCollisions, PSC), `quality_metrics` (a subset of `relevant_principles`, e.g. P1, P2, P3), and convert
  the failure-mode language already in `evaluation_notes` into explicit
  `failure_modes` and `labeling_criteria` entries, plus the matching "Scenario Usage
  Guide" prose section in `scenario.md`.

### 4. `name` field does not match the scenario.md title heading — should-fix
- **Section/field:** `id`/`name` (schema.json required fields) vs. `scenario.md` title
- **Issue:** The document title is `# Scenario: Robot Overtaking`, but the YAML `name`
  field is `Overtaking a Pedestrian from Behind`. The audit checklist requires `name` to
  match the scenario's title heading in `scenario.md`; here they diverge (though both are
  reasonable descriptions of the same scenario).
- **Recommended fix:** Either rename the YAML `name` to match the title heading ("Robot
  Overtaking") or update the title heading to match the YAML name, so the two are
  consistent.

### 5. Over-specification risk in `expected_behaviors.should_not` — suggestion
- **Section/field:** `expected_behaviors.should_not` (P&G Guideline N6)
- **Issue:** Entries are phrased at the level of a *kind* of behavior ("follow too
  closely", "pass abruptly or at excessive speed") rather than exact numeric thresholds,
  which is correct. This is a minor suggestion rather than a real violation: "pass
  abruptly or at excessive speed" borders on conflating two distinct behaviors (abrupt
  lateral motion vs. excessive speed) in one bullet.
- **Recommended fix:** Consider splitting into two bullets for clarity ("pass abruptly /
  with sudden lateral motion" and "accelerate excessively when passing"), though this is
  optional polish, not a compliance issue.

## Source Fidelity

SOURCE is cited informally as "Prompt to ChatGPT 5.2" with no retrievable content, but
the Social Navigation Context section explicitly says this scenario "is inspired by
pedestrian overtaking cases discussed in the *Principles and Guidelines for Social Robot
Navigation* paper," and the scenario clearly corresponds to the **Robot Overtaking**
entry in P&G Table 3 (per `../../../.claude/skills/_shared/pg_scenarios.md`):

- **P&G Table 3 "Robot Overtaking":** Description: "Robot overtakes a moving pedestrian";
  Physical Env: Generic; Geometric Layout: Passable space; Scientific Purpose: Pedestrian
  interaction; Robot Task: Navigate A to B; Human Behavior: Navigate A to B (slower);
  Ideal Outcome: Robot passes human.

Comparing against the card:
- **Robot/human roles and relative speed:** Match — robot is faster (`relative_speed:
  robot_faster`), human is the slower pedestrian being overtaken. Consistent with "Human
  Behavior: Navigate A to B (slower)."
- **Task:** Consistent — robot navigates forward and must decide whether to overtake,
  matching "Navigate A to B."
- **Ideal outcome:** Consistent in spirit — the card's evaluation_notes describe
  "successful overtaking characterized by early intent signaling, sufficient lateral
  clearance, and minimal disruption," aligned with Table 3's "Robot passes human," though
  the card leaves open the possibility the robot chooses not to overtake (a reasonable,
  compatible elaboration, not a contradiction).
- **Physical environment mismatch:** Table 3 lists Physical Env as "Generic" and
  Geometric Layout as "Passable space" (i.e., not indoor-specific), while the card's YAML
  sets `context.environment.type: indoor` and `setting: corridor or sidewalk-like
  passage`. This is a **drift**, not a contradiction — the scenario is a reasonable indoor
  specialization of a "generic" paper scenario, but the mismatch is worth flagging since
  the card doesn't note this is a deliberate narrowing.

Overall: no outright contradictions found; one drift (physical environment specialization
vs. paper's "generic" categorization) worth a should-fix note, captured above as informing
Finding 2's Scenario Card Summary (Physical Environment field should either say "Generic"
per the paper or explicitly note the indoor specialization as a deliberate choice).

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

- **Scenario Card Summary** (Scenario Name, Description, Scientific Purpose, Physical
  Environment, Geometric Layout, Robot Role, Robot Task, Human Behavior, Ideal Outcome,
  Success/Quality Metrics, Related Scenarios, Cited In): **should probably be filled in
  now** — the section is entirely missing, but all core fields are readily inferable from
  the existing Overview/Social Navigation Context prose and the YAML block (see Finding 2).
  Related Scenarios and Cited In could reasonably stay blank/minimal for now, but note the
  card's own "Notes for Scenario Designers and Evaluators" section already names related
  scenarios in prose ("pairs naturally with frontal approach scenarios, group overtaking
  variants, narrow-passage constraints, and distracted pedestrian variants") — this is
  should-fill-in-now material for the "Related Scenarios" field.
- **Scenario Usage Guide — Success Metrics:** should probably be filled in now — nothing
  currently in YAML or prose; P&G-style metrics (SR, NoCollisions, PSC) are a natural fit
  given the scenario's safety/comfort focus.
- **Scenario Usage Guide — Quality Metrics:** should probably be filled in now — the
  `relevant_principles` list (P0, P1–P4) already identifies applicable candidates;
  reuse a subset directly.
- **Scenario Usage Guide — Ideal Outcome:** reasonably present in spirit (see
  `ideal_outcome`-equivalent language in `evaluation_notes`), but there is no explicit
  top-level `ideal_outcome` field in the YAML at all (the schema defines one) — should
  probably be filled in now, e.g. "Robot passes the pedestrian with adequate clearance,
  minimal speed differential, and no perceived pressure or startle."
- **Scenario Usage Guide — Failure Modes:** should probably be filled in now — already
  implied in `evaluation_notes` prose ("tailgating, sudden lateral movements, passing in
  a way that causes surprise or discomfort") but not extracted into a structured
  `failure_modes` list.
- **Scenario Usage Guide — Labeling Criteria:** should probably be filled in now — no
  criteria currently given for recognizing this scenario in data (e.g. "robot and human
  moving same direction," "robot approaching from behind at higher speed," "passable
  width available").
