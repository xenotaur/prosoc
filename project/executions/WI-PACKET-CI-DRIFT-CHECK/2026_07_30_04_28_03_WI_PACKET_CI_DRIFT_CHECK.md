---
execution_id: 2026_07_30_04_28_03_WI_PACKET_CI_DRIFT_CHECK
prompt_id: PROMPT(WI-PACKET-CI-DRIFT-CHECK:WI_PACKET_CI_DRIFT_CHECK)[2026-07-30T04:17:01-04:00]
work_item: WI-PACKET-CI-DRIFT-CHECK
status: in_progress
rerun_of:
pr: https://github.com/xenotaur/prosoc/pull/59
commit:
created_at: 2026-07-30T04:28:03-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-PACKET-CI-DRIFT-CHECK.md
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Implementation of `WI-PACKET-CI-DRIFT-CHECK` (Phase 3, the final phase of
`WS-NORMATIVE-PACKET-ASSEMBLY`): a `--check` flag on `prosoc/packet/cli.py`
that compares an assembled packet against a checked-in golden file, plus a
new CI workflow enumerating golden-having manifests.

# Result

Added `--check` to `prosoc/packet/cli.py`: assembles as usual (respecting
`--allow-unapproved`/`--format`), then byte-compares the rendered output
against `<manifest_dir>/packet.golden.yml`. Exact match exits 0 silently;
drift exits 1 with a unified diff on stderr; a missing golden exits 1 with a
clear error explaining how to create one via a redirected normal run. No
`--check-all` CLI mode was added, per the work item's `forbidden_actions`.

Generated the first checked-in golden,
`prosoc/manifests/sample_packet/packet.golden.yml`, via
`scripts/assemble prosoc/manifests/sample_packet/manifest.yml --allow-unapproved "CI packet-drift check (dev-mode golden; corpus not yet APPROVED)"`.
Verified determinism empirically by running the assembly twice and diffing
the output byte-for-byte identical before committing.

Added `.github/workflows/packet.yml`, mirroring `charter.yml`'s
trigger/step shape (path-scoped to `prosoc/manifests/**`, `prosoc/packet/**`,
itself), which shell-loops over every `prosoc/manifests/*/packet.golden.yml`
and runs `--check` against each with the same fixed justification string —
directory-convention enumeration in the workflow, not a CLI flag.

Documented the `--check` flag, the golden-file convention, and the fixed
justification string (which must match verbatim between golden generation
and CI, per the work item's risk note) in `prosoc/packet/README.md`. Fixed a
stale usage-comment path in `scripts/assemble` left over from
`WI-PACKET-MANIFEST-FAMILY` (`prosoc/packet/examples/sample_manifest.yml` →
`prosoc/manifests/sample_packet/manifest.yml`) and added a `--check` example.

Added `--check` test coverage in `tests/packet/cli_test.py`: matching golden
(exit 0, silent), drifted golden (exit 1, unified diff on stderr), and
missing golden (exit 1, clear error) — using a scratch manifest directory so
the drift/missing cases never touch the checked-in golden. Also added a
regression test that `--check` currently passes against the real checked-in
golden.

# Validation

- `scripts/format --check --diff`: 71 files unchanged, clean.
- `scripts/lint`: all checks passed.
- `scripts/test`: 204 tests, OK.
- `lrh validate`: 0 errors, 0 warnings.
- Manual verification of all three `--check` outcomes (match, drift with
  diff on stderr, missing golden with clear error) before writing the
  automated tests.
- Determinism verified empirically: assembled the sample manifest twice,
  diffed the two outputs byte-for-byte identical.

# Follow-up

- Wait for review, respond via `/lrh-review-response`, confirm via
  `/lrh-confirm-fixes`, then merge (human gate) and run `/lrh-closeout` to
  land this record and move the work item to `resolved/`. Completing this
  work item satisfies `WS-NORMATIVE-PACKET-ASSEMBLY`'s last exit criterion.
