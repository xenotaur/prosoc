---
execution_id: 2026_08_13_06_51_07_WI_CHARTER_FRONTIERS_SYNC
prompt_id: PROMPT(AD_HOC:WI_CHARTER_FRONTIERS_SYNC)[2026-08-13T06:50:22+00:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/94
commit: d8a164a56655c42af612f1196f0d88445a3c6f9f
created_at: 2026-08-13T06:51:07+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CHARTER-FRONTIERS-SYNC.md
session_transcript: claude-app:6b2ba6cf-e741-4636-96d3-430b7f169c45
---

# Summary

Created work item `WI-CHARTER-FRONTIERS-SYNC` to implement the charter
content edits decided in `PROP-CHARTER-FRONTIERS-SYNC` (PR #92) —
translating the proposal's per-principle decisions into concrete
`prosoc/charter/charter.md` edit targets for P1–P9.

# Result

Wrote `project/work_items/proposed/WI-CHARTER-FRONTIERS-SYNC.md` with a
`## Required Changes` section giving draft target text per principle (P1
broadened scope, P2/P3/P4/P7 merged wording, P5 hedge restored, P6 modal
only, P8 taxonomy inlined, P9 qualifier trimmed, MUST-for-P0-and-P1/
SHOULD-elsewhere modal convention applied throughout), plus the
distill/re-audit/lifecycle steps needed to carry the charter back through
EDITED → AUDITED → APPROVED. `owner`/`contributors` fields were omitted
per this project's known gap (no contributors registry yet) after an
initial `lrh validate` failure on `UNKNOWN_OWNER`/`UNKNOWN_CONTRIBUTOR`.

# Validation

- `lrh validate` — 0 errors, 0 warnings (after removing `owner`/
  `contributors`, which failed validation on first pass since this
  project has no contributors registry).

# Follow-up

- Run `/lrh-implement WI-CHARTER-FRONTIERS-SYNC` (or equivalent) once
  `PROP-CHARTER-FRONTIERS-SYNC` (PR #92) lands, to actually edit
  `prosoc/charter/charter.md`, regenerate `charter.yml`, and carry the
  charter through its lifecycle back to APPROVED.
- This work item's `depends_on` is currently empty even though it
  logically depends on `PROP-CHARTER-FRONTIERS-SYNC` being adopted first
  — proposals aren't `WI-*` IDs so there's no `depends_on` slot for them;
  worth confirming the proposal's `status` before starting
  implementation.
- `session_transcript` above uses the live host session ID; update if a
  more durable pointer becomes available.
