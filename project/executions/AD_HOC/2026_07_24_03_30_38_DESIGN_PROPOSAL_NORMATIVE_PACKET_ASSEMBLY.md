---
execution_id: 2026_07_24_03_30_38_DESIGN_PROPOSAL_NORMATIVE_PACKET_ASSEMBLY
prompt_id: PROMPT(AD_HOC:DESIGN_PROPOSAL_NORMATIVE_PACKET_ASSEMBLY)[2026-07-24T03:30:23-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/36
commit: 6706e829c91b195bf51ffa84cf9edc7f18dab678
created_at: 2026-07-24T03:30:38-04:00
agent: claude_app
instruction_source: ad hoc — second half of a split delivery from a design session on the normative packet assembler; authored via /lrh-proposal, which mints no execution record, so this primary record is created retroactively at closeout
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Primary record for PR #36, which added the design proposal
`PROP-NORMATIVE-PACKET-ASSEMBLY` at
`project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`.
The proposal captures the settled design for assembling normative cards
(charter principles, constitutions, tasks, contexts, scenarios) into a single
machine-readable guidance packet for a downstream agent: a human-authored,
auditable manifest names the member cards, and a deterministic engine
resolves, lifecycle-gates, and composes them into a signing-ready provenance
envelope (Option 4 with Option 2 as its engine).

This record is created retroactively at closeout — `/lrh-proposal` produces
the proposal artifact and PR but no execution record, so PR #36 had only the
`_REVIEW` and `_CONFIRM` side records until now. It is the second half of a
split delivery; the first half (the `project/design/proposals/` scaffolding
this proposal lives in) landed as PR #35
(`2026_07_24_00_01_15_PROJECT_DESIGN_PROPOSALS_SCAFFOLD`).

# Result

Landed a `status: proposed` / `implementation_status: not_started` proposal
recording seven design decisions, the load-bearing ones being: insert a
distinct `APPROVED` lifecycle state after `AUDITED` so agent auditing and
human approval stop colliding (Decision 1); author `status` in the card YAML
and project it into the Markdown STATUS block rather than cross-validating two
copies (Decision 2); a manifest-plus-engine composition strategy, because the
scenario→task/context edges a graph traversal would need do not exist
(Decision 3); one generic `CardLoader` instead of eight per-family modules
(Decision 4); and a namespaced, in-toto/DSSE-shaped provenance envelope that
records the escape hatch inside the payload (Decision 5).

The proposal remains `proposed`, not `adopted`: merging the PR lands the
document, but adopting the design (making it govern) is a separate human
decision, naturally triggered by a governing workstream plus implementation —
the next phase discussed in the design session.

# Validation

- `lrh validate`: 0 errors, 0 warnings.
- Two Copilot review threads addressed (`/lrh-review-response`) and verified
  against the live diff then resolved (`/lrh-confirm-fixes`); see the linked
  `_REVIEW` and `_CONFIRM` side records.

# Follow-up

- Adoption of `PROP-NORMATIVE-PACKET-ASSEMBLY` and the phased implementation
  (Phase 0a lifecycle/status work onward) are future work, best owned by a
  governing workstream.
- The proposal's open question on the corpus stage-5 term (`VALIDATED` in
  `scenarios/workflow.md` vs `VERIFIED` in `constitutions/template.md` and the
  paper) must be resolved as part of Phase 0a.
