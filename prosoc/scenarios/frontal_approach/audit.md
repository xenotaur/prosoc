# Audit: Frontal Approach

- **Scenario:** `prosoc/scenarios/frontal_approach/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-05
- **Verdict:** Not ready for AUDITED — 1 blocking issue, several should-fix completeness gaps

## Findings

### 1. `ideal_outcome` field missing entirely — blocking
- **Section/field:** `scenario.yml` top-level `ideal_outcome` / Scenario Card Summary "Ideal Outcome"
- **Issue:** The schema supports a top-level `ideal_outcome` field, and both `template.md`'s Scenario Card Summary and the P&G Table 3 entry for Frontal Approach ("Robot/humans pass") expect a concise ideal-outcome statement. Neither `scenario.md` nor `scenario.yml` contains this field at all — it is not merely blank in a labeled section, it is absent from the machine-readable spec entirely. Without it, there is no anchor to check the prose's implicit "good ending" against (per the audit checklist's prose/YAML cross-check row), and the card cannot be considered complete for AUDITED.
- **Recommended fix:** Add a top-level `ideal_outcome:` field to `scenario.yml` (and reflect it in `scenario.md`'s YAML block), e.g. summarizing "robot and human pass each other without collision, without prolonged hesitation, and without discomfort" — consistent with the `summary` field's own language.

### 2. `scientific_purpose` and `geometric_layout` fields omitted — should-fix
- **Section/field:** `scenario.yml` top-level `scientific_purpose`, `geometric_layout` (schema-optional but Card-Summary-required fields)
- **Issue:** P&G Table 3 lists Scientific Purpose as "Pedestrian interaction" and Geometric Layout as "Passable space" for Frontal Approach. Neither field appears in `scenario.yml`. These are readily inferable from the existing prose (the Overview explicitly frames this as testing "pedestrian interaction" via listed principles) and from `context.environment.setting: office hallway` / `width: narrow`.
- **Recommended fix:** Add `scientific_purpose: Pedestrian interaction` and a `geometric_layout` value (e.g. "corridor" or "passable space", consistent with the paper's category) to `scenario.yml`.

### 3. No separate Scenario Card Summary, Social Navigation Context, Normative Expectations, or Scenario Usage Guide sections in prose — should-fix
- **Section/field:** `scenario.md` structure vs. `template.md`
- **Issue:** `scenario.md` uses a condensed "Overview" + embedded YAML + "Discussion" structure. It has no distinct Scenario Card Summary block, no Social Navigation Context or Normative Expectations prose sections, and no Scenario Usage Guide section (Success Metrics / Quality Metrics / Ideal Outcome / Failure Modes / Labeling Criteria as prose). `template.md` marks the Card Summary and Scenario Usage Guide as "Required for AUDITED scenarios." This appears to be a corpus-wide drafting convention (all other scenarios checked are similarly DRAFT-stage and condensed), so it's flagged here as a should-fix specific to promotion readiness rather than a defect unique to this card.
- **Recommended fix:** Before promoting to AUDITED, expand `scenario.md` to include the sections `template.md` requires, at least as short prose restating what's already in the YAML (success_metrics, quality_metrics, failure_modes, labeling_criteria are already present in YAML and could be lifted directly into prose form).

### 4. "robot fails to pass within time limit" implies an unspecified time limit — suggestion
- **Section/field:** `expected_behaviors` / `scenario_usage_guide.failure_modes`
- **Issue:** The failure mode "robot fails to pass within time limit" references a time limit that is not defined anywhere in `initial_conditions` or elsewhere in the card. This is a minor internal-consistency gap (not over-specification, since no numeric threshold is actually given — but the concept it references is dangling).
- **Recommended fix:** Either add a qualitative note on what "reasonable time" means for this scenario, or reword to something like "robot fails to make progress toward passing" to avoid implying an undefined external parameter.

### 5. Minor prose typos — suggestion
- **Section/field:** `evaluation_notes`
- **Issue:** "typiocal" (should be "typical") and "attettentive too it" (should be "attentive to it") in the `evaluation_notes` field, present in both `scenario.md` and `scenario.yml`.
- **Recommended fix:** Correct the typos when the card is next edited.

## Source Fidelity

SOURCE is not stated as citing P&G directly in the scenario's own STATUS block (`SOURCE: Prompt to ChatGPT 5.2`), but the scenario's name and content clearly correspond to the P&G Table 3 "Frontal Approach" entry, so it is checked against `../../../.claude/skills/_shared/pg_scenarios.md`:

| Field | P&G Table 3 | This scenario | Match? |
|---|---|---|---|
| Description | Pedestrian and robot approach head-on in a passable space | Robot and human approach each other in opposite directions in a narrow hallway | Consistent (hallway is a valid instance of "passable space") |
| Physical Env | Generic | Indoor office hallway | Consistent specialization, not a contradiction |
| Geometric Layout | Passable space | Narrow hallway (field itself absent from YAML — see Finding 2) | Consistent in prose; missing as a discrete field |
| Scientific Purpose | Pedestrian interaction | Not present as a field, but Overview names "pedestrian interaction"-adjacent principles | Consistent in spirit; missing as a discrete field |
| Robot Task | Navigate A to B | `intended_robot_task` field is absent from YAML entirely; Overview implies A-to-B hallway traversal | Not directly checkable — field missing (see note below) |
| Human Behavior | Navigate B to A | `intended_human_behavior` field is absent from YAML entirely; Overview implies the human approaches from the opposite end | Not directly checkable — field missing |
| Ideal Outcome | Robot/humans pass | Absent (Finding 1) | Not checkable — field missing |
| Related Scenarios | Ped. Obstruct | Not present (optional field) | Reasonably blank |

Note: `intended_robot_task` and `intended_human_behavior` are schema-supported fields (per `template.md`'s YAML skeleton) that are also absent from this scenario's `scenario.yml`, though the audit checklist step 1 dry-run reported no schema violation (these fields are not in schema.json's `required` list and schema.json does not define them as top-level properties at all — only `intended_robot_task`/`intended_human_behavior` are referenced by template.md, not by schema.json itself). Their absence is therefore not a schema error, but it does widen the source-fidelity gap above, since Robot Task and Human Behavior are two of the eight Table 3 comparison fields.

**Overall:** No contradictions with the P&G source were found; the scenario is a faithful elaboration of the "Frontal Approach" entry. Several comparison fields are simply not present in the machine-readable card, which limits how fully fidelity could be checked (see Findings 1–2).

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields:

**Scenario Card Summary** (no distinct section exists in `scenario.md`; assessed against equivalent YAML fields):
- Scenario Name: present (`name: Frontal Approach`) — complete
- Scenario Description: present (`summary`) — complete
- Scientific Purpose: **blank** — should probably be filled in now (inferable from Overview's principle list and P&G source)
- Physical Environment: present (`context.environment.type: indoor`) — complete
- Geometric Layout: **blank** as a discrete field — should probably be filled in now (inferable: "narrow hallway" / "passable space")
- Robot Role: present (`agents.robot.role: navigating_agent`) — complete
- Robot Task: **blank** (`intended_robot_task` absent) — should probably be filled in now (inferable from Overview: navigate the hallway to the opposite end)
- Human Behavior: **blank** (`intended_human_behavior` absent) — should probably be filled in now (inferable: navigate hallway toward the robot, opposite direction)
- Success Metrics: present (`scenario_usage_guide.success_metrics`) — complete
- Quality Metrics: present (`scenario_usage_guide.quality_metrics`) — complete
- Ideal Outcome: **blank** — should probably be filled in now (see Finding 1; blocking, not merely a completeness nit)
- Related Scenarios: blank — reasonably blank (P&G lists "Ped. Obstruct" as related; not yet cross-referenced, but cross-scenario linking is a corpus-level concern out of this audit's scope)
- Cited In: blank — reasonably blank (optional bibliographic metadata; can be added later without blocking review)

**Scenario Usage Guide:**
- Success Metrics: present in YAML (SR, NoCollisions) — complete, though no separate prose subsection exists (Finding 3)
- Quality Metrics: present in YAML (P2, P3, P5) — complete, same caveat
- Ideal Outcome: **blank** — should probably be filled in now (Finding 1)
- Failure Modes: present in YAML (2 entries) — complete, same caveat; one entry has the dangling "time limit" reference (Finding 4)
- Labeling Criteria: present in YAML (3 entries) — complete, same caveat
