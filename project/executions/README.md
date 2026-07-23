# Execution Records

Execution records live under `project/executions/<WORK_ITEM_OR_AD_HOC>/`,
one Markdown file per record, filed under the work item they belong to
(e.g. `project/executions/WI-SCENARIO-SECTION-RENDERER/`) or under
`AD_HOC/` for prompt-driven work with no formal work item. This is the
schema already in use across every record in this directory, produced by
`/lrh-implement`, `/lrh-review-response`, and `/lrh-confirm-fixes`.

## Filename and `execution_id`

Files are named `<execution_id>.md`, and `execution_id` follows
`YYYY_MM_DD_HH_MM_SS_<SLUG>` — a creation timestamp plus an uppercase
slug describing the work (e.g.
`2026_07_23_02_41_20_AUDIT_ALL_SCENARIOS_2026_07_22_CONFIRM`). Prosoc
layers two suffix conventions onto the slug beyond LRH's generic
prompt-id concept: `_REVIEW` for an `/lrh-review-response` pass and
`_CONFIRM` for a following `/lrh-confirm-fixes` pass on the same PR.

## Required frontmatter

These fields are the canonical execution-record schema (see LRH's
`prompt_workflow_records.ExecutionRecord`):

| Field | Meaning |
|---|---|
| `execution_id` | Matches the filename stem. |
| `prompt_id` | `PROMPT(<WORK_ITEM_OR_AD_HOC>:<SLUG>)[<ISO-8601 timestamp with offset>]` — the authoritative identity for rerun/idempotence decisions. |
| `work_item` | The work-item ID this record belongs to, or `AD_HOC`. |
| `status` | One of `planned`, `in_progress`, `landed`, `failed`, `reverted`, `superseded` (only `landed` has been used in this repo so far). |
| `rerun_of` | `execution_id` of a prior record this one supersedes/reruns, or blank if none. |
| `pr` | Full PR URL (not a bare number — see `project/executions/AD_HOC/2026_07_05_02_55_03_PROSOC_AUDIT_SCENARIO_SKILL_REVIEW.md` for why: an earlier record used a bare number and was corrected for consistency). |
| `commit` | The landed commit SHA. |
| `created_at` | ISO-8601 timestamp with offset. |

Prosoc's own records additionally populate `agent`, `instruction_source`,
and `session_transcript` — not part of LRH's canonical dataclass, but used
consistently across every record here to trace which agent/session/source
produced the work.

## Looking up execution records

- `lrh prompt check-execution --prompt-id ...` — the authoritative exact
  lookup for soft-idempotence/rerun decisions. Exact matches against the
  frontmatter `prompt_id` field are authoritative.
- `lrh match executions <prompt-file>` — when a prompt file contains the
  ID and you want the command to extract it before applying exact
  matching.
- `lrh search executions <query>` — exploratory local substring search
  only. Useful for discovery/auditing/debugging, but not authoritative for
  blocking or rerun decisions.
