---
execution_id: 2026_07_19_22_39_29_SCENARIO_SECTION_RENDERER_CORPUS_PASS
prompt_id: PROMPT(AD_HOC:SCENARIO_SECTION_RENDERER_CORPUS_PASS)[2026-07-19T22:38:34-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/22
commit: 
agent: claude_app
instruction_source: ad_hoc conversation — follow-up to WI-SCENARIO-SECTION-RENDERER (PR #21): user asked to execute "batch-render the 3 ready scenarios" and "bring movable_obstruction (and similarly-structured scenarios) into template.md conformance" from the post-closeout next-steps summary
session_transcript: pending
created_at: 2026-07-19T22:39:29-04:00
---

# Summary

Follow-up to WI-SCENARIO-SECTION-RENDERER (`render_sections.py`, PR #21):
(1) bring the 5 scenarios that predate `template.md`'s current section-
heading and Status-block conventions into conformance, since that
structure is a prerequisite for the renderer's insertion anchors and its
`EDITED:`-stamp mechanism, and (2) actually invoke `render_sections.py`
for real (not `--dry-run`) against all scenarios with conformant
structure, rather than leaving it only exercised in dry-run mode as in
PR #21.

# Result

- Discovered during investigation, not anticipated in the original WI:
  `frontal_approach`, `movable_obstruction`, `pedestrian_overtaking`,
  `robot_overtaking`, `single_file_hallway` used an older `## STATUS:
  <STATE> <date>` heading with plain (non-bold) `- SOURCE:`/`- DRAFTED:`/
  `- EDITED:` bullets — matching `workflow.md`'s own "Status Section
  Template" example verbatim, but not what `render_sections.py`'s
  `_stamp_edited` (built against the newer bold-bullet convention used by
  `join_a_group`/`leading`/`object_handover`/`intersection_gesture_proceed`,
  and by `template.md` itself) recognizes. Raised this as a scope decision
  for the user via `AskUserQuestion` rather than silently picking a
  resolution; user chose to normalize to `template.md`'s bold convention
  (treating `template.md` as canonical over `workflow.md`'s stale example)
  and to render into all structurally-fixable scenarios, not just fix
  headings.
- Normalized all 5 scenarios' Status blocks to `## Status` +
  `- **STATE:**`/`- **SOURCE:**`/`- **DRAFTED:**`/`- **EDITED:**`, and
  renamed `## Overview` → `## Scenario Overview`; added
  `## Scenario Specification (Machine-Readable)` where no heading wrapped
  the YAML fence (`frontal_approach`, `movable_obstruction`,
  `single_file_hallway` — `pedestrian_overtaking`/`robot_overtaking`
  already had that heading). Applied via a small Python script for
  mechanical precision across all 5 files identically; did not touch
  `## Discussion` headings (present in 3 of the 5) — left as-is, relying on
  `render_sections.py`'s existing fallback-append behavior for the
  optional Usage Guide anchor.
- Verified no YAML content changed: `distill.py --dry-run --show-diffs`
  produces zero diff for all 5, both before and after the structural edit.
- Ran `render_sections.py` for real (dropping `--dry-run`, after first
  reviewing each with `--dry-run --show-diffs`) against all 8
  structurally-eligible scenarios: `join_a_group`, `leading`,
  `object_handover` (zero schema-backed gaps — only the two permanent
  `Related Scenarios`/`Cited In` gaps), and `frontal_approach`,
  `movable_obstruction`, `pedestrian_overtaking`, `robot_overtaking`,
  `single_file_hallway` (correct, non-fabricated gaps checklists — spot
  checked `movable_obstruction`'s output against its own prior `audit.md`
  Completeness section and it matches exactly).
- Confirmed `distill.py --dry-run --show-diffs` still shows zero diff
  after rendering, for all 8 — rendering only adds prose outside the
  YAML fence.

# Validation

- `scripts/lint` — all checks passed
- `scripts/test` — 80 tests OK (unchanged from PR #21; no new test code in
  this follow-up, only scenario-corpus content changes)
- `lrh validate` — 1 pre-existing error (`focus/current_focus.md` not
  found), unrelated; 0 errors attributable to this change
- `python3 -m prosoc.scenarios.distill --scenario <name> --dry-run --show-diffs`
  for all 5 restructured scenarios — zero diff, confirming the structural
  edit did not alter compiled YAML
- `python3 -m prosoc.scenarios.render_sections <name> --dry-run --show-diffs`
  for all 8 target scenarios, reviewed before running for real
- Re-ran the distill zero-diff check post-render for all 8

# Follow-up

- The underlying missing-YAML-field gaps surfaced by this render pass
  (`scientific_purpose`, `ideal_outcome`, etc., across `frontal_approach`,
  `movable_obstruction`, `pedestrian_overtaking`, `robot_overtaking`,
  `single_file_hallway`) remain unaddressed — separate, scenario-by-
  scenario editorial work, consistent with WI-SCENARIO-SECTION-RENDERER's
  original Non-Goals.
- `workflow.md`'s "Status Section Template" section still documents the
  older plain-bullet convention this PR moved away from; it was not
  updated in this change (out of scope — a docs-accuracy fix, not a
  scenario-corpus fix) but now describes a pattern no longer used
  anywhere in the corpus.
- `session_transcript: pending` should be updated to
  `claude-app:<session-id>` before or when this PR lands.
