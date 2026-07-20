# Post-render follow-up: what's left for a human, per scenario

**Not an audit.** This is a synthesis of (a) which findings in each
scenario's existing `audit.md` were resolved by
[PR #21](https://github.com/xenotaur/prosoc/pull/21) /
[PR #22](https://github.com/xenotaur/prosoc/pull/22), and (b) the
"Remaining gaps" bullets `render_sections.py` already wrote into each
`scenario.md`, gathered in one place to speed up the manual editing pass.
It does not re-verify prose/YAML consistency, schema/charter compliance, or
source fidelity — those are unchanged from each scenario's last real audit
(2026-07-05) and are not re-checked here. **After filling gaps, re-run
`/prosoc-scenario-audit-all` scoped to these 8 scenarios for the
authoritative, up-to-date `audit.md` per scenario and a refreshed
`AUDIT_SUMMARY.md`.**

Scope: the 8 scenarios touched by PR #21/#22 —
`join_a_group`, `leading`, `object_handover`, `frontal_approach`,
`movable_obstruction`, `pedestrian_overtaking`, `robot_overtaking`,
`single_file_hallway`. The other 12 scenarios in the corpus are unaffected
and not covered here.

---

## join_a_group

- **Resolved:** Finding 1 (Card Summary missing, blocking), Finding 2
  (Usage Guide missing, blocking) — both sections now rendered.
- **No other findings** in the original audit.
- **Needs a researcher's judgment:** `Related Scenarios`, `Cited In` — no
  schema field exists for either; these can only ever be filled by hand
  (see `Notes for Scenario Designers and Evaluators`, which already names
  *Leave Group* and *Accompany Peer* as related — consider promoting that
  into a formal Related Scenarios entry).

## leading

- **Resolved:** Finding 1 (Card Summary missing, blocking), Finding 2
  (Usage Guide missing, blocking).
- **Still open:** Finding 3 (suggestion) — `initial_conditions` duplicates
  `intended_robot_task`; a minor YAML tidy-up, not a research judgment call.
- **Needs a researcher's judgment:** `Related Scenarios`, `Cited In`.

## object_handover

- **Resolved:** Finding 1 (Card Summary missing, should-fix), Finding 2
  (Usage Guide missing, should-fix).
- **Still open:** Finding 3 (should-fix) — `STATE` is still `DRAFTED`
  while `EDITED` is now populated (`render_sections.py` stamped it per
  `workflow.md`'s convention, but never promotes lifecycle `STATE` — that
  stays a human decision). This is a good candidate to reconsider now.
  Finding 4 (suggestion) — Normative Expectations prose doesn't mirror the
  `must`/`should`/`should_not` split.
- **Needs a researcher's judgment:** `Related Scenarios`, `Cited In`.

## frontal_approach

- **Resolved:** Finding 3 (should-fix) — structural non-conformance
  (missing sections) fixed.
- **Still open:** Finding 1 (blocking) — `ideal_outcome` missing entirely.
  Finding 2 (should-fix) — `scientific_purpose` and `geometric_layout`
  omitted. Finding 4 (suggestion) — the failure mode "robot fails to pass
  within time limit" references an undefined time limit; reword or define
  it. Finding 5 (suggestion) — typos in `evaluation_notes` ("typiocal",
  "attettentive too it").
- **Needs a researcher's judgment:** `Scientific Purpose`, `Geometric
  Layout`, `Robot Task`, `Human Behavior`, `Ideal Outcome`, `Related
  Scenarios`, `Cited In`.
- **Not yet added** (optional per `template.md`, not required for
  AUDITED, out of scope for `render_sections.py`): `## Social Navigation
  Context`, `## Normative Expectations` prose sections — the card still
  only has `## Scenario Overview` and `## Discussion`.

## movable_obstruction

- **Resolved:** Finding 3 (blocking) — structural non-conformance fixed.
- **Still open:** Finding 2 (blocking) — `relevant_principles` has 7
  entries (P1, P2, P3, P5, P6, P7, P9), above the 3–5 guidance; audit
  suggests narrowing to P1/P7/P5 as most load-bearing, reconsidering
  P2/P3/P6/P9. Finding 4 (should-fix) — Overview/Discussion prose names
  `NAVIGATE_POINT_TO_POINT`/`DELIVER_OBJECT`/etc. task/context IDs not tied
  to any structured YAML field. Finding 5 (suggestion, no action needed —
  expected distiller reflow behavior).
- **Needs a researcher's judgment:** `Scientific Purpose`, `Geometric
  Layout`, `Robot Task`, `Human Behavior`, `Ideal Outcome`, `Related
  Scenarios`, `Cited In`.
- **Not yet added:** `## Social Navigation Context`, `## Normative
  Expectations` — same gap as `frontal_approach`.

## pedestrian_overtaking

- **Resolved:** Finding 2 (blocking) — sections missing; Finding 3
  (should-fix) — outdated STATUS block format (now normalized); Finding 4
  (suggestion) — title heading missing a space (fixed in the PR #22
  review round, along with aligning the H1 to the canonical name).
- **Still open:** Finding 5 (suggestion) — `relevant_principles` lists 6
  (P0, P1–P4, P9), one above the 3–5 guidance.
- **Needs a researcher's judgment:** `Scientific Purpose`, `Geometric
  Layout`, `Robot Task`, `Human Behavior`, `Success Metrics`, `Quality
  Metrics`, `Ideal Outcome`, `Failure Modes`, `Labeling Criteria`,
  `Related Scenarios`, `Cited In` — no `scenario_usage_guide:` key exists
  at all in this scenario's YAML (same as `robot_overtaking`, below); the
  largest gap of the 8.

## robot_overtaking

- **Resolved:** Finding 2 (blocking) — Card Summary section missing;
  Finding 4 (should-fix) — `name` field didn't match the scenario.md
  title (fixed in the PR #22 review round).
- **Still open / partially resolved:** Finding 3 (blocking) — "Missing
  `scenario_usage_guide` YAML block and prose section." The **prose**
  section now exists (rendered), but the **YAML block itself is still
  absent** from `scenario.yml`/`scenario.md` — confirmed no
  `scenario_usage_guide:` key exists in the embedded YAML. This is the one
  scenario in this batch where the underlying data gap is largest: Success
  Metrics, Quality Metrics, Failure Modes, and Labeling Criteria all need
  authoring from scratch, not just transcription. Finding 5 (suggestion) —
  over-specification risk in `expected_behaviors.should_not`.
- **Needs a researcher's judgment:** `Scientific Purpose`, `Geometric
  Layout`, `Robot Task`, `Human Behavior`, `Success Metrics`, `Quality
  Metrics`, `Ideal Outcome`, `Failure Modes`, `Labeling Criteria`,
  `Related Scenarios`, `Cited In`.

## single_file_hallway

- **Resolved:** Finding 2 (blocking) — Card Summary missing; Finding 3
  (blocking) — Usage Guide prose missing.
- **Still open:** Finding 1 (blocking) — duplicated
  `expected_behaviors.should_not` entries; needs a content fix, not a
  structural one. Finding 4 (should-fix) — no `ideal_outcome` field.
  Finding 6 (suggestion) — minor over-specification phrasing.
- **Needs a researcher's judgment:** `Scientific Purpose`, `Geometric
  Layout`, `Robot Task`, `Human Behavior`, `Ideal Outcome`, `Related
  Scenarios`, `Cited In`.
- **Not yet added:** `## Social Navigation Context`, `## Normative
  Expectations` — same gap as `frontal_approach`/`movable_obstruction`.

---

## Cross-scenario patterns worth a single decision rather than 8 separate ones

- **`Related Scenarios` / `Cited In`** are blank in all 8 — there is no
  schema field for either (confirmed during `render_sections.py`'s
  design), so they will *always* show as gaps no matter how complete the
  YAML gets. Worth deciding once whether these become real schema fields
  or stay prose-only, rather than re-deciding per scenario.
- **`Scientific Purpose` / `Geometric Layout` / `Robot Task` / `Human
  Behavior` / `Ideal Outcome`** are missing in the same pattern across
  `frontal_approach`, `movable_obstruction`, `pedestrian_overtaking`,
  `robot_overtaking`, `single_file_hallway` — these 5 scenarios were
  evidently drafted before those fields were adopted project-wide (they're
  present in every scenario in the "ready" bucket of the original
  [AUDIT_SUMMARY.md](../../prosoc/scenarios/AUDIT_SUMMARY.md) table).
- **`robot_overtaking` and `pedestrian_overtaking`** are the two scenarios
  where `scenario_usage_guide` is missing or empty outright, not just
  incompletely populated — likely the highest-effort fills in this batch.
