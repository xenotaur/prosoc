---
execution_id: 2026_11_06_23_47_01_WI_CHARTER_SUPPLEMENT_LIFECYCLE_STALE_DEMOTION
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION:WI_CHARTER_SUPPLEMENT_LIFECYCLE_STALE_DEMOTION)[2026-11-06T23:34:03+00:00]
work_item: WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/134
commit: 24e5aadf9d5255fbcd1ca1529a696f603da7d2ef
created_at: 2026-11-06T23:47:01+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implements `WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION`: demotes 9
normative cards from `APPROVED` to `EDITED` since each carries a real
content edit postdating its last `audit.md`.

# Result

For each of the 9 cards (charter, frontal_approach, single_file_hallway,
movable_obstruction, navigate_point_to_point, deliver_object,
navigate_follow_agent, navigate_lead_agent, high_urgency): flipped the
embedded fenced-YAML `state:` field, added a dated `**EDITED:**` history
bullet documenting the demotion (preserving all existing bullets
verbatim), regenerated distilled YAML via the family's distiller
(confirmed single-field diffs only), and projected the corrected `STATE`
line via `scripts/validate/status --fix` -- run only after distillation,
per the WI's own explicit ordering requirement (`--fix` reads the
*distilled* YAML, not the fenced Markdown YAML). For the charter
specifically, hand-synced its separate free-text `**Status:**` header to
`Edited (Normative)` (confirmed via `check_charter_status_line`'s actual
regex in `status.py` that this text satisfies the check), since `--fix`
never touches that header.

`high_urgency`'s `contexts` family has no pre-existing `**EDITED:**`
bullet convention (confirmed via corpus-wide grep: contexts use a bare
`MODIFIED:` field, no history list) -- a diff-mode self-review subagent
caught this card's demotion as initially undocumented (state flipped,
but no bullet added). Fixed before push by adding the same bullet
convention the other 8 cards use, in the positionally-analogous slot
after `MODIFIED:` -- a harmless first for this family, not a schema
change (the bullet is free-text STATUS-block prose, outside the
distilled YAML schema).

Did not regenerate `packet.golden.yml`: `charter`, `navigate_lead_agent`,
and `high_urgency` are all members of
`src/prosoc/manifests/sample_packet/manifest.yml`, and `scripts/assemble`
now fails closed on that manifest -- there is no successful assembly to
generate a new golden from. Confirmed exactly 6 (not the WI's originally
estimated 2) `tests/nca/packet/cli_test.py` tests fail as a result, all
explained by this one root cause; corrected the WI's own text (and a
cross-reference in `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`) to the
verified count and exact test names as a drive-by documentation fix.

# Validation

- `scripts/validate/status` -- `All 32 card(s) consistent.`
- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
  -- 344 tests, `FAILED (failures=6, skipped=1)` -- exactly:
  `CliTest.test_sample_packet_default_now_succeeds_since_pilot_approved`,
  `CliTest.test_allow_unapproved_on_fully_approved_manifest_does_not_engage_hatch`,
  `CliTest.test_check_matches_the_checked_in_golden`,
  `CliCheckTest.test_matching_golden_exits_zero_silently`,
  `CliCheckTest.test_drifted_golden_exits_one_with_diff`,
  `CliCheckTest.test_missing_golden_exits_one_with_clear_error` --
  confirmed twice, once by the self-review subagent and once directly by
  this session after the `high_urgency` fix.
- `scripts/assemble src/prosoc/manifests/sample_packet/manifest.yml --check`
  -- fails closed, naming the 3 demoted members by family/id, not a
  crash or byte-diff.
- `scripts/lint` -- all checks passed.
- `scripts/format --check --diff` -- 22 pre-existing files flagged,
  confirmed unrelated (`git diff origin/main --stat` shows no Python
  file in this change).
- Diff-mode `/lrh-self-review` dispatched before this PR's first push
  (see the companion `_SELFREVIEW` record): one real finding (the
  `high_urgency` missing bullet), independently re-verified by this
  session directly against the diff and fixed before push; everything
  else (charter header-regex correctness, the 3 excluded contexts
  untouched, no `packet.golden.yml` touched, exact test-failure list, 0
  `scripts/validate/status` errors) confirmed clean.

# Follow-up

None blocking. `WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH` is next in
the workstream's dependency order; the 6 packet-related test failures
and CI's packet-drift check stay red until
`WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION` restores the 3 overlapping
members to `APPROVED` -- land that work item promptly.
