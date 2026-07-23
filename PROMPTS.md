# Prompt Workflow

Prompt IDs track meaningful prompt-driven implementation work in this repo,
tying a commit and its execution record back to the instruction that
produced it. This is the schema already in use across every commit message
and execution record in `project/executions/`.

## Prompt ID format

```
PROMPT(<WORK_ITEM_OR_AD_HOC>:<SLUG>)[<ISO-8601 timestamp with offset>]
```

- `<WORK_ITEM_OR_AD_HOC>` — a work-item ID (e.g. `WI-SCENARIO-SECTION-RENDERER`)
  when the work traces to a formal work item under `project/work_items/`, or
  `AD_HOC` when it doesn't.
- `<SLUG>` — an uppercase, underscore-separated description of the work.
- The timestamp is when the prompt was issued, not when the resulting
  execution record was created (see `project/executions/README.md` — the
  two are usually close but not identical).

Example, from `project/executions/AD_HOC/2026_07_18_23_42_57_README_DISTILL_SCRIPT_PATH.md`:

```
PROMPT(AD_HOC:README_DISTILL_SCRIPT_PATH)[2026-07-18T23:41:22-04:00]
```

## Prosoc's slug-suffix convention

Beyond the base format, prosoc layers two suffixes onto the slug for
follow-up passes on the same PR:

- `_REVIEW` — an `/lrh-review-response` pass addressing open PR review
  comments.
- `_CONFIRM` — a following `/lrh-confirm-fixes` pass, verifying the
  `_REVIEW` fixes with fresh eyes before merge.

## Generating and tracking prompt IDs

- `lrh prompt label --work-item <ID-or-AD_HOC> --slug <SLUG>` — generate a
  new prompt ID and its suggested execution-record path.
- `lrh prompt record-execution --prompt-id ... --slug ... [--status ...] [--pr ...] [--commit ...]` —
  create the execution-record file itself.
- `lrh prompt update-execution --execution-id ... --status landed --pr ... --commit ... --session-transcript ...` —
  used by `/lrh-closeout` to flip an `in_progress` record to `landed`.

## Looking up existing execution records for a prompt ID

- `lrh prompt check-execution --prompt-id ...` — the authoritative exact
  lookup for soft-idempotence/rerun decisions. Exact matches against the
  frontmatter `prompt_id` field are authoritative.
- `lrh match executions <prompt-file>` — when a prompt file contains the ID
  and you want the command to extract it before applying exact matching.
- `lrh search executions <query>` — exploratory local substring search
  only. Useful for discovery/auditing/debugging, but not authoritative for
  blocking or rerun decisions.

See `project/executions/README.md` for the full execution-record schema and
status conventions.
