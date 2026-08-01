---
execution_id: 2026_07_31_20_58_37_WI_CARD_APPROVAL_PILOT
prompt_id: PROMPT(WI-CARD-APPROVAL-PILOT:WI_CARD_APPROVAL_PILOT)[2026-07-31T20:45:15+00:00]
work_item: WI-CARD-APPROVAL-PILOT
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/65
commit: 0049f6c2297655516bbb75e3963a2dacad2f09c9
created_at: 2026-07-31T20:58:37+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-APPROVAL-PILOT.md
session_transcript: claude-app:1d38659c-be69-49bc-80ce-5b0f7bf4f368
---

# Summary

Implemented `WI-CARD-APPROVAL-PILOT`: promoted the 5 `sample_packet` cards
(charter, `asimov_three_laws`, `intersection_gesture_wait`,
`navigate_lead_agent`, `high_urgency`) from their pre-existing states
through `AUDITED` to `APPROVED` using the mechanics `WI-CARD-APPROVE-SKILLS`
built, then regenerated `sample_packet`'s golden packet in production
mode -- the corpus's first-ever `gate_threshold: APPROVED` packet.

# Result

Before promoting, re-verified all 5 cards' `audit.md` verdicts hadn't
drifted since the WI was written (all still `ready`/`ready_with_fixes`,
zero blocking) and independently read each audit's findings rather than
trusting the verdict line alone -- all 6 (2 charter, 2 navigate_lead_agent,
2 high_urgency) should-fix findings are prose/documentation completeness
gaps or already-acknowledged known corpus issues (dangling
`example_scenarios` refs), none affecting the machine-readable content the
packet actually ships. Presented this assessment plus the full technical
plan to the user as one batch confirm gate rather than 10 separate prompts,
consistent with `prosoc-card-review-all`'s batching design.

Performed 10 mechanical promotions (5 cards x AUDITED then APPROVED):
edited each card's fenced-YAML `state:` field, re-ran that family's
distiller, ran `scripts/validate/status --fix`, re-verified consistency.
Confirmed via `git diff` that every card's change is exactly the state
line in both representations (Markdown STATE bullet + fenced YAML) and
both files (source `.md` + distilled `.yml`) -- no normative content
touched, satisfying `forbidden_actions: edit_card_normative_content`.

Verified via `prosoc/packet/assemble.py`'s actual logic (not assumed) that
the escape hatch only stamps when a member is genuinely below the
production floor -- confirmed the golden packet needed full regeneration,
not just a diff refresh, since `predicate.policy.allow_unapproved`/
`gate_threshold` differ between dev- and prod-mode regardless of hatch
engagement. Regenerated `packet.golden.yml` via
`scripts/assemble ... > packet.golden.yml` (no `--allow-unapproved`);
self-verified with `--check`.

Updated `.github/workflows/packet.yml` and `prosoc/packet/README.md` to
drop the now-unneeded escape hatch for `sample_packet` specifically
(README still documents the dev-mode path for not-yet-approved manifests).
Discovered and fixed two additional breakages from promoting real corpus
cards, beyond the WI's stated `tests/packet/cli_test.py` scope: several
`cli_test.py` tests implicitly depended on `sample_packet`'s members being
unapproved (asserting the default gate blocks it, or that
`--allow-unapproved` engages the hatch) -- rewrote them using a new
synthetic-manifest fixture (a real, permanently-`DRAFTED` card outside the
pilot) to preserve that coverage generically; and `tests/packet/loader_test.py`
(not in the WI's artifact list at all) hardcoded `asimov_three_laws`'s
state as `"EDITED"` as an incidental fixture value -- updated to
`"APPROVED"`.

# Validation

- Every card's `git diff` manually inspected: exactly the `state:` line
  changed, both representations, both files.
- `scripts/validate/status` per card and full-corpus -- all `ok`, 32/32
  consistent.
- `scripts/assemble prosoc/manifests/sample_packet/manifest.yml` -- exit 0,
  `gate_threshold: APPROVED`, `allow_unapproved: false`, `escape_hatch: null`.
- `scripts/assemble ... --check` -- exit 0, golden matches.
- `python -m unittest tests.packet.cli_test` -- 12 tests, OK (10 original,
  2 new).
- `scripts/test` -- full suite, 239 tests, OK (caught and fixed the
  `loader_test.py` regression here).
- `scripts/lint` -- all checks passed.
- `black --check` on touched files -- clean.
- `lrh validate` -- 0 errors, 0 warnings.

# Follow-up

- This is the last work item on `WS-NORMATIVE-PACKET-ASSEMBLY`'s current
  `work_items:` list -- once this PR lands, all 11 are resolved and the
  workstream's second exit criterion is arguably satisfied for the pilot
  scope (full-corpus promotion of the remaining 27 cards is still
  deferred/offered work, not committed).
- Full-corpus promotion candidates, in priority order per
  `scripts/validate/review-queue`: the 4 audit-coverage-gap cards
  (`asimov_four_laws`, `guidance_docent`, `public_navigation`,
  `routine_delivery`) sort first (no `audit.md` at all), then the
  remaining 23 already-audited cards by severity/scope.
