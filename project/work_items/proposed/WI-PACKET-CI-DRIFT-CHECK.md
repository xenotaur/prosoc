---
resolution: null
blocked_reason: null
blocked: false
id: WI-PACKET-CI-DRIFT-CHECK
title: CI packet-drift check against checked-in golden packets (Phase 3)
type: deliverable
status: proposed
assigned_agents: []
related_focus:
  - FOCUS-NORMATIVE-PACKET-ASSEMBLY
related_roadmap: []
related_workstreams:
  - WS-NORMATIVE-PACKET-ASSEMBLY
related_design:
  - project/design/proposals/proposed/normative-packet-assembly/00_proposal.md
depends_on:
  - WI-PACKET-MANIFEST-FAMILY
blocked_by: []
expected_actions:
  - create_file
  - edit_file
  - run_tests
  - create_pr
forbidden_actions:
  - force_push
  - delete_branch
  - promote_card_state
  - edit_card_normative_content
  - implement_cryptographic_signing
  - implement_check_all_cli_flag
acceptance:
  - scripts/assemble prosoc/manifests/sample_packet/manifest.yml --check --allow-unapproved "<fixed justification>" exits 0 against the checked-in golden packet
  - A deliberate edit to a member card (or the golden itself) makes --check exit 1 with a unified diff to stderr
  - A new CI workflow runs the drift check for every manifest with a checked-in golden and fails the build on drift
  - lrh validate, scripts/lint, scripts/test, and scripts/format --check all pass
required_evidence:
  - lrh_validate
  - test_output
  - manual_review
artifacts_expected:
  - prosoc/packet/cli.py
  - prosoc/manifests/sample_packet/packet.golden.yml
  - .github/workflows/packet.yml
  - prosoc/packet/README.md
  - scripts/assemble
  - tests/packet/cli_test.py
---

# WI-PACKET-CI-DRIFT-CHECK

## Summary

Add a `--check` flag to the packet assembler CLI that compares a freshly
assembled packet against a checked-in "golden" reference file, and a new CI
workflow that runs this check on every PR touching the manifest or packet
engine — the proposal's Phase 3, and the workstream's final exit criterion.

## Problem / Context

The proposal's Implementation Plan gives Phase 3 one line: "CI drift check
(`scripts/assemble --check`) against checked-in golden packets." Like
Phase 2, it has **no dedicated numbered Decision** — the design is settled
here.

Two corpus facts constrain the design, both re-verified before scoping:

- **The corpus is currently all-DRAFTED.** The default fail-closed gate
  (threshold `APPROVED`) emits nothing for any manifest today, so the only
  meaningful golden packet right now is a **development-mode** one, produced
  with `--allow-unapproved` and a fixed justification string baked into
  `predicate.policy.escape_hatch.justification`. The same justification
  string must be used at golden-generation time and in CI, or the string
  mismatch alone would register as drift.
