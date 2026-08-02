---
family: scenarios
card: robot_overtaking
verdict: ready
blocking: 0
should_fix: 0
suggestion: 3
audited: 2026-08-02
---

# Audit: Robot Overtaking

- **Card:** `prosoc/scenarios/robot_overtaking/`
- **Audited:** Claude (prosoc-card-audit skill), 2026-08-02 (fresh audit —
  prior audit dated 2026-07-22 was stale relative to the card's last
  touch on 2026-07-25 — the corpus-wide `WI-CARD-STATUS-FOUNDATION`
  mechanical migration, not a content edit — and is superseded by this
  pass; Findings 1–2 carry forward unchanged, Finding 3 is new)
- **Verdict:** Ready — no blocking or should-fix issues found; three
  low-severity suggestions

## Findings

### 1. Physical Environment specialization vs. P&G Table 3 "Generic" — suggestion
- **Section/field:** Scenario Card Summary "Physical Environment" / YAML
  `context.environment.type` vs. P&G Table 3's Robot Overtaking entry
- **Issue:** The card specifies `indoor` / "corridor or sidewalk-like
  passage," while P&G Table 3 categorizes Robot Overtaking's Physical Env
  as "Generic" (Geometric Layout: "Passable space," which the card does
  match). This is a reasonable specialization, not a contradiction, but
  the card doesn't note that it's a deliberate narrowing of the paper's
  more general categorization.
- **Recommended fix:** Optionally add a brief note (in `evaluation_notes`
  or the Social Navigation Context section) that "indoor" is a deliberate
  specialization of the paper's "generic" passable-space categorization.

### 2. `related_scenarios` could include additional corpus matches named in prose — suggestion
- **Section/field:** `related_scenarios` (YAML) / "Related Scenarios"
  (Card Summary) vs. "Notes for Scenario Designers and Evaluators"
- **Issue:** `related_scenarios` lists only `pedestrian_overtaking`, but
  the Notes section says this scenario "pairs naturally with frontal
  approach scenarios, group overtaking variants, narrow-passage
  constraints, and distracted pedestrian variants." Two of these
  correspond to scenarios that already exist in the corpus —
  `frontal_approach` and `single_file_hallway` — but neither is added to
  `related_scenarios`.
- **Recommended fix:** Consider adding `frontal_approach` and
  `single_file_hallway` to `related_scenarios` if the pairing is intended
  as a formal cross-reference; leave as-is if the Notes mention is meant
  only as a loose, non-binding aside.

### 3. "Normative Expectations" prose doesn't clearly bullet either `must`-level behavior — suggestion
- **Section/field:** Normative Expectations (prose) vs. `expected_behaviors.must`
- **Issue:** `expected_behaviors.must` has two entries ("avoid colliding
  with or startling the pedestrian," "maintain a safe and respectful
  distance during approach and passing"). The prose "Acceptable robot
  behavior" list covers the `should` entries reasonably well, and one
  phrase ("passing smoothly with adequate clearance") loosely paraphrases
  the distance-related `must` item, but neither `must` item gets its own
  explicit bullet — collision/startle avoidance is only implicit via the
  Overview's general framing. Same pattern independently found this
  session on `intersection_no_gesture`, `entering_room`, and
  `intersection_gesture_proceed` — logged as a recurring item in
  `project/design/backlog.md` for a dedicated future pass.
- **Recommended fix:** Optionally add explicit collision/startle-avoidance
  and safe-distance bullets under Normative Expectations for symmetry with
  the `must` list — not required for `AUDITED`.

## Source Fidelity

SOURCE is cited informally as "Prompt to ChatGPT 5.2" with no retrievable
content, but the Social Navigation Context section explicitly ties this
scenario to the P&G paper, and it clearly corresponds to the **Robot
Overtaking** entry in P&G Table 3 (per
`.claude/skills/_shared/pg_scenarios.md`):

| Field | P&G Table 3 | This card | Match |
|---|---|---|---|
| Description | Robot overtakes a moving pedestrian | Robot approaches a human from behind, decides to follow or overtake safely/legibly/comfortably | Match (elaborated) |
| Physical Env | Generic | Indoor (corridor/sidewalk-like) | Deliberate specialization, not a contradiction (Finding 1) |
| Geometric Layout | Passable space | passable space | Exact match |
| Scientific Purpose | Pedestrian interaction | pedestrian interaction | Exact match |
| Robot Task | Navigate A to B | navigate from A to B | Match |
| Human Behavior | Navigate A to B (slower) | navigate from A to B, slower than the robot | Exact match |
| Ideal Outcome | Robot passes human | robot passes the human safely, comfortably, and without disruption | Match (elaborated) |
| Related Scenarios | (none listed) | pedestrian_overtaking | Expected addition — Table 3 silence isn't a claim of no relationship |
| Cited In | [50, 157] | 50, 157 | Exact match |

Overall: strong fidelity to the P&G Table 3 entry, with one minor,
non-contradictory specialization (physical environment) noted above.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" fields, all are
present:

- **Scenario Card Summary:** Complete — Scenario Name, Description,
  Scientific Purpose, Physical Environment, Geometric Layout, Robot Role,
  Robot Task, Human Behavior, Success Metrics, Quality Metrics, Ideal
  Outcome, Related Scenarios, and Cited In are all populated and
  consistent with the YAML.
- **Scenario Usage Guide** — Success Metrics (SR, NoCollisions), Quality
  Metrics (P2, P3, P4), Ideal Outcome, Failure Modes (3 entries), Labeling
  Criteria (3 entries) — all complete and consistent between prose and
  YAML.

No required fields are blank. `related_scenarios` is populated but could
arguably be expanded (Finding 2, a suggestion rather than a completeness
gap, since a single related scenario is a valid non-empty answer).
