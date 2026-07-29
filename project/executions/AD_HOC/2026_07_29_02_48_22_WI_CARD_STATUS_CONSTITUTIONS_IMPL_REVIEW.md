---
execution_id: 2026_07_29_02_48_22_WI_CARD_STATUS_CONSTITUTIONS_IMPL_REVIEW
prompt_id: PROMPT(AD_HOC:WI_CARD_STATUS_CONSTITUTIONS_IMPL_REVIEW)[2026-07-29T02:45:02-04:00]
work_item: AD_HOC
status: in_progress
rerun_of: 2026_07_29_02_41_43_WI_CARD_STATUS_CONSTITUTIONS
pr: https://github.com/xenotaur/prosoc/pull/47
commit: 
created_at: 2026-07-29T02:48:22-04:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/47
session_transcript: claude-app:ca4961c6-505e-4771-b683-a69b25ac2c2a
---

# Summary

Addressed one Copilot review comment on PR #47 (implementation of
WI-CARD-STATUS-CONSTITUTIONS). `rerun_of` points at the implementation primary
(`2026_07_29_02_41_43_...`, PR #47), disambiguated from the same-slug
work-item-creation primary (`2026_07_29_00_16_07_...`, PR #46) by `pr:`/bucket.

# Result

[r3671661945](https://github.com/xenotaur/prosoc/pull/47#discussion_r3671661945)
— the constitutions family was registered with `supports_flat=False`, but
`discover_constitutions` handles both directory and flat layouts (unlike the
directory-only tasks/contexts discoverers), so `--layout flat` was wrongly
rejected. Fixed by setting `supports_flat=True`.

Fixing it surfaced a **latent bug**: `discover_flat_layout`'s exclusion set
named the template `constitution_template.md`, but the actual file is
`template.md`, so flat discovery over the real corpus picked up `template.md`
and crashed on the missing `template.yml`. Corrected the exclusion to
`template.md` (kept the legacy name for safety). Added a constitutions
flat-layout test. Now `--family constitutions --layout flat` validates flat
cards and reports "no cards found" gracefully on the directory-layout corpus;
the default `scripts/validate/status` stays 30/30.

The comment passed presence/validity/feasibility triage; nothing was skipped.

# Validation

- `scripts/format --check` (black 25.12.0): clean.
- `scripts/lint`: All checks passed.
- `scripts/test`: 139 passed (+1 flat-layout test).
- `lrh validate`: 0 errors, 0 warnings.
- `scripts/validate/status`: all 30 cards consistent.

# Follow-up

- Suggest `/lrh-confirm-fixes` on PR #47 before merge to resolve the review
  thread.
