---
scenario: crowd_navigation
verdict: ready
blocking: 0
should_fix: 0
suggestion: 1
audited: 2026-07-21
---

# Audit: Crowd Navigation

- **Scenario:** `prosoc/scenarios/crowd_navigation/`
- **Audited:** Claude (prosoc-scenario-audit skill), 2026-07-21
- **Verdict:** Ready — no blocking or should-fix issues found; one minor suggestion

## Findings

### 1. STATUS block's EDITED date does not reflect the latest edit — suggestion
- **Section/field:** Status block (`EDITED: render_sections.py, 2026-07-20`)
- **Issue:** `git log` shows the most recent edit to `scenario.md`/`scenario.yml` is commit `93d55c3` ("Resolve the two deferred follow-ups from PR #27"), which backfilled `related_scenarios`/`cited_in`. The STATUS block still shows the prior `render_sections.py, 2026-07-20` entry and does not record this most recent pass.
- **Recommended fix:** Add an additional `EDITED` line (or update the existing one) noting the `related_scenarios`/`cited_in` backfill and its date/author, consistent with how the STATUS block tracks provenance elsewhere in the corpus.

## Source Fidelity

SOURCE cites P&G Paper Table 3, "cited in various." Compared against `.claude/skills/_shared/pg_scenarios.md`'s "Crowd Navigation" entry (Crowd Scenarios section):

- Description ("A robot navigates through a crowd") — matches.
- Physical Environment: Generic — matches (`context.environment.type: generic`).
- Geometric Layout: Passable space — matches (`geometric_layout: passable space`).
- Scientific Purpose: Crowd navigation — matches (`scientific_purpose: crowd navigation`).
- Robot Task: Navigate thru — matches (`intended_robot_task: navigate through the crowd to a destination on the far side`).
- Human Behavior: Mill about — matches (`intended_human_behavior: mill about, moving independently...`).
- Ideal Outcome: No collision/obstruction — matches, with an added "steady progress" clause that is an elaboration rather than a contradiction.
- Cited In: Various — matches (`cited_in: [various]`).
- Related Scenarios: the reference table lists "Robot Crowding," but Robot Crowding is a Figure 7 scenario with no implemented directory in this repo (confirmed: no `robot_crowding` directory exists under `prosoc/scenarios/`). The card's own `related_scenarios` field instead links to `parallel_traffic` and `perpendicular_traffic`, both implemented sibling crowd scenarios discussed in the "Notes for Scenario Designers and Evaluators" section, consistent with `template.md`'s definition of `related_scenarios` as pointing to actual corpus directories. This is not a mismatch — it's the correct choice given the field's constraint to real directories, and the prose still names Robot Crowding as a conceptual relative.

No mismatches found. Source fidelity: confirmed against P&G Table 3.

## Completeness

Per `template.md`'s "Required for AUDITED scenarios" checklist:

- **Scenario Card Summary block** — fully present, including `Related Scenarios: parallel_traffic, perpendicular_traffic` and `Cited In: various`, resolving the should-fix from the prior audit (2026-07-20).
- **Scenario Usage Guide (Success Metrics, Quality Metrics, Ideal Outcome, Failure Modes, Labeling Criteria)** — present as prose, mirroring the YAML `scenario_usage_guide` block.
- **`relevant_principles`** (P1, P2, P6, P7) — 4 entries, within the 3-5 guidance, all valid P0-P9.
- **`expected_behaviors`** — qualitative kind-of-behavior descriptions throughout; no numeric-threshold or exact-motion over-specification found.
- Single-scenario dry-run distill (`scripts/distill/scenarios --scenario crowd_navigation --dry-run --show-diffs`) reported no diff and no schema errors — `scenario.yml` is in sync with `scenario.md`.

No blank fields remain from the prior audit's completeness pass.

## Change vs. prior audit (2026-07-20)

The prior audit (`verdict: ready_with_fixes`, `should_fix: 1`, `suggestion: 0`) flagged one should-fix: `Related Scenarios`/`Cited In` left blank in the Scenario Card Summary. Since then, both `scenario.md` and `scenario.yml` were backfilled with `related_scenarios: [parallel_traffic, perpendicular_traffic]` and `cited_in: [various]` (commit `93d55c3`), fully resolving that finding. No new should-fix or blocking issues were found in this pass. One new suggestion-level observation was added: the STATUS block's `EDITED` provenance line has not been updated to record this backfill pass.
