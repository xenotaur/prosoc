---
execution_id: 2026_07_30_15_38_44_NORMATIVE_CARD_APPROVAL
prompt_id: PROMPT(AD_HOC:NORMATIVE_CARD_APPROVAL)[2026-07-30T13:30:35-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/61
commit: 68a49b89f393c67292cb9d3cf5ce92668bea28af
created_at: 2026-07-30T15:38:44-04:00
agent: claude_app
instruction_source: project/design/proposals/proposed/normative-card-approval/00_proposal.md
session_transcript: claude-app:1d38659c-be69-49bc-80ce-5b0f7bf4f368
---

# Summary

Scoped and drafted `PROP-NORMATIVE-CARD-APPROVAL`, a design proposal for how
a human reviewer promotes prosoc normative cards from `AUDITED` to
`APPROVED`, satisfying `WS-NORMATIVE-PACKET-ASSEMBLY`'s second exit
criterion. Ran via `/lrh-proposal` against user-supplied grounding facts
(independently re-verified against the live corpus: 32 cards, all `DRAFTED`
except 2 `EDITED` constitutions, uneven `audit.md` coverage), followed by an
interactive brainstorm that replaced the original single `prosoc-card-approve`
skill design with a three-skill stack plus a deterministic corpus
review-queue engine.

# Result

Wrote `project/design/proposals/proposed/normative-card-approval/00_proposal.md`
with five Design Decisions: (1) pilot the 5 `sample_packet` cards before any
full-corpus promotion; (2) a `prosoc-card-approve` / `prosoc-card-review` /
`prosoc-card-review-all` skill stack, single approver (repo owner), evidence
gated on `audit.md` verdict; (3) a deterministic `scripts/validate/review-queue`
engine reusing `prosoc/utils/cards/validate_status.py`'s `FAMILIES` registry
and `prosoc/packet/gate.py`'s `PRODUCTION_ORDER` to rank cards by
severity/scope, with audit-less cards sorting as highest priority (subsuming
the 4-card coverage gap into the ranked worklist rather than a separate
decision); (4) an ephemeral worklist (JSON + table), no committed dashboard,
with an optional end-of-session Markdown snapshot; (5) governance unchanged
from the parent proposal — `--allow-unapproved` stays permanent, state
staleness deferred as an Open Question. Prior art check found no existing
promotion/ranking tooling and no duplicate work item or proposal. Opened
[PR #61](https://github.com/xenotaur/prosoc/pull/61) from
`xenotaur/feat/normative-card-approval`.

# Validation

- `lrh validate` — 0 errors, 0 warnings.
- Independently re-verified the user's grounding facts against the live
  corpus (state census across all 6 families via `grep`, `audit.md` census)
  before drafting, rather than trusting them as given.
- Confirmed the 5 pilot cards (charter, `asimov_three_laws`,
  `intersection_gesture_wait`, `navigate_lead_agent`, `high_urgency`) all
  already have `audit.md`, so the pilot needs no new audits.
- Confirmed via `lrh prompt check-execution` and a slug-based
  `project/executions/AD_HOC/` search that no prior record exists for this
  slug (not a rerun).

# Follow-up

- Two work items offered, not yet created: WI 1 (build the review-queue
  engine + three-skill stack) and WI 2 (run the pilot on the 5
  `sample_packet` cards) against `WS-NORMATIVE-PACKET-ASSEMBLY`.
- Open Questions left in the proposal: whether WI 1+2 alone satisfy the WS
  exit criterion or full-corpus promotion is required; state-staleness/
  auto-regression detection; whether `project/focus/current_focus.md` and
  the WS prose need updating; packet-centrality weighting in the ranking
  engine.
- Next steps: `/lrh-review-response` for reviewer comments,
  `/lrh-confirm-fixes` before merge, `/lrh-closeout` after merge to land
  this record as `landed`.