- **The assembled envelope is deterministic.** `assemble()` builds the
  envelope via plain, insertion-ordered dict construction, and
  `prosoc.packet.cli`'s YAML rendering uses `sort_keys=False` — re-running
  `scripts/assemble` on an unchanged corpus with the same flags produces
  byte-identical output. `subject.digest` and every
  `predicate.resolved_cards[].sha256` are already content-addressed. This is
  exactly the property a byte-diff drift check needs: the golden only goes
  stale when something real changed (a member card's content, or the
  assembler's own logic), not from incidental non-determinism.

### Duplication search
- In-repo: `.github/workflows/charter.yml` is the closest precedent — a
  path-scoped CI job that dry-run distills the charter and
  `git diff --exit-code`s the checked-in `prosoc/charter/charter.yml`. This
  WI's `--check`
  is a CLI-level analog (compare-in-process rather than shell `git diff`)
  applied to assembled packets rather than a single family's distilled YAML;
  the workflow structure (path-scoped triggers, checkout/setup-python/install
  steps) is mirrored, not duplicated.
- Sibling repos: None identified.
- External libraries: Not applicable.
- Recommendation: Proceed.

### Demand search
- Work items: None found. `WI-PACKET-MANIFEST-FAMILY` (resolved, Phase 2) is
  the immediate predecessor — this WI needs `prosoc/manifests/sample_packet/`
  to exist as the manifest to golden-check.
- Proposals: `PROP-NORMATIVE-PACKET-ASSEMBLY` governs this item (Phase 3
  row; no dedicated Decision).
- Backlog: No `project/design/backlog.md` exists.
- Recommendation: No action.

## Scope

`--check` on `prosoc/packet/cli.py`, one checked-in golden file, and a new
CI workflow. No changes to `assemble`/`gate`/`resolve`/`loader` logic itself.

## Required Changes

1. **`prosoc/packet/cli.py`**: add `--check`. When set, assemble normally
   (respecting `--allow-unapproved`/`--format` as given), then compare the
   rendered output byte-for-byte against a checked-in golden file at
   `<manifest_dir>/packet.golden.yml` (convention-based path derived from the
   manifest's own directory — no override flag, keeping the CLI surface
   minimal). Match: exit 0, no output. Mismatch: print a unified diff to
   stderr, exit 1. Golden file missing: a clear error explaining how to
   create one (regenerate via a normal run redirected to that path — no
   dedicated "write golden" flag, consistent with how every other family's
   `.yml` is regenerated).
2. **`prosoc/manifests/sample_packet/packet.golden.yml`**: the first checked-in
   golden, generated via
   `scripts/assemble prosoc/manifests/sample_packet/manifest.yml
   --allow-unapproved "<fixed justification>"` redirected to this path. The
   justification string used here must be documented and reused verbatim by
   CI.
3. **`.github/workflows/packet.yml`**: new workflow, path-scoped to
   `prosoc/manifests/**`, `prosoc/packet/**`, and the workflow file itself
   (mirroring `charter.yml`'s trigger shape). Enumerates every
   `prosoc/manifests/*/` directory containing a `packet.golden.yml` (a shell
   loop, not a new CLI `--check-all` mode — keeps future manifests covered
   automatically without CLI scope growth) and runs `--check` with the fixed
   justification for each.
4. **`prosoc/packet/README.md`**: document `--check`, the golden-packet
   convention (path, regeneration procedure), and the fixed justification
   string.
5. **`scripts/assemble`**: fix its own usage-comment example, which still
   references the removed `prosoc/packet/examples/sample_manifest.yml`
   (missed when that path was retired in `WI-PACKET-MANIFEST-FAMILY`) — point
   it at `prosoc/manifests/sample_packet/manifest.yml` and add a `--check`
   example.
6. **`tests/packet/cli_test.py`**: add `--check` coverage — matching golden
   (exit 0), drifted golden (exit 1, diff on stderr), missing golden (exit 1,
   clear error).

## Non-Goals

- Does not add a `--check-all` or golden-path-override CLI flag — CI
  enumerates by directory convention instead.
- Does not produce a golden packet for a future APPROVED-mode corpus —
  today's golden is dev-mode only (`--allow-unapproved`); an APPROVED-mode
  golden is future work once the corpus has real human-approved cards.
- Does not implement cryptographic signing (Phase 4).
- Does not change `assemble`/`gate`/`resolve`/`loader`/`manifest` engine
  logic — verified the existing determinism already supports this WI's needs.
- Does not promote any card's STATE, or edit any card's normative content.

## Acceptance Criteria

- `scripts/assemble prosoc/manifests/sample_packet/manifest.yml --check
  --allow-unapproved "<fixed justification>"` exits 0 against the checked-in
  golden packet.
- A deliberate edit to a member card (or the golden itself) makes `--check`
  exit 1 with a unified diff to stderr.
- A new CI workflow runs the drift check for every manifest with a
  checked-in golden and fails the build on drift.
- `lrh validate`, `scripts/lint`, `scripts/test`, and `scripts/format --check`
  all pass.

## Validation

- `scripts/format --check --diff`
- `scripts/lint`
- `scripts/test`
- `lrh validate`
- `scripts/assemble prosoc/manifests/sample_packet/manifest.yml --check
  --allow-unapproved "<fixed justification>"` (expect exit 0)
- Deliberately edit `sample_packet`'s golden (or a member card) and re-run
  `--check` (expect exit 1 with a diff), then revert
- `python -m prosoc.packet.cli --help` (confirm `--check` is documented)

## Risk Notes

- **Justification-string coupling.** The golden's baked-in
  `escape_hatch.justification` string must match exactly between generation
  and CI, or the string itself is flagged as drift. Document the fixed
  string in one place (`prosoc/packet/README.md`) and reference it from both
  the golden-generation command and the CI workflow, rather than letting it
  drift independently in two places.
- **Corpus-wide drift blast radius.** Because `subject.digest` covers the
  whole `guidance` block, editing *any* member card referenced by
  `sample_packet`'s manifest (charter, the one constitution, one scenario,
  one task, one context) will trip the drift check — this is intentional
  (the point of the check), but should be called out in the README so a
  future card-editing PR isn't surprised by an unrelated-looking CI failure.
- **Determinism is necessary, not sufficient.** Verify byte-for-byte
  reproducibility empirically (regenerate twice, diff the two outputs) before
  relying on it for the golden-file comparison, rather than trusting the
  code-reading argument alone.

## Related Workstream and Designs

- Workstream: `project/workstreams/proposed/WS-NORMATIVE-PACKET-ASSEMBLY.md`
  (Phase 3 — completing this WI satisfies the workstream's final exit
  criterion).
- Design: `project/design/proposals/proposed/normative-packet-assembly/00_proposal.md`
  (Implementation Plan, Phase 3 row).
