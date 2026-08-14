---
family: scenarios
card: intersection_gesture_proceed
verdict: ready
blocking: 0
should_fix: 0
suggestion: 3
audited: 2026-08-02
---

# Audit: Intersection – Gesture Proceed

- **Card:** `prosoc/scenarios/intersection_gesture_proceed/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — and is superseded by this
  pass; Findings 1–2 carry forward unchanged, Finding 3 is new)
- **Verdict:** Ready — no contradictions, no schema issues; three
  low-severity suggestions

## Findings

### 1. `expected_behaviors.should` edges toward a measurable-latency criterion — suggestion
- **Section/field:** `expected_behaviors.should` — "commit promptly to
  motion after the gesture"
- **Issue:** This remains qualitative ("promptly," not a numeric
  threshold), so it does not clearly violate P&G Guideline N6
  over-specification as written. But timing/promptness is a recurring
  theme across the Overview, Normative Expectations, and failure modes
  ("hesitates excessively after permission is given"), and no qualitative
  anchor is given for what counts as acceptable, which could invite
  inconsistent labeling across evaluators.
- **Recommended fix:** No change strictly required; optionally clarify in
  `evaluation_notes` what a "prompt" response window looks like
  qualitatively without introducing a hard numeric threshold.

### 2. Related Scenarios lists one more entry than the P&G source — suggestion
- **Section/field:** Scenario Card Summary / YAML `related_scenarios` vs.
  P&G Table 3
- **Issue:** P&G Table 3 lists only "Gesture Wait" as the related scenario
  for Intersection Gesture Proceed. This card additionally lists
  `intersection_no_gesture`. Both referenced IDs exist in the corpus and
  both reciprocally list `intersection_gesture_proceed` back, so this
  isn't a broken reference — just a reasonable, intentional broadening
  beyond what the source paper states.
- **Recommended fix:** No change required; noted for the human editor's
  awareness that this is an addition beyond the source, not an error.

### 3. "Normative Expectations" prose omits one `must`-level behavior — suggestion
- **Section/field:** Normative Expectations (prose) vs. `expected_behaviors.must`
- **Issue:** The prose's "Acceptable robot behavior" list covers "recognize
  the human's gesture" (must #1) and loosely covers "commit promptly"/
  "smooth trajectory" (the `should` entries), but never explicitly states
  "enter and traverse the intersection safely" or "avoid collision with
  the human" (must #2–3) as their own bullets — though safety/collision
  avoidance is implicit throughout (Overview, Ideal Outcome). Same pattern
  independently found this session on `intersection_no_gesture` and
  `entering_room`.
- **Recommended fix:** Optionally add explicit safety/collision-avoidance
  bullets under Normative Expectations for symmetry with the `must` list
  — not required for `AUDITED`.

## Prose/YAML Consistency and Schema Check

- `scripts/distill/scenarios --scenario intersection_gesture_proceed
  --dry-run --show-diffs` produced no diff and no schema errors —
  `scenario.yml` is in sync with the embedded YAML block in `scenario.md`.
- No contradictions found between prose (Overview, Social Navigation
  Context, Normative Expectations) and YAML (`agents`,
  `expected_behaviors`, `ideal_outcome`,
  `intended_robot_task`/`intended_human_behavior`).
- `relevant_principles` (P0, P1, P2, P3, P4) validate against P0–P9; count
  of 5 is within the 3–5 guideline, and P0's inclusion is well-founded by
  the Overview's explicit "balancing goal achievement with safety and
  comfort" language.
- `expected_behaviors` entries describe kinds of behavior ("commit
  promptly to motion after the gesture," "maintain a smooth and legible
  trajectory") rather than exact motions or numeric thresholds — no
  over-specification (P&G Guideline N6) flagged.
- `related_scenarios` (`intersection_gesture_wait`, `intersection_no_gesture`)
  — both directories exist under `prosoc/scenarios/` and reciprocally
  reference `intersection_gesture_proceed`; the broadening beyond P&G
  Table 3's single "Gesture Wait" citation is expected per the checklist's
  convention and self-documented in the card's own `evaluation_notes`.

## Source Fidelity

SOURCE is explicitly stated as "Principles and Guidelines for Social
Robot Navigation (Table 3)," checked directly against
`.claude/skills/_shared/pg_scenarios.md`'s "Intersection Gesture Proceed"
entry:

| Field | P&G Table 3 | This card | Match? |
|---|---|---|---|
| Description | Robot told to proceed at intersection | Human explicitly gestures for robot to proceed; robot recognizes and crosses | Consistent — same interaction, elaborated |
| Physical Env | Indoor | Indoor | Match |
| Geometric Layout | Intersection | intersection | Match |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Match |
| Robot Role | Servant | servant | Match |
| Robot Task | Navigate A to B | navigate from A to B | Match |
| Human Behavior | Cross navigate (gesture proceed) | cross navigate (gesture proceed) | Exact match |
| Ideal Outcome | Robot goes first | human gestures the robot to proceed; robot goes first and both cross without collision | Match (elaborated) |
| Related Scenarios | Gesture Wait | intersection_gesture_wait, intersection_no_gesture | Consistent, appropriately broader (Finding 2) |
| Cited In | [126] | "126" | Match |

**Overall:** Full fidelity to the P&G source — no mismatches found.

## Completeness

Walked against `template.md`'s "Required for AUDITED scenarios" sections:

- **Scenario Card Summary** — all fields present and mirrored in
  `scenario.yml`: `id`, `name`, `summary`, `scientific_purpose`,
  `geometric_layout`, `agents.robot.role`, `intended_robot_task`,
  `intended_human_behavior`, `ideal_outcome`, `related_scenarios`,
  `cited_in` all populated in both prose and YAML.
- **Scenario Usage Guide** — Success Metrics, Quality Metrics, Ideal
  Outcome, Failure Modes, Labeling Criteria all present and consistent
  between prose and the embedded `scenario_usage_guide` YAML block.

No fields were found to be reasonably blank in this card.
