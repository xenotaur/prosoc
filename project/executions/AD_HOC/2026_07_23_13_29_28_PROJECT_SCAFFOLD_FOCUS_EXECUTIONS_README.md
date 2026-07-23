---
execution_id: 2026_07_23_13_29_28_PROJECT_SCAFFOLD_FOCUS_EXECUTIONS_README
prompt_id: PROMPT(AD_HOC:PROJECT_SCAFFOLD_FOCUS_EXECUTIONS_README)[2026-07-23T13:29:28-04:00]
work_item: AD_HOC
status: landed
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/33
commit: 1da16c4af451acf41743ccd274a2bfcfcb004fa7
created_at: 2026-07-23T13:29:28-04:00
agent: claude_app
instruction_source: ad hoc — investigation into bootstrapping prosoc onto the LRH project control plane (`lrh project init`), which surfaced two `doctor`/`validate` gaps worth closing directly rather than deferring both to the separate `/lrh-init` design session
session_transcript: claude-app:18a43d9f-32c1-4b82-8883-e2cb590cf592
---

# Summary

Investigated what it would take to bootstrap `prosoc` onto the LRH project
control plane via `lrh project init` (`--dry-run` against all three
profiles: `minimal`, `prompt-workflow`, `full`), without running init or
creating scaffold files as part of the investigation itself. Found that no
profile ever creates `project/focus/current_focus.md` even though `lrh
validate` unconditionally requires it — a standing gap independent of any
bootstrap choice — and that `project/executions/README.md` was one of two
`doctor`-required paths still missing despite ~30 real execution records
already using a de facto standardized schema. Landed both files directly,
plus fed a separate finding (that `project/audits/` is an established
cross-repo LRH convention, not a prosoc-specific naming collision) into
the ongoing `/lrh-init` design session as a follow-up prompt.

# Result

**`project/focus/current_focus.md`:** authored with the required
frontmatter (`id`, `title`, `status: active`) and body describing the
actual current engineering focus — maintaining the scenario corpus's
audit-clean state (20/20 scenarios, reached via PR #30–#32) as further
changes land — rather than a placeholder. Also notes the file's scope is
prosoc's own LRH-facing engineering focus, distinct from the P1–P8 charter
and the scenario-content lifecycle.

**`project/executions/README.md`:** documents the execution-record schema
already in use across every record in this directory (filename/`execution_id`
convention, required frontmatter fields including the `status` enum,
prosoc's own `_REVIEW`/`_CONFIRM` slug-suffix convention, and the
`agent`/`instruction_source`/`session_transcript` fields prosoc adds beyond
LRH's canonical dataclass), plus the `lrh prompt check-execution` / `lrh
match executions` / `lrh search executions` lookup commands.

**Deliberately out of scope:** `project/principles`, `goal`, `roadmap`,
`status`, `evidence`, `AGENTS.md`, `STYLE.md` — all would be empty stubs
with nothing real to put in them yet. `project/principles` in particular
has an unresolved naming overlap with `.claude/skills/_shared/principles.md`
(P1–P8 charter) and README's own "Guiding Principles" section, left for
the `/lrh-init` design conversation.

This is a retroactive execution record — the session was ad hoc
investigation-then-implementation, not started via `/lrh-implement`, so no
`in_progress` record existed prior to `/lrh-closeout`.

# Validation

- `lrh validate`: 0 errors, 0 warnings (was 1 pre-existing error —
  `focus/current_focus.md` not found — before this change)
- `lrh project doctor`: `project/focus` and `project/executions/README.md`
  now report `present` (2 fewer `missing_required` errors; 5 remain,
  deliberately out of scope per above)
