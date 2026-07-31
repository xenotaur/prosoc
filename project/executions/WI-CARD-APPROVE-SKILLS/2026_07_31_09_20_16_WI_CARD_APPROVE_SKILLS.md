---
execution_id: 2026_07_31_09_20_16_WI_CARD_APPROVE_SKILLS
prompt_id: PROMPT(WI-CARD-APPROVE-SKILLS:WI_CARD_APPROVE_SKILLS)[2026-07-31T09:05:24+00:00]
work_item: WI-CARD-APPROVE-SKILLS
status: in_progress
rerun_of: 
pr: https://github.com/xenotaur/prosoc/pull/64
commit: ec751c4
created_at: 2026-07-31T09:20:16+00:00
agent: claude_app
instruction_source: project/work_items/proposed/WI-CARD-APPROVE-SKILLS.md
session_transcript: claude-app:1d38659c-be69-49bc-80ce-5b0f7bf4f368
---

# Summary

Implemented `WI-CARD-APPROVE-SKILLS`: the corpus review-queue engine
(`prosoc/utils/cards/review_queue.py` + `scripts/validate/review-queue`)
and the three skills (`prosoc-card-approve`, `prosoc-card-review`,
`prosoc-card-review-all`) settled in `PROP-NORMATIVE-CARD-APPROVAL`
Decisions 2 and 3. Ran via `/lrh-implement`, following the confirmed
implementation plan exactly.

# Result

**`prosoc/utils/cards/review_queue.py`**: `build_queue()` scans every
registered family via `validate_status.FAMILIES`, computing `scope`
(lifecycle steps remaining to `APPROVED`, via `packet.gate.PRODUCTION_ORDER`,
floored at 0 for end-of-life/unrecognised states) and `severity` (weighted
sum of a card's `audit.md` frontmatter — `blocking*100 + should_fix*10 +
suggestion*1`; a card with no `audit.md` at all gets a sentinel severity
above any possible weighted sum). `sort_queue()` composes independent
per-field stable sorts (exploiting `list.sort`'s stability guarantee) for
configurable multi-key ranking, always tiebreaking by `(family, id)`.
`main()` exposes `--family`, `--sort`, `--order`, `--format table|json`,
`--limit`. Manually verified against the live 32-card corpus: all 4 known
audit-coverage-gap cards (`guidance_docent`, `public_navigation`,
`routine_delivery`, `asimov_four_laws`) correctly sort first under the
default ranking — the design goal of subsuming the coverage-gap question
into the ranked list rather than a separate decision.

**Three skills** (`.claude/skills/prosoc-card-approve`,
`prosoc-card-review`, `prosoc-card-review-all`): pure prose, no Python
companion, matching `prosoc-card-audit`'s shape. `prosoc-card-approve` is
the mechanical primitive (evidence gate, confirm gate, edit fenced-YAML
`state:`, regenerate via the family's distiller, project via
`scripts/validate/status --fix`, re-verify). `prosoc-card-review` adds the
human-judgment layer, including a concrete staleness check for `audit.md`
(compare `git log -1 --format=%cI` on the card file vs. `audit.md` — an
implementation decision the WI's own Risk Notes flagged as
under-specified in the proposal). `prosoc-card-review-all` mirrors
`prosoc-card-audit-all`'s git-action pattern (branch/commit/PR) since
`prosoc-card-approve`/`prosoc-card-review` deliberately do not take git
actions themselves, staying usable standalone inside any existing branch.
One design correction made during writing: initially specified that
`prosoc-card-approve` always re-shows its own confirm gate even when
`prosoc-card-review` just got approval for the same transition — reworked
to let one clear "yes" satisfy both, avoiding redundant double-confirmation
in the composed flow while still requiring `prosoc-card-approve`'s own
gate on standalone invocation.

Provenance-bullet appending (`- **APPROVED:** <name>, <date>` in the
Markdown `STATUS` block) was considered and deliberately **not** built —
not specified in the WI's Required Changes or the governing proposal's
Decision 2, and adding it would have been scope creep beyond what was
confirmed at the plan gate.

# Validation

- `tests/utils/cards/review_queue_test.py` (new, 29 tests) — scope
  computation for every lifecycle state, `audit.md` frontmatter parsing
  (valid/missing/no-frontmatter/malformed-YAML/non-mapping), severity
  weighting (blocking always outranks any should-fix/suggestion count, and
  should-fix always outranks any suggestion count), `build_queue`/`sort_queue`
  via `dataclasses.replace(FAMILIES[name], default_root=tmp)` fixtures
  (mirroring `validate_status_test.py`'s pattern), and CLI integration
  against the live corpus (32 entries, all 6 families present, JSON output
  sorted, `--family`/`--limit` filters, unknown `--sort`/`--order` reject).
- `scripts/test` — full suite, 234 tests, OK.
- `scripts/lint` — one real finding (`B905`, `zip()` without `strict=` in
  `sort_queue`), fixed (`strict=True` is correct since `keys`/`orders` are
  constructed to always match in length); re-ran clean.
- `scripts/format --check --diff` — scoped check on both new files via
  direct `black --check`, since `scripts/format`'s wrapper doesn't
  actually restrict to given paths (always checks the whole `prosoc tests`
  tree first). `review_queue.py` was clean; `review_queue_test.py` had
  genuine line-length wrapping needed (not the known local/CI black
  version-drift artifact) — fixed via `black tests/utils/cards/review_queue_test.py`
  scoped to just that file, confirmed clean afterward. Did not touch any
  of the 22 pre-existing drifted files (known `black==25.12.0` CI pin vs.
  local `26.3.1`, per `project_prosoc_ci_black_pin` memory).
- `lrh validate` — 0 errors, 0 warnings.
- `git status` confirmed only the 6 intended files were staged before
  commit.

# Follow-up

- `WI-CARD-APPROVAL-PILOT` (the follow-on pilot item) depends on this WI
  and can now be implemented once this PR merges.
- The three skills are new and unexercised end-to-end against a real card
  promotion — the pilot WI's implementation will be the first real-world
  test of the full `prosoc-card-review` → `prosoc-card-approve` path.
- Next steps: wait for reviewer comments and run `/lrh-review-response`
  (repeat as needed), then `/lrh-confirm-fixes` before merge. After
  merging, run `/lrh-closeout` to land this record and resolve the work
  item.
