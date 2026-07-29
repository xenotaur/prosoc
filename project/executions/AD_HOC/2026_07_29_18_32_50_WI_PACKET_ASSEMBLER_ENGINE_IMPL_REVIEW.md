---
execution_id: 2026_07_29_18_32_50_WI_PACKET_ASSEMBLER_ENGINE_IMPL_REVIEW
prompt_id: PROMPT(AD_HOC:WI_PACKET_ASSEMBLER_ENGINE_IMPL_REVIEW)[2026-07-29T18:32:50-04:00]
work_item: AD_HOC
status: landed
rerun_of: 2026_07_29_18_17_24_WI_PACKET_ASSEMBLER_ENGINE
pr: https://github.com/xenotaur/prosoc/pull/51
commit: 308da1fa6b20739ffdbc0a2ef0c3c4c79080d716
created_at: 2026-07-29T18:32:50-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/51
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Addressed three Copilot review comments on PR #51 (implementation of
WI-PACKET-ASSEMBLER-ENGINE). `rerun_of` points at the implementation primary
(`2026_07_29_18_17_24_WI_PACKET_ASSEMBLER_ENGINE`).

# Result

All three passed presence/validity/feasibility triage; all applied.

1. [`prosoc/packet/loader.py`] — `load_card` decoded card bytes as UTF-8 but
   caught only `yaml.YAMLError`, so a non-UTF-8 card would escape the documented
   `ResolveError` contract. Now catches `(UnicodeDecodeError, yaml.YAMLError)`.
2. [`prosoc/packet/manifest.py`] — `load_manifest` read the file but caught only
   `yaml.YAMLError`, so `OSError`/`UnicodeDecodeError` could escape
   `ManifestError`. Now catches `(OSError, UnicodeDecodeError, yaml.YAMLError)`.
3. [`prosoc/packet/assemble.py`] — the charter was special-cased to
   `guidance["charter"] = ...` (not nested under its id), contradicting the
   "namespaced by family/id" contract and the README. Now every family,
   including the single-source charter, nests as `guidance[family][id]`
   (`guidance.charter.charter`). The schema already allowed this (family
   sections are additional properties); no schema change needed.

Added regression tests: a charter-nesting assertion and manifest read-error
cases (missing file, invalid UTF-8) surfacing `ManifestError`.

# Validation

- `scripts/test` / pytest: 190 passed (+4 regression tests; 42 in tests/packet).
- `scripts/lint`: All checks passed.
- `scripts/format --check` (black 25.12.0): clean.
- `lrh validate`: 0 errors, 0 warnings.
- Smoke: `scripts/assemble … --allow-unapproved` confirms
  `guidance.charter.charter` is now nested under its id.

# Follow-up

- `/lrh-confirm-fixes` on PR #51 to verify against the live diff and resolve the
  three review threads before merge.
