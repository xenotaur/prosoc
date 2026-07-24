---
execution_id: 2026_07_24_00_01_15_PROJECT_DESIGN_PROPOSALS_SCAFFOLD
prompt_id: PROMPT(AD_HOC:PROJECT_DESIGN_PROPOSALS_SCAFFOLD)[2026-07-24T00:00:31-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/35
commit: 0577f1f8e28732735ebba3fe23760b4912c46917
created_at: 2026-07-24T00:01:15-04:00
agent: claude_app
instruction_source: ad hoc — first half of a split delivery from a design session on the normative packet assembler; the scaffolding was separated from the design proposal (PR #36) so the new project/ convention could be reviewed on its own terms
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Scaffolded `project/design/proposals/` and its README, so the repo has a
home for design proposals. Prosoc had deliberately deferred fleshing out
`project/` until a concrete need arose; authoring the first design proposal
(manifest-driven normative packet assembly, PR #36) was that need, so the
directory and its conventions landed here as a separate, reviewable change
ahead of the proposal itself.

# Result

**`project/design/proposals/README.md`:** documents the proposal-set layout,
the two-axis lifecycle (`status` for whether a design decision governs;
`implementation_status` for whether it is delivered), the `PROP-*` ID
convention, and the status→bucket mapping — all taken from LRH's own
`project/design/proposals/`, not invented.

Adapted rather than copied: LRH's version refers throughout to `design.md`,
`architecture.md`, and `repository_spec.md` as the canonical documents a
proposal folds into on adoption, and prosoc has none of those yet, so the
README states that proposals here stand on their own until it does.

Following the convention already set by `project/audits/README.md`, it
disambiguates the two lifecycles that would otherwise collide: a proposal's
`status` governs an engineering design decision, while a normative card's
`STATE` governs whether card content is fit for downstream use. Card states
are named as `prosoc/scenarios/workflow.md` actually defines them — optional
`SOURCE`, then `DRAFTED`, `EDITED`, `AUDITED` (human review), optional
`VALIDATED` (empirical evidence), and terminal `DEPRECATED`/`RETIRED` — after
a check found the repo's own stage-5 term is inconsistent (`VALIDATED` in
`workflow.md` vs `VERIFIED` in `constitutions/template.md` and the paper).

Buckets are created on demand rather than pre-created empty, matching LRH's
own repo, which carries only `proposed/` and `adopted/`. The five other
`lrh project doctor` paths (`principles`, `goal`, `roadmap`, `evidence`,
`status`) were intentionally left unscaffolded, consistent with prosoc's
deferred-scaffolding decision.

This is a retroactive execution record — the session was an ad hoc
design-then-implement conversation, not started via `/lrh-implement`, so no
`in_progress` record existed prior to `/lrh-closeout`.

# Validation

- `lrh validate`: 0 errors, 0 warnings.

# Follow-up

- PR #36 (PROP-NORMATIVE-PACKET-ASSEMBLY) is stacked on this scaffolding and
  still open; it needs retargeting from the now-merged scaffold branch to
  `main`, and gets its own execution record on merge.
