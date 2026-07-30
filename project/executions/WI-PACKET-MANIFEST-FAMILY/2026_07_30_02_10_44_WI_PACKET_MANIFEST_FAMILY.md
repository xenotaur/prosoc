---
execution_id: 2026_07_30_02_10_44_WI_PACKET_MANIFEST_FAMILY
prompt_id: PROMPT(WI-PACKET-MANIFEST-FAMILY:WI_PACKET_MANIFEST_FAMILY)[2026-07-30T01:39:48-04:00]
work_item: WI-PACKET-MANIFEST-FAMILY
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/56
commit: 
created_at: 2026-07-30T02:10:44-04:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-PACKET-MANIFEST-FAMILY.md
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Implemented WI-PACKET-MANIFEST-FAMILY — Phase 2 of
`PROP-NORMATIVE-PACKET-ASSEMBLY`: turning the manifest from Phase 1's plain
YAML input into a sixth, genuinely auditable card family. New
`prosoc/manifests/` package, registered into the two existing generic
status/audit systems, with no `prosoc/packet/` engine changes.

# Result

- `prosoc/manifests/schema.json`: flat shape (not root-wrapped, like
  tasks/contexts) — `id`/`name`/`state` (canonical 7-value enum)/`builder`
  (optional)/`members[]` (`{family, id}`, non-empty). `members[].family` is
  an enum excluding `manifests`, so a manifest structurally cannot name
  another manifest as a member (the recursion risk flagged in the WI's Risk
  Notes).
- `prosoc/manifests/template.md` + `distill.py` + `scripts/distill/manifests`:
  mirror `prosoc/tasks/`'s structure exactly (`discover_directory_layout`,
  `distill_all`, `root_key=None`).
- `prosoc/manifests/sample_packet/manifest.md`: migrated
  `prosoc/packet/examples/sample_manifest.yml`'s content into a real,
  schema-valid card; old ad-hoc example removed
  (`prosoc/packet/examples/` no longer exists). Updated the one place that
  referenced the old path: `prosoc/packet/README.md`'s two usage examples,
  plus `tests/packet/cli_test.py`'s `SAMPLE` constant. `prosoc/packet/`'s
  engine code itself (`loader.py`, `resolve.py`, `gate.py`, `assemble.py`,
  `cli.py`, `manifest.py`) is byte-for-byte unchanged — confirmed
  `parse_manifest` already tolerated the added `id`/`name`/`state` keys, so
  no engine-side change was needed, exactly as planned.
- `prosoc/utils/cards/validate_status.py`: registered `manifests` in
  `FAMILIES` (flat, directory-layout, `yaml_root_key=None`) — 
  `scripts/validate/status` now covers 32 cards across 6 families.
- `.claude/skills/_shared/audit_checklists/manifests.md`: new checklist,
  genuinely different in focus from the five content-family checklists — a
  manifest's primary risk is member *resolvability* (does every named
  `{family, id}` actually resolve via `prosoc.packet.loader.load_card`?),
  not prose/YAML content drift.
- `.claude/skills/prosoc-card-audit/SKILL.md` and
  `prosoc-card-audit-all/SKILL.md`: extended to dispatch on `manifests`
  (locate/enumeration tables, family lists, dry-run commands — manifests
  joins tasks/contexts/constitutions as a whole-family, no-per-card-scoping
  distiller).
- Added test coverage: `tests/manifests/distill_test.py` (discovery + a
  distill round-trip) and a `ManifestsFamilyTest` in
  `tests/utils/cards/validate_status_test.py`.

Encountered and worked around a pre-existing bug in
`prosoc.literate.utils.atomic_write`: with `show_diffs=True` it
unconditionally reads the target file for the diff, raising
`FileNotFoundError` on a card's very first distill (before its `.yml`
exists). This is not specific to manifests — it would hit any brand-new card
in any family's first `--show-diffs` run — and is out of this WI's scope
(`prosoc/literate/` isn't in Required Changes); worked around by running the
first distill without `--show-diffs`, exactly how any new card in an
existing family would naturally be authored.

Manually validated per the WI's own `## Validation` section: ran
`prosoc-card-audit` against `sample_packet` (all 5 members verified
resolvable via `prosoc.packet.loader.load_card`, zero card mutation — see
`prosoc/manifests/sample_packet/audit.md`), and confirmed
`scripts/assemble prosoc/manifests/sample_packet/manifest.yml` still works
unchanged (fail-closed by default; `--allow-unapproved` emits a valid,
hatch-stamped packet).

Prior-art check present in the WI. No `prosoc/packet/` engine changes; no CI
drift check (Phase 3); `manifests` not added to
`prosoc/packet/loader.py`'s five-family registry (by design); no normative
card content changed.

# Validation

- `scripts/test`: 196 passed (+6: 5 manifest distill tests + 1 family-test
  class covering 3 cases; no regressions elsewhere).
- `scripts/lint`: All checks passed.
- `scripts/format --check` (black 25.12.0): clean (71 files unchanged).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 32 cards (6 families) consistent.
- `scripts/distill/manifests --dry-run --show-diffs`: no differences
  (idempotent, after the initial creation run).
- Manual: `prosoc-card-audit` against `sample_packet` — `audit.md` written,
  `git diff` on the card empty (no mutation).
- Manual: `scripts/assemble prosoc/manifests/sample_packet/manifest.yml`
  (fail-closed) and `--allow-unapproved "manual WI validation"` (emits a
  valid packet) both behave identically to Phase 1's ad-hoc example.

# Follow-up

- At closeout, resolve WI-PACKET-MANIFEST-FAMILY (Phase 2's manifest family
  is done). The workstream stays open for Phase 3 (CI drift check against
  checked-in golden packets).
- The pre-existing `atomic_write`/`show_diffs`-on-first-run bug noted above
  is real but out of scope; worth a small follow-up fix at some point (not
  urgent — every family's cards are already distilled once in the checked-in
  corpus, so it only bites a brand-new card's very first `--show-diffs` run).
