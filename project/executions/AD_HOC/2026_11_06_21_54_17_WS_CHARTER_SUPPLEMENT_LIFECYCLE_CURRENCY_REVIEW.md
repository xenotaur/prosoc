---
execution_id: 2026_11_06_21_54_17_WS_CHARTER_SUPPLEMENT_LIFECYCLE_CURRENCY_REVIEW
prompt_id: PROMPT(AD_HOC:WS_CHARTER_SUPPLEMENT_LIFECYCLE_CURRENCY_REVIEW)[2026-11-06T21:53:57+00:00]
work_item: AD_HOC
status: landed
rerun_of: 2026_11_06_21_38_30_WS_CHARTER_SUPPLEMENT_LIFECYCLE_CURRENCY
pr: https://github.com/xenotaur/prosoc/pull/133
commit: 3f430773f974061a713b46f5043f8d5691a6301d
created_at: 2026-11-06T21:54:17+00:00
agent: claude_app
instruction_source: https://github.com/xenotaur/prosoc/pull/133
session_transcript: claude-app:0e614511-4f01-4980-80be-9f1202cf16c6
---

# Summary

Review-response pass for PR #133: 7 Copilot findings against the work
items' own prescribed procedures (this PR is planning-only, so every
finding targets the WI text's accuracy, not code).

# Result

All 7 findings triaged present/valid/feasible and fixed by editing the
affected work item files; none skipped. Each was independently
re-verified against actual tool behavior (not accepted from the review
prose alone) before fixing:

1. **Audit-currency-guard timestamp rule also rejects ordinary
   promotions** (`WI-CHARTER-SUPPLEMENT-AUDIT-CURRENCY-GUARD`). Confirmed
   `prosoc-card-approve`'s Step 5 commits state+projections strictly
   after the audit it promotes from -- a naive timestamp rule would
   permanently fail all 9 cards the moment they're promoted. Reframed
   the check's scope around "lifecycle-tracking surface vs. normative
   content" so one rule covers both the backfill case and the promotion
   case; added a third required test case.
2. **Promotion skill never writes dated AUDITED:/APPROVED: history
   bullets** (`WI-CHARTER-SUPPLEMENT-LIFECYCLE-PROMOTION`). Confirmed by
   reading `prosoc-card-approve/SKILL.md` in full: Step 5 touches only
   `state:` and its two projections, never a history bullet. Added an
   explicit hand-edit step after each of the 18 promotions.
3. **Charter's separate Status: header never gets synced by the
   promotion skill** (same WI). Confirmed via
   `validate_status.py`'s own comment ("`--fix` only ever projects the
   STATE line; it never addresses" the header) and
   `prosoc-card-approve`'s own quality checklist ("Only the `state:`
   field... changed"). Added an explicit hand-sync + re-validate step
   after each of the charter's 2 promotions.
4. **PDF-based history check is impossible for 2 of the 9 cards** (same
   WI). Confirmed `navigate_follow_agent`/`navigate_lead_agent` are
   absent from `papers/01_charter/sources.txt`. Scoped the PDF-text
   check to the 7 in-sources.txt cards; added a direct file-level check
   for the other 2.
5. **Wrong PDF output path** (same WI). Confirmed `render.py`'s own
   `BUILD_DIR = REPO_ROOT / "build" / "papers" / "01_charter"`. Fixed
   `artifacts_expected` and the `pdftotext` validation command.
6. **`--fix` reads the distilled YAML, not the fenced Markdown YAML, so
   running it before distillation re-projects the stale state**
   (`WI-CHARTER-SUPPLEMENT-LIFECYCLE-STALE-DEMOTION`). Confirmed via
   `validate_status.py`'s own module docstring. Reordered Required
   Changes: edit fenced YAML -> regenerate distilled YAML -> `--fix` ->
   hand-sync the charter header (which `--fix` still never touches).
7. **Demoting 3 sample_packet members breaks packet-drift CI and 2 real
   tests before any promotion lands** (same WI). Confirmed `charter`,
   `navigate_lead_agent`, and `high_urgency` are all members of
   `src/prosoc/manifests/sample_packet/manifest.yml`, and that
   `.github/workflows/packet.yml`/`tests/nca/packet/cli_test.py` assert
   production-mode (no `--allow-unapproved`) success against that real
   manifest. Documented this as an expected, bounded, 2-test failure
   window rather than weakening the fail-closed gate -- removed the
   (now-impossible) instruction to regenerate `packet.golden.yml` during
   demotion.

# Validation

- `lrh validate` -- 0 errors, 20 pre-existing warnings (unrelated).
- `scripts/lint` -- all checks passed.
- `scripts/format --check --diff` -- 22 files would be reformatted, all
  pre-existing drift confirmed unrelated to this PR (`git diff
  origin/main --stat` shows only the 10 Markdown planning files this PR
  touches; no Python file is among them).
- `scripts/version tools` -- not available in this repo (no
  `scripts/version` script exists here); treated as an environment gap,
  not a regression, per this skill's own guidance.
- `PYTHONPATH="$(pwd)/src" python -m unittest discover tests "*_test.py"`
  -- 344 tests, `OK (skipped=1)` -- unaffected, as expected for a
  Markdown-only change.
- **Publication outcome: Pushed directly** -- to
  `xenotaur/feat/ws-charter-supplement-lifecycle-currency` on
  `xenotaur/prosoc#133`.

# Follow-up

None blocking. Thread resolution (if any GitHub-side thread exists for
these findings) is `/lrh-confirm-fixes`'s job, not this record's.
