---
execution_id: 2026_07_30_14_55_00_PACKET_COMBINATORICS_EXPERIMENT
prompt_id: PROMPT(AD_HOC:PACKET_COMBINATORICS_EXPERIMENT)[2026-07-30T14:54:50-04:00]
work_item: AD_HOC
status: landed
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/60
commit: 4451de08e9add4004f6c8ff07b09e2b5881447b8
created_at: 2026-07-30T14:55:00-04:00
agent: claude_app
instruction_source: ad_hoc conversation — dogfooding prosoc.packet and scaffolding experiments/2026_07 to demonstrate packet variation across (task, context, scenario) combinations
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Primary execution record for PR #60 — dogfoods `prosoc.packet` (the
manifest-driven normative packet assembler, `PROP-NORMATIVE-PACKET-ASSEMBLY`,
adopted) by scaffolding `experiments/2026_07/`, parallel to
`experiments/2026_01/`. No `/lrh-implement` was run for this PR (it grew
directly out of live conversation exploration), so this record is created
at the start of `/lrh-land`'s review-response step per the backfill-early
convention (mint the primary now rather than waiting for closeout-time
backfill, since review required a fix).

# Result

Before scaffolding, live-verified the assembler end-to-end in conversation:
default production gate fail-closes correctly against the real corpus;
a dev-mode packet's envelope shape matches the design (in-toto statement,
namespaced `guidance`, SLSA-style `predicate.resolved_cards`); the
principle union with emphasis annotations (Decision 6) behaves correctly,
including that `deprioritized` principles are retained, not dropped; the
namespace-collision guard between `scenario.context` and the `contexts`
family holds; and `subject.digest` was independently recomputed (exact
serialization from `assemble.py`) and matched the envelope's claimed
digest byte-for-byte, proving the detached-`guidance`-stays-verifiable
property actually holds, not just assumed from code-reading.

Built on that: 15 hand-curated (task, context, scenario) combinations
across 5 role-coherent (task, context) pairs (out of 16 possible — most
others are role-mismatched or redundant), each justified against the
actual task/context/scenario card content since prosoc has no
scenario->task/context reference edges (Decision 3's deliberate
deferral) — pairing is a human judgment call, not inferred by tooling.
Two scenario groups are deliberately repeated under two different
contexts to isolate context's effect on the same scenario+task.

`experiments/2026_07/scripts/combinations.py` is the single source of
truth; `build_manifests.py` writes ad-hoc manifests to `corpora/`;
`assemble_all.py` assembles each into `results/packets/`, writes
`results/summary.json`, and generates `results/summary.md` with an
auto-detected "highlighted diffs" section for same-scenario+task pairs
differing only by context — which correctly reproduced the exact P2/P3
emphasis flip found manually in conversation.

Copilot review raised two real issues in `assemble_all.py`: the script
exited 0 even when combos failed to assemble (silent partial-failure
risk in automation), and `_write_summary_md` carried an unused
`combos_by_id` parameter. Both fixed: the script now exits 1 whenever
any combo fails, and the dead parameter was removed. Fix verified by
deliberately breaking a manifest (confirmed exit 1, "14/15 packets"),
then restoring it and confirming exit 0 with byte-identical output to
before.

No `prosoc.packet` engine code was changed — pure dogfooding of the
already-shipped Phase 1-3 assembler.

# Validation

- Both scripts run cleanly, 15/15 packets assembled, 0 failures.
- Reproducibility verified: deleted `corpora/`+`results/`, reran from
  scratch, identical output.
- `black`/`ruff` clean on all three new scripts (note: `experiments/` is
  not part of the repo's CI-enforced lint/format scope — `2026_01`'s own
  scripts fail both — this is extra hygiene, not a requirement).
- Post-review-fix: deliberately broke one manifest, confirmed exit 1 and
  "14/15 packets" reported; restored it, confirmed exit 0 and
  byte-identical summary.md/summary.json to the pre-break run.
- CI on PR #60 (`lint`, `test`): pass on both the initial commit and the
  review-fix commit.
- `lrh validate`: 0 errors, 0 warnings.

# Follow-up

- Full review-response/confirm-fixes narrative recorded in this run's
  `_CONFIRM` record
  (`rerun_of: 2026_07_30_14_55_00_PACKET_COMBINATORICS_EXPERIMENT`).
- No work item or workstream involved (AD_HOC, pure dogfooding of
  already-shipped tooling) — nothing further to resolve.

CHAIN-NOTE: cycles=1; stops=0; gates=[merge]; friction="the _CONFIRM record's commit field (23bfba5) is the pre-merge HEAD verified at confirm time, not the eventual squash-merge commit (4451de0), since the execution-record commit itself landed after the confirm pass was written -- expected under this record-then-commit-records ordering, not a bug"; note="backfill path (no prior /lrh-implement); primary record minted early at review-response per the mint-early-on-required-fix convention, so no closeout-time backfill was needed"
