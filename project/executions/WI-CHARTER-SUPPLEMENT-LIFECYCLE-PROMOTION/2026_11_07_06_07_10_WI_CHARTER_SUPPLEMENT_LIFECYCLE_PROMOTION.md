---
execution_id: 2026_11_07_06_07_10_WI_CHARTER_SUPPLEMENT_LIFECYCLE_PROMOTION
prompt_id: PROMPT(WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION:WI_CHARTER_SUPPLEMENT_LIFECYCLE_PROMOTION)[2026-11-07T04:58:54+00:00]
work_item: WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/136
commit:
created_at: 2026-11-07T06:07:10+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION.md
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Implements `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`: promotes the 9
cards `WI-CHARTER-SUPPLEMENT-LIFECYCLE-AUDIT-REFRESH` refreshed back
through `EDITED -> AUDITED -> APPROVED`, 18 individually-gated
transitions, then regenerates the charter-supplement PDF.

# Result

- **Charter content fix before its first promotion:** the Normative
  Statement for P1, P2, P4, P5, P6 had drifted from the YAML
  `description` field. P1/P2/P5/P6 backported verbatim; P4 additionally
  hedged ("offering help or at least an acknowledgement when asked")
  since an unconditional help obligation conflicted with the charter's
  own P8 crash-cart subordination example -- discussed and confirmed
  with the human before applying.
- **9 cards x 2 transitions = 18 live human-confirmation gates**, none
  batched. `EDITED -> AUDITED`: all 9 audits were current and 0-blocking;
  one (`frontal_approach`) was held at first ask over a SOURCE/fidelity
  tension, fixed (reworded SOURCE to cite the matching P&G Table 3 entry
  explicitly), re-audited clean, then approved. `AUDITED -> APPROVED`:
  3 cards (`single_file_hallway`, `movable_obstruction`,
  `navigate_point_to_point`) had their should-fix findings fixed rather
  than accepted as-is per explicit human direction; 2 cards
  (`navigate_lead_agent`, `high_urgency`) had should-fix findings that
  had sat open in `project/design/backlog.md`'s "APPROVED cards with
  unresolved findings" table since 2026-08-02 -- fixed and removed from
  that table, mirroring the charter's own 2026-08-06 cleanup precedent;
  2 cards (`deliver_object`, `navigate_follow_agent`) had should-fix
  findings already tracked as known, non-blocking forward references in
  that same backlog file and needed no action beyond confirming the
  tracking was current.
- **Found and fixed a pre-existing history-bullet ordering bug** in 5
  cards (`navigate_point_to_point`, `deliver_object`,
  `navigate_follow_agent`, `navigate_lead_agent`, `high_urgency`): each
  card's original first-audit bullet sat after later `EDITED` bullets
  instead of before them chronologically. Caught by this WI's own
  acceptance criterion #6 (PDF-text history-ordering check) during
  validation, not by review -- fixed by moving each card's original
  `AUDITED` bullet to immediately follow its `DRAFTED`/`CREATED` bullet.
- Each promotion added its own dated `AUDITED:`/`APPROVED:` history
  bullet by hand (`prosoc-card-approve` never writes one); the charter's
  separate free-text `Status:` header was hand-synced at both of its
  promotions.
- Regenerated `papers/01_charter/golden/rendered.tex` and
  `src/prosoc/manifests/sample_packet/packet.golden.yml` via their
  supported pipelines only -- never hand-edited.
- Backfilled "(PR #TBD)" in all 9 `APPROVED:` bullets to "(PR #136)" once
  the PR number was known, as a disclosed follow-up commit.

# Validation

- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- `scripts/lint` -- all checks passed.
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
  -- 344 tests, 0 failures, 1 pre-existing skip. The 6 packet-related
  failures `WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION` introduced as
  a disclosed, temporary consequence are gone now that `charter`,
  `navigate_lead_agent`, and `high_urgency` are `APPROVED` again.
- `PYTHONPATH="$(pwd)/src" python -m prosoc.nca.utils.cards.validate_status`
  -- 32/32 cards consistent.
- `scripts/assemble src/prosoc/manifests/sample_packet/manifest.yml --check`
  -- passes, no golden drift, after regenerating the golden file (member
  content genuinely changed this round, unlike the prior work item).
- `PYTHONPATH="$(pwd)/src" papers/01_charter/render.py --pdf` -- 48-page
  PDF rebuilt clean via the full render pipeline.
- Visual spot-check of rendered PDF pages (charter P1/P4 principle
  sections, multiple cards' STATUS blocks, final page) -- no clipping,
  malformed characters, or pagination regressions.
- `pdftotext -layout` extraction of the full PDF -- confirmed correct
  STATE/EDITED/AUDITED/APPROVED date ordering for all 9 cards, including
  `navigate_follow_agent` and `navigate_lead_agent` (not in
  `papers/01_charter/sources.txt`), checked directly against their
  `task.md` files per the work item's own instruction.
- Throughout: every `scripts/*` wrapper and `python -m prosoc...`
  invocation used an explicit `PYTHONPATH="$(pwd)/src"` after discovering
  this machine's global `prosoc` editable install resolves to an
  unrelated, stale checkout (`CharterReconciliation`) otherwise -- caught
  mid-session via an implausible `validate_status` result, not assumed.

# Follow-up

None blocking. Once this PR merges, resolve `WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`
and execute the workstream's final item,
`WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD` (new validator code to catch
future APPROVED-but-stale drift automatically), then close
`WS-CHARTER-SUPPLEMENT-LIFECYCLE-CURRENCY`.
